"""Verify staged source IDs against their actual USER-ID columns before installation."""
import json,pathlib,sys
import social_xlsx_common as soc
R=pathlib.Path(__file__).resolve().parents[1];O=R/'tmp/tw_batch7_20261116';p=R/'tmp/tw_batch7_enriched/TW-PERSON-000571.json'
load=lambda p:json.loads(p.read_text(encoding='utf-8'))
d=load(p);records=load(R/'tmp/social_xlsx_20261116/records.json');audit=[]
for a in d['social_accounts']:
 if a['platform']=='line':continue
 key=soc.urlkey(a['url']);hits=[h for h in records if tuple(h['key'])==key];values={soc.bare(h['raw_user_id']) for h in hits if h.get('raw_user_id')}
 assert len(values)==1,(a['platform'],values)
 value=next(iter(values));prior=a.get('user_id')
 if a['platform']=='facebook':assert soc.bare(prior)=='168362567115285' and value=='100052208030441'
 else:assert soc.bare(prior)==value
 a['user_id']=soc.uidval(a['platform'],value)
 locs=sorted({f"{h['sheet']}!第{h['row']}行" for h in hits})
 a['source_note']='用户提供社交.xlsx同人实名、URL与USER-ID匹配：'+'；'.join(locs[-4:])+'；平台本体未完成实时认证。'
 if a['platform']=='facebook':a['source_note']+='PAGE-ID为168362567115285，未将其混入USER-ID。'
 audit.append({'platform':a['platform'],'url':a['url'],'staged_before':prior,'correct_user_id':a['user_id'],'source_locations':locs})
d['collection_meta']['notes']+=' 主会话写入前核对USER-ID/PAGE-ID列，纠正Facebook草稿混列；未改动已有正式人物账号。'
p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8');(O/'chou_account_review.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
print('Verified four platform USER-IDs and corrected staged Facebook PAGE-ID confusion')
