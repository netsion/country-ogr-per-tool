"""Produce reproducible first-batch coverage and actual JSON Schema findings."""
import json
import pathlib
import sys
from collections import Counter
import jsonschema
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.agents/skills/country-org-collector/scripts'))
from atomic_write import load_json, save_json
BASE = ROOT / 'output/tw/2026-07-27'
SC = ROOT / '.agents/skills/country-org-collector'
progress = load_json(str(BASE / '_phase_progress.json'))
errors = {}
for folder, schema_name in [('orgs', 'org_profile_schema.json'), ('persons', 'person_profile_schema.json')]:
    validator = jsonschema.Draft7Validator(load_json(str(SC / schema_name)))
    errors[folder] = [{'file': str(file.relative_to(ROOT)), 'path': list(err.path), 'message': err.message}
       for file in sorted((BASE / folder).glob('TW-*.json'))
       for err in validator.iter_errors(load_json(str(file)))]
save_json(str(ROOT / 'tmp/tw_jsonschema_validation.json'), errors)
people = [load_json(str(BASE / 'persons' / (pid + '.json'))) for pid in progress['completed']]
headers = ['# 台湾地区首批人物采集记录（2026-11-13）', '',
    '本轮先修整底表，再逐人采集首批10人。人物总数仍为527；有效组织隔离4条后为98条，另为人物任职关联补建4个有官方来源的组织骨架，目前为102条。', '',
    '完整原始备份与隔离审计：`tmp/tw_before_repair_20261113_021320/`。结构修整详情见 `docs/tw_repair_report.md`。', '',
    f'首批完成 {len(people)}/10。完成表示本轮公开资料研究与写入结束，不表示达到85分，也不表示全部字段已核实。', '',
    '| 人物 | ID | 完整度 | 教育 | 履历 | 简介字数 | 引用页数 |',
    '|---|---|---:|---:|---:|---:|---:|']
for p in people:
    m = p['collection_meta']
    headers.append(f"| {p['name_zh']} | {p['person_id']} | {m.get('completeness_score')} | {len(p.get('education', []))} | {len(p.get('work_experience', []))} | {len(p.get('biography_summary', ''))} | {len(m.get('quotes', []))} |")
headers += ['', '实际 JSON Schema 校验：人物错误 ' + str(len(errors['persons'])) + ' 项；组织错误 ' + str(len(errors['orgs'])) + ' 项。完整逐项清单为 `tmp/tw_jsonschema_validation.json`。', '',
    '限制与后续：', '',
    '- 仍有组织细分类缺证据，保留缺失并如实报错，不为通过验证编造分类。',
    '- 首批教育、履历、现职和简介按本轮引用来源丰富；部分出生日期仍只有单一来源，已在人物 notes 标注。',
    '- 社交平台检索遇到访问限制或身份凭据不足，旧头像、社交账号及平台标识保留但不得视为本轮独立核验；魏哲家无可靠本人账号时留空。',
    '- 其他517人仍为待研究候选。历史来源链接转入 quotes 仅为格式迁移，并非本轮读取或确认；notes 保留原阶段及未研究说明。',
    '- 组织旧领导记录仍有历史任职和错绑风险，已核实首批对应关系回填，不能将其余列表视作当前领导名录。',
    '- 已核实并纠正 TW-CORP-014：欣兴电子应为 Unimicron Technology Corp.（Q15908529），原 King Yuan Electronics 属于京元电子；原错误内容保留在备份。',
    '- 新总统府、外交部、国防部、台北市政府均为有来源的骨架，未宣称完成组织深采。', '',
    '采集证据：', '']
for p in people:
    headers.append('**' + p['name_zh'] + '**')
    for q in p['collection_meta']['quotes']:
        headers.append('- [' + q['title'].replace('[', '').replace(']', '') + '](' + q['url'] + ')')
    headers.append('')
(ROOT / 'docs/tw_batch1_report.md').write_text('\n'.join(headers) + '\n', encoding='utf-8')
print(json.dumps({'completed': len(people), 'person_schema_errors': len(errors['persons']), 'org_schema_errors': len(errors['orgs']), 'average_batch_score': round(sum(p['collection_meta'].get('completeness_score', 0) for p in people) / len(people), 1)}, ensure_ascii=False))
