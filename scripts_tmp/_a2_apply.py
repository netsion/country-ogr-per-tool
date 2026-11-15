# A2 final apply: write source_url for 16 persons, append notes for 7 missing
import json

BASE = "output/ng/2026-11-10/persons/"

FILL = {
    "000317": "https://refinery.dangote.com/wp-content/uploads/2026/09/David-Bird-768x768-1.jpg",
    "000321": "https://www.mtn.com/wp-content/uploads/2018/09/Karl-Toriola_MTNN-CEO-Jan-2024-1.png",
    "000327": "https://www.airtel.africa/sites/default/files/2025-05/Sunil_Taldar_2_0_0.jpg",
    "000350": "https://brandcom.ng/wp-content/uploads/2023/06/akinyemi.jpg",
    "000380": "https://21stcenturychronicle.com/wp-content/uploads/2025/02/Prof-Adamu-Ahmed-Vice-Chancellor-Ahmadu-Bello-University-ABU-Zaria.jpg",
    "000445": "https://upload.wikimedia.org/wikipedia/commons/b/b3/Innocent_Ifediaso_Chukwuma2.jpg",
    "000459": "https://cdn.nairametrics.com/wp-content/uploads/2023/10/Segun-Agbaje-scaled-e1750506415368.jpg",
    "000460": "https://cdn.nairametrics.com/wp-content/uploads/2021/07/Miriam-Olusanya.jpg",
    "000474": "https://cdn.nairametrics.com/wp-content/uploads/2023/04/MicrosoftTeams-image-16-e1687794201387.jpg",
    "000488": "https://www.parl.ecowas.int/wp-content/uploads/2024/05/speaker-poster-2.jpeg",
    "000491": "https://webdesk.nta.ng/wp-content/uploads/2026/07/dg.jpg",
    "000496": "https://media.premiumtimesng.com/wp-content/files/2025/06/Sam-Amuka-Pemu-1.png",
    "000498": "https://cdn.modernghana.com/images/content/alexibrufast.jpg",
    "000522": "https://cdn.punchng.com/wp-content/uploads/2025/07/24150630/482223648_627125213270681_6620795270715423960_n-810x630.jpg",
    "000524": "https://media.premiumtimesng.com/wp-content/files/2026/01/Untitled-design-9.jpg",
    "000584": "https://dawncommission.org/wp-content/uploads/2023/05/Otunba-Subomi-Balogunn.jpg",
}

NOTE_FILL = {
    "000317": "头像补齐(A2)：Dangote Refinery 官网 about-us 领导层页配图（alt=David Bird, CEO/MD），HTTP 200 image/jpeg，已人工目检确认。",
    "000321": "头像补齐(A2)：MTN Group 官网 Executive Committee 页官方照片（Download Photo 源），HTTP 200 image/png，已人工目检确认。",
    "000327": "头像补齐(A2)：Airtel Africa 官网 leadership 页配图，HTTP 200 image/jpeg，已人工目检确认。",
    "000350": "头像补齐(A2)：Brandcom.ng 2023-06-08 报道《Lafarge Appoints Lolu Alade-Akinyemi As CEO》题图，HTTP 200 image/jpeg，已人工目检确认（职业形象照）。",
    "000380": "头像补齐(A2)：21st Century Chronicle 2025-02-05 ABU 新任副校长报道配图（文件名含 Prof-Adamu-Ahmed-Vice-Chancellor），HTTP 200 image/jpeg，已人工目检确认（学位服肖像，与 ABU 校刊 Special Bulletin 2025-02-05 版内肖像一致）。",
    "000445": "头像补齐(A2)：Wikimedia Commons 原图直链 File:Innocent Ifediaso Chukwuma2.jpg（225x225），HTTP 200 image/jpeg，已人工目检确认。",
    "000459": "头像补齐(A2)：Nairametrics 2025-07-12 GTCO CEO Agbaje 报道官方肖像（og:image），HTTP 200 image/jpeg，已人工目检确认。",
    "000460": "头像补齐(A2)：Nairametrics《Meet the 7 women heading Nigerian banks》(2021-07-25) 其个人条目配图（文件名 Miriam-Olusanya.jpg），HTTP 200 image/jpeg，已人工目检确认（与 2021-07 任命报道人像一致）。",
    "000474": "头像补齐(A2)：Nairametrics 2023-06-26 Alawuba 增持 UBA 报道 og:image，HTTP 200 image/jpeg，已人工目检确认（职业形象照）。",
    "000488": "头像补齐(A2)：ECOWAS 议会官网（parl.ecowas.int）2024-05 议长专题 poster 图，HTTP 200 image/jpeg（该站经代理不可达，本机直连验证通过），已人工目检确认。",
    "000491": "头像补齐(A2)：NTA 官网新闻页（标题含 Mallam Salihu Abdulhamid Dembos, DG NTA）配图，HTTP 200 image/jpeg，已人工目检确认（NTA 活动讲台照）。",
    "000496": "头像补齐(A2)：Premium Times 2025-06-13《Nigerian editors celebrate Vanguard publisher on 90th birthday》配图（文件名 Sam-Amuka-Pemu-1），HTTP 200 image/png，已人工目检确认（在世人物公开照）。",
    "000498": "头像补齐(A2)：ModernGhana 2011-11-20 讣告《Alex Ibru is dead》配图（alexibrufast.jpg），HTTP 200 image/jpeg，已人工目检确认（生前公开照）。",
    "000522": "头像补齐(A2)：Punch 2025-07-24《Meet APC's new national chairman Yilwatda Nentawe》档案照（File photo），HTTP 200 image/jpeg，已人工目检确认。",
    "000524": "头像补齐(A2)：Premium Times 2026-04-28《LP elects Nenadi Usman as substantive national chair》og:image（LP 党旗旁个人肖像），HTTP 200 image/jpeg，已人工目检确认。",
    "000584": "头像补齐(A2)：DAWN Commission（奥贡州政府机构）2023-05 追思文《Otunba Subomi Balogun, The Grand Master of FCMB dies at 89》配图，HTTP 200 image/jpeg，已人工目检确认（晚年传统服饰肖像）。",
}

MISSING_NOTE = {
    "000493": "头像补齐(A2)复核：未找到可验证单人照——FRCN 官方站（radionigeria.gov.ng/kapitalfm.gov.ng）对爬虫 403 或图片已删除（404），其余公开照仅见 Facebook 视频截帧与多人合影，按「宁缺勿错」保持缺失。",
    "000508": "头像补齐(A2)复核：Isa Abdullahi 为常见通用名，且尼日利亚陆军高级军官人事调整报道均无个人配图，无可靠直链，保持缺失。",
    "000512": "头像补齐(A2)复核：US Africa Command 官方照片（Wikimedia Commons）中其身影出现于多人会议合照（图说列有其名），但无法确认个人对应位置，不宜作头像，保持缺失。",
    "000515": "头像补齐(A2)复核：SERAP 官网 board/who-we-are 页无照片，CNBC Africa 人物页仅有视频缩略图，新闻报道以文字为主，无可靠单人照直链，保持缺失。",
    "000529": "头像补齐(A2)复核：公开照片仅见 Facebook/Instagram 社交媒体帖，无可靠媒体或官网直链，保持缺失。",
    "000534": "头像补齐(A2)复核：APGA 全国财务部长为低曝光职务，公开报道无配图，保持缺失。",
    "000779": "头像补齐(A2)复核：VON 报道原图已删除（404），Gazette/US AFRICAM 图片均为多人拼图或合照无法定位个人，无可靠单人官方照直链，保持缺失。",
}

for suffix, url in FILL.items():
    pid = "NG-PERSON-" + suffix
    d = json.load(open(BASE + pid + ".json", encoding="utf-8"))
    assert not d["profile"].get("source_url"), pid + " already has source_url"
    d["profile"]["source_url"] = url
    notes = d.get("collection_meta", {}).get("notes") or ""
    d.setdefault("collection_meta", {})["notes"] = notes + ("\n" if notes and not notes.endswith("\n") else "") + NOTE_FILL[suffix]
    json.dump(d, open(BASE + pid + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(BASE + pid + ".json", "a", encoding="utf-8").close()
    print("FILL", pid)

for suffix, note in MISSING_NOTE.items():
    pid = "NG-PERSON-" + suffix
    d = json.load(open(BASE + pid + ".json", encoding="utf-8"))
    assert not d["profile"].get("source_url"), pid + " unexpectedly has source_url"
    notes = d.get("collection_meta", {}).get("notes") or ""
    d.setdefault("collection_meta", {})["notes"] = notes + ("\n" if notes and not notes.endswith("\n") else "") + note
    json.dump(d, open(BASE + pid + ".json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(BASE + pid + ".json", "a", encoding="utf-8").close()
    print("NOTE", pid)
