"""Re-encode a JSON file with ensure_ascii=False for readable CJK output.

Usage: python scripts/ensure_utf8.py <path> [path2 ...]

Reads each JSON file, validates it parses correctly, then re-writes with
ensure_ascii=False + indent=2 so CJK characters are human-readable.
"""
import json, sys

for path in sys.argv[1:]:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    org_id = data.get('org_id', data.get('person_id', '?'))
    score = data.get('collection_meta', {}).get('completeness_score', '?')
    print(f"OK: {org_id} score={score} ({len(json.dumps(data))} chars)")
