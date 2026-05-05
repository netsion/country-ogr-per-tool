#!/usr/bin/env python3
import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('output/kr/2026-05-04/orgs/KR-PARTY-007.json', encoding='utf-8') as f:
    d = json.load(f)
bi = d.get('basic_info', {})
# Check each basic_info field
for k, v in bi.items():
    val = str(v)[:120]
    print(f'  {k}: {val}')
print()
# Check key_people
for i, kp in enumerate(d.get('key_people', [])):
    print(f'kp[{i}] name: {str(kp.get("name",""))[:80]}')
    print(f'kp[{i}] title: {str(kp.get("title",""))[:80]}')
print()
# Check departments
for i, dept in enumerate(d.get('departments', [])):
    print(f'dept[{i}] name: {str(dept.get("name",""))[:80]}')
