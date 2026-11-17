"""Clarify announcement stage and the date of the public retrospective."""
import pathlib,json
p=pathlib.Path(__file__).resolve().parents[1]/'tmp/tw_batch9_enriched/TW-PERSON-000515.json'
d=json.loads(p.read_text(encoding='utf-8'));r=d['major_achievements'][1]
assert r['date']=='2021-08-21' and '2021年3月5日' in r['achievement']
r['achievement']='据PrideWatch保存的本人2021年8月21日公开回顾，经持续讨论及预算监督，国防部已于2021年3月5日公告将多元性别认识与尊重纳入全军性平课程，并规划占年度课时六分之一以上。记录限于其自述的课程规范公告及监督贡献，不代表已独立核实全军授课落实或成效；非个人独力立法，单源自述。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
