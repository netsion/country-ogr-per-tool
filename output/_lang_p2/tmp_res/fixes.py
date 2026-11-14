import io, json
base = r"D:/ai-workspace/apec-osint-tool/output/_lang_p2/tmp_res"
def fix(path, i, newzh):
    lines = []
    with io.open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            if rec["i"] == i:
                rec["zh"] = newzh
            lines.append(json.dumps(rec, ensure_ascii=False))
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
fix(base + "/batch_007_r2.jsonl", 6701, "保罗-亨利·桑达奥戈·达米巴")
fix(base + "/batch_008_r2.jsonl", 7622, "艾哈迈德·本·萨勒曼·穆萨拉姆")
fix(base + "/batch_008_r2.jsonl", 7732, "优素福·本·艾哈迈德·贾拉赫马")
print("fixes applied")
