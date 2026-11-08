"""
Probe (a) continued: can the committed bytes already exhibit the divergence?
Run _qual vs count on the landing tree; compare sets, not just totals.
Also check D1/D2 membership and http values in committed corpus.
"""
import importlib.util, collections
spec = importlib.util.spec_from_file_location("gr87", "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/wt/corpus/evidence/round87/gate-records-r87.py")
gr87 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gr87)
root = "/fast/scratch/hyaku/chousa-r87/R87ReviewerC1/tree-pristine"
q = gr87._qualifying_203(root)
print("qualifying rows (sid,url,http):", [(x[0], x[7], x[1]) for x in q])
print("len qual:", len(q))
print("count:", gr87.count_203_rows(root))
# duplicates in qual?
c = collections.Counter((x[0], x[1]) for x in q)
print("dup (sid,url) in qual:", [k for k,v in c.items() if v>1] or "none")
d1 = gr87.build_d1_203_admits(root)
d2 = gr87.build_d2_203_rejects(root)
print("D1 sids:", [s for s,_ in d1])
print("D2 sids:", [s for s,_ in d2])
print("D2 lines:")
for s,l in d2: print(" ", l[:200])
# raw refetch non-200 rows detail
rows = gr87.refetch_rows(root)
for f in rows:
    if f[6] != "200":
        print("non-200 row:", f[0], f[1][:60], "rc=",f[5],"http=",f[6],"len=",len(f[6]),"txt=",f[8][:12])
