# R54W2ExecLedger — considerthese ledger attack (round 54, W2 FALSIFY)

Seat: `R54W2ExecLedger`. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` (read-only for me).
Nothing was judged or changed in production; my only writes are this report and removable scratch
`/fast/scratch/hyaku/chousa-r54/R54W2ExecLedger` (removed at the end). No tool installed or upgraded.

## 0. Bytes attacked (identical at the L1 tip and at the tip I ran on)

Lane HEAD moved 178667d → 25abbe8 while I worked (sibling W2 reports landing). The ledger did not move:

```
$ git diff --stat 447cf7ed4dc1a3708518b99e9a5e62e177c11ce9 HEAD -- considerthese \
    corpus/evidence/round54/considerthese-ledger.tsv corpus/evidence/round54/considerthese-ledger-check.py
(empty)
$ sha256sum corpus/evidence/round54/considerthese-ledger*.{py,tsv}
1f9f01f70dbba78a2b27d80be81b70e25084219d6681d7012f842fdfc7605ae4  considerthese-ledger-check.py
43113504729bcd3910fb3763ed9654e69b246d2d094c76043961d8cca5132eab  considerthese-ledger.tsv
$ git show 447cf7e…:corpus/evidence/round54/considerthese-ledger-check.py | sha256sum
1f9f01f7…  -                       # same bytes at the integrated tip
```

## 1. The check passes at the tip — reproduced

```
$ python3 corpus/evidence/round54/considerthese-ledger-check.py --root .
PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0
EXIT=0
```

## 2. Five mutants, each in its own scratch root (considerthese/ copied; ledger copied; corpus/, tools/,
SCORECARD.md symlinked read-only), invoked as
`python3 …/considerthese-ledger-check.py --root $dir --ledger $dir/ledger.tsv`

| mutant | change | observed | exit |
|---|---|---|---|
| drop a row | deleted ledger row `CT-20261020-3` | `FAIL MISSING CT-20261020-3` · `PROPOSALS=35 ROWS=34 … BAD=1` | 1 |
| duplicate a row | appended `CT-20261020-3` verbatim | `FAIL DUP CT-20261020-3` · `ROWS=36 … BAD=1` | 1 |
| IMPL row → missing file | `CT-20261020-3` pointer `tools/quote-reopen.py` → `tools/does-not-exist.py` | `FAIL POINTER CT-20261020-3 tools/does-not-exist.py` · `BAD=1` | 1 |
| row with three columns | dropped the `note` field of `CT-20261020-3` | `FAIL COLUMNS CT-20261020-3` · `IMPL=23 … BAD=1` | 1 |
| new `considerthese/2026-10-27.md`, `## Self-improvement proposals` + 2 `- ` bullets | file added | `FAIL MISSING CT-20261027-1` / `FAIL MISSING CT-20261027-2` · `PROPOSALS=37 ROWS=35 BAD=2` | 1 |

Extra, the checker's other declared failure mode: pointer `tools/quote-reopen.py::^ZZZ_NO_MATCH` →
`FAIL REGEX CT-20261020-3 tools/quote-reopen.py::^ZZZ_NO_MATCH`, exit 1.
All five required mutants behave as the lesson claims; the four declared modes are real, not vacuous.

## 3. Holes the checker does not close (all observed, exit 0 with BAD=0)

1. **Year glob.** `pathlib.glob("2026-*.md")` (`considerthese-ledger-check.py:17`) hard-codes the year.
   `considerthese/2027-01-01.md` with a proposals heading and two `- ` bullets → `PROPOSALS=35 … BAD=0`,
   **exit 0**: every file after 2026-12-31 escapes the ledger with no signal.
2. **Bullet marker.** Only `line.startswith("- ")` counts (`:21`). A `*` bullet inserted *inside* the
   proposals section of `2026-10-26.md` → `BAD=0`, exit 0; an unledgered proposal is invisible.
3. **Ids are positional and the id→text binding is never checked** (`want` = 1-based bullet order, `:16-21`;
   the ledger's `note` column is never compared to anything, `:26-33`). Swapping bullets 1 and 2 of
   `2026-10-26.md` → `BAD=0` exit 0, although `CT-20261026-1`'s row now describes proposal 2. Replacing
   bullet 1's text wholesale with `- **Something completely different.** No ids, no ledger, no uptake.` →
   `BAD=0` exit 0, while the row that *is* the stable-id proposal (`CT-20261026-1`) now points at a
   proposal that no longer exists. The checker proves a count, never an identity.

## 4. Eight IMPL rows opened by hand (bullet text vs pointed file)

| row | proposal asks for | pointed artifact, what it actually does | implements? |
|---|---|---|---|
| CT-20261019-1 | run `--selftest`/`--drift` read-only against r8, confirm `PASS (85 cases)` / `GATE_DRIFT: none` | `corpus/evidence/round40/c1-count.py:2` "Count r39 receipts that verify against their committed input bytes"; prints `R39_ACTIVE_RECEIPTS=6/6`; `grep argparse\|selftest\|drift\|r8` → none | **NO** |
| CT-20261019-2 | hardening-r10 ledger (68 rows) + 27-item r11 queue + `A-r9.md:50` finding, daily | `round25-ledger-recount.py:6` "the 71 §3 rows"; run: `rows=71 … queue_committed=24 queue_true=25`; `grep A-r9\|audit\|27` → none; one-shot | **PARTIAL** |
| CT-20261019-3 | flag when Saturation line and window N are declared and Capabilities rows earned | `SCORECARD.md::^## Capabilities` matches the first of 23 such headings; that table is `| — none yet — |` (`SCORECARD.md:461-467`). A heading is not a nudge; `round51/c3-count.py` (which does read those tables) is not cited | **NO** |
| CT-20261020-3 | second non-author verifier for SOURCES.md: re-open rows, check the quote verbatim | `tools/quote-reopen.py:2,8,20-21` reads `corpus/SOURCES.md` (`:51`), fetches each registry URL, prints `VERBATIM`/`ABSENT` | YES (unrunnable today: L0 `8d77e6c1`) |
| CT-20261020-4 | track the round-25 debt queue to closure; name which of nine debts close; flag restatement (criterion 9) | same `round25-ledger-recount.py`: prints only `queue_committed`/`queue_true`; no nine-debt list, no criterion-9 scan | **NO** |
| CT-20261020-5 | recheck calendar: flag rows as they come due | pointer is the design note `corpus/knowledge/recheck-due-r26.md`; the flag itself is `tools/research-gate.sh:3708` `emit_finding META_RECHECK_OVERDUE` | **NO** (pointer ≠ implementation) |
| CT-20261021-2 | run QUALITY 15 myself read-only: gate blob at reported revision vs pinned digest | `corpus/lessons/round-27-verifier-spotcheck.md:30` records one comparison ("gate bytes equal measured `4f484194` … SHA256 `ac1315dd…`") made by the verifier; no repeatable tool | **NO** (single record) |
| CT-20261026-3 | report where lane and verifier disagree | `corpus/evidence/round52/verdict-gap.py` parses both axis tables, prints per-axis gaps + `VERDICT_GAPS/UNPARSED` | YES |

Rows whose pointer exists but does not implement the proposal: **CT-20261019-1, CT-20261019-3,
CT-20261020-4, CT-20261020-5, CT-20261021-2** (5/8); **CT-20261019-2** is partial (ledger recount yes,
the named `A-r9.md:50` finding and the 27-item queue no — the tool prints 24/25, not 27). Two of eight
implement (CT-20261020-3, CT-20261026-3).

## 5. The class, not the sample

9 of 24 IMPL rows point at a document heading or a criterion line, never at runnable code
(`SCORECARD.md::^## Capabilities`; `corpus/QUALITY.md::^9`, `::^8`, `::^18`, `::^23`, `::^60`, `::^44`,
`::^61`, `::^68`). The checker accepts such a pointer whenever `re.search` matches; nothing establishes
that the criterion is enforced. Consequence: `IMPL=24` is the ledger author's assertion, not a
measurement, and the tally the lesson cites as uptake cannot distinguish "a check exists" from
"a rule is written". Two rows also show a mis-cite inside this class: round40/c1-count.py is the
QUALITY-68 receipt re-verification check (`corpus/QUALITY.md:664-676` names it), so it is the right
pointer for CT-20261024-4 and the wrong one for CT-20261019-1.

## 6. Lesson claim, narrowed

`corpus/lessons/round-54.md:67` states "a dropped row, a dead pointer, a stale regex or a new unledgered
bullet each exit 1 (seat receipts)". All four reproduce (§2). But "a new unledgered bullet" holds only
for a `- ` bullet in a `2026-*.md` file; §3.1/§3.2 show a 2027 file and a `*` bullet both exit 0. The
sentence over-states the guard's domain; the guard itself is not wrong.

## 7. Risks / limits

- The ledger's IMPL semantics are unverifiable by its own checker — this is a height limit of the
  checker, not a defect in the frozen C1/C2 counters (both independently attested by sibling seats).
- `considerthese/` is untouched by the ledger (ids assigned lane-side), so ids are stable only until
  the next edit to those files; an inserted bullet is caught, a swap or a re-text is not.
- No blocker: every check above ran on committed bytes at the tip. Scratch removed.

VERDICT — attacked the considerthese ledger's checker with five required mutants plus three structural
probes and audited 8 IMPL rows by hand: the checker survived the five required mutants (all exit 1 with
the declared FAIL line) but **failed** the entailment attack — 5/8 audited IMPL pointers exist without
implementing their proposal, 9/24 IMPL rows are prose pointers, and a 2027 file, a `*` bullet, or a
swapped/re-texted bullet all leave `BAD=0`.
