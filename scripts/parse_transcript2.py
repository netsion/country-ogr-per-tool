import json
from datetime import datetime

path = r'C:\Users\R4314\.claude\projects\D--claude-workspace-apec-osint-tool\3c5783ca-646a-4d16-936d-d2d66e78542e\subagents\agent-a7cbbd0976d7a859e.jsonl'

events = []
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
        msg = obj.get('message', {})
        role = msg.get('role', '')
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
                        s = inp['command'][:100]
                    elif 'keyword' in inp:
                        s = inp['keyword'][:80]
                    elif 'url' in inp:
                        s = inp['url'][:100]
                    events.append((ts, 'TOOL', name + ' | ' + s))
                elif btype == 'text':
                    t = block.get('text', '')
                    if len(t) > 5:
                        events.append((ts, 'TEXT', t[:150]))
        elif isinstance(content, str) and len(content) > 5 and role == 'assistant':
            events.append((ts, 'TEXT', content[:150]))

prev = None
for ts, typ, detail in events:
    delta = ''
    if prev and ts:
        try:
            t1 = datetime.fromisoformat(prev.replace('Z', '+00:00'))
            t2 = datetime.fromisoformat(ts.replace('Z', '+00:00'))
            d = (t2 - t1).total_seconds()
            delta = '+%.0fs' % d
        except:
            pass
    prev = ts
    print('%s %7s | %6s | %s' % (ts, delta, typ, detail))
