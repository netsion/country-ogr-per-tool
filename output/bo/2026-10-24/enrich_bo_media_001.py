#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase3 enrichment for BO-MEDIA-001 (El Deber, Bolivia). Writes UTF-8 JSON atomically."""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..',
                                '.agents', 'skills', 'country-org-collector', 'scripts'))
try:
    from atomic_write import atomic_json_write
except Exception:
    atomic_json_write = None

TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'orgs', 'BO-MEDIA-001.json')

with open(TARGET, encoding='utf-8') as f:
    data = json.load(f)

data['basic_info']['aliases'] = ['Diario Mayor El Deber', 'Grupo EL DEBER', '任务报']
data['basic_info']['founded_date'] = '1953-02-11'
data['basic_info']['website'] = 'https://www.eldeber.com.bo/'

data['social_accounts'] = [
    {
        'platform': 'twitter_x',
        'account_name': 'diarioeldeber',
        'url': 'https://twitter.com/diarioeldeber',
        'source': 'wikidata'
    },
    {
        'platform': 'twitter_x',
        'account_name': 'grupoeldeber',
        'url': 'https://x.com/grupoeldeber',
        'source': 'https://x.com/grupoeldeber/status/2021539717829784058'
    },
    {
        'platform': 'facebook',
        'account_name': 'Grupo EL DEBER',
        'url': 'https://www.facebook.com/GrupoELDEBER',
        'source': 'https://www.facebook.com/GrupoELDEBER'
    },
    {
        'platform': 'instagram',
        'account_name': 'eldeber.com.bo',
        'url': 'https://www.instagram.com/eldeber.com.bo/',
        'source': 'https://www.instagram.com/reel/DUmTHgsCcxe/'
    },
    {
        'platform': 'tiktok',
        'account_name': 'eldeber.com.bo',
        'url': 'https://www.tiktok.com/@eldeber.com.bo',
        'source': 'https://www.tiktok.com/@eldeber.com.bo/video/7605395521175375124'
    },
    {
        'platform': 'youtube',
        'account_name': 'EL DEBER (@webeldeber)',
        'url': 'https://www.youtube.com/@webeldeber',
        'source': 'https://www.youtube.com/@webeldeber'
    }
]

data['digital_assets'] = [
    {
        'name': 'ED24 Streaming TV',
        'url': None,
        'description': '集团流媒体电视频道，2025-09-27 在 Expocruz 2025 开播，经 AXS Plus 有线电视 64 频道等播出，主打新闻分析类内容，是集团全媒体转型的核心载体。',
        'source': 'https://eldeber.com.bo/pais/grupo-el-deber-estrena-su-senal-de-television-ed24_531542/'
    },
    {
        'name': 'El Deber Play (ED Play)',
        'url': 'https://play.eldeber.com.bo',
        'description': '官方流媒体点播平台，提供新闻视频、直播与节目点播服务。',
        'source': 'https://play.eldeber.com.bo'
    },
    {
        'name': 'El Deber Radio (FM 103.3)',
        'url': 'https://www.eldeber.com.bo/',
        'description': '集团广播电台，频率 FM 103.3，官网提供在线直播入口（Nuestra senal al Vivo）。',
        'source': 'https://www.eldeber.com.bo/'
    },
    {
        'name': 'e-Paper 数字报',
        'url': None,
        'description': '印刷日报的电子版（e-Paper），官网导航提供入口。',
        'source': 'https://www.eldeber.com.bo/'
    }
]

data['key_people'] = [
    {
        'person_id': None,
        'name': 'Juan Carlos Rivero Jordán',
        'title': '社长兼总经理（Presidente / Gerente General del Grupo EL DEBER）',
        'title_description': '官网 2020-08-17 报道其出任集团总经理（Gerente General）；CONNECTAS 2024-12 视频称其为 presidente EL DEBER；西语维基百科信息框将其列为 Director（台长）。各来源称谓略有差异，均指向其为现任最高负责人。',
        'description': '土木工程师出身，拥有明尼苏达大学结构计算硕士学位及 Utepsa-哈瓦那大学金融硕士学位；1994 年加入集团，历任记者、总编辑（editor general）、主编（director periodístico）及董事会成员，曾以环境报道获国际保护组织（Conservation International）2001 年首奖。2020 年 8 月出任总经理，公司治理回归创始家族；2026 年 2 月以集团负责人身份主导创刊 73 周年纪念活动。'
    },
    {
        'person_id': None,
        'name': 'Pedro Rivero Jordán',
        'title': '编辑委员会主席（Presidente del Consejo Editorial de EL DEBER）',
        'title_description': '官网 2026-07-30 报道中以其编辑委员会主席身份代表报社领奖。',
        'description': 'Rivero 创始家族成员，主持报社编辑委员会；2026-07-30 代表 EL DEBER 接受圣克鲁斯省议会机构表彰，重申新闻独立与捍卫言论自由的承诺。与 Juan Carlos Rivero Jordán 同为家族治理核心（两者具体亲属关系未获权威来源明确说明）。'
    },
    {
        'person_id': None,
        'name': 'Lucas Saucedo Sevilla',
        'title': '创办人（Fundador，1953 年）',
        'title_description': '西语维基百科信息框记载其为创办人。',
        'description': '1953 年在圣克鲁斯-德拉谢拉创办 El Deber。官方以 2 月 11 日为创刊纪念日（2026-02-11 庆祝 73 周年，据此推定创刊日为 1953-02-11）；西语维基百科信息框记载创办日期为 1953-06-10，与官方纪念日期不一致，本档案采用官方纪念日期。'
    }
]

data['departments'] = [
    {
        'name': '新闻编辑部（Redacción）',
        'dept_id': 'BO-MEDIA-001-DEPT-001',
        'head': None,
        'description': '统筹日报与新闻网站的采编业务，官网版面下设圣克鲁斯地方、国内（País）、经济（Economía）、国际（Mundo）、体育（Deportes）、观点（Opinión）、教育与社会（Educación y Sociedad）等条线。',
        'parent_dept_id': None
    },
    {
        'name': '调查报道项目（ED Investiga）',
        'dept_id': 'BO-MEDIA-001-DEPT-002',
        'head': None,
        'description': '深度调查与数据核查团队，隶属编辑部，专注调查性新闻报道。',
        'parent_dept_id': 'BO-MEDIA-001-DEPT-001'
    },
    {
        'name': '印刷厂（Imprenta）',
        'dept_id': 'BO-MEDIA-001-DEPT-003',
        'head': None,
        'description': '负责日报印制并对外提供商业印刷服务；据官网 2020-08 报道，此前三年完成了制版新技术引进与印刷设备自动化升级。',
        'parent_dept_id': None
    },
    {
        'name': 'ED24 电视台',
        'dept_id': 'BO-MEDIA-001-DEPT-004',
        'head': None,
        'description': '2025-09-27 在 Expocruz 2025 开播的流媒体电视频道，经 AXS Plus 有线 64 频道等播出，定位为从圣克鲁斯分析、解释并连接全国受众的新闻频道。',
        'parent_dept_id': None
    },
    {
        'name': 'El Deber Radio（FM 103.3 电台）',
        'dept_id': 'BO-MEDIA-001-DEPT-005',
        'head': None,
        'description': '集团广播电台，频率 FM 103.3，官网提供在线直播；曾设 El Deber Sports 等品牌栏目。',
        'parent_dept_id': None
    }
]

data['recent_events'] = [
    {
        'date': '2025-09-27',
        'title': 'Grupo EL DEBER 开播流媒体电视台 ED24',
        'description': '集团在 Expocruz 2025 展位举行开播仪式，ED24 经 AXS Plus 有线电视 64 频道等正式播出；集团宣称由此成为玻利维亚唯一同时覆盖报纸、网络、广播、电视与流媒体的 360 度媒体。',
        'impact': '完成从传统纸媒向全媒体集团的关键转型，显著扩大音视频内容受众与广告触达。',
        'source': 'https://eldeber.com.bo/pais/grupo-el-deber-estrena-su-senal-de-television-ed24_531542/'
    },
    {
        'date': '2026-02-11',
        'title': 'El Deber 庆祝创刊 73 周年，政学界表彰其公信力',
        'description': '报社以 73 años informando con pasión y compromiso 为主题推出纪念特刊与专题（官网设 73-aniversario 专题页），回顾玻利维亚民主化进程、自治运动等标志性报道；学者与机构公开表彰其 73 年透明、均衡的新闻实践，官方叙事强调其印刷、数字、广播、电视、流媒体一体的 360 度媒体定位。',
        'impact': '巩固其圣克鲁斯乃至全国主流媒体声望，为品牌信任度与商业合作背书。',
        'source': 'https://eldeber.com.bo/santa-cruz/academicos-instituciones-destacan-trayectoria-deber-73-anos_1770850934'
    },
    {
        'date': '2026-02-10',
        'title': '社长 Juan Carlos Rivero Jordán 发表 73 周年致辞并推出家族传承专题',
        'description': '集团官方账号发布 Rivero Jordán 致辞视频，称真正的新闻业依靠职业精神、承诺与同社会的真实连接构建；同期推出 El Deber, el legado de la familia Rivero 家族传承访谈，并继续宣传与拉美新闻平台 CONNECTAS 合作的独立新闻众筹项目（该合作 2024-12 已启动）。',
        'impact': '重申独立编辑立场，探索众筹等多元化可持续商业模式。',
        'source': 'https://www.facebook.com/GrupoELDEBER/videos/1409421240206884/'
    },
    {
        'date': '2026-07-30',
        'title': '圣克鲁斯省议会授予 EL DEBER 机构表彰',
        'description': '在圣伊格纳西奥-德贝拉斯科建城 278 周年荣誉会议上，圣克鲁斯省议会表彰 EL DEBER 对内陆省份议题（森林火灾、领土保护等）的持续报道及其对玻利维亚新闻业的贡献；编辑委员会主席 Pedro Rivero Jordán 代表领奖，重申独立、捍卫言论自由与服务社会的承诺。',
        'impact': '获省级官方机构背书，强化其区域新闻公信力与省份覆盖优势。',
        'source': 'https://eldeber.com.bo/santa-cruz/reconocen-aporte-periodistico-deber-d_1785408042'
    },
    {
        'date': '2026-10-15',
        'title': '所属报业协会 ANP 谴责伪造公告（媒体行业动态）',
        'description': 'El Deber 报道：其成员组织玻利维亚全国新闻协会（ANP）谴责有伪造公告滥用该协会标志，并公开澄清相关文件系虚假文件。',
        'impact': '反映玻利维亚报业面临虚假信息伪造风险，协会与成员媒体协同维护行业公信力。',
        'source': 'https://eldeber.com.bo/pais/anp-denuncia-comunicado-falso-logotipo-institucion_1792108072'
    }
]

data['related_entities'] = [
    {
        'org_id': None,
        'org_name': 'Empresa de Comunicación Social El Deber S.A. (Grupo EL DEBER)',
        'org_type': 'MEDIA',
        'org_description': 'El Deber 的出版母公司，玻利维亚圣克鲁斯的多媒体集团，由创始家族 Rivero 家族主导治理；业务涵盖报纸、新闻网站、广播、流媒体电视（ED24）与点播平台（El Deber Play）。',
        'relationship_type': 'parent_org'
    },
    {
        'org_id': None,
        'org_name': 'Asociación Nacional de la Prensa de Bolivia (ANP)',
        'org_type': 'NGO',
        'org_description': '玻利维亚全国新闻（报业）协会，非营利行业组织，由全国主要印刷日报组成（含 Correo del Sur、El Deber、ANF 等），维护新闻自由与行业权益。',
        'relationship_type': 'member_of'
    },
    {
        'org_id': None,
        'org_name': 'CONNECTAS',
        'org_type': 'NGO',
        'org_description': '拉丁美洲调查性新闻非营利平台，2024-12 起与 EL DEBER 开展联合众筹与合作新闻项目，支持独立新闻生产。',
        'relationship_type': 'partner'
    }
]

data['core_business'] = ('El Deber（任务报）是玻利维亚圣克鲁斯-德拉谢拉的主流西语日报，由 Empresa de Comunicación Social El Deber S.A. '
                         '（Grupo EL DEBER）出版，1953 年创刊，是圣克鲁斯地区历史最悠久、最具影响力的日报之一，自称玻利维亚最大的新闻门户。'
                         '核心业务涵盖：印刷日报（Diario Mayor）及 e-Paper 数字报；新闻网站 eldeber.com.bo（集团 2020 年披露月独立访客超 600 万，'
                         '为玻利维亚媒体中最大的数字受众规模）；广播电台 El Deber Radio（FM 103.3）；2025 年 9 月开播的流媒体电视台 ED24'
                         '（经 AXS Plus 有线 64 频道等播出）；点播流媒体平台 El Deber Play；以及覆盖 Facebook、X、Instagram、TikTok、YouTube 的'
                         '社交媒体矩阵（2020 年披露合计粉丝超 300 万）。内容版面包括圣克鲁斯地方、国内、经济、国际、体育、观点、教育与社会等，'
                         '设调查报道项目 ED Investiga，并与 BBC、埃菲社（EFE）、RFI 等国际媒体开展内容合作。另经营商业印刷业务并颁发 Premio Mayor'
                         ' 新闻奖。编辑立场标榜独立与捍卫言论自由，公司治理由创始家族 Rivero 家族主导。')

data['apec_stance'] = ('玻利维亚不是APEC成员（APEC现有21个成员经济体，玻利维亚未加入）。因此不存在El Deber对APEC的官方立场；'
                       '玻利维亚的对外经贸合作主要通过安第斯共同体、南方共同市场等区域机制开展。作为商业媒体，该报对APEC及亚太议题仅作一般性新闻报道，无专门的公开立场文件。')

data['industries'] = ['media_publishing', 'broadcasting', 'digital_media']

data['profile'] = {
    'source_url': 'https://es.wikipedia.org/wiki/El_Deber',
    'local_path': None
}

data['collection_meta'] = {
    'collection_date': '2026-10-24',
    'phase': 'phase3_enriched',
    'data_sources': [
        'wikipedia',
        'wikidata',
        'official_website',
        'eldeber.com.bo articles (2020-08-17, 2025-09-27, 2026-02-11, 2026-07-30, 2026-10-15)',
        'facebook.com/GrupoELDEBER',
        'instagram.com/eldeber.com.bo',
        'tiktok.com/@eldeber.com.bo',
        'x.com/grupoeldeber',
        'youtube.com/@webeldeber',
        'connectas.org video (2024-12-10)',
        'anp-bolivia.com',
        'instantaneas.org.bo (2026-02-11)'
    ],
    'quotes': [
        {
            'title': 'Diario Mayor El Deber - Wikipedia (fundación, propietario, director)',
            'url': 'https://es.wikipedia.org/wiki/El_Deber'
        },
        {
            'title': 'Grupo EL DEBER da nuevos pasos hacia la transformación (EL DEBER, 2020-08-17)',
            'url': 'https://eldeber.com.bo/pais/grupo-el-deber-da-nuevos-pasos-hacia-la-transformacion_196314/'
        },
        {
            'title': 'Grupo EL DEBER estrena su señal de televisión ED24 (EL DEBER, 2025-09-27)',
            'url': 'https://eldeber.com.bo/pais/grupo-el-deber-estrena-su-senal-de-television-ed24_531542/'
        },
        {
            'title': 'Académicos e instituciones destacan trayectoria de EL DEBER en sus 73 años (EL DEBER, 2026-02-11)',
            'url': 'https://eldeber.com.bo/santa-cruz/academicos-instituciones-destacan-trayectoria-deber-73-anos_1770850934'
        },
        {
            'title': 'Reconocen el aporte periodístico de EL DEBER (EL DEBER, 2026-07-30)',
            'url': 'https://eldeber.com.bo/santa-cruz/reconocen-aporte-periodistico-deber-d_1785408042'
        },
        {
            'title': 'Jorge Carrasco asume la presidencia de la ANP - ANP conformada por ... El Deber (EL DEBER, 2023-02-24)',
            'url': 'https://eldeber.com.bo/pais/jorge-carrasco-asume-la-presidencia-de-la-asociacion-nacional-de-la-prensa_315622/'
        }
    ],
    'completeness_score': 13,
    'notes': ('Phase3 enrichment 2026-10-24. founded_date 采用官方 73 周年纪念日期（2026-02-11）推定为 1953-02-11；西语维基百科信息框记载 1953-06-10，'
              '与官方纪念日期不一致，已在字段描述中说明。Juan Carlos Rivero Jordán 头衔综合官网（Gerente General, 2020）、CONNECTAS（presidente, 2024-12）'
              '与维基百科（Director）。key_people 三人及 ANP、CONNECTAS、母公司均未命中 _name_index.json，org_id/person_id 置 null，未修改 id_registry.json。'
              '搜索来源共 6 次检索 + 4 次页面读取（维基百科、官网首页、官网 2020 文章、表彰文章元数据）。')
}

payload = json.dumps(data, ensure_ascii=False, indent=2)

if atomic_json_write:
    atomic_json_write(TARGET, data)
else:
    tmp = TARGET + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, TARGET)

# sanity: reload and confirm
with open(TARGET, encoding='utf-8') as f:
    check = json.load(f)
print('WROTE', TARGET)
print('phase:', check['collection_meta']['phase'],
      '| key_people:', len(check['key_people']),
      '| departments:', len(check['departments']),
      '| events:', len(check['recent_events']),
      '| social:', len(check['social_accounts']),
      '| related:', len(check['related_entities']),
      '| digital:', len(check['digital_assets']))
print('core_business chars:', len(check['core_business']), '| apec_stance chars:', len(check['apec_stance']))
