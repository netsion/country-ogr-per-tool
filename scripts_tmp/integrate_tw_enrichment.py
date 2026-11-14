"""Install researched TW profiles with identity and schema checks; maintain batch progress."""
import json
import pathlib
import sys
from datetime import datetime

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / 'output/tw/2026-07-27'
STAGE = ROOT / 'tmp/tw_enrichment'
SCHEMA = json.loads((ROOT / '.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'))
BATCH = ['000001', '000012', '000018', '000032', '000011', '000035', '000023', '000026', '000508', '000526']

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def save(path, data):
    temp = path.with_suffix('.json.tmp')
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temp.replace(path)

def main():
    pid = sys.argv[1]
    if pid not in ['TW-PERSON-' + n for n in BATCH]:
        raise ValueError('Profile is not in the reviewed first batch')
    data = read(STAGE / (pid + '.json'))
    current_path = BASE / 'persons' / (pid + '.json')
    old = read(current_path)
    assert data['person_id'] == old['person_id'] == pid
    assert data.get('wikidata_qid') == old.get('wikidata_qid'), 'Identity changed'
    jsonschema.Draft7Validator(SCHEMA).validate(data)
    meta = data.get('collection_meta', {})
    assert meta.get('phase') == 'phase4_person_profile'
    assert len(meta.get('quotes', [])) >= 3
    assert len(data.get('biography_summary', '')) >= 200
    assert len(data.get('work_experience', [])) >= 2
    backup = STAGE / 'before_install'
    backup.mkdir(exist_ok=True)
    bp = backup / (pid + '.json')
    if not bp.exists():
        save(bp, old)
    save(current_path, data)
    pp = BASE / '_phase_progress.json'
    progress = read(pp) if pp.exists() else {}
    if progress.get('phase') != 'P4_person_enrichment_batch1':
        progress = {'phase': 'P4_person_enrichment_batch1', 'started_at': datetime.now().isoformat(timespec='seconds'),
                    'completed': [], 'remaining': ['TW-PERSON-' + n for n in BATCH], 'current': None, 'failed': []}
    if pid not in progress['completed']:
        progress['completed'].append(pid)
    progress['remaining'] = [v for v in progress['remaining'] if v != pid]
    progress['current'] = None
    progress['last_updated'] = datetime.now().isoformat(timespec='seconds')
    save(pp, progress)
    print(json.dumps({'installed': pid, 'completed': len(progress['completed']), 'remaining': len(progress['remaining'])}))

if __name__ == '__main__':
    main()
