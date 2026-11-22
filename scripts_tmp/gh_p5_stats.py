# -*- coding: utf-8 -*-
"""P5 统计：persons/orgs 完整度分布与字段覆盖率。"""
import json, os, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"D:\claude-workspace\country-ogr-per-tool\output\gh\2026-11-17"

def load_dir(sub):
    d = os.path.join(BASE, sub)
    out = []
    for f in sorted(os.listdir(d)):
        if f.startswith("_") or not f.endswith(".json"):
            continue
        try:
            out.append(json.load(open(os.path.join(d, f), encoding="utf-8")))
        except Exception as e:
            print("PARSE FAIL", f, e)
    return out

persons = load_dir("persons")
orgs = load_dir("orgs")

def score_of(x):
    return (x.get("collection_meta") or {}).get("completeness_score")

ps = [s for s in (score_of(p) for p in persons) if isinstance(s, (int, float))]
os_ = [s for s in (score_of(o) for o in orgs) if isinstance(s, (int, float))]
ps.sort(); os_.sort()

def dist(vals, buckets):
    c = Counter()
    for v in vals:
        for lo, hi, label in buckets:
            if lo <= v <= hi:
                c[label] += 1
                break
    return c

pb = [(85, 100, "85-100"), (75, 84.999, "75-84"), (65, 74.999, "65-74"), (50, 64.999, "50-64"), (0, 49.999, "<50")]
ob = [(90, 100, "90-100"), (80, 89.999, "80-89"), (70, 79.999, "70-79"), (0, 69.999, "<70")]

print("=== PERSONS (%d) ===" % len(persons))
print("scored: %d | avg %.1f | median %.1f | min %s | max %s" % (
    len(ps), sum(ps)/len(ps), ps[len(ps)//2], ps[0], ps[-1]))
for k in ("85-100", "75-84", "65-74", "50-64", "<50"):
    print("  %-7s %3d (%.1f%%)" % (k, dist(ps, pb)[k], 100*dist(ps, pb)[k]/len(ps)))
print("  >=85: %d (%.1f%%)" % (sum(1 for s in ps if s >= 85), 100*sum(1 for s in ps if s >= 85)/len(ps)))

print("\n=== ORGS (%d) ===" % len(orgs))
print("scored: %d | avg %.1f | median %.1f | min %s | max %s" % (
    len(os_), sum(os_)/len(os_), os_[len(os_)//2], os_[0], os_[-1]))
for k in ("90-100", "80-89", "70-79", "<70"):
    print("  %-7s %3d (%.1f%%)" % (k, dist(os_, ob)[k], 100*dist(os_, ob)[k]/len(os_)))

def cov(items, getter):
    n = sum(1 for x in items if getter(x))
    return n, 100*n/len(items)

print("\n=== PERSON FIELD COVERAGE ===")
checks = [
    ("wikidata_qid", lambda p: bool(p.get("wikidata_qid"))),
    ("profile.source_url", lambda p: bool((p.get("profile") or {}).get("source_url"))),
    ("birth_date", lambda p: bool(p.get("birth_date"))),
    ("education>=1", lambda p: bool(p.get("education"))),
    ("work_experience>=3", lambda p: len(p.get("work_experience") or []) >= 3),
    ("family_members>=1", lambda p: bool(p.get("family_members"))),
    ("social_accounts>=1", lambda p: bool(p.get("social_accounts"))),
    ("contacts>=1", lambda p: bool(p.get("contacts"))),
    ("political_stances>=1", lambda p: bool(p.get("political_stances"))),
    ("major_achievements>=3", lambda p: len(p.get("major_achievements") or []) >= 3),
    ("person_relationships>=1", lambda p: bool(p.get("person_relationships"))),
    ("biography>=200字", lambda p: len(p.get("biography_summary") or "") >= 200),
    ("quotes>=3", lambda p: len((p.get("collection_meta") or {}).get("quotes") or []) >= 3),
]
for label, fn in checks:
    n, pct = cov(persons, fn)
    print("  %-26s %3d / %d  (%.0f%%)" % (label, n, len(persons), pct))

print("\n=== ORG FIELD COVERAGE ===")
ochecks = [
    ("key_people>=1", lambda o: bool(o.get("key_people"))),
    ("recent_events>=1", lambda o: bool(o.get("recent_events"))),
    ("related_entities>=1", lambda o: bool(o.get("related_entities"))),
    ("website", lambda o: bool((o.get("basic_info") or {}).get("website"))),
]
for label, fn in ochecks:
    n, pct = cov(orgs, fn)
    print("  %-26s %3d / %d  (%.0f%%)" % (label, n, len(orgs), pct))

# total quotes & sources
tq = sum(len((p.get("collection_meta") or {}).get("quotes") or []) for p in persons)
print("\nTotal person quotes: %d (avg %.1f/person)" % (tq, tq/len(persons)))
