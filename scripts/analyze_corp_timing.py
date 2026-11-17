import json, os, glob, sys, io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = os.path.expanduser('~/.claude/projects/D--claude-workspace-apec-osint-tool/3c5783ca-646a-4d16-936d-d2d66e78542e/subagents')

corp_agents = []
for meta_file in glob.glob(os.path.join(base, '*.meta.json')):
    with open(meta_file, 'r', encoding='utf-8') as f:
        meta = json.load(f)
    name = meta.get('name', '')
    if 'corp' not in name.lower():
        continue
    agent_id = os.path.basename(meta_file).replace('.meta.json', '')
    jsonl_path = os.path.join(base, agent_id + '.jsonl')
    if not os.path.exists(jsonl_path):
        continue

    first_ts = None
    last_ts = None
    tool_calls = {}

    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except:
                continue
            ts = obj.get('timestamp', '')
            if not ts:
                continue
            if not first_ts:
                first_ts = ts
            last_ts = ts
            msg = obj.get('message', {})
            content = msg.get('content', '')
            if isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get('type') == 'tool_use':
                        tn = block.get('name', '')
                        short = tn.split('__')[-1] if '__' in tn else tn
                        tool_calls[short] = tool_calls.get(short, 0) + 1

    try:
        t1 = datetime.fromisoformat(first_ts.replace('Z', '+00:00'))
        t2 = datetime.fromisoformat(last_ts.replace('Z', '+00:00'))
        duration = (t2 - t1).total_seconds()
    except:
        duration = 0

    corp_agents.append({
        'name': name,
        'duration': duration,
        'tools': tool_calls,
    })

corp_agents.sort(key=lambda x: -x['duration'])

print(f"{'Agent':25s} | {'Duration':>12s} | Tool calls")
print('-' * 90)
for a in corp_agents:
    tstr = ', '.join(f'{k}:{v}' for k, v in sorted(a['tools'].items(), key=lambda x: -x[1]))
    print(f"{a['name']:25s} | {a['duration']:>7.0f}s ({a['duration']/60:.1f}m) | {tstr}")
