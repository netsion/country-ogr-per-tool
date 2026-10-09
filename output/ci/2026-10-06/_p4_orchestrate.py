"""P4 orchestration: build progress, emit per-person dispatch prompt, validate output."""
import json
import sys

BASE = "output/ci/2026-10-06"
PROGRESS = f"{BASE}/_phase_progress.json"
PLIST = f"{BASE}/person_list.json"

# skip the 2 orphan registry entries (no org references, no anchor for search)
ORPHANS = {"CI-PERSON-000009", "CI-PERSON-000020"}
IMP_ORDER = {"high": 0, "medium": 1, "low": 2}


def build_progress():
    data = json.load(open(PLIST, encoding="utf-8"))
    persons = [p for p in data["persons"]
               if p.get("p4_action", "dispatch") == "dispatch" and p["person_id"] not in ORPHANS]
    persons.sort(key=lambda p: (IMP_ORDER.get(p["importance_level"], 9), p["person_id"]))
    prog = {
        "phase": "P4_person_enrichment",
        "concurrency": 4,
        "started_at": "2026-10-07",
        "last_updated": "2026-10-07",
        "completed": [],
        "remaining": [p["person_id"] for p in persons],
        "current": [],
        "failed": [],
        "skipped_trim": sum(1 for p in data["persons"] if p.get("p4_action") == "skip"),
        "orphans_dropped": sorted(ORPHANS),
        "persons": {p["person_id"]: {"name": p["name"], "name_zh": p.get("name_zh"),
                                     "importance": p["importance_level"],
                                     "orgs": [(so.get("org_id"), so.get("position_title"))
                                              for so in p.get("source_orgs", []) if isinstance(so, dict)]}
                    for p in persons},
    }
    with open(PROGRESS, "w", encoding="utf-8") as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)
    print(f"P4 progress built: dispatch={len(persons)}, skipped_trim={prog['skipped_trim']}, orphans={len(ORPHANS)}")


def person_info(pid):
    prog = json.load(open(PROGRESS, encoding="utf-8"))
    info = prog.get("persons", {}).get(pid)
    if not info:
        raise SystemExit(f"person not in progress: {pid}")
    return info


def prompt_for(pid):
    info = person_info(pid)
    name = info["name"]
    name_zh = info.get("name_zh")
    orgs = info.get("orgs") or []
    ctx = " ; ".join(f"{oid}:{title}" for oid, title in orgs[:3] if title)
    zh_hint = f"已收录中文名「{name_zh}」可直接使用" if name_zh else "中文名未收录，按规则优先级获取（Wikidata zh→中文维基→通行译名）"
    # dedup warning if this person_id already referenced in _name_index (cross-org person)
    import os
    dedup = ""
    idx_path = f"{BASE}/_name_index.json"
    if os.path.exists(idx_path):
        idx = json.load(open(idx_path, encoding="utf-8"))
        if pid in json.dumps(idx, ensure_ascii=False):
            dedup = "\n⚠️ 该人物已被多个组织引用（跨组织人物）：务必复用本 person_id，仅创建一份档案，整合所有组织的职务信息。\n"
    p = f"""你是人物信息调查 Agent，从事公开人物百科资料整理。任务：为 {pid}（{name}）生成高质量人物画像。

已知背景（已核实，可直接引用）：{ctx}
中文名处理：{zh_hint}
{dedup}
第一步：读取必要文件（不可跳过）
1. 规则手册：output/ci/2026-10-06/_person_rules_ci.md（配合 .agents/skills/country-org-collector/person_collection_rules.md 使用；字段约束、语言规范、枚举值、写入方式）
2. Schema：.agents/skills/country-org-collector/person_profile_schema.json
3. ID 索引：output/ci/2026-10-06/_name_index.json（organization/person_name 命中用 ID，未命中 null，禁止自创 ID，禁止修改 id_registry.json）

第二步：搜索并获取详情（法语 → 英语 → 中文）
1. Wikipedia（法语/英语）：「{name}」biographie/profile → biography、education、career
2. 官方/机构页：按上面已知背景中的组织找 leadership/board 页面核实现任职务
3. 法语新闻：「{name} Côte d'Ivoire actualités 2025 2026」→ recent activity、political_stances、major_achievements
4. 社媒搜索："{name}" site:linkedin.com / site:facebook.com 等
至少读取 3 个独立来源全文；总请求 ≤15 次，间隔 ≥1 秒（页面 3 秒）
工具：mcp__search-read__search + mcp__search-read__read_url 首选；失败 WebSearch / curl --proxy http://127.0.0.1:7890 -L；web_reader 配额耗尽勿用

第三步：组装画像并写入 output/ci/2026-10-06/persons/{pid}.json
严格按两份规则手册：字段名约束、中文(法语)格式、枚举值、collection_meta.phase=phase4_person_profile、quotes 对象数组 ≥3 条；biography_summary 中文 ≥100 字；搜不到的字段留空/null，family_members 无真实全名就删条目；用 Write 工具直接写 JSON（禁止 python -c 内联）

第四步：写入后验证（不可跳过）
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ci/2026-10-06 --file persons/{pid}.json
如有 ERRORS → 修复 → 重验直到 0 errors
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ci/2026-10-06 --file persons/{pid}.json --score

铁律：禁止编造，搜不到留空；重要信息 2 个独立来源交叉确认。
完成后返回：person_id、completeness_score、来源数、缺失字段列表（一行式简短汇报）。"""
    print(p)


def check(pid):
    import os
    fp = f"{BASE}/persons/{pid}.json"
    if not os.path.exists(fp):
        print(f"FAIL {pid}: file not found")
        sys.exit(1)
    try:
        with open(fp, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(f"FAIL {pid}: JSON broken: {e}")
        sys.exit(1)
    cm = d.get("collection_meta", {})
    bio = d.get("biography_summary") or ""
    is_zh = any("\u4e00" <= c <= "\u9fff" for c in bio)
    n_we = len(d.get("work_experience") or [])
    n_sa = len(d.get("social_accounts") or [])
    quotes = cm.get("quotes") or []
    ok = cm.get("phase") == "phase4_person_profile" and is_zh and len(bio) >= 100 and quotes
    print(f"{'OK ' if ok else 'FAIL'} {pid}: score={cm.get('completeness_score', 0)} bio={'zh*' if is_zh else 'NOT-ZH'}({len(bio)}) work={n_we} social={n_sa} quotes={len(quotes)}")
    if not d.get("name_zh"):
        print(f"  WARN: name_zh empty")
    if n_sa < 2:
        print(f"  WARN: social_accounts < 2")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build_progress()
    elif cmd == "prompt":
        prompt_for(sys.argv[2])
    elif cmd == "check":
        check(sys.argv[2])
    elif cmd == "advance":
        pid = sys.argv[2]
        prog = json.load(open(PROGRESS, encoding="utf-8"))
        if pid in prog["current"]:
            prog["current"].remove(pid)
        if pid not in prog["completed"]:
            prog["completed"].append(pid)
        with open(PROGRESS, "w", encoding="utf-8") as f:
            json.dump(prog, f, ensure_ascii=False, indent=2)
        print(f"advanced: {pid} | completed={len(prog['completed'])}/{len(prog['persons'])} remaining={len(prog['remaining'])}")
    elif cmd == "mark":
        pid = sys.argv[2]
        prog = json.load(open(PROGRESS, encoding="utf-8"))
        if pid in prog["remaining"]:
            prog["remaining"].remove(pid)
        if pid not in prog["current"]:
            prog["current"].append(pid)
        with open(PROGRESS, "w", encoding="utf-8") as f:
            json.dump(prog, f, ensure_ascii=False, indent=2)
        print(f"marked: {pid} in flight")
    else:
        raise SystemExit("unknown cmd")
