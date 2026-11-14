import json,pathlib,shutil,subprocess,sys
import jsonschema
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';D=R/'tmp/tw_family_qa_before';D.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8'))
wu='https://www-ws.cy.gov.tw/Download.ashx?icon=..pdf&n=5buJ5pS%2F5bCI5YiK56ysMTU25pyfLnBkZg%3D%3D&u=LzAwMS9VcGxvYWQvMS9yZWxmaWxlLzg4NjEvMTYyNjEvZmVhNzcwODUtNzkzZC00ODI0LTk1ODQtY2E1ZThkNDA4NGMwLnBkZg%3D%3D'
rows=[('000049','苏如玉（蘇如玉）',wu,'主会话来源QA已读官方廉政156期印刷104页，姓名栏明确配偶蘇如玉，与先前知新闻全文交叉确认；仅提取配偶姓名，不保留财产内容。'),('000199','骆武昌（駱武昌）','https://news.tvbs.com.tw/local/73216','主会话来源QA已读TVBS2011年现场采访及Newtalk独立自采 https://newtalk.tw/news/view/2026-09-10/1058978 ，交叉确认配偶駱武昌；仅取姓名及婚姻关系，不采报道中的争议指控或财产。')]
audit=[]
for n,name,source,note in rows:
 p=B/'persons'/('TW-PERSON-'+n+'.json');x=read(p)
 if not(D/p.name).exists():shutil.copy2(p,D/p.name)
 oldnotes=x['collection_meta'].get('notes','')
 x['family_members']=[{'person_id':None,'name':name,'relationship':'spouse','industry_or_organization':None,'source':source,'description':note}]
 x['collection_meta']['notes']+='；补充来源QA纠正：前述关于家庭缺第二原文的中间结论已失效。'+note
 quotes=x['collection_meta']['quotes'];urls={q['url'] for q in quotes}
 for title,url in [('配偶身份核验（仅姓名关系）',source)]+([('Newtalk配偶身份独立采访','https://newtalk.tw/news/view/2026-09-10/1058978')] if n=='000199' else []):
  if url not in urls:quotes.append({'title':title,'url':url})
 jsonschema.Draft7Validator(read(R/'.agents/skills/country-org-collector/person_profile_schema.json')).validate(x)
 p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 cmd=[sys.executable,str(R/'.agents/skills/country-org-collector/scripts/validate_schema.py'),str(B),'--file',str(p),'--score'];r=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8');assert r.returncode==0,r.stdout+r.stderr
 audit.append({'person_id':x['person_id'],'action':'增量补配偶，不覆盖本轮引用ID修正','source':source,'previous_notes':oldnotes})
(R/'tmp/tw_family_qa_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Patched two family identities with source QA and rescored')
