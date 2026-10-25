# ReviewReplacementBindings — three round-40 c1 replacement receipts vs committed bindings

Lane: chousa-shokunin. Round 40, wave 1. Seat: leaf reviewer (no dispatch).
Lane HEAD at audit: `6bc90e04ac60307befacd554f7eee2b7284e2652`; evidence commit `d164f88eb71a6c48a66ae1e7abfcb5fef82219d9`.
Read-only audit: the lane tree was not modified; independent re-run receipts were written to `/tmp/rb-repro/` only. No tool installs or upgrades were needed.

## Assigned attack

Independently verify that all three round-40 c1 replacement receipts bind the committed
expectations, counter, verifier, and the **intended** base / landed / mutant gate bytes:

- `corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json`
- `corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json`
- `corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json`

## Verdict

**All three receipts bind the committed bytes, and each reproduces byte-for-byte from an
independent run of the committed counter against the committed gate at this HEAD.** No HIGH
finding and no binding defect; one MEDIUM finding (M1) concerns the predicate's scope, not the
receipts. The digests match the `git show HEAD:` blobs (not merely the
worktree), each receipt's gate metadata resolves to the manifest's gate column, and
cross-role gate swaps are refused by name. Three LOW notes (population/`6/6` composition
wording; verifier never compares receipt path metadata; the frozen After stanza still reads
"Pending") and three informational residuals.
The R1 repair is a digest re-seal of unchanged observations, and the observation content is
independently confirmed truthful for the committed gate bytes.

**Environment note at audit tail (finding M1).** At 04:23:17, while this audit was running,
concurrent round-41 work modified the lane worktree's `tools/research-gate.sh`
(+75 lines of capture-tool pins; `corpus/evidence/round41/` and `.ufo/waves/round-41/` are
present, untracked). The frozen C1 counter no longer prints `6/6`: an observed re-run at
04:24 returned `R39_ACTIVE_RECEIPTS=2/6`, exit 1, with four rows refusing
`gate-sha256-mismatch`. That is the predicate's worktree sensitivity, not receipt corruption:
E2 ran at 04:19:34-04:19:53, while the gate path still held the committed bytes.

## Evidence

### E1 — frozen counter at HEAD

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round40/c1-count.py; echo "EXIT=$?"
```
```
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: ok VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: ok VERIFY: ok receipt=c1-after-s39111.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round39/receipts/c2-after-s39101.json: ok VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
corpus/evidence/round39/receipts/c2-after-s39121.json: ok VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
R39_ACTIVE_RECEIPTS=6/6
EXIT=0
```

The round-40 counter hardcodes the verifier and expectations it binds
(`corpus/evidence/round40/c1-count.py:9-11`) and joins each manifest row to the lane root
(`:31-33`); the manifest gate column therefore selects the gate each receipt is checked
against.

### E2 — independent re-run, per role (the core test)

```
python3 corpus/evidence/round39/c1-count.py --gate <G> --seed <S> --receipt /tmp/rb-repro/<role>.json
```

| role | gate | seed | counter output | fresh receipt sha256 | committed receipt sha256 | equal |
|---|---|---|---|---|---|---|
| base | `.ufo/waves/round-39/controls/base-gate-r39.sh` | 39001 | `ENV_PIN_CAPTURE_MATCH=7/8` | `e33199c1193ce6f0fb12cef788b41d79d2eb31181bbfdafe3d2f2eba97aa46af` | `e33199c1…46af` | **yes** |
| landed | `tools/research-gate.sh` | 39011 | `ENV_PIN_CAPTURE_MATCH=8/8` | `482e716a4d5a57b5f9f62c3652b82b72ae21e3255b61f4b18d1edc35d99bd131` | `482e716a…d131` | **yes** |
| mutant | `.ufo/waves/round-39/controls/mut-gate-path-env.sh` | 39013 | `ENV_PIN_CAPTURE_MATCH=4/8` | `ac2c24fa10406fad8c60cb7225b43632ccd8ac7fe5372df8b86d2ce5e8150fcb` | `ac2c24fa…0fcb` | **yes** |

`diff` of each fresh receipt against the committed replacement (`python3 -m json.tool` on
both sides) is empty for all three; the shared digest is the whole receipt including its
`receipt_sha256` self-digest. Wall time ~12.5 s / 13.9 s / 12.5 s. Fresh copies:
`/tmp/rb-repro/{base,after,mut}.json` (scratch, not lane artifacts). The committed receipts
are the resolvable artifacts.

This is strictly stronger than the verifier: `verify-receipts.py` re-derives the arithmetic
but never executes a gate, whereas the re-runs above executed each committed gate over its
eight scenarios and produced the committed bytes. Therefore the carried `observed` data are
truthful descriptors of those exact gate bytes, not merely internally consistent.

### E3 — digest bindings vs committed blobs

Four bindings per receipt; all recomputed from committed files:

| binding | receipt value (all three receipts) | source file | `git show HEAD:` blob |
|---|---|---|---|
| `expect_sha256` | `01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a` | `corpus/evidence/round39/expectations.jsonl` | same |
| `counter_sha256` | `91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5` | `corpus/evidence/round39/c1-count.py` | same |
| `verifier_sha256` | `1b6e0de688deda7493db3af5397d1e5bbf1fcdf556d8e254acae3ac6a8496267` | `corpus/evidence/round39/verify-receipts.py` | same |
| `gate_sha256`/`_pre`/`_post` | base `0447ad14b6135441f39f9220d02ae2967b810f791a2f1058654ee0c800c3b85a` | `.ufo/waves/round-39/controls/base-gate-r39.sh` | same |
| | landed `4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3` | `tools/research-gate.sh` | same |
| | mutant `e1251030ef61722cbba94b4645bd3dced2c8460b2fef89458f488f01c2bd231a` | `.ufo/waves/round-39/controls/mut-gate-path-env.sh` | same |

All three receipts carry `pre == post == gate_sha256` (single-valued gate binding); none of
the three receipts is a c2-family receipt, so `subject_counter*` is correctly absent for the
`c1` family (`verify-receipts.py:54-57`). Worktree bytes equal the `git show HEAD:` blob for
all nine bound files, so "committed" here is an externally verified fact, not an assumption;
`git diff --stat d164f88..HEAD` over the receipts, expectations, verifier, counter, gates is
empty — the bound bytes are frozen since the evidence commit.

### E4 — the intended role of each gate

- **base** = the pre-round-39 gate: `git show 8c7c867:tools/research-gate.sh | sha256sum` →
  `0447ad14…3b85a`, byte-identical to `.ufo/waves/round-39/controls/base-gate-r39.sh`,
  exactly as `corpus/evidence/round39/claims.md:11-15,63-72` states.
- **landed** = the current lane gate, unchanged since the round-39 tip
  (`git diff --stat 691d264..HEAD -- tools/research-gate.sh` empty), sha `4253c187…b07e3`.
- **mutant** = the landed gate + exactly **one** hunk:
  `diff -U0 tools/research-gate.sh .ufo/waves/round-39/controls/mut-gate-path-env.sh` yields
  1 `@@` (line 4066-4070), substituting the capture's `"$ENV_BIN"` with a bare `env` — the
  single-hunk mutant the round-39 claims describe. `base → landed` is 6 hunks, so the base
  and landed gates are genuinely different versions, not near-copies.
- Receipt `gate` metadata vs the manifest gate column: SAME for all three (base/landed/mutant).
- Cross-role probes (each receipt against the wrong committed gate) refuse by name:
  ```
  base-receipt   vs landed-gate rc=1 VERIFY-FAIL: gate-sha256-mismatch
  landed-receipt vs base-gate   rc=1 VERIFY-FAIL: gate-sha256-mismatch
  mut-receipt    vs landed-gate rc=1 VERIFY-FAIL: gate-sha256-mismatch
  mut-receipt    vs base-gate   rc=1 VERIFY-FAIL: gate-sha256-mismatch
  ```
  So each receipt is bound to its *role's* bytes, not to "some committed gate".

### E5 — the replacements are re-seals, and that is now content-verified

`diff` original vs replacement for each pair: the only differing fields are `expect_sha256`
(`3abd2dcb…6480` → `01cbdc3a…583a`) and `receipt_sha256`. Every `expect`, `observed`, `ok`,
`matched`, `total`, `predicate`, `gate`, `gate_sha256*`, `seed`, `counter*`, `verifier*` is
unchanged. The r39 originals are untouched by round 40
(`git diff --stat 691d264..HEAD -- corpus/evidence/round39/receipts/` empty), so the claim's
"without rewriting their committed originals" holds.

The peer reading that a re-seal could launder fabricated observations is defeated **for the
current bytes** by E2: a fresh run of the committed counter on the committed gates emits the
committed receipt bytes exactly, so the observations are the deterministic output of the
bound bytes. What a re-seal cannot prove is *authorship or run time* (the verifier's own
limit, `verify-receipts.py:34-39`); that residual is named below.

### E6 — provenance of the stale digest (why the re-seal is semantically safe for c1)

- current whole file: `01cbdc3a…583a`; current c1 block (first 8 rows): `703adb31…b7be`.
- stale binding: `3abd2dcb…6480`. Reconstruction attempts over current content:
  - prefixes of the current 16-line file: 8→`703adb31`, 9→`fb1f9633`, 10→`6ccb2856`,
    16→`01cbdc3a`; none is `3abd2dcb`;
  - all 40 320 permutations of the 8 c1 rows × every c2 prefix (k=0..8) — 362 880 hashes —
    none is `3abd2dcb`.
- Conclusion: the intermediate `expectations.jsonl` that produced `3abd2dcb` is not
  reconstructible from any committed artifact (it was never committed; only the digest
  survives). The "no semantic change" step therefore rests on the receipts themselves: each
  replacement carries all 8 c1 `expect` rows, and `expect-tie` re-derivation
  (`verify-receipts.py:171-184`) proves those carried rows equal today's frozen rows. c1
  coverage is total (8/8 ids), so no c1 expectation can hide outside the receipts. For P1
  this is sufficient; what remains unprovable is the *non-c1* content of the stale preimage,
  which is irrelevant to C1 (the claims' Separability clause, `claims.md:35-37`).

### E7 — discrimination ladder reproduced (what each role measures)

| role | matched | failing scenarios | failing cells (observed ≠ frozen expect) |
|---|---|---|---|
| base | 7/8 | `capture-bash-path-pin` | `path_bash_shim_echo` drift `-GATE_GREP`/rc 1/echo 1; `path_bash_shim_suppress` no pin file, pin rc 2, drift rc 2; `override_relative_refused` honoured (pin rc 0, no refusal) |
| landed | 8/8 | — | — |
| mutant | 4/8 | `env-fn-echo-scrub`, `env-fn-root-move`, `env-fn-suppress`, `capture-bash-path-pin` | the three `BASH_FUNC_env%%` cells re-open (`-GATE_GREP` echo 1; root-move drift with findings; suppress kills the capture) and `path_env_shim_echo` fails (`-GATE_GREP` echo 1) |

These are exactly the before/control results the round-39 claims pre-register
(`corpus/evidence/round39/claims.md:63-88`), and the reproduction shows they are still the
live behavior of the committed bytes.

### E8 — composition of the six-row active population

| manifest row | bound gate sha | matched | `predicate_holds` |
|---|---|---|---|
| `round40/receipts/c1-base-s39001-regenerated.json` | `0447ad14…` (base) | 7/8 | false |
| `round40/receipts/c1-after-s39011-regenerated.json` | `4253c187…` (landed) | 8/8 | true |
| `round40/receipts/c1-mutenv-s39013-regenerated.json` | `e1251030…` (mutant) | 4/8 | false |
| `round39/receipts/c1-after-s39111.json` | `4253c187…` (landed) | 8/8 | true |
| `round39/receipts/c2-after-s39101.json` | `4253c187…` (landed) | 8/8 | true |
| `round39/receipts/c2-after-s39121.json` | `4253c187…` (landed) | 8/8 | true |

Four rows bind the landed gate; one the base control; one the mutant control. Four rows carry
`predicate_holds=true`, two carry `false`. `6/6` is therefore six *verifiable* receipts, not
six predicate-holding measurements.

### E9 — the predicate is worktree-pinned, and the worktree moved mid-audit (observed)

```
sha256sum tools/research-gate.sh            → 3b631e863558d19e88394c9bab4bb55cc9977128bee03351c2f8d8668a6baff4
git show HEAD:tools/research-gate.sh | sha256sum → 4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3
git diff --stat -- tools/research-gate.sh   → 1 file changed, 75 insertions(+)
stat -c '%y' tools/research-gate.sh         → 2026-10-24 04:23:17 -0300
```

The 75 inserted lines are round-41 C1 capture-tool pins (`CAPTOOL_BIN`, `captool_pin_init`,
`CAP_CHILD_PATH`, `-u LD_PRELOAD -u LD_LIBRARY_PATH` in `gate_canonical_capture`); the
untracked `corpus/evidence/round41/` and `.ufo/waves/round-41/` trees are present.
`corpus/SOURCES.md` is also modified in the worktree (round-41 sources work); unlike the gate
it is not a round-40 C1 counter input.

The worktree gate kept moving during the audit window, so the live path is a moving target:
`4253c187…` (HEAD, still the value at 04:19:53) → `3b631e86…` (04:23:17, my E9 snapshot) →
`77791864…` (04:23:46, per `SentinelWriteScope.md` W0) → `2cb04bdd…` (04:26:28, re-checked
here), then stable at SentinelWriteScope's 04:28:10 re-measure and at this seat's final
re-check. Every digest claim in this report is bound to the **HEAD blob `4253c187…`**, never
to the worktree path; `SentinelWriteScope` separately confirmed that substituting the HEAD bytes
into a temp root restores `ok` for the affected rows, which corroborates M1's fix (a).
Observed consequence at 04:24, with no receipt touched:

```
python3 corpus/evidence/round40/c1-count.py
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok …
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok …
corpus/evidence/round39/receipts/c1-after-s39111.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39121.json: fail VERIFY-FAIL: gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6
EXIT=1
```

My reproductions (E2) ran 04:19:34-04:19:53, before the 04:23:17 edit: the landed receipt
they produced binds `4253c187…`, the committed blob. So the receipts are intact; what changed
is the bytes the counter reads. `ExecC1Count.md` records the same sensitivity deliberately
("`tools/research-gate.sh` bytes appended → `2/6`, exit 1") as a predicate bound.

## Findings by severity

### HIGH — none

### MEDIUM-1 — the frozen predicate is not commit-pinned, so its truth value is time-dependent

P1 (`claims.md:11`) is "C1 is met iff `python3 corpus/evidence/round40/c1-count.py` prints
`R39_ACTIVE_RECEIPTS=6/6` and exits 0". The counter resolves every bound path from the
worktree (`corpus/evidence/round40/c1-count.py:9-10,31-33`), and the verifier hashes live
file bytes (`verify-receipts.py:133,139,210`), so the predicate is a statement about the
current worktree, not about the evidence commit the Before/After blocks name (`claims.md:15,17`;
`measure-after.txt:1` "Measured against the lane work commit `d164f88…`"). E9 is the live
counterexample: an unrelated later edit to a bound file flips the predicate from 6/6 to 2/6
without any receipt being altered, and the counter output cannot distinguish "receipt
corrupted" from "worktree moved". A concurrent round-41 preparation in the same worktree
does exactly that, mid-wave, and kept doing it (E9: four distinct worktree digests inside the
audit window). `SentinelWriteScope.md` W0 reached the same conclusion independently and showed
that substituting the HEAD bytes restores `ok` for the affected rows — the empirical case for
fix (a). Impacted axes: operability (a documented check that no longer
returns its recorded result) and calibration (a seat that runs it now and reports C1 failed
would be measuring the environment, not the claim). The receipts themselves are not at
fault, and the claim is true at `d164f88` — I verified 6/6 there before the edit.
Smallest safe correction, either: (a) have `c1-count.py` read the bound files from git
(`git show <evidence-commit>:<path>`) and print that commit, or (b) refuse with a named
message when `git status --porcelain -- <bound paths>` is non-empty, and record the commit in
`measure-after.txt`'s output block (it already names it in prose). Until one is in place, any
round-40 report citing `6/6` should also state the tree state at measurement time.

### LOW-1 — `6/6` composition and one phrase in the C1 text invite a misread

`claims.md:9` calls the population "the six selected active round-39 evidence receipts",
but three of the six paths are round-40 artifacts, and two of the six (`base` 7/8, `mutant`
4/8) are negative/discrimination controls whose `predicate_holds` is false by design. P1 is
precise — it requires a `VERIFY: ok` prefix per row (`claims.md:11`), and the counter
implements exactly that (`corpus/evidence/round40/c1-count.py:39-40`) — so the claim is not
overstated at the predicate level. The misread risk is at the prose level: a reader can take
`R39_ACTIVE_RECEIPTS=6/6` as "six 8/8 runs". Corroborates `CriticC1Predicate.md` §78-81 and
`ExecC1BaseReceipt.md`'s reading caution; this seat adds the exact composition table (E8).
Smallest safe correction: one sentence in the C1 After block — "6/6 = six verifiable
receipts (4 landed-gate, 1 base 7/8 control, 1 mutant 4/8 control; four predicates hold)".

### LOW-2 — the verifier proves byte bindings but never compares receipt path metadata

`verify-receipts.py` compares `receipt["counter_sha256"]` to the bytes of `--counter`
(`:131-133`), `receipt["expect_sha256"]` to `--expectations` (`:137-139`), and
`receipt["gate_sha256_pre"]`/`gate_sha256` to the bytes of `--gate` (`:208-215`). It never
compares the receipt's `gate`, `counter`, or `expectations` *strings* to the paths it was
given. For these three receipts the metadata agrees (E4), so this is latent, not a defect in
the claim: "bind the committed gate bytes" is established by digests plus the E4 provenance
check. It matters only if a future claim asserts that a receipt *names* its subject. The
receipts' `gate` fields are absolute author-machine paths (e.g.
`/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`), so that assertion
would also be root-dependent. Smallest safe correction (if ever relied on): add
`os.path.realpath(receipt["gate"]) == os.path.realpath(args.gate)` and the same for counter
and expectations as a named refusal.

### LOW-3 — the frozen C1 After stanza still reads "Pending" after the data landed

`claims.md:17` says "**After.** Pending re-derivation after all three replacements are
committed." The replacements are committed (`d164f88`) and the after result exists in
`corpus/evidence/round40/measure-after.txt` (which names `d164f88`), `corpus/lessons/round-40.md`,
and `LOG.md`, and no erratum records the re-derivation (`claims.md:43-45` carries only the
S059 entry). The file's own convention is "a later change ... is an appended erratum", so the
omission is consistent with the round-39 practice of leaving results to the report — but a
reader of `claims.md` alone sees C1 as unmeasured. This is documentation, not evidence: P1 is
satisfied at the evidence commit by E1-E2. Smallest safe correction: one erratum line carrying
the After block plus the tree state at measurement (which also discharges the M1 documentation
side) — "R39_ACTIVE_RECEIPTS=6/6, exit 0 at `d164f88` in a clean tree; worktree not at HEAD
from 04:23:17 (round-41 in flight)".

### INFO-1 — reproduction is root-bound; verification is not

Because `gate`/`subject_counter` embed the lane's absolute root, the receipts reproduce only
when the lane lives at `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Verification is
unaffected (paths are not compared), but `receipt_sha256` equality as a reproduction check is
a property of that canonical runtime, not of an arbitrary checkout. Single canonical runtime
is satisfied here: the lane root is that path, `/usr/bin/bash` is present, and the four runs
(frozen counter plus three role re-runs) executed on the same host in the same session.

### INFO-2 — `seed` is inert

`c1-count.py` accepts `--seed` only to stamp the receipt field; the verifier checks neither
range nor uniqueness, and the scenarios are deterministic. Seeds 39001/39011/39013 are
labels identifying the three runs, not stochastic coverage. Nothing in the round-40 claim
depends on them; they should not be cited as independent sampling.

### INFO-3 — the mutant reproduction is duplicated by a sibling seat

`ExecC1MutantReceipt` is reproducing the mutant receipt concurrently. My result (E2, mutant
sha `ac2c24fa…`) is method-independent of that seat and is reported here as corroboration;
no conflict was observed. `ExecC1BaseReceipt` and `ExecC1LandedReceipt` likewise report
byte-identical reproductions of the other two roles.

## Residual risk

1. **Authorship/time of the original observations is unprovable.** The verifier's own limit
   (`verify-receipts.py:34-39`) plus the R1 history (originals bound a digest that no commit
   contained) mean the three receipt *bodies* were authored against an intermediate working
   tree. Content truth for the committed bytes is established by E2; provenance of the r39
   moment is not, and cannot be from committed artifacts.
2. **Nothing pins future bytes.** `6/6` dies by design if any of the six bound files changes;
   that is the intended sensitivity, not a gap. It also means the measurement is a statement
   about HEAD only. As of 04:24 the lane worktree is not at HEAD for `tools/research-gate.sh`
   (E9), so the predicate reads 2/6 until round-41 work either lands or is set aside; my
   6/6 observation and all three reproductions predate that change.
3. **Stale preimage unrecoverable (E6).** The semantic-equality argument for the digest
   substitution relies on receipt-carried c1 rows plus total c1 id coverage; the non-c1 part
   of the stale file is unknowable and irrelevant to C1 but would matter if the same re-seal
   pattern were used for a family whose rows were not fully carried in a receipt.

## Verification gaps (what I did not establish)

- No LSP server answers these artifacts: `pyright`, `pylsp`, `basedpyright` are absent from
  PATH and no `lsp` device is exposed to this seat, so caller/definition/reference checks
  were not available. `ty check` over the three involved Python files reports
  `All checks passed!` (exit 0) as the only available diagnostics. Text search was used only
  to locate check lines for citation, never as proof of absence.
- I did not re-execute the c2 family (out of the assigned attack); the two c2 rows were
  exercised only through the frozen counter's `VERIFY: ok`, and their subject-counter
  binding looked consistent (`subject_counter` = `…/corpus/evidence/round39/c1-count.py`,
  sha `91618e…`).
- I did not audit the S059 sourced-claim row or the C2 disposition record (other seats).
- I did not audit or judge the concurrent round-41 work that changed `tools/research-gate.sh`
  at 04:23:17; I only record its effect on the round-40 predicate (M1, E9). Because that
  change landed mid-wave, sibling round-40 seats may have measured the counter at different
  tree states; the state at each measurement is therefore part of the evidence, not a detail.
- `/tmp/rb-repro/` receipts are scratch and may disappear; the committed receipts plus the
  commands above are the durable pointer.

**Artifacts:** this report;
`corpus/evidence/round40/receipts/c1-{base-s39001,after-s39011,mutenv-s39013}-regenerated.json`;
`corpus/evidence/round40/active-r39-receipts.tsv`; `corpus/evidence/round40/c1-count.py`;
`corpus/evidence/round39/{verify-receipts.py,c1-count.py,expectations.jsonl}`;
`.ufo/waves/round-39/controls/{base-gate-r39.sh,mut-gate-path-env.sh}`.
