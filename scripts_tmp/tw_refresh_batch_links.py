"""Refresh only researched first-batch names, verified current leadership and list metadata."""
import pathlib
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/country-org-collector/scripts'))
from atomic_write import load_json, save_json
BASE = ROOT / 'output/tw/2026-07-27'
progress = load_json(str(BASE / '_phase_progress.json'))
completed = set(progress['completed'])
mapping = {
 '000001': [('TW-GOV-023', '台湾地区领导人'), ('TW-PARTY-012', '主席')],
 '000012': [('TW-GOV-023', '台湾地区副领导人')],
 '000018': [('TW-GOV-019', '院长')],
 '000032': [('TW-GOV-019', '副院长')],
 '000011': [('TW-GOV-020', '院长')],
 '000035': [('TW-GOV-020', '副院长')],
 '000023': [('TW-GOV-024', '部长')],
 '000026': [('TW-GOV-025', '部长')],
 '000508': [('TW-CORP-041', '董事长兼总裁')],
 '000526': [('TW-GOV-026', '市长')],
}
persons = load_json(str(BASE / 'person_list.json'))
reg = load_json(str(BASE / 'id_registry.json'))
for number, links in mapping.items():
    pid = 'TW-PERSON-' + number
    if pid not in completed:
        continue
    person = load_json(str(BASE / 'persons' / (pid + '.json')))
    source_orgs = []
    for oid, title in links:
        op = BASE / 'orgs' / (oid + '.json')
        org = load_json(str(op))
        org['key_people'] = [k for k in org.get('key_people', []) if k.get('person_id') != pid]
        org['key_people'].append({'person_id': pid, 'name': person['name'], 'title': title,
             'title_description': None, 'description': '本轮依据人物档案所列官方履历核实；其他旧关键人物记录仍待复核。'})
        om = org.setdefault('collection_meta', {})
        quotes = om.setdefault('quotes', [])
        for quote in person['collection_meta']['quotes']:
            if quote['url'] not in {q['url'] for q in quotes}:
                quotes.append(quote)
        sources = om.setdefault('data_sources', [])
        if 'official_website' not in sources:
            sources.append('official_website')
        save_json(str(op), org)
        source_orgs.append({'org_id': oid, 'org_name': org['basic_info']['name_original'], 'position_title': title})
    for entry in persons['persons']:
        if entry['person_id'] == pid:
            entry.update(name=person['name'], name_zh=person.get('name_zh'), name_en=person['name_en'],
                         importance_level='high', importance_reason='首批核心人物；现职已按引用来源核查', source_orgs=source_orgs,
                         notes='已完成首批公开资料丰富；字段缺失与证据边界见人物collection_meta.notes。完整度未达85者仍需补充。')
    for entry in reg.get('person_registry', []):
        if entry.get('person_id') == pid:
            entry.update(name=person['name'], name_zh=person.get('name_zh'), name_en=person['name_en'])
persons['summary']['by_importance_level'] = {level: sum(x['importance_level'] == level for x in persons['persons']) for level in ['high', 'medium', 'low']}
persons['metadata']['source_org_count'] = len(list((BASE / 'orgs').glob('TW-*.json')))
persons['metadata']['total_persons'] = len(persons['persons'])
save_json(str(BASE / 'person_list.json'), persons)
save_json(str(BASE / 'id_registry.json'), reg)
print('Refreshed current leadership for', len(completed), 'researched people')
