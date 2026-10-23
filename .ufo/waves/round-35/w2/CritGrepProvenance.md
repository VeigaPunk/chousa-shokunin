# CritGrepProvenance — round-35 w2 critic report (C1 grep-pin attack + claim-shape audit)

Seat: `chousa-r35-w2-CritGrepProvenance` (leaf, no subagents). Date: 2026-10-23.
Scope: attack C1's provenance check (`grep_pin_init`/`grep_pin_verify`) in
`tools/research-gate.sh`; audit the claim record and round shape. C2 not re-derived
(out of item scope).

## Verdicts

1. **C1 P1 stands as measured.** I reproduced `GREP_PIN_MATCH=9/9`,
   `predicate_holds=true` with the committed counter, clean environment, seed
   424242, against the landed gate
   (sha `1f2fb4f5…7617`, receipt `.ufo/waves/round-35/w2/CritGrepProvenance/c1-clean-s424242.json`).
   Kill rule not triggered.
2. **Fixable defect (demonstrated, verdict-changing for the claim's robustness
   narrative): the verify step fails open under the claim's own threat class.**
   `grep_pin_verify` pipes `--version` through `head` (gate line 361 at the
   landed sha). A caller-supplied `BASH_ENV` that defines `head()` rewrites the
   version line, so the gate **accepts and pins a truthful non-GNU override** —
   the S6-class refusal silently breaks. NOT covered by the disclosed limit
   (claims.md: "a binary that lies about its version is out of this check's
   reach"): here the binary tells the truth (`grep (pi-uu-grep) 0.2.0` on
   stdout) and the gate's own plumbing lies. Demonstrated at counter level:
   committed `c1-count.py` against the landed gate with ambient
   `BASH_ENV=head()` prints `GREP_PIN_MATCH=6/9` with **S6 FAIL**
   (`marker=false`, `stub_calls=5` — the non-GNU stub was pinned and used)
   (receipt `c1-hostile-s424243.json`). Also poisons the receipt evidence: S8's
   echo shows a forged `version="grep (GNU grep) 3.11-fake"` while
   `path=/usr/bin/grep` (`t14-headonly`).
3. **Smallest safe correction, validated:** capture without `head`
   (`v=$("$cand" --version 2>/dev/null || true); v=${v%%$'\n'*}`, optionally
   timeout-bounded). On a scratch copy (`c1-grep-pin-verify-patched.sh`): the
   hostile replay refuses rc=2
   (`override does not report GNU grep: grep (pi-uu-grep) 0.2.0`); counter
   re-run clean = **9/9** (`c1-patched-clean-s424244.json`); counter re-run
   hostile = 7/9 with **S6 PASS** and honest echo versions
   (`c1-patched-hostile-s424245.json`). Residual: ambient function injection
   still corrupts other gate plumbing (gate `head` uses at lines 942/2017/2176 —
   the hostile runs' reference run goes insane via a `sed` fed the forged line);
   closing that is beyond the C1 surface (any single bash process trusts its
   function table).
4. **Claim-shape finding (with peer `CritGrepClaimScope`): P1 measures behavior,
   not mechanism.** Their named control `ctl-resolve-each-call.sh` —
   `grep(){ PATH=/usr/bin:/bin command grep "$@"; }`, per-call PATH sanitizing,
   no version probe, no pin, fabricated echo — scores **9/9,
   predicate_holds=true** on seeds 3535/3553 (receipts in
   `.ufo/waves/round-35/w2/CritGrepClaimScope/c1-resolve-each-call-s{3535,3553}.json`,
   gate sha `fc2aeaea…`, a named control). So claims.md's "the counter
   discriminates" rests on the committed hardcoded control (3/9) but is false
   against the cheapest 9/9-skipping work. P1 remains a valid kill rule for the
   landed gate; it is not evidence that verification/pinning specifically
   happened. Fixable in the claim record (calibration), not in the gate.
5. **TOCTOU, undisclosed, low severity (out of the claim's stated surface):**
   the pin is verified once at startup; `grep()` re-execs the pinned path per
   call. A candidate that atomically replaces itself after verification runs
   unchecked for the rest of the invocation (demonstrated: 4 post-swap matcher
   calls executed the replacement; receipt in /tmp logs). An attacker who can
   keep `--version` truthful gains nothing over the disclosed limit; a racy
   swapper with write access mid-run is outside claims.md's caller-environment
   model. Smallest correction: disclose it, or re-verify per call (impractical).

## Attack battery (landed gate sha `1f2fb4f5…7617` throughout; log
`/tmp/hyaku/chousa-r35/w2/CritGrepProvenance/`, driver `battery.sh` copied here)

| Test | Setup | Result | Classification |
|---|---|---|---|
| T1 wrap-lie | override script prints GNU line for `--version`, logs+execs real grep otherwise | rc=1, pin accepted, 9 match calls hit wrapper, echo shows lie version | **Disclosed limit** (self-reported provenance) — gate behaves exactly as claimed; not a finding |
| T2 symlink→`true` | override = symlink to non-GNU binary | rc=2 `does not report GNU grep: true (GNU coreutils) 9.12` | refused correctly |
| T3 directory override | | rc=2 `not a regular file` | refused |
| T4 FIFO override | | rc=2 `not a regular file` (no hang; verify never opens it) | refused |
| T5 0-byte executable | | rc=2 `does not report GNU grep: <no version>` | refused |
| T6 path with space | real GNU grep copied | accepted, `verdict=match` | correct (quoting sound) |
| T7 path with newline | real GNU grep copied | rc=2, `version="grep"` | **False refusal** (safe direction): GNU grep's line 1 is argv[0]-derived (`grep\nnl (GNU grep)…`), so line-1 read misses "GNU grep". Operability papercut |
| T8 `--version` exits nonzero | | rc=2 `<no version>` | refused |
| T9 `--version` silent | | rc=2 `<no version>` | refused |
| T10 GNU on line 2 only | | rc=2 with line-1 content | refused (safe direction) |
| T12b head()+non-GNU stub | hostile `BASH_ENV head()` + truthful pi-uu stub override | **rc=1, stub pinned, 5 match calls, echo forged** | **Finding 2** — fails open |
| T13 `command()` shim | `BASH_ENV command()` logger | pin identity held (`path=/usr/bin/grep`, match OK); 5 dispatches intercepted | grep name reclamation works; BASH_ENV remains arbitrary-code execution (context for Finding 2) |
| T14 head() only, default | hostile `BASH_ENV head()` | rc=1, echo version forged, path honest | receipt-evidence forgery (Finding 2 impact) |
| T11 TOCTOU | self-swapping candidate | verified GNU at pin, 4 later calls ran replacement | Finding 5 |

## Audit notes (round shape)

- Gate sha re-verified at session start: `1f2fb4f5…7617` (matches contract);
  `repairs/base-gate.sh` = `a6307edf…995b` (matches). Both my counter receipts
  record `gate_sha256=1f2fb4f5…7617`.
- **Mid-wave mutation observed:** during this wave the working copy's
  `tools/research-gate.sh` was changed (uncommitted, jj `M`; sha now
  `a4768851…`, mtime 17:07). The new text closes both Finding 2 (timeout +
  `v=${v%%$'\n'*}` in `grep_pin_verify`) and T13 (`grep_pin_define` via eval,
  no `command`; readonly guards on `grep`/`GREP_BIN`; PATH fallback removed) —
  i.e. the wave incorporated the critic results live. Consequence: any receipt
  generated against the working tree after ~17:07 is not the claim's canonical
  measurement; canonical C1 evidence must pin `1f2fb4f5…7617`.
- `.ufo/waves/round-35/repairs/slen-probe.sh` fails as invoked
  (`line 16: $1: unbound variable`) — needs fixture arguments; observed, not
  scored (R1 not re-derived by this seat).
- No installs; no network; all experiments in `/tmp/hyaku/chousa-r35/w2/CritGrepProvenance`;
  artifacts (receipts ×4, patched gate 371KB, drivers) in
  `.ufo/waves/round-35/w2/CritGrepProvenance/`, each <1 MiB.

## Impacted axes

- **Operability**: Finding 2 (verify fails open in the claim's declared
  environment class) — fixable, fix validated; T7 false-refusal trivia.
- **Calibration**: Finding 4 — the claim record's "counter discriminates"
  statement is inaccurate at the 9/9 level; P1 certifies behavior, not the
  pinned-verified mechanism.

## Limits

C2 witness and R1/R2 repairs not re-derived here (item scope is C1). Hostile-env
counter runs are constructed environments, not the L1's canonical measurement;
they are evidence about the gate's mechanism, not a P1 kill. T11's swap used my
own candidate file (write access to the pinned path is the precondition).
