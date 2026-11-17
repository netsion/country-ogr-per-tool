"""Materialize the explicitly reviewed 27 null organization references."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/tw_batch7_20261116'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
reviewed={
569:{0:'TW-GOV-020',1:'TW-PARTY-012',3:'TW-GOV-020'},
570:{0:'TW-GOV-020',1:'TW-GOV-020',5:'TW-PARTY-012'},
571:{6:'TW-GOV-020'},572:{1:'TW-GOV-020',2:'TW-GOV-020',5:'TW-GOV-019'},
573:{0:'TW-ACAD-019',5:'TW-GOV-019',7:'TW-GOV-019',8:'TW-GOV-019'},
574:{8:'TW-ACAD-015'},575:{4:'TW-PARTY-012'},
576:{0:'TW-GOV-020',1:'TW-GOV-020',4:'TW-PARTY-012'},
577:{0:'TW-GOV-020',5:'TW-PARTY-012'},578:{4:'TW-GOV-020',8:'TW-PARTY-012'},
579:{0:'TW-GOV-020',3:'TW-ACAD-016',7:'TW-NGO-004'},581:{0:'TW-GOV-020'}}
candidates={(x['person_id'],x['index']):x for x in load(O/'null_org_candidates.json')};decisions=[]
for num,rows in reviewed.items():
 pid=f'TW-PERSON-{num:06d}'
 for i,tid in rows.items():
  c=candidates[pid,i];target=load(B/'orgs'/f'{tid}.json')
  assert any(t['id']==tid for t in c['candidates'])
  decisions.append({'person_id':pid,'index':i,'expected_row':c['reference'],'target_id':tid,'expected_target_name':target['basic_info']['name_original'],'review_note':'逐条比对引用文字、实际画像的主名称、官网、TWN总部与机构性质；不跨层级推断。'})
assert len(decisions)==27
(O/'org_link_decisions.json').write_text(json.dumps(decisions,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared 27 explicitly reviewed organization references')
