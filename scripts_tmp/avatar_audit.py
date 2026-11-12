# -*- coding: utf-8 -*-
"""Global avatar audit across all country datasets (read-only).

Checks per person/org profile:
  1. source_url classification: wikimedia_direct / wiki_file_page / qid_page /
     social_page / other_direct_image / html_page / malformed / null
     + malformed profile objects (string instead of dict)
  2. local_path: existence, naming (must equal <ID>.<ext>), location
     (root photos/ vs persons/photos/ vs other)
  3. download gap: fetchable direct link but no local file
  4. photo-dir inventory: orphan files (referenced by nobody)

Outputs (UTF-8):
  output/_avatar_audit/audit_result.json   full detail
  output/_avatar_audit/report.md           human summary
"""
import glob
import json
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = "D:/ai-workspace/apec-osint-tool/output"
OUT_DIR = os.path.join(BASE, "_avatar_audit")

IMG_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".svg", ".tif", ".tiff",
           ".ico", ".jfif", ".avif"}
# exact host -> social PAGE (profile/video pages, expiring CDN, token-gated APIs)
SOCIAL_HOST_EXACT = {"x.com", "www.x.com", "twitter.com", "www.twitter.com",
                     "facebook.com", "www.facebook.com", "m.facebook.com",
                     "graph.facebook.com", "lookaside.fbsbx.com",
                     "instagram.com", "www.instagram.com",
                     "linkedin.com", "www.linkedin.com",
                     "youtube.com", "www.youtube.com", "youtu.be",
                     "tiktok.com", "www.tiktok.com",
                     "telegram.org", "t.me", "threads.com", "www.threads.net", "www.threads.net"}
SOCIAL_HOST_SUFFIX = (".facebook.com", ".fbcdn.net", ".cdninstagram.com", ".x.com",
                      ".twitter.com", ".instagram.com", ".linkedin.com", ".youtube.com",
                      ".tiktok.com", ".fbsbx.com")
PERSON_STEM = re.compile(r"^[A-Z]{2}-PERSON-\d+$")
ORG_STEM = re.compile(r"^[A-Z]{2}-(GOV|CORP|ACAD|MEDIA|NGO|PARTY|BANK|ORG|SOE|THINK|INTL)-\d+$")

WIKIMIDIA_UPLOAD = ("upload.wikimedia.org", "thumb.wikimedia.org", "maps.wikimedia.org")


def host_is_social(netloc):
    n = netloc.lower()
    n = n.split(":")[0]
    if n in SOCIAL_HOST_EXACT:
        return True
    # img.youtube.com is a thumbnail CDN, not a page — allow as direct image
    if n == "img.youtube.com" or n.endswith(".img.youtube.com"):
        return False
    return n.endswith(SOCIAL_HOST_SUFFIX)


FB_GRAPH_PICTURE_RE = re.compile(r"^https?://graph\.facebook\.com/[^/]+/picture\b", re.I)


def classify_url(url):
    if url is None or (isinstance(url, str) and not url.strip()):
        return "null"
    if not isinstance(url, str):
        return "wrong_type"
    u = url.strip()
    low = u.lower()
    if u.startswith("data:"):
        return "data_uri"
    if not low.startswith(("http://", "https://")):
        return "malformed_no_scheme"
    if "wikidata.org" in low and re.search(r"/wiki/q\d+|entitydata|/q\d+($|/|\?)", low):
        return "qid_page"
    if "/wiki/file:" in low or "/wiki/image:" in low:
        return "wiki_file_page"
    netloc = low.split("/")[2]
    if any(n == netloc or netloc.endswith("." + n) for n in WIKIMIDIA_UPLOAD):
        return "wikimedia_direct"
    ext = os.path.splitext(low.split("?")[0])[1]
    if ext in IMG_EXT:
        return "other_direct_image"
    if FB_GRAPH_PICTURE_RE.match(u):
        # live image API endpoint (returns image/jpeg) — a valid direct source
        return "other_direct_image"
    if host_is_social(netloc):
        return "social_page"
    return "html_page"


def resolve_local(ds_root, lp):
    """Resolve local_path; return abs path.

    Layouts:
      - minio-store/...  -> relative to PROJECT ROOT (parent of output/)
      - output/<cc>/<date>/... -> normalized onto dataset
      - anything else -> relative to dataset root (legacy)
    """
    if not isinstance(lp, str) or not lp.strip():
        return None
    lp = lp.replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", lp):
        return os.path.normpath(lp)
    if lp.startswith("minio-store/"):
        return os.path.normpath(os.path.join(os.path.dirname(BASE), lp))
    m = re.match(r"^output/([a-z]{2}/\d{4}-\d{2}-\d{2})/(.*)$", lp, re.I)
    if m:
        return os.path.normpath(os.path.join(BASE, m.group(1), m.group(2)))
    return os.path.normpath(os.path.join(ds_root, lp))


def loc_class(ds_root, full):
    root_rel = os.path.relpath(full, os.path.dirname(BASE)).replace("\\", "/")
    if root_rel.startswith("minio-store/"):
        return "minio_store", root_rel
    rel = os.path.relpath(full, ds_root).replace("\\", "/")
    if rel.startswith("persons/photos/"):
        return "persons_photos", rel
    if rel.startswith("photos/"):
        return "root_photos", rel
    if rel.startswith("orgs/"):
        return "orgs_dir", rel
    return "other", rel


def audit_entity(ds_root, kind, issues, inv):
    ids = []
    for f in sorted(glob.glob(os.path.join(ds_root, kind, "*.json"))):
        eid = os.path.splitext(os.path.basename(f))[0]
        ids.append(eid)
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            issues.append({"file": f, "kind": kind, "type": "json_error", "detail": str(e)})
            continue
        real_id = d.get("person_id") or d.get("org_id")
        if real_id and real_id != eid:
            issues.append({"file": f, "kind": kind, "type": "id_mismatch",
                           "detail": f"filename={eid} field={real_id}"})
        p = d.get("profile")
        if p is None:
            issues.append({"file": f, "kind": kind, "type": "no_profile"})
            continue
        if not isinstance(p, dict):
            vt = "url_like" if isinstance(p, str) and p.startswith("http") else "text_like"
            issues.append({"file": f, "kind": kind, "type": "malformed_profile",
                           "value_type": vt, "detail": str(p)[:120]})
            continue
        su, lp = p.get("source_url"), p.get("local_path")
        cls = classify_url(su)
        if cls not in ("null", "wikimedia_direct", "other_direct_image"):
            issues.append({"file": f, "kind": kind, "type": "bad_source_url",
                           "class": cls, "detail": str(su)[:200]})
        if lp:
            full = resolve_local(ds_root, lp)
            ok = os.path.isfile(full)
            stem, ext = os.path.splitext(os.path.basename(full))
            loc, rel = loc_class(ds_root, full)
            if not ok:
                issues.append({"file": f, "kind": kind, "type": "local_missing",
                               "detail": rel})
            else:
                inv["referenced"].add(full.lower())
            name_ok = stem == eid and ext.lower() in IMG_EXT
            if not name_ok:
                issues.append({"file": f, "kind": kind, "type": "bad_naming",
                               "detail": f"{rel} (expected {eid}.<img-ext>)"})
            if kind == "persons" and ok and loc not in ("persons_photos", "minio_store"):
                issues.append({"file": f, "kind": kind, "type": "wrong_location",
                               "detail": rel})
        # download gap: direct link, no existing local file
        has_local = bool(lp) and os.path.isfile(resolve_local(ds_root, lp))
        if cls in ("wikimedia_direct", "other_direct_image") and not has_local:
            issues.append({"file": f, "kind": kind, "type": "download_gap",
                           "detail": str(su)[:250]})
    return set(ids)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    inv = {"referenced": set()}
    all_issues = []
    per_ds = {}
    datasets = sorted(glob.glob(os.path.join(BASE, "[a-z][a-z]", "20*")))
    for ds in datasets:
        rel = os.path.relpath(ds, BASE).replace("\\", "/")
        person_ids = audit_entity(ds, "persons", all_issues, inv)
        _ = audit_entity(ds, "orgs", all_issues, inv)
        per_ds[rel] = {
            "persons": len(glob.glob(os.path.join(ds, "persons", "*.json"))),
            "orgs": len(glob.glob(os.path.join(ds, "orgs", "*.json"))),
        }
        # unreferenced photo files
        orphans, wrong_name_files = [], []
        for photos_dir in (os.path.join(ds, "photos"), os.path.join(ds, "persons", "photos"),
                           os.path.join(ds, "orgs", "photos")):
            for pf in glob.glob(os.path.join(photos_dir, "*")):
                if not os.path.isfile(pf):
                    continue
                if pf.lower() not in inv["referenced"]:
                    orphans.append(os.path.relpath(pf, ds).replace("\\", "/"))
        per_ds[rel]["orphan_files"] = orphans

    # summary
    from collections import Counter
    cnt = Counter(i["type"] for i in all_issues)
    url_cls = Counter(i.get("class") for i in all_issues if i["type"] == "bad_source_url")
    summary = {"datasets": len(datasets), "issues_total": len(all_issues),
               "by_type": dict(cnt), "bad_url_classes": dict(url_cls)}

    with open(os.path.join(OUT_DIR, "audit_result.json"), "w", encoding="utf-8") as fh:
        json.dump({"summary": summary, "per_dataset": per_ds, "issues": all_issues},
                  fh, ensure_ascii=False, indent=1)

    dl = [{"file": i["file"], "url": i["detail"]} for i in all_issues if i["type"] == "download_gap"]
    with open(os.path.join(OUT_DIR, "download_candidates.json"), "w", encoding="utf-8") as fh:
        json.dump(dl, fh, ensure_ascii=False, indent=1)

    print("datasets:", len(datasets))
    print("issues_total:", len(all_issues))
    for k, v in cnt.most_common():
        print(f"  {k:20} {v}")
    print("bad_url_classes:", dict(url_cls))
    print("orphans:", sum(len(v["orphan_files"]) for v in per_ds.values()))
    print("reports ->", OUT_DIR)


if __name__ == "__main__":
    main()
