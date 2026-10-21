# FC3 falsify — `nonstandalone-duplicate` (round27 attempt1)

Item: C3 control `nonstandalone-duplicate`, `corpus/evidence/round27-regressions.py:156`
(`source: ref S002x and S002`; registry `S001 mined` + `S002 queued`; expect exit 1,
exactly one `FINDING META_SOURCE_NOT_MINED … source_id=S002`, exactly one `^FINDING META_SOURCE_`).

Revision dd72641e574679c4f7882dd43de072b4c8892d6f; gate sha256
`ca39d14d…2f84` and regressions.py sha256 `5afea786…a5df` verified in sandbox.
Base 64eec5d4 gate sha256 `c2c813f1…3abc6` (matches the r26 target cited by
`CriticRegistryGrammar.md`); committed oracle `round26-registry-oracle.py`
sha256 `6b2d135c…f1d78`. Sandbox `/tmp/chousa-r27-falsify-FC3NonstandaloneDuplicate40`
(git archive). GNU bash 5.3.20(1), GNU grep 3.12-modified (`/usr/bin/grep`),
Python 3.14.8. No installs. No full `--selftest` and no whole regression run
(L1 owns those); only single gate commands, gate mutants in the sandbox, and a
replay of the script's own `observe` helper for this one case.

## Verdict: HOLDS as a control

The expectation is contract-derived and implementation-independent; reverting the
exact production fix makes it fail on the finding count for the intended reason.
Two negative results are reported: (a) the control alone is vacuous against
multiplicity/window mutants (siblings catch them), and (b) an inherited
rule-level calibration case at the non-ASCII boundary, which the landed gate
shares with base and with the committed oracle — not an r27 code regression.
No same-class input was found where the landed gate disagrees with the committed
oracle (20/20 set agreement).

## (1) Expectation independence — holds for this input

- The C3 section never reads gate source. `text = gate.read_text()` (`:25`) is
  used only at `:75` to extract the two C1 usage helpers; every C3 expectation
  (exit code, required diagnostic, count) is a literal.
- Exit 1 and the `source_id=S002` finding follow from the fixture alone: `S001`
  is mined and its `used-by` names `corpus/knowledge/entry.md`; `S002` is queued.
- The count 1 follows from the operative boundary rule — a standalone id is a
  maximal `[A-Za-z0-9_]` run equal to `S` + ≥3 digits (r26 spec-v1, quoted at
  `.ufo/waves/round-26/falsify/FRegistryIdBoundary.md:134`, and encoded by the
  oracle as `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`). On
  `ref S002x and S002` that yields exactly `{S002}`, which is also the accepted
  r26 b3 receipt (one standalone occurrence emitted ×2 was the reported
  "duplicate emission" defect, `FRegistryIdBoundary.md:94-97`).
- The claim's ambiguous "without … duplicate occurrences" has two readings
  (per-occurrence vs per-id dedup; `CriticRegistryGrammar.md` defect 2); both
  give 1 for this input, so this control does not depend on resolving it. The
  sibling `two-real-occurrences` (`S002,S002` → ×2) is where the suite commits
  to per-occurrence counting without the claim text saying so — see advice 1.

## (2) Mutation of the targeted production fix

`mutant1-gate.sh` replaces `metadata_registry_check_source` with the base
function (compressed regex + `source_scan=${source_scan#*"$source_match"}`
rescan), byte-identical to the base function (verified by extracting both
functions and comparing; the only inter-function difference the head fix added,
the redundant `local LC_ALL=C`, was dropped because `verify_metadata` already
pins `LC_ALL=C` at `:2564`). sha256 `81f88216…06ad`.

Harness: the exact control fixture from `round27-regressions.py:52-56,151,161-164`
replayed once per gate, checked with the script's own extracted `observe`
(patterns `^FINDING META_SOURCE_NOT_MINED\b[^\n]* source_id=S002(?: |$)` and
`^FINDING META_SOURCE_`, both expected 1).

| gate | change | rc | NOT_MINED count | total META_SOURCE_ | observe |
|---|---|---|---|---|---|
| landed | — | 1 | 1 | 1 | PASS |
| mutant1 | exact base function (rescan revert) | 1 | 2 | 2 | FAIL: `count …: 2 != 1` ×2 |
| mutant3 | tokenizer boundaries dropped (`grep -oE 'S[0-9]{3,}'`) | 1 | 2 | 2 | FAIL: same two counts |
| mutant9 | id anchor dropped (`^S[0-9]{3,}` without `$`) | 1 | 1 | 2 | FAIL: total count only |

The failing mutants fail for the intended reason, not parse/setup: exit is 1,
stderr empty, and the output carries a well-formed
`RESEARCH_GATE: DRIFT (… findings=2 drift=2)` verdict plus `META entry=…`
lines. mutant1's second finding is a duplicate of the first, produced by the
literal-prefix strip landing inside `S002x` and re-anchoring `^` on the
remainder — the r26 root cause.

Specificity: mutant1 still passes `two-real-occurrences` (`S002,S002` → 2) and
`underscore-glued` (`xS002 S002x _S002 S002_ S001` → 0), so the failure is
uniquely attributable to the rescan-duplicate and not a global count shift.
mutant9 shows the second (total) count pattern is load-bearing: the fabricated
`source_id=S002x` ROW_MISSING is invisible to the `source_id=S002(?: |$)`
pattern.

## (3) Nearby same-class inputs

### 3a. Landed gate vs the committed oracle (set level)

20 same-class inputs, gate `verify-metadata` vs `round26-registry-oracle.py`:
no finding-set divergence (20/20), including `ref S002_ and S002`,
`ref S002S002 and S002`, `ref S002x,S002`, `ref S002x and S002 ` (trailing
space), `see S001S002 and S001`, `see S001_S003 and S001`, `x S1234S0003 y S1234`,
`(S001S003) S001`, `ref S002x`, `ref S002x S002y S002`, `éS002`, `S002٣`,
`S002１`, `S002é`, `S002-1`, `S002.1`. So no wrongness in this class relative to
the existing independent authority.

### 3b. Individual vacuity (mutants that PASS this control)

| mutant | mechanism | this control | suite sibling |
|---|---|---|---|
| M5 `sort -u` | one finding per distinct id | PASS (1) | `two-real-occurrences` FAIL (1 vs 2) |
| M7 `tail -n 1` | only the last token is examined | PASS (1) | `two-real-occurrences` FAIL (1 vs 2) |
| M8 `grep -oE 'S[0-9]{3,}' \| head -n 1` | first matching substring; the fabricated `S002` from `S002x` is reported and the real standalone occurrence is never examined | PASS (1) | `two-real-occurrences` FAIL; `underscore-glued` FAIL |

So the control cannot tell *which* textual occurrence produced its single
finding, and it cannot see occurrence-multiplicity collapse. Both gaps are
covered by `two-real-occurrences` (and `underscore-glued` for M8); no suite
failure results from the landed control set. `two-real-occurrences` must not be
weakened.

### 3c. Inherited rule-level counterexample (non-ASCII adjacency)

Minimal pair, same class, one byte changed (`S002` queued in the fixture):

```
source: ref S002x  → rc 0, FINDING META_SOURCE_NO_ROW_ID (info), RESEARCH_GATE: CLEAN
source: ref S002é  → rc 1, FINDING META_SOURCE_NOT_MINED … source_id=S002, RESEARCH_GATE: DRIFT
```

Same for `S002٣` and `S002１`. The base-function mutant emits the identical
result, so this is inherited, not introduced by the r27 repair. Under the
operative r26 rule ("standalone ASCII alphanumeric/underscore boundaries") and
the oracle's explicit `[A-Za-z0-9_]` lookarounds, the non-ASCII byte is a
boundary and the finding is rule-consistent; under a plain reading of
"standalone ASCII S-id" the occurrence is invented. `CriticRegistryGrammar.md`
defect 3 recommended a non-ASCII-adjacent control; the landed C3 controls have
none, so the boundary-set decision is unpinned — the suite also runs every C3
case under `LC_ALL=C`, so a locale-class change in the scanner would not be
noticed by any current C3 control.

## Limits

- Full `--selftest` and the whole regression script were not run (L1 owns both);
  one control case was replayed with the script's own `observe`.
- All probes ran under `LC_ALL=C` (the control's declared env); no C3
  inherited-locale execution.
- Mutants are sandbox copies; no lane file, registry, git/jj state, or sibling
  fixture was touched. Fixtures live in `/tmp`; no network, host secrets,
  `/proc`, strace, or live processes.
- The oracle is set-based, so multiplicity expectations rest on the accepted r26
  b3 receipt and the per-occurrence reading, not on the oracle.
- C3 header-state/width and full-path denylist stages are out of scope (other seats).

## Advice to the author lane

1. Amend the C3 claim to state the counting rule ("one finding per standalone
   ASCII token occurrence; none for non-standalone text"), or cite the accepted
   r26 b3 receipt from the claim, as `CriticRegistryGrammar.md` defect 2 asks.
   Today the claim's "duplicate occurrences" wording is disambiguated only by a
   sibling control.
2. Add a non-ASCII-adjacent control (`ref S002é`) with the expectation matching
   the intended rule (NO_ROW_ID under a plain "ASCII S-id" reading, or
   NOT_MINED as an explicit ASCII-boundary decision) so the boundary set is
   pinned rather than implicit.
3. Keep both count patterns in this control: only the total `^FINDING
   META_SOURCE_` count catches fabricated ids such as `S002x` ROW_MISSING.
4. Keep `two-real-occurrences` unchanged; it is the sole control that kills the
   dedup, last-token, and first-substring mutants above.
