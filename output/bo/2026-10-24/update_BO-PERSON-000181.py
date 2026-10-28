# -*- coding: utf-8 -*-
"""Update BO-PERSON-000181 profile: add profile photo block and contacts."""
import json

path = r"D:\claude-workspace\apec-osint-tool\output\bo\2026-10-24\persons\BO-PERSON-000181.json"
with open(path, encoding="utf-8") as f:
    data = json.load(f)

# profile photo from official YPFB article on his assumption
data["profile"] = {
    "source_url": "https://www.ypfb.gob.bo/sites/default/files/2026-04/WhatsApp%20Image%202026-04-24%20at%206.40.49%20AM_0.jpeg",
    "local_path": "photos/BO-PERSON-000181.jpg"
}
data["profile_note"] = "照片下载自YPFB官网2026-04-24关于其就任的官方新闻稿（node/510），为就任期间官方活动照（与玻利维亚国旗及塔里哈省旗前握手场景）。"

# official / verified public contact channels
data["contacts"] = [
    {
        "type": "website",
        "value": "https://www.ypfb.gob.bo/Presidente_ejecutivo",
        "source": "YPFB官网「Presidente Ejecutivo de YPFB」官方页面，展示其为现任执行总裁"
    },
    {
        "type": "website",
        "value": "https://x.com/SebastianYPFB",
        "source": "其经认证使用的X（推特）官方账号，简介为「Presidente ejecutivo de YPFB」"
    }
]

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("UPDATED", path)
