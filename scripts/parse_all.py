import json
from datetime import datetime

agents = {
    'Baldwin': 'agent-a774df79484eba990',
    'Crafar': 'agent-ae4f862ad149b6c96',
    'Plested': 'agent-a15ce683db2e541b3',
    'Brownlee': 'agent-a4f04cfe67c436f7a',
}

base = r'C:\Users\R4314\.claude\projects\D--claude-workspace-apec-osint-tool\3c5783ca-646a-4d16-936d-d2d66e78542e\subagents'

for label, agent_id in agents.items():
    path = f'{base}\\{agent_id}.jsonl'
    events = []
    first_ts = None
    last_ts = None

    with open(path, 'r', encoding='utf-8') as f:
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
                    btype = block.get('type', '')
                    if btype == 'tool_use':
                        name = block.get('name', '')
                        inp = block.get('input', {})
                        s = ''
                        if 'file_path' in inp:
                            s = inp['file_path'].split('\\')[-1]
                        elif 'command' in inp:
                            s = inp['command'][:80]
                        elif 'keyword' in inp:
                            s = inp['keyword'][:60]
                        elif 'url' in inp:
                            s = inp['url'][:80]
                        events.append((ts, name, s))

    # Calculate total time
    try:
        t1 = datetime.fromisoformat(first_ts.replace('Z', '+00:00'))
        t2 = datetime.fromisoformat(last_ts.replace('Z', '+00:00'))
        total = (t2 - t1).total_seconds()
    except:
        total = 0

    # Count phases
    search_count = sum(1 for _, n, _ in events if n == 'mcp__search-read__search')
    readurl_count = sum(1 for _, n, _ in events if n == 'mcp__search-read__read_url')

    # Find key timestamps
    first_search = None
    first_readurl = None
    write_ts = None
    for ts, name, _ in events:
        if name == 'mcp__search-read__search' and not first_search:
            first_search = ts
        if name == 'mcp__search-read__read_url' and not first_readurl:
            first_readurl = ts
        if name == 'Write':
            write_ts = ts

    def to_epoch(ts):
        try:
            return datetime.fromisoformat(ts.replace('Z', '+00:00')).timestamp()
        except:
            return 0

    file_reading_s = to_epoch(first_search) - to_epoch(first_ts) if first_search else 0
    search_phase_s = to_epoch(write_ts) - to_epoch(first_search) if write_ts and first_search else 0
    write_valid_s = to_epoch(last_ts) - to_epoch(write_ts) if write_ts else 0

    print(f'\n=== {label} ({agent_id}) ===')
    print(f'Total: {total:.0f}s ({total/60:.1f}min)')
    print(f'File reading: {file_reading_s:.0f}s')
    print(f'Search+read_url phase: {search_phase_s:.0f}s ({search_count} searches + {readurl_count} reads)')
    print(f'Write+validate phase: {write_valid_s:.0f}s')
    print()
    # Detailed timeline
    prev = None
    for ts, name, detail in events:
        delta = ''
        if prev:
            try:
                d1 = datetime.fromisoformat(prev.replace('Z', '+00:00'))
                d2 = datetime.fromisoformat(ts.replace('Z', '+00:00'))
                d = (d2 - d1).total_seconds()
                delta = '+%.0fs' % d
            except:
                pass
        prev = ts
        short_name = name.replace('mcp__search-read__', '')
        print(f'  {ts} {delta:>7s} | {short_name:12s} | {detail[:80]}')
