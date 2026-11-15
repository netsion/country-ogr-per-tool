import re

html = open(r"_tmp/a1_pages/kyari_ifad.html", encoding="utf-8", errors="replace").read()
urls = set()
for m in re.finditer(r'https?://fmino\.gov\.ng/wp-content/uploads/[^"\'\s\\)]+\.(?:jpg|jpeg|png|webp)', html, re.I):
    urls.add(m.group(0))
for m in re.finditer(r'(?:data-src|data-img-url|data-lazy-srcset|srcset)=["\']([^"\']+)["\']', html):
    for u in re.findall(r'https?://[^"\'\s,]+', m.group(1)):
        if "uploads" in u:
            urls.add(u)
for u in sorted(urls):
    print(u[:220])
