# -*- coding: utf-8 -*-
"""Fetch helper for BO-PERSON-000316 research: direct page fetch + Bing SERP."""
import sys
import urllib.parse
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

OUT = "D:/claude-workspace/apec-osint-tool/output/bo/2026-10-24/persons/_tmp/"


def build_opener(use_proxy=True):
    handlers = []
    if use_proxy:
        handlers.append(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
    op = urllib.request.build_opener(*handlers)
    op.addheaders = [
        ("User-Agent", UA),
        ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"),
        ("Accept-Language", "es-ES,es;q=0.9,en;q=0.7"),
    ]
    return op


def fetch(url, name, use_proxy=True):
    for attempt, proxy in ((1, use_proxy), (2, not use_proxy)):
        try:
            op = build_opener(proxy)
            resp = op.open(url, timeout=45)
            raw = resp.read()
            try:
                html = raw.decode("utf-8")
            except UnicodeDecodeError:
                html = raw.decode("latin-1", "replace")
            path = OUT + name
            with open(path, "w", encoding="utf-8") as f:
                f.write("URL: " + url + "\nSTATUS: " + str(resp.status) + "\n----\n" + html)
            print("OK  [%s] proxy=%s -> %s (%d bytes)" % (name, proxy, path, len(html)))
            return True
        except Exception as e:
            print("ERR [%s] proxy=%s : %s" % (name, proxy, e))
    return False


def bing(query, name):
    q = urllib.parse.quote(query)
    return fetch("https://www.bing.com/search?q=" + q + "&setlang=es", name)


def ddg(query, name):
    q = urllib.parse.quote(query)
    return fetch("https://lite.duckduckgo.com/lite/?q=" + q, name)


if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "url":
        fetch(sys.argv[2], sys.argv[3])
    elif mode == "bing":
        bing(sys.argv[2], sys.argv[3])
    elif mode == "ddg":
        ddg(sys.argv[2], sys.argv[3])
