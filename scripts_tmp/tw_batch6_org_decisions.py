"""Record only explicit, manually inspected reference-to-identity decisions."""
import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];O=R/'tmp/tw_batch6_20261115'
rows=json.loads((O/'null_org_candidates.json').read_text(encoding='utf-8'))
allowed={'TW-GOV-020':'立法院','TW-PARTY-012':'民主進步黨','TW-PARTY-013':'中國國民黨','TW-ACAD-019':'國立臺灣大學'}
reviewed={('TW-PERSON-000556',3),('TW-PERSON-000556',4),('TW-PERSON-000556',5),('TW-PERSON-000556',6),('TW-PERSON-000557',2),('TW-PERSON-000557',4),('TW-PERSON-000557',5),('TW-PERSON-000557',7),('TW-PERSON-000558',0),('TW-PERSON-000559',0),('TW-PERSON-000559',6),('TW-PERSON-000560',7),('TW-PERSON-000560',8),('TW-PERSON-000560',9),('TW-PERSON-000561',0),('TW-PERSON-000562',4),('TW-PERSON-000562',6),('TW-PERSON-000563',0),('TW-PERSON-000564',0),('TW-PERSON-000564',1),('TW-PERSON-000565',0),('TW-PERSON-000565',1),('TW-PERSON-000565',3),('TW-PERSON-000565',4),('TW-PERSON-000565',5),('TW-PERSON-000565',6),('TW-PERSON-000566',0),('TW-PERSON-000566',5)}
reviewed.update({('TW-PERSON-000567',0),('TW-PERSON-000568',2)})
result=[]
for r in rows:
 if (r['person_id'],r['index']) not in reviewed:continue
 assert len(r['candidates'])==1
 t=r['candidates'][0];assert allowed[t['id']]==t['info']['name_original']
 result.append({'person_id':r['person_id'],'index':r['index'],'expected_row':r['reference'],'target_id':t['id'],'expected_target_name':t['info']['name_original']})
assert len(result)==len(reviewed)
(O/'org_link_decisions.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Recorded',len(result),'manually inspected organization decisions')
