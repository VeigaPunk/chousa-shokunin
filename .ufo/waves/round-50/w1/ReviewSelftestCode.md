# ReviewSelftestCode — line review of `assimilate-rows --selftest` (round 50 W1)

Reviewed `tools/assimilate-rows.py` at candidate ec52e63: `split_cells` (L146), `observe` (L150),
`fixtures_digest` (L197), `selftest` (L204), `main` (L231). Working tree matches the candidate
(`git diff ec52e63 -- tools/assimilate-rows.py` empty; HEAD 7754172). Frozen interface:
`corpus/evidence/round50/c1-count.py`; frozen claim `corpus/evidence/round50/claims.md:20-32`.
No `lsp` device is mounted in this session → semantic checks were runtime repros + line reads (recorded);
no tools installed (tooling authorization: nothing needed). Scratch `/dev/shm/chousa-r50-ReviewSelftestCode/`
(deleted before filing); fixtures were copies, pinned `c1-fixtures/` untouched (digest re-verified below).

Ground truth:
```
$ python3 corpus/evidence/round50/c1-count.py
BASELINE=PASS rc=0 findings=26 · PERTURB P1-P6 all applied=1 rc=1 -> PASS · PERTURB_PASS=6/6
EXPECTED_BAD=PASS rc=2 · R49_REGRESSION=PASS rc=0 · LEGS=5/5 · C1=PASS · rc=0
$ python3 tools/assimilate-rows.py --selftest
…26 FINDING lines… FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43
SELFTEST=PASS findings=26 expected=26 · rc=0
```
Every finding below leaves this ground truth intact — contract/calibration defects of the harness, not
counter-breaking bugs today.

## Findings by severity

### F1 MEDIUM — comparison is set-based, not multiset; duplicate findings pass
`selftest` L220: `miss, extra = sorted(set(want) - set(got)), sorted(set(got) - set(want))`.
Docstring L41-42: "compares the observed finding lines with the `findings` list" — a list is a multiset;
the implementation collapses duplicates on both sides. A person-authored expected with one duplicated
line exits 0 PASS; worse, a future `observe` regression emitting one finding twice would pass against a
correct expected. The `findings=N expected=M` print exposes the count but does not gate it
(`ok = not miss and not extra`, L229). The frozen BASELINE leg (findings==26==expected) guards only the
pristine expected.json, so the counter cannot catch this class.
Repro (pinned fixtures copied to scratch, `findings[0]` appended a second time to expected.json):
```
$ python3 tools/assimilate-rows.py --selftest --fixtures $D --expected $D/expected.json   # $D = copy
SELFTEST=PASS findings=26 expected=27
rc=0
```
Fix direction: compare `Counter(want) == Counter(got)` (multiset), or reject duplicate lines in
expected.json at parse time — either satisfies the docstring's list semantics.

### F2 LOW — `--selftest` silently ignores normal arguments
`main` L240-241 returns `selftest(...)` before `--staged/--knowledge/--registry/--opened/--out/--entry`
are validated; docstring L39 grammar is `--selftest [--fixtures DIR] [--expected FILE]` only.
A misassembled command runs the lane default and reports success:
```
$ python3 tools/assimilate-rows.py --selftest --staged /nonexistent --opened 9999-99-99 --entry /abs --out $S/BOOM
SELFTEST=PASS findings=26 expected=26
rc=0        # BOOM never created; every normal argument silently dropped
```
Fix direction: exit 2 when `--selftest` is combined with any normal-path argument.

### F3 LOW — `ENTRYCITES` emits a bare trailing space for an id-less entry
`observe` L184: `found.append(f"ENTRYCITES {e} {','.join(ids)}")` — an entry whose substituted text has
no `S\d{3,}` token yields `','.join([]) == ""`, so the finding line ends in a space. The frozen grammar
(`ENTRYCITES entry ids`) defines no empty marker — compare `COLLISIONS ids|-`, which does — so an
expected author must encode an invisible trailing space; a clean-looking expected fails with two DIFF
lines that print identically. Repro: fixture with staged S101 + registry S001 (disjoint) and an entry
`knowledge/corpus/knowledge/c.md` = "No ids here.", expected `["TOOLEXIT 0","COLLISIONS -"]`:
```
$ python3 tools/assimilate-rows.py --selftest --fixtures $D --expected $D/expected.json
'FINDING ENTRYCITES corpus/knowledge/c.md '          # repr: trailing space
'DIFF unexpected ENTRYCITES corpus/knowledge/c.md '
rc=1
```
Not reachable with the pinned fixtures (a.md/b.md both cite ids), so C1 is unaffected; it is a trap for
the next fixture package. Fix direction: emit `ENTRYCITES e -` when ids is empty.

### F4 LOW — `SELFTEST=ERROR` misattributes the missing path; `--fixtures ""` silently selects lane default
`selftest` L206-215 reads the expected file before checking fixtures, so a bogus `--fixtures DIR`
reports the expected path as the problem:
```
$ python3 tools/assimilate-rows.py --selftest --fixtures /dev/shm/chousa-r50-ReviewSelftestCode/afile
SELFTEST=ERROR expected file /dev/shm/chousa-r50-ReviewSelftestCode/afile/expected.json: [Errno 2] …
rc=2        # the fixtures path is the missing thing, not the expected file
```
And L205 tests `if fixtures` (truthiness), so an empty string silently means lane default:
`python3 tools/assimilate-rows.py --selftest --fixtures ""` → `SELFTEST=PASS findings=26 expected=26`,
rc=0, lane fixtures used with no hint.
Exit codes are correct in both cases; diagnostic quality only.

## Verified clean (attack surfaces with no defect found)

- Temp-dir cleanup on every path: L154 `mkdtemp`, L155-192 try/finally `shutil.rmtree(out, ignore_errors=True)`;
  a mkdtemp failure raises before anything exists. PASS/FAIL/ERROR selftests with `TMPDIR` pointed into
  scratch: `pass rc 0 tmp-before [] tmp-after []` · `fail rc 1 tmp-before [] tmp-after []` ·
  `error rc 2 tmp-before [] tmp-after []`.
- Writes outside the temp dir: none. The child's complete write set is under `--out` (direct run listing:
  append.md, collisions, corpus/knowledge/a.md, reg-ids, renumber.tsv, staged-ids, stripped.tsv — exactly
  the documented outputs); `observe`/`selftest`/`fixtures_digest` only read and print; no `__pycache__`
  (child runs as `__main__`).
- Zero-entry fixture: graceful, deterministic — `FINDING TOOLEXIT 0`, `FINDING COLLISIONS -`,
  `SELFTEST=PASS findings=2 expected=2`, rc 0, no leaks; missing `knowledge/` behaves identically (entries=[]).
- Symlink / foreign cwd: `selftest` default (L205) and the child command (L156) both use
  `Path(__file__).resolve()`, so fixtures travel with the real tool. `ln -s <tool> link.py`, run from
  /dev/shm via absolute and via relative path: both print `FIXTURES_SHA256=c5c564…d43`,
  `SELFTEST=PASS findings=26 expected=26`, rc 0 — identical to in-place, no cwd dependence.
- Digest definition: byte-identical algorithm to the frozen counter (relpath + NUL + bytes + NUL over
  sorted files). Imported both modules, compared on the pinned dir:
  `tool.digest(FIX) == count.digest(FIX) == c5c564…d43 → True`; inputs are read-only, so the printed
  digest is stable and BASELINE's re-check is consistent.
- `--fixtures <file>` cannot crash the harness: the L215 staged.md/registry.md guard returns 2 before
  `observe`/`fixtures_digest` touch the path (F4 output).
- `split_cells` (L146-147) on tool-written `append.md` rows has no empty-cell crash path: every written
  row is `"| " + " | ".join(cells) + " |"`, so ESC_SPLIT yields ≥2 parts and `[1:-1]` is non-empty; a
  degenerate row surfaces as `ROWCELLS <lid> <n≠11>` (the intended signal), not a traceback.

## Residual risk / verification gaps

- `observe` L161 `subprocess.run` has no timeout: a hung child would hang `--selftest` forever. No hang path
  found in the tool (FIFO fixtures fail `is_file()` → refused/exit 2) — code-read only [INFERENCE]; the frozen
  counter is immune (its `run()` wraps `timeout=120` → rc 124 fails the leg).
- Entry filenames containing tabs would inject raw tabs into `ROWUSEDBY` finding lines (findings are not
  sanitized, unlike stripped.tsv which replaces tabs); unreachable with sane paths, not demoed.
- `RECHECK_RE`/cadence acceptance was not fuzzed beyond the frozen P4 leg.
- Out of my five functions: `registry_rows` (L139) splits cells with plain `split("|")` while `staged_rows`
  (L113) uses ESC_SPLIT — an escaped `\|` in a registry URL cell would truncate the held-mapping key;
  unexercised by P1-P6 (plain registry URLs); flagged for the tool owner.

VERDICT: attacked the frozen C1 self-test harness line by line with 9 runtime repros — harness operational (C1=PASS 5/5; cleanup/writes/zero-entry/symlink/digest all clean) but the set-based comparison (F1) silently accepts duplicated findings and three low calibration defects (F2-F4) await the L1's verdict; no counter-breaking defect.
