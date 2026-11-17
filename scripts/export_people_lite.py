"""Batch export dated country snapshots, validate, then publish each lite JSONL.

All relative paths (including paths in --config) resolve from the working directory.
Only one batch may use a work directory at a time; an exclusive lock enforces this.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date, datetime, timezone
from pathlib import Path

from build_people_lite import (BuildError, atomic_json, collect_records, guard_destinations,
                               load_excluded_ids, load_overrides, load_policy)
from opencc import OpenCC
from validate_people_lite import validate


def snapshot(source_root: Path, country: str, selected_date: str | None) -> Path:
    country_root = source_root / country
    candidates = []
    for path in country_root.iterdir():
        if not path.is_dir() or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", path.name):
            continue
        date.fromisoformat(path.name)
        if (path / "persons").is_dir():
            candidates.append(path)
    if selected_date:
        date.fromisoformat(selected_date)
        candidates = [path for path in candidates if path.name == selected_date]
    if not candidates:
        raise BuildError(f"no dated persons snapshot for {country}: {selected_date or 'latest'}")
    return (max(candidates, key=lambda p: p.name) / "persons").resolve()


def fingerprint(directory: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(directory.glob("*-PERSON-*.json")):
        digest.update(path.name.encode("utf-8"))
        digest.update(hashlib.sha256(path.read_bytes()).digest())
    return digest.hexdigest()


def optional_path(value: str | None) -> Path | None:
    return Path(value).resolve() if value else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--countries", nargs="+", help="ISO source directory codes, e.g. hk tw kh")
    parser.add_argument("--config", type=Path, help="Optional country-specific dates, exclusions and overrides")
    parser.add_argument("--source-root", type=Path, default=Path("output"))
    parser.add_argument("--work-dir", type=Path, default=Path("tmp/people_lite"))
    parser.add_argument("--exclude-ids", type=Path, help="Explicitly reviewed exclusions, may be shared across countries")
    parser.add_argument("--include-all", action="store_true", help="Explicitly skip deceased filtering (not an alive assertion)")
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--translation-endpoint", default="http://10.11.204.238:8080/translate")
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--country-workers", type=int, default=3)
    parser.add_argument("--fail-on-quality-warnings", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.workers <= 32 or not 1 <= args.country_workers <= 4:
        raise BuildError("workers must be 1..32; country-workers must be 1..4")
    if args.include_all and args.exclude_ids:
        raise BuildError("--include-all and --exclude-ids are mutually exclusive")
    config = json.loads(args.config.read_text(encoding="utf-8-sig")) if args.config else {"countries": []}
    if not isinstance(config, dict) or set(config) != {"countries"}:
        raise BuildError("config must contain only a countries array")
    entries = config.get("countries")
    if not isinstance(entries, list) or any(not isinstance(v, dict) for v in entries):
        raise BuildError("config.countries must be an array of objects")
    by_country = {}
    for entry in entries:
        if set(entry) - {"region", "date", "exclude_ids", "overrides"} or not isinstance(entry.get("region"), str):
            raise BuildError("country entry requires region and accepts only date/exclude_ids/overrides")
        code = entry["region"].lower()
        if not re.fullmatch("[a-z]{2}", code):
            raise BuildError(f"invalid config region {code}")
        if code in by_country:
            raise BuildError(f"duplicate config country {code}")
        by_country[code] = entry
    countries = [v.lower() for v in (args.countries or list(by_country))]
    if not countries or len(countries) != len(set(countries)) or any(not re.fullmatch("[a-z]{2}", v) for v in countries):
        raise BuildError("provide unique two-letter --countries or config countries")
    work = args.work_dir.resolve()
    plans = []
    policy = load_policy(args.policy)
    for code in countries:
        entry = by_country.get(code, {})
        source = snapshot(args.source_root, code, entry.get("date"))
        excluded = optional_path(entry.get("exclude_ids")) or args.exclude_ids
        overrides = optional_path(entry.get("overrides"))
        if args.include_all and excluded:
            raise BuildError(f"{code}: --include-all conflicts with configured exclusions")
        if not excluded and not args.include_all:
            raise BuildError(f"{code}: supply reviewed --exclude-ids/config exclusions, or explicitly --include-all")
        records, errors, _, omitted = collect_records([source], OpenCC("t2s"), policy, load_excluded_ids(excluded))
        if errors:
            raise BuildError("; ".join(errors))
        load_overrides(overrides, records)
        plans.append({"region": code, "source": source, "excluded": excluded,
                      "overrides": overrides, "records": len(records), "excluded_count": sum(omitted.values())})
    destinations = [work / "batch_progress.json", work / ".export.lock"]
    protected = [args.config, args.policy, args.exclude_ids]
    for plan in plans:
        code = plan["region"]
        destinations += [work / f"{code}_people_{suffix}" for suffix in (
            "simplified.jsonl", "translation_cache.json", "translation_progress.json",
            "build_report.json", "validation.json", "export.log")]
        destinations.append(work / ".staging" / f"{code}_people_simplified.jsonl")
        protected += [plan["excluded"], plan["overrides"]]
    guard_destinations([p["source"] for p in plans], destinations, protected)
    if args.dry_run:
        print(json.dumps({"status": "dry_run", "countries": plans}, ensure_ascii=False, default=str))
        return 0
    work.mkdir(parents=True, exist_ok=True)
    lock_path = work / ".export.lock"
    try:
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as error:
        raise BuildError(f"another batch may be using {work}; inspect .export.lock PID before removing a stale lock") from error
    state_lock = threading.Lock()
    state = {"stage": "running", "pid": os.getpid(), "total": len(plans), "completed": 0,
             "succeeded": 0, "failed": 0, "percent": 0, "countries": {}}
    def save_state() -> None:
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        atomic_json(work / "batch_progress.json", state)

    def run(plan: dict) -> dict:
        code, source = plan["region"], plan["source"]
        with state_lock:
            state["countries"][code] = {"status": "running", "source": str(source),
                "progress_file": str(work / f"{code}_people_translation_progress.json")}
            save_state()
        output = work / f"{code}_people_simplified.jsonl"
        staging = work / ".staging" / f"{code}_people_simplified.jsonl"
        report_path = work / f"{code}_people_validation.json"
        log_path = work / f"{code}_people_export.log"
        before = fingerprint(source)
        command = [sys.executable, "-X", "utf8", str(Path(__file__).with_name("build_people_lite.py")),
                   "--input", str(source), "--output", str(staging),
                   "--cache", str(work / f"{code}_people_translation_cache.json"),
                   "--progress", str(work / f"{code}_people_translation_progress.json"),
                   "--report", str(work / f"{code}_people_build_report.json"),
                   "--workers", str(args.workers), "--translation-endpoint", args.translation_endpoint]
        for flag, value in (("--exclude-ids", plan["excluded"]), ("--overrides", plan["overrides"]), ("--policy", args.policy)):
            if value:
                command += [flag, str(value)]
        with log_path.open("w", encoding="utf-8") as stream:
            result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, check=False)
        if result.returncode:
            raise BuildError(f"{code}: build failed ({result.returncode}); see {log_path}")
        report = validate([source], staging, plan["excluded"], args.policy, plan["overrides"])
        report.update({"source_directory": str(source), "source_sha256": before,
                       "validated_at": datetime.now(timezone.utc).isoformat(),
                       "translation_endpoint": args.translation_endpoint,
                       "configuration": {key: str(value.resolve()) if value else None for key, value in
                           (("exclude_ids", plan["excluded"]), ("overrides", plan["overrides"]), ("policy", args.policy))}})
        if fingerprint(source) != before:
            report["errors"].append("source changed during export; rerun against a stable snapshot")
            report["error_count"] += 1
        report["status"] = "failed" if report["error_count"] or (args.fail_on_quality_warnings and report["warning_count"]) else "passed"
        if report["status"] == "passed":
            staging.replace(output)
            report["output"] = str(output)
        atomic_json(report_path, report)
        if report["status"] != "passed":
            raise BuildError(f"{code}: validation failed; see {report_path}; previous final output unchanged")
        return {"status": "completed", "output": str(output), "records": report["records"],
                "excluded": report["excluded_persons"], "warnings": report["warning_count"],
                "source": str(source), "source_sha256": before}
    try:
        os.write(lock_fd, str(os.getpid()).encode("ascii"))
        save_state()
        with ThreadPoolExecutor(max_workers=args.country_workers) as pool:
            futures = {pool.submit(run, plan): plan["region"] for plan in plans}
            for future in as_completed(futures):
                code = futures[future]
                try:
                    result = future.result()
                except Exception as error:
                    result = {"status": "failed", "error": str(error)}
                with state_lock:
                    state["countries"][code] = result
                    state["completed"] += 1
                    state["succeeded" if result["status"] == "completed" else "failed"] += 1
                    state["percent"] = round(100 * state["completed"] / state["total"], 2)
                    save_state()
                print(json.dumps({"region": code, **result}, ensure_ascii=False), flush=True)
        state["stage"] = "failed" if state["failed"] else "completed"
        save_state()
        return 1 if state["failed"] else 0
    finally:
        os.close(lock_fd)
        lock_path.unlink()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (BuildError, OSError, ValueError) as error:
        print(f"ERROR: {error}")
        raise SystemExit(2)
