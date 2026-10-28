# -*- coding: utf-8 -*-
import json
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "persons", "BO-PERSON-000279.json")
d = json.load(open(p, encoding="utf-8"))
print("score =", d["collection_meta"]["completeness_score"])
print("quotes =", len(d["collection_meta"]["quotes"]))
print("work =", len(d["work_experience"]), "| edu =", len(d["education"]),
      "| rel =", len(d["person_relationships"]), "| achievements =", len(d["major_achievements"]),
      "| social =", len(d["social_accounts"]), "| family =", len(d["family_members"]),
      "| stances =", len(d.get("political_stances", [])), "| contacts =", len(d.get("contacts", [])))
print("bio_len =", len(d["biography_summary"]))
print("name =", d["name"], "| nat =", d["nationality"], "| gender =", d["gender"])
allowed = {
    "work_experience": {"start_date", "end_date", "organization", "org_id", "position"},
    "education": {"institution", "degree", "field", "start_date", "end_date"},
    "person_relationships": {"person_id", "person_name", "relationship_type", "description"},
    "family_members": {"person_id", "name", "relationship", "industry_or_organization"},
    "social_accounts": {"platform", "account_name", "url", "source"},
    "major_achievements": {"date", "achievement", "organization"},
}
for k, a in allowed.items():
    ok = all(set(x) <= a for x in d[k])
    print(f"{k} fields ok: {ok}")
print("platforms:", [x["platform"] for x in d["social_accounts"]])
print("rel_types:", [x["relationship_type"] for x in d["person_relationships"]])
print("degrees:", [x["degree"] for x in d["education"]])
print("fm_rel:", [x["relationship"] for x in d["family_members"]])
empty_ids = [x.get("org_id") == "" for x in d["work_experience"]] + \
            [x.get("person_id") == "" for x in d["person_relationships"] + d["family_members"]]
print("no empty-str ids:", not any(empty_ids))
print("top_keys =", sorted(d.keys()))
