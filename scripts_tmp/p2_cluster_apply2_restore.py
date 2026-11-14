# -*- coding: utf-8 -*-
"""Restore cluster-2 nulls that were actually correct aliases."""
import json,os,sys,time
BASE='D:/ai-workspace/apec-osint-tool'; OUT=os.path.join(BASE,'output/_id_audit')
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def main():
    apply='--apply' in sys.argv
    u=json.load(open(os.path.join(OUT,'p2_cluster_apply2_undo.json'),encoding='utf-8'))
    restore=[]
    for c in u['changes']:
        old=c['old']; ref=c['ref_name']
        keep=False
        if old=='SA-ACAD-009' and '健康科学大学' in ref: keep=True
        elif old=='TM-SOE-001' and ('Türkmengaz' in ref or '土库曼国家天然气' in ref): keep=True
        elif old=='CL-GOV-038' and ('金融市场监管委员会' in ref or 'CMF' in ref): keep=True
        elif old=='MX-PARTY-003' and ('Partido Nacional Revolucionario' in ref or '国民革命党' in ref): keep=True
        if keep: restore.append(c)
    print('restore candidates',len(restore))
    for c in restore: print(c['old'],c['ref_name'],c['file'],c['index'])
    if apply:
        for c in restore:
            fp=os.path.join(BASE,c['file']); d=json.load(open(fp,encoding='utf-8'))
            arr=d.get(c['array']); i=c['index']
            if i<len(arr) and arr[i].get(c['field']) is None:
                arr[i][c['field']]=c['old']
                save(fp,d)
        p=os.path.join(OUT,'p2_cluster_apply2_restore.json')
        json.dump({'count':len(restore),'rows':restore},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
        print('restored ->',p)
if __name__=='__main__': main()
