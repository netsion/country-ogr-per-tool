# -*- coding: utf-8 -*-
"""Update BO-PERSON-000246: add profile photo, 2 relationships, 2 achievements."""
import json
import os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000246.json")
with open(path, encoding="utf-8") as f:
    data = json.load(f)

# 1. Profile photo (Expocruz 2026 presentation, Negocios Press article image)
data["profile"] = {
    "source_url": "https://negociospress.com.bo/wp-content/uploads/2026/09/WhatsApp-Image-2026-09-26-at-00.07.15.jpeg",
    "local_path": "persons/photos/BO-PERSON-000246.jpg"
}
data["profile_note"] = "照片为2026年9月26日EXPOCRUZ 2026新手机银行发布会上以总经理身份致辞的现场图（Negocios Press报道配图，文章正文确认发布会由其主持）。"

# 2. Two additional verified relationships
data["person_relationships"].append({
    "person_id": "BO-PERSON-000247",
    "person_name": "阿曼多·阿尔瓦雷斯·阿尔纳尔 (Armando Álvarez Arnal)",
    "relationship_type": "superior",
    "description": "Banco Unión S.A. 董事会第一副主席，为其上级；属2025年12月决议任命其为总经理的董事会成员。"
})
data["person_relationships"].append({
    "person_id": None,
    "person_name": "安德烈斯·库恩·桑吉内斯 (Andrés Kuhn Sangines)",
    "relationship_type": "colleague",
    "description": "玻利维亚信贷银行（BCP）同事；2023年7月1日其接任企业银行区域总经理一职时，库恩·桑吉内斯转任其他岗位（ASFI高管登记卡2022-09-30重大事项记录）。"
})

# 3. Two additional verified achievements
data["major_achievements"].append({
    "date": "2026-04-28",
    "achievement": "任内推动Banco Unión在其Yasta移动钱包中上线通过EFY平台购买USDT（泰达币）的新功能，为玻利维亚国有银行在数字资产服务上的重要举措（银行公告，Erbol报道）。",
    "organization": "玻利维亚国民联盟银行 (Banco Unión S.A.)"
})
data["major_achievements"].append({
    "date": "2026-09-26",
    "achievement": "在EXPOCRUZ 2026（第50届）发布会上主持发布银行新版同名手机银行App（逐步替代UNImóvil，采用微服务架构），提出「把银行放在客户手心」并强调安全与可用性（Negocios Press、Economy两家媒体报道）。",
    "organization": "玻利维亚国民联盟银行 (Banco Unión S.A.)"
})

# 4. Update notes
data["collection_meta"]["notes"] = "核心事实均有官方来源支撑并交叉验证：现任职务见银行官网领导名录；任命经过见玻利维亚证券交易所2025-12-05重大信息公告；BCP任职完整时间线（2022-09入职、2023-07升任、2025-07转任零售银行部、2025-11-28离职）见ASFI高管登记卡（政府登记源）；获奖见Fintech Americas第11届获奖者页（该届颁奖典礼于2026年3月迈阿密举行）；USDT功能与新版手机银行发布分别经Erbol（2026-04-28）与Negocios Press/Economy（2026-09）直读核实。出生日期、出生地、家庭、政见等经多轮检索未见公开资料，相应字段留空——评分为机械字段计数，非政治人物且公开信息有限，此类客观缺失拉低总分。存疑事项：中文媒体0xzx（2026-04-30）将USDT功能介绍引语归于其名下，但西语原始报道（Erbol）中该引语出自数字创新总经理Diego Fuentes Chávez，故成就条目未采用其对个人的直接引语。姓名在ASFI记录中存在带重音（Amenábar）与不带重音（Amenabar）两种拼写，带重音变体已列入aliases。"

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("UPDATED:", path)
print("relationships:", len(data["person_relationships"]), "| achievements:", len(data["major_achievements"]))
