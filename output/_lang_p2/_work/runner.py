# -*- coding: utf-8 -*-
import json, os, re, sys, importlib
sys.stdout.reconfigure(encoding='utf-8')

BASE = r'D:\ai-workspace\apec-osint-tool\output\_lang_p2'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
BATCH = sys.argv[1]
if not BATCH.endswith('.json'):
    BATCH += '.json'
OV = importlib.import_module('ov_' + BATCH.replace('batch_', '').replace('.json', '')).OV

CJK = re.compile(r'[\u3400-\u9fff\uf900-\ufaff]')

def strip_trailing_orig(s):
    s = s.strip()
    while True:
        if not s:
            return s
        last = s[-1]
        if last not in (')', '）'):
            break
        open_ch = '(' if last == ')' else '（'
        depth = 0
        idx = -1
        for k in range(len(s) - 1, -1, -1):
            c = s[k]
            if c == last:
                depth += 1
            elif c == open_ch:
                depth -= 1
                if depth == 0:
                    idx = k
                    break
        if idx < 0:
            break
        inner = s[idx + 1:-1]
        if CJK.search(inner):
            break
        s = s[:idx].strip()
    s = re.sub(r'[ \t]+', ' ', s).strip()
    return s

def main():
    with open(os.path.join(BASE, 'batches', BATCH), encoding='utf-8') as f:
        data = json.load(f)
    assert len(data) == 1000, len(data)
    assert [e['i'] for e in data] == list(range(data[0]['i'], data[0]['i'] + 1000))
    out = []
    auto_null, changed = [], 0
    for e in data:
        i, v = e['i'], e['v']
        if i in OV:
            zh = OV[i]
        elif CJK.search(v):
            zh = strip_trailing_orig(v) or None
        else:
            zh = None
            auto_null.append((i, v))
        if zh != v.strip():
            changed += 1
        out.append({"i": i, "zh": zh})
    resdir = os.path.join(BASE, 'results')
    os.makedirs(resdir, exist_ok=True)
    with open(os.path.join(resdir, BATCH), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    print('WROTE', BATCH, 'entries:', len(out), 'changed:', changed)
    print('--- AUTO NULLS (pure-latin v) ---')
    for i, v in auto_null:
        print(i, '|', v)
    print('--- OVERRIDE NULLS ---')
    for o in out:
        if o['zh'] is None and o['i'] not in dict(auto_null):
            print(o['i'])
    print('--- CHANGED OR NULL ENTRIES (i|zh) ---')
    for o, e in zip(out, data):
        if o['zh'] != e['v'].strip() or o['zh'] is None:
            print(o['i'], '|', ('' if o['zh'] is None else o['zh']))

main()
