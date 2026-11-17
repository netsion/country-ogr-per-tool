"""Extract account evidence and propose scoped person-only additions; never executes workbook text."""
import pathlib,json,re,urllib.parse,collections,unicodedata,sys
import zhconv
R=pathlib.Path(__file__).resolve().parents[1];B=R/'output/tw/2026-07-27';O=R/'tmp/social_xlsx_20261116'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def norm(s):return re.sub(r'\s+','',zhconv.convert(unicodedata.normalize('NFKC',str(s)),'zh-cn')).casefold()
def hn(s):return re.sub(r'[\s_\-]','',str(s)).lower()
codes={'facebook':6,'instagram':8,'threads':24,'twitter':3,'youtube':9,'tiktok':29,'line':21,'telegram':19}
def urlkey(u):
 u=urllib.parse.unquote(str(u).strip());p=urllib.parse.urlsplit(u if '://' in u else 'https://'+u);host=p.netloc.lower().split(':')[0]
 host=re.sub(r'^(www\.|m\.|web\.|mobile\.)','',host);path=p.path.strip('/');parts=path.split('/')
 plat={'facebook.com':'facebook','fb.com':'facebook','instagram.com':'instagram','threads.net':'threads','threads.com':'threads','x.com':'twitter','twitter.com':'twitter','youtube.com':'youtube','tiktok.com':'tiktok','t.me':'telegram','page.line.me':'line'}.get(host)
 if not plat or not path:return None
 if plat=='facebook':
  q=urllib.parse.parse_qs(p.query);identity=q.get('id',[None])[0] if path=='profile.php' else None
  if len(parts)==1 and parts[0].isdigit():identity=parts[0]
  if parts[0]=='people' and len(parts)>=3 and parts[-1].isdigit():identity=parts[-1]
  if parts[0]=='p' and re.search(r'-(\d{8,})$',path):identity=re.search(r'-(\d{8,})$',path).group(1)
  if identity:return plat,'id:'+identity
  if len(parts)!=1 or parts[0].lower() in ['share','sharer.php','groups','watch','reel','login','photo','photo.php','permalink.php']:return None
  return plat,parts[0].casefold()
 if plat=='youtube':
  if len(parts)==2 and parts[0]=='channel' and re.fullmatch(r'UC[\w-]{22}',parts[1]):return plat,'id:'+parts[1]
  if len(parts)==1 and parts[0].startswith('@') and len(parts[0])>1:return plat,parts[0].casefold()
  if len(parts)==2 and parts[0] in ['c','user']:return plat,path.casefold()
  return None
 if plat in ['instagram','twitter'] and (len(parts)!=1 or parts[0].lower() in ['p','reel','explore','home','search','i']):return None
 if plat in ['threads','tiktok'] and (len(parts)!=1 or not parts[0].startswith('@')):return None
 return plat,path.casefold()
def rawid(v,cell=None):
 s=str(v or '').strip()
 if not s or s in ['/','-','无','None','null']:return None
 if cell and cell.get('type')=='n' and (re.search('[eE.]',s) or len(s)>15):return None
 if re.fullmatch(r'\d+|UC[\w-]{22}|(?:fb#RHINO#|instagram#|threads#|twitter#|youtube#|tiktok#)\S+',s):return s
 return None
def uidval(p,s):
 if not s:return None
 return s if '#' in s else ('fb#RHINO#' if p=='facebook' else p+'#')+s
def bare(s):return str(s).split('#')[-1]
