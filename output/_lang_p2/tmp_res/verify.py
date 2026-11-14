import io, json, re, sys
base = r"D:/ai-workspace/apec-osint-tool/output/_lang_p2"
ok = True
total_null = 0
total = 0
# leftover Arabic script chars, or half-sentence issues
arabic = re.compile(r'[\u0600-\u06FF\u0750-\u077F]')
trad = re.compile(r'[爾萊內國萬細條裡風應當為實現龜觀點這個說沒開關門問間]')
for num in ["006", "007", "008", "009", "010"]:
    with io.open(f"{base}/batches/batch_{num}.json", encoding="utf-8") as f:
        src = json.load(f)
    with io.open(f"{base}/results/batch_{num}.json", encoding="utf-8") as f:
        res = json.load(f)
    assert isinstance(res, list) and len(res) == 1000 == len(src), (num, len(res))
    nulls = 0
    for s, r in zip(src, res):
        total += 1
        assert s["i"] == r["i"], (num, s["i"], r["i"])
        assert set(r.keys()) == {"i", "zh"}, (num, r.keys())
        z = r["zh"]
        if z is None:
            nulls += 1
        else:
            assert isinstance(z, str) and z.strip(), (num, r["i"])
            if arabic.search(z):
                print("ARABIC leftover:", num, r["i"], z); ok = False
            if trad.search(z):
                print("TRADITIONAL char:", num, r["i"], z); ok = False
    total_null += nulls
    print(f"batch_{num}: 1000 ok, nulls={nulls}")
print("TOTAL:", total, "nulls:", total_null, "ALL OK" if ok else "PROBLEMS FOUND")
