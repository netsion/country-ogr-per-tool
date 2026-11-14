# P4 编排 tick：人物完成后调用。用法: python scripts_tmp/p4_tick_ng.py <person_id> [start|done|failed]
import json, sys
from datetime import datetime

BASE = 'output/ng/2026-11-10'
pid = sys.argv[1]
status = sys.argv[2] if len(sys.argv) > 2 else 'done'

pp = f'{BASE}/_p4_progress.json'
prog = json.load(open(pp, encoding='utf-8'))

if pid in prog.get('current', []):
    prog['current'].remove(pid)
if pid in prog.get('remaining', []):
    prog['remaining'].remove(pid)
if status == 'start' and pid not in prog['current']:
    prog['current'].append(pid)
elif status == 'done' and pid not in prog['completed']:
    prog['completed'].append(pid)
elif status == 'failed' and pid not in prog['failed']:
    prog['failed'].append(pid)
prog['last_updated'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
json.dump(prog, open(pp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

if status == 'start':
    print(f"MARK {pid}: inflight (current={len(prog['current'])}, remaining={len(prog['remaining'])})")
    sys.exit(0)

try:
    o = json.load(open(f'{BASE}/persons/{pid}.json', encoding='utf-8'))
    cm = o.get('collection_meta', {})
    print(f"TICK {pid}: status={status} | phase={cm.get('phase')} | score={cm.get('completeness_score')} | "
          f"work={len(o.get('work_experience', []))} edu={len(o.get('education', []))} "
          f"stance={len(o.get('political_stances', []))} rel={len(o.get('person_relationships', []))} "
          f"family={len(o.get('family_members', []))} sa={len(o.get('social_accounts', []))} | "
          f"quotes={len(cm.get('quotes', []) or [])}")
except Exception as e:
    print(f"TICK {pid}: FILE INVALID -> {e}")
    sys.exit(1)

total = len(prog['completed']) + len(prog['remaining']) + len(prog['current']) + len(prog['failed'])
print(f"PROGRESS: completed={len(prog['completed'])}/{total} inflight={len(prog['current'])} failed={len(prog['failed'])}")
