# R1 probe matrix — ExecSlenProbe (round 35, w2)

Access date for every quote below: 2026-10-23. Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
All production files were read-only; every experiment ran under `/tmp/hyaku/chousa-r35/w2/ExecSlenProbe/`.
No git/jj write command was issued; no subagent was spawned.

## Pinned gates (sha256, re-derived)

| gate | path | sha256 |
|---|---|---|
| landed | `tools/research-gate.sh` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` |
| base | `.ufo/waves/round-35/repairs/base-gate.sh` | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` |
| probe under test | `.ufo/waves/round-35/repairs/slen-probe.sh` | `0938c4c21e9b4e311a6786204f954a6a7351e861c3597db665db0ce47988ce60` |

Both match the sha256 the round-35 context names. Command:
`cd chousa-shokunin && sha256sum tools/research-gate.sh .ufo/waves/round-35/repairs/base-gate.sh .ufo/waves/round-35/repairs/slen-probe.sh`.

## 1. Committed probe, as assigned

```
bash .ufo/waves/round-35/repairs/slen-probe.sh .ufo/waves/round-35/repairs/base-gate.sh
  -> SLEN_PROBE offsets=0 first=            exit 1        (expected 0 / 1)
bash .ufo/waves/round-35/repairs/slen-probe.sh tools/research-gate.sh
  -> SLEN_PROBE offsets=1 first=5           exit 0        (expected 1 / 0)
```

Both expectations hold. The probe's two calls are reproducible and the exit codes carry the verdict.

**The repair site.** Base `.ufo/waves/round-35/repairs/base-gate.sh:1632`:
`local hay=$1 span=$2 slen=${#span} chunk pattern occurrence offset resume=0`.
Landed `tools/research-gate.sh:1701` splits it, then `:1706-1707`:
`local slen` / `slen=${#span}`. Because bash expands every right-hand side of a `local`
command before performing any of its assignments, the base form reads `${#span}` from the
*caller's* dynamically visible `span`; the landed form reads it after `span=$2` has been
assigned, i.e. from the parameter.

## 2. Extended matrix (the assigned three cases, plus controls)

Probe: `ext-slen-probe.sh` (my artifact). Extraction is byte-identical to the committed
probe (`sed -n '/^tok_hex_pattern()/,/^}/p'` + `sed -n '/^TOK_DIRECT_SPAN_MAX=/,/^token_matcher_require()/p' | sed '$d'`),
then each case runs in a fresh subshell so `span` visibility is exactly what the row says.
Input in every row: `hay="lead <S> tail"`, `<S>` = 32766 bytes (`printf 'w%04d ' {1..5461}`,
the dead zone), passed as `$2` to `tok_span_offsets_chunk`.

| case | caller-visible `span` | nounset | base offsets / first / rc | landed offsets / first / rc |
|---|---|---|---|---|
| **a** | none (unset) | `set -u` | **0** / – / **rc=1** + `span: unbound variable` | **1** / 5 / 0 |
| **a** | none (unset) | `set +u` | **0** / – / 0 | **1** / 5 / 0 |
| **b** | 1 byte | `set -u` | **0** / – / 0 | **1** / 5 / 0 |
| **b** | 1 byte | `set +u` | **0** / – / 0 | **1** / 5 / 0 |
| **c** | 30000 bytes | `set -u` | **0** / – / 0 | **1** / 5 / 0 |
| **c** | 30000 bytes | `set +u` | **0** / – / 0 | **1** / 5 / 0 |
| d | 32766 bytes, other content | `set -u` | **1** / 5 / 0 | **1** / 5 / 0 |
| e | == the argument (real path) | `set -u` | **1** / 5 / 0 | **1** / 5 / 0 |
| f | 29-byte decoy (committed probe's) | `set -u` | **0** / – / 0 | **1** / 5 / 0 |
| g | `tok_span_offsets` (real call path), visible span none / arg | `set -u`, `set +u` | **1** / 5 / 0 | **1** / 5 / 0 |

Raw TSV: `base.tsv`, `landed.tsv` (in this directory). **The assigned expectation is met
exactly: base 0 offsets in all three of (a)(b)(c), landed 1 offset at 5 in all three.**
The landed gate emits the same answer at 14 distinct visible-span states; the base emits
`0` everywhere except when the visible length is exactly right.

## 3. Attacks on the repair and on the probe

### F1 — the committed probe does not discriminate the repair from two cheats (probe-strength note, not a claim violation)

Four scratch mutants of the landed gate (`mutant-receipt.txt`; full files in
`/tmp/hyaku/chousa-r35/w2/ExecSlenProbe/mutants/`), scored with the committed
`slen-probe.sh` and with the gate's own `--selftest`:

| mutant | committed probe | gate `--selftest` |
|---|---|---|
| `slen=32766` (hardcoded length) | `offsets=1 first=5` rc=0 → **passes** | FAIL (3/256) |
| confirmation line `[[ ${hay:offset:slen} == "$span" ]] \|\| continue` deleted | `offsets=1 first=5` rc=0 → **passes** | FAIL (4/256) |
| `slen=${#2}` | `offsets=1 first=5` rc=0 → **passes** | FAIL (2/256) |
| `slen=${#1}` (hay length) | `offsets=0` rc=1 → fails | FAIL (5/256) |

So "the probe prints offsets=1" is **not** evidence that `slen` is read from the parameter:
a hardcoded literal and a deleted confirmation also print it. What actually separates them
is `research-gate.sh --selftest`. This is consistent with `claims.md` classifying R1 as a
repair with "no direction-of-improvement measured", but a future round that upgrades R1 to a
claim must not use this probe alone as the counter.

### F2 — the base's latent defect is length-only and fail-closed

Sweep over visible `span` lengths (`slen-sweep.sh`, `sweep-base.tsv`, `sweep-landed.tsv`),
offsets reported by the chunk matcher:

```
vislen   0 1 2 100 4096 16384 32763 32764 32765 32766 32767 32768 40000
base     0 0 0  0    0    0     0     0     0     1     0     0     0
landed   1 1 1  1    1    1     1     1     1     1     1     1     1
```

The base reports offsets **iff** the caller-visible length equals `len($2)` = 32766. The
visible span's *content* is irrelevant (row `d`). The base therefore under-reports; it never
emits a wrong offset, because `[[ ${hay:offset:slen} == "$span" ]]` compares a slice of
length `slen` against `$span` and `$span` inside the function is correctly `$2`.

This sharpens `claims.md`'s "no measured behaviour changes today": the base's real call path
is unaffected because `tok_span_offsets` declares `local hay=$1 span=$2` on a *separate*
statement (base `:1598`) and forwards that same value, so `slen == len($2)` there. Verified
at function level: row `g` gives `5` for base (and `5,32776` on a double-occurrence hay —
`multi.tsv`) exactly as landed does.

### F3 — under the gate's own `set -u`, case (a) is a hard error on the base, not a 0

The gate sets `set -euo pipefail` (`tools/research-gate.sh:292`, base `:292`). With no
caller-visible `span`, the base's single-statement `local` expands `${#span}` on an unbound
name: stderr `span: unbound variable`, function abort, rc=1 (row `a`, nounset=1). The landed
gate returns 1 offset, rc=0. Unreachable through the real call path (always a visible
`span`), so still latent — but the failure mode is an abort, not a silent wrong answer.

### F4 — the base gate's own selftest does not catch this bug

The base blob run **in place** reports `RESEARCH_GATE_SELFTEST: FAIL (2/256 cases)`
(`base-selftest.log`), on `claims-lane-fallback` and `ptr-lane-abs`. That is a **location
artifact, not a defect**: the lane root is derived from the script's directory, so the blob
in `repairs/` looks for `.ufo/waves/round-35/PROVINCE.md` (observed in the log's
`ptr=...` line). Control: the same bytes at `lanesim/tools/research-gate.sh` with `PROVINCE.md`
beside it → `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`, exit 0.
**Consequence for the audit:** anyone who executes the base blob where it sits will see a
spurious 2-case failure and could misread it as a round-34 regression. And the base passes
256/256 *while carrying the `slen` bug* — the round-34 selftest is blind to it; only the
probe demonstrates the repair.

### F5 — R2 numbering verified, with one undocumented half

`base-gate.sh:7824` says "cases 252-254" and `:7857` says "cases 255-257"; landed
`tools/research-gate.sh:7899` says "cases 252-253" and `:7932` says "cases 254-256".
Case counting confirms the landed text: `tclaims` increments `cases` once per call
(`tools/research-gate.sh:4220`), the C1 block holds 2 `tclaims` calls and the C2 block holds
3, and landed selftest ends at case 256 PASS — so C1 = 252-253 and C2 = 254-256. The case
*bodies* of the two blocks are byte-identical between gates; only comment numbers changed.
`claims.md` R2 describes only the `255-257 → 254-256` half; the `252-254 → 252-253` half was
also changed and is undescribed there. Comment-only, no behavioural effect. [INFERENCE on
"undescribed": I compared the R2 text against both gates, not against any r34 erratum.]

### F6 — residual-hazard scan of the same class

`scope-scan.py` reports `local` statements where one declared variable's initializer
references a sibling declared in the same statement. Result: base → exactly one hit,
`:1632` (`slen` reads sibling `span`); landed → **none**. The scanner is validated by that
base hit, i.e. it is not silently returning empty. Every other `local a=$1 b=...` in both
gates declares no sibling reference (e.g. landed `:679 local line body=${SEC_BODY[$sec]-}`
is safe because `sec` is assigned by the preceding statement `:675`).

## 4. Verdict on this item

- Committed probe: base `offsets=0` exit 1, landed `offsets=1 first=5` exit 0 — as expected.
- Extended matrix: **(a) no visible span → base 0 / landed 1; (b) 1-byte visible span →
  base 0 / landed 1; (c) 30000-byte visible span → base 0 / landed 1.** Target met.
- No MEETS finding against the R1 repair: the landed gate is insensitive to caller-scope
  `span` in all 14 measured states, in both nounset modes, at function level and on the real
  call path. The repair is real and complete for this class.
- The one probe-strength MEETS-adjacent result is **F1**: a hardcoded `slen=32766` and a
  deleted confirmation both satisfy the committed probe. They die on `--selftest`, so the
  gate is not weakened, but the probe alone is not a counter.

## 5. Limits

- All measurements except the `--selftest` runs are **function-level**: the probe sources
  the extracted matcher block, it does not execute a gate verdict. Rows `g` and `multi.tsv`
  exercise the real `tok_span_offsets` wrapper, still with the extracted block.
- The extraction stops at `token_matcher_require()`, so it does **not** include the landed
  gate's `grep() { command "$GREP_BIN" "$@"; }` wrapper (`tools/research-gate.sh:351`).
  The probe therefore runs `/usr/bin/grep` from `PATH=/usr/bin:/bin`, not the pinned
  `GREP_BIN`. That is orthogonal to `slen` (C1's subject, not R1's) but means no row here
  measures grep provenance.
- Mutants are scratch copies under `/tmp`; no production file, counter, witness tool or jj
  state was written. `lanesim/` is a scratch tree holding a copy of the base blob plus
  `PROVINCE.md`.
- Rows `d`, `f`, `g` and the 13-point sweep are additions beyond the assigned matrix; the
  assigned three cases are `a`, `b`, `c`.

## 6. Artifacts (this directory, each < 1 MiB)

```
ext-slen-probe.sh      a8dd739bb35e6d1b7cb8106855655f311b20991a6925896bed8093627cc0da22
scope-scan.py          262ed9838feba49d8055be1fa740521be26d22e3c9488b2c1a9b772e84d57d25
slen-sweep.sh          c635c70d499e74d4edaa1fcc1b6195334ea9152be038f9b58d7bfecb09efc828
multi-occurrence.sh    36b8aa43c6e906772c6d017c97ea39a149753498bd461a8dafc04a9a39b96724
base.tsv               aa048cc6ac156578a086491d9e703954141070d6a4323d3bf2f24510b76a2a84
landed.tsv             3e8ae1ff6a33218556d0e5458b8cb210c1c9f482e9067aabc09ae2a1973407f5
sweep-base.tsv         92bd204904d39a8bad6e31dae854a4ded4c514d51ecc9bb273bcdc4fd5ece56c
sweep-landed.tsv       2cdb1186b303a33482ddc408ff6ad29a08267a86e3b08bb2ba027352bfe5a5ea
multi.tsv              8cbf14fc19a26ba99f207792f70776727b0d04438a3567c51dee25de148548c0
base-selftest.log      38b179e8a1dee59780ed5a18e58187929a0cabfc5430ba284f9fbc6979565361
landed-selftest.log    5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12
mutant-receipt.txt     4b5318af1d885434bac5e83be48a3e5d628537649869c5d52078eb92158e0d11
```

Mutant gate files (371 KB each) stay in `/tmp/hyaku/chousa-r35/w2/ExecSlenProbe/mutants/`
with the sha256 recorded in `mutant-receipt.txt`.

## 7. Tool installs

None. No package manager was invoked (`pacman` transactions are paused host-wide per the
tooling directive); every tool used (`bash`, `grep`, `sed`, `awk`, `od`, `tr`, `python3`)
was already present.
