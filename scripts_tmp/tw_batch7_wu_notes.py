"""Remove superseded draft-status notes after the research follow-up."""
import pathlib,json
p=pathlib.Path(__file__).resolve().parents[1]/'tmp/tw_batch7_enriched/TW-PERSON-000578.json'
d=json.loads(p.read_text(encoding='utf-8'));n=d['collection_meta']['notes']
n=n.replace('家庭已检索，TVBS单源公开儿子吴昇翰，未获第二独立全文故暂不结构化；配偶未核。','配偶未核。')
n=n.replace('关系检索发现苏巧慧公开称双方共同争取轨道预算，因未完成引用画像核验暂不链接。','')
n=n.replace('前述暂不结构化说明以此补充为准。','')
d['collection_meta']['notes']=n
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
