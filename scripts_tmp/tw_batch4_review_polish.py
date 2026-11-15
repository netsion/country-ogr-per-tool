"""Integrate facts from official committee record reviewed by the parent."""
import pathlib,json,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';S=R/'tmp/tw_batch4_enriched'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
url='https://ppg.ly.gov.tw/ppg/SittingCommitteesInfo/download/communique1/final/pdf/115/78/LCIDC01_1157801_00012.pdf'
for pid in ['TW-PERSON-000150','TW-PERSON-000159']:
 p=B/'persons'/f'{pid}.json';d=load(p);role='立法院第11届第6会期财政委员会委员'
 if role not in d['current_positions']:d['current_positions'].append(role)
 if not any(q['url']==url for q in d['collection_meta']['quotes']):d['collection_meta']['quotes'].append({'title':'立法院2026-10-08财政委召委选任会议：本会期委员选举人名册','url':url})
 note=' 主会话另核2026-10-08立院公报，第6会期财政委选举人名册有本人，补记本会期委员身份；不据名册推定实际出席，也不记为获选召委。'
 if note.strip() not in d['collection_meta']['notes']:d['collection_meta']['notes']+=note
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 result=subprocess.run([sys.executable,str(R/'.agents/skills/country-org-collector/scripts/validate_schema.py'),str(B),'--file',f'persons/{pid}.json','--score'],capture_output=True,text=True,encoding='utf-8');assert 'Errors: 0' in result.stdout,result.stdout
 (S/p.name).write_bytes(p.read_bytes())
p=B/'persons/TW-PERSON-000014.json';d=load(p)
if not any('2026年新名单' in w['position'] for w in d['work_experience']):d['work_experience'].append({'organization':'总统府（總統府）','org_id':'TW-GOV-023','position':'资政（2026年新名单，个人起聘日未核）','start_date':None,'end_date':None})
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');(S/p.name).write_bytes(p.read_bytes())
print('Added two current committee memberships from original record; distinguished Su appointment periods')
