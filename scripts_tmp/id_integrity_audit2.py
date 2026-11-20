# -*- coding: utf-8 -*-
"""Global ID-reference integrity audit v2 (normalization-aware).

Improvements over v1:
  - zhconv traditional->simplified
  - honorific/title stripping (Sheikh/Sultan/Sir/Dr/苏丹/谢赫/...)
  - token-subset matching (Donald Trump vs Donald J. Trump)
  - CJK containment for truncated names (最高石油委员会 ⊂ 阿布扎比最高石油委员会)
  - every bad ref classified: target_elsewhere_unique / ambiguous / absent
  - emits repair_candidates.json for later mechanical repair

Directions:
  A person.work_experience.org_id -> org
  B person.person_relationships.person_id -> person
  C person.family_members.person_id -> person
  D org.key_people.person_id -> person
  E org.related_entities.org_id -> org

Usage: python scripts_tmp/id_integrity_audit2.py
"""
import glob
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict

import zhconv

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
OUT = os.path.join(BASE, "output", "_id_audit")

CJK = re.compile(r"[\u4e00-\u9fff]")
PAREN = re.compile(r"[（(]([^）)]*)[）)]")
SUFFIXES = [
    "incorporated", "inc", "corporation", "corp", "company", "co", "limited",
    "ltd", "llc", "plc", "gmbh", "ag", "sa", "nv", "bv", "holding", "holdings",
    "group", "公司", "集团", "股份有限公司", "有限公司", "株式会社", "控股",
]
TITLES = {
    "mr", "mrs", "ms", "miss", "dr", "prof", "professor", "sir", "dame", "hon",
    "sheikh", "sheik", "sheikha", "shaykh", "sultan", "prince", "princess",
    "king", "queen", "president", "senator", "governor", "general", "admiral",
    "h.e", "he", "his", "her", "highness", "majesty", "lord", "lady", "eng",
    "saint", "st", "rev", "capt", "col", "lt", "gen", "amb", "judge",
}
CN_TITLES = ["苏丹", "谢赫", "殿下", "博士", "教授", "先生", "女士", "爵士",
             "总统", "部长", "亲王", "王子", "公主", "阁下", "大使", "将军"]


def _clean(s):
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return zhconv.convert(s, "zh-cn")


def norm(s):
    s = _clean(s).lower()
    return re.sub(r"[\s\.\,\-\'’`&·:：/\\|]+", "", s)


def words(s):
    s = _clean(s).lower()
    s = re.sub(r"[\.\,\-\'’`&·:：/\\|]+", " ", s)
    toks = [t for t in s.split() if t and t not in TITLES]
    if toks and toks[0] == "the":
        toks = toks[1:]
    if toks:
        for t in CN_TITLES:
            if toks[0] == t:
                toks = toks[1:]
                break
            if toks[0].startswith(t) and len(toks[0]) > len(t):
                toks[0] = toks[0][len(t):]
                break
    return toks


def sig(s):
    """Return (compacts:set, tokens:list[frozenset])."""
    if not s:
        return set(), []
    parts = PAREN.findall(str(s))
    outside = PAREN.sub(" ", str(s))
    pieces = []
    for c in [outside] + parts:
        pieces += re.split(r"[/、;；]", c)
    compacts = set()
    tokens = []
    for c in pieces:
        n = norm(c)
        if n:
            compacts.add(n)
            for suf in SUFFIXES:
                if n.endswith(suf) and len(n) > len(suf) + 1:
                    compacts.add(n[: -len(suf)])
        t = words(c)
        if t:
            tokens.append(frozenset(t))
    return compacts, tokens


def sig_union(values):
    compacts, tokens = set(), []
    for v in values:
        c, t = sig(v)
        compacts |= c
        tokens += t
    return compacts, tokens


def ref_name(item, keys):
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def match(a, b):
    """Strong name match between two sig objects."""
    ac, at = a
    bc, bt = b
    if ac & bc:
        return True
    for x in ac:
        for y in bc:
            if len(x) >= 5 and len(y) >= 5 and (x in y or y in x):
                return True
    for x in at:
        for y in bt:
            if len(x) >= 2 and len(y) >= 2 and (x <= y or y <= x):
                return True
    return False


def person_sig(d):
    keys = ["name", "name_en", "name_zh", "name_native", "name_original",
            "name_local", "name_th", "name_ms", "name_ja", "name_kr", "name_km"]
    vals = [d.get(k) for k in keys]
    vals += d.get("aliases") or []
    return sig_union(vals)


def org_sig(d):
    bi = d.get("basic_info") or {}
    keys = ["name_zh", "name_en", "name_original", "name", "name_local",
            "name_ru", "name_ky", "short_name"]
    vals = [bi.get(k) for k in keys]
    vals += bi.get("aliases") or []
    vals += bi.get("former_names") or []
    return sig_union(vals)


def load_datasets():
    by_cc = defaultdict(list)
    for p in glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*")):
        rel = os.path.relpath(p, BASE).replace(os.sep, "/").split("/")
        by_cc[rel[1]].append((rel[2], p))
    latest, older = {}, []
    for cc, items in by_cc.items():
        items.sort()
        latest[cc] = items[-1]
        for date, p in items[:-1]:
            older.append((cc, date, p))
    return latest, older


def save_json(f, d):
    with open(f, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=1)


def main():
    os.makedirs(OUT, exist_ok=True)
    latest, older = load_datasets()

    persons, orgs = {}, {}
    per_dataset = {}
    id_issues = {"filename_mismatch": [], "load_errors": []}

    for cc, (date, folder) in sorted(latest.items()):
        per_dataset[cc] = {"date": date, "persons": 0, "orgs": 0}
        for f in sorted(glob.glob(os.path.join(folder, "persons", "*.json"))):
            bn = os.path.basename(f)
            if bn.startswith("_"):
                continue
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception as e:
                id_issues["load_errors"].append([f, str(e)])
                continue
            pid = d.get("person_id")
            if pid != bn[:-5]:
                id_issues["filename_mismatch"].append([f, pid, bn[:-5]])
            persons[pid] = {"cc": cc, "file": f, "d": d, "sig": person_sig(d)}
            per_dataset[cc]["persons"] += 1
        for f in sorted(glob.glob(os.path.join(folder, "orgs", "*.json"))):
            bn = os.path.basename(f)
            if bn.startswith("_"):
                continue
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception as e:
                id_issues["load_errors"].append([f, str(e)])
                continue
            oid = d.get("org_id")
            if oid != bn[:-5]:
                id_issues["filename_mismatch"].append([f, oid, bn[:-5]])
            orgs[oid] = {"cc": cc, "file": f, "d": d, "sig": org_sig(d)}
            per_dataset[cc]["orgs"] += 1

    # duplicate wikidata qids
    qid_person = defaultdict(list)
    qid_org = defaultdict(list)
    for pid, r in persons.items():
        q = (r["d"].get("wikidata_qid") or "").strip()
        if q:
            qid_person[q].append([pid, r["cc"], r["d"].get("name"), r["d"].get("name_zh")])
    for oid, r in orgs.items():
        q = ((r["d"].get("basic_info") or {}).get("wikidata_qid") or "").strip()
        if q:
            qid_org[q].append([oid, r["cc"],
                               (r["d"].get("basic_info") or {}).get("name_original")])
    dup_qid_person = [v for v in qid_person.values() if len(v) > 1]
    dup_qid_org = [v for v in qid_org.values() if len(v) > 1]

    # name indexes
    p_compact = defaultdict(set)
    p_token = defaultdict(set)
    for pid, r in persons.items():
        c, t = r["sig"]
        for x in c:
            p_compact[x].add(pid)
        for ts in t:
            for tok in ts:
                if len(tok) >= 4:
                    p_token[tok].add(pid)

    orgs_by_cc = defaultdict(list)
    o_compact = defaultdict(set)
    o_token = defaultdict(set)
    for oid, r in orgs.items():
        orgs_by_cc[r["cc"]].append(oid)
        c, t = r["sig"]
        for x in c:
            o_compact[x].add(oid)
        for ts in t:
            for tok in ts:
                if len(tok) >= 4:
                    o_token[tok].add(oid)

    def find_org(name, cc, global_fallback=True):
        rs = sig(name)
        hits = [oid for oid in orgs_by_cc.get(cc, []) if match(rs, orgs[oid]["sig"])]
        scope = "same_cc"
        if not hits and global_fallback:
            cands = set()
            for x in rs[0]:
                cands |= o_compact.get(x, set())
            if not cands and rs[1]:
                sets = [o_token[t] for t in {t for ts in rs[1] for t in ts} if len(t) >= 4]
                if sets:
                    cands = set.intersection(*sets) if len(sets) > 1 else set(sets[0])
                    if len(cands) > 2000:
                        cands = set()
            hits = [oid for oid in cands if match(rs, orgs[oid]["sig"])]
            scope = "global"
        uniq = sorted(set(hits))
        if len(uniq) == 1:
            return uniq[0], "unique", scope
        if len(uniq) > 1:
            return None, f"ambiguous({len(uniq)})", scope
        return None, "absent", scope

    def find_person(name, prefer_cc):
        rs = sig(name)
        cands = set()
        for x in rs[0]:
            cands |= p_compact.get(x, set())
        if not cands and rs[1]:
            sets = [p_token[t] for t in {t for ts in rs[1] for t in ts} if len(t) >= 4]
            if sets:
                cands = set.intersection(*sets) if len(sets) > 1 else set(sets[0])
                if len(cands) > 2000:
                    cands = set()
        hits = [pid for pid in cands if match(rs, persons[pid]["sig"])]
        if len(hits) > 1:
            same = [pid for pid in hits if persons[pid]["cc"] == prefer_cc]
            if len(same) >= 1:
                hits = same
        uniq = sorted(set(hits))
        if len(uniq) == 1:
            return uniq[0], "unique"
        if len(uniq) > 1:
            return None, f"ambiguous({len(uniq)})"
        return None, "absent"

    # ---------------- audit ----------------
    t0 = time.time()
    print(f"[load] persons={len(persons)} orgs={len(orgs)} ({time.time()-t0:.1f}s)", flush=True)
    audit = {}
    repair = {"work_org": [], "person_rel": [], "family": [], "key_people": [],
              "related_org": []}

    def new_bucket(with_names=True):
        b = {"total": 0, "filled": 0, "null_id": 0, "ok": 0, "wrong_target": 0,
             "dangling": 0}
        if with_names:
            b.update({"bad_fixable_unique": 0, "bad_fixable_ambiguous": 0,
                      "bad_target_absent": 0,
                      "null_resolvable": 0, "null_ambiguous": 0,
                      "null_notfound": 0, "samples": []})
        return b

    for k in ("work_org", "person_rel", "family", "key_people", "related_org"):
        audit[k] = new_bucket()
    per_cc = defaultdict(lambda: defaultdict(Counter))

    def add_sample(bucket, row):
        if len(audit[bucket]["samples"]) < 60:
            audit[bucket]["samples"].append(row)

    # A person -> org
    for pid, r in persons.items():
        cc, d = r["cc"], r["d"]
        for w in d.get("work_experience") or []:
            if not isinstance(w, dict):
                continue
            a = audit["work_org"]
            a["total"] += 1
            per_cc[cc]["work_org"]["total"] += 1
            j = w.get("org_id")
            name = ref_name(w, ["organization", "org_name", "organization_en"])
            if not j:
                a["null_id"] += 1
                per_cc[cc]["work_org"]["null_id"] += 1
                continue
            a["filled"] += 1
            if j in orgs and match(sig(name), orgs[j]["sig"]):
                a["ok"] += 1
                continue
            if j in orgs:
                a["wrong_target"] += 1
                per_cc[cc]["work_org"]["wrong_target"] += 1
                kind = "wrong_target"
            else:
                a["dangling"] += 1
                per_cc[cc]["work_org"]["dangling"] += 1
                kind = "dangling"
            sug, st, scope = find_org(name, cc)
            if st == "unique":
                a["bad_fixable_unique"] += 1
                per_cc[cc]["work_org"]["fixable"] += 1
                action = "replace"
            elif st.startswith("ambiguous"):
                a["bad_fixable_ambiguous"] += 1
                per_cc[cc]["work_org"]["ambiguous"] += 1
                action = "review"
            else:
                a["bad_target_absent"] += 1
                per_cc[cc]["work_org"]["absent"] += 1
                action = "null_id"
            row = {"cc": cc, "person_id": pid, "person": d.get("name"),
                   "org_id": j, "organization": name, "issue": kind,
                   "suggested": sug, "suggest_status": st, "scope": scope,
                   "action": action,
                   "target": ((orgs[j]["d"].get("basic_info") or {}).get("name_zh")
                              if j in orgs else None)}
            add_sample("work_org", row)
            if len(repair["work_org"]) < 40000:
                repair["work_org"].append(row)

    # B/C person -> person
    print(f"[A done] work_org ({time.time()-t0:.1f}s)", flush=True)
    for i, (pid, r) in enumerate(persons.items()):
        cc, d = r["cc"], r["d"]
        for arr, bucket, nk in [("person_relationships", "person_rel", ["person_name", "name"]),
                                ("family_members", "family", ["name", "person_name"])]:
            for rel in d.get(arr) or []:
                if not isinstance(rel, dict):
                    continue
                a = audit[bucket]
                a["total"] += 1
                per_cc[cc][bucket]["total"] += 1
                j = rel.get("person_id")
                name = ref_name(rel, nk)
                if not j:
                    a["null_id"] += 1
                    per_cc[cc][bucket]["null_id"] += 1
                    sug, st = find_person(name, cc)
                    if st == "unique":
                        a["null_resolvable"] += 1
                        per_cc[cc][bucket]["null_resolvable"] += 1
                        repair[bucket].append({"cc": cc, "person_id": pid,
                                               "person": d.get("name"), "ref_name": name,
                                               "current": None, "suggested": sug,
                                               "issue": "null_id", "action": "fill"})
                    elif st.startswith("ambiguous"):
                        a["null_ambiguous"] += 1
                    else:
                        a["null_notfound"] += 1
                    continue
                a["filled"] += 1
                if j in persons and match(sig(name), persons[j]["sig"]):
                    a["ok"] += 1
                    continue
                if j in persons:
                    a["wrong_target"] += 1
                    per_cc[cc][bucket]["wrong_target"] += 1
                    kind = "wrong_target"
                else:
                    a["dangling"] += 1
                    per_cc[cc][bucket]["dangling"] += 1
                    kind = "dangling"
                sug, st = find_person(name, cc)
                if st == "unique":
                    a["bad_fixable_unique"] += 1
                    per_cc[cc][bucket]["fixable"] += 1
                    action = "replace"
                elif st.startswith("ambiguous"):
                    a["bad_fixable_ambiguous"] += 1
                    per_cc[cc][bucket]["ambiguous"] += 1
                    action = "review"
                else:
                    a["bad_target_absent"] += 1
                    per_cc[cc][bucket]["absent"] += 1
                    action = "null_id"
                row = {"cc": cc, "person_id": pid, "person": d.get("name"),
                       "ref_name": name, "person_id_ref": j, "issue": kind,
                       "suggested": sug, "suggest_status": st, "action": action,
                       "target": (persons[j]["d"].get("name") if j in persons else None)}
                add_sample(bucket, row)
                if len(repair[bucket]) < 40000:
                    repair[bucket].append(row)

    # D org -> person
    print(f"[B/C done] person refs ({time.time()-t0:.1f}s)", flush=True)
    for oid, r in orgs.items():
        cc, d = r["cc"], r["d"]
        for kp in d.get("key_people") or []:
            if not isinstance(kp, dict):
                continue
            a = audit["key_people"]
            a["total"] += 1
            per_cc[cc]["key_people"]["total"] += 1
            j = kp.get("person_id")
            name = ref_name(kp, ["name", "name_en"])
            if not j:
                a["null_id"] += 1
                per_cc[cc]["key_people"]["null_id"] += 1
                continue
            a["filled"] += 1
            if j in persons and match(sig(name), persons[j]["sig"]):
                a["ok"] += 1
                continue
            if j in persons:
                a["wrong_target"] += 1
                per_cc[cc]["key_people"]["wrong_target"] += 1
                kind = "wrong_target"
            else:
                a["dangling"] += 1
                per_cc[cc]["key_people"]["dangling"] += 1
                kind = "dangling"
            sug, st = find_person(name, cc)
            if st == "unique":
                a["bad_fixable_unique"] += 1
                per_cc[cc]["key_people"]["fixable"] += 1
                action = "replace"
            elif st.startswith("ambiguous"):
                a["bad_fixable_ambiguous"] += 1
                per_cc[cc]["key_people"]["ambiguous"] += 1
                action = "review"
            else:
                a["bad_target_absent"] += 1
                per_cc[cc]["key_people"]["absent"] += 1
                action = "null_id"
            row = {"cc": cc, "org_id": oid,
                   "org": (d.get("basic_info") or {}).get("name_zh"),
                   "ref_name": name, "person_id_ref": j, "issue": kind,
                   "suggested": sug, "suggest_status": st, "action": action,
                   "target": (persons[j]["d"].get("name") if j in persons else None)}
            add_sample("key_people", row)
            if len(repair["key_people"]) < 40000:
                repair["key_people"].append(row)

    # E org -> org
    print(f"[D done] key_people ({time.time()-t0:.1f}s)", flush=True)
    for oid, r in orgs.items():
        cc, d = r["cc"], r["d"]
        for re_ in d.get("related_entities") or []:
            if not isinstance(re_, dict):
                continue
            a = audit["related_org"]
            a["total"] += 1
            per_cc[cc]["related_org"]["total"] += 1
            j = re_.get("org_id")
            name = ref_name(re_, ["org_name", "name"])
            if not j:
                a["null_id"] += 1
                per_cc[cc]["related_org"]["null_id"] += 1
                continue
            a["filled"] += 1
            if j in orgs and match(sig(name), orgs[j]["sig"]):
                a["ok"] += 1
                continue
            if j in orgs:
                a["wrong_target"] += 1
                per_cc[cc]["related_org"]["wrong_target"] += 1
                kind = "wrong_target"
            else:
                a["dangling"] += 1
                per_cc[cc]["related_org"]["dangling"] += 1
                kind = "dangling"
            sug, st, scope = find_org(name, cc)
            if st == "unique":
                a["bad_fixable_unique"] += 1
                per_cc[cc]["related_org"]["fixable"] += 1
                action = "replace"
            elif st.startswith("ambiguous"):
                a["bad_fixable_ambiguous"] += 1
                per_cc[cc]["related_org"]["ambiguous"] += 1
                action = "review"
            else:
                a["bad_target_absent"] += 1
                per_cc[cc]["related_org"]["absent"] += 1
                action = "null_id"
            row = {"cc": cc, "org_id": oid,
                   "org": (d.get("basic_info") or {}).get("name_zh"),
                   "ref_name": name, "org_id_ref": j, "issue": kind,
                   "suggested": sug, "suggest_status": st, "scope": scope,
                   "action": action,
                   "target": ((orgs[j]["d"].get("basic_info") or {}).get("name_zh")
                              if j in orgs else None)}
            add_sample("related_org", row)
            if len(repair["related_org"]) < 40000:
                repair["related_org"].append(row)

    # departments quick stats
    print(f"[E done] related_org ({time.time()-t0:.1f}s)", flush=True)
    dep = {"total": 0, "null_parent": 0, "dangling": 0, "self": 0, "ok": 0}
    for oid, r in orgs.items():
        deps = [x for x in (r["d"].get("departments") or []) if isinstance(x, dict)]
        ids = {x.get("dept_id") for x in deps if x.get("dept_id")}
        for x in deps:
            dep["total"] += 1
            par = x.get("parent_dept_id")
            if not par:
                dep["null_parent"] += 1
            elif par == x.get("dept_id"):
                dep["self"] += 1
            elif par not in ids:
                dep["dangling"] += 1
            else:
                dep["ok"] += 1

    # index consistency
    idx = {"person_missing_file": 0, "person_id_mismatch": 0, "person_dup": 0,
           "persons_not_in_index": 0, "org_missing_file": 0, "org_dup": 0,
           "org_name_mismatch": 0, "orgs_not_in_index": 0, "details": []}
    for cc, (date, folder) in sorted(latest.items()):
        pfolder = os.path.join(folder, "persons")
        pfiles = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(pfolder, "*.json"))
                  if not os.path.basename(p).startswith("_")}
        pidx = os.path.join(pfolder, "_index.json")
        if os.path.exists(pidx):
            d = json.load(open(pidx, encoding="utf-8"))
            seen = Counter()
            for p in d.get("profiles") or []:
                pid = p.get("person_id")
                seen[pid] += 1
                if pid not in pfiles:
                    idx["person_missing_file"] += 1
                    idx["details"].append([cc, "person_missing_file", pid])
                if pid not in persons:
                    idx["person_id_mismatch"] += 1
                    idx["details"].append([cc, "person_id_mismatch", pid])
            for pid, n in seen.items():
                if n > 1:
                    idx["person_dup"] += 1
                    idx["details"].append([cc, "person_dup", pid, n])
            idx["persons_not_in_index"] += len(pfiles - set(seen))
        ofolder = os.path.join(folder, "orgs")
        ofiles = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(ofolder, "*.json"))
                  if not os.path.basename(p).startswith("_")}
        oidx = os.path.join(ofolder, "_index.json")
        if os.path.exists(oidx):
            d = json.load(open(oidx, encoding="utf-8"))
            seen = Counter()
            for p in d.get("profiles") or []:
                oid = p.get("org_id")
                seen[oid] += 1
                if oid not in ofiles:
                    idx["org_missing_file"] += 1
                elif oid in orgs:
                    if not match(sig(p.get("name")), orgs[oid]["sig"]):
                        idx["org_name_mismatch"] += 1
                        idx["details"].append([cc, "org_name_mismatch", oid,
                                               p.get("name"),
                                               (orgs[oid]["d"].get("basic_info") or {}).get("name_zh")])
            for oid, n in seen.items():
                if n > 1:
                    idx["org_dup"] += 1
            idx["orgs_not_in_index"] += len(ofiles - set(seen))

    # dangling ID ranges (org) per country
    dangling_org_ids = defaultdict(Counter)
    for row in repair["work_org"]:
        if row["issue"] == "dangling":
            dangling_org_ids[row["cc"]][row["org_id"]] += 1
    dangling_org_ids = {cc: dict(c) for cc, c in dangling_org_ids.items()}

    # old datasets
    older_info = {}
    for cc, date, folder in older:
        oldp = {}
        for f in glob.glob(os.path.join(folder, "persons", "*.json")):
            bn = os.path.basename(f)
            if bn.startswith("_"):
                continue
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            oldp[d.get("person_id")] = d.get("name")
        older_info[f"{cc}/{date}"] = {
            "persons": len(oldp),
            "overlap_latest": len(set(oldp) & set(persons)),
            "same_id_diff_name": sum(1 for k, v in oldp.items()
                                     if k in persons and persons[k]["d"].get("name") != v),
        }

    report = {
        "generated_at": "2026-11-13",
        "totals": {"persons": len(persons), "orgs": len(orgs),
                   "countries": len(latest)},
        "references": audit,
        "departments": dep,
        "duplicate_wikidata": {"persons": len(dup_qid_person),
                               "orgs": len(dup_qid_org),
                               "person_samples": dup_qid_person[:30],
                               "org_samples": dup_qid_org[:30]},
        "id_integrity": {"filename_mismatch": len(id_issues["filename_mismatch"]),
                         "load_errors": len(id_issues["load_errors"]),
                         "samples": id_issues["filename_mismatch"][:20]},
        "index": idx,
        "dangling_org_ids": dangling_org_ids,
        "older_datasets": older_info,
        "per_country": {cc: {b: dict(c) for b, c in m.items()}
                        for cc, m in per_cc.items()},
    }
    save_json(os.path.join(OUT, "report_v2.json"), report)
    save_json(os.path.join(OUT, "repair_candidates.json"), repair)

    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk != "samples"}
                      for k, v in audit.items()}, ensure_ascii=False, indent=1))
    print("departments", dep)
    print("duplicate wikidata: persons", len(dup_qid_person), "orgs", len(dup_qid_org))
    print("index", {k: v for k, v in idx.items() if k != "details"})
    print("older", older_info)
    print("report ->", os.path.join(OUT, "report_v2.json"))


if __name__ == "__main__":
    main()
