# Round 25 — Claim 2 critic
Evidence: `round25-claims.md:52-60`; frozen output `round25-measure-before.log:6-10` = 2+13+43+8=66. Axis: freshness. No install; no gate/selftest run.
## Counterexamples
- 2a (`round25-measure.sh:26-30`) searches a path substring, not a unique table row, nonempty cells or resolvable target; prose can fake it. Use table parsing.
- 2b (`:31-33`) only requires `^Round N\b`; isolated test of exact regex matched `Round 11 ` (`True`). No paragraph/pointer check. Pre-reg acceptance is unspecified (`round25-claims.md:59-60`).
- 2c (`:34-42`) inspects only present rows matching a narrow filename regex. Delete all 43 rows or change names outside the regex and `mis` becomes 0. No frozen identity set, uniqueness, cell or file check. README confirms r12–r23 are queued under Round-8 (`corpus/evidence/README.md:938-942`); all 43 frozen receipt files exist.
- 2d (`:43-53`) derives its population from mutable LOG and accepts any 4-cell numeric-round row, any pointer. Isolated probe `| fake capability | does something | unverifiable-pointer | 15 |` passed the row predicate (`True`). Deleting a LOG claim also shrinks the population. Existing r13/r14 rows provide valid controls (`SCORECARD.md:674,731`).
- Therefore current checks detect base defects but are gameable; zero need not mean re-indexing/re-derivation. `QUALITY.md:33-51` requires owning revision/command and same-landing capability rows.
## Exact predicates to replace Claim-2 Python block
Keep `base_files` and imports. These preserve base counts: 2a exact missing rows, 13 unqualified Frontier entries, 43 pinned receipt identities in wrong section, 8 missing/invalid capability rows.
```python
cov = readme.split("## Frontier",1)[0]; cr=[]
ev=open("corpus/evidence/README.md",encoding="utf-8").read().splitlines(); log=open("LOG.md",encoding="utf-8").read().splitlines(); sc=open("SCORECARD.md",encoding="utf-8").read()
for l in cov.splitlines():
 c=l.strip().strip("|").split("|",2)
 if len(c)==3 and c[0].strip().startswith("`") and c[0].strip().endswith("`"): cr.append((c[0].strip()[1:-1],c[1].strip(),c[2].strip()))
unindexed=[p for p in base_files if sum(bool(r[0]==p and r[1] and r[2]) for r in cr)!=1 or not os.path.isfile("corpus/"+p)]; print("2a UNINDEXED=%d %s"%(len(unindexed),unindexed))
front=readme.split("## Frontier",1)[1] if "## Frontier" in readme else ""; blocks={}
for p in re.split(r"\n\s*\n",front):
 m=re.match(r"^Round (1[1-9]|2[0-3]) — .+",p)
 if m: blocks.setdefault(int(m.group(1)),[]).append(p)
def linked(s):
 r=re.findall(r"`(corpus/(?:evidence|knowledge)/[^`]+)`",s)
 return bool(r) and all(os.path.isfile(x) for x in r)
def fok(p):
 e=re.search(r"(?m)^Evidence: (.+)$",p)
 return all(re.search(r"(?m)^%s: \S"%k,p) for k in ("Claim","Before","After","Evidence","Rerun","Limit")) and bool(e and linked(e.group(1)) and re.search(r"(?m)^Rerun: `[^`]+`$",p))
missing=[n for n in range(11,24) if len(blocks.get(n,[]))!=1 or not fok(blocks[n][0])]; print("2b FRONTIER_MISSING=%d rounds=%s"%(len(missing),missing))
ev_spec={12:("scope","115519","selftest A-fix drift-r8"),13:("alias","123621","selftest bypass-before bypass-after battery"),14:("mount","132025","selftest bypass-before bypass-after battery"),15:("root","152000","selftest demo battery drift"),17:("fence","171200","selftest demo battery drift"),18:("scope","173000","selftest demo battery drift"),19:("symlink","174500","selftest demo battery drift"),20:("verify","180000","selftest demo battery drift"),21:("ptr","184000","selftest demo battery drift"),22:("deny","190000","selftest demo battery drift"),23:("fanchor","192000","selftest demo battery drift")}
ex={n:{f"{p}-r{n}-20261019T{t}Z-{s}.log" for s in ss.split()} for n,(p,t,ss) in ev_spec.items()}; head=None; loc={}
for l in ev:
 m=re.match(r"^## Round-(\d+)\b",l)
 if m: head=int(m.group(1)); continue
 if l.startswith("## "): head=None; continue
 c=l.strip().strip("|").split("|",2); m=re.match(r"`([^`]+)`",c[0].strip()) if len(c)==3 else None
 if m: loc.setdefault(m.group(1),[]).append((head,bool(c[1].strip()),bool(c[2].strip())))
def evok(n,f):
 z=loc.get(f,[]); return len(z)==1 and z[0][0]==n and z[0][1] and z[0][2] and os.path.isfile("corpus/evidence/"+f)
mis=sum(not evok(n,f) for n,fs in ex.items() for f in fs); print("2c EVIDENCE_MISFILED_ROWS=%d"%mis)
claimed={13,14,15,17,18,19,20,21,22,23}; log_claims={int(m.group(1)) for l in log for m in [re.search(r"SCORECARD §Round (\d+)\)?.*Capabilities \+1",l)] if m}; rows={}
for sec in re.split(r"^## ",sc,flags=re.M):
 if sec.startswith("Capabilities"):
  for l in sec.splitlines():
   c=[x.strip() for x in l.strip().strip("|").split("|")]
   if len(c)==4 and c[3].isdigit(): rows.setdefault(int(c[3]),[]).append(c)
def cpok(n,p):
 r=re.findall(r"`(corpus/(?:evidence|knowledge)/[^`]+)`",p)
 if any(not os.path.isfile(x) for x in r): return False
 cs=re.findall(r"selftest cases? (\d+)[–-](\d+)",p)
 if "selftest case" in p and not cs: return False
 if cs:
  sf=next((f for f in ex[n] if f.endswith("-selftest.log")),None)
  if not sf: return False
  nums={int(x) for x in re.findall(r"^ok-case\s+(\d+)\b",open("corpus/evidence/"+sf,encoding="utf-8").read(),re.M)}
  return all(set(range(int(a),int(b)+1))<=nums for a,b in cs)
 return any(x.startswith("corpus/evidence/") for x in r)
cm=[n for n in sorted(claimed) if n not in log_claims or len(rows.get(n,[]))!=1 or not all(rows[n][0][:2]) or not cpok(n,rows[n][0][2])]; print("2d CAP_ROWS_MISSING=%d rounds=%s (LOG Capabilities +1 rounds=%s)"%(len(cm),cm,sorted(log_claims)))
print("STALE_INDEX_ITEMS=%d"%(len(unindexed)+len(missing)+mis+len(cm)))
```
Qualitative acceptance: Frontier text states specific move, measured before/after, what evidence establishes, honest limit; `Rerun` reproduces it. Evidence rows move exactly once under the true heading, with Shows/Key result matching receipt bytes. Capability rows name bounded behavior; case/receipt pointer must support the behavior, not merely exist. Coverage rows need actual path and substantive Holds/Sources. Human review rejects unrelated-but-existing pointers; syntax cannot establish truth.
VERDICT: Current Claim 2 is baseline-diagnostic but vacuously closable. Freeze the populations and add these predicates; verify a new round-25 capability separately. Installs: none.