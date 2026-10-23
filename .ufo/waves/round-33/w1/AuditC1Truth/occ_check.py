import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import verify_truth as vt
out={}
for keep in sys.argv[1:]:
    root=os.path.abspath(keep)
    lines=open(os.path.join(root,'claims.jsonl'),encoding='utf-8').read().splitlines()
    dist={}; amb=[]
    for line in lines:
        rec=vt.parse_line(line)
        if any(k in ('line','sha256') and sum(1 for kk,_ in rec.pairs if kk==k)>1 for k in ('line','sha256')): continue
        src=rec.get('source'); span=rec.get('span')
        if not isinstance(src,str) or not isinstance(span,str): continue
        p=os.path.join(root,src)
        if not os.path.isfile(p): continue
        hay=open(p,encoding='utf-8').read()
        occ=list(vt.occurrences(hay,span))
        dist[len(occ)]=dist.get(len(occ),0)+1
        # ambiguity: occurrence not on named line(s) while also on them
        lf=rec.get('line')
        if isinstance(lf,str) and occ and len(set(occ))>1: amb.append((rec.get('id'),occ,lf))
    out[keep.split('/')[-1]]={'occurrence_count_distribution':dist,'multi_distinct_line_ranges':amb[:5],'n_multi':len(amb)}
print(json.dumps(out,indent=1))
