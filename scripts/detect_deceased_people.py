"""Generate pending death-review candidates, NOT approved exclusions.

The primary signal is Wikidata property P570 (date of death).  A narrowly
scoped biography fallback is used only when no P570 value was found: the
profile biography may mention death. Identity and sentence subject need human review.
"""

from __future__ import annotations

import argparse
import json
import re
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from build_people_lite import guard_destinations


QID = re.compile(r"^Q\d+$")
PERSON_ID = re.compile(r"^([A-Z]{2})-PERSON-\d{6}$")
EXPLICIT_DEATH = re.compile(
    r"(?:于\s*\d{4}年[^。；，]{0,32}(?:去世|逝世|病逝)|"
    r"(?:去世|逝世|病逝)\s*(?:，|。|$)|"
    r"\bdied\b|\bpassed away\b)",
    re.IGNORECASE,
)


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def collect_people(input_dirs: list[Path]) -> tuple[list[dict[str, Any]], list[str]]:
    people: list[dict[str, Any]] = []
    errors: list[str] = []
    seen: set[str] = set()
    for directory in input_dirs:
        if not directory.is_dir():
            errors.append(f"input directory does not exist: {directory}")
            continue
        paths = sorted(directory.glob("*-PERSON-*.json"))
        if not paths:
            errors.append(f"no canonical person files: {directory}")
        for path in paths:
            try:
                item = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"{path}: cannot parse JSON: {error}")
                continue
            person_id = text(item.get("person_id")) if isinstance(item, dict) else ""
            match = PERSON_ID.fullmatch(person_id)
            if not match or path.stem != person_id:
                errors.append(f"{path}: invalid person_id")
                continue
            if person_id in seen:
                errors.append(f"{path}: duplicate person_id {person_id}")
                continue
            seen.add(person_id)
            people.append(
                {
                    "person_id": person_id,
                    "region": match.group(1),
                    "name": text(item.get("name_zh")) or text(item.get("name")) or text(item.get("name_en")),
                    "qid": text(item.get("wikidata_qid")),
                    "birth_date": text(item.get("birth_date")),
                    "source_file": str(path.resolve()),
                    "biography": text(item.get("biography_summary")),
                }
            )
    return people, errors


def parse_death_binding(binding: dict[str, Any]) -> str:
    death = binding.get("death", {})
    value = text(death.get("value"))
    if death.get("type") not in {"literal", "typed-literal"} or not re.match(r"^\d{4}-\d{2}-\d{2}T", value):
        return ""
    try:
        precision = int(binding.get("precision", {}).get("value", "0"))
    except (TypeError, ValueError):
        return ""
    return value[:10] if precision >= 11 else value[:7] if precision == 10 else value[:4] if precision == 9 else ""


def query_death_dates(qids: list[str], endpoint: str) -> tuple[dict[str, str], list[str]]:
    found: dict[str, str] = {}
    errors: list[str] = []
    for start in range(0, len(qids), 75):
        batch = qids[start : start + 75]
        values = " ".join(f"wd:{qid}" for qid in batch)
        query = (f"SELECT ?person ?death ?precision WHERE {{ VALUES ?person {{ {values} }} "
                 "?person p:P570/psv:P570 ?node. ?node wikibase:timeValue ?death; wikibase:timePrecision ?precision. }")
        payload: dict[str, Any] | None = None
        for attempt in range(3):
            try:
                response = requests.get(
                    endpoint,
                    params={"query": query, "format": "json"},
                    headers={"Accept": "application/sparql-results+json", "User-Agent": "apec-osint-deceased-detector/1.0"},
                    timeout=(10, 90),
                )
                response.raise_for_status()
                payload = response.json()
                if not isinstance(payload, dict) or not isinstance(payload.get("results", {}).get("bindings"), list):
                    raise ValueError("unexpected SPARQL response structure")
                break
            except (requests.RequestException, ValueError) as error:
                if attempt == 2:
                    errors.append(f"batch {start // 75 + 1}: {error}")
                else:
                    time.sleep(2 + attempt)
        if payload:
            for binding in payload.get("results", {}).get("bindings", []):
                uri = text(binding.get("person", {}).get("value"))
                death = parse_death_binding(binding)
                qid = uri.rsplit("/", 1)[-1]
                if QID.fullmatch(qid) and death:
                    found[qid] = death
        if start + 75 < len(qids):
            time.sleep(12)
    return found, errors


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", nargs="+", required=True, type=Path, help="Canonical persons directories")
    parser.add_argument("--output", required=True, type=Path, help="Pending review candidate JSON (not an exclusion list)")
    parser.add_argument("--report", required=True, type=Path, help="Detection report JSON")
    parser.add_argument("--wikidata-endpoint", default="https://query.wikidata.org/sparql")
    parser.add_argument("--offline", action="store_true", help="Only inspect biographies; do not query Wikidata")
    args = parser.parse_args()

    guard_destinations(args.input, [args.output, args.report])
    people, source_errors = collect_people(args.input)
    qids = sorted({person["qid"] for person in people if QID.fullmatch(person["qid"])})
    death_dates, query_errors = ({}, []) if args.offline else query_death_dates(qids, args.wikidata_endpoint)
    evidence: list[dict[str, str]] = []
    matched_ids: set[str] = set()
    for person in people:
        death_date = death_dates.get(person["qid"])
        if death_date:
            matched_ids.add(person["person_id"])
            evidence.append({**{key: person[key] for key in ("person_id", "region", "name", "qid", "birth_date", "source_file")}, "death_date": death_date, "source": "wikidata_p570", "url": f"https://www.wikidata.org/wiki/{person['qid']}"})
            continue
        sentence = next((part.strip() for part in re.split(r"[。\n]", person["biography"]) if EXPLICIT_DEATH.search(part)), "")
        if sentence:
            matched_ids.add(person["person_id"])
            evidence.append({**{key: person[key] for key in ("person_id", "region", "name", "qid", "birth_date", "source_file")}, "death_date": "", "source": "biography_death_mention", "sentence": sentence})

    evidence.sort(key=lambda item: item["person_id"])
    by_region = Counter(item["region"] for item in evidence)
    generated_at = datetime.now(timezone.utc).isoformat()
    manifest = {
        "generated_at": generated_at,
        "review_status": "pending",
        "candidate_person_ids": sorted(matched_ids),
        "review_note": "核对QID身份、生卒时间及原句主语。亲属、前任、同名人物和未证实死亡报道不能直接排除。复核后另外创建 excluded_person_ids 清单。",
        "evidence": evidence,
    }
    report = {
        "generated_at": generated_at,
        "source_records": len(people),
        "wikidata_qids_queried": 0 if args.offline else len(qids),
        "offline": args.offline,
        "wikidata_death_dates_found": sum(item["source"] == "wikidata_p570" for item in evidence),
        "biography_death_mentions_found": sum(item["source"] == "biography_death_mention" for item in evidence),
        "candidate_count": len(evidence),
        "candidate_by_region": dict(sorted(by_region.items())),
        "exclusions_approved": 0,
        "source_errors": source_errors,
        "query_errors": query_errors,
    }
    atomic_json(args.output, manifest)
    atomic_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False))
    if source_errors or query_errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
