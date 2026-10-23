# CritClaimSizing — round 35 §9 audit

Access date: **2026-10-23**. Axes: **operability (C1)** and **calibration (C2)**. This is a scoped critic finding, not an admission or a canonical judgment. No production edits, Git/jj writes, subagents, network, or installs.

## Principal counterexample: P1 MEETS without the claimed matcher pin

I independently replayed MutGrepPinEngines' V-A control, copied and named `V-A-bash-pin-unused-control.sh` in my scratch. SHA-256:

`fd6d5a8ea9d4288370d9ef2d26dfd7bdf04ee227c5a9d55a4bf334d9de837c53`

The control leaves startup pinning/refusals/echo intact but replaces `tok_span_offsets_direct` with Bash substring/glob search. Opened source: `.ufo/waves/round-35/w2/MutGrepPinEngines/vA-glob-pin-unused.sh:1675-1690`. My unchanged committed C1 counter run on fresh seed **353505** returned **exit 0, `GREP_PIN_MATCH=9/9`, `predicate_holds=true`, `reference_sane=true`**. Receipt: `.ufo/waves/round-35/w2/CritClaimSizing/c1-pin-unused-s353505.json:3-7,182-184`.

I then ran the control and landed gate against the same three-record fixture with the same absolute GNU-reporting recording override. Both gate runs returned **exit 1**, with K1 supported, K2/K3 unsupported, and `RESEARCH_GATE: DRIFT`. Their recorded calls differ:

| Candidate | All recorded calls | Full-span hex-pattern matcher calls |
|---|---:|---:|
| Landed gate `1f2fb4f5…` | 6 | **3** |
| V-A `fd6d5a8e…` | 3 | **0** |

Durable logs in my artifact directory: `landed-grep-calls.log:1-6` and `mutant-grep-calls.log:1-3`. The latter contains only `--version`, the one-byte `-P -- x` capability probe, and a nearest-line diagnostic query. Thus this is **not** a claim that the pinned binary is never executed: it is never queried for the three span matches. The relevant pin is present but not load-bearing for matching.

**Why it scores:** C1 S1/S2 accept an empty interception tripwire plus reference-equivalent output (`c1-count.py:211-222`); doing no grep span search satisfies both. S3 checks equivalent output without PATH grep (`:223-228`). S4-S6 test startup refusals (`:229-247`), and S7-S9 test echo/output/interception (`:248-275`). None requires a positive span-matcher invocation of the verified override. This directly contradicts the claimed measurement surface at `claims.md:21-27`, while satisfying its finite numeric target.

**Smallest safe correction:** retain the frozen P1 and report this discrimination failure; do not narrow the landed claim to startup-only pinning. A subsequent frozen counter can add a GNU-reporting recording override and require actual span-pattern queries through it, covering both direct and chunk paths. This is a counter/claim defect, not a demonstrated output-correctness regression or an axis tradeoff. Canonical disposition belongs to the judge.

Control attribution: authored by MutGrepPinEngines; independently copied, pinned, scored, and recorded here. My preserved control, recorder, fixture, logs, and receipt are all under `.ufo/waves/round-35/w2/CritClaimSizing/`.

## Concrete after-values over committed bytes

The following commands were executed from the lane root through `timeout 30s python3 -c …`; each reads only receipt blobs at the fixed revision, not draft files or my attack artifacts.

### C1: one value, `C1_AFTER=9/9`

```sh
timeout 30s python3 -c 'import json,subprocess
r=[json.loads(subprocess.check_output(["timeout","10s","git","show","e87c5d7ea2dbf3730b36a3961de3f06261d015e4:.ufo/waves/round-35/measure/c1-after-s%d.json"%s])) for s in (3501,3517)]
print("C1_AFTER=%d/9 P1_PAIR=%s"%(min(x["matched"] for x in r),str(all(x["predicate_holds"] for x in r)).lower()))'
```

Observed **exit 0**: `C1_AFTER=9/9 P1_PAIR=true`. Sources: committed `measure/c1-after-s3501.json:3-7,182-184` and `c1-after-s3517.json:3-7,182-184`.

### C2: one value, `(2/2, 2/2, pass)`

```sh
timeout 30s python3 -c 'import json,subprocess
r=[json.loads(subprocess.check_output(["timeout","10s","git","show","e87c5d7ea2dbf3730b36a3961de3f06261d015e4:.ufo/waves/round-35/measure/c2-after-s%d.json"%s])) for s in (3501,3517)]
print("C2_AFTER=%d/2 OUTPUT_EQUIV=%d/2 LANDED_WITNESS=%s P2_PAIR=%s"%(min(x["matched"] for x in r),min(x["output_equiv"] for x in r),"pass" if all(x["landed_witness"]=="pass" for x in r) else "fail",str(all(x["predicate_holds"] for x in r)).lower()))'
```

Observed **exit 0**: `C2_AFTER=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass P2_PAIR=true`. Sources: committed `measure/c2-after-s3501.json:7-25` and `c2-after-s3517.json:7-25`.

These commands re-derive the recorded finite values, not their adequacy for the broader prose. I also freshly executed the actual counters, rather than relying only on receipt arithmetic; see the run table below.

## Baseline authenticity and freeze chronology

Read-only commands executed, all **exit 0**:

- `timeout 30s git log -3 --format='%H %P %s' e87c5d7ea2dbf3730b36a3961de3f06261d015e4`: exact parent chain is **08be4c9e → 0e167649 (freeze) → e87c5d7e (gate/measurements)**.
- `timeout 30s git ls-tree -r 0e167649a1f45aad4e4f05f2b14975b6a80484f3 -- corpus/evidence/round35/claims.md .ufo/waves/round-35/controls .ufo/waves/round-35/measure tools/research-gate.sh tools/mechanism-witness.py`: all five requested baseline/control receipts and their control sources were committed at freeze; no after-measurement receipts were present there.
- `timeout 30s git diff 0e167649a1f45aad4e4f05f2b14975b6a80484f3 e87c5d7ea2dbf3730b36a3961de3f06261d015e4 -- corpus/evidence/round35/claims.md corpus/evidence/round35/c1-count.py corpus/evidence/round35/c2-count.py tools/mechanism-witness.py`: **empty**. Frozen claim, counters, and witness bytes did not change between those commits.
- `timeout 30s git diff e87c5d7ea2dbf3730b36a3961de3f06261d015e4 -- corpus/evidence/round35 tools/research-gate.sh tools/mechanism-witness.py .ufo/waves/round-35/controls .ufo/waves/round-35/measure .ufo/waves/round-35/repairs`: **empty** at audit time; opened production/evidence bytes match the pinned revision.
- `timeout 30s git show 08be4c9e3a4ebe55d915ce4761c81854286c23ae:tools/research-gate.sh | timeout 30s sha256sum`: **a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b**. The committed `repairs/base-gate.sh` has the same SHA-256. `git ls-tree` of that base's `tools/mechanism-witness.py` returned no entry.

Opened every specifically requested receipt:

| Receipt, under `.ufo/waves/round-35/controls/` | Recorded result and authenticity evidence |
|---|---|
| `c1-base-s3501.json:3-7,97-124` | Gate SHA matches the independently hashed base; **0/9**, sane reference. Receipt records S1/S2 logs of 852/867 bytes and S3 exit 2. |
| `c1-hardcoded-s3501.json:3-7,97-125` | Gate SHA **05bdf6543858a551852b6b9725d4cd327140f8d94589ae87ce82c5232248a378** matches `sha256sum controls/ctl-c1-hardcoded-grep.sh` at the full wave path; **3/9**, sane reference. |
| `c2-before-s3501.json:2-13` | Base gate SHA matches. **0/2 battery=absent**, with `battery=/nonexistent/witness.py` and empty variants. This is an **absence sentinel**, not two experimentally observed engine-separation failures; the code returns that constant before running variants (`c2-count.py:150-158`). Base-tree absence is independently confirmed by Git. |
| `c2-stub-pass-s3501.json:2-25,27-55` | Battery SHA **3ef9643fccf3fbab1f45ee5b2af378a5dbb19adc5ab77bc9ad5fa9a006de95e1** matches the committed pass stub. **0/2**, landed witness pass, predicate false. |
| `c2-stub-fail-s3501.json:2-25,27-55` | Battery SHA **a9854141ad37db4cd572d85262abd12d5b001ce7740846b9e0d955103ba46290** matches the committed fail stub. **2/2**, landed witness fail, predicate false. Its numeric 2/2 alone is not P2. |

All source hashes above were obtained with `timeout 30s sha256sum` at their full paths. The two stub bodies were opened (`ctl-c2-stub-{pass,fail}.py:1-13`); their recorded unconditional behavior matches those bytes. These are authentic committed records with matching source pins, not signed proof of historical execution or wall-clock writing order.

I enumerated **all 10 committed round-35 JSON files** using `git ls-tree -r -z --name-only e87c5d7e -- .ufo/waves/round-35 corpus/evidence/round35`, loaded their blobs with bounded `git show`, and filtered by landed gate SHA plus the two claim labels. Exactly four matched: the two C1 and two C2 after receipts above, all predicate true; both C2 receipts pin the real witness. This checks the committed-run clause for this round at this revision, not future commits.

## Causal separability — demonstrated in both directions

1. **C1 without C2:** copied only committed `tools/research-gate.sh` and `corpus/evidence/round35/c1-count.py` into a new sparse scratch tree using `cp --parents`. `test ! -e tools/mechanism-witness.py` exited 0; `find . -type f -print` listed exactly those two files. C1 seed **353501**: **9/9, exit 0**, predicate true. Receipt `CritClaimSizing/c1-without-witness-s353501.json:3-7,182-184` pins the landed gate.
2. **C2 without C1/R1:** copied committed `repairs/base-gate.sh` as the named `base-round34-control.sh`, SHA **a6307edf…2995b**, and ran the committed C2 counter and witness against it. Seed **353503**: **2/2 separation, 2/2 output equivalence, landed witness pass, exit 0**. Receipt `CritClaimSizing/c2-base-s353503.json:4-25`. The earlier committed `controls/c2-base-s3501.json:4-25` records the same result. C2 does not require the grep-pin or slen repair to have landed.

Thus coupling between C1 and C2 is not the defect found here.

## §9 calibration mismatch: P2 does not inspect a self-assessment

The designated §9 source requires an assessment-versus-observation mismatch count (`/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-35.md:355-356`, opened 2026-10-23). `c2-count.py:164-190` counts output-full variants rejected by a witness, and a landed witness pass. Neither it nor `mechanism-witness.py` reads SCORECARD/SHONEN; a targeted search for `SCORECARD|SHONEN|mismatch|self.assess` in both returned **no matches**. The witness compares generated truth to output and counts function entries (`mechanism-witness.py:281-300`), not lane self-assessment to observed repository state.

Concrete check: I copied only the committed gate, witness, and C2 counter into another sparse scratch tree. Both `test ! -e SCORECARD.md` and `test ! -e SHONEN.md` exited 0. Running P2 there at seed **353504** still returned **2/2, 2/2, pass; exit 0; predicate true** (`CritClaimSizing/c2-without-assessment-s353504.json:2-25`). P2 is therefore independent of the presence or accuracy of those assessment files.

This is a counterexample to treating the P2 value as the required calibration measurement, **not** a bypass of the fixed committed witness. The added witness is a demonstrated capability. The missing assessment comparison cannot be repaired by relabeling the frozen C2 after landing; report the mismatch for canonical disposition and use an explicit assessment/observation census in a subsequent frozen claim.

## Universal clauses, narrowing, and artifact dependence

- **C1 universal matcher scope is not enumerated.** Located wording: “at every matcher call site” (`claims.md:25-27`, accessed 2026-10-23). P1 generates three fixed **63-byte** spans, verified by `.span | length` over my copied fixture: `63,63,63`. Source `c1-count.py:64-84` has no seeded variation in those texts; the seed changes the temporary prefix (`:157-164`). Routing at `research-gate.sh:1650,1668-1672` sends them only to the direct matcher. The chunk site and other modes are not enumerated. The peer's chunk-entry-tag control receipt was also opened at `MutGrepPinEngines/receipts/vD-s3521.json:3-7`; it is 9/9. I did not independently replay that tagged control. The direct-path MEETS reproduction above already establishes the stronger discrimination defect.
- **The historical diagnosis also overstates its surface.** `claims.md:28-30` says the base cannot run at all without PATH grep. I constructed a PATH containing only symlinks to `dirname`, `date`, `cat`, `head`, `readlink`, and ran the pinned base with `--help`: **exit 0**, output began `usage: research-gate.sh [--selftest] [--help]`. No grep existed in that PATH. This does not change S3's recorded verify-claims failure. An initial completely empty-PATH attempt exited 1 because `dirname` was unavailable; the isolated grep-free farm removes that confounder.
- **C2 output-equivalence wording exceeds its enumeration.** Located wording: “every output counter passes” (`claims.md:66-67`, accessed 2026-10-23). The committed P2 actually evaluates nine generated records for each of two constructed engines, not an enumeration of output counters (`c2-count.py:165-190`; `mechanism-witness.py:54-63`). The cited round-34 result concerns its named counter and controls (`MutC2Keyed.md:40-47,94-111`), not every possible counter.
- **K2's location claim is overbroad.** Located wording: “active on any counter fixture” (`claims.md:75-76`, accessed 2026-10-23). Its actual key is only `/tmp/*|/fast/*|/var/tmp/*` (`c2-count.py:76-81`). [INFERENCE] a fixture rooted at `/home/fixtures/x` does not activate it. I did not create an out-of-scope fixture outside my permitted scratch.
- **Entry evidence is aggregate.** The witness tests total chunk stamps against total long records (`mechanism-witness.py:294-295`); it does not map each stamp to a particular record. The trace-awareness/show-call and confirmation-correctness limits are genuinely present before data (`claims.md:106-110`) and were byte-identical at freeze and landing. They are not newly discovered exemptions in this review.
- **No silent edits to the frozen claim were found.** The commit comparison above is empty. However, landed `research-gate.sh:346-347` attributes its self-reported-version caveat to a frozen C1 limit that does not exist in `claims.md:19-59`; the file's explicit limit is under C2 at `:106-110`. Correct that provenance, not the frozen rule. The later draft `corpus/knowledge/grep-pin-r35.md:54-60` spells out a non-integrity scope, but `git ls-tree` at the wave base has **no entry** for that draft or for `corpus/lessons/round-35.md`; neither can establish an additional pre-data C1 exclusion. The canonical assignment's GNU-reporting requirement must not be inflated into a cryptographic-origin guarantee either.
- **Frozen numeric evidence does not require an uncommitted artifact.** Counters, witness, requested controls/receipts, after receipts, and the historical keyed-engine report all exist at `e87c5d7e`. The shorthand `controls/...` references in the prose mean `.ufo/waves/round-35/controls/...`, not a directory beside `claims.md`. Generated mutant gate paths and helper paths are temporary and deleted by C2 (`c2-count.py:160-172,201-205`), so an old variant SHA alone is not reopenable original bytes; the committed construction is reproducible. My attack artifacts are explicitly new review evidence, not claimed frozen evidence.

## Executed run commands and pins

For compactness, `S` below denotes `/tmp/hyaku/chousa-r35/w2/CritClaimSizing`, and `A` denotes `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/CritClaimSizing`. Every counter command was prefixed with `timeout 900s env C1_TMP=$S C2_TMP=$S WITNESS_TMP=$S TMPDIR=$S`, using those literal paths. No counter or witness source was edited.

| cwd | Command after that prefix | Exit / key output |
|---|---|---|
| `$S/c1-without-witness` | `python3 corpus/evidence/round35/c1-count.py --seed 353501 --receipt $A/c1-without-witness-s353501.json` | 0; 9/9 |
| lane root | `python3 corpus/evidence/round35/c2-count.py --seed 353502 --receipt $A/c2-landed-s353502.json` | 0; 2/2, 2/2, pass |
| lane root | `python3 corpus/evidence/round35/c2-count.py --gate $S/base-round34-control.sh --seed 353503 --receipt $A/c2-base-s353503.json` | 0; 2/2, 2/2, pass |
| `$S/c2-without-assessment` | `python3 corpus/evidence/round35/c2-count.py --seed 353504 --receipt $A/c2-without-assessment-s353504.json` | 0; 2/2, 2/2, pass |
| lane root | `python3 corpus/evidence/round35/c1-count.py --gate $S/V-A-bash-pin-unused-control.sh --seed 353505 --receipt $A/c1-pin-unused-s353505.json` | 0; 9/9 |

Recording runs used `timeout 300s env TMPDIR=$S GREP_CALL_LOG=$S/{mutant,landed}-grep-calls.log RESEARCH_GATE_GREP=$S/recorder-grep.sh CHOUSA_GREP_PIN_ECHO=1 /usr/bin/bash GATE verify-claims $S/pin-fixture/claims.jsonl --root $S/pin-fixture`, separately substituting the actual gate and log path. Both exited 1 with the expected three observed dispositions. The recorder is a real delegating wrapper, not a fabricated output oracle (`recorder-grep.sh:1-3`).

Observed source pins:

| Source | SHA-256 |
|---|---|
| Landed gate, also `git show e87c5d7e:tools/research-gate.sh` | `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` |
| C1 counter | `da207fd725658b84469ce1fe540a7b94fcb1027cef49da376a8d7ac19ac715e3` |
| C2 counter | `557fdbf0bd793a6589fcb28fbc0a589db9145be0ae3c92790041fe8ebd907171` |
| Real witness | `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` |
| Copied recording override | `dc672d185afae569d09052f399bcd6c01fad2abe3f84cdfbe60bd9f1bc5e32ea` |

My receipt SHA-256 values:

- `c1-without-witness-s353501.json`: `bc07a26d04707de8dc62a2cca69c3e10a0353f449f0e140664c61ea6cc6ceced`
- `c2-landed-s353502.json`: `46f6464d5c12ec44bc738bcf2b7979aaf7ee971c0b9e19ed87a2f103f0037900`
- `c2-base-s353503.json`: `82063e745c5eaf7c00d9cae97bec752ee55760a2c5544a84c42e4be43562fa9f`
- `c2-without-assessment-s353504.json`: `61286cf04f68ebbacf484d18ec6fff63d0b5658aa0db6beac02d2c5b1051b213`
- `c1-pin-unused-s353505.json`: `3e63b976fd055e6bc504fb4246c0569f9df4f483c8837b06f9d91f015eb29a82`
- `landed-grep-calls.log`: `a797d439aaab9f875470f6942d357ba6227ac6cf245f0369a98fb316ca31b724`
- `mutant-grep-calls.log`: `a7ec2aeb7aee9285a9ce112ab0eceb27a79a9c2d2b2c20675dbb36fa99ce5047`

## Limits

One host, locally installed GNU-reporting grep 3.12-modified. No selftest, full gate battery, slen-probe rerun, or arbitrary-input equivalence proof was performed in this scoped audit. R1/R2 source/probe and frozen descriptions were opened as required, but their execution review belongs to the repair seats. No alternate-battery result is represented here as a bypass of the fixed real witness. The P1 MEETS finding is independently executed; the C2 objection is the missing §9 assessment comparison despite its correctly reproduced finite witness result. Report written once.
