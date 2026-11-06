# R81ExecTrial — end-to-end trial of the round-81 method (chousa round 81, w1)

Seat: `R81ExecTrial` (leaf; Godspeed axes: record completeness, checklist discrimination, receipt
reproducibility). Landing bytes attacked: `7e2da96a0541946e796384d42fea18e09ede9e9f`. Base for the
frozen predicates: `378fda82`; freeze `bb54e7f8`; prefreeze controls `f7929f87`.

All trial work ran in `/fast/scratch/hyaku/chousa-r81/R81ExecTrial/` (tree = `git archive 7e2da96a | tar -x`);
scratch is deleted after this report and every cited receipt is copied here. Nothing in `corpus/`,
`SKILL.md`, the counters, fixtures or receipts was amended; no lane or fleet git/jj mutation; no
tool install (nothing needed); no pacman transaction. Network: exactly one live GET (S205, via the
item-5 tool) under the round-81 egress table; S203 was **not** re-fetched (its re-open is not named by
this seat's item; see Limits).

## 1. The research record (real question, record v1)

Question: *Is the TARCiS statement's recommendation on stand-alone citation searching supported by the
accepted manuscript, and is the statement's correction status known?*

Answer as recorded: **supported** — the accepted manuscript's recommendation 9 reads "Stand-alone
citation searching should not be used for literature searches that aim at completeness of recall."
(committed capture `corpus/captures/f2489455cc311a4de981e926.txt`, located at capture line 789, sha256
`31493aa66bfd…`; the same sentence recurs at line 2393). **Correction status unknown** — the BMJ
correction `BMJ 2024;387:q2458` answered HTTP 403 on 2026-11-06 (`refetch.tsv` row S208); no readable
copy was obtained, recorded as negative claim N1 with sweep W1 naming the URL, and S208 kept in
`## Rejections` with a flip-condition (a readable copy whose recommendation-5 wording is located).
The record does not cite any recommendation-5 wording, so the open correction does not touch the
answer it does give.

Artifacts (copied here): `record.md` (sha256 `027f669b763c0c8b…`), `claims.jsonl`
(`f80aa66c0c1d8f17…`, three spans with `sha256` pins of the capture bytes), `items.tsv`
(`dbcc29f05490c3ec…`), `00-artifact-pins.txt`. The record declares `claims_file` in `## Meta` so that
`verify-all <record> --root .` composes the claims section without `--claims`.

## 2. Checklist Run lines executed (tree root, landing bytes)

| item | exact command | rc | observed verdict line | receipt |
|---|---|---|---|---|
| 1 | `bash tools/research-gate.sh verify-claims corpus/evidence/round81/trial/claims.jsonl --root .` | 0 | `VERDICT_BEARING_CLAIMS=3/3`; `RESEARCH_GATE: CLEAN (claims=3 supported=3 … findings=0 drift=0)`; all three `verdict=match` (`at=line:789`, `at=line:323`, `at=line:134`) | `01-item1-verify-claims.txt` |
| 2 | `f=corpus/evidence/round81/trial/record.md; ! bash tools/research-gate.sh verify "$f" --root . \| grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .` | 0 | `SWEEP id=W1 … looked=non-local … verdict=exempt`; `REJECTION id=R1 … flip=present observed=complete verdict=match`; `VERIFIED_SWEEPS=0/1 REJECTIONS_OK=1/1`; `RESEARCH_GATE: CLEAN` | `04-item2-verify-run.txt` |
| 4 | `bash tools/research-gate.sh verify-sweeps corpus/evidence/round81/trial/record.md --root .` | 0 | same sweeps/rejection lines, `REJECTIONS_OK=1/1`, `RESEARCH_GATE: CLEAN` | `07-item4-verify-sweeps.txt` |
| 5 | `TMPDIR=$S python3 tools/quote-reopen.py verify --items corpus/evidence/round81/trial/items.tsv` (live GET of the S205 NLM page) | 0 | `QUOTE_REOPEN Q1 VERBATIM matched in normalized page text`; `QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0` | `10-item5-quote-reopen.txt` |
| 6 | `CHOUSA_GREP_PIN_ECHO=1 bash tools/research-gate.sh --selftest 2>&1 \| grep -m1 '^GATE_GREP: '` | pipeline 0 (gate 141) | `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"` — exactly the pinned value | `11-item6-grep-pin.txt` |
| — | `bash tools/research-gate.sh verify-all corpus/evidence/round81/trial/record.md --root .` | 0 | `SECTION structure/claims/chain/sweeps/integrity … verdict=CLEAN`; `RESOLVED_HOPS=2/3`; `INTEGRITY refs=10 resolved=6 unresolved=0`; `VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0`; `RESEARCH_GATE: CLEAN` | `12-verify-all.txt` |

Item 1 root adjustment, stated: the record sits at `corpus/evidence/round81/trial/`, so the Run line's
literal `--root ..` names `corpus/evidence/round81`, which does **not** contain `corpus/captures/`. I ran
the line from the tree root with `--root .` (the captures are then inside the declared root). I also
measured the literal `--root ..` form from the tree root and from the record directory
(`03-item1-root-and-pin-probes.txt`): both still print `VERDICT_BEARING_CLAIMS=3/3` rc 0, because
`claim_source_path` falls back to `LANE_ROOT` = the directory above `tools/`, i.e. the lane tree itself.
So the root adjustment is not load-bearing when the gate is run from inside the lane tree — and the
literal `--root ..` does **not** test the boundary it appears to test. Item 3 was not run: its Run line
takes `--entry corpus/knowledge/<entry>.md`, and the trial artifact is a research record, not a
knowledge entry; running it on the new entries is C1's surface, not this trial's.

Frozen counters at the landing bytes (read-only, receipts): `13-checklist-run.txt` —
`CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, `CHECKLIST=PASS`, rc 0; `14-depth-r81.txt` —
`DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14`, `DEPTH_R81=PASS`, rc 0. Both frozen predicates
hold at the bytes I attacked; the findings below are about what those predicates and Run lines do
**not** see.

## 3. Mandated mutated twins — each Run line exits 1

| item | twin (exactly the named defect) | command | rc | observed |
|---|---|---|---|---|
| 1 | capture byte changed: byte 100 of the S203 `.txt` set to `X` in a copied root whose `claims.jsonl` keeps the original pin | `bash tools/research-gate.sh verify-claims $S/mut1/claims.jsonl --root $S/mut1` | **1** | `CLAIM id=C1 … observed=stale … verdict=mismatch`; `FINDING CLAIM_SOURCE_REVISION_MISMATCH … pin=31493aa66bfd actual=ce915c394d37`; `VERDICT_BEARING_CLAIMS=1/3` (`02-item1-mut-capture-changed.txt`) |
| 2 | negative claim N1 has an empty `sweep` cell and no Sweeps row (`mut2-no-sweep.md`) | the item-2 Run line verbatim | **1** | structure only: `FINDING NEGATIVE_WITHOUT_SWEEP severity=warn surface=negatives obs=claim=N1 negative without sweep`; `RESEARCH_GATE: DRIFT … findings=1 drift=1`, rc 1 (`05-06-item2-twins.txt`) |
| 4 | kept rejection R1 with an empty `flip_condition` cell (`mut4-no-flip.md`) | `verify-sweeps … --root .` | **1** | `REJECTION id=R1 … flip=absent observed=incomplete verdict=mismatch`; `FINDING SWEEP_REJECTION_INCOMPLETE … missing=flip`; `REJECTIONS_OK=0/1`; `RESEARCH_GATE: DRIFT`, rc 1 (`08-09-item4-twins.txt`) |

All three mandated twins behave exactly as the item text says. The counter's own fixture pairs agree
(`13-checklist-run.txt` legs pass).

## 4. Findings — two C2 kill-rule firings

### F1 (C2 K2, item 2): a negative claim with no sweep at all passes the landed Run line

Record `atk2-dangling-sweep.md` is `record.md` with one change: N1's `sweep` cell names `W1`, and the
`## Sweeps` section is removed. The record therefore names **no location anywhere** for its negative
claim — the only trace of a sweep is a dangling id.

- `! bash tools/research-gate.sh verify "$f" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .`
  → **rc 0**; `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1`; `RESEARCH_GATE: CLEAN` (`05-06-item2-twins.txt`).
- Structure alone on the same record: `RESEARCH_GATE: CLEAN (findings=0 … negatives=1 …)` — it has a
  `sweep` cell, so `NEGATIVE_WITHOUT_SWEEP` never fires; `verify-sweeps` has no row to inspect.
- The composed gate is blind too, when the id is `W1`: `verify-all` → all five sections CLEAN,
  `INTEGRITY refs=7 resolved=4 unresolved=0`, rc 0 (`06b-verify-all-atk2.txt`). Integrity's id shapes
  are `S…`, `C|N…`, `SW…`; a bare `W1` (the id convention the lane's own `sweeps-r5.md` fixture uses) is
  not a checked shape.
- With `SW1` instead (`atk2b-dangling-sw1.md`) the item-2 Run line still exits **0**
  (`VERIFIED_SWEEPS=0/0 … CLEAN`), while `verify-all` finally catches it: `FINDING REF_UNRESOLVED …
  kind=sweep id=SW1 section=claims row=N1 cell=sweep`, `INTEGRITY … unresolved=1`, rc 1
  (`06c-item2-sw1-variant.txt`). So the checklist line itself is blind in both spellings; the composed
  gate is blind in one.

This is the item-2 defect ("a negative claim with no named location") in a form the item text names,
on which the landed Run command exits 0. **C2 K2 fires.**

### F2 (C2 K2, item 4): a kept rejection whose flip cell is a placeholder passes the landed Run line

Two twins differing from `record.md` only in R1's `flip_condition` cell:

| twin | flip cell | `verify-sweeps` (item-4 Run line) | `verify-all` |
|---|---|---|---|
| `atk4-dash-flip.md` | `-` | `flip=present observed=complete verdict=match`; `REJECTIONS_OK=1/1`; `RESEARCH_GATE: CLEAN`; **rc 0** | all sections CLEAN, rc 0 |
| `atk4b-flip-none.md` | `none` | not run separately; its composed suite shows the sweeps section `verdict=CLEAN tally=VERIFIED_SWEEPS=0/1 REJECTIONS_OK=1/1` | all sections CLEAN, rc 0 |

The item-4 Run line itself is therefore measured directly on the `-` twin (rc 0); the `none` twin is
measured through the composed gate, which runs the same `verify-sweeps` child and reports it CLEAN.

Receipts: `08-09-item4-twins.txt`, `09b-verify-all-item4-twins.txt`. The criterion is cell
non-emptiness: `sweep_flip_cell` accepts any non-empty value, and this lane's tables use `-` for "no
value" (e.g. `corpus/fixtures/sweeps-r5.md` chain hop 3 uses `-` in both anchor columns). Under that
convention a `-` flip cell is a missing flip-condition, and the record that says `none` declares its
own absence — yet the item-4 Run line exits 0. **C2 K2 also fires on this reading.** I record it as a
second firing with the reading stated; F1 alone is enough for K2 and does not depend on placeholder
semantics.

### F3 (non-kill, item 1): the Run line does not enforce the pin it is documented to require

`claims-nopin.jsonl` is a two-claim claims file (C1 and C2, the same spans as `claims.jsonl`) with no
`sha256` field. Item 1's line on it:
`VERDICT_BEARING_CLAIMS=2/2`, `RESEARCH_GATE: CLEAN`, **rc 0** (`03-item1-root-and-pin-probes.txt`).
The item text itself admits "a claim without a pin is not checked for revision", so this is an
admitted limit, not a hidden defect — but the checklist line reads as if pins were enforced, and the
trial record's own pins are what caught the changed byte in §3. A reader who follows only the Run line
gets no revision guarantee.

## 5. Which checklist lines were awkward or wrong in practice (plainly)

1. **Item 1** — the Run line's fixed `--root ..` is wrong for a record under
   `corpus/evidence/round81/trial/` unless the gate's `LANE_ROOT` fallback saves it, which it does here;
   the caller cannot tell from the output which root actually resolved the sources, and the adjusted
   `--root .` is unobservable in the verdict. The line also has no placeholder for the claims path (only
   `<claims.jsonl>`), no pin requirement, and no fail leg unless the caller happens to change a byte.
2. **Item 2** — the composite `! … | grep -q … && …` is awkward: on the defect it exits 1 **without
   printing why** (the failing finding is swallowed by the pipeline), and the gate's own exit code is
   discarded by `grep`. It only tests the claim's `sweep` *cell*, not whether the sweep exists. The
   dangling-id form in F1 passes. If the Run line were used under `set -o pipefail` it would also read
   as a failure on the pass path.
3. **Item 4** — it checks cell presence, not whether the condition is one; `-` and `none` pass. It also
   does not check that the row's `ref` resolves (integrity does; the URL ref is exempt by design).
4. **Item 5** — correct and useful, but non-hermetic: its pass leg needs a live GET, so the "executable
   checklist" cannot be run offline or in a sandbox; and only the fail leg is exercised by the frozen
   counter (`CHECKLIST_RUN` item 5 leg uses `item5-fail.tsv`). This trial's item-5 run cost one network
   GET and is the only such fetch.
5. **Item 6** — the pinned value is host-specific (`3.12-modified`), and `grep -m1` closes the pipe so
   the gate exits **141 (SIGPIPE)**; the required line prints and the pipeline rc is 0, but a
   `pipefail` shell or a reader who checks the gate's rc would call a correct run a failure.
6. **The counter vs the record** — `checklist-run.py` measures the Run lines against frozen fixtures
   only; it never runs them against a real record. That is why `6/6` and `3/3` can pass while F1/F2
   show the landed lines do not produce their stated outcome on the current round's own record shapes.
   Items 1, 3, 6 are counted runnable-only; the trial exercised item 1's pass and fail legs on a real
   record, which the counter never does.

## 6. C1 measurements (not an attack seat for C1)

- `python3 -B corpus/evidence/round81/depth-r81.py --root <landing tree>` → `DEPTH_R81 entries=2
  fresh_rows=5 located_quotes=14`, `DEPTH_R81=PASS`, rc 0 (`14-depth-r81.txt`). The frozen C1 counter
  holds at the landing bytes.
- One counted quote from the correction/retraction entry (S205) was re-opened live by item 5 and read
  `VERBATIM` — not `ABSENT` (`10-item5-quote-reopen.txt`). That is one S205 row of C1's K2 check; the
  S203 PDF row was not re-opened (see Limits) and the remaining counted quotes were not re-opened by
  this seat.
- The trial record's two observations cite the committed captures with pins; both locate verbatim
  (`01-item1-verify-claims.txt`). No C1 kill rule fired on what this seat measured.

## 7. Limits / risks

- F2 rests on reading a placeholder (`-`, `none`) as "no flip-condition"; if the L1 rejects that
  reading, F2 is a reading-dependent finding. F1 does not have this dependency.
- F1's `W1` variant also passes the composed `verify-all`; the `SW1` variant passes only the item-2 Run
  line. Both are recorded, so the L1 can judge the kill rule on either.
- The item-2 defect record has no `## Sweeps` section at all; a defender could call this "a dangling
  reference" rather than "no sweep". The record names no location for its negative claim, which is the
  defect the item text names; the evidence is exact so the judgment is auditable.
- One live GET only (S205). S203's PDF row was not re-opened: this seat's egress grant names a re-open
  only when its item names it, and the item names a live fetch only for S205. C1's S203 K2 leg remains
  unmeasured by this seat.
- Trial artifacts are not corpus admissions: no `SOURCES.md`, registry, capture or refetch edit was
  made. Scratch `/fast/scratch/hyaku/chousa-r81/R81ExecTrial/` is deleted after this report.

VERDICT: R81ExecTrial C1 held — the depth counter passes at the landing bytes (`DEPTH_R81=PASS`, rc 0) and the one counted S205 quote re-opened live is VERBATIM, though this seat did not re-open an S203 quote.
VERDICT: R81ExecTrial C2 fired — the landed item-2 Run line exits 0 on a record whose negative claim names no location (dangling `W1`/`SW1`, no Sweeps row), and the landed item-4 Run line exits 0 on a kept rejection whose flip cell is `-` or `none`.
