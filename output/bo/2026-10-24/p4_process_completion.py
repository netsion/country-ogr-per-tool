# -*- coding: utf-8 -*-
"""P4 completion processor: validate person profile, run resolve_ids + name index,
schema check, update _phase_progress.json. Usage: python p4_process_completion.py BO-PERSON-000001 [--fail]"""
import json
import os
import subprocess
import sys
import time
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(D, '..', '..', '..'))
SCRIPTS = os.path.join(ROOT, '.agents', 'skills', 'country-org-collector', 'scripts')
pid = sys.argv[1]
failed_mode = '--fail' in sys.argv

def run(args):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT)

prog_path = os.path.join(D, '_phase_progress.json')
prog = json.load(open(prog_path, encoding='utf-8'))

if failed_mode:
    prog['current'] = [x for x in (prog.get('current') or []) if x != pid]
    if pid not in prog['failed']:
        prog['failed'].append(pid)
    prog['last_updated'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    with open(prog_path + '.tmp', 'w', encoding='utf-8') as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)
        f.flush(); os.fsync(f.fileno())
    os.replace(prog_path + '.tmp', prog_path)
    print('FAILED %s | completed=%d failed=%d remaining=%d' % (pid, len(prog['completed']), len(prog['failed']), len(prog['remaining'])))
    sys.exit(2)

fp = os.path.join(D, 'persons', pid + '.json')
try:
    p = json.load(open(fp, encoding='utf-8'))
except Exception as e:
    print('INVALID OUTPUT for %s: %s' % (pid, e))
    sys.exit(1)

problems = []
cm = p.get('collection_meta') or {}
score = cm.get('completeness_score', 0)
if cm.get('phase') != 'phase4_person_profile':
    problems.append('phase not phase4_person_profile')
quotes = cm.get('quotes') or []
if not quotes or not isinstance(quotes[0], dict):
    problems.append('quotes not object array')
if not p.get('biography_summary'):
    problems.append('biography_summary missing')

r1 = run([os.path.join(SCRIPTS, 'resolve_ids.py'), os.path.join('output', 'bo', '2026-10-24'), '--allow-register', '--max-register', '30'])
reg_note = (r1.stdout or '').strip().splitlines()[-1] if r1.stdout.strip() else 'no output'
r2 = run([os.path.join(SCRIPTS, 'generate_name_index.py'), os.path.join('output', 'bo', '2026-10-24')])
r3 = run([os.path.join(SCRIPTS, 'validate_schema.py'), os.path.join('output', 'bo', '2026-10-24'), '--file', os.path.relpath(fp, ROOT)])
vout = (r3.stdout or '') + (r3.stderr or '')
if 'ERRORS:' in vout:
    for line in vout.splitlines():
        if 'ERR:' in line:
            problems.append(line.strip())

prog['current'] = [x for x in (prog.get('current') or []) if x != pid]
if pid not in prog['completed']:
    prog['completed'].append(pid)
prog['last_updated'] = time.strftime('%Y-%m-%dT%H:%M:%S')
with open(prog_path + '.tmp', 'w', encoding='utf-8') as f:
    json.dump(prog, f, ensure_ascii=False, indent=2)
    f.flush(); os.fsync(f.fileno())
os.replace(prog_path + '.tmp', prog_path)

print('DONE %s | score=%s | completed=%d remaining=%d failed=%d' % (pid, score, len(prog['completed']), len(prog['remaining']), len(prog['failed'])))
print('registry: %s' % reg_note)
print('problems: %s' % (problems if problems else 'none'))
