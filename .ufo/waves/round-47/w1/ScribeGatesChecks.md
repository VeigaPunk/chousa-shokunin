# ScribeGatesChecks — round 47 wave 1 (scribe)

**Item.** Draft SKILL.md `## Gates` rows for `corpus/evidence/round29/prose-check.py`, `corpus/evidence/round30/rerun-check.py`, `corpus/evidence/round32/q33-check.py` and `corpus/evidence/round25-meta-oracle.py`. Run each script read-only on a /tmp `git archive` of the lane, insert the rows into a /tmp copy of SKILL.md, and show with `round47/c2-count.py --root <tmp> --list` that these paths are no longer UNREGISTERED.

**Verdict.** Done. With the four rows added to a /tmp SKILL.md copy, all four paths drop out of the UNREGISTERED list: `UNREGISTERED=25` goes to `21`, `MISMATCHES=25` goes to `21`, `DANGLING=0` stays 0 and `ENTRY_POINTS=92` stays 92. `C2=FAIL` remains, because 21 other paths belong to other items. No lane production file was modified.

## Setup (all commands are mine; nothing ran in the lane)

`git -C …/chousa-shokunin rev-parse HEAD master` returned `a15610a59aaeaf43b79ccc650acee4bd4da00341` for both. `git … archive master | tar -x -C /tmp/chousa-r47-ScribeGatesChecks/lane`. All runs below were made with cwd at the /tmp lane root.

sha256 values, which equal the lane tree:
- prose-check.py `51859479a17219d4f44a20a9e88749ef98cb05fee4919360d8df7d317ae14fec`
- rerun-check.py `7f36e65b2480436b9029253dc65f58e5cd1aef5580ac73654199d8f6b745acd9`
- q33-check.py `d9077374116ab41309ee8acf53eb13c459a83bf39dfba938256327b357dbfa26`
- round25-meta-oracle.py `48127da0861b3f802071bf38e4fc0987ff8e80f2bd128a1bebcbe27b88ea5c57`, which matches `corpus/evidence/round25-final-pin.json:9`

## What names each path

- `prose-check.py`: QUALITY 23, `corpus/QUALITY.md:155`. The criterion says exit 0 on new prose, and exit 1 on `lessons/round-28.md` with 9 glued tokens and 5 custody hits.
- `rerun-check.py`: QUALITY 27, `corpus/QUALITY.md:191`. The criterion says `RERUN_RECEIPTS=5/6` exit 1 against 6, and exit 0 against 5.
- `q33-check.py`: QUALITY 33, `corpus/QUALITY.md:255`. The criterion says FAIL exit 1 on the round-31 lesson at `4111607c`, and PASS exit 0 after the correction.
- `round25-meta-oracle.py`: **QUALITY.md does not name this path** (a grep finds 0 hits). It is named at `corpus/evidence/round25-meta-differential.sh:6,40`, which is the script that invokes it, and at `SKILL.md:86`, in the pinned-values cell of the verify-metadata row. The item's description of it as "QUALITY-named" is inaccurate. See finding F1.

## Runs (verbatim; long output trimmed to the decisive lines)

```
$ python3 corpus/evidence/round29/prose-check.py corpus/lessons/round-28.md
  digit-glued tokens: 9   (actual64 all69 blanket64 legacy161×2 most25 on2026 original187 proposal64)
  custody vocabulary: 5   (CURRENT_MAIN_DIRECTIVE:53 'Parent decision':5 'Root report':63 'private original':39 report-LAST:63)
TOTAL hits=14 files=1                                  exit=1
$ python3 corpus/evidence/round29/prose-check.py corpus/lessons/round-29.md
  digit-glued tokens: 0 / custody vocabulary: 0 / TOTAL hits=0 files=1   exit=0
$ python3 corpus/evidence/round29/prose-check.py
usage: python3 prose-check.py FILE...                  exit=2
$ python3 corpus/evidence/round30/rerun-check.py --stated 6 <5 round-29 receipts>
seed=16442982337510174646 MATCH=130/130 …RerunCounterA/receipt.json
seed=5392061795029416258  MATCH=130/130 …RerunCounterB/receipt-1.json
seed=1932010155184684229  MATCH=130/130 …RerunCounterB/receipt-2.json
seed=13173258806708832500 MATCH=130/130 …ScoutFreshnessH/rederive-receipt.json
seed=3497534629407128034  QUOTE_REOPEN_MATCH=130/130 …ScoutFreshnessH/rederive3.out
RERUN_RECEIPTS=5/6                                     exit=1
$ … --stated 5 <same 5>   → same seed lines, RERUN_RECEIPTS=5/5   exit=0
$ … --stated 1 SKILL.md   → rerun-check: SKILL.md: no seed field and no seed= line   exit=2
$ python3 corpus/evidence/round30/rerun-check.py → error: the following arguments are required: --stated, FILE   exit=2
$ python3 corpus/evidence/round32/q33-check.py
PASS: claim=True receipts=120/120,120/120 correction=True   exit=0
$ git -C <lane> show 4111607c:corpus/lessons/round-31.md > /tmp/…/round-31@4111607c.md   (exit 0)
$ python3 corpus/evidence/round32/q33-check.py /tmp/…/round-31@4111607c.md
FAIL: claim=True receipts=120/120,120/120 correction=False  exit=1
$ (cd /tmp/chousa-r47-ScribeGatesChecks && python3 lane/corpus/evidence/round32/q33-check.py lane/corpus/lessons/round-31.md)
q33: expected 2 fail-open receipts, found 0            exit=2
$ python3 corpus/evidence/round32/q33-check.py /nonexistent.md
FileNotFoundError: [Errno 2] No such file or directory: '/nonexistent.md'   exit=1
$ python3 corpus/evidence/round25-meta-oracle.py corpus/fixtures/metadata-r25/bom-first-line.md
META entry=bom-first-line.md source=present verified_at=dated recheck=scheduled verdict=clean
METADATA_COMPLETE=1/1 / RESEARCH_GATE: CLEAN           exit=0
$ python3 corpus/evidence/round25-meta-oracle.py corpus/knowledge
drift: archives-verified-r9.md audit-r11.md gate-baseline-r8.md (recheck=absent), dead-zone-pcre-r34.md (all absent)
METADATA_COMPLETE=57/61 / RESEARCH_GATE: DRIFT         exit=1
$ python3 corpus/evidence/round25-meta-oracle.py /nonexistent.md
verify-metadata: PATH is missing, unreadable, or is not a .md file/directory   exit=2
$ python3 corpus/evidence/round25-meta-oracle.py → error: the following arguments are required: path   exit=2
$ bash corpus/evidence/round25-meta-differential.sh | tail -1
AGREE=54/54 (fixtures=27, modes normal+strict)         exit=0
```

## Counter: before and after (the /tmp SKILL.md copy is byte-equal to master, `git diff --quiet master -- SKILL.md` exit 0; rows inserted after line 118, the last Gates row)

```
before  $ python3 corpus/evidence/round47/c2-count.py --root /tmp/…/lane --list
UNREGISTERED_PATH corpus/evidence/round25-meta-oracle.py
UNREGISTERED_PATH corpus/evidence/round29/prose-check.py
UNREGISTERED_PATH corpus/evidence/round30/rerun-check.py
UNREGISTERED_PATH corpus/evidence/round32/q33-check.py
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7) FLOOR=92 GATES_ROWS=36
REGISTERED=67/92 UNREGISTERED=25 DANGLING=0 MISMATCHES=25 C2=FAIL   exit=1
after   (same command, rows added; grep for the four paths in --list output: no hits, grep exit 1)
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7) FLOOR=92 GATES_ROWS=40
REGISTERED=71/92 UNREGISTERED=21 DANGLING=0 MISMATCHES=21 C2=FAIL   exit=1
```

Each row has exactly 8 cells (`awk -F'|' '{print NF-2}'` gives `8 8 8 8`; re-checked on the report copy with the counter's own split, 8 cells and 0 `\|` per row) and contains no tab characters. The rows file sha256 is `8a5d3b0618ed122a58d6165b1a61b39d85ec94c580a67c73d86eb7c28b6730e1`.

## Rows (verbatim, for insertion after the `chousa round-46 counters` row, SKILL.md:118)

```
| `prose-check` (QUALITY 23, r29) | check | `python3 corpus/evidence/round29/prose-check.py FILE...` (lane root; one or more files) | exit `0` no hits: per file `digit-glued tokens: 0` and `custody vocabulary: 0`, then `TOTAL hits=0 files=N` · exit `1` at least one digit-glued token (outside code spans, fences and URLs) or custody term (whole text), `TOTAL hits=k files=N` with k ≥ 1 · exit `2` no FILE (`usage: python3 prose-check.py FILE...`) or an unreadable or non-UTF-8 file | control `corpus/lessons/round-28.md` → `digit-glued tokens: 9`, `custody vocabulary: 5`, `TOTAL hits=14 files=1`, exit 1; pass leg `corpus/lessons/round-29.md` → `TOTAL hits=0 files=1`, exit 0; no argument → exit 2 | measured on a `git archive` of lane commit `a15610a59aaeaf43b79ccc650acee4bd4da00341` (round-47 wave-1 `ScribeGatesChecks`); sha256 `51859479a17219d4f44a20a9e88749ef98cb05fee4919360d8df7d317ae14fec`; QUALITY 23 | read-only | chousa |
| `rerun-check` (QUALITY 27, r30) | check | `python3 corpus/evidence/round30/rerun-check.py --stated N FILE [FILE ...]` (JSON receipts or captured counter output) | prints one tab-separated `seed=<int>` · `<NAME>=n/t` · file line per receipt, then `RERUN_RECEIPTS=<distinct seeds>/<stated>`; exit `0` distinct seeds = N · exit `1` they differ (shared seeds count once, stderr note) · exit `2` a file with no seed or no match line (`no seed field and no seed= line`), or argparse usage | control: the five round-29 re-run receipts (`.ufo/waves/round-29/falsify/RerunCounterA/receipt.json`, `RerunCounterB/receipt-1.json`, `receipt-2.json`, `ScoutFreshnessH/rederive-receipt.json`, `rederive3.out`) with `--stated 6` → `RERUN_RECEIPTS=5/6`, exit 1; same files `--stated 5` → `RERUN_RECEIPTS=5/5`, exit 0; `--stated 1 SKILL.md` → exit 2 | measured on a `git archive` of lane commit `a15610a59aaeaf43b79ccc650acee4bd4da00341` (round-47 wave-1 `ScribeGatesChecks`); sha256 `7f36e65b2480436b9029253dc65f58e5cd1aef5580ac73654199d8f6b745acd9`; QUALITY 27 | read-only | chousa |
| `q33-check` (QUALITY 33, r32) | check | `python3 corpus/evidence/round32/q33-check.py [LESSON]` (cwd MUST be the lane root: it globs `.ufo/waves/round-31/falsify/MutC2Hash/failopen.mutated.*.receipt.json` relative to cwd; default LESSON `corpus/lessons/round-31.md`) | a single-purpose probe bound to the round-31 R1 attribution, not a general gate · exit `0` `PASS: claim=… receipts=…,… correction=…` · exit `1` `FAIL: claim=True receipts=120/120,120/120 correction=False` (kill sentence present, both receipts matched == total, no correction section citing both receipts with "survived") · exit `2` receipt count ≠ 2 (`q33: expected 2 fail-open receipts, found 0`) · a missing LESSON raises an uncaught `FileNotFoundError` and exits `1`, the same code as FAIL (named limit) | control: the round-31 lesson as committed at `4111607c` → `FAIL: claim=True receipts=120/120,120/120 correction=False`, exit 1; the lesson at HEAD → `PASS: claim=True receipts=120/120,120/120 correction=True`, exit 0; run from outside the lane root → exit 2 | measured on a `git archive` of lane commit `a15610a59aaeaf43b79ccc650acee4bd4da00341` (round-47 wave-1 `ScribeGatesChecks`); sha256 `d9077374116ab41309ee8acf53eb13c459a83bf39dfba938256327b357dbfa26`; QUALITY 33 | read-only | chousa |
| `round25-meta-oracle` (r25 verify-metadata oracle) | instrument | `python3 corpus/evidence/round25-meta-oracle.py PATH [--root DIR]` (PATH is one `.md` or a directory of direct `.md` children; `--root` accepted for the registered command shape, unused; `CHOUSA_STRICT=1` turns info findings into drift) | the independent stdlib oracle the round-25 differential compares with `research-gate verify-metadata`; it reports, it does not admit: exit `0` `METADATA_COMPLETE=n/m` then `RESEARCH_GATE: CLEAN` · exit `1` any warn finding (or info under `CHOUSA_STRICT=1`), `RESEARCH_GATE: DRIFT` · exit `2` missing, unreadable or non-`.md` PATH, a directory without `.md` (`verify-metadata: PATH is missing, unreadable, or is not a .md file/directory`), or argparse usage | differential `bash corpus/evidence/round25-meta-differential.sh` → `AGREE=54/54 (fixtures=27, modes normal+strict)`, exit 0; `corpus/fixtures/metadata-r25/bom-first-line.md` → `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN`, exit 0; `corpus/knowledge` → `METADATA_COMPLETE=57/61`, `RESEARCH_GATE: DRIFT`, exit 1; a missing path → exit 2 | measured on a `git archive` of lane commit `a15610a59aaeaf43b79ccc650acee4bd4da00341` (round-47 wave-1 `ScribeGatesChecks`); sha256 `48127da0861b3f802071bf38e4fc0987ff8e80f2bd128a1bebcbe27b88ea5c57`, equal to the pin in `corpus/evidence/round25-final-pin.json` | read-only | chousa |
```

## Findings

- **F1 (item premise).** QUALITY.md does not name `round25-meta-oracle.py`. It enters the entry-point set through the r46 set or the dependence closure from `round25-meta-differential.sh:40`, not through CHECK-NAMED. Its row is typed `instrument` and marked "reports, it does not admit".
- **F2 (row-parse defect, routed to the owner of SKILL.md:114).** The r46 row `round24–27 counting instruments` writes `[c1\|c2\|c3\|holds\|all]` in its entry cell. Both the r46 and r47 counters split on every raw `|` (`r.strip().strip("|").split("|")`), so this row parses as 14 cells and cell 4 is `c2\`, which does not contain `exit`. As a result, none of the row's ten paths register. That covers `round24-measure.sh`, `round25-measure.sh`, `round25-ledger-recount.py`, `round25-meta-differential.sh`, `round26-*`, `round27-*`, all present in the before list. Run: `python3 -` over SKILL.md gave `114 cells 14 exit-in-cell4 False`. A fix is to drop the escaped pipes, for example `{c1,c2,c3,holds,all}`. `ScribeGatesWaves` reported, and I re-ran to confirm, the same split on SKILL.md:100 (`mechanism-witness`, r35). That row has no `\|`; the raw pipes are inside the code span `WITNESS=pass|fail|unparseable|timeout …`, and the row parses as 11 cells with no `exit` in cell 4. That is why `tools/mechanism-witness.py` is in the UNREGISTERED list. The rule for every row: no `|` inside any cell, whether escaped or in backticks. Routing, agreed with `ScribeGatesWaves`: line 100 is covered by row 4 of `ScribeGatesWaves.md`, which they report registers `tools/mechanism-witness.py` on their /tmp splice, so this item drafts no row for it. Line 114 is in neither item and goes to Main as an open row-repair item. My first draft named `round25-meta-differential.sh` in the oracle's entry cell, which also registered that path (`UNREGISTERED=20`). I removed it from the entry cell so my rows register only the four assigned paths.
- **F3 (q33 exit contract).** A missing LESSON gives an uncaught traceback with exit 1, which collides with `FAIL` exit 1. The receipt glob is relative to cwd, so running it outside the lane root gives exit 2. Both limits are named in the row. I did not change the script.
- **F4 (observed, not routed).** The oracle over `corpus/knowledge` reports `METADATA_COMPLETE=57/61`. The drift entries are the three entries SKILL.md:86 already names (recheck absent), plus `dead-zone-pcre-r34.md`, which has no source, verified-at or recheck.

## Scope and limits

- Out of scope: the other 21 UNREGISTERED paths and any edit to the lane's SKILL.md. Integration belongs to L1.
- Each row's verdict map was checked by running the script, but the counter does not verify row truth (as `c2-count.py:38` states).
- No network. No installs. No subagents.
- Scratch dir `/tmp/chousa-r47-ScribeGatesChecks/` was deleted at the end.
