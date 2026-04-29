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
    """从人物画像提取所有名称变体。"""
    names = []
    basic = profile.get("basic_info", {})
    for field in ["name_en", "name_zh", "name_original"]:
        val = basic.get(field)
        if val:
            names.append(val)
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
            for name in extract_names_from_registry_entry(entry):
                if name and name not in index:
                    index[name] = org_id

        for entry in registry.get("person_registry", []):
            person_id = entry.get("person_id")
            if not person_id:
                continue
            for name in extract_names_from_registry_entry(entry):
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

    # 4. 写入
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
    print(f"  Name index generated: {len(index)} entries ({org_count} org refs, {person_count} person refs)")
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
