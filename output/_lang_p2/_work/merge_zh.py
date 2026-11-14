# Merge a zh-dict (key = input index as string, missing => null) with an input batch,
# writing results in identical order/count. Usage:
#   python -I merge_zh.py <input_batch.json> <zh_dict.json> <output_results.json>
import json, sys

inp, dic, out = sys.argv[1], sys.argv[2], sys.argv[3]
batch = json.load(open(inp, encoding="utf-8"))
overrides = json.load(open(dic, encoding="utf-8"))

results = []
missing = 0
for e in batch:
    key = str(e["i"])
    zh = overrides.get(key)
    if zh is None:
        missing += 1
    results.append({"i": e["i"], "zh": zh})

with open(out, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, separators=(",", ":"))

assert len(results) == len(batch), "count mismatch"
print(f"OK wrote {out}: {len(results)} entries, null={missing}, non-null={len(results)-missing}")
