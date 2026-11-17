"""Build multilingual person lite JSONL from one or more canonical persons directories.

The canonical source files are never modified.  Translations are cached by
``language + NUL + source text`` so interrupted runs can resume safely.
"""

from __future__ import annotations

import argparse
import json
import re
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from opencc import OpenCC


PERSON_ID = re.compile(r"^[A-Z]{2}-PERSON-\d{6}$")
NAME_LANGUAGES = ("ar", "km", "ru", "fr", "es")
POSITION_LANGUAGES = ("ar", "km", "ru", "en", "fr", "es")
DEFAULT_POLICY = {
    "TW": [
        ("中华民国总统", "台湾地区领导人"),
        ("中华民国副总统", "台湾地区副领导人"),
        ("中华民国立法院", "台湾地区立法机构"),
        ("中华民国行政院", "台湾地区行政机构"),
        ("中华民国外交部", "台湾地区外事主管部门"),
        ("中华民国", "台湾地区"),
        ("台湾总统", "台湾地区领导人"),
        ("台湾副总统", "台湾地区副领导人"),
    ]
}


class BuildError(RuntimeError):
    """A source-data or translation condition that prevents a safe export."""


def text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def unique(values: list[Any]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        value = text(value)
        if value and value not in seen:
            seen.add(value)
            result.append(value)
    return result


def keyword_terms(values: list[Any]) -> list[str]:
    """The exported pipe is a delimiter, including in legacy alias strings."""
    return unique([part for value in values if isinstance(value, str) for part in value.split("|")])


def guard_destinations(input_dirs: list[Path], destinations: list[Path | None], protected_files: list[Path | None] | None = None) -> None:
    resolved = [path.resolve() for path in destinations if path is not None]
    if len(resolved) != len(set(resolved)):
        raise BuildError("output/cache/progress/report paths must be distinct")
    protected = {path.resolve() for path in (protected_files or []) if path is not None}
    for destination in resolved:
        if destination in protected:
            raise BuildError(f"refusing to overwrite an input configuration: {destination}")
        if any(destination.is_relative_to(directory.resolve()) for directory in input_dirs):
            raise BuildError(f"refusing to write inside a source persons directory: {destination}")


def load_overrides(path: Path | None, records: list[dict[str, Any]]) -> dict[str, Any]:
    if path is None:
        return {}
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, dict):
        raise BuildError("overrides must be a person-ID-keyed JSON object")
    by_id = {record["person_id"]: record for record in records}
    for person_id, entry in raw.items():
        if not PERSON_ID.fullmatch(person_id) or not isinstance(entry, dict):
            raise BuildError(f"invalid override entry: {person_id}")
        if person_id not in by_id:
            raise BuildError(f"override ID not in the exported source set: {person_id}")
        record = by_id[person_id]
        if entry.get("source_name") != record["name"]:
            raise BuildError(f"{person_id}: override source_name is stale or missing")
        if set(entry) - {"source_name", "source_positions", "transPersonName", "occupation", "note"}:
            raise BuildError(f"{person_id}: unknown override fields")
        names = entry.get("transPersonName", {})
        jobs = entry.get("occupation", {})
        if not isinstance(names, dict) or set(names) - set(NAME_LANGUAGES) or any(not text(value) for value in names.values()):
            raise BuildError(f"{person_id}: invalid name overrides (zh/en must map to source)")
        if not isinstance(jobs, dict) or set(jobs) - set(POSITION_LANGUAGES):
            raise BuildError(f"{person_id}: invalid occupation override languages")
        if jobs and entry.get("source_positions") != record["positions"]:
            raise BuildError(f"{person_id}: override source_positions is stale or missing")
        for language, values in jobs.items():
            if not isinstance(values, list) or len(values) != len(record["positions"]) or any(not text(value) for value in values):
                raise BuildError(f"{person_id}: invalid occupation override {language}")
    return raw


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def atomic_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        "".join(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n" for row in rows),
        encoding="utf-8",
    )
    temp.replace(path)


def load_policy(path: Path | None) -> dict[str, list[tuple[str, str]]]:
    policy = {key: list(value) for key, value in DEFAULT_POLICY.items()}
    if not path:
        return policy
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(raw, dict):
        raise BuildError("policy must be a region-keyed JSON object")
    for region, entry in raw.items():
        replacements = entry.get("replacements", entry) if isinstance(entry, dict) else entry
        if not isinstance(replacements, list):
            raise BuildError(f"policy {region} must contain a replacements list")
        pairs: list[tuple[str, str]] = []
        for pair in replacements:
            if not isinstance(pair, list) or len(pair) != 2 or not all(isinstance(x, str) for x in pair) or not pair[0]:
                raise BuildError(f"invalid policy replacement in {region}: {pair!r}")
            pairs.append((pair[0], pair[1]))
        policy[region.upper()] = pairs
    return policy


def source_region(person_id: str) -> str:
    return person_id.split("-", 1)[0]


def normalize_position(value: str, dataset_region: str, to_simplified: OpenCC, policy: dict[str, list[tuple[str, str]]]) -> str:
    normalized = to_simplified.convert(value)
    # Longest source text first prevents a short replacement from damaging a
    # longer phrase that has a more precise policy mapping.
    for original, replacement in sorted(policy.get(dataset_region, []), key=lambda pair: len(pair[0]), reverse=True):
        normalized = normalized.replace(original, replacement)
    return normalized


def load_excluded_ids(path: Path | None) -> set[str]:
    """Load an auditable JSON list of canonical person IDs to omit."""
    if not path:
        return set()
    raw = json.loads(path.read_text(encoding="utf-8-sig"))
    if isinstance(raw, dict) and "excluded_person_ids" not in raw:
        raise BuildError(f"{path}: missing excluded_person_ids; candidate files are not reviewed exclusions")
    if isinstance(raw, dict) and raw.get("review_status", "reviewed") != "reviewed":
        raise BuildError(f"{path}: exclusions have not been reviewed")
    values = raw.get("excluded_person_ids") if isinstance(raw, dict) else raw
    if not isinstance(values, list) or not all(isinstance(value, str) and PERSON_ID.fullmatch(value) for value in values):
        raise BuildError(f"{path}: expected a JSON list of valid person IDs or an excluded_person_ids list")
    return set(values)


def collect_records(
    input_dirs: list[Path],
    to_simplified: OpenCC,
    policy: dict[str, list[tuple[str, str]]],
    excluded_ids: set[str],
) -> tuple[list[dict[str, Any]], list[str], Counter[str], Counter[str]]:
    records: list[dict[str, Any]] = []
    errors: list[str] = []
    counts: Counter[str] = Counter()
    excluded_counts: Counter[str] = Counter()
    ids: set[str] = set()
    for directory in input_dirs:
        if not directory.is_dir():
            errors.append(f"input directory does not exist: {directory}")
            continue
        paths = sorted(directory.glob("*-PERSON-*.json"))
        if not paths:
            errors.append(f"no canonical person files in: {directory}")
        for path in paths:
            try:
                data = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"{path}: cannot parse JSON: {error}")
                continue
            if not isinstance(data, dict):
                errors.append(f"{path}: root must be an object")
                continue
            person_id = text(data.get("person_id"))
            if not PERSON_ID.fullmatch(person_id):
                errors.append(f"{path}: invalid person_id {person_id!r}")
                continue
            dataset_region = source_region(person_id)
            if path.stem != person_id:
                errors.append(f"{path}: filename does not match person_id {person_id}")
                continue
            if person_id in ids:
                errors.append(f"{path}: duplicate person_id {person_id}")
                continue
            ids.add(person_id)
            if person_id in excluded_ids:
                excluded_counts[dataset_region] += 1
                continue
            name = text(data.get("name")) or text(data.get("name_zh")) or text(data.get("name_en"))
            if not name:
                errors.append(f"{path}: missing name/name_zh/name_en")
                continue
            # ``transPersonName.zh`` is a direct field mapping.  Keep the
            # canonical value intact rather than silently changing its script.
            zh = text(data.get("name_zh")) or name
            en = text(data.get("name_en")) or name
            raw_positions = data.get("current_positions")
            if raw_positions is not None and not isinstance(raw_positions, (list, str)):
                errors.append(f"{path}: current_positions must be an array or legacy string")
                continue
            if isinstance(raw_positions, list) and any(not isinstance(value, str) for value in raw_positions):
                errors.append(f"{path}: current_positions contains a non-string item")
                continue
            if isinstance(raw_positions, str):
                # Some legacy profiles store a semicolon-separated string.
                # Preserve those positions in the lite array rather than
                # silently exporting an empty occupation list.
                positions = unique(re.split(r"[；;]", raw_positions))
            else:
                positions = unique(raw_positions if isinstance(raw_positions, list) else [])
            # The lite ``current_positions`` field must retain the source
            # value.  Its translated representation, including simplified
            # Chinese and any China-stance policy normalization, belongs in
            # ``occupation``.
            positions_zh = [normalize_position(item, dataset_region, to_simplified, policy) for item in positions]
            profile = data.get("profile")
            avatar = text(profile.get("source_url")) if isinstance(profile, dict) else ""
            nationality = text(data.get("nationality")).upper()
            region = nationality if re.fullmatch(r"[A-Z]{2}", nationality) else dataset_region
            records.append(
                {
                    "person_id": person_id,
                    "dataset_region": dataset_region,
                    "name": name,
                    "zh": zh,
                    "en": en,
                    "aliases": unique(data.get("aliases") if isinstance(data.get("aliases"), list) else []),
                    "region": region,
                    "avatar": avatar,
                    "positions": positions,
                    "positions_zh": positions_zh,
                }
            )
            counts[dataset_region] += 1
    return records, errors, counts, excluded_counts


class Translator:
    def __init__(self, endpoint: str, cache_path: Path, progress_path: Path, workers: int) -> None:
        self.endpoint = endpoint
        self.cache_path = cache_path
        self.progress_path = progress_path
        self.workers = workers
        try:
            loaded = json.loads(cache_path.read_text(encoding="utf-8-sig"))
            if not isinstance(loaded, dict):
                raise BuildError("translation cache must be a JSON object")
            self.cache = {key: value for key, value in loaded.items() if isinstance(key, str) and isinstance(value, str) and value.strip()}
        except FileNotFoundError:
            self.cache = {}
        except json.JSONDecodeError as error:
            raise BuildError(f"translation cache is invalid JSON: {cache_path}: {error}") from error
        self.lock = threading.Lock()

    @staticmethod
    def key(language: str, value: str) -> str:
        return f"{language}\0{value}"

    def save_cache(self) -> None:
        with self.lock:
            atomic_json(self.cache_path, self.cache)

    def save_progress(self, stage: str, language: str, completed: int, total: int, succeeded: int, failed: int) -> None:
        atomic_json(
            self.progress_path,
            {
                "stage": stage,
                "updated_at": datetime.now(timezone.utc).isoformat(),
                "language": language,
                "completed": completed,
                "total": total,
                "succeeded": succeeded,
                "failed": failed,
                "percent": round((completed / total) * 100, 2) if total else 100.0,
            },
        )

    def translate_one(self, language: str, value: str) -> str | None:
        key = self.key(language, value)
        with self.lock:
            cached = self.cache.get(key)
        if cached:
            return cached
        for attempt in range(4):
            try:
                response = requests.post(self.endpoint, json={"dest": language, "content": value}, timeout=(5, 60))
                response.raise_for_status()
                payload = response.json()
                result = payload.get("res") if isinstance(payload, dict) else None
                translated = text(result.get("content")) if isinstance(result, dict) else ""
                if translated:
                    with self.lock:
                        self.cache[key] = translated
                    return translated
            except (requests.RequestException, ValueError, TypeError):
                pass
            if attempt < 3:
                time.sleep(1 + attempt)
        return None

    def ensure_group(self, stage: str, language: str, values: list[str]) -> None:
        values = sorted(set(value for value in values if value))
        total = len(values)
        missing = [value for value in values if self.key(language, value) not in self.cache]
        completed = total - len(missing)
        succeeded = completed
        failed = 0
        self.save_progress(stage, language, completed, total, succeeded, failed)
        if not missing:
            return
        failed_values: list[str] = []
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {executor.submit(self.translate_one, language, value): value for value in missing}
            for future in as_completed(futures):
                value = futures[future]
                completed += 1
                if future.result():
                    succeeded += 1
                else:
                    failed += 1
                    failed_values.append(value)
                if completed % 25 == 0 or completed == total:
                    self.save_cache()
                    self.save_progress(stage, language, completed, total, succeeded, failed)
        self.save_cache()
        if failed_values:
            sample = "; ".join(failed_values[:5])
            raise BuildError(f"{stage}/{language}: {failed} translations failed; examples: {sample}")


def build_rows(
    records: list[dict[str, Any]],
    translator: Translator,
    to_traditional: OpenCC,
    normalized_current_positions: bool = False,
    overrides: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    overrides = overrides or {}
    for language in NAME_LANGUAGES:
        name_values = [record["name"] for record in records if language not in overrides.get(record["person_id"], {}).get("transPersonName", {})]
        translator.ensure_group("names", language, name_values)
    for language in POSITION_LANGUAGES:
        position_values = [position for record in records if language not in overrides.get(record["person_id"], {}).get("occupation", {}) for position in record["positions_zh"]]
        translator.ensure_group("occupations", language, position_values)

    rows: list[dict[str, Any]] = []
    for record in sorted(records, key=lambda item: item["person_id"]):
        entry = overrides.get(record["person_id"], {})
        name_translations = {language: entry.get("transPersonName", {}).get(language) or translator.cache[translator.key(language, record["name"])] for language in NAME_LANGUAGES}
        trans = {"ar": name_translations["ar"], "km": name_translations["km"], "ru": name_translations["ru"], "en": record["en"], "fr": name_translations["fr"], "zh": record["zh"], "es": name_translations["es"]}
        values: list[Any] = [record["name"], record["zh"], record["en"], *trans.values(), *record["aliases"]]
        if record["dataset_region"] in {"HK", "TW"}:
            values.append(to_traditional.convert(record["zh"]))
        positions = record["positions"]
        positions_zh = record["positions_zh"]
        occupation = {"zh": positions_zh}
        for language in POSITION_LANGUAGES:
            occupation[language] = entry.get("occupation", {}).get(language) if language in entry.get("occupation", {}) else [translator.cache[translator.key(language, position)] for position in positions_zh]
        rows.append(
            {
                "personId": record["person_id"],
                "personAvatar": record["avatar"],
                "personName": record["name"],
                "transPersonName": trans,
                "keyword": "|".join(keyword_terms(values)),
                "region": record["region"],
                # The default is an exact source mapping.  The optional
                # legacy mode reproduces the early lite-export behaviour,
                # where current_positions itself used normalized Chinese.
                "current_positions": positions_zh if normalized_current_positions else positions,
                "occupation": occupation,
            }
        )
    return rows


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", nargs="+", required=True, type=Path, help="One or more canonical persons directories")
    parser.add_argument("--output", required=True, type=Path, help="Destination JSONL")
    parser.add_argument("--cache", required=True, type=Path, help="Persistent translation JSON cache")
    parser.add_argument("--progress", required=True, type=Path, help="Progress JSON path")
    parser.add_argument("--report", type=Path, help="Optional JSON audit report")
    parser.add_argument("--translation-endpoint", default="http://10.11.204.238:8080/translate")
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument("--policy", type=Path, help="Optional region replacement policy JSON")
    parser.add_argument("--overrides", type=Path, help="Reviewed per-person translations with source guards")
    parser.add_argument(
        "--exclude-ids",
        type=Path,
        help="Optional JSON list (or object with excluded_person_ids) of canonical person IDs to omit",
    )
    parser.add_argument(
        "--normalized-current-positions",
        action="store_true",
        help="Use normalized Chinese positions in current_positions (legacy export compatibility)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Validate source records without translating or writing JSONL")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.workers < 1 or args.workers > 32:
        raise BuildError("--workers must be between 1 and 32")
    guard_destinations(args.input, [args.output, args.cache, args.progress, args.report], [args.policy, args.exclude_ids, args.overrides])
    to_simplified = OpenCC("t2s")
    records, errors, counts, excluded_counts = collect_records(
        args.input, to_simplified, load_policy(args.policy), load_excluded_ids(args.exclude_ids)
    )
    report = {
        "records": len(records),
        "by_dataset_region": dict(counts),
        "excluded_persons": sum(excluded_counts.values()),
        "excluded_by_dataset_region": dict(excluded_counts),
        "source_errors": errors,
    }
    if errors:
        if args.report:
            atomic_json(args.report, report)
        raise BuildError(f"source validation failed ({len(errors)} errors); see --report for details")
    if args.dry_run:
        load_overrides(args.overrides, records)
        print(json.dumps(report, ensure_ascii=False))
        return
    overrides = load_overrides(args.overrides, records)
    translator = Translator(args.translation_endpoint, args.cache, args.progress, args.workers)
    rows = build_rows(records, translator, OpenCC("s2t"), args.normalized_current_positions, overrides)
    atomic_jsonl(args.output, rows)
    translator.save_progress("completed", "all", len(rows), len(rows), len(rows), 0)
    report.update({"output": str(args.output), "translations_cache": str(args.cache), "status": "completed"})
    if args.report:
        atomic_json(args.report, report)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except (BuildError, OSError, ValueError) as error:
        print(f"ERROR: {error}")
        raise SystemExit(2)
