#!/usr/bin/env python3
"""
generate_name_index.py — 从已有数据生成名称→ID 精确查找表

用法: python scripts/generate_name_index.py output/kr/2026-04-28

功能:
  1. 读取 id_registry.json 获取已注册的 org/person ID 和名称
  2. 扫描 orgs/*.json 和 persons/*.json 提取所有名称变体
  3. 输出 _name_index.json（扁平 key→value 映射）

输出格式:
  {
    "State Council of South Korea": "KR-GOV-001",
    "国务会议": "KR-GOV-001",
    "국무회의": "KR-GOV-001",
    "Lee Jae-myung": "KR-PERSON-000001",
    ...
  }
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import json
import os
import glob

# Add scripts dir to path for shared imports
sys.path.insert(0, os.path.dirname(__file__))
from atomic_write import decompose_name

DEAD_STATUS = {"trimmed", "merged", "removed", "duplicate", "excluded",
               "deprecated_broken_id", "archived", "pruned"}


def _is_dead(entry):
    """Merged/tombstoned entries must never enter the index (incl. merged_into_<ID>)."""
    status = str(entry.get("status") or "")
    return status in DEAD_STATUS or status.startswith("merged_into_")


def _safe_component(component, target_id):
    """Reject single letters / tiny fragments that poison the index."""
    c = (component or "").strip()
    if not c:
        return False
    has_cjk = any("一" <= ch <= "鿿" for ch in c)
    has_hangul = any("가" <= ch <= "힯" for ch in c)
    if has_cjk or has_hangul:
        return len(c) >= 3
    # Latin / other: require at least 4 characters and a letter
    return len(c) >= 4 and any(ch.isalpha() for ch in c)


def extract_names_from_org(profile):
    """从组织画像提取所有名称变体。"""
    names = []
    basic = profile.get("basic_info", {})
    for field in ["name_en", "name_zh", "name_original"]:
        val = basic.get(field)
        if val:
            names.append(val)
    for alias in basic.get("aliases", []):
        if alias:
            names.append(alias)
    return names


def extract_names_from_person(profile):
    """从人物画像提取所有名称变体（含 top-level 字段 + basic_info）。"""
    names = []
    # Top-level fields (person profiles store names here)
    for field in ["name", "name_en", "name_zh", "name_original"]:
        val = profile.get(field)
        if val:
            names.append(val)
    # basic_info fields (fallback for org-style profiles)
    basic = profile.get("basic_info", {})
    for field in ["name_en", "name_zh", "name_original"]:
        val = basic.get(field)
        if val:
            names.append(val)
    # aliases
    for alias in profile.get("aliases", []):
        if alias:
            names.append(alias)
    return names


def extract_names_from_registry_entry(entry):
    """从 registry 条目提取名称。"""
    names = []
    for field in ["name", "name_en", "name_zh", "name_local"]:
        val = entry.get(field)
        if val:
            names.append(val)
    return names


def build_index(output_dir):
    """构建名称索引并写入文件。"""
    registry_path = os.path.join(output_dir, "id_registry.json")
    index = {}

    # 1. 从 registry 读取（即使没有画像文件，registry 里也有基本名称）
    if os.path.exists(registry_path):
        registry = json.load(open(registry_path, encoding='utf-8'))

        for entry in registry.get("registry", []):
            org_id = entry.get("org_id")
            if not org_id:
                continue
            # 人物行误混入组织 registry 时不得进入索引（防止人物名→org_id 污染）
            if entry.get("person_id"):
                continue
            # 已裁剪/合并/移除的组织不进入索引，防止子代理误引用废弃 ID
            if _is_dead(entry):
                continue
            for name in extract_names_from_registry_entry(entry):
                name = (name or "").strip()
                if name and name not in index:
                    index[name] = org_id

        for entry in registry.get("person_registry", []):
            person_id = entry.get("person_id")
            if not person_id:
                continue
            # 已合并/裁剪/移除的人物不进入索引，防止子代理引用已废弃的 ID
            if _is_dead(entry):
                continue
            for name in extract_names_from_registry_entry(entry):
                name = (name or "").strip()
                if name and name not in index:
                    index[name] = person_id

    # 2. 扫描 orgs/*.json 补充名称变体
    orgs_dir = os.path.join(output_dir, "orgs")
    if os.path.isdir(orgs_dir):
        for fpath in glob.glob(os.path.join(orgs_dir, "*.json")):
            if os.path.basename(fpath).startswith("_"):
                continue
            try:
                profile = json.load(open(fpath, encoding='utf-8'))
            except (json.JSONDecodeError, Exception):
                continue
            org_id = profile.get("org_id")
            if not org_id:
                continue
            for name in extract_names_from_org(profile):
                if name and name not in index:
                    index[name] = org_id

    # 3. 扫描 persons/*.json 补充名称变体
    persons_dir = os.path.join(output_dir, "persons")
    if os.path.isdir(persons_dir):
        for fpath in glob.glob(os.path.join(persons_dir, "*.json")):
            if os.path.basename(fpath).startswith("_"):
                continue
            try:
                profile = json.load(open(fpath, encoding='utf-8'))
            except (json.JSONDecodeError, Exception):
                continue
            person_id = profile.get("person_id")
            if not person_id:
                continue
            for name in extract_names_from_person(profile):
                if name and name not in index:
                    index[name] = person_id

    # 4. Decomposition pass: break composite names into components
    decomposed_added = 0
    ambiguous = set()
    keys_snapshot = list(index.keys())
    for key_name in keys_snapshot:
        target_id = index[key_name]
        for component in decompose_name(key_name):
            component = (component or "").strip()
            # 人物目标的单键分解（仅名或仅姓）歧义过大，曾致同名不同人误并，不入索引
            if "-PERSON-" in target_id and " " not in component:
                continue
            if not _safe_component(component, target_id):
                continue
            if component in index:
                if index[component] != target_id:
                    # same fragment maps to multiple identities → ambiguity
                    ambiguous.add(component)
                continue
            index[component] = target_id
            decomposed_added += 1
    for key in ambiguous:
        index.pop(key, None)
    # single-character keys are never safe (aliases/fragments like "T", "Ъ", "汗")
    for key in list(index.keys()):
        if len(str(key).strip()) <= 1:
            index.pop(key, None)

    # 5. 写入
    out_path = os.path.join(output_dir, "_name_index.json")

    # 原子写入
    dir_path = os.path.dirname(out_path)
    import tempfile
    fd, tmp_path = tempfile.mkstemp(dir=dir_path, prefix=".tmp_", suffix="_name_index.json", text=True)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, out_path)
    except Exception:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise

    org_count = sum(1 for v in index.values() if "-GOV-" in v or "-SOE-" in v or "-CORP-" in v
                    or "-NGO-" in v or "-ACAD-" in v or "-MEDIA-" in v or "-FIN-" in v
                    or "-INTL-" in v or "-PARTY-" in v or "-MIL-" in v)
    person_count = sum(1 for v in index.values() if "-PERSON-" in v)
    print(f"  Name index generated: {len(index)} entries ({org_count} org refs, {person_count} person refs, +{decomposed_added} decomposed)")
    print(f"  Output: {out_path}")
    return index


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_name_index.py <output_dir>")
        sys.exit(1)

    output_dir = sys.argv[1].rstrip("/\\")
    print(f"=== Generating Name Index for {output_dir} ===")
    build_index(output_dir)
    print("Done.")
