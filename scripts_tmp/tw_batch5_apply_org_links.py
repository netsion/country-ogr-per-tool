"""Apply a reviewed explicit row list; never infer or globally resolve links."""
import pathlib,json,subprocess,sys
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch5_20261115'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
decisions=load(O/'org_link_decisions.json');files={};changes=[]
assert len({(d['person_id'],d['index']) for d in decisions})==len(decisions)
for c in decisions:
 assert c['person_id'] in load(B/'_batch5_progress.json')['completed']
 p=B/'persons'/f"{c['person_id']}.json";d=files.setdefault(c['person_id'],load(p));row=d['work_experience'][c['index']]
 assert row==c['expected_row'] and row.get('org_id') is None
 target=load(B/'orgs'/f"{c['target_id']}.json")
 assert target['org_id']==c['target_id'] and target['basic_info']['hq_country_iso3']=='TWN'
 assert target['basic_info']['name_original']==c['expected_target_name']
 row['org_id']=c['target_id'];changes.append(c)
for pid,d in files.items():
 p=B/'persons'/f'{pid}.json'
 d['collection_meta']['notes']+=' 主会话已逐条核对并补齐部分既有组织画像链接；其余未知引用保持空值。'
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 result=subprocess.run([sys.executable,str(R/'.agents/skills/country-org-collector/scripts/validate_schema.py'),str(B),'--file',f'persons/{pid}.json','--score'],capture_output=True,text=True,encoding='utf-8')
 errs=[s.strip() for s in result.stdout.splitlines() if s.strip().startswith('ERR:')]
 assert not errs or (not d['name_en'] and errs==['ERR: missing required field: name_en']),result.stdout
 (R/'tmp/tw_batch5_enriched'/p.name).write_bytes(p.read_bytes())
log=O/'verified_org_links.json';assert not log.exists(),'Avoid overwriting earlier execution log'
log.write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'Applied {len(changes)} reviewed organization links in {len(files)} profiles')
