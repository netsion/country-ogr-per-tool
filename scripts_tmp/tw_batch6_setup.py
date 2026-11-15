"""Prepare isolated sixth-batch tools, preserving previous batch artifacts."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'tmp/tw_batch6_20261115';O.mkdir(exist_ok=True)
def convert(s):return s.replace('batch5','batch6').replace('第五批','第六批').replace('fifth 15-person','sixth 15-person')
s=convert((R/'scripts_tmp/tw_batch5_manage.py').read_text(encoding='utf-8'))
s=s.replace("load(B/'_batch4_progress.json')['completed']);assert", "load(B/'_batch4_progress.json')['completed']+load(B/'_batch5_progress.json')['completed']);assert")
s='\n'.join(line for line in s.splitlines() if not line.strip().startswith("lines+=['','评论员内容"))+'\n'
target=R/'scripts_tmp/tw_batch6_manage.py';assert not target.exists();target.write_text(s,encoding='utf-8');compile(s,str(target),'exec')
for base in ['register','null_review','global_person_review','org_review','inspect']:
 p=R/'scripts_tmp'/f'tw_batch6_{base}.py';assert not p.exists();p.write_text(convert((R/'scripts_tmp'/f'tw_batch5_{base}.py').read_text(encoding='utf-8')),encoding='utf-8')
s=(R/'tmp/tw_batch4_20261115/agent_instructions.md').read_text(encoding='utf-8').replace('batch4','batch6').replace('第四批','第六批')
s+='''

## 第六批：仅政治人物，不收评论员

- 采集日2026-11-15。须核2026实际公务/公开政治活动，尽量下半年原文。官方议事视频目录仅能证质询参与与日期，观点须完整发言、本人文章或明确直接引语。
- 政策力争3个不同公共议题，成果力争2个实际已通过/实施事项。提案、规划、争取、核定、动工、完工、执行效果须分清。集体立法和行政成果不得归为个人独力完成。
- 人物关系可记有原文证明的具体共事、共同提案、公务会见，注明时间与范围；不从同党同台推私人盟友。家庭仅公开实名与必要关系，不采地址、财产、健康或无名子女。
- 当前党务、召委、竞选身份必须当期核。2026年底选举尚未结束，不预写当选。网页导航会期不等于正文会期，日期冲突检查正文及公报，不能从摘要推断。
- 主姓名和现职等重要信息尽量两个独立原文。未知英文名可空并在notes明写英文未核，不能自行音译为正式名称；真实Schema允许空字符串，旧validator的该项限制须如实报告。
- 至少尝试核实公开家庭和可限定关系，不因不是私人/长期关系而一律留空。无据保留空值；不为分数编造。主要官方教育、职业经历尽量覆盖完整。
- 每60秒报告进度；只写本人物暂存JSON，不派代理，不碰正式registry/index/progress，非空引用须读实际画像确认身份。
'''
(O/'agent_instructions.md').write_text(s,encoding='utf-8')
print('Prepared sixth-batch isolated helpers and political-figure evidence rules')
