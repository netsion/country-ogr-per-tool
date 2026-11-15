import json,pathlib,jsonschema
p=pathlib.Path('tmp/tw_batch5_enriched/TW-PERSON-000542.json');d=json.loads(p.read_text('utf-8'))
d['major_achievements'][0]['achievement']='2019年起主持《POP撞新闻》，并坚持广播同步YouTube直播与观众互动，记录广播及网络制作的职业节点。'
d['major_achievements'][1]={'date':'2019-03-07','achievement':'与高嘉瑜共同主持WIN TV《我要当选》，节目首集于3月7日播出；为独立于广播节目的电视主持节点。','organization':'WIN TV综合台'}
d['collection_meta']['quotes'] += [{'title':'Hit Fm广告价目及节目表（2026年9月30日更新）','url':'https://www.hitoradio.com/showtime/pdf/HITFM2026.pdf'},{'title':'王其／高嘉瑜主持秀的背后（记载我要当选已播出首集）','url':'https://www.i-media.tw/Article/Detail/7804'}]
d['collection_meta']['notes'] += ' 补核：官方2026-09-30更新节目表仍列黄暐瀚主持，支持嗆新闻为当期节目。发现2026-10-28及11-13实际节目影片链接，但YouTube和观测原文读取失败，故不以摘要认定该两日参与或观点。品观点两条政策原文均署编辑中心，正文明确以黄暐瀚表示/强调归属本人，其中能源文章直接引述解决问题而不是政治秀；属于节目方对本人意见的明确归属报道，并非本人署名全文或完整逐字稿，保留此限制。成果已将广播及同步直播合一，第二条改为独立电视节目已播出节点（爱传媒全文可读）。'
jsonschema.validate(d,json.loads(pathlib.Path('.agents/skills/country-org-collector/person_profile_schema.json').read_text('utf-8')));p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
