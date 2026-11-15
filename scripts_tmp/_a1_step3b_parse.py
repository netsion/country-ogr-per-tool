import json, os, re

BASE = r"D:\ai-workspace\apec-osint-tool"
TMP = os.path.join(BASE, "_tmp", "a1_pages")

KEYWORDS = {
    "kyari_fmino": ["kyari", "minister"],
    "fcda": ["dauda", "yunana", "executive", "secretary", "fcda"],
    "ncc": ["maida", "evc", "executive", "commissioner"],
    "youth": ["olawande", "wisdom", "minister", "youth"],
    "nipost": ["odeyemi", "tola", "postmaster", "ceo"],
    "cac": ["ida", "ibrahim", "chairman", "board"],
}

IMG_RE = re.compile(r'<img[^>]+(?:src|data-src|data-lazy-src|data-srcset)=["\']([^"\']+)["\']', re.I)
OG_RE = re.compile(r'property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']', re.I)

out_lines = []
for key, kws in KEYWORDS.items():
    p = os.path.join(TMP, key + ".html")
    if not os.path.exists(p):
        continue
    html = open(p, encoding="utf-8", errors="replace").read()
    imgs = IMG_RE.findall(html) + OG_RE.findall(html)
    out_lines.append("=" * 30 + " " + key + " (%d imgs)" % len(imgs))
    for u in imgs:
        low = u.lower()
        if any(k in low for k in kws) or "/wp-content/uploads/" in low:
            out_lines.append("   " + u[:220])

res = "\n".join(out_lines)
print(res[:6000])
with open(os.path.join(BASE, "scripts_tmp", "_a1_imgs.txt"), "w", encoding="utf-8") as f:
    f.write(res)
