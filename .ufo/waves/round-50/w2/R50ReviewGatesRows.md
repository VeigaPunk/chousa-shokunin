# R50ReviewGatesRows — review of SKILL.md `## Gates` r50 changes

Scope: the replaced `assimilate-rows` row and the new `chousa round-50 counters and checks` row in
`SKILL.md`, diffed `git -C . diff 3c51da77b3696ed884c943548ec4b4006e3ca528
74794db07e1b383d5c3e96ad5122fd158a541271 -- SKILL.md` (working tree identical to 74794db).

## Diff scope — PASS

The diff is exactly the two rows and nothing else: `-|` the old `assimilate-rows` row,
`+|` the rewritten `assimilate-rows` row and `+|` the new `chousa round-50 counters and checks` row
inserted after the round-49 row (SKILL.md:130-132). No other line touched.

## Commands exist and run — PASS (all 11 row commands + the required counter)

| command | observed |
|---|---|
| `python3 tools/assimilate-rows.py --selftest` | `FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43`, `SELFTEST=PASS findings=26 expected=26`, rc=0 — matches the row's pinned digest |
| `python3 corpus/evidence/round50/c1-count.py` | `SELFTEST_DEFAULT=PASS`, `BASELINE=PASS rc=0 findings=26`, `PERTURB_PASS=6/6`, `EXPECTED_BAD=PASS rc=2`, `R49_REGRESSION=PASS`, `LEGS=5/5`, `C1=PASS`, rc=0 |
| `python3 corpus/evidence/round50/c2-count.py` | `ENTRIES=3/3`, `BOUND=3/4 REFUSED=1`, `BOUND_IDS=S104,S105,S106`, `REF_ID_UNBOUND=0`, `NEW_GROUND=3/3`, `QUOTE_ROWS=55 ON_BOUND=55/55`, `SPAN_IDS=3/3`, all quote legs `55/55`, `SUBSTANCE=PASS`, `ANCHOR_BOUND=3/3`, `INFERENCE_GROUNDED=3/3`, `QUARANTINE_BLOCKED_ADOPTED=0`, `C2=PASS`, rc=0 — every number the row names reproduced |
| `c2-count.py --lane-only` | `CAPTURE_BOUND=skipped`, `C2=PASS`, rc=0 |
| `build-spans.py --check` | `SPANS_ROWS=55 STALE=0`, rc=0 |
| `build-spans.py --root <scratch>` (write mode, scratch copy of `quotes.tsv`) | `QUOTE <id> char <N>` per row then `SPANS_ROWS=55 WRITTEN=55`, rc=0; rebuilt `spans.tsv`+`spans/` byte-identical to committed (`--check` on the rebuild: `STALE=0`) — substantiates "derived by build-spans, never hand-written" and the anchor semantics `char N = offset + quote position in span` (build-spans.py:118-139, 199-201) |
| `quote-substance-check.py` | `IDS=3 QUOTES=55 FAILURES=0`, rc=0; against `quotes.tsv` (wrong shape) prints `MALFORMED` and rc=1 |
| `stale-count-check.py` | `STALE_HITS=8 UNRESOLVED=2 RECEIPT_ROWS=31`, `STALE_COUNT=FAIL`, rc=1 — see finding 3 |
| `wave-complete-check.py w1-spec.json w1-dir` | `MISSING` per absent report, `OK 29/42`, rc=1; `w2`: `OK 4/43`, rc=1; `--rev` code path resolves `rev-parse`, `ls-tree` (wave-complete-check.py:59-76) |
| `name-collision-check.py w1-spec.json` | `NAME_COLLISIONS=13 ITEMS=42`, rc=1 (the 13 misdirected seat names, matching `name-collision-before.txt`); `w2-spec.json`: `NAME_COLLISIONS=0`, rc=0 |
| `cited-id-check.py <renumber> <entries>` | rc=1 with `BODY_CROSSREF` per row when entry `source:` lines name the lane id (code: exit 0 PASS / 1 BODY_CROSSREF / 2 no rows, cited-id-check.py:14-33) |
| `decode-form-check.py corpus/lessons/round-50.md` | `FORM_NAMED`, `DECODE_FORM=PASS`, rc=0; on `corpus/lessons/round-47.md` → `FORM_MISSING`, `DECODE_FORM=FAIL`, rc=1 (confirms the row's evidence pointer) |
| `cjk-ground-check.py` | cases A/B/C all PASS, `CJK_GROUND=PASS`, rc=0; `--old <pre-2573dc1 tool>` prints `OLD_TOOL case A rc=1 INF_UNGROUNDED` — the row's evidence claim reproduced live |
| `controls/build-c2-controls.py` | ran (ignores args, takes none): STAGED control `BOUND=0/4`, `REF_ID_UNBOUND=15`, `C2=FAIL`, exit=1; TOOLED `BOUND=4/4`, `REF_ID_UNBOUND=3`, `QUOTE_ROWS=55 ON_BOUND=0/55`, `C2=FAIL`, exit=1. Note the row quotes `BOUND=3/4`, `REF_ID_UNBOUND=8`, `QUOTE_ROWS=0` for TOOLED — that matches `controls/c2-before.txt` (the old receipt run against the staged package before four rows were adopted); the script's CURRENT output differs since the staged package's registry/entries moved on. The receipt file exists and matches the row text; the script still fails every control (the contract "Both must print C2=FAIL" holds). See finding 4. |
| `python3 corpus/evidence/round47/c2-count.py --list` (assigned) | `ENTRY_POINTS=114 (abc=93 dependence=+5 check_named=+16)`, `FLOOR=92`, `GATES_ROWS=55`, `REGISTERED=114/114`, `UNREGISTERED=0`, `DANGLING=0`, `MISMATCHES=0`, `C2=PASS`, rc=0 — the required print matches exactly |

## Exit contracts vs code — PASS except findings

- `assimilate-rows.py`: adopter 0 (`COLLISIONS=`/`CITED= APPEND= HELD=`), 1 (missing/not-UTF-8 entry; staged row ≠11 cells or no URL; recheck without leading valid date/`NNd`/cadence — REFUSED exits 1, assimilate-rows.py:290-308,348-353), 2 (missing file, non-UTF-8 staged/registry, invalid `--opened`, absolute/`..` entry — :262-277). Selftest 0 PASS, 1 `DIFF missing/unexpected` (`SELFTEST=FAIL`), 2 `SELFTEST=ERROR` (missing fixtures/unparseable expected — :213-241). `tempfile.mkdtemp` for `--out` confirmed :160. `--selftest` rejects other options with rc=2 (:253-256).
- `c1-count.py`: `PIN_CHANGED`→2 (:83-85); each leg verified live above; `LEGS=n/5`, `C1=PASS` only at 5/5, else rc=1 (:146-150).
- `c2-count.py`: `NO_BASE_OR_REGISTER`→2 (:142-143); every leg named in the row exists in the printed legs.
- `build-spans.py`: refuse→1 (:140-143), stale→1 (:173), env/usage→2 (:71-97,186); `--check` writes nothing (:189-190).
- `stale-count-check.py`: unresolved→1, missing receipt/prose→2, resolved-by-`correction:`-naming-line logic at :35-49 — verified live.
- `wave-complete-check.py`: MISSING→1, unusable spec/lane→2 (:13,:26-35,:57,:66).
- `name-collision-check.py`: collision→1 (:48), unusable spec→2 (:30,:36).
- `decode-form-check.py`: any FORM_MISSING→1, usage→2 (:17,:30).
- `cjk-ground-check.py`: any case misbehaves→1 (:55). (Docstring's own `2 usage` is supplied by argparse.)
- `controls/c1-before.txt` reproduced by re-running `c1-count --tool` on `tool-before.py` (`LEGS=2/5 C1=FAIL`), `echo-tool.py` (`LEGS=4/5`), `const-tool.py` (`LEGS=2/5`) — all `C1=FAIL` as the row claims.
- Contract pins verified: `claims.md` base `3c51da77`, freeze `6a068f2` exists; `c2-count.py` `BASE_REV=3c51da77`; `git diff 6a068f2a 74794db -- c1-count.py c2-count.py claims.md controls c1-fixtures` empty (erratum's "unchanged since the freeze" holds); `c1-fixtures` digest = pin `c5c56480…`; candidate `ec52e63` exists; `corpus/fixtures/assimilate-selftest/` exists as the selftest default (:214).

## Findings

1. **Low — `decode-form-check.py` crashes on a missing file.** Its docstring says `2 on usage`, but
   `python3 corpus/evidence/round50/decode-form-check.py /nonexistent.md` raises an uncaught
   `FileNotFoundError` (line 21 `pathlib.Path(p).read_text`) — traceback, exit 1, no `DECODE_FORM`
   line. The row text itself does not claim an exit-2 for decode-form (the row omits `2` for
   decode-form, wave-complete, stale-count, cjk-ground), so the row is not wrong; the script's own
   docstring is. Fix (either side):
   ```python
   # decode-form-check.py:21 — route unreadable input to the usage exit
   try:
       t = pathlib.Path(p).read_text(encoding="utf-8", errors="replace")
   except OSError as exc:
       print(f"usage: unreadable {p}: {exc}", file=sys.stderr); sys.exit(2)
   ```
   or drop `2 on usage` from the docstring (the no-args path already exits 2 via the usage print).

2. **Low — row omits the `2` exit for four checks whose code implements it.** The row's contract
   clause lists `0`/`1` for wave-complete, stale-count, decode-form, cjk-ground but not `2`, while
   every script exits 2 on unusable input (`wave-complete-check.py /nonexistent.json` → `ERROR …`
   rc=2; `stale-count-check.py --root /nonexistent` → `RECEIPT_MISSING` rc=2; `decode-form-check.py`
   no args → usage rc=2; `cjk-ground-check.py` via argparse). Sibling clauses in the same row DO list
   `2` (build-spans, quote-substance, cited-id, name-collision), so the omission is an accuracy gap
   in an otherwise honest row. Fix: append to SKILL.md:132's contract cell —
   ```
   … `MISSING` per item without one · `2` unusable spec/lane. … (`STALE` …) · `2` missing receipt/prose.
   … `1` a lesson with offsets and no named form · `2` usage. … `1` a case misbehaves · `2` usage.
   ```

3. **Advisory — `stale-count-check.py` currently prints `STALE_COUNT=FAIL` rc=1 on the live lane**
   (not a row inaccuracy; the check works as specified). Two unresolved hits:
   - `LOG.md:1803` says `28 located quotes` (round-49 receipt 31) and NO correction line names it —
     a genuine uncorrected stale count. Fix: append a LOG.md correction naming `LOG.md:1803` that
     quotes only the superseded value (`correction: LOG.md:1803 superseded by round-50 adoption;
     per the rule it may quote 28 but must not add a new number-shaped phrase — write the resolution
     without digits, e.g. "…superseded by the 31-row round-49 receipt" would itself trip the
     `(\d+)-row` pattern; phrase as "superseded by the round-49 span receipt (31 data rows)" is fine
     — `31 data rows` matches no counted pattern). Verify: `stale-count-check.py` then prints
     `RESOLVED LOG.md:1803`.
   - `corpus/README.md:1080` `55-row manifest` — CORRECT prose (round-50 spans.tsv really has 55
     rows) but the check scores every `N-row manifest` count against the round-49 receipt (31), so
     it is a false positive by design limitation (stale-count-check.py:4-6,19: patterns and receipt
     are single-scoped to round-49). Fix: reword README.md:1080 cell — replace `span builder and
     55-row manifest` with `span builder and the round-50 span manifest` (no counted pattern), or
     extend the check's receipt scoping (touches the landed check — prefer the prose fix).

4. **Advisory — `controls/c2-before.txt` documents the controls as scored pre-landing; re-running
   `build-c2-controls.py` now prints different numbers** (`REF_ID_UNBOUND=3` not 8, `BOUND=4/4` not
   3/4, `QUOTE_ROWS=55` not 0) because the staged package and lane registry have since adopted the
   rows. The row cites the receipt file (which exists and matches the quoted values), and both
   controls still end `C2=FAIL` exit 1, so the gate decision stands; the numbers in the row are the
   receipt's, not re-derivable today. No fix needed; noted so a later seat does not mistake the drift
   for a defect.

## Residual risk

- `wave-complete`'s `--rev` path checks ONLY the git tree at REV (not disk); row's "on disk or at
  `REV`" is accurate (either mode, not both).
- `decode-form`'s `FORM` regex is permissive (`.txt.{0,40}UTF-8` etc.) — a lesson that names the
  form anywhere passes, once per file; the check's own docstring discloses "one naming per file,
  not one per offset". Accepted limit.
- `QUARANTINE_VERDICTS=0/0` vacuously satisfies "a verdict for every register id" (no quarantined
  ids this round); leg is honest since it prints `0/0` rather than hiding.

VERDICT: attacked the two SKILL.md Gates rows (commands, exit contracts, evidence pointers, diff scope, r47 `REGISTERED=114/114`) — survived; two minor defects found (decode-form crash-on-missing-file contradicting its own `2 on usage`; row omits the `2` exit of four checks), plus two advisories (live `STALE_COUNT=FAIL` on LOG.md:1803/README.md:1080; c2-controls receipt vs re-run drift).
