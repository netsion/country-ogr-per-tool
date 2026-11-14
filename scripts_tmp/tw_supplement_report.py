"""Track substantive research coverage rather than just file completion."""
import json
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
BASE=ROOT/'output/tw/2026-07-27'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
progress=read(BASE/'_supplement_progress.json')
fields=['political_stances','major_achievements','person_relationships','family_members']
lines=['# 台湾地区首批四项专项补采（2026-11-13）','',
 '补采原因为首轮政策、成果、关系和家庭采集不足。每人针对这些字段重新检索，未确认的信息不以留空代替检索。', '',
 '| 人物 | 政策主张 前→后 | 主要成就 前→后 | 人物关系 前→后 | 家庭成员 前→后 | 当前完整度 |',
 '|---|---:|---:|---:|---:|---:|']
for pid in progress['completed']:
 old=read(ROOT/'tmp/tw_supplement_before'/(pid+'.json'));new=read(BASE/'persons'/(pid+'.json'))
 counts=[f'{len(old.get(k,[]))}→{len(new.get(k,[]))}' for k in fields]
 lines.append('| '+new['name_zh']+' | '+' | '.join(counts)+' | '+str(new['collection_meta'].get('completeness_score'))+' |')
lines += ['',f"完成 {len(progress['completed'])}/10；余下 {len(progress['remaining'])} 人。",'',
 '关系仅记录证据支持的具体关系，政策是本人公开表述，成就区分已实现成果与承诺，团队成果明确归因。家庭信息仅采公开且可核验的最小必要身份，不含私人联系方式、住址或非公众家庭成员的敏感细节。', '',
 '每条政策附原文source；关系及家庭按当前Schema允许的source保存来源，人物关系另附corroborating_sources。原文出处统一纳入quotes。保留原履历、头像和已有社交平台标识；未知关系ID维持null，不自创人物。', '',
 '人物详情及无法确认原因见每份人物档案的collection_meta.notes。原始本轮前档案完整保存在tmp/tw_supplement_before。', '']
(ROOT/'docs/tw_batch1_supplement_report.md').write_text('\n'.join(lines),encoding='utf-8')
print('Supplement report updated:',len(progress['completed']),'/10')
