"""Materialize the manually reviewed 26 organization-reference rows."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch8_20261117'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
reviewed={584:{6:'TW-GOV-019',7:'TW-PARTY-013',11:'TW-GOV-026'},585:{2:'TW-GOV-020',6:'TW-GOV-020'},586:{0:'TW-ACAD-016',1:'TW-ACAD-016',2:'TW-ACAD-016',6:'TW-ACAD-016',10:'TW-ACAD-018',15:'TW-GOV-019'},588:{0:'TW-GOV-020',1:'TW-GOV-020',5:'TW-PARTY-013'},592:{0:'TW-GOV-020',6:'TW-PARTY-012'},593:{1:'TW-GOV-020'},595:{6:'TW-GOV-020'},596:{0:'TW-ACAD-019'},597:{8:'TW-PARTY-012',9:'TW-PARTY-012',10:'TW-GOV-020'},598:{0:'TW-GOV-020',1:'TW-GOV-020',2:'TW-GOV-020',6:'TW-PARTY-012'}}
candidates={(x['person_id'],x['index']):x for x in load(O/'null_org_candidates.json')};decisions=[]
for num,rows in reviewed.items():
 pid=f'TW-PERSON-{num:06d}'
 for i,tid in rows.items():
  c=candidates[pid,i];t=load(B/'orgs'/f'{tid}.json')
  assert any(x['id']==tid for x in c['candidates']) and t['basic_info']['hq_country_iso3']=='TWN'
  decisions.append({'person_id':pid,'index':i,'expected_row':c['reference'],'target_id':tid,'expected_target_name':t['basic_info']['name_original'],'review_note':'主会话已逐条读取目标画像，核对主名称、机构性质、官网及台湾总部；不按相近名称推断分支或前身。'})
assert len(decisions)==26
(O/'org_link_decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared 26 explicitly reviewed organization links')
