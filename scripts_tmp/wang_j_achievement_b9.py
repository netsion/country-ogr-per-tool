import json
from pathlib import Path
import jsonschema
p=Path('tmp/tw_batch9_enriched/TW-PERSON-000027.json'); d=json.loads(p.read_text(encoding='utf-8'))
d['major_achievements']=[{'date':'2014-04-10','organization':'立法院','achievement':'參與化解太陽花學運占領議場僵局：4月6日以院長職權承諾監督條例立法前不召集服貿黨團協商，成為促成學生4月10日退場的協調因素。2014年4月18日Newtalk全文明載其聲明促成退場，並記錄他曾接觸各黨及綜合各方意見；此為學生、社運及朝野等多方共同形成的退場結果，不代表他單獨完成，也不代表監督條例已立法或服貿已通過。'}]
d['collection_meta']['quotes'].append({'title':'馬英九若私下邀約 王金平：一定盡快赴約（記錄協調與退場作用）','url':'https://newtalk.tw/news/view/2014-04-18/46442'})
d['collection_meta']['notes']+=' 定向補核2014退場成果：Newtalk 2014-04-18全文明載4月6日聲明促成退場，並確認學生於10日退場；據此收錄一項有限度的多方協調成果，非由相鄰日期推因果。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');jsonschema.validate(d,json.loads(Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text(encoding='utf-8')));print('JSONSCHEMA PASS')
