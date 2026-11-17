# -*- coding: utf-8 -*-
"""Add name-collision warning to EG-PERSON-000121 registry entry."""
import sys
sys.path.insert(0, r"D:\ai-workspace\apec-osint-tool\.agents\skills\country-org-collector\scripts")
from atomic_write import load_json, save_json
BASE = r"D:\ai-workspace\apec-osint-tool\output\eg\2026-11-16"
reg = load_json(f"{BASE}/id_registry.json")
for e in reg.get("person_registry", []):
    if e.get("person_id") == "EG-PERSON-000121":
        e["name_collision_warning"] = "⚠️ 同名不同人：NSPO前总干事穆斯塔法·阿明(当代) ≠ 今日消息报创始人记者穆斯塔法·阿明(1914-1997)。媒体/历史语境检索此名时禁止绑定000121"
        print("flagged 000121")
save_json(f"{BASE}/id_registry.json", reg)
