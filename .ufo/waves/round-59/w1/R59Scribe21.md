# R59Scribe21 — round-59 `Gate` / `Mistakes` wording draft

Seat: scribe (leaf; no dispatch, no fetch, no install, no lane writes except this file).
Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `af8c0a460d087cbfb8245fb9326608783ccc510b`
(`git rev-parse HEAD`, ran). Axes carried by this item: depth. Observation window
`2026-10-27T18:12Z`–`18:21Z`. All lane paths below are relative to the lane root; fleet paths are written
absolute or prefixed `.ufo/` under the fleet root `/home/vgpnk/Projects/shokunin`.

Deliverable: a liftable `## Gate` and `## Mistakes` body for `corpus/lessons/round-59.md`, grounded only in
bytes that exist, plus the constraints the round-59 report must satisfy. The draft is **conditional**: it is
written against the state actually observed (no round-59 freeze), and it names the exact replacement clauses
for the case where a freeze lands before the lesson is filed. It is a draft; the lesson, LOG, SCORECARD and
claims files are not mine to write.

## 0. Behavior (what this seat did)

Read: `corpus/lessons/round-58.md` (39 lines), `corpus/lessons/round-58-verifier-spotcheck.md` (38 lines),
`corpus/evidence/round58/claims.md`, `corpus/evidence/round58/c1-count.py` (406 lines),
`corpus/evidence/round58/c2-count.py` (165 lines), the round-58 control receipts and `c2/quotes.tsv`,
`corpus/QUALITY.md:974`, `SCORECARD.md` (round-58 block), `LOG.md` (round-58 close),
`.ufo/waves/round-59/w1-spec.json`, `.ufo/waves/round-59/w1-dispatch.json`, `w1.ready`, `w1.ready.partial`,
`.ufo/l0-questions.md` (fleet root), `considerthese/2026-10-26.md`, `SHONEN.md`,
`corpus/evidence/round58/s101-open.txt`, and the peer reports `R59Critic55.md`, `R59Scribe22.md`,
`R59Scout29.md`.

Ran (exact commands are quoted in §1; every claim below is tagged with what produced it):

- `python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` with
  `PYTHONDONTWRITEBYTECODE=1 TMPDIR=/fast/scratch/hyaku/chousa-r59/R59Scribe21` → stdout 47,356 bytes /
  27,012 characters. Read-only; no lane file touched.
- `python3 -c` analyses over that stdout and over `corpus/evidence/round58/c2/quotes.tsv`
  (quote uniqueness/offset/word counts).
- Deterministic file facts: `sha256sum`, `diff`, `wc -l`, `stat -c '%s %y'`, `grep -c`, `git status --porcelain`,
  `git log -1`, `git show --stat`.

**Not run, and not claimed:** `scripts/sources-census.sh validate`, `corpus/evidence/round58/c1-count.py`,
`corpus/evidence/round58/c2-count.py`, `tools/build-spans.py`, any `controls/*` builder, any mutation or network
tool. The census `exit=0` in §1 is the **content of a receipt file**, not a validation this seat executed.

## 1. Evidence ledger (verified — each row names its producer)

| # | Fact | Producer | Exact basis |
|---|---|---|---|
| E1 | No round-59 freeze exists at the path the wave names | `read` + `test -e` + `find` | `read corpus/evidence/round59/claims.md` → “Path not found”; `test -e …; echo $?` → `1` at `18:15:31Z`, `18:17:16Z`, `18:18:27Z`, `18:21:03Z`; `find corpus/evidence/round59 -type f` → exactly `census-start.txt` (535 B, 7 lines) and `controls/c1-before.txt` (958 B, 16 lines); `.ufo/waves/round-59/predata/` empty |
| E2 | Wave was marked ready before the freeze/predecessor receipt was written | `stat`, `cat` | `w1.ready` mtime `18:12:15Z` (154 B, body names `l1: ChousaR59`); `controls/c1-before.txt` mtime `18:14:30Z`; `w1.ready.partial` lists six names (ramp in progress). At `18:14Z` the before-receipt was observed at size 0 mid-write, then at 958 B |
| E3 | Round-59 “before” receipt is byte-identical to round-58’s | `sha256sum`, `diff` | both `2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe`; `diff` → `rc=0` |
| E4 | That identity is *expected* under determinism, not evidence of a copy | `sha256sum`, `diff` | `tools/build-spans.py` and `corpus/evidence/round58/controls/build-spans-r55.py` are the same bytes (`1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`); `git log -1 -- tools/build-spans.py` → `6ca9249` (2026-10-27T00:42:38-03:00). No round-58 patch landed, so the only builder in the tree is the pinned base |
| E5 | The receipt cannot distinguish copy from re-run | `head`/`cat` | `c1-before.txt` has no `Command:`/revision line. Contrast `corpus/evidence/round58/controls/c1-controls.txt:1`, which starts `Command: \`python3 corpus/evidence/round58/c1-count.py --builder …\`` |
| E6 | Round-58 C1 `C1=PASS` is unreachable for **any** builder | static read of `c1-count.py` | `51: PASS = "pass"`. Every refusal line is emitted through that constant: `147` `expect_ok`, `160` `expect_refuse` → `{name}={PASS}(refused)` (FIFO_TXT, DEVZERO_TXT, FAT_RAW, MANY_QUOTES, SYMLINK_CACHE), `207` REBUILD_OK, `223` FOREIGN → `{PASS}(refused)`, `234` SYMLINK_OUT → `{PASS}(refused)`. The only literal uppercase `=PASS` writes are `377–378` (a control’s *tail* string, not a refusal leg) and the aggregates `391`/`399`. `ref_pass` (`391`) requires `=PASS` in every refusal line; Python `in` is case-sensitive; each of the seven refusal legs appends exactly one line (`218–306`; the FIFO/DEVZERO `except` branches and FOREIGN’s three branches still yield one line and never an uppercase `=PASS`), so `ref_legs` always has 7 entries. Hence `ref_pass` is False in every run and `verdict` (`394`) is always `FAIL` |
| E7 | The aggregate carries dead code as well | static read | `389` assigns `ok_pass` then `390` overwrites it; the `389` expression is already unsatisfiable for `EMPTY_OK=pass` (it does not end with `)`). Frozen claim bytes cite `391`/`399`; `389–390` should be cited too if the defect is repaired under a new file |
| E8 | Round-58 C2 bind/rebuild clauses are mutually exclusive | static read + receipts | `101` requires `occurrences[0]==off`; `105` slices `form[off-80:off+len+quote+80]`; `124` requires `tmp/spans.tsv` **bytes** equal the committed manifest, i.e. the pinned builder’s own offset convention (span-start, per `LOG.md` round-58 close). Receipts in `SCORECARD.md:2902` block: builder manifest → `CAPTURE_BOUND=0/12 REBUILD=MATCH`; occurrence-offset rewrite → `CAPTURE_BOUND=12/12 REBUILD=FAIL` |
| E9 | The C2 *content* is sound; only the binding convention is not | `python3 -c` over `c2/quotes.tsv` + capture-text stdout | 12/12 quotes occur exactly once in the 27,012-char defined form; 0-based offsets `315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723`; lengths ≤36 chars (max 36), so `QUOTE_TOO_LONG` never fires. A re-freeze can keep all 12 quotes and change only the offset/rebuild coupling |
| E10 | The S101 opening receipt reproduces exactly | `sha256sum` + `capture-text.py` + `python3 -c` | raw sha256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` (matches `corpus/evidence/round58/claims.md`); output 27,012 chars (matches `s101-open.txt`); `form.find("并以[文献类型标识/载体类型标识]表示") == 797`, `form.count == 1`, `form[797:816]` is the quote, context `…联机网络(online)—OL，并以[文献类型标识/载体类型标识]表示包括了文献载体类型的参考文献类型标识：\n如：[M`. 797 is the **0-based index** (1-based character 798); the counter’s `re.finditer` offsets are 0-based, so the receipt’s prose is consistent with the code but ambiguous to a human reader |
| E11 | The round-58 closure spot-check mislabels units | `python3 -c` | spot-check line reads “quote is exactly 19 whitespace-delimited words, below the ≤25-word cap”; measured `len(quote)=19`, `len(quote.split())=1`. `s101-open.txt` itself says “19 characters; one whitespace-delimited word”. The `≤25` cap is still satisfied (1 ≤ 25), so the agree verdict is unaffected |
| E12 | Round-59 wave shape is inside policy | `python3 -c` over `w1-spec.json`; `w1-dispatch.json` | 66 items; roles executor 16 / reviewer 14 / scribe 12 / scout 12 / critic 7 / mutation-tester 5; axes `operability, depth, calibration`; policy `waveMinLanes 64`, `waveMaxLanes 128`; `counts: spawn 66, resume 0, total 66`; `w1.ready` body `{"lane":"chousa","round":59,"wave":"w1",…,"l1":"ChousaR59"}` |
| E13 | Census at round start: 133 rows, `exit=0`, five W04 warnings | receipt + `grep -c` | `corpus/evidence/round59/census-start.txt` ends `exit=0` with S051/S053/S073/S074/S075 W04 lines; `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `133` (ran) |
| E14 | Census receipt format drifted from round-58’s | `diff` | `diff corpus/evidence/round58/census-end.txt corpus/evidence/round59/census-start.txt` → r58 end carries a `Command:` line and `EXIT=0`; round-59 start has no command header and lowercase `exit=0` |
| E15 | Criterion 115 is landed and names a positive-control duty | read | `corpus/QUALITY.md:974` (file is 974 lines): “…if the positive control cannot reach the token, do not dispatch or change the claim post-data. Shown able to fail (ran): the R58 positive-leg probe prints 11 passing leg lines but `REFUSE=0/7`, `C1=FAIL`, exit 1.” |
| E16 | L0 ids are fleet **commits**, not register ids | `git log`, read | `git log -1 8d77e6c1` → `round-29: chousa L0 question (quote re-open fetch scope)`; `git log -1 2c6edbab` → `round-57: chousa L0 admission ruling question`; `.ufo/l0-questions.md` rows are `lane \| round \| text` with no status column (head of file), so “open” is not machine-readable from the register |
| E17 | `CT-20261026-4` is a positional label, not source text | `grep` | the only literal `CT-` id in `considerthese/2026-10-26.md` is the example `CT-20261026-1` inside the id proposal at line 41; the cited item is the 4th proposal bullet (line 44, “Do one independent CJK quote spot-check per review”), so the id is assigned by the lane by position |
| E18 | Same-lane seats converged on the freeze absence | peer reports | `R59Critic55.md` (“not auditable … claims.md is absent”), `R59Scribe22.md` (“Read-first gate (fails)”), `R59Scout29.md` (“absent from the current lane tree”). Same-lane evidence: corroboration only, never discernment evidence |

## 2. Draft — `## Gate` body for `corpus/lessons/round-59.md`

Lift as-is for the observed state. Bracketed clauses are the replacements to use if a freeze lands before
filing; delete the branch that did not happen.

```markdown
## Gate

### Freeze state

- The wave context (`w1-spec.json` `context`) names `corpus/evidence/round59/claims.md` as frozen and
  required before work. At `18:12:15Z` the wave was marked ready (`.ufo/waves/round-59/w1.ready`); at
  `18:15:31Z`, `18:17:16Z` and `18:18:27Z` that path still did not exist (`read` → “Path not found”,
  `test -e` → 1), `corpus/evidence/round59/` held only `census-start.txt` (535 B) and
  `controls/c1-before.txt` (958 B), and `.ufo/waves/round-59/predata/` was empty. No round-59 claim
  predicate, source pin, counter, control builder or acceptance condition exists to adjudicate.
- The one predata receipt is `corpus/evidence/round59/controls/c1-before.txt` (mtime `18:14:30Z`, i.e.
  after `w1.ready` by 2 min 15 s). Its leg names, `SUMMARY`/`C1`/`EXIT` shape and byte content match
  `corpus/evidence/round58/c1-count.py` run against the only builder in the tree, giving
  `SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=0/0`, `C1=FAIL`, `EXIT=1`; with no command
  header, the exact invocation is inferred from that format, not recorded. Its
  sha256 is `2c9bbe54…`, byte-identical to round-58’s `controls/c1-before.txt`; that identity is the
  expected outcome of determinism (`tools/build-spans.py` is still the pinned round-55 builder,
  `1ed2650a…`), but the file carries no `Command:` or revision line, so from bytes alone a copy and a
  re-run cannot be distinguished.
- No admit/reject decision is made on round-59 evidence. [If a freeze lands before filing, replace this
  sentence with the claim ids, the frozen counter sha256 values, the must-pass positive-control receipt
  path, and the explicit before → target pair for each claim; a freeze landed after seat reports exist
  must be disclosed with its timestamp and the seats it could not have guided.]

### Source opened / candidate decisions (round-58 closure intake)

- **Admit as source evidence, not as admitted knowledge:** S101’s lane-held HIT capture states scoped
  rules and examples about reference-type/carrier labels (`并以[文献类型标识/载体类型标识]表示`, unique
  at 0-based offset 797 of the 27,012-character defined form, raw sha256 `6063a3af…`). This seat
  re-derived the offset and uniqueness from the committed raw capture with the pinned
  `tools/capture-text.py` (`corpus/evidence/round58/s101-open.txt` is the matching receipt). Round 58’s
  C2 counter could not verify its frozen predicate, so still no `knowledge/` entry is admitted.
- **Reject:** any claim about the current status, legal force or present-day use of GB3469. No live fetch
  was made while the fetch-scope ruling is open; flip condition unchanged — an operator-approved research
  window plus a located current authority.
- Unit correction to carry forward: the closure spot-check calls the quote “19 whitespace-delimited
  words”; measured it is 19 **characters** and **1** whitespace-delimited word. The `≤25` cap and the
  agree verdict are unaffected; copy the corrected units into the lesson.

### SOURCES changes

- Rows 133 → [133 if unchanged]: counting command
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `133` at this seat’s snapshot.
  Round-start census receipt: `corpus/evidence/round59/census-start.txt`, five pre-existing W04 warnings
  (S051, S053, S073, S074, S075) and `exit=0`. The census validator was **not** re-run by this seat; the
  `exit` value is read from the receipt. [If a row is added, name the row id, tier, and the added-row
  count by tier A/B/C, and re-run the validator for the end receipt.]
- Receipt-format note: the round-59 start receipt omits the `Command:` header that round-58 receipts carry
  and writes `exit=0` where round-58 wrote `EXIT=0`. Fold the command line in before the end receipt;
  token case is this lane’s documented failure mode (`QUALITY.md:115`).

### Outside spot-check

- The round-58 closure artifact (`corpus/lessons/round-58-verifier-spotcheck.md`, author
  `hyaku closure / @m_opus`) closes the duty that round-58’s lesson recorded as open: it re-opened the S101
  capture and agreed with both the admit-as-source-evidence decision and the reject on GB3469 present
  status. This is the non-author sample; the lane should cite it rather than re-assert “no sample exists”.
- [If no new non-author sample exists for round 59, say so plainly and do not claim discernment
  improvement; a same-lane wave is not a sample.]

### Open L0 items

- `.ufo/l0-questions.md` (fleet root; the lane has no copy of this file) holds `chousa | round-29` /
  `round-41` / `round-42` rows citing the fetch-scope id `8d77e6c1` and `chousa | round-57` carrying the
  admission-ruling question; both ids resolve to fleet commits (`round-29: chousa L0 question (quote
  re-open fetch scope)`; `round-57: chousa L0 admission ruling question`). The register has no status
  column, so this lesson must state “no operator answer is recorded in the register” rather than “open”
  as a verified state.
```

## 3. Draft — `## Mistakes` rows for `corpus/lessons/round-59.md`

House pattern: label · Evidence · Captured-by · Fix · Flip. M1, M2 and M6 record this round’s state;
M3–M4 are carried and sharpened from round 58; M5 is a wording defect in the closure artifact.

1. **ordering — the wave was made ready before the freeze it cites existed** · Evidence:
   `.ufo/waves/round-59/w1.ready` mtime `18:12:15Z`; the file it points readers to
   (`corpus/evidence/round59/claims.md`) did not exist at `18:15:31Z`, `18:17:16Z`, `18:18:27Z` or
   `18:21:03Z` (`read` → “Path not found”; `test -e` → 1); the only predata receipt was written at
   `18:14:30Z`; by `18:21:03Z` fifty-one seat report files existed under `.ufo/waves/round-59/w1/` while
   no claim text did
   (same-lane corroboration: `R59Critic55.md`, `R59Scribe22.md`, `R59Scout29.md`). · Captured-by: the
   freeze-before-data rule that `corpus/lessons/round-58.md` states (“Claims frozen … before any wave
   data”) and `corpus/QUALITY.md:115`’s pre-freeze positive control; both are satisfied only if the
   context path resolves when `.ready` is written. · Fix: write the claims file and the must-pass
   positive-control receipt before `w1.ready`, and have the ready step refuse when the context path does
   not resolve. · Flip: a `.ready` whose named claims file exists at dispatch time and whose mtime
   precedes the ready file, with the positive-control receipt already committed.

2. **provenance — a before-receipt with no command or revision line cannot distinguish a re-run from a
   copy** · Evidence: `corpus/evidence/round59/controls/c1-before.txt` sha256 `2c9bbe54…` equals
   round-58’s `controls/c1-before.txt` byte for byte (`diff` → 0); the builder bytes are unchanged
   (`1ed2650a…` == `controls/build-spans-r55.py`), so identity is expected — but the file has no
   `Command:` header, while `corpus/evidence/round58/controls/c1-controls.txt:1` does name its exact
   command. From the bytes alone, a copy and a deterministic re-run are indistinguishable. · Captured-by:
   `corpus/QUALITY.md` criterion 108 (a measurement citation names the revision its receipt header names)
   — that criterion presumes a header exists. · Fix: prepend `Command:`, the lane revision, and a UTC
   timestamp to every receipt, and make the end receipt re-derivable from its own first line. · Flip: a
   receipt whose first line names the exact command and whose recorded output is reproduced by running
   that command.

3. **vacuous — the round-58 C1 aggregate compares a token no refusal emitter writes (carried; sharpened
   from the lesson’s one-line statement)** · Evidence: `corpus/evidence/round58/c1-count.py:51`
   `PASS = "pass"`; every refusal emitter goes through it (`160`, `223`, `234`; the seven refusal legs are
   appended at `218–306`; each name yields exactly one line), while `391` requires `=PASS` and `399` counts `=PASS`; the only
   uppercase `=PASS` writers are `377–378` (a control’s tail string, outside `ref_legs`) and the
   aggregates. Python `in` is case-sensitive and `ref_legs` always has 7 entries, so `ref_pass` is False
   and `verdict` (`394`) is always `FAIL`; `389` is dead code overwritten by `390`. Independent receipts:
   `corpus/evidence/round58/controls/c1-before.txt` and `R58ScribeMistakeMine.md:57-83`. · Captured-by:
   `corpus/QUALITY.md:115` (positive control must reach the declared token) and criterion 86 (a counter’s
   tokenizer is run on a positive control seeded with the class it can mangle). · Fix: compare against
   `f"={PASS}(refused)"` or normalise case, delete the dead `389` assignment, and land a builder distinct
   from the pinned base that prints `C1=PASS` and exits 0 before any claim cites it. · Flip: one run of the
   counter on that builder prints `C1=PASS` and exits 0, and the same run on the pinned base still fails
   `FOREIGN`.

4. **vacuous — round-58 C2’s `CAPTURE_BIND` and byte-identical `REBUILD` require mutually exclusive offset
   conventions (carried)** · Evidence: `c2-count.py:101` requires `occurrences[0]==off`; `105` slices the
   span at `off-80`; `124` byte-compares the committed manifest to the pinned builder’s output, whose
   `offset` column is the span start. `SCORECARD.md` round-58 block records
   `CAPTURE_BOUND=0/12 REBUILD=MATCH` (builder offsets) and `CAPTURE_BOUND=12/12 REBUILD=FAIL`
   (occurrence offsets) — neither reaches `C2=PASS`. This seat adds that the *content* is sound: all 12
   frozen quotes occur exactly once in the 27,012-character form, offsets reproduce
   (`315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723`), and every quote is ≤36 characters. ·
   Captured-by: criterion 115 and criterion 110 (dry-run the recipe before dispatch). · Fix: keep the 12
   quotes, bind to occurrence offsets, and either pin a builder whose manifest writes occurrences or
   replace the byte-identical rebuild with a span-content comparison that states the builder’s convention.
   · Flip: one run with the frozen quote set prints `C2=PASS` and exit 0, and the entry lands with
   `used-by` naming it.

5. **calibration — the round-58 closure artifact mislabels character and word counts** · Evidence:
   `corpus/lessons/round-58-verifier-spotcheck.md` says “quote is exactly 19 whitespace-delimited words,
   below the ≤25-word cap”; measured on the quote `并以[文献类型标识/载体类型标识]表示`,
   `len(quote)=19` characters and `len(quote.split())=1` whitespace-delimited word, matching
   `corpus/evidence/round58/s101-open.txt` (“19 characters; one whitespace-delimited word”). · Captured-by:
   the lesson copies this sample; a copied unit error becomes a false measurement in the Gate. · Fix:
   record character and word counts as separate quantities, and state the cap’s unit. · Flip: the Gate’s
   quote row carries both counts and matches a re-derivation.

6. **format — the round-59 census receipt drops the command header and lowercases the exit token** ·
   Evidence: `diff corpus/evidence/round58/census-end.txt corpus/evidence/round59/census-start.txt` → the
   round-58 receipt starts `Command: \`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate …\``
   and ends `EXIT=0`; the round-59 start receipt has no command line and ends `exit=0`. · Captured-by: this
   lane’s own failure mode is a token-case mismatch (`QUALITY.md:115`); a receipt whose exit token changes
   case across rounds invites a reader or script to mis-count it. · Fix: restore the `Command:` line and
   one casing (the validator’s own output, unedited). · Flip: the end receipt diffs equal in header shape
   to the round-58 receipt, with only the timestamp/body differing.

## 4. Findings (report-facing, not lesson prose)

| id | finding | severity | status |
|---|---|---|---|
| F1 | Round-59 freeze absent at dispatch and through `18:21:03Z`; three peer seats independently recorded it (E1, E2, E18) | high — blocks claim-level adjudication and maps the whole wave to carry-over work | open; needs the claims file + positive-control receipt before any lesson claim |
| F2 | The predata before-receipt is written 2 min 15 s after `.ready`, and fifty-one report files exist before any claims text (`18:21:03Z`) | high — freeze-before-data is the round’s own control | open; fix in the ready step |
| F3 | Round-58 `C1=PASS` is unreachable for any builder; proven statically from all emitters, not only from the reported probe (E6, E7) | high — the round-58 C1 claim is unprovable as frozen | carried; lesson wording stands, add `389–390` to the cited lines |
| F4 | Round-58 `C2` contradiction is confined to the bind/rebuild convention; all 12 quotes verify against bytes (E9) | medium — a re-freeze can keep the corpus content and change only the counter coupling | carried; constructive input for the re-freeze |
| F5 | `tools/build-spans.py` is still the pinned round-55 base, so a positive control must supply a *different* builder (E4) | medium — a “positive” run reusing the default builder will fail `FOREIGN` by construction | open; name the builder and its sha256 in the new freeze |
| F6 | Before-receipt provenance is unverifiable from bytes (E3, E5) | medium | open; add the header |
| F7 | Census start receipt: 133 rows, `exit=0`, five W04 warnings, but no command header and lowercase exit token (E13, E14) | low | open; cosmetic but this lane has been bitten by token case |
| F8 | Closure spot-check unit error (“19 whitespace-delimited words”) and the trend disagreement below (E11, §6) | low — does not overturn the agree verdicts | open; correct the units when carrying the sample |
| F9 | `CT-20261026-4` is positional; the source file contains no such literal id (E17) | low — provenance of the intake label | note in the lesson; keep the id but say it is lane-assigned |
| F10 | Wave shape conforms: 66 seats inside the 64–128 band, axes operability/depth/calibration, L1 holds the planner seat (E12) | — | pass |
| F11 | A foreign writer used this seat’s assigned scratch path after this seat’s cleanup: my `form.txt` was deleted at `18:19:49Z` (verified absent), then `refuseall/`, `refuseall.err` (891 B), `refuseall.out` (0 B) appeared at `18:20:56Z` and `form.txt` (47,356 B) + `form.err` (0 B) at `18:21:34Z`; no process matching the path was running at `18:22:49Z`. The `refuseall.err` bytes are an unhandled `FileNotFoundError` from `corpus/evidence/round58/c1-count.py:212` on `…/refuseall/out-empty/spans/S777-1.txt` — i.e. the counter aborts with a traceback instead of emitting a leg when the builder never creates `out-empty/spans`. Observed artifact, not reproduced here | medium — cleanup cannot be asserted; scratch namespaces collided mid-wave, and the round-58 counter has an unhandled failure path | open; the lane should namespace scratch per seat-run and let the round-59 positive-control work treat a builder-less run as a leg, not a crash |

## 5. Touched surfaces and writes

- Written: this file only — `.ufo/waves/round-59/w1/R59Scribe21.md`.
- Scratch: `/fast/scratch/hyaku/chousa-r59/R59Scribe21/` — my one artifact (`form.txt`) was removed at
  `18:19:49Z`; the path was then reused by a foreign writer and is no longer empty. See §9 and F11.
- Not touched: `corpus/evidence/round59/*` (claims, counters, controls), `corpus/lessons/*`, `LOG.md`,
  `SCORECARD.md`, `QUALITY.md`, `SOURCES.md`, `corpus/knowledge/*`, `.ufo/waves/round-59/w1/*` peer files,
  `.ufo/l0-questions.md`, `considerthese/*`, and any sibling or fleet repository.
- `git status --porcelain` at the end of the read window showed only the pre-existing untracked
  `.ufo/waves/round-59/` and `corpus/evidence/round59/`; the only file this seat added under either is
  this report, and it changed no existing byte there.

## 6. Conflicts recorded verbatim

1. **Discernment trend, same round:** `corpus/lessons/round-58-verifier-spotcheck.md` §Trend verdicts says
   “Discernment **improved**: this outside spot-check agrees with both the admit and reject decisions,
   satisfying the LEARNING standard for an agreed outside sample.” `SCORECARD.md` round-58 block says
   “Learning trends: … discernment **unchanged** (no outside non-author sample was available before
   filing).” `corpus/lessons/round-58.md` says “No discernment improvement is claimed; the external
   spot-check duty remains open for closure.” All three describe the same round from different times; the
   round-59 Gate must adopt the closure artifact’s state without rewriting the earlier text (the skill’s
   append-only rule), and should state the ordering explicitly.
2. **Quote unit:** spot-check “19 whitespace-delimited words” vs `s101-open.txt` “19 characters; one
   whitespace-delimited word” (E11). Resolved in favor of the receipt and this seat’s measurement.
3. **C1 receipt cause attribution:** `SCORECARD.md` attributes `REFUSE=0/7` to the token case alone; this
   seat’s static read confirms the token case is sufficient, and adds that the round’s *actual* runs also
   passed the pinned base as the candidate — `corpus/evidence/round58/controls/c1-controls.txt:1` names
   `--builder tools/build-spans.py`, which is the pinned base’s bytes (E4) — so those runs would fail
   `FOREIGN` even with the case fixed. Both statements are true; the lesson should not present the
   base-receipt cause as purely lexical.

## 7. Out of scope / not claimed

- No external fetch, no network call, no capture, no install, no pacman, no fleet/sibling/shokuknow/
  considerthese write, no git/jj/index write, no subagent dispatch.
- No census validation, counter run, builder run or mutation run by this seat; every count attributed to
  a tool is either run here and labelled (§1 producer column) or read from a receipt and labelled as
  such.
- No claim that a round-59 freeze will not appear later. F1/F2 describe the observed window
  (`18:12Z`–`18:21Z`); if a freeze lands afterwards, the defect narrows to “dispatch preceded the freeze”
  with the measured gap, and the Gate’s bracket clause in §2 is the replacement.
- No score, axis grade, trend verdict or capability is asserted by this draft. No lesson, LOG, SCORECARD
  or claims byte is proposed for rewriting.
- No assertion that the round-59 receipt is fabricated. The receipt’s bytes are consistent with a
  deterministic re-run (E4); the defect is the missing header (E5), not the content.

## 8. Artifact paths

- This report: `.ufo/waves/round-59/w1/R59Scribe21.md`
- Round-59 predata observed: `corpus/evidence/round59/census-start.txt`,
  `corpus/evidence/round59/controls/c1-before.txt`, `.ufo/waves/round-59/w1.ready`,
  `.ufo/waves/round-59/w1.ready.partial`, `.ufo/waves/round-59/w1-spec.json`,
  `.ufo/waves/round-59/w1-dispatch.json`
- Round-58 evidence read: `corpus/evidence/round58/{claims.md,c1-count.py,c2-count.py,census-start.txt,census-end.txt,s101-open.txt}`,
  `corpus/evidence/round58/c2/quotes.tsv`, `corpus/evidence/round58/controls/{c1-before.txt,c1-controls.txt,c2-before.txt,build-spans-r55.py}`
- Lessons: `corpus/lessons/round-58.md`, `corpus/lessons/round-58-verifier-spotcheck.md`
- Lane state: `SCORECARD.md` (round-58 block), `LOG.md` (round-58 close), `corpus/QUALITY.md:974`,
  `SHONEN.md`
- Fleet: `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md`, `/home/vgpnk/Projects/shokunin/.ufo/reports/round-58/chousa.md`
- Peer corroboration: `.ufo/waves/round-59/w1/{R59Critic55.md,R59Scribe22.md,R59Scout29.md}`

## 9. Scratch cleanup

`/fast/scratch/hyaku/chousa-r59/R59Scribe21/` held one file from this seat (`form.txt`, 47,356 bytes, the
`capture-text.py` stdout used for E9/E10). It was removed at `18:19:49Z` (`rm -rf` followed by
`ls -d …` → “No such file or directory”). No `/tmp` path was used for evidence.

The path did not stay absent. At `18:22:12Z` it existed again with files this seat did not create:

```
form.txt      47356 B  18:21:34Z
form.err          0 B  18:21:34Z
refuseall/      dir    18:20:56Z   (cache/, out-empty/, quotes.tsv)
refuseall.out     0 B  18:20:56Z
refuseall.err   891 B  18:20:56Z   (unhandled FileNotFoundError from
                                    corpus/evidence/round58/c1-count.py:212 on
                                    …/refuseall/out-empty/spans/S777-1.txt)
```

`ps -eo pid,etime,cmd | grep -F 'R59Scribe21'` returned no matching process at `18:22:49Z`; the newest
mtime was `18:21:34Z`. Because these bytes belong to another writer and one of them records a counter
failure path, this seat did **not** delete them. The cleanup duty is therefore satisfied for this seat’s
own artifact only; the residual directory is a mid-wave scratch collision (F11), not this seat’s evidence.

A second, independent collision was reported to this seat by peer `R59Executor07-2` at `18:23Z`: a C2 poison
probe (`positive-path/poison-base.py`, `positive-path/c2-poison-zh.stdout`) appeared at `15:23` local
(`18:23Z`) inside `/fast/scratch/hyaku/chousa-r59/R59Executor07/`, which that seat does not own; the peer left
it in place and asked whether it was mine — it was not (this seat wrote only under `R59Scribe21/` and the
report). Observed at `18:24:15Z`: that namespace holds `positive-path/` with mtime `15:24`. Peer-reported,
not observed by this seat; together with F11 it indicates a wave-wide scratch-path misdirection, not a single
errant run.

Final freeze-state check at `18:21:03Z`: `corpus/evidence/round59/claims.md` still absent (`test -e` → 1);
`find corpus/evidence/round59 -type f` lists exactly `census-start.txt` and `controls/c1-before.txt`;
`ls .ufo/waves/round-59/w1/*.md | wc -l` → `51`. If the freeze lands after this report, F1 narrows to the
measured dispatch-to-freeze gap and the Gate’s §2 bracket clause is the replacement text.

---

# Second pass — retry instance of the same seat (appended, not a rewrite)

Window `2026-10-27T18:19Z`–`18:27Z`. §0–§9 above were written by the first instance of this seat (last
revision `18:22:00Z`, 303 lines). This section is the retry's own pass: it re-ran what can be re-run,
re-verifies the §1 ledger row by row, and records seven measurements the first instance did not make —
one of which is the mechanism the round-59 milestone actually names ("positive verdict-path calibration").
The residual scratch directory that §9/F11 attributed to "another writer" **was this retry's scratch**; the
891-byte `refuseall.err` cited there is measurement N2. Everything under it is removed at the end (§16).

## 10. Commands this pass ran (exact; observed results)

Environment: `python3 -V` → `Python 3.14.8`. Every write went to
`/fast/scratch/hyaku/chousa-r59/R59Scribe21/` with `TMPDIR` pointed there. No lane path was written.

```
# N1 — execute the frozen counter's own refusal emitter and its aggregate (no full battery)
python3 -B -c '<import c1-count.py by path; call expect_refuse; evaluate 391/390/393>'
  module PASS token = 'pass'
  expect_refuse success string = 'SYMLINK_OUT=pass(refused)'
  all-7-refusals-pass  -> ref_pass = False  ok_pass = True
  aggregate verdict on perfect builder = FAIL
  SUMMARY line = REFUSE=0/7
  denied_pass with no --controls = True

# N2 — full battery on the deny control
PYTHONDONTWRITEBYTECODE=1 TMPDIR=… timeout 420 python3 -B \
  corpus/evidence/round58/c1-count.py \
  --builder corpus/evidence/round58/controls/REFUSEALL.py --work …/refuseall
  EXIT=1 ; stdout 0 bytes ; stderr Traceback → FileNotFoundError at c1-count.py:212
  ('…/out-empty/spans/S777-1.txt') ; post-state work/out-empty/ exists and is EMPTY (no spans/)

# M-content re-check in the defined form (read-only)
python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw   (exit 0, 47,356 B)
  chars 27012 ; 12 quote rows, count==1 each ; offsets
  315,330,590,683,734,781,797,838,965,993,1460,11723 ; max 36 chars ; 3 line-start
  quote at 797 → 19 characters, 1 whitespace-delimited word

# identity / determinism / receipt shape
sha256sum corpus/evidence/round59/controls/c1-before.txt corpus/evidence/round58/controls/c1-before.txt
  → 2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe  (both)
sha256sum tools/build-spans.py corpus/evidence/round58/controls/build-spans-r55.py
  → 1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  (both)
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 133
stat → w1.ready 15:12:15-0300 (154 B) ; round59 c1-before 15:14:30-0300 (958 B) ; delta 0:02:15
diff round58/census-end.txt round59/census-start.txt → r58 carries `Command:` and `EXIT=0`; r59 neither
git -C /home/vgpnk/Projects/shokunin log -1 8d77e6c1 → round-29: chousa L0 question (quote re-open fetch scope)
git -C /home/vgpnk/Projects/shokunin log -1 2c6edbab → round-57: chousa L0 admission ruling question
```

Not run: `scripts/sources-census.sh validate` (the `exit=0` above is **receipt content**), `tools/build-spans.py`
as a builder, any mutation tool, any fetch, any git/jj/index write, any install.

## 11. §1 ledger re-verified

| row | verdict | basis of this pass |
|---|---|---|
| E1 freeze absent | agree | `test -e corpus/evidence/round59/claims.md` → absent again at `18:21Z`; `find corpus/evidence/round59 -type f` → the same two files |
| E2 ready precedes receipt | agree | `stat` mtimes above; gap `0:02:15` |
| E3 receipt identity | agree | sha256 `2c9bbe54…` on both files |
| E4 identity is determinism | agree | builder bytes = r55 control bytes (`1ed2650a…`); the tree holds no patched builder |
| E5 no command header | agree | first line is `EMPTY_OK=pass`; round-58's `c1-controls.txt` does start with `Command: …` |
| E6 `C1=PASS` unreachable | **agree, strengthened** | first instance derived it statically; N1 now *executes* the emitters and the aggregate: a perfect refusal set still yields `ref_pass=False`, `C1=FAIL`, `REFUSE=0/7` |
| E7 dead aggregate line | agree | `c1-count.py:389` is overwritten by `:390`; **add `:399`** — the SUMMARY counts `=PASS` with its own uppercase literal, a third site |
| E8 C2 bind/rebuild exclusive | agree, sharpened | code-level: `tools/build-spans.py:142` `start = max(0, off - CONTEXT)`, `:149` writes `str(start)`; `c2-count.py:101` demands `occurrences[0]==off`, `:105` slices at `off-80`, `:124` byte-compares to the builder's manifest |
| E9 C2 content sound | agree | 12/12 unique at the stated offsets, max 36 chars, 3 line-start (recomputed here) |
| E10 S101 offset 797 | agree | `form.find` → 797, count 1, quote 19 chars |
| E11 unit mislabel | agree | `len(quote)=19`, `len(quote.split())=1` |
| E12 wave shape | agree | roles `executor 16 / reviewer 14 / scribe 12 / scout 12 / critic 7 / mutation-tester 5`; policy `waveMinLanes 64`, `waveMaxLanes 128`; `counts.spawn=66` |
| E13 census start | agree | 133 rows by count; five W04 lines and `exit=0` read from the receipt |
| E14 census receipt drift | agree | `diff` output above |
| E15 criterion 115 landed | agree | `corpus/QUALITY.md` is 974 lines; the criterion text is at `:974` |
| E16 L0 ids are fleet commits | agree | both `git log -1` subjects reproduce **from the fleet root** (they do not resolve inside the lane repo) |
| E17 `CT-20261026-4` positional | agree | the only literal id in `considerthese/2026-10-26.md` is `CT-20261026-1` at `:41`; `:44` is the 4th proposal bullet counting `:41` as 1 |
| E18 peer convergence | **not re-verified here** | peer reports were not re-read by this pass; treat as first-instance evidence |

## 12. New measurements (N1–N7)

- **N1 (ran) — the positive path is unreachable, demonstrated by execution.** Loading the frozen
  `c1-count.py` and calling its own `expect_refuse` returns `'SYMLINK_OUT=pass(refused)'`; feeding seven
  such lines to the `:391` predicate gives `ref_pass=False` while the four safe legs give `ok_pass=True`.
  A builder satisfying all 11 declared legs therefore prints `C1=FAIL` with `REFUSE=0/7`. This is the
  criterion-115 defect, now an observed output rather than a static reading.
- **N2 (ran) — the counter aborts on a refusing builder.** Against `controls/REFUSEALL.py` the run exits 1
  with **0 bytes of stdout** and a traceback at `c1-count.py:212`: `foreign.write_bytes(...)` targets
  `out-empty/spans/S777-1.txt`, but `out.mkdir()` (`:190`) creates only `out-empty/`; `spans/` appears
  only after a successful build. Post-run state confirms `out-empty/` is empty. There is no guard.
- **N3 (derived from N2 + `:371–383`) — the deny leg fails open.** The `--controls` block runs the same
  counter on each control and reads only lines starting with `C1=`; a crash produces an empty tail, which
  falls into `else: denied += 1` and prints `CONTROL_<name>=denied`. Round-58's
  `CONTROL_REFUSEALL=denied` / `DENIED=2/2` is therefore consistent with a **crash**, and that receipt
  cannot distinguish a crash from a measured `C1=FAIL`.
- **N4 (ran/read) — the deny clause is true by construction when no controls are given.** `:393`
  `denied_pass = (denied == total) if total else True`, and `--controls` defaults to `None` (`:168`). The
  round-59 predata receipt prints `DENIED=0/0`, i.e. it took the vacuous branch; round-58's own control
  receipt prints `DENIED=2/2`. Round 59 opens with strictly **fewer** controls than round 58 closed with.
- **N5 (read) — the pinned interpreter is not propagated to the controls.** The control child is invoked
  with `sys.executable` (`:374`) while the measured builder runs under `args.python` (`run_builder`). A run
  pinned with `--python` measures one interpreter and denies on another.
- **N6 (read, consequential) — a one-line repair produces a self-contradictory receipt.** The uppercase
  token appears twice in the aggregates: `:391` (`ref_pass`) and `:399` (the SUMMARY `REFUSE=` count),
  in addition to the `PASS = "pass"` constant at `:51`. Repairing only `:391` makes the verdict print
  `C1=PASS` while the same run's SUMMARY still prints `REFUSE=0/7`. Any repair must change both literals,
  and the positive control must assert **both** lines (and the exit code, `:401`).
- **N7 (read) — the C2 exclusion is total, not marginal.** Because `CONTEXT = 80` and every frozen quote
  offset is > 0 (315 … 11723), a builder-produced manifest offset is always `off-80 ≠ off`, so
  `CAPTURE_BIND` fires for all 12 rows; rewriting the offsets to occurrences makes the manifest bytes
  differ from the builder's output, so `:124` fails. There is no row where both clauses can hold.

## 13. Draft Gate clause — positive verdict-path calibration (liftable)

```markdown
### Positive verdict path (criterion 115) — required before any round-59 claim is adjudicated

- **P+ (must pass).** A builder whose sha256 differs from the pinned base `1ed2650a…` (so
  `BEFORE_FOREIGN=deleted` keeps its meaning), which creates `spans/` on its first safe leg (otherwise the
  counter aborts at `c1-count.py:212`), and which refuses all seven hazard classes with a named reason
  token. On the repaired/re-frozen counter it must print exactly `C1=PASS`, exit 0, and
  `OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=n/n (n≥2)`. The receipt names the counter's sha256.
  `REFUSE=7/7` is required because it is a second literal (`:399`); a `C1=PASS` next to `REFUSE=0/7` is a
  broken receipt, not a pass.
- **F− (must fail, on the same counter).** (a) `REFUSEALL.py` must print a **non-empty** `C1=FAIL` line
  and exit 1 — a crash (empty stdout) must be recorded as `crashed`, never as `denied`; (b) the pinned
  base `1ed2650a…` must still fail `FOREIGN` with the foreign file deleted, proving the token repair did
  not neuter the destructiveness leg; (c) a builder satisfying six of seven refusal legs must print
  `C1=FAIL`, proving per-leg counting rather than a whole-set shortcut.
- **Counter mutant (the falsification of the counter, not of the builder).** A counter that hard-wires
  `C1=PASS` must be rejected by (b) and (c); a counter that leaves `:212` unguarded must be rejected by
  (a). Without this leg, a counter that always prints PASS satisfies P+ trivially.
- **Both tokens.** Assert `C1=<token>` and the exit code (`:401` returns 0 iff the verdict is PASS).
  stdout alone does not bind the exit contract.
```

## 14. Additional Mistakes rows (M7–M9, additive to §3)

7. **vacuous — the deny leg scores a crash as a denial (fail-open control)** · Evidence: ran the frozen
   counter with `--builder …/controls/REFUSEALL.py` → `EXIT=1`, stdout `0` bytes, `FileNotFoundError` at
   `c1-count.py:212` writing `out-empty/spans/S777-1.txt` (the directory is created only by a successful
   build, `:190`); the `--controls` block (`:371–383`) counts only `C1=` lines and appends
   `CONTROL_<name>=denied` on an empty tail; round-58's `DENIED=2/2` therefore contains at least one
   crash-scored denial. · Captured-by: criterion 115's positive-path duty and criterion 86's
   positive-control principle — a control set that cannot distinguish crash from measurement measures
   nothing. · Fix: require the child's `C1=` line **and** exit code; make `crashed` its own class and fail
   the run on any crash. · Flip: the REFUSEALL control prints `C1=FAIL`, exit 1, non-empty stdout.
8. **vacuous — the default control set is empty and its clause is then true by construction** · Evidence:
   `c1-count.py:393` (`(denied == total) if total else True`), `:168` (`--controls` default `None`);
   round-59's only predata receipt prints `DENIED=0/0` while round-58's control receipt prints
   `DENIED=2/2`. · Captured-by: criterion 115 (a deny-only set cannot prove reachability; an empty set
   proves less). · Fix: make `--controls` mandatory for a claim-bearing run and refuse `total == 0` with a
   non-zero exit. · Flip: a claim receipt prints `DENIED=n/n`, n≥2, and an unset/empty control dir exits
   non-zero.
9. **evidence — the round-59 "before" receipt cannot evidence its own refusal legs** · Evidence: it is
   byte-identical to round-58's (`2c9bbe54…` both) and records `REFUSE=0/7` for the *unfixed base builder*,
   where a failing refusal leg is the expected before-state — so a working leg and a dead leg print the
   same thing. The only lines that separate them live in round-58's `c1-controls.txt`
   (`BEFORE_FOREIGN=deleted`, `DENIED=2/2`) and were not carried into round 59. · Captured-by: criterion
   115; criterion 108 (a receipt names its revision). · Fix: carry the control receipt forward and give
   every receipt a `Command:` line plus the counter's sha256. · Flip: a round-59 before receipt that names
   its counter pin, includes the control receipt, and carries one positive-control run whose legs are
   legible.

## 15. Limits of this pass

- No fetch, no network, no install, no pacman, no git/jj/index write, no subagent dispatch, no lane file
  written other than this report (appended).
- `claims.md` is still absent, so no round-59 claim is adjudicated here; §13 is a conditional clause, not
  a verdict.
- Peer reports were not re-read (E18 stands as first-instance evidence).
- The census validator was not run; `exit=0` is quoted from the receipt.
- N2 is a single measurement on `Python 3.14.8`; the traceback site is interpreter-independent (it is a
  missing directory, not a version behaviour), but only this interpreter was exercised.

## 16. Scratch

`/fast/scratch/hyaku/chousa-r59/R59Scribe21/` held `form.txt` (47,356 B), `form.err` (0 B),
`refuseall/` (cache, empty `out-empty/`, `quotes.tsv`), `refuseall.out` (0 B) and `refuseall.err`
(891 B, the N2 traceback). The directory was removed with `rm -rf` before this section was yielded; it is
the same directory §9/F11 recorded as a foreign writer and the writer was this retry. No `/tmp` path was
used for evidence.

## 17. Cross-pass check (first instance, appended)

- **Scratch reconciliation:** §16 identifies the writer into `R59Scribe21/` as this seat's retry, and the
  directory is absent at `18:24:57Z` (`ls` → “No such file or directory”). §9/F11 was accurate at its
  observation time (`18:22:12Z`–`18:24:15Z`); the retry’s own §16 is the resolving record. The
  `R59Executor07-2` collision (`positive-path/` in another seat’s namespace) remains a separate event.
- **Line citations in the second pass, verified against the frozen file (no edits):** `:190` →
  `193–194` (`out = work / "out-empty"`; `out.mkdir()`; `out-empty/spans/` exists only if the builder
  creates it, and `:212` writes into it); `:371–383` (control block) → `365–382` (`if args.controls:` …
  `DENIED=` line); `:401` (exit contract) → `402` (`return 0 if verdict == "PASS" else 1`), while `:401`
  prints `C1=`.
- **Citations confirmed accurate:** `:212` (traceback site), `:393` (`denied_pass` default-true when
  `total == 0`), `:399` (`REFUSE=` summary literal), `:391` (uppercase `=PASS` aggregate).
- The second pass’s N1/N2 measurements are its own; they are not re-run here, and this note changes no
  text above it.
