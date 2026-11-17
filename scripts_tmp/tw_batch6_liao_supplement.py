"""Record a same-batch, primary-source professional-role supplement."""
import json,pathlib,subprocess,sys,shutil
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch6_20261115';pid='TW-PERSON-000564'
p=B/'persons'/f'{pid}.json';d=json.loads(p.read_text(encoding='utf-8'))
backup=O/f'late_supplement_before_{pid}.json';assert not backup.exists();shutil.copy2(p,backup)
source='https://www.hwe.org.tw/news/cG9zdDozMDU2?page=1'
assert not any(source==q['url'] for q in d['collection_meta']['quotes'])
d['work_experience'].append({'organization':'立法院厚生会（立法院厚生會）','position':'第三十四届秘书长（2026年4月24日交接组织名单所列）','start_date':None,'end_date':None,'org_id':None,'source':source})
d['collection_meta']['quotes'].append({'title':'厚生会第34届交接及秘书长名单','url':source})
d['collection_meta']['collection_date']='2026-11-16'
d['collection_meta']['notes']+=' 2026年11月16日依据厚生会原文补记4月24日组织交接名单所列第三十四届秘书长；此为当时公开任职，未将交接日推定为任命生效日，未推定任期或今日是否仍任职。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
result=subprocess.run([sys.executable,str(R/'.agents/skills/country-org-collector/scripts/validate_schema.py'),str(B),'--file',f'persons/{pid}.json','--score'],capture_output=True,text=True,encoding='utf-8');assert 'Errors: 0' in result.stdout,result.stdout
(R/'tmp/tw_batch6_enriched'/p.name).write_bytes(p.read_bytes())
print('Supplemented dated professional role without inferring appointment dates')
