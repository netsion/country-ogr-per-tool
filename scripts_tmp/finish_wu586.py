import json,pathlib,jsonschema
p=pathlib.Path('tmp/tw_batch8_enriched/TW-PERSON-000586.json');d=json.loads(p.read_text(encoding='utf-8'))
d['person_relationships']=[dict(person_id=None,person_name=n,relationship_type='subordinate',description=x) for n,x in [('林法正','2024年5月22日新任國科會團隊記者會，吳誠文說明邀請其任政務副主委，借重電力電網專業推動功率半導體；僅記當時具體任職分工，不推定長期私人關係。來源：https://www.ithome.com.tw/news/163029'),('陳炳宇','2024年5月22日，吳誠文說明邀請其任國科會政務副主委，借重AI電腦視覺專業協助AI技術及產業應用；僅記當時上下級分工，未核其2026續任。來源：https://www.ithome.com.tw/news/163029')]]
d['collection_meta']['quotes'].append(dict(title='新任國科會主委吳誠文：借重半導體產業優勢，結合AI等科技加速產業智慧化發展',url='https://www.ithome.com.tw/news/163029'))
d['collection_meta']['notes']+=' 人物關係僅記2024年5月具體分工；兩人索引無命中，ID為null。所有任職org_id暫null，避免未讀正式組織画像而引錯。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
