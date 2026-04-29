#!/usr/bin/env python3
"""
resolve_ids.py — 扫描 null ID，精确匹配 name_index，分配新 ID 并注册

用法:
  python scripts/resolve_ids.py output/kr/2026-04-28
  python scripts/resolve_ids.py output/kr/2026-04-28 --dry-run

功能:
  1. 读取 _name_index.json（精确查找表）
  2. 扫描 orgs/*.json 中 related_entities[].org_id 和 key_people[].person_id
  3. 扫描 persons/*.json 中 work_experience[].org_id 和 person_relationships[].person_id
  4. 精确匹配 name → 有则填 ID
  5. 无匹配 → 分配新 ID + 注册到 id_registry.json + 添加到 _name_index.json
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import glob
import tempfile

# org_type 映射：用于从组织名称推断 ID 前缀
ORG_TYPE_MAP = {
    "GOV": "GOV", "SOE": "SOE", "CORP": "CORP", "NGO": "NGO",
    "ACAD": "ACAD", "MEDIA": "MEDIA", "FIN": "FIN", "INTL": "INTL",
    "PARTY": "PARTY", "MIL": "MIL",
}


def load_json_safe(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


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


def get_next_org_id(registry, iso, org_type="GOV"):
    """获取下一个 org_id。格式: {ISO}-{TYPE}-{SEQ:03d}"""
    key = f"{iso}-{org_type}"
    counters = registry.get("counters", {})
    seq = counters.get(key, 0) + 1
    counters[key] = seq
    registry["counters"] = counters
    return f"{iso}-{org_type}-{seq:03d}"


def get_next_person_id(registry, iso):
    """获取下一个 person_id。格式: {ISO}-PERSON-{SEQ:06d}"""
    key = f"{iso}-PERSON"
    counters = registry.get("person_counters", {})
    seq = counters.get(key, 0) + 1
    counters[key] = seq
    registry["person_counters"] = counters
    return f"{iso}-PERSON-{seq:06d}"


def register_new_org(registry, index, iso, name, org_type="GOV"):
    """注册新组织到 registry 和 index。返回 org_id。"""
    org_id = get_next_org_id(registry, iso, org_type)
    entry = {
        "org_id": org_id,
        "name": name,
        "org_type": org_type,
        "status": "auto_registered",
    }
    registry.setdefault("registry", []).append(entry)
    index[name] = org_id
    return org_id


def register_new_person(registry, index, iso, name):
    """注册新人物到 registry 和 index。返回 person_id。"""
    person_id = get_next_person_id(registry, iso)
    entry = {
        "person_id": person_id,
        "name_en": name,
        "importance_level": "low",
        "org_ids": [],
    }
    registry.setdefault("person_registry", []).append(entry)
    index[name] = person_id
    return person_id


def resolve_orgs(output_dir, index, registry, iso, dry_run=False):
    """扫描 orgs/*.json，解析 null org_id 和 person_id。"""
    orgs_dir = os.path.join(output_dir, "orgs")
    if not os.path.isdir(orgs_dir):
        return 0, 0, 0

    filled_org = 0
    filled_person = 0
    new_registered = 0

    for fpath in glob.glob(os.path.join(orgs_dir, "*.json")):
        if os.path.basename(fpath).startswith("_"):
            continue
        profile = load_json_safe(fpath)
        if not profile:
            continue
        modified = False

        # related_entities[].org_id
        for ent in profile.get("related_entities", []):
            if ent.get("org_id"):
                continue
            name = ent.get("org_name", "").strip()
            if not name:
                continue
            if name in index:
                ent["org_id"] = index[name]
                filled_org += 1
                modified = True
            elif not dry_run:
                ent["org_id"] = register_new_org(registry, index, iso, name,
                                                  ent.get("org_type", "GOV"))
                new_registered += 1
                modified = True

        # key_people[].person_id
        for kp in profile.get("key_people", []):
            if kp.get("person_id"):
                continue
            name = kp.get("name", "").strip()
            if not name:
                continue
            if name in index:
                kp["person_id"] = index[name]
                filled_person += 1
                modified = True
            elif not dry_run:
                kp["person_id"] = register_new_person(registry, index, iso, name)
                new_registered += 1
                modified = True

        if modified and not dry_run:
            save_json_atomic(fpath, profile)

    return filled_org, filled_person, new_registered


def resolve_persons(output_dir, index, registry, iso, dry_run=False):
    """扫描 persons/*.json，解析 null org_id 和 person_id。"""
    persons_dir = os.path.join(output_dir, "persons")
    if not os.path.isdir(persons_dir):
        return 0, 0, 0

    filled_org = 0
    filled_person = 0
    new_registered = 0

    for fpath in glob.glob(os.path.join(persons_dir, "*.json")):
        if os.path.basename(fpath).startswith("_"):
            continue
        profile = load_json_safe(fpath)
        if not profile:
            continue
        modified = False

        # work_experience[].org_id
        for we in profile.get("work_experience", []):
            if we.get("org_id"):
                continue
            org_name = we.get("organization", "").strip()
            if not org_name:
                continue
            if org_name in index:
                we["org_id"] = index[org_name]
                filled_org += 1
                modified = True
            elif not dry_run:
                we["org_id"] = register_new_org(registry, index, iso, org_name, "GOV")
                new_registered += 1
                modified = True

        # person_relationships[].person_id
        for rel in profile.get("person_relationships", []):
            if rel.get("person_id"):
                continue
            name = rel.get("person_name", "").strip()
            if not name:
                continue
            if name in index:
                rel["person_id"] = index[name]
                filled_person += 1
                modified = True
            elif not dry_run:
                rel["person_id"] = register_new_person(registry, index, iso, name)
                new_registered += 1
                modified = True

        if modified and not dry_run:
            save_json_atomic(fpath, profile)

    return filled_org, filled_person, new_registered


def main():
    if len(sys.argv) < 2:
        print("Usage: python resolve_ids.py <output_dir> [--dry-run]")
        sys.exit(1)

    output_dir = sys.argv[1].rstrip("/\\")
    dry_run = "--dry-run" in sys.argv

    # 推断 ISO
    iso = os.path.basename(os.path.dirname(output_dir)).upper()
    if len(iso) != 2:
        iso = "KR"

    print(f"=== Resolving IDs for {output_dir} (ISO: {iso}) ===")
    if dry_run:
        print("  DRY RUN — no files will be modified")

    # 加载 index
    index_path = os.path.join(output_dir, "_name_index.json")
    if os.path.exists(index_path):
        index = load_json_safe(index_path)
        print(f"  Loaded name index: {len(index)} entries")
    else:
        index = {}
        print("  WARNING: _name_index.json not found, creating empty index")

    # 加载 registry
    registry_path = os.path.join(output_dir, "id_registry.json")
    registry = load_json_safe(registry_path) or {"registry": [], "counters": {},
                                                   "person_registry": [], "person_counters": {}}

    # 解析 orgs
    o_filled_o, o_filled_p, o_new = resolve_orgs(output_dir, index, registry, iso, dry_run)

    # 解析 persons
    p_filled_o, p_filled_p, p_new = resolve_persons(output_dir, index, registry, iso, dry_run)

    total_filled = o_filled_o + o_filled_p + p_filled_o + p_filled_p
    total_new = o_new + p_new

    if not dry_run:
        # 保存 registry
        save_json_atomic(registry_path, registry)
        # 保存 name_index
        save_json_atomic(index_path, index)

    print(f"\n=== Results ===")
    print(f"  IDs filled from index: {total_filled}")
    print(f"  New IDs allocated:     {total_new}")
    print(f"  Name index size:       {len(index)}")
    if dry_run:
        print("  (dry run — no changes written)")


if __name__ == "__main__":
    main()
