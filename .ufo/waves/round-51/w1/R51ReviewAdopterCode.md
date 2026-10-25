# R51ReviewAdopterCode — line review of `tools/assimilate-rows.py` (round 51 W1)

Reviewed `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff d603f6f00f78d64f123d3aed2dd9f8701547a4ba 2a3389da0306e41f1b4797c1bc69017f23a38aef -- tools/assimilate-rows.py` (102+/19- across L1-463) against its docstring (L1-83) and frozen predicate R51-C1 (`corpus/evidence/round51/claims.md:23-61`, `c1-count.py:4-31`). No `lsp` device is mounted (`No such tool: xd://lsp`), so caller/definition checks were runtime repros and line reads; no tools installed. Scratch `/dev/shm/chousa-r51-R51ReviewAdopterCode/` removed after repros (`SCRATCH_REMOVED=ok`).

Baseline ground truth (`T=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/assimilate-rows.py`, `S=/dev/shm/chousa-r51-R51ReviewAdopterCode`):
```
$ python3 corpus/evidence/round51/c1-count.py --seed 51
SELFTEST_DEFAULT=PASS · LEGACY_ALL=PASS rc=0 · SOURCE_ONLY=PASS default_rc=0 map=['S757', 'S782'] appended=1 bodyonly=[['corpus/knowledge/e.md', 'S582']] all_rc=0 all_map=['S582', 'S757', 'S782'] · PIPE_IDENTITY=PASS d1=ok d2=ok · REGISTRY_STRUCTURE=PASS 4/4 · LEGS=5/5 · C1=PASS
$ python3 $T --selftest
…25 FINDING lines… FIXTURES_SHA256=d778c7f58036f76a2557824657a3ff5c1f2f490ea9350a6e40e43d218ed8c8a1 · SELFTEST=PASS findings=25 expected=25
```

## Findings by severity

### F1 HIGH — Cross-entry bleed in `--cites source`: an id cited on Entry A's `source:` line and mentioned only in Entry B's body is renumbered in Entry B, omitted from `bodyonly.tsv`, and absent from `used-by`
`main` L367 computes `cited` globally across all entries (`{t for tx in texts.values() for t in source_ids(tx) if t in staged}`), L436 applies the global `subst(tx)` (L399-402) to every entry, L417-418 computes `used-by` per entry via `twins & set(source_ids(tx))`, and L439-440 computes `body` by subtracting the global `set(cited)` (`set(TOKEN_RE.findall(tx)) - set(cited)`) instead of the entry's own `set(source_ids(tx))`. When `a.md` cites `S010` on `source:` and `b.md` mentions `S010` only in its body (`c4b`): (1) `S010` is rewritten to `S003` inside `out/corpus/knowledge/b.md` (violating `claims.md:26-29`: *"an id an entry mentions only in its body is neither renumbered nor appended, is left in the entry text unchanged and is listed in `bodyonly.tsv`"*), (2) `(b.md, S010)` is omitted from `bodyonly.tsv` (`BODYONLY=0`), and (3) `S003`'s `used-by` in `append.md` lists only `corpus/knowledge/a.md`, leaving `b.md` citing `S003` in its body without a `source:` line or `used-by` entry.
```
$ python3 $T --staged $S/c4b/staged.md --knowledge $S/c4b/knowledge --registry $S/c4b/registry.md --opened 2026-10-25 --out $S/c4b/out --entry corpus/knowledge/a.md --entry corpus/knowledge/b.md
COLLISIONS=0 / CITED=2 APPEND=2 HELD=0 / BODYONLY=0
# append.md S003 used-by: corpus/knowledge/a.md | bodyonly.tsv: header only
# out/corpus/knowledge/b.md body: "- cites S004, and mentions S003 only in its body."
```

### F2 MEDIUM — `ASSIMILATE_CITES=all` fails the frozen round-50 counter when invoked with no flags, contradicting docstring L66-68
Docstring L66-68 claims `ASSIMILATE_CITES=source|all` sets the default of both modes because *"the frozen round-49 and round-50 counters call the tool with no flag and need `all`"*. While `ASSIMILATE_CITES=all python3 corpus/evidence/round49/c1-count.py` passes (`SETS_PASS=3/3 C1=PASS`), `round50/c1-count.py` runs both `--selftest` (no `--fixtures`, using `corpus/fixtures/assimilate-selftest/` which commit `2a3389d` rewrote to expect `source` mode) and `--selftest --fixtures .../round50/c1-fixtures` (expecting `all` mode). Because L315 applies `ASSIMILATE_CITES` even when `a.fixtures is None`, `round50/c1-count.py` (no `--tool` flag) fails under both settings:
```
$ python3 corpus/evidence/round50/c1-count.py
SELFTEST_DEFAULT=PASS · BASELINE=FAIL rc=1 findings=? · PERTURB_PASS=6/6 · EXPECTED_BAD=PASS rc=2 · R49_REGRESSION=FAIL rc=1 · LEGS=3/5 · C1=FAIL (rc=1)
$ ASSIMILATE_CITES=all python3 corpus/evidence/round50/c1-count.py
SELFTEST_DEFAULT=FAIL · BASELINE=PASS rc=0 findings=26 · PERTURB_PASS=6/6 · EXPECTED_BAD=PASS rc=2 · R49_REGRESSION=PASS rc=0 · LEGS=4/5 · C1=FAIL (rc=1)
```

### F3 MEDIUM — `source_ids` (L159-165) scans all tokens on any line starting with `source:` across the whole file, breaking QUALITY 77 on tail tokens, citing mid-body `source:` lines, classifying `Source:` as `BODYONLY`, and duplicating same-line repeats
1. **Tail tokens on `source:` line break `cited-id-check.py` (QUALITY 77)**: L164 runs `TOKEN_RE.findall(line)` across the entire `source:` line instead of matching the id after `source:`. If the anchor/note tail mentions another staged id (`source: S010 — https://example.test/new-a — section 1 (supersedes S011)`), `assimilate-rows.py` cites and appends `S011->S003`, which then fails `cited-id-check.py` (L29 `^source: {staged}\b`):
```
$ python3 $T --staged $S/q77_tail/staged.md --knowledge $S/q77_tail/knowledge --registry $S/q77_tail/registry.md --opened 2026-10-25 --out $S/q77_tail/out --entry corpus/knowledge/a.md && python3 corpus/evidence/round50/cited-id-check.py $S/q77_tail/out/renumber.tsv $S/q77_tail/knowledge/corpus/knowledge/a.md
COLLISIONS=0 / CITED=2 APPEND=2 HELD=0 / BODYONLY=0
BODY_CROSSREF S011->S003 / CITED_IDS=FAIL rows=2 (rc=1)
```
2. **Mid-body `source:` line (`c2_mid_body_source`)**: L162-163 iterates `text.splitlines()` over the whole file without stopping after the provenance header or skipping fenced blocks. A body line under `#### Observation` starting with `source: S011 is mentioned here...` is cited (`CITED=2 APPEND=2 BODYONLY=0`), renumbered to `S004`, and appended to `append.md`.
3. **Capitalised `Source:` (`c3_capital_source`)**: `line.startswith("source:")` is case-sensitive. An entry starting with `Source: S010 — https://example.test/new-a — sec` yields `CITED=0 APPEND=0 HELD=0 BODYONLY=1`, leaves `S010` unrenumbered, and lists `corpus/knowledge/a.md\tS010` in `bodyonly.tsv`.
4. **Same-line duplicate bug (L164)**: `[i for i in TOKEN_RE.findall(line) if i not in out]` checks `out` before extending it, so `source_ids("source: S010 — https://example.test/S010 — sec S010\n")` returns `['S010', 'S010', 'S010']`, violating L160 (`"in order of first mention"`).

### F4 MEDIUM — Non-staged ids on `source:` lines (or in bodies) are silently ignored by `cited`, `bodyonly.tsv`, and `bodyclash.tsv` (`c1_non_staged_source_id`)
Both `cited` (L367 `if t in staged`) and `body` (L440 `if i in staged`) drop any `S\d{3,}` token absent from `staged`. If an entry has `source: S999` (missing from `staged.md`), `source: S001` (existing lane id), or `source: S003` (absent from `staged.md`, but minted in the same run via `S010->S003`), the tool exits 0 with `CITED=1 APPEND=1 BODYONLY=0`, writes no `bodyclash.tsv` and no `WARN`, and produces duplicate `source: S003` lines for different URLs:
```
$ python3 $T --staged $S/c1/staged.md --knowledge $S/c1/knowledge --registry $S/c1/registry.md --opened 2026-10-25 --out $S/c1/out --entry corpus/knowledge/a.md
COLLISIONS=0 / CITED=1 APPEND=1 HELD=0 / BODYONLY=0   # out/a.md has two `source: S003` lines; no WARN or bodyclash.tsv
```

### F5 LOW — Two entries citing different staged ids for one new URL (`c5_two_entries_diff_ids_one_url`) misclassify the second id as `held` and skip `recheck` refusal on all `held` rows
When `a.md` cites `S010` (`https://example.test/same`, `recheck=90d`) and `b.md` cites `S011` (same URL, `recheck=INVALID_RECHECK`):
1. L392-393 maps `S011` via `elif u in by_url:` to `(S003, "held")`, writing `S011\tS003\theld` in `renumber.tsv` and `HELD=1` on stdout — contradicting docstring L20-22 (`held` = URL *"a Registry row already carries"*).
2. Because L408 (`if action != "append": continue`) precedes `recheck` validation (L420-424), `S011`'s `INVALID_RECHECK` (and any Registry-held row's invalid `recheck`) is never refused (`rc=0`), violating docstring L50-51.
3. `stripped.tsv` logs `S003\tused-by\tcorpus/knowledge/a.md` from `S010` while silently discarding `S011`'s cells (`used-by` becomes `corpus/knowledge/a.md, corpus/knowledge/b.md`).
(By contrast, the **same id on two `source:` lines of two entries**, `c4a`, works cleanly: `CITED=1 APPEND=1 HELD=0`, `S010->S003 append`, `used-by` = `corpus/knowledge/a.md, corpus/knowledge/b.md`.)
```
$ python3 $T --staged $S/c5/staged.md --knowledge $S/c5/knowledge --registry $S/c5/registry.md --opened 2026-10-25 --out $S/c5/out --entry corpus/knowledge/a.md --entry corpus/knowledge/b.md
COLLISIONS=0 / CITED=2 APPEND=1 HELD=1 / BODYONLY=0 (rc=0; S011 INVALID_RECHECK not refused; S011 marked held)
```

### F6 LOW — Refusal ordering and coverage gaps (`refusal_order`, `broken_reg_no_entry`, L344-378, L420-424)
- Docstring L47-51 orders refusals as: (1) registry structure (`registry_problems`), (2) entry missing/not UTF-8, (3) cited staged row with no URL, (4) invalid `recheck`. Code L356-378 emits `entry missing` (L359) *before* `registry_problems` (L365), emits two `REFUSED` lines when `## Registry` is missing on a non-empty registry (`no ## Registry heading` + `rows outside the Registry section`), and defers `recheck` to L420-424 (so `recheck` is skipped whenever an L356-374 refusal triggers, and exits on the first bad `recheck`).
- When `--entry` is omitted (L349-350), `registry_problems` is never called (`rc=0` on a headingless registry).
```
$ python3 $T --staged $S/refusal_order/staged.md --knowledge $S/refusal_order/knowledge --registry $S/refusal_order/registry.md --opened 2026-10-25 --out $S/refusal_order/out --entry corpus/knowledge/missing.md --entry corpus/knowledge/a.md
REFUSED entry missing: corpus/knowledge/missing.md
REFUSED registry has no `## Registry` heading
REFUSED registry rows outside the Registry section: S001
REFUSED S010: staged row has 2 cells, not 11   # rc=1; S011 BAD_RECHECK unreached; reg-ids/staged-ids/collisions written
```

### F7 LOW — Minor harness/helper inconsistencies (`pipe_free`, `registry_problems`, `observe`, CLI flags)
- `pipe_free` (L154-156): L373/389/450 run `url_of(pipe_free(staged[sid][1]))` before `subst`, whereas `append.md` (L410-414) runs `subst(c)` before inline pipe rewriting; a URL containing a cited `S\d{3,}` token at word boundaries differs between `append.md` and `renumber.tsv`. Also, while `registry_rows` (L150) uses `ESC_SPLIT` (D2), `scripts/sources-census.sh:635` and `c2-count.py:109` split registry rows on plain `"|"`.
- `registry_problems` / `lane_ids` (L168-186, L438): `GREP_RE` (L99) matches `| S005 (note) |` into `reg-ids`/`collisions`, whereas `ROW_RE` (L100) requires `|` after the id, so `registry_problems`, `base`, `nxt`, and `lane_ids` ignore it.
- `observe` (L246): `ENTRYCITES` uses `TOKEN_RE.findall` even in `source` mode, reporting `BODYONLY` tokens (`S016`, `S011`) inside `ENTRYCITES`. L313 error text omits `--cites`; main path ignores `--fixtures`/`--expected`.

VERDICT: reviewed the round-51 `tools/assimilate-rows.py` diff line by line with 11 runtime repros — frozen `c1-count.py` passes (5/5) and live round-51 staging maps S109..S126->S107..S113 with 5 body-clash warnings (S097, S105, S106), but found 1 HIGH (`--cites source` cross-entry body bleed in `subst`/`bodyonly.tsv`/`used-by`), 3 MEDIUM (`ASSIMILATE_CITES=all` failing `round50/c1-count.py`, `source_ids` full-line/full-file/case/duplicate bugs, silent drop of non-staged `source:` ids), and 3 LOW (`held`/recheck twin handling, refusal ordering, helper asymmetries) defects.
