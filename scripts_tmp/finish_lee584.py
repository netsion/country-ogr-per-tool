import json
from pathlib import Path
p=Path('tmp/tw_batch8_enriched/TW-PERSON-000584.json');d=json.loads(p.read_text(encoding='utf-8'))
d['person_relationships']=[dict(person_id='TW-PERSON-000526',person_name='蔣萬安',relationship_type='superior',description='2022年12月至2026年3月任臺北市副市長期間，蔣萬安為市長及其直接行政上級；2026年2月輝達簽約時本人公開感謝其信任授權，3月5日蔣表示批准其3月10日離職。限此任職合作關係。')]
d['collection_meta']['notes']=d['collection_meta']['notes'].replace('组织与关系ID未核真实画像，均不填','组织ID未核真实画像不填；蔣萬安ID已读取真实画像核为台北市长')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
import jsonschema
jsonschema.validate(d,json.loads(Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')))
