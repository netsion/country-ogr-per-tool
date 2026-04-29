# Malaysia Collection Error Log

Started: 2026-04-17

## Format
- `[TIMESTAMP]` `[PHASE]` `[SEVERITY]` Message

---

## Phase 1: Broad Scan

- [2026-04-17T01:15] [phase1_wikidata] [WARN] Template A (general orgs) timed out/502 multiple times. Had to split into individual type queries.
- [2026-04-17T01:20] [phase1_wikidata] [WARN] Template F (FIN) returned 502 Bad Gateway on first attempt.
- [2026-04-17T01:30] [phase1_wikidata] [WARN] MIL (Q176742) and SOE (Q3230) direct queries returned 0 results - Malaysia not well-tagged in Wikidata for these types.
- [2026-04-17T01:45] [phase1_wikidata] [WARN] Rate limited (429) on academic query - had to wait 15s between requests.

## Phase 1: QID Verification

- [2026-04-17T02:00] [phase1_qid_verify] [WARN] 123 target orgs: 41 OK, 46 auto-fixed, 36 needed manual fix
- [2026-04-17T02:10] [phase1_qid_fix] [WARN] Manual QID fix round 1: fixed 28/48 via wbsearchentities
- [2026-04-17T02:15] [phase1_qid_fix] [WARN] Manual QID fix round 2: fixed 8/20 via alternative search terms
- [2026-04-17T02:20] [phase1_qid_fix] [WARN] Manual QID fix round 3: fixed 6/12 via Malay-language searches
- [2026-04-17T02:20] [phase1_qid_fix] [INFO] Final: 2 orgs still missing QIDs (Ministry of NRES, Bank Rakyat Malaysia)
- [2026-04-17T02:20] [phase1_qid_fix] [WARN] Bank Rakyat wrongly matched to Bank Rakyat Indonesia (Q623042) - set to null
- [2026-04-17T02:20] [phase1_qid_fix] [WARN] Telekom Malaysia wrongly matched to scholarly article (Q129960587) - set to null (later fixed to Q1640639)

## Phase 2: Batch Collection

- (Running in background - results to be logged after completion)

## Phase 2.5: Org Profile Enrichment

- [2026-04-17T03:58] [phase2_5] [INFO] enrich_org_profiles.py completed. 120/120 orgs processed.
- [2026-04-17T03:58] [phase2_5] [INFO] Score distribution: 40-49: 4, 50-59: 6, 60-69: 20, 70-79: 30, 80-89: 43, 90-99: 6, 100: 11
- [2026-04-17T03:58] [phase2_5] [INFO] 94 orgs have departments, 57 have social accounts, 120 have Chinese names

## Phase 3: Person List

- [2026-04-17T04:02] [phase3] [INFO] resolve_key_people.py: resolved 22/22 QIDs to names, 0 failed
- [2026-04-17T04:02] [phase3] [INFO] update_person_list.py: 22 persons, 3 medium + 19 low importance
- [2026-04-17T04:03] [phase3] [INFO] Importance boosted: 19 low → medium (key political/business figures)

## Phase 4: Person Profiles

- [2026-04-17T04:10] [phase4] [INFO] batch_person_profiles.py: 22/22 success, 0 failed
- [2026-04-17T04:10] [phase4] [INFO] Score distribution: 100×15, 90-95×3, 70-80×4
- [2026-04-17T04:12] [phase4] [INFO] resolve_person_qids.py: 19 profiles fixed (degree/field restored), 3 QIDs unresolved

## Known Data Quality Issues

- MY-GOV-007: Wrong QID → resolved to "Template:Chamber members box listing" instead of Ministry of Defence
- MY-GOV-011: Wrong QID → resolved to "新加坡小鈴螺" (a snail species) instead of MITI
- MY-GOV-030: Wrong QID → resolved to "斯里兰卡总检察长" (Attorney General of Sri Lanka) instead of Malaysia AGC
- MY-SOE-005: Wrong QID → resolved to "Replichore" instead of KWAP
- MY-SOE-016: Wrong QID → resolved to "USS Rebel" instead of UEM Group
- MY-CORP-012: Wrong QID → resolved to "Pedro José Pinazo Arias" instead of Petronas Chemicals Group
- 3 unresolved QIDs in person profiles: Q12702063, Q7447848, Q110132312

## Script Bug Fixes (applied during this session)

- [2026-04-17T04:00] [fix] Fixed hardcoded "SG" in resolve_key_people.py (person ID prefix, counters key)
- [2026-04-17T04:00] [fix] Fixed hardcoded "SG" in update_person_list.py (nationality, metadata)
- [2026-04-17T04:00] [fix] Fixed hardcoded "SG" in batch_person_profiles.py (nationality, TODAY date)
- [2026-04-17T04:00] [fix] Fixed hardcoded "SG" in generate_profiles.py (counters save key)

