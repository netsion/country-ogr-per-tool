# -*- coding: utf-8 -*-
"""Build the full 826-row pending review workbook.

- pending = v3 plan status pending_review minus the 80 next-batch rows
- reallocates candidate IDs with ever_used including ALL business refs
- groups same shadow identity via v3 identity_key
- adds ref counts / risk flags; outputs CSV + XLSX
"""
import csv, glob, json, os, re, sys
from collections import Counter, defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from id_integrity_audit2 import BASE, OUT, sig, match
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

V3 = os.path.join(OUT, "registry_newid_plan_v3.csv")
NEXT = os.path.join(OUT, "registry_newid_sample_80_next_reviewed.csv")
CC_NAMES = {
    "kr": ["韩国", "korea"], "mx": ["墨西哥", "mexico"], "nz": ["新西兰", "new zealand"],
    "jp": ["日本", "japan"], "cn": ["中国", "china", "清华", "tsinghua"],
    "us": ["美国", "united states"], "vn": ["越南", "vietnam"], "sg": ["新加坡", "singapore"],
    "pg": ["巴布亚新几内亚", "papua new guinea"], "id": ["印度尼西亚", "indonesia"],
    "au": ["澳大利亚", "australia"], "gb": ["英国", "united kingdom", "britain"],
    "fr": ["法国", "france"], "ch": ["瑞士", "switzerland"], "br": ["巴西", "brazil"],
    "es": ["西班牙", "spain"], "it": ["意大利", "italy"], "de": ["德国", "germany"],
}
NONORG_WORDS = ["考试", "资格", "职位", "总局长", "集合", "小组", "项目", "内设",
                "部门", "竞选团队", "支部", "委员会办公室"]


def norm_key(s):
    return re.sub(r"[\s\.\,\-\'’`&·:：/\\|（）()\[\]【】]+", "", (s or "").lower())


def ref_name(item, kind):
    keys = (["organization", "org_name", "organization_en"] if kind == "org"
            else ["person_name", "name"] if kind in ("rel", "family") else ["name", "name_en"])
    for k in keys:
        v = item.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def main():
    v3 = list(csv.DictReader(open(V3, encoding="utf-8-sig")))
    next_rows = list(csv.DictReader(open(NEXT, encoding="utf-8-sig")))
    next_keys = {(r["国家"].lower(), r["冲突ID"], r["影子名称"].strip()) for r in next_rows}
    pending = [r for r in v3 if r["status"] == "pending_review"
               and (r["collision_id"][:2].lower(), r["collision_id"], r["shadow"].strip()) not in next_keys]
    print("pending", len(pending))

    # ever_used incl. refs
    used = set()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/id_registry.json")):
        d = json.load(open(f, encoding="utf-8"))
        for key, idk in [("registry", "org_id"), ("person_registry", "person_id"),
                         ("deprecated_registry", "org_id"),
                         ("deprecated_person_registry", "person_id")]:
            for e in d.get(key) or []:
                if e.get(idk): used.add(e[idk])
        for e in d.get("registry") or []:
            if e.get("person_id"): used.add(e["person_id"])
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8"))
        if d.get("person_id"): used.add(d["person_id"])
        for w in d.get("work_experience") or []:
            if w.get("org_id"): used.add(w["org_id"])
        for x in d.get("person_relationships") or []:
            if x.get("person_id"): used.add(x["person_id"])
        for x in d.get("family_members") or []:
            if x.get("person_id"): used.add(x["person_id"])
        for x in d.get("org_ids") or []:
            if x: used.add(x)
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8"))
        if d.get("org_id"): used.add(d["org_id"])
        for x in d.get("related_entities") or []:
            if x.get("org_id"): used.add(x["org_id"])
        for x in d.get("key_people") or []:
            if x.get("person_id"): used.add(x["person_id"])
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/_name_index.json")):
        try: d = json.load(open(f, encoding="utf-8"))
        except Exception: continue
        for v in d.values():
            if isinstance(v, str) and re.match(r"^[A-Z]{2}-(PERSON|[A-Z_]+)-\d+$", v): used.add(v)
    maxseq = defaultdict(int)
    for i in used:
        m = re.match(r"^([A-Z]{2})-([A-Z_]+)-(\d+)$", i)
        if m: maxseq[(m.group(1), m.group(2))] = max(maxseq[(m.group(1), m.group(2))], int(m.group(3)))
    def alloc(cc, cat):
        key = (cc.upper(), cat)
        while True:
            maxseq[key] += 1; n = maxseq[key]
            cand = f"{cc.upper()}-PERSON-{n:06d}" if cat == "PERSON" else f"{cc.upper()}-{cat}-{n:03d}"
            if cand not in used:
                used.add(cand); return cand

    # profiles / owner sig / index
    profs = []
    owner = {}
    for kind, pat, idk in [("org", "output/[a-z][a-z]/20*/orgs/*.json", "org_id"),
                           ("person", "output/[a-z][a-z]/20*/persons/*.json", "person_id")]:
        for f in glob.glob(os.path.join(BASE, pat)):
            if os.path.basename(f).startswith("_"): continue
            d = json.load(open(f, encoding="utf-8")); i = d.get(idk)
            if not i: continue
            if kind == "org":
                bi = d.get("basic_info") or {}
                vals = [bi.get("name_zh"), bi.get("name_en"), bi.get("name_original")] + (bi.get("aliases") or [])
                nm = bi.get("name_zh") or bi.get("name_original")
            else:
                vals = [d.get("name"), d.get("name_en"), d.get("name_zh")] + (d.get("aliases") or [])
                nm = d.get("name") or d.get("name_zh")
            c = set()
            for v in vals: c |= sig(v)[0]
            profs.append((i, kind, i[:2].lower(), c, nm))
    idx = defaultdict(set)
    for i, kind, cc, c, nm in profs:
        for x in c: idx[(kind, cc, x)].add(i)
    for i, kind, cc, c, nm in profs:
        owner[(kind, i)] = c

    # ref counts
    by_cid = defaultdict(list)
    for j, r in enumerate(pending): by_cid[r["collision_id"]].append(j)
    refs = Counter()
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/persons/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8"))
        for arr, kind in [("work_experience", "org"), ("person_relationships", "person"), ("family_members", "person")]:
            for item in d.get(arr) or []:
                cid = item.get("org_id") if kind == "org" else item.get("person_id")
                if cid not in by_cid: continue
                nm = ref_name(item, kind)
                if not nm or match(sig(nm), (owner.get((kind, cid), set()), [])): continue
                hits = [j for j in by_cid[cid] if match(sig(nm), (sig(pending[j]["shadow"])[0], []))]
                if len(hits) == 1: refs[hits[0]] += 1
    for f in glob.glob(os.path.join(BASE, "output/[a-z][a-z]/20*/orgs/*.json")):
        if os.path.basename(f).startswith("_"): continue
        d = json.load(open(f, encoding="utf-8"))
        for arr, kind in [("key_people", "person"), ("related_entities", "org")]:
            for item in d.get(arr) or []:
                cid = item.get("person_id") if kind == "person" else item.get("org_id")
                if cid not in by_cid: continue
                nm = ref_name(item, kind)
                if not nm or match(sig(nm), (owner.get((kind, cid), set()), [])): continue
                hits = [j for j in by_cid[cid] if match(sig(nm), (sig(pending[j]["shadow"])[0], []))]
                if len(hits) == 1: refs[hits[0]] += 1

    # identity groups + allocation
    groups = {}
    out = []
    for j, r in enumerate(pending):
        cc = r["collision_id"][:2].lower()
        key = (cc, norm_key(r["shadow"]))
        cat = r["category"]
        new_id = ""
        if key in groups:
            status = "same_identity"; new_id = groups[key]
        else:
            new_id = alloc(cc, cat); groups[key] = new_id; status = "pending_review"
        shadow = r["shadow"]; low = shadow.lower()
        hints = []
        for occ, names in CC_NAMES.items():
            if occ != cc and any(n.lower() in low for n in names):
                hints.append(f"含他国名:{occ}")
        if any(w in shadow for w in NONORG_WORDS):
            hints.append("疑似非独立组织")
        # existing profile candidates
        rs = sig(shadow)
        cands = set()
        for x in rs[0]:
            cands |= idx.get(("org", cc, x), set())
            cands |= idx.get(("person", cc, x), set())
        ph = [i for i in cands if i != r["collision_id"] and match(rs, (owner.get(("org", i), set()) | owner.get(("person", i), set()), []))]
        if ph:
            pkind = "person" if any(i in {p[0] for p in profs if p[1] == "person"} for i in ph) else "org"
            hints.append(f"已有画像候选:{','.join(ph[:3])}")
        if refs[j] == 0:
            hints.append("无引用")
        pri = 3
        if refs[j] >= 3 or any(h.startswith(("含他国名", "已有画像", "疑似非独立")) for h in hints):
            pri = 1
        elif refs[j] > 0:
            pri = 2
        advice = ("需复核（国别/身份）" if any(h.startswith(("含他国名", "已有画像", "疑似非独立")) for h in hints)
                  else "可分配（低风险）" if refs[j] > 0 else "无引用可延后")
        out.append({"优先级": pri, "国家": cc.upper(), "冲突ID": r["collision_id"],
                    "现画像": r["owner"], "影子名称": shadow, "计划类别": cat,
                    "候选新ID": new_id, "身份组": key[1], "同身份": "是" if status == "same_identity" else "",
                    "引用数": refs[j], "风险提示": ";".join(hints), "机器建议": advice,
                    "复核结论": "", "建议类别": "", "建议国别": "", "备注": ""})
    out.sort(key=lambda x: (x["优先级"], -x["引用数"], x["国家"], x["冲突ID"]))

    fields = list(out[0].keys())
    csvp = os.path.join(OUT, "registry_newid_pending826_review.csv")
    with open(csvp, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows(out)
    # priority sample
    with open(os.path.join(OUT, "registry_newid_pending826_priority.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields); w.writeheader(); w.writerows([r for r in out if r["优先级"] == 1])

    # xlsx
    wb = Workbook()
    ws = wb.active; ws.title = "全部826"
    ws.append(fields)
    for r in out: ws.append([r[f] for f in fields])
    for c in range(1, len(fields)+1):
        ws.column_dimensions[get_column_letter(c)].width = 18 if c <= 10 else 42
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(fields))}{len(out)+1}"
    head_fill = PatternFill("solid", fgColor="1F4E78")
    for c in range(1, len(fields)+1):
        cell = ws.cell(row=1, column=c)
        cell.font = Font(color="FFFFFF", bold=True); cell.fill = head_fill
    p1 = wb.create_sheet("P1优先")
    p1.append(fields)
    for r in out:
        if r["优先级"] == 1: p1.append([r[f] for f in fields])
    p1.freeze_panes = "A2"; p1.auto_filter.ref = f"A1:{get_column_letter(len(fields))}{p1.max_row}"
    # country summary
    sm = wb.create_sheet("按国家统计")
    sm.append(["国家", "总数", "P1", "P2", "P3", "有引用", "无引用"])
    for cc in sorted({r["国家"] for r in out}):
        sub = [r for r in out if r["国家"] == cc]
        sm.append([cc, len(sub), sum(1 for r in sub if r["优先级"] == 1),
                   sum(1 for r in sub if r["优先级"] == 2),
                   sum(1 for r in sub if r["优先级"] == 3),
                   sum(1 for r in sub if r["引用数"] > 0),
                   sum(1 for r in sub if r["引用数"] == 0)])
    info = wb.create_sheet("说明")
    info["A1"] = "复核填写：复核结论填 分配/改类别后分配/不分配/挂起；建议类别/国别仅在改类别时填；备注写理由。"
    info["A2"] = "P1=高引用或高风险（国别/已有画像/疑似非独立组织）；P2=有引用低风险；P3=无引用可延后。"
    info["A3"] = "候选新ID已按全部历史编号 + 业务引用ID重新分配；若改类别/国别，执行时会重新发号。"
    wb.save(os.path.join(OUT, "registry_newid_pending826_review.xlsx"))

    print("rows", len(out), "status", dict(Counter(r["同身份"] for r in out)),
          "priority", dict(Counter(r["优先级"] for r in out)),
          "with_refs", sum(1 for r in out if r["引用数"] > 0))
    print("->", csvp)
    print("->", os.path.join(OUT, "registry_newid_pending826_review.xlsx"))


if __name__ == "__main__":
    main()
