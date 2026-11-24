# -*- coding: utf-8 -*-
"""Plan A: downgrade skeleton profiles back to key_people entries.

Steps:
1. Find all skeleton person profiles (flagged in collection_meta.notes).
2. For each org whose key_people references a skeleton ID:
   - restore person_id=null, keep name/title/description (already there)
3. Delete skeleton person files (move to _pruned for backup).
4. Remove skeleton entries from person_registry (move to deprecated).
5. Also remove skeleton avatar files from minio-store if any.
6. Null all person_relationships/family_members refs pointing to skeleton IDs.
"""
import glob, json, os, sys, time, shutil
from collections import Counter

BASE = 'D:/ai-workspace/apec-osint-tool'
DIRS = [('bd','2026-11-23'),('eg','2026-11-16'),('gh','2026-11-17'),('ma','2026-10-05'),('ml','2026-11-18'),('ng','2026-11-10'),('sd','2026-11-16')]
BACKUP = BASE + '/output/_id_audit/skeleton_downgrade_backup'

def save(p, obj):
    payload = json.dumps(obj, ensure_ascii=False, indent=2) + '\n'
    tmp = p + '.tmp'
    for _ in range(6):
        try:
            with open(tmp, 'w', encoding='utf-8', newline='\n') as fh:
                fh.write(payload)
            os.replace(tmp, p)
            return
        except PermissionError:
            time.sleep(0.5)
    with open(p, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(payload)

def main():
    apply = '--apply' in sys.argv
    # 1. find all skeleton profiles
    skeletons = {}  # pid -> filepath
    for cc, date in DIRS:
        for f in glob.glob(BASE + f'/output/{cc}/{date}/persons/*.json'):
            if os.path.basename(f).startswith('_'): continue
            d = json.load(open(f, encoding='utf-8'))
            cm = d.get('collection_meta') or {}
            notes = cm.get('notes') or ''
            src = cm.get('source') or ''
            if '骨架画像' in notes or 'org key_people skeleton' in src:
                skeletons[d.get('person_id')] = f
    print('skeleton profiles found:', len(skeletons))

    # 2. null all refs pointing to skeleton IDs (person_relationships/family_members/key_people/work_experience.org_id)
    stats = Counter()
    changed_files = set()
    for cc, date in DIRS:
        for sub in ('persons', 'orgs'):
            for f in glob.glob(BASE + f'/output/{cc}/{date}/{sub}/*.json'):
                if os.path.basename(f).startswith('_'): continue
                d = json.load(open(f, encoding='utf-8'))
                dirty = False
                for arr, field in (('work_experience','org_id'),('person_relationships','person_id'),('family_members','person_id'),('key_people','person_id'),('related_entities','org_id')):
                    for x in d.get(arr) or []:
                        if not isinstance(x, dict): continue
                        if x.get(field) in skeletons:
                            x[field] = None; dirty = True; stats['refs_nulled'] += 1
                if dirty:
                    changed_files.add(f)
                    if apply: save(f, d)

    # 3. delete skeleton profile files (backup first)
    os.makedirs(BACKUP, exist_ok=True)
    deleted = 0
    for pid, f in skeletons.items():
        cc_dir = os.path.basename(os.path.dirname(os.path.dirname(f)))
        bdir = os.path.join(BACKUP, cc_dir)
        os.makedirs(bdir, exist_ok=True)
        shutil.copy2(f, os.path.join(bdir, os.path.basename(f)))
        if apply:
            os.remove(f)
        deleted += 1

    # 4. clean registry: remove skeleton entries (move to deprecated)
    for cc, date in DIRS:
        rp = BASE + f'/output/{cc}/{date}/id_registry.json'
        if not os.path.exists(rp): continue
        reg = json.load(open(rp, encoding='utf-8'))
        pre = reg.get('person_registry') or []
        dep = reg.setdefault('deprecated_person_registry', [])
        cc_pids = {pid for pid in skeletons if pid.startswith(cc.upper() + '-')}
        keep = []; removed = 0
        for e in pre:
            pid = e.get('person_id')
            if pid in cc_pids:
                e2 = dict(e)
                e2['status'] = 'skeleton_downgraded'
                e2['deprecated_reason'] = 'Plan A: skeleton profile removed, info kept in org key_people'
                dep.append(e2)
                removed += 1
                continue
            keep.append(e)
        if removed:
            reg['person_registry'] = keep
            if apply: save(rp, reg)
            stats['registry_removed'] += removed

        # 5. clean person _index.json
        ip = BASE + f'/output/{cc}/{date}/persons/_index.json'
        if not os.path.exists(ip): continue
        idx = json.load(open(ip, encoding='utf-8'))
        before = len(idx.get('profiles') or [])
        idx['profiles'] = [p for p in (idx.get('profiles') or []) if p.get('person_id') not in cc_pids]
        idx['total_profiles'] = len(idx['profiles'])
        if apply and before != len(idx['profiles']):
            save(ip, idx)
            stats['index_removed'] += before - len(idx['profiles'])

        # 6. remove skeleton avatars from minio-store
        for pid in cc_pids:
            for av in glob.glob(BASE + f'/minio-store/default/*-profile/{cc}/{pid}.*'):
                if apply: os.remove(av)
                stats['avatar_removed'] += 1

    summary = {'apply': apply, 'skeletons': len(skeletons), 'deleted_files': deleted, **dict(stats)}
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    if apply:
        json.dump(summary, open(BASE + '/output/_id_audit/skeleton_downgrade_summary.json', 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=1)
        print('summary ->', BASE + '/output/_id_audit/skeleton_downgrade_summary.json')
    else:
        print('DRY')

if __name__ == '__main__':
    main()
