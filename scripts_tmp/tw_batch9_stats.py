"""Compact read-only batch progress and verified-field counts."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
p=load(B/'_batch9_progress.json');ds=[load(B/'persons'/f'{pid}.json') for pid in p['completed']]
print(json.dumps({'status':p['status'],'completed':len(ds),'remaining':len(p['remaining']),'current':p.get('current'),**{k:sum(len(d.get(k,[])) for d in ds) for k in ['political_stances','major_achievements','person_relationships','family_members','social_accounts']},'source_links':sum(len(d['collection_meta']['quotes']) for d in ds)},ensure_ascii=False))
