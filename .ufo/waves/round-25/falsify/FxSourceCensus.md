# FxSourceCensus — round 25 falsify

## Observed
- Private clone started at `0fc037e6b07f3820ead8c9207a8034ac854197a`; fetched/switched to full integration `e93ac711f885a10d44fdd80a1734997419595b5a`. Live lane `HEAD` also observed as e93 (`git rev-parse HEAD`).
- Frozen `corpus/evidence/round25-sources-census.sh`, run against the complete d730ae4 base archive (not a SOURCES-only extraction), returned:
```text
rows=18
malformed=0
tiers=A=14 B=1 C=3 
status=mined=8 queued=7 rejected=3 
duplicates=[]
enum=[]
missing-used-by=[]
baseline_full_manual_exit=0
```
- Same frozen script run in the full e93 clone returned:
```text
rows=28
malformed=0
tiers=A=22 B=1 C=5 
status=mined=10 queued=14 rejected=4 
duplicates=[]
enum=[]
missing-used-by=[]
manual_exit=0
```
- Histogram deltas: tier A +8, B +0, C +2; mined +2, queued +7, rejected +1. Totals reconcile to 18→28. Round-25 lesson records the same additions at `corpus/lessons/round-25.md:86-90`.
- Maintained read-only validation, run after the manual census: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` →
```text
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
maintained_exit=0
```
- Gate quote coverage: `corpus/lessons/round-25.md:61-64` states access date **2026-10-21** for the new-row quote table; table rows `:68-77` list all S019–S028. Matching registry rows `corpus/SOURCES.md:29-38` each have opened date `2026-10-21`. The date is a shared table-level annotation, not repeated on each quote row.
- `git diff --quiet 0fc037e6b07f3820ead8c9207a8034ac854197a e93ac711f885a10d44fdd80a1734997419595b5a -- corpus/SOURCES.md corpus/evidence/round25-sources-census.sh` returned `source_and_census_diff_exit=0`; the source-only result is unchanged across these pins.

## Checkpoint corrections retained
- The 0fc→d8 diff contains `M tools/research-gate.sh` and `M SHONEN.md`: the first package omitted the updated metadata gate (L1 correction; diff observed in the private clone). Use d8/e93, not 0fc, for gate claims.
- The d8→e93 diff contains `M corpus/evidence/README.md` (among other integration files): the intermediate d8 package also omitted the evidence-index update. Full C2/index checkpoint is e93, as corrected by L1.

## Assessment and limits
- High confidence: both complete-tree census populations and maintained CLI pass; no duplicate IDs, malformed counted rows, enum violations, or missing mined `used-by` targets were reported by the frozen checks. The documented 10 additions reconcile exactly with the measured histogram deltas.
- High confidence, documentation-only: all ten quote IDs are enumerated under the shared 2026-10-21 access-date statement. This verifies the Gate documentation/registry date, not independent external access or quote truth; no pages were re-opened for this census task.
- A preliminary baseline run against a SOURCES-only scratch directory produced false missing-path lines because its referenced knowledge files were absent; it was discarded and rerun against the complete d730ae4 archive above. No production file was changed.
- Installs: none.

VERDICT: No SOURCES census defect found at the full e93 checkpoint; the source histograms reconcile and all ten documented Gate quotes carry the shared access date.