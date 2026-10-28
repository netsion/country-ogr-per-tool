# -*- coding: utf-8 -*-
"""P4 avatar patch agent A - B_badurl group: write photos + update profile JSONs."""
import json, os, shutil

BASE = os.path.dirname(os.path.abspath(__file__))
MAGIC = [(b"\xff\xd8\xff", "jpg"), (b"\x89PNG\r\n\x1a\n", "png")]

def sniff_ext(path):
    with open(path, "rb") as f:
        head = f.read(12)
    if len(head) < 3072 + 12:
        pass
    for m, ext in MAGIC:
        if head.startswith(m):
            return ext
    if head[0:4] == b"RIFF" and head[8:12] == b"WEBP":
        return "webp"
    return None

def load(pid):
    return json.load(open(os.path.join(BASE, "persons", pid + ".json"), encoding="utf-8"))

def save(pid, p):
    with open(os.path.join(BASE, "persons", pid + ".json"), "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)
        f.write("\n")

# --- 1. write validated photos ---
photo_jobs = [
    ("BO-PERSON-000100", os.path.join(BASE, "_b_cand_000100_opinion.jpg"),
     "https://www.opinion.com.bo/media/opinion/images/2017/05/18/2017N219595.jpg"),
    ("BO-PERSON-000458", os.path.join(BASE, "_b_cand_000458_lupo2.jpeg"),
     "https://www.aldeasinfantiles.org.bo/getmedia/a2a15ff4-eae8-4a39-a21e-9499c9de56bb/ALFONSO-LUPO-2.jpeg"),
]
for pid, srcfile, newurl in photo_jobs:
    ext = sniff_ext(srcfile)
    size = os.path.getsize(srcfile)
    assert ext in ("jpg", "png", "webp") and size >= 3072, (pid, ext, size)
    dst = os.path.join(BASE, "photos", pid + "." + ext)
    shutil.copyfile(srcfile, dst)
    p = load(pid)
    old = p["profile"].get("source_url")
    p["profile"]["source_url"] = newurl
    save(pid, p)
    print("[OK] %s photo=%s (%d bytes, %s) | source_url: %s -> %s" % (pid, os.path.basename(dst), size, ext, str(old)[:70], newurl))

# --- 2. null out the two without legit direct image links ---
NULL_NOTE = "社交页链接不可作头像源，未找到可直取肖像"
for pid in ("BO-PERSON-000065", "BO-PERSON-000350"):
    p = load(pid)
    old = p["profile"].get("source_url")
    p["profile"]["source_url"] = None
    p["profile"]["profile_note"] = NULL_NOTE
    save(pid, p)
    print("[NULL] %s | source_url: %s -> None | profile_note=%s" % (pid, str(old)[:70], NULL_NOTE))
