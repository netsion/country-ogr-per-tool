"""Report both requested research batches with data quality limits."""
import pathlib,sys,json
import jsonschema
ROOT=pathlib.Path(__file__).resolve().parents[1];BASE=ROOT/'output/tw/2026-07-27'
sys.path.insert(0,str(ROOT/'.agents/skills/country-org-collector/scripts'))
from atomic_write import load_json,save_json
first=load_json(str(BASE/'_supplement_progress.json'))
second=load_json(str(BASE/'_batch2_progress.json'))
fields=['political_stances','major_achievements','person_relationships','family_members']
lines=['# 台湾地区人物专项采集与第二批研究','',
 '采集日期：2026-11-13至2026-11-14。范围：首批10人补采政策主张、主要成就、人物关系及公开家庭信息，随后研究15位具有公开决策职责或政治影响力的人物。', '',
 '原文来源逐条存于人物档案的source及collection_meta.quotes；关系尽可能交叉验证，家庭仅记录有可靠公开证据的最小身份信息。成就区分已实施成果、团队归因、官方自陈与计划，不把承诺当已实现结果。', '']
for label,progress in [('首批专项补采',first),('第二批15人',second)]:
 lines += ['## '+label,'',f"完成 {len(progress['completed'])} 人，待完成 {len(progress['remaining'])} 人。",'',
 '| 人物 | ID | 政策 | 成就 | 人物关系 | 家庭 | 完整度 |','|---|---|---:|---:|---:|---:|---:|']
 for pid in progress['completed']:
  x=load_json(str(BASE/'persons'/(pid+'.json')))
  lines.append('| '+x.get('name_zh',x['name'])+' | '+pid+' | '+' | '.join(str(len(x.get(k,[]))) for k in fields)+' | '+str(x['collection_meta'].get('completeness_score'))+' |')
 lines.append('')
errors={}
for folder,sn in [('persons','person_profile_schema.json'),('orgs','org_profile_schema.json')]:
 v=jsonschema.Draft7Validator(load_json(str(ROOT/'.agents/skills/country-org-collector'/sn)))
 errors[folder]=[{'file':f.name,'path':list(e.path),'message':e.message} for f in sorted((BASE/folder).glob('TW-*.json')) for e in v.iter_errors(load_json(str(f)))]
save_json(str(ROOT/'tmp/tw_jsonschema_validation.json'),errors)
lines += ['## 验证与未完成内容','',
 f"台湾地区当前数据集人物档案 {len(list((BASE/'persons').glob('TW-*.json')))} 份，组织档案 {len(list((BASE/'orgs').glob('TW-*.json')))} 份。该数据集真正 JSON Schema 人物错误 {len(errors['persons'])} 项，组织错误 {len(errors['orgs'])} 项。",'',
 '其他历史人物尚未本轮事实核验。组织历史细分类、领导记录和旧来源仍有待补查；结构规范化与保留历史链接不代表已阅读核实。完整度是字段覆盖评分，不能代替来源可靠性评价。', '',
 '未确认的家庭关系不猜测；未找到可靠本人社交账号的保留空值。原账号及平台ID如仅保留未复核，均应在人物notes中说明。未知关系ID为null，不把相关人无证据注册为本轮完整人物。', '',
 '备份：tmp/tw_before_repair_20261113_021320、tmp/tw_supplement_before、tmp/tw_batch2_before。', '',
 '相关报告：docs/tw_repair_report.md、docs/tw_batch1_supplement_report.md、docs/tw_batch2_selection.md。','']
(ROOT/'docs/tw_research_report.md').write_text('\n'.join(lines),encoding='utf-8')
if not second['remaining']:
 resumed=['000184','000148','000533','000041','000141','000039','000163']
 extra=['','## 2026-11-14续采收尾','','本轮从8/15恢复，依次完成管碧玲、卢秀燕、侯友宜、陈其迈、傅崐萁、柯建铭、罗智强，第二批15/15已执行完毕。完成表示本轮公开资料研究与写入结束，不表示所有事实均已多源确认，也不表示达到85分。','','本轮7人合计政策主张21条、主要成就13条、人物关系5条、公开配偶关系7条。傅崐萁与罗智强未找到足够明确的非家庭人物关系，保持空数组；柯建铭具体立法成果缺独立归因，未凑足第二项成就。','','关键纠正包括管碧玲现职、卢秀燕/陈其迈历史头衔分离、柯建铭卸任党团总召，以及罗智强旧议员/府职分离。罗智强无发表日期的政见未推定年份，改用有明确报道日期的本人发言。','','配偶信息仅记录公开姓名与关系：卢秀燕以自由时报及台视原文补证；柯建铭以监察院公开申报补证，未采集财产、地址或其他私人数据。其他单源日期、旧履历及当前职务核验的截止时间逐档注明。','','质量检查：7份真正JSON Schema与自带严格检查均0错误；严格检查有7条将TW中文姓名当非本国语言的提示，保留正确中文姓名。逐条人工核对20处非空ID的真实画像名称，0缺失目标。与续采前635份人物/组织画像快照对账：只有本轮7份人物画像改变，所有画像ID与头像字段一致；组织画像未改。','','已同步两批25位已研究人物的索引信息，保留原有历史名称。Wellington Koo同时涉及顾维钧与顾立雄，未覆盖原映射或据此自动改链；中文全名可分别定位。未执行全库resolve_ids自动补链。组织73项Schema错误为此前已存在的细分类缺失，不属于本轮人物写入错误。','','复核明细：tmp/tw_resume_20261114/validation.json；严格检查：tmp/tw_resume_20261114/strict_validation.json。']
 with (ROOT/'docs/tw_research_report.md').open('a',encoding='utf-8') as f:f.write('\n'.join(extra)+'\n')
print(json.dumps({'supplement_completed':len(first['completed']),'batch2_completed':len(second['completed']),'person_errors':len(errors['persons']),'org_errors':len(errors['orgs'])}))
