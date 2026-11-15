# -*- coding: utf-8 -*-
"""Fill name_zh for GN/NG orgs from a curated mapping (common names only)."""
import glob, json, os
BASE='D:/ai-workspace/apec-osint-tool'
ZH={
 'Abia State University, Uturu':'阿比亚州立大学',
 'Adeyemi College of Education':'阿德耶米教育学院',
 'Adamu Tafawa Balewa College of Education, Kangere':'阿达姆·塔法瓦·巴莱瓦教育学院（康盖雷）',
 'Adesina College of Education':'阿德西纳教育学院',
 'African University of Science & Technology, Abuja':'非洲科学技术大学（阿布贾）',
 'Adamawa State College of Education Hong':'阿达马瓦州教育学院（洪）',
 'Achievers University':'艾奇弗斯大学',
 'Abia State College of Education (Tech), Arochukwu':'阿比亚州技术教育学院（阿罗丘克武）',
 'Paystack':'Paystack（支付科技公司）',
 'National Network Newspaper':'国民网络报',
 'Blueprint Newspaper':'蓝图报',
 'National Mirror':'国民镜报',
 'Nigerian Tribune':'尼日利亚论坛报',
 'Nigerian Entertainment Today':'尼日利亚今日娱乐报',
 'Idoma Voice Newspaper':'伊多马之声报',
 'The Triumph':'凯旋报',
 'Next Newspaper':'下一报表',
 'Ripples Nigeria':'尼日利亚涟漪报',
 'TheNiche':'利基报',
 'Business Hallmark':'商业印记报',
 'Naija News':'奈加新闻',
 'Stears News':'斯蒂尔斯新闻',
 'Barau F.C.':'巴劳足球俱乐部',
 'Ifeanyi Ubah F.C.':'伊费安尼·乌巴足球俱乐部',
 'Ibom Youths FC':'伊博姆青年足球俱乐部',
 'United Nigeria Airlines Limited':'联合尼日利亚航空有限公司',
 'African Trans Air':'非洲跨洲航空',
 'Freedom Air Services':'自由航空服务公司',
 'Merchant Express Aviation':'商人快运航空',
 'Premium Air Shuttle':' premium 航空穿梭公司',
 'Dangote Refinery':'丹格特炼油厂',
 'Airtel Networks Limited':'Airtel 尼日利亚电信',
 'Globacom':'Globacom 电信（Glo）',
 'Seplat Energy Plc':'塞普拉特能源公司',
 'First City Monument Bank':'第一城市纪念碑银行',
 'Jaiz Bank':'贾伊兹银行',
 'Federal Ministry of Livestock Development':'联邦畜牧业发展部',
 'Channels Television':'频道电视台',
 'Premium Times':'优质时报',
 'Young Progressive Party':'青年进步党',
 'Accord':'协同党',
}
n=0
for f in glob.glob(f'{BASE}/output/ng/2026-07-29/orgs/*.json')+glob.glob(f'{BASE}/output/ng/2026-11-10/orgs/*.json'):
    if os.path.basename(f).startswith('_'): continue
    d=json.load(open(f,encoding='utf-8')); bi=d.get('basic_info') or {}
    if bi.get('name_zh'): continue
    en=bi.get('name_en') or bi.get('name_original')
    if en in ZH:
        bi['name_zh']=ZH[en]
        json.dump(d,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
        n+=1
print('filled',n)
