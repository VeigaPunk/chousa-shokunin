# Round 35 / w2 / MutPinRefusals — refusal completeness for `RESEARCH_GATE_GREP`

Seat: mutation tester (leaf). Scope: C1 operability, malformed-override refusal.
Date: 2026-10-23. Lane read-only; all runs in
`/tmp/hyaku/chousa-r35/w2/MutPinRefusals/`; artifacts in
`.ufo/waves/round-35/w2/MutPinRefusals/`.

Gate scored (copy, byte-identical to the landed file):

```
sha256sum research-gate.sh                    1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617
sha256sum <lane>/tools/research-gate.sh       1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617
```

## What I ran

Driver `probe.py` (copied to my dir) builds a three-claim fixture
(`K1` supported/match, `K2` mutated/mismatch, `K3` glued/mismatch) and runs

```
env PATH=/usr/local/bin:/usr/bin:/bin CHOUSA_GREP_PIN_ECHO=1 [RESEARCH_GATE_GREP=<case>] \
  timeout 30 strace -f -qq -e trace=openat -o trace.log \
  bash research-gate.sh verify-claims <fixture>/claims.jsonl --root <fixture>
```

per case; it records exit code, stdout bytes, `CLAIM` lines, first stderr lines,
the `GATE_GREP:` echo, and **claims-path `openat` count** as the
"no record was read" detector. Positive controls (`P1` unset, `P2` valid
override) prove the detector sees a read: `claims_opens=2`, 3 `CLAIM` lines, rc 1.

## Six assigned cases (all refused, no record read)

| case | override | rc | claims opens | CLAIM lines | stderr / echo |
|---|---|---|---|---|---|
| P1 unset (control) | — | 1 | 2 | 3 | `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` |
| P2 valid (control) | `/usr/bin/grep` | 1 | 2 | 3 | `GATE_GREP: ... source=override ...` |
| A empty | `` (set, empty) | **1** | **2** | **3** | `GATE_GREP: ... source=default ...` |
| B comma | `,` | 2 | 0 | 0 | `GREP_PROVENANCE refused: override is not an absolute path (candidate=,)` |
| C slash | `/` | 2 | 0 | 0 | `... not a regular file (candidate=/)` |
| D directory | `/tmp/…/cand/a-directory` | 2 | 0 | 0 | `... not a regular file (candidate=…)` |
| E FIFO | `/tmp/…/cand/fifo` | 2 | 0 | 0 | `... not a regular file (candidate=…)` (no block: 0.03 s) |
| F 0-byte | `/tmp/…/cand/zero-byte` | 2 | 0 | 0 | `... not executable (candidate=…)` |
| F′ 0-byte +x | `/tmp/…/cand/zero-byte-exec` | 2 | 0 | 0 | `... does not report GNU grep: <no version> (candidate=…)` |

Extra shapes (cheap, same detector): `/usr/bin/grep/` → rc 2 "not a regular
file"; `/dev/null` → rc 2 "not a regular file"; symlink to `/usr/bin/true` →
rc 2 `does not report GNU grep: true (GNU coreutils) 9.12`. No case exited 0/1
except A, and A is the assignment's own carve-out (below).

Refusal ordering is proven independently of the counter: with override `,` and
a **nonexistent** claims path the only output is the pin refusal, rc 2
(`grep_pin_init` at `tools/research-gate.sh:8039` runs before mode dispatch);
with the same nonexistent path and an empty/unset override the gate reaches
claims mode (`research-gate: claims file not found`, usage, rc 2). Refusal
precedes any record access, matching `tools/research-gate.sh:341-343`.

## `RESEARCH_GATE_GREP=` (set, empty): treated as UNSET, not refused

`tools/research-gate.sh:371` tests `[[ -n ${RESEARCH_GATE_GREP:-} ]]`, so an
empty value takes the default branch: pin `/usr/bin/grep`, echo
`source=default`, read the record, exit 1 — byte-identical in rc/stdout/echo to
the truly unset control (`P1` vs `A`). Both the assignment rule (UNSET or
refused) and C1's frozen text allow this; nothing in `corpus/evidence/round35/claims.md`
promises refusal of an empty override.

Honesty note (wording, not behavior): `corpus/knowledge/grep-pin-r35.md:36`
says "`RESEARCH_GATE_GREP`, **when set**, must be an absolute path, a regular
file and executable". In shell terms an empty variable *is* set
(`[[ -v RESEARCH_GATE_GREP ]]` → true, measured), so the doc's "when set" is
broader than the implemented "when non-empty". The implementation is the safe
one and `source=default` in the echo makes the decision auditable; the doc
should say "when set to a non-empty value". Not a claim violation.

## Surviving mutant M1 — the counter cannot see a read-before-refusal

Mutant (`mutant-m1.sh`, output-identical, built from the pinned copy): three
lines before `grep_pin_init` open the record when an override is present.

```
if [[ -n ${RESEARCH_GATE_GREP:-} && -n ${RECORD_ARG:-} && -f ${RECORD_ARG:-} ]]; then
  head -c 1 -- "$RECORD_ARG" >/dev/null 2>&1 || true   # read, then refuse
fi
```

| bytes | sha256 | detector |
|---|---|---|
| pristine copy | `1f2fb4f5…ef617` | openat on claims fixture = **0**, rc 2 |
| mutant M1 | `147ded031b9443098c874f8ae19a07113d31943477e1e993b69abd6cfe0e70ee` | openat on claims fixture = **1**, rc 2, stdout 0 B |

Detector output on the mutant with override `,`:
`research-gate: GREP_PROVENANCE refused: override is not an absolute path (candidate=,)`,
stdout 0 bytes, `claims_opens=1` (`m1-trace.log`).

Counter on both, same seed:

```
C1_TMP=<scratch> python3 corpus/evidence/round35/c1-count.py --gate <copy> --seed 3599 --receipt <dir>/c1-{pristine,m1}-s3599.json
c1-pristine-s3599.json  GREP_PIN_MATCH=9/9 predicate_holds=True gate_sha256=1f2fb4f5…ef617
c1-m1-s3599.json        GREP_PIN_MATCH=9/9 predicate_holds=True gate_sha256=147ded03…70ee
```

**Verdict: SURVIVED (coverage finding).** S4/S5/S6 assert only
`rc == 2 and "GREP_PROVENANCE" in err` (`corpus/evidence/round35/c1-count.py:231,237,244`);
none checks that the refusal precedes a record read, and none checks stdout is
empty. C1's *scored* predicate is about provenance, which the mutant does not
break — the pin is still resolved and verified — so this is not a MEETS
finding against P1. It is a gap between the claim record's stronger text
("refused **before any record is read**", `corpus/knowledge/grep-pin-r35.md`,
item 3; `tools/research-gate.sh:342`) and what the counter measures. The
landed gate is clean on the ordering (0 opens in every refusal above); the
counter simply could not tell.

## Other observations (not mutants)

1. **`--version` probe has no timeout.** `tools/research-gate.sh:361` runs
   `v=$("$cand" --version 2>/dev/null | head -n 1 || true)`. An executable,
   absolute override that never answers (`#!/bin/sh` + `exec sleep 30`) makes
   the gate block: outer `timeout 5` → rc **124**, 0 B stdout, 0 B stderr,
   `claims_opens=0` (`hang-trace.log`). It neither refuses nor proceeds, so
   "refuses a pin it cannot verify" is not universal. Low severity (the counter's
   own 300 s `GATE_TIMEOUT_S` would score it `predicate_holds=false`, so it
   cannot fake 9/9), but it is the one candidate class the check cannot terminate on.
2. **Self-reported provenance limit is real and recorded.** A wrapper printing
   `grep (GNU grep) 3.12-liar` then `exec /usr/bin/grep` is accepted:
   rc 1, 3 `CLAIM` lines, echo
   `GATE_GREP: path=…/cand/liar source=override version="grep (GNU grep) 3.12-liar"`.
   This matches the declared limit at `tools/research-gate.sh:348-350`; the echo
   writes the lie into the receipt, which is the intended audit trail.
3. The FIFO case does not open the FIFO (0 opens, 0.03 s) — the `-f` test runs
   before `-x`/exec, so no blocking read path exists for the six shapes.

## Limits

- "No record read" = zero `openat` of the claims path under `strace -f`. `stat`/
  `access` were not traced; [INFERENCE] a byte read is impossible without an open,
  and the positive controls show the detector counts real opens.
- Only `verify-claims` was exercised (pin init is mode-independent, line 8039).
- One host, one GNU grep (`3.12-modified`), no network, no package installs.
- The mutant is an extra file; the pristine scratch copy and the lane file were
  never edited and both still hash `1f2fb4f5…ef617` (restore evidence).

## Verdicts

- **Six assigned malformed overrides: all refused**, rc 2, named
  `GREP_PROVENANCE` reason, zero record opens. No finding.
- **`RESEARCH_GATE_GREP=` empty: UNSET, not refused** (allowed by the rule;
  doc wording "when set" is the only imprecision).
- **M1 read-before-refusal: survived the C1 counter** → counter covers the pin,
  not the claim's "before any record is read" ordering.
- **Hang on a never-answering executable override:** unbounded wait at
  `research-gate.sh:361`.

## Artifacts (all < 1 MiB)

In `.ufo/waves/round-35/w2/MutPinRefusals/`:
`MutPinRefusals.md`, `results.json` (`0a71701c…b660d`), `probe.py`
(`b2add464…554f`), `gate-copy.sh` (`1f2fb4f5…ef617`), `c1-pristine-s3599.json`
(`71395c14…fbf`), `c1-m1-s3599.json` (`1638c6e0…e7e`), `tmp-log-hashes.txt`.
Scratch logs (kept in `/tmp/hyaku/chousa-r35/w2/MutPinRefusals/`):
`m1-trace.log` `7ff29b65…3cf0`, `m1.err` `f66de1a3…f267`, `m1.out` empty
(`e3b0c442…b855`), `hang-trace.log` `3624b364…3927`, `liar-trace.log`
`b5a57d55…621f`, `mutant-m1.sh` `147ded03…70ee`.
