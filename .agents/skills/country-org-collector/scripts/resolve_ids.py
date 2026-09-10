#!/usr/bin/env python3
"""
resolve_ids.py — 扫描 null ID，精确匹配 name_index，按需分配新 ID 并注册

用法:
  python scripts/resolve_ids.py output/kr/2026-04-28 [--dry-run]
  python scripts/resolve_ids.py output/kr/2026-04-28 --allow-register [--max-register 30]
  python scripts/resolve_ids.py output/kr/2026-04-28 --allow-register --allow-register-work-orgs

功能:
  1. 读取 _name_index.json（精确查找表，含 decompose 分解匹配）
  2. 扫描 orgs/*.json 中 related_entities[].org_id 和 key_people[].person_id
  3. 扫描 persons/*.json 中 work_experience[].org_id 和 person_relationships[].person_id
  4. 精确匹配 name → 有则填 ID
  5. 无匹配 → 默认保持 null 并列入报告；仅当显式给出 --allow-register 时才分配新 ID

护栏（防幽灵 ID 事故）:
  --allow-register        显式开启自动注册（默认关闭！）
  --max-register N        本次运行注册上限（默认 20），超出部分保持 null 并报告
  --allow-register-work-orgs  人物 work_experience 的未注册组织默认只报告不注册，
                          加此标志才允许（注册需自行确认 org_type）
  计数器防回卷: 加载后扫描磁盘上已有的 org/person ID，计数器低于真实 max+1 时自动修正
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import glob
import re
import tempfile

# Add scripts dir to path for shared imports
sys.path.insert(0, os.path.dirname(__file__))
from atomic_write import decompose_name

# org_type 映射：用于从组织名称推断 ID 前缀
ORG_TYPE_MAP = {
    "GOV": "GOV", "SOE": "SOE", "CORP": "CORP", "NGO": "NGO",
    "ACAD": "ACAD", "MEDIA": "MEDIA", "FIN": "FIN", "INTL": "INTL",
    "PARTY": "PARTY", "MIL": "MIL",
}

# Stats counters for decomposed matches
_decompose_hits = {"exact": 0, "decomposed": 0}


class Guardrails:
    """Registration guardrail state."""
    def __init__(self, allow_register, max_register, allow_work_orgs):
        self.allow_register = allow_register
        self.max_register = max_register
        self.allow_work_orgs = allow_work_orgs
        self.registered = 0        # used this run
        self.overflow = 0          # blocked by cap
        self.blocked_no_flag = 0   # blocked because --allow-register not given
        self.blocked_work_orgs = 0 # blocked because --allow-register-work-orgs not given
        self.registry_log = []     # (kind, id, name)

    def can_register(self, kind="org"):
        """Returns (True, '') or (False, reason)."""
        if not self.allow_register:
            self.blocked_no_flag += 1
            return False, "auto-register disabled (use --allow-register)"
        if kind == "work-org" and not self.allow_work_orgs:
            self.blocked_work_orgs += 1
            return False, "work-org registration disabled (use --allow-register-work-orgs)"
        if self.registered >= self.max_register:
            self.overflow += 1
            return False, f"registration cap reached (--max-register {self.max_register})"
        return True, ""

    def note_registered(self, kind, new_id, name):
        self.registered += 1
        self.registry_log.append((kind, new_id, name))


def lookup_name(name, index):
    """Look up a name in the index, trying exact match first then decomposed components.

    Returns (id_or_None, method_str).
    """
    if name in index:
        _decompose_hits["exact"] += 1
        return index[name], "exact"
    for component in decompose_name(name):
        if component in index:
            _decompose_hits["decomposed"] += 1
            return index[component], "decomposed"
    return None, None


def load_json_safe(path):
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None


def save_json_atomic(path, data):
    dir_path = os.path.dirname(path)
    os.makedirs(dir_path, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dir_path, prefix=".tmp_", suffix=os.path.basename(path), text=True)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


_ID_SEQ_RE = re.compile(r'-(\d+)$')


def _reconcile_counters(registry, output_dir, iso):
    """Scan disk + registry for the true max sequence per counter key, and bump
    counters upward if they are stale. Prevents the duplicate-ID failure mode where
    a corrupted/stale counter re-allocates already-used numbers."""
    counters = registry.setdefault("counters", {})
    pcounters = registry.setdefault("person_counters", {})

    def bump(counter_map, key, seq):
        if seq > counter_map.get(key, 0):
            old = counter_map.get(key, 0)
            counter_map[key] = seq
            if old:
                print(f"  COUNTER FIX: {key} {old} -> {seq} (stale counter reconciled from disk/registry)")

    # registry-declared IDs
    for entry in registry.get("registry", []):
        oid = entry.get("org_id") or ""
        m = re.match(r'^([A-Z]{2})-([A-Z]+)-(\d+)$', oid)
        if m and m.group(1) == iso:
            bump(counters, f"{iso}-{m.group(2)}", int(m.group(3)))
    for entry in registry.get("person_registry", []):
        pid = entry.get("person_id") or ""
        m = re.match(r'^([A-Z]{2})-PERSON-(\d+)$', pid)
        if m and m.group(1) == iso:
            bump(pcounters, f"{iso}-PERSON", int(m.group(2)))

    # on-disk profile files (authoritative: a file with an id means the number is taken)
    orgs_dir = os.path.join(output_dir, "orgs")
    if os.path.isdir(orgs_dir):
        for fname in os.listdir(orgs_dir):
            m = re.match(rf'^{iso}-([A-Z]+)-(\d+)\.json$', fname)
            if m:
                bump(counters, f"{iso}-{m.group(1)}", int(m.group(2)))
    persons_dir = os.path.join(output_dir, "persons")
    if os.path.isdir(persons_dir):
        for fname in os.listdir(persons_dir):
            m = re.match(rf'^{iso}-PERSON-(\d+)\.json$', fname)
            if m:
                bump(pcounters, f"{iso}-PERSON", int(m.group(1)))


def get_next_org_id(registry, iso, org_type="GOV"):
    """获取下一个 org_id。格式: {ISO}-{TYPE}-{SEQ:03d}"""
    key = f"{iso}-{org_type}"
    counters = registry.get("counters", {})
    seq = counters.get(key, 0) + 1
    counters[key] = seq
    registry["counters"] = counters
    return f"{iso}-{org_type}-{seq:03d}"


def get_next_person_id(registry, iso):
    """获取下一个 person_id。格式: {ISO}-PERSON-{SEQ:06d}"""
    key = f"{iso}-PERSON"
    counters = registry.get("person_counters", {})
    seq = counters.get(key, 0) + 1
    counters[key] = seq
    registry["person_counters"] = counters
    return f"{iso}-PERSON-{seq:06d}"


def register_new_org(registry, index, iso, name, org_type="GOV"):
    """注册新组织到 registry 和 index。返回 org_id。"""
    org_id = get_next_org_id(registry, iso, org_type)
    entry = {
        "org_id": org_id,
        "name": name,
        "org_type": org_type,
        "status": "auto_registered",
    }
    registry.setdefault("registry", []).append(entry)
    index[name] = org_id
    return org_id


def register_new_person(registry, index, iso, name):
    """注册新人物到 registry 和 index。返回 person_id。"""
    person_id = get_next_person_id(registry, iso)
    entry = {
        "person_id": person_id,
        "name_en": name,
        "importance_level": "low",
        "org_ids": [],
    }
    registry.setdefault("person_registry", []).append(entry)
    index[name] = person_id
    return person_id


def resolve_orgs(output_dir, index, registry, iso, dry_run, guard):
    """扫描 orgs/*.json，解析 null org_id 和 person_id。"""
    orgs_dir = os.path.join(output_dir, "orgs")
    if not os.path.isdir(orgs_dir):
        return 0, 0, 0

    filled_org = 0
    filled_person = 0
    new_registered = 0

    for fpath in glob.glob(os.path.join(orgs_dir, "*.json")):
        if os.path.basename(fpath).startswith("_"):
            continue
        profile = load_json_safe(fpath)
        if not profile:
            continue
        modified = False

        # related_entities[].org_id
        for ent in profile.get("related_entities", []):
            if ent.get("org_id"):
                continue
            name = ent.get("org_name", "").strip()
            if not name:
                continue
            found_id, _ = lookup_name(name, index)
            if found_id:
                ent["org_id"] = found_id
                filled_org += 1
                modified = True
            else:
                ok, reason = guard.can_register("org")
                if not ok:
                    continue
                org_type = ent.get("org_type") or "GOV"  # None-safe default
                ent["org_id"] = register_new_org(registry, index, iso, name, org_type)
                new_registered += 1
                modified = True
                guard.note_registered("org", ent["org_id"], f"{name} ({org_type})")

        # key_people[].person_id
        for kp in profile.get("key_people", []):
            if kp.get("person_id"):
                continue
            name = kp.get("name") or ""
            if isinstance(name, str):
                name = name.strip()
            if not name:
                continue
            found_id, _ = lookup_name(name, index)
            if found_id:
                kp["person_id"] = found_id
                filled_person += 1
                modified = True
            else:
                ok, reason = guard.can_register("person")
                if not ok:
                    continue
                kp["person_id"] = register_new_person(registry, index, iso, name)
                new_registered += 1
                modified = True
                guard.note_registered("person", kp["person_id"], name)

        if modified and not dry_run:
            save_json_atomic(fpath, profile)

    return filled_org, filled_person, new_registered


def resolve_persons(output_dir, index, registry, iso, dry_run, guard):
    """扫描 persons/*.json，解析 null org_id 和 person_id。"""
    persons_dir = os.path.join(output_dir, "persons")
    if not os.path.isdir(persons_dir):
        return 0, 0, 0

    filled_org = 0
    filled_person = 0
    new_registered = 0

    for fpath in glob.glob(os.path.join(persons_dir, "*.json")):
        if os.path.basename(fpath).startswith("_"):
            continue
        profile = load_json_safe(fpath)
        if not profile:
            continue
        modified = False

        # work_experience[].org_id
        for we in profile.get("work_experience", []):
            if we.get("org_id"):
                continue
            org_name = we.get("organization") or ""
            if isinstance(org_name, str):
                org_name = org_name.strip()
            if not org_name:
                continue
            found_id, _ = lookup_name(org_name, index)
            if found_id:
                we["org_id"] = found_id
                filled_org += 1
                modified = True
            else:
                ok, reason = guard.can_register("work-org")
                if not ok:
                    continue
                # org_type unknowable from a bare work org name; "GOV" is almost
                # always wrong, so this path requires explicit opt-in
                we["org_id"] = register_new_org(registry, index, iso, org_name, "CORP")
                new_registered += 1
                modified = True
                guard.note_registered("work-org", we["org_id"], org_name)

        # person_relationships[].person_id
        for rel in profile.get("person_relationships", []):
            if rel.get("person_id"):
                continue
            name = rel.get("person_name") or ""
            if isinstance(name, str):
                name = name.strip()
            if not name:
                continue
            found_id, _ = lookup_name(name, index)
            if found_id:
                rel["person_id"] = found_id
                filled_person += 1
                modified = True
            else:
                ok, reason = guard.can_register("person")
                if not ok:
                    continue
                rel["person_id"] = register_new_person(registry, index, iso, name)
                new_registered += 1
                modified = True
                guard.note_registered("person", rel["person_id"], name)

        if modified and not dry_run:
            save_json_atomic(fpath, profile)

    return filled_org, filled_person, new_registered


def main():
    argv = sys.argv[1:]
    if not argv:
        print("Usage: python resolve_ids.py <output_dir> [--dry-run] [--allow-register] "
              "[--max-register N] [--allow-register-work-orgs]")
        sys.exit(1)

    output_dir = argv[0].rstrip("/\\")
    dry_run = "--dry-run" in argv
    allow_register = "--allow-register" in argv
    allow_work_orgs = "--allow-register-work-orgs" in argv
    max_register = 20
    if "--max-register" in argv:
        i = argv.index("--max-register")
        if i + 1 < len(argv):
            try:
                max_register = int(argv[i + 1])
            except ValueError:
                print(f"Invalid --max-register value: {argv[i + 1]}")
                sys.exit(1)

    guard = Guardrails(allow_register, max_register, allow_work_orgs)

    # 推断 ISO
    iso = os.path.basename(os.path.dirname(output_dir)).upper()
    if len(iso) != 2:
        iso = "KR"

    print(f"=== Resolving IDs for {output_dir} (ISO: {iso}) ===")
    print(f"  Guardrails: allow-register={'ON' if allow_register else 'OFF'} | "
          f"max-register={max_register} | allow-work-orgs={'ON' if allow_work_orgs else 'OFF'}")
    if dry_run:
        print("  DRY RUN — no files will be modified")

    # 加载 index
    index_path = os.path.join(output_dir, "_name_index.json")
    if os.path.exists(index_path):
        index = load_json_safe(index_path)
        print(f"  Loaded name index: {len(index)} entries")
    else:
        index = {}
        print("  WARNING: _name_index.json not found, using empty index")

    # 加载 registry
    registry_path = os.path.join(output_dir, "id_registry.json")
    registry = load_json_safe(registry_path) or {"registry": [], "counters": {},
                                                   "person_registry": [], "person_counters": {}}

    # 计数器防回卷：从磁盘与注册表取真实最大序号
    _reconcile_counters(registry, output_dir, iso)

    # 解析 orgs
    o_filled_o, o_filled_p, o_new = resolve_orgs(output_dir, index, registry, iso, dry_run, guard)

    # 解析 persons
    p_filled_o, p_filled_p, p_new = resolve_persons(output_dir, index, registry, iso, dry_run, guard)

    total_filled = o_filled_o + o_filled_p + p_filled_o + p_filled_p
    total_new = o_new + p_new

    if not dry_run:
        # 保存 registry
        save_json_atomic(registry_path, registry)
        # 保存 name_index
        save_json_atomic(index_path, index)

    print(f"\n=== Results ===")
    print(f"  IDs filled from index: {total_filled}")
    print(f"    (exact match: {_decompose_hits['exact']}, decomposed: {_decompose_hits['decomposed']})")
    print(f"  New IDs allocated:     {total_new}")
    for kind, new_id, name in guard.registry_log:
        print(f"    + {new_id}  {name}")
    if guard.overflow:
        print(f"  Blocked by --max-register cap: {guard.overflow} (left as null)")
    if guard.blocked_no_flag:
        print(f"  Left as null (auto-register OFF): {guard.blocked_no_flag} "
              f"— run with --allow-register to register them")
    if guard.blocked_work_orgs:
        print(f"  Left as null (work-org registration OFF): {guard.blocked_work_orgs} "
              f"— run with --allow-register-work-orgs to register them")
    print(f"  Name index size:       {len(index)}")
    if dry_run:
        print("  (dry run — no changes written)")


if __name__ == "__main__":
    main()
