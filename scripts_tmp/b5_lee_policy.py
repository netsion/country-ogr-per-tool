import json,jsonschema
p='tmp/tw_batch5_enriched/TW-PERSON-000547.json'
d=json.load(open(p,encoding='utf-8'));u='https://www.ftvnews.com.tw/news/detail/2023A02W0211'
d['political_stances']=[{'date':'2023-10-02','topic':'國造潛艦預算審查','stance_content':'在臉書評論劍龍級潛艦戰鬥系統提升案預算審查時，反對其認為缺乏合理依據、為阻擋而阻擋的預算凍結方式，並肯定該次凍結失敗、同意動支的結果。此為媒體人對具體國防預算審查的評論，不代表官方審計結論。','source':u}]
d['collection_meta']['quotes'].append({'title':'快新聞／潛艦連中國農民都會做 他爆馬文君為擋潛艦國造驚句連發','url':u})
d['collection_meta']['notes']+=' 補充核讀民視2023-10-02全文，僅摘國造潛艦預算凍結的具體評論；排除對個人動機及洩密指控。其他已搜核三投票率預測、罷免策略、媒宣費政治反制，未視為公共政策立場補數，跨議題仍不足。'
jsonschema.validate(d,json.load(open('.agents/skills/country-org-collector/person_profile_schema.json',encoding='utf-8')))
open(p,'w',encoding='utf-8').write(json.dumps(d,ensure_ascii=False,indent=2));print('jsonschema PASS')
