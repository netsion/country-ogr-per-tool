"""Record only previously inspected exact-reference organization decisions."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];O=R/'tmp/tw_batch5_20261115'
rows=json.loads((O/'null_org_candidates.json').read_text(encoding='utf-8'))
allowed={'TW-ACAD-019':'國立臺灣大學','TW-GOV-024':'外交部','TW-GOV-020':'立法院','TW-PARTY-012':'民主進步黨','TW-GOV-019':'行政院','TW-ACAD-028':'國立臺灣藝術大學'}
reviewed={('TW-PERSON-000512',1),('TW-PERSON-000548',10),('TW-PERSON-000549',0),('TW-PERSON-000549',2),('TW-PERSON-000550',0),('TW-PERSON-000550',2),('TW-PERSON-000550',3),('TW-PERSON-000551',0),('TW-PERSON-000552',4),('TW-PERSON-000553',0),('TW-PERSON-000553',5),('TW-PERSON-000554',2),('TW-PERSON-000554',3),('TW-PERSON-000554',4)}
result=[]
for r in rows:
 if (r['person_id'],r['index']) not in reviewed:continue
 assert len(r['candidates'])==1
 t=r['candidates'][0];assert allowed[t['id']]==t['info']['name_original']
 result.append({'person_id':r['person_id'],'index':r['index'],'expected_row':r['reference'],'target_id':t['id'],'expected_target_name':t['info']['name_original']})
assert len(result)==len(reviewed)
(O/'org_link_decisions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded',len(result),'manually reviewed decisions')
