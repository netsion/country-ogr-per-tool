# 重试下载剩余 Wikimedia 头像（429 限流解除后运行）
# 用法: python scripts_tmp/retry_wikimedia_downloads.py [--loop]
# --loop: 全部成功或尝试 5 轮后退出
import json, subprocess, time, os, sys

BASE = 'output/ng/2026-11-10'
jobs = json.load(open('scripts_tmp/_retry_jobs.json', encoding='utf-8'))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36'

def dl(pid, url, lp, direct):
    os.makedirs(os.path.dirname(lp), exist_ok=True)
    proxy = [] if direct else ['-x', 'http://127.0.0.1:7897']
    try:
        r = subprocess.run(['curl', '-s'] + proxy + ['--max-time', '60', '-A', UA,
                            '-o', lp, '-w', '%{http_code}', url],
                           capture_output=True, text=True, timeout=90)
        code = r.stdout.strip() or '000'
        if code == '200' and os.path.exists(lp) and os.path.getsize(lp) > 3000:
            return True, code
        if os.path.exists(lp) and os.path.getsize(lp) <= 3000:
            os.remove(lp)
        return False, code
    except Exception as e:
        return False, f'EXC:{e.__class__.__name__}'

rounds = 5 if '--loop' in sys.argv else 1
pending = jobs
for rnd in range(1, rounds + 1):
    print(f'=== round {rnd}: {len(pending)} jobs ===')
    still = []
    for n, j in enumerate(pending):
        ok, code = dl(j['pid'], j['url'], j['lp'], j.get('direct', False))
        print(f'  [{n+1}/{len(pending)}] {j["pid"]} {"OK" if ok else code}')
        if not ok:
            still.append(j)
        time.sleep(20)
    pending = still
    if not pending:
        break
    if rnd < rounds:
        print('waiting 600s for rate-limit window...')
        time.sleep(600)

json.dump(pending, open('scripts_tmp/_retry_jobs.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(f'FINAL: success={len(jobs)-len(pending)} still-failed={len(pending)}')
if pending:
    for j in pending:
        print('  PENDING:', j['pid'], j['url'][:70])
