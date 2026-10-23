# MutGrepPinEngines — round 35 w2, C1 probe: correct non-grep matchers vs the grep pin

Date 2026-10-23. Lane base `e87c5d7ea2dbf3730b36a3961de3f06261d015e4` (clone
`/tmp/hyaku/chousa-r35/w2/MutGrepPinEngines/lane`, HEAD verified). Scored gate
`tools/research-gate.sh` sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`
(pinned, unchanged before and after). Counter
`corpus/evidence/round35/c1-count.py` sha256
`da207fd725658b84469ce1fe540a7b94fcb1027cef49da376a8d7ac19ac715e3`, never edited, run with
`C1_TMP` inside my scratch. No production file was written; no subagent dispatched.

## Verdict

**MEETS — two mutually independent engines (V-A bash glob, V-B awk index) score
`GREP_PIN_MATCH=9/9` on two fresh seeds while the pinned binary receives zero
matcher queries.** The counter gives full C1 credit to a gate whose direct
matcher never execs the thing C1 claims to pin. V-C (pin enforcement actually
removed) is killed 0/9, so the counter is not vacuous: the leak is precisely
*pin present at startup, unused by the matcher*.

## Mutants (all built from the pinned clone gate; diffs are single-function)

| id | direct matcher (`tok_span_offsets_direct`) | pin block | sha256 |
|---|---|---|---|
| V-A | bash glob: `[[ $rest == *"$span"* ]]`, `${rest%%…}` / `${rest#…}` offset loop | untouched | `fd6d5a8ea9d4288370d9ef2d26dfd7bdf04ee227c5a9d55a4bf334d9de837c53` |
| V-B | `awk 'BEGIN{RS="\0"; getline h; getline s; … index(substr(h,p),s) …}'` | untouched | `9040dcba3fdb1f6948dad28d04fcc8ef190e505a7166e954876883c9f8f07772` |
| V-C | `python3` `bytes.find` loop over `hay\0span\0` | enforcement removed (wrapper defanged, `grep_pin_init` call removed; dead defs remain) | `07e8b9f42ade9b87f01837a9bca5dda1005d53e4189f70470b1af83b098ce0f9` |
| V-D | untouched | untouched, entry tag only (`CHUNK_TAG`) in `tok_span_offsets_chunk` | `891dab975f6ae0429e6294ea994047716acea85cfaffc3045b4e4cc0b07dbbbe` |

All four pass `bash -n`. Helpers: `recorder-grep.sh` (logs argv, execs
`/usr/bin/grep`, so it *reports* GNU grep), `saboteur-grep.sh` (reports GNU grep
3.12, answers only `--version` and the one-byte capability probe, never
matches), `plus_fixture.py` (imports the committed counter's `make_fixture`).
Full diffs are recoverable from the artifacts (variants vs `lane/tools/research-gate.sh`).

## Detector runs (`python3 c1-count.py --gate <abs> --seed N --receipt …`)

Each invocation runs one reference + S1–S9 (10 gate runs). Receipt paths in this
report are relative to `.ufo/waves/round-35/w2/MutGrepPinEngines/` (scratch twin:
`/tmp/hyaku/chousa-r35/w2/MutGrepPinEngines/receipts/`).

| gate | seed 3521 | seed 3523 | receipt |
|---|---|---|---|
| base (1f2fb4f5…) | 9/9, rc 0 | 9/9 | `receipts/base-s3521.json`, `base-s3523.json` |
| V-A | **9/9, rc 0** | **9/9** | `receipts/vA-s3521.json`, `vA-s3523.json` |
| V-B | **9/9, rc 0** | **9/9** | `receipts/vB-s3521.json`, `vB-s3523.json` |
| V-C | 0/9, rc 1 | 0/9 | `receipts/vC-s3521.json`, `vC-s3523.json` |
| V-D | 9/9, rc 0 | — | `receipts/vD-s3521.json` |

Every receipt parses as JSON with `predicate_holds=true` exactly for base/V-A/V-B/V-D
(`reference_sane=true` in all runs, including V-C); each receipt records the gate
sha256 of the gate actually scored. Seed-3523 runs were piped through `head -1`, so
Python raised `BrokenPipeError` on the per-scenario print *after* the receipt was
written; the receipts are complete and valid (checked by parsing).

Independent corroboration (reported by `chousa-r35-w2-CritClaimSizing`, not run by
me): its own V-A replay at seed 353505 scored 9/9, and its recorder showed 0
full-span queries versus 3 for the landed gate — same result as seeds 3521/3523.

V-A and V-B stdout is byte-identical to the base gate on the fixture, all three
claims:
```
CLAIM id=K1 expected=supported observed=supported   at=line:1 verdict=match
CLAIM id=K2 expected=supported observed=unsupported at=-      verdict=mismatch
CLAIM id=K3 expected=supported observed=unsupported at=-      verdict=mismatch
```
(`diff receipts/base-out.txt receipts/vA-out.txt` and `…/vB-out.txt`: no output.)

## Why the 9/9 is earned without the pin (two measurements)

1. **Recording override.** `RESEARCH_GATE_GREP=<recorder>` (absolute, reports GNU
   grep via `exec /usr/bin/grep "$@"`), `CHOUSA_GREP_PIN_ECHO=1`, same fixture:
   ```
   base rc=1  calls=6  hexpat_calls=3      V-A/V-B rc=1  calls=3  hexpat_calls=0
   base log: --version | -a -z -b -o -P -- x | 3× -a -z -b -o -P -- \x61\x6c…(4N hex) | -Fn -m1 -e charlie
   vA   log: --version | -a -z -b -o -P -- x | -Fn -m1 -e charlie
   ```
   (`receipts/base-calls.log`, `receipts/vA-calls.log`, `receipts/vB-calls.log`.)
   The two surviving calls are the startup version probe and
   `token_matcher_require`'s one-byte probe; no matcher pattern reaches the pin.

2. **Sabotaged verified pin.** Same absolute override mechanism, but the binary
   reports GNU grep and never matches:
   ```
   base: K1 observed=unsupported at=-   (matcher broke, as it should)
   V-A : K1 observed=supported   at=line:1 (unchanged)
   V-B : K1 observed=supported   at=line:1 (unchanged)
   ```
   (`receipts/*-saboteur-out.txt`.) Under V-A/V-B the pinned binary's *identity and
   behaviour* are not load-bearing for the matcher at all; C1's surface
   ("grep-binary provenance at every matcher call site") is vacuous there.

## Which scenario is too weak — and the minimal fix

- **S1 and S2 are the weak ones.** Both assert `empty_trip(tripwire)` plus
  reference-equal output. A tripwire is a *negative* instrument: it detects a grep
  call that was intercepted, and "no grep call at all" is indistinguishable from
  "a correctly pinned grep call". Both survive precisely because the engine never
  consults `grep`. In effect the pair rewards removing the matcher's dependency on
  grep, the opposite of C1's intent.
- **S3** (`no grep on PATH`) only checks output + absence of "not found"; it is
  satisfied by never needing grep, and the counter itself ships `python3` and `awk`
  on that PATH (`NOGREP_TOOLS`, c1-count.py:145-146), so both bypass engines run.
- **S4–S6** exercise refusals before any record; **S7–S9** check the `GATE_GREP:`
  line, `source=`, and output. All seven are startup-surface checks. None observes
  a matcher invocation.
- **Missing scenario (would kill V-A/V-B while keeping base):** set
  `RESEARCH_GATE_GREP=<absolute recorder that also reports GNU grep>` *and*
  `CHOUSA_GREP_PIN_ECHO=1`, require reference-equal output **and** at least one
  logged matcher query of the form `-a -z -b -o -P -- \xHH…` (4N hex escapes) per
  present span. Measured under exactly that override: base 3 matcher queries,
  V-A/V-B 0 → the mutant dies, the landed gate survives. [INFERENCE] this is the
  cheapest sufficient scenario; I did not implement it (the committed counter is
  read-only for this seat).

## Side finding for claim sizing (chunk call site is unscored)

P1's fixture spans are 63 bytes each (measured: `len(json.loads(l)["span"])` on the
counter's own `claims.jsonl` → 63,63,63; words sum 54 + 9 spaces), and
`tok_span_offsets` dispatches to `_direct` whenever `${#span} <= 32764`
(research-gate.sh:1668). V-D inserts only an entry tag in
`tok_span_offsets_chunk` and scores 9/9, and **the tag file was never created across
all 10 gate runs** (`receipts/vD-s3521.json`; tag absent). The chunk matcher is
therefore unreachable in every C1 scenario, so any chunk-only unpin or bypass is
invisible to P1 and necessarily scores whatever the rest of the gate scores.
This answers `chousa-r35-w2-CritClaimSizing`'s ask; names/shas/receipts above.

## V-C: pin removal is caught

0/9 on both seeds: S1/S2 tripwires fire (39 and 45 bytes — reproduced by hand: the
intercepted calls are exactly `-a -z -b -o -P -- x` and `-Fn -m1 -e charlie`, with
`fn ` prefixes under `BASH_ENV`; `receipts/vC-s1-trip.log`, `receipts/vC-s2-trip.log`),
S3 returns rc 2
("GNU grep with -z/-P support is required"), S4–S9 lose refusal/echo
(`receipts/vC-s3521.json`). So the counter separates "pin removed" from "pin
present"; only "pin present but bypassed in the matcher" slips through.

## Limits

- Engines replace only the direct (short-span) path; long spans still use the
  chunk matcher and greps. Their role is to be output-correct on the P1 fixture,
  which was verified byte-identically; they are not fuzzed for adversarial spans
  (glob metacharacters V-A, awk record/escape handling V-B, argv limits).
- One host, one grep: `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"`.
- S3's `path_tools=38`: symlinked tool set built by the counter, unchanged.
- No production edits, no git/jj writes. Scratch: `/tmp/hyaku/chousa-r35/w2/MutGrepPinEngines/`.
- Artifacts mirrored: `.ufo/waves/round-35/w2/MutGrepPinEngines/` — variant/helper
  scripts at top level, all receipts and logs under `receipts/`, every file <1 MiB,
  full sha256 list in `MANIFEST.sha256`.
