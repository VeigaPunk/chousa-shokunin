#!/usr/bin/env python3
"""Independent C2 checker (no lane scripts)."""
import json, re, sys
ENTRY="/fast/scratch/hyaku/chousa-r99/R99ExecC2Repro/repo/corpus/knowledge/quotation-error-rates-r99.md"
CAPJ="/fast/scratch/hyaku/chousa-r99/R99ExecC2Repro/repo/corpus/captures/405a0054e1f6dbd1854a3618.txt"
CAPG="/fast/scratch/hyaku/chousa-r99/R99ExecC2Repro/repo/corpus/captures/4b70901ad80c513f0c2f750c.txt"
def norm(s):
    return " ".join(s.replace("\u2018","'").replace("\u2019","'").replace("\u201c",'"').replace("\u201d",'"').split())
text=open(ENTRY,encoding="utf-8").read()
lines=text.splitlines()
def section(title):
    on=False; out=[]
    for ln in lines:
        if ln.strip()==f"## {title}": on=True; continue
        if on and ln.startswith("## "): break
        if on: out.append(ln)
    return out
ROW=re.compile(r'^\| ([A-Z][0-9]+) \| (S[0-9]+) \| "(.*)" \|$')
quotes=[m.groups() for m in (ROW.match(ln) for ln in section("Located quotes")) if m]
capJraw=open(CAPJ,encoding="utf-8").read()
rec=json.loads(capJraw)["resultList"]["result"][0]
capJnorm=norm(capJraw)
capGnorm=norm(open(CAPG,encoding="utf-8").read())
titleJ=rec.get("title",""); abstr=rec.get("abstractText","")
print(f"quotes_parsed={len(quotes)}")
in_cap=0; j0_ok=0; j18_ok=0; per=[]
for qid,src,q in quotes:
    cap = capJnorm if src=="S236" else capGnorm
    found = norm(q) in cap
    in_cap += found
    if src=="S236":
        if qid=="J0":
            m = norm(q)==norm(titleJ); j0_ok+=m
            per.append((qid,found,f"J0_norm_eq_title={m} title={titleJ!r}"))
        else:
            m = norm(q) in norm(abstr); j18_ok+=m
            per.append((qid,found,f"in_abstract={m}"))
    else:
        per.append((qid,found,""))
for p in per: print(p)
print(f"QUOTES_IN_CAPTURE={in_cap}/23 J0_OK={j0_ok}/1 J1-J8_OK={j18_ok}/8")
# decision rows: numbers in Do cell must be in warrant quotes
rows=[ln for ln in section("Decision table") if ln.startswith("|")]
cells=[[c.strip() for c in r.strip()[1:-1].split(" | ")] for r in rows[2:]]
print(f"decision_rows={len(cells)}")
byqid={q: (s,qq) for q,s,qq in quotes}
NUM=re.compile(r"[0-9]+(?:[.,][0-9]+)*%?|\d[\d,]*")
for i,c in enumerate(cells):
    do=c[1]; warrants=c[3].split(",")
    warrants=[w.strip() for w in warrants if w.strip()]
    nums=NUM.findall(do)
    wtext=" ".join(byqid[w][1] for w in warrants if w in byqid)
    ok=[]
    for n in nums:
        ok.append((n, n in wtext))
    print(f"row{i+1} Do={do!r} warrants={warrants} nums_ok={ok} all={all(x[1] for x in ok)}")
# identity check
print("J0 raw title check:", "Quotation accuracy in medical journal articles" in titleJ, "| pmid=",rec.get("pmid"),"doi=",rec.get("doi"),"journalInfo=",rec.get("journalInfo"))
print("G capture has doi/title:", "10.1371/journal.pone.0184727" in open(CAPG,encoding="utf-8").read(), "Accuracy of cited" in open(CAPG,encoding="utf-8").read())
