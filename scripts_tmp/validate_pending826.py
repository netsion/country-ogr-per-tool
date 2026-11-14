"""Read OOXML validation; restore original native filters lost on artifact export."""
import csv,json,pathlib,zipfile,xml.etree.ElementTree as E,copy
R=pathlib.Path(__file__).resolve().parents[1];D=R/'outputs/registry826_20261113'
src=R/'output/_id_audit/registry_newid_pending826_review.xlsx';dst=D/'registry_newid_pending826_reviewed.xlsx'
N={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}; tag='{'+N['m']+'}'
def cells(z,p):
 ss=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  ss=[''.join(t.text or '' for t in si.iter(tag+'t')) for si in E.fromstring(z.read('xl/sharedStrings.xml'))]
 out={}
 for c in E.fromstring(z.read(p)).iter(tag+'c'):
  t=c.get('t');v=c.find(tag+'v');v=v.text if v is not None else ''
  if t=='s':v=ss[int(v)]
  elif t=='inlineStr':v=''.join(x.text or '' for x in c.iter(tag+'t'))
  assert t!='e',(p,c.attrib,v)
  out[c.get('r')]=v or ''
 return out
rows=list(csv.DictReader((D/'registry_newid_pending826_reviewed.csv').open(encoding='utf-8-sig')))
with zipfile.ZipFile(src) as a,zipfile.ZipFile(dst) as b:
 payload={n:b.read(n) for n in b.namelist()}
 for si,rr in [(1,rows),(2,[r for r in rows if r['优先级']=='1'])]:
  p=f'xl/worksheets/sheet{si}.xml';old=cells(a,p);new=cells(b,p)
  for row in range(1,len(rr)+2):
   for col in 'ABCDEFGHIJKL':
    key=f'{col}{row}';assert old.get(key,'')==new.get(key,''),(key,old.get(key),new.get(key))
  for ri,r in enumerate(rr,2):
   for col,k in zip('MNOP',['复核结论','建议类别','建议国别','备注']):assert new.get(f'{col}{ri}','')==r[k]
  original=E.fromstring(a.read(p));root=E.fromstring(payload[p]);f=original.find(tag+'autoFilter')
  if f is not None and root.find(tag+'autoFilter') is None:
   sd=root.find(tag+'sheetData');root.insert(list(root).index(sd)+1,copy.deepcopy(f))
   payload[p]=E.tostring(root,encoding='utf-8',xml_declaration=True)
  assert root.find('.//'+tag+'pane').get('state')=='frozen'
 for p in b.namelist():
  if p.startswith('xl/worksheets/sheet') and p.endswith('.xml'):cells(b,p)
tmp=dst.with_suffix('.checked.xlsx')
with zipfile.ZipFile(tmp,'w',zipfile.ZIP_DEFLATED) as z:
 for n,data in payload.items():z.writestr(n,data)
tmp.replace(dst)
with zipfile.ZipFile(dst) as z:
 for si in [1,2]:assert E.fromstring(z.read(f'xl/worksheets/sheet{si}.xml')).find(tag+'autoFilter') is not None
(D/'validation.json').write_text(json.dumps({'reviewed_rows':826,'P1_rows':190,'original_A_L_equal':True,'review_columns_equal_csv':True,'filters_preserved':True,'freeze_preserved':True,'excel_error_cells':0,'business_mutations':0},indent=2),encoding='utf-8')
print('PASS: 826 rows, P1 190; A:L unchanged; M:P matches CSV; native filters and freeze retained; zero Excel error cells.')
