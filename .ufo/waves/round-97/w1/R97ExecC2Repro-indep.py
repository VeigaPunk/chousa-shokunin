#!/usr/bin/env python3
import re
R="/fast/scratch/hyaku/chousa-r97/R97ExecC2Repro/repo/"
t=open(R+"corpus/knowledge/press-checklist-questions-r97.md").read()
lq=re.findall(r"\| (L\d+) \| (S22[56]) \| \"(.*?)\" \|",t)
caps={"S225":open(R+"corpus/captures/347c55ba9be9d63afe17986e.txt").read().splitlines(),"S226":open(R+"corpus/captures/80a844fe287a1a26d4280251.txt").read().splitlines()}
miss=[]
for qid,src,q in lq:
    hits=[i+1 for i,ln in enumerate(caps[src]) if q in ln]
    print(qid,src,len(q),"lines",hits)
    if not hits: miss.append(qid)
s225=[q for i,s,q in lq if s=="S225"]
def n(s): return " ".join(s.split())
def l(s): return re.sub(r"[^a-z0-9]","",s.lower())
t226=open(R+"corpus/captures/80a844fe287a1a26d4280251.txt").read()
print("missing_line_quotes",miss)
print(f"VERBATIM {sum(n(q) in n(t226) for q in s225)}/{len(s225)} LETTERS {sum(l(q) in l(t226) for q in s225)}/{len(s225)}")
