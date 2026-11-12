# -*- coding: utf-8 -*-
"""social_accounts normalization migration (idempotent).

Steps per entry:
  1. platform normalize (lowercase + alias map; twitter_x/x/Twitter... -> twitter;
     bluesky/Google Scholar/... -> other; website/个人网站/email -> move to contacts)
  2. source -> source_note (rename, content preserved); source = numeric code or null
  3. fill nickname/username/user_id by URL match against the user's parsed xlsx
  4. drop extra keys (verified/followers/description/notes/handle/username/account_id...)
  5. fix URLs (add scheme, trim spaces); drop entries without url
  6. platform-url mismatch: re-detect by host; non-social websites -> contacts
  7. dedupe same normalized URL within one entity
Usage: python social_migrate.py [--dry]
"""
import glob
import json
import os
import sys
import urllib.parse

import openpyxl

sys.stdout.reconfigure(encoding="utf-8")
BASE = "D:/ai-workspace/apec-osint-tool"
XLSX = r"E:\WeCom\WXWork\1688851012089893\Cache\File\2026-11\重点国家人物组织-20261102.xlsx"
DRY = "--dry" in sys.argv

PLATFORM_CODES = {
    "twitter": 3, "facebook": 6, "instagram": 8, "youtube": 9,
    "odnoklassniki": 10, "vkontakte": 11, "weibo": 14, "reddit": 15,
    "tumblr": 16, "linkedin": 17, "telegram": 19, "whatsapp": 20,
    "line": 21, "wechat": 23, "threads": 24, "snapchat": 25, "tiktok": 29,
}
ALIAS = {
    "twitter_x": "twitter", "twitter": "twitter", "x": "twitter",
    "Twitter": "twitter", "X": "twitter", "x (twitter)": "twitter",
    "X (Twitter)": "twitter", "X/Twitter": "twitter", "Twitter/X": "twitter",
    "Twitter/X ": "twitter",
    "Facebook": "facebook", "facebook": "facebook",
    "Instagram": "instagram", "instagram": "instagram",
    "YouTube": "youtube", "youtube": "youtube",
    "LinkedIn": "linkedin", "linkedin": "linkedin",
    "TikTok": "tiktok", "tiktok": "tiktok",
    "Threads": "threads", "threads": "threads",
    "Telegram": "telegram", "telegram": "telegram",
    "weibo": "weibo", "Weibo": "weibo", "wechat": "wechat", "WeChat": "wechat",
    "github": "github", "medium": "medium", "mastodon": "mastodon",
    "substack": "substack", "gitlab": "gitlab",
    "reddit": "reddit", "tumblr": "tumblr", "whatsapp": "whatsapp",
    "line": "line", "snapchat": "snapchat",
    "odnoklassniki": "odnoklassniki", "vkontakte": "vkontakte",
    "other": "other", "Other": "other",
    # non-social / unknown -> other (see CONTACTS_MOVE for website-ish)
    "bluesky": "other", "Google Scholar": "other", "researchgate": "other",
    "orcid": "other", "Linktree": "other", "blogspot": "other",
    "WordPress": "other", "Blog": "other", "blog": "other",
    "Naver Blog": "other", "Naver blog": "other", "KakaoTalk": "other",
    "Kakao": "other",
}
CONTACTS_MOVE = {"website", "个人网站", "Website", "email"}
HOST_PLATFORM = {
    "facebook.com": "facebook", "fb.com": "facebook",
    "instagram.com": "instagram",
    "x.com": "twitter", "twitter.com": "twitter",
    "linkedin.com": "linkedin",
    "youtube.com": "youtube", "youtu.be": "youtube",
    "tiktok.com": "tiktok", "douyin.com": "tiktok",
    "t.me": "telegram", "telegram.me": "telegram",
    "threads.net": "threads", "threads.com": "threads",
    "weibo.com": "weibo", "weibo.cn": "weibo",
    "weixin.qq.com": "wechat", "wechat.com": "wechat",
    "github.com": "github",
    "medium.com": "medium", "substack.com": "substack",
    "mastodon": "mastodon", "reddit.com": "reddit",
    "tumblr.com": "tumblr", "vk.com": "vkontakte", "ok.ru": "odnoklassniki",
}
ALLOWED = {"platform", "account_name", "url", "source", "source_note",
           "nickname", "username", "user_id"}


def norm_url(u):
    """Normalized URL key for matching: strip scheme/www/trailing slash, decode."""
    if not isinstance(u, str):
        return None
    u = u.strip()
    if not u:
        return None
    u = urllib.parse.unquote(u)
    for pre in ("https://", "http://", "www."):
        if u.lower().startswith(pre):
            u = u[len(pre):]
    return u.rstrip("/").lower()


def save_json(f, d):
    tmp = f + ".tmp"
    payload = json.dumps(d, ensure_ascii=False, indent=2) + "\n"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
    os.replace(tmp, f)


def load_xlsx_map():
    wb = openpyxl.load_workbook(XLSX, read_only=True, data_only=True)
    ws = wb["Merged Data"]
    url_map = {}
    for r in ws.iter_rows(min_row=2, values_only=True):
        if not r or not r[0]:
            continue
        k = norm_url(str(r[0]))
        if not k:
            continue
        uid = str(r[8]).strip() if r[8] not in (None, "") else None
        uname = str(r[9]).strip() if r[9] not in (None, "") else None
        nick = str(r[10]).strip() if r[10] not in (None, "") else None
        if k not in url_map or (uid and uname and nick):
            url_map[k] = {"user_id": uid, "username": uname, "nickname": nick}
    return url_map


def main():
    xmap = load_xlsx_map()
    print(f"xlsx URL map: {len(xmap)} unique keys")

    stats = {
        "entries": 0, "platform_fixed": 0, "source_note_renamed": 0,
        "code_filled": 0, "matched": 0, "extra_dropped": 0,
        "url_fixed": 0, "no_url_dropped": 0, "contacts_moved": 0,
        "dedup": 0, "platform_corrected_by_host": 0,
    }
    per_cc = {}  # cc -> [entries, matched]
    for f in sorted(glob.glob(os.path.join(BASE, "output", "[a-z][a-z]", "20*",
                                           "*", "*.json"))):
        rel = os.path.relpath(f, BASE)
        if os.sep in rel and ("/persons/" not in rel.replace(os.sep, "/")
                              and "/orgs/" not in rel.replace(os.sep, "/")):
            continue
        cc = rel.replace(os.sep, "/").split("/")[1]
        d = json.load(open(f, encoding="utf-8"))
        sa = d.get("social_accounts")
        if not isinstance(sa, list) or not sa:
            continue
        contacts = d.get("contacts")
        changed = False
        out = []
        seen = {}
        for e in sa:
            if not isinstance(e, dict):
                stats["no_url_dropped"] += 1
                changed = True
                continue
            e_orig = dict(e)  # snapshot for change detection
            stats["entries"] += 1
            cc_stats = per_cc.setdefault(cc, [0, 0])
            cc_stats[0] += 1
            # --- platform normalize ---
            p_raw = e.get("platform")
            if p_raw in CONTACTS_MOVE:
                # move to contacts as website/email
                u = (e.get("url") or "").strip()
                if u:
                    ctype = "email" if (u.startswith("mailto:") or p_raw == "email") else "website"
                    if not isinstance(contacts, list):
                        contacts = d.get("contacts") or []
                    vals = {c.get("value") for c in contacts if isinstance(c, dict)}
                    if u not in vals:
                        contacts.append({"type": ctype, "value": u,
                                         "source": "migrated from social_accounts"})
                        stats["contacts_moved"] += 1
                changed = True
                continue  # drop from social_accounts
            p_new = ALIAS.get(p_raw)
            if p_new is None and isinstance(p_raw, str):
                low = p_raw.strip().lower()
                p_new = ALIAS.get(low, "other" if low not in PLATFORM_CODES else low)
            if p_new != p_raw:
                stats["platform_fixed"] += 1
            # --- url fix ---
            u = e.get("url")
            if isinstance(u, str):
                u2 = u.strip().replace(" ", "%20")
                if u2 and not u2.lower().startswith(("http://", "https://", "mailto:")):
                    u2 = "https://" + u2
                    stats["url_fixed"] += 1
                if u2 != u:
                    stats["url_fixed"] += 1
                e["url"] = u2
            if not e.get("url"):
                stats["no_url_dropped"] += 1
                changed = True
                continue
            # --- platform-url mismatch correction ---
            if p_new in HOST_PLATFORM.values() or p_new == "other":
                host = urllib.parse.urlparse(e["url"]).netloc.lower().lstrip("www.") if "://" in e["url"] else ""
                host = host.replace("www.", "", 1)
                detected = None
                for h, plat in HOST_PLATFORM.items():
                    if host == h or host.endswith("." + h):
                        detected = plat
                        break
                if detected and detected != p_new:
                    p_new = detected
                    stats["platform_corrected_by_host"] += 1
            e["platform"] = p_new
            # --- source -> source_note rename + numeric code ---
            if "source" in e and isinstance(e.get("source"), str):
                e["source_note"] = e.pop("source")
                stats["source_note_renamed"] += 1
            code = PLATFORM_CODES.get(p_new)
            if e.get("source") is None or e.get("source") != code:
                e["source"] = code
                if code is not None:
                    stats["code_filled"] += 1
            # --- fill from xlsx ---
            k = norm_url(e["url"])
            if k and k in xmap:
                m = xmap[k]
                for fld in ("user_id", "username", "nickname"):
                    v = m.get(fld)
                    if v and not e.get(fld):
                        e[fld] = v
                if any(m.get(fld) for fld in ("user_id", "username", "nickname")):
                    stats["matched"] += 1
                    cc_stats[1] += 1
            # --- drop extra keys ---
            extra = set(e.keys()) - ALLOWED
            for kx in extra:
                e.pop(kx)
            if extra:
                stats["extra_dropped"] += 1
            # --- dedupe ---
            if k and k in seen:
                stats["dedup"] += 1
                changed = True
                continue
            if k:
                seen[k] = True
            out.append(e)
            if e != e_orig:
                changed = True
        if len(out) != len(sa) or out != sa:
            changed = True
        if changed and not DRY:
            d["social_accounts"] = out
            if contacts is not None and contacts != d.get("contacts"):
                d["contacts"] = contacts
            save_json(f, d)
        elif not DRY and changed:
            pass
    print(("DRY-RUN" if DRY else "APPLIED"), stats)
    print()
    print("per-country match (entries / matched / %):")
    zero = []
    for cc, (tot, m) in sorted(per_cc.items()):
        pct = m * 100 // tot if tot else 0
        flag = ""
        if pct == 0:
            zero.append(cc)
            flag = "  <-- ZERO"
        print(f"  {cc}: {tot:5} / {m:5}  {pct:3}%{flag}")
    print()
    print("ZERO-match countries (user to supplement):", zero)


if __name__ == "__main__":
    main()
