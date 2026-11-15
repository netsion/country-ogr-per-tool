"""Isolate fifth-batch tools and apply commentator-specific evidence rules."""
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'tmp/tw_batch5_20261115';O.mkdir(exist_ok=True)
def convert(s):return s.replace('batch4','batch5').replace('第四批','第五批').replace('fourth 15-person','fifth 15-person')
s=convert((R/'scripts_tmp/tw_batch4_manage.py').read_text(encoding='utf-8'))
s=s.replace("load(B/'_batch3_progress.json')['completed']);assert", "load(B/'_batch3_progress.json')['completed']+load(B/'_batch4_progress.json')['completed']);assert")
s='\n'.join(line for line in s.splitlines() if "## 重点复核与边界" not in line)+'\n'
s=s.replace(" if conflicts:lines+=", " lines+=['','评论员内容只记录明确署名或可核发言，不将评论意见、节目标题或主持人转述当作客观事实；无依据的阵营、派系和政治影响力标签不填写。近期活跃证据保存在selection.json及各画像quotes/notes，活跃记录不代表所有政策字段均发生于最近。出版/节目等职业成果与政府施政成果分开，未把未经核实的收视粉丝数当影响力。']\n if conflicts:lines+=")
(R/'scripts_tmp/tw_batch5_manage.py').write_text(s,encoding='utf-8');compile(s,'batch5_manage','exec')
for old,new in [('tw_batch4_register.py','tw_batch5_register.py'),('tw_batch4_null_review.py','tw_batch5_null_review.py'),('tw_batch4_global_person_review.py','tw_batch5_global_person_review.py'),('tw_batch4_org_review.py','tw_batch5_org_review.py')]:
 (R/'scripts_tmp'/new).write_text(convert((R/'scripts_tmp'/old).read_text(encoding='utf-8')),encoding='utf-8')
s=convert((R/'tmp/tw_batch4_20261115/agent_instructions.md').read_text(encoding='utf-8'))
s+='''

## 本批活跃政治人物与评论员专项

- 日期仍为2026-11-15。近期活跃应有2026年实际公开活动、节目、署名文章或公务记录；无近期原文不要靠过去知名度假定活跃。节目视频说明可证参与和日期，不能仅据标题推断本人观点；观点须本人署名原文、可核访谈/逐字稿或明确直接引述。
- political_stances记录本人对具体公共政策的明确意见，写明时间、场合和评论属性。不要把节目里的猜测、记者转述或主持人题目写成客观事实。不无据标蓝绿、亲某阵营、派系或私人盟友；不收与任务无关的个人指控或八卦。
- 评论员major_achievements可记有据的出版、获奖、正式节目/媒体创办及实际职业节点，不硬凑政府政绩，不将自述粉丝数、收视率或政治影响当独立量化成效。至少尝试补够2项，找不到则透明留缺。
- 节目明确固定搭档、具体合著/共同制作可作限定的职业关系；一次同台不能推政治联盟。家庭只可靠公开全名与最小关系，不扩私人地址财产健康或无名子女。任职媒体与本人账号区分，机关/节目社群不能当本人账号。
- 请优先提取每次实际阅读来源中的多项信息，覆盖已知主要经历；不要仅为满足最低条数截断易核的官方履历。QID、同名身份、原URL/user_id组合必须保留和消歧。历史职称不当现职。最近活跃原文须在notes注明日期和场合。
'''
(O/'agent_instructions.md').write_text(s,encoding='utf-8')
print('Prepared fifth batch with commentator attribution, activity and identity guards')
