# -*- coding: utf-8 -*-
"""P2 remediation round 3 (v2): map invalid org_subtype values to schema enums.
Writes each modified file back in the same iteration."""
import json
import glob
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
M = {
    ('GOV', 'head_of_state_office'): 'head_of_state',
    ('GOV', 'executive_agency'): 'statutory_board',
    ('GOV', 'oversight'): 'independent_organ',
    ('GOV', 'tax_agency'): 'statutory_board',
    ('GOV', 'statistical_agency'): 'statutory_board',
    ('GOV', 'electoral_body'): 'independent_organ',
    ('GOV', 'regulator'): 'regulatory_agency',
    ('GOV', 'prosecution'): 'independent_organ',
    ('MIL', 'police'): None, ('MIL', 'army'): None,
    ('MIL', 'navy'): None, ('MIL', 'air_force'): None,
    ('MIL', 'armed_forces'): None,
    ('SOE', 'lithium'): 'state_owned_enterprise',
    ('SOE', 'electricity'): 'state_owned_enterprise',
    ('SOE', 'urban_transport'): 'state_owned_enterprise',
    ('SOE', 'aviation'): 'state_owned_enterprise',
    ('SOE', 'oil_and_gas'): 'state_owned_enterprise',
    ('SOE', 'food'): 'state_owned_enterprise',
    ('SOE', 'steel'): 'state_owned_enterprise',
    ('SOE', 'mining'): 'state_owned_enterprise',
    ('SOE', 'telecommunications'): 'state_owned_enterprise',
    ('CORP', 'beverages'): 'private_company',
    ('CORP', 'pharmacy_retail'): 'private_company',
    ('CORP', 'retail'): 'private_company',
    ('CORP', 'cement'): 'private_company',
    ('CORP', 'food'): 'private_company',
    ('CORP', 'mining'): 'private_company',
    ('CORP', 'telecommunications'): 'private_company',
    ('CORP', 'energy_transport'): 'private_company',
    ('NGO', 'labor_union'): 'trade_union',
    ('NGO', 'business_association'): 'professional_association',
    ('NGO', 'environment'): 'advocacy_group',
    ('NGO', 'human_rights'): 'advocacy_group',
    ('NGO', 'wildlife_conservation'): 'advocacy_group',
    ('NGO', 'child_welfare'): 'humanitarian_org',
    ('NGO', 'cultural_foundation'): 'foundation',
    ('NGO', 'development'): 'foundation',
    ('NGO', 'research'): 'think_tank',
    ('NGO', 'education'): 'community_org',
    ('ACAD', 'public_university'): 'university',
    ('ACAD', 'private_university'): 'university',
    ('ACAD', 'academy'): 'research_institute',
    ('MEDIA', 'television'): 'broadcaster',
    ('MEDIA', 'radio'): 'broadcaster',
    ('FIN', 'microfinance_bank'): 'commercial_bank',
    ('FIN', 'development_bank'): 'commercial_bank',
    ('FIN', 'central_bank'): None,
    ('FIN', 'financial_regulator'): None,
    ('INTL', 'regional_integration'): 'regional_org',
    ('INTL', 'global'): 'multilateral_org',
    ('INTL', 'development_bank'): 'multilateral_org',
    ('INTL', 'regional'): 'regional_org',
    ('PARTY', ''): None,
}

changed = 0
for f in sorted(glob.glob(os.path.join(D, 'orgs', '*.json'))):
    p = json.load(open(f, encoding='utf-8'))
    ot = p['basic_info'].get('org_type')
    st = p['basic_info'].get('org_subtype')
    if st is None:
        continue
    key = (ot, st)
    if key in M:
        new = M[key]
        p['basic_info']['org_subtype'] = new
        with open(f + '.tmp', 'w', encoding='utf-8') as fh:
            json.dump(p, fh, ensure_ascii=False, indent=2)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(f + '.tmp', f)
        print('%s: %s/%s -> %r' % (p['org_id'], ot, st, new))
        changed += 1
print('changed:', changed)
