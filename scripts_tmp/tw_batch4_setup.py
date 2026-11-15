"""Prepare isolated fourth-batch tooling from the reviewed third-batch workflow."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'tmp/tw_batch4_20261115';O.mkdir(exist_ok=True)
def convert(s):return s.replace('batch3','batch4').replace('20261114','20261115').replace('2026-11-14','2026-11-15').replace('第三批','第四批').replace('third 15-person','fourth 15-person')
s=convert((R/'scripts_tmp/tw_batch3_manage.py').read_text(encoding='utf-8'))
s=s.replace("load(B/'_batch2_progress.json')['completed']);assert", "load(B/'_batch2_progress.json')['completed']+load(B/'_batch3_progress.json')['completed']);assert")
s='\n'.join(line for line in s.splitlines() if '本轮复用11份原有画像' not in line and '本批合计政策主张44条' not in line)+'\n'
anchor=" if conflicts:lines+="
extra=""" totals={k:sum(t[k] for t in summaries) for k in ['political_stances','major_achievements','person_relationships','family_members']}
 registration=load(O/'new_id_registration.json') if (O/'new_id_registration.json').exists() else {'created':[]}
 created=registration['created']
 lines+=['',f'本批合计政策主张{totals["political_stances"]}条、成就{totals["major_achievements"]}条、人物关系{totals["person_relationships"]}条、公开家庭关系{totals["family_members"]}条。',f'复用{15-len(created)}份已有画像，新注册{len(created)}份人物身份；新增者头像保持null。新ID清单：'+', '.join(e['person_id']+' '+e['name'] for e in created),'来源列是链接数量，不等同独立来源数量；同源转载不重复算独立核实。未知关系ID保持null，未按姓名自动补链。','本批严格检查中文姓名提示详见strict_validation.json；不修改正确中文姓名。完整度是字段覆盖指标，尚有缺项及单源边界，不等同全部事实已核实。']
"""
s=s.replace(anchor,extra+anchor)
(R/'scripts_tmp/tw_batch4_manage.py').write_text(s,encoding='utf-8')
s=convert((R/'scripts_tmp/tw_batch3_register.py').read_text(encoding='utf-8'))
(R/'scripts_tmp/tw_batch4_register.py').write_text(s,encoding='utf-8')
s=convert((R/'tmp/tw_batch3_20261114/agent_instructions.md').read_text(encoding='utf-8'))
s+='\n尽量完整覆盖官方明确列出的主要职业经历，不只填最低2段；日期未载可null并注明历史任职。政策、家庭及关系有同名风险时必须用任职、配偶上下文及来源消歧，禁止仅凭名字链接。\n'
(O/'agent_instructions.md').write_text(s,encoding='utf-8')
s=convert((R/'scripts_tmp/tw_batch3_null_review.py').read_text(encoding='utf-8'))
(R/'scripts_tmp/tw_batch4_null_review.py').write_text(s,encoding='utf-8')
compile((R/'scripts_tmp/tw_batch4_manage.py').read_text(encoding='utf-8'),'batch4_manage','exec')
print('Fourth-batch staging, guarded installer and instructions ready')
