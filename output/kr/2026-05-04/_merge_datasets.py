#!/usr/bin/env python3
"""
Merge KR 2026-04-28 data into 2026-05-04 directory.

Handles:
1. Build org_id and person_id mapping tables
2. Merge org content (same-org, different-org collisions)
3. Migrate 380 person files with org_id remapping
4. Fix cross-references in org files
5. Merge registries
6. Rebuild indexes
"""

import json
import os
import sys
import re
import shutil
from pathlib import Path

# Configure encoding
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).parent
OLD_DIR = BASE_DIR.parent / '2026-04-28'
NEW_DIR = BASE_DIR  # 2026-05-04


def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def normalize_name(name):
    """Normalize org/person name for matching."""
    if not name:
        return ''
    # Remove parenthetical content
    name = re.sub(r'\([^)]*\)', '', name)
    name = re.sub(r'[（）]', '', name)
    return name.strip().lower()


def extract_english(name):
    """Extract English text from mixed name like '共同民主党 (Democratic Party of Korea)'."""
    if not name:
        return ''
    m = re.search(r'\(([^)]+)\)', name)
    if m:
        return m.group(1).strip()
    return name


# ============================================================
# Step 1: Build mapping tables
# ============================================================

def build_mappings():
    print("=" * 60)
    print("STEP 1: Building mapping tables")
    print("=" * 60)

    old_reg = load_json(OLD_DIR / 'id_registry.json')
    new_reg = load_json(NEW_DIR / 'id_registry.json')

    # Build new org name index: name variants -> org_id
    new_org_index = {}
    for r in new_reg['registry']:
        oid = r['org_id']
        name = r.get('name', '')
        name_en = ''
        name_zh = ''
        if '(' in name:
            m = re.match(r'(.+?)\s*\((.+?)\)', name)
            if m:
                name_zh = m.group(1).strip()
                name_en = m.group(2).strip()
        else:
            name_en = name

        for variant in [name, name_en, name_zh, normalize_name(name), normalize_name(name_en)]:
            if variant:
                new_org_index[variant] = oid

    # Also index from actual org files for richer name data
    for fp in (NEW_DIR / 'orgs').glob('*.json'):
        d = load_json(fp)
        oid = d['org_id']
        bi = d.get('basic_info', {})
        for key in ['name_en', 'name_zh', 'name_original']:
            val = bi.get(key, '')
            if val:
                for v in [val, normalize_name(val)]:
                    if v:
                        new_org_index[v] = oid
        for alias in bi.get('aliases', []):
            for v in [alias, normalize_name(alias)]:
                if v:
                    new_org_index[v] = oid

    # Build old registry name -> org_id map
    old_entries = {}
    for r in old_reg['registry']:
        oid = r['org_id']
        if oid not in old_entries:
            old_entries[oid] = r

    # Manual override mappings (verified from analysis)
    manual_org_map = {
        # Same ID, same org - keep as is
        'KR-PARTY-001': 'KR-PARTY-001',
        'KR-PARTY-002': 'KR-PARTY-002',
        'KR-PARTY-003': 'KR-PARTY-003',
        # Same ID, different org - map to correct 05-04 ID
        'KR-GOV-001': 'KR-GOV-001',  # State Council -> Presidential Office (merge content)
        'KR-GOV-002': 'KR-GOV-016',  # Supreme Court -> KR-GOV-016 (Supreme Court in 05-04)
        'KR-PARTY-004': 'KR-PARTY-005',  # Reform Party -> KR-PARTY-005
        'KR-PARTY-005': 'KR-PARTY-006',  # Basic Income Party -> KR-PARTY-006
        'KR-PARTY-007': 'KR-PARTY-004',  # Progressive Party -> KR-PARTY-004
        'KR-PARTY-008': 'KR-PARTY-007',  # Social Democratic Party -> KR-PARTY-007
        # Non-standard IDs -> standard
        'KR-political_party-001': None,  # 共同市民党 - no match in 05-04
        'KR-political_party-002': None,  # 共同民主联合 - no match
        'KR-political_party-003': None,  # 新未来党 - no match
        'KR-political_party-004': 'KR-PARTY-004',  # 进步党 = Progressive Party
        'KR-political_party-005': 'KR-PARTY-006',  # 基本收入党 = Basic Income Party
        'KR-political_party-006': 'KR-PARTY-007',  # 社会民主党 = Social Democratic Party
        'KR-political_party-007': 'KR-PARTY-005',  # 改革新党 = Reform Party
        'KR-political_party-008': None,  # 通合进步党 - historical, no match
        'KR-political_party-009': None,  # 美国绿党 - not Korean
        'KR-think_tank-001': None,  # 民主研究院 - no match
        'KR-ngo-001': None,  # 全国农民会总联盟 - no match
        'KR-None-001': None,  # 尹锡悦 person misclassified as org
        'KR-INTL-001': None,  # APEC - not in 05-04 as KR-INTL
        'KR-INTL-002': None,
        'KR-INTL-003': None,
    }

    # Build full org_id mapping
    org_id_map = {}  # old_id -> new_id (or None)
    unresolved = []

    for old_id, entry in old_entries.items():
        if old_id in manual_org_map:
            org_id_map[old_id] = manual_org_map[old_id]
            continue

        # Try to match by name
        name = entry.get('name', '')
        matched = False

        # Try various name forms
        name_forms = [name, normalize_name(name), extract_english(name)]
        for nf in name_forms:
            if nf and nf in new_org_index:
                org_id_map[old_id] = new_org_index[nf]
                matched = True
                break

        if not matched:
            org_id_map[old_id] = None
            if entry.get('status') != 'auto_registered' or old_id.startswith('KR-PARTY'):
                unresolved.append((old_id, name))

    # Build person_id mapping: name -> old person_id
    old_person_map = {}  # normalized_name -> person_id
    old_person_reg = old_reg.get('person_registry', [])
    for pr in old_person_reg:
        pid = pr['person_id']
        name = pr.get('name_en', '')
        # Extract Chinese and English parts
        m = re.match(r'(.+?)\s*\((.+?)\)', name)
        if m:
            name_zh = m.group(1).strip()
            name_en = m.group(2).strip()
            old_person_map[normalize_name(name_en)] = pid
            old_person_map[normalize_name(name_zh)] = pid
        else:
            old_person_map[normalize_name(name)] = pid

    # Also index from actual person files for richer matching
    person_name_to_id = {}  # name_variant -> person_id
    for fp in (OLD_DIR / 'persons').glob('*.json'):
        d = load_json(fp)
        pid = d['person_id']
        for key in ['name_en', 'name_zh']:
            val = d.get(key, '')
            if val:
                person_name_to_id[normalize_name(val)] = pid
        # Also index the Chinese part of name_en like "李在明 (Lee Jae Myung)"
        ne = d.get('name_en', '')
        m = re.match(r'(.+?)\s*\((.+?)\)', ne)
        if m:
            person_name_to_id[normalize_name(m.group(1))] = pid
            person_name_to_id[normalize_name(m.group(2))] = pid

    # Stats
    mapped_count = sum(1 for v in org_id_map.values() if v is not None)
    null_count = sum(1 for v in org_id_map.values() if v is None)
    print(f"\nOrg ID mapping: {mapped_count} mapped, {null_count} unresolved (no match in 05-04)")
    if unresolved:
        print(f"  Non-auto-registered unresolved ({len(unresolved)}):")
        for oid, name in unresolved[:20]:
            print(f"    {oid}: {name}")
        if len(unresolved) > 20:
            print(f"    ... and {len(unresolved) - 20} more")

    # Save mapping for review
    merge_map = {
        'org_id_map': {k: v for k, v in sorted(org_id_map.items())},
        'unresolved': [{'org_id': o, 'name': n} for o, n in unresolved],
        'person_count': len(old_person_reg),
        'person_file_count': len(list((OLD_DIR / 'persons').glob('*.json'))),
        'person_name_to_id_sample': dict(list(person_name_to_id.items())[:10])
    }
    save_json(NEW_DIR / '_merge_map.json', merge_map)
    print(f"\nMapping saved to _merge_map.json")
    print(f"Person files to migrate: {merge_map['person_file_count']}")

    return org_id_map, person_name_to_id, old_entries


# ============================================================
# Step 2: Merge org content
# ============================================================

def merge_orgs(org_id_map, old_entries):
    print("\n" + "=" * 60)
    print("STEP 2: Merging org content")
    print("=" * 60)

    # Case 1: Same ID, same org (PARTY-001/002/003) - use 04-28 as base, add 05-04 extras
    same_org_ids = ['KR-PARTY-001', 'KR-PARTY-002', 'KR-PARTY-003']

    for oid in same_org_ids:
        old_fp = OLD_DIR / 'orgs' / f'{oid}.json'
        new_fp = NEW_DIR / 'orgs' / f'{oid}.json'

        if not old_fp.exists() or not new_fp.exists():
            print(f"  SKIP {oid}: missing file")
            continue

        old_org = load_json(old_fp)
        new_org = load_json(new_fp)

        # Use old as base (richer content)
        merged = dict(old_org)
        merged['org_id'] = oid

        # Merge recent_events: add unique events from new
        old_titles = {e.get('title', '') for e in merged.get('recent_events', [])}
        for event in new_org.get('recent_events', []):
            if event.get('title', '') not in old_titles:
                merged.setdefault('recent_events', []).append(event)
                old_titles.add(event.get('title', ''))

        # Merge related_entities: add unique entities from new
        old_rels = {(r.get('org_id'), r.get('relationship_type')) for r in merged.get('related_entities', [])}
        for rel in new_org.get('related_entities', []):
            key = (rel.get('org_id'), rel.get('relationship_type'))
            if key not in old_rels:
                merged.setdefault('related_entities', []).append(rel)
                old_rels.add(key)

        # Update meta
        merged['collection_meta']['data_sources'] = sorted(set(
            merged['collection_meta'].get('data_sources', []) +
            new_org['collection_meta'].get('data_sources', [])
        ))
        merged['collection_meta']['notes'] = f"Merged from 2026-04-28 (score={old_org['collection_meta']['completeness_score']}) + 2026-05-04 (score={new_org['collection_meta']['completeness_score']})"
        merged['collection_meta']['completeness_score'] = max(
            old_org['collection_meta']['completeness_score'],
            new_org['collection_meta']['completeness_score']
        )

        save_json(new_fp, merged)
        print(f"  MERGED {oid} ({merged['basic_info']['name_en']}): "
              f"{len(merged['recent_events'])} events, {len(merged.get('related_entities',[]))} rels, "
              f"{len(merged.get('key_people',[]))} people")

    # Case 2: Same ID, different org - merge 04-28 content to correct 05-04 file
    collision_map = {
        'KR-GOV-001': ('KR-GOV-001', 'state_council'),  # State Council -> Presidential Office
        'KR-GOV-002': ('KR-GOV-016', 'supreme_court'),  # Supreme Court -> KR-GOV-016
        'KR-PARTY-004': ('KR-PARTY-005', 'reform_party'),  # Reform Party -> KR-PARTY-005
        'KR-PARTY-005': ('KR-PARTY-006', 'basic_income'),  # Basic Income -> KR-PARTY-006
        'KR-PARTY-007': ('KR-PARTY-004', 'progressive'),  # Progressive -> KR-PARTY-004
        'KR-PARTY-008': ('KR-PARTY-007', 'social_democratic'),  # Social Dem -> KR-PARTY-007
    }

    for old_oid, (target_oid, label) in collision_map.items():
        old_fp = OLD_DIR / 'orgs' / f'{old_oid}.json'
        target_fp = NEW_DIR / 'orgs' / f'{target_oid}.json'

        if not old_fp.exists():
            print(f"  SKIP {old_oid}->{target_oid} ({label}): no old file")
            continue

        old_org = load_json(old_fp)
        target_score = 0

        if target_fp.exists():
            target_org = load_json(target_fp)
            target_score = target_org['collection_meta']['completeness_score']

            # If target is a skeleton (score <= 30), replace entirely with old
            if target_score <= 30:
                merged = dict(old_org)
                merged['org_id'] = target_oid
                merged['collection_meta']['notes'] = f"Replaced skeleton with 2026-04-28 enriched profile (original ID: {old_oid})"
                save_json(target_fp, merged)
                print(f"  REPLACED {target_oid} with {old_oid} content ({label}): "
                      f"old_score={old_org['collection_meta']['completeness_score']}, target was skeleton")
            else:
                # Both enriched - merge: use richer as base, add unique content from other
                if old_org['collection_meta']['completeness_score'] >= target_score:
                    # Use old as base
                    merged = dict(old_org)
                    merged['org_id'] = target_oid
                    # Add unique events from target
                    merged_titles = {e.get('title', '') for e in merged.get('recent_events', [])}
                    for event in target_org.get('recent_events', []):
                        if event.get('title', '') not in merged_titles:
                            merged.setdefault('recent_events', []).append(event)
                            merged_titles.add(event.get('title', ''))
                    # Add unique related_entities from target
                    merged_rels = {(r.get('org_id'), r.get('relationship_type')) for r in merged.get('related_entities', [])}
                    for rel in target_org.get('related_entities', []):
                        key = (rel.get('org_id'), rel.get('relationship_type'))
                        if key not in merged_rels:
                            merged.setdefault('related_entities', []).append(rel)
                            merged_rels.add(key)
                    merged['collection_meta']['notes'] = f"Merged: 04-28 {old_oid} (score={old_org['collection_meta']['completeness_score']}) + 05-04 {target_oid} (score={target_score})"
                    merged['collection_meta']['completeness_score'] = max(
                        old_org['collection_meta']['completeness_score'], target_score)
                    save_json(target_fp, merged)
                    print(f"  MERGED(old>new) {old_oid}->{target_oid} ({label}): "
                          f"old={old_org['collection_meta']['completeness_score']}, new={target_score}")
                else:
                    # Use target as base, add unique content from old
                    merged = dict(target_org)
                    merged_titles = {e.get('title', '') for e in merged.get('recent_events', [])}
                    for event in old_org.get('recent_events', []):
                        if event.get('title', '') not in merged_titles:
                            merged.setdefault('recent_events', []).append(event)
                            merged_titles.add(event.get('title', ''))
                    # Add unique key_people from old
                    merged_kp_names = {kp.get('name', '') for kp in merged.get('key_people', [])}
                    for kp in old_org.get('key_people', []):
                        if kp.get('name', '') not in merged_kp_names:
                            merged.setdefault('key_people', []).append(kp)
                            merged_kp_names.add(kp.get('name', ''))
                    merged_rels = {(r.get('org_id'), r.get('relationship_type')) for r in merged.get('related_entities', [])}
                    for rel in old_org.get('related_entities', []):
                        key = (rel.get('org_id'), rel.get('relationship_type'))
                        if key not in merged_rels:
                            merged.setdefault('related_entities', []).append(rel)
                            merged_rels.add(key)
                    merged['collection_meta']['notes'] = f"Merged: 05-04 {target_oid} (score={target_score}) + 04-28 {old_oid} (score={old_org['collection_meta']['completeness_score']})"
                    merged['collection_meta']['completeness_score'] = max(
                        old_org['collection_meta']['completeness_score'], target_score)
                    save_json(target_fp, merged)
                    print(f"  MERGED(new>old) {old_oid}->{target_oid} ({label}): "
                          f"old={old_org['collection_meta']['completeness_score']}, new={target_score}")
        else:
            # Target doesn't exist - write old org with new ID
            merged = dict(old_org)
            merged['org_id'] = target_oid
            merged['collection_meta']['notes'] = f"Migrated from 2026-04-28 (original ID: {old_oid})"
            save_json(target_fp, merged)
            print(f"  CREATED {target_oid} from {old_oid} ({label})")

    # Special handling: State Council content merge into Presidential Office
    # The 04-28 KR-GOV-001 has 21 cabinet members as key_people
    # Merge them into 05-04 KR-GOV-001 as additional key_people
    old_gov001 = load_json(OLD_DIR / 'orgs' / 'KR-GOV-001.json')
    new_gov001 = load_json(NEW_DIR / 'orgs' / 'KR-GOV-001.json')

    # Add cabinet members from old as key_people (they're under Presidential Office hierarchy)
    existing_names = {kp.get('name', '') for kp in new_gov001.get('key_people', [])}
    added = 0
    for kp in old_gov001.get('key_people', []):
        if kp.get('name', '') not in existing_names:
            new_gov001.setdefault('key_people', []).append(kp)
            existing_names.add(kp.get('name', ''))
            added += 1

    # Add unique events
    existing_titles = {e.get('title', '') for e in new_gov001.get('recent_events', [])}
    for event in old_gov001.get('recent_events', []):
        if event.get('title', '') not in existing_titles:
            new_gov001.setdefault('recent_events', []).append(event)
            existing_titles.add(event.get('title', ''))

    # Add unique related entities
    existing_rels = {(r.get('org_id'), r.get('relationship_type')) for r in new_gov001.get('related_entities', [])}
    for rel in old_gov001.get('related_entities', []):
        key = (rel.get('org_id'), rel.get('relationship_type'))
        if key not in existing_rels:
            new_gov001.setdefault('related_entities', []).append(rel)
            existing_rels.add(key)

    new_gov001['collection_meta']['notes'] = (
        f"Merged: 05-04 Presidential Office + 04-28 State Council/Cabinet "
        f"({added} cabinet members added)"
    )
    save_json(NEW_DIR / 'orgs' / 'KR-GOV-001.json', new_gov001)
    print(f"  ENHANCED KR-GOV-001: added {added} cabinet members from State Council")

    print("\nStep 2 complete.")


# ============================================================
# Step 3: Migrate person files with org_id remapping
# ============================================================

def migrate_persons(org_id_map):
    print("\n" + "=" * 60)
    print("STEP 3: Migrating person files")
    print("=" * 60)

    dest_dir = NEW_DIR / 'persons'
    dest_dir.mkdir(exist_ok=True)

    src_dir = OLD_DIR / 'persons'
    files = list(src_dir.glob('*.json'))
    print(f"Migrating {len(files)} person files...")

    remapped = 0
    kept = 0
    errors = 0

    for fp in files:
        try:
            person = load_json(fp)

            # Remap work_experience org_ids
            for we in person.get('work_experience', []):
                old_oid = we.get('org_id')
                if old_oid and old_oid in org_id_map:
                    new_oid = org_id_map[old_oid]
                    if new_oid != old_oid:
                        we['org_id'] = new_oid
                        remapped += 1
                    else:
                        kept += 1

            # Remap top-level org_ids
            if 'org_ids' in person and person['org_ids']:
                person['org_ids'] = [
                    org_id_map.get(oid, oid) if oid in org_id_map else oid
                    for oid in person['org_ids']
                ]

            save_json(dest_dir / fp.name, person)

        except Exception as e:
            errors += 1
            print(f"  ERROR {fp.name}: {e}")

    print(f"Done: {len(files)} files, {remapped} org_ids remapped, {kept} unchanged, {errors} errors")


# ============================================================
# Step 4: Fix org file person_id references
# ============================================================

def fix_org_person_ids(person_name_to_id):
    print("\n" + "=" * 60)
    print("STEP 4: Fixing org file person_id references")
    print("=" * 60)

    # Build person file index: person_id -> person data
    person_files = {}
    for fp in (NEW_DIR / 'persons').glob('*.json'):
        d = load_json(fp)
        person_files[d['person_id']] = d

    # For each org file, update key_people person_id
    fixed = 0
    not_found = 0

    for fp in (NEW_DIR / 'orgs').glob('*.json'):
        org = load_json(fp)
        changed = False

        for kp in org.get('key_people', []):
            pid = kp.get('person_id')
            name = kp.get('name', '')

            # If person_id exists and matches a person file, keep it
            if pid and pid in person_files:
                continue

            # Try to match by name
            if name:
                # Extract Chinese and English parts
                m = re.match(r'(.+?)\s*\((.+?)\)', name)
                candidates = [normalize_name(name)]
                if m:
                    candidates.extend([normalize_name(m.group(1)), normalize_name(m.group(2))])

                for c in candidates:
                    if c in person_name_to_id:
                        new_pid = person_name_to_id[c]
                        kp['person_id'] = new_pid
                        fixed += 1
                        changed = True
                        break
                else:
                    not_found += 1

        # Also fix related_entities with non-standard org_ids
        for rel in org.get('related_entities', []):
            oid = rel.get('org_id', '')
            # Fix non-standard IDs
            non_std_map = {
                'KR-political_party-001': None,
                'KR-political_party-002': None,
                'KR-political_party-003': None,
                'KR-political_party-004': 'KR-PARTY-004',
                'KR-political_party-005': 'KR-PARTY-006',
                'KR-political_party-006': 'KR-PARTY-007',
                'KR-political_party-007': 'KR-PARTY-005',
                'KR-political_party-008': None,
                'KR-political_party-009': None,
                'KR-think_tank-001': None,
                'KR-ngo-001': None,
            }
            if oid in non_std_map:
                new_oid = non_std_map[oid]
                if new_oid:
                    rel['org_id'] = new_oid
                    changed = True
                else:
                    # Remove this related_entity as it has no equivalent
                    pass

        if changed:
            save_json(fp, org)

    print(f"Fixed {fixed} person_id references, {not_found} names not matched")


# ============================================================
# Step 5: Merge registries
# ============================================================

def merge_registries(org_id_map, old_entries):
    print("\n" + "=" * 60)
    print("STEP 5: Merging registries")
    print("=" * 60)

    old_reg = load_json(OLD_DIR / 'id_registry.json')
    new_reg = load_json(NEW_DIR / 'id_registry.json')

    # Add old auto-registered org entries (those with no match in new registry)
    existing_new_ids = {r['org_id'] for r in new_reg['registry']}
    added = 0

    for old_entry in old_reg['registry']:
        old_oid = old_entry['org_id']
        new_oid = org_id_map.get(old_oid)

        # Skip if already exists in new registry (or maps to existing ID)
        if new_oid and new_oid in existing_new_ids:
            continue
        if old_oid in existing_new_ids:
            continue

        # Add as unresolved reference
        entry = {
            'org_id': old_oid,
            'name': old_entry.get('name', ''),
            'org_type': old_entry.get('org_type', ''),
            'status': 'auto_registered_legacy',
            'notes': f'Migrated from 2026-04-28, no profile file'
        }
        if new_oid:
            entry['mapped_to'] = new_oid
        new_reg['registry'].append(entry)
        existing_new_ids.add(old_oid)
        added += 1

    # Add person registry
    old_person_reg = old_reg.get('person_registry', [])
    new_reg['person_registry'] = old_person_reg
    new_reg['person_counters'] = old_reg.get('person_counters', {})

    # Update org counters to account for legacy entries
    # Count max legacy GOV seq
    max_gov = 0
    for r in new_reg['registry']:
        if r['org_id'].startswith('KR-GOV-'):
            try:
                seq = int(r['org_id'].split('-')[-1])
                max_gov = max(max_gov, seq)
            except ValueError:
                pass

    if 'counters' not in new_reg:
        new_reg['counters'] = {}
    new_reg['counters']['KR-GOV-legacy'] = max_gov

    save_json(NEW_DIR / 'id_registry.json', new_reg)
    print(f"Added {added} legacy org entries from 04-28")
    print(f"Added {len(old_person_reg)} person registry entries")


# ============================================================
# Step 6: Final validation
# ============================================================

def validate():
    print("\n" + "=" * 60)
    print("STEP 6: Validation")
    print("=" * 60)

    # Check person file count
    person_files = list((NEW_DIR / 'persons').glob('*.json'))
    print(f"Person files: {len(person_files)}")

    # Check org file count
    org_files = list((NEW_DIR / 'orgs').glob('*.json'))
    print(f"Org files: {len(org_files)}")

    # Check person_id references in org files
    person_ids = {fp.stem for fp in person_files}
    org_ids = {fp.stem for fp in org_files}

    broken_person_refs = 0
    total_person_refs = 0
    for fp in org_files:
        org = load_json(fp)
        for kp in org.get('key_people', []):
            pid = kp.get('person_id')
            if pid:
                total_person_refs += 1
                if pid not in person_ids:
                    broken_person_refs += 1

    print(f"Person refs in orgs: {total_person_refs} total, {broken_person_refs} broken")

    # Check org_id references in person files
    broken_org_refs = 0
    total_org_refs = 0
    registry_ids = set()
    reg = load_json(NEW_DIR / 'id_registry.json')
    for r in reg['registry']:
        registry_ids.add(r['org_id'])

    for fp in person_files:
        person = load_json(fp)
        for we in person.get('work_experience', []):
            oid = we.get('org_id')
            if oid:
                total_org_refs += 1
                if oid not in org_ids and oid not in registry_ids:
                    broken_org_refs += 1

    print(f"Org refs in persons: {total_org_refs} total, {broken_org_refs} broken (not in org files or registry)")

    # Check for person_relationships references
    broken_rel_refs = 0
    total_rel_refs = 0
    for fp in person_files:
        person = load_json(fp)
        for rel in person.get('person_relationships', []):
            pid = rel.get('person_id')
            if pid:
                total_rel_refs += 1
                if pid not in person_ids:
                    broken_rel_refs += 1

    print(f"Person-to-person refs: {total_rel_refs} total, {broken_rel_refs} broken")

    print(f"\nRegistry total entries: {len(reg['registry'])}")


# ============================================================
# Main
# ============================================================

def main():
    print("KR Dataset Merge: 2026-04-28 → 2026-05-04")
    print(f"Source: {OLD_DIR}")
    print(f"Target: {NEW_DIR}")

    if not OLD_DIR.exists():
        print(f"ERROR: Source directory {OLD_DIR} not found")
        sys.exit(1)

    # Step 1
    org_id_map, person_name_to_id, old_entries = build_mappings()

    # Step 2
    merge_orgs(org_id_map, old_entries)

    # Step 3
    migrate_persons(org_id_map)

    # Step 4
    fix_org_person_ids(person_name_to_id)

    # Step 5
    merge_registries(org_id_map, old_entries)

    # Step 6
    validate()

    print("\n" + "=" * 60)
    print("MERGE COMPLETE")
    print("=" * 60)


if __name__ == '__main__':
    main()
