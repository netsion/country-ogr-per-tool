import json, os

BASE = r"D:\ai-workspace\apec-osint-tool"
PDIR = os.path.join(BASE, "output", "ng", "2026-11-10", "persons")

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

MISSING_NOTES = {
    "NG-PERSON-000163": "未找到可验证直链",
    "NG-PERSON-000185": "未找到可验证直链",
}

NOTE = "[2026-11-15 头像补弱轮] 未找到可验证直链"

changed = []
for pid, url in AVATARS.items():
    p = os.path.join(PDIR, pid + ".json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    prof = d.get("profile")
    if prof is None:
        print(pid, "NO profile object, skip")
        continue
    old = prof.get("source_url")
    prof["source_url"] = url
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    changed.append(pid)
    print(pid, "source_url:", old, "->", url[:80], flush=True)

for pid in MISSING_NOTES:
    p = os.path.join(PDIR, pid + ".json")
    with open(p, encoding="utf-8") as f:
        d = json.load(f)
    cm = d.get("collection_meta")
    if cm is None:
        cm = {}
        d["collection_meta"] = cm
    notes = cm.get("notes") or ""
    if NOTE not in notes:
        cm["notes"] = (notes + " " + NOTE).strip() if notes else NOTE
    with open(p, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(pid, "note appended", flush=True)

print("SUMMARY: updated", len(changed), "source_url;", len(MISSING_NOTES), "notes appended")
