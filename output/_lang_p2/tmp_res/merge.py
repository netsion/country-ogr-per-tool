import json, sys, io
base = r"D:/ai-workspace/apec-osint-tool/output/_lang_p2"
num = sys.argv[1]
with io.open(f"{base}/batches/batch_{num}.json", encoding="utf-8") as f:
    src = json.load(f)
out = []
for k in range(4):
    p = f"{base}/tmp_res/batch_{num}_r{k}.jsonl"
    with io.open(p, encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line: continue
            rec = json.loads(line)
            out.append(rec)
assert len(out) == len(src) == 1000, (len(out), len(src))
for s, o in zip(src, out):
    assert s["i"] == o["i"], (s["i"], o["i"])
    z = o["zh"]
    assert z is None or (isinstance(z, str) and z.strip()), (o["i"], z)
dst = f"{base}/results/batch_{num}.json"
with io.open(dst, "w", encoding="utf-8", newline="\n") as f:
    json.dump(out, f, ensure_ascii=False, separators=(",", ":"))
print(num, "merged ok ->", dst)
