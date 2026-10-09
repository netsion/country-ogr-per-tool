"""P3 orchestration helpers: build progress file, emit per-org dispatch prompt, validate output."""
import json
import sys

BASE = "output/ci/2026-10-06"
PROGRESS = f"{BASE}/_phase_progress.json"
TRIM = f"{BASE}/_p3_trim_plan.json"
TARGETS = f"{BASE}/_target_orgs.json"
FACTCHECK_IDS = {
    "CI-GOV-008", "CI-SOE-002", "CI-FIN-002", "CI-FIN-004", "CI-FIN-005", "CI-FIN-006",
    "CI-FIN-007", "CI-FIN-008", "CI-MEDIA-004", "CI-MEDIA-007", "CI-NGO-003",
    "CI-MIL-002", "CI-GOV-011", "CI-GOV-012",
}
# dispatch order per skill suggestion (category batching)
ORDER = ["GOV", "SOE", "FIN", "CORP", "ACAD", "MEDIA", "NGO", "PARTY", "MIL", "INTL"]


def build_progress():
    with open(TARGETS, encoding="utf-8") as f:
        targets = json.load(f)
    with open(TRIM, encoding="utf-8") as f:
        trim_ids = {t["org_id"] for t in json.load(f)["trim"]}
    keep = [t for t in targets if t["id"] not in trim_ids]
    keep.sort(key=lambda t: (ORDER.index(t["category"]), t["id"]))
    progress = {
        "phase": "P3_org_enrichment",
        "concurrency": 4,
        "started_at": "2026-10-06T00:00:00",
        "last_updated": "2026-10-06T00:00:00",
        "completed": [],
        "remaining": [t["id"] for t in keep],
        "current": [],
        "failed": [],
        "trimmed_not_dispatched": sorted(trim_ids),
    }
    with open(PROGRESS, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    print(f"progress built: remaining={len(progress['remaining'])}, trimmed={len(trim_ids)}")


def org_info(org_id):
    with open(TARGETS, encoding="utf-8") as f:
        for t in json.load(f):
            if t["id"] == org_id:
                return t
    raise SystemExit(f"org not found: {org_id}")


def prompt_for(org_id):
    t = org_info(org_id)
    filepath = f"{BASE}/orgs/{org_id}.json"
    factcheck = ""
    if org_id in FACTCHECK_IDS:
        factcheck = ("\n本组织已有人工核实事实，先读 output/ci/2026-10-06/_factcheck_noqid_orgs.md "
                     "中本组织条目，直接引用其中已核实信息（负责人、成立年份、存续状态），不要重复搜索。\n")
    p = f"""你是组织信息丰富 Agent。任务：为 {org_id}（{t['name']}）生成高质量画像。

第一步：读取必要文件（不可跳过）
1. 规则手册：output/ci/2026-10-06/_org_rules_ci.md（字段名约束、语言规范、APEC 立场、ID 规则、写入方式——全部以此为准）
2. 当前骨架：{filepath}
3. ID 索引：output/ci/2026-10-06/_name_index.json（命中用对应 ID，未命中写 null，禁止自创 ID，禁止修改 id_registry.json）
{factcheck}
第二步：搜索并综合（每步都从结果中提取所有字段信息，不要只关注主目标字段）
1. 读 Wikipedia 页面：法语「{t['name']}」+ 英语（中/法语维基有则读）
2. 读官网（骨架 website 字段）首页+关于/联系页 → social_accounts（页脚图标）、digital_assets、departments
3. 搜法语新闻：「{t['name']} actualités 2025 2026」→ recent_events（≥3 条，每条含 YYYY-MM-DD 日期+source URL）
4. 检查空缺字段做 0-2 次补充搜索；总请求 ≤15 次，间隔 ≥1 秒（页面 3 秒）
工具：搜索 mcp__search-read__search → 失败用 WebSearch；读取 mcp__search-read__read_url → 失败用 curl --proxy http://127.0.0.1:7890 -L。web_reader 配额耗尽勿用。

第三步：写入完整画像到 {filepath}（严格按规则手册：字段名、中文(法语)命名、collection_meta.phase=phase3_enriched、quotes 为对象数组 ≥3 条、apec_stance 如实声明科特迪瓦非 APEC 成员）

第四步：写入后验证（不可跳过）
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ci/2026-10-06 --file {filepath}
如有 ERRORS → 修复 → 重验直到 0 errors
python .agents/skills/country-org-collector/scripts/validate_schema.py output/ci/2026-10-06 --file {filepath} --score

铁律：禁止编造，搜不到留空；重要信息 2 个独立来源交叉确认。
完成后返回：org_id、最终 completeness_score、来源数、缺失字段列表（一行式简短汇报）。"""
    print(p)


def check(org_id):
    filepath = f"{BASE}/orgs/{org_id}.json"
    try:
        with open(filepath, encoding="utf-8") as f:
            d = json.load(f)
    except Exception as e:
        print(f"FAIL {org_id}: JSON broken: {e}")
        sys.exit(1)
    bi = d.get("basic_info", {})
    cm = d.get("collection_meta", {})
    score = cm.get("completeness_score", 0)
    quotes = cm.get("quotes") or []
    n_ev = len(d.get("recent_events") or [])
    n_kp = len(d.get("key_people") or [])
    phase = cm.get("phase")
    ok = phase == "phase3_enriched" and n_ev >= 1 and quotes
    warn = score < 70
    print(f"{'OK ' if ok else 'FAIL'} {org_id}: score={score} phase={phase} events={n_ev} key_people={n_kp} quotes={len(quotes)}")
    if bi.get("name_original") in (None, ""):
        print(f"  WARN: name_original empty")
    if not ok:
        sys.exit(1)
    if warn:
        print(f"  WARN: score < 70")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build_progress()
    elif cmd == "prompt":
        prompt_for(sys.argv[2])
    elif cmd == "check":
        check(sys.argv[2])
    elif cmd == "advance":
        # move org from current -> completed, update timestamp
        org_id = sys.argv[2]
        with open(PROGRESS, encoding="utf-8") as f:
            p = json.load(f)
        if org_id in p["current"]:
            p["current"].remove(org_id)
        if org_id not in p["completed"]:
            p["completed"].append(org_id)
        p["last_updated"] = "2026-10-06"
        with open(PROGRESS, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)
        print(f"advanced: {org_id} | completed={len(p['completed'])}/{102 - len(p['remaining'])} remaining={len(p['remaining'])}")
    elif cmd == "mark":
        # mark started: move from remaining -> current
        org_id = sys.argv[2]
        with open(PROGRESS, encoding="utf-8") as f:
            p = json.load(f)
        if org_id in p["remaining"]:
            p["remaining"].remove(org_id)
        if org_id not in p["current"]:
            p["current"].append(org_id)
        with open(PROGRESS, "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=2)
        print(f"marked: {org_id} in flight")
    else:
        raise SystemExit("unknown cmd")
