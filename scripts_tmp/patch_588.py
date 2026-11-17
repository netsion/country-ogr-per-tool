import json,pathlib
p=pathlib.Path('tmp/tw_batch8_enriched/TW-PERSON-000588.json');d=json.loads(p.read_text(encoding='utf-8'))
d['family_members'] += [dict(person_id=None,name='張榮味',relationship='father',industry_or_organization='前云林县长'),dict(person_id='TW-PERSON-000136',name='張麗善',relationship='aunt',industry_or_organization='云林县政府')]
d['political_stances'][2]=dict(date='2026-11-01',topic='宗教文化与高龄友善空间',stance_content='在宗教团体后援会成立活动承诺延续宫庙产权保障与合法化辅导，推动高龄友善庙埕、无障碍设施和长者休憩空间，结合民俗艺阵及周边商圈；属于竞选政策承诺。',source='https://www.cna.com.tw/news/aipl/202611010143.aspx')
d['collection_meta']['quotes'] += [dict(title=t,url=u) for t,u in [('中央社：张荣味儿任参议及实名家属','https://www.cna.com.tw/news/aipl/202404270089.aspx'),('中央社：张嘉郡宗教团体后援会成立','https://www.cna.com.tw/news/aipl/202611010143.aspx'),('联合报：张嘉郡11月15日两场造势','https://udn.com/vote2026/story/124652/9880390')]]
d['collection_meta']['notes'] += ' 补核：2026-11-15联合报可读全文确认当天台西及斗六竞选活动，最新公开活动截止更新至该日。中央社2026-11-01正文直接确认张荣味为父亲；2024-04-27中央社实名家属脉络确认父亲与姑姑，姑姑关系为该篇可靠新闻单源并由维基交叉；张丽善实际画像000136已读核为云林县长。上述补核取代先前未收亲属说明。未把亲属或助选同台推为政治盟友。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
print('jsonschema PASS')
