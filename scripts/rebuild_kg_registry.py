"""Rebuild id_registry.json to include all org files in output/kg/2026-06-21/orgs/."""
import json, glob, os, sys, re
sys.stdout.reconfigure(encoding='utf-8')

output_dir = 'output/kg/2026-06-21'
reg_path = os.path.join(output_dir, 'id_registry.json')

# Load existing registry (preserve person_registry & counters)
reg = json.load(open(reg_path, encoding='utf-8'))
existing_org_entries = reg.get('registry', [])
existing_org_ids = {e['org_id'] for e in existing_org_entries}

# Scan all org files
org_files = sorted(glob.glob(os.path.join(output_dir, 'orgs', '*.json')))
print(f'Org files on disk: {len(org_files)}')
print(f'Org entries in registry: {len(existing_org_entries)}')

# Build map of existing
reg_by_id = {e['org_id']: e for e in existing_org_entries}

# For each org file, ensure registry entry exists
new_count = 0
for f in org_files:
    d = json.load(open(f, encoding='utf-8'))
    org_id = d.get('basic_info', {}).get('org_id') or d.get('org_id') or os.path.basename(f).replace('.json', '')
    if not org_id or not re.match(r'^[A-Z]{2}-[A-Z]+-[0-9]{3}$', org_id):
        continue
    if org_id in reg_by_id:
        # Update status to profiled
        reg_by_id[org_id]['status'] = 'profiled'
        # Update name if missing/None
        if not reg_by_id[org_id].get('name') or reg_by_id[org_id].get('name') == 'None':
            name_zh = d.get('basic_info', {}).get('name_zh') or d.get('name_zh')
            name_en = d.get('basic_info', {}).get('name_en') or d.get('name_en')
            reg_by_id[org_id]['name'] = name_zh or name_en or org_id
        # Update org_type
        ot = d.get('basic_info', {}).get('org_type') or d.get('org_type')
        if ot:
            reg_by_id[org_id]['org_type'] = ot
        # Update org_subtype
        ost = d.get('basic_info', {}).get('org_subtype')
        if ost:
            reg_by_id[org_id]['org_subtype'] = ost
        # Update wikidata_qid
        wqid = d.get('basic_info', {}).get('wikidata_qid') or d.get('wikidata_qid')
        if wqid:
            reg_by_id[org_id]['wikidata_qid'] = wqid
    else:
        # New entry
        bi = d.get('basic_info', {}) or {}
        name_zh = bi.get('name_zh') or d.get('name_zh')
        name_en = bi.get('name_en') or d.get('name_en')
        new_entry = {
            'org_id': org_id,
            'name': name_zh or name_en or org_id,
            'org_type': bi.get('org_type') or d.get('org_type'),
            'org_subtype': bi.get('org_subtype'),
            'wikidata_qid': bi.get('wikidata_qid') or d.get('wikidata_qid'),
            'status': 'profiled',
            'notes': None,
        }
        existing_org_entries.append(new_entry)
        reg_by_id[org_id] = new_entry
        new_count += 1

# Sort entries by org_id
def sort_key(e):
    parts = e['org_id'].split('-')
    return (parts[0], parts[1], int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0)
existing_org_entries.sort(key=sort_key)

reg['registry'] = existing_org_entries
# Update counters
from collections import Counter
type_counts = Counter(e['org_type'] for e in existing_org_entries if e.get('org_type'))
reg['counters'] = dict(type_counts)

# Atomic write
tmp = reg_path + '.tmp'
with open(tmp, 'w', encoding='utf-8') as out:
    json.dump(reg, out, ensure_ascii=False, indent=2)
os.replace(tmp, reg_path)

print(f'Added {new_count} new org entries to registry')
print(f'Total org entries now: {len(existing_org_entries)}')
print(f'Type counts: {dict(type_counts)}')
