#!/usr/bin/env python3
"""
verify_qids.py — Verify all QIDs in target org list before batch collection
Usage: python .claude/skills/country-org-collector/scripts/verify_qids.py output/sg/2026-04-15

Ensures every QID in _target_orgs.json resolves to the expected entity.
Fixes wrong QIDs by searching Wikidata for the correct one.

Exit codes:
  0 — all QIDs verified
  1 — some QIDs fixed (re-run to confirm)
  2 — some QIDs could not be resolved
"""
import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import time
import urllib.error
import urllib.request
import urllib.parse

from atomic_write import save_json, load_json, setup_proxy

RATE_LIMIT = 8  # seconds between API calls
RATE_LIMIT_BACKOFF = (45, 90, 90)  # waits on HTTP 429 before giving up

ENTITY_MISSING = "MISSING"  # sentinel: QID genuinely does not exist on Wikidata


def _fetch_json(url, timeout=15):
    """GET JSON with 429 backoff. Returns parsed dict, or None on persistent failure."""
    waits = (None,) + tuple(RATE_LIMIT_BACKOFF)
    for i, wait in enumerate(waits):
        if wait is not None:
            print(f"    RATE LIMITED (429), waiting {wait}s before retry {i}/{len(RATE_LIMIT_BACKOFF)}...")
            time.sleep(wait)
        req = urllib.request.Request(url, headers={"User-Agent": "ApecOsintTool/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429:
                continue
            print(f"    ERROR: {e}")
            return None
        except Exception as e:
            print(f"    ERROR: {e}")
            return None
    print(f"    ERROR: persistent 429 rate limiting")
    return None


def fetch_entity(qid):
    """Fetch entity labels from Wikidata to verify QID.

    Returns dict on success, ENTITY_MISSING if the QID does not exist,
    None on API errors (must NOT be treated as an invalid QID).
    """
    url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={qid}&format=json&props=labels|description"
    data = _fetch_json(url)
    if data is None:
        return None
    entity = data.get("entities", {}).get(qid)
    if not entity or "missing" in entity:
        return ENTITY_MISSING
    return {
        "en": entity.get("labels", {}).get("en", {}).get("value", ""),
        "zh": entity.get("labels", {}).get("zh", {}).get("value", ""),
        "desc": entity.get("descriptions", {}).get("en", {}).get("value", ""),
    }


def search_entity(name_en):
    """Search Wikidata for the correct QID."""
    url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={urllib.parse.quote(name_en)}&language=en&format=json&limit=5"
    data = _fetch_json(url)
    if data is None:
        return None, None, None
    results = data.get("search", [])
    if results:
        return results[0]["id"], results[0].get("label", ""), results[0].get("description", "")
    return None, None, None


def name_similarity(a, b):
    """Check if two names likely refer to the same entity. Returns 0-1."""
    if not a or not b:
        return 0
    a_lower = a.lower().strip()
    b_lower = b.lower().strip()
    if a_lower == b_lower:
        return 1.0
    # Check if one contains the other
    if a_lower in b_lower or b_lower in a_lower:
        return 0.8
    # Token overlap
    tokens_a = set(a_lower.split())
    tokens_b = set(b_lower.split())
    if not tokens_a or not tokens_b:
        return 0
    overlap = len(tokens_a & tokens_b) / max(len(tokens_a), len(tokens_b))
    return overlap


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <output_dir>")
        sys.exit(1)

    base_dir = sys.argv[1]
    targets_file = os.path.join(base_dir, "_target_orgs.json")

    if not os.path.exists(targets_file):
        print(f"ERROR: {targets_file} not found")
        sys.exit(1)

    setup_proxy()

    targets_raw = load_json(targets_file)
    # Support both flat array and object format
    if isinstance(targets_raw, dict):
        targets = targets_raw.get("organizations", [])
    else:
        targets = targets_raw

    print(f"=== QID Verification ===")
    print(f"Target orgs: {len(targets)}")
    print()

    ok = 0
    fixed = 0
    failed = 0

    for i, org in enumerate(targets):
        # Normalize field names: qid/wikidata_qid, name_en/name, category
        qid = org.get("qid") or org.get("wikidata_qid")
        name_en = org.get("name_en") or org.get("name", "")
        category = org.get("category")

        if not qid:
            print(f"[{i+1}/{len(targets)}] MISSING QID: {name_en}")
            # Try to find it
            new_qid, label, desc = search_entity(name_en)
            if new_qid:
                org["qid"] = new_qid
                print(f"  FOUND: {new_qid} ({label}: {desc})")
                fixed += 1
            else:
                print(f"  NOT FOUND")
                failed += 1
            time.sleep(RATE_LIMIT)
            continue

        # Verify existing QID
        entity = fetch_entity(qid)
        if entity is None:
            # API error (e.g. persistent 429) — QID may well be valid, never replace it
            print(f"[{i+1}/{len(targets)}] UNVERIFIED (API error): {name_en} QID={qid}")
            failed += 1
            time.sleep(RATE_LIMIT)
            continue
        if entity == ENTITY_MISSING:
            print(f"[{i+1}/{len(targets)}] INVALID: {name_en} QID={qid} does not exist")
            # Search for correct QID (only accept if name similarity is convincing)
            new_qid, label, desc = search_entity(name_en)
            if new_qid and name_similarity(name_en, label) >= 0.5:
                print(f"  FIXED: {qid} -> {new_qid} ({label}: {desc})")
                org["qid"] = new_qid
                fixed += 1
            elif new_qid:
                print(f"  KEEP: search top hit '{label}' too dissimilar, keeping {qid}")
                failed += 1
            else:
                print(f"  NOT FOUND")
                failed += 1
            time.sleep(RATE_LIMIT)
            continue

        # Check if QID resolves to expected entity
        sim = name_similarity(name_en, entity["en"])
        if sim < 0.3:
            print(f"[{i+1}/{len(targets)}] MISMATCH: {name_en} QID={qid}")
            print(f"  QID resolves to: {entity['en']} ({entity['desc']})")
            print(f"  Similarity: {sim:.2f}")
            # Search for correct QID
            new_qid, label, desc = search_entity(name_en)
            if new_qid:
                new_sim = name_similarity(name_en, label)
                if new_sim > sim:
                    print(f"  FIXED: {qid} -> {new_qid} ({label}: {desc}) [sim={new_sim:.2f}]")
                    org["qid"] = new_qid
                    fixed += 1
                else:
                    print(f"  KEEP: search result not better ({label}, sim={new_sim:.2f})")
                    ok += 1
            else:
                print(f"  NO FIX FOUND")
                ok += 1  # Keep existing, might be close enough
            time.sleep(RATE_LIMIT)
            continue

        ok += 1
        print(f"[{i+1}/{len(targets)}] OK: {name_en} -> {entity['en']} [sim={sim:.2f}]")
        time.sleep(RATE_LIMIT)

    # Save updated targets
    save_json(targets_file, targets)

    print(f"\n=== Verification Complete ===")
    print(f"  OK: {ok}")
    print(f"  Fixed: {fixed}")
    print(f"  Failed: {failed}")

    if failed > 0:
        sys.exit(2)
    if fixed > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
