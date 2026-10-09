# -*- coding: utf-8 -*-
"""P5 cleanup: fill empty name_zh (org skeletons) + strip schema-forbidden extra fields."""
import json
import os

BASE = "output/ci/2026-10-06"

# 1. name_zh fills (from name_index / known identities)
ZH_FILLS = {
    "CI-ACAD-007": ("Université de Man", "曼大学"),
    "CI-ACAD-008": ("University of San Pedro", "圣佩德罗大学"),
    "CI-ACAD-009": ("University of Bondoukou", "邦杜库大学"),
    "CI-CORP-008": ("Nestlé Côte d'Ivoire", "雀巢科特迪瓦"),
    "CI-CORP-009": ("Unilever Côte d'Ivoire", "联合利华科特迪瓦"),
    "CI-MEDIA-005": ("Life TV", "生命电视台"),
    "CI-NGO-006": ("Fondation Franck Kessié", "弗兰克·凯西耶基金会"),
    "CI-NGO-012": ("Ligue Ivoirienne des Droits des Femmes", "科特迪瓦妇女权利联盟"),
    "CI-PARTY-007": ("Mouvement des Forces de l'Avenir", "未来力量运动"),
    "CI-PARTY-009": ("Liberté et Démocratie pour la République", "共和自由与民主党"),
    "CI-PARTY-010": ("Congrès Panafricain pour la Justice et l'Égalité des Peuples", "泛非正义与人民平等大会"),
}

# 2. allowed fields per array (schema/rules)
ALLOWED = {
    "work_experience": {"start_date", "end_date", "organization", "org_id", "position"},
    "education": {"institution", "degree", "field", "start_date", "end_date"},
    "political_stances": {"date", "topic", "stance_content", "source"},
    "person_relationships": {"person_id", "person_name", "relationship_type", "description"},
    "major_achievements": {"date", "achievement", "organization"},
    "social_accounts": {"platform", "account_name", "url", "source"},
    "family_members": {"person_id", "name", "relationship", "industry_or_organization"},
    "contacts": {"type", "value", "source"},
    "key_people": {"person_id", "name", "title", "title_description", "description"},
    "departments": {"name", "dept_id", "head", "description", "parent_dept_id"},
    "recent_events": {"date", "title", "description", "impact", "source"},
    "related_entities": {"org_id", "org_name", "org_type", "org_description", "relationship_type"},
    "digital_assets": {"name", "url", "description", "source"},
}

stripped = 0
files_fixed = 0
for d in ("orgs", "persons"):
    dp = os.path.join(BASE, d)
    for fn in os.listdir(dp):
        if not fn.endswith(".json") or fn == "_index.json":
            continue
        fp = os.path.join(dp, fn)
        with open(fp, encoding="utf-8") as f:
            data = json.load(f)
        orig = json.dumps(data, sort_keys=True, ensure_ascii=False)
        # strip extra fields
        for arr, ok in ALLOWED.items():
            for item in data.get(arr, []) or []:
                if isinstance(item, dict):
                    for bad in list(item.keys()):
                        if bad not in ok:
                            del item[bad]
                            stripped += 1
        # fill name_zh / name_en
        if d == "orgs":
            oid = data.get("org_id", fn[:-5])
            if oid in ZH_FILLS:
                b = data.setdefault("basic_info", {})
                en, zh = ZH_FILLS[oid]
                if not (b.get("name_en") or "").strip():
                    b["name_en"] = en
                if not (b.get("name_zh") or "").strip():
                    b["name_zh"] = zh
        new = json.dumps(data, sort_keys=True, ensure_ascii=False)
        if new != orig:
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            files_fixed += 1

print(f"stripped {stripped} extra fields; fixed {files_fixed} files")
