# -*- coding: utf-8 -*-
"""Batch fetch UCB posts, grep for Peres/Ximena context; query pages; check profile article media."""
import json
import re
import urllib.parse
import urllib.request

PROXY = "http://127.0.0.1:7890"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
opener = urllib.request.build_opener(urllib.request.ProxyHandler({"http": PROXY, "https": PROXY}))
opener.addheaders = [("User-Agent", UA), ("Accept-Language", "es-ES,es;q=0.9,en;q=0.7")]


def fetch(url, timeout=50):
    try:
        resp = opener.open(url, timeout=timeout)
        return resp.read().decode("utf-8", "replace")
    except Exception as e:
        return f"__ERR__ {e}"


def strip_html(h):
    h = re.sub(r"<script.*?</script>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    for a, b in [("&nbsp;", " "), ("&amp;", "&"), ("&#8220;", '"'), ("&#8221;", '"'), ("&#8217;", "'"),
                 ("&quot;", '"'), ("&#8211;", "-"), ("&#8216;", "'"), ("&laquo;", "«"), ("&raquo;", "»")]:
        h = h.replace(a, b)
    return re.sub(r"\s+", " ", h).strip()


SLUGS = [
    "espana-reconoce-la-excelencia-academica-de-la-u-c-b-a-traves-de-la-fundacion-carlos-iii",
    "la-u-c-b-inaugura-oficialmente-el-ano-conmemorativo-por-su-60-aniversario-con-la-xiv-leccion-inaugural-de-humanismo",
    "la-u-c-b-clausura-las-actividades-del-bicentenario-con-la-presentacion-de-una-obra-que-reune-200-voces-de-todo-el-pais",
    "la-u-c-b-presento-el-libro-violencias-en-la-vejez-desafios-y-herramientas-en-el-derecho-boliviano-y-argentino",
    "u-c-b-inaugura-modernos-laboratorios-en-el-alto-para-fortalecer-la-excelencia-academica-en-bioquimica-y-farmacia",
    "la-u-c-b-celebra-59-anos-de-vida-institucional-con-emotivo-acto-academico",
    "la-u-c-b-sede-la-paz-lanza-dos-nuevas-carreras-una-apuesta-por-la-comunicacion-y-la-salud",
    "la-u-c-b-y-unitas-fortaleciendo-lazos-entre-la-academia-y-la-sociedad-civil",
    "u-c-b-sede-la-paz-lanza-nueva-carrera-de-medicina",
    "acto-central-por-los-60-anos-de-la-u-c-b-destaco-el-compromiso-con-la-excelencia-la-investigacion-y-la-formacion-integral",
    "la-u-c-b-consolida-su-eficiencia-institucional-y-proyeccion-financiera-en-el-ii-consejo-administrativo-financiero-nacional",
    "el-iii-congreso-internacional-resiliencias-frente-a-la-crisis-climatica-arranca-en-la-u-c-b-con-un-fuerte-llamado-a-la-accion",
    "u-c-b-entrega-primera-fase-del-proyecto-de-rescate-y-conservacion-del-patrimonio-del-archivo-y-biblioteca-arquidiocesanos-de-sucre",
    "marcos-delgadillo-me-comprometo-a-liderar-con-integridad-transparencia-y-responsabilidad-este-nuevo-desafio-en-la-u-c-b",
    "secrad-de-la-u-c-b-la-paz-y-cochabamba-fortalecen-la-articulacion-intersedes-en-su-primera-reunion-de-trabajo",
]

hits = {}
for slug in SLUGS:
    raw = fetch(f"https://www.ucb.edu.bo/wp-json/wp/v2/posts?slug={slug}")
    if raw.startswith("__ERR__") or raw.strip() in ("[]", ""):
        print(slug, "-> skip")
        continue
    try:
        p = json.loads(raw)[0]
    except Exception:
        print(slug, "-> parse fail")
        continue
    txt = strip_html(p.get("content", {}).get("rendered", ""))
    ctx = []
    for m in re.finditer(r"[Pp]eres|[Xx]imena", txt):
        s = max(0, m.start() - 350)
        e = min(len(txt), m.end() + 350)
        ctx.append(txt[s:e])
    if ctx:
        hits[slug] = {"link": p.get("link"), "date": p.get("date"), "title": strip_html(p.get("title", {}).get("rendered", "")), "contexts": ctx[:4]}
        print("=" * 90)
        print(p.get("date"), "|", slug)
        for c in ctx[:3]:
            print("  >>>", c)
            print()

with open(r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\_xpa_ucb_mentions.json", "w", encoding="utf-8") as f:
    json.dump(hits, f, ensure_ascii=False, indent=1)

# pages: Sede La Paz autoridades
print("\n== PAGES search ==")
for q in ["la paz", "autoridades", "sede"]:
    raw = fetch("https://www.ucb.edu.bo/wp-json/wp/v2/pages?search=" + urllib.parse.quote(q) + "&per_page=30")
    if raw.startswith("__ERR__"):
        print(q, "ERR", raw[:100])
        continue
    try:
        pages = json.loads(raw)
    except Exception:
        continue
    if isinstance(pages, list):
        print(f"== pages '{q}': {len(pages)} ==")
        for pg in pages:
            print("  -", pg.get("link", ""))

# media of the profile article
print("\n== profile article media ==")
raw = fetch("https://www.ucb.edu.bo/wp-json/wp/v2/posts?slug=ximena-peres-arenas-mujer-madre-psicologa-y-rectora-un-ejemplo-de-fe-y-liderazgo")
try:
    p = json.loads(raw)[0]
    media = re.findall(r'src="([^"]+)"', p.get("content", {}).get("rendered", ""))
    for m in media:
        print("  img:", m)
    # featured media via _embed
    raw2 = fetch("https://www.ucb.edu.bo/wp-json/wp/v2/posts?slug=ximena-peres-arenas-mujer-madre-psicologa-y-rectora-un-ejemplo-de-fe-y-liderazgo&_embed")
    p2 = json.loads(raw2)[0]
    fm = p2.get("_embedded", {}).get("wp:featuredmedia", [])
    for m in fm:
        print("  featured:", m.get("source_url"))
except Exception as e:
    print("media ERR", e)
