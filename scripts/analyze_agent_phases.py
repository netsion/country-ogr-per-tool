"""Deep timing analysis for a single sub-agent transcript."""
import json, os, sys, io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

base = os.path.expanduser('~/.claude/projects/D--claude-workspace-apec-osint-tool/3c5783ca-646a-4d16-936d-d2d66e78542e/subagents')

# Target agent
TARGET = 'jp-p3-corp-018'

# Find the agent
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
    sys.exit(1)

jsonl_path = os.path.join(base, agent_id + '.jsonl')

# Parse all events with timestamps
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

        # Extract tool calls and text
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

        events.append({
            'ts': ts,
            'role': role,
            'tools': tools_used,
            'text_len': text_len,
        })

# Convert timestamps
for e in events:
    try:
        e['dt'] = datetime.fromisoformat(e['ts'].replace('Z', '+00:00'))
    except:
        e['dt'] = None

# Print timeline
print(f"=== Timeline for {TARGET} ===")
print(f"Total events: {len(events)}")
if events:
    first = events[0]['dt']
    last = events[-1]['dt']
    total = (last - first).total_seconds()
    print(f"Total duration: {total:.0f}s ({total/60:.1f}m)")
    print()

    # Categorize into phases
    phases = []
    current_phase = None
    phase_start = None
    phase_tools = []

    for i, e in enumerate(events):
        if e['dt'] is None:
            continue
        elapsed = (e['dt'] - first).total_seconds()

        if e['role'] == 'user':
            # tool results come back
            if current_phase:
                phases.append({
                    'name': current_phase,
                    'start': phase_start,
                    'end': elapsed,
                    'duration': elapsed - phase_start,
                    'tools': list(phase_tools),
                })
            # The next assistant message will set the new phase
            current_phase = None
            continue

        if e['role'] == 'assistant' and e['tools']:
            # Tool use — record what tool
            for tn, inp in e['tools']:
                desc = ''
                if tn == 'search':
                    kw = inp.get('keyword', '')
                    desc = f'search("{kw[:50]}")'
                elif tn == 'read_url':
                    url = inp.get('url', '')
                    desc = f'read_url("{url[:60]}")'
                elif tn == 'Read':
                    fp = inp.get('file_path', '')
                    desc = f'Read("{fp[-60:] if len(fp) > 60 else fp}")'
                elif tn == 'Write':
                    fp = inp.get('file_path', '')
                    desc = f'Write("{fp[-50:] if len(fp) > 50 else fp}")'
                elif tn == 'Bash':
                    cmd = inp.get('command', '')
                    desc = f'Bash("{cmd[:60]}")'
                elif tn == 'Edit':
                    fp = inp.get('file_path', '')
                    desc = f'Edit("{fp[-50:] if len(fp) > 50 else fp}")'
                elif tn == 'Grep':
                    pat = inp.get('pattern', '')
                    desc = f'Grep("{pat[:40]}")'
                else:
                    desc = f'{tn}()'

                if current_phase is None:
                    current_phase = f'[~{elapsed:.0f}s] {desc}'
                    phase_start = elapsed
                    phase_tools = []
                phase_tools.append(desc)

    # Close last phase
    if current_phase:
        phases.append({
            'name': current_phase,
            'start': phase_start,
            'end': (last - first).total_seconds(),
            'duration': (last - first).total_seconds() - phase_start,
            'tools': list(phase_tools),
        })

    # Group into macro phases
    print("--- By turn (assistant messages grouped) ---")
    turn_idx = 0
    for e in events:
        if e['role'] != 'assistant':
            continue
        if e['dt'] is None:
            continue
        elapsed = (e['dt'] - first).total_seconds()
        turn_idx += 1

        # Find next event timestamp to calculate thinking+output time
        next_ts = None
        idx = events.index(e)
        for j in range(idx+1, len(events)):
            if events[j]['dt'] and events[j]['dt'] != e['dt']:
                next_ts = events[j]['dt']
                break

        think_time = ''
        if next_ts:
            gap = (next_ts - e['dt']).total_seconds()
            if gap > 5:
                think_time = f' [wait {gap:.0f}s]'

        tools_str = ''
        if e['tools']:
            parts = []
            for tn, inp in e['tools']:
                if tn == 'search':
                    kw = inp.get('keyword', '')[:40]
                    parts.append(f'search("{kw}")')
                elif tn == 'read_url':
                    url = inp.get('url', '')[:50]
                    parts.append(f'read("{url}")')
                elif tn == 'Write':
                    fp = inp.get('file_path', '')[-40:]
                    parts.append(f'Write({fp})')
                elif tn == 'Bash':
                    cmd = inp.get('command', '')[:50]
                    parts.append(f'Bash("{cmd}")')
                elif tn == 'Edit':
                    fp = inp.get('file_path', '')[-40:]
                    parts.append(f'Edit({fp})')
                else:
                    parts.append(tn)
            tools_str = ' | '.join(parts)
        else:
            tools_str = f'[text only, {e["text_len"]} chars]'

        print(f"  T{turn_idx:>2d} @{elapsed:>6.0f}s: {tools_str}{think_time}")

    # Summary statistics
    print()
    print("--- Time breakdown ---")

    # Calculate gaps between events (LLM thinking time vs tool execution)
    total_think = 0
    total_tool = 0
    gaps = []
    for i in range(1, len(events)):
        if events[i]['dt'] is None or events[i-1]['dt'] is None:
            continue
        gap = (events[i]['dt'] - events[i-1]['dt']).total_seconds()
        if gap > 2:
            gaps.append((i, gap, events[i-1]['role'], events[i]['role']))

    if gaps:
        think_gaps = [g for g in gaps if g[2] == 'user' and g[3] == 'assistant']
        tool_gaps = [g for g in gaps if g[2] == 'assistant' and g[3] == 'user']

        print(f"  LLM thinking gaps (user->assistant): {len(think_gaps)} events")
        for idx, gap, r1, r2 in think_gaps:
            print(f"    @{(events[idx-1]['dt'] - first).total_seconds():.0f}s: {gap:.0f}s wait")
        total_think = sum(g[1] for g in think_gaps)

        print(f"  Tool execution gaps (assistant->user): {len(tool_gaps)} events")
        for idx, gap, r1, r2 in tool_gaps:
            # What tool was called
            prev = events[idx-1]
            tool_names = [t[0] for t in prev.get('tools', [])] if prev.get('tools') else ['?']
            elapsed = (events[idx-1]['dt'] - first).total_seconds()
            print(f"    @{elapsed:.0f}s: {gap:.0f}s for {', '.join(tool_names)}")
        total_tool = sum(g[1] for g in tool_gaps)

    print()
    print(f"  Total LLM thinking: {total_think:.0f}s ({total_think/60:.1f}m, {total_think/total*100:.0f}%)" if total > 0 else "")
    print(f"  Total tool execution: {total_tool:.0f}s ({total_tool/60:.1f}m, {total_tool/total*100:.0f}%)" if total > 0 else "")
    other = total - total_think - total_tool
    print(f"  Other (text output, etc): {other:.0f}s ({other/60:.1f}m, {other/total*100:.0f}%)" if total > 0 else "")
