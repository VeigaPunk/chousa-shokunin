# RevC2Knowledge — fact-check of dead-zone-pcre-r34.md + C2/C3 re-derivation

Reviewer: chousa-r34-w2a2-RevC2Knowledge-9. Lane tip frozen at
`707da8184a0fc4d10ab3f17271556cdf364f0af5`. All experiments in scratch
`/fast/scratch/hyaku/chousa-r34-a2/w2/RevC2Knowledge/` (clone at frozen tip; `git checkout -q
707da818…`; GIT_* unset). Read-only on lane files; host gate `sha256sum
tools/research-gate.sh` = `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`
(= committed blob `a6307edf…` at `fe0f22e0`, verified via `git show`).

## 1. Numeric-claim trace (dead-zone-pcre-r34.md)

| Claim in knowledge doc | Evidence | Verdict |
|---|---|---|
| 32764-byte span compiles; 32765 fails ("regular expression is too large") | S065 SOURCES row host note (`corpus/SOURCES.md:75`); `w1/ScribeSrcPcre2/evidence.md` lines 39-41 (`largest_compiling_span_bytes=32764 next_failing_span_bytes=32765`); **reproduced today**: pattern files of `\x41` repeats via `/usr/bin/grep -P -f` — 32764 → grep exit 1 compile=OK; 32765/32766/32767 → exit 2 `regular expression is too large` (scratch `boundary/pat-<n>.txt`, sha256 f1117ce0…/5e453de2…) | ✔ traced + reproduced |
| three dead-zone lengths 32765/32766/32767 | selftest cases 254-256 use exactly these: `dz_span`=5461×6=32766 (cases 254/255), `dz_low`=32765, `dz_high`=32767 (case 256) — gate `tools/research-gate.sh:7867-7897`; committed `measure-a2/selftest-a2.log` lines 255-257 + `battery/selftest.cases` | ✔ |
| 'length-only' across five content classes (space-joined words, newline-dense, punctuation-dense, single-byte, escape-dense) | probe `/fast/scratch/hyaku/chousa-r34-a2/probe/` holds the five classes: `root/` (space-joined words, 20 spans 16400..32782 B incl. 32764/32766/32770/32776), `r-nl/`, `r-punct/`, `r-same/` (single-byte 'a'), `r-esc/`; failure mechanism is PCRE compile-ceiling (length-only) and identical for all classes in my direct compile reproduction. Raw 15:35 run stdout is NOT archived — accepted as "scratch probe with its path" per target; see §4 | ✔ (with gap) |
| case numbers 254-256 | committed selftest log + `battery/selftest.cases` lines 254-256 (`claims-deadzone`, `claims-deadzone-line`, `claims-deadzone-edge`); SKILL.md gates table rows | ✔ |
| gate hashes a6307edf (landed) / 772a1d8e (before) | `sha256sum` of working-tree gate = a6307edf687ac0fb…; `git show bf7c931a:tools/research-gate.sh` = 772a1d8e4d94dbf3… (extracted to scratch `gate-before-772a1d8e.sh`); `measure-a2/deadzone-fixture-vs-gates.txt` exercises both | ✔ |
| seeds 5011/5023/5033/5047 → 37/37 | committed receipts `measure-a2/c2-after-s{5011,5023,5033,5047}.json` — all label `DEADZONE_MATCH=37/37`, `predicate_holds=true`, `gate_sha256=a6307edf…`, `counter_sha256=8c0def4d…` | ✔ |
| before 21/37 | committed `c2-before-s5011/5023.json`: 21/37, gate 772a1d8e, stderr `grep: regular expression is too large` ×32; **reproduced** on fresh seed 3401 = 21/37, 16 misses (all 16 supported/mislocated long records), exit 1 | ✔ |

## 2. C2 re-derivation (operability)

- Clone at frozen tip, `sha256sum corpus/evidence/round34/c2-count.py` = `8c0def4d…` (= audit pin).
- **Landed gate (a6307edf), fresh seeds**: `C2_TMP=<scratch> python3 c2-count.py --seed 6001/6013 --receipt …` →
  both `DEADZONE_MATCH=37/37`, `predicate_holds=true`, exit 0 (receipts sha256
  633def8f…/552e8460…). Committed seed 5011 re-run → 37/37 (ac4e358d…).
- **Before gate (772a1d8e, extracted blob), fresh seed 3401**: `DEADZONE_MATCH=21/37`, exit 1; per-class
  misses exactly the 16 supported/mislocated long records (verbatim-ml 0/3, verbatim-1l 0/2, edge 0/2,
  decoys-exact 0/2, decoys-line-wrong 0/2, glued-then-valid 0/1, line-bound 0/2, line-wrong 0/2); all
  unsupported-truth long classes match (2/2) because grep error → `observed=unsupported` = truth.
- Committed-run inventory at frozen tip (`git ls-tree -r 707da818… | grep c2-`): exactly the 2 before
  (21/37) + 4 after (37/37) receipts; history search (`git log -S DEADZONE_MATCH -- measure-a2/`) shows
  only `2592f9da` (before) and `fe0f22e0` (after) added them → **no committed run on the landed gate below 37**.
- Wave-2a2 scratch rerun receipts `w2a2/ExecC2Rerun/c2-rerun-s{7311,7417}.json` (untracked, not committed)
  also read 37/37 on a6307edf.
- **P2 verdict: met.** Before 21/37 (reproduced), after 37/37 on two fresh seeds (plus 4 committed), no
  committed lower run.

## 3. C3 re-derivation (calibration)

- `python3 corpus/evidence/round34/self-audit.py --lane <clone>` → 43/43 checks ok,
  `SELF_AUDIT_MISMATCHES=0`, `SELF_AUDIT_UNDISPOSITIONED=0`, exit 0 — byte-equivalent to committed
  `measure-a2/audit-first-run.txt` (same lines). Set = 43 checks (20 path, 12 git_commit, 4 sha256,
  4 receipt_binding, 3 grep_assert). `audit-dispositions.md` empty (no mismatches to disposition).
- Negative control committed (`audit-negative-control.txt`): 2 injected lies → K=2, disposition key exact.
- **P3 verdict: met.** Count reproduced verbatim; every counted mismatch would carry a committed disposition
  (none currently).

## 4. No-harm / identity

- Old gate selftest (772a1d8e, from a scratch checkout of bf7c931a with the blob placed at
  `tools/research-gate.sh`) → `PASS (253 cases, 0 skipped)`, exit 0; landed gate (a6307edf) →
  `PASS (256 cases, 0 skipped)`. First 253 case lines identical (sha256 `69454af6…` both; diff clean).
  (First extraction-location run failed only case 106 `claims-lane-fallback` because the extracted blob
  ran outside a lane checkout — the case locates the lane via the script path; not a gate defect.)
- Dead-zone fixture committed evidence (`deadzone-fixture-vs-gates.txt`) matches: old gate reads DD1/DD4
  `unsupported` (stderr too-large), landed gate reads `supported` (2/2).

## 5. Findings by severity

None high. Minor/nuance:
1. **C1 caveat omitted in one clause** (low): "Spans of 32768 bytes and more … and verify" (knowledge doc
   line 23) states C1's capability as verified; the frozen record keeps C1 at `unverified (required
   controls held)` (claims.md exclusion record; claims-a2.md). Same wording is inherited from
   claims-a2.md ("already verify via the C1 chunk matcher"); recommend attaching the caveat.
2. **Probe run stdout not archived** (low): the 20×5 boundary probe's run outputs (2026-10-23 ~15:35) are
   not committed; the fixture directory exists at the cited path and the boundary is independently
   reproducible (done) and recorded in S065 host note + Scribe evidence.
3. **"roughly two code units per span byte"** (info): explanatory inference, not measured; the measured
   boundary does not depend on it.
4. **Gate comment off-by-one** (info): `tools/research-gate.sh:7857` says "cases 255-257"; actual numbers
   are 254-256 (log/.cases confirm). Cosmetic.
5. **Design-expectation vs measured before** (info): claims-a2.md "Expected ceiling 4/37" vs measured
   21/37 (unsupported-truth long records still match under a too-large pattern error); the committed
   before-receipts, commit message and SCORECARD consistently use 21/37 — no claim overreach.

## 6. Residual risk

- Boundary is host-specific (PCRE2 10.49-1, grep 3.12-2); knowledge doc says so; selftest pins this host.
- Verify-claims on the dead zone was attacked via the committed counter and its fresh/re-run receipts; the
  shortcut-control family for C1 remains excluded per the frozen hold (not re-opened).
- No network used; all evidence local.

## 7. Commands run (key)

```
git clone -q <lane> lane && git -C lane checkout -q 707da818…   # sha256 gate a6307edf…
python3 corpus/evidence/round34/self-audit.py --lane lane         # 0/0, exit 0
C2_TMP=<scratch> python3 c2-count.py --seed 6001 --receipt …     # 37/37 exit 0
C2_TMP=<scratch> python3 c2-count.py --seed 6013 --receipt …     # 37/37 exit 0
C2_TMP=<scratch> python3 c2-count.py --seed 5011 --receipt …     # 37/37 rerun exit 0
C2_TMP=<scratch> python3 c2-count.py --gate gate-before…sh --seed 3401 --receipt …  # 21/37 exit 1
bash tools/research-gate.sh --selftest                           # PASS 256
bash gate-before-772a1d8e.sh --selftest (from bf7c931a checkout) # PASS 253
grep -P -f boundary/pat-32764.txt /dev/null                      # exit 1 compile OK
grep -P -f boundary/pat-32765.txt /dev/null                      # exit 2 too large
```
