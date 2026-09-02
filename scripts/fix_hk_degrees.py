"""Recover degree values nulled by --normalize: compare HEAD vs worktree education entries."""
import json, subprocess, sys, io, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def map_degree(v):
    if not v or not isinstance(v, str): return None
    s = v.strip()
    if not s: return ''
    low = s.lower()
    if re.search(r'博士|phd|doctor|dba\b', low): return 'doctorate'
    if re.search(r'硕士|碩士|mba|llm|master', low): return 'master'
    if re.search(r'学士|學士|bachelor|llb|\bbs\b|\bba\b|\bbe\b', low): return 'bachelor'
    if re.search(r'jd|会计師|會計師|特許|律师|律師|专业资|專業資|cia|cfa|aca|fcca|acca|hkicpa|cpa', low): return 'professional'
    if re.search(r'中学|中學|high.?school|secondary', low): return 'high_school'
    if re.search(r'diploma|副学士|副學士|associate', low): return 'associate'
    return None  # unmappable -> leave as-is

def head_version(path):
    r = subprocess.run(['git', 'show', f'HEAD:{path}'], capture_output=True)
    if r.returncode != 0: return None
    try:
        return json.loads(r.stdout.decode('utf-8'))
    except Exception:
        return None

files = subprocess.run(['git', 'diff', '--name-only', '--', 'output/hk/2026-07-24/persons/'],
                       capture_output=True, text=True).stdout.split()
restored = {}
for path in files:
    if not path.endswith('.json'): continue
    if not os.path.exists(path): continue
    cur = json.load(open(path, encoding='utf-8'))
    old = head_version(path)
    if not old: continue
    old_edu, cur_edu = old.get('education') or [], cur.get('education') or []
    if not old_edu or not cur_edu: continue
    fixes = []
    norm = lambda s: re.sub(r'[^\w]', '', (s or ''), flags=re.UNICODE)
    def inst_norm(s):
        s = norm(s).lower()
        return re.sub(r'(the|universityof|hongkong|of)', '', s) if s else s
    for i, ce in enumerate(cur_edu):
        cd = ce.get('degree')
        if cd not in (None, ''): continue
        ci = inst_norm(ce.get('institution'))
        if not ci: continue
        best = None
        for oe in old_edu:
            oi = inst_norm(oe.get('institution'))
            if not oi: continue
            if oi in ci or ci in oi:
                od = oe.get('degree')
                if od and map_degree(od):
                    best = od
                    if len(oi) > len(inst_norm(best and best or '')) : pass
                    break
        if best:
            m = map_degree(best)
            ce['degree'] = m
            fixes.append(f'education[{i}].degree: {best!r} -> {m!r}')
    if any('->' in x and 'unmapped' not in x for x in fixes):
        tmp = path + '.tmp'
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump(cur, f, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
        restored[path] = fixes

print(f'Restored degrees in {len(restored)} files')
for p, fx in restored.items():
    print(f'\n{p}:')
    for x in fx: print(f'  {x}')
