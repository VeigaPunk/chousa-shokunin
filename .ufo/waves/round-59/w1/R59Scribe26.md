# R59Scribe26 — round-58 lesson/spot-check intake; round-59 Gate/Mistakes wording

Seat `R59Scribe26` (scribe, leaf, axis **depth**). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`,
all source repositories read-only, no fetch, no install, no spawn, no git/jj/index write.
Assignment: read the round-58 lesson and verifier spot-check, draft evidence-backed round-59
Gate/Mistakes (or report) wording, claim no check unrun. This file is my only write; scratch
`/fast/scratch/hyaku/chousa-r59/R59Scribe26/` is removed before yield.

This is the second pass over this seat path. It keeps the earlier drafts where they were right,
**adds executed measurements made in this pass**, and **corrects one statement** about C2 span bytes
(§3.3) that the earlier text left ambiguous.

---

## 0. What this pass executed (commands and observations)

Scratch only; every command below exited with the stated status in
`/fast/scratch/hyaku/chousa-r59/R59Scribe26/` unless noted.

```
sha256sum corpus/evidence/round58/c1-count.py → 65da18bb…703d3f   (406 lines)
sha256sum corpus/evidence/round58/c2-count.py → dbb85961…8503     (165 lines)
sha256sum tools/build-spans.py                → 1ed2650a…0bf6    (== the round-55 pin)
sha256sum tools/capture-text.py               → 2c0140bc…2573
git -C chousa-shokunin rev-parse HEAD         → af8c0a460d087cbfb8245fb9326608783ccc510b
git status --porcelain                        → "?? .ufo/waves/round-59/"  "?? corpus/evidence/round59/"  (nothing else)
git ls-tree -r --name-only HEAD corpus/evidence/round59 → (no output)
git ls-files corpus/evidence/round59                    → (no output)
git ls-tree -r --name-only HEAD corpus/evidence/round58 → 17 files, all present+tracked
bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa → exit 0, five W04
python3 -B corpus/evidence/round58/c1-count.py --builder tools/build-spans.py --work …/e2e-base
    → rc=1, 951 B stdout, byte-identical to head -c951 of the round-59 receipt (sha 2fc6f5c8…cc6d)
python3 -B corpus/evidence/round58/c1-count.py --builder tools/build-spans.py --work …/e2e-ctrl \
        --controls corpus/evidence/round58/controls  → rc=1, DENIED=2/2, C1=FAIL
python3 -B corpus/evidence/round58/c1-count.py --builder corpus/evidence/round58/controls/REFUSEALL.py …
    → rc=1, empty stdout, traceback at c1-count.py:212 FileNotFoundError
importlib probe of the frozen module's expect_refuse/expect_ok (no builder run) → §2.1
tools/capture-text.py on corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw + 12-quote offset sweep → §3
```

Not run by me: `c1-count.py` with a conforming positive builder; any lowercase-patched counter copy;
`c2-count.py` end-to-end; D2's `--seed 35` reproduction; mutation fixtures; any live fetch. Items below
that rest on those are attributed to the seat that measured them.

---

## 1. Round-58 lesson + verifier spot-check: what they establish

`corpus/lessons/round-58.md` and `corpus/lessons/round-58-verifier-spotcheck.md` agree on three things
that bound round 59:

1. **C1 (operability) is unprovable, not merely unmet.** The lesson's Mistake 1 says the frozen counter
   "cannot represent its positive state"; the spot-check re-checks the committed bytes and reaches
   "operability **unprovable** (C1); depth **unprovable** (C2)".
2. **The routed obligation for round 59** (spot-check, "Routed defects for next round"): "freeze
   must-pass positive controls that exercise the exact final counter predicate before wave data;
   repair/re-freeze C1 output-token comparison and C2 offset/rebuild contradiction before re-claiming
   either." Criterion 115 in `corpus/QUALITY.md:974` is the same duty as standing policy.
3. **The report rewrite rule** the spot-check enforced: correction is append-only; a filed report is
   never rewritten in place. My drafts below are therefore *content for the round's own Gate/Mistakes*,
   not edits to round 58.

Round 59, as measured in §4, has not discharged (2): no claims artifact, no repaired counter, no
committed positive control.

---

## 2. The round-58 C1 verdict path, re-derived with execution

### 2.1 The aggregate cannot accept its own refusal lines (D1, reproduced)

`c1-count.py:51` defines `PASS = "pass"`. Every refusal emitter formats with that constant:
`expect_refuse` success at `:160` (`f"{name}={PASS}(refused)"`), `FOREIGN` at `:223`, the
`SYMLINK_OUT` overwrite at `:234`. The aggregate searches uppercase: `ref_pass = all(("=PASS" in l) …)`
at `:391`; `SUMMARY … REFUSE={sum('=PASS' in l …)}` at `:399`.

Executed by importing the frozen module and calling its **own** `expect_refuse` with a process that
really refused (`rc=1`, reason present, forbidden path untouched). The module returned, verbatim:

```
LEG FOREIGN=pass(refused)   LEG SYMLINK_OUT=pass(refused)   LEG SYMLINK_CACHE=pass(refused)
LEG FIFO_TXT=pass(refused)  LEG DEVZERO_TXT=pass(refused)   LEG FAT_RAW=pass(refused)
LEG MANY_QUOTES=pass(refused)
ref_pass = False
REFUSE   = 0 / 7
```

So seven legs that the counter itself scores as passing produce `REFUSE=0/7` and `ref_pass=False`;
`verdict` at `:394` therefore cannot be `PASS` for any builder, and `exit 0` (`:402`) is unreachable.
The alternative `ok_pass` assignment at `:389` is dead (overwritten at `:390`).

### 2.2 The deny-control leg is vacuous twice over (D6, D6b — executed)

- `:377` flags a control only if the **inner** counter's stdout contains a line equal to `C1=PASS`.
  The inner invocation (`:372`) re-runs `HERE/c1-count.py` — the same frozen bytes — so by §2.1 it
  can never print that line. `CONTROL_*=PASS(!)` is dead code; `DENIED=n/n` is unfalsifiable.
- `REFUSEALL.py` exits 1 immediately (its whole body is one stderr line + `sys.exit(1)`), so the
  counter's own fixture write at `:212` (`foreign.write_bytes(...)` into `out-empty/spans/`) raises:

```
FileNotFoundError: [Errno 2] No such file or directory:
  '…/refuseall-probe/out-empty/spans/S777-1.txt'
```

  stdout was **empty**; `tail` is empty; `:377` therefore counts the control as `denied`. The denial is
  a **counter crash**, not an observed refusal. My control run reproduces the shape:
`CONTROL_REFUSEALL=denied`, `CONTROL_build-spans-r55=denied`, `DENIED=2/2`, `C1=FAIL`.

### 2.3 The three `rc=1` legs fail on diagnostic class, not on acceptance (D7 — read, reproduced in the receipt)

In the base run, `FIFO_TXT`/`DEVZERO_TXT`/`FAT_RAW` all returned `rc=1` yet failed the reason check:

- `FIFO_TXT`, `DEVZERO_TXT`: the pinned builder resolves `raw.is_file()` (false) then `txt.is_file()`
  — false for a FIFO and for a symlink to a character device — and falls to
  `"no defined text form for <key> (raw neither OLE nor zip, no .txt)"` (`tools/build-spans.py:90-91`).
  The FIFO was never opened (no hang), but `NOT_REGULAR`/`REGTYPE`/`FIFO` never appear.
- `FAT_RAW`: the fixture is an 80 MiB sparse file whose first 8 bytes are the OLE magic
  (`c1-count.py:282-290`). The builder sees `head[:8] == OLE` and hands it to `capture-text`, which
  refuses `ole-malformed` before any size test, so the required `SIZE` token never appears.

Consequence for a positive control: the declared reason classes are **ordering requirements** —
`SIZE` must be checked before format dispatch, and input type before content lookup. A conforming
builder that checks size after parsing fails `FAT_RAW` even though it is hardened.

### 2.4 What "`C1=PASS`" would still not certify (D8, and D3/D5 from the round-58 audit)

- `:399` recomputes the uppercase test for `SUMMARY`, so a token-repaired counter prints
  `REFUSE=0/7` **while** `C1=PASS` (`R59Executor01.md` §2, `R59Executor05.md` Run C — their
  measurements, not mine). The summary counts must never be cited as an operability metric.
- From the round-58 audit (cited, not re-run here): `SYMLINK_OUT`'s verdict is overwritten
  unconditionally at `:234`, so a candidate that writes through the symlink can still pass the leg;
  containment is only checked inside `expect_ok` (`:141-146`), so `C1=PASS` after the token repair is
  containment-unsound.

---

## 3. The round-58 C2 predicate: capture binding vs byte-identical rebuild

### 3.1 Measured form

`tools/capture-text.py` on `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`
(sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`, 129,024 B) exits 0 and
emits **27,012 chars**, form sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`.

### 3.2 Binding test (executed over all 12 frozen quotes in `c2/quotes.tsv`)

`c2-count.py:101-102` rejects a row when `occurrences[0] != off`, where `off` is the manifest's
`offset` cell. `tools/build-spans.py:142-149` writes `offset = str(start)` with
`start = max(0, off - CONTEXT)`, `CONTEXT = 80`. Measured:

```
 #   occurrence  start(written)  quote_len  span_len  line-start
 1          315             235         14       174   yes
 2          330             250         36       196   yes
 3          590             510         13       173   no
 4          683             603         29       189   no
 5          734             654         20       180   no
 6          781             701         15       175   no
 7          797             717         19       179   no
 8          838             758         33       193   no
 9          965             885         27       187   no
10          993             913         33       193   yes
11         1460            1380         27       187   no
12        11723           11643         21       181   no
```

`occurrence == start` holds for **0/12** rows (it can hold only when the quote starts at char 0).
Line-start anchors = **3/12** (315, 330, 993), exactly at the frozen floor with no margin.

### 3.3 Correction to the earlier draft of this report

The earlier text implied the counter and the builder disagree about span **bytes**. They do not:
`c2-count.py:105-107` computes `start = max(0, off-80)`, `end = off+len+80`,
`expected = form[start:end]`; the builder writes `text[start:off+len+80]`. For every row above the two
slices are identical, and the measured span lengths agree. The contradiction is confined to the
**offset cell**: `CAPTURE_BIND` requires `offset == occurrence`, the pinned builder writes
`offset == occurrence-80`. Writing `occurrence` satisfies binding but changes `spans.tsv` bytes, so
`BUILDER_REBUILD_MISMATCH` (`:124-129`) fires. Exactly one of the two frozen clauses can hold — for
every quote whose occurrence is not 0.

---

## 4. Round-59 state as measured (2026-10-27 15:14 → 15:24 -03)

| Fact | Evidence |
|---|---|
| `corpus/evidence/round59/claims.md` **absent** at four reads | `15:14`, `15:16:56`, `15:20:08`, `15:23:57`; directory holds exactly 2 files |
| Round-59 evidence is **untracked** | `git ls-files corpus/evidence/round59` → empty; `git ls-tree -r HEAD corpus/evidence/round59` → empty; `git status --porcelain` → `?? corpus/evidence/round59/`, `?? .ufo/waves/round-59/`; HEAD `af8c0a46…510b` |
| Round-58 evidence is tracked | `git ls-tree -r HEAD corpus/evidence/round58` → 17 files (claims, both counters, `c2/quotes.tsv`, all controls) |
| Only pre-data receipt | `corpus/evidence/round59/controls/c1-before.txt`, 958 B, **16 lines**, sha256 `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`, mtime `15:14:30.645295308 -0300` |
| Receipt byte decomposition (executed) | first **951 B** = counter stdout, sha256 `2fc6f5c851568c976f78ee07c73fa92484d11f498243903c546c6e3bbec0cc6d`; last **7 B** = literal `EXIT=1\n` |
| Receipt is **reproducible, byte-exact** | `python3 -B corpus/evidence/round58/c1-count.py --builder tools/build-spans.py --work <fresh>` with **default `--seed 7`** and no `--controls` regenerates the 951 B (diff identical), so the content is reproducible from recorded inputs; whether the committed file came from a fresh run or a copy is **not decidable** from these bytes |
| Receipt is byte-identical to round 58's | `cmp` with `corpus/evidence/round58/controls/c1-before.txt` → identical (`2c9bbe54…`) — expected, because the counter and `tools/build-spans.py` (sha `1ed2650a…`, the r55 pin) are unchanged |
| Receipt records no command, no builder/counter path, no seed, no `--controls` | 16 lines: 12 legs + `DENIED=0/0` + `SUMMARY` + `C1=FAIL` + `EXIT=1` |
| Leg outcomes reproduced | `OK=4/4`; `FOREIGN` rc=0 with the foreign file deleted; `SYMLINK_OUT` rc=0 with target-dir-written; `SYMLINK_CACHE` rc=0; `MANY_QUOTES` rc=0; `FIFO_TXT`/`DEVZERO_TXT`/`FAT_RAW` rc=1 with the wrong reason class (§2.3) |
| No after/positive/C2 receipt | the directory has exactly `census-start.txt` + `controls/c1-before.txt`; no `c1-measure-after.txt`, no `c2-*` |
| No committed positive control | `git ls-tree -r HEAD` filename scan for `c1-ideal|positive|mock-builder|must-pass` finds only unrelated `corpus/fixtures/*positive*` files |
| Census | validator exit 0, five W04 (S051/S053/S073/S074/S075); `corpus/SOURCES.md` sha256 `666dc9f16ccf6ece45529d60ec5e529d6a968dff49840c9c01d864885eb2cbc4`; `census-start.txt` sha256 `09ce4a959ddba208da141bc97e872fd5eb36fd428390a1ecf8cf741853016207` |
| No source opened, no fetch | no round-59 capture record; L0 question `8d77e6c1` still open |

**Reading.** The only round-59 artifact before wave data is a *reproducible but unbound* before-state:
its content is exactly what the frozen counter prints for the unpatched base, and it records no
provenance of its own. Nothing in the round is bound to a claim predicate; nothing demonstrates a
positive verdict path; the positive-path observations available in the wave are scratch or peer
measurements (§8).

---

## 5. Draft A — Gate wording for `corpus/lessons/round-59.md`

`⟨…⟩` marks facts only the round owner can supply. Nothing here asserts a pass.

```markdown
## Gate

### Read-time precondition (binding defect, recorded not repaired)

- `corpus/evidence/round59/claims.md` does not exist in the lane tree. Measured at 15:14, 15:16:56,
  15:20:08 and 15:23:57 -03 the same day: the evidence directory held exactly `census-start.txt` and
  `controls/c1-before.txt`; `git ls-files corpus/evidence/round59` and
  `git ls-tree -r HEAD corpus/evidence/round59` both returned empty, and `git status --porcelain`
  listed `?? corpus/evidence/round59/` (HEAD `af8c0a46…510b`). No seat output in this wave is bound to
  a frozen predicate, and this lesson makes no claim-level verdict.
- The only pre-data receipt is `ancillary`: `corpus/evidence/round59/controls/c1-before.txt`, 958 B,
  16 lines, sha256 `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`, mtime
  15:14:30 -03. Its bytes are the frozen counter's stdout (951 B, sha256 `2fc6f5c8…cc6d`) followed by
  the literal `EXIT=1\n`; the receipt records no command line, no seed and no `--controls`, so the
  command was reconstructed and re-run: `python3 -B corpus/evidence/round58/c1-count.py --builder
  tools/build-spans.py --work <fresh>` (default `--seed 7`) reproduces the 951 B byte-for-byte. The
  receipt is therefore reproducible content, and equally reproducible evidence of the *unrepaired*
  state, not a control.
- The receipt is byte-identical to `corpus/evidence/round58/controls/c1-before.txt` (same sha256),
  which is what an unchanged counter (`65da18bb…`) and an unpatched builder (`1ed2650a…`, the r55 pin)
  must produce. Byte-identity here is not evidence of copying and not evidence of a fresh run; the
  digest chain is the only fact the Gate may use.

### Source opened / candidate decisions

- No source was opened and no live fetch was made; the fetch-scope L0 question `8d77e6c1` remains open.
  Offline reconnaissance only: the census validator exits 0 with the five pre-existing W04 warnings
  (S051/S053/S073/S074/S075), `corpus/SOURCES.md` sha256 `666dc9f1…cbc4`, counting command
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → 133.
- Admit as source evidence, not as a claim: ⟨none / row S… reopened from a lane capture with digest,
  located quote, access date⟩.
- Reject: any statement about the present-day status, validity or legal force of a cited standard, and
  any reading of the five W04 URL warnings as duplicate claims or invalid sources. Flip: an
  operator-approved research window plus a located current authority.
- No knowledge entry, no `SOURCES` row change and no frontier move is claimed this round.

### Controls frozen before wave data (calibration duty)

- **No positive control exists in the lane.** Round 58's routed obligation — "freeze must-pass positive
  controls that exercise the exact final counter predicate before wave data" (round-58 verifier
  spot-check; `corpus/QUALITY.md` criterion 115) — is not discharged: no committed builder reaches the
  declared target token, and no repaired counter is frozen. The only positive-path observations in this
  wave are scratch mutations made by W1 seats and are not round evidence.
- A positive control accepted into a future freeze must be a lane byte with a digest, and must satisfy
  all of: (a) prints the exact target token (`C1=PASS` or the repaired spelling) **and** exits 0;
  (b) is run by the same counter bytes and the same `--work` discipline a verifier can repeat;
  (c) satisfies every safe leg including the counter's exact span slice
  `form[offset : offset+len+min(80,offset)+80]`, which is shorter than the builder's natural
  `[-80, +80]` window whenever the quote begins before char 80; (d) produces each declared refusal
  class in the declared order (type before content; size before format dispatch for `FAT_RAW`);
  (e) leaves `DENIED=n/n` non-zero with controls whose denial is an observed refusal, not a harness
  crash.
- Negative controls must include one that fails for an *observable reason*; `REFUSEALL`'s `denied`
  today is produced by a `FileNotFoundError` at `c1-count.py:212` before any leg prints, so it cannot
  discriminate.

### Counter status (frozen round-58 bytes, unmodified)

- `corpus/evidence/round58/c1-count.py` sha256 `65da18bb…703d3f`, `c2-count.py` sha256 `dbb85961…8503`;
  no repair was landed or claimed this round. Their measured defects are re-freeze requirements, not
  round-59 results: refusal legs print `=pass` while the aggregate and SUMMARY search `=PASS`
  (`:51,160,223,234,391,399`); the deny leg can only be flagged by the counter's own unreachable
  `C1=PASS` (`:377`); C2 `CAPTURE_BIND` (`:100`) requires the manifest offset to equal the quote
  occurrence while the pinned builder writes `occurrence-80`, so binding and byte-identical rebuild
  cannot both hold.
- No axis score changes are claimed. Operability stays **3/10** as scored; depth is unchanged; this
  lesson records the binding and calibration state, not an improvement.
```

---

## 6. Draft B — Mistakes wording for the round-59 lesson

**M1 is outcome-independent. M2 holds of the round as measured. M3 is the calibration duty. M4 is
conditional on a repair landing in a later round.**

```markdown
## Mistakes

1. **unbound — the wave ran without the frozen claim it is judged against** · Evidence: no
   `corpus/evidence/round59/claims.md` at 15:14, 15:16:56, 15:20:08 or 15:23:57 -03; the evidence
   directory held two files; the directory is untracked (`git ls-files` empty, `git status` `??`), so
   even the before-state has no commit to bind to. Every seat verdict in the wave is therefore
   unbound to a predicate and can neither support nor refute a claim. Captured-by: criterion 115's
   sequencing rule and the round-58 spot-check's routed defect. Fix: commit the claims artifact and
   its digest before dispatching data seats; bind every receipt to that digest in the report. Flip:
   the claims file exists with a citable digest and each receipt quotes it.

2. **vacuous — the only round-59 receipt cannot distinguish a healthy refusal set from a broken one** ·
   Evidence: `controls/c1-before.txt` (958 B, sha256 `2c9bbe54…ebfe`) is the frozen counter's stdout
   (951 B, sha256 `2fc6f5c8…cc6d`) plus `EXIT=1\n`, with no command, seed or `--controls` recorded;
   it ends `SUMMARY OK=4/4 REFUSE=0/7 … DENIED=0/0`, `C1=FAIL`. Of the seven refusal legs, four
   returned `rc=0` with real side effects (FOREIGN deleted, SYMLINK_OUT wrote its target,
   SYMLINK_CACHE and MANY_QUOTES accepted) and three returned `rc=1` with the wrong reason class
   (type forfeited to "no defined text form"; format refusal pre-empting SIZE). Independently, the
   frozen aggregate cannot count a correct refusal at all: seven legs its own formatter scores
   `pass(refused)` yield `REFUSE=0/7`, `ref_pass=False` (`:391`), so `C1=PASS` and exit 0 are
   unreachable for any builder. Fix: never quote `REFUSE=n/7` or `DENIED=n/n` as an operability
   measure; quote leg-level outcomes and the verdict token, and require the token to be reachable.
   Flip: a receipt whose safe and refusal legs are individually shown able to fail.

3. **uncalibrated — "controls falsify the predicate" was never demonstrated for the positive path** ·
   Evidence: no committed positive control exists (`git ls-tree` scan for `c1-ideal|mock-builder|
   must-pass` finds only unrelated fixtures); the deny leg is dead twice over — it can only be flagged
   by the counter's own unreachable `C1=PASS` (`:377`, inner re-invocation uses the same frozen
   bytes), and `REFUSEALL` denial is a harness `FileNotFoundError` at `:212` before any leg prints
   (measured: empty stdout). Round-58's routed obligation and criterion 115 require the opposite.
   Fix: freeze a lane-byte positive control with digest, exact target token, exit code, and the
   counter's exact span slice; freeze negatives whose denial is an observed refusal; run the sweep
   before wave data. Flip: a committed positive control reproduced by a non-author seat, and a
   negative that fails for a named reason.

4. **(if a repair lands) the repaired predicate still needs the round-58 defects closed, not just the
   token** · Evidence: `:136-140` expects a span shorter by `offset` when the quote starts before
   char 80, which fails a correct builder (`R58ExecC1CounterAudit.md` D2 at `--seed 35`);
   `:232-236` overwrites the `SYMLINK_OUT` verdict, so a leak through the symlink can still pass;
   `:399` still prints `REFUSE=0/7` under `C1=PASS`; C2 needs one offset convention for binding and
   byte-identical rebuild. Fix: one mutant probe per defect before re-freezing, each recorded as a
   leg that flips. Flip: the repair receipt shows each leg both passing and failing across its
   mutants.
```

---

## 7. Draft C — report-table rows (fill rules, not results)

| Claim | Before → after | Counting command / revision | Verdict |
|---|---|---|---|
| C1 operability | Before: `tools/build-spans.py` sha `1ed2650a…`; `controls/c1-before.txt` sha `2c9bbe54…`, `OK=4/4 REFUSE=0/7 DENIED=0/0`, `C1=FAIL`, exit 1, reproducible with default seed 7. After: ⟨receipt path + digest, or "none"⟩ | ⟨the exact `python3 …/c1-count.py …` line **as recorded in the receipt**, including `--seed` and `--controls`⟩ | ⟨**unchanged** (no after-receipt) / **unprovable** (positive token unreachable) / **improved** only with token + exit 0 + legs shown able to fail⟩ |
| C2 depth | Before: ⟨`C2=FAIL` receipt/digest, or "no C2 receipt this round"⟩ | ⟨`c2-count.py --root … --work …` line⟩ | ⟨not claimed unless `CAPTURE_BOUND` and `REBUILD` both pass under one offset convention⟩ |
| calibration | Before: no committed positive control; deny leg vacuous (§2.2) | ⟨two receipts: positive target token + negative named reason⟩ | ⟨**unchanged** unless a must-pass control and a falsifying control both exist as lane bytes⟩ |

Rules not to relax: no axis score change without a reachable predicate; `REFUSE=n/7` and `DENIED=n/n`
are not measures; a control that passes only after editing frozen bytes is a **repair** and needs both
receipts; a scratch probe is not a control.

---

## 8. Cross-seat corroboration and recorded conflicts

Agreement (my execution vs the peer's statement):

| Peer statement | What I measured |
|---|---|
| `R59Executor01.md` §1 "the frozen counter cannot print `C1=PASS` for *any* builder"; §1 receipt `REFUSE=0/7` with an all-legs candidate | Agree: §2.1 probe + my base run; the all-legs candidate itself is theirs, not mine |
| `R59Executor01.md` F5 "`round59/controls/c1-before.txt` is byte-identical to `round58/controls/c1-before.txt`" | Agree (`cmp` identical, sha `2c9bbe54…`), with the qualification in §5: expected under unchanged bytes, and the content is reproducible, so identity alone proves neither copy nor fresh run |
| `R59Executor05.md` "REFUSEALL aborts the harness with `FileNotFoundError` before any `C1=` line, denial-by-crash" | Agree: §2.2 traceback at `:212`, empty stdout |
| `R59Executor01.md` F2 / `R59Executor05.md` Run C (`C1=PASS` with `REFUSE=0/7` after the single token fix) | Code read agrees (`:399` recomputes uppercase); the PASS receipt is theirs, I did not run a repaired counter |
| `R59Critic56.md` §1 leg-level reading of the receipt | Agree with the four `rc=0` legs and the three reason-class failures |
| `R59Critic59.md` §1 "`CONTROL_REFUSEALL=denied` … results from counter crash" | Agree, executed (§2.2) |

Conflicts, recorded verbatim rather than adjudicated:

- `R59Critic57.md:8`: "the latter contains only an empty line." Measured: 958 bytes, 16 lines, sha
  `2c9bbe54…`, mtime `15:14:30.645295308 -0300`; `R59Critic57.md` mtime `15:14:51.234719522 -0300`,
  i.e. 21 s later. On the mtimes a read after 15:14:30 sees content, so the empty-line report is not
  explained by a write race with that mtime; I do not know what path or buffer it read.
- `R59Critic59.md:5`: "`git ls-tree -r --name-only HEAD corpus/evidence/round59` lists only round59
  `census-start.txt` and `controls/c1-before.txt` under round59". Measured at HEAD `af8c0a46…`:
  `git ls-tree` returns **no output** and `git ls-files corpus/evidence/round59` returns nothing; the
  directory is untracked (`?? corpus/evidence/round59/`). The cited HEAD matches; the tree listing does
  not.
- `R59Executor01.md` frames byte-identity as "a copy of the before receipt, not a control" — true as a
  statement about its status (it is not a control) and not contradicted by my run, but byte-identity is
  also the necessary output of re-running unchanged bytes, so it should not be read as evidence of
  copying.

Scratch attribution: `/fast/scratch/hyaku/chousa-r59/R59Executor07/` holds a C2 poison probe that is
not mine (`R59Executor07-2` raised it; I confirmed my writes are confined to my own scratch dir and
declined to remove it).

---

## 9. Limits

- I did not run `c1-count.py` against a conforming (all-legs) builder, so I do not claim a personal
  `C1=PASS` observation; §2.1 uses the module's own formatter, §2.2/2.3 use real runs.
- I did not run a lowercase-patched counter; F2/D8 rest on code read plus `R59Executor01.md` §2 and
  `R59Executor05.md` Run C.
- I did not run `c2-count.py` end-to-end, nor the `--seed 35` D2 reproduction. §3 is a direct
  measurement of form, occurrences, builder offsets and the two predicates, not a counter run.
- I did not re-derive the counter's fixtures from scratch beyond §2.3; the leg outcomes I quote are
  from my own base run's stdout, byte-identical to the receipt.
- No fetch, no install (so `/home/vgpnk/.omp/agent/RULES.md` was not consulted for an install), no
  git/jj/index write, no edit to frozen claims, counters or controls.
- Round-59 artifacts may change after 15:24 -03; §4 is scoped to that window.

## 10. Routing for the round owner

1. Either commit `corpus/evidence/round59/claims.md` (with digest) and bind every receipt to it, or
   declare in the round report that no claim-level verdict is given. The untracked state of the whole
   evidence directory is itself a binding failure to fix before dispatch.
2. Do not re-claim the round-58 C1/C2 predicates; land the token repair **together with** the D2/D3/D5
   span and containment fixes and one mutant per leg, then freeze a lane-byte positive control that
   prints the exact token and exits 0.
3. Rebuild the deny leg so denial is an observed refusal: run each control against the declared hazard
   legs directly, and treat a crash as `ERROR`, never `denied`.
4. When quoting the round-59 receipt, cite size + sha256 `2c9bbe54…ebfe` and say `DENIED=0/0`; cite the
   951-byte stdout digest `2fc6f5c8…cc6d` and the default seed 7 when claiming reproducibility.

Report: `.ufo/waves/round-59/w1/R59Scribe26.md`

VERDICT: Gate/Mistakes wording drafted on executed bytes, not on a claim. Executed this pass: the
frozen counter reproduces the round-59 before receipt byte-exactly (951 B stdout + `EXIT=1`), its
seven passing refusal legs still yield `REFUSE=0/7`/`C1=FAIL`, the deny leg is dead by construction and
its `denied` is a harness `FileNotFoundError`, and C2's `CAPTURE_BIND` fails 0/12 rows against the
pinned builder's `occurrence-80` offset while span bytes agree. Falsified along the way: that the
receipt is unauditable (it is reproducible from recorded bytes), that byte-identity to round 58 proves
copying (it also follows from unchanged bytes), and that `REFUSE=0/7` measures refusal behaviour (it
measures a token mismatch). Round 59 itself remains unbound: no claims artifact, no committed positive
control, no after-receipt.

---

## Appendix P — provenance for this path (appended by the first pass of this seat, 15:27 -03)

- **Two passes share this path.** Pass 1 filed a 236-line draft (sha256
  `9aa894258ed21994a0c058c1abc7bb0c608d323d0bec3fad29e4b941704ac0a6`); pass 2 replaced it at
  `15:26:05` with the present report. Pass 2's §3.3 correctly narrows the pass 1 wording: the counter
  and builder do **not** disagree about span bytes (they agree on all 12 rows); the contradiction is
  confined to the offset cell. Pass 1's other verified items are carried in §2.1, §3.2 and §4.
- **Independent re-check of §4's key numbers** (run by pass 1 at 15:27 in
  `/fast/scratch/hyaku/chousa-r59/R59Scribe26-verify/`, since removed):
  `python3 -B corpus/evidence/round58/c1-count.py --builder tools/build-spans.py --work <fresh>
  --seed 7` → stdout sha256 `2fc6f5c851568c976f78ee07c73fa92484d11f498243903c546c6e3bbec0cc6d`, the same
  digest as `head -c 951` of `controls/c1-before.txt`; `corpus/SOURCES.md` sha256 `666dc9f1…cbc4`;
  `git rev-parse HEAD` `af8c0a46…510b`. Three §4 numbers confirmed by a second execution, independently
  of pass 2.
- **Reciprocal scratch collision, recorded because it explains two paths.** Pass 1 removed
  `/fast/scratch/hyaku/chousa-r59/R59Scribe26/` at ~15:17; another writer recreated it at 15:20–15:23
  (`base.out`, `ctrl.out`, `probe_agg.out`, `probe_c2.out`, `ra.err`, `refuseall-probe/`, `e2e-base/`,
  `e2e-ctrl/`); it is absent again at 15:27. The foreign copies inside it went with the directory; the
  citable copies remain in `R59Executor07/positive-path/keep/`. Pass 1 did not delete them and recorded
  their digests: `probe_agg.out` `3da34e43…`, `probe_c2.out` `c056dd50…`, `ra.err` `9b5aec39…`.
- **Attribution resolution (15:26).** `R59Executor07-2` confirmed the `R59Executor07/` writer is a
  duplicate instance of its own seat and accepted the attributed append; its F4 (control-gate vacuity)
  is the same finding as §2.2/D6 reached independently. §8's "not mine" remains true for this seat's
  writes; ownership of the `R59Executor07/` bytes is settled as same-seat duplicate, still scratch-only
  and not citable as a control.
- **One corroborating receipt not in §8:** `R59Executor07/positive-path/keep/c1-positive.txt` (sha256
  `105c3d41…`) is a purpose-built all-legs builder that prints every leg as `pass` and still yields
  `REFUSE=0/7`, `C1=FAIL`, exit 1 — the strongest single confirmation of §2.1. It is the duplicate's
  scratch, not this seat's measurement, so §9's limit stands unchanged.
