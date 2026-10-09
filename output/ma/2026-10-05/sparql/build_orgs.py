# -*- coding: utf-8 -*-
"""Build _target_orgs.json for Morocco (MA / Q1028) from collected SPARQL + Wikipedia + web search data."""
import json, re, os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = r"D:/claude-workspace/apec-osint-tool/output/ma/2026-10-05/_target_orgs.json"

consolidated = {e['qid']: e for e in json.load(open(os.path.join(BASE, 'consolidated.json'), encoding='utf-8'))}
wv2 = json.load(open(os.path.join(BASE, 'wiki_verify2.json'), encoding='utf-8'))
wv3 = json.load(open(os.path.join(BASE, 'wiki_verify3.json'), encoding='utf-8'))
wv4 = json.load(open(os.path.join(BASE, 'wiki_verify4.json'), encoding='utf-8'))
wiki = {}
for r in wv2 + wv3 + wv4:
    if r.get('qid'):
        wiki[r['qid']] = r

def prop(qid, key):
    e = consolidated.get(qid)
    if e and key in e['props']:
        return e['props'][key]
    return None

def norm_date(v):
    if not v:
        return None
    v = str(v)
    m = re.match(r'^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?', v)
    if not m:
        return None
    y, mo, d = m.group(1), m.group(2) or '01', m.group(3) or '01'
    return f"{y}-{mo}-{d}"

def W(qid):
    """wikidata source url"""
    return {"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"}

def WP(qid):
    r = wiki.get(qid)
    return {"type": "wikipedia", "url": r['url']} if r and r.get('url') else None

def OW(qid):
    w = prop(qid, 'website')
    return {"type": "official_website", "url": w} if w else None

orgs = []
used_ids = set()

def add(id_, qid, name, category, subcategory=None, desc=None, aliases=None, hq=None,
        founded=None, website=None, parent=None, key_people=None, relationships=None,
        extra_sources=None, status="unverified"):
    assert id_ not in used_ids, f"dup id {id_}"
    used_ids.add(id_)
    if qid and not founded:
        founded = norm_date(prop(qid, 'inception') or prop(qid, 'established') or prop(qid, 'founded'))
    if qid and not website:
        website = prop(qid, 'website')
    if qid and not hq:
        hq = prop(qid, 'hqLabel')
    sources = []
    if qid:
        sources.append(W(qid))
        wp = WP(qid)
        if wp:
            sources.append(wp)
        ow = OW(qid)
        if ow:
            sources.append(ow)
    for s in (extra_sources or []):
        sources.append(s)
    # de-dup sources
    seen = set()
    srcs = []
    for s in sources:
        if s['url'] not in seen:
            seen.add(s['url'])
            srcs.append(s)
    entry = {
        "id": id_,
        "wikidata_qid": qid,
        "name": name,
        "category": category,
        "country": "MA",
        "verification_status": status,
    }
    if aliases:
        entry["aliases"] = aliases
    if subcategory:
        entry["subcategory"] = subcategory
    if desc:
        entry["description"] = desc
    if hq:
        entry["headquarters"] = hq
    if founded:
        entry["founded"] = founded
    if website:
        entry["website"] = website
    if parent:
        entry["parent_organization"] = parent
    if key_people:
        entry["key_people"] = key_people
    if relationships:
        entry["relationships"] = relationships
    if srcs:
        entry["sources"] = srcs
    orgs.append(entry)

# ---------------- GOV: ministries (from SPARQL rH2, ar labels verified) ----------------
V = "verified"      # Wikipedia summary or EntityData cross-check
P = "partial"       # Wikidata SPARQL data with ar/fr label, no external page check
U = "unverified"

add("MA-GOV-001", "Q3315358", "Ministry of Foreign Affairs, African Cooperation and Moroccan Expatriates",
    "GOV", "Ministry", "Moroccan government ministry in charge of foreign relations, African cooperation and Moroccans residing abroad.",
    aliases=["وزارة الشؤون الخارجية والتعاون الإفريقي والمغاربة المقيمين بالخارج",
             "ministère des Affaires étrangères, de la Coopération africaine et des Marocains résidant à l'étranger", "MAE"],
    founded="1906-01-01", website="https://diplomatie.ma/", status=V)
add("MA-GOV-002", "Q3315238", "Ministry of Economy and Finance (Morocco)", "GOV", "Ministry",
    "Moroccan government ministry responsible for public finances.",
    aliases=["وزارة الاقتصاد والمالية", "Ministère de l'Économie et des Finances", "MEF"],
    website="https://www.finances.gov.ma/", status=P)
add("MA-GOV-003", "Q3315292", "Ministry of Justice (Morocco)", "GOV", "Ministry",
    "Moroccan government ministry in charge of the courts and justice administration.",
    aliases=["وزارة العدل", "Ministère de la Justice"], website="https://www.justice.gov.ma/", status=P)
add("MA-GOV-004", "Q3315316", "Ministry of Health and Social Protection (Morocco)", "GOV", "Ministry",
    "Moroccan government ministry in charge of public health.",
    aliases=["وزارة الصحة", "Ministère de la Santé"], website="https://www.sante.gov.ma/", status=P)
add("MA-GOV-005", "Q22934919", "Ministry of Interior (Morocco)", "GOV", "Ministry",
    "Moroccan government ministry in charge of interior affairs, local administration and elections.",
    aliases=["وزارة الداخلية", "Ministère de l'Intérieur"], website="https://www.interieur.gov.ma/", status=P)
add("MA-GOV-006", "Q12250943", "Ministry of National Education (Morocco)", "GOV", "Ministry",
    "Ministry in charge of primary and secondary education in Morocco.",
    aliases=["وزارة التربية الوطنية", "Ministère de l'Éducation Nationale"], status=P)
add("MA-GOV-007", "Q25463514", "Ministry of Higher Education, Scientific Research and Innovation (Morocco)", "GOV", "Ministry",
    "Ministry in charge of universities and scientific research in Morocco.",
    aliases=["وزارة التعليم العالي والبحث العلمي والابتكار"], status=P)
add("MA-GOV-008", "Q30094020", "Ministry of Agriculture, Maritime Fisheries, Rural Development and Water and Forests", "GOV", "Ministry",
    "Ministry in charge of agriculture and maritime fisheries in Morocco.",
    aliases=["وزارة الفلاحة والصيد البحري", "Ministère de l'Agriculture"], website="https://www.agriculture.gov.ma/", status=P)
add("MA-GOV-009", "Q30262038", "Ministry of Energy Transition and Sustainable Development (Morocco)", "GOV", "Ministry",
    "Ministry in charge of energy policy and sustainable development in Morocco.",
    aliases=["وزارة الانتقال الطاقي والتنمية المستدامة"], status=P)
add("MA-GOV-010", "Q30261920", "Ministry of Industry and Trade (Morocco)", "GOV", "Ministry",
    "Ministry in charge of industry and commerce in Morocco.",
    aliases=["وزارة الصناعة والتجارة"], status=P)
add("MA-GOV-011", "Q108829759", "Ministry of Equipment and Water (Morocco)", "GOV", "Ministry",
    "Ministry in charge of public works and water resources in Morocco.",
    aliases=["وزارة التجهيز والماء", "Ministère de l'Équipement et de l'Eau"], status=P)
add("MA-GOV-012", "Q1445967", "Ministry of Transport and Logistics (Morocco)", "GOV", "Ministry",
    "Ministry in charge of transport infrastructure in Morocco.",
    aliases=["وزارة النقل واللوجيستيك"], status=P)
add("MA-GOV-013", "Q12250923", "Ministry of Endowments and Islamic Affairs (Morocco)", "GOV", "Ministry",
    "Ministry in charge of religious affairs and Islamic endowments (habous) in Morocco.",
    aliases=["وزارة الأوقاف والشؤون الإسلامية", "Ministère des Habous et des Affaires Islamiques"],
    founded="1955-12-07", website="https://www.habous.gov.ma", status=P)
add("MA-GOV-014", "Q62202002", "Ministry of Tourism, Handicrafts and Social and Solidarity Economy (Morocco)", "GOV", "Ministry",
    "Ministry in charge of tourism and handicrafts in Morocco.",
    aliases=["وزارة السياحة والصناعة التقليدية والاقتصاد الاجتماعي"], status=P)
add("MA-GOV-015", "Q25463136", "Ministry of National Territory Planning, Land Planning, Housing and City Policy (Morocco)", "GOV", "Ministry",
    "Ministry in charge of housing and urban policy in Morocco.",
    aliases=["وزارة السكنى وسياسة المدينة"], status=P)
add("MA-GOV-016", "Q26459282", "Ministry of Youth, Culture and Communication (Morocco)", "GOV", "Ministry",
    "Ministry in charge of culture and communication in Morocco.",
    aliases=["وزارة الشباب والثقافة والتواصل"], status=P)
add("MA-GOV-017", "Q26459781", "Ministry of Solidarity, Women, Family and Social Development (Morocco)", "GOV", "Ministry",
    "Ministry in charge of social development and family affairs in Morocco.",
    aliases=["وزارة التضامن والمرأة والأسرة والتنمية الاجتماعية"], status=P)
add("MA-GOV-018", "Q79403282", "Ministry of Economic Inclusion, Small Business, Employment and Skills (Morocco)", "GOV", "Ministry",
    "Ministry in charge of employment and small business in Morocco.",
    aliases=["وزارة الإدماج الاقتصادي والمقاولة الصغرى والتشغيل والكفاءات"], status=P)
add("MA-GOV-019", "Q121754399", "Ministry of Culture and Communication (Morocco)", "GOV", "Ministry",
    "Ministry in charge of culture in Morocco.",
    aliases=["وزارة الثقافة والاتصال"], status=P)
add("MA-GOV-020", "Q12208534", "Government of Morocco", "GOV", "Executive Branch",
    "Executive power of the Kingdom of Morocco, composed of the Head of Government, ministers, ministers delegate and secretaries of state.",
    aliases=["حكومة المملكة المغربية", "Cabinet of Morocco"],
    key_people=[{"title": "Head of Government", "name": "Aziz Akhannouch", "since": "2021"},
                {"title": "King", "name": "Mohammed VI", "since": "1999"}],
    extra_sources=[{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Government_of_Morocco"},
                   {"type": "official_website", "url": "https://www.cg.gov.ma/en"},
                   {"type": "web_search", "url": "https://www.chambredesrepresentants.ma/fr/membres-du-gouvernement"}],
    status=V)
add("MA-GOV-021", "Q3004884", "Parliament of Morocco", "GOV", "Legislature",
    "Bicameral national legislature of Morocco, composed of the House of Representatives and the House of Councillors.",
    aliases=["البرلمان المغربي", "Parlement du Maroc"],
    extra_sources=[{"type": "official_website", "url": "https://www.parlement.ma/"}], status=V)
add("MA-GOV-022", "Q1572773", "House of Representatives (Morocco)", "GOV", "Legislature",
    "Lower house of the Parliament of Morocco, 395 members elected for five-year terms.",
    aliases=["مجلس النواب", "Chambre des Représentants"],
    extra_sources=[{"type": "official_website", "url": "https://www.chambredesrepresentants.ma/"}], status=V)
add("MA-GOV-023", "Q2718576", "House of Councillors (Morocco)", "GOV", "Legislature",
    "Upper house of the Parliament of Morocco.",
    aliases=["مجلس المستشارين", "Chambre des Conseillers"], status=V)
add("MA-GOV-024", "Q3000934", "Constitutional Court of Morocco", "GOV", "Judiciary",
    "Highest judicial body for constitutional matters in Morocco, established by the 2011 constitution.",
    aliases=["المحكمة الدستورية", "Cour Constitutionnelle du Maroc"], status=V)
add("MA-GOV-025", "Q3001004", "Supreme Court of Morocco", "GOV", "Judiciary",
    "Former highest ordinary court of Morocco; succeeded by the Court of Cassation after the 2011 constitution.",
    aliases=["المحكمة العليا المغربية", "Cour suprême (Maroc)"], status=P)
add("MA-GOV-026", "Q2049108", "Royal Advisory Council for Saharan Affairs", "GOV", "Independent Organ",
    "Advisory committee to the Moroccan government on Western Sahara affairs.",
    aliases=["المجلس الملكي الاستشاري للشؤون الصحراوية", "CORCAS"],
    website="http://www.corcas.com", status=P)
add("MA-GOV-027", "Q2993703", "National Human Rights Council (Morocco)", "GOV", "Independent Organ",
    "Moroccan national human rights institution.",
    aliases=["المجلس الوطني لحقوق الإنسان", "CNDH", "Conseil National des Droits de l'Homme"],
    founded="1990-04-20", website="http://www.cndh.ma", status=P)
add("MA-GOV-028", "Q2993767", "Competition Council (Morocco)", "GOV", "Independent Organ",
    "Moroccan independent competition regulator.",
    aliases=["مجلس المنافسة", "Conseil de la Concurrence"],
    founded="2008-01-01", website="https://www.conseil-concurrence.ma", status=P)
add("MA-GOV-029", "Q3128426", "High Commission for Planning (Morocco)", "GOV", "Statutory Board",
    "Moroccan government statistical agency producing national statistics and census.",
    aliases=["المندوبية السامية للتخطيط", "HCP", "Haut-Commissariat au Plan"],
    extra_sources=[{"type": "official_website", "url": "https://www.hcp.ma/"}], status=V)
add("MA-GOV-030", "Q2931748", "National Commission for the Control of Personal Data Protection (Morocco)", "GOV", "Independent Organ",
    "Moroccan data protection authority established under Law 09-08.",
    aliases=["CNDP", "اللجنة الوطنية لمراقبة حماية المعطيات ذات الطابع الشخصي"],
    extra_sources=[{"type": "official_website", "url": "https://www.cndp.ma/"}], status=P)
add("MA-GOV-031", None, "National Telecommunications Regulatory Agency (Morocco)", "GOV", "Statutory Board",
    "Moroccan public establishment in charge of regulation of the telecommunications sector.",
    aliases=["ANRT", "وكالة التنظيم للبريد والاتصالات الفلاحية"],
    website="https://www.anrt.ma/",
    extra_sources=[{"type": "web_search", "url": "https://www.mmsp.gov.ma/fr/anrt"}], status=V)
add("MA-GOV-032", "Q99149541", "General Delegation of the Penitentiary and Reintegration Administration (Morocco)", "GOV", "Statutory Board",
    "Moroccan prison administration agency.",
    aliases=["المندوبية السامية لإدارة السجون وإعادة الإدماج", "DGAPR"],
    founded="2008-01-01", website="https://www.dgapr.gov.ma/", status=P)
add("MA-GOV-033", "Q138542815", "National Agency for the Regulation of Cannabis-Related Activities (Morocco)", "GOV", "Statutory Board",
    "Moroccan agency regulating legal cannabis activities, created in 2022.",
    aliases=["ANRAC", "الوكالة الوطنية لتدبير الأنشطة المرتبطة بالقنب"],
    founded="2022-01-01", website="https://www.anrac.gov.ma/fr/", status=P)
add("MA-GOV-034", "Q138542383", "Moroccan Agency for Investment and Export Development", "GOV", "Statutory Board",
    "Moroccan investment and export promotion agency (AMDIE).",
    aliases=["AMDIE", "وكالة المغرب للاستثمار وتصدير المقاولات"],
    founded="2017-01-01", status=P)
add("MA-GOV-035", "Q30261778", "Direction Générale de la Météorologie Nationale (Morocco)", "GOV", "Statutory Board",
    "Moroccan national meteorological service.",
    aliases=["المديرية العامة للأرصاد الجوية"],
    founded="1961-01-01", website="https://www.marocmeteo.ma/", status=P)
add("MA-GOV-036", "Q25462921", "General Secretariat of the Government of Morocco", "GOV", "Executive Branch",
    "Moroccan government body in charge of preparing and publishing official texts.",
    aliases=["الأمانة العامة للحكومة", "SGG"],
    extra_sources=[{"type": "official_website", "url": "https://www.sgg.gov.ma/"}], status=P)
add("MA-GOV-037", "Q2518185", "Royal Institute of Amazigh Culture", "GOV", "Research Institute",
    "Moroccan public institute in charge of the promotion of Amazigh (Berber) culture and language.",
    aliases=["المعهد الملكي للثقافة الأمازيغية", "IRCAM"],
    founded="2001-10-17", website="https://www.ircam.ma/", status=P)

# ---------------- MIL ----------------
add("MA-MIL-001", "Q34511", "Royal Moroccan Armed Forces", "MIL", "Military",
    "Combined military forces of Morocco, comprising the Army, Navy, Air Force and Royal Gendarmerie.",
    aliases=["القوات المسلحة الملكية المغربية", "FAR", "Forces Armées Royales"],
    key_people=[{"title": "Supreme Commander", "name": "Mohammed VI", "since": "1999"}],
    extra_sources=[{"type": "official_website", "url": "https://www.far.ma/"}], status=V)
add("MA-MIL-002", "Q1238830", "Royal Moroccan Gendarmerie", "MIL", "Gendarmerie",
    "Gendarmerie branch of Morocco's military in charge of rural policing.",
    aliases=["القوات الملكية للمحافظة", "Gendarmerie Royale Marocaine"],
    status=V)
add("MA-MIL-003", "Q687114", "General Directorate of Territorial Surveillance (Morocco)", "MIL", "Intelligence",
    "Moroccan domestic intelligence agency.",
    aliases=["مديرية مراقبة التراب الوطني", "DGST", "Direction Générale de la Surveillance du Territoire"],
    status=V)
add("MA-MIL-004", "Q117198344", "General Directorate for National Security (Morocco)", "MIL", "Police",
    "Moroccan national civilian police force (DGSN/Sûreté Nationale).",
    aliases=["المديرية العامة للأمن الوطني", "DGSN"],
    status=P)

# ---------------- SOE ----------------
add("MA-SOE-001", "Q501605", "OCP Group", "SOE", "Phosphate Mining",
    "Moroccan state-owned phosphate and fertilizer producer, one of the world's largest phosphate exporters.",
    aliases=["مجموعة المكتب الشريف للفوسفاط", "Office Chérifien des Phosphates"],
    founded="1920-08-07", website="https://www.ocpgroup.ma/",
    extra_sources=[{"type": "web_search", "url": "https://en.wikipedia.org/wiki/OCP_Group"}], status=V)
add("MA-SOE-002", "Q1815809", "ONCF (Office National des Chemins de Fer)", "SOE", "Rail Transport",
    "National railway operator of Morocco.",
    aliases=["المكتب الوطني للسكك الحديدية", "ONCF"],
    website="https://www.oncf.ma/", status=V)
add("MA-SOE-003", "Q3349644", "ONEE (Office National de l'Électricité et de l'Eau Potable)", "SOE", "Utilities",
    "Moroccan state-owned utility in charge of electricity and drinking water.",
    aliases=["المكتب الوطني للكهرباء والماء الصالح للشرب", "ONEE", "ONE"],
    status=P)
add("MA-SOE-004", "Q128051781", "Phosboucraa", "SOE", "Phosphate Mining",
    "Moroccan phosphate mining subsidiary of OCP Group operating in Boucraa, Western Sahara.",
    aliases=["فوسبوكرة"],
    parent="OCP Group", status=P)
add("MA-SOE-005", "Q2933285", "Caisse de Dépôt et de Gestion (Morocco)", "SOE", "Financial Institution",
    "Moroccan state-owned long-term investment institution.",
    aliases=["صندوق الإيداع والتدبير", "CDG"],
    website="https://www.cdg.ma/", status=V)
add("MA-SOE-006", "Q3294973", "Marsa Maroc", "SOE", "Port Operations",
    "Moroccan state-controlled port terminal operator.",
    aliases=["مرسى المغرب", "Société d'Exploitation des Ports"],
    founded="2006-01-01", website="https://www.marsamaroc.co.ma/", status=P)
add("MA-SOE-007", "Q1945306", "Société Nationale des Autoroutes du Maroc", "SOE", "Road Infrastructure",
    "Moroccan state-owned motorway operator.",
    aliases=["الشركة الوطنية للطرق السيارة بالمغرب", "ADM"],
    founded="1989-06-12", website="http://www.adm.co.ma", status=P)
add("MA-SOE-008", "Q18384641", "Masen (Moroccan Agency for Sustainable Energy)", "SOE", "Renewable Energy",
    "Moroccan agency in charge of renewable energy programs (Noor solar).",
    aliases=["ماسن", "Moroccan Agency for Sustainable Energy"],
    founded="2010-03-18", website="http://www.masen.ma", status=P)
add("MA-SOE-009", "Q7072765", "Barid Al-Maghrib", "SOE", "Postal Services",
    "Moroccan national postal operator.",
    aliases=["بريد المغرب", "National Posts and Telecommunication Office"],
    founded="1981-01-01", status=P)
add("MA-SOE-010", "Q3117542", "Royal Air Maroc", "SOE", "Airline",
    "Flag carrier airline of Morocco, majority state-owned.",
    aliases=["الخطوط الملكية المغربية", "RAM"],
    website="http://www.royalairmaroc.com",
    extra_sources=[{"type": "web_search", "url": "https://en.wikipedia.org/wiki/Royal_Air_Maroc"}], status=P)
add("MA-SOE-011", "Q138844227", "Tamwilcom", "SOE", "Financial Institution",
    "Moroccan public financial institution financing SMEs (ex-CCG).",
    aliases=["تمويلكوم", "Caisse Centrale de Garantie"],
    founded="2021-01-01", website="https://www.tamwilcom.ma/", status=P)

# ---------------- CORP ----------------
add("MA-CORP-001", "Q2299942", "Maroc Telecom", "CORP", "Telecommunications",
    "Morocco's main telecommunications operator (Itissalat Al-Maghrib), majority state-owned and listed on CSE.",
    aliases=["اتصالات المغرب", "IAM", "Itissalat Al-Maghrib"],
    founded="1998-02-03", website="https://www.iam.ma", status=V)
add("MA-CORP-002", "Q1388949", "Inwi", "CORP", "Telecommunications",
    "Moroccan mobile and fixed-line telecom operator (formerly Wana).",
    aliases=["إنوي", "Wana Corporate"],
    founded="1999-01-01", website="https://inwi.ma/", status=V)
add("MA-CORP-003", "Q2300422", "Orange Morocco", "CORP", "Telecommunications",
    "Moroccan telecom operator, subsidiary of Orange S.A. (formerly Maroc Connect / Médi Télécom).",
    aliases=["أورنج المغرب", "Méditelecom"],
    founded="1999-01-01", website="https://www.orange.ma/", status=P)
add("MA-CORP-004", "Q2829178", "Akwa Group", "CORP", "Conglomerate",
    "Moroccan diversified conglomerate in fuel distribution and chemicals (Afriquia), headquartered in Casablanca.",
    aliases=["مجموعة أكوا"],
    founded="1959-01-01", website="http://www.akwagroup.com/", status=V)
add("MA-CORP-005", "Q2055692", "Marjane Group", "CORP", "Retail",
    "Moroccan retail chain (hypermarkets and supermarkets).",
    aliases=["مرجان", "Marjane Holding"],
    founded="1990-01-01", website="https://www.marjane.ma/", status=P)
add("MA-CORP-006", "Q3117513", "ONA Group", "CORP", "Conglomerate",
    "Historic Moroccan holding company (Omnium Nord-Africain), precursor of listed holding companies around SNI.",
    aliases=["مجموعة اللجنة الوطنية الأفريقية", "Omnium Nord-Africain"],
    founded="1934-01-01", website="http://www.ona.ma/", status=P)
add("MA-CORP-007", "Q3117487", "Managem", "CORP", "Mining",
    "Moroccan mining company operating precious and base metals mines in Morocco and Africa.",
    aliases=["منجم"],
    website="https://www.managem.ma/",
    extra_sources=[{"type": "web_search", "url": "https://en.wikipedia.org/wiki/Managem"}], status=V)
add("MA-CORP-008", "Q2998496", "Cosumar", "CORP", "Food Processing",
    "Moroccan sugar producer, subsidiary of Wilmar International.",
    aliases=["كوسومار"],
    status=P)
add("MA-CORP-009", "Q119439768", "Taqa Morocco", "CORP", "Energy",
    "Moroccan independent power producer operating the Jorf Lasfar power plant, listed on Casablanca Stock Exchange.",
    aliases=["طاقة المغرب", "TAQA Morocco"],
    status=P)
add("MA-CORP-010", "Q2972439", "Ciments du Maroc", "CORP", "Cement",
    "Moroccan cement producer, subsidiary of Heidelberg Materials, listed on Casablanca Stock Exchange.",
    aliases=["إسمنت المغرب"],
    status=P)
add("MA-CORP-011", None, "Holcim Maroc", "CORP", "Cement",
    "Moroccan subsidiary of Holcim Group, cement and construction materials producer, listed on Casablanca Stock Exchange.",
    aliases=["هولسيم المغرب"],
    extra_sources=[{"type": "web_search", "url": "https://www.tradingview.com/markets/stocks-morocco/market-movers-large-cap/"}],
    status=U)
add("MA-CORP-012", "Q3236658", "Lesieur Cristal", "CORP", "Food Processing",
    "Moroccan producer of edible oils and soap.",
    aliases=["لوزيور كريستال"],
    founded="1940-01-01", website="http://www.lesieur-cristal.ma", status=P)
add("MA-CORP-013", "Q2989899", "Compagnie de Transports au Maroc (CTM)", "CORP", "Transport",
    "Historic Moroccan intercity bus transport company.",
    aliases=["شركة النقل المغربية"],
    founded="1917-01-01", website="http://www.ctm.ma", status=P)
add("MA-CORP-014", "Q3490063", "Sonasid", "CORP", "Steel",
    "Moroccan steel producer, subsidiary of ArcelorMittal.",
    aliases=["سوناسيد"],
    founded="1974-01-01", website="https://www.sonasid.ma", status=P)
add("MA-CORP-015", "Q56300032", "Afriquia", "CORP", "Fuel Distribution",
    "Moroccan fuel distribution brand of the Akwa Group.",
    aliases=["أفريقيا"],
    website="http://www.afriquia.ma", status=P)
add("MA-CORP-016", "Q2992735", "General Confederation of Moroccan Enterprises", "CORP", "Employers Association",
    "Moroccan employers' business confederation (CGEM).",
    aliases=["الكونفدرالية العامة لمقاولات المغرب", "CGEM"],
    extra_sources=[{"type": "official_website", "url": "https://www.cgem.ma/"}], status=P)

# ---------------- FIN ----------------
add("MA-FIN-001", "Q328198", "Bank Al-Maghrib", "FIN", "Central Bank",
    "Central bank of Morocco, in charge of monetary policy and currency (dirham) issuance.",
    aliases=["بنك المغرب", "BAM", "Bank of Morocco"],
    extra_sources=[{"type": "official_website", "url": "https://www.bkam.ma/"},
                   {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Bank_Al-Maghrib"}], status=V)
add("MA-FIN-002", "Q758052", "Attijariwafa Bank", "FIN", "Commercial Bank",
    "Largest bank in Morocco by market capitalization and assets, subsidiary of Al Mada (ex-SNI).",
    aliases=["الجهة الأولى", "AWB"],
    founded="1904-01-01", website="https://www.attijariwafabank.com/",
    extra_sources=[{"type": "web_search", "url": "https://www.statista.com/statistics/1304506/leading-companies-in-morocco-by-market-capitalization/"}], status=V)
add("MA-FIN-003", "Q2883441", "Banque Centrale Populaire (BCP Group)", "FIN", "Commercial Bank",
    "Moroccan cooperative banking group, one of the country's largest banks.",
    aliases=["البنك الشعبي", "Groupe Banque Populaire", "BCP"],
    founded="1926-05-25", website="https://www.groupebcp.com/", status=V)
add("MA-FIN-004", "Q2300433", "Bank of Africa (BMCE Bank)", "FIN", "Commercial Bank",
    "One of Morocco's largest banks (formerly Banque Marocaine du Commerce Extérieur).",
    aliases=["بنك أفريقيا", "BMCE"],
    founded="1959-01-01",
    extra_sources=[{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Bank_of_Africa"}], status=V)
add("MA-FIN-005", "Q3006220", "CIH Bank", "FIN", "Commercial Bank",
    "Moroccan bank originally founded for housing and tourism financing (Crédit Immobilier et Hôtelier).",
    aliases=["القرض العقاري والسياحي"],
    founded="1920-01-01", website="http://www.cihbank.ma/ar", status=P)
add("MA-FIN-006", "Q3006193", "Crédit Agricole du Maroc", "FIN", "Commercial Bank",
    "Moroccan bank focused on rural and agricultural financing.",
    aliases=["القرض الفلاحي بالمغرب", "GCAM"],
    founded="1961-01-01", website="https://www.creditagricole.ma/", status=P)
add("MA-FIN-007", "Q2940784", "CFG Bank", "FIN", "Commercial Bank",
    "Moroccan private bank (Crédit du Maroc / Compagnie Financière et de Gestion).",
    aliases=["CFG"],
    founded="1992-01-01", website="https://www.cfgbank.com/", status=P)
add("MA-FIN-008", "Q2829300", "Al Barid Bank", "FIN", "Commercial Bank",
    "Moroccan postal bank, subsidiary of Barid Al-Maghrib.",
    aliases=["بريد بنك"],
    founded="2010-01-01", website="http://www.albaridbank.ma/ar", status=P)
add("MA-FIN-009", "Q2882984", "BMCI (Banque Marocaine du Commerce et de l'Industrie)", "FIN", "Commercial Bank",
    "Moroccan bank, subsidiary of BNP Paribas (former Banque Commerciale du Maroc).",
    aliases=["البنك المغربي للتجارة والصناعة"],
    founded="1911-01-01", status=P)
add("MA-FIN-010", "Q3488352", "Saham Bank", "FIN", "Commercial Bank",
    "Moroccan private bank of the Saham group.",
    aliases=["بنك سهم"],
    founded="1913-01-01", website="https://www.sahambank.com/", status=P)
add("MA-FIN-011", "Q3565044", "Wafa Assurance", "FIN", "Insurance",
    "Moroccan insurance company, subsidiary of Attijariwafa Bank group.",
    aliases=["وفاء للتأمين"],
    founded="1972-10-01", website="https://www.wafaassurance.ma/", status=P)
add("MA-FIN-012", "Q2931758", "Saham Assurance", "FIN", "Insurance",
    "Moroccan insurance company of the Saham group.",
    aliases=["سهم للتأمين"],
    founded="1949-01-01", website="http://sahamassurance.com/", status=P)
add("MA-FIN-013", "Q42794743", "RMA Assurance", "FIN", "Insurance",
    "Moroccan insurance company (RMA, ex-Royal Mutuelle Marocaine d'Assurance).",
    aliases=["RMA"],
    website="http://www.rmaassurance.com", status=P)
add("MA-FIN-014", "Q2602796", "Casablanca Stock Exchange", "FIN", "Stock Exchange",
    "Morocco's stock exchange, ~78 listed companies and ~1 trillion dirhams market capitalization (2025).",
    aliases=["بورصة الدار البيضاء", "Bourse de Casablanca", "BVC"],
    extra_sources=[{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Casablanca_Stock_Exchange"},
                   {"type": "official_website", "url": "https://www.casablanca-bourse.com/"}], status=V)
add("MA-FIN-015", "Q123476789", "Moroccan Capital Market Authority (AMMC)", "FIN", "Regulator",
    "Moroccan public authority regulating the capital markets.",
    aliases=["هيئة سوق المساهمات", "AMMC", "Autorité Marocaine du Marché des Capitaux"],
    status=V)
add("MA-FIN-016", "Q12199351", "Wafabank (defunct)", "FIN", "Commercial Bank",
    "Former Moroccan bank, merged into Attijariwafa Bank in 2003.",
    aliases=["وفا بنك"],
    founded="1904-01-01", status=P)

# ---------------- NGO ----------------
add("MA-NGO-001", "Q2867861", "Moroccan Association for Human Rights", "NGO", "Human Rights",
    "Moroccan non-governmental human rights organization founded in 1979.",
    aliases=["AMDH", "الجمعية المغربية لحقوق الإنسان"],
    founded="1979-01-01",
    extra_sources=[{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Moroccan_Association_for_Human_Rights"}], status=V)
add("MA-NGO-002", "Q3537756", "Transparency Maroc", "NGO", "Anti-Corruption",
    "Moroccan national chapter of Transparency International.",
    aliases=["شفافية المغرب"],
    extra_sources=[{"type": "official_website", "url": "https://www.transparency-maroc.ma/"}], status=P)
add("MA-NGO-003", "Q106646266", "High Atlas Foundation", "NGO", "Development",
    "Moroccan NGO founded by Peace Corps Volunteers in 2000 for sustainable development projects.",
    aliases=["HAF"],
    founded="2000-01-01",
    extra_sources=[{"type": "web_search", "url": "https://moroccotravelblog.com/top-4-moroccan-ngos-making-a-social-impact-in-womens-empowerment/"}], status=V)
add("MA-NGO-004", "Q3550326", "Moroccan Workers' Union (UMT)", "NGO", "Trade Union",
    "Morocco's oldest trade union confederation.",
    aliases=["الاتحاد المغربي للشغل", "UMT"],
    status=P)
add("MA-NGO-005", "Q3550304", "General Union of Moroccan Workers (UGTM)", "NGO", "Trade Union",
    "Moroccan trade union confederation linked to the Istiqlal party.",
    aliases=["الاتحاد العام لعمال المغرب", "UGTM"],
    status=P)
add("MA-NGO-006", "Q3075505", "Mohammed V Foundation for Solidarity", "NGO", "Foundation",
    "Moroccan public-interest foundation for social solidarity founded by King Mohammed VI.",
    aliases=["مؤسسة محمد الخامس للتضامن", "Fondation Mohammed V pour la Solidarité"],
    status=V)
add("MA-NGO-007", "Q12251181", "Bayt Mal Al-Qods Asharif Agency", "NGO", "International Cooperation",
    "Moroccan agency supporting Jerusalem and Palestinian institutions, under the Al-Quds Committee.",
    aliases=["وكالة بيت مال القدس الشريف"],
    status=P)
add("MA-NGO-008", "Q3356052", "Moroccan Human Rights Organization (OMDH)", "NGO", "Human Rights",
    "Moroccan human rights organization.",
    aliases=["المنظمة المغربية لحقوق الإنسان", "OMDH"],
    status=P)
add("MA-NGO-009", "Q16677412", "Association Solidarité Féminine", "NGO", "Women's Rights",
    "Moroccan non-profit supporting women in distress in Casablanca.",
    aliases=["جمعية التضامن النسائي"],
    status=P)
add("MA-NGO-010", "Q3116927", "Royal Moroccan Football Federation", "NGO", "Sports Federation",
    "Governing body of football in Morocco.",
    aliases=["الجامعة الملكية المغربية لكرة القدم", "FRMF"],
    extra_sources=[{"type": "official_website", "url": "https://www.frmf.ma/"}], status=P)

# ---------------- ACAD ----------------
add("MA-ACAD-001", "Q378014", "University of al-Qarawiyyin", "ACAD", "University",
    "Historic Moroccan university in Fez, founded in 859 as a madrasa/mosque; considered the oldest existing degree-granting university.",
    aliases=["جامعة القرويين", "Al-Qarawiyyin University", "Université Al Quaraouiyine"],
    founded="0859-01-01", website="http://uaq.ma/", status=P)
add("MA-ACAD-002", "Q1360237", "Mohammed V University (Rabat)", "ACAD", "University",
    "Morocco's first modern university, founded 1957 in Rabat.",
    aliases=["جامعة محمد الخامس", "Université Mohammed V"],
    founded="1957-01-01", website="http://www.um5.ac.ma",
    extra_sources=[{"type": "web_search", "url": "https://www.usnews.com/education/best-global-universities/morocco"}], status=P)
add("MA-ACAD-003", "Q61931430", "Mohammed VI Polytechnic University (UM6P)", "ACAD", "University",
    "Private research university in Benguerir founded 2014, affiliated with OCP Group; top Moroccan research institution in rankings.",
    aliases=["جامعة محمد السادس متعددة التخصصات التقنية", "UM6P"],
    founded="2014-01-01", website="https://www.um6p.ma/",
    extra_sources=[{"type": "web_search", "url": "https://research.com/university-rankings/computer-science/ma"}], status=P)
add("MA-ACAD-004", "Q82826", "Hassan II University of Casablanca", "ACAD", "University",
    "Public university in Casablanca, one of Morocco's largest.",
    aliases=["جامعة الحسن الثاني بالدار البيضة"],
    founded="1975-01-01",
    extra_sources=[{"type": "web_search", "url": "https://www.scimagoir.com/rankings.php?sector=Higher+educ.&page=1&country=MAR"}], status=V)
add("MA-ACAD-005", "Q737095", "Cadi Ayyad University", "ACAD", "University",
    "Public university in Marrakesh, ranked #1 nationally in uniRank 2026.",
    aliases=["جامعة القاضي عياض", "Université Cadi Ayyad"],
    founded="1978-01-01",
    extra_sources=[{"type": "web_search", "url": "https://www.unirank.org/ma/ranking/"}], status=V)
add("MA-ACAD-006", "Q3551418", "Ibn Zohr University", "ACAD", "University",
    "Public university in Agadir.",
    aliases=["جامعة ابن زهر"],
    founded="1989-01-01", website="http://www.uiz.ac.ma/", status=P)
add("MA-ACAD-007", "Q3551490", "Sidi Mohamed Ben Abdellah University", "ACAD", "University",
    "Public university in Fez.",
    aliases=["جامعة سيدي محمد بن عبد الله", "USMBA"],
    founded="1975-01-01", website="http://www.usmba.ac.ma/", status=P)
add("MA-ACAD-008", "Q3551367", "Abdelmalek Essaâdi University", "ACAD", "University",
    "Public university based in Tétouan serving northern Morocco.",
    aliases=["جامعة عبد المالك السعدي", "UAE"],
    founded="1982-01-01", website="http://www.uae.ma/", status=P)
add("MA-ACAD-009", "Q3551453", "Moulay Ismail University", "ACAD", "University",
    "Public university in Meknes.",
    aliases=["جامعة مولاي إسماعيل"],
    founded="1989-01-01", website="http://www.umi.ac.ma/", status=P)
add("MA-ACAD-010", "Q3551445", "Mohammed I University", "ACAD", "University",
    "Public university in Oujda.",
    aliases=["جامعة محمد الأول"],
    founded="1978-01-01", website="http://www.ump.ma/", status=P)
add("MA-ACAD-011", "Q2405067", "Hassan First University", "ACAD", "University",
    "Public university in Settat.",
    aliases=["جامعة الحسن الأول"],
    founded="1997-01-01", website="https://www.uh1.ac.ma/", status=P)
add("MA-ACAD-012", "Q12204499", "Chouaib Doukkali University", "ACAD", "University",
    "Public university in El Jadida.",
    aliases=["جامعة شعيب الدكالي"],
    founded="1985-01-01", website="http://www.ucd.ac.ma", status=P)
add("MA-ACAD-013", "Q3551417", "Ibn Tofail University", "ACAD", "University",
    "Public university in Kénitra.",
    aliases=["جامعة ابن طفيل"],
    status=V)
add("MA-ACAD-014", "Q2829294", "Al Akhawayn University", "ACAD", "University",
    "American-style English-medium private university in Ifrane.",
    aliases=["جامعة الأخوين", "AUI"],
    founded="1993-01-01", status=V)
add("MA-ACAD-015", "Q3551785", "International University of Rabat", "ACAD", "University",
    "Private international university in Rabat, top-1000 in THE rankings.",
    aliases=["الجامعة الدولية للرباط", "UIR"],
    founded="2010-01-01", website="http://www.uir.ac.ma/",
    extra_sources=[{"type": "web_search", "url": "https://www.timeshighereducation.com/student/where-to-study/study-in-morocco"}], status=P)
add("MA-ACAD-016", "Q19407257", "Mohammed VI University of Health Sciences (UM6SS)", "ACAD", "University",
    "Private health sciences university in Casablanca founded 2014.",
    aliases=["جامعة محمد السادس لعلوم الصحة", "UM6SS"],
    founded="2014-01-01", website="http://www.um6ss.ma", status=P)
add("MA-ACAD-017", "Q140915110", "Mohammadia School of Engineers (EMI)", "ACAD", "Engineering School",
    "Historic Moroccan engineering school in Rabat founded 1946.",
    aliases=["المدرسة المحمدية للمهندسين", "École Mohammadia d'Ingénieurs"],
    founded="1946-01-01", website="http://www.emi.ac.ma/", status=P)
add("MA-ACAD-018", "Q3577670", "École Hassania des Travaux Publics (EHTP)", "ACAD", "Engineering School",
    "Prestigious Moroccan engineering school for public works in Casablanca.",
    aliases=["المدرسة الحسنية للأشغال العمومية"],
    founded="1971-01-01", website="http://www.ehtp.ac.ma/", status=P)
add("MA-ACAD-019", "Q2737222", "National Institute of Statistics and Applied Economics (INSEA)", "ACAD", "Statistics Institute",
    "Moroccan graduate school of statistics and economics in Rabat.",
    aliases=["المعهد الوطني للإحصاء والاقتصاد التطبيقي"],
    founded="1961-01-01", website="https://insea.ac.ma/", status=P)
add("MA-ACAD-020", "Q3151828", "Institut Agronomique et Vétérinaire Hassan II (IAV)", "ACAD", "Engineering School",
    "Moroccan agronomy and veterinary institute in Rabat.",
    aliases=["معهد الحسن الثاني للزراعة والبيطرة"],
    founded="1966-01-01", website="http://www.iav.ac.ma", status=P)
add("MA-ACAD-021", "Q3578067", "École Nationale d'Administration (Rabat)", "ACAD", "Public Administration School",
    "Moroccan national school training senior civil servants, founded 1948.",
    aliases=["المدرسة الوطنية للإدارة المغربية", "ENA"],
    founded="1948-03-08", status=P)
add("MA-ACAD-022", "Q30281767", "Institut Pasteur du Maroc", "ACAD", "Research Institute",
    "Moroccan public health research institute founded 1911, member of the Pasteur Network.",
    aliases=["معهد باستور المغرب"],
    founded="1911-01-01", website="http://www.pasteur.ma/", status=P)
add("MA-ACAD-023", "Q30284534", "Centre National pour la Recherche Scientifique et Technique (CNRST)", "ACAD", "Research Institute",
    "Moroccan national research council in Rabat, operator of IMIST.",
    aliases=["المركز الوطني للبحث العلمي والتقني"],
    status=P)
add("MA-ACAD-024", "Q30261797", "King Abdul-Aziz Al Saoud Foundation for Islamic Studies", "ACAD", "Research Institute",
    "Documentation, scientific and cultural institute in Casablanca.",
    aliases=["مؤسسة الملك عبد العزيز آل سعود"],
    status=P)

# ---------------- MEDIA ----------------
add("MA-MEDIA-001", "Q27491", "Société Nationale de Radio et Télévision (SNRT)", "MEDIA", "Public Broadcaster",
    "Morocco's state-owned public broadcaster, operating Al Aoula, 2M stake, radio stations and regional channels.",
    aliases=["الشركة الوطنية للإذاعة والتلفزة", "SNRT Group", "ex-RTM"],
    extra_sources=[{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Soci%C3%A9t%C3%A9_Nationale_de_Radio_et_T%C3%A9l%C3%A9vision"},
                   {"type": "official_website", "url": "https://www.snrt.ma/"}], status=V)
add("MA-MEDIA-002", "Q2276749", "Al Aoula", "MEDIA", "TV Channel",
    "Moroccan public flagship television channel operated by SNRT.",
    aliases=["الأولى", "Al Aoula TV"],
    parent="Société Nationale de Radio et Télévision (SNRT)", status=V)
add("MA-MEDIA-003", "Q222061", "2M (TV channel)", "MEDIA", "TV Channel",
    "Second Moroccan national television channel, state-owned (SOREAD-2M).",
    aliases=["الدوزيم", "2M Maroc"],
    extra_sources=[{"type": "official_website", "url": "https://www.2m.ma/"}], status=V)
add("MA-MEDIA-004", "Q2401659", "Maghreb Arabe Presse (MAP)", "MEDIA", "News Agency",
    "Morocco's official state news agency founded in 1959.",
    aliases=["وكالة المغرب العربي للأنباء", "MAP", "Maghreb Arabe Press"],
    founded="1959-01-01",
    extra_sources=[{"type": "official_website", "url": "https://www.mapnews.ma/"}], status=V)
add("MA-MEDIA-005", "Q3303949", "Medi 1 TV", "MEDIA", "TV Channel",
    "Moroccan news channel broadcasting in Arabic and French (Tanger-based).",
    aliases=["مدي 1 تي في"],
    extra_sources=[{"type": "official_website", "url": "https://www.medi1tv.com/"}], status=V)
add("MA-MEDIA-006", "Q3224400", "Le Matin (Morocco)", "MEDIA", "Newspaper",
    "Daily francophone Moroccan newspaper, historically close to the palace.",
    aliases=["صباح", "Le Matin du Sahara"],
    extra_sources=[{"type": "official_website", "url": "https://lematin.ma/"}], status=V)
add("MA-MEDIA-007", "Q4808310", "Assabah", "MEDIA", "Newspaper",
    "Daily Arabophone Moroccan newspaper.",
    aliases=["الصباح"],
    extra_sources=[{"type": "official_website", "url": "https://assabah.ma/"}], status=V)
add("MA-MEDIA-008", "Q2743630", "Al Massae", "MEDIA", "Newspaper",
    "Major Moroccan Arabic daily newspaper founded 2003 by Rachid Nini.",
    aliases=["المساء"],
    status=P)
add("MA-MEDIA-009", "Q12249940", "Hespress", "MEDIA", "Online News",
    "Most-visited Moroccan online news website.",
    aliases=["هسبريس"],
    extra_sources=[{"type": "official_website", "url": "https://en.hespress.com/"}], status=V)
add("MA-MEDIA-010", "Q1115018", "TelQuel (Morocco)", "MEDIA", "News Magazine",
    "Weekly French-language news magazine in Morocco.",
    aliases=["تلكيال"],
    extra_sources=[{"type": "official_website", "url": "https://telquel.ma/"}], status=V)

# ---------------- PARTY ----------------
elect_src = {"type": "web_search", "url": "https://moroccoelections.com/en/"}
add("MA-PARTY-001", "Q1255232", "Justice and Development Party (Morocco)", "PARTY", "Islamist Conservative",
    "Moroccan Islamist-conservative party (PJD), governing party 2011-2021, 54 seats in 2026 legislative elections.",
    aliases=["حزب العدالة والتنمية", "PJD"],
    founded="1967-01-01", website="https://www.pjd.ma/",
    extra_sources=[elect_src], status=V)
add("MA-PARTY-002", "Q1630297", "National Rally of Independents (RNI)", "PARTY", "Liberal Centrist",
    "Moroccan liberal party (RNI) founded 1978 by Ahmed Osman; led the governing coalition under Akhannouch; 66 seats in 2026 elections.",
    aliases=["التجمع الوطني للأحرار", "RNI"],
    founded="1978-01-01", website="http://www.rni.ma",
    key_people=[{"title": "President", "name": "Aziz Akhannouch", "since": "2016"}],
    extra_sources=[elect_src], status=V)
add("MA-PARTY-003", "Q784586", "Authenticity and Modernity Party (PAM)", "PARTY", "Centrist Secular",
    "Moroccan centrist party (PAM) founded 2008; came first with 97 seats in the 2026 legislative elections.",
    aliases=["حزب الأصالة والمعاصرة", "PAM"],
    founded="2008-08-07", website="http://www.pam.ma/",
    extra_sources=[elect_src,
                   {"type": "news_search", "url": "https://en.le360.ma/politics/2026-legislative-elections-a-new-political-hierarchy-and-multiple-coalition-options_U773JLLOJVESPNG2EKS22XZ6SE/"}],
    status=V)
add("MA-PARTY-004", "Q477273", "Istiqlal Party", "PARTY", "Nationalist Conservative",
    "Historic Moroccan nationalist party founded 1943 during the independence movement; 65 seats in 2026 elections.",
    aliases=["حزب الاستقلال", "Independence Party"],
    founded="1943-01-01", website="http://www.istiqlal.info/",
    extra_sources=[elect_src], status=V)
add("MA-PARTY-005", "Q2297130", "Socialist Union of Popular Forces (USFP)", "PARTY", "Social Democratic",
    "Moroccan social-democratic party, governing party 1998-2011.",
    aliases=["الاتحاد الاشتراكي للقوات الشعبية", "USFP"],
    founded="1975-01-01", website="http://www.usfp.ma/", status=P)
add("MA-PARTY-006", "Q1471276", "Popular Movement (MP)", "PARTY", "Centrist Amazigh",
    "Moroccan centrist party founded 1957.",
    aliases=["الحركة الشعبية", "MP"],
    founded="1957-09-28", website="http://www.alharaka.ma/", status=P)
add("MA-PARTY-007", "Q1888857", "Party of Progress and Socialism (PPS)", "PARTY", "Left-wing",
    "Moroccan left-wing party (ex-communist).",
    aliases=["حزب التقدم والاشتراكية", "PPS"],
    founded="1974-08-23", website="http://www.ppsmaroc.com", status=P)
add("MA-PARTY-008", "Q692325", "National Union of Popular Forces (UNFP)", "PARTY", "Socialist",
    "Historic Moroccan socialist party founded 1959, precursor of the USFP.",
    aliases=["الاتحاد الوطني للقوات الشعبية", "UNFP"],
    founded="1959-01-01", status=P)
add("MA-PARTY-009", "Q3550065", "Constitutional Union (UC)", "PARTY", "Liberal Conservative",
    "Moroccan liberal-conservative party founded 1983.",
    aliases=["الاتحاد الدستوري", "UC"],
    founded="1983-04-10", website="http://possible.ma/", status=P)
add("MA-PARTY-010", "Q3088478", "Front of Democratic Forces (FFD)", "PARTY", "Social Democratic",
    "Moroccan social-democratic party founded 1997 by Thami El Khyari.",
    aliases=["جبهة القوات الديمقراطية", "FFD"],
    founded="1997-07-27", website="http://www.ffd.ma/", status=P)

# ---------------- INTL (HQ in Morocco) ----------------
add("MA-INTL-001", "Q1264411", "ICESCO (Islamic World Educational, Scientific and Cultural Organization)", "INTL", "International Organization",
    "Islamic world educational, scientific and cultural organization headquartered in Rabat.",
    aliases=["الإيسيسكو", "ICESCO"],
    website="https://www.icesco.org/",
    extra_sources=[{"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Islamic_World_Educational,_Scientific_and_Cultural_Organization"}], status=V)
add("MA-INTL-002", "Q22686285", "Arab Civil Aviation Commission (ACAC)", "INTL", "International Organization",
    "Arab civil aviation body headquartered in Rabat.",
    aliases=["لجنة الطيران المدني العربي", "ACAC"],
    status=P)
add("MA-INTL-003", "Q2974848", "United Cities and Local Governments of Africa (UCLG Africa)", "INTL", "International Organization",
    "African regional section of UCLG, headquartered in Rabat.",
    aliases=["أفريقيا للمدن والحكومات المحلية", "UCLG Africa"],
    status=P)

# ---------------- summary ----------------
from collections import Counter, defaultdict
cat_count = Counter(o['category'] for o in orgs)
by_cat = defaultdict(list)
for o in orgs:
    by_cat[o['category']].append(o)

TOP = {
    "GOV": ["Ministry of Foreign Affairs, African Cooperation and Moroccan Expatriates", "Government of Morocco", "Parliament of Morocco"],
    "SOE": ["OCP Group", "ONCF (Office National des Chemins de Fer)", "Caisse de Dépôt et de Gestion (Morocco)"],
    "CORP": ["Maroc Telecom", "Inwi", "Akwa Group"],
    "NGO": ["Moroccan Association for Human Rights", "Transparency Maroc", "High Atlas Foundation"],
    "ACAD": ["University of al-Qarawiyyin", "Mohammed V University (Rabat)", "Mohammed VI Polytechnic University (UM6P)"],
    "MEDIA": ["Société Nationale de Radio et Télévision (SNRT)", "Maghreb Arabe Presse (MAP)", "Hespress"],
    "FIN": ["Bank Al-Maghrib", "Attijariwafa Bank", "Banque Centrale Populaire (BCP Group)"],
    "INTL": ["ICESCO (Islamic World Educational, Scientific and Cultural Organization)", "Arab Civil Aviation Commission (ACAC)", "United Cities and Local Governments of Africa (UCLG Africa)"],
    "PARTY": ["Justice and Development Party (Morocco)", "National Rally of Independents (RNI)", "Authenticity and Modernity Party (PAM)"],
    "MIL": ["Royal Moroccan Armed Forces", "Royal Moroccan Gendarmerie", "General Directorate of Territorial Surveillance (Morocco)"],
}

order = ["GOV", "SOE", "CORP", "NGO", "ACAD", "MEDIA", "FIN", "INTL", "PARTY", "MIL"]
by_category = {}
for c in order:
    lst = by_cat.get(c, [])
    by_category[c] = {
        "count": len(lst),
        "top_orgs": TOP[c][:3],
    }

verified = sum(1 for o in orgs if o['verification_status'] == 'verified')
n = len(orgs)
result = {
    "metadata": {
        "country": "Morocco",
        "country_iso": "MA",
        "country_qid": "Q1028",
        "collection_date": "2026-10-05",
        "phase": "phase1_broad_scan",
        "categories_covered": order,
        "depth": "overview",
        "total_organizations": n,
    },
    "organizations": orgs,
    "summary": {
        "by_category": by_category,
        "data_quality": {
            "verified_count": verified,
            "unverified_count": n - verified,
            "completeness_pct": round(verified / n * 100),
        },
    },
}

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"written {n} orgs to {OUT}")
print(dict(cat_count))
