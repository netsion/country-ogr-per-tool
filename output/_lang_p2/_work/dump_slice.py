# Dump a slice of a batch file as readable lines. Usage:
#   python -I dump_slice.py <batch.json> <start_pos> <end_pos>   (0-based positions in array)
import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

path, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
data = json.load(open(path, encoding="utf-8"))
print(f"TOTAL {len(data)}")
for e in data[a:b]:
    v = e["v"].replace("\n", " ")
    print(f"{e['i']}|{e['cat']}|{e['cc']}|{v}")
