# P3 编排 tick 工具（scripts_tmp/ 按 workspace-hygiene 规范存放）
# 用法: python scripts_tmp/p3_tick_ng.py <org_id> [start|done|failed]
import json, sys
from datetime import datetime

BASE = 'output/ng/2026-11-10'
org_id = sys.argv[1]
status = sys.argv[2] if len(sys.argv) > 2 else 'done'

pp = f'{BASE}/_phase_progress.json'
with open(pp, encoding='utf-8') as f:
    prog = json.load(f)

if org_id in prog.get('current', []):
    prog['current'].remove(org_id)
if org_id in prog.get('remaining', []):
    prog['remaining'].remove(org_id)

if status == 'start':
    if org_id not in prog['current']:
        prog['current'].append(org_id)
elif status == 'done':
    if org_id not in prog['completed']:
        prog['completed'].append(org_id)
elif status == 'failed':
    if org_id not in prog['failed']:
        prog['failed'].append(org_id)

prog['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
with open(pp, 'w', encoding='utf-8') as f:
    json.dump(prog, f, ensure_ascii=False, indent=2)

if status == 'start':
    print(f"MARK {org_id}: inflight (current={len(prog['current'])}, remaining={len(prog['remaining'])})")
    sys.exit(0)

try:
    with open(f'{BASE}/orgs/{org_id}.json', encoding='utf-8') as f:
        o = json.load(f)
    cm = o.get('collection_meta', {})
    print(f"TICK {org_id}: status={status} | phase={cm.get('phase')} | score={cm.get('completeness_score')} | "
          f"kp={len(o.get('key_people', []))} sa={len(o.get('social_accounts', []))} re={len(o.get('recent_events', []))} "
          f"dept={len(o.get('departments', []))} rel={len(o.get('related_entities', []))} da={len(o.get('digital_assets', []))} | "
          f"quotes={len(cm.get('quotes', []) or [])}")
except Exception as e:
    print(f"TICK {org_id}: FILE INVALID -> {e}")
    sys.exit(1)

total = len(prog['completed']) + len(prog['remaining']) + len(prog['current']) + len(prog['failed'])
print(f"PROGRESS: completed={len(prog['completed'])}/{total} inflight={len(prog['current'])} failed={len(prog['failed'])}")
