"""Review second 80-row sample. Outputs opinions and evidence only."""
import csv,hashlib,json,pathlib,re,sys
from collections import Counter,defaultdict
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'output/_id_audit'
sys.stdout.reconfigure(encoding='utf-8')
D=json.loads((OUT/'registry_newid_next80_context.json').read_text(encoding='utf-8'))
M=json.loads((OUT/'registry_newid_next80_read_manifest.json').read_text(encoding='utf-8'))
def read(p):
 raw=p.read_bytes();M[p.relative_to(ROOT).as_posix()]=hashlib.sha256(raw).hexdigest()
 return json.loads(raw.decode('utf-8-sig'))
V={}
def add(i,decision,cc,cat,reason,urls=()):
 assert i not in V
 V[i]={'conclusion':decision,'country':cc,'category':cat,'reason':reason,'external_sources':list(urls)}

add(1,'挂起','KR','ACAD','汉阳大学可独立于KDI School，但另有KR-GOV-176汉阳大学、KR-GOV-714汉阳大学校注册项；先归一为一个高校身份，不单独照本行发号。无当前引用不能代替实体去重。',['https://www.hanyang.ac.kr/web/eng/'])
add(2,'挂起','KR','ACAD','西江大学不是KIST；KR-GOV-695另有同一大学注册项，应合一。KR-GOV-321学生会、455法学院、753社会科学研究所不能仅因包含校名一并合并。',['https://summer.sogang.ac.kr/About/AboutSogangUniversity'])
add(3,'分配','KR','CORP','Lotte Group与SK Energy不同，可建立集团级CORP身份；不要合并到Lotte Insurance或把模糊匹配得到的人物当组织。当前无引用，优先级低于有引用项。')
add(4,'挂起','KR','CORP','Amorepacific是独立企业，但当前KR-CORP-027实际画像为SK Innovation，registry却另有Amorepacific的profiled记录。上轮将KR-CORP-030影子标merged_into=KR-CORP-036，而036尚未注册；该036已被另两处引用用来表示POSCO DX和Korail Logis，不能再赋给Amorepacific。先修合并闭合性、引用编号占用和registry标签矛盾。')
add(5,'挂起','KR','GOV','农林畜产食品部不是海洋水产部；但KR-GOV-112/113已登记同一部，应先并为一个身份。外国同名农业部及仅词元相近的韩国总务处都不可作为目标。',['https://www.mafra.go.kr/english/engIndex.do'])
add(6,'挂起','KR（待核）','CORP（拟议）','株式会社/㈜表明企业，GOV显然不合适；IBF拉丁缩写与아이비피转写还不一致。无原引用、无地址/法人号等证据，不足以确认具体公司后按CORP发号。')
add(7,'不分配','KR','不适用：未指明具体办公室','“国会议员辅佐官室”没有议员姓名、届次、地点，是职位/办公室通名，不是已识别组织。保留原登记待清理，不为该通名建独立GOV身份。')
add(8,'挂起','KR','GOV','总统秘书室有KR-GOV-121/192/691等同名或近名注册项，另有金大中政府任期限定项。先定机构持续身份与任期部门的区别再合并，不重复发新的GOV号；现画像空不代表原ID第一条legacy记录是已证实owner。')
add(9,'挂起','KR','PARTY（确定需改类）','自由韩国党是历史政党，不能建GOV；KR-GOV-092也登记相同政党，先去重并核与后继政党关系，再只建一个历史PARTY身份。')
add(10,'挂起','KR','GOV（临时过渡机构）','总统当选人秘书室为过渡机构，需明确哪一届当选人及任期；KR-GOV-382另有同名注册项。不是可跨总统任期随意视作单一常设部门的名称。')
add(11,'挂起','KR','ACAD（大学内设研究所）','庆北大学基础医学研究所不是大学本体，也不是陆军第三师团。需确认是否独立建研究所画像，或建大学部门；不能直接合到KR-ACAD-004，也不能按GOV发号。')
add(12,'不分配','JP','ACAD（科研机构建议）','否定KR-GOV-1169方案：明确是日本NIHS，不是韩国机构；官网确认其从事医药食品等评价研究。先在日本主实体口径归一，不能根据引用登记分区创造韩国副本。',['https://www.nihs.go.jp/'])
add(13,'挂起','未知','待核','“地区合作研究中心”是通名，无原文、主管单位、地点或实际引用，无法确认实体或类别，不发号。')
add(14,'挂起','KR','待核：TechnoPark内部事业团','源为大邱TechnoPark的新技术事业团，而非整个园区或政府厅。无原引用，不足以判断独立主体、部门层级及存续期；先补机构沿革与主管关系。')
add(15,'挂起','KR','GOV','庆尚北道厅已有KR-GOV-732等重复登记；KR-GOV-381中文/韩文是庆尚北道，英文却写Gyeonggi（京畿道），需先纠正身份标签，不能按同名无差别合并。')
add(16,'分配','KR','GOV','大邱庆北经济自由区域厅为明确的区域管理机构，不同于原碰撞ID登记的政党；独立GOV身份原则可用。无当前引用，建档优先级低。')
add(17,'挂起','KR','GOV（咨询委员会；待核）','地方分权协议会名称具体但没有原引用及设立依据，需确认委员会是否单独建档、所属政府及任期；不能只因GOV编号可用即确认。')
add(18,'不分配','KR','不适用：考试资格/经历','“第23届行政高等考试合格”是个人考试经历，不是组织。应记教育/资格或履历备注，不分配GOV或其他组织ID；也不自动删除原登记。')
add(19,'挂起','KR','GOV','忠清北道厅另有KR-GOV-754（North Chungcheong Provincial Government），应先归为一个机构，不能重复发GOV新身份。')
add(20,'分配','KR','GOV','忠清北道阴城郡是明确的地方政府辖区/郡政府，不是文在寅竞选委员会；可按地方政府GOV独立登记，规范名应明确为郡政府，当前无引用。')

add(21,'挂起','MX','ACAD/NGO（网络口径待定）','源是墨西哥多所耶稣会大学组成的SUJ网络，不是单独大学。先与上一批AUSJAL统一教育系统/大学联盟分类和建档粒度，不直接把网络当一所学校。')
add(22,'不分配','US','ACAD','Georgetown是美国华盛顿的大学，源也明确美国；不按MX-ACAD-023建墨西哥副本。应在美国主实体口径去重后登记。',['https://www.georgetown.edu/about/'])
add(23,'不分配','MX','PERSON（身份已有；本行不是组织）','源是MX-PERSON-000114的work_experience[0]，把本人姓名写成organization。已有MX-PERSON-000102和114两份同名人物档案，不能再建组织或把自己当雇主。职位指SECIHTI，已有MX-GOV-033可作为组织修正候选；需同时修文字并核任期，不能仅将ID换成人物ID。')
add(24,'挂起','MX','ACAD/NGO（研究倡导机构）','INDESIG官网同时列学术研究、数字行动与政策倡导，主体存在；但不能仅因“研究所”就当大学/学术院校。需按智库/社会倡导机构统一类别口径再分配。',['https://www.indesig.org/quienes-somos/'])
add(25,'不分配','US','CORP','不按MX-CORP-062发号：Pemex条目明确Talos为美国油气公司。额外发现Grupo México条目混写América Móvil/Talos，但说明全部指Slim电信企业，不能按Talos关键词将该复合条目一起改走。应先拆/修复文字再单独判引用。')
add(26,'不分配','BR','CORP','源明确巴西Braskem集团，不是Walmex；否定按MX-CORP新建。还需区分巴西母集团与墨西哥Braskem Idesa合资主体，不能用供应项目所在地替代法人身份。')
add(27,'不分配','ES','CORP','源明确西班牙Iberdrola，不是FEMSA。否定MX-CORP方案，先核西班牙母集团与墨西哥地方子公司，按具体主体登记。')
add(28,'不分配','MX','PERSON（身份已有；本行不是组织）','源是MX-PERSON-000119的work_experience[0]，把本人姓名当雇主。已有MX-PERSON-000107及119同名档案，不能建CORP或把org_id指到人物；董事长雇主可核FEMSA（MX-CORP-003），但需同时改组织文字、核职务和期间，并处理重复人物档案。')
add(29,'分配','MX','CORP','源明确Telcel / Radiomóvil Dipsa为América Móvil墨西哥移动运营商，不是Grupo México或电信集团母体。可建立独立运营公司身份。')
add(30,'挂起','跨拉美多个国家','CORP（品牌/集团口径待定）','源明确Claro是多国统一品牌，单一名称不能确定国家法人；已有Claro Chile/Perú/Nicaragua画像，不能任选其一，也不能默认墨西哥法人。先明确品牌节点或具体运营公司。')
add(31,'挂起','MX','CORP（品牌/连锁体系；待定）','Bodega Aurrerá是Walmex零售连锁品牌，源用subsidiary但未给独立法人。先定品牌是否建组织画像、对应运营公司，而非只换成一个CORP编号。')
add(32,'挂起','MX','CORP（MVNO业务/品牌；待定）','标题写“Bait电商平台”，说明却是Walmex移动虚拟运营商；官方确认其为移动连接服务。先纠正文字及品牌/法律运营实体粒度，不能让新ID固化错误标题。',['https://walmex.mx/nosotros/ecosistema.html','https://www.walmartmexico.com/sala-de-prensa/2022/12/14/inaugura-walmart-de-mexico-y-centroamerica-los-primeros-centros-de-experiencia-bait'])
add(33,'分配','MX（集团登记口径；法律主体另核）','CORP','源明确Solistica物流业务，不是Grupo Elektra；可建集团级物流实体。其最新所有权、区域运营法人及FEMSA股权叙述需另核，ID复核不背书旧股东关系。')
add(34,'不分配','US','CORP','源明确ASARCO LLC为美国矿业公司，不是Grupo Lala。否定MX-CORP-084，按美国法人核主ID，母公司Grupo México国别不能覆盖子公司国别。')
add(35,'分配','MX','CORP','源明确Ferromex墨西哥铁路货运经营主体，不是Kimberly-Clark México。可以独立CORP；国名不意味着国有，股权比例另核。')
add(36,'不分配','MX','PERSON（关系对象需另核）','实际是MX-PERSON-000133父亲档案的person_relationships[1].person_id，说明写其子、Marea Rosa及反腐组织活动；影子却给父亲Laporte全名。不能新建CORP，也不能改回133造成自指；需识别儿子Claudio X. González Guajardo，现本国人物主名扫描未见该儿子的独立画像。')
add(37,'不分配','MX','PERSON（已有候选MX-PERSON-000134）','实际为父亲MX-PERSON-000133的儿子关系，person_id误用了CORP编号。儿子Pablo Roberto González Guajardo已有MX-PERSON-000134；应走人物改链复核，而不是建新组织。关系说明中的接任年份也有冲突，另核。')
add(38,'不分配','US','CORP','源明确Bimbo Bakeries USA为美国业务子公司，不是Grupo Bimbo母体或Soriana。否定墨西哥新ID方案，核美国经营主体后登记，不能直接合回母集团。')
add(39,'不分配','IT','FIN','源明确意大利Generali保险集团，不是BBVA México；不按MX-FIN新建。先核意大利母集团主ID及具体墨西哥合资保险公司的区别。')
add(40,'不分配','US','FIN（历史银行）','源明确美国得州Inter National Bank，不能指Banorte或任何含International/National的其他银行；不按MX-FIN发号。应核历史银行、后续出售及合并沿革，不能把历史持股表述当成现时子公司。')

add(41,'分配','NZ','GOV','明确Broadcasting Standards Authority公共广播内容监管机构，不是卫生部或媒体运营商，保持GOV；与资助机构NZ On Air也不同。')
add(42,'挂起','NZ','GOV（LINZ内部单位；待定）','源明确LINZ下属地理空间办公室；需确定办公室现/历史名称和部门建档口径，不能与LINZ本体自动合并，也不能把部门当独立法人。')
add(43,'分配','NZ','GOV（监管办公室，标parent=LINZ）','明确海外投资审查办公室，不是社会发展部或投资公司；可作为有明确行政职能的办公室节点，建档时必须记录隶属LINZ，不宣称其为独立法人。')
add(44,'不分配','NZ','不适用：法定职务','Surveyor-General是LINZ法定官员职位，源自己也明确为官员岗位。不能把职务新建为组织；应用岗位/部门或具体任职人物表示。',['https://www.linz.govt.nz/our-work/statutory-and-support-roles'])
add(45,'分配','NZ','GOV（已撤销历史机构）','可建历史Productivity Commission身份，不是教育审查办公室；财政部资料确认至2024-02-29运作，源“2024年1月撤销”错误。监管部官网明确其未取代委员会，原predecessor关系也需纠正，不能随ID通过而背书。',['https://www.treasury.govt.nz/publications/annual-report/new-zealand-productivity-commission-annual-report-1-july-2023-29-february-2024','https://www.regulation.govt.nz/news/building-up-from-establishment-phase/'])
add(46,'不分配','GB','GOV','枢密院司法委员会是位于伦敦的司法机构；历史承接新西兰上诉不使其成为新西兰机构。否定NZ-GOV-143，核英国主身份。')
add(47,'分配','NZ','GOV（历史机构）','源明确New Zealand Fire Service，2017年前消防机构；与癌症控制署或现FENZ不同。可保留独立历史身份，并用继承关系连接新机构。')
add(48,'分配','NZ','GOV（历史机构）','源明确National Rural Fire Authority及2017年整合，不能指新西兰最高法院，也不与FENZ主体直接等同；可建历史GOV身份。')
add(49,'分配','NZ','GOV','明确Sport Integrity Commission / Te Kahu Raunui独立公共机构，不是选举委员会，GOV类别与主体均可确认。',['https://sportintegrity.nz/news/sport-integrity-commission-te-kahu-raunui-opens-its-doors'])
add(50,'挂起','NZ','GOV（法定咨询组；待定）','源限定为Taumata Arowai下Te Puna毛利咨询小组，不是所有同名Te Puna机构；应先定咨询组是否独立组织建档及与董事会的层级关系。')
add(51,'挂起','NZ','GOV（政府品牌平台；待定）','New Zealand Story Group是政府国际品牌平台/跨机构项目，尚未确认独立行政机关或法人。需核管理主体后定组织/项目节点，不按“Group”或政府背景直接发GOV号。')
add(52,'挂起','NZ','待定：公共机构子公司CORP/SOE口径','源明确Qualmark New Zealand Limited为Tourism NZ旗下公司；不能因母机构为公共部门直接继承GOV。需核公司性质，并与上一批HPSNZ的Crown实体公司规则统一。')
add(53,'改类别后分配','NZ','ACAD','NZIST是职业高等教育机构/网络，不是政府部委。官方确认其为Te Pūkenga后名称、仍在过渡重组；按教育机构ACAD分配并标明历史及重组状态，不复用GOV提案号。',['https://www.tec.govt.nz/strategic-initiatives/vocational-education-system/delivering-vocational-education/new-zealand-institute-of-skills-and-technology','https://www.nzist.ac.nz/about/faqs'])
add(54,'分配','NZ','GOV（历史资格机构）','明确Universities Entrance Board是NZQA前身资格机构，不是海事局；可按历史公共考试资格管理机构GOV建档，不能仅因universities改为学校。')
add(55,'分配','NZ','GOV','明确独立法律改革咨询委员会，不是WorkSafe，可独立GOV；法律研究职能不等于大学或律师协会。')
add(56,'挂起','NZ','GOV（历史沿革待定）','源用Te Arawhiti旧名并描述毛利—王室关系职能；官方审计资料确认2025年更名、部分职能转移。须区分旧机构/继任机构及剩余职权，不能当当前机构直接分配后维持旧关系。',['https://ao.parliament.nz/2026/engagement-with-maori/part4.htm'])
add(57,'挂起','NZ','GOV（咨询委员会；待核）','NACEW为妇女就业咨询委员会，不能因名称含妇女与上一批NCWNZ慈善组织合并；需核本委员会存续时段、主管部门及组织级建档口径。')
add(58,'分配','NZ','GOV（行政业务机构，标parent=MBIE）','明确Immigration New Zealand，不是自然灾害委员会；可建移民行政业务机构节点，必须标隶属MBIE，不宣称为独立政府部。')
add(59,'挂起','NZ','GOV（CAA安保业务单元；待定）','政府目录明确AvSec是CAA的一部分。先定独立服务单元还是CAA部门节点，不能把它当另一家航空监管法人，也不能直接用CAA取代具体安保服务引用。',['https://www.govt.nz/organisations/aviation-security-service/'])
add(60,'不分配','NZ','不适用：多个组织集合','CDEM Groups指16个地区应急管理小组，不是单一机构。应选具体地区或保留集合关系，不创建一个虚构全国“民防应急管理小组”画像。',['https://www.civildefence.govt.nz/guidance-training/exercises/cdem-exercise-programme'])

add(61,'分配','JP','ACAD','RIETI经济产业政策研究所是明确科研智库机构，不是东京工业大学；按科研职能ACAD建独立身份，主管省关系单独表示。')
add(62,'分配','JP','ACAD','国立环境研究所是环境科研机构，不是东北大学，可独立ACAD并标主管/资助关系。')
add(63,'分配','JP','ACAD','大阪公立大学为明确大学，不是北海道大学或大阪大学；不能因大阪校名相近而合并。')
add(64,'不分配','CN','ACAD','源为与东京工大合作的中国大陆Tsinghua University；不能建JP-ACAD-035，也不能误连台湾National Tsing Hua University。已有多个未建画像的Tsinghua注册项，需先全球归一，不能再多建一个日本副本。')
add(65,'分配','JP','ACAD','明确岐阜大学，不是早稻田大学；同属东海国立大学机构并不意味着等同名古屋大学或该运营法人。')
add(66,'分配','JP','ACAD','明确九州工业大学，不是庆应义塾或九州大学；可独立ACAD。')
add(67,'分配','JP','CORP','明确日野汽车，不是Sony。可保留运营公司独立身份；源有2026年Archion整合及丰田控股表述，最新所有权与控股母公司须另核，不把合并控股公司与日野本体混同。')
add(68,'分配','JP','CORP','明确Toyota Tsusho综合商社，不是三菱商事，可独立CORP；controlling_shareholder关系及持股比例另核。')
add(69,'分配','JP','CORP','明确Toyota Industries自动织机公司，不是Mitsui & Co.或Toyota Motor；集团交叉持股不等于同一企业。')
add(70,'分配','JP','CORP','明确JTEKT轴承/转向等工业企业，不是Hitachi，可独立CORP。')
add(71,'挂起','JP','CORP/ACAD（企业科研机构口径待定）','官网证实丰田中央研发所是独立出资设立的株式会社，以基础研究为主要职能。主体明确，但需统一企业科研公司CORP与研究所ACAD的分类规则，不能仅见“研究所”强改类，也不能与丰田内部研发部门等同。',['https://www.tytlabs.co.jp/en/company/profile.html','https://global.toyota/en/company/profile/facilities/r-d/'])
add(72,'不分配','US（全球总部；日本法人另有）','CORP','源明确总部San Mateo的SIE全球业务，不能按JP-CORP-197默认日本主体；官方区分美国LLC与日本Inc.，先按具体实体核定。',['https://www.playstation.com/en-us/corporate/about-us/','https://sonyinteractive.com/en/press-releases/sony-computer-entertainment-and-sony-network--entertainment-announce-the-formation-of--sony-interactive-entertainment-llc/'])
add(73,'不分配','US','CORP/MEDIA（影视集团口径）','Sony Pictures Entertainment为美国影视业务主体，不是日本制铁，也不是Sony母公司；不按JP-CORP发日本副本，应按美国主实体核定。',['https://www.sony.com/en/SonyInfo/IR/library/FY2020_20F_PDF.pdf'])
add(74,'不分配','US（全球音乐集团）','CORP/MEDIA（音乐集团口径）','源为全球Sony Music Group（录音及词曲出版），不能按JP-CORP创建日本Sony Music Entertainment副本；先区分全球集团与日本本土音乐公司及具体法律实体。',['https://www.sonymusic.com/facts-and-figures/'])
add(75,'分配','JP','CORP','明确Sony Semiconductor Solutions独立半导体业务主体，不是Seven & i，可独立CORP；芯片市场份额为旧数据，另核。')
add(76,'改类别后分配','JP','FIN','Sony Financial Group以寿险、财险、银行等金融业务为核心，按FIN金融控股集团建档，不照JP-CORP-201发号；分拆上市日期和Sony持股另核。',['https://www.sonyfg.co.jp/en/company/about_us.html','https://www.sonyfg.co.jp/en/faq.html'])
add(77,'分配','JP','CORP','明确KADOKAWA综合内容集团，不是TEPCO；按综合企业CORP可建独立主体。Sony“最大股东”不当然等于控制股东，源controlling_shareholder关系须另核。')
add(78,'不分配','注册地CYM；总部/上市地HKG','CORP','不按JP-CORP发号：TCL Electronics是开曼注册、香港上市并设总部联系地址的公司，不是日本电装，也不宜按母集团名直接归惠州法人。需分开法律注册地、总部、运营地。',['https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0429/2026042900031.pdf','https://electronics.tcl.com/'])
add(79,'不分配','US（法律主体待核）','CORP/MEDIA（流媒体平台）','Crunchyroll不是Japan Post。Sony持股不使美国流媒体业务成为日本本土法人；应先区分公司与平台品牌并在美国主实体口径核定，不照JP-CORP-205发号。')
add(80,'不分配','ID','FIN','源明确印尼Bank Danamon，为MUFG子公司，不是日本MUFG母体。否定JP-FIN-046，核印尼主银行ID；历史/拟议分行合并不等于已经与母集团成为同一银行。')
assert set(V)==set(range(1,81))

# Check proposed identifiers against every dated registry, including archived entries.
allreg={};historical=defaultdict(list)
for p in (ROOT/'output').glob('[a-z][a-z]/20*/id_registry.json'):
 data=read(p);allreg[p.relative_to(ROOT).as_posix()]=data
 for arr,idkey in [('registry','org_id'),('deprecated_registry','org_id'),('person_registry','person_id'),('deprecated_person_registry','person_id')]:
  for e in data.get(arr) or []:
   if e.get(idkey):historical[e[idkey]].append({'file':p.relative_to(ROOT).as_posix(),'array':arr,'entry':e})
reserved=[{'review_row':x['review_row'],'id':x['row']['建议新ID'],'history':historical[x['row']['建议新ID']]} for x in D if x['row']['建议新ID'] in historical]
assert not reserved, reserved

# Verify seven prior merges close to real, active canonical registry entries.
undo=read(OUT/'registry_newid_exec_undo.json');merge_checks=[]
for rp,items in undo['registry'].items():
 rel=pathlib.Path(rp).relative_to(ROOT).as_posix();data=allreg[rel]
 for e in items:
  if e.get('action')!='same_identity':continue
  target=e['new_id'];active=[r for arr in ['registry','person_registry'] for r in data.get(arr,[]) if (r.get('org_id')==target or r.get('person_id')==target) and not r.get('merged_into') and r.get('status') not in ['merged','trimmed','duplicate','excluded','archived']]
  merge_checks.append({'source_id':e['id'],'source_name':e['name'],'target_id':target,'registry_file':rel,'target_active_registered':bool(active),'profile_exists':any((p/'orgs'/f'{target}.json').exists() for p in [ROOT/pathlib.Path(rel).parent]),'current_reference_count':0,'prior_exec_changed_reference_count':sum(r.get('new')==target for r in undo.get('ref_changes',[]))})
missing={e['target_id']:e for e in merge_checks if not e['target_active_registered']}
merge_targets={e['target_id']:e for e in merge_checks}
proposed_refs=defaultdict(list)
proposed_ids={x['row']['建议新ID'] for x in D}
for path in list(M):
 if ('/persons/' not in path and '/orgs/' not in path) or not path.endswith('.json'):continue
 data=json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
 for arr,field in [('work_experience','org_id'),('related_entities','org_id'),('key_people','person_id'),('person_relationships','person_id'),('family_members','person_id')]:
  for j,e in enumerate(data.get(arr) or []):
   if not isinstance(e,dict):continue
   if e.get(field) in merge_targets:merge_targets[e[field]]['current_reference_count']+=1
   if e.get(field) in proposed_ids:proposed_refs[e[field]].append({'file':path,'pointer':f'{arr}[{j}].{field}','entry':e})
assert len(merge_checks)==7
for x in D:
 if proposed_refs.get(x['row']['建议新ID']):
  if V[x['review_row']]['conclusion'] in ['分配','改类别后分配']:V[x['review_row']]['conclusion']='挂起'
  V[x['review_row']]['reason']+=' 建议编号已存在于业务引用，须先核对这些存量引用主体，不能因registry未登记就当空号。'

changed=[p for p,h in M.items() if not (ROOT/p).exists() or hashlib.sha256((ROOT/p).read_bytes()).hexdigest()!=h]
assert not changed, changed[:10]
records=[];proof=[]
for x in D:
 i=x['review_row'];v=V[i];r=dict(x['row']);matching=[q for q in x['all_current_collision_references'] if q['matches_shadow_heuristic']]
 r['复核结论']=v['conclusion'];r['备注']=v['reason']+' 本轮仅为复核建议，不授权执行。'
 r.update({'复核序号':i,'国别建议':v['country'],'类别建议':v['category'],'建议编号占用检查':('registry未登记但业务引用已使用，禁止直接分配' if proposed_refs.get(r['建议新ID']) else '全部日期registry/归档项和当前业务引用未见该号；执行前仍需再查'),
 '当前匹配引用数（含跨类型及复合项）':len(matching),'匹配引用字段类型':' ; '.join(sorted(set(q['kind'] for q in matching))) or '无当前引用',
 '引用证据位置':' ; '.join(q['file']+'#'+q['pointer'] for q in matching),
 '原始引用内容':json.dumps([q['entry'] for q in matching],ensure_ascii=False,separators=(',',':')),
 '参考来源':' ; '.join(v['external_sources']),'证据范围':'本地原条目/现画像/活动和归档注册项核对'+('；疑难点有官方来源' if v['external_sources'] else '；未逐项重新外网事实核验'),
 '执行授权':'否；新ID分配、引用修复和合并回退均未执行'})
 records.append(r);proof.append({'review_row':i,**v,'original':x['row'],'references':matching})
for filename,items in [('registry_newid_sample_80_next_reviewed.csv',records),('registry_newid_sample_80_next_attention.csv',[r for r in records if r['复核结论']!='分配'])]:
 with (OUT/filename).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(items)
summary={'review_only':True,'execution_authorized':False,'sample':80,'conclusions':dict(Counter(r['复核结论'] for r in records)),
 'by_country':{c:dict(Counter(r['复核结论'] for r in records if r['国家']==c)) for c in ['KR','MX','NZ','JP']},
 'no_current_reference_rows':[r['复核序号'] for r in records if r['当前匹配引用数（含跨类型及复合项）']==0],
 'person_as_org_rows':[23,28,36,37],'non_organization_rows':[7,18,44,60],
 'occupied_proposed_ids':reserved,'proposed_ids_already_in_references':dict(proposed_refs),'matching_references_including_compound':sum(r['当前匹配引用数（含跨类型及复合项）'] for r in records),
 'prior_merge_checks':merge_checks,'prior_missing_canonical_count':len(missing),'source_hashes_checked':len(M),'changed_source_files':changed,
 'input_csv_sha256':M['output/_id_audit/registry_newid_sample_80_next.csv']}
(OUT/'registry_newid_next80_review_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'registry_newid_next80_review_decisions.json').write_text(json.dumps({'review_only':True,'execution_authorized':False,'rows':proof},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'registry_newid_prior_merge_check.json').write_text(json.dumps({'review_only':True,'checks':merge_checks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'registry_newid_next80_review_manifest.json').write_text(json.dumps(M,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
with (OUT/'registry_newid_prior_merge_check.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(merge_checks[0]));w.writeheader();w.writerows(merge_checks)
report=['# 第二批80条新ID复核','',
 '日期：2026-11-13。本轮已完成80条逐项意见及必要的上轮合并复核，只写复核产物，没有更改registry、画像、引用ID、索引或图片。没有执行新的分配，也没有回退上一轮操作。','',
 '**结论：本批建议25条可分配独立身份、2条改类别后分配、25条不按原方案分配、28条挂起。先处理已确认的编号占用与合并闭合性问题，再生成执行计划。**','',
 '|意见|KR|MX|NZ|JP|合计|','|---|---:|---:|---:|---:|---:|']
for k in ['分配','改类别后分配','不分配','挂起']:
 report.append('|'+k+'|'+ '|'.join(str(summary['by_country'][c].get(k,0)) for c in ['KR','MX','NZ','JP'])+'|'+str(summary['conclusions'][k])+'|')
report += ['',
 '“分配”表示独立主体和类别在当前证据下原则可用，不是写入授权，也不表示本行全部职务、股权、日期与关系内容已核实。“不分配”是否定本行所提组织身份/国别/编号，不代表删除已知实体；外国实体要走主身份归一，人物要走人物修复，不能永久丢弃。','',
 '## 1. 编号分配器还缺一类保留号：已有悬空业务引用','',
 '80个建议编号均未出现在全部日期registry及deprecated注册项中，但其中3个编号已经出现在当前业务引用，合计5个位置，而且名称不是本次拟赋予的实体。只检查registry、画像和索引仍不够。','',
 '|候选编号|本次拟分配身份|当前业务引用实际写的身份|','|---|---|---|',
 '|KR-ACAD-028|Hanyang University|Korea Institute for National Unification（统一研究院）|',
 '|KR-CORP-035|Lotte Group|POSCO E&C；Korail Retail|',
 '|KR-CORP-036|Amorepacific Corporation|POSCO DX；Korail Logis|','',
 '以上样本第1、3、4条均挂起。后两号在存量数据里本来就各自被两家不同公司共用；这是已有未注册ID混乱，不能通过给它们新建本次候选画像来解决。应将所有引用字段中的非空ID也纳入保留集合，并对每个已用ID的名称/主体冲突分别处理。','',
 '证据：output/kr/2026-05-04/orgs/KR-GOV-007.json#related_entities[7].org_id；KR-CORP-006.json#related_entities[2]/[4].org_id；KR-SOE-003.json#related_entities[4]/[6].org_id。完整原条目见review_summary.json的proposed_ids_already_in_references。','',
 '## 2. 上轮7条same_identity中4条目标尚未建立','',
 '|源影子ID|影子主体|merged_into|目标活动注册项|当前引用数|','|---|---|---|---|---:|']
for e in merge_checks:
 if not e['target_active_registered']:
  report.append(f"|{e['source_id']}|{e['source_name']}|{e['target_id']}|不存在|{e['current_reference_count']}|")
report += ['',
 '这4条可在registry_newid_exec_undo.json定位到same_identity动作；对应canonical在v3计划中仍为pending_review，却已归档源项并设置merged_into。其余3条（KAIST、雇佣劳动部、Commerce Commission）已存在活动目标注册项。','',
 '4个问题目标没有画像；其中KR-CORP-036已有2条业务引用，但它们指POSCO DX和Korail Logis，不是Amorepacific，而且本次61条执行日志没有将任何引用改到这4个目标。因此不能把这2条归因于刚执行的226条改链，也不能称这些只是正确新身份“暂无画像”：这4个canonical连注册身份都未建立。','',
 '处理建议：只有canonical身份通过复核且先建立后，才能归档同实体影子；本批不自动补这4个目标。尤其KR-GOV-1249拟代表新千年民主党，GOV类别本身就不合适。KR-CORP-036还有引用身份冲突，不应原号直接补建。','',
 '执行器的same_identity分支先修改old的status/merged_into，再把old写入undo，日志中的old已是修改后状态。若要回退，必须先核对真实执行前条目，不能直接把该old当完整原始快照恢复。本轮未修改执行器或运行回滚。','',
 '## 3. 人物被列为组织候选：第23、28、36、37条','',
 '- 第23条Rosaura Ruiz的114号档案把本人写作雇主，拟建MX-ACAD身份；已有102号和114号人物档案。其部长职位对应SECIHTI，已有MX-GOV-033可作核实候选，须修组织文字及任期，并另处理人物重复，不能把org_id换成人物ID。',
 '- 第28条Fernández Carbajal的119号档案同样把本人写作董事长雇主；已有107号和119号重复人物档案。FEMSA是雇主候选，不是新增同名CORP。',
 '- 第36条实际位于父亲MX-PERSON-000133.person_relationships[1]，说明明确是儿子Claudio的社会活动，影子却用父亲Laporte全名。若机械改到133会产生自指；须识别儿子Claudio X. González Guajardo。',
 '- 第37条也是父亲的儿子关系，Pablo已有MX-PERSON-000134，应该走人物改链复核，不新建组织。','',
 '这4条说明仅依据collision_id前缀继承kind/category有结构性错误：必须先看引用字段期待的人物/组织类型，再验证名称究竟是自然人还是组织；work_experience中的organization也可能填错，不能只看字段名称。','',
 '## 4. 不是可直接建独立机构的条目','',
 '- 第7条“国会议员辅佐官室”未指明任何议员/届次，是通名；第18条“行政高等考试合格”是资格经历。均不分配组织ID。',
 '- 第44条Surveyor-General是法定官员职位，不是组织。[LINZ法定岗位说明](https://www.linz.govt.nz/our-work/statutory-and-support-roles)。',
 '- 第60条CDEM Groups指16个地区机构的集合，不应新建一个全国同名机构。[国家应急管理机构说明](https://www.civildefence.govt.nz/guidance-training/exercises/cdem-exercise-programme)。',
 '- Claro、Bodega Aurrerá、Bait、New Zealand Story、大学网络、咨询小组及大学内设研究所等需要明确品牌/项目/部门建档规则，不能默认为独立法人。','',
 '## 5. 国别、类别及沿革','',
 '外国候选包括Georgetown（美国）、Talos（美国）、Braskem（巴西）、Iberdrola（西班牙）、ASARCO（美国）、Bimbo Bakeries USA（美国）、Generali（意大利）、Inter National Bank（美国）、伦敦JCPC、日本NIHS、中国大陆清华大学、美国索尼娱乐主体、TCL Electronics和印尼Danamon等。源说明本身已明确多项国别，机器风险提示只覆盖少数；不能按引用方所在地机械发号。','',
 '索尼旗下美国公司不等于日本母体。TCL Electronics还须分开开曼注册地与香港总部/上市地，不能只在日本/中国之间二选一。[SIE总部官方](https://www.playstation.com/en-us/corporate/about-us/)、[TCL发行人2025年报](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0429/2026042900031.pdf)。清华大学也不能选用台湾National Tsing Hua University画像来替代大陆Tsinghua。','',
 '本批两条改类建议：第53条NZIST按高等教育ACAD；第76条Sony Financial Group按金融控股FIN。第9条自由韩国党已确定应PARTY，但因重复登记及历史身份尚未归一，仍挂起；第71条企业科研公司CORP/ACAD需先统一口径。[NZIST官方过渡说明](https://www.nzist.ac.nz/about/faqs)、[索尼金融官方](https://www.sonyfg.co.jp/en/faq.html)、[丰田中央研究所公司概况](https://www.tytlabs.co.jp/en/company/profile.html)。','',
 '实体链接通过也不证明关系事实正确：第45条生产力委员会实际于2024-02-29终止，而源写2024年1月；监管部官网明确它没有取代生产力委员会，原predecessor关系需要另修。[财政部终结报告](https://www.treasury.govt.nz/publications/annual-report/new-zealand-productivity-commission-annual-report-1-july-2023-29-february-2024)、[监管部声明](https://www.regulation.govt.nz/news/building-up-from-establishment-phase/)。第56条Te Arawhiti在2025年已有更名和职权转移，不能继续当现状不变。第32条标题写Bait电商平台而官方明确MVNO业务，同样需要修文字。','',
 '## 6. 覆盖范围与验证','',
 f'- 80/80行均给出结论、理由、类别/国别建议和本地引用位置；60行有原碰撞ID引用，韩国20行没有对应当前引用。另发现Talos一条复合引用，故保留61个匹配候选引用位置，不将其自动迁移。',
 f'- 证据快照含五种引用方向，故能识别person_id用了CORP编号的跨类型问题；仅扫描work/related会漏掉第36、37条。',
 f'- {len(M):,}个输入文件SHA256校验未变，含原80条清单、v3计划、注册表和读取的画像/执行记录。仅复核与输出报告，未重新盘点头像文件，也未写入头像。',
 '- 主要为本地身份一致性复核，疑难国别/类别/机构性质/沿革查了官方来源；不是80行所有事实逐条独立外网复证。非随机取样，不外推906条剩余计划的错误率。','',
 '## 交付与建议顺序','',
 '- output/_id_audit/registry_newid_sample_80_next_reviewed.csv：80条完整意见。',
 '- output/_id_audit/registry_newid_sample_80_next_attention.csv：55条非直接分配意见。',
 '- output/_id_audit/registry_newid_prior_merge_check.csv / .json：上轮7条合并闭合性证据。',
 '- output/_id_audit/registry_newid_next80_review_summary.json：计数、5个存量引用位置、编号占用证据。',
 '- output/_id_audit/registry_newid_next80_review_decisions.json / registry_newid_next80_context.json：逐项结构化意见及原始证据。',
 '- output/_id_audit/registry_newid_next80_review_manifest.json：本轮输入哈希。','',
 '优先顺序：先补分配器的全引用保留号与same_identity目标存在性检查；再处理4个未闭合合并及当前编号多身份冲突；人物/考试/职位/集合不走组织分配；最后按本轮25+2条原则可用意见重新生成待执行计划。不要从助手CSV直接触发批量写入。','']
(ROOT/'docs/registry-newid-next80-review.md').write_text('\n'.join(report),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
