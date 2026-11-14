"""Produce opinions for all 80 samples; never allocate IDs or rewrite source data."""
import csv,hashlib,json,pathlib,sys
from collections import Counter,defaultdict
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'output/_id_audit'
sys.stdout.reconfigure(encoding='utf-8')
D=json.loads((OUT/'registry_newid_80_context.json').read_text(encoding='utf-8'))
M=json.loads((OUT/'registry_newid_80_read_manifest.json').read_text(encoding='utf-8'))
V={}
def add(i,decision,name,cc,cat,reason,urls=()):
 assert i not in V
 V[i]={'decision':decision,'canonical_name':name,'entity_country':cc,'category':cat,'reason':reason,'external_sources':list(urls)}

add(1,'挂起','Shinhan Financial Group','KR','FIN','新韩金融集团与韩亚金融集团是不同主体，应拆出；但拟用KR-FIN-015已登记Bank of Korea（duplicate），严禁复用，先重排编号。')
add(2,'挂起','Ministry of Trade, Industry and Energy（历史主体）','KR','GOV','产业通商资源部与中小风险企业部不同，但2025年政府改组后名称及能源职权已变化；7条引用混合历史任职与现时监管。先确定旧部、继任部及历史任职粒度，不能整组迁到单一现职部委。',['https://english.motir.go.kr/kor/search?kwd=2025&site=main','https://www.me.go.kr/eng/web/board/read.do?boardId=1773240&boardMasterId=522&menuId=461'])
add(3,'分配','JoongAng Ilbo / 中央日报','KR','MEDIA','7处引用明确中央日报，现画像OhmyNews不是该报；可建立独立MEDIA身份。JTBC条目把报纸与中央集团股权混写，关系内容另核，不能随ID修复视为已证实。')
add(4,'挂起','Korea University / 高丽大学','KR','ACAD','不是UNIST，也不是Korea University of Science and Technology；需独立身份。但KR-ACAD-017已登记Incheon National University（duplicate），先重排编号。')
add(5,'挂起','Yonsei University / 延世大学','KR','ACAD','源为延世大学及其研究所，不是釜山大学；拟用KR-ACAD-018已登记Korea University of Science and Technology（duplicate），先重排编号。')
add(6,'挂起','KAIST / Korea Advanced Institute of Science and Technology','KR','ACAD','应与全量计划KR-ACAD-006下的英文全称合并为一个实体，不能发两个新ID；且KR-ACAD-019已登记KDI School（duplicate）。',['https://www.kaist.ac.kr/en/'])
add(7,'挂起','Hyundai Steel / 现代制铁','KR','CORP','独立钢铁企业，不是Samsung Engineering或Hyundai Motor；全量计划KR-CORP-022与本行KR-CORP-025下两条Hyundai Steel应共用一个主ID，不能分别发KR-CORP-033和034。源关系说明还混入HD现代/现代汽车集团错误，另核。')
add(8,'挂起','POSTECH / Pohang University of Science and Technology','KR','ACAD','不是全北大学或Korea University of Science and Technology；拟用KR-ACAD-020已登记Korea Institute of Science and Technology（duplicate），先重排编号。')
add(9,'分配','Ministry of Climate, Energy and Environment','KR','GOV','4条均明确韩国气候能源环境部，不能指向大法院。官方确认2025-10-01举行成立仪式，可建独立GOV身份；源“2025年9月新设”须另行校正为相应决定/生效日期。',['https://www.me.go.kr/eng/web/board/read.do?boardId=1773240&boardMasterId=522&menuId=461'])
add(10,'分配','Korea Hydro & Nuclear Power','KR','SOE','源明确韩国水力核电公司及KEPCO子公司，不是中小企业银行；SOE口径与经营性质相符，可独立分配。')
add(11,'挂起','Munhwa Broadcasting Corporation / MBC','KR','MEDIA','与Channel A不同，应拆出；但拟用KR-MEDIA-017已登记Newstapa（duplicate），不可复用。')
add(12,'挂起','Yonhap News Agency / 韩联社','KR','MEDIA','不是Newstapa，也不是阿塞拜疆Report或塔吉克Avesta；拟用KR-MEDIA-018已登记OhmyNews（duplicate），先重排编号。')
add(13,'挂起','LG Energy Solution','KR','CORP','源明确LG新能源，不是韩华；拟用KR-CORP-031已登记Korea Aerospace Industries（duplicate），先重排编号。')
add(14,'分配','Ministry of Culture, Sports and Tourism（韩国）','KR','GOV','引用为韩国文化体育观光部及部长任职，不是国土交通部；同名外国文化部均不是合并目标。历史任期另按当时部名保留。')
add(15,'分配','Ministry of Health and Welfare（韩国）','KR','GOV','源为韩国保健福祉部，不是国会；不能合并到其他国家卫生部，按KR/GOV建立独立身份。')
add(16,'分配','Republic of Korea Armed Forces','KR','MIL','明确韩国武装力量整体，不是国家情报院；MIL可保留。具体军法务官属哪军种不能仅凭总体名称擅自细化。')
add(17,'分配','Woori Bank / 友利银行','KR','FIN','源为友利金融集团旗下银行，不是Toss银行或友利金融控股本体，应独立FIN身份；泰国Islamic Bank候选是误匹配。')
add(18,'挂起','Ministry / Ministry of Patriots and Veterans Affairs（沿革待拆）','KR','GOV','源是黄基哲的国家报勋处长任职，英文却用升格后的Ministry；应先区分旧处和2023年升格的部及任期，不能直接按现名新建再整段改链。')
add(19,'分配','Ministry of Employment and Labor（韩国）','KR','GOV','源明确雇佣劳动部，不是宪法法院或澳大利亚工党，GOV类别适当。')
add(20,'分配','Korea Airports Corporation / 韩国空港公社','KR','SOE','官网明确state-owned company，保持SOE，不按Corporation词形改CORP；与仁川国际机场公社是不同运营主体。',['https://www.airport.co.kr/wwweng/cms/frCon/index.do?MENU_ID=50'])

add(21,'分配','Asamblea Legislativa del Distrito Federal（历史立法机构）','MX','GOV','18条为联邦区立法议会任职，不是农业改革与城市发展部。可建历史GOV身份；不得自动当作2018年后墨西哥城市议会，早期代表大会/立法议会沿革与年份需保持。')
add(22,'分配','Gobierno del Distrito Federal（历史政府）','MX','GOV','10条为1997—2008年前后的联邦区政府任职，不是INEGI；可建历史地方政府身份，与现墨西哥城政府的继承关系另表述。')
add(23,'分配','Gobierno del Estado de Veracruz','MX','GOV','源为韦拉克鲁斯州政府/州长及秘书，不是社会保险局，可分配地方政府GOV。')
add(24,'改类别后分配','Teléfonos de México / Telmex','MX','CORP','4条为Telmex董事、高管任职，不是国防部。按企业CORP重发号，不能继续MX-GOV-861；本次未实际发号。')
add(25,'挂起','Tlalpan：Delegación 与 Alcaldía 沿革','MX','GOV','4条混合2009—2017年Delegación时期任职与Alcaldía现称；实体类别GOV无争议，但需明确历史区政府与2018年后Alcaldía是否同一主ID，不能仅同地名批量迁移。')
add(26,'挂起','Valora Holding AG','CH','CORP','源明确瑞士零售控股，FEMSA持股不改变其法人所在地；现画像Liverpool错误。拟建MX-CORP-079前需先确定瑞士主实体登记位置与全球去重口径，不按母公司国别机械分配。',['https://valora.com/en/contact'])
add(27,'挂起','Southern Copper Corporation','US','CORP','公司自身披露Delaware注册、Phoenix总部；不是Televisa，也不能仅因Grupo México控股当墨西哥法人。先确定美国主实体编号/跨国存储策略。',['https://southerncoppercorp.com/eng/wp-content/uploads/sites/2/2026/04/8k260417.pdf'])
add(28,'分配','Gobierno del Estado de Campeche','MX','GOV','3条明确坎佩切州政府任职，不是联邦旅游部，GOV合适。')
add(29,'分配','El Norte（蒙特雷）','MX','MEDIA','源明确Grupo Reforma旗下蒙特雷报纸，不是Organización Editorial Mexicana；以地域和所属集团约束同名El Norte，建立独立MEDIA身份。')
add(30,'挂起','AUSJAL','区域网络／秘书处在墨西哥','NGO（建议）','是跨国耶稣会大学协会/网络，不是一所大学；建议NGO或先定教育联盟统一口径，不直接MX-ACAD-023。秘书处在墨西哥不等于网络法律注册地已确认，需明确主体及主ID归属。',['https://www.ausjal.org/en/contacto/'])
add(31,'分配','Procuraduría Federal del Consumidor / PROFECO','MX','GOV','引用明确联邦消费者保护机构及检察官任职，不是联邦议会；GOV合适。')
add(32,'分配','Centro Nacional de Control de Energía / CENACE','MX','GOV','引用明确电力调度及市场运行公共机构，不是最高法院；沿用公共行政实体GOV，不因能源运营词形当普通发电企业。')
add(33,'分配','Comisión Nacional Bancaria y de Valores / CNBV','MX','GOV','政府官网确认其为SHCP下属监管机关；保持GOV，不按“银行、证券”关键词改FIN。它与司法选举法院为不同主体。',['https://www.gob.mx/cnbv/que-hacemos'])
add(34,'分配','Gobierno del Estado de Puebla','MX','GOV','源为普埃布拉州政府及州长/福利副秘书任职，不是墨西哥总检察院，GOV合适。')
add(35,'分配','Mural（瓜达拉哈拉报纸）','MX','MEDIA','源明确Grupo Reforma旗下Mural，与El Universal不同，可建独立报纸身份。')
add(36,'分配','Siglo XXI Editores（墨西哥出版社）','MX','MEDIA','源明确1966年创建的墨西哥出版社，MEDIA可覆盖出版机构，不是El Financiero等现画像；出版社与FCE的successor关系表述本身另核。')
add(37,'分配','Conferencia del Episcopado Mexicano','MX','NGO','是墨西哥天主教主教团，非政府宗教组织；与Semillas基金会不同，NGO作为现有大类可用，子类标宗教团体。')
add(38,'分配','Universidad Tecmilenio','MX','ACAD','源明确Tec教育集团旗下大学，独立于UNAM、Tec de Monterrey及Milenio报纸；可独立ACAD，不能按Milenio词元误合并媒体。')
add(39,'挂起','TecSalud','MX','待定：医疗体系／教育医疗平台','源是Tec旗下含医学院及多家医院的医疗体系，不能当作另一所独立大学，也不是联邦卫生部。先定组织级医疗平台是否独立建档及类别，或拆到旗下具体院校/医院。')
add(40,'不分配','Southern Association of Colleges and Schools Commission on Colleges / SACSCOC','US','NGO（建议）','不分配所提MX-ACAD-017：美国教育认证组织不是墨西哥大学/政府机关；SACSCOC还应与更广的SACS区别。可另在美国非营利认证组织口径下核定主ID，并保留其认证关系。',['https://almanac.chea.org/accreditor/southern-association-colleges-and-schools-commission-colleges'])

add(41,'分配','NZ On Air / Broadcasting Commission','NZ','GOV','官方将其列为Autonomous Crown Entity、公共内容资助机构，保持GOV，不改MEDIA；不是Statistics NZ。资助媒体不等于自己是媒体运营商。',['https://www.mch.govt.nz/our-work/governance-and-monitoring/entities-overview'])
add(42,'分配','Civil Aviation Authority of New Zealand','NZ','GOV','5条明确新西兰民航安全监管机构，不是族裔社区部或其他国家民航局，可独立GOV。')
add(43,'分配','Commerce Commission（新西兰）','NZ','GOV','与第47行是同一市场监管机构，合计7处影子引用只建立一个主身份。可采用一个全新未占用GOV编号，但禁止分别创建NZ-GOV-153与174；美国商务部不是合并目标。',['https://www.publicservice.govt.nz/guidance/advising-on-organisational-form/what-do-the-question-1-answers-mean-for-organisational-form'])
add(44,'分配','Court of Appeal of New Zealand','NZ','GOV','3条明确新西兰上诉法院，不是海关或乌干达同名上诉法院，可独立GOV。')
add(45,'分配','Climate Change Commission（新西兰）','NZ','GOV','源为独立气候政策咨询委员会，不是监管部；GOV适当，不能把咨询职责误作一般企业。')
add(46,'挂起','High Performance Sport New Zealand Limited','NZ','GOV（公共体育实体；待定分类口径）','政府确认其为Sport NZ全资子公司，不能与现有Sport NZ画像合并。须统一Crown实体公司与SOE的类别口径；不能仅看到Limited改CORP，当前GOV方案暂缓确认。',['https://www.beehive.govt.nz/release/structural-change-confirmed-top-sport-nz-and-hpsnz'])
add(47,'不分配','Commerce Commission（新西兰；并入第43行身份）','NZ','GOV','不独立分配NZ-GOV-174：与第43行是同一机构；应与其共用最终主ID，现画像司法部及机器候选美国商务部都不对。两条引用后续须逐项改指共同主ID。')
add(48,'挂起','Auckland Council / Auckland City Council（需分开）','NZ','GOV','2处分别是现Auckland Council与Goldsmith在2007—2010年任职的旧Auckland City Council；2010年重组不是单纯译名差异。应分两个历史身份，不能整组迁到一个新ID。',['https://at.govt.nz/media/imported/4827/AT_ACC_Policy_Vol3Final.pdf'])
add(49,'分配','New Zealand Special Air Service / NZSAS','NZ','MIL','源为NZSAS特种部队，不是GCSB；MIL合适，不能把情报合作关系当身份等同。')
add(50,'分配','National Council of Women of New Zealand','NZ','NGO','官网明确非营利注册慈善团体，保留NGO，不按“委员会”改GOV；与Graeme Dingle Foundation不是同一慈善组织。',['https://www.ncwnz.org.nz/our-people'])
add(51,'挂起','Progressive Coalition / Progressive Party（Jim Anderton，新西兰历史组织）','NZ','PARTY','源明确Jim Anderton在2002年的联盟，机器却建议合并韩国Progressive Party，属于跨国误匹配；原计划新ID为空。还需区分联盟与后续Anderton政党沿革，再生成新西兰PARTY主ID。')
add(52,'不分配','Geological Survey of Japan / GSJ','JP','ACAD（研究机构；需区分历史本体与现AIST内部域）','不分配NZ-ACAD-021：引用明确日本GSJ，不是新西兰大学或日本国交省。官网说明现GSJ为AIST研究领域，先定部门/历史机构粒度，再在日本口径分配或建立部门关系。',['https://www.gsj.jp/en/about/greeting.html','https://unit.aist.go.jp/gsc/index_en.html'])
add(53,'不分配','Intuit Inc.','US','CORP','不分配NZ-CORP-068：源明确美国QuickBooks开发商，官网总部在加州Mountain View；与Fletcher Building不同。应先核美国主ID，不能按引用方国别创建新西兰副本。',['https://www.intuit.com/company/locations/'])
add(54,'不分配','Groupe Lactalis','FR','CORP','不分配NZ-CORP-070：源明确法国乳业集团，官网法律声明注册办公室为Laval法国；海外收购不使其变成新西兰法人。应明确法国实体登记方案。',['https://www.lactalis.com/en/legal'])
add(55,'不分配','Vocus Group Limited','AU','CORP','不分配NZ-CORP-071：源明确澳大利亚集团，官网隐私声明给出澳洲ABN；不要与历史新西兰运营公司/品牌混用。应先在澳大利亚口径确认主ID。',['https://www.vocus.com.au/privacy-policy'])
add(56,'挂起','Macquarie Asset Management / MAM','AU（集团业务）','FIN（建议）','源为麦格理资产管理业务中的高管任职；现有AU-FIN-007是集团母体，不能直接当成同一具体雇主。NZ-CORP-077的国别与类别都需重定，同时明确业务分部是否独立实体、实际雇主法人。',['https://www.macquarie.com/ch/en/about/company.html'])
add(57,'分配','Synlait Milk Limited','NZ','CORP','源明确新西兰Synlait乳制品加工企业，不是EBOS或a2 Milk；可建独立CORP身份，代工/持股关系不等同实体。')
add(58,'分配','Finance Now Limited','NZ','FIN','源为Finance Now董事任职，金融业务实体，不是金融市场管理局或澳洲财政部，FIN可用。')
add(59,'分配','Creative New Zealand / Arts Council of New Zealand Toi Aotearoa','NZ','GOV','官方将其列为Autonomous Crown Entity，公共艺术资助实体，GOV合适，不是总理及内阁部。',['https://www.mch.govt.nz/our-work/governance-and-monitoring/entities-overview'])
add(60,'分配','Heritage New Zealand Pouhere Taonga','NZ','GOV','源明确本国法定遗产保护机构，不是外交贸易部或美国Heritage Foundation，保持GOV公共机构口径。')

add(61,'分配','Sumitomo Mitsui Banking Corporation / SMBC','JP','FIN','19处源明确三井住友银行，不能指邮贮银行或三井住友金融集团SMFG；应独立FIN。SMFG子公司关系应保留，不能以集团代替银行。')
add(62,'分配','SMBC Nikko Securities','JP','FIN','源为SMBC日兴证券及其高管任职，不是Resona Holdings；证券公司FIN合适。')
add(63,'分配','中道改革連合','JP','PARTY','源明确2026年成立的新政党，不是自民党；可建立历史/现存政党身份，具体存续状态与2026年后续变动另核，不用现任职标签覆盖早期任职。',['https://cdp-japan.jp/about/activity_plan_fy2026'])
add(64,'分配','National Institutes for Quantum Science and Technology / QST','JP','ACAD','源为量子科学技术研究开发机构及其研究管理任职，不是名古屋大学；按核心科研职能ACAD建国立科研机构身份。')
add(65,'分配','Japan Society for the Promotion of Science / JSPS','JP','GOV','官网定义科学资助机构，不是外务省；保留公共资助机构GOV口径，与直接从事研究的ACAD研究所区分。',['https://www.jsps.go.jp/english/e-aboutus/index.html'])
add(66,'分配','National Institute of Advanced Industrial Science and Technology / AIST','JP','ACAD','源为产总研科研法人及研究中心任职，不是大阪大学；核心科研职能用ACAD，政府主管关系不意味着它与主管省是同一主体。')
add(67,'改类别后分配','RIKEN / 理化学研究所','JP','ACAD','官方明确国家综合研究机构。应按与AIST、QST一致的科研机构口径使用ACAD，而不是复制旧冲突ID类别GOV；历史机构沿革可写画像中，不与内阁府合并。',['https://www.riken.jp/en/about/'])
add(68,'分配','Japan Science and Technology Agency / JST','JP','GOV','源为科技振兴与资助机构，不是法务省；保留公共政策/资助执行机构GOV口径，不能仅因科学技术字样归为大学或具体实验室。',['https://www.jst.go.jp/kisoken/evaluation/kokusai/kokusai_vol5/houkoku_jp_en.pdf'])
add(69,'挂起','Japan Investment Corporation / JIC 与 INCJ（须区分）','JP','FIN（拟议；政府基金与SOE规则需统一）','中文产业革新投资机构/日文産業革新投資機構及横尾敬介任职指JIC，缩写却混入INCJ；2018年改组后两者不是可随意互换的名称。先按每处源文确认实体，再定FIN/SOE分类，不仅把GOV换FIN就执行。',['https://www.j-ic.co.jp/en/news/20260423-jic-pressrelease-en','https://www.incj.co.jp/newsroom/INCJ_20181211.pdf'])
add(70,'分配','独立行政法人情報処理推進機構 / IPA','JP','GOV','日本IT政策执行机构，与阿尔及利亚Pasteur Institute无关。拒绝原review_cross_country合并目标，允许建立独立日本GOV身份；原建议新ID为空，必须用修正后的分配器另生成。2026年英文品牌变更不改变日文法人名称。',['https://www.ipa.go.jp/about/disclosure/teikyo/soshiki.html','https://www.ipa.go.jp/pressrelease/2026/press20260605-2.html'])
add(71,'分配','Tokyo Medical and Dental University / TMDU（历史大学）','JP','ACAD','2024年10月与东京工业大学合并成立Science Tokyo；可为此前TMDU任职建立历史ACAD身份，不能合并到防卫大学校，也不把历史主体直接抹成继任大学。',['https://www.isct.ac.jp/en/news/kk3b39ld4qtx'])
add(72,'分配','Daihatsu Motor / 大发工业','JP','CORP','丰田的子公司和董事任职明确指大发，不是丰田母公司；独立CORP身份适当。')
add(73,'分配','Woven by Toyota','JP','CORP','明确丰田旗下软件公司，不是NTT或丰田母体；可以独立CORP，2021年任职与后续更名日期须另核沿革。')
add(74,'分配','Sony Honda Mobility','JP','CORP','索尼与本田合资公司，独立于Fast Retailing或Honda母体，可建立独立CORP；两条业务计划状态彼此不一致，需另核，不影响主体分离。')
add(75,'分配','Japan Aerospace Exploration Agency / JAXA','JP','GOV','源为日本国家航天机构，不能指总务省；保留国家航天机构GOV口径，所属研究所另用组织/部门关系区分。')
add(76,'分配','Urban Renaissance Agency / UR都市機構','JP','GOV','源明确城市再生与住宅供应独立行政法人，不是会计检查院，GOV公共执行机构口径可用。')
add(77,'分配','Japan International Broadcasting / 日本国際放送','JP','MEDIA','源明确NHK持股的独立广播运营公司及其董事任职，不是NHK母体本身；应独立MEDIA并保留股权关系。')
add(78,'分配','Japan Federation of Bar Associations / 日本弁護士連合会','JP','NGO','全国律师职业自治组织，不是World Vision Japan；NGO现有大类可用，标专业团体，不能因法定入会义务直接当政府机关。')
add(79,'分配','National Agriculture and Food Research Organization / NARO（日本）','JP','ACAD','日本官网确认名称与缩写，不能因英文近名并到乌干达National Agricultural Research Organisation。拒绝原跨国合并目标；保持ACAD，原新ID为空，须另生成有效日本编号。',['https://www.naro.go.jp/introduction/profile.html','https://www.naro.go.jp/english/'])
add(80,'分配','NLI Research Institute / ニッセイ基礎研究所','JP','ACAD','源明确日本生命旗下经济保险研究机构，不是东京大学；按研究机构ACAD口径可建独立身份。企业所有制与科研类别分别记录，不把子机构直接合并到日本生命。')

V[61]['reason']+=' 19处中4处起始于2001年成立前（1985、1989、1991、1997），必须分别核实三井/樱花等前身并拆段，不能因主体允许新建就整组迁移。'
V[61]['external_sources']=['https://www.smbc.co.jp/global/aboutus/profile/history.html']
V[62]['reason']+=' 其中2005—2023年的长段经历跨越旧名及重组，迁移引用前须核对当时证券公司沿革；主体新建建议不授权整段自动改链。'
V[9]['external_sources'].append('https://niwdc.me.go.kr/eng/web/board/read.do?boardId=1818710&boardMasterId=523&menuId=460')

assert set(V)==set(range(1,81))
changed=[p for p,h in M.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed, f'Source files changed: {changed[:5]}'
registered=defaultdict(list)
for path in M:
 if path.endswith('id_registry.json'):
  data=json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
  for e in (data.get('registry') or [])+(data.get('person_registry') or []):
   if e.get('person_id') and e.get('org_id'):continue
   eid=e.get('person_id') or e.get('org_id')
   if eid:registered[eid].append({'file':path,'entry':e})
P=list(csv.DictReader((OUT/'registry_dedupe_plan_v2.csv').open(encoding='utf-8-sig')))
reserved=[]
for p in P:
 if p['action']=='assign_new_id' and p['new_id'] in registered:
  reserved.append({'plan':p,'prior_registry_entries':registered[p['new_id']]})
records=[];proof=[]
for x in D:
 i=x['review_row'];v=V[i];r=dict(x['row']);eid=r['建议新ID'];used=registered.get(eid,[]) if eid else []
 if used:assert v['decision']=='挂起'
 matching=[q for q in x['all_current_collision_references'] if q['matches_shadow_heuristic']]
 r['复核结论']=v['decision'];r['备注']=v['reason']+' 仅为助手复核意见，不是执行授权。'
 r.update({'复核序号':i,'规范实体建议':v['canonical_name'],'实体国别建议':v['entity_country'],'类别建议':v['category'],
 '建议新ID是否曾登记':'已登记，禁止复用' if used else ('原计划未给编号' if not eid else '当前注册表未见登记；执行时仍须重查'),
 '既往编号身份':json.dumps(used,ensure_ascii=False,separators=(',',':')) if used else '',
 '对应计划动作':' ; '.join(p['action'] for p in x['plan']),
 '原计划合并目标':' ; '.join(p['target'] for p in x['plan'] if p['target']),
 '引用证据位置':' ; '.join(q['file']+'#'+q['pointer'] for q in matching),
 '本轮匹配引用数':len(matching),'参考来源':' ; '.join(v['external_sources']),
 '证据范围':'本地注册项/现画像/原引用上下文复核'+('；疑难点查官方或行业认证来源' if v['external_sources'] else '；未逐项重查外网事实'),
 '执行授权':'否；不写入新ID、不改引用'})
 records.append(r);proof.append({'review_row':i,**v,'proposed_id':eid,'proposed_id_prior_registry_entries':used,'references':matching})
fields=list(records[0])
for filename,items in [('registry_newid_sample_80_reviewed.csv',records),('registry_newid_sample_80_attention.csv',[r for r in records if r['复核结论']!='分配'])]:
 with (OUT/filename).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(items)
summary={'review_only':True,'execution_authorized':False,'total':80,'by_conclusion':dict(Counter(r['复核结论'] for r in records)),
 'by_country':{c:dict(Counter(r['复核结论'] for r in records if r['国家']==c)) for c in ['KR','MX','NZ','JP']},
 'machine_said_assign_but_not_pass':[r['复核序号'] for r in records if r['机器建议']=='可分配' and r['复核结论']!='分配'],
 'sample_reserved_ids':[r['复核序号'] for r in records if r['建议新ID是否曾登记']=='已登记，禁止复用'],
 'global_planned_newids':sum(p['action']=='assign_new_id' for p in P),'global_reserved_ids_count':len(reserved),
 'sample_only_no_extrapolation':True,'files_hash_checked':len(M),'changed_source_files':changed,
 'empty_planned_id_rows':[r['复核序号'] for r in records if not r['建议新ID']],
 'input_csv_sha256':M[str(pathlib.Path('output/_id_audit/registry_newid_sample_80.csv'))]}
(OUT/'registry_newid_80_review_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'registry_newid_80_review_decisions.json').write_text(json.dumps({'review_only':True,'execution_authorized':False,'rows':proof},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'registry_newid_reserved_14.json').write_text(json.dumps({'review_only':True,'scope':'983 planned identifiers checked against all statuses in latest registries; not a review of all983 identities','rows':reserved},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
reserved_csv=[]
for item in reserved:
 p=item['plan']
 reserved_csv.append({'原冲突ID':p['collision_id'],'拟分配身份':p['shadow'],'已被使用的建议新ID':p['new_id'],
 '既往登记身份':' ; '.join(e['entry'].get('name','') for e in item['prior_registry_entries']),
 '既往状态':' ; '.join(e['entry'].get('status','') for e in item['prior_registry_entries']),
 '依据文件':' ; '.join(e['file'] for e in item['prior_registry_entries']),'建议':'禁止复用；先按全部历史编号重排候选，不改既有画像ID','执行授权':'否'})
with (OUT/'registry_newid_reserved_14.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(reserved_csv[0]));w.writeheader();w.writerows(reserved_csv)
report=['# 80条新ID抽查复核','',
 '日期：2026-11-13。已逐条复核全部80条（KR/MX/NZ/JP各20）。本轮仅生成助手意见，未分配任何新ID，未更改registry、原画像、引用、索引和头像。原始80条CSV与全量计划CSV保持不变。用户的“继续”按继续完成本轮复核理解，不视为ID变更授权。','',
 '结论：不能采用“其余按可分配执行”。原机器判断71条可分配，其中24条本轮未直接通过。并且候选ID分配器忽略了非活动条目占用的历史编号，存在再次制造身份错乱的风险。','',
 '|复核意见|数量|含义|','|---|---:|---|',
 '|分配|51|独立身份/类别原则可用；编号仍须用修正后的分配器重新确认，引用迁移另核|',
 '|改类别后分配|2|第24条Telmex改CORP；第67条RIKEN按科研机构ACAD口径|',
 '|不分配|6|否定本行所提新ID或重复新身份，并不否认机构存在|',
 '|挂起|21|历史编号占用、重复影子、跨国主体、沿革或组织粒度未解决|','',
 '“分配”是复核建议，不等于允许立即写入本行建议编号，也不是对全组引用及所有任职/股权内容的事实背书。分类是本项目当前大类下的建议：公共资助/行政执行机构用GOV，核心科研机构用ACAD，国有经营企业用SOE；不同于仅按法律形式或名称关键词分类。','',
 '## 1. 必须先修的编号问题','',
 '样本8条（1、4、5、6、8、11、12、13）的建议新ID已在注册表出现，状态均为duplicate，且旧主体与拟赋予的新主体不同。它们全部标为挂起。扩大到全量983个assign_new_id计划只检查编号占用，发现14个历史编号重用，均在韩国。这不是对983个实体完成了复核。','',
 '|拟分配ID|拟分配身份|该ID既往登记身份|','|---|---|---|']
for r in reserved_csv:
 report.append(f"|{r['已被使用的建议新ID']}|{r['拟分配身份']}|{r['既往登记身份']}|")
report += ['',
 '原因可直接在scripts_tmp/registry_dedupe_plan_v2.py复现：maxseq只从现画像和active注册项计算，而active排除了duplicate等状态。编号不应因条目失活而变成空号。修正时须纳入活动/非活动/归档/合并/已预留编号，并在写入前再次检查；本轮没有修改分配器或重排编号。','',
 '## 2. 同一个实体被建议发多个ID','',
 '- 第6条KAIST与全量计划KR-ACAD-006下Korea Advanced Institute of Science and Technology是同一高校，应合为一个身份，不能分别发019和021。[KAIST官网历史全名](https://www.kaist.ac.kr/eng/)。',
 '- 第7条Hyundai Steel与KR-CORP-022下同名影子是同一钢铁公司，不能分别发033、034。与Hyundai Motor或HD Hyundai集团也不等同。',
 '- 第43和47条Commerce Commission是同一新西兰监管机构，合计7处引用。第43条可作为共同主身份候选，第47条标不分配，不能同时发153和174。','',
 '## 3. 机器类别提示中4条应维持原类别','',
 '|样本行|机构|复核类别|依据|','|---|---|---|',
 '|20|Korea Airports Corporation|SOE|[官网明确state-owned company](https://www.airport.co.kr/wwweng/cms/frCon/index.do?MENU_ID=50)|',
 '|33|CNBV|GOV|[墨西哥政府确认SHCP下属监管机关](https://www.gob.mx/cnbv/que-hacemos)|',
 '|41|NZ On Air|GOV|[新西兰政府列为自主Crown实体及内容资助机构](https://www.mch.govt.nz/our-work/governance-and-monitoring/entities-overview)|',
 '|50|National Council of Women NZ|NGO|[官网确认非营利注册慈善团体](https://www.ncwnz.org.nz/our-people)|','',
 '第24条Telmex确需由GOV改CORP。第69条INCJ/JIC不能只改FIN：引用把2018年后JIC与INCJ混写，需先区分具体主体及FIN/SOE口径。另有机器未提示的第67条RIKEN，建议与AIST/QST统一按ACAD科研机构处理。[RIKEN官方定义](https://www.riken.jp/en/about/)、[JIC官网](https://www.j-ic.co.jp/en/news/20260423-jic-pressrelease-en)、[INCJ官方明确为JIC子公司](https://www.incj.co.jp/newsroom/INCJ_20181211.pdf)。','',
 '## 4. 未被机器充分识别的国别与粒度问题','',
 '- 第26条Valora为瑞士公司，第27条Southern Copper为美国注册/总部公司。母公司来自墨西哥，不等于应新建另一个墨西哥身份；均挂起确认登记策略。[Valora联系页](https://valora.com/en/contact)、[Southern Copper公司备案](https://southerncoppercorp.com/eng/wp-content/uploads/sites/2/2026/04/8k260417.pdf)。',
 '- 第53—55条Intuit、Lactalis、Vocus明确分别为美国、法国、澳大利亚集团，不同意照提案在NZ下直接分配；跨国存储策略可讨论，但不能复制出第二个“新西兰总部”身份。[Intuit总部](https://www.intuit.com/company/locations/)、[Lactalis法定地址](https://www.lactalis.com/en/legal)、[Vocus澳洲法人](https://www.vocus.com.au/privacy-policy)。',
 '- 第40条SACSCOC不应按MX-ACAD直接建“美国南部院校协会”，需明确美国教育认证组织口径，并与SACS区分；第30条AUSJAL是跨国高校协会，不是一所大学，秘书处位置和法律注册地也需区分。',
 '- 第52条GSJ是日本地质科研机构、当前AIST内部研究领域，不是新西兰大学或日本国交省。第56条Macquarie Asset Management是澳大利亚金融集团业务，不能直接归到NZ-CORP或直接以集团代替实际雇主。',
 '- 第48条同组两个引用分别是现Auckland Council和2007—2010年的Auckland City Council，需分开；第25条也涉及Tlalpan旧Delegación与Alcaldía。第2、18、69条的部委/基金前后身需按日期核定。',
 '- 第61条SMBC可以建立独立银行身份，但19条引用中4条开始于2001年成立前，须拆历史前身或核实当时雇主；不能整组迁移。第62条也有跨证券公司旧名/重组的长段任职。[SMBC官方沿革](https://www.smbc.co.jp/global/aboutus/profile/history.html)。','',
 '## 5. 三条原计划未给新编号','',
 '第51条机器拟合并韩国Progressive Party，但源明确新西兰Jim Anderton政党/联盟，标挂起；第70条日本IPA误候选为阿尔及利亚Pasteur Institute，第79条日本NARO误候选为乌干达同名研究机构。后两条日本独立身份可以分配，但必须拒绝原跨国合并目标，并重新生成未占用编号。三条均不能把空建议ID当成已通过的执行计划。[IPA官方机构定义](https://www.ipa.go.jp/about/disclosure/teikyo/soshiki.html)、[NARO官方名称](https://www.naro.go.jp/introduction/profile.html)。','',
 '## 6. 复核范围及验证','',
 f'- 读取最新国别数据集的注册表、画像和全部相关引用，证据快照保留原条目、指针、候选画像、同名注册项；共{len(M):,}个输入文件通过SHA256未变校验。',
 '- 样本由各国按引用数排序取前20，并非随机抽样，不能估计全库错误率，也不能把53条原则可用外推为983条全部可执行。',
 '- 独立主体判断结合本地完整引用上下文，疑难分类/国别/沿革查询了官方和行业认证来源；没有声称80行的所有关系、日期、任职和股权事实均独立外网复证。',
 '- 候选搜索沿用原有模糊匹配只作召回，没有自动采纳其结果；例如Korea University→UST、IPA→阿尔及利亚研究所、NARO→乌干达机构已人工排除。',
 '- 现画像自己的ID、图片profile字段、头像文件、registry、原始抽样CSV及全量分配计划均未修改。','',
 '## 交付及建议顺序','',
 '1. `registry_newid_sample_80_reviewed.csv`：80行完整意见、类别/国别建议、编号占用和引用证据位置。',
 '2. `registry_newid_sample_80_attention.csv`：29行非直接分配意见，方便优先讨论。',
 '3. `registry_newid_reserved_14.csv`：全量983候选中14个已用历史编号证据。',
 '4. `registry_newid_80_review_decisions.json` / `registry_newid_80_review_summary.json`：带review_only和未授权标志的结构化结果。',
 '5. 先修编号分配器，再做跨collision_id的影子实体去重，接着明确外国主体、历史实体及业务分部粒度；最后才重新生成执行计划。51条“分配”及2条“改类别后分配”也应在新计划中逐项复验，而不是直接读助手CSV批量执行。','']
(ROOT/'docs/registry-newid-sample-80-review.md').write_text('\n'.join(report),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
