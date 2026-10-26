# R51W2ExecReplayAll — every round-51 counter replayed from committed bytes at the tip

seat: R51W2ExecReplayAll (chousa lane, round 51, wave 2) · date: 2026-10-25
lane `/home/vgpnk/Projects/shokunin/chousa-shokunin` · tip `4436e279b91d8d68fd439c9095695035fbeeab74` (lane HEAD is `72566c8`, which only adds `w2` spec files: `git diff --stat 4436e27..HEAD` = gen-w2-spec.py, w2-dispatch.json, w2-run.err, w2-spec.json) · base `9ec1751a…` · env: Python 3.14.8, git 2.56.0, `TMPDIR` under `/dev/shm/chousa-r51-R51W2ExecReplayAll/tmp`

## Method (read-only; every command below was run)

```
git clone -q /home/vgpnk/Projects/shokunin/chousa-shokunin /dev/shm/chousa-r51-R51W2ExecReplayAll/clone
git -C …/clone checkout -q 4436e279b91d8d68fd439c9095695035fbeeab74   # rev-parse HEAD = 4436e27…, status --porcelain = 0 lines
cd …/clone && env -u ASSIMILATE_CITES python3 <cmd>                    # each of the 12 assigned commands
```
The clone stayed clean after every run (`git -C …/clone status --porcelain | wc -l` → `0`); no counter wrote into it. A second clone at `9ec1751` and `--root`/`--tool` runs gave the before-states; a `cp -a` copy made read-only, a `--depth 2` clone, and a `bwrap` mask of `.qcache` probed the replay preconditions. Two scratch copies (`t2`, `t3`) and one byte-tampered fixtures copy (`pin`) probed non-vacuity.

## Every assigned command at the tip (clone of `4436e27`)

| command (`env -u ASSIMILATE_CITES python3 …`) | output lines that matter | exit |
|---|---|---|
| `corpus/evidence/round51/c1-count.py` | `SELFTEST_DEFAULT=PASS` `LEGACY_ALL=PASS rc=0` `SOURCE_ONLY=PASS default_rc=0 map=['S746','S876'] appended=1 bodyonly=[['corpus/knowledge/e.md','S610']] all_rc=0 all_map=['S610','S746','S876']` `PIPE_IDENTITY=PASS d1=ok d2=ok` `REGISTRY_STRUCTURE=PASS 4/4` `LEGS=5/5` `C1=PASS` | 0 |
| `…/c1-supplement.py` | `SHAPE=PASS 3/3` `MUTATION=PASS 3/3` `CROSS_ENTRY=PASS 3/3` `SOURCE_LINE=PASS 3/3` `UNKNOWN_SRC=PASS 3/3` `CLASH=PASS 3/3` `SUPPLEMENT_LEGS=6/6` `C1_SUPPLEMENT=PASS` | 0 |
| `…/c2-count.py` | `ENTRIES=3/3` `BOUND=6/7 (min 5) REFUSED=1` `BOUND_IDS=S107,S108,S109,S110,S111,S112` `REF_ID_UNBOUND=0` `NEW_GROUND=3/3` `QUOTE_ROWS=61 ON_BOUND=61/61` `SPAN_IDS=6/6` `QUOTES_IN_SPAN/ENTRY/LESSON=61/61` `QUOTE_SHORT=61/61` `SPAN_CONTEXT=61/61` `CAPTURE_BOUND=61/61` `SUBSTANCE=PASS` `ANCHOR_BOUND=6/6` `INFERENCE_GROUNDED=3/3` `QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)` `QUARANTINE_BLOCKED_ADOPTED=0` `C2=PASS` | 0 |
| `…/c2-count.py --lane-only` | identical except `CAPTURE_BOUND=skipped`; `C2=PASS` | 0 |
| `…/c3-count.py` | `CAP_ROWS=36 (base 36)` `POINTERS=74 (base 74)` `RESOLVED_BY_CORRECTION=4` `DANGLING=0` `C3=PASS` | 0 |
| `…/build-spans.py --check` | `SPANS_ROWS=61 STALE=0` | 0 |
| `…/quote-substance-check.py` | `IDS=6 QUOTES=61 FAILURES=0` | 0 |
| `corpus/evidence/round47/c2-count.py` | `ENTRY_POINTS=125 (abc=98 dependence=+7 check_named=+20)` `FLOOR=92` `GATES_ROWS=56` `REGISTERED=125/125` `UNREGISTERED=0` `DANGLING=0` `MISMATCHES=0` `C2=PASS` | 0 |
| `corpus/evidence/round50/stale-count-check.py` | 8× `RESOLVED …:NNNN says 28, receipt 31` `STALE_HITS=8 UNRESOLVED=0 RECEIPT_ROWS=31` `STALE_COUNT=PASS` | 0 |
| `tools/assimilate-rows.py --selftest` | 27 `FINDING …` lines (incl. `BODYONLY`×4, one `BODYCLASH`, `STRIPPED`×5) `FIXTURES_SHA256=3b7ad2583…` `SELFTEST=PASS findings=27 expected=27` | 0 |
| `corpus/evidence/round51/controls/build-c2-controls.py` | STAGED `BOUND=0/7 REF_ID_UNBOUND=30 QUOTE_ROWS=0 SUBSTANCE=FAIL C2=FAIL`; TOOLED `BOUND=7/7 REF_ID_UNBOUND=0 QUOTE_ROWS=0 ANCHOR_BOUND=0/7 C2=FAIL`; both `exit=1` | 0 |
| `corpus/evidence/round51/controls/build-c3-controls.py` | BLANKET `DANGLING=5 C3=FAIL exit=1`; DELETED `CAP_ROWS=32 POINTERS=59 C3=FAIL exit=1`; EMPTY `DANGLING=5 C3=FAIL exit=1`; DOTPATH `CAP_ROWS=37 POINTERS=75 RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS exit=0`; pre-erratum DOTPATH `DANGLING=4 C3=FAIL exit=1` | 0 |

Both control-builder outputs are **byte-identical** to the committed receipts `controls/c2-controls.txt` and `controls/c3-controls-final.txt` (string compare after dropping my wrapper's `EXIT=` lines: `True`, `True`). Extra landed checks replayed: `receipt-check.py` (see F1/F2) and `open-items-age.py` (needs `REPORT --round N`, `EXIT=2` usage without them; no round-51 report exists yet to score). `corpus/evidence/round50/c1-count.py` at the tip tool (`6b975f91…`): `BASELINE=FAIL rc=1 findings=?`, `R49_REGRESSION=FAIL rc=1`, `LEGS=3/5 C1=FAIL` exit 1 — the disclosed one-shot failure; with `--tool` = the round-50 blob (`git show 1d7aba09:tools/assimilate-rows.py`, sha256 `382aca9b…`) it reproduces the receipt exactly: `BASELINE=PASS rc=0 findings=26 … R49_REGRESSION=PASS rc=0 LEGS=5/5 C1=PASS` exit 0. The receipt's own digests check out: `1d7aba09`/`9ec1751` tool = `382aca9b…`, `2a3389d` = `bdaf80f4…`, tip = `6b975f91…`.

## Clone replay vs the lane working tree's own runs

Same 10 commands run in `cd /home/vgpnk/Projects/shokunin/chousa-shokunin` produced 131 output lines with **one** differing line — `SOURCE_ONLY=… map=['S692','S777'] … bodyonly=[['corpus/knowledge/e.md','S819']]` instead of `…['S746','S876'] … 'S610'` — i.e. only the fresh per-run random ids; after masking `S\d{3}` the two logs are identical (`A==B → True`, 0 differing lines). Reason: `c1-count.py` seeds from `os.urandom(8)`. Production bytes are identical to the assigned tip: `git diff --stat 4436e27 -- corpus tools SCORECARD.md SHONEN.md QUALITY.md SKILL.md` → empty (the tree's only changes are seat reports: ` M .ufo/waves/round-51/w1/R51DraftSkillGates.md`, `?? .ufo/waves/round-51/w2.ready`, `?? .ufo/waves/round-51/w2/`). The lane tree was not modified by any run (`git status --porcelain` before and after: the same three report entries).

## Replay preconditions and environment sensitivity (measured, not defects of the predicates)

- **Determinism**: `c1-count.py --seed 7` twice → byte-identical; three unseeded runs → `LEGS=5/5` each; `c1-supplement.py --seed 5` twice → byte-identical; two runs each of `c2-count.py`/`c3-count.py` → byte-identical; `c2`/`c3`/`c1 --seed 7` from `cwd=/` → byte-identical; `PYTHONHASHSEED=0` and `98765`, `LC_ALL=C` → byte-identical.
- **Round-50 receipt reproduces and is derived**: `build-spans.py` re-run without `--check` in a scratch copy regenerates `spans.tsv` byte-identically to `git show 4436e27:corpus/evidence/round51/spans.tsv`.
- **Base object required**: in a `--depth 2` clone checked out at the tip, `c2-count.py` prints `NO_BASE_OR_REGISTER` exit 2 and `c3-count.py` `NO_BASE` exit 2 (`git -C LANE show 9ec1751:` fails); `c1-count.py` still prints `LEGS=5/5 C1=PASS` exit 0. So C1 replays from an export-class clone, C2/C3 do not.
- **Exactly one substrate leg**: with `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` masked by an empty dir (`bwrap --dev-bind / / --bind <empty> <qcache>`), full `c2-count.py` prints `CAPTURE_BOUND=0/61 … C2=FAIL` exit 1 while `--lane-only` prints `CAPTURE_BOUND=skipped … C2=PASS` exit 0. The capture binding is the only cache-dependent leg, as claimed.
- **Ambient env**: `ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-count.py` (no `env -u`) → `SELFTEST_DEFAULT=FAIL`, `SOURCE_ONLY=FAIL`, `LEGS=3/5`, `C1=FAIL` exit 1, because `run()` (`c1-count.py:56-62`) passes no scrubbed env; the same polluted env on `c1-supplement.py` → `C1_SUPPLEMENT=PASS` (`ENV` scrubbed at `c1-supplement.py:46-47`). See F5.
- **No network, no clock**: only `tools/assimilate-rows.py` imports `datetime` (`:96,210`) and it parses `--opened`; none of the counters imports `urllib`, `socket`, `requests`, or reads the wall clock.

## Before-state replays (base tree, tip counters via `--root`)

`c1-count.py --root <base>` → `LEGS=1/5 C1=FAIL` exit 1, nonce line only differing from `controls/c1-lane-before.txt`; `c2-count.py --root <base>` → `ENTRIES=0/3 BOUND=0/7 NEW_GROUND=0/3 SUBSTANCE=FAIL C2=FAIL` exit 1, line-identical to `controls/c2-before.txt`; `c3-count.py --root <base>` → `CAP_ROWS=36 POINTERS=74 RESOLVED_BY_CORRECTION=0 DANGLING=5` (the five named rows/lines) `C3=FAIL` exit 1, identical to `controls/c3-before-erratum.txt`; the **pre-erratum** counter (`git show d603f6f0:…/c3-count.py`) at base → `DANGLING=8` including `ufo/waves/round-34/measure/`, `…-a2/`, `ufo/waves/round-25/build/ConnectorMetaSiblings.md` — erratum E1's 8→5 reproduced exactly.

## Non-vacuity probes (each should redden; each did)

`printf 'x' >> corpus/evidence/round50/c1-fixtures/staged.md` in a copy → `PIN_CHANGED … exit=2`. One byte changed in one quote of `spans.tsv` in a copy → `QUOTES_IN_SPAN=60/61 QUOTES_IN_ENTRY=60/61 QUOTES_IN_LESSON=60/61 … C2=FAIL` (and `SUBSTANCE=PASS`, consistent with its length-floor limit). One `correction:` line deleted in a copy → `RESOLVED_BY_CORRECTION=3 DANGLING SCORECARD.md:1843 measure/final/ DANGLING=1 C3=FAIL`. One byte appended to a span file → `SPANS_FILE_STALE spans/S107-1.txt SPANS_ROWS=61 STALE=1` exit 1.

## Independent re-derivation of the C2 depth facts (not the counter's own code path)

From `spans.tsv` (61 rows, all 7 cells) and the capture cache directly: per-id rows `S107:16 S108:11 S109:13 S110:7 S111:6 S112:8` (min 6 ≥ 3); 0 problems across the four structural legs (capture `.txt` digest = recorded sha256, `text[offset:offset+len(span)] == span`, `text.count(quote) == 1`, quote ≤25 words and ≤160 chars, span longer than quote). `corpus/SOURCES.md` Registry: exactly one row each for `S107`–`S112`, each `mined`, `opened=2026-10-25`, `used-by` exactly the citing entry; none of those ids exists in `9ec1751:corpus/SOURCES.md`. Entry tokens: `r38 {S107,S108}`, `r39 {S109,S110,S111}`, amendment `{S112}` — no unbound token. `refused-doc:` line names `https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx` (staged S125); six register verdicts `S104 absent-as-written · S105 absent-as-written · S111 present · S112 absent-as-written · S114 absent-as-written · S120 present` (none fabricated/unverifiable). At base `git grep` for 検索式 / 検索期間 / 检索策略 over `corpus/knowledge` → rc 1 (absent); the entries hold 6/4/6 occurrences of their own term. Staged→lane map in `c2-count.py DOCS` is the assigned one (S109→S107, S110→S108, S116→S109, S117→S110, S119→S111, S126→S112, S125→refused).

## What breaks (all at the tip `4436e279`)

- **F1 (calibration, worst): a landed lesson line claims evidence that does not exist.** `corpus/lessons/round-51.md:27` reads “Done for this round: `corpus/evidence/round51/measure-after.txt` opens with a `tool-rev:` header and `receipt-check.py` (QUALITY 84) prints `RECEIPT_OK`; the `SKILL.md` rows carry the pin.” At the tip: `git ls-files corpus/evidence/round51 | grep measure` → only `measure-r50-at-tip.txt`; `git grep -n '^tool-rev:'` → **no match in the whole tree**; `receipt-check.py corpus/evidence/round50/measure-after.txt corpus/evidence/round51/measure-r50-at-tip.txt --skill SKILL.md` → `RECEIPT_NO_REV` ×2, `SKILL_NO_PIN SKILL.md`, `CHECKS=3 OK=0 FAILS=3`, `RECEIPT_CHECK=FAIL` exit 1. Either land the pinned receipt this round or the row must not read “Done”.
- **F2: `receipt-check.py` passes vacuously with no receipt.** `python3 corpus/evidence/round51/receipt-check.py` → `CHECKS=0 OK=0 FAILS=0` `RECEIPT_CHECK=PASS` exit 0; cause `ap.add_argument("receipts", nargs="*")` (`receipt-check.py:73`). A caller who drops the argument sees green. Fix (not applied): `nargs="+"`, or exit 2 on zero receipts.
- **F3: `SKILL.md:135` says “five blocks line-identical to `corpus/evidence/round50/measure-after.txt`”, the receipt holds four.** `grep -c '^\$ python3' corpus/evidence/round51/measure-r50-at-tip.txt` → `4` (c1-count, c1-supplement, c2-count, stale-count-check); the fifth block the W1 seat compared (`round50/c2-count.py --lane-only`, `.ufo/waves/round-51/w1/R51ExecRevisionPin.md:100`) is not in the landed receipt. My per-block compare: three blocks byte-identical, stale block identical except one trailing blank line removed (`unified_diff` shows only `-` an empty line), so “zero differing lines” holds for content but the count “five” is wrong for the file.
- **F4: `c1-supplement.py` aborts in a read-only checkout; every other counter passes there.** `chmod -R a-w` copy of the clone, all 10 commands: 9 exit 0 with `C1=PASS`/`C2=PASS`/`C3=PASS`/`STALE=0`/`FAILURES=0`/`STALE_COUNT=PASS`/`SELFTEST=PASS`; `c1-supplement.py` exits 1 with an uncaught `PermissionError` at `c1-supplement.py:77` writing `<TMPDIR>/chousa-r51-sup-*/…/fix/staged.md`, because `shutil.copytree(c1.R50_FIX, m)` (`:119`) carries the 0444 source modes. Suggested fix (draft, inside this report only): `shutil.copytree(c1.R50_FIX, m, copy_function=shutil.copyfile)`.
- **F5: `c1-count.py` inherits ambient `ASSIMILATE_CITES`.** `ASSIMILATE_CITES=all python3 corpus/evidence/round51/c1-count.py` → `SELFTEST_DEFAULT=FAIL … SOURCE_ONLY=FAIL … LEGS=3/5 C1=FAIL` exit 1 while the tool is behaving as designed; the run recipe (`env -u`) is load-bearing and the counter should scrub or print the ambient value (the supplement already scrubs). Disclosed in QUALITY 85, but the frozen counter's own `run()` never does.
- **F6: `c1-count.py --seed 13` never terminates.** Colliding first two id draws leave the loop redrawing only `c_id` (`c1-count.py:123-125`): `timeout 20 … c1-count.py --seed 13` prints `SELFTEST_DEFAULT=PASS`, `LEGACY_ALL=PASS rc=0`, then `EXIT=124` (killed); `c1-supplement.py --seed 13` → `SUPPLEMENT_LEGS=6/6` (its `safe_seed`). Probability 1/401 per unseeded run; disclosed in QUALITY 85, but an unseeded replay can hang with no internal timeout on that loop (the subprocess timeouts do not cover it).
- **F7: C3's coverage hole.** Of the 36 capability rows, three carry no extractable backtick pointer (`SCORECARD.md:465` `— none yet —`, `:601`/`:602` prose cells `selftest cases 95–98`/`93–94`), so a dangling claim written in those cells is invisible; `CAP_ROWS` still counts them, so deleting one is caught while corrupting one is not. The docstring names existence-not-truth but not this.

## What holds

All 12 assigned commands pass at `4436e27` with the claimed key lines, from a clean clone, twice in two independent trees, deterministic under fixed seeds/hash seed/locale/cwd; the committed control receipts (`c1-before`, `c1-supplement-controls`, `c2-controls`, `c3-before-erratum`, `c3-controls-final`) and the before-states reproduce; the erratum 8→5 reproduces; C1's five legs and C2's thirteen legs each redden under a targeted tamper, so none is a rubber stamp; C2's depth facts (61 quotes, per-id ≥6, unique-in-capture, offset-exact, registry binding, refusal, six verdicts, base-term absence) re-derive independently of `c2-count.py`; C3's four correction targets are non-empty at the tip and `.ufo/waves/round-32/measure/final/` holds 9 files; no counter writes into the tree and none touches the network.

VERDICT — attacked the three counters, the two control builders, the supplement and every landed receipt by replaying them from committed bytes at `4436e27` in a clean clone, a read-only clone, a depth-2 clone, a cache-masked namespace and four tampered copies: C1/C2/C3 all pass deterministically and non-vacuously and every receipt reproduces, but the round breaks on calibration, not on counters — F1 (lesson route row 1 cites a `measure-after.txt` with a `tool-rev:` header and a `RECEIPT_OK` that are absent; `RECEIPT_CHECK=FAIL` at the tip), F2 (zero-receipt vacuous PASS), F3 (“five blocks” vs four in the receipt), F4 (supplement crashes in a read-only checkout), F5/F6 (ambient `ASSIMILATE_CITES` flips C1 to 3/5; `--seed 13` hangs).

## Retry seat `R51W2ExecReplayAll-2` — second, independent replay (appended, not overwriting)

The assigned path already held the first seat's complete report (published 21:14:42, before this seat started), so I append a second replay run in my own tree rather than replace it. Method difference: my clone was rebuilt per command, and the before-states were replayed by **checking out `d603f6f` and `cfe6c9f`** and running the counters **as committed there** (not tip counters with `--root`), plus a bare `git archive` export.

```
$ git clone -q …/chousa-shokunin /dev/shm/chousa-r51-R51W2ExecReplayAll/clone
$ git -C …/clone checkout -q 4436e279…; rev-parse HEAD → 4436e279…; status --porcelain → 0 lines
$ git -C …/clone checkout -q 72566c8…   # lane HEAD: only .ufo/waves/round-51/{gen-w2-spec.py,w2-spec.json,w2-dispatch.json,w2-run.err} differ
```

All 12 assigned commands at `4436e27`, `env -u ASSIMILATE_CITES`, cwd = clone root — every exit 0:

| command | lines observed |
|---|---|
| `c1-count.py` | `SELFTEST_DEFAULT=PASS` `LEGACY_ALL=PASS rc=0` `SOURCE_ONLY=PASS default_rc=0 map=['S676','S773'] appended=1 bodyonly=[['corpus/knowledge/e.md','S830']] all_rc=0` `PIPE_IDENTITY=PASS d1=ok d2=ok` `REGISTRY_STRUCTURE=PASS 4/4` `LEGS=5/5` `C1=PASS` |
| `c1-count.py` ×3 unseeded | `LEGS=5/5 C1=PASS` each, three different nonce triples (`S676/S773/S830`, `S806/S807/S530`, `S655/S834/S654`); `--seed 4242` twice byte-identical (`map=['S514','S567']`, bodyonly `S815`) |
| `c1-supplement.py` | `SHAPE/MUTATION/CROSS_ENTRY/SOURCE_LINE/UNKNOWN_SRC/CLASH` all `3/3`, `SUPPLEMENT_LEGS=6/6`, `C1_SUPPLEMENT=PASS` |
| `c2-count.py` | `ENTRIES=3/3` `BOUND=6/7 REFUSED=1` `BOUND_IDS=S107,…,S112` `REF_ID_UNBOUND=0` `NEW_GROUND=3/3` `QUOTE_ROWS=61 ON_BOUND=61/61` `SPAN_IDS=6/6` `QUOTES_IN_*` `61/61`×3 `QUOTE_SHORT=61/61` `SPAN_CONTEXT=61/61` `CAPTURE_BOUND=61/61` `SUBSTANCE=PASS` `ANCHOR_BOUND=6/6` `INFERENCE_GROUNDED=3/3` `QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)` `C2=PASS` |
| `c2-count.py --lane-only` | same except `CAPTURE_BOUND=skipped`; `C2=PASS` |
| `c3-count.py` | `CAP_ROWS=36 (base 36)` `POINTERS=74 (base 74)` `RESOLVED_BY_CORRECTION=4` `DANGLING=0` `C3=PASS` |
| `build-spans.py --check` | `SPANS_ROWS=61 STALE=0` |
| `quote-substance-check.py` | `IDS=6 QUOTES=61 FAILURES=0` |
| `round47/c2-count.py` | `ENTRY_POINTS=125 (abc=98 dependence=+7 check_named=+20)` `FLOOR=92` `GATES_ROWS=56` `REGISTERED=125/125` `UNREGISTERED=0` `DANGLING=0` `MISMATCHES=0` `C2=PASS` |
| `round50/stale-count-check.py` | 8× `RESOLVED …says 28, receipt 31`; `STALE_HITS=8 UNRESOLVED=0 RECEIPT_ROWS=31` `STALE_COUNT=PASS` |
| `assimilate-rows.py --selftest` | `SELFTEST=PASS findings=27 expected=27`, `FIXTURES_SHA256=3b7ad258…` |
| `build-c2-controls.py` | STAGED `BOUND=0/7 REF_ID_UNBOUND=30 SUBSTANCE=FAIL`; TOOLED `BOUND=7/7 SPAN_IDS=0/7 INFERENCE_GROUNDED=0/3 SUBSTANCE=FAIL`; both `exit=1`, both `C2=FAIL`. stdout **byte-identical** to `controls/c2-controls.txt` (`diff` empty) |
| `build-c3-controls.py` | BLANKET `DANGLING=5 FAIL`; DELETED `CAP_ROWS=32 POINTERS=59 FAIL`; EMPTY `DANGLING=5 FAIL`; DOTPATH `DANGLING=0 PASS exit=0`; DOTPATH@pre-erratum `DANGLING=4 FAIL`. stdout **byte-identical** to `controls/c3-controls-final.txt`; equal to `c3-controls-erratum.txt` + the two DOTPATH blocks |

### Before-state exactness (checkout method)

- At `d603f6f`: `c2-count.py` stdout = `controls/c2-before.txt` **byte-exact** (receipt minus its appended `exit=1`); `c3-count.py` stdout = `controls/c3-before.txt` **byte-exact** (`DANGLING=8`, incl. the three leading-dot false positives); `c1-count.py` `LEGS=1/5 C1=FAIL` rc1 matching `c1-lane-before.txt` leg-for-leg modulo nonces — but the receipts (and `c1-before.txt`) omit the four `REGISTRY <case> rc=…` detail lines the frozen counter prints, i.e. they are trimmed transcripts, not raw stdout.
- At `cfe6c9f`: `c3-count.py` stdout = `controls/c3-before-erratum.txt` **byte-exact** (`DANGLING=5`).
- `c1-count.py --tool <controls/*.py>` at `d603f6f`: tool-before `1/5`, echo-tool `2/5`, const-tool `1/5`, flag-noop-tool `2/5` — matches `c1-before.txt`; the supplement matrix reproduces (`forge-dirname` 1/6, `tool-candidate1` 3/6, real tool 6/6; the receipt's “real tool” block is trimmed to its last three lines).
- Receipt-fidelity nit: `controls/c3-controls.txt` is the pre-erratum receipt and does **not** reproduce from the shipped builder; `c3-controls-final.txt` does. `claims.md`'s C3 Before/Controls bullets still print `DANGLING=8`, `CAP_ROWS=30`, `POINTERS=50`; erratum E1 supersedes them (`5`, `32`, `59`) but a reader of `claims.md` alone is misled.

### Independent re-derivation (not the counter's code path)

61/61 manifest rows: capture `.txt` digest = recorded sha; `form[off:off+len(span)] == span`; quote unique in form; `≤25` words/`≤160` chars; span longer than quote; quote present in span, entry and lesson — 0 failures. **`offset` is the SPAN's start**, quote offset = `offset + span.find(quote)`; S111's `.txt` is CRLF (390 CRLF), so the form is `read_text`'s newline-translated text (decoding raw bytes shifts every offset — an initial false alarm of mine, recorded so nobody repeats it). Anchors: every `char N` of the six bound rows lies in the manifest quote offsets (S107 8, S108 6, S109 7, S110 3, S111 5, S112 7). `git grep -l -e 検索式 -e 検索期間 -e 检索策略 9ec1751 -- corpus/knowledge` → rc 1. Entry S-tokens = `{S107,S108}` `{S109,S110,S111}` `{S112}`; `refused-doc:` names the NIPH `.docx`.

### Preconditions and teeth

- Bare `git archive 4436e27` export (14840 files, no `.git`): `c1` 5/5, spans 0, substance 0 failures, selftest PASS; `c2` `NO_BASE_OR_REGISTER` rc2; `c3` `NO_BASE` rc2 — so a clone, not an export, is the replay unit for C2/C3.
- `ASSIMILATE_CITES=all` (no `env -u`): `SELFTEST_DEFAULT=FAIL` + `SOURCE_ONLY=FAIL` → `LEGS=3/5` rc1; `=body` → `LEGS=1/5` rc1 (`c1-count.py:60` passes no scrubbed env).
- Pin tamper (1 byte into `round50/c1-fixtures/staged.md`): `PIN_CHANGED` rc2; restored rc0. Span tamper (1 char in a quote): `SPANS_ROW_STALE spans/S107-1.txt` `STALE=1` rc1; restored `STALE=0`.
- `--seed 13` under `timeout 20`: prints `SELFTEST_DEFAULT=PASS`, `LEGACY_ALL=PASS rc=0`, then rc124 — the first seat's F6 reproduces; `c1-supplement.py --seed 13` → `6/6`.
- Clone vs lane tree: `c2`/`c3` stdout **byte-identical** (`diff` empty); `c1` differs only in the random triple. No counter references `.ufo/waves/round-51/w*` (only the C3 DOTPATH control names committed `gen-w1-spec.py`).

### F1–F3 confirmed from this tree

`ls corpus/evidence/round51 | grep -c measure-after` → `0`; `git grep -l '^tool-rev:'` → rc1; `receipt-check.py <round50/measure-after.txt> <measure-r50-at-tip.txt> --skill SKILL.md` → `RECEIPT_NO_REV`×2, `SKILL_NO_PIN`, `CHECKS=3 OK=0 FAILS=3`, `RECEIPT_CHECK=FAIL` rc1. Zero-arg `receipt-check.py` → `CHECKS=0 OK=0 FAILS=0` `RECEIPT_CHECK=PASS` rc0. `grep -c '^\$ python3' measure-r50-at-tip.txt` → `4`.

VERDICT — attacked the twelve assigned commands, both control builders and the landed receipts with a second, independently built clone, checkout-based before-state replays, a bare export and two tampered copies: every counter and receipt reproduces (builders byte-identical; before receipts byte-exact), the only lane-vs-clone difference is C1's random nonce, and the failures are the ones already named above (F1–F6), with one added documentation nit (claims.md's C3 numbers are pre-erratum; `c3-controls.txt` is not reproducible from the shipped builder).
