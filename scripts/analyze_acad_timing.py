"""Analyze timing for specific agent(s)."""
import json, os, sys, io, glob
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = os.path.expanduser('~/.claude/projects/D--claude-workspace-apec-osint-tool/3c5783ca-646a-4d16-936d-d2d66e78542e/subagents')

TARGETS = sys.argv[1:] if len(sys.argv) > 1 else ['jp-p3-acad-001']

for TARGET in TARGETS:
    agent_id = None
    for meta_file in os.listdir(base):
        if not meta_file.endswith('.meta.json'):
            continue
        with open(os.path.join(base, meta_file), 'r', encoding='utf-8') as f:
            meta = json.load(f)
        if meta.get('name') == TARGET:
            agent_id = meta_file.replace('.meta.json', '')
            break

    if not agent_id:
        print(f"Agent {TARGET} not found")
        continue

    jsonl_path = os.path.join(base, agent_id + '.jsonl')
    events = []
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
            role = obj.get('message', {}).get('role', '')
            msg = obj.get('message', {})
            content = msg.get('content', '')
            tools_used = []
            text_len = 0
            if isinstance(content, list):
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get('type') == 'tool_use':
                        tn = block.get('name', '')
                        short = tn.split('__')[-1] if '__' in tn else tn
                        inp = block.get('input', {})
                        tools_used.append((short, inp))
                    elif block.get('type') == 'text':
                        text_len += len(block.get('text', ''))
            elif isinstance(content, str):
                text_len = len(content)
            events.append({'ts': ts, 'role': role, 'tools': tools_used, 'text_len': text_len})

    for e in events:
        try:
            e['dt'] = datetime.fromisoformat(e['ts'].replace('Z', '+00:00'))
        except:
            e['dt'] = None

    if not events:
        print(f"No events for {TARGET}")
        continue

    first = events[0]['dt']
    last = events[-1]['dt']
    total = (last - first).total_seconds()

    print(f"\n=== {TARGET}: {total:.0f}s ({total/60:.1f}m) ===")

    # Count tools
    tool_counts = {}
    write_method = "unknown"
    edit_count = 0
    write_count = 0
    bash_count = 0
    search_count = 0
    readurl_count = 0

    for e in events:
        for tn, inp in e['tools']:
            tool_counts[tn] = tool_counts.get(tn, 0) + 1
            if tn == 'Write':
                write_count += 1
                fp = inp.get('file_path', '')
                if '.json' in fp:
                    write_method = "Write direct JSON"
                elif '.py' in fp:
                    write_method = "Write .py script"
            elif tn == 'Edit':
                edit_count += 1
            elif tn == 'Bash':
                bash_count += 1
            elif tn == 'search':
                search_count += 1
            elif tn == 'read_url':
                readurl_count += 1

    print(f"  Write method: {write_method}")
    print(f"  Tool calls: Write:{write_count} Edit:{edit_count} Bash:{bash_count} search:{search_count} read_url:{readurl_count}")

    # Find major gaps
    gaps = []
    for i in range(1, len(events)):
        if events[i]['dt'] is None or events[i-1]['dt'] is None:
            continue
        gap = (events[i]['dt'] - events[i-1]['dt']).total_seconds()
        if gap > 20:
            prev_tools = [t[0] for t in events[i-1]['tools']] if events[i-1]['tools'] else ['text']
            gaps.append((i, gap, events[i-1]['role'], events[i]['role'], prev_tools))

    # Phase analysis
    think_gaps = [g for g in gaps if g[2] == 'user' and g[3] == 'assistant']
    tool_gaps = [g for g in gaps if g[2] == 'assistant' and g[3] == 'user']

    total_think = sum(g[1] for g in think_gaps)
    total_tool = sum(g[1] for g in tool_gaps)

    print(f"\n  LLM thinking: {total_think:.0f}s ({total_think/total*100:.0f}%)")
    print(f"  Tool execution: {total_tool:.0f}s ({total_tool/total*100:.0f}%)")
    print(f"  Other: {total - total_think - total_tool:.0f}s ({(total-total_think-total_tool)/total*100:.0f}%)")

    # Show big gaps
    big_gaps = sorted(gaps, key=lambda x: -x[1])[:10]
    print(f"\n  Top 10 gaps:")
    for idx, gap, r1, r2, tools in big_gaps:
        elapsed = (events[idx-1]['dt'] - first).total_seconds()
        print(f"    @{elapsed:>6.0f}s: {gap:>5.0f}s ({r1}->{r2}) after {','.join(tools)}")
