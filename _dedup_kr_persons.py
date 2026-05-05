#!/usr/bin/env python3
"""
_dedup_kr_persons.py — Merge duplicate KR person profiles and update all references.

For each (winner, loser) pair:
  1. Merge loser's content into winner (field by field)
  2. Convert loser file to a dedup marker
  3. Update all ID references across orgs, persons, id_registry, name_index, person_list
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import glob
import tempfile

BASE_DIR = "output/kr/2026-05-04"
PERSONS_DIR = os.path.join(BASE_DIR, "persons")
ORGS_DIR = os.path.join(BASE_DIR, "orgs")

# Duplicate pairs: (winner_num, loser_num)
DUPLICATE_PAIRS = [
    (1, 98),       # 이재명/Lee Jae Myung
    (2, 229),      # 김민석/Kim Min-seok
    (3, 33),       # 구윤철/Koo Yun-cheol
    (6, 128),      # 정동영/Chung Dong-young
    (7, 342),      # 정성호/Jeong Seong-ho
    (8, 293),      # 안규백/Ahn Gyu-back
    (9, 309),      # 윤호중/Yun Ho-jung
    (15, 232),     # 김성환/Kim Sung-hwan
    (20, 32),      # 한성숙/Han Seong-sook
    (21, 276),     # 박홍근/Park Hong-keun
    (38, 512),     # 김용현/Kim Yong-hyun
    (67, 94),      # 오경미/Oh Kyeong-mi
    (75, 95),      # 이숙연/Lee Sook-yeon
    (109, 150),    # 박지원/Park Ji-won
    (118, 489),    # 조광한/Cho Gwang-han
    (131, 422),    # 안철수/Ahn Cheol-soo
    (170, 466),    # 천하람/Chun Ha-ram
    (178, 504),    # 용혜인/Yong Hye-in
    (187, 518),    # 김재연/Kim Jae-yeon
    (188, 467),    # 윤종오/Yoon Jong-o
    (197, 468),    # 전종덕/Jeon Jong-deok
    (196, 469),    # 정혜경/Jeong Hye-kyung
    (210, 471),    # 우원식/Woo Won-shik
    (211, 216),    # 강선우/Kang Sun-woo
    (212, 470),    # 김종민/Kim Jong-min (1)
    (212, 246),    # 김종민/Kim Jong-min (2 — 3-way)
    (231, 510),    # 김병주/Kim Byung-joo
    (257, 265),    # 박범계/Park Beom-gye
    (213, 329),    # 이춘석/Lee Chun-seok
    (376, 476),    # 권영진/Kwon Young-jin
    (398, 487),    # 김태호/Kim Tae-ho
    (465, 514),    # 이주영/Lee Ju-young
    (111, 112),    # Q13064531 — verify same person
]


def person_id(num):
    return f"KR-PERSON-{num:06d}"


def person_path(num):
    return os.path.join(PERSONS_DIR, f"KR-PERSON-{num:06d}.json")


def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def save_json_atomic(path, data):
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dir_path, prefix=".tmp_", suffix=os.path.basename(path), text=True)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def merge_list_field(winner_list, loser_list, dedup_key_fn):
    """Merge two lists, deduping by key function. Loser items appended if not duplicate."""
    if not loser_list:
        return winner_list or []
    if not winner_list:
        return loser_list
    existing_keys = set()
    for item in winner_list:
        key = dedup_key_fn(item)
        if key:
            existing_keys.add(key)
    result = list(winner_list)
    for item in loser_list:
        key = dedup_key_fn(item)
        if key and key not in existing_keys:
            result.append(item)
            existing_keys.add(key)
        elif not key:
            result.append(item)
    return result


def merge_person_profiles(winner, loser, winner_num, loser_num):
    """Merge loser's content into winner. Returns merged winner profile."""
    winner_id = person_id(winner_num)
    loser_id = person_id(loser_num)

    # biography_summary: keep the longer one
    w_bio = winner.get("biography_summary") or ""
    l_bio = loser.get("biography_summary") or ""
    if len(l_bio) > len(w_bio):
        winner["biography_summary"] = l_bio

    # birth_place: keep the more detailed one
    w_bp = winner.get("birth_place") or ""
    l_bp = loser.get("birth_place") or ""
    if len(l_bp) > len(w_bp):
        winner["birth_place"] = l_bp

    # aliases: merge sets
    w_aliases = set(winner.get("aliases") or [])
    l_aliases = set(loser.get("aliases") or [])
    winner["aliases"] = sorted(w_aliases | l_aliases)

    # current_positions: merge, normalize str/dict
    def normalize_cp(item):
        if isinstance(item, str):
            return item.strip()
        if isinstance(item, dict):
            return (item.get("position", "") or "").strip()
        return str(item).strip()

    w_cp = winner.get("current_positions") or []
    l_cp = loser.get("current_positions") or []
    seen = set()
    merged_cp = []
    for item in w_cp + l_cp:
        key = normalize_cp(item)
        if key not in seen:
            merged_cp.append(item)
            seen.add(key)
    winner["current_positions"] = merged_cp

    # work_experience: merge by (position + organization)
    winner["work_experience"] = merge_list_field(
        winner.get("work_experience") or [],
        loser.get("work_experience") or [],
        lambda x: (x.get("position", "") or "").strip().lower() + "|" + (x.get("organization", "") or "").strip().lower()
    )

    # education: merge by institution
    winner["education"] = merge_list_field(
        winner.get("education") or [],
        loser.get("education") or [],
        lambda x: (x.get("institution", "") or "").strip().lower()
    )

    # political_stances: merge by topic
    winner["political_stances"] = merge_list_field(
        winner.get("political_stances") or [],
        loser.get("political_stances") or [],
        lambda x: (x.get("topic", "") or "").strip().lower()
    )

    # person_relationships: merge by person_name, but remap loser's self-reference
    loser_rels = []
    for rel in (loser.get("person_relationships") or []):
        r = dict(rel)
        # Fix: if loser references itself, point to winner
        if r.get("person_id") == loser_id:
            r["person_id"] = winner_id
        # Fix: if loser has self-reference by content (same person diff entry)
        if r.get("relationship_type") == "other" and loser_id in (r.get("person_id") or ""):
            continue  # skip self-reference
        loser_rels.append(r)
    winner["person_relationships"] = merge_list_field(
        winner.get("person_relationships") or [],
        loser_rels,
        lambda x: (x.get("person_name", "") or "").strip().lower()
    )

    # social_accounts: merge by url
    winner["social_accounts"] = merge_list_field(
        winner.get("social_accounts") or [],
        loser.get("social_accounts") or [],
        lambda x: (x.get("url", "") or "").strip().lower().rstrip("/")
    )

    # family_members: merge by name
    winner["family_members"] = merge_list_field(
        winner.get("family_members") or [],
        loser.get("family_members") or [],
        lambda x: (x.get("name", "") or "").strip().lower()
    )

    # major_achievements: merge by achievement text (first 60 chars as key)
    winner["major_achievements"] = merge_list_field(
        winner.get("major_achievements") or [],
        loser.get("major_achievements") or [],
        lambda x: (x.get("achievement", "") or "").strip().lower()[:60]
    )

    # contacts: merge by value
    winner["contacts"] = merge_list_field(
        winner.get("contacts") or [],
        loser.get("contacts") or [],
        lambda x: (x.get("value", "") or "").strip().lower().rstrip("/")
    )

    # collection_meta: update completeness_score, merge data_sources, merge quotes
    w_meta = winner.get("collection_meta", {})
    l_meta = loser.get("collection_meta", {})
    w_meta["completeness_score"] = max(
        w_meta.get("completeness_score", 0),
        l_meta.get("completeness_score", 0)
    )
    # Merge data_sources
    w_ds = set(w_meta.get("data_sources") or [])
    l_ds = set(l_meta.get("data_sources") or [])
    w_meta["data_sources"] = sorted(w_ds | l_ds)
    # Merge quotes by url
    w_meta["quotes"] = merge_list_field(
        w_meta.get("quotes") or [],
        l_meta.get("quotes") or [],
        lambda x: (x.get("url", "") or "").strip()
    )
    # Merge notes
    w_notes = w_meta.get("notes") or ""
    l_notes = l_meta.get("notes") or ""
    if l_notes and l_notes not in w_notes:
        w_meta["notes"] = (w_notes + "\n" + l_notes).strip() if w_notes else l_notes
    winner["collection_meta"] = w_meta

    return winner


def make_dedup_marker(loser_num, winner_num, loser_data):
    """Create a minimal dedup marker for the loser."""
    loser_id = person_id(loser_num)
    winner_id = person_id(winner_num)
    return {
        "person_id": loser_id,
        "name_zh": loser_data.get("name_zh", ""),
        "name": loser_data.get("name", ""),
        "name_en": loser_data.get("name_en", ""),
        "nationality": "KR",
        "gender": loser_data.get("gender", "unknown"),
        "biography_summary": f"此条目为 {winner_id} 的重复条目。",
        "duplicate_of": winner_id,
        "collection_meta": {
            "phase": "duplicate",
            "completeness_score": 6
        }
    }


def update_org_references(loser_num, winner_num):
    """Update person_id references in orgs/*.json from loser → winner."""
    loser_id = person_id(loser_num)
    winner_id = person_id(winner_num)
    updated = 0

    for fpath in glob.glob(os.path.join(ORGS_DIR, "*.json")):
        if os.path.basename(fpath).startswith("_"):
            continue
        data = load_json(fpath)
        modified = False

        for kp in data.get("key_people", []):
            if kp.get("person_id") == loser_id:
                kp["person_id"] = winner_id
                modified = True
                updated += 1

        if modified:
            save_json_atomic(fpath, data)

    return updated


def update_person_references(loser_num, winner_num):
    """Update person_id references in persons/*.json from loser → winner."""
    loser_id = person_id(loser_num)
    winner_id = person_id(winner_num)
    updated = 0

    for fpath in glob.glob(os.path.join(PERSONS_DIR, "*.json")):
        if os.path.basename(fpath).startswith("_"):
            continue
        fname = os.path.basename(fpath)
        # Skip the loser's own file (it's now a dedup marker)
        if fname == f"KR-PERSON-{loser_num:06d}.json":
            continue

        data = load_json(fpath)
        modified = False

        for rel in data.get("person_relationships", []):
            if rel.get("person_id") == loser_id:
                rel["person_id"] = winner_id
                modified = True
                updated += 1

        for fm in data.get("family_members", []):
            if fm.get("person_id") == loser_id:
                fm["person_id"] = winner_id
                modified = True
                updated += 1

        if modified:
            save_json_atomic(fpath, data)

    return updated


def update_id_registry(loser_nums):
    """Remove loser entries from id_registry.json."""
    reg_path = os.path.join(BASE_DIR, "id_registry.json")
    reg = load_json(reg_path)
    loser_ids = {person_id(n) for n in loser_nums}

    before = len(reg.get("person_registry", []))
    reg["person_registry"] = [
        p for p in reg.get("person_registry", [])
        if p.get("person_id") not in loser_ids
    ]
    after = len(reg["person_registry"])

    save_json_atomic(reg_path, reg)
    return before - after


def update_person_list(loser_nums):
    """Remove loser entries from person_list.json."""
    pl_path = os.path.join(BASE_DIR, "person_list.json")
    if not os.path.exists(pl_path):
        return 0
    pl = load_json(pl_path)
    loser_ids = {person_id(n) for n in loser_nums}

    before = len(pl.get("persons", []))
    pl["persons"] = [
        p for p in pl.get("persons", [])
        if p.get("person_id") not in loser_ids
    ]
    after = len(pl["persons"])

    # Update metadata
    if "metadata" in pl:
        pl["metadata"]["total_persons"] = after

    # Update summary
    if "summary" in pl and "data_quality" in pl["summary"]:
        pl["summary"]["data_quality"]["with_person_id"] = after

    save_json_atomic(pl_path, pl)
    return before - after


def update_name_index(loser_nums, winner_nums):
    """Update _name_index.json to point loser name entries to winner IDs."""
    ni_path = os.path.join(BASE_DIR, "_name_index.json")
    if not os.path.exists(ni_path):
        return 0

    ni = load_json(ni_path)
    loser_to_winner = {}
    for w, l in zip(winner_nums, loser_nums):
        loser_to_winner[person_id(l)] = person_id(w)

    updated = 0
    for name, pid in ni.items():
        if pid in loser_to_winner:
            ni[name] = loser_to_winner[pid]
            updated += 1

    save_json_atomic(ni_path, ni)
    return updated


def main():
    print("=" * 60)
    print("KR Person Deduplication")
    print("=" * 60)

    winner_nums = [w for w, l in DUPLICATE_PAIRS]
    loser_nums = [l for w, l in DUPLICATE_PAIRS]

    # Verify loser files exist and are not already dedup markers
    print(f"\nVerifying {len(DUPLICATE_PAIRS)} duplicate pairs...")
    for w, l in DUPLICATE_PAIRS:
        wp = person_path(w)
        lp = person_path(l)
        if not os.path.exists(wp):
            print(f"  ERROR: Winner file missing: {wp}")
            return
        if not os.path.exists(lp):
            print(f"  WARNING: Loser file missing (already dedup?): {lp}")
            continue
        loser_data = load_json(lp)
        if loser_data.get("duplicate_of"):
            print(f"  SKIP: {person_id(l)} already a dedup marker → {loser_data['duplicate_of']}")
            continue

    # Step 1: Merge content
    print(f"\n--- Step 1: Merging content ({len(DUPLICATE_PAIRS)} pairs) ---")
    merged_count = 0
    for w, l in DUPLICATE_PAIRS:
        wp = person_path(w)
        lp = person_path(l)

        if not os.path.exists(lp):
            print(f"  SKIP {person_id(l)}: file not found")
            continue

        loser_data = load_json(lp)
        if loser_data.get("duplicate_of"):
            print(f"  SKIP {person_id(l)}: already dedup marker")
            continue

        winner_data = load_json(wp)

        w_score = winner_data.get("collection_meta", {}).get("completeness_score", 0)
        l_score = loser_data.get("collection_meta", {}).get("completeness_score", 0)
        print(f"  Merge {person_id(l)} (score={l_score}) → {person_id(w)} (score={w_score})")

        # Merge content
        merged = merge_person_profiles(winner_data, loser_data, w, l)
        save_json_atomic(wp, merged)

        # Convert loser to dedup marker
        marker = make_dedup_marker(l, w, loser_data)
        save_json_atomic(lp, marker)

        merged_count += 1

    print(f"  Merged {merged_count} pairs")

    # Step 2: Update ID references
    print(f"\n--- Step 2: Updating ID references ---")
    total_org_refs = 0
    total_person_refs = 0

    for w, l in DUPLICATE_PAIRS:
        if not os.path.exists(person_path(l)):
            continue
        loser_data = load_json(person_path(l))
        if not loser_data.get("duplicate_of"):
            continue

        org_refs = update_org_references(l, w)
        person_refs = update_person_references(l, w)
        total_org_refs += org_refs
        total_person_refs += person_refs
        if org_refs or person_refs:
            print(f"  {person_id(l)} → {person_id(w)}: {org_refs} org refs, {person_refs} person refs")

    print(f"  Total: {total_org_refs} org refs, {total_person_refs} person refs")

    # Step 3: Update registry and indexes
    print(f"\n--- Step 3: Updating registry and indexes ---")
    active_losers = []
    for w, l in DUPLICATE_PAIRS:
        lp = person_path(l)
        if os.path.exists(lp):
            d = load_json(lp)
            if d.get("duplicate_of"):
                active_losers.append(l)

    reg_removed = update_id_registry(active_losers)
    print(f"  id_registry.json: removed {reg_removed} entries")

    pl_removed = update_person_list(active_losers)
    print(f"  person_list.json: removed {pl_removed} entries")

    ni_updated = update_name_index(
        [w for w, l in DUPLICATE_PAIRS if l in active_losers],
        active_losers
    )
    print(f"  _name_index.json: updated {ni_updated} entries")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"DONE: Merged {merged_count} duplicate pairs")
    print(f"  Org references updated: {total_org_refs}")
    print(f"  Person references updated: {total_person_refs}")
    print(f"  Registry entries removed: {reg_removed}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
