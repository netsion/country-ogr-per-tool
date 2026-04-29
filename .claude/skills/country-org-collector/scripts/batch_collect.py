#!/usr/bin/env python3
"""
batch_collect.py — 批量采集组织原始数据（Wikidata + Wikipedia）
用法: python .claude/skills/country-org-collector/scripts/batch_collect.py output/sg/2026-04-15
功能:
  1. 读取 _target_orgs.json
  2. 对每个 org 依次获取 Wikidata EntityData + Wikipedia REST summary
  3. 缓存到 _cache/ 目录
  4. 更新 _progress.json
  5. 支持断点续跑（跳过已缓存的 org）
"""

import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import time
import urllib.request
import urllib.parse
import urllib.error

from atomic_write import save_json, load_json, setup_proxy

CACHE_DIR_NAME = "_cache"
WIKIDATA_RATE_LIMIT = 12  # seconds between requests
WIKIPEDIA_RATE_LIMIT = 3  # seconds between requests
MAX_RETRIES = 2
RETRY_DELAY = 30  # seconds


def fetch_url(url, timeout=30):
    """Fetch URL with User-Agent header, return raw bytes."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "ApecOsintTool/1.0 (research; bot)",
        "Accept": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    except Exception as e:
        print(f"    ERROR fetching {url}: {e}")
        return None


def fetch_wikidata_entity(qid):
    """Fetch Wikidata EntityData JSON for a QID."""
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{qid}.json"
    raw = fetch_url(url)
    if raw is None:
        return None
    data = json.loads(raw)
    entities = data.get("entities", {})
    entity = entities.get(qid)
    return entity


def fetch_wikipedia_summary(title_en):
    """Fetch Wikipedia REST API summary for an article."""
    encoded = urllib.parse.quote(title_en.replace(" ", "_"))
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    raw = fetch_url(url)
    if raw is None:
        return None
    return json.loads(raw)


def extract_wikipedia_title(wikidata_entity):
    """Extract English Wikipedia article title from Wikidata sitelinks."""
    sitelinks = wikidata_entity.get("sitelinks", {})
    enwiki = sitelinks.get("enwiki", {})
    return enwiki.get("title")


def process_org(org, cache_dir):
    """Process a single org: fetch and cache Wikidata + Wikipedia data."""
    qid = org.get("qid") or org.get("wikidata_qid")
    name_en = org.get("name_en") or org.get("name", "")
    category = org.get("category")

    # Check cache
    cache_file = os.path.join(cache_dir, f"{qid or name_en.replace(' ', '_')}.json")
    if os.path.exists(cache_file):
        print(f"  CACHED: {name_en} ({qid})")
        return True

    print(f"  FETCHING: {name_en} ({category}, QID={qid})")

    result = {
        "org": org,
        "wikidata": None,
        "wikipedia": None,
        "errors": [],
    }

    # Step 1: Wikidata
    if qid:
        for attempt in range(MAX_RETRIES + 1):
            try:
                entity = fetch_wikidata_entity(qid)
                if entity:
                    result["wikidata"] = entity
                    print(f"    OK: Wikidata entity fetched")
                    # Extract Wikipedia title from sitelinks
                    wp_title = extract_wikipedia_title(entity)
                    if wp_title:
                        result["wikipedia_title"] = wp_title
                else:
                    result["errors"].append(f"Wikidata returned no data for {qid}")
                break
            except Exception as e:
                if attempt < MAX_RETRIES:
                    print(f"    Retry {attempt+1}/{MAX_RETRIES} after error: {e}")
                    time.sleep(RETRY_DELAY)
                else:
                    result["errors"].append(f"Wikidata error: {e}")
        time.sleep(WIKIDATA_RATE_LIMIT)

    # Step 2: Wikipedia
    wp_title = result.get("wikipedia_title", name_en)
    for attempt in range(MAX_RETRIES + 1):
        try:
            summary = fetch_wikipedia_summary(wp_title)
            if summary and summary.get("type") != "disambiguation":
                result["wikipedia"] = summary
                print(f"    OK: Wikipedia summary fetched")
            else:
                result["errors"].append(f"Wikipedia returned disambiguation or no data for '{wp_title}'")
            break
        except Exception as e:
            if attempt < MAX_RETRIES:
                print(f"    Retry {attempt+1}/{MAX_RETRIES} after error: {e}")
                time.sleep(RETRY_DELAY)
            else:
                result["errors"].append(f"Wikipedia error: {e}")
    time.sleep(WIKIPEDIA_RATE_LIMIT)

    # Save cache (even if all fetches failed, write a minimal stub)
    if result["wikidata"] is None and result["wikipedia"] is None and result.get("errors"):
        result["source_unavailable"] = True
        print(f"    WARNING: No data fetched, writing stub with source_unavailable flag")
    save_json(cache_file, result)
    print(f"    SAVED: {cache_file}")
    return True


def main():
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <output_dir>")
        sys.exit(1)

    base_dir = sys.argv[1]
    targets_file = os.path.join(base_dir, "_target_orgs.json")
    cache_dir = os.path.join(base_dir, CACHE_DIR_NAME)
    progress_file = os.path.join(base_dir, "_progress.json")

    if not os.path.exists(targets_file):
        print(f"ERROR: {targets_file} not found")
        sys.exit(1)

    os.makedirs(cache_dir, exist_ok=True)

    targets_raw = load_json(targets_file)
    # Support both flat array [{qid,name_en,category}] and object format {organizations:[...]}
    if isinstance(targets_raw, dict):
        targets = targets_raw.get("organizations", [])
    else:
        targets = targets_raw

    print(f"=== Batch Collection ===")
    print(f"Target orgs: {len(targets)}")
    print(f"Cache dir: {cache_dir}")

    setup_proxy()

    success = 0
    cached = 0
    failed = 0

    for i, org in enumerate(targets):
        print(f"\n[{i+1}/{len(targets)}]", end=" ")
        cache_file = os.path.join(cache_dir, f"{org.get('qid') or org.get('wikidata_qid') or org.get('name_en', org.get('name', '')).replace(' ', '_')}.json")
        was_cached = os.path.exists(cache_file)

        try:
            process_org(org, cache_dir)
            if was_cached:
                cached += 1
            else:
                success += 1
        except Exception as e:
            print(f"    FATAL: {e}")
            failed += 1

        # Update progress after each org
        if os.path.exists(progress_file):
            progress = load_json(progress_file)
            progress["current_action"] = f"phase1_cached_{i+1}_of_{len(targets)}"
            progress["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            save_json(progress_file, progress)

    print(f"\n=== Done ===")
    print(f"  Newly fetched: {success}")
    print(f"  Already cached: {cached}")
    print(f"  Failed: {failed}")

    # Final progress update
    if os.path.exists(progress_file):
        progress = load_json(progress_file)
        progress["phases"]["phase1_scan"]["status"] = "done"
        progress["phases"]["phase1_scan"]["wikidata_queries_done"] = ["template_A_general", "template_B_gov", "template_C_corp", "template_D_acad", "template_E_party", "template_F_media"]
        progress["phases"]["phase1_scan"]["web_searches_done"] = progress["phases"]["phase1_scan"]["web_searches_remaining"]
        progress["phases"]["phase1_scan"]["web_searches_remaining"] = []
        progress["phases"]["phase1_scan"]["orgs_file"] = "_target_orgs.json"
        progress["current_phase"] = "phase1_done"
        progress["current_action"] = "cache_complete"
        progress["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        save_json(progress_file, progress)


if __name__ == "__main__":
    main()
