# ExecNoHarmBase34 — round-34 W1 no-harm baseline on the base gate

Seat `ChousaR34.ExecNoHarmBase34`, WAVE 1 (pre-freeze adversarial controls). Lane
`/home/vgpnk/Projects/shokunin/chousa-shokunin`, branch `master`, lane revision
`70feb5eacc959eb98071461fe89f0b892c0810d8` (verified before and after the run; the branch did not
move during the measurement). Measured gate `tools/research-gate.sh`, SHA-256
`43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346` — the round-34 base named by
the assignment (prefix `43a1af35ca668fe5`).

No candidate gate was built, patched or scored by this seat. The round-34 counter
`corpus/evidence/round34/c1-count.py` (the C1 long-span counter, `LONGSPAN_MATCH`) was **not
invoked at all**, and neither was `corpus/evidence/round33/c1-count.py`; the round-34 control rule
("no seat in this wave runs c1-count.py against a candidate implementation of C1"; the L1 commits
the control receipts first and scores candidates afterwards) is observed — no run of that counter
against the landed base gate exists, so no "lower run on the landed gate" was created.

## Deliverable

`.ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh` (mode 0755, 10760 bytes before adaptation →
SHA-256 `f1a1591c55bb6dad8c3e138c4158caf4fd62fda575643fd09320713904a5eeef`), copied verbatim from
`.ufo/waves/round-33/w1/ExecNoHarmBase33/battery.sh` and adapted only in paths, round labels, the
seed set and the counter list. The D3 revision-bound header was kept intact (lane revision, gate
path + sha256, gate tree revision, every counter path + sha256, fixture hashes, battery-script
hash, utc, hostname, scratch, seeds).

Adaptations, verbatim diff summary:

- header comment: "round-33 W1 no-harm battery" → "round-34 W1 no-harm battery"; base gate sha256 in
  the usage comment updated to `43a1af35…`; the control-rule paragraph names the round-34 counter.
- `SCRATCH` default → `/fast/scratch/hyaku/chousa-r34/w1/ExecNoHarmBase34`.
- seeds: one fresh seed per counter row, `3801` (round-31 c1-count-v3), `3802` (round-31
  c2-count-v3), `3803` (round-32 c2-count-v2), `3804` (round-33 c1-count-v2), `3805` (round-32
  c2-count-v3). Round-33 ran two seeds per counter; round-34 runs one, per the assignment ("each
  on one fresh seed"). The 3801-3805 band is unused in rounds 33/34 and outside the reserved
  3401-3409 band.
- counters added to the header hash list and to the rows: `corpus/evidence/round33/c1-count-v2.py`
  (`TOPLEVEL_FIELD_MATCH`, TOTAL 156) and `corpus/evidence/round32/c2-count-v3.py`
  (metadata-decoupled `EXEMPT_AUDIT_MATCH`, TOTAL 132). `P_CNT` extended with
  `^TOPLEVEL_FIELD_MATCH=|^COUNTER `.
- row names dropped the `-a`/`-b` suffixes; each counter row now asserts one seed and one receipt.

Everything else (the `row`/`has`/`receipt` helpers, the timeouts, the claims-lane-root base
fingerprint row, the awk-extracted round-1 observable, the exit-code expectations) is unchanged.

### Machine-diffable baseline

`.ufo/waves/round-34/w1/ExecNoHarmBase34/base-baseline.txt` (2256 bytes, SHA-256
`844cc3e110b961daca2058776af5439a7a1a0253607095f6a764a5b7b0f4f0da`) lists every expected value
from this base run in `row<TAB>value` form, plus the counter/fixture hashes and the seeds. The
L1's candidate-side transcript must reproduce every line; `gate_sha256` and `battery_script` sha256
are expected to differ on the candidate side by design.

## Base run (one retained invocation)

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
bash .ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh \
  "$PWD/tools/research-gate.sh" \
  "$PWD/.ufo/waves/round-34/w1/ExecNoHarmBase34" \
  > .ufo/waves/round-34/w1/ExecNoHarmBase34/battery-base.out 2>&1
```

exit **0**, `ROWS=11`, `BATTERY_RESULT=PASS`. Transcript `battery-base.out`, SHA-256
`3f72230737c9d9aa856aceb05eff2e94c1edc3fa3828dcf798382f4459fbf3bd` (wall 266 s).

Header (verbatim from the transcript, lines 1-18):

```
# round-34 W1 no-harm battery (D3 revision-bound header)
lane=/home/vgpnk/Projects/shokunin/chousa-shokunin
lane_revision=70feb5eacc959eb98071461fe89f0b892c0810d8
gate=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
gate_sha256=43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346
gate_tree_revision=70feb5eacc959eb98071461fe89f0b892c0810d8
battery_script=…/ExecNoHarmBase34/battery.sh sha256=f1a1591c55bb6dad8c3e138c4158caf4fd62fda575643fd09320713904a5eeef
utc=2026-10-23T11:04:00Z
hostname=plazir27
scratch=/fast/scratch/hyaku/chousa-r34/w1/ExecNoHarmBase34
seeds=r31-c1-v3:3801 r31-c2-v3:3802 r32-c2-v2:3803 r33-c1-v2:3804 r32-c2-v3:3805
```

Counter hashes in the header: round-31 c1-count-v3 `0efbd172…`, round-31 c2-count-v3 `654183e1…`,
round-32 c2-count-v2 `8ec1a1ed…`, round-33 c1-count-v2 `cb354dd1…`, round-32 c2-count-v3
`6f362ece…` (full values in `base-baseline.txt`). Fixture hashes: claims-r2 `23d078cb…`,
chain-r3 `06115f2f…`, chain-r3-broken `b66222a1…`.

## Rows on the base gate

| run | command (cwd = lane root) | exit (want) | wall ms | key output | log sha256 |
|---|---|---:|---:|---|---|
| selftest | `bash tools/research-gate.sh --selftest` | 0 (0) | 149395 | `RESEARCH_GATE_SELFTEST: PASS (251 cases, 0 skipped)`; 0 `FAIL-case` | `acf0564a…` |
| claims-lane-root | `verify-claims corpus/fixtures/claims-r2.jsonl --root .` | 1 (1) | 945 | `VERDICT_BEARING_CLAIMS=0/17`; `DRIFT (claims=17 … refused=17 … drift=17)` | `3650a659…` |
| claims-fleet-root | `verify-claims corpus/fixtures/claims-r2.jsonl --root /home/vgpnk/Projects/shokunin` | 0 (0) | 1733 | `VERDICT_BEARING_CLAIMS=17/17`; `CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 …)` | `55d0ed38…` |
| chain-r3 | `verify-chain corpus/fixtures/chain-r3.md --root <fleet>` | 0 (0) | 6096 | `RESOLVED_HOPS=17/22`; `CLEAN (hops=22 verified=17 exempt=5 …)` | `259a0f6e…` |
| chain-r3-broken | `verify-chain corpus/fixtures/chain-r3-broken.md --root <fleet>` | 1 (1) | 929 | `RESOLVED_HOPS=1/2`; `DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 …)` | `f925e10d…` |
| observable | awk-extracted `## Planned` bash block from `SCORECARD.md` | 0 (0) | 299 | `VERDICT_BEARING_EXPORTS=3/3` | `2ae02592…` |
| r31-c1-v3 | `c1-count-v3.py --gate … --seed 3801 --receipt …` | 0 (0) | 13359 | `LINE_BINDING_MATCH=132/132` | `2406fc73…` |
| r31-c2-v3 | `c2-count-v3.py --gate … --seed 3802 --receipt …` | 0 (0) | 9447 | `REVISION_BINDING_MATCH=132/132` | `d2c70fea…` |
| r32-c2-v2 | `c2-count-v2.py --gate … --seed 3803 --receipt …` | 0 (0) | 31885 | `EXEMPT_AUDIT_MATCH=132/132`; `RECORD_CHECKS=ok` | `91ac37bc…` |
| r33-c1-v2 | `c1-count-v2.py --gate … --seed 3804 --receipt …` | 0 (0) | 13896 | `TOPLEVEL_FIELD_MATCH=156/156` | `1eeb8be8…` |
| r32-c2-v3 | `c2-count-v3.py --gate … --seed 3805 --receipt …` | 0 (0) | 37646 | `COUNTER c2-count-v3 … metadata_decoupled: true`; `EXEMPT_AUDIT_MATCH=132/132`; `RECORD_CHECKS=ok` | `b0c6f0e8…` |

`<fleet>` = `/home/vgpnk/Projects/shokunin`. Every row's `CHECK` line passed and every counter
receipt passed the `receipt()` assertion (`predicate_holds=true`, `matched==total`, empty `misses`,
empty/absent `record_fails`, `gate_timed_out=false`, `gate_sha256=43a1af35…`, `counter_sha256`
equal to the header value).

### Selftest receipt

`selftest.cases` holds the **251** `ok-case` lines (0 `FAIL-case`), SHA-256
`46c9c092ba7d49244ec42e34bea52a8ab10b8d61dcb1a6ea1b72499c12b5f779`
(`selftest.log` SHA-256 `acf0564af458e7a28cae8f66c1a5e87b2647d29b4b6edcc1722747d21a3bf16f`).
Diffed against round-33's base list: the first 241 lines are byte-identical; round-33's own
round-33 top-level cases were appended as lines 242-251 (`r33-top-nested-line` … `r33-post-escapes`),
matching the round-33 final-gate commit note "selftest PASS 251". The base case list therefore
moved 241 → 251 since the round-33 battery ran — a fact the L1 must carry into the candidate
comparison (the candidate must not lose any of the 251 lines).

### Counter receipts (in this directory)

| receipt | schema | seed | matched/total | predicate_holds | misses | record_fails | gate_rc | gate_timed_out | sha256 |
|---|---|---:|---:|---|---:|---|---:|---|---|
| `r31-c1-v3.json` | chousa-r31-c1-receipt/v3 | 3801 | 132/132 | true | 0 | – | 1 | false | `fdf0ca91…` |
| `r31-c2-v3.json` | chousa-r31-c2-receipt/v3 | 3802 | 132/132 | true | 0 | – | 1 | false | `07e860b9…` |
| `r32-c2-v2.json` | chousa-r32-c2-receipt/v2 | 3803 | 132/132 | true | 0 | `[]` | 1 | false | `5bc38c70…` |
| `r33-c1-v2.json` | chousa-r33-c1-receipt/v2 | 3804 | 156/156 | true | 0 | – | 1 | false | `e182c508…` |
| `r32-c2-v3.json` | chousa-r32-c2-receipt/v3 | 3805 | 132/132 | true | 0 | `[]` | 1 | false | `391fffcf…` |

`gate_rc=1` in every receipt is expected, not a failure: those fixtures hold drifting records by
contract (the counters assert their own exit 0 and the receipt fields, not `gate_rc`).

## Verdict

- **No-harm baseline established on base gate `43a1af35…` at lane revision `70feb5eacc…`.**
  All 11 rows matched their expected values (`BATTERY_RESULT=PASS`, exit 0, `ROWS=11`): selftest
  PASS 251 cases / 0 `FAIL-case` (case list `46c9c092…`), claims-r2 17/17 CLEAN (fleet root),
  chain-r3 17/22 CLEAN, chain-r3-broken 1/2 DRIFT, round-1 observable 3/3, round-31 C1 v3 132/132,
  round-31 C2 v3 132/132, round-32 C2 v2 132/132, **round-33 C1 v2 156/156**, **round-32 C2 v3
  132/132** — each on one fresh seed (3801-3805).
- The base side of the no-harm comparison the L1 will repeat on the candidate is now recorded with
  a revision-bound header and a machine-diffable baseline file.

## How L1 reruns on the candidate

```
LANE=<candidate checkout> FLEET=/home/vgpnk/Projects/shokunin \
SCRATCH=/fast/scratch/hyaku/chousa-r34/<seat> \
bash <candidate checkout>/.ufo/waves/round-34/w1/ExecNoHarmBase34/battery.sh \
     <candidate checkout>/tools/research-gate.sh <outdir> > <outdir>/battery-candidate.out 2>&1
```

Use the same `SEED_A..SEED_E` values (3801-3805) so the candidate run is comparable with the base
run row by row. `battery.sh` must be the copy in the candidate checkout (or this one — it is
identical if the L1 cherry-picks it unchanged; its sha256 `f1a1591c…` must appear in the header).
Expect `gate_sha256` and `battery_script` sha256 to differ; every other header line (counters,
fixtures, seeds) and every one of the 11 rows must match `base-baseline.txt`.

## Limits and risks

- Only the base side was measured. No harm criterion is claimed for the candidate; the L1 must run
  the same battery on the candidate and diff against `base-baseline.txt`.
- The claims-lane-root row (exit 1, `0/17`, all 17 claims refused `CLAIM_SOURCE_OUT_OF_CORPUS`) is
  an asserted base fingerprint of the root convention, not a correctness bar: the fixture `source`
  values are fleet-root-relative, so under the lane root they resolve outside the allowed root.
  Round-32 (`ExecNoHarmBase32.md:34-37`) recorded the identical artifact. A candidate that changes
  this row is surfaced by the row mismatch, not silently accepted.
- One fresh seed per counter (assignment) is weaker than round-33's two seeds per counter; a
  single-seed regression in a class that only fires on some draws would not be caught by this
  battery alone.
- The lane branch moved **after** this measurement: `master` is now `ef16afb16c05fb9a4e9a6c5b67cba44bdf3acbdb`
  ("round-34: design v2 before data"), committed by the L1 while this seat was measuring. The
  measured gate bytes are unchanged by that commit — `sha256sum tools/research-gate.sh` still gives
  `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346` at `ef16afb`, and the commit
  touches only `corpus/evidence/round34/c1-count-v2.py` and `corpus/evidence/round34/claims.md`.
  The baseline is therefore bound to the gate hash `43a1af35…`, not to the branch name; the header
  records the revision that was live during the run (`70feb5eacc…`). The L1's candidate run must
  not expect `lane_revision=70feb5eacc…`; it must expect `gate_sha256=43a1af35…` (the candidate
  gate will differ by design).
- The round-34 C1 long-span surface is **not** covered by this battery: it exercises the round-33
  C1 v2 top-level-field counter (156/156), not `LONGSPAN_MATCH`. The base gate's C1 long-span
  behaviour is measured only by the round-34 counter, which this seat must not run against the
  landed gate (no "lower run on the landed gate"), and which the control seats score on CONTROL
  gate copies.
- Selftest wall time on this shared host was 149 s (round-33's base run: 29 s); the 251 case lines
  and their hash are the stable artifact, not the wall time.
- Process hygiene: no process was signalled by name or pattern; the single backgrounded battery
  job (`bg_7566`) completed on its own before this report; nothing was killed. No subagent was
  dispatched.
- Writes: only `.ufo/waves/round-34/w1/ExecNoHarmBase34/` (battery.sh, battery-base.out,
  selftest.log, selftest.cases, five logs, five receipts, base-baseline.txt) and this report. No
  lane production file (`tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`, `SKILL.md`, `README.md`,
  `PROVINCE.md`), no lane jj/Git state, no fleet file was modified; `git status --porcelain` shows
  only untracked wave paths (mine plus `w1/`, `w1-spec.json`, `w1-dispatch.json`,
  `controls/L1-keyed/`, `controls/L1-windows/`, `corpus/evidence/round34/c1-count-v2.py` — the last
  one is not mine). Scratch use: 20 K under `/fast/scratch/hyaku/chousa-r34/w1/ExecNoHarmBase34`;
  this directory 124 K. No installs were made, so no tooling-directive entry is owed.
