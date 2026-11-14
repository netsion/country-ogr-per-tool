"""Correct a verified cross-company identity mix-up without carrying over the false alias."""
import pathlib
import sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/country-org-collector/scripts'))
from atomic_write import load_json, save_json
BASE = ROOT / 'output/tw/2026-07-27'
path = BASE / 'orgs/TW-CORP-014.json'
org = load_json(str(path))
org['wikidata_qid'] = 'Q15908529'
org['basic_info'].update(name_en='Unimicron Technology Corp.', name_original='欣興電子股份有限公司', org_subtype='publicly_listed', website='https://www.unimicron.com/')
org['collection_meta']['notes'] += '；本轮核实旧英文King Yuan Electronics属于京元电子，与本档中文名和PCB业务不符，已纠正为Unimicron Technology Corp.，QID由错绑Q117262637改为Q15908529。历史错误链接不作为本轮证据。'
org['collection_meta']['quotes'] = [q for q in org['collection_meta']['quotes'] if 'Q117262637' not in q['url']]
org['collection_meta']['quotes'] += [
 {'title': '欣興電子：名称、上市类型与业务', 'url': 'https://zh.wikipedia.org/wiki/欣興電子'},
 {'title': 'Unimicron Wikidata：QID及中文链接', 'url': 'https://www.wikidata.org/wiki/Q15908529'},
 {'title': '京元电子官网：排除King Yuan Electronics误绑', 'url': 'https://www.kyec.com.tw/zh-tw/About/公司簡介'}]
org['collection_meta']['data_sources'] = ['wikipedia', 'wikidata', 'official_website']
save_json(str(path), org)
reg = load_json(str(BASE / 'id_registry.json'))
for entry in reg['registry']:
    if entry.get('org_id') == 'TW-CORP-014':
        entry.update(name=org['basic_info']['name_original'], name_en=org['basic_info']['name_en'], wikidata_qid=org['wikidata_qid'])
save_json(str(BASE / 'id_registry.json'), reg)
tsmcpath = BASE / 'orgs/TW-CORP-041.json'
tsmc = load_json(str(tsmcpath))
tsmc['basic_info']['org_subtype'] = 'publicly_listed'
tsmc['collection_meta']['quotes'].append({'title': 'TSMC董事会公告：上市代码与董事长任命', 'url': 'https://pr.tsmc.com/schinese/news/3148'})
if 'official_website' not in tsmc['collection_meta']['data_sources']:
    tsmc['collection_meta']['data_sources'].append('official_website')
save_json(str(tsmcpath), tsmc)
print('Corrected TW-CORP-014 identity and verified two listed-company subtypes')
