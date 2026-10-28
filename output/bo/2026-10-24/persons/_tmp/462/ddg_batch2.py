# -*- coding: utf-8 -*-
"""DDG batch 2: handover timing, ZoomInfo, retirement date, social accounts."""
from ddg_search import ddg

QUERIES = [
    ("site:worldvision.bo Mosquera", "q2_sitebo.html"),
    ("puntovidascc Mosquera retiro World Vision", "q2_punto.html"),
    ("ZoomInfo Alberto Mosquera World Vision Bolivia Ecuador", "q2_zoom.html"),
    ("World Vision Bolivia nuevo director nacional 2023 Juan Carlo Ramirez asume", "q2_asume.html"),
    ("World Vision Bolivia despedida Alberto Mosquera 2022", "q2_despedida.html"),
    ("Vision Mundial Bolivia 40 anos evento 2022 Alberto Mosquera", "q2_40.html"),
    ("Alberto Mosquera World Vision Bolivia linkedin", "q2_li.html"),
    ("Vision Mundial Bolivia emergencia COVID Alberto Mosquera 2020", "q2_covid.html"),
]

if __name__ == "__main__":
    for q, fn in QUERIES:
        try:
            res = ddg(q, fn)
        except Exception as e:
            print(q, "ERR", e)
            continue
        print("#" * 12, "QUERY:", q, "-> results:", len(res))
        for r in res[:9]:
            print("-", r["title"][:120])
            print(" ", r["url"][:160])
            if r["snippet"]:
                print("  S:", r["snippet"][:240])
        print()
