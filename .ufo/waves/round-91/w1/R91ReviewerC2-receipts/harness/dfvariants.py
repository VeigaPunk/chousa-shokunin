import os,importlib.util
S="/fast/scratch/hyaku/chousa-r91/R91ReviewerC2"; ROOT=os.path.join(S,"repo")
spec=importlib.util.spec_from_file_location("cur",os.path.join(ROOT,"corpus","evidence","round91","curation-r91.py"))
cur=importlib.util.module_from_spec(spec); spec.loader.exec_module(cur)
EA="corpus/knowledge/search-transparency-reporting-r84.md"
reg=cur.parse_registry(ROOT)
text=open(os.path.join(ROOT,EA),encoding="utf-8").read()
quotes={}
for ln,c in cur.data_lines(cur.section_lines(text,"Located quotes")):
    if cur.q_shape_violation(c) is None:
        q=c[2].strip().strip('"')
        if cur.locates(q,cur.capture_text(ROOT,reg,c[1])): quotes[c[0]]=cur.norm(q)
rows=list(cur.table_rows(cur.section_lines(text,"Decision table"),4))
def df(docs,w):
    return sum(1 for d in docs if w in cur.quote_terms(d))
coded=list(quotes.values())+[c[1]+" "+c[2] for c in rows]
split=list(quotes.values())+[x for c in rows for x in (c[1],c[2])]
rows_only_don=[c[1] for c in rows]
print("ENTRY_A quotes",len(quotes),"rows",len(rows))
for name,docs in (("coded (quotes + row Do/Never joined)",coded),
                  ("quotes + Do and Never as separate docs",split),
                  ("quotes only",list(quotes.values())),
                  ("row Do cells only",rows_only_don)):
    print(f"  {name}: docs={len(docs)} df(source)={df(docs,'source')} df(resource)={df(docs,'resource')}")
# occurrence count (not df)
occ=sum(d.lower().count("source") for d in coded)
print("  occurrence count of 'source' over coded docs:",occ)
