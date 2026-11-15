"""Scoped evidence-backed additions from the ministry official resume already read."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';S=R/'tmp/tw_batch3_enriched'
p=B/'persons/TW-PERSON-000535.json';d=json.loads(p.read_text(encoding='utf-8'))
add=[('财政部国有财产局（財政部國有財產局）','主任秘书（历史任职）'),('财政部国有财产局（財政部國有財產局）','副局长（历史任职）'),('财政部（財政部）','参事（历史任职）')]
existing={r['position'] for r in d['work_experience']}
prefix=[{'organization':org,'org_id':None,'position':position,'start_date':None,'end_date':None} for org,position in add if position not in existing]
d['work_experience']=prefix+d['work_experience']
note=' 财政部官方履历另明确列国有财产局主任秘书、副局长及财政部参事经历，已补入历史任职；原文未给任职日期，不补造年份。'
if note.strip() not in d['collection_meta']['notes']:d['collection_meta']['notes']+=note
for target in [p,S/p.name]:target.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
print('Added',len(prefix),'officially listed historical roles; unknown dates retained')
