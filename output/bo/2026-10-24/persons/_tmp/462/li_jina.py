# -*- coding: utf-8 -*-
"""LinkedIn fetch with bot UA + r.jina.ai reader for YouTube videos."""
import subprocess
import re
import html
import os

PROXY = "http://127.0.0.1:7890"
BASE = os.path.dirname(os.path.abspath(__file__))


def get(url, ua):
    r = subprocess.run(["curl", "-sL", "--max-time", "35", "-x", PROXY, "-A", ua,
                        "-H", "Accept-Language: es,en;q=0.8", url],
                       capture_output=True, text=True, encoding="utf-8", errors="ignore")
    return r.stdout


if __name__ == "__main__":
    li_ua = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    c = get("https://ec.linkedin.com/in/alberto-mosquera-aa210523b", li_ua)
    with open(os.path.join(BASE, "li_g.html"), "w", encoding="utf-8") as f:
        f.write(c)
    print("linkedin googlebot bytes:", len(c))
    t = re.search(r"<title>(.*?)</title>", c, re.S)
    print("title:", html.unescape(t.group(1)).strip()[:200] if t else "n/a")
    if len(c) > 20000:
        text = re.sub(r"<script.*?</script>", " ", c, flags=re.S)
        text = re.sub(r"<style.*?</style>", " ", text, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        text = html.unescape(re.sub(r"\s+", " ", text)).strip()
        print(text[:3000])

    # r.jina.ai reader for YT video description
    rj_ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    for vid in ["zeTPrJG9G80", "fSBYJjphF-U", "KBNJu9xNooU", "VjvjZlDHfpM"]:
        c = get("https://r.jina.ai/https://www.youtube.com/watch?v=" + vid, rj_ua)
        with open(os.path.join(BASE, "jina_%s.txt" % vid), "w", encoding="utf-8") as f:
            f.write(c)
        print("--- jina", vid, "bytes:", len(c))
        print(c[:600].replace("\n", " | "))
