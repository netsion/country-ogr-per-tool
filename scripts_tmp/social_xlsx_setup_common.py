from pathlib import Path
import json
R=Path(__file__).resolve().parents[1];p=R/'scripts_tmp/social_xlsx_plan.py';s=p.read_text(encoding='utf-8');i=s.index("raw=load(O/'workbook_raw.json')")
common=R/'scripts_tmp/social_xlsx_common.py';assert not common.exists();common.write_text(s[:i],encoding='utf-8');p.write_text('from social_xlsx_common import *\n'+s[i:],encoding='utf-8')
d=json.loads((R/'.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8'));print(json.dumps(d['properties']['social_accounts'],ensure_ascii=False))
