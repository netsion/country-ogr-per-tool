# -*- coding: utf-8 -*-
"""Resolve Google News article IDs (from _gnrss_llobet.xml) to publisher URLs."""
import io
import json
import re
import sys
import time
import urllib.parse
import urllib.request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PROXY = {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
opener = urllib.request.build_opener(urllib.request.ProxyHandler(PROXY))
opener.addheaders = [
    ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"),
    ("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8"),
]

LINKS = [
    ("WWF_Peru_financiar", "CBMipAFBVV95cUxPQjR2SmF4dzdobkVyNjR1Z3hHeUE5TFNvRkd5NExXQWJZYzZ1QU5meTlQRTktQXRHS29aS1ctLXl5MjFRWDVfbG5BZ2pna015WUxGRTlvZ2V6RzlkWWhNUmdWYVdzUDlubjRSUnIyaGZHQy1vTER5UkRlU0Z4cFlaWGZXbXVWZm5hWVN3b0hHRVBzQndxeGdkRU0wXzhZWWxRUHBqaQ"),
    ("eldiario_horaplaneta2025", "CBMipgFBVV95cUxPRTRqX2R0SWtoTE9fbk96VFRHMVNES1hjZGVLOVpjYmNYODBhU0MxcmVuZFBhY0NraU9xTThodEQzZV80MFI3YjducHhsNTFSUE1mcGpHZlA1VnZmbEF1dDhFLVV2ZmxvakdkZFZ1Q1U0aVp6alo3NFY0YkNMV1BaWHJvLUVWUGNzSlNXMkFmS1phd0c0UmRIemdScXU0WUlZTFBUQVZ3"),
    ("lavozdetarija_horaplaneta2023", "CBMikAFBVV95cUxQOXJkX2c0RXg0bGNUbjU3NlB2S0ZMRXhfQjgtUnAyR2dBN0tYN3lLN1BhOUZHRDN5ZzJ2QmRhQ0QzOGRLZ09TR0g1b1BNQ0loZ1FnR0tjWktabW0xenAtVWR5WEt6d1pVem9sTXhYWGpvMEhLbWdGZFR0cHVBZXVwMlpFNmpUR25Zc3FRMTJEVTQ"),
    ("economy_horaplaneta2025", "CBMi4gFBVV95cUxNSGtEMklINTE1UzBBTG5DQ005OHhNQ1h1LXllX0ZTX0JLNTFTRi1ESkRJMHk2QXFwUzUxdWp3UE8xVElPTlFUTG9qUUY5SUtDUDkwSGJHYlNkNzV2MzVNM2gtbUJxU1ozWTdOaVB3aEpEcTJaZ1lUTVo5NlJTSmNqbDYxVWVtLW5XT1Z2ZWVHdFZoZ1Q0YUxacFBMUzJaTmZ2RHE1b2w5MUZrYTdxS0N4S3lqaTFXVmtQalZkODJCTHlucmVnem5EOHlIbDZGQXpkdDJ2WnQwTHFxbUVGVURVemZB"),
    ("eldiario_tedx", "CBMihgFBVV95cUxQX2J5cDRfWlRaTHNwd2gxWlZLR2xnWGlQNFk1N3phcmNWczdHMDBEb3Nfdmg2dUdfOVA1QUU0NGtsUkdBOEpQYTU0NkJMbWNTbTZBQ2xlMndnakthSE9jckRseW5Ja0JzeUNaQWhxRjRfY3ppVEU2ZUVIbnVuRFlLSWZEYVQ2UQ"),
    ("eldiario_trafico", "CBMirgFBVV95cUxORmVPUzgxU2xLdzZZbHk5ZHBYLV9SYnpibHZxVXNvNjNQUXlldnZwSWRlVlJmeFY4MEtHejJ6eU1paS00NElkWFFFQVBMYzc5MTlXWXB2RnhqR3dweDdyRU1yRTJaNzJIRkdSbmJsN1VaOTBfY042SEwxaHRzSklEeFpnbDd0SllLQWNkaFhDTlBNY3NzQTRSTTdwTmxtX1JuallMTVJMdUdjMHExX3c"),
]


def resolve(gn_art_id):
    inner = [
        "garturlreq",
        [
            ["es-419", "BO", [], "DEFAULT", None, None, 1, 1, "BO:es-419",
             None, 180, None, None, [], None, 0, None, [], None, 0, None,
             None, 0, None, None, 0, 0],
            None,
            None,
            [],
        ],
    ]
    payload = [[["Fbv4je", json.dumps(inner), None, "generic"]]]
    data = "f.req=" + urllib.parse.quote(json.dumps(payload))
    resp = opener.open(
        "https://news.google.com/_/DotsSplashUi/data/batchexecute",
        data=data.encode(),
        timeout=40,
    )
    txt = resp.read().decode("utf-8", "ignore")
    m = re.search(r'https?://[^"\\\[\s]+', txt)
    return m.group(0) if m else None


def main():
    for name, aid in LINKS:
        try:
            u = resolve(aid)
            print(name, "->", u if u else "NONE")
        except Exception as e:
            print(name, "ERR", repr(e)[:120])
        time.sleep(1.5)


if __name__ == "__main__":
    main()
