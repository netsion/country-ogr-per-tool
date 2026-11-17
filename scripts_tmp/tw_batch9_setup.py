"""Prepare an existing-profile-only ninth batch; never register new identities."""
import pathlib,json
R=pathlib.Path(__file__).resolve().parents[1];O=R/'tmp/tw_batch9_20261117';O.mkdir(exist_ok=True)
def conv(s):return s.replace('batch8','batch9').replace('第八批','第九批').replace('eighth 15-person','ninth 15-person')
for name in ['manage','org_review','null_review','global_person_review','inspect','apply_org_links','social_ids','social_review','stats']:
 s=conv((R/'scripts_tmp'/f'tw_batch8_{name}.py').read_text(encoding='utf-8'))
 if name=='manage':s=s.replace("load(B/'_batch7_progress.json')['completed']);assert", "load(B/'_batch7_progress.json')['completed']+load(B/'_batch8_progress.json')['completed']);assert")
 p=R/'scripts_tmp'/f'tw_batch9_{name}.py';assert not p.exists();compile(s,str(p),'exec');p.write_text(s,encoding='utf-8')
s=conv((R/'tmp/tw_batch8_20261117/agent_instructions.md').read_text(encoding='utf-8'))
s+='''\n\n## 第九批现有画像内重采\n- 用户限定从现有598份人物画像内选15人，排除前115名已深采；本批不新建人物、不改person_id、不改QID及profile头像引用。原current_positions大量混杂历史职位，必须按近期原文重建现职，不把旧主席、旧立委、旧部长沿用。\n- 所有既有social_accounts必须按原platform+原URL逐条保留，原user_id、username、nickname非空值和原source_note均不得删除/替换。已有归属疑点只注明与回报主会话，不直接覆盖；在此基础上补可靠新账号和证据。保留原aliases全部（可追加），不清空原QID。所有未查清引用ID留null，既有错误引用可纠正但必须读目标真实画像。\n- 无证不补当前党务或政务职位；退休人物可据2026实际公开政治活动证明活跃，不能只搜到历史报道。不是政治人物的纯评论员不作为研究对象。旧画像姓名简繁可规范，但需保留旧主名称为别名便于索引，避免无故改变已用名称。\n'''
(O/'agent_instructions.md').write_text(s,encoding='utf-8')
(O/'new_id_registration.json').write_text(json.dumps({'created':[],'reason':'用户限定既有598人内研究；不分配新ID、不新建画像'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Prepared existing-profile-only batch9 helpers; no profile changes')
