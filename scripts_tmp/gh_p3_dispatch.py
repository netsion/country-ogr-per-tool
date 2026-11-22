# -*- coding: utf-8 -*-
"""P3 派发 prompt 生成器（重建版）：python gh_p3_dispatch.py <org_id> [<org_id> ...]
从 _p3_final_targets.json 读取参数，打印完整内联 prompt（模板固化在此文件，防上下文衰减）。"""
import json, os, sys

BASE = r"D:\claude-workspace\country-ogr-per-tool\output\gh\2026-11-17"
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

tpl = """你是组织信息丰富 Agent。任务：为 {org_id}（{name_en}，org_type={org_type}）生成高质量画像（加纳数据集，目标 completeness 85+，但铁律优先于分数）。

先读两个文件（不可跳过）：
1. 骨架文件：output/gh/2026-11-17/orgs/{org_id}.json（了解现有字段与 completeness_score）
2. ID索引：output/gh/2026-11-17/_name_index.json（实体ID映射，支持中/英分解匹配）

ID规则：引用的组织/人物在 index 中命中→用其 org_id/person_id；未命中→写 null（JSON null，禁止""）；禁止自创ID格式；不要修改 id_registry.json（主会话统一批量注册，避免并发写冲突）。

按来源执行搜索（每步从结果中提取所有相关字段，不要只盯主目标）：
Step1 读 Wikipedia（英文条目为主，可查中文条目获取译名）：提取 key_people, departments, core_business, related_entities
Step2 读官网 {website}（首页 + About/Contact 页；无官网则搜）：social_accounts(页脚图标链接), digital_assets, departments 补充
Step3 搜新闻："{name_en} Ghana news 2025 2026" → recent_events(≥3条), related_entities
Step4 补缺：检查仍为空的字段，做 0-2 次补充搜索

工具优先级：搜索 mcp__search-read__search（keyword参数）/备选 WebSearch；读页 mcp__search-read__read_url（url参数）/备选 mcp__web_reader__webReader。Cloudflare拦截→跳过换源标记 source_blocked_cloudflare，不绕过。

将丰富后的完整画像写回原路径 output/gh/2026-11-17/orgs/{org_id}.json，规则：
- 字段名严格禁止自创：key_people[]: person_id|name|title|title_description|description；departments[]: name|dept_id|head|description|parent_dept_id；social_accounts[]: platform|account_name|url|source；recent_events[]: date|title|description|impact|source；related_entities[]: org_id|org_name|org_type|org_description|relationship_type；digital_assets[]: name|url|description|source；顶层仅保留 schema 字段（org_id, wikidata_qid, basic_info, social_accounts, digital_assets, key_people, departments, recent_events, related_entities, core_business, industries, apec_stance, profile, collection_meta）
- 语言规范（加纳官方语言=英语）：basic_info.name_original=英文原名, name_en=英文, name_zh=中文；key_people[].name=中文(英文)中文在前；title=中文或中文(英文)；departments[].head=中文(英文)；所有描述类字段=中文；core_business=中文200字+；apec_stance=中文；industries 与 social_accounts[].platform=英文枚举值（platform 全小写）；URL 保留原样
- 人名中文译名：优先可查证通行译名（中国外交部/新华社/主流中文媒体），查不到自行音译并全文一致
- recent_events：date 必须 YYYY-MM-DD（仅知年月用 YYYY-MM-01），每条必须有 source URL；impact 可写分析但注明依据
- 交叉验证：人物职位/重大事件至少 2 个独立来源；禁止编造，查不到留空/null
- apec_stance：必须如实写明加纳不是APEC成员（APEC现有21个成员经济体，加纳从未加入），可补充其实际国际合作框架，禁止编造APEC历史
- collection_meta：phase="phase3_enriched"；quotes=对象数组[{{"title":"...","url":"..."}}]≥3条(Wikipedia+官网+新闻)，禁止纯字符串数组或空数组；data_sources=本次实际来源类型枚举
- Windows编码（必读）：用 Write 工具创建临时 .py 脚本（放 scripts_tmp/），脚本内 json.dump(data, f, ensure_ascii=False, indent=2) + open(...,'w',encoding='utf-8') 写入后再 Bash 执行；或直接用 Write 工具写完整 JSON；中文引号用「」
- 工作区纪律：只允许删除你本次自己创建的临时文件；scripts_tmp/ 和 output/gh/2026-11-17/_tmp/ 中其他文件（含 gh_p3_dispatch.py、gh_p3_finalize.py 等主会话编排脚本）禁止触碰

写入后验证（不可跳过）：
python .agents/skills/country-org-collector/scripts/validate_schema.py output/gh/2026-11-17 --file output/gh/2026-11-17/orgs/{org_id}.json
如有 ERRORS→修复→重验直到 0 errors；然后运行同命令加 --score 更新 completeness_score。

工作区卫生：临时文件只放 output/gh/2026-11-17/_tmp/ 或 scripts_tmp/，收尾清理你自己的临时文件。

完成后返回：org_id、最终 completeness_score、来源数量、仍缺失字段列表。"""

targets = {t["org_id"]: t for t in json.load(open(os.path.join(BASE, "_p3_final_targets.json"), encoding="utf-8"))["targets"]}

for oid in sys.argv[1:]:
    t = targets[oid]
    sk = json.load(open(os.path.join(BASE, "orgs", oid + ".json"), encoding="utf-8"))
    ot = sk.get("basic_info", {}).get("org_type") or t["category"]
    print("=" * 30, oid, "=" * 30)
    print(tpl.format(org_id=oid, name_en=t["name_en"],
                     website=t["website"] or "(搜索确认官网)", org_type=ot))
    print()
