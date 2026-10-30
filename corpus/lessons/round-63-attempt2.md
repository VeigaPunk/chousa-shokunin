# Round 63 attempt 2 — the wave's falsifier class closed in a v2 battery; a claims-audit checker for the erratum class; no wave dispatched (2026-10-30)

Re-dispatch of steered round 63 after the run-11 wrap-up released attempt 1 without a closure (attempt 1's
lesson is `corpus/lessons/round-63.md`; its claims, verdicts and instruments stand). Base
`4ece131ca826c646bd28a50802d41bc78d8a9717`; claims froze in `corpus/evidence/round63/claims-a2.md`. **No wave:
the orchestrator paused new campaign dispatches on 2026-10-30 (provider failures — "minimax plan exhaustion,
Cursor pricing, Anthropic 429, ZAI 429 and Devin permission denial"; "Do not request new waves/replacement
seats just to retry these failures"; "New campaign dispatches paused pending provider availability"), so no
`.ready` was written and the round's L2 floor is unmet, reported as such.** Every verdict below rests on the
frozen counters, the committed controls and receipts named in `claims-a2.md`.

## Gate

Access date for every row: 2026-10-30. Local files only — the installed pages of Arch packages (grep 3.12-2,
git 2.56.0-1, file 5.48-1, `pacman -Qo`); no URL fetched. Render: `MANWIDTH=1000 man -l FILE | col -bx`.

- **S146 — ADMIT (A).** `/usr/share/man/man1/grep.1.gz`, page header "GNU grep 3.12-modified". Rendered
  line 29, the `-F` option: "Interpret PATTERNS as fixed strings, not regular expressions." Scope: fixed-string
  occurrence semantics for the verbatim-heading class.
- **S147 — ADMIT (A).** `/usr/share/man/man1/git-log.1.gz`, `.TH` date 2026-09-27 (git 2.56.0-1). Rendered
  line 1376, `--diff-filter`: "Select only files that are Added (A), Copied (C), Deleted (D), Modified (M)…".
  Scope: first-add-commit reads for the git-first-commit class.
- **S148 — ADMIT (B, own-work).** `corpus/evidence/round63/audit-probe.txt`, line `PROBE_FACTS=11/11`
  (committed output of `audit-probe.py`; expected values typed by the author, observed fields carry the
  evidence). Scope: the seven rule classes' behavior on fixtures.
- **S149 — REJECT (A page, no claim rests on it).** `/usr/share/man/man1/file.1.gz` (file 5.48-1), NAME line:
  "file — determine file type". Opened to check whether the file-kind class should classify by magic content;
  refused because the classes classify by suffix and no round claim rests on magic detection. Flip: a rule
  class that must discriminate file content beyond the suffix.
- **Old → new changes to existing rows:** none (S146–S149 are new; no `status`, `recheck` or `used-by` cell of
  an older row changed).
- Spot-check for the non-author closure (LEARNING.md): re-open admit S147 (Q: rendered line 1376, `--diff-filter`
  letters) and reject S149.

Assimilation: none. The wave-4 quarantine duty was discharged in round 42 (24-row slice verdicted,
`corpus/evidence/round42/quarantine-verdicts.tsv`, zero rows present), so package adoption stays closed; this
round re-derived the slice registry and ran the id-collision check: **64 of the staged package's 114 staged
ids already sit in the lane registry** (`.ufo/waves/round-63/assimilation/{reg-ids,staged-ids,collisions}` —
reg 145 rows, staged 114, collisions 64). That mass drift is a second, independent reason adoption stays
closed; any future adoption must renumber staged ids by document in scratch.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
start `.ufo/waves/round-63/census-start-a2.txt` exit 0; end `census-end-a2.txt` exit 0 (`chousa ok`; the same
five pre-existing W04 duplicate-url warnings, none new). Rows 145 → 149 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`);
tiers A/B/C 113/25/7 → 116/26/7; status mined/queued/rejected 118/19/8 → 121/19/9.

## Mistakes

| # | class · what | evidence | captured-by | fix, and whether shown able to fail |
|---|---|---|---|---|
| 1 | **a rule written from the sample at hand, again** — the v2 judge's first gate regex checked that a GATE line's name is *a* contract name, not *the line's id's* name, so the wrong-name exhibit (E03) still passed the hardened battery once | `exhibit-v2-after.txt` first run: `LEG E03-wrong-name [D06] rc=0 LEG D06 defect ok ok`; after the pair fix: `LEG E03-wrong-name … FAIL 1 non-contract lines on stdout` | none — the v1 battery had the same shape of hole (its regex ignores the name entirely) and the fix reproduced it at one remove | the regex now matches the id+name pair (`G01 census|G02 knowledge-index|…`); red-before is the first v2 receipt run (E03 accepted), red-after the second (rejected); a rule that reads a vocabulary must bind each token to its own key, not to set membership |
| 2 | **standalone-token rules that tokens inside words defeat** — the first `json-count` match read the `2` inside `v2` as a named count on a minimal fixture, so a 2-item spec "passed" a 64-seat claim shape | scratch fixture during probe bring-up: `FLAGGED=0/1 AUDIT=PASS` with true count 2 and claim 64; after the `(?<![\w.)])\d+(?![\w])` fix the same fixture fires | the selftest's good case (both fixtures used 64/66, which never collide with `v2`) — a counter tested only on its demonstration instances misses the collision class | the regex requires a standalone token; the probe's P01 fixture now uses a 2-item spec so the collision class is exercised; red-before kept in the probe bring-up note (this row) |
| 3 | **a generator's lane-root offset, twice** — two new scripts derived the lane root from `Path(__file__).parents[2]` while living one directory deeper than their model (the frozen battery), so `landed-tool` runs measured an absent tool and the probe called a missing checker | first `exhibit-v1-before.txt`: `FULL landed-tool rc=1 CLEAN=0/1 DEFECTS=0/15` with no failing LEG line (the absent-tool print); probe run one: all MISMATCH with a missing-file traceback path under `corpus/tools/` | none — a copied harness line is only wrong one directory away from its source | both fixed to `parents[3]`; the receipts were regenerated after the fix (`exhibit-v1-before.txt` seed `exhv1c`); a path derived from `__file__` needs an existence assert on the file it is meant to name — not yet a checker, routed |
| 4 | **a receipt quoting the pipe's exit, not the command's** — the first null and landing receipts piped the battery through `tail`, so their `rc=` lines recorded tail's status and a `BATTERY=FAIL` tool read `rc=0` | first `c1v2-nulls-v2.txt` (superseded, not committed): `BATTERY=FAIL` with `rc=0 tool=null-pass` | the battery's own verdict line is the pinned value, so the wrong rc was cosmetic — but a reader re-deriving "exit 1" from the receipt would have been misled | receipts regenerated with `PIPESTATUS` capture: `rc=1` for both nulls, `rc=0` for the three landing runs (`c1v2-nulls-v2.txt`, `c1v2-landed-runs.txt`); rule: a receipt that prints an exit code captures it from the command, never from a pipeline stage |

## What the round did about the routed items

- Taken: the zero-gate leg (Z01–Z03), the six judge holes (strict judge), the path-keyed forger (E08 +
  harness variation + keyword-free plants), the oracle-breaking legs (D16/D17), the G04/G05 false positives
  (B07/B08 benign legs + the landed tool's amended rules, verified on the three sibling roots the finding
  named: kagi `caught=18/18`, kake brace shorthand, and the G04 fixture shapes — each reads PASS after the
  fix), and the round-62 spot-check's item 3 (the claims-audit checker + the pre-freeze audit of this round's
  own claims file, `audit-a2-result.txt` `FLAGGED=0/4`).
- Not taken, with reasons: round-62 routed item 2's full v3 line for the round-62 counter (pid shim,
  randomised subject path) — superseded by the fact that the v2 battery's discrimination target is the
  attempt-1 exhibit set, and one more counter generation without a wave's non-author attack would only add
  unattacked surface; `CritC1Semantics.md` (4 of 15 real past defects the preflight would catch) — relevance
  work, no instrument change claimed; `RevG02.md`'s ten gate defects — routed to the next battery round;
  the G01 `--root`-relative fleet default — a UX default, no defect demonstrated on a real run.
- Attack items the paused wave would have carried, routed to the next round: a non-author re-run of every
  counting command; a mutation pass on `c1-battery-v2.py` and `claims-audit.py`; a re-open of S146–S149; an
  entailment read of `self-claim-audit-r63.md`; the non-author spot-check named in the Gate; a non-author
  review of the C2 entry's claims; a forger author external to the battery author for the v2 exhibit set.

## Trends

- **expansion — improved (narrowly).** One admitted entry on ground `corpus/knowledge` did not hold
  (`grep -rl 'claims-audit' corpus/knowledge` printed nothing at the base), citing three rows opened this
  round; one capability-adjacent instrument (the checker) registered in SKILL.md's gate table.
- **quality — improved (narrowly).** The G04/G05 rules that false-positived on real sibling files are fixed
  and pinned by benign legs; the attempt-1 battery's demonstrated acceptance of the falsifier class is
  closed by a measured v2 (9/9 exhibits rejected, honest controls kept); no admitted entry was found false.
- **discernment — unchanged**, pending the non-author spot-check named in the Gate (S147 admit, S149 reject)
  and the entry's entailment read; the wave that would have attacked these claims was not dispatched.

## Routed to the next round

A non-author run of every counting command and the spot-check above; a mutation pass on the v2 battery and
the checker (the L1-authored instruments have had no external attack this round); the round-62 v3-counter
line if the lane keeps the forger-armory thread; `RevG02.md`'s ten gate defects; an existence-assert rule for
`__file__`-derived paths (mistake 3); `CT-20261019-4` (the size-watch threshold) stays with the operator.
