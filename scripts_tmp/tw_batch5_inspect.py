"""Compact, read-only review of one staged profile."""
import json,pathlib,sys
R=pathlib.Path(__file__).resolve().parents[1]
p=R/'tmp/tw_batch5_enriched'/f'{sys.argv[1]}.json'
x=json.loads(p.read_text(encoding='utf-8'))
keys=['person_id','name','name_en','wikidata_qid','current_positions','political_stances','major_achievements','person_relationships','family_members','social_accounts','collection_meta']
print(json.dumps({**{k:x.get(k) for k in keys},'education_count':len(x.get('education',[])),'work_count':len(x.get('work_experience',[])),'bio_length':len(x.get('biography_summary',''))},ensure_ascii=False,indent=2))
