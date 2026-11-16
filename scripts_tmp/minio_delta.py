# -*- coding: utf-8 -*-
"""Compute MinIO upload delta: profile-referenced local_paths vs disk; new files since last upload."""
import glob, json, os, datetime
from collections import Counter
BASE = 'D:/ai-workspace/apec-osint-tool'
BS = chr(92)
refs = set()
for f in glob.glob(BASE + '/output/[a-z][a-z]/20*/persons/*.json') + glob.glob(BASE + '/output/[a-z][a-z]/20*/orgs/*.json'):
    if os.path.basename(f).startswith('_'):
        continue
    d = json.load(open(f, encoding='utf-8'))
    lp = (d.get('profile') or {}).get('local_path')
    if lp:
        refs.add(lp.replace(BS, '/'))
disk = set()
for root, dirs, files in os.walk(BASE + '/minio-store'):
    for fn in files:
        disk.add(os.path.relpath(os.path.join(root, fn), BASE).replace(BS, '/'))
missing = sorted(refs - disk)
print('referenced local_paths:', len(refs))
print('files on disk:', len(disk))
print('referenced but missing on disk:', len(missing))
for m in missing[:10]:
    print(' MISSING', m)
cutoff = datetime.datetime(2026, 11, 12, 14, 40).timestamp()
newer = []
for p in disk:
    if os.path.getmtime(BASE + '/' + p) > cutoff:
        newer.append(p)
print('files newer than 2026-11-12 14:40 (post-upload):', len(newer))
print(Counter(p.split('/')[2] for p in newer).most_common(12))
json.dump({'referenced': sorted(refs), 'missing_on_disk': missing,
           'newer_than_upload': sorted(newer)},
          open(BASE + '/output/_id_audit/minio_upload_delta.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=1)
print('-> output/_id_audit/minio_upload_delta.json')
