# R55W2CritForgeNonReader — non-reading C1 forge attack

**Axis:** round-55 C1 operability / capability acquisition. The round-56 frozen claims were read first (`corpus/evidence/round56/claims.md` lines 41–49 route the 36 undispatched W2 items as round-55 corrections). Attack target is round-55 C1, whose frozen predicate is in `corpus/evidence/round55/c1-count.py` lines 3–47. No predicate, target, counter, or control changed. No tools installed or updated.

## Forge

This forge does not import, copy, invoke, or reimplement `tools/capture-text.py`; it does not parse CFB/FIB/Clx. It guesses text from `.txt` sidecars or UTF-16LE-decoded raw bytes, stripping control characters, then takes a minimal one-character context on each side. Offset is the guess's own index, not an oracle-derived offset.

```python
import argparse, hashlib, pathlib, sys
p=argparse.ArgumentParser(); p.add_argument('--quotes',required=True); p.add_argument('--out',required=True); p.add_argument('--cache',required=True); a=p.parse_args()
q=pathlib.Path(a.quotes); out=pathlib.Path(a.out); cache=pathlib.Path(a.cache); (out/'spans').mkdir(parents=True,exist_ok=True)
rows=q.read_text(encoding='utf-8').splitlines()[1:]
manifest=['id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry']; counts={}; fails=[]
for line in rows:
 sid,url,quote,entry=line.split('\t'); key=hashlib.sha256(url.encode()).hexdigest()[:24]; raw=cache/(key+'.raw'); txt=cache/(key+'.txt'); data=''; f=raw if raw.exists() else txt
 if txt.exists(): data=txt.read_text(encoding='utf-8',errors='replace').replace('\r\n','\n').replace('\r','\n')
 if raw.exists():
  u=raw.read_bytes().decode('utf-16le',errors='replace'); u=''.join(c for c in u if c in '\n\t' or ord(c)>=32)
  if quote in u: data=u
 pos=data.find(quote)
 if pos<0: fails.append((sid,quote)); continue
 lo=max(0,pos-1); hi=min(len(data),pos+len(quote)+1); span=data[lo:hi]
 counts[sid]=counts.get(sid,0)+1; name=f"spans/{sid}-{counts[sid]}.txt"; (out/name).write_text(span,encoding='utf-8')
 manifest.append('\t'.join((sid,url,hashlib.sha256(f.read_bytes()).hexdigest(),str(lo),name,quote,entry)))
 print(f'QUOTE {sid} char {lo+span.find(quote)} {name}')
if fails:
 for sid,_ in fails: print(f'build-spans: refused {sid}: surrogate quote absent',file=sys.stderr)
 sys.exit(1)
(out/'spans.tsv').write_text('\n'.join(manifest)+'\n',encoding='utf-8')
```

## Measurement

Ran the frozen driver three times against that forge, each with an empty explicit `--work` under `/fast/scratch/hyaku/chousa-r56/R55W2CritForgeNonReader`; `--per-leg` remained the counter default 3. Commands: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round55/c1-count.py --tool /fast/scratch/hyaku/chousa-r56/R55W2CritForgeNonReader/forge.py --work <empty-work>` with `--seed 7` for the first run and no seed for the next two. `TMPDIR` was the same scratch directory and `PYTHONDONTWRITEBYTECODE=1`.

Observed driver receipts (the unseeded seeds are the values actually printed):

```text
seed 7:        GENOLE=FAIL S901 span is not a slice of the defined form
               OLEPIN=FAIL S921 span is not a slice of the defined form
               REFUSE=FAIL NOFORM: rc=0
               REGRESS=FAIL spans.tsv differs from round 54's
               LEGS=0/4; C1=FAIL
seed 671734806:GENOLE=FAIL S901 span is not a slice of the defined form
               OLEPIN=FAIL S921 span is not a slice of the defined form
               REFUSE=FAIL NOFORM: rc=0
               REGRESS=FAIL spans.tsv differs from round 54's
               LEGS=0/4; C1=FAIL
seed 249804021:GENOLE=FAIL S901 span is not a slice of the defined form
               OLEPIN=FAIL rc=1, stderr ends `build-spans: refused S923: surrogate quote absent`
               REFUSE=FAIL NOFORM: rc=0
               REGRESS=FAIL spans.tsv differs from round 54's
               LEGS=0/4; C1=FAIL
```

Per-leg first counter divergence: GENOLE rejects the first S901 span as not an exact slice; OLEPIN rejects first S921 likewise in the first two runs, and cannot find S923 in the third. REFUSE accepts the UTF-16-decoded NOFORM bait (`rc=0`) instead of refusing it. REGRESS first rejects the round-54 manifest byte comparison (`spans.tsv differs`). These are the counter's first reported failures for those legs, not claims that no later mismatch exists. The round-55 judge's slice check is `c1-count.py` lines 267–272; refusal check lines 318–328; regression comparison lines 391–405.
As a direct form-position cross-check after measurement (not part of the forge), I used the pinned `tools/capture-text.py` on the saved cache raw files. For seed 7 GENOLE, the first S901 forge offset was 1408 while the defined form length was 249; the emitted span began `wR4 jflj 丱嗂坭`, so the indexed defined-form slice is empty. Seed 7 OLEPIN S921 used offset 6010; at that position the defined form begins `指触发漏洞对受影响组件造成的损害程度。影`, versus the emitted `符串作为参数时，因参数类型、数量等过滤不`. For unseeded seed 671734806, GENOLE S901 used offset 1373 while its form length was 299; OLEPIN S921 used offset 15517 while its form length was 13041, so the defined-form slice is empty. For seed 249804021, GENOLE S901 offset 1522 exceeded its form length; the first OLEPIN failure occurred before any valid manifest row could be judged. The counter's own failure reasons above are the authoritative per-leg evidence.

Best demonstrated score: this forge reached 0/4 on all three required runs. The prior `R55CritForgeEcho.md` lines 66–72 records a distinct refusal-only attempt at 1/4; its lines 75–83 disclose the surrogate-generation defect and define that as the only demonstrated success. Thus best LEGS reached by the tested non-reading attempts is 1/4, refusal-only, not this surrogate forge. No evidence supports a claim that a non-reading forge reaches any positive leg.

Scratch was confined to `/fast/scratch/hyaku/chousa-r56/R55W2CritForgeNonReader`; no lane or campaign files besides this report were written. Scratch was removed after recording these receipts.

VERDICT: attacked round-55 C1 with a genuine non-reading surrogate; it scored 0/4 in seed 7 and both unseeded runs, and the best previously demonstrated non-reading attempt remains 1/4 (refusal-only).