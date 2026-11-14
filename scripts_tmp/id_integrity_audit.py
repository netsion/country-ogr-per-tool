# -*- coding: utf-8 -*-
"""Global ID-reference integrity audit across all country datasets.

Directions audited:
  A. person.work_experience.org_id       -> orgs
  B. person.person_relationships.person_id -> persons
  C. person.family_members.person_id     -> persons
  D. org.key_people.person_id            -> persons
  E. org.related_entities.org_id         -> orgs
  F. departments.parent_dept_id          -> departments (same org)

Also:
  G. filename stem vs internal id, duplicate ids, duplicate wikidata_qid
  H. _index.json vs files consistency
  I. name-resolvability estimate for null/dangling person refs

Datasets: latest date folder per country (NG has 2026-07-29 + 2026-11-10;
only latest is treated as canonical, old one reported separately).

Output: output/_id_audit/report.json + report.md (+ samples json)
Usage: python scripts_tmp/id_integrity_audit.py
"""
import glob
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
OUT = os.path.join(BASE, "output", "_id_audit")
MAX_SAMPLES = 4000

CJK = re.compile(r"[\u4e00-\u9fff]")
PAREN = re.compile(r"[（(]([^）)]*)[）)]")
SUFFIXES = [
    "incorporated", "inc", "corporation", "corp", "company", "co", "limited",
    "ltd", "llc", "plc", "gmbh", "ag", "sa", "nv", "bv", "holding", "holdings",
    "group", "公司", "集团", "股份有限公司", "有限公司", "株式会社", "控股",
]


def norm(s):
    """Aggressive but deterministic name normalization."""
    if not s:
        return ""
    s = unicodedata.normalize("NFKC", str(s)).lower()
    s = re.sub(r"[\s\.\,\-\'’`&·:：/\\|]+", "", s)
    return s


def candidates(s):
    """Name -> set of normalized comparison candidates (outside + bracket contents)."""
    if not s:
        return set()
    s = str(s).strip()
    parts = PAREN.findall(s)
    outside = PAREN.sub(" ", s)
    out = set()
    for c in [outside] + parts:
        n = norm(c)
        if not n:
            continue
        out.add(n)
        for suf in SUFFIXES:
            if n.endswith(suf) and len(n) > len(suf) + 1:
                out.add(n[: -len(suf)])
    return out


def person_names(d):
    vals = [d.get("name"), d.get("name_en"), d.get("name_zh")]
    vals += d.get("aliases") or []
    out = set()
    for v in vals:
        out |= candidates(v)
    return out


def org_names(d):
    bi = d.get("basic_info") or {}
    vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")]
    vals += bi.get("aliases") or []
    out = set()
    for v in vals:
        out |= candidates(v)
    return out


def load_countries():
    """Latest date folder per country (plus extra old folders list)."""
    by_cc = defaultdict(list)
    for p in glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*")):
        rel = os.path.relpath(p, BASE).replace(os.sep, "/").split("/")
        by_cc[rel[1]].append((rel[2], p))
    latest = {}
    older = []
    for cc, items in by_cc.items():
        items.sort()
        latest[cc] = items[-1]
        for date, p in items[:-1]:
            older.append((cc, date, p))
    return latest, older


def main():
    os.makedirs(OUT, exist_ok=True)
    latest, older = load_countries()

    persons = {}   # pid -> (cc, path, data)
    orgs = {}      # oid -> (cc, path, data)
    per_dataset = {}
    id_issues = {"filename_mismatch": [], "dup_person_id": [], "dup_org_id": [],
                 "dup_person_qid": [], "dup_org_qid": []}

    # ---- load canonical datasets ----
    for cc, (date, folder) in sorted(latest.items()):
        pdir = os.path.join(folder, "persons")
        odir = os.path.join(folder, "orgs")
        for f in sorted(glob.glob(os.path.join(pdir, "*.json"))):
            bn = os.path.basename(f)
            if bn == "_index.json" or bn.startswith("_"):
                continue
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception as e:
                id_issues.setdefault("load_errors", []).append([f, str(e)])
                continue
            pid = d.get("person_id")
            stem = bn[:-5]
            if pid != stem:
                id_issues["filename_mismatch"].append([f, pid, stem])
            if pid in persons:
                id_issues["dup_person_id"].append([pid, persons[pid][1], f])
            persons[pid] = (cc, f, d)
        for f in sorted(glob.glob(os.path.join(odir, "*.json"))):
            bn = os.path.basename(f)
            if bn == "_index.json" or bn.startswith("_"):
                continue
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception as e:
                id_issues.setdefault("load_errors", []).append([f, str(e)])
                continue
            oid = d.get("org_id")
            stem = bn[:-5]
            if oid != stem:
                id_issues["filename_mismatch"].append([f, oid, stem])
            if oid in orgs:
                id_issues["dup_org_id"].append([oid, orgs[oid][1], f])
            orgs[oid] = (cc, f, d)
        per_dataset[cc] = {"date": date, "folder": folder,
                           "persons": 0, "orgs": 0}

    for pid, (cc, f, d) in persons.items():
        per_dataset[cc]["persons"] += 1
    for oid, (cc, f, d) in orgs.items():
        per_dataset[cc]["orgs"] += 1

    # duplicate wikidata qids
    qid_map = defaultdict(list)
    for pid, (cc, f, d) in persons.items():
        q = (d.get("wikidata_qid") or "").strip()
        if q:
            qid_map[q].append((pid, cc, d.get("name"), d.get("name_zh")))
    for q, lst in qid_map.items():
        if len(lst) > 1:
            id_issues["dup_person_qid"].append([q, lst])
    oqid_map = defaultdict(list)
    for oid, (cc, f, d) in orgs.items():
        q = ((d.get("basic_info") or {}).get("wikidata_qid") or "").strip()
        if q:
            oqid_map[q].append((oid, cc, (d.get("basic_info") or {}).get("name_original")))
    for q, lst in oqid_map.items():
        if len(lst) > 1:
            id_issues["dup_org_qid"].append([q, lst])

    # name lookup for resolvability
    pname_index = defaultdict(set)   # normalized name -> set(pid)
    for pid, (cc, f, d) in persons.items():
        for n in person_names(d):
            pname_index[n].add(pid)
    org_names_idx = {oid: org_names(d) for oid, (cc, f, d) in orgs.items()}

    def resolve_person(name):
        c = candidates(name)
        if not c:
            return None, "no-name"
        hits = set()
        for n in c:
            hits |= pname_index.get(n, set())
        if len(hits) == 1:
            return next(iter(hits)), "unique"
        if len(hits) > 1:
            return None, f"ambiguous({len(hits)})"
        return None, "not-found"

    # ---- audit references ----
    audit = {
        "work_org": {"total": 0, "filled": 0, "null_id": 0, "dangling": 0,
                     "mismatch": 0, "ok": 0, "samples": []},
        "person_rel": {"total": 0, "filled": 0, "null_id": 0, "dangling": 0,
                       "mismatch": 0, "ok": 0, "null_resolvable": 0,
                       "null_ambiguous": 0, "null_notfound": 0, "samples": []},
        "family": {"total": 0, "filled": 0, "null_id": 0, "dangling": 0,
                   "mismatch": 0, "ok": 0, "null_resolvable": 0,
                   "null_ambiguous": 0, "null_notfound": 0, "samples": []},
        "key_people": {"total": 0, "filled": 0, "null_id": 0, "dangling": 0,
                       "mismatch": 0, "ok": 0, "samples": []},
        "related_org": {"total": 0, "filled": 0, "null_id": 0, "dangling": 0,
                        "mismatch": 0, "ok": 0, "samples": []},
        "dept_parent": {"total": 0, "filled": 0, "null_id": 0, "dangling": 0,
                        "self": 0, "cycle": 0, "ok": 0, "samples": []},
    }
    per_cc = defaultdict(lambda: defaultdict(Counter))
    # mismatch samples keyed for human review
    mismatch_detail = defaultdict(list)

    def sample(bucket, row):
        if len(audit[bucket]["samples"]) < MAX_SAMPLES:
            audit[bucket]["samples"].append(row)

    # A. person -> org
    for pid, (cc, f, d) in persons.items():
        for w in d.get("work_experience") or []:
            if not isinstance(w, dict):
                continue
            a = audit["work_org"]
            a["total"] += 1
            per_cc[cc]["work_org"]["total"] += 1
            oid = (w.get("org_id") or "").strip() if isinstance(w.get("org_id"), str) else w.get("org_id")
            name = w.get("organization") or ""
            if not oid:
                a["null_id"] += 1
                per_cc[cc]["work_org"]["null_id"] += 1
                continue
            a["filled"] += 1
            if oid not in orgs:
                a["dangling"] += 1
                per_cc[cc]["work_org"]["dangling"] += 1
                sample("work_org", {"cc": cc, "person_id": pid, "name": d.get("name"),
                                    "org_id": oid, "organization": name, "issue": "dangling"})
                continue
            tgt = orgs[oid][2]
            if candidates(name) & org_names_idx[oid]:
                a["ok"] += 1
            else:
                a["mismatch"] += 1
                per_cc[cc]["work_org"]["mismatch"] += 1
                bi = tgt.get("basic_info") or {}
                row = {"cc": cc, "person_id": pid, "person": d.get("name"),
                       "org_id": oid, "organization": name,
                       "target": bi.get("name_zh") or bi.get("name_original"),
                       "issue": "mismatch"}
                sample("work_org", row)
                if len(mismatch_detail["work_org"]) < MAX_SAMPLES:
                    mismatch_detail["work_org"].append(row)

    # B/C. person -> person
    for pid, (cc, f, d) in persons.items():
        for arr, bucket, namekey in [
            ("person_relationships", "person_rel", "person_name"),
            ("family_members", "family", "name"),
        ]:
            for r in d.get(arr) or []:
                if not isinstance(r, dict):
                    continue
                a = audit[bucket]
                a["total"] += 1
                per_cc[cc][bucket]["total"] += 1
                rid = r.get("person_id")
                name = r.get(namekey) or ""
                if not rid:
                    a["null_id"] += 1
                    per_cc[cc][bucket]["null_id"] += 1
                    pid2, st = resolve_person(name)
                    if st == "unique":
                        a["null_resolvable"] += 1
                    elif st.startswith("ambiguous"):
                        a["null_ambiguous"] += 1
                    else:
                        a["null_notfound"] += 1
                    sample(bucket, {"cc": cc, "person_id": pid, "person": d.get("name"),
                                    "ref_name": name, "ref_person_id": None,
                                    "resolve": st, "resolved_to": pid2})
                    continue
                a["filled"] += 1
                if rid not in persons:
                    a["dangling"] += 1
                    per_cc[cc][bucket]["dangling"] += 1
                    sample(bucket, {"cc": cc, "person_id": pid, "person": d.get("name"),
                                    "ref_name": name, "ref_person_id": rid,
                                    "issue": "dangling"})
                    continue
                tgt = persons[rid][2]
                if candidates(name) & person_names(tgt):
                    a["ok"] += 1
                else:
                    a["mismatch"] += 1
                    per_cc[cc][bucket]["mismatch"] += 1
                    row = {"cc": cc, "person_id": pid, "person": d.get("name"),
                           "ref_name": name, "ref_person_id": rid,
                           "target": tgt.get("name") or tgt.get("name_zh"),
                           "issue": "mismatch"}
                    sample(bucket, row)
                    mismatch_detail[bucket].append(row)

    # D. org -> person
    for oid, (cc, f, d) in orgs.items():
        for kp in d.get("key_people") or []:
            if not isinstance(kp, dict):
                continue
            a = audit["key_people"]
            a["total"] += 1
            per_cc[cc]["key_people"]["total"] += 1
            rid = kp.get("person_id")
            name = kp.get("name") or ""
            if not rid:
                a["null_id"] += 1
                per_cc[cc]["key_people"]["null_id"] += 1
                continue
            a["filled"] += 1
            if rid not in persons:
                a["dangling"] += 1
                per_cc[cc]["key_people"]["dangling"] += 1
                sample("key_people", {"cc": cc, "org_id": oid, "org": (d.get("basic_info") or {}).get("name_zh"),
                                      "ref_name": name, "ref_person_id": rid, "issue": "dangling"})
                continue
            tgt = persons[rid][2]
            if candidates(name) & person_names(tgt):
                a["ok"] += 1
            else:
                a["mismatch"] += 1
                per_cc[cc]["key_people"]["mismatch"] += 1
                row = {"cc": cc, "org_id": oid, "org": (d.get("basic_info") or {}).get("name_zh"),
                       "ref_name": name, "ref_person_id": rid,
                       "target": tgt.get("name") or tgt.get("name_zh"), "issue": "mismatch"}
                sample("key_people", row)
                mismatch_detail["key_people"].append(row)

    # E. org -> org
    for oid, (cc, f, d) in orgs.items():
        for re_ in d.get("related_entities") or []:
            if not isinstance(re_, dict):
                continue
            a = audit["related_org"]
            a["total"] += 1
            per_cc[cc]["related_org"]["total"] += 1
            rid = re_.get("org_id")
            name = re_.get("org_name") or ""
            if not rid:
                a["null_id"] += 1
                per_cc[cc]["related_org"]["null_id"] += 1
                continue
            a["filled"] += 1
            if rid not in orgs:
                a["dangling"] += 1
                per_cc[cc]["related_org"]["dangling"] += 1
                sample("related_org", {"cc": cc, "org_id": oid,
                                       "ref_name": name, "ref_org_id": rid, "issue": "dangling"})
                continue
            tgt = orgs[rid][2]
            if candidates(name) & org_names_idx[rid]:
                a["ok"] += 1
            else:
                a["mismatch"] += 1
                per_cc[cc]["related_org"]["mismatch"] += 1
                bi = tgt.get("basic_info") or {}
                row = {"cc": cc, "org_id": oid,
                       "org": (d.get("basic_info") or {}).get("name_zh"),
                       "ref_name": name, "ref_org_id": rid,
                       "target": bi.get("name_zh") or bi.get("name_original"),
                       "issue": "mismatch"}
                sample("related_org", row)
                mismatch_detail["related_org"].append(row)

    # F. departments
    for oid, (cc, f, d) in orgs.items():
        deps = [x for x in (d.get("departments") or []) if isinstance(x, dict)]
        ids = {x.get("dept_id") for x in deps if x.get("dept_id")}
        parent_map = {x.get("dept_id"): x.get("parent_dept_id") for x in deps if x.get("dept_id")}
        for dep in deps:
            a = audit["dept_parent"]
            a["total"] += 1
            per_cc[cc]["dept_parent"]["total"] += 1
            par = dep.get("parent_dept_id")
            did = dep.get("dept_id")
            if not par:
                a["null_id"] += 1
                continue
            a["filled"] += 1
            if par == did:
                a["self"] += 1
                sample("dept_parent", {"cc": cc, "org_id": oid, "dept_id": did, "issue": "self"})
            elif par not in ids:
                a["dangling"] += 1
                per_cc[cc]["dept_parent"]["dangling"] += 1
                sample("dept_parent", {"cc": cc, "org_id": oid, "dept_id": did,
                                       "parent": par, "issue": "dangling"})
            else:
                # cycle check
                seen = set()
                cur = par
                cyc = False
                while cur and cur in parent_map:
                    if cur in seen:
                        cyc = True
                        break
                    seen.add(cur)
                    cur = parent_map.get(cur)
                if cyc:
                    a["cycle"] += 1
                    sample("dept_parent", {"cc": cc, "org_id": oid, "dept_id": did,
                                           "parent": par, "issue": "cycle"})
                else:
                    a["ok"] += 1

    # G/H. index files
    index_issues = {"person_index_missing_file": [], "person_index_dup": [],
                    "person_index_id_mismatch": [], "org_index_missing_file": [],
                    "org_index_dup": [], "org_index_name_mismatch": [],
                    "persons_not_in_index": [], "orgs_not_in_index": []}
    for cc, (date, folder) in sorted(latest.items()):
        pidx = os.path.join(folder, "persons", "_index.json")
        files = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(folder, "persons", "*.json"))
                 if not os.path.basename(p).startswith("_")}
        if os.path.exists(pidx):
            d = json.load(open(pidx, encoding="utf-8"))
            profs = d.get("profiles") or []
            seen = Counter()
            for p in profs:
                pid = p.get("person_id")
                seen[pid] += 1
                fn = p.get("file") or f"{pid}.json"
                if fn[:-5] not in files:
                    index_issues["person_index_missing_file"].append([cc, pid, fn])
                if pid not in persons:
                    index_issues["person_index_id_mismatch"].append([cc, pid])
            for pid, n in seen.items():
                if n > 1:
                    index_issues["person_index_dup"].append([cc, pid, n])
            for fstem in files:
                if fstem not in seen:
                    index_issues["persons_not_in_index"].append([cc, fstem])
        oidx = os.path.join(folder, "orgs", "_index.json")
        ofiles = {os.path.basename(p)[:-5] for p in glob.glob(os.path.join(folder, "orgs", "*.json"))
                  if not os.path.basename(p).startswith("_")}
        if os.path.exists(oidx):
            d = json.load(open(oidx, encoding="utf-8"))
            profs = d.get("profiles") or []
            seen = Counter()
            for p in profs:
                oid = p.get("org_id")
                seen[oid] += 1
                if oid not in ofiles:
                    index_issues["org_index_missing_file"].append([cc, oid])
                elif oid in orgs:
                    idx_name = p.get("name") or ""
                    if candidates(idx_name) and not (candidates(idx_name) & org_names_idx[oid]):
                        index_issues["org_index_name_mismatch"].append(
                            [cc, oid, p.get("name"), (orgs[oid][2].get("basic_info") or {}).get("name_zh")])
            for oid, n in seen.items():
                if n > 1:
                    index_issues["org_index_dup"].append([cc, oid, n])
            for fstem in ofiles:
                if fstem not in seen:
                    index_issues["orgs_not_in_index"].append([cc, fstem])

    # ---- old NG dataset quick check ----
    ng_old = {}
    for cc, date, folder in older:
        old_p = {}
        for f in glob.glob(os.path.join(folder, "persons", "*.json")):
            bn = os.path.basename(f)
            if bn.startswith("_"):
                continue
            try:
                d = json.load(open(f, encoding="utf-8"))
            except Exception:
                continue
            old_p[d.get("person_id")] = d.get("name")
        ng_old[f"{cc}/{date}"] = {"persons": len(old_p),
                                  "id_overlap_with_latest": len(set(old_p) & set(persons)),
                                  "same_id_diff_name": sum(
                                      1 for pid, nm in old_p.items()
                                      if pid in persons and (persons[pid][2].get("name") != nm))}

    report = {
        "generated_at": "2026-11-13",
        "datasets": per_dataset,
        "totals": {"persons": len(persons), "orgs": len(orgs)},
        "references": audit,
        "per_country": {cc: {b: dict(c) for b, c in m.items()} for cc, m in per_cc.items()},
        "id_issues": {k: (v[:200] if isinstance(v, list) else v) for k, v in id_issues.items()},
        "index_issues": {k: v[:200] for k, v in index_issues.items()},
        "older_datasets": ng_old,
    }
    with open(os.path.join(OUT, "report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "mismatch_samples.json"), "w", encoding="utf-8") as fh:
        json.dump({k: v for k, v in mismatch_detail.items()}, fh, ensure_ascii=False, indent=1)

    # ---- markdown ----
    L = []
    L.append("# 全库 ID 引用完整性审计\n")
    L.append(f"- 数据范围：{len(latest)} 个国家最新日期目录，person {len(persons):,}，org {len(orgs):,}")
    L.append(f"- 生成时间：2026-11-13\n")
    L.append("## 1. 引用完整性总表\n")
    L.append("| 引用方向 | 总条数 | 已填 ID | ID 为空 | ID 悬空 | ID 指错(名称不符) | 正常 |")
    L.append("|---|---:|---:|---:|---:|---:|---:|")
    labels = {
        "work_org": "person.work_experience.org_id → org",
        "person_rel": "person.person_relationships.person_id → person",
        "family": "person.family_members.person_id → person",
        "key_people": "org.key_people.person_id → person",
        "related_org": "org.related_entities.org_id → org",
        "dept_parent": "org.departments.parent_dept_id → dept",
    }
    for b, lab in labels.items():
        a = audit[b]
        L.append(f"| {lab} | {a['total']:,} | {a['filled']:,} | {a['null_id']:,} | "
                 f"{a['dangling']:,} | {a.get('mismatch', 0):,} | {a.get('ok', 0):,} |")
    L.append("")
    L.append("## 2. 空 person_id 的可解析性（按姓名）\n")
    L.append("| 方向 | 空 ID | 姓名可唯一定位 | 姓名重名歧义 | 姓名找不到 |")
    L.append("|---|---:|---:|---:|---:|")
    for b, lab in [("person_rel", "关系人"), ("family", "家庭成员")]:
        a = audit[b]
        L.append(f"| {lab} | {a['null_id']:,} | {a['null_resolvable']:,} | "
                 f"{a['null_ambiguous']:,} | {a['null_notfound']:,} |")
    L.append("")
    L.append("## 3. ID 体系问题\n")
    L.append(f"- 文件名 vs 内部 ID 不一致：{len(id_issues['filename_mismatch'])}")
    L.append(f"- person_id 重复（跨目录）：{len(id_issues['dup_person_id'])}")
    L.append(f"- org_id 重复（跨目录，含 NG 双日期）：{len(id_issues['dup_org_id'])}")
    L.append(f"- person wikidata_qid 重复：{len(id_issues['dup_person_qid'])} 组")
    L.append(f"- org wikidata_qid 重复：{len(id_issues['dup_org_qid'])} 组")
    L.append("")
    L.append("## 4. _index.json 一致性\n")
    for k, v in index_issues.items():
        L.append(f"- {k}: {len(v)}")
    L.append("")
    L.append("## 5. 各国 work_experience org 引用异常（Top 20）\n")
    L.append("| 国家 | 总数 | 空 ID | 悬空 | 指错 |")
    L.append("|---|---:|---:|---:|---:|")
    rows = []
    for cc, m in per_cc.items():
        w = m.get("work_org") or {}
        bad = (w.get("dangling") or 0) + (w.get("mismatch") or 0)
        rows.append((bad, cc, w))
    for bad, cc, w in sorted(rows, reverse=True)[:20]:
        L.append(f"| {cc} | {w.get('total',0):,} | {w.get('null_id',0):,} | "
                 f"{w.get('dangling',0):,} | {w.get('mismatch',0):,} |")
    L.append("")
    L.append("## 6. 典型错配样例（Musk 相关 + 全局抽样）\n")
    for b in ("work_org", "person_rel", "family", "key_people", "related_org"):
        L.append(f"### {b}\n")
        L.append("```json")
        L.append(json.dumps(audit[b]["samples"][:15], ensure_ascii=False, indent=1))
        L.append("```\n")
    with open(os.path.join(OUT, "report.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L))

    print(json.dumps({
        "persons": len(persons), "orgs": len(orgs),
        "refs": {b: {k: v for k, v in audit[b].items() if k != "samples"} for b in audit},
        "id_issues": {k: len(v) if isinstance(v, list) else v for k, v in id_issues.items()},
        "index_issues": {k: len(v) for k, v in index_issues.items()},
        "older": ng_old,
    }, ensure_ascii=False, indent=1))
    print("\nreport ->", os.path.join(OUT, "report.md"))


if __name__ == "__main__":
    main()
