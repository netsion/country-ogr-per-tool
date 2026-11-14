# -*- coding: utf-8 -*-
"""P2 cluster batch 13: selected clear wrong clusters; keep by keywords."""
import glob,json,os,sys,time
from collections import Counter
sys.path.insert(0,os.path.dirname(__file__))
from id_integrity_audit2 import BASE,OUT,load_datasets
from p2_plan_strict import strict_match
EX={'gn','ng'}
CLUSTERS={
 'CL-ACAD-003':['康塞普西翁大学','Universidad de Concepción'],
 'TM-SOE-001':['土库曼天然气','土庫曼天然氣','Türkmen gaz','Turkmengaz'],
 'CL-NGO-001':['智利基金会','Fundación Chile'],
 'MX-CORP-001':['美洲移动','América Móvil','Telcel'],
 'JP-FIN-007':['邮贮银行','郵貯銀行','ゆうちょ','Yucho','Japan Post Bank'],
 'RU-PERSON-000113':['卡里萨洛夫','Karisalov'],
 'SA-ACAD-009':['本阿卜杜勒阿齐兹国王健康科学大学','King Saud bin Abdulaziz'],
 'CA-GOV-004':['加拿大众议院','House of Commons'],
 'BO-CORP-005':['玻利维亚水泥','Sociedad Boliviana de Cemento','Soboce'],
 'CM-GOV-008':['对外关系部','Relations extérieures'],
 'CD-GOV-011':['内政、安全','Ministère de l’Intérieur',"Ministère de l'Intérieur"],
 'MX-PARTY-003':['制度革命党','Partido Revolucionario Institucional','PRI'],
 'MX-FIN-010':['墨西哥陆海空三军国家银行','Banco Nacional del Ejército'],
 'CL-GOV-038':['金融市场委员会','Comisión para el Mercado Financiero'],
 'RU-CORP-013':['VK','Mail.ru'],
 'RU-PERSON-000114':['科诺夫','Konov'],
 'TD-GOV-008':['乍得外交部','Ministère des Affaires étrangères'],
 'RU-PERSON-000001':['登金','Dynkin'],
 'CI-GOV-009':['外交与国际合作部','Ministère des Affaires étrangères'],
 'CL-CORP-001':['法拉贝拉','Falabella'],
}
def names_of(p):
    bi=p.get('basic_info') or {}
    vals=[bi.get('name_zh'),bi.get('name_en'),bi.get('name_original')]+list(bi.get('aliases') or [])
    return [v.strip() for v in vals if isinstance(v,str) and v.strip()]
def save(p,obj):
    payload=json.dumps(obj,ensure_ascii=False,indent=2)+'\n'; tmp=p+'.tmp'
    for _ in range(6):
        try:
            open(tmp,'w',encoding='utf-8',newline='\n').write(payload); os.replace(tmp,p); return
        except PermissionError: time.sleep(.5)
    open(p,'w',encoding='utf-8',newline='\n').write(payload)
def nm(x,cat):
    keys={'work_org':('organization','org_name','organization_en'),'related_org':('org_name','name','organization'),'person_rel':('person_name','name'),'family':('name','person_name'),'key_people':('name','name_en','person_name')}[cat]
    for k in keys:
        v=x.get(k)
        if isinstance(v,str) and v.strip(): return v.strip()
    return ''
def main():
    apply='--apply' in sys.argv
    latest,_=load_datasets(); names={}
    for cc,(date,folder) in latest.items():
        if cc in EX: continue
        for sub in ('orgs','persons'):
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); oid=d.get('org_id') or d.get('person_id')
                if oid: names[oid]=names_of(d)
    changes=[]; stats=Counter()
    for cc,(date,folder) in latest.items():
        if cc in EX: continue
        for sub,arrs in [('persons',[('work_experience','org_id','work_org'),('person_relationships','person_id','person_rel'),('family_members','person_id','family')]),('orgs',[('key_people','person_id','key_people'),('related_entities','org_id','related_org')])]:
            for f in glob.glob(os.path.join(folder,sub,'*.json')):
                if os.path.basename(f).startswith('_'): continue
                d=json.load(open(f,encoding='utf-8')); dirty=False
                for arr,field,cat in arrs:
                    for i,x in enumerate(d.get(arr) or []):
                        if not isinstance(x,dict): continue
                        v=x.get(field)
                        if v not in CLUSTERS: continue
                        ref=nm(x,cat)
                        if not ref: continue
                        low=ref.lower(); kw=CLUSTERS[v]
                        if any(k.lower() in low for k in kw) or strict_match(ref,names.get(v,[])):
                            stats['keep']+=1; continue
                        changes.append({'file':os.path.relpath(f,BASE).replace(os.sep,'/'),'array':arr,'index':i,'field':field,'old':v,'new':None,'ref_name':ref,'cat':cat})
                        x[field]=None; dirty=True; stats['null']+=1
                if apply and dirty: save(f,d)
    summary={'apply':apply,'keep':stats['keep'],'null':stats['null']}
    print(json.dumps(summary,ensure_ascii=False,indent=1))
    if apply:
        p=os.path.join(OUT,'p2_cluster_apply2_undo.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('undo ->',p)
    else:
        p=os.path.join(OUT,'p2_cluster_apply2_dry.json'); json.dump({'summary':summary,'changes':changes},open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1); print('dry ->',p); print('DRY')
if __name__=='__main__': main()
