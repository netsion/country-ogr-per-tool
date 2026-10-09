"""P4B orchestration: social-account + avatar enrichment, rolling dispatch."""
import json
import sys

BASE = "output/ci/2026-10-06"
PROG = f"{BASE}/_p4b_progress.json"

BAD_SOURCE = {"CI-PERSON-000114", "CI-PERSON-000118", "CI-PERSON-000178", "CI-PERSON-000331", "CI-PERSON-000354"}


def load():
    return json.load(open(PROG, encoding="utf-8"))


def save(p):
    with open(PROG, "w", encoding="utf-8") as f:
        json.dump(p, f, ensure_ascii=False, indent=2)


def next_batch(n=4):
    p = load()
    idle = [t for t in p["targets"] if t not in p["completed"] and t not in p["current"] and t not in p["failed"]]
    print(json.dumps(idle[:n]))


def mark(pid):
    p = load()
    if pid in p["targets"] and pid not in p["completed"] and pid not in p["current"]:
        p["current"].append(pid)
        save(p)
        print(f"marked: {pid} in flight | completed={len(p['completed'])} remaining={len(p['targets'])-len(p['completed'])-len(p['current'])-len(p['failed'])} current={len(p['current'])}")
    else:
        print(f"cannot mark {pid}")


def prompt(pid):
    p = load()
    d = json.load(open(f"{BASE}/persons/{pid}.json", encoding="utf-8"))
    name = d.get("name") or pid
    zh = d.get("name_zh") or ""
    prof = d.get("profile") or {}
    url = prof.get("source_url") or ""
    lp = prof.get("local_path") or ""
    socs = d.get("social_accounts") or []
    soc_desc = ", ".join(f"{a.get('platform')}:{a.get('url','')[:40]}" for a in socs) if socs else "（当前为空）"
    need_soc = "无社交账号，需补采" if not socs else "已有部分，需核查补充"
    av_task = "已有链接但无效/非直链，需换新直链并重新下载" if (pid in BAD_SOURCE or url) else "缺失，需查找并下载"
    known = f"已知照片 local_path={lp}（文件在盘，仅需核实/替换 source_url）" if lp else "无本地文件"
    print(f"""人物：{pid}（{zh} / {name}）
社交账号现状：{need_soc}。现有：{soc_desc}
头像现状：{av_task}。source_url={url or '（空）'}；{known}""")


def check(pid):
    fp = f"{BASE}/persons/{pid}.json"
    d = json.load(open(fp, encoding="utf-8"))
    prof = d.get("profile") or {}
    ok_url = bool((prof.get("source_url") or "").strip())
    lp = (prof.get("local_path") or "").strip()
    ok_file = bool(lp) and os.path.exists(os.path.join(BASE, lp))
    print(json.dumps({
        "social_accounts": len(d.get("social_accounts") or []),
        "has_source_url": ok_url,
        "local_path": lp,
        "local_exists": ok_file,
    }, ensure_ascii=False))


def advance(pid):
    p = load()
    if pid in p["current"]:
        p["current"].remove(pid)
    if pid not in p["completed"]:
        p["completed"].append(pid)
    save(p)
    print(f"advanced: {pid} | completed={len(p['completed'])}/{len(p['targets'])} remaining={len(p['targets'])-len(p['completed'])-len(p['failed'])}")


def fail(pid, reason=""):
    p = load()
    if pid in p["current"]:
        p["current"].remove(pid)
    if pid not in p["failed"]:
        p["failed"].append({"pid": pid, "reason": reason})
    save(p)
    print(f"failed: {pid} ({reason})")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "next":
        next_batch(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif cmd in ("mark", "prompt", "check", "advance"):
        globals()[cmd](sys.argv[2])
    elif cmd == "fail":
        fail(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
    else:
        print("usage: next|mark|prompt|check|advance|fail")
