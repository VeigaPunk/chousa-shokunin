# Round 62 verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Dispatch digest (`.ufo/watchdog.log`, mutable): `2026-10-28T20:13:09-03:00 launch chousa round=62 pgid=2003641 driver=hyaku-inline attempt=1`; `2026-10-28T21:30:33-03:00 complete chousa round=62; hyaku-inline attempt=1`. Lane HEAD before `8607de84723d5ff9bbcbe71eedebd6a0d30bfd87`, after `a7d0f8ae90988e3a69dd5aeab237acc3ee84b321`.

## Conformance (step 1)

- Report `.ufo/reports/round-62/chousa.md` committed by the lane identity: `git log --format='%an %H' -- .ufo/reports/round-62/chousa.md` → `chousa-shokunin eefe8ed64ab8b706ae3a4d722059f1d8df9c403b`.
- `## SHONEN` heading present, four lines (`[~]` ×4) for the four boxes of `SHONEN.md` (`grep -c '^- \[' SHONEN.md` → 4); no `[x]`.
- Cited lane commits `388d1535`, `d173d144`, `c4c11e9d`, `85ef0b44`, `dc95f03c`, `9530ebbe`, `a7d0f8ae` (and base `8607de84`): each `git -C chousa-shokunin merge-base --is-ancestor <hash> master` → exit 0.
- `scripts/hyaku/jj-lane.sh state chousa-shokunin` → `local=a7d0f8ae… remote=a7d0f8ae… ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` in the lane printed nothing.
- Prompt `.ufo/prompts/chousa-round-62.md` (689 lines) carries the template contract: `SHONEN` ×4, `Sources & frontier` ×5, `Trend verdict` ×4, hash-citation, lands-last and write-scope clauses all present by `grep -ci`.
- Report carries a Sources & frontier section and three trend verdicts. Wave: `.ufo/waves/round-62/w1-results.json` → `seats: 66`, `results` list length 66; `ls w1/*.md | wc -l` → 66.
- Status: `ok` (real report, real committed work).
- Defects (status-neutral): (a) the frozen claims file carried 14 statements its own files contradict (lane-disclosed, `claims-erratum.md`); (b) the lane disclosed using a Python one-liner for five file edits where the edit tool was required; (c) the C2 counter's default fleet-root resolution is the lane's parent `scripts/` — run from a bare `git archive` export it exits 2 (`c2v2-count: no census script`); it needs the `--fleet` flag or a fleet-shaped layout (a usage note for "executable without oral context"); (d) the report's lines are very long (truncated at 768 bytes in some reads) — readable but dense.

## Claims — re-checks

All commands ran from a scratch `git archive a7d0f8ae…` export (counters read the committed bytes; nothing written in the lane).

**C1 — operability (re-measured by me).** Frozen bytes unchanged since the freeze: `git diff --stat 388d1535…a7d0f8ae -- corpus/evidence/round62/c1v2-count.py corpus/evidence/round62/c1v2-battery.py corpus/evidence/round62/c2v2-count.py tools/build-spans.py` → empty.
- Before: `python3 -B corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round61/c1-count.py --work w1` → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL`, exit 1 (reported identically; committed `controls/c1v2-before.txt`).
- After: same battery, `--counter corpus/evidence/round62/c1v2-count.py` → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`, exit 0 (matches `c1v2-measure-after.txt` and `c1v2-measure-head.txt`; F12, noted as a race, was rejected in my run).
- Committed gate evidence verified, not executed: `controls/null-counters.txt` (null-fail and null-hashlist `BATTERY=FAIL`; null-pass likewise per the lane), `controls/c1v2-controls.txt` ends `CONTROLS_UNEXPECTED=0`, battery and counter frozen at `388d1535`.
- Verdict: **improved** on the frozen predicate (0/12 → 12/12, reproduced). Limits are the lane's own and accepted as honestly disclosed: the v2 counter is still forgeable by detection of its own PID-namespace sandbox, the battery hands the counter the subject path, and the forgers were written by the counter's author (non-author wave seats found further forger classes, routed). The numeric 3/10 is not claimed moved.

**C2 — coverage, sourced (re-measured by me).**
- Before: `git grep -l openat2 8607de84 -- corpus/knowledge | wc -l` → 0; SOURCES rows at base `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 137. After at `a7d0f8ae`: `git grep -l openat2 a7d0f8ae -- corpus/knowledge` → `corpus/knowledge/openat2-resolve-r62.md`; rows → 141. Committed before-receipt `controls/c2v2-before.txt` → `C2=FAIL` exit 1 (rows S138–S140 absent).
- After: `python3 -B corpus/evidence/round62/c2v2-count.py` (in a fleet-shaped scratch layout) → `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=16/16 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS`, exit 0 (identical to `c2v2-measure-after.txt`).
- Evidence-verified only: `controls/c2v2-controls.txt` → `C2V2_CONTROLS_UNEXPECTED=0`; `research-gate-selftest.txt` → `RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)`, exit 0 (not re-run: lane-owned gate).
- Entailment (the counter is structural, per the lane): I re-read the entry's claims against the located quotes; Q1–Q4, Q5, Q8–Q11 re-found in the rendered page/header (see spot-check), Claim 5 correctly states the page note and defers the glibc fact to Limits (`nm -D /usr/lib/libc.so.6 | grep -i openat2` → `0000000000112aa0 W openat2@@GLIBC_2.43`, as the Limits say). Verdict: **improved**.

**No owned axis harmed.** `git diff 8607de84 a7d0f8ae -- SCORECARD.md` is append-only (+26 lines: the round-62 verdict block and planned r63; no numeric row or capability row changed; the numeric operability stays 3/10). Spot reads: `SKILL.md` +3 lines, `corpus/QUALITY.md` +10 (criteria 124–127), `corpus/SOURCES.md` +6/−1 (the one deleted line is the rewritten `openat2(2)` lead bullet), `corpus/knowledge/` +1 entry, nothing else in `knowledge/` touched.

## Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| operability | **improved** | C1 battery 0/12 → 12/12 re-run by me; limits disclosed |
| coverage | **improved** | openat2 entry absent at base (0 hits) → present, `C2=PASS` re-run by me |
| depth | unchanged | no existing entry deepened |
| calibration | unchanged | 14-statement erratum is a defect but was disclosed and corrected; no verdict rests on them |
| freshness | unchanged | local files only, no fetch |
| adjacency | unchanged | battery shape contested with tameshi, routed not absorbed |

## Discernment spot-check (LEARNING.md)

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → five `W04` duplicate-url warnings (S051, S053, S073, S074, S075; pre-existing, none new) then `chousa ok …/corpus/SOURCES.md`, exit 0.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S138 openat2(2) man page, Q4 | admit (A) | `zcat /usr/share/man/man2/openat2.2.gz \| grep -m1 '^.TH'` → `.TH openat2 2 2026-07-02 "Linux man-pages 6.19"`; `pacman -Q man-pages` → `6.19-1`; render `MANWIDTH=1000 man -l … \| col -bx` line 86: "…differs from the effect of the O_NOFOLLOW file creation flag (in how.flags), which affects the handling of symbolic links only in the final component of path"; raw source `sed -n '335,341p'` contains the same sentence | **agree** | the page contrasts all-components (NO_SYMLINKS) with final-component-only (O_NOFOLLOW) exactly as the row's `teaches`; page date 2026-07-02 matches the corrected row; Q1, Q2, Q9 and Q10 (wrapper note, render line 18) also re-found |
| S139 linux/openat2.h | admit (A, scope narrowed) | `/usr/include/linux/openat2.h` lines 37–38; `pacman -Q linux-api-headers` → `7.2-1`; `grep -n OEXT` → only line 38 | **agree** | quote is verbatim, ≤25 words; the comment names `OEXT_NO_MAGICLINKS`, which the header never defines — tier A for the values and words, not behaviour, is the right scope |
| S140 probe output | admit (B, own-work) | `corpus/evidence/round62/openat2-probe.txt` line 7: `PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok` | **agree** | quote located; B tier fits because `expected=` values are author-typed (the entry's Limits say so and rest the claims on `observed=`) |
| S141 candidate probe docstring | reject (C) | `corpus/evidence/round62/controls/candidate-openat2-probe.py` lines 7–8 (quote, 17 words, located); `MANWIDTH=1000 man -l … \| col -bx \| grep -c 'os.open\|Python'` → `0`; typed `expected` args at P01 (`False`), P02 (`"opened"`), P03 (`"ELOOP"`), P11 (`"outside"`) | **agree** | a docstring states intent, not evidence; the page has no text on `os.open`/Python so "the page states or implies" overstates, and the expectations are typed constants — rejection with a stated flip condition is sound |

Newly written SOURCES row re-opened: S141 (quote, 17 words ≤ 25, located at lines 7–8) and S139 (locator header lines 37–38 verified); S138 row's "SYNOPSIS note … glibc provides no wrapper" re-found at render line 18.

## Trend verdicts

- **expansion — improved.** One admitted entry on ground `corpus/knowledge` did not hold (0 openat2 hits at base), citing three rows opened this round (S138–S140), 16 located quotes, `C2=PASS` re-run.
- **quality — improved.** The round-61 counter (0/12 on the forger battery, re-run) is superseded by one measured 12/12; the entry's claims were rewritten before landing; the glibc fact in the entry's Limits is confirmed on this host; no admitted entry found false.
- **discernment — improved.** This outside check agrees with the gate on all three admits and the one reject (table above), and the lane's own wave disagreements became QUALITY 124–127 with lesson rows and red-before receipts (the round-62 `## Mistakes`).

## Routed to the lane (next round)

1. State in the C2 counter's usage (or default) the fleet-root assumption; a bare export exits 2.
2. Carry the lane's own routed list forward (v3 counter: pid shim or no-namespace profile, randomised subject path, rows for the accepted forgers, battery control gaps M09/M13/M17/M18, stable X02/F12); a non-author forger author for the next battery, since this round's twelve were the counter's author's.
3. Give the 14-statement class a checker or a pre-freeze claims-vs-files read (lesson Mistake 2 says none exists).
4. Use the edit tool, not shell one-liners, for edits (lane's own process note).
5. SHONEN: box 2 (end-to-end task, LOG `## Round 62`) and box 3 (executable without oral context: both counters reproduced from a clean export by me, modulo defect (c)) look checkable by a non-author; promotion stays operator-owned and nothing was written to `SHONEN.md`.
