# A2 Task2: apply badlink fixes
import json

BASE = "output/ng/2026-11-10/persons/"

def load(pid):
    return json.load(open(BASE + pid + ".json", encoding="utf-8"))

def save(pid, d):
    json.dump(d, open(BASE + pid + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(BASE + pid + ".json", "a", encoding="utf-8").close()

def append_note(d, text):
    notes = d.get("collection_meta", {}).get("notes") or ""
    if not notes.endswith("\n"):
        notes += "\n"
    d.setdefault("collection_meta", {})["notes"] = notes + text

# 1) replacements
repl = [
    ("NG-PERSON-000325",
     "https://www.airtel.africa/sites/default/files/2025-05/dinesh-balsingh-1.jpg",
     "2026-11-15 坏链复核：原头像直链 independent.ng/wp-content/uploads/Airtel-Dinesh-Balsingh-1.jpg 因 403 反盗链失效（浏览器可访问，curl 携 UA 仍 403）；已替换为 Airtel Africa 官网领导层页原图直链（HTTP 200，image/jpeg，76KB），并经人工目检确认为本人官方就任照。"),
    ("NG-PERSON-000465",
     "https://www.bfxsummits.com/17africabanksummit/wp-content/uploads/2026/04/Eduofon-Japhet.jpg",
     "2026-11-15 坏链复核：原头像直链 squadco.com/assets/Edu.png 因 403 反盗链失效（squadco.com 全站对爬虫返回 403）；已替换为 Africa Bank Summit (bfxsummits.com) 讲者页官方头像直链（HTTP 200，image/jpeg），页面讲者栏明确标注 Eduofon Japhet / Managing Director / HabariPay，并经人工目检确认为本人（着 Squad by GTCo 工作服）。"),
    ("NG-PERSON-000533",
     "https://www.ripplesnigeria.com/wp-content/uploads/2024/11/Ezeokenwa-as-APGA-chairman.jpg",
     "2026-11-15 坏链复核：原头像直链 thecable.ng/wp-content/uploads/2024/11/Sylvester-Ezeokenwa-.webp 因 403 反盗链失效；已替换为 Ripples Nigeria 新闻配图直链（HTTP 200，image/jpeg，150KB），原发布页图文对应 APGA 全国主席 Ezeokenwa（着 APGA 标识服饰），并经人工目检确认。"),
    ("NG-PERSON-000596",
     "https://cdn.nairametrics.com/wp-content/uploads/2025/08/undefined-20.jpg",
     "2026-11-15 坏链复核：原头像直链 independent.ng/wp-content/uploads/Oyetan-STANBIC.jpg 因 403 反盗链失效（浏览器可访问，curl 携 UA 仍 403）；已替换为 Nairametrics《Meet the CEOs of the largest Pension Funds in Nigeria》(2025-08-17) 一文 Oyetan 章节配图直链（HTTP 200，image/jpeg），并经人工目检确认为本人肖像。"),
]
for pid, newurl, note in repl:
    d = load(pid)
    old = d["profile"]["source_url"]
    assert old, pid
    d["profile"]["source_url"] = newurl
    append_note(d, note)
    save(pid, d)
    print(pid, ":", old, "->", newurl)

# 2) 000476 note only
pid = "NG-PERSON-000476"
d = load(pid)
append_note(d, "2026-11-15 坏链复核：头像直链 wemaprodstorage.blob.core.windows.net 返回 HTTP 200 但 content-type 标注为 application/octet-stream（Azure Blob 存储未设 MIME）；实际下载 42869 字节、文件头为 JPEG(ff d8 ff e0)，可直接下载使用，视为有效链接，链接不变。")
save(pid, d)
print(pid, ": note appended, url unchanged:", d["profile"]["source_url"])
