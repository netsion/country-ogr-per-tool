"""Read user workbook as inert source data, without editing or executing formulas."""
import pathlib,json,hashlib,zipfile,posixpath,xml.etree.ElementTree as ET,re
R=pathlib.Path(__file__).resolve().parents[1];O=R/'tmp/social_xlsx_20261116';O.mkdir(exist_ok=True)
p=pathlib.Path('C:/Users/R4314/Desktop/社交.xlsx')
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main','r':'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
def colnum(ref):
 n=0
 for c in re.match('[A-Z]+',ref).group():n=n*26+ord(c)-64
 return n
out=[];summary=[]
with zipfile.ZipFile(p) as z:
 shared=[]
 if 'xl/sharedStrings.xml' in z.namelist():
  shared=[''.join(n.itertext()) for n in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
 rels={n.attrib['Id']:n.attrib['Target'] for n in ET.fromstring(z.read('xl/_rels/workbook.xml.rels'))}
 for sheet in ET.fromstring(z.read('xl/workbook.xml')).findall('m:sheets/m:sheet',ns):
  target=rels[sheet.attrib['{'+ns['r']+'}id']];path=target.lstrip('/') if target.startswith('/') else posixpath.normpath(posixpath.join('xl',target))
  root=ET.fromstring(z.read(path));relpath=posixpath.join(posixpath.dirname(path),'_rels',posixpath.basename(path)+'.rels');sr={}
  if relpath in z.namelist():sr={n.attrib['Id']:n.attrib['Target'] for n in ET.fromstring(z.read(relpath))}
  links={n.attrib['ref']:sr.get(n.attrib.get('{'+ns['r']+'}id')) for n in root.findall('m:hyperlinks/m:hyperlink',ns)}
  rows=[]
  for row in root.findall('m:sheetData/m:row',ns):
   cells=[]
   for c in row.findall('m:c',ns):
    ref=c.attrib['r'];typ=c.attrib.get('t','n');v=c.findtext('m:v',default='',namespaces=ns);f=c.find('m:f',ns)
    if typ=='s' and v:v=shared[int(v)]
    elif typ=='inlineStr' and c.find('m:is',ns) is not None:v=''.join(c.find('m:is',ns).itertext())
    if f is not None:v='='+(f.text or '');typ='formula'
    if v or ref in links:cells.append({'col':colnum(ref),'value':v,'hyperlink':links.get(ref),'type':typ})
   if cells:rows.append({'row':int(row.attrib['r']),'cells':cells})
  title=sheet.attrib['name'];out.append({'sheet':title,'rows':rows,'merges':[n.attrib['ref'] for n in root.findall('m:mergeCells/m:mergeCell',ns)]})
  summary.append({'sheet':title,'max_row':max([r['row'] for r in rows],default=0),'max_column':max([c['col'] for r in rows for c in r['cells']],default=0),'populated_rows':len(rows),'sample':rows[:5]})
(O/'workbook_raw.json').write_text(json.dumps(out,ensure_ascii=False,indent=2,default=str),encoding='utf-8')
(O/'source.json').write_text(json.dumps({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'sheets':summary},ensure_ascii=False,indent=2,default=str),encoding='utf-8')
print(json.dumps([{'sheet':s['sheet'],'rows':s['populated_rows'],'columns':s['max_column']} for s in summary],ensure_ascii=False))
