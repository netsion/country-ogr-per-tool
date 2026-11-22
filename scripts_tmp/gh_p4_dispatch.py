# -*- coding: utf-8 -*-
"""P4 人物派发 prompt 生成器：python gh_p4_dispatch.py <person_id> [...]
模板固化在此文件（防上下文衰减）。GH 适配 + 中性事实表述（防内容过滤）。"""
import json, os, sys

BASE = r"D:\claude-workspace\country-ogr-per-tool\output\gh\2026-11-17"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

tpl = """你是人物信息调查 Agent。任务：为 {person_id}（{name_en}，加纳数据集，目标 completeness 85+，铁律优先于分数）生成人物画像。

【表述纪律】全程使用百科式、事实性中性表述：只记录可查证事实（日期、职务、学历、家族成员、得票、政纲名称）。禁止评价性、倾向性、渲染性措辞。分析只允许出现在 political_stances[].stance_content 与相关 description，且必须有来源依据。若某网页无法以中性事实改写，跳过换源。

第一步：读取规则与索引（不可跳过）
1. 字段规则手册：.agents/skills/country-org-collector/person_collection_rules.md（字段名白名单、语言规范、枚举值、自检清单）
2. Schema：.agents/skills/country-org-collector/person_profile_schema.json
3. ID索引：output/gh/2026-11-17/_name_index.json（组织/人物 ID 映射）
4. 人物背景：{org_files}

ID 规则：work_experience[].org_id、person_relationships[].person_id、family_members[].person_id 在 index 命中→用其 ID；未命中→写 null（JSON null，禁止""）；禁止自创 ID；不要修改 id_registry.json。

第二步：搜索（加纳官方语言=英语，英语优先；至少读取 3 个独立来源完整页面，优先 Wikipedia英文条目 > 政府名录/议会页/官网 leadership 页 > 主流新闻）
1. "<name_en> biography career Ghana"
2. "<name_en> education university"
3. "<name_en> Ghana news 2025 2026"（近期动态，供 political_stances/major_achievements）
4. 社媒扫描："<name_en>" site:facebook.com / site:x.com / site:linkedin.com / site:instagram.com / site:tiktok.com / site:youtube.com（可验证才写）
工具优先级：mcp__search-read__search（keyword）→失败换 WebSearch；读页 mcp__search-read__read_url（url）→失败换 mcp__web_reader__webReader。Cloudflare 拦截→跳过换源标记 source_blocked_cloudflare，不绕过。

第三步：组装画像写入 output/gh/2026-11-17/persons/{person_id}.json
- 顶层仅 schema 字段：person_id, wikidata_qid, name, name_zh, name_en, aliases, nationality, gender, birth_date, birth_place, contacts, current_positions, education, work_experience, person_relationships, social_accounts, family_members, political_stances, major_achievements, biography_summary, profile, collection_meta（importance_level 等一律不写）
- 语言规范（加纳官方语言=英语）：name=英文原名；name_zh=中文（通行译名优先：中国外交部/新华社/主流中文媒体，查不到自行音译并全文一致）；name_en=英文；work_experience[].organization / education[].institution / major_achievements[].organization / person_relationships[].person_name / family_members[].name = 中文(英文)且中文在前；current_positions[]、biography_summary（中文200字+）、political_stances、descriptions = 中文；dates 独立字段（禁止"1998-2002"范围写法）；degree 用枚举（MBA→master 等）；nationality="GH"；gender 用枚举
- family_members[].name 必须真实全名，查不到整条删除；political_stances 无内容不写
- profile.source_url 仅接受图片直链，查不到整字段 null
- 交叉验证：职务/学历/家族至少 2 个独立来源；禁止编造，查不到留空/null

第四步：collection_meta
phase="phase4_person_profile"；collection_date=当天日期；quotes=对象数组[{{"title":"...","url":"..."}}]≥3条；data_sources=实际来源枚举；notes=中文简述来源确认情况与存疑项

第五步：写入后验证（不可跳过）
python .agents/skills/country-org-collector/scripts/validate_schema.py output/gh/2026-11-17 --file output/gh/2026-11-17/persons/{person_id}.json
ERRORS→修复→重验直到 0 errors；然后同命令加 --score 更新 completeness_score。

工作区纪律：临时文件放 output/gh/2026-11-17/_tmp/{person_id}/（专属目录）；禁止删除 scripts_tmp/、_tmp/ 中非自己创建的文件（含 gh_p4_dispatch.py 等编排脚本）；id_registry.json 禁改。

完成后返回：person_id、最终 completeness_score、来源数量、各字段条目数、仍缺失字段。"""

targets = {t["person_id"]: t for t in json.load(open(os.path.join(BASE, "_p4_final_person_targets.json"), encoding="utf-8"))["targets"]}

for pid in sys.argv[1:]:
    t = targets[pid]
    src = t.get("source_orgs") or []
    org_files = "; ".join(
        "output/gh/2026-11-17/orgs/%s.json（%s，来源组织档案可查其 key_people 条目与组织背景）" % (s["org_id"], s.get("org_name", "?"))
        for s in src[:3])
    print("=" * 30, pid, "=" * 30)
    print(tpl.format(person_id=pid, name_en=t.get("name_en") or t.get("name"), org_files=org_files or "（无来源组织档案）"))
    print()
