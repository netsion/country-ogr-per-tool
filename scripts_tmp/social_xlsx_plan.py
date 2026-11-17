from social_xlsx_common import *
raw=load(O/'workbook_raw.json');records=[];id_only=[]
name_headers=['姓名','person_nm','目标','orgname','用户昵称','昵称','nickname']
for sh in raw:
 rows=sh['rows'];headers={c['col']:hn(c['value']) for c in rows[0]['cells']};byrow={r['row']:{c['col']:c for c in r['cells']} for r in rows}
 namecols=[c for label in name_headers for c,h in headers.items() if h==hn(label)]
 uidcols=[c for c,h in headers.items() if h in ['userid','账号id','脸书id','facebook账号id']]
 pagecols=[c for c,h in headers.items() if h=='pageid']
 for r in rows[1:]:
  cells={c['col']:c for c in r['cells']};name=next((str(cells[c]['value']).strip() for c in namecols if c in cells and cells[c]['value']),None)
  if not name and namecols:
   for merge in sh.get('merges',[]):
    m=re.fullmatch(r'([A-Z]+)(\d+):([A-Z]+)(\d+)',merge)
    if not m:continue
    def cn(s):
     n=0
     for a in s:n=n*26+ord(a)-64
     return n
    if int(m[2])<=r['row']<=int(m[4]) and cn(m[1])==cn(m[3]) and cn(m[1]) in namecols:
     name=byrow.get(int(m[2]),{}).get(cn(m[1]),{}).get('value');break
  seen=set()
  for c in r['cells']:
   vals=[c.get('hyperlink'),c.get('value')]
   for v in vals:
    if not isinstance(v,str) or not re.match('https?://',v.strip(),re.I):continue
    key=urlkey(v)
    if not key or key in seen:continue
    seen.add(key);plat=key[0];uc=None;pc=None
    # Wide platform tables associate only the nearby platform-specific ID columns.
    if headers.get(c['col']) in ['facebook','instagram','threads','x','youtube','tiktok']:
     j=c['col']+1
     while j<=max(headers) and headers.get(j) not in ['facebook','instagram','threads','x','youtube','tiktok']:
      h=headers.get(j,'')
      if (h=='userid' or h in [plat+'id','xid']) and j in cells:uc=cells[j]
      if h=='pageid' and j in cells:pc=cells[j]
      j+=1
    else:
     uc=next((cells[j] for j in uidcols if j in cells),None);pc=next((cells[j] for j in pagecols if j in cells),None)
    records.append({'sheet':sh['sheet'],'row':r['row'],'cell_col':c['col'],'name':str(name) if name else None,'platform':plat,'url':v.strip(),'key':list(key),'raw_user_id':rawid(uc.get('value'),uc) if uc else None,'raw_page_id':rawid(pc.get('value'),pc) if pc else None})
  if not seen and name and uidcols:
   u=next((cells[j] for j in uidcols if j in cells),None)
   if u and rawid(u['value'],u):id_only.append({'sheet':sh['sheet'],'row':r['row'],'name':name,'raw_id':rawid(u['value'],u)})
profiles={p.stem:load(p) for p in (B/'persons').glob('TW-PERSON-*.json')};nameidx=collections.defaultdict(set);urlidx=collections.defaultdict(set);uididx=collections.defaultdict(set)
for pid,d in profiles.items():
 for n in [d.get('name'),d.get('name_zh'),d.get('name_en')]:
  if n:nameidx[norm(n)].add(pid)
 for a in d.get('social_accounts',[]):
  k=urlkey(a.get('url',''))
  if k and not re.search('待核|归属.*疑|官方性存在疑',a.get('source_note','')):
   urlidx[k].add(pid)
   if k[1].startswith('id:'):uididx[(k[0],k[1][3:])].add(pid)
  if a.get('user_id'):uididx[(a.get('platform'),bare(a['user_id']))].add(pid)
# Per-row identity anchors prevent name-only homonym linking.
anchors=collections.defaultdict(set)
for r in records:
 anchors[(r['sheet'],r['row'])].update(urlidx.get(tuple(r['key']),set()))
 if r['raw_user_id']:anchors[(r['sheet'],r['row'])].update(uididx.get((r['platform'],bare(r['raw_user_id'])),set()))
proposals=[];unmatched=[]
for r in records:
 direct=urlidx.get(tuple(r['key']),set());named=nameidx.get(norm(r['name']),set()) if r['name'] else set();rowanchor=anchors[(r['sheet'],r['row'])]
 if direct and named and not direct.intersection(named):
  unmatched.append({**r,'reason':'url_name_identity_conflict','named':sorted(named),'anchors':sorted(direct)});continue
 owners=direct or (named & rowanchor if named and rowanchor else rowanchor or named)
 if len(owners)!=1:
  if named or rowanchor:unmatched.append({**r,'reason':'ambiguous_or_conflicting_identity','named':sorted(named),'anchors':sorted(rowanchor)})
  continue
 pid=next(iter(owners));d=profiles[pid];existing=[]
 for i,a in enumerate(d.get('social_accounts',[])):
  ak=urlkey(a.get('url',''));same_id=r['raw_user_id'] and a.get('platform')==r['platform'] and ((a.get('user_id') and bare(a['user_id'])==bare(r['raw_user_id'])) or (ak and ak[1]=='id:'+bare(r['raw_user_id'])))
  if ak==tuple(r['key']) or same_id:existing.append(i)
 proposals.append({**r,'person_id':pid,'person_name':d.get('name_zh',d['name']),'method':'existing_url' if direct else 'row_anchor' if rowanchor else 'exact_name_only','existing_indices':existing,'existing_accounts':[d['social_accounts'][i] for i in existing],'suggested_user_id':uidval(r['platform'],r['raw_user_id'])})
save=lambda name,d:(O/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
save('records.json',records);save('proposals.json',proposals);save('ambiguous.json',unmatched);save('id_only.json',id_only)
people=collections.defaultdict(list)
for p in proposals:people[p['person_id']].append(p)
print(json.dumps({'sheets':len(raw),'link_records':len(records),'proposals':len(proposals),'people':len(people),'methods':dict(collections.Counter(p['method'] for p in proposals)),'new_candidate_unique':len({(p['person_id'],tuple(p['key'])) for p in proposals if not p['existing_indices']}),'by_person':[{'id':pid,'name':profiles[pid].get('name_zh',profiles[pid]['name']),'matched_rows':len(ps),'new_accounts':len({tuple(p['key']) for p in ps if not p['existing_indices']})} for pid,ps in people.items()]},ensure_ascii=False))
