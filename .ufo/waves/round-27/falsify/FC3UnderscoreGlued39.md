# FC3UnderscoreGlued39 — C3 control `underscore-glued` (round 27, attempt 1, falsify)

Seat `ChousaR27.FC3UnderscoreGlued39-11`. Author-lane advice, not outside admission.

**Item attacked:** `corpus/evidence/round27-regressions.py:155` at
`dd72641e574679c4f7882dd43de072b4c8892d6f`. The control has source
`xS002 S002x _S002 S002_ S001`, a registry with `S001` mined (exact used-by) and
`S002` queued, and expects exit 0 with zero `META_SOURCE_*` findings.

**Verdict: HOLDS for the landed gate, but the control is non-discriminating for
the round-27 rescan fix.**

- I found no counterexample against the landed scanner: 42 of 42 synthetic rows
  agree with a contract oracle, across 22 sources and the C and en_US.UTF-8
  locales.
- The control's expectation is contract-derived.
- The control kills underscore-boundary and no-boundary mutants for the intended
  reason.
- It still passes when the round-27 rescan fix is reverted to the base scanner,
  and when the scan is skipped entirely. On its own, it does not witness the C3
  "no duplicate occurrences" repair. Sibling controls do witness it.

## Setup

- Sandbox: `/tmp/chousa-r27-falsify-FC3UnderscoreGlued39`, created with
  `git archive dd72641e… | tar -x`.
- Gate sha256 is `ca39d14db907ec3f…`, which matches the assignment.
- Tools: GNU bash 5.3.20, GNU grep 3.12 (`/usr/bin/grep`; child `bash` resolves
  this binary, not the harness-shell builtin), Python 3.14.8. Nothing was
  installed.
- Harness files, all in the sandbox only:
  - `fx/mkmut.py` (sha `e58bcb75…`) generates the mutants. Each one replaces only
    `metadata_registry_check_source`.
  - `fx/probe.py` (sha `705b554e…`) is an oracle-diff runner. It uses the same
    registry, entry and env shape as `round27-regressions.py:151-164`. It also
    re-applies the control's exact count regexes (`CONTROL-AS-WRITTEN`).
- Logs: `fx/probe-landed-M1.log`, `fx/probe-mutants.log`, `fx/probe-M7.log`,
  `fx/probe-hardened.log`.
- Oracle: `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])` with `re.ASCII`. Each
  occurrence produces one finding. There is no dedupe.

## (1) Is the expectation independent of gate code?

Yes.

- Expected rc 0 and zero findings follow from the round-26 spec-v1 correction
  (`round26-claims.md:134-135`: "S + three or more digits (standalone ASCII
  alphanumeric/underscore boundaries)").
- They also follow from the round-27 C3 target (`round27-claims.md:15`:
  "standalone ASCII S-ids without invented or duplicate occurrences").
- Under that grammar, `xS002`, `S002x`, `_S002` and `S002_` contain no id. The
  only id is `S001`, which is mined and whose used-by is exactly
  `corpus/knowledge/entry.md` (exact-path rule, `round26-claims.md:136-137`).
- The values 0 and 0 are literals in the script. Nothing is computed from the
  gate.

## (2) Reverting or mutating the targeted fix

Commands: `timeout 120 python3 fx/probe.py <gate…>`, all exit 0, with
`PROBE_LOCALES="C en_US.UTF-8"` where noted.

| mutant (lines changed) | what it does | control as written | intended reason? |
|---|---|---|---|
| landed | `grep -oE '[[:alnum:]_]+'` word runs, keep `^S[0-9]{3,}$` | PASS (C, en_US) | — |
| **M1 revert-r27 (12)** | base `64eec5d` regex plus the `${source_scan#*"$match"}` rescan loop | **PASS** (C, en_US) | **not killed** |
| M2 `_` as separator (2) | `[[:alnum:]]+` | FAIL rc=1, S002×2 | yes: `_S002` and `S002_` become ids |
| M3 no boundaries (2) | `S[0-9]{3,}` | FAIL rc=1, S002×4 | yes |
| M4 base regex, `_` not word (12) | `[^[:alnum:]]` | FAIL rc=1, S002×2 | yes |
| M5 trailing `_` allowed (2) | `[[:alnum:]_]*[[:alnum:]]` | FAIL rc=1, S002×1 | yes (`S002_`) |
| M6 leading `_` allowed (2) | `[[:alnum:]][[:alnum:]_]*` | FAIL rc=1, S002×1 | yes (`_S002`) |
| M7 locale pin removed (3) | drop `local LC_ALL=C` and the grep `LC_ALL=C` | PASS | n/a: the caller pins C (`research-gate.sh:2814`) and the control env sets `LC_ALL=C` |
| **M8 scan skipped (1)** | `found_id=1; return 0` before the loop | **PASS** | **vacuous** |

All failures are the intended kind: exit 1 with `FINDING META_SOURCE_NOT_MINED
… source_id=S002` counts. There were no parse errors, setup errors or rc 2.

**Why M1 passes:** the only end-of-value standalone token is ` S001`, and its
literal text appears exactly once. So the base literal-prefix strip never
re-enters a glued `S002` token. This exact source was already `a7-allplus`
"agree" on the buggy round-26 gate (`round-26/falsify/FRegistryIdBoundary.md`,
fixture table). The control therefore preserves the underscore boundary but
cannot see the C3 rescan repair. M1 is killed by sibling controls instead:
`nonstandalone-duplicate` (`ref S002x and S002`), `glued-before-terminal` and
`glued-repeat-duplicate`.

**Why M8 passes:** `S001` is mined and clean, so it emits nothing. The control
has no positive assertion (`required=()`) showing that the registry scan ran.

## (3) Nearby inputs of the same class

**Landed gate:** 0 disagreements. These sources were checked in C and
en_US.UTF-8, with exact per-id finding multiplicities and rc:

- `xS002 S002x _S002 S002_` (NO_ROW_ID)
- the control plus a trailing ` S002` (1)
- `ref S002_ and S002` (1)
- `ref _S002 and S002` (1)
- `x S002_S003 S002` (1)
- `see S001_S003 and S001` (0)
- `S002__ __S002 S001` (0)
- `___S002___ S001` (0)
- `S001_S002` (NO_ROW_ID)
- `S002_,S002` (1)
- `S002` followed by 100000 `_` then ` S001` (0)
- continuation lines `xS002 / _S002 / S002_ / S001` (0)
- `éS002` and `S002é` (1 each; non-ASCII is a boundary per the ASCII contract)
- `S002＿` (fullwidth low line, 1)
- tab and hyphen boundaries (1)
- `9S002 S0021 S001` (S0021 ROW_MISSING ×1)
- `s002 S001` (0)
- `xS002 S002x _S002 S002_ S002` (1)
- `S002_` followed by CR (NO_ROW_ID)

**Coverage gap (counterexample to the control, not to the gate):** two
underscore-class shapes that base M1 gets wrong appear in no persisted control,
neither in the regression script nor in the selftest
(`research-gate.sh:6450-6467`):

- `ref S002_ and S002`: M1 reports `NOT_MINED S002 ×2`; expected ×1. This is
  round-26 `b11-dup-us`.
- `x S002_S003 S002`: M1 reports `NOT_MINED S002 ×2`; expected ×1.

Impacted axis: calibration (the control's evidential weight). There is no
defect in the landed behavior.

## Smallest safe correction (author lane)

Keep `underscore-glued` unchanged. It is a valid underscore-boundary guard
against M2–M6. Add one sibling with a terminal same-id occurrence:

```python
('underscore-glued-terminal', 'xS002 S002x _S002 S002_ S002', 1, 1),
```

The observed results for this sibling were:

- On the landed gate it gives rc 1 with exactly 1 `NOT_MINED S002`.
- On M1 it gives ×3, on M2 ×3, M3 ×5, M4 ×3, M5 ×2, M6 ×2, and on M8 rc 0 with
  ×0 (`fx/probe-hardened.log`).

So it kills every non-equivalent mutant above, including the reverted round-27
fix. Optionally, also add `required=('verdict=clean',)` to `underscore-glued`
so a skipped scan cannot pass silently.

## Limits

- I did not run the full selftest, the whole regression script, or the
  differentials, because L1 owns those.
- M7 is equivalent under the current call path. I did not test a direct caller
  without `verify_metadata`'s pin.
- The oracle encodes the ASCII contract. Non-ASCII adjacency counting as a
  boundary is a spec choice, not something I tested as a defect.
- No network, no host files, no lane edits other than this report.
