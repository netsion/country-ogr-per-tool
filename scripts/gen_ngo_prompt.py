"""Generate a P4 sub-agent prompt for a JP NGO person from external template + data.

Usage:
    python gen_ngo_prompt.py JP-PERSON-000431
    python gen_ngo_prompt.py 431

Outputs the final prompt to stdout. Designed to be read by the main session
before each Agent dispatch, ensuring prompt structure stays consistent across
batches (防退化).
"""
import json
import re
import sys
from pathlib import Path

BASE = Path("D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09")
TEMPLATE_FILE = BASE / "_p4_ngo_template.md"
PERSONS_FILE = BASE / "_p4_ngo_persons.json"


def load_template_body() -> str:
    """Extract the template body between the '## 模板正文' marker and the next '## '."""
    text = TEMPLATE_FILE.read_text(encoding="utf-8")
    m = re.search(r"## 模板正文[^\n]*\n(.*?)(?=\n## |\Z)", text, re.S)
    if not m:
        raise RuntimeError("Template body marker not found")
    return m.group(1).strip()


def load_person(person_id: str) -> dict:
    data = json.loads(PERSONS_FILE.read_text(encoding="utf-8"))
    for p in data["persons"]:
        if p["id"] == person_id:
            return p
    raise KeyError(f"{person_id} not found in {PERSONS_FILE}")


def build_prompt(person: dict) -> str:
    template = load_template_body()
    filepath = f"D:/claude-workspace/apec-osint-tool/output/jp/2026-06-09/persons/{person['id']}.json"
    values = {
        "person_id": person["id"],
        "name_local": person["name_local"],
        "name_zh": person["name_zh"],
        "name_en": person["name_en"],
        "org_id": person["org_id"],
        "org_name_local": person["org_name_local"],
        "org_name_zh": person["org_name_zh"],
        "org_short_local": person.get("org_short_local", ""),
        "org_short_en": person.get("org_short_en", ""),
        "org_official_url": person["org_official_url"],
        "role_zh": person["role_zh"],
        "filepath": filepath,
    }
    return re.sub(r"\{(\w+)\}", lambda m: values.get(m.group(1), m.group(0)), template)


def main():
    if len(sys.argv) < 2:
        print("Usage: python gen_ngo_prompt.py <person_id>", file=sys.stderr)
        sys.exit(1)
    arg = sys.argv[1]
    if arg.isdigit():
        arg = f"JP-PERSON-{int(arg):06d}"
    person = load_person(arg)
    prompt = build_prompt(person)
    sys.stdout.reconfigure(encoding="utf-8")
    print(prompt)
    sys.stderr.write(f"\n[meta] person_id={person['id']} prompt_chars={len(prompt)}\n")


if __name__ == "__main__":
    main()
