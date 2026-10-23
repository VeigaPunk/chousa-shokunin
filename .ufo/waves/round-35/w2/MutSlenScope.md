# MutSlenScope — R1 kill test: pre-fix vs landed `slen` (round 35, wave 2)

Date 2026-10-23. Seat: mutation tester. Item: attack repair R1 only. C1/P1 and
C2/P2 re-derivation belong to other seats; I did not run their counters.

## Pinned inputs (read-only; hashed before and after the runs, unchanged)

| file | sha256 |
|---|---|
| `tools/research-gate.sh` (landed) | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` |
| `.ufo/waves/round-35/repairs/base-gate.sh` (r34 blob) | `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` |
| `.ufo/waves/round-35/repairs/slen-probe.sh` | `0938c4c21e9b4e311a6786204f954a6a7351e861c3597db665db0ce47988ce60` |

Opened: `corpus/evidence/round35/claims.md`, `repairs/slen-probe.sh`,
`c1-count.py` header, `c2-count.py` header, `tools/mechanism-witness.py` header.
(`sha256sum` re-run after all runs: same three digests.)

## Scratch and mutant construction

Scratch `/tmp/hyaku/chousa-r35/w2/MutSlenScope/`, `TMPDIR` under it. Variants are
copies of the landed gate with exactly one matcher-local change each; diffs are
archived in my report directory. No lane production file was written; every
experiment ran in `/tmp`.

| variant | matcher local form (landed line 1701/1706-1707) | sha256 of variant |
|---|---|---|
| (a) pre-fix | `local hay=$1 span=$2 slen=${#span} chunk pattern occurrence offset resume=0` | `a9116812813c9852be869a32503b11250613ad916a8b675f522696eb48665bd8` |
| (b) landed control | `local slen` + `slen=${#span}` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` |
| (c) argument length | `local slen` + `slen=${#2}` | `4a312fb9b52f3cb4a5049a3c23ebccc4aecccd5592d8957507c79335da734ddf` |
| (c2) literal `$2` | `local slen` + `slen=$2` | `22f9ef22bfa37a1656f287c88416ea3438068d31432d7540add1ea2e597907b8` |

`bash -n` parses all four; diff vs landed is the single hunk shown in
`variant-*.diff` (variant a's replacement text is byte-identical to `base-gate.sh:1632`).

## Probe sweep (assigned detector)

`bash .ufo/waves/round-35/repairs/slen-probe.sh <gate>`, `TMPDIR=$SCRATCH/tmpdir`,
each call under `timeout 300`. Verbatim receipt: `receipt-probes.txt`
(sha256 `ddc26ead…2fe6`).

| gate | rc | output |
|---|---|---|
| base-gate.sh | 1 | `SLEN_PROBE offsets=0 first=` |
| landed (b) | 0 | `SLEN_PROBE offsets=1 first=5` |
| (a) pre-fix | 1 | `SLEN_PROBE offsets=0 first=` |
| (c) `slen=${#2}` | 0 | `SLEN_PROBE offsets=1 first=5` |
| (c2) `slen=$2` | 1 | `matcher.sh: line 72: w0001: unbound variable` + `SLEN_PROBE offsets=0 first=` |

### Verdicts on the three formulations

- **(a) is killed by the probe**: offsets 0 vs the probe's required 1. Mutant dead.
- **(c) `slen=${#2}` is an equivalent repair** at probe level, not a wrong one:
  `$2` is the function's own untampered positional parameter, and
  `local hay=$1 span=$2` does not alter `$2`, so `${#2} == ${#span}` on every
  call. It passes exactly like the landed form. Caveat (intent, not behaviour):
  it reads the raw argument rather than the local, so it would silently diverge
  if the local ever normalized `span`; as shipped, equivalent.
- **(c2) `slen=$2` is a wrong repair**: the gate runs `set -euo pipefail`
  (`tools/research-gate.sh:292`), so `slen` holds the span text and
  `${hay:offset:slen}` (line 1713) re-evaluates it as an arithmetic variable
  name → `nounset` failure. Probe: `w0001: unbound variable`, 0 offsets.

### Control: the probe's kill condition is dynamic-scope divergence, not an artifact

A copy of the probe with the visible decoy set to the argument itself
(`span=$span_long`, archived as `slen-probe-decoysame.sh`) yields
`SLEN_PROBE offsets=1 first=5`, rc=0 **on (a) as well as on (b)**. So (a) only
fails the probe when the caller-visible `span` differs from the argument — the
exact defect — and the unmodified probe is discriminating.

## Public path does not catch (a): selftest PASS

Run in a scratch lane root `lane/` (`tools/` + byte-copied `PROVINCE.md`, so
case 127 resolves `$LANE_ROOT/PROVINCE.md`; all other fixtures are built under
`WORK`):

```
cd /tmp/hyaku/chousa-r35/w2/MutSlenScope/lane
TMPDIR=.../tmpdir timeout 900 bash tools/research-gate.sh --selftest
```

- (a) pre-fix: **rc=0**, `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`,
  54 s. Dead-zone cases 254/255/256 (`ok-case 254 claims-deadzone` etc.) all pass.
- (b) landed control: rc=0, same PASS, 54 s. The two logs are **byte-identical**
  (`5311643cc95e…`), i.e. the 256-case public battery cannot distinguish (a)
  from (b) at all.

Why the defect was latent (source-level): `tok_span_offsets_chunk` has exactly
one call site, `tools/research-gate.sh:1669`, inside `tok_span_offsets`, whose
own `local hay=$1 span=$2` is line 1667. That caller passes `"$span"`, a value
equal to the chunk matcher's `$2` on every production path; the `local`
one-liner's right sides are all expanded before assignment, so pre-fix
`slen=${#span}` nevertheless saw the caller's `span` — the same string. Hence
no output difference and no selftest difference today. Expansion rule demo:
`bash -c 'f(){ local a=$1 b=${#a}; echo $b; }; f hello'` prints `0`.

Contrast — the public battery is not blind to all `slen` breakage: with (c2)
`slen=$2` it **FAILs** (`RESEARCH_GATE_SELFTEST: FAIL (3/256 cases)`, rc=1), on
exactly `claims-deadzone`, `claims-deadzone-line`, `claims-deadzone-edge`, with
`line 1713: w0001: unbound variable` in the case body. So the public path
catches the wrong repair but not the latent dynamic-scope misread.

## Verdict

- Mutant (a): **KILLED by the assigned `slen` probe** (offsets=0, expected 1);
  **SURVIVED the 256-case public selftest** (PASS, identical log to landed).
  R1 describes a real dynamic-scope coupling, the probe is a valid discriminating
  detector, and the claimed latency (caller's `span` equals the argument on every
  landed path) is confirmed at `research-gate.sh:1667,1669`.
- (b) landed passes probe and selftest — matches the round's R1 statement.
- (c) is an equivalent repair; (c2) is a wrong repair and is caught publicly.
- No MEETS finding against P1/P2 follows from this item; R1 is repair evidence,
  not a scored claim, and I did not re-measure C1/C2.
- Coverage finding (not permission to change the contract): the selftest has no
  case that calls the chunk matcher through a caller whose `span` differs from
  the argument; the probe is the only guard on that surface.

## Limits

- The probe is structural: it `sed`-extracts `tok_hex_pattern()` and the
  `TOK_DIRECT_SPAN_MAX=` block and calls the functions with a synthesized global
  `span`. A gate that renamed or reordered the matcher would read as
  `offsets=0` — a false kill. Not triggered here (all three functions and the
  block unchanged; `bash -n` guard passed).
- The probe scores one 32766-byte span in one call; it does not model a caller
  that normalizes the span, which is the only way pre-fix code goes live.
- Selftest runs used a minimal scratch lane root, not the repo root; the only
  lane-root file the selftest reads (`PROVINCE.md`, case 127) was byte-copied
  (`cf7826a4…43ec`).
- [INFERENCE] `slen` is read only at lines 1707/1713/1715 of the landed matcher
  (grep: four occurrences); no other subsystem depends on the coupling.
- No installs, no network, no signals; PIDs all short-lived under `timeout`.
- Note: `git status --porcelain` shows concurrent peers' writes under
  `corpus/` (QUALITY.md, SOURCES.md, new round-35 knowledge files, `__pycache__`);
  none are mine.

## Artifacts (in `.ufo/waves/round-35/w2/MutSlenScope/`, all < 1 MiB)

| file | sha256 |
|---|---|
| `receipt-probes.txt` | `ddc26eadb47489f206fb682a36c49645e8941c5ca0e0becd64a1a5c223b02fe6` |
| `selftest-a.log` | `5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12` |
| `selftest-b.log` | `5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12` |
| `selftest-c2.log` | `52902a6c087ee6f44f460f73ed5050eab54db647dcdae02df68c980320b21798` |
| `slen-probe-decoysame.sh` | `06610df4c4f7dfa64b31b9e0583ae4cb2bbee881f63761eca255ff10067baf76` |
| `variant-a-prefix.diff` | `e8662fbf01b2266b689da2f0ccac7f0099addf58c65e9684c0ba4823f7823b28` |
| `variant-c-arglen.diff` | `865efd9feb24def7560eecf8289882ebfc6d74a81a985a84f07ec5bb397af407` |
| `variant-c2-literal.diff` | `b349f836af29833747da01b97ac89609d43743e7f0644a3ce53469bb631a5551` |
| `sha256s.txt` | `9a62ed3ffb619c59773390fb480c962a793bd707452347586d011f6a4ec627ce` |

Variants, full logs with `time` lines and the scratch `lane/` tree remain at
`/tmp/hyaku/chousa-r35/w2/MutSlenScope/` (variant hashes above; logs copied).
