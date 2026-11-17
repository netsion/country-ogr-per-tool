import json, os, glob
from datetime import datetime

base = r'C:\Users\R4314\.claude\projects\D--claude-workspace-apec-osint-tool\3c5783ca-646a-4d16-936d-d2d66e78542e\subagents'

# Only JP P3 agents
jp_names = ['jp-p3-gov-001', 'jp-p3-gov-002', 'jp-p3-gov-003', 'jp-p3-gov-004',
            'jp-p3-gov-005', 'jp-p3-gov-006', 'jp-p3-gov-007', 'jp-p3-gov-008',
            'jp-p3-gov-009', 'jp-p3-gov-010']

results = []

for name in jp_names:
    # Find meta file with this name
    found = False
    for meta_file in glob.glob(os.path.join(base, '*.meta.json')):
        with open(meta_file, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        if meta.get('name') == name:
            agent_id = os.path.basename(meta_file).replace('.meta.json', '')
            jsonl_path = os.path.join(base, f'{agent_id}.jsonl')
            if not os.path.exists(jsonl_path):
                continue

            first_ts = None
            last_ts = None
            search_count = 0
            readurl_count = 0
            write_count = 0

            with open(jsonl_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line: continue
                    try:
                        obj = json.loads(line)
                    except: continue
                    ts = obj.get('timestamp', '')
                    if not ts: continue
                    if not first_ts: first_ts = ts
                    last_ts = ts
                    msg = obj.get('message', {})
                    content = msg.get('content', '')
                    if isinstance(content, list):
                        for block in content:
                            if not isinstance(block, dict): continue
                            if block.get('type') == 'tool_use':
                                tn = block.get('name', '')
                                if tn == 'mcp__search-read__search': search_count += 1
                                elif tn == 'mcp__search-read__read_url': readurl_count += 1
                                elif tn == 'Write': write_count += 1

            try:
                t1 = datetime.fromisoformat(first_ts.replace('Z', '+00:00'))
                t2 = datetime.fromisoformat(last_ts.replace('Z', '+00:00'))
                duration = (t2 - t1).total_seconds()
            except:
                duration = 0

            results.append({
                'name': name,
                'duration': duration,
                'search': search_count,
                'readurl': readurl_count,
                'write': write_count,
            })
            found = True
            break
    if not found:
        results.append({'name': name, 'duration': 0, 'search': 0, 'readurl': 0, 'write': 0})

# Map to org names
org_map = {
    'jp-p3-gov-001': 'JP-GOV-001 内阁官房',
    'jp-p3-gov-002': 'JP-GOV-002 内阁府',
    'jp-p3-gov-003': 'JP-GOV-003 总务省',
    'jp-p3-gov-004': 'JP-GOV-004 法务省',
    'jp-p3-gov-005': 'JP-GOV-005 外务省',
    'jp-p3-gov-006': 'JP-GOV-006 财务省',
    'jp-p3-gov-007': 'JP-GOV-007 文部科学省',
    'jp-p3-gov-008': 'JP-GOV-008 厚生劳动省',
    'jp-p3-gov-009': 'JP-GOV-009 农林水产省',
    'jp-p3-gov-010': 'JP-GOV-010 经济产业省',
}

print(f'{"Batch":>4} | {"Org":>24} | {"Duration":>10} | {"Search":>6} | {"ReadURL":>7} | {"Write":>5}')
print('-' * 80)

for i in range(0, len(results), 2):
    batch_num = i // 2 + 1
    batch = results[i:i+2]
    max_dur = max(r['duration'] for r in batch)
    for r in batch:
        d = r['duration']
        label = org_map.get(r['name'], r['name'])
        print(f'{batch_num:>4} | {label:>24} | {d:>7.0f}s ({d/60:.1f}m) | {r["search"]:>6} | {r["readurl"]:>7} | {r["write"]:>5}')
    if len(batch) == 2:
        print(f'     | {"wall clock":>24} | {max_dur:>7.0f}s ({max_dur/60:.1f}m) |')
    print()

total_agent = sum(r['duration'] for r in results)
print(f'Total agent time:  {total_agent:.0f}s ({total_agent/60:.1f}m)')
print(f'Avg per org:       {total_agent/len(results):.0f}s ({total_agent/len(results)/60:.1f}m)')
print(f'Avg search/org:    {sum(r["search"] for r in results)/len(results):.1f}')
print(f'Avg read_url/org:  {sum(r["readurl"] for r in results)/len(results):.1f}')
