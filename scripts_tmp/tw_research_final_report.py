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
 '采集日期：2026-11-13。范围：首批10人补采政策主张、主要成就、人物关系及公开家庭信息，随后研究15位具有公开决策职责或政治影响力的人物。', '',
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
print(json.dumps({'supplement_completed':len(first['completed']),'batch2_completed':len(second['completed']),'person_errors':len(errors['persons']),'org_errors':len(errors['orgs'])}))
