# R59Scout29 — bounded offline data walk

## Observed

- The frozen-claims path named by lane context, `corpus/evidence/round59/claims.md`, is absent from the current lane tree (`read` returned not found; `corpus/evidence/round59/` lists only `census-start.txt` and `controls/c1-before.txt`). I did not infer claim predicates, source pins, or acceptance conditions from other artifacts.
- `corpus/evidence/round59/census-start.txt` records validator `exit=0` and five W04 duplicate-URL warnings: S051, S053, S073, S074, S075. `corpus/SOURCES.md` confirms distinct scopes can share a URL; S074 is explicitly rejected as a duplicate of S059's `hashlib` scope, whereas S073 corrects S070's anchor and S075 is a different local-manual scope. Thus URL reuse warnings alone do not establish duplicated or invalid source evidence.
- `corpus/evidence/round59/controls/c1-before.txt` records `OK=4/4 REFUSE=0/7`, `DENIED=0/0`, `C1=FAIL`, `EXIT=1`. Several purported refusal cases instead returned `rc=0` (FOREIGN, SYMLINK_OUT, SYMLINK_CACHE, MANY_QUOTES); FOREIGN was deleted and SYMLINK_OUT wrote to its target directory. Other cases refused but failed their expected diagnostic checks (FIFO_TXT, DEVZERO_TXT, FAT_RAW). These are literal before-capture observations, not a final round verdict.
- `corpus/lessons/round-58.md` identifies the prior positive-verdict-path defect: C1's frozen counter could not represent its positive state, printing `REFUSE=0/7` even when a scratch build reportedly passed all 11 safe/refusal legs. The lesson says to leave frozen bytes unchanged and classify C1 unprovable, and records criterion 115 as the prospective requirement for a positive control reaching the declared final verdict before freeze. The same lesson says the fetch-scope L0 remains open and no live fetch occurred.
- `corpus/SOURCES.md` contains offline source-scope rows, including S051–S056 on HTML boundary/network semantics. In particular S052 bounds socket timeout claims to individual blocking operations, not a total transfer; S053 does not establish DNS pinning. The registry's own scope disclaimers matter: these are relevant prior source records, not evidence of a current fetch or round59 claim.

## Inference (bounded)

The current before-capture independently exhibits why positive-path calibration matters: zero refusal denominator makes `DENIED=0/0` non-informative, and the listed success outcomes plus side effects contradict expected refusal for those fixtures. It does not by itself identify whether failures lie in builder, verifier/counter, or fixture/harness interpretation. The five census warnings are a pre-existing census condition, not a substitute for source-scope adjudication.

## Unresolved

No claims body was available at the specified frozen path, and no after-capture/final round59 counter was established in this walk; therefore claim-level alignment and any repair outcome remain unverified here. The open L0 fetch-scope ruling prevents turning these offline notes into authority for live retrieval. No external fetch was attempted.

## Provenance

Read lane-local files only: `corpus/evidence/round59/census-start.txt`, `corpus/evidence/round59/controls/c1-before.txt`, `corpus/SOURCES.md`, `corpus/lessons/round-58.md`, and `.ufo/waves/round-59/w1-spec.json` (milestone/axis context). No source repo was changed; no tools were installed. Confidence high for the quoted local artifact contents; causal attribution and alignment to absent frozen claims are unresolved.
