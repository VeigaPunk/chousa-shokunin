# CritC1JudgeHoles — attack on `judge()` in c1-battery.py (round 63, C1)

Scope: the parser `judge(name, exp, rc, out, err)` in `corpus/evidence/round63/c1-battery.py`
(frozen, sha256 prefix `0073fba73c89aaf8`, re-checked before my runs). Question: which outputs a lying tool
can print that the frozen judge accepts for a defect leg while no gate ran. I edited nothing under the lane,
committed nothing, installed nothing. Scratch: `/fast/scratch/hyaku/chousa-r63/CritC1JudgeHoles/` (deleted at yield).

## What judge() checks (read from the frozen source, lines 267-308)

- GATE lines: `GATE_RE = ^GATE (G\d\d) (\S+) (PASS|FAIL|ENV|SKIP)\b` — the status is matched by prefix plus a
  word boundary; the name `(\S+)` is read and then ignored; nothing after the status is checked.
- Summary: exactly one line starting `PREFLIGHT=`, which must fully match `SUM_RE` (`$`-anchored).
- Input is `out.splitlines()`; `err` is never read.
- Lines that match neither pattern are ignored (no check that stdout is only the contract lines).
- Gate ids: first match per id kept; a second GATE line for an id fails; order must equal G01..G08.
- Summary numbers and member sets are compared to the GATE lines as sets.

## Probes (18 scratch tools, each a fixed-output program that runs no gate; each run with `--only <leg>`)

Each tool prints a fixed answer. Control probes (t00, t01, t17) print the honest answer for their leg. The rest
print the honest answer with one lie. Command for each: `python3 -B corpus/evidence/round63/c1-battery.py
--tool <probe>.py --work <absent dir> --fleet /home/vgpnk/Projects/shokunin --only <LEG>`. Driver:
`bash run.sh` (scratch), output `rc=0` for all 18 runs; per-run logs under scratch `logs/`.

Frozen judge, per probe (`LEG <name> <kind> ok|FAIL <why>` lines from the battery, verbatim):

| probe | leg | lie printed | frozen judge |
|---|---|---|---|
| t00 | D06 | none (control) | ok |
| t01 | CLEAN | none (control) | ok |
| t17 | D14 | none (control) | ok |
| t02 | CLEAN | 2 non-contract lines (before and after the GATE block) | ok |
| t03 | D06 | `GATE G03 ... fail` (lowercase) | FAIL gate lines G01,G02,G04..G08 |
| t04 | D06 | `PREFLIGHT=... SKIPPED=G08 (6 of 7 pass)` | FAIL rc=1 summary lines=1 |
| t05 | D06 | `PREFLIGHT=... SKIPPED=G08\x0c(6 of 7 pass)` | **ok** |
| t06 | D06 | GATE G03 with name `census` | **ok** |
| t07 | D06 | G03 printed SKIP, summary consistent | FAIL ran G01,G02,G04..G07 want ...G03... |
| t08 | D06 | summary line printed twice | FAIL summary lines=2 |
| t09 | D06 | all output on stderr, stdout empty | FAIL summary lines=0 |
| t10 | D06 | `GATE G03 ... FAIL(` and `PASS.` on the others | **ok** |
| t11 | CLEAN | every gate `PASS (not run)`, no gate run | ok |
| t12 | D13 | 8 GATE PASS lines, rc=2, no PREFLIGHT | **ok** |
| t13 | D13 | rc=2, no output at all | **ok** |
| t14 | D14 | all 8 gates printed (none skipped) under `--only G03` | FAIL ran ...G08 want G03 |
| t15 | D06 | `PREFLIGHT=6/7 FAILED=G03,G03 ...` | **ok** |
| t16 | CLEAN | `GATE G01 census PASSED` | FAIL gate lines G02..G08 |

Battery verdict lines for the accepted probes (e.g. `t05`): `LEG D06 defect ok ok` and
`CLEAN=0/1 DEFECTS=1/15 BENIGN=0/6 BATTERY=PARTIAL`. The honest controls read `LEG ... ok ok`.

## Accepted holes (frozen judge accepts; no gate ran)

1. **t05 — form feed hides trailing text on PREFLIGHT (D06).** `str.splitlines()` splits on `\x0c`, so the text
   after it is a separate, ignored line; the summary still matches `SUM_RE`. Human view: the summary line
   looks clean.
2. **t06 — GATE name not checked (D06).** `m.group(2)` is never compared. A G03 line named `census` is accepted.
   This is the battery's declared limit ("does not check the gate names"); confirmed, not new.
3. **t10 — status prefix plus `\b` (D06).** `FAIL(` and `PASS.` are read as FAIL and PASS, because the regex ends
   in `\b`, not in end-of-token. A tool can glue text to a status.
4. **t12 — usage leg accepts GATE lines (D13).** The D13 test checks only rc==2 and no PREFLIGHT line. A tool
   that runs and prints every gate PASS, then exits 2, is accepted.
5. **t13 — usage leg accepts silence (D13).** Any run that exits 2 with no output is accepted. The D13 leg never
   requires the bad id to be named. (The CLEAN leg still binds the tool to exit 0 on a valid `--skip G08`, so a
   tool cannot pass CLEAN and D13 by blanket exit 2. The hole is the leg's acceptance of an unexplained exit 2.)
6. **t15 — summary member sets not checked for duplicates or `none` mixing (D06).** `FAILED=G03,G03` compares as
   the set {G03}.

Not holes, but accepted because the frozen judge only reads what it parses (no defect leg):
- **t02** — extra non-contract lines on stdout are ignored. Verdict-neutral; a contract breach the judge does not see.
- **t11** — `PASS (not run)`: free text after a status is allowed (the reference itself prints free-text details,
  e.g. `PASS 3 entries indexed`, `PASS exit=0`). No structural rule can reject it without a contract change. Residual.

Rejected (correct): t03 lowercase status; t04 plain trailing text on PREFLIGHT; t07 SKIP for a gate the leg
requires; t08 duplicate PREFLIGHT; t09 stderr-only output; t14 gates run under `--only`; t16 `PASSED`.

## Stricter judge rules (tested, not applied to the frozen file)

`corpus/evidence/round63/...` is frozen; the rules below were tested in scratch by a harness
(`strict_probe.py`, run `python3 -B strict_probe.py`) that imports the frozen module, runs each probe with its
leg's argv, and applies the frozen judge first, then the stricter rules:

- **S1 (stdout shape).** stdout is exactly 8 `GATE` lines in id order, then one `PREFLIGHT=` line last; names must
  equal the contract's names (G01 census, G02 knowledge-index, G03 lesson-gate, G04 shonen-pointers,
  G05 scorecard-paths, G06 freeze-selftest, G07 assimilate-selftest, G08 gate-selftest); each GATE status is
  followed by end-of-line or one space; no control characters (`\x00-\x08`, `\x0b-\x1f`, `\x7f`, `\x85`,
  `\u2028`, `\u2029`) on stdout. Closes t02, t05, t06, t10.
- **S2 (summary sets).** Each of FAILED, ENV, SKIPPED is `none` alone or distinct `G\d\d` ids. Closes t15.
- **S3 (usage leg).** On D13: no GATE line on stdout; stderr names the bad id (`unknown gate id` and `G99`).
  The reference prints exactly this (`pos-ref-preflight.py` line 178, `unknown gate id for --skip: G99`, to stderr).
  Closes t12, t13.

Harness output (`python3 -B strict_probe.py`, exit 0):
```
t00-d06-honest               leg=D06   frozen=ACCEPT strict=ACCEPT
t01-clean-honest             leg=CLEAN frozen=ACCEPT strict=ACCEPT
t02-clean-extra-lines        leg=CLEAN frozen=ACCEPT strict=REJECT  | S1 11 stdout lines
t03-d06-lowercase            leg=D06   frozen=REJECT strict=REJECT
t04-d06-summary-trailing     leg=D06   frozen=REJECT strict=REJECT
t05-d06-summary-formfeed     leg=D06   frozen=ACCEPT strict=REJECT  | S1 control character on stdout
t06-d06-wrong-name           leg=D06   frozen=ACCEPT strict=REJECT  | S1 line 3 is not `GATE G03 lesson-gate STATUS`
t07-d06-skip-should-run      leg=D06   frozen=REJECT strict=REJECT
t08-d06-dup-summary          leg=D06   frozen=REJECT strict=REJECT
t09-d06-stderr-only          leg=D06   frozen=REJECT strict=REJECT
t10-d06-glued-status         leg=D06   frozen=ACCEPT strict=REJECT  | S1 line 1 is not `GATE G01 census STATUS`
t11-clean-pass-not-run       leg=CLEAN frozen=ACCEPT strict=ACCEPT  | residual
t12-d13-gate-lines           leg=D13   frozen=ACCEPT strict=REJECT  | S3 usage path printed GATE lines
t13-d13-silent-exit2         leg=D13   frozen=ACCEPT strict=REJECT  | S3 usage path names no bad id on stderr
t14-d14-ran-unselected       leg=D14   frozen=REJECT strict=REJECT
t15-d06-dup-set-member       leg=D06   frozen=ACCEPT strict=REJECT  | S2 summary member sets malformed
t16-clean-passed-glue        leg=CLEAN frozen=REJECT strict=REJECT
t17-d14-honest               leg=D14   frozen=ACCEPT strict=ACCEPT
```

Strict rules keep all three honest controls (t00, t01, t17) accepted and reject every parser hole except t11.

## What the strict rules do not close (residuals, for the next round's battery)

- **A well-formed fabricated answer.** Probe t00 is the honest D06 answer; it is also exactly what a tool would
  print if it knew the leg and ran nothing. No judge rule over stdout text can tell it apart from a real run. The
  only defences are the frozen benign legs and the diff structure, and `null-diff-oracle.py` (committed control)
  shows the benign legs are what catch a forger of this kind. This is a forger class, not a parser hole; it is
  INFERENCE that a tool keyed to leg content could pass all 15 defect legs and fail only some benign legs.
- **Free text after PASS (t11).** Not closable structurally without forbidding details on PASS, which the
  reference does not do. Residual.
- **Name check, not in the frozen battery.** The declared limit stands; a name rule (S1 above) would close t06
  in the next round's battery.

## Recommendation (for L1; the frozen judge is not edited by this seat)

Adopt S1-S3 in the next round's battery as a new predicate (a limit and supplement, per claims.md: a post-freeze
finding is a limit, not a rewrite). For this round, the frozen judge's six defect-leg holes stand as recorded
limits.

Checks run: `sha256sum corpus/evidence/round63/c1-battery.py | cut -c1-16` → `0073fba73c89aaf8` (frozen bytes
matched); 18 `c1-battery.py --only` runs (driver `run.sh`, all rc=0); `python3 -B strict_probe.py` (exit 0);
`find corpus tools -name __pycache__ -newer corpus/evidence/round63/claims.md` → no output (no lane writes).
Installs: none. Lane writes: none (this report only; scratch deleted at yield).

VERDICT: JUDGE_HOLES=6 accepted=t05-formfeed-summary,t06-wrong-gate-name,t10-glued-status,t12-d13-gate-lines,t13-d13-silent-exit2,t15-dup-set-member
