# ExecSelftestEdge — edge probes for `assimilate-rows.py --selftest` (R50 W1, C1)

tool: `tools/assimilate-rows.py` @ `ec52e63`, sha256 `bff32c11d02bc1bdc28ed484d4895d86c7f3537d8a9496ad474c73d4531f5b81`, 363 lines, worktree clean for that path.
fixtures: scratch copies of `corpus/evidence/round50/c1-fixtures/` under `/dev/shm/chousa-r50-ExecSelftestEdge/` (`cp -a base` per probe). Scratch deleted at the end. No installs, no network.
baseline (pinned package, pinned expected):
`python3 tools/assimilate-rows.py --selftest --fixtures $S/base --expected $S/base/expected.json` → rc 0, last line
`SELFTEST=PASS findings=26 expected=26`, `FIXTURES_SHA256=c5c56480e9f6a08d6a2077b6a11267a4cabf0bc0d3f726408a9bb0238283cd43` (= C1 `PIN`).
expected.json is duplicate-free: `lines 26 unique 26 dups []`.

## Probe table (each on its own `cp -a` copy; last line of `--selftest`)

| # | probe | rc | last line | class |
|---|---|---|---|---|
| a | `findings` = first line prepended (one duplicate) | 0 | `SELFTEST=PASS findings=26 expected=27` | **defect**: silent pass, multiplicity ignored |
| b | same 26 findings reversed | 0 | `SELFTEST=PASS findings=26 expected=26` | designed (order-insensitive) |
| c | `knowledge/corpus/knowledge/a.md` = `...\xff\xfe bad\n` | 1 | `SELFTEST=FAIL findings=3 expected=26` | designed |
| d | `rm -rf knowledge/` | 1 | `SELFTEST=FAIL findings=2 expected=26` | half: FAIL not ERROR; tool exits 0 |
| e | `rm -f registry.md` | 2 | `SELFTEST=ERROR fixtures $S/e: staged.md or registry.md missing` | designed |
| f | literal tab inside the stripped `recheck` cell, and inside the `anchor` cell | 1 | `SELFTEST=FAIL findings=25 expected=26` + `DIFF missing STRIPPED S015 cell6-pipe` | designed for the pipe leg; **defect** for the tab (see f2) |
| g | `--fixtures $S/base/staged.md` | 2 | `SELFTEST=ERROR fixtures .../staged.md: staged.md or registry.md missing` | designed rc, misleading message |
| h | `{"findings": null}` | 2 | `SELFTEST=ERROR expected file $S/h/expected.json: findings must be a list of strings` | designed |

## a — duplicate expected line passes (set comparison, source:220)
`miss, extra = sorted(set(want) - set(got)), sorted(set(got) - set(want))`; `ok = not miss and not extra`.
Observed: rc 0, `SELFTEST=PASS findings=26 expected=27`. The verdict ignores the count delta it prints, and no `DIFF` line names the duplicate. A hand-written expected file whose duplicate hides a copy error is reported PASS. Impact on frozen C1: none — the pinned file has 26 unique lines and its bytes are inside `FIXTURES_SHA256`.

## c — non-UTF-8 entry: refusal, not a crash (designed)
`--selftest` on the poisoned copy: rc 1, `DIFF unexpected TOOLEXIT 1`, `DIFF unexpected REFUSED entry not UTF-8: corpus/knowledge/a.md`. Tool run directly:
`... --entry corpus/knowledge/a.md` → `COLLISIONS=2` / `REFUSED entry not UTF-8: corpus/knowledge/a.md`, rc 1, no traceback.
Nit: `reg-ids`, `staged-ids`, `collisions` are written into `--out` before the refusal (docstring's "exit 1, nothing claimed" holds for claims only).

## d — missing `knowledge/`: FAIL instead of ERROR, and the tool exits 0
`--selftest` rc 1, `SELFTEST=FAIL findings=2 expected=26` — a broken fixture tree is reported as a tool regression, while a missing `registry.md` is `SELFTEST=ERROR` rc 2 (source:214-215 checks only `staged.md`/`registry.md`).
Tool directly, `--knowledge $S/d/knowledge` (absent), no `--entry`: `COLLISIONS=2`, **rc 0** — `main` guards only `--staged`/`--registry`/`--opened` (source:247), so the docstring's "2 usage (missing file ...)" does not cover `--knowledge`. With `--entry` it refuses correctly (`REFUSED entry missing: corpus/knowledge/a.md`, rc 1).
**Silent-pass defect (no work floor):** `knowledge/` removed *and* expected reduced to what survives:
`{"findings": ["TOOLEXIT 0", "COLLISIONS S011,S012"]}` → rc 0, `SELFTEST=PASS findings=2 expected=2` with **zero entries exercised**. The self-test never asserts that any entry was found or any `ENTRYCITES`/`ROWCELLS` line exists, so a degenerate package passes.

## f — literal tab: absorbed when stripped, silently carried when not
f(recheck cell `2026-12-01<TAB>— re-verify after release`): `LEAD_RE`'s `^\s*` absorbs the tab; tool rc 0; `stripped.tsv` shows `S014<TAB>recheck<TAB>2026-12-01 — re-verify after release` (tab→space by source:356), `append.md` cell clean (`| 2026-12-01 |`). Designed.
f(anchor cell with a tab instead of the escaped pipe): `DIFF missing STRIPPED S015 cell6-pipe`, rc 1 — correct (no pipe left to rewrite).
**Defect f2 — unrecorded normalisation asymmetry:** tab in the `teaches` cell (a cell nothing else rewrites), tool run directly, rc 0; `append.md` byte-exact:
`| S013 | New doc A — https://example.test/new-a | docs | A | scope a | section a | what row^Ia teaches | mined | 2026-10-25 | 90d | corpus/knowledge/a.md |` (`cat -A`, `^I` = literal tab).
`stripped.tsv` has no row for it (`S013 opened` only), while a `|` in the same position *is* rewritten to ` / ` and recorded as `cell6-pipe`. So a tab enters the lane append block verbatim and the round-49 Gate block ("every cell text the normalisation removed") cannot see it; a TSV/awk consumer of the lane row breaks. `--selftest` on that package: rc 0, `SELFTEST=PASS findings=26 expected=26`, digest `c888245c63e6...` — a changed fixture with unchanged findings passes (the digest is printed, never compared to a pin).
Second reading of the probe (tabs inside an entry *file*): tool rc 0, tab preserved in the copied entry (`- tab^Iseparated^Iprose citing (S013) and (S014).`), `--selftest` rc 1 on `DIFF unexpected ENTRYCITES corpus/knowledge/a.md S013,S014` — correct.

## g / h — usage errors (designed rc, weak messages)
g: rc 2, `SELFTEST=ERROR fixtures .../staged.md: staged.md or registry.md missing` (path is a file, not a dir). With `--expected` omitted: rc 2, `SELFTEST=ERROR expected file .../staged.md/expected.json: [Errno 20] Not a directory: '...'` (path concatenation leaks into the message).
h: `findings: null` → rc 2 `findings must be a list of strings`; `{"rows": []}` → rc 2 with the bare KeyError text `'findings'`; `["TOOLEXIT 0", 7]` → rc 2; `--expected` a directory → rc 2 `[Errno 21] Is a directory`. No tracebacks in any of these.

## Extras that bound the claim (measured)
- External `--expected` (moved out of the package): rc 0 PASS, `FIXTURES_SHA256=f7f0a8d7ff8e79651c6dca23b920369eb632bd41d74911bd88b11f2dcab6b685` ≠ pin → the digest covers the expected bytes only while they live inside the fixture dir.
- Lane default `python3 tools/assimilate-rows.py --selftest` → rc 0, `SELFTEST=PASS findings=26 expected=26`, digest = pin. `diff -r corpus/fixtures/assimilate-selftest corpus/evidence/round50/c1-fixtures` → rc 0, but `stat -c %i` gives 172309908 vs 172407927: two byte-identical copies, so the default leg and the counter leg can drift apart silently.
- Temp root: `observe()` uses `tempfile.mkdtemp` (source:154); `tempfile.gettempdir()` = `/tmp`; with `TMPDIR=$S` the created dir is `$S/assimilate-selftest-_wspq2wv` and is removed (`leftover []`). A full `/tmp` (round-49 failure) is therefore avoidable only via `TMPDIR`; there is no `--out`/`--tmpdir` flag. I could not force an ENOSPC temp root (64k and `nr_inodes=3` tmpfs both still accepted `mkdir`), so the no-temp-root crash path is [INFERENCE], not exercised.
- Child stderr is filtered to `REFUSED ` lines only (source:163), so a traceback inside the tool and a designed refusal both surface as `TOOLEXIT 1`; the crash would be visible only as a missing `REFUSED` line (code-read, not exercised — no fixture input I tried crashes the tool).

## Draft fixes — round-51 material, NOT for landing in round 50 (would change the frozen C1 candidate)
```text
intended lane path: tools/assimilate-rows.py  (do not apply this round)
selftest:  want_m, got_m = collections.Counter(want), collections.Counter(got)
           ok = not miss and not extra and want_m == got_m        # a: multiplicity
           if not know.is_dir(): SELFTEST=ERROR fixtures ... knowledge/ missing  # d: rc 2
main:      if not know.is_dir() ... : usage rc 2                  # d: tool leniency
append.md: for tabs as for pipes: record (lid, f"cell{i+1}-tab", c); cells[i] = re.sub(r"\t+", " ", c)  # f2
```

## Risks / blockers
- a and d(degenerate) are silent-pass holes in the reusable gate the round-49 closure asked for; neither touches C1's pinned leg (pin reproduced, expected file duplicate-free), so C1's operability measurement stands as far as this seat's surface goes.
- f2 shows the adopter can emit an unrecorded literal tab into a lane row; the pinned fixtures never exercise it.
- Blockers: none. Files changed: this report only.

VERDICT: attacked `assimilate-rows.py --selftest` with the 8 assigned edge probes plus 6 extras — 5 designed behaviours (c, e, h, b, and the pipe leg of f), 3 defects (a: duplicate expected line passes as PASS findings=26 expected=27; d: no work floor, a 2-line expected file PASSes with `knowledge/` absent and zero entries exercised, plus the tool's exit-0 on a missing `--knowledge`; f2: literal tab reaches `append.md` unrecorded and a changed fixture still PASSes at digest `c888245c…`), C1's pinned leg unaffected.
