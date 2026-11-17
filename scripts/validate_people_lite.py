"""Validate lite JSONL against canonical records, without network requests."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from opencc import OpenCC
from build_people_lite import (BuildError, atomic_json, collect_records, guard_destinations,
                               keyword_terms, load_excluded_ids, load_overrides, load_policy)

LANGUAGES = {"ar", "km", "ru", "en", "fr", "zh", "es"}
FIELDS = {"personId", "personAvatar", "personName", "transPersonName", "keyword",
          "region", "current_positions", "occupation"}
CJK = re.compile(r"[\u3400-\u9fff]")
SCRIPTS = {"ar": re.compile(r"[\u0600-\u06ff]"), "km": re.compile(r"[\u1780-\u17ff]"),
           "ru": re.compile(r"[\u0400-\u04ff]")}


def validate(input_dirs: list[Path], output: Path, excluded: Path | None = None,
             policy_path: Path | None = None, overrides_path: Path | None = None,
             normalized: bool = False) -> dict[str, Any]:
    records, errors, counts, exclusions = collect_records(
        input_dirs, OpenCC("t2s"), load_policy(policy_path), load_excluded_ids(excluded))
    overrides = load_overrides(overrides_path, records)
    expected = {record["person_id"]: record for record in records}
    warnings: list[str] = []
    ids: list[str] = []
    avatars = 0
    traditional = OpenCC("s2t")
    for line_no, line in enumerate(output.read_text(encoding="utf-8-sig").splitlines(), 1):
        prefix = f"line {line_no}"
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            errors.append(f"{prefix}: invalid JSON (blank lines are not allowed)")
            continue
        if not isinstance(row, dict):
            errors.append(f"{prefix}: must be an object")
            continue
        person_id = row.get("personId")
        if not isinstance(person_id, str):
            errors.append(f"{prefix}: invalid personId")
            continue
        ids.append(person_id)
        record = expected.get(person_id)
        if record is None:
            errors.append(f"{person_id}: unexpected or excluded ID")
            continue
        def check(condition: bool, field: str) -> None:
            if not condition:
                errors.append(f"{person_id}: {field}")
        check(set(row) == FIELDS, "top-level fields")
        for field, source in (("personAvatar", "avatar"), ("personName", "name"), ("region", "region")):
            check(row.get(field) == record[source], f"{field} source mapping")
        avatars += bool(row.get("personAvatar"))
        check(row.get("current_positions") == record["positions_zh" if normalized else "positions"], "current_positions mapping")
        names = row.get("transPersonName")
        jobs = row.get("occupation")
        if not isinstance(names, dict) or not isinstance(jobs, dict):
            errors.append(f"{person_id}: multilingual objects required")
            continue
        check(set(names) == LANGUAGES and all(isinstance(v, str) and v.strip() for v in names.values()), "name languages/nonempty strings")
        check(names.get("zh") == record["zh"], "name_zh mapping")
        check(names.get("en") == record["en"], "name_en mapping")
        check(set(jobs) == LANGUAGES, "occupation language keys")
        check(jobs.get("zh") == record["positions_zh"], "occupation.zh normalization")
        for language, values in jobs.items():
            valid = isinstance(values, list) and len(values) == len(record["positions"]) and all(isinstance(v, str) and v.strip() for v in values)
            check(valid, f"occupation.{language} array/length/nonempty")
            if valid and language != "zh" and any(CJK.search(v) for v in values):
                warnings.append(f"{person_id}: occupation.{language} contains Chinese characters; review mixed/untranslated text")
        entry = overrides.get(person_id, {})
        for language, value in entry.get("transPersonName", {}).items():
            check(names.get(language) == value, f"reviewed name override {language}")
        for language, value in entry.get("occupation", {}).items():
            check(jobs.get(language) == value, f"reviewed occupation override {language}")
        for language, value in names.items():
            if language != "zh" and isinstance(value, str) and CJK.search(value):
                warnings.append(f"{person_id}: transPersonName.{language} contains Chinese characters")
            if language in SCRIPTS and isinstance(value, str) and not SCRIPTS[language].search(value):
                warnings.append(f"{person_id}: transPersonName.{language} lacks expected script; review transliteration")
        ordered_names = [names.get(lang) for lang in ("ar", "km", "ru", "en", "fr", "zh", "es")]
        required = [record["name"], record["zh"], record["en"], *ordered_names, *record["aliases"]]
        if record["dataset_region"] in {"HK", "TW"}:
            required.append(traditional.convert(record["zh"]))
        check(row.get("keyword") == "|".join(keyword_terms(required)), "keyword content/order/traditional/deduplication")
    if len(ids) != len(set(ids)):
        errors.append("duplicate output personId")
    missing = sorted(set(expected) - set(ids))
    if missing:
        errors.append(f"missing output IDs: {missing}")
    return {"status": "failed" if errors else "passed", "output": str(output.resolve()),
            "records": len(records), "output_lines": len(ids), "avatars_populated": avatars,
            "by_dataset_region": dict(counts), "excluded_persons": sum(exclusions.values()),
            "error_count": len(errors), "errors": errors,
            "warning_count": len(warnings), "warnings": warnings,
            "semantic_review": "required; structural checks do not prove translation accuracy or current tenure"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", nargs="+", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--exclude-ids", type=Path)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--overrides", type=Path)
    parser.add_argument("--report", type=Path)
    parser.add_argument("--normalized-current-positions", action="store_true")
    parser.add_argument("--fail-on-quality-warnings", action="store_true")
    args = parser.parse_args()
    guard_destinations(args.input, [args.report], [args.output, args.policy, args.exclude_ids, args.overrides])
    if args.report and args.report.resolve() == args.output.resolve():
        raise BuildError("report must not overwrite JSONL")
    report = validate(args.input, args.output, args.exclude_ids, args.policy, args.overrides, args.normalized_current_positions)
    if args.report:
        atomic_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False))
    raise SystemExit(1 if report["error_count"] or (args.fail_on_quality_warnings and report["warning_count"]) else 0)


if __name__ == "__main__":
    try:
        main()
    except (BuildError, OSError, ValueError) as error:
        print(f"ERROR: {error}")
        raise SystemExit(2)
