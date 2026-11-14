"""Register four verified institutions missing from the TW collection."""
import json
import pathlib
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/country-org-collector/scripts'))
from atomic_write import save_json, load_json
BASE = ROOT / 'output/tw/2026-07-27'
reg = load_json(str(BASE / 'id_registry.json'))
rows = [
 ('總統府', '总统府', 'Office of the President', 'head_of_state', 'https://www.president.gov.tw/', 'https://www.president.gov.tw/Page/694'),
 ('外交部', '外交部', 'Ministry of Foreign Affairs', 'ministry', 'https://www.mofa.gov.tw/', 'https://www.mofa.gov.tw/MofaLeader_Content.aspx?mls=138&n=88'),
 ('國防部', '国防部', 'Ministry of National Defense', 'ministry', 'https://www.mnd.gov.tw/', 'https://www.mnd.gov.tw/Publication/83001'),
 ('臺北市政府', '台北市政府', 'Taipei City Government', 'local_government', 'https://www.gov.taipei/', 'https://www.gov.taipei/News_Content_Leader.aspx?n=5A0C91ADEE6E7C46&s=5C77853F1AB78232&sms=7CAF6BD4D3E48630'),
]
for original, zh, en, subtype, website, source in rows:
    existing = next((r for r in reg['registry'] if r.get('name') == original or r.get('name_en') == en), None)
    if existing:
        print('existing', existing['org_id'], original)
        continue
    seq = reg['counters'].get('TW-GOV', 0) + 1
    oid = f'TW-GOV-{seq:03d}'
    assert not (BASE / 'orgs' / (oid + '.json')).exists()
    reg['counters']['TW-GOV'] = seq
    reg['registry'].append({'org_id': oid, 'name': original, 'name_zh': zh, 'name_en': en, 'org_type': 'GOV', 'wikidata_qid': None, 'status': 'profiled'})
    save_json(str(BASE / 'id_registry.json'), reg)
    data = {'org_id': oid, 'wikidata_qid': None,
        'basic_info': {'name_original': original, 'name_zh': zh, 'name_en': en, 'org_type': 'GOV', 'org_subtype': subtype, 'country_iso3': 'TWN', 'hq_country_iso3': 'TWN', 'website': website, 'aliases': []},
        'key_people': [], 'departments': [], 'related_entities': [], 'recent_events': [], 'social_accounts': [], 'digital_assets': [],
        'collection_meta': {'collection_date': '2026-11-13', 'phase': 'phase2_skeleton', 'data_sources': ['official_website'], 'quotes': [{'title': original + '官方首长简介', 'url': source}], 'notes': '本轮为首批人物任职关联补建的来源骨架；尚未执行组织全面深度采集。'}}
    save_json(str(BASE / 'orgs' / (oid + '.json')), data)
    print('registered', oid, original)
