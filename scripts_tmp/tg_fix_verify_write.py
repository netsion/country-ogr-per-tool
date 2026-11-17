# -*- coding: utf-8 -*-
"""修复 verify_qids.py --write 的两个副作用：
1. 顶层结构被拍平成裸数组 -> 恢复 {metadata, organizations, summary}（metadata/summary 取自备份）
2. 4 个无国家过滤的错误 QID 匹配（意大利/智利/中国/法国实体）-> 回退，仅保留 2 个核验通过的
"""
import json
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r"D:\ai-workspace\apec-osint-tool\output\tg\2026-11-16"
BAK = BASE + r"\_tmp\_target_orgs.pre_verify.bak.json"
CUR = BASE + r"\_target_orgs.json"

# SPARQL P17 核验通过的仅此两个
GOOD_QIDS = {"Q115236251", "Q140444821"}

bak = json.load(open(BAK, encoding="utf-8"))
cur = json.load(open(CUR, encoding="utf-8"))

reverted = []
kept = []
for org in cur:
    qid = org.pop("qid", None)  # 统一折叠回 wikidata_qid 字段
    if qid and qid in GOOD_QIDS:
        if not org.get("wikidata_qid"):
            org["wikidata_qid"] = qid
            kept.append((org["id"], qid))
    elif qid:
        reverted.append((org["id"], qid))

out = {
    "metadata": bak.get("metadata", {}),
    "organizations": cur,
    "summary": bak.get("summary", {}),
}
with open(CUR, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# 验证
chk = json.load(open(CUR, encoding="utf-8"))
assert isinstance(chk, dict) and len(chk["organizations"]) == 88, "structure check failed"
residual = [o["id"] for o in chk["organizations"] if "qid" in o]
assert not residual, f"stray qid fields: {residual}"
print("metadata keys:", list(chk["metadata"].keys()))
print("summary keys:", list(chk["summary"].keys()))
print("kept (good):", kept)
print("reverted (bogus):", reverted)
print("orgs:", len(chk["organizations"]))
print("OK")
