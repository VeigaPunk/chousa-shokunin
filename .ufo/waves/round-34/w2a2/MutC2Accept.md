# MutC2Accept — C2 accept-dead-zone controls (a)–(d)

Seat: mutation-tester, chousa lane round 34 attempt 2, wave 2 (w2a2). Access 2026-10-23.
Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` read-only; every experiment under
`/fast/scratch/hyaku/chousa-r34-a2/w2/chousa-r34-w2a2-MutC2Accept-7/`. Artifacts (gates,
patches, receipts, logs, probe, manifest): `.ufo/waves/round-34/w2a2/MutC2Accept/`.

## Pins (verified, before and after the runs)

- `sha256sum tools/research-gate.sh` = `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`
  (frozen blob; identical at `707da81` and at lane HEAD `fe3db76` via `git show <c>:tools/research-gate.sh | sha256sum`).
- Lane HEAD is `fe3db76`, one commit past the frozen tip `707da818`; `git show --stat fe3db76`
  touches only the three `.ufo/waves/round-34/w2a2-*.json` files (24+/24−), and the gate/counter
  blobs are byte-identical at both commits — the frozen production bytes are what was scored.
- Counter `corpus/evidence/round34/c2-count.py` = `8c0def4d377cdf1a1e4bd2c9151bb0846216658ff14d725d15ac037c12212173`,
  used unmodified; every receipt carries `counter_sha256=8c0def4d…`.
- Pre-fix gate `git show bf7c931a:tools/research-gate.sh` = `772a1d8e4d94dbf3a44a64bf850b1324e51546eeb62abcd7b3ec585f0e003e58`.
- After all work: `git status --porcelain --untracked-files=no` empty; gate still `a6307edf…`.

## Controls built (each a minimal patch of the landed gate; `bash -n` OK; diffs in `patch-*.diff`)

| id | sha256 | change | semantics |
|---|---|---|---|
| A | `5472501a8701be1b21780765a2304c5fcdc19331c8ff2f7482780d32aa778093` | `tok_span_at` returns `line:1` rc0 for `${#span} >= 32765`; `tok_span_all` prints `1 1`; no haystack search | every dead-zone span supported |
| B | `7dcc7318d0159f86f1d73f066aad14b440e7d64ee55638e156f520b1ba7fb8cf` | chunk `= ${span:0:64}`; whole-span confirmation `[[ ${hay:offset:slen} == "$span" ]]` deleted; boundary test skipped for such spans | supported iff the first 64 bytes occur anywhere |
| C | `ef90b5788f3edec6b4daba306db6f1d61dc79771a885b019ab80082941e5abeb` | chunk `= ${span%%$'\n'*}`; confirmation deleted; boundary test skipped | supported iff the first line occurs |
| D | `3e26dfba5bc7de35e88f75822bdc1c937057523011240e7a4d5336f8531e4d39` | A's no-search accept plus `verify_claims` binding by `line_m−line_n+1 == count_nl(span)+1` | (a) + line binding by line-count arithmetic only |

## Scores (frozen counter, two fresh seeds each, receipts in `MutC2Accept/receipts/`)

Command (cwd = lane root): `C2_TMP=<scratch> python3 corpus/evidence/round34/c2-count.py --gate <control> --seed N --receipt <artifact>/<id>-sN.json`.
Counter exit 1 = predicate not met; 0 = holds. Max elapsed 58.9 s (bound 1500 s); no timeouts.

| run | gate | seed | label | counter rc | predicate_holds |
|---|---|---|---|---|---|
| baseline | landed `a6307edf` | 6101 | `DEADZONE_MATCH=37/37` | 0 | true |
| baseline | landed `a6307edf` | 6131 | `DEADZONE_MATCH=37/37` | 0 | true |
| A | `5472501a` | 6103 | `18/37` | 1 | false |
| A | `5472501a` | 6107 | `18/37` | 1 | false |
| B | `7dcc7318` | 6109 | `20/37` | 1 | false |
| B | `7dcc7318` | 6113 | `20/37` | 1 | false |
| C | `ef90b578` | 6117 | `17/37` | 1 | false |
| C | `ef90b578` | 6119 | `18/37` | 1 | false |
| D | `3e26dfba` | 6121 | `16/37` | 1 | false |
| D | `3e26dfba` | 6123 | `16/37` | 1 | false |

**Verdicts: A MISSES (18/37), B MISSES (20/37), C MISSES (17–18/37), D MISSES (16/37).**
All four are killed by the frozen counter; none reaches 37/37, so the "counter let it
through" branch does not fire. Nearest is B, 17 records short.

### Per-class lines (representative seed; second seed identical except where noted)

A (6103 = 6107): verbatim-ml 3/3 · verbatim-1l 2/2 · edge 2/2 · mut-head 0/2 · mut-tail 0/2 ·
mut-center 0/2 · decoys 0/5 · decoys-exact 2/2 · decoys-line-wrong 2/2 · split 0/2 ·
glued-left 0/2 · glued-right 0/2 · glued-then-valid 1/1 · line-bound 0/2 · line-wrong 2/2 ·
short-verbatim 2/2 · short-mut 2/2 = 18.

B (6109 = 6113): 3/3 · 2/2 · 2/2 · mut-head 2/2 · mut-tail 0/2 · mut-center 0/2 · decoys 0/5 ·
decoys-exact 2/2 · decoys-line-wrong 0/2 · split 0/2 · glued-left 0/2 · glued-right 0/2 ·
glued-then-valid 1/1 · line-bound 2/2 · line-wrong 2/2 · short 4/4 = 20.

C (6117; 6119 differs only mut-head 2/2): 3/3 · verbatim-1l **0/2** · edge 2/2 · mut-head 1/2 ·
mut-tail 0/2 · mut-center 0/2 · decoys 0/5 · decoys-exact 2/2 · decoys-line-wrong 0/2 ·
split 0/2 · glued 0/4 · glued-then-valid 1/1 · line-bound 2/2 · line-wrong 2/2 · short 4/4 = 17 (18 on 6119).

D (6121 = 6123): 3/3 · 2/2 · 2/2 · mut 0/6 · decoys 0/5 · decoys-exact 2/2 ·
decoys-line-wrong 0/2 · split 0/2 · glued 0/4 · glued-then-valid 1/1 · line-bound 2/2 ·
line-wrong **0/2** · short 4/4 = 16.

### Why each is killed (class arithmetic matches the receipts exactly)

Fixture composition (`c2-count.py:71-90`, confirmed by `--keep`): 33 in-window long records
(12 truth=supported, 17 truth=unsupported, 4 truth=mislocated) + 4 short.
- **A** (18): the 17 unsupported flip to supported, and `dz-line-bound` (2) flips to
  mislocated because the phantom `line:1` can never equal the named second-occurrence range
  (`MISS … dz-line-bound truth=supported observed=mislocated`). It keeps the 4 mislocated
  records (a phantom `TOK_AT=line:1` cannot bind) and the 4 short ones.
- **B** (20): loses mut-tail 2 + mut-center 2 (first 64 bytes intact), decoys 5 (a decoy
  leaves the prefix), split 2 (prefix occurs in the first half; boundary test removed),
  glued 4, decoys-line-wrong 2. Keeps mut-head 2 (prefix mutated) and line-bound 2 (real
  offsets feed the line arithmetic).
- **C** (17–18): additionally loses `dz-verbatim-1l` 2 — a single-line span's "first line"
  is the whole span, so the 4N-byte pattern still exceeds PCRE2 and grep fails
  (`gate_stderr_tail` in both C receipts holds exactly two `grep: regular expression is too large` lines).
- **D** (16): 17 unsupported flip to supported, and both line-wrong classes (4) bind because
  every generated named range has the span's line width; `dz-line-bound` is right.

## Independent re-derivation of C2's premise (detector outside the counter)

`probe-boundary.py` builds four sources, each holding one delimited span of exactly
32764/32765/32766/32767 bytes, `expect=supported`:
- pre-fix gate `772a1d8e`: `len32764 supported`; `len32765/6/7 observed=unsupported`,
  three `grep: regular expression is too large` lines, `RESEARCH_GATE: DRIFT`, exit 1.
- landed gate `a6307edf`: all four `observed=supported`, `VERDICT_BEARING_CLAIMS=4/4`,
  `RESEARCH_GATE: CLEAN`, exit 0.

So the three-length dead zone and its closure reproduce on hash-pinned bytes with a fixture
that is not the frozen counter's.

## Counter fixture audit (`--keep`, seed 6131, `run/keep-s6131/`)

- 37 records, 17 classes; all 28 non-decoy `dz-` spans inside 32765..32767
  (histogram 32765×6, 32766×8, 32767×14), `dz-decoys` 5 more also in-window.
- `dz-edge` lengths {32765, 32767}; `dz-verbatim-1l` both 32767 here (the edge class draws
  per record, `c2-count.py:194`, so the pair is seed-dependent — the claim's parenthetical
  is one draw, not a guarantee).
- `dz-decoys`: 0 exact copies of the record span, 12 copies share a 40-byte prefix (truth
  `unsupported` holds). `dz-line-bound`: 2 occurrences, named range = second occurrence
  (710–1378). `dz-decoys-line-wrong`: the exact span occurs once; the named range 5232–5863
  belongs to a decoy.

## Claim-record finding (calibration; does not touch P2, the kill rule or the counter)

`corpus/evidence/round34/claims-a2.md:100-103` predicts the do-nothing control as
"The 17 long-supported records (3+2+2+2+2+1…)" and "Expected ceiling 4/37". Both are wrong
against the claim's own committed measurement: the counter's truth table has **12**
long-supported, **17** long-unsupported, **4** long-mislocated (and the listed sum
3+2+2+2+2+1 = 12), while `measure-a2/c2-before-s5011.json` / `-s5023.json` record
`DEADZONE_MATCH=21/37` (per_class: dz-decoys 5/5, dz-mut-head/tail/center 2/2 each,
dz-split 2/2, dz-glued-left/right 2/2, short 4/4 — i.e. 17 unsupported-truth + 4 short).
The base gate passes those 17 by absence, so the real ceiling is 21, not 4; SCORECARD.md:1956
already reports 21/37, but no erratum corrects the frozen claim text. Record-level defect only:
the after-state (37/37 on two fresh seeds 6101/6131) and the kill rule are unaffected.

## Limits

- One reading per control, taken literally ("supported iff … occurs somewhere", so B/C skip
  boundary tests); a boundary-keeping variant of B would score higher but still cannot reach
  37/37 because mut-tail/mut-center/decoys/split/decoys-line-wrong do not depend on boundaries
  [INFERENCE, not run].
- No network, no lane/git/jj writes, no signals; scratch retained with receipts; largest
  artifact 368,420 bytes (<1 MiB each).
