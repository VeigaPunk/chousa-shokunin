# gate-baseline-r8.md — the gate's own behavioral baseline: `--pin`/`--drift` design, the volatile contract, what it catches and what it cannot

source: `tools/research-gate.sh` entering this round
`3ba718bf9207eed70c66b8c849ac43b44c76890785e1576eeb5e795a604166b2` (round-7 bytes, 3666
lines, `VERSION=research-gate-r1`) → **settled**
`46f5ddb39d5fafa220fb584121dba2f4a15e071a91fa42728849f3c7567c6ccd`
(`git diff --numstat` = 523 +, 6 −; 4183 lines; `VERSION` unchanged, so the revision is
distinguished by SHA, not by a version bump). The implementation landed in visible steps between
03:27Z and 03:36Z (observed shas `05f076ac…`, `d1562d6a…`, `fc8695cd…`, `b4dd27a1…`, `ab23ea85…`,
`c1a45a61…`, `02e001ce…`, `30d89dbf…`, `bbd90e84…`, `46f5ddb3…`: docs first, then the pin/drift
section, then selftest cases and guards). All line numbers below are `46f5ddb3…`'s.

verified-at: 2026-10-16T03:30–03:41Z, three arms — snapshot `c1a45a61…` (full battery), snapshot
`bbd90e84…` (post battery), and live lane legs at `30d89dbf…` and `46f5ddb3…` (the settled
bytes). Instruments and raw logs: `$HOME/.cache/chousa-tmp/r8-note/` (ephemeral). A reader
re-running any leg must re-check the gate SHA first.

scope: detection and report only. This seat wrote no lane file but this note; no remediation, no
commit; every fixture, snapshot and mutant of my own lives under `$HOME/.cache`. The lane's own
committed baseline is the receipts-writer's artifact (§5).

## 1. Design at `46f5ddb3…`

Round 7 registered this as the round-8 move: *"the gate's own behavioral baseline (`--pin`/`--drift`
adapted from the sibling lane's proven pattern) — the verification tool's drift becomes
detectable"* (`SCORECARD.md:305-309`). Before it, i.e. at `3ba718bf…`, a gate regression (a mode
silently skipped, an output field changed) was only catchable by reading receipts after the fact:
`--pin`/`--drift` were unknown flags (measured: `research-gate: unknown flag: --pin`, exit 2, no
file written) and `corpus/evidence/` held no baseline.

Contract (declared in the file header, `tools/research-gate.sh:153` ff.; usage `:266`, `:316`):

| element | behavior | site |
|---|---|---|
| `--pin <path>` | runs the canonical capture (§ below), normalizes it, writes the baseline text file; prints `GATE_PIN: ok path=… gate_sha256=…`; exit 0 — pinning a DRIFT run is still a pin; exit 2 when the capture or the write fails | `run_pin` `:2410-2444` |
| `--drift <path>` | re-runs the same capture, normalizes with the **current** rules, byte-compares against the baseline body: equal → `GATE_DRIFT: none` exit 0; differ → `GATE_DRIFT: <changed tokens>` exit 1; baseline missing/unreadable/malformed, or a failed capture → message on stderr, exit 2. Writes nothing | `run_drift` `:2446-2504` |
| guards | `--pin`/`--drift` accept only a baseline path (a record, `--claims`, `--json`, `--root` → usage, exit 2); both modes at once → exit 2 | `:4144-4146`; selftest case `pin-drift-exclusive` `:4089` |
| selftest | cases 75–85 are the pin/drift arms (:4055–4089); cases 1–74 keep their numbers, names and exits | tpin `:3989`, tdrift `:4016` |
| no verdict line | neither mode prints a `RESEARCH_GATE:` line — their contract is the `GATE_PIN:`/`GATE_DRIFT:` line plus the exit code, so a consumer counting verdict lines cannot mistake a baseline operation for a record verdict | `:153-170` |

Design decisions that carry weight:

- **The canonical invocation is hermetic by construction.** `gate_pin_fixture` (`:2220-2268`)
  writes a fresh temp fixture — `record.md` with every r6 section and one deliberately dangling
  sweep binding (`C9`), `claims.jsonl` with one supported claim, `lib/primary.md`,
  `noise/chat-export-sources.md` — and `gate_canonical_capture` (`:2270-2305`) runs
  `verify-all record.md --claims claims.jsonl --json manifest.jsonl --root .` inside it, then
  removes it. Every printed path is relative, so the capture is byte-stable wherever the gate is
  run; the fixture is never committed. The one integrity finding is deliberate, so the capture
  covers `SECTION` (both CLEAN and DRIFT), `FINDING`, `VERIFY_ALL`, the composed verdict, and the
  `--json` manifest line.
- **Captures are frozen before anything compares them**: the run writes to a file (never read
  from a live pipe), the file is normalized into a variable, and the fixture is removed before
  any report prints (`:2194-2198`). A capture that returns anything but rc ∈ {0,1}, exactly one
  `RESEARCH_GATE` line and one manifest line is exit 2, never a false `none` (`:2287-2304`).
- **Behavioral, not revision-bound**: the manifest's `gate_sha256` is masked, so the comparison
  is over behavior (mori r10's `script_sha256` rule). Measured: a comment-only change in a gate
  copy drifts `none`, exit 0.
- **The masked set travels in the artifact** (header `# volatile_fields=…`), so a `none` is
  auditable: the baseline says what was not looked at. A baseline whose declared list differs
  from the current one is itself drift (`volatile_fields`) — mori's r10 refinement, carried.

## 2. The volatile contract, and why each entry is in it

The masked set is `ts gate_sha256` (`GATE_DRIFT_VOLATILE_FIELDS`, `:2199`), recorded verbatim in
every baseline header.

| field | rule | why (measured) |
|---|---|---|
| `ts` | shape-scoped: `ts=<YYYY-MM-DDTHH:MM:SSZ>` (header line) and `"ts":"…"` (manifest line) → `<V>` (`:2212-2215`) | the single live input of the canonical invocation. Measured before landing: two hermetic `verify-all` runs with different clocks differ in exactly this token; the lessons-distiller's inventory measured 1 of 16 field tokens churning live, 0 when `CHOUSA_NOW_EPOCH` is pinned. Shape-scoped, so a malformed timestamp keeps its bytes and surfaces: a `ts=epoch-…` mutant drifts `GATE_DRIFT: ts`, exit 1. |
| `gate_sha256` | `"gate_sha256":"…"` → `<V>` (`:2215`) | the manifest's revision stamp; masked so the pin compares behavior, not revision. Measured: comment-only mutant → `GATE_DRIFT: none`, exit 0. |
| everything else | compared unmasked | including `record_sha256` (the fixture bytes are part of the behavior — a change to the fixture moves it) and every contract word (`VERSION`, `mode=`, `record=`, `claims=`, `root=`, `state=`, `verdict=`, `findings=`, `drift=`, `tally=`, `severity=`, `surface=`, `obs=`, section/manifest keys), so editing one is drift. |

Measured rationale, and the lineage's inversion:

- **Churn is absorbed, not assumed away.** Pin with the live clock, then drift: `none`
  immediately, `none` after 61 s of live churn, `none` when the second run's clock is 7200 s
  ahead (the capture unsets `CHOUSA_RECORD`/`CLAIMS`/`STRICT`/`ROOT`/`AGGREGATOR_ERE` but inherits
  `CHOUSA_NOW_EPOCH`, `:2282-2286`). Every one of those runs had a different `ts` in its bytes;
  the mask is what makes them equal — a falsifiable statement, not a tautology, because the same
  comparator exits 1 on a one-field tamper (§3).
- **The contract is invocation-derived, not copied from mori.** The sibling lane's census reads
  host state, so its volatile set is six special rules plus a counter-class list (~47 % of its
  schema; `../mori-shokunin/corpus/knowledge/drift-pin-r10.md` §2). This gate reads only the
  record, its fixture and the clock, so the set is two fields — and zero if the clock is pinned,
  which the canonical invocation does not do (it keeps the live clock and declares the `ts` mask
  instead; the pin records `pinned_ts`). The transferable rule is "derive the set from the
  invocation"; copying mori's list onto this schema would mask ~94 % of stable tokens.
- **Direction of safety** survives as-is: prefer a false red (a named token a human reads) over a
  false green, and declare the masked set so the reader can see the blind spot.

## 3. What it catches — measured

All legs below are mine (full battery at snapshot `c1a45a61…`, post battery at `bbd90e84…`), each
a fresh process against the shipped CLI; raw logs under `$HOME/.cache/chousa-tmp/r8-note/`.

| probe | result (verbatim) | exit |
|---|---|---|
| pin → drift, live clock | `GATE_DRIFT: none` | 0 |
| drift after 61 s of live churn | `GATE_DRIFT: none` | 0 |
| drift with the clock 7200 s ahead | `GATE_DRIFT: none` | 0 |
| baseline body tampered (`unresolved=1` → `0` in the SECTION integrity tally) | `GATE_DRIFT: unresolved` | 1 |
| **mode-skip mutant** (copy with `integrity` dropped from `VA_ORDER`, `:2041`) | `GATE_DRIFT: -FINDING:REF_UNRESOLVED -SECTION:integrity -refs -resolved -unresolved REJECTIONS_OK drift drift-sections drift_sections exempt findings name native run sections sections_run state tallies verdict` | 1 |
| **output-field mutant** (copy with `INTEGRITY refs=` renamed to `refs_count=`) | `GATE_DRIFT: -refs native tally` | 1 |
| volatile list rewritten in a copy of the baseline | `GATE_DRIFT: volatile_fields` | 1 |
| malformed `ts` (copy printing `ts=epoch-…`) | `GATE_DRIFT: ts` | 1 |
| baseline missing | `research-gate: --drift baseline missing: …` | 2 |
| baseline empty / junk | `research-gate: --drift baseline malformed (magic line absent): …` | 2 |
| `--pin` or `--drift` without a path; `--pin PATH --root .`; `--pin a --drift b` | usage refusal | 2 |
| comment-only change in a gate copy | `GATE_DRIFT: none` | 0 |

The mode-skip row is the round's central falsifiable claim measured end to end: **the same mutant
passes every composed verdict line as CLEAN with exit 0** (measured at `3ba718bf…` pre-pin, and
again as the `--drift` driver at the settled bytes), because a skipped section's finding never
reaches the roll — while the byte pin names the vanished `SECTION:integrity`, the vanished
`FINDING:REF_UNRESOLVED`, and every count that moved (section and manifest keys). The
output-field row is the other half: a renamed tally token moves no verdict either, and the pin
names `-refs` plus the composition/manifest strings that carried it (`native`, `tally`).

## 4. What it cannot — measured and read

1. **Exit-code-only regressions.** A copy whose `verify_all` always returns 0 (`return 1` →
   `return 0`) drifts `GATE_DRIFT: none`, exit 0: the capture's rc is only sanity-checked
   (`rc ∈ {0,1}`, `:2290`), never compared. A regression that moves the printed roll is caught; one
   that moves only the process exit is not. (Candidate follow-up: record the capture rc in the
   baseline header.)
2. **Behavior outside the canonical invocation.** Two copies changing `AGG_ERE`'s default — one
   dropping `wikipedia`, one dropping even `chat-export-sources` — both drift `none`, exit 0: the
   canonical fixture never exercises that code path, so a behavior change confined to other
   records is invisible. The pin freezes one invocation's surface, not the gate's semantics on all
   inputs.
3. **Oracle strength.** A copy with a selftest assertion removed (the `volatile_fields` want-token
   from case 81) runs `PASS (84 cases)` with byte-identical case lines to the unmutated copy
   (measured with both copies co-located so their environments were equal). The PASS set contains
   case names and exits, never assertion text; the lessons-distiller's m1 (a `verify-all` want
   token removed) measured the same for the fixture surface.
4. **A semantic regression inside a stable field** — the class the round names. By construction:
   any internal change that leaves the normalized canonical capture byte-identical (a masked
   value, a code path the fixture never takes, an assertion, an exit code) is unobservable to the
   pin. What the pin guarantees is the converse, and it is worth stating exactly: *if the
   canonical capture's unmasked bytes move, the move is named.*
5. **The masked fields themselves** are blind spots by design (`ts`, `gate_sha256`), bounded by
   the fact that the masked set is declared in the artifact and a changed list is itself drift.
6. **Per-row movement outside the pinned surface.** The lessons-distiller's span-shift probe:
   moving one claim's `at=line:1` to `at=line:2` leaves the composed `verify-all` bytes identical
   while a solo `verify-claims` run names it. A composed-surface pin inherits exactly the composed
   surface's resolution.

No behavioral comparison can see §4.3; the ritual must therefore pair the drift check with a
source review of the gate at the same SHA (mori note §5.6; the lessons-distiller's m1 and m3 are
the measured reason).

## 5. The committed lane baseline (receipts-writer's artifact)

| fact | value |
|---|---|
| path | `corpus/evidence/gate-baseline-r8-20261016T033757Z.json` |
| baseline sha256 | `1c81a6cb34543bb99c8797a7a0dd8dfbd1f13e3d86ec5b81aa0c7249381a8426` (2988 B) |
| header `pinned_ts` | `2026-10-16T03:38:57Z` (the capture run's own clock; the filename stamp is `20261016T033757Z`) |
| header `gate_sha256` | `46f5ddb3…` (the settled bytes) |
| header `volatile_fields` | `ts gate_sha256` |
| written by | `bash tools/research-gate.sh --pin corpus/evidence/gate-baseline-r8-20261016T033757Z.json` → `GATE_PIN: ok`, exit 0 |

Despite the `.json` suffix the file is the `chousa-gate drift baseline v1` **text** format (header
comments, `# --- canonical output follows ---`, the masked canonical capture, `# --- json manifest
line follows ---`, the masked manifest line). A reader reaching for `jq` will fail; naming
observation, not a contract defect.

My own checks of the committed artifact (not the receipts-writer's): at the settled `46f5ddb3…`,
`bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json` →
`GATE_DRIFT: none`, exit 0. The committed body is byte-identical to the body of my independent pin
at the prior revision `bbd90e84…` (compared marker-to-end), and that `bbd90e84…`-pinned baseline
also reads `GATE_DRIFT: none` at the settled bytes — behavior did not move across the revision
pair. That is the design's central claim on a live case: the revision moved, the normalized
behavior did not, and the pin reports behavior.

Re-run recipe (cwd = lane root; the same invocation shape the receipts use):

```sh
sha256sum tools/research-gate.sh                       # 46f5ddb3… is the sha the header records
sha256sum corpus/evidence/gate-baseline-r8-20261016T033757Z.json   # 1c81a6cb…
bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r8-20261016T033757Z.json
#   expect: GATE_DRIFT: none  (exit 0) while the canonical invocation's behavior is unchanged;
#   a red result names changed tokens, e.g. -SECTION:integrity  /  -refs native tally  /
#   ts  /  volatile_fields
bash tools/research-gate.sh --pin /tmp/<new>.txt       # re-pin deliberately, with a reason
```

## 6. Admission ritual and cost (adapted from mori r10 §5)

1. **Pin on admit**: after the round's acceptance battery passes, at the admitted gate bytes:
   `--pin corpus/evidence/gate-baseline-r8-<STAMP>.json`; record path, `pinned_ts`, baseline sha
   and pinned `gate_sha256` in the verdict. Round 8 did this (§5).
2. **Drift before each new round**: the first gate measurement of a round is `--drift <the lane
   baseline>`. A red result is a named finding in the round's before-state: either an intended
   change (re-pin, recorded, with the reason) or a regression the round must address. The failure
   mode to avoid is re-pinning to turn red green.
3. **Re-pin only as a recorded act with a reason.** This baseline does not age with the host (the
   gate reads no host state), so a red result is a gate behavior change, not fleet drift — which
   makes the re-pin discipline stricter here than mori's, not looser.
4. **Run the whole battery in acceptance**, because a pin that only passes the first leg proves
   nothing about the comparator: pin → drift (`none`); drift after ≥60 s of live clock churn
   (`none`); drift from a one-field tamper (exit 1, field named); drift from a mode-skip or a
   field-rename mutant (exit 1, section/field named); drift on missing/empty/junk (exit 2); drift
   against a rewritten volatile list (exit 1 `volatile_fields`). Measured this round:
   `RESEARCH_GATE_SELFTEST: PASS (85 cases)` exit 0 at the settled bytes (cases 75–85 are the
   pin/drift arms, `:4055-4089`); cases 1–74 byte-identical (`cmp` clean against
   `corpus/evidence/integrity-r7-20261016T030552Z-selftest.log`); prior modes held (claims 17/17,
   chain 17/22, full-r6 CLEAN, broken fixture DRIFT, r1 archives 3/3); strace over `--pin` and
   `--drift` shows 0 network syscalls (2 pin/drift probes, `-e trace=network`).
5. **Cost**: a capture is a few seconds of wall (measured 2–6 s at wave load); the selftest
   ≈ 50–60 s (measured 47 s and 58 s runs). Cheap enough to run in every acceptance battery.

## 7. What this note does not claim

- No remediation, kill or config change; no commit; the only lane file this seat wrote is this
  note; snapshots, mutants and logs live under `$HOME/.cache/chousa-tmp/r8-note/` and are
  ephemeral by design.
- The gate moved during the round (`3ba718bf…` → ten observed shas → `46f5ddb3…`). All design
  claims are read at `46f5ddb3…`; the battery legs ran at `c1a45a61…` (full) and `bbd90e84…`
  (post), with live lane legs at `30d89dbf…` and `46f5ddb3…`. A reader re-running any leg must
  re-check the SHA: a later revision that changes behavior is reported by `--drift` itself
  (`volatile_fields` when the contract moves; named fields when the output does).
- Environment caveat, measured: running `--selftest` from a scratch copy whose implied `LANE_ROOT`
  (the copy's parent directory) contains the selftest's `OUTSIDE_FILE` flips the three
  out-of-corpus cases to FAIL — observed (3/84 FAIL) with the copy at
  `$HOME/.cache/chousa-tmp/r8-note/` and `TMPDIR=$HOME/.cache/chousa-tmp`; the same copy one
  directory deeper (implied lane root `…/r8-note`, `OUTSIDE_FILE` outside it) passes 84/84. The
  lane-path selftest is unaffected. This is the `LANE_ROOT` boundary fallback the r8 lesson
  warned about, not a gate defect.
- The pin verifies the canonical invocation's output on a fixture the gate writes itself; it does
  not verify records, other modes on other inputs, the selftest's assertion strength (§4.3), or
  the exit-code contract (§4.1).
- The lane baseline and its receipts are the receipts-writer's artifacts; this note cites them and
  adds independent readings of its own, not their verification.