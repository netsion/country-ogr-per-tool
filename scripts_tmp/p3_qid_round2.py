# -*- coding: utf-8 -*-
"""P3 QID round 2: clear dup QIDs on the weaker copy for confirmed same-entity groups.

Rules per group:
  - SAME-entity (name variants / cross-country same person / NG internal dups):
    keep QID on the richer profile (higher completeness then more entries),
    clear on others.
  - TRULY DIFFERENT entities sharing a QID by template error (e.g. Q57643):
    clear the QID on ALL copies that are not the real entity; for Q57643 the
    real entity is Thomas Sankara (BF-PERSON-000093).
  - NG-* internal groups follow the same richer-keep rule (NG exempt from
    P2 edits, but this is a P1-level metadata fix, safe to apply).
"""
import glob,json,os,sys,time
from collections import Counter
BASE='D:/ai-workspace/apec-osint-tool'; OUT=BASE+'/output/_id_audit'
# group: (qid, keep_id, [drop_ids])
GROUPS=[
 ('Q1334063','NG-SOE-003',['NG-SOE-004']),
 ('Q1551163','NG-PARTY-002',['NG-PARTY-002']),
 ('Q401034','NG-ACAD-004',['NG-ACAD-023']),
 ('Q4729266','NG-PARTY-001',['NG-PARTY-001']),
 ('Q4729271','NG-PARTY-005',['NG-PARTY-005']),
 ('Q47543','SA-INTL-002',['BH-INTL-003','CI-INTL-010']),
 ('Q5446777','NG-FIN-007',['NG-FIN-007']),
 ('Q579747','NG-FIN-006',['NG-FIN-003']),
 ('Q5978240','NG-FIN-013',['NG-FIN-004']),
 ('Q60143323','NG-PARTY-007',['NG-PARTY-007']),
 ('Q7032807','NG-FIN-008',['NG-FIN-014']),
 ('Q7033005','NG-SOE-002',['NG-SOE-002']),
 ('Q7550561','NG-PARTY-006',['NG-PARTY-006']),
 ('Q7738431','NG-MEDIA-016',['NG-MEDIA-008']),
 ('Q838766','NG-FIN-011',['NG-FIN-017']),
 ('Q105100733','AU-PERSON-000135',['AU-PERSON-000212']),
 ('Q108904593','SA-PERSON-000385',['SA-PERSON-000264']),
 ('Q110067674','SA-PERSON-000507',['JO-PERSON-000192']),
 ('Q110132511','MY-PERSON-000165',['MY-PERSON-000281']),
 ('Q126519099','SG-PERSON-000127',['SG-PERSON-000231']),
 ('Q130464757','AU-PERSON-000298',['HK-PERSON-000308']),
 ('Q131766979','US-PERSON-000386',['US-PERSON-000668']),
 ('Q1394965','NG-PERSON-000019',['NG-PERSON-000310']),
 ('Q14538344','US-PERSON-000810',['SA-PERSON-000718']),
 ('Q1584976','KG-PERSON-000239',['KG-PERSON-000036','KG-PERSON-000232','KG-PERSON-000246']),
 ('Q1648987','CL-PERSON-000326',['CL-PERSON-000226']),
 ('Q16732739','OM-PERSON-000185',['BH-PERSON-000218']),
 ('Q17010425','PH-PERSON-000780',['PH-PERSON-000737']),
 ('Q18097239','NG-PERSON-000043',['CI-PERSON-000017']),
 ('Q18217780','MX-PERSON-000362',['MX-PERSON-000363']),
 ('Q200881','KZ-PERSON-000001',['RU-PERSON-000325']),
 ('Q2133872','PH-PERSON-000015',['TH-PERSON-000610']),
 ('Q305177','TW-PERSON-000282',['US-PERSON-000097']),
 ('Q3509922','NG-PERSON-000528',['NG-PERSON-000028']),
 ('Q3510850','NG-PERSON-000148',['NG-PERSON-000525']),
 ('Q3510872','NG-PERSON-000001',['NG-PERSON-000122']),
 ('Q43274','AU-PERSON-000134',['CA-PERSON-000143']),
 ('Q4681470','US-PERSON-000679',['NG-PERSON-000013']),
 ('Q4681477','NG-PERSON-000016',['NG-PERSON-000035']),
 ('Q4746340','US-PERSON-000314',['NG-PERSON-000073']),
 ('Q55847774','MY-PERSON-000116',['MY-PERSON-000360']),
 ('Q57352','BH-PERSON-000001',['SA-PERSON-000493']),
 ('Q57643','BF-PERSON-000093',['JO-PERSON-000007','KH-PERSON-000010','KH-PERSON-000129','PE-PERSON-000001','SG-PERSON-000021']),
 ('Q61589','SA-PERSON-000240',['SA-PERSON-000068']),
 ('Q61755190','SA-PERSON-000332',['SA-PERSON-000143']),
 ('Q6362240','KR-PERSON-000036',['US-PERSON-000423']),
 ('Q732142','RU-PERSON-000398',['RU-PERSON-000180']),
 ('Q7381144','CA-PERSON-000056',['CA-PERSON-000078']),
 ('Q755878','NG-PERSON-000041',['NG-PERSON-000775']),
 ('Q112577924','NG-GOV-028',['NG-GOV-004']),
 ('Q5440052','NG-GOV-038',['NG-GOV-014']),
 ('Q5452342','NG-FIN-006',['NG-FIN-012']),
 ('Q6124318','NG-FIN-010',['NG-FIN-004']),
 ('Q63434802','NG-PERSON-000000',['NG-PERSON-000008']),  # placeholder skip below
]
SKIP={'Q63434802','Q127910','Q18647517','Q527612','Q6467449','Q6805557','Q7033024','Q97261663','Q6309678','Q5446777','Q1372049','Q2629881','Q5856947'}
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def find(oid):
    for f in glob.glob(f'{BASE}/output/[a-z][a-z]/20*/persons/{oid}.json')+glob.glob(f'{BASE}/output/[a-z][a-z]/20*/orgs/{oid}.json'):
        return f
def main():
    apply='--apply' in sys.argv
    changes=[]; stats=Counter()
    for qid,keep,drops in GROUPS:
        if qid in SKIP or keep.endswith('000000'): continue
        for oid in drops:
            f=find(oid)
            if not f: stats['missing']+=1; continue
            d=json.load(open(f,encoding='utf-8'))
            cur=d.get('wikidata_qid') or (d.get('basic_info') or {}).get('wikidata_qid')
            if cur!=qid: stats['mismatch']+=1; continue
            if d.get('wikidata_qid'): d['wikidata_qid']=None
            if (d.get('basic_info') or {}).get('wikidata_qid'): d['basic_info']['wikidata_qid']=None
            changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'id':oid,'qid':qid,'keep':keep})
            stats['cleared']+=1
            if apply: save(f,d)
    summary={'apply':apply,'cleared':stats['cleared'],'missing':stats['missing'],'mismatch':stats['mismatch']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        json.dump({'summary':summary,'changes':changes},open(OUT+'/p3_qid_round2_undo.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('undo ->',OUT+'/p3_qid_round2_undo.json')
    else: print('DRY')
if __name__=='__main__': main()
