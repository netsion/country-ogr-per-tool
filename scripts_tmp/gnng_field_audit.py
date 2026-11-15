# -*- coding: utf-8 -*-
"""GN/NG field-norm audit: social v2, profile paths, empty IDs."""
import glob, json, os, sys
BASE = 'D:/ai-workspace/apec-osint-tool'
PLAT = {'twitter','facebook','instagram','youtube','linkedin','telegram','tiktok','threads','wechat','weibo','github','gitlab','medium','substack','mastodon','whatsapp','line','snapchat','tumblr','odnoklassniki','vkontakte','reddit','other'}
issues = {}
def add(cc, dirn, k, n=1):
    issues.setdefault((cc, dirn), {}).setdefault(k, 0)
    issues[(cc, dirn)][k] += n
for cc, dirn in [('gn','2026-11-10'), ('ng','2026-11-10'), ('ng','2026-07-29')]:
    for sub in ('persons','orgs'):
        for f in glob.glob(f'{BASE}/output/{cc}/{dirn}/{sub}/*.json'):
            if os.path.basename(f).startswith('_'):
                continue
            d = json.load(open(f, encoding='utf-8'))
            for s in d.get('social_accounts') or []:
                if not isinstance(s, dict):
                    add(cc, dirn, 'social_non_dict'); continue
                p = (s.get('platform') or '').lower()
                if p not in PLAT: add(cc, dirn, 'social_bad_platform')
                if p == 'twitter_x': add(cc, dirn, 'social_twitter_x')
                if s.get('source') is not None and not isinstance(s.get('source'), int):
                    add(cc, dirn, 'social_source_nonint')
                if s.get('source_note') is not None and not isinstance(s.get('source_note'), str):
                    add(cc, dirn, 'social_source_note_nonstr')
            pr = d.get('profile')
            if isinstance(pr, dict):
                for k in ('source_url','local_path','minio_path'):
                    if pr.get(k) is not None and not isinstance(pr.get(k), str):
                        add(cc, dirn, 'profile_bad_type')
                lp = pr.get('local_path') or ''
                if lp and (chr(92) in lp or lp.startswith(chr(47))):
                    add(cc, dirn, 'profile_path_backslash_or_abs')
                if lp and not lp.startswith('minio-store/'):
                    add(cc, dirn, 'profile_path_non_std')
            for arr, field in (('work_experience','org_id'),('person_relationships','person_id'),('family_members','person_id'),('key_people','person_id'),('related_entities','org_id')):
                for x in d.get(arr) or []:
                    if isinstance(x, dict) and x.get(field) == '':
                        add(cc, dirn, 'empty_str_id')
for k, v in sorted(issues.items()):
    print(k, v)
