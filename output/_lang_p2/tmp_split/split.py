import json, sys, io
base = r"D:/ai-workspace/apec-osint-tool/output/_lang_p2"
num = sys.argv[1]
with io.open(f"{base}/batches/batch_{num}.json", encoding="utf-8") as f:
    items = json.load(f)
assert len(items) == 1000, len(items)
CH = 250
for k in range(4):
    part = items[k*CH:(k+1)*CH]
    with io.open(f"{base}/tmp_split/batch_{num}_p{k}.json", "w", encoding="utf-8", newline="\n") as f:
        for it in part:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
print(num, "ok", len(items))
