import json, os, subprocess

BASE = r"D:\ai-workspace\apec-osint-tool"
PROXY = "http://127.0.0.1:7897"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"

AVATARS = {
    "NG-PERSON-000017": "https://statehouse.gov.ng/wp-content/uploads/2026/02/Kyari.jpeg",
    "NG-PERSON-000130": "https://upload.wikimedia.org/wikipedia/commons/e/e5/Joseph_Tegbe.jpg",
    "NG-PERSON-000140": "https://dailytrust.com/wp-content/uploads/2024/11/ata.jpg",
    "NG-PERSON-000159": "https://amcow-online.org/wp-content/uploads/2025/09/Joseph-Utsev-Nigeria-minister-1-996x1024.jpg",
    "NG-PERSON-000167": "https://cdn.punchng.com/wp-content/uploads/2025/10/01080432/The-Minister-of-Labour-Employment-Muhammed-Maigari-Dingyadi.png",
    "NG-PERSON-000168": "https://6thchildlabourconf.org/wp-content/uploads/2026/02/Nkeiruka-Onyejeocha.jpeg",
    "NG-PERSON-000172": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEjgt7Xtba6t7cQZX6nfbEp1B8832HGVKgyW4BjRDd9ETibhAPxVIddlP_mKsSBtXMBTOhOCA_A2mbCVbfHl55Q8C217ffcN-tGLuEH170r9y5kuG2jT98WtTRrcoTyzow-aZ34M1lr7H50/s0/FB_IMG_1598529993068.jpg",
    "NG-PERSON-000173": "https://regionaldev.gov.ng/wp-content/uploads/2025/06/Engr.-Abubakar-Momoh-1.jpg",
    "NG-PERSON-000174": "https://regionaldev.gov.ng/wp-content/uploads/2025/06/H.E.-Uba-Maigari-Ahmadu.jpg",
    "NG-PERSON-000183": "https://statehouse.gov.ng/wp-content/uploads/2026/01/images-1.jpeg",
    "NG-PERSON-000201": "https://cdn.punchng.com/wp-content/uploads/2025/07/16010023/Bashir-Adewale-Adeniyi.png",
    "NG-PERSON-000212": "https://ncc.gov.ng/sites/default/files/styles/large/public/2024-10/evc_maida_large.jpg",
    "NG-PERSON-000226": "https://news.cac.gov.ng/wp-content/uploads/2026/08/WhatsApp-Image-2026-08-10-at-17.40.00.jpeg",
    "NG-PERSON-000233": "https://leadership.ng/wp-content/uploads/2023/09/IMG-20230917-WA0014.jpg",
    "NG-PERSON-000237": "https://fmyd.gov.ng/wp-content/uploads/2024/11/WhatsApp-Image-2024-11-25-at-12.01.44-1.jpeg",
    "NG-PERSON-000268": "https://tcn.org.ng/images/profiles/sule.JPG",
    "NG-PERSON-000273": "https://ndphc.net/assets/img/jennifer%20adighije.jpg",
    "NG-PERSON-000281": "https://leadership.ng/wp-content/uploads/2025/04/IMG-20250404-WA0042.jpg",
    "NG-PERSON-000293": "https://statecraftinc.com/wp-content/uploads/Tola-Odeyemi.png",
    "NG-PERSON-000311": "https://www.dangote.com/wp-content/uploads/2026/06/Olakunle-Alake.jpg",
    "NG-PERSON-000312": "https://www.dangote.com/wp-content/uploads/2026/06/DVG-Edwin.jpg",
}

# fallbacks to try if original fails (original-size variants)
FALLBACK = {
    "NG-PERSON-000237": "https://fmyd.gov.ng/wp-content/uploads/2024/11/WhatsApp-Image-2024-11-25-at-12.01.44-1-768x960.jpeg",
    "NG-PERSON-000159": "https://amcow-online.org/wp-content/uploads/2025/09/Joseph-Utsev-Nigeria-minister-1-740x740.jpg",
}

def head_check(url):
    r = subprocess.run(
        ["curl", "-s", "-o", os.devnull, "-x", PROXY, "-A", UA, "--max-time", "40",
         "-w", "%{http_code} %{content_type}", url],
        capture_output=True)
    out = r.stdout.decode("utf-8", "replace")
    parts = out.split(" ", 1)
    code = parts[0]
    ctype = parts[1] if len(parts) > 1 else ""
    return code, ctype

results = {}
for pid, url in AVATARS.items():
    code, ctype = head_check(url)
    ok = code == "200" and ctype.startswith("image/")
    if not ok and pid in FALLBACK:
        code2, ctype2 = head_check(FALLBACK[pid])
        if code2 == "200" and ctype2.startswith("image/"):
            results[pid] = {"url": FALLBACK[pid], "http": code2, "ctype": ctype2, "used_fallback": True}
            print(pid, "FALLBACK", code2, ctype2, flush=True)
            continue
    results[pid] = {"url": url, "http": code, "ctype": ctype, "ok": ok, "used_fallback": False}
    print(pid, code, ctype[:40], "OK" if ok else "FAIL", flush=True)

with open(os.path.join(BASE, "scripts_tmp", "_a1_verified.json"), "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=1)

bad = [p for p, v in results.items() if not v.get("ok")]
print("BAD:", bad)
