# FC3 falsify — `claims-raw-colon-denied` (round27 attempt1)

Item: C3 control `claims-raw-colon-denied`, `corpus/evidence/round27-regressions.py:213` (claims source
`ROOT/synthetic:fixture/.config/entry.md`, expect exit 1, `FINDING CLAIM_SOURCE_SESSION`, one
`^RESEARCH_GATE: ` line; lines 210–222).
Revision dd72641e574679c4f7882dd43de072b4c8892d6f; gate sha256 ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84
(recomputed in the sandbox); regressions.py sha256 5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df
(identical in lane and sandbox). Base gate 64eec5d sha256 c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6.
Sandbox: `/tmp/chousa-r27-falsify-FC3ClaimsRawColonDenied55` (git archive of dd72641e). No installs.
Axis: calibration (C3). I did not run the full `--selftest` or the whole regressions script.

## Verdict: FALSIFIED (calibration)

The landed gate does refuse the shipped fixture before reading it, and a full revocation of both denial
legs makes the control fail for the intended reason. But the control is not a control for the repair its
name and the C3 claim describe:

1. Reverting the companion repair (gate line 1139 `is_denylist_fs_path "$src"` → the base predicate
   `is_denylist_path "$src"`) leaves the control **green**: the new canonical check (line 1166) refuses
   alone. Reverting line 1166 alone also leaves it green: the raw check refuses alone. The control only
   fails when **both** legs are removed. So no single-site revert shows up; the raw leg has no control.
   The same revert is also invisible to the other 57 controls (they never call `claim_source_path`),
   to `round27-mechanisms.py` (C3 stays 0: it counts only the registry function), and, by static
   enumeration, to the gate selftest (its only colon claims fixture is `claim:synthetic/alias.md`, gate
   line 6507, whose refusal is canonical-only).
2. The control cannot observe the contract's actual requirement ("no **reading** a denylisted synthetic
   path"). It asserts a self-reported string. A mutant that emits `CLAIM_SOURCE_SESSION` and then falls
   through reads the file (`CLAIM … observed=supported at=line:2`, `supported=1`) and still satisfies
   every assertion in `observe` (exit 1, token present, one verdict line).
3. Nearby inputs of the same class break the rule the control is supposed to establish: with an earlier
   colon, `a:b/synthetic.env:1` is **read** (rc 0 CLEAN) while its sibling `synthetic.env:1` is refused;
   `notes.env:2026.md` (complete path clean) is refused. The class's two claims controls encode two
   different rules, so "a colon occurs earlier ⇒ denylisted paths are not read" is false for the suffix
   patterns even on the landed gate.

## (1) Expectation vs the declared contract

- The denial outcome is contract-derived: C3 says "no reading a denylisted synthetic path when a colon
  occurs earlier", and `.config` is a pre-existing accepted denylist component (r22 path-start forms).
  The fixture content would be `supported` if read, so the deny-vs-read distinction is observable in the
  verdict. At base the gate reads it: `observed=supported at=line:2`, `RESEARCH_GATE: CLEAN`, rc 0.
- The assertions themselves (exit 1, `FINDING CLAIM_SOURCE_SESSION`, one verdict line) are gate-interface
  vocabulary, not r27-claims.md text. This C3 branch does not introspect gate source (unlike the C1
  helpers), so it is implementation-independent, but the expected strings come from the gate's documented
  output. More importantly the assertion is **weaker than the contract**: it never requires
  `refused=1`, `supported=0`, `VERDICT_BEARING_CLAIMS=0/1`, `at=-`, or the `denied (not opened)` phrase.
- The fixture is a conjunction input: its raw and canonical forms are both denylisted, so a pass cannot
  say which predicate refused. It is therefore structurally incapable of attributing the raw repair.

## (2) Mutation of the targeted fix(es)

Harness: one claims file per probe, run as `env CHOUSA_STRICT=0 LC_ALL=C bash <gate> verify-claims
claims.jsonl --root <temp root>` from the temp root (the script's own cwd/env), timeout 120 s. Fixture:
`<root>/synthetic:fixture/.config/entry.md` holds the entry text (span `synthetic`); `--root <root>`.
Sanitised-environment reruns (`env -i PATH=… LC_ALL=C CHOUSA_STRICT=0`) reproduce the landed and M-raw
outputs byte-for-byte apart from the timestamp.

| gate | change (sha256) | rc | key output | control predicate |
|---|---|---|---|---|
| landed | — (ca39d14d…) | 1 | `observed=refused`, `CLAIM_SOURCE_SESSION`, claims=1 refused=1 | PASS |
| BASE 64eec5d | pre-fix (c2c813f1…) | 0 | `observed=supported at=line:2`, `RESEARCH_GATE: CLEAN` | FAIL (intended) |
| M-raw | 1139 → `is_denylist_path "$src"` (f8cfb2a1…) | 1 | same refusal, produced by canon check | **PASS** |
| M-canon | 1166 → `is_denylist_path "$canon"` (890c6fc0…) | 1 | same refusal, produced by raw check | **PASS** |
| M-both | both → prefix predicate (53ce8381…) | 0 | `observed=supported at=line:2`, CLEAN | FAIL (intended) |
| M-read | landed + `head -c 16 -- "$src"` before the checks (8e331821…) | 1 | byte-identical to landed | **PASS** (read invisible) |
| M-log-read | both deny blocks emit the finding and fall through (6379ec5c…) | 1 | `observed=supported at=line:2`, `supported=1`, token present, one verdict line | **PASS** (file read) |

`observe` from the script was re-applied mechanically to each captured output (`expected_rc=1`,
`required=('FINDING CLAIM_SOURCE_SESSION',)`, `counts={'^RESEARCH_GATE: ':1}`), producing the last column.
M-base/M-both fail for the intended reason (the spanning content was accepted: `supported=1`), not a parse
or setup error. M-raw and M-canon are exactly the two r27 hunks applied separately; both survive.

The only input class where the raw predicate is behaviourally distinct is raw-denied but canonically
clean. Probe: `<root>/synthetic:fixture/.config` is a symlink to a clean directory holding the entry text.
Landed: rc 1, `CLAIM_SOURCE_SESSION`. M-raw: rc 0, CLEAN, `observed=supported` (file read). No shipped
control uses that shape, so the raw leg's effect is untested.

## (3) Nearby synthetic inputs — landed gate wrong, and control vacuity

All fixtures are synthetic under `/tmp`; each is a regular file containing the claim span.

- Under-refusal, same class, production gate: source `<root>/a:b/synthetic.env:1` →
  rc 0, `RESEARCH_GATE: CLEAN (claims=1 supported=1 … refused=0)`, `at=line:2` (file read).
  The sibling control's `<root>/synthetic.env:1` → rc 1, `CLAIM_SOURCE_SESSION`. Inserting an earlier
  colon defeats the suffix refusal because `is_denylist_fs_path` checks only the complete string (which
  ends `:1`) and the text before the **first** colon (`<root>/a`, clean); later prefixes are never tried.
  By contrast `<root>/a:b/.config/entry.md` is refused: the `*/.config/*` arm is a substring test and
  colon-independent. One rule ("colon earlier") therefore yields opposite outcomes depending on which
  pattern style names the denied path. Either `synthetic.env:1` is denylisted (then the gate under-refuses
  `a:b/synthetic.env:1`) or complete paths are the rule (then the legacy sibling control is wrong).
- Over-refusal: `<root>/notes.env:2026.md` → rc 1, `CLAIM_SOURCE_SESSION`, although its complete path
  contains no denylisted component; only the first-colon prefix (`…/notes.env`) matches `*.env`.
  So the r27 "complete filesystem paths" repair did not change claim sources from prefix semantics; it
  added a full-string arm alongside the prefix arm (`is_denylist_fs_path`, gate 609–613).
- Misreported evidence on the control's own fixture: the finding's `obs=path=` is
  `$(ptr_file_part "$src")`, the text before the first colon (gate 1141/1168). For
  `<root>/synthetic:fixture/.config/entry.md` it prints `<root>/synthetic`. With a clean unrelated file at
  that truncated path, the finding names that other file as `denied (not opened)`; the true file is only
  in `source=`. The control requires neither field's value beyond the token, so this false recovery path
  passes.
- Vacuity on non-read: M-read shows a real 16-byte read is output-invisible; M-log-read shows a gate that
  reads the file and logs a denial still satisfies the control. The contract clause "not opened" is
  asserted only by a string the gate itself writes.
- No read bypass was found for the `.config` component family itself: colon-before variants
  (`a:b/.config/entry.md`, `x:/.config/entry.md`, relative forms) are all refused before the read.

## Smallest safe corrections (author-lane advice)

1. Control fixture: make the raw case canonically clean so it discriminates the raw predicate — e.g.
   `synthetic:fixture/.config` as a symlink to a clean directory, or `synthetic:fixture/.config/../entry.md`
   with a real `.config` directory. Keep `claims-canonical-colon-denied` (alias) for the canon leg.
2. Strengthen `observe` for this case: add counts `^CLAIM id=.* observed=refused`, `refused=1`,
   `supported=0`, `VERDICT_BEARING_CLAIMS=0/1`, and require `denied (not opened)`. This catches M-log-read.
   It cannot catch M-read (silent read) — record that as an acknowledged limit rather than a claim.
3. Reconcile the class rule: either test every colon prefix in `is_denylist_fs_path` (as the
   `claims-legacy-env-anchor-refused` sibling implies) and add `a:b/synthetic.env:1` expecting refusal,
   or drop the prefix arm and flip that sibling control. Add `notes.env:2026.md` as the over-refusal
   control for whichever rule is chosen. Also add a positive claims-mode ordinary-colon control
   (`synthetic:ordinary.md`): the landed gate allows it (rc 0 CLEAN), but only the registry surface has
   such a control today.
4. Diagnostics: for claims (a filesystem input, not a citation pointer) emit the complete source in
   `obs=path=`, or label it as a truncated pointer part; do not present a different existing path as the
   refused one.

## Limits

- I did not run the full `--selftest` or the whole regression script (L1 owns both). The selftest-coverage
  statement is static: `grep '"source":"[^"]*:' tools/research-gate.sh` yields only line 6507
  (`claim:synthetic/alias.md`, canonical-only), plus URL sources.
- M-read/M-log-read are constructed mutants, not observed production behaviour; no production read of a
  denylisted `.config` claim source was found. The under-refusal and over-refusal in (3) are observed on
  the landed gate.
- No network, host secrets, `/proc`, live processes, strace or debugger; no lane edits except this report.
- Scratch artifacts: `mutations/{m1,m2,m3}.sh`, `mut-m{1,2,3,4,5}/tools/research-gate.sh`,
  `gate-base.sh`, `.probe{1..7}/`, `*.out` in the sandbox above.
