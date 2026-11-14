# 修正 NG 数据集 org_subtype 旧枚举值 -> 新枚举（2026-11-12 schema）语义就近映射
# 依据 enum_reference.md: GOV/CORP/NGO/ACAD/MEDIA/FIN/INTL/PARTY/MIL 各自子类型
import json, glob

BASE = 'output/ng/2026-11-10/orgs'

MAP = {
    # CORP: oil_refining -> 子公司（丹格特炼油厂为 Dangote Group 旗下单一资产子公司）
    'oil_refining': 'subsidiary',
    # INTL: 区域组织/区域司法机构/区域立法机构 -> regional_org；国际研究机构 -> multilateral_org（CGIAR 体系）
    'regional_organization': 'regional_org',
    'regional_judicial_organ': 'regional_org',
    'regional_legislative_organ': 'regional_org',
    'international_research_institute': 'multilateral_org',
    # MEDIA: 在线报纸 -> 数字媒体（数字原生）
    'online_newspaper': 'digital_media',
    # MIL: 军种 -> 武装力量；执法/准军事 -> 安全机构
    'military_branch': 'armed_forces',
    'law_enforcement': 'security_agency',
    'paramilitary': 'security_agency',
    # NGO: 各类专门 NGO -> advocacy_group；NGO 网络 -> professional_association（会员制网络）
    'advocacy_ngo': 'advocacy_group',
    'civic_tech_ngo': 'advocacy_group',
    'digital_rights_ngo': 'advocacy_group',
    'election_observation_ngo': 'advocacy_group',
    'cso_network': 'professional_association',
    # PARTY: political_party -> 执政党/反对党（按语义：APC 联邦执政，其余反对）
    'political_party': '__party_by_id__',
}

# 政党按 2025-2026 尼日利亚联邦层面实际地位
RULING = {'NG-PARTY-001'}  # APC

fixed = 0
for fp in sorted(glob.glob(f'{BASE}/*.json')):
    with open(fp, encoding='utf-8') as f:
        o = json.load(f)
    bi = o.get('basic_info', {})
    st = bi.get('org_subtype')
    if st not in MAP:
        continue
    new = MAP[st]
    if new == '__party_by_id__':
        new = 'ruling_party' if o['org_id'] in RULING else 'opposition_party'
    bi['org_subtype'] = new
    with open(fp, 'w', encoding='utf-8') as f:
        json.dump(o, f, ensure_ascii=False, indent=2)
    print(f"{o['org_id']}: {st} -> {new}")
    fixed += 1

print(f"\nTotal fixed: {fixed}")
