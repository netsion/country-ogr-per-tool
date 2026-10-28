# -*- coding: utf-8 -*-
"""Set profile.source_url for successfully downloaded avatars (Agent C)."""
import json, io, sys, os

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = os.path.dirname(os.path.abspath(__file__))

UPDATES = {
    'BO-PERSON-000347': 'https://www.univalle.edu/wp-content/uploads/2025/11/588246529_1287109820110223_1814691545770974701_n.jpg',
    'BO-PERSON-000352': 'https://www.nur.edu/wp-content/uploads/2020/05/Rector350x250.jpg',
    'BO-PERSON-000355': 'https://www.nur.edu/wp-content/uploads/2022/04/WhatsApp-Image-2022-07-11-at-10.23.34-AM.jpeg',
    'BO-PERSON-000380': 'https://editored.org/wp-content/uploads/2026/01/CLAUDIA-BENAVENTE-5.jpg',
    'BO-PERSON-000391': 'https://estaticos-noticias.unitel.bo/binrepository/600x348/0c0/0d0/none/125450566/RIIA/ejecutivo_UN48002_MG146270679.jpg',
    'BO-PERSON-000410': 'https://radiofides.com/es/wp-content/uploads/2024/12/471547128_1005449101613637_7202023900116567198_n.jpg',
    'BO-PERSON-000413': 'https://www.panamericana.bo/media/radiopanamerica/images/2020/08/07/2020080712333117546.jpg',
    'BO-PERSON-000418': 'https://i.ytimg.com/vi/v6FhqBpy4Uw/hqdefault.jpg',
    'BO-PERSON-000421': 'https://www.opinion.com.bo/media/opinion/images/2025/10/10/2025101015583227254.jpg',
    'BO-PERSON-000425': 'https://cdn.theorg.com/2e34dca0-5198-4812-8c89-e53b264b78b9.jpg',
    'BO-PERSON-000437': 'https://www.cipca.org.bo/images/news/es/b_4113_marco-antonio-albornoz-posesionado-como-nuevo-director-general-del-cipca-1.jpg',
    'BO-PERSON-000446': 'https://i.ytimg.com/vi/FY0psrT_dzM/maxresdefault.jpg',
    'BO-PERSON-000456': 'https://patino.org/wp-content/uploads/2025/11/CUL-Alba-Balderrama-scaled-800x0-c-default.jpg',
    'BO-PERSON-000467': 'https://lens.civicus.org/wp-content/uploads/2023/12/jordi-surkin2.png',
    'BO-PERSON-000486': 'https://upload.wikimedia.org/wikipedia/commons/2/23/Eduardo_Del_Castillo.jpg',
    'BO-PERSON-000492': 'https://i.ytimg.com/vi/tZR5vggtMGs/maxresdefault.jpg',
    'BO-PERSON-000512': 'https://s3.amazonaws.com/activos.concejomunicipalscz.gob.bo/img/noticias-del-concejo/2025/2025-10-20-A-00-d4f8r7f554-800.jpg',
}

ok, fail = 0, []
for pid, url in UPDATES.items():
    path = os.path.join(BASE, 'persons', pid + '.json')
    try:
        with open(path, encoding='utf-8') as f:
            d = json.load(f)
        prof = d.get('profile')
        if prof is None:
            prof = {}
            d['profile'] = prof
        prof['source_url'] = url
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(d, f, ensure_ascii=False, indent=1)
        ok += 1
        print('OK', pid, '->', url[:80])
    except Exception as e:
        fail.append((pid, str(e)))
        print('FAIL', pid, e)

print('updated:', ok, 'failed:', len(fail))
