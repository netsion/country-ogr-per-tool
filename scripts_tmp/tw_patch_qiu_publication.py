import pathlib,json,shutil,sys,subprocess
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';p=B/'persons/TW-PERSON-000529.json';x=json.loads(p.read_text(encoding='utf-8'));d=R/'tmp/tw_qiu_publication_before';d.mkdir(exist_ok=True)
if not(d/p.name).exists():shutil.copy2(p,d/p.name)
url='https://npl.ly.gov.tw/do/www/FileViewer?id=8163'
x['major_achievements'].append({'date':'2014','achievement':'与张仕贤合著《海峡西岸经济区与粤港澳合作框架综论》，由独立作家于2014年出版；此项为学术出版记录，不代表治理成效或奖项。','organization':'独立作家'})
x['collection_meta']['quotes'].append({'title':'国会图书馆书目：邱垂正、张仕贤2014合著','url':url})
x['collection_meta']['notes']+='；主会话QA成功阅读全文国会图书馆PDF印刷32页（物理第2页），确认2014合著出版；前述缺出版日期的中间结论已由此补证纠正。仅作为学术出版记录。'
p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(R/'tmp/tw_qiu_publication_audit.json').write_text(json.dumps({'person_id':x['person_id'],'source':url,'change':'增量补2014出版，不改profile/履历/ID'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
r=subprocess.run([sys.executable,str(R/'.agents/skills/country-org-collector/scripts/validate_schema.py'),str(B),'--file',str(p),'--score'],capture_output=True,text=True,encoding='utf-8');assert r.returncode==0,r.stdout+r.stderr
print('Added sourced 2014 publication to Qiu')
