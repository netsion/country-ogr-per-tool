# -*- coding: utf-8 -*-
"""Social media scan for P. Jose Fuentes Cano (6 platforms)."""
import re
import subprocess
import json
import html as H

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
PROXY = "http://127.0.0.1:7890"


def fetch(url, extra=None, timeout=40):
    cmd = ["curl", "-s", "-L", "-m", str(timeout), "-x", PROXY, "-A", UA,
           "-w", "\n===HTTP:%{http_code}===", url]
    if extra:
        cmd += extra
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=timeout + 10)
        return r.stdout.decode("utf-8", errors="ignore")
    except Exception as e:
        return "FETCH_ERR " + str(e)


def strip(s):
    return re.sub(r"\s+", " ", re.sub("<[^>]+>", " ", s)).strip()


def main():
    name_q = "%22Jos%C3%A9+Fuentes+Cano%22"
    name_raw = "José Fuentes Cano"

    # 1. YouTube
    t = fetch(f"https://www.youtube.com/results?search_query={name_q}")
    vids = re.findall(r'"videoRenderer":\{"videoId":"([^"]{11})".*?"title":\{"runs":\[\{"text":"((?:[^"\\]|\\.)*)"', t)
    chans = re.findall(r'"channelRenderer":\{"channelId":"([^"]+)".*?"simpleText":"((?:[^"\\]|\\.)*)"', t)
    http = re.search(r"===HTTP:(\d+)===", t)
    print("[youtube] http=", http.group(1) if http else "?", "videos=", len(vids), "channels=", len(chans))
    for v, title in vids[:8]:
        print("  video:", "https://www.youtube.com/watch?v=" + v, "|", title.encode().decode("unicode_escape", errors="ignore")[:100])
    for c, title in chans[:5]:
        print("  channel:", "https://www.youtube.com/channel/" + c, "|", title[:100])

    # 2. Facebook public directory
    t = fetch("https://www.facebook.com/public/Jos%C3%A9-Fuentes-Cano")
    http = re.search(r"===HTTP:(\d+)===", t)
    entries = re.findall(r'href="(https://www\.facebook\.com/[^"]+)"[^>]*>\s*(?:<[^>]+>)*([^<]{4,80})', t)
    print("[facebook] http=", http.group(1) if http else "?", "entries=", len(entries))
    seen = set()
    for u, n in entries:
        if "login" in u or u in seen or "policy" in u or "help" in u:
            continue
        seen.add(u)
        print("  ", u[:100], "|", strip(n)[:80])
        if len(seen) > 10:
            break
    if "checkpoint" in t or "login" in t[:3000]:
        print("  (login wall likely)")

    # 3. Instagram topsearch API
    t = fetch("https://www.instagram.com/web/search/topsearch/?context=blended&query=jose%20fuentes%20cano")
    http = re.search(r"===HTTP:(\d+)===", t)
    body = re.sub(r"===HTTP:\d+===", "", t)
    print("[instagram] http=", http.group(1) if http else "?", "len=", len(body))
    try:
        j = json.loads(body)
        users = j.get("users", [])
        for u in users[:8]:
            us = u.get("user", {})
            print("  user: https://www.instagram.com/" + us.get("username", ""), "|", us.get("full_name", ""), "| verified:", us.get("is_verified"))
    except Exception as e:
        print("  parse fail:", e, body[:200])

    # 4. LinkedIn people search (public dir)
    t = fetch("https://www.linkedin.com/pub/dir/Jos%C3%A9-Fuentes-Cano")
    http = re.search(r"===HTTP:(\d+)===", t)
    print("[linkedin] http=", http.group(1) if http else "?", "len=", len(t))
    profs = re.findall(r'href="(https://[a-z.]*linkedin\.com/in/[A-Za-z0-9_%-]+)"', t)
    for p in list(dict.fromkeys(profs))[:8]:
        print("  profile:", p)

    # 5. X (twitter) via oembed-less search probe
    t = fetch(f"https://x.com/search?q={name_q}&f=top")
    http = re.search(r"===HTTP:(\d+)===", t)
    print("[x] http=", http.group(1) if http else "?", "len=", len(t), "| login-wall:", ("login" in t[:2000].lower()))

    # 6. TikTok search page
    t = fetch(f"https://www.tiktok.com/search?q={name_q}")
    http = re.search(r"===HTTP:(\d+)===", t)
    print("[tiktok] http=", http.group(1) if http else "?", "len=", len(t), "| captcha/js:", ("verify" in t[:3000].lower() or len(t) < 5000))


if __name__ == "__main__":
    main()
