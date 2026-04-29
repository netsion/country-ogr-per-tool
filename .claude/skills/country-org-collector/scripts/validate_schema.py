#!/usr/bin/env python3
"""
validate_schema.py — Validate org/person JSON files against schema rules
Usage:
  python validate_schema.py output/kr/2026-04-28 [--fix] [--score]
  python validate_schema.py output/kr/2026-04-28 --file orgs/KR-GOV-001.json [--fix] [--score]
  --fix   Auto-fix Unicode smart quotes
  --score Auto-calculate and update completeness_score
"""

import sys; sys.stdout.reconfigure(encoding='utf-8'); sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import re
import glob
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

# --- ID Patterns ---
ORG_ID_RE = re.compile(r'^[A-Z]{2}-[A-Z]+-[0-9]{3}$')
PERSON_ID_RE = re.compile(r'^[A-Z]{2}-PERSON-[0-9]{6}$')
DEPT_ID_RE = re.compile(r'^[A-Z]{2}-[A-Z]+-[0-9]{3}-DEPT-[0-9]{3}$')
QID_RE = re.compile(r'^Q[0-9]+$')
ISO3_RE = re.compile(r'^[A-Z]{3}$')
ISO2_RE = re.compile(r'^[A-Z]{2}$')
STRICT_DATE_RE = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$')
FLEXIBLE_DATE_RE = re.compile(r'^[0-9]{4}(-[0-9]{2}(-[0-9]{2})?)?$')
SMART_QUOTES_RE = re.compile(r'[“”„‟]')


# --- Load enums from JSON Schema files ---
def load_schema_enums():
    enums = {}
    for schema_file in ("org_profile_schema.json", "person_profile_schema.json"):
        path = os.path.join(SKILL_DIR, schema_file)
        if not os.path.exists(path):
            print(f"WARNING: Schema file not found: {path}", file=sys.stderr)
            continue
        with open(path, encoding='utf-8') as f:
            schema = json.load(f)
        for name, defn in schema.get("$defs", {}).items():
            if "enum" in defn:
                enums[name] = set(defn["enum"])
    return enums

ENUMS = load_schema_enums()

# Map schema def names to convenient aliases
ORG_TYPES = ENUMS.get("org_type_enum", set())
ORG_SUBTYPES = ENUMS.get("org_subtype_enum", set())
RELATIONSHIP_TYPES = ENUMS.get("relationship_type_enum", set())
SOCIAL_PLATFORMS = ENUMS.get("social_platform_enum", set())
INDUSTRIES = ENUMS.get("industry_enum", set())
GENDERS = ENUMS.get("gender_enum", set())
CONTACT_TYPES = ENUMS.get("contact_type_enum", set())
DEGREE_LEVELS = ENUMS.get("degree_level_enum", set())
PERSON_REL_TYPES = ENUMS.get("person_relationship_type_enum", set())
FAMILY_RELATIONS = ENUMS.get("family_relation_enum", set())


# --- Helpers ---
class ValidationResult:
    def __init__(self, filepath):
        self.filepath = filepath
        self.errors = []
        self.warnings = []
        self.fixes = []

    @property
    def ok(self):
        return len(self.errors) == 0

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def fix(self, msg):
        self.fixes.append(msg)


def validate_date(value, strict=True, field_name="date"):
    if value is None:
        return None
    if not isinstance(value, str):
        return f"{field_name}: expected string, got {type(value).__name__}"
    pattern = STRICT_DATE_RE if strict else FLEXIBLE_DATE_RE
    if not pattern.match(value):
        expected = "YYYY-MM-DD" if strict else "YYYY / YYYY-MM / YYYY-MM-DD"
        return f"{field_name}: '{value}' does not match {expected}"
    return None


def check_smart_quotes(obj, path=""):
    findings = []
    if isinstance(obj, str):
        matches = SMART_QUOTES_RE.findall(obj)
        if matches:
            findings.append((path, matches))
    elif isinstance(obj, dict):
        for k, v in obj.items():
            findings.extend(check_smart_quotes(v, f"{path}.{k}" if path else k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            findings.extend(check_smart_quotes(v, f"{path}[{i}]"))
    return findings


def fix_smart_quotes(data):
    changed = False
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str):
                fixed = SMART_QUOTES_RE.sub('"', v)
                if fixed != v:
                    data[k] = fixed
                    changed = True
            elif isinstance(v, (dict, list)):
                if fix_smart_quotes(v):
                    changed = True
    elif isinstance(data, list):
        for i, v in enumerate(data):
            if isinstance(v, str):
                fixed = SMART_QUOTES_RE.sub('"', v)
                if fixed != v:
                    data[i] = fixed
                    changed = True
            elif isinstance(v, (dict, list)):
                if fix_smart_quotes(v):
                    changed = True
    return changed


def load_json_file(fpath):
    with open(fpath, encoding='utf-8') as f:
        return json.load(f)


def save_json_file(fpath, data):
    with open(fpath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')


# --- Completeness Scoring ---
def calc_org_score(data):
    filled = 0
    total = 0

    bi = data.get("basic_info", {})
    for f in ["name_original", "name_en", "name_zh", "website",
              "founded_date", "country_iso3", "hq_country_iso3", "org_type", "org_subtype"]:
        total += 1
        if bi.get(f):
            filled += 1

    for field, weight, cap in [
        ("key_people", 3, 5),
        ("social_accounts", 2, 4),
        ("recent_events", 3, 5),
        ("related_entities", 2, 4),
        ("departments", 1, 3),
        ("digital_assets", 1, 3),
    ]:
        items = data.get(field, [])
        total += weight * cap
        filled += weight * min(len([x for x in items if x]), cap)

    for field, weight in [("core_business", 8), ("apec_stance", 4)]:
        total += weight
        val = data.get(field)
        if val and isinstance(val, str):
            filled += weight if len(val) >= 100 else weight // 2

    total += 2
    if data.get("profile", {}).get("source_url"):
        filled += 2

    return min(round(filled / total * 100), 100) if total > 0 else 0


def calc_person_score(data):
    filled = 0
    total = 0

    for f in ["name", "name_en", "name_zh", "nationality", "gender", "birth_date", "birth_place"]:
        total += 1
        if data.get(f):
            filled += 1

    # biography_summary
    total += 12
    bio = data.get("biography_summary")
    if bio and isinstance(bio, str):
        if len(bio) >= 200:
            filled += 12
        elif len(bio) >= 100:
            filled += 8
        else:
            filled += 4

    for field, weight, cap in [
        ("education", 2, 4),
        ("work_experience", 3, 5),
        ("social_accounts", 2, 4),
        ("political_stances", 2, 4),
        ("person_relationships", 2, 4),
        ("major_achievements", 2, 4),
        ("family_members", 1, 3),
        ("contacts", 1, 2),
    ]:
        items = data.get(field, [])
        total += weight * cap
        filled += weight * min(len([x for x in items if x]), cap)

    total += 2
    if data.get("wikidata_qid"):
        filled += 1
    if data.get("profile", {}).get("source_url"):
        filled += 1

    return min(round(filled / total * 100), 100) if total > 0 else 0


# --- Validation ---
def validate_org_profile(data, filepath):
    r = ValidationResult(filepath)

    org_id = data.get("org_id", "")
    if not org_id:
        r.error("missing org_id")
    elif not ORG_ID_RE.match(org_id):
        r.error(f"org_id '{org_id}' does not match pattern {{ISO2}}-{{TYPE}}-{{SEQ}}")

    bi = data.get("basic_info")
    if not bi:
        r.error("missing basic_info")
        return r

    required_bi = ["name_original", "name_en", "org_type", "org_subtype", "country_iso3", "hq_country_iso3"]
    for f in required_bi:
        if not bi.get(f):
            r.warn(f"basic_info.{f} is empty")

    if bi.get("org_type") and bi["org_type"] not in ORG_TYPES:
        r.error(f"basic_info.org_type '{bi['org_type']}' not in valid org_types")
    if bi.get("org_subtype") and bi["org_subtype"] not in ORG_SUBTYPES:
        r.error(f"basic_info.org_subtype '{bi['org_subtype']}' not in valid org_subtypes")
    if bi.get("country_iso3") and not ISO3_RE.match(bi["country_iso3"]):
        r.error(f"basic_info.country_iso3 '{bi['country_iso3']}' not ISO3 format")
    if bi.get("hq_country_iso3") and not ISO3_RE.match(bi["hq_country_iso3"]):
        r.error(f"basic_info.hq_country_iso3 '{bi['hq_country_iso3']}' not ISO3 format")

    err = validate_date(bi.get("founded_date"), strict=True, field_name="basic_info.founded_date")
    if err:
        r.error(err)

    for i, sa in enumerate(data.get("social_accounts", [])):
        if not sa.get("platform"):
            r.warn(f"social_accounts[{i}].platform is empty")
        elif sa["platform"] not in SOCIAL_PLATFORMS:
            r.error(f"social_accounts[{i}].platform '{sa['platform']}' not valid")
        if not sa.get("url"):
            r.warn(f"social_accounts[{i}].url is empty")

    for i, kp in enumerate(data.get("key_people", [])):
        if not kp.get("name"):
            r.warn(f"key_people[{i}].name is empty")
        if not kp.get("title"):
            r.warn(f"key_people[{i}].title is empty")
        pid = kp.get("person_id")
        if pid and not PERSON_ID_RE.match(pid):
            r.error(f"key_people[{i}].person_id '{pid}' invalid format")

    for i, dept in enumerate(data.get("departments", [])):
        if not dept.get("dept_id"):
            r.warn(f"departments[{i}].dept_id is empty")
        elif not DEPT_ID_RE.match(dept["dept_id"]):
            r.error(f"departments[{i}].dept_id '{dept['dept_id']}' invalid format")
        if not dept.get("name"):
            r.warn(f"departments[{i}].name is empty")

    for i, ev in enumerate(data.get("recent_events", [])):
        err = validate_date(ev.get("date"), strict=True, field_name=f"recent_events[{i}].date")
        if err:
            r.error(err)
        if not ev.get("title"):
            r.warn(f"recent_events[{i}].title is empty")
        if not ev.get("description"):
            r.warn(f"recent_events[{i}].description is empty")

    for i, re_ in enumerate(data.get("related_entities", [])):
        if not re_.get("org_name"):
            r.warn(f"related_entities[{i}].org_name is empty")
        if re_.get("relationship_type") and re_["relationship_type"] not in RELATIONSHIP_TYPES:
            r.error(f"related_entities[{i}].relationship_type '{re_['relationship_type']}' not in standard enum")

    for i, ind in enumerate(data.get("industries", [])):
        if ind not in INDUSTRIES:
            r.error(f"industries[{i}] '{ind}' not in valid industries")

    for field in ("apec_stance", "core_business"):
        val = data.get(field)
        if val is not None and not isinstance(val, str):
            r.error(f"{field}: expected string or null, got {type(val).__name__}")

    meta = data.get("collection_meta", {})
    err = validate_date(meta.get("collection_date"), strict=True, field_name="collection_meta.collection_date")
    if err:
        r.error(err)
    score = meta.get("completeness_score")
    if score is not None and (not isinstance(score, int) or score < 0 or score > 100):
        r.error(f"completeness_score {score} out of range [0, 100]")

    return r


def validate_person_profile(data, filepath):
    r = ValidationResult(filepath)

    pid = data.get("person_id", "")
    if not pid:
        r.error("missing person_id")
    elif not PERSON_ID_RE.match(pid):
        r.error(f"person_id '{pid}' does not match pattern {{ISO2}}-PERSON-{{SEQ(6)}}")

    for f in ["name", "name_en", "nationality", "gender"]:
        if not data.get(f):
            r.error(f"missing required field: {f}")

    nat = data.get("nationality")
    if nat and not ISO2_RE.match(nat):
        r.error(f"nationality '{nat}' not ISO2 format")
    gender = data.get("gender")
    if gender and gender not in GENDERS:
        r.error(f"gender '{gender}' not in valid values")

    qid = data.get("wikidata_qid")
    if qid and not QID_RE.match(qid):
        r.error(f"wikidata_qid '{qid}' not valid QID format")

    err = validate_date(data.get("birth_date"), strict=True, field_name="birth_date")
    if err:
        r.error(err)

    for i, edu in enumerate(data.get("education", [])):
        if not edu.get("institution"):
            r.warn(f"education[{i}].institution is empty")
        for df in ["start_date", "end_date"]:
            err = validate_date(edu.get(df), strict=False, field_name=f"education[{i}].{df}")
            if err:
                r.error(err)

    for i, work in enumerate(data.get("work_experience", [])):
        if not work.get("organization"):
            r.warn(f"work_experience[{i}].organization is empty")
        if not work.get("position"):
            r.warn(f"work_experience[{i}].position is empty")
        for df in ["start_date", "end_date"]:
            err = validate_date(work.get(df), strict=False, field_name=f"work_experience[{i}].{df}")
            if err:
                r.error(err)

    for i, sa in enumerate(data.get("social_accounts", [])):
        if not sa.get("platform"):
            r.warn(f"social_accounts[{i}].platform is empty")
        elif sa["platform"] not in SOCIAL_PLATFORMS:
            r.error(f"social_accounts[{i}].platform '{sa['platform']}' not valid")
        if not sa.get("url"):
            r.warn(f"social_accounts[{i}].url is empty")

    for i, rel in enumerate(data.get("person_relationships", [])):
        if not rel.get("person_name"):
            r.warn(f"person_relationships[{i}].person_name is empty")
        rt = rel.get("relationship_type")
        if rt and rt not in PERSON_REL_TYPES:
            r.error(f"person_relationships[{i}].relationship_type '{rt}' not in valid enum")

    import re
    _PLACEHOLDER_PATTERNS = re.compile(
        r'^(未公开|姓名未公开|不详|未知|'
        r'配偶|长子|次子|三子|长女|次女|女儿|儿子|父亲|母亲|'
        r'[^\s]{1,2}氏[^\s]*(之子)?$|'
        r'[（(].*[)）]$|'
        r'.*[（(](?:姓名未公开|未公开|妻子|配偶|长女|次女|长子|次子|一子|一女).*$|'
        r'.*未公开.*$|'
        r'.*不详.*$)',
        re.IGNORECASE
    )

    for i, fam in enumerate(data.get("family_members", [])):
        if not fam.get("name"):
            r.error(f"family_members[{i}].name is empty (discard the entry if name is unknown)")
        elif _PLACEHOLDER_PATTERNS.match(fam.get("name", "").strip()):
            r.error(f"family_members[{i}].name '{fam['name']}' is a placeholder, not a real name — discard this entry")
        fr = fam.get("relationship")
        if not fr:
            r.error(f"family_members[{i}].relationship is empty")
        elif fr not in FAMILY_RELATIONS:
            r.error(f"family_members[{i}].relationship '{fr}' not in valid enum (expected: spouse, son, daughter, etc.)")

    for i, ps in enumerate(data.get("political_stances", [])):
        if not ps.get("topic"):
            r.warn(f"political_stances[{i}].topic is empty")
        if not ps.get("stance_content"):
            r.error(f"political_stances[{i}].stance_content is empty or using wrong field name (not 'stance')")

    for i, ach in enumerate(data.get("major_achievements", [])):
        if not ach.get("achievement"):
            r.warn(f"major_achievements[{i}].achievement is empty")

    meta = data.get("collection_meta", {})
    err = validate_date(meta.get("collection_date"), strict=True, field_name="collection_meta.collection_date")
    if err:
        r.error(err)
    score = meta.get("completeness_score")
    if score is not None and (not isinstance(score, int) or score < 0 or score > 100):
        r.error(f"completeness_score {score} out of range [0, 100]")

    return r


# --- Single file processing ---
def process_file(fpath, is_org, fix=False, score=False):
    fname = os.path.basename(fpath)
    try:
        data = load_json_file(fpath)
    except json.JSONDecodeError as e:
        print(f"  PARSE ERROR: {fname}: {e}")
        return 1, 0, 0

    validate_fn = validate_org_profile if is_org else validate_person_profile
    calc_fn = calc_org_score if is_org else calc_person_score

    result = validate_fn(data, fpath)

    sq_findings = check_smart_quotes(data)
    for path, matches in sq_findings:
        result.warn(f"Unicode smart quote(s) at {path}: {matches}")

    if fix and sq_findings:
        if fix_smart_quotes(data):
            save_json_file(fpath, data)
            result.fix(f"Fixed {len(sq_findings)} smart quote occurrences")

    if score:
        new_score = calc_fn(data)
        old_score = data.get("collection_meta", {}).get("completeness_score")
        if old_score != new_score:
            if "collection_meta" not in data:
                data["collection_meta"] = {}
            data["collection_meta"]["completeness_score"] = new_score
            save_json_file(fpath, data)
            result.fix(f"completeness_score: {old_score} → {new_score}")

    if result.errors or result.warnings or result.fixes:
        status = "ERRORS" if result.errors else ("FIXES" if result.fixes else "WARNINGS")
        print(f"  {status}: {fname}")
        for e in result.errors:
            print(f"    ERR: {e}")
        for w in result.warnings:
            print(f"    WRN: {w}")
        for f in result.fixes:
            print(f"    FIX: {f}")

    return len(result.errors), len(result.warnings), len(result.fixes)


# --- Cross-reference Validation ---

def validate_cross_refs(base_dir):
    """Check cross-file references: org key_people→persons, person work_experience→orgs, related_entities→registry."""
    orgs_dir = os.path.join(base_dir, "orgs")
    persons_dir = os.path.join(base_dir, "persons")
    registry_file = os.path.join(base_dir, "id_registry.json")

    errors = 0
    warnings = 0

    # Build index sets
    org_ids_in_files = set()
    person_ids_in_files = set()
    registry_org_ids = set()
    registry_person_ids = set()

    if os.path.isdir(orgs_dir):
        for fpath in glob.glob(os.path.join(orgs_dir, "*.json")):
            if os.path.basename(fpath).startswith("_"):
                continue
            try:
                data = load_json_file(fpath)
                org_ids_in_files.add(data.get("org_id"))
            except Exception:
                pass

    if os.path.isdir(persons_dir):
        for fpath in glob.glob(os.path.join(persons_dir, "*.json")):
            if os.path.basename(fpath).startswith("_"):
                continue
            try:
                data = load_json_file(fpath)
                person_ids_in_files.add(data.get("person_id"))
            except Exception:
                pass

    if os.path.exists(registry_file):
        reg = load_json_file(registry_file)
        for r in reg.get("registry", []):
            registry_org_ids.add(r.get("org_id"))
        for p in reg.get("person_registry", []):
            registry_person_ids.add(p.get("person_id"))

    print(f"\n=== Cross-Reference Validation ===")
    print(f"  Org files: {len(org_ids_in_files)}, Person files: {len(person_ids_in_files)}")
    print(f"  Registry orgs: {len(registry_org_ids)}, Registry persons: {len(registry_person_ids)}")

    # Check org → person references
    if os.path.isdir(orgs_dir):
        for fpath in sorted(glob.glob(os.path.join(orgs_dir, "*.json"))):
            if os.path.basename(fpath).startswith("_"):
                continue
            fname = os.path.basename(fpath)
            try:
                data = load_json_file(fpath)
            except Exception:
                continue
            for i, kp in enumerate(data.get("key_people", [])):
                pid = kp.get("person_id")
                if not pid:
                    continue
                if pid not in person_ids_in_files and pid not in registry_person_ids:
                    print(f"  WRN: {fname} key_people[{i}].person_id '{pid}' not found in persons/ or registry")
                    warnings += 1
                elif pid not in person_ids_in_files and pid in registry_person_ids:
                    print(f"  WRN: {fname} key_people[{i}].person_id '{pid}' in registry but no profile file")
                    warnings += 1
            for i, re_ in enumerate(data.get("related_entities", [])):
                oid = re_.get("org_id")
                if not oid:
                    continue
                if oid not in registry_org_ids:
                    print(f"  ERR: {fname} related_entities[{i}].org_id '{oid}' not in id_registry.json")
                    errors += 1

    # Check person → org references
    if os.path.isdir(persons_dir):
        for fpath in sorted(glob.glob(os.path.join(persons_dir, "*.json"))):
            if os.path.basename(fpath).startswith("_"):
                continue
            fname = os.path.basename(fpath)
            try:
                data = load_json_file(fpath)
            except Exception:
                continue
            for i, we in enumerate(data.get("work_experience", [])):
                oid = we.get("org_id")
                if not oid:
                    continue
                if oid not in org_ids_in_files and oid not in registry_org_ids:
                    print(f"  WRN: {fname} work_experience[{i}].org_id '{oid}' not found in orgs/ or registry")
                    warnings += 1
            for i, rel in enumerate(data.get("person_relationships", [])):
                pid = rel.get("person_id")
                if not pid:
                    continue
                if pid not in person_ids_in_files and pid not in registry_person_ids:
                    print(f"  WRN: {fname} person_relationships[{i}].person_id '{pid}' not found")
                    warnings += 1

    # Check registry → file consistency
    for oid in registry_org_ids:
        if oid and oid not in org_ids_in_files:
            reg_entry = next((r for r in reg.get("registry", []) if r.get("org_id") == oid), {})
            status = reg_entry.get("status", "")
            if status == "profiled":
                print(f"  WRN: registry org '{oid}' status=profiled but no file in orgs/")
                warnings += 1

    print(f"  Cross-ref errors: {errors}, warnings: {warnings}")
    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description="Validate org/person JSON profiles against schema")
    parser.add_argument("output_dir", help="Output directory (e.g., output/kr/2026-04-28)")
    parser.add_argument("--fix", action="store_true", help="Auto-fix Unicode smart quotes")
    parser.add_argument("--score", action="store_true", help="Auto-calculate and update completeness_score")
    parser.add_argument("--type", choices=["org", "person", "all"], default="all", help="What to validate")
    parser.add_argument("--file", help="Validate a single file (relative to output_dir)")
    parser.add_argument("--cross-ref", action="store_true", help="Validate cross-file references (org↔person, registry)")
    args = parser.parse_args()

    base_dir = args.output_dir.rstrip("/\\")

    total_errors = 0
    total_warnings = 0
    total_fixes = 0
    files_checked = 0

    # Single file mode
    if args.file:
        fpath = os.path.join(base_dir, args.file) if not os.path.isabs(args.file) else args.file
        if not os.path.exists(fpath):
            print(f"File not found: {fpath}")
            return 1
        is_org = "\\orgs\\" in fpath or "/orgs/" in fpath or ORG_ID_RE.match(os.path.basename(fpath).split(".")[0])
        files_checked = 1
        errors, warnings, fixes = process_file(fpath, is_org, args.fix, args.score)
        total_errors = errors
        total_warnings = warnings
        total_fixes = fixes
    else:
        # Directory scan mode
        orgs_dir = os.path.join(base_dir, "orgs")
        persons_dir = os.path.join(base_dir, "persons")

        if args.type in ("org", "all") and os.path.isdir(orgs_dir):
            print(f"\n=== Validating Org Profiles ({orgs_dir}) ===")
            for fpath in sorted(glob.glob(os.path.join(orgs_dir, "*.json"))):
                if os.path.basename(fpath).startswith("_"):
                    continue
                files_checked += 1
                e, w, f = process_file(fpath, True, args.fix, args.score)
                total_errors += e
                total_warnings += w
                total_fixes += f

        if args.type in ("person", "all") and os.path.isdir(persons_dir):
            print(f"\n=== Validating Person Profiles ({persons_dir}) ===")
            for fpath in sorted(glob.glob(os.path.join(persons_dir, "*.json"))):
                if os.path.basename(fpath).startswith("_"):
                    continue
                files_checked += 1
                e, w, f = process_file(fpath, False, args.fix, args.score)
                total_errors += e
                total_warnings += w
                total_fixes += f

    print(f"\n=== Summary ===")
    print(f"  Files checked: {files_checked}")
    print(f"  Errors: {total_errors}")
    print(f"  Warnings: {total_warnings}")
    if args.fix or args.score:
        print(f"  Auto-fixes: {total_fixes}")

    # Cross-reference validation
    if args.cross_ref and not args.file:
        cr_errors, cr_warnings = validate_cross_refs(base_dir)
        total_errors += cr_errors
        total_warnings += cr_warnings

    return 1 if total_errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
