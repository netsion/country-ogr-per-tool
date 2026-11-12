# -*- coding: utf-8 -*-
"""Batch A+B cleanup: explicit temp dirs, root junk, dataset-dir residue.

Safety rules:
  - never touch tracked git files (batch A/B are untracked only)
  - whitelist: .mcp.json at root
  - keep: minio-store, tmp/ (lite artifacts), docs, scripts*, .agents, upload_kit_stage
  - dry-run prints plan; --apply executes
"""
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
ROOT = "D:/ai-workspace/apec-osint-tool"
DRY = "--apply" not in sys.argv

tracked = set(subprocess.run(["git", "ls-files"], capture_output=True,
                             text=True, cwd=ROOT).stdout.splitlines())

# dirs to prune while walking (explicit temp/cache patterns)
TEMP_DIR_RE = re.compile(r"^(_tmp|tmp|_cache|cache|wiki|_raw|_avtmp|_av2?_?tmp|_archived.*|\.tmp.*|_p\d+_tmp.*)$", re.I)
# root keep-list
ROOT_KEEP = {".mcp.json"}
# top-level dirs that are legit (never touch)
ROOT_KEEP_DIRS = {".git", ".agents", ".claude", ".zcode", ".cache", ".cache_tmp",
                  "__pycache__", "docs", "minio-store", "output", "scripts",
                  "scripts_tmp", "tmp", "upload_kit_stage", ".vscode", ".idea",
                  "node_modules"}
# files under output/ tree to always keep (docs-referenced legacy tool)
OUTPUT_FILE_KEEP = {"output/_fix_wiki_file_avatars.py"}
# subtree to skip entirely (audit ledger + recoverable trash)
SKIP_SUBTREE = {"output/_avatar_audit"}

# dataset-dir file rules (untracked only):
#   batch B: everything that is NOT a legit registry/list json inside output/<cc>/<date>/
LEGIT_DATASET_FILE = re.compile(
    r"^(person_list\.json|org_list\.json|id_registry\.json|_target_orgs\.json|"
    r"_name_index\.json|_phase_progress\.json|_coverage_report\.json|coverage_report\.json|"
    r".*_queue\.json|remaining_persons\.json|.*_progress.*\.json|_missing_persons.*\.json|"
    r"\.inflight)$")
EXT_DELETE = re.compile(
    r"\.(html?|pdf|txt|xml|jpg|jpeg|png|gif|webp|svg|avif|ico|jp2|bmp|bin|js|"
    r"csv|tsv|md|htm|docx?|xlsx?|pptx?|rq|jsonl|pkl|b64|b64txt)$", re.I)


def kill(f):
    if DRY:
        return 1, os.path.getsize(f) if os.path.isfile(f) else 0
    try:
        if os.path.isdir(f):
            import shutil
            shutil.rmtree(f)
            return 1, 0
        sz = os.path.getsize(f)
        os.remove(f)
        return 1, sz
    except OSError as e:
        print("ERR", f, str(e)[:60])
        return 0, 0


n_root = n_tmpdir = n_ds = 0
sz_root = sz_tmpdir = sz_ds = 0

# --- batch A1: root-level untracked files AND junk dirs ---
for fn in os.listdir(ROOT):
    p = os.path.join(ROOT, fn)
    if os.path.isdir(p):
        if fn in ROOT_KEEP_DIRS:
            continue
        # untracked junk dir at root (tmp_mo/, _av2/, --allow-register/, .tmp_avatar_b/ ...)
        total = 0
        for dp, _, fs in os.walk(p):
            for f in fs:
                try: total += os.path.getsize(os.path.join(dp, f))
                except OSError: pass
        ok, _ = kill(p)
        n_root += ok; sz_root += total
        continue
    if fn in ROOT_KEEP:
        continue
    if fn in tracked:
        continue
    ok, sz = kill(p)
    n_root += ok; sz_root += sz

# --- batch A2+B: walk output/ ---
os.chdir(ROOT)
for dirpath, dirnames, filenames in os.walk("output"):
    # skip audit subtree entirely
    if "output" + os.sep + "_avatar_audit" in dirnames:
        dirnames.remove("_avatar_audit")
    # in-flight datasets: skip ENTIRE dataset dir (highest priority protection)
    if os.path.exists(os.path.join(dirpath, ".inflight")):
        dirnames[:] = []
        continue
    # prune temp dirs entirely
    pruned = [d for d in dirnames
              if TEMP_DIR_RE.match(d)
              and os.path.normpath(os.path.join(dirpath, d)).replace("\\", "/")
              not in tracked]
    for d in pruned:
        p = os.path.join(dirpath, d)
        total = 0
        for dp, _, fs in os.walk(p):
            for f in fs:
                try: total += os.path.getsize(os.path.join(dp, f))
                except OSError: pass
        ok, _ = kill(p)
        n_tmpdir += ok; sz_tmpdir += total
    dirnames[:] = [d for d in dirnames if d not in pruned]
    for fn in filenames:
        f = os.path.normpath(os.path.join(dirpath, fn)).replace("\\", "/")
        if f in OUTPUT_FILE_KEEP:
            continue
        if f in tracked:
            continue  # batch C handles tracked junk separately
        if LEGIT_DATASET_FILE.match(fn):
            continue
        # untracked file in dataset tree: delete if it is NOT persons/orgs json
        if re.search(r"/(persons|orgs)/[^/]+\.json$", f):
            continue  # real data json (untracked but legit, e.g. CL recovered)
        ok, sz = kill(f.replace("/", os.sep))
        n_ds += ok; sz_ds += sz

mb = lambda b: b / 1048576
print(("DRY-RUN" if DRY else "APPLIED"))
print(f"root junk:       {n_root:5} files  {mb(sz_root):8.1f} MB")
print(f"temp dirs:       {n_tmpdir:5} dirs   {mb(sz_tmpdir):8.1f} MB")
print(f"dataset residue: {n_ds:5} files  {mb(sz_ds):8.1f} MB")
print(f"TOTAL:           {mb(sz_root+sz_tmpdir+sz_ds):.1f} MB")
