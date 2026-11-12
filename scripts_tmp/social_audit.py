# -*- coding: utf-8 -*-
"""Deep audit of social_accounts across all datasets (read-only)."""
import glob
import json
import os
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

HOSTS = {
    "facebook": ("facebook.com", "fb.com"),
    "instagram": ("instagram.com",),
    "twitter": ("x.com", "twitter.com"),
    "linkedin": ("linkedin.com",),
    "youtube": ("youtube.com", "youtu.be", "yt.be"),
    "tiktok": ("tiktok.com",),
    "telegram": ("t.me", "telegram.me", "telegram.org"),
    "threads": ("threads.net", "threads.com"),
    "weibo": ("weibo.com", "weibo.cn"),
    "wechat": ("weixin.qq.com", "wechat.com"),
    "github": ("github.com",),
    "mastodon": ("mastodon", ".social", "mastodon.social"),
    "medium": ("medium.com",),
    "substack": ("substack.com",),
}

issues = Counter()
samples = {}
dup = 0
dup_ex = []
for f in glob.glob("output/[a-z][a-z]/20*/persons/*.json") + \
         glob.glob("output/[a-z][a-z]/20*/orgs/*.json"):
    try:
        d = json.load(open(f, encoding="utf-8"))
    except Exception:
        continue
    sa = d.get("social_accounts") or []
    seen = set()
    for e in sa:
        if not isinstance(e, dict):
            issues["entry-not-dict"] += 1
            continue
        if not e.get("platform"):
            issues["platform-missing"] += 1
        if not e.get("url"):
            issues["url-missing"] += 1
        u = (e.get("url") or "").lower()
        p = (e.get("platform") or "").lower()
        hosts = HOSTS.get(p)
        if hosts and u and not any(h in u for h in hosts):
            key = f"mismatch:{p}"
            issues[key] += 1
            samples.setdefault(key, f"{os.path.basename(f)} | {u[:70]}")
        if u and not u.startswith("http"):
            issues["url-no-scheme"] += 1
        if " " in (e.get("url") or ""):
            issues["url-has-space"] += 1
        k = u.rstrip("/").lower()
        if k and k in seen:
            dup += 1
            dup_ex.append(os.path.basename(f) + " | " + u[:60])
        seen.add(k)
        extra = set(e.keys()) - {"platform", "account_name", "url", "source"}
        if extra:
            issues["extra-keys:" + ",".join(sorted(extra))] += 1
        an = e.get("account_name")
        if isinstance(an, str) and an.startswith("http"):
            issues["account_name-is-url"] += 1
        if any(s in u for s in ("bit.ly", "t.co/", "goo.gl", "tinyurl")):
            issues["url-shortener"] += 1
        if any(x in u for x in ("utm_", "fbclid", "igshid", "igsh=")):
            issues["url-tracker-params"] += 1
        # facebook numeric-id style urls (fb.com/profile.php?id=) or /people/ pages
        if "facebook.com" in u and ("profile.php" in u or "/people/" in u):
            issues["fb-ugly-url"] += 1

print("duplicate URLs within same entity:", dup)
print("issues:")
for k, v in issues.most_common(30):
    print(f"  {v:5}  {k}")
print("samples:")
for k, s in list(samples.items())[:12]:
    print("  ", k, "->", s)
print("dup samples:")
for s in dup_ex[:5]:
    print("  ", s)
