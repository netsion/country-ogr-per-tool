# -*- coding: utf-8 -*-
"""Build _target_orgs.json for Bolivia (BO, Q750) from collected SPARQL/Wikipedia/web-search data."""
import json
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SPARQL_DIR = os.path.join(BASE, "sparql")
OUT_PATH = os.path.join(BASE, "_target_orgs.json")

COUNTRY = "BO"
DATE = "2026-10-24"

# ---------------------------------------------------------------- load SPARQL enrichment index
SPARQL_FILES = [
    "H_state_organs", "A_general", "B_corp", "C_acad", "D_party", "E_media",
    "F_fin", "SOE", "NGO", "MIL", "supp_ministries", "supp_state_enterprises",
    "supp_military", "supp_media",
]

def qid_of(uri: str) -> str:
    return uri.rsplit("/", 1)[-1]

def norm_date(v):
    if not v:
        return None
    v = str(v).lstrip("+")
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", v)
    return m.group(1) if m else None

index = {}

def merge_row(q, **kw):
    rec = index.setdefault(q, {})
    for k, v in kw.items():
        if v and not rec.get(k):
            rec[k] = v

for fn in SPARQL_FILES:
    path = os.path.join(SPARQL_DIR, fn + ".json")
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    for b in data.get("results", {}).get("bindings", []):
        q = qid_of(b["org"]["value"])
        name_es = b.get("nameEs", {}).get("value")
        name_en = b.get("nameEn", {}).get("value")
        label = b.get("orgLabel", {}).get("value")
        desc = b.get("orgDescription", {}).get("value")
        website = b.get("website", {}).get("value")
        founded = norm_date((b.get("inception") or b.get("founded") or b.get("established") or {}).get("value"))
        hq = b.get("hqLabel", {}).get("value")
        merge_row(q, name_es=name_es, name_en=name_en, label=label, desc=desc, website=website, founded=founded, hq=hq)

# ---------------------------------------------------------------- load verification results
verify = {}
path = os.path.join(BASE, "verify_results.json")
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        verify = json.load(f)

VERIFY_URL = {
    # key -> (wikidata_key_in_verify, wiki_source_url)
}
def wiki_sources(key):
    v = verify.get(key)
    out = []
    if not v:
        return out
    if v.get("wikibase_item"):
        pass  # QID handled separately
    sp = v.get("source_page")
    if sp and ":" in sp:
        lang, title = sp.split(":", 1)
        out.append({"type": "wikipedia", "url": f"https://{lang}.wikipedia.org/wiki/{title.replace(' ', '_')}"})
    return out

# ---------------------------------------------------------------- curated entry definitions
# name_zh: only well-established translations (Xinhua/zh-Wikipedia usage); else None.

WIKI = {}  # key -> wikibase_item from verify step
for k, v in verify.items():
    if v and v.get("wikibase_item"):
        WIKI[k] = v["wikibase_item"]

SRC_OAS = {"type": "web_search", "url": "https://www.oas.org/ext/en/main/oas/member-states/national-authorities/country/id/689"}
SRC_CIA = {"type": "web_search", "url": "https://www.cia.gov/resources/world-leaders/foreign-governments/bolivia"}
SRC_POLITICS = {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Politics_of_Bolivia"}
SRC_OEP = {"type": "official_website", "url": "https://web.oep.org.bo/organizaciones-politicas/organizaciones-alcance-nacional/"}
SRC_MERCO = {"type": "web_search", "url": "https://www.merco.info/bo/ranking-merco-empresas"}
SRC_MERGR = {"type": "web_search", "url": "https://mergr.com/companies/bolivia/largest"}
SRC_ZOOMINFO = {"type": "web_search", "url": "https://www.zoominfo.com/top-lists/top-companies-in-BO"}
SRC_BBC = {"type": "web_search", "url": "https://www.bbc.com/news/world-latin-america-18729332"}
SRC_SCRIBD_INST = {"type": "web_search", "url": "https://www.scribd.com/document/472290247/LISTA-DE-INSTITUCIONES-PUBLICAS-BOLIVIA"}
SRC_SDSN = {"type": "web_search", "url": "https://www.unsdsn.org/our-networks/bolivia/"}
SRC_BORGEN = {"type": "web_search", "url": "https://borgenproject.org/5-charities-operating-in-bolivia/"}
SRC_SOBOCE = {"type": "official_website", "url": "https://soboce.com/"}
SRC_BNAMERICAS_SOBOCE = {"type": "web_search", "url": "https://www.bnamericas.com/es/perfil-empresa/sociedad-boliviana-de-cemento-sa"}
SRC_ERBOL = {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/ERBOL"}
SRC_UNITY = {"type": "wikipedia", "url": "https://en.wikipedia.org/wiki/Unity_(Bolivia)"}
SRC_COMPANYDATA = {"type": "web_search", "url": "https://companydata.com/bolivia/"}

E = []
def org(cat, sub, qid=None, key=None, name=None, aliases=(), website=None, founded=None,
        hq=None, desc=None, name_en=None, name_zh=None, parent=None, people=(), rels=(), extra_sources=()):
    E.append(dict(cat=cat, sub=sub, qid=qid, key=key, name=name, aliases=list(aliases),
                  website=website, founded=founded, hq=hq, desc=desc, name_en=name_en,
                  name_zh=name_zh, parent=parent, people=list(people), rels=list(rels),
                  extra_sources=list(extra_sources)))

# ============================ GOV ============================
org("GOV", "head_of_state_office", qid="Q373548", key="Presidente_gov", name="Presidente de Bolivia",
    aliases=["Presidencia del Estado Plurinacional de Bolivia"],
    desc="jefe de Estado y Gobierno de Bolivia",
    name_en="President of Bolivia", name_zh="玻利维亚总统",
    people=[
        {"title": "Presidente del Estado Plurinacional", "name": "Rodrigo Paz Pereira", "since": "2025-11-08"},
        {"title": "Vicepresidente del Estado Plurinacional", "name": "Edman Lara Montaño", "since": "2025-11-08"},
    ], extra_sources=[SRC_OAS, SRC_CIA])
org("GOV", "ministry", qid="Q6866989", name="Ministerio de Relaciones Exteriores", aliases=["Cancillería de Bolivia", "MRE"],
    people=[{"title": "Ministro de Relaciones Exteriores", "name": "Fernando Hugo Aramayo Carrasco", "since": None}],
    extra_sources=[SRC_OAS])
org("GOV", "ministry", qid="Q16607736", name="Ministerio de Gobierno", aliases=["Ministerio de Gobierno de Bolivia"],
    desc="ministry of the Bolivian government (interior)")
org("GOV", "ministry", qid="Q44225409", name="Ministerio de Defensa",
    people=[{"title": "Ministro de Defensa", "name": "Ernesto Amilcar Justiniano Hurtado", "since": None}],
    extra_sources=[SRC_CIA])
org("GOV", "ministry", qid="Q16607730", name="Ministerio de Economía y Finanzas Públicas", aliases=["MEFP"])
org("GOV", "ministry", qid="Q61835455", name="Ministerio de la Presidencia")
org("GOV", "ministry", qid="Q44225411", name="Ministerio de Salud")
org("GOV", "ministry", qid="Q25414135", name="Ministerio de Educación")
org("GOV", "ministry", qid="Q51737043", name="Ministerio de Justicia")
org("GOV", "ministry", qid="Q4294751", name="Ministerio de Trabajo, Empleo y Previsión Social")
org("GOV", "ministry", qid="Q4294431", name="Ministerio de Culturas y Turismo")
org("GOV", "ministry", qid="Q56317840", name="Ministerio de Desarrollo Productivo y Economía Plural")
org("GOV", "ministry", qid="Q42331387", name="Ministerio de Obras Públicas, Servicios y Vivienda")
org("GOV", "ministry", qid="Q62005843", name="Ministerio de Minería y Metalurgia")
org("GOV", "ministry", qid="Q52536720", name="Ministerio de Hidrocarburos y Energías")
org("GOV", "ministry", qid="Q56316758", name="Ministerio de Medio Ambiente y Agua")
org("GOV", "ministry", qid="Q60830049", name="Ministerio de Planificación del Desarrollo")
org("GOV", "ministry", qid="Q105752851", name="Ministerio de Desarrollo Rural y Tierras", aliases=["MDRyT"])
org("GOV", "ministry", qid="Q4294279", name="Ministerio de Autonomías")
org("GOV", "ministry", qid="Q54853188", name="Ministerio de Deportes")
org("GOV", "legislature", qid="Q1968458", key="ALP_gov", name="Asamblea Legislativa Plurinacional", aliases=["ALP"],
    desc="parlamento bicameral boliviano (Cámara de Diputados y Cámara de Senadores)",
    name_en="Plurinational Legislative Assembly", name_zh="多民族立法议会")
org("GOV", "judiciary", qid="Q2999600", name="Tribunal Supremo de Justicia de Bolivia", aliases=["TSJ"],
    desc="supreme court of Bolivia (ordinary jurisdiction)",
    name_en="Supreme Tribunal of Justice of Bolivia")
org("GOV", "judiciary", qid="Q7205559", name="Tribunal Constitucional Plurinacional", aliases=["TCP"],
    name_en="Plurinational Constitutional Court")
org("GOV", "judiciary", name="Tribunal Agroambiental",
    desc="tribunal especializado agrario y ambiental de Bolivia (órgano constitucional del Sistema Judicial)",
    extra_sources=[SRC_POLITICS])
org("GOV", "judiciary", qid="Q2999936", name="Consejo de la Judicatura",
    website="http://magistratura.organojudicial.gob.bo/")
org("GOV", "electoral_body", key="TSE_gov", name="Órgano Electoral Plurinacional", aliases=["Tribunal Supremo Electoral", "TSE", "OEP"],
    desc="órgano electoral de Bolivia (Tribunal Supremo Electoral)",
    website="https://web.oep.org.bo", extra_sources=[SRC_OEP])
org("GOV", "oversight", qid="Q28663691", key="Contraloria_gov", name="Contraloría General del Estado", aliases=["CGE"],
    desc="Organismo superior técnico de control de cuentas de recursos del Estado",
    name_en="Office of the Comptroller General of Bolivia", website="https://www.contraloria.gob.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.contraloria.gob.bo"}])
org("GOV", "oversight", qid="Q60919785", key="Defensoria_gov", name="Defensoría del Pueblo de Bolivia",
    name_en="Defender of the People (Bolivia)")
org("GOV", "prosecution", qid="Q57275461", name="Ministerio Público de Bolivia", aliases=["Fiscalía General del Estado"])
org("GOV", "statistical_agency", qid="Q1818139", key="INE_gov", name="Instituto Nacional de Estadística de Bolivia", aliases=["INE"],
    desc="institución gubernamental encargada de las estadísticas oficiales",
    name_en="National Institute of Statistics of Bolivia", website="https://www.ine.gob.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.ine.gob.bo"}])
org("GOV", "tax_agency", name="Servicio de Impuestos Nacionales", aliases=["SIN"],
    website="https://www.impuestos.com.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.impuestos.com.bo"}])
org("GOV", "regulator", name="Autoridad de Regulación y Fiscalización de Telecomunicaciones y Transportes", aliases=["ATT"],
    website="https://www.att.gob.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.att.gob.bo"}])
org("GOV", "executive_agency", qid="Q28715", name="Agencia para el Desarrollo de la Sociedad de la Información", aliases=["ADSIB"])
org("GOV", "executive_agency", qid="Q936350", name="Dirección General de Aeronáutica Civil", aliases=["DGAC"])
org("GOV", "executive_agency", qid="Q4090805", name="Agencia Boliviana Espacial", aliases=["ABE"],
    desc="national space agency of Bolivia")
org("GOV", "executive_agency", qid="Q111522234", name="Servicio Nacional de Hidrología y Meteorología", aliases=["SENAMHI"])
org("GOV", "executive_agency", qid="Q125396534", name="Administradora Boliviana de Carreteras", aliases=["ABC"])
org("GOV", "executive_agency", qid="Q126961073", name="Agencia Nacional de Hidrocarburos", aliases=["ANH"])
org("GOV", "executive_agency", qid="Q6126064", name="Servicio Nacional de Áreas Protegidas", aliases=["SERNAP"],
    desc="state authority for protected areas of Bolivia")
org("GOV", "executive_agency", qid="Q111636365", name="Servicio Geológico Minero", aliases=["SERGEOMIN"])

# ============================ SOE ============================
org("SOE", "oil_and_gas", qid="Q1807091", name="Yacimientos Petrolíferos Fiscales Bolivianos", aliases=["YPFB"],
    desc="empresa estatal boliviana de petróleo y gas; la mayor empresa del país por ingresos",
    name_en="Bolivian Fiscal Oilfields", name_zh="玻利维亚国家石油公司",
    rels=[{"type": "has_subsidiary", "target_name": "YPFB Transporte"}],
    extra_sources=[SRC_ZOOMINFO])
org("SOE", "mining", qid="Q1134645", name="Corporación Minera de Bolivia", aliases=["COMIBOL"],
    desc="Bolivian state mining corporation")
org("SOE", "electricity", qid="Q5816178", name="Empresa Nacional de Electricidad", aliases=["ENDE", "ENDE Corporación"],
    desc="Empresa pública boliviana de electricidad", website="https://www.ende.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.ende.bo"}])
org("SOE", "telecommunications", qid="Q3054977", name="Entel Bolivia", aliases=["ENTEL", "Empresa Nacional de Telecomunicaciones"],
    desc="Empresa Boliviana Estatal de Telecomunicaciones")
org("SOE", "aviation", qid="Q891372", name="Boliviana de Aviación", aliases=["BoA"],
    desc="línea aérea de bandera de Bolivia (empresa pública)", name_en="Boliviana de Aviación", name_zh="玻利维亚航空",
    website="https://www.boa.bo", extra_sources=[{"type": "official_website", "url": "https://www.boa.bo"}])
org("SOE", "lithium", qid="Q57451059", name="Yacimientos de Litio Bolivianos", aliases=["YLB"],
    desc="empresa pública estatal de litio de Bolivia")
org("SOE", "urban_transport", qid="Q16472522", name="Mi Teleférico",
    desc="sistema de teleférico urbano de La Paz y El Alto (empresa pública)",
    name_en="Mi Teleférico", website="https://miteleferico.bo",
    extra_sources=[{"type": "official_website", "url": "https://miteleferico.bo"}])
org("SOE", "food", name="Empresa de Apoyo a la Producción de Alimentos", aliases=["Emapa"],
    website="https://www.emapa.gob.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.emapa.gob.bo"}])
org("SOE", "steel", qid="Q132798272", name="Siderúrgica del Mutún",
    desc="empresa pública siderúrgica (planta del Mutún, Puerto Suárez)")

# ============================ CORP ============================
org("CORP", "beverages", qid="Q2946943", name="Cervecería Boliviana Nacional", aliases=["CBN"],
    desc="empresa cervecera boliviana líder del sector bebidas; parte del grupo AB InBev",
    rels=[{"type": "owned_by", "target_name": "AB InBev"}],
    extra_sources=[SRC_MERCO])
org("CORP", "beverages", name="EMBOL", aliases=["Embotelladora Boliviana S.A."],
    desc="embotelladora de productos Coca-Cola en Bolivia (Cochabamba)",
    extra_sources=[SRC_MERCO])
org("CORP", "pharmacy_retail", qid="Q81968937", name="Farmacorp",
    desc="cadena boliviana de farmacias",
    extra_sources=[SRC_MERCO])
org("CORP", "retail", qid="Q81968262", name="Hipermaxi",
    desc="cadena de supermercados en Bolivia", extra_sources=[SRC_COMPANYDATA])
org("CORP", "cement", name="Sociedad Boliviana de Cemento S.A.", aliases=["SOBOCE"],
    desc="empresa líder en producción y comercialización de cemento en Bolivia",
    website="https://soboce.com", founded="1925-09-24",
    extra_sources=[SRC_SOBOCE, SRC_BNAMERICAS_SOBOCE])
org("CORP", "food", name="Industrias de Aceite Sofía", aliases=["Sofía Ltda."],
    desc="empresa boliviana de aceites y alimentos consumos, entre las mayores privadas del país",
    extra_sources=[SRC_MERCO])
org("CORP", "mining", qid="Q5555501", name="Minera San Cristóbal",
    desc="mina de zinc-plomo-plata en Potosí, una de las mayores empresas del país por ingresos",
    rels=[{"type": "owned_by", "target_name": "Sumitomo Corporation"}],
    extra_sources=[SRC_ZOOMINFO])
org("CORP", "telecommunications", qid="Q10952410", name="Tigo Bolivia",
    desc="operador de telecomunicaciones en Bolivia (marca Tigo del grupo Millicom)",
    rels=[{"type": "subsidiary_of", "target_name": "Millicom International Cellular"}])
org("CORP", "telecommunications", qid="Q56015581", name="Viva",
    desc="operador de telecomunicaciones boliviano (antigua Telefónica Bolivia, adquirida por Millicom)",
    rels=[{"type": "acquired_by", "target_name": "Millicom International Cellular"}])
org("CORP", "energy_transport", name="Gas TransBoliviano S.A.", aliases=["GTB"],
    desc="transportadora de gas natural por ductos en Bolivia",
    extra_sources=[SRC_MERGR])

# ============================ NGO ============================
org("NGO", "labor_union", qid="Q1053929", name="Central Obrera Boliviana", aliases=["COB"],
    desc="Organización central sindical de Bolivia", name_zh="玻利维亚工人中央工会")
org("NGO", "business_association", name="Confederación de Empresarios Privados de Bolivia", aliases=["CEPB"],
    website="https://www.cepb.org.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.cepb.org.bo"}])
org("NGO", "development", qid="Q24949729", name="Centro de investigación y promoción del campesinado", aliases=["CIPCA"],
    desc="organización boliviana de investigación y promoción del campesinado (1970-)")
org("NGO", "environment", qid="Q100956247", name="Fundación Tierra", aliases=["FTierra"],
    desc="fundación boliviana de investigación y desarrollo (temas de tierra y territorio)")
org("NGO", "human_rights", name="Asamblea Permanente de los Derechos Humanos de Bolivia", aliases=["APDHB"],
    extra_sources=[SRC_SCRIBD_INST])
org("NGO", "wildlife_conservation", qid="Q5157850", name="Comunidad Inti Wara Yassi",
    desc="organización boliviana de conservación de fauna")
org("NGO", "cultural_foundation", qid="Q115271356", name="Fundación Patiño",
    desc="fundación cultural y filantrópica boliviana (herencia de Simón I. Patiño)")
org("NGO", "child_welfare", qid="Q137383399", name="Aldeas Infantiles SOS Bolivia",
    desc="organización nacional de Aldeas Infantiles SOS en Bolivia",
    rels=[{"type": "member_of", "target_name": "SOS Children's Villages International"}])
org("NGO", "child_welfare", qid="Q137590984", name="World Vision Bolivia",
    desc="socio nacional de World Vision en Bolivia",
    rels=[{"type": "member_of", "target_name": "World Vision International"}])
org("NGO", "child_welfare", qid="Q30288293", name="Plan International Bolivia",
    rels=[{"type": "part_of", "target_name": "Plan International"}])
org("NGO", "environment", qid="Q132472253", name="WWF Bolivia",
    desc="oficina nacional del Fondo Mundial para la Naturaleza en Bolivia",
    rels=[{"type": "part_of", "target_name": "WWF International"}])
org("NGO", "education", qid="Q5856947", name="Fe y Alegría Bolivia",
    desc="movimiento de educación popular presente en Bolivia (red internacional Fe y Alegría)",
    rels=[{"type": "part_of", "target_name": "Fe y Alegría (red internacional)"}])
org("NGO", "research", qid="Q30293536", name="Observatorio San Calixto",
    desc="institución científica y social en La Paz (sismología y derechos humanos)")
org("NGO", "environment", name="PRODENA", aliases=["Asociación Boliviana Pro Defensa de la Naturaleza"],
    desc="asociación boliviana de defensa de la naturaleza",
    extra_sources=[SRC_SDSN])
org("NGO", "human_rights", name="Fundación Bolivia Digna",
    desc="ONG boliviana de promoción y defensa de derechos, con base en Cochabamba (2006)",
    hq="Cochabamba", founded="2006-01-01", extra_sources=[SRC_BORGEN])

# ============================ ACAD ============================
org("ACAD", "public_university", qid="Q3290454", name="Universidad Mayor de San Andrés", aliases=["UMSA"],
    desc="universidad pública de La Paz, la mayor de Bolivia")
org("ACAD", "public_university", qid="Q1767912", name="Universidad Mayor de San Simón", aliases=["UMSS"],
    desc="universidad pública de Cochabamba")
org("ACAD", "public_university", qid="Q7894237", name="Universidad Autónoma Gabriel René Moreno", aliases=["UAGRM"],
    desc="universidad pública de Santa Cruz de la Sierra")
org("ACAD", "public_university", qid="Q930279", name="Universidad Mayor, Real y Pontificia San Francisco Xavier de Chuquisaca",
    aliases=["USFX", "Universidad de San Francisco Xavier"], desc="universidad pública de Sucre, fundada en la época colonial")
org("ACAD", "public_university", qid="Q7894325", name="Universidad Técnica de Oruro", aliases=["UTO"])
org("ACAD", "public_university", qid="Q10968607", name="Universidad Pública de El Alto", aliases=["UPEA"])
org("ACAD", "public_university", qid="Q30294055", name="Universidad Autónoma Juan Misael Saracho", aliases=["UAJMS"])
org("ACAD", "private_university", qid="Q2495675", name="Universidad Católica Boliviana San Pablo", aliases=["UCB"])
org("ACAD", "private_university", qid="Q6155045", name="Universidad Privada Boliviana", aliases=["UPB"],
    website="https://www.upb.edu.bo", extra_sources=[{"type": "official_website", "url": "https://www.upb.edu.bo"}])
org("ACAD", "private_university", qid="Q9091601", name="Universidad Privada de Santa Cruz de la Sierra", aliases=["UPSA"])
org("ACAD", "private_university", qid="Q9091606", name="Universidad Privada del Valle", aliases=["Univalle"])
org("ACAD", "private_university", qid="Q9091593", name="Universidad Privada Franz Tamayo", aliases=["UDEM"])
org("ACAD", "private_university", qid="Q7069999", name="Universidad Núr", aliases=["NUR"])
org("ACAD", "private_university", qid="Q10387889", name="Universidad de Aquino Bolivia", aliases=["UDABOL"])
org("ACAD", "private_university", qid="Q2495648", name="Universidad Andina Simón Bolívar", aliases=["UASB"],
    desc="universidad del Sistema Andino de Integración con sede en Bolivia")
org("ACAD", "academy", qid="Q30266822", name="Academia Nacional de Ciencias de Bolivia",
    desc="research institute")

# ============================ MEDIA ============================
org("MEDIA", "newspaper", qid="Q5351111", name="El Deber",
    desc="periódico de Santa Cruz de la Sierra, de mayor circulación del país", website="https://eldeber.com.bo")
org("MEDIA", "newspaper", qid="Q6683294", name="Los Tiempos",
    desc="periódico de Cochabamba", website="https://www.lostiempos.com")
org("MEDIA", "newspaper", name="La Razón",
    desc="periódico de La Paz", website="http://www.la-razon.com", extra_sources=[SRC_BBC])
org("MEDIA", "newspaper", qid="Q1324064", name="El Diario",
    desc="periódico de La Paz", website="http://www.eldiario.net")
org("MEDIA", "newspaper", qid="Q7098285", name="Opinión",
    desc="periódico de Cochabamba", website="https://www.opinion.com.bo")
org("MEDIA", "newspaper", name="El Mundo",
    desc="periódico de Santa Cruz de la Sierra", website="https://elmundo.com.bo", extra_sources=[SRC_BBC])
org("MEDIA", "newspaper", name="Correo del Sur",
    desc="periódico de Sucre", website="http://correodelsur.com", extra_sources=[SRC_BBC])
org("MEDIA", "television", qid="Q2457700", name="Unitel",
    desc="canal de televisión abierta privado (Santa Cruz)", website="https://www.unitel.bo",
    extra_sources=[SRC_BBC])
org("MEDIA", "television", qid="Q2756386", name="Bolivisión",
    desc="Canal de TV abierta en Bolivia")
org("MEDIA", "television", qid="Q3422796", name="Red Uno", aliases=["Canal 11"],
    desc="canal de televisión abierta privado (La Paz)", website="http://www.reduno.com.bo", extra_sources=[SRC_BBC])
org("MEDIA", "television", qid="Q3422654", name="ATB", aliases=["Red ATB"],
    desc="canal de televisión abierta privado (La Paz)", website="http://www.atb.com.bo", extra_sources=[SRC_BBC])
org("MEDIA", "television", qid="Q2756421", name="Bolivia TV", aliases=["Canal 7", "Televisión Boliviana"],
    desc="canal de televisión estatal", website="http://www.boliviatv.bo", extra_sources=[SRC_BBC])
org("MEDIA", "radio", name="ERBOL",
    desc="red boliviana de emisoras de radio", website="https://www.erbol.com.bo", extra_sources=[SRC_ERBOL])
org("MEDIA", "radio", qid="Q6096338", name="Radio Fides",
    desc="emisora católica de noticias y actualidad", website="http://radiofides.com", extra_sources=[SRC_BBC])
org("MEDIA", "radio", name="Radio Panamericana",
    desc="red nacional de radio (noticias y actualidad)", website="https://panamericana.bo", extra_sources=[SRC_BBC])
org("MEDIA", "radio", name="Red Patria Nueva",
    desc="red estatal de radios comunitarias", website="https://redpatrianueva.bo", extra_sources=[SRC_BBC])
org("MEDIA", "news_agency", qid="Q2826717", name="Agencia Boliviana de Información", aliases=["ABI"],
    desc="agencia de noticias estatal de Bolivia", website="https://www.abi.bo", name_zh="玻利维亚通讯社")
org("MEDIA", "news_agency", qid="Q5659776", name="Agencia de Noticias Fides", aliases=["ANF"],
    desc="agencia de noticias boliviana propiedad de la Iglesia Católica", website="http://www.noticiasfides.com", extra_sources=[SRC_BBC])

# ============================ FIN ============================
org("FIN", "central_bank", qid="Q806180", name="Banco Central de Bolivia", aliases=["BCB"],
    desc="principal ente monetario de Bolivia", name_zh="玻利维亚中央银行",
    website="https://www.bcb.gob.bo", extra_sources=[{"type": "official_website", "url": "https://www.bcb.gob.bo"}])
org("FIN", "financial_regulator", qid="Q137592300", name="Autoridad de Supervisión del Sistema Financiero", aliases=["ASFI"],
    desc="entidad pública boliviana de supervisión financiera", website="https://www.asfi.gob.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.asfi.gob.bo"}])
org("FIN", "commercial_bank", qid="Q16826675", name="Banco de Crédito de Bolivia", aliases=["BCP Bolivia"],
    desc="filial boliviana del banco peruano BCP; uno de los mayores bancos privados del país",
    rels=[{"type": "subsidiary_of", "target_name": "Banco de Crédito del Perú (BCP)"}],
    extra_sources=[SRC_ZOOMINFO])
org("FIN", "commercial_bank", qid="Q21044226", name="Banco Nacional de Bolivia", aliases=["BNB"],
    desc="uno de los mayores bancos de Bolivia por activos", website="https://www.bnb.com.bo")
org("FIN", "commercial_bank", qid="Q26250269", name="Banco Mercantil Santa Cruz S.A.", aliases=["BMSC"])
org("FIN", "commercial_bank", qid="Q21044225", name="Banco BISA", aliases=["BISA"])
org("FIN", "commercial_bank", qid="Q130101006", name="Banco Unión S.A.",
    desc="banco privado, entre los mayores por personal", extra_sources=[SRC_COMPANYDATA])
org("FIN", "microfinance_bank", qid="Q130590123", name="BancoSol", aliases=["Banco Solidario S.A."],
    desc="banco de microfinanzas, uno de los mayores del país", extra_sources=[SRC_ZOOMINFO])
org("FIN", "commercial_bank", qid="Q62118592", name="Banco Fassil")
org("FIN", "microfinance_bank", qid="Q81782924", name="Banco Fie",
    desc="banco de microfinanzas")
org("FIN", "commercial_bank", qid="Q81788241", name="Banco Ganadero")
org("FIN", "commercial_bank", qid="Q4854087", name="Banco Económico")
org("FIN", "development_bank", qid="Q5718076", name="Banco de Desarrollo Productivo", aliases=["BDP"],
    desc="banco público de desarrollo de Bolivia", website="https://www.bdp.gob.bo",
    extra_sources=[{"type": "official_website", "url": "https://www.bdp.gob.bo"}])
org("FIN", "microfinance_bank", qid="Q141149552", name="Banco Prodem")

# ============================ PARTY ============================
org("PARTY", None, qid="Q1142239", name="Movimiento al Socialismo", aliases=["MAS", "MAS-IPSP"],
    desc="Political party in Bolivia, gobernante 2006-2019 y 2020-2025", name_zh="争取社会主义运动")
org("PARTY", None, qid="Q7893757", name="Alianza Unidad", aliases=["Unidad", "Bloque de Unidad", "Unidad Nacional"],
    desc="coalición electoral boliviana formada en diciembre de 2024, ganadora de las elecciones de 2025 (Rodrigo Paz)",
    founded="2024-12-18", extra_sources=[SRC_UNITY])
org("PARTY", None, qid="Q2605787", name="Partido Demócrata Cristiano de Bolivia", aliases=["PDC"], name_zh="玻利维亚基督教民主党")
org("PARTY", None, qid="Q100740699", name="Creemos",
    desc="alianza política de derecha boliviana (Santa Cruz)")
org("PARTY", None, qid="Q134398739", name="Libre",
    desc="partido político boliviano en torno a Evo Morales (2025)")
org("PARTY", None, qid="Q1536051", name="Movimiento Nacionalista Revolucionario", aliases=["MNR"], name_zh="革命民族主义运动")
org("PARTY", None, qid="Q2823680", name="Acción Democrática Nacionalista", aliases=["ADN"], name_zh="民族主义民主行动党")
org("PARTY", None, qid="Q5124336", name="Unidad Cívica Solidaridad", aliases=["UCS"])
org("PARTY", None, qid="Q3021809", name="Movimiento Demócrata Social", aliases=["MDS"])
org("PARTY", None, qid="Q1951202", name="Movimiento de Izquierda Revolucionaria", aliases=["MIR Bolivia"])
org("PARTY", None, qid="Q7318805", name="Frente Revolucionario de Izquierda", aliases=["FRI"])
org("PARTY", None, qid="Q120019158", name="Movimiento Tercer Sistema")
org("PARTY", None, qid="Q131629757", name="APB Súmate", aliases=["Autonomía Para Bolivia - Súmate"])
org("PARTY", None, qid="Q135559560", name="Alianza Popular (Bolivia)")

# ============================ MIL ============================
org("MIL", "armed_forces", qid="Q834291", name="Fuerzas Armadas de Bolivia",
    desc="combined military forces of Bolivia", name_en="Bolivian Armed Forces", name_zh="玻利维亚武装力量")
org("MIL", "army", qid="Q4939559", name="Ejército de Bolivia",
    desc="land warfare branch of Bolivia's military forces", name_en="Bolivian Army", name_zh="玻利维亚陆军")
org("MIL", "navy", qid="Q151698", name="Armada Boliviana", aliases=["Armada de Bolivia", "Fuerza Naval Boliviana"],
    desc="naval force of Bolivia (fluvial y lacustre, país sin litoral marítimo)", name_en="Bolivian Navy", name_zh="玻利维亚海军")
org("MIL", "air_force", qid="Q960033", name="Fuerza Aérea Boliviana",
    desc="air warfare branch of Bolivia's military forces", name_en="Bolivian Air Force", name_zh="玻利维亚空军")
org("MIL", "police", qid="Q3065571", name="Policía Nacional de Bolivia",
    desc="law enforcement agency of Bolivia", name_en="Bolivian National Police", name_zh="玻利维亚国家警察")

# ============================ INTL ============================
def intl(qid, name, aliases, desc, sub, website, name_zh=None):
    org("INTL", sub, qid=qid, name=name, aliases=aliases, desc=desc, website=website, name_zh=name_zh,
        rels=[{"type": "member_country", "target_name": "Bolivia"}])

intl("Q1065", "Organización de las Naciones Unidas", ["ONU", "United Nations", "UN"],
     "organización internacional (Bolivia miembro desde 1945)", "global", "https://www.un.org", name_zh="联合国")
intl("Q49416", "Organización de los Estados Americanos", ["OEA", "OAS"],
     "organización regional americana (Bolivia miembro)", "regional", "https://www.oas.org", name_zh="美洲国家组织")
intl("Q471690", "Comunidad Andina", ["CAN"],
     "Organización de integración de la región andina (Bolivia miembro)", "regional_integration", "https://www.comunidadandina.org",
     name_zh="安第斯共同体")
intl("Q607301", "Asociación Latinoamericana de Integración", ["ALADI"],
     "organismo internacional de integración latinoamericano (sede en Montevideo; Bolivia miembro)", "regional_integration",
     "https://www.aladi.org", name_zh="拉丁美洲一体化协会")
intl("Q2614129", "CAF - Banco de Desarrollo de América Latina y el Caribe", ["CAF", "Corporación Andina de Fomento"],
     "banco de desarrollo de América Latina (Bolivia accionista)", "development_bank", "https://www.caf.com",
     name_zh="拉丁美洲开发银行")
intl("Q1045401", "Comunidad de Estados Latinoamericanos y Caribeños", ["CELAC"],
     "bloque regional de estados latinoamericanos y caribeños (Bolivia miembro)", "regional_integration", None,
     name_zh="拉美和加勒比国家共同体")
intl("Q4040", "Mercosur", ["Mercado Común del Sur"],
     "bloque regional sudamericano (Bolivia miembro en proceso de adhesión plena)", "regional_integration", "https://www.mercosur.int",
     name_zh="南方共同市场")
intl("Q7700", "UNESCO", ["Organización de las Naciones Unidas para la Educación, la Ciencia y la Cultura"],
     "agencia de la ONU para educación, ciencia y cultura (Bolivia miembro)", "global", "https://www.unesco.org",
     name_zh="联合国教科文组织")

# ---------------------------------------------------------------- build final entries
CAT_ORDER = ["GOV", "SOE", "CORP", "NGO", "ACAD", "MEDIA", "FIN", "PARTY", "MIL", "INTL"]
counters = {c: 0 for c in CAT_ORDER}
results = []
def has_cjk(s):
    return any('\u4e00' <= ch <= '\u9fff' for ch in s or '')

for e in E:
    cat = e["cat"]
    counters[cat] += 1
    oid = f"BO-{cat}-{counters[cat]:03d}"
    qid = e["qid"]
    rec = index.get(qid, {}) if qid else {}
    name = e["name"] or rec.get("name_es") or rec.get("label") or ""
    if not name:
        raise SystemExit(f"no name for {oid} qid={qid}")
    desc = e["desc"] or rec.get("desc")
    vrec = verify.get(e["key"]) if e["key"] else None
    if vrec and not desc and vrec.get("description"):
        desc = vrec["description"]
    website = e["website"] or rec.get("website")
    founded = e["founded"] or rec.get("founded")
    hq = e["hq"] or rec.get("hq")
    if hq and (re.match(r"^Q[0-9]+$", hq) or hq == name):
        hq = None  # drop unresolved QID references or self-referential P159 values
    name_en = e["name_en"] or rec.get("name_en") or (rec.get("label") if rec.get("label") and not has_cjk(rec["label"]) and rec.get("label") != name else None)
    aliases = list(e["aliases"])
    if not name_en and name.isascii() and " " in name and name not in aliases:
        pass
    sources = []
    if qid:
        sources.append({"type": "wikidata", "url": f"https://www.wikidata.org/wiki/{qid}"})
    sources.extend(wiki_sources(e["key"]) if e["key"] else [])
    for s in e["extra_sources"]:
        sources.append(dict(s))
    # dedupe sources by url
    seen = set()
    dsources = []
    for s in sources:
        if s["url"] in seen:
            continue
        seen.add(s["url"])
        dsources.append(s)
    if not dsources:
        raise SystemExit(f"no sources for {oid} {name}")
    if qid:
        status = "verified"
    else:
        status = "partial"
    entry = {
        "id": oid,
        "wikidata_qid": qid,
        "name": name,
        "category": cat,
        "country": COUNTRY,
        "verification_status": status,
    }
    if aliases:
        entry["aliases"] = aliases
    if e["sub"]:
        entry["subcategory"] = e["sub"]
    entry["description"] = desc
    entry["headquarters"] = hq
    if founded:
        entry["founded"] = founded
    entry["website"] = website
    entry["parent_organization"] = e["parent"]
    if e["people"]:
        entry["key_people"] = [{"title": p["title"], "name": p["name"], "since": p.get("since")} for p in e["people"]]
    if e["rels"]:
        entry["relationships"] = [{"type": r["type"], "target_name": r["target_name"]} for r in e["rels"]]
    entry["sources"] = dsources
    if e["name_en"]:
        entry["name_en"] = e["name_en"]
    if e["name_zh"]:
        entry["name_zh"] = e["name_zh"]
    results.append(entry)

# schema order: keep required keys present; extra keys name_en/name_zh are NOT in schema!
# -> schema has additionalProperties:false; name_en/name_zh not defined. Merge them into aliases instead.
for entry in results:
    extra = []
    if "name_en" in entry:
        extra.append(entry.pop("name_en"))
    if "name_zh" in entry:
        extra.append(entry.pop("name_zh"))
    if extra:
        entry.setdefault("aliases", [])
        for x in extra:
            if x not in entry["aliases"]:
                entry["aliases"].insert(0, x)

# ---------------------------------------------------------------- summary + metadata
by_category = {}
for c in CAT_ORDER:
    entries_c = [r for r in results if r["category"] == c]
    subs = {}
    for r in entries_c:
        s = r.get("subcategory") or "general"
        subs[s] = subs.get(s, 0) + 1
    top = [r["name"] for r in entries_c[:10]]
    by_category[c] = {"count": len(entries_c), "subcategories": subs, "top_orgs": top}

verified = sum(1 for r in results if r["wikidata_qid"])
total = len(results)
doc = {
    "metadata": {
        "country": "Bolivia (Plurinational State of)",
        "country_iso": "BO",
        "country_qid": "Q750",
        "collection_date": DATE,
        "phase": "phase1_broad_scan",
        "categories_covered": CAT_ORDER,
        "subcategories_covered": sorted({r.get("subcategory") or "general" for r in results}),
        "depth": "overview",
        "total_organizations": total,
    },
    "organizations": results,
    "summary": {
        "by_category": by_category,
        "data_quality": {
            "verified_count": verified,
            "unverified_count": total - verified,
            "completeness_pct": round(verified * 100.0 / total),
        },
    },
}

with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(doc, f, ensure_ascii=False, indent=2)

print(f"Wrote {OUT_PATH}")
print(f"Total organizations: {total}")
for c in CAT_ORDER:
    print(f"  {c}: {by_category[c]['count']}")
print(f"With QID (verified): {verified} ({doc['summary']['data_quality']['completeness_pct']}%)")
no_qid = [(r["id"], r["name"]) for r in results if not r["wikidata_qid"]]
print("Entries needing manual confirmation (no QID):")
for i, n in no_qid:
    print(f"  {i} {n}")
