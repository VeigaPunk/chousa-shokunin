# ScribeGatesR46 — Gates rows for round 46 (tool + three counters)

Seat `L1Chousa46.ScribeGatesR46` (scribe, leaf). Freeze commit named in the item
`c2f0e9d100c0d46633a6277b2fd51d2ac99678eb`. No network; no installs; no lane production file written
by this seat — only this report. `/tmp/chousa-r46-ScribeGatesR46` removed at exit.

## Item

Draft `## Gates` rows for (a) `tools/inference-ground.py` (entry contract; self-test = the r46 C1
counter) and (b) `corpus/evidence/round46/{c1,c2,c3}-count.py` with the frozen targets of
`corpus/evidence/round46/claims.md`; run each once read-only, paste output and exit code, quote the
committed controls for the self-test cells.

Read: `claims.md`; counter docstrings and `main()`s; `tools/inference-ground.py:1-232`;
`controls/{c1,c2,c3}-{before,controls}.txt`; Gates conventions `SKILL.md:75-112` (section ends at
`## Round26 …`, `SKILL.md:503`).

## Runs at the freeze tree (read-only; decisive lines verbatim)

```
$ python3 corpus/evidence/round46/c1-count.py            # tool present → this is the target state
TOOL=present / POSITIVE_PASS=3/3 / JUNK_KILLED=3/3 / C1=PASS            exit=0

$ python3 corpus/evidence/round46/c2-count.py --list    # tail
UNREGISTERED_PATH corpus/evidence/round46/c2-count.py
UNREGISTERED_PATH corpus/evidence/round46/c3-count.py
UNREGISTERED_PATH tools/inference-ground.py
ENTRY_POINTS=72 (tools=8 counters=50 named=70) / GATES_ROWS=30
REGISTERED=55/72 / UNREGISTERED=17 / C2=FAIL                           exit=1

$ python3 corpus/evidence/round46/c3-count.py
ENTRIES=0/2 / CITES_BOUND=0/5 / QUOTE_ROWS=0/11 / QUOTES_IN_SPAN=0/11
QUOTES_IN_ENTRY=0/11 / CAPTURE_BOUND=0/11 / REF_ID_UNBOUND=0 / REF_BOUND=0/2 / C3=FAIL   exit=1
$ … c3-count.py --lane-only                             → same, CAPTURE_BOUND=skipped, C3=FAIL, exit=1
```
Tool, all three exit codes (fixtures `corpus/fixtures/inference-ground-r46/`):
```
positive-a.md   → GROUND entry=positive-a.md section=1 bullets=1 tokens=1 grounded=1 / GROUND: PASS   exit=0
junk-uncited.md → FINDING INF_UNCITED bullet=1 token=''
                  FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='the release ships a frozen pool'
                  GROUND: FAIL                                                              exit=1
junk-ungrounded → FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='reverse index of every citation'     exit=1
--entry /tmp/nope.md → inference-ground: no entry /tmp/nope.md                          exit=2
no --spans/--counts  → error: the following arguments are required: --spans, --counts    exit=2
```
Counter exit-2 legs: `c1-count.py --root <empty>` → `C1=FAIL no-fixtures` exit 2;
`c2-count.py --root <empty>` → `C2=FAIL no-entry-points` exit 2. `c3-count.py` has **no** explicit
exit-2 return (`main()` returns 0/1 only); 2 is argparse-only — the row says so.

c1 controls re-derived live (the committed files name `/tmp/chousa-r46-controls/…`, now gone):
always-exit-0 `JUNK_KILLED=0/3`, bullet-level citation-presence-only `JUNK_KILLED=1/3`, both `C1=FAIL`
exit 1 — both reproduce `controls/c1-controls.txt`. A *file-level* S-id regex scores `0/3`
(`junk-uncited.md` cites S901 in Observation only), so the frozen control B is bullet-level.

Landing simulation at the freeze tree (temp `SKILL.md` copy, both rows after `tag-count`, lane
untouched): `GATES_ROWS=32 REGISTERED=59/72 UNREGISTERED=13` exit 1 — the pair registers exactly the
four item paths; the residual 13 were sibling-owned.

## State at re-read (lane moved under this seat; counters revised)

Blobs now: `c1-count.py` `96833e22b0eb…`, `c2-count.py` `60ad448e99b1…`, `c3-count.py` `234e2272e8e2…`
(all three `M` in `git status`); `spans.tsv`, `spans/`, `build-spans.py` present and untracked. Observed:
```
$ python3 …/c1-count.py      TOOL=present / 3/3 / 3/3 / C1=PASS                                   exit=0
$ python3 …/c2-count.py --list   ENTRY_POINTS=72 (tools=8 counters=50 named=70)
                                 GATES_ROWS=35 REGISTERED=72/72 UNREGISTERED=0 C2=PASS          exit=0
$ python3 …/c3-count.py      ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11
                             QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0
                             REF_BOUND=2/2 C3=PASS                                              exit=0
```
The two rows have landed (`SKILL.md:117` `inference-ground (r46)`, `SKILL.md:118`
`chousa round-46 counters`), expanded by the landing seat: `--registry corpus/SOURCES.md` added to the
tool entry, `--quiet` dropped, `build-spans.py [--check]` added to the counters row. My drafts are
below as the artifact I was asked for; the landed text is the lane's.

## Draft rows (verbatim; 8 cells each, one line each)

```markdown
| `inference-ground` (round 46) | tool | `python3 tools/inference-ground.py --entry PATH --spans TSV --counts JSON [--root DIR] [--json OUT] [--quiet]` | exit `0` grounded, no findings (`GROUND entry=… section=N bullets=N tokens=N grounded=N` then `GROUND: PASS`) · exit `1` findings (one `FINDING` line per bullet: `INF_SECTION_ABSENT`/`INF_UNCITED`/`INF_UNGROUNDED`/`INF_TOKEN_NOT_IN_SPAN`, then `GROUND: FAIL`) · exit `2` usage or unreadable input (argparse, unreadable entry/spans/counts) | `python3 corpus/evidence/round46/c1-count.py` → `TOOL=present` `POSITIVE_PASS=3/3` `JUNK_KILLED=3/3` `C1=PASS` exit `0` over `corpus/fixtures/inference-ground-r46/`; controls `corpus/evidence/round46/controls/c1-controls.txt`: always-exit-0 `JUNK_KILLED=0/3`, citation-presence-only `JUNK_KILLED=1/3`, both exit `1` (both re-observed 2026-10-25) | frozen `corpus/evidence/round46/claims.md` (R46-C1) at lane commit `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb`; before `TOOL=absent POSITIVE_PASS=0/3 JUNK_KILLED=0/3 C1=FAIL` exit `1` (`controls/c1-before.txt`); observed at that commit `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` exit `0` | read-only over the entry, the spans TSV and the counts JSON; `--json OUT` writes that one path only; no network | chousa |
| `chousa round-46 counters` | gate | `python3 corpus/evidence/round46/c1-count.py` · `python3 corpus/evidence/round46/c2-count.py --list` · `python3 corpus/evidence/round46/c3-count.py` · `python3 corpus/evidence/round46/c3-count.py --lane-only` | C1 exit `0` `POSITIVE_PASS=3/3` `JUNK_KILLED=3/3` `C1=PASS`; exit `1` any leg short (`TOOL=absent` or a junk fixture passed); exit `2` `C1=FAIL no-fixtures` · C2 exit `0` `UNREGISTERED=0` `C2=PASS`; exit `1` `UNREGISTERED=k` `C2=FAIL`; exit `2` `C2=FAIL no-entry-points` · C3 exit `0` `ENTRIES=2/2` `CITES_BOUND=5/5` `QUOTE_ROWS=11/11` `QUOTES_IN_SPAN=11/11` `QUOTES_IN_ENTRY=11/11` `CAPTURE_BOUND=11/11` `REF_ID_UNBOUND=0` `REF_BOUND=2/2` `C3=PASS`, `--lane-only` the same with `CAPTURE_BOUND=skipped`; exit `1` any count short of its target in either mode; exit `2` usage only (argparse; c3 has no explicit env exit) | c2 forges stay unregistered — paths pasted as prose, a six-cell row, an eight-pipe row without `exit`, a valid row after the next `## ` heading (`controls/c2-controls.txt`; its receipt tree is `6e2630a6` plus this round's counters and fixtures with the tool absent, so its tally is NOT the bare-base-commit tally); c3 forged entries plus invented capture digests `C3=PASS` exit `0` under `--lane-only` and `CAPTURE_BOUND=0/11 C3=FAIL` exit `1` by default (`controls/c3-controls.txt`); c1 controls as in the `inference-ground` row | frozen `corpus/evidence/round46/claims.md` (R46-C1/C2/C3) at lane commit `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb`; before `controls/c2-before.txt` (augmented tree, tool absent) `ENTRY_POINTS=71 (tools=7 counters=50 named=66) GATES_ROWS=30 REGISTERED=55/71 UNREGISTERED=16` exit `1` — not reproducible at bare `6e2630a6`, so pin the target shape, not that tally; `controls/c3-before.txt` `ENTRIES=0/2 CITES_BOUND=0/5 QUOTE_ROWS=0/11 C3=FAIL` exit `1`; observed at `c2f0e9d1` `ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=30 REGISTERED=55/72 UNREGISTERED=17` exit `1`, still before these rows land | read-only over `SKILL.md`, `SCORECARD.md`, `corpus/evidence/round*/claims*.md`, `tools/`, `corpus/SOURCES.md` and the fixtures; c3 also reads the campaign capture cache `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (`--cache`); no writes, no network | chousa |
```

## Verdict

Drafted as asked; both rows are now landed in expanded form and every r46 leg is observed at the
current blobs: `C1=PASS`, `C2=PASS` (`UNREGISTERED=0`, `GATES_ROWS=35`), `C3=PASS` (all 11/11 legs,
default mode). Counts in a row must carry their blob, since all three counters moved after this lane's
freeze.

## Findings

1. **F1** `tools/inference-ground.py:181` accepts `--registry`, absent from the item's entry string; the
   landed row adds it. Ran once (`--registry corpus/SOURCES.md --quiet`, exit `0`).
2. **F2** `c3-count.py` docstring promises exit `2 usage/env`; `main()` has no exit-2 return
   (argparse only). The row says "usage only"; no behaviour change requested.
3. **F3** Committed c1/c2/c3 control receipts are `/tmp`-based and no longer on disk: c1 controls
   re-derived (`0/3`, `1/3` reproduced); c2/c3 controls quoted from their files, not re-run.
4. **F4 (from `L1Chousa46.MutC2Forge`)** `c2-count.py` credits a path by raw substring — a row of
   nonexistent `X.pyc`/`X.py.disabled`/`X.shc` names, or a fenced/`<!-- -->` row, reaches
   `UNREGISTERED=0 C2=PASS` registering nothing. Both rows are unaffected (visible 8-column rows, each
   real path its own backticked token; regex check: no `.pyc`/`.shc`, all four paths exist).
5. **F5 (same peer, and a conflict to report verbatim)** three trees for the same frozen counter:
   bare `6e2630a6` + this round's counters/fixtures, tool absent → `ENTRY_POINTS=68 (tools=7
   counters=47 named=66) REGISTERED=55/68 UNREGISTERED=13` exit 1; the receipt's own declared tree →
   `71 (7/50/69) 55/71 UNREGISTERED=16` exit 1 per that peer, while the committed
   `controls/c2-before.txt` line and my own freeze run both print `71 (7/50/66)` / `72 (8/50/70)` —
   the `named` leg differs (66 vs 69) and this seat cannot reproduce 69 from any tree it opened; live
   with the untracked tool → `72 (8/50/70) 55/72 UNREGISTERED=17` (matches my run). The "base tree"
   parenthetical at `claims.md:40` is the mislabel (it describes c1's before line and does not hold for
   `controls/c2-before.txt`); the receipts themselves declare their tree correctly.
6. Nothing superseded among counters; round-45 counters keep their own rows.
   `corpus/evidence/round46/build-spans.py` is now named in the landed counters row (it was not an
   R46-C2 entry point at freeze, and is untracked).
7. No install or upgrade; no lane file modified by this seat (only this report).

Pointers: `corpus/evidence/round46/claims.md`; `corpus/evidence/round46/{c1,c2,c3}-count.py`;
`corpus/evidence/round46/controls/`; `tools/inference-ground.py:1-232`;
`corpus/fixtures/inference-ground-r46/`; `SKILL.md:75-502`, landed rows `SKILL.md:117-118`.
