# -*- coding: utf-8 -*-
"""Build person profile BO-PERSON-000216 (María Esther Hinojosa García)."""
import json
import os

profile = {
    "person_id": "BO-PERSON-000216",
    "wikidata_qid": None,
    "name": "María Esther Hinojosa García",
    "name_en": "Maria Esther Hinojosa Garcia",
    "name_zh": "玛丽亚·埃丝特·伊诺霍萨·加西亚",
    "aliases": [
        "Maria Esther Hinojosa Garcia"
    ],
    "nationality": "BO",
    "gender": "female",
    "birth_date": None,
    "birth_place": None,
    "contacts": [
        {
            "type": "email",
            "value": "planificacion@esm.gob.bo",
            "source": "ESM官网「透明度与人力资源」页面 (esm.gob.bo/transparencia.php)，访问日期2026-10-25"
        }
    ],
    "current_positions": [
        "穆通钢铁公司规划总经理"
    ],
    "education": [],
    "work_experience": [
        {
            "organization": "穆通钢铁公司 (Empresa Siderúrgica del Mutún)",
            "org_id": "BO-SOE-009",
            "position": "规划总经理",
            "start_date": None,
            "is_current": "true",
            "start_date_note": "具体就任日期未公开。ESM于2024-03-07发布「规划经理」外部招聘公告（ESM官方Facebook）；矿业与冶金部官方Facebook在2025-02-24穆通钢铁厂落成典礼帖文中标注其姓名，表明其当时已在ESM任职",
            "source": "ESM官网「透明度与人力资源」页面 (esm.gob.bo/transparencia.php)，访问日期2026-10-25"
        },
        {
            "organization": "玻利维亚公共工程服务与住房部 (Ministerio de Obras Públicas, Servicios y Vivienda)",
            "org_id": "BO-GOV-013",
            "position": "公职人员",
            "start_date": None,
            "end_date": None,
            "note": "单一来源信息：LatamVerify公职人员数据库记录其于2023-09-22为该部公职人员（FUNCIONARIO PÚBLICO），具体职务未披露；存在同名者可能，采信程度较低",
            "source": "LatamVerify (latamverify.com/profile/bo/fp/maria-esther-hinojosa-garcia-61573.html)"
        }
    ],
    "person_relationships": [
        {
            "person_id": "BO-PERSON-000215",
            "person_name": "阿尔瓦罗·特赫里纳·奥利维拉 (Álvaro Tejerina Olivera)",
            "relationship_type": "superior",
            "description": "特赫里纳自2026年1月起出任穆通钢铁公司执行总裁（代理，a.i.），为伊诺霍萨在公司管理层的直接上级；两人同列于ESM官网「透明度与人力资源」页面管理团队名单",
            "source": "ESM官网 (esm.gob.bo/transparencia.php)；El Deber/eju.tv 2026-02-12报道"
        }
    ],
    "social_accounts": [],
    "family_members": [],
    "political_stances": [],
    "major_achievements": [],
    "biography_summary": "玛丽亚·埃丝特·伊诺霍萨·加西亚是玻利维亚国有钢铁企业穆通钢铁公司（Empresa Siderúrgica del Mutún，ESM）现任规划总经理（Gerente de Planificación），负责公司战略与规划事务。ESM受玻利维亚矿业与冶金部管辖，运营位于圣克鲁斯省苏亚雷斯港附近的穆通钢铁综合项目：该项目由中国中钢集团承建、总投资约5.46亿美元，于2025年2月24日正式落成，设计年产能20万吨建筑用钢材。在罗德里戈·帕斯政府整顿国有企业的背景下，阿尔瓦罗·特赫里纳·奥利维拉出任ESM执行总裁（代理），伊诺霍萨与其同列公司官网管理团队名单。矿业与冶金部官方Facebook在2025年2月落成典礼帖文中曾标注其姓名，表明其至少自该时点已在ESM任职。据LatamVerify公职人员数据库，2023年她曾在公共工程服务与住房部任公职（单一来源，存疑）。其使用LIC.（Licenciatura，本科）头衔，学历背景、出生日期等个人信息均未公开，媒体报道极少。",
    "profile": None,
    "name_zh_note": "中文媒体无该人物独立报道，译名沿用项目既有译名索引（_name_index.json）中的「玛丽亚·埃丝特·伊诺霍萨·加西亚」",
    "position_note": "官方职务名称为Gerente de Planificación（规划经理/规划总经理），见ESM官网管理团队名单",
    "work_note": "ESM规划经理一职在2012-2013年间由Óscar Álvarez担任（La Razón 2013-01-16报道），伊诺霍萨为现任。2026年1月特赫里纳出任执行总裁（代理）后其留任规划总经理",
    "education_note": "ESM官网显示其使用LIC.（Licenciatura，本科学位）头衔，可推断持有本科学历，但毕业院校、专业与年份均未公开",
    "social_accounts_note": "社交媒体6项扫描结果：Facebook存在同名个人账户（多次评论玻利维亚时政、公共工程部长Montano帖文及矿业部落成典礼帖文标注），但无法获取可验证的个人主页URL，故留空；Instagram（mariaestherhinojosacastillo）与TikTok（maria.esther.hino2）命中的同名账户属其他人，未采信；LinkedIn、X/Twitter、YouTube未发现其账户",
    "identity_note": "LatamVerify同名公职记录与Facebook同名个人账户均为单一来源，未能以第二独立来源确认与ESM现任规划总经理的同一性，相关推断仅用于备注及已标注存疑的条目，未计入其他结构化字段",
    "collection_meta": {
        "collection_date": "2026-10-25",
        "phase": "phase4_person_profile",
        "data_sources": [
            "official_website",
            "government_directory",
            "wikipedia",
            "news_search",
            "web_search",
            "social_media"
        ],
        "notes": "人物公开信息极其有限。核心事实（现任职务、官方邮箱、管理团队名单）来自ESM官网透明度页面（官方一手来源）。时间线依据：ESM于2024-03-07公开发布规划经理外部招聘公告；2025-02-24矿业与冶金部落成典礼帖文标注其姓名；2026年3月 Facebook 评论中第三方以女性称谓（la gerente de planificación）提及该职务，与官网名单互证。2023年公职记录（公共工程服务与住房部）为LatamVerify单一聚合来源，存在同名可能，已标注存疑。Wikidata无条目，中文媒体无独立报道。2021年Facebook同名账户曾留言「soy del MAS」，因账户身份未获两源确认，未录入political_stances。",
        "quotes": [
            {
                "title": "Transparencia y Recursos Humanos - Empresa Siderúrgica del Mutún（ESM官网管理团队名单）",
                "url": "https://esm.gob.bo/transparencia.php"
            },
            {
                "title": "Maria Esther Hinojosa Garcia - Funcionario Público - 61573（LatamVerify公职人员数据库）",
                "url": "https://latamverify.com/profile/bo/fp/maria-esther-hinojosa-garcia-61573.html"
            },
            {
                "title": "Complejo Siderúrgico del Mutún: la 「ciudad de acero」 que hoy respira óxido y maleza（El Deber via eju.tv, 2026-02-12）",
                "url": "https://eju.tv/2026/02/complejo-siderurgico-del-mutun-la-ciudad-de-acero-que-hoy-respira-oxido-y-maleza/"
            },
            {
                "title": "Siderúrgica del Mutún - Wikipedia (es)",
                "url": "https://es.wikipedia.org/wiki/Sider%C3%BArgica_del_Mut%C3%BAn"
            },
            {
                "title": "#ConvocatoriaPersonalExterno GERENTE DE PLANIFICACIÓN（ESM官方Facebook, 2024-03-07）",
                "url": "https://www.facebook.com/EmpresaSiderurgicaDelMutun/posts/convocatoriapersonalexterno-la-empresa-sider%C3%BArgica-del-mut%C3%BAn-invita-a-las-intere/885598823362726/"
            },
            {
                "title": "Ministerio de Minería y Metalurgia Bolivia - Facebook（2025-02-25落成典礼帖文，标注其姓名）",
                "url": "https://www.facebook.com/minmineriabol/photos/d41d8cd9/122223380102068615/"
            },
            {
                "title": "La ESM utilizará equipos de la Jindal para operar en el Mutún - La Razón（2013-01-16，时任规划经理为Óscar Álvarez）",
                "url": "https://hemeroteca.larazon.bo/economia/2013/01/16/la-esm-utilizara-equipos-de-la-jindal-para-operar-en-el-mutun/"
            }
        ]
    }
}

out_path = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\BO-PERSON-000216.json"
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(profile, f, ensure_ascii=False, indent=2)
print("WROTE", out_path)
print("bio length:", len(profile["biography_summary"]))
