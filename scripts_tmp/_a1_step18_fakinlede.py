import re

html = open(r"_tmp/a1_pages/fakinlede_bits.html", encoding="utf-8", errors="replace").read()
idx = 0
count = 0
low = html.lower()
while True:
    idx = low.find("fakinlede", idx + 1)
    if idx == -1:
        break
    seg = html[max(0, idx - 800): idx + 200]
    m = re.search(r'src=["\']([^"\']+)["\']', seg[::-1][::-1])  # any src in segment
    imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:jpg|jpeg|png|webp)', seg)
    if imgs:
        count += 1
        print("--- hit", count, "---")
        for u in imgs[-3:]:
            print("   ", u[:200])
    if count >= 4:
        break
