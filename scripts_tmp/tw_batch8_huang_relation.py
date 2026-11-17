"""Clarify the election-stage party roles without implying earlier inauguration."""
import pathlib,json
p=pathlib.Path(__file__).resolve().parents[1]/'tmp/tw_batch8_enriched/TW-PERSON-000596.json'
d=json.loads(p.read_text(encoding='utf-8'));r=d['person_relationships'][0]
assert r['person_id']=='TW-PERSON-000577' and '2026年5月24日' in r['description']
r['description']='2026年5月24日中央社报道，吴沛忆、黄捷分别当选台北、高雄市党部主委，并宣布组成北高连线共同推动党务革新。仅限定该次公开党务合作，不推定私人关系；黄捷6月8日正式就职另据就职报道。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
