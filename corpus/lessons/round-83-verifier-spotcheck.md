# chousa round 83 — verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Closed 2026-11-06. Report `.ufo/reports/round-83/chousa.md` (fleet repo). Lane HEAD before `a46534a51756f7e7d9bb55dd9a275156d908d84c`,
after `49bc8778560cd88773335bdb12ebc15178cb6231`. Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-06T17:50:30-03:00 launch chousa round=83 pgid=33320 driver=hyaku-inline attempt=1`;
`2026-11-06T18:32:14-03:00 complete chousa round=83; hyaku-inline attempt=1`.

Verdict: **status ok, not admitted (`rejected-honest-stop`)**. C1 depth verifies on closure's own re-run; C2
operability is falsified by its own frozen kill rules K2 and K3, and the closure agrees with the stop after a static read
of the landed tool.

## Step-1 conformance

| check | command | observed | result |
|---|---|---|---|
| report committed by lane identity | `git log --format='%an %H %ci' -- .ufo/reports/round-83/chousa.md` | `chousa-shokunin 09b54078… 2026-11-06 18:31:47 -0300` (after lane tip 18:31:02, before the 18:32:14 complete line) | pass |
| prompt committed | same over `.ufo/prompts/chousa-round-83.md` | `chousa-shokunin 085abd1c 17:50:28-03:00`; §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract (path, SHONEN, hash citation), §5 commit/push scope/L0, §6 hyaku addendum | pass |
| `## SHONEN` heading, one line per box | report lines 93–98; `git show 49bc8778:SHONEN.md \| grep -c '^- \['` → 4 | 4 lines, all `[~]` | pass |
| cited commits exist and are ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for a46534a5, 8fff80ee, 1b9b2ff8, 3fbf8d12, 81b81173, dd373b0c, aca2a781, c7d29e1c, 3269af9c, 566b9a95, 49bc8778 | 11/11 ok | pass |
| pushed, nothing uncommitted | `jj-lane.sh state …`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote = `49bc8778…` | pass |
| egress before fetch | `TZ=UTC git log -1 --date=iso-strict-local --format=%cd 8fff80ee`; `refetch.tsv:157-159` | 20:53:00Z < first fetch 20:53:06Z; three rows curl_rc 0, HTTP 200 | pass |
| all lane-round commits by the lane | `git log --format=%an a46534a5..49bc8778 \| sort \| uniq -c` | `10 chousa-shokunin` | pass |

Conformance defects: none found. The r82 routed defects 2 (revision-pinned receipts: `after/` and `repair/` carry
`# rev` headers) and 3 (`.md` count: report 94 → 95 equals `git ls-tree -r --name-only <rev> corpus/knowledge | grep -c '\.md$'`
at a46534a5 → 81b81173) are closed.

## Per-claim re-check

### C1 depth — re-measured by closure

Instrument pin: `sha256sum depth-r83.py` = `18716627…` at 1b9b2ff8, 3fbf8d12, 81b81173 and 49bc8778, equal to
`corpus/evidence/round83/instrument-pins.txt`. Command (frozen counter from the 3fbf8d12 archive, run against each archive
tree): `git archive <rev> | tar -x -C $S/<rev>; python3 -B $S/3fbf8d12/corpus/evidence/round83/depth-r83.py --root $S/<rev>`

| rev | observed |
|---|---|
| 1b9b2ff8 | `DEPTH_R83 entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0` / `DEPTH_R83=FAIL` rc 1 |
| 81b81173 | `ENTRY appraisal-judgment-records-r83.md ok=yes rows=10 quotes=16/16 fails=-` / `entries=1 ok_entries=1 rows=10 located_quotes=16 fresh_sources=3` / `PASS` rc 0 |
| 49bc8778 | identical to 81b81173, `PASS` rc 0 |

Matches report. K4 re-checked: `git grep -lE 'S009|S212|S213|chapter-07|chapter-08|assessing-risk-bias-included-studies' a46534a5 -- corpus/knowledge`
→ no file. K2 spot: the three Gate quotes FOUND in their captures (lines 494, 611, 544) and on live re-open (below). K3
rests on `R83ReviewerEntry`/`R83CriticClaims` (evidence-verified); the counter's limit (structure, not warrant) is stated
in `claims.md:45`. **Verified.**

### C2 operability — evidence-verified, plus static read (lane tool; not executed by closure)

`tools/gate-records.py` is the lane's own verifier and `gate-records-r83.py` drives it, so closure verified committed
evidence and read the bytes; it did not run either.

- Pin: `gate-records-r83.py` sha `a1d86a92…` at all four revisions = `instrument-pins.txt`.
- Before: `controls/receipts/c2-k0-donothing.txt` → `TOOL=absent POSITIVE=0/15 FORGED_REFUSED=0/198 … RC=0/3`, `FAIL`, rc 1.
  After: `after/c2-after.txt` (`# rev 81b81173…`) → `TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198 EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3`, `PASS`, rc 0. Controls `summary.tsv` 8/8 expected = observed. Matches report.
- **K3 fired — closure agrees.** `git show 81b81173:tools/gate-records.py` line 117: rev form `if not quote or
  quote.startswith('"'): return None` → `FAIL PARSE`; the docstring's rev form is `quote=<text to end of line>` with no
  such restriction, so a genuine rev record whose quoted line begins with `"` is refused. Repaired at c7d29e1c (guard gone).
- **K2 fired — closure agrees, with a note.** Line 76 `INT_RE = re.compile(r"0|[1-9]\d{0,6}")`; plain check
  `re.fullmatch(r"0|[1-9]\d{0,6}","2٢٢")` → `True` (Python `\d` is Unicode). Forge input
  `.ufo/waves/round-83/w1/R83ExecForge/forge/c052-line-arabic-222.md` printed `OK` per `R83ExecForge.md:42-43`. Whether a
  non-ASCII numeral "violates" the docstring's `line=<n>` is a reading the docstring left open; K3 alone kills C2.
- Repair c7d29e1c, evidence only: `repair/c2-counter-repaired.txt` (`# rev c7d29e1c…`) still `PASS`;
  `repair/firing-inputs-repaired.txt` Arabic-Indic record → `FAIL PARSE`. Post-scoring; does not rescue the claim.

**Falsified (honest stop).**

### No-harm check

`git diff a46534a5 49bc8778 -- SCORECARD.md`: append-only (+34, round-83 verdict + r84 plan). Non-evidence diff: LOG +20,
SKILL +1 (tool row), QUALITY +5, README +9, SOURCES +3/−1 (S009 row rewritten queued → mined; S212, S213 added), new
entry, lesson, tool. The only deleted line in the whole range is the superseded S009 row
(`git diff --numstat a46534a5 49bc8778 | awk '$2!=0'`). `PROVINCE.md` untouched. Census
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, only the five pre-existing W04
warnings (S051, S053, S073, S074, S075). Registry `grep -cE '^\| S[0-9]{3,} \|'`: 211 → 213. No axis harmed.

## Per-axis verdicts

| axis | verdict | basis |
|---|---|---|
| depth | improved | C1 re-measured FAIL → PASS (10 rows, 16/16 located quotes, 3 fresh sources); K4 held on closure grep |
| operability | unprovable-but-better | claim falsified (K3 by static read, K2 agreed); the tool exists, refuses 198/198 frozen forgeries and is repaired post-scoring, but no frozen predicate scores the repaired tool and the counter has a whitelist forger (`R83CriticClaims` §1.2) |
| calibration | unchanged | QUALITY 164–165 (mined mistakes); no calibration measurement |
| coverage | unchanged | PROVINCE untouched |
| freshness | unchanged | S009 queued → mined; no drift surface measured |
| adjacency | unchanged | `R83ConnectorSiblings.md`: no sibling holds this ground |

The lane's own SCORECARD calls operability "improved narrowly, claim falsified"; closure grades it
`unprovable-but-better` because no frozen predicate measured the change that survives.

## Discernment spot-check (lesson `## Gate`)

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S009 | admit | live MECIR C52–C60 page (HTTP 200) + capture ea16817c line 494 | agree | Gate quote (24 words) FOUND live and in capture; capture sha `3dfd10e5…` = `refetch.tsv:157` txt_sha256; the standard is the conduct rule the entry cites |
| Millard et al. sentence inside S212 | reject | live Handbook ch.7 (HTTP 200) + capture 708022d4 line 622 | agree | sentence FOUND live; it sits in the "Novel methods" paragraph reporting one study ("A study showed that about one-third…"), while the conduct standard is line 611; `grep -c -i millard` on the entry → 0 |
| S213 (new SOURCES row) | admit | live Handbook ch.8 (HTTP 200) + capture 963807d1 line 544 | agree | Gate quote (16 words, ≤25) FOUND live and in capture; sha `f5dae335…` = `refetch.tsv:159`; row's teaches cell paraphrases section 8.2 faithfully |
| S212 (new SOURCES row) | admit | live Handbook ch.7 + capture line 611 | agree | Gate quote (14 words) FOUND live and in capture; sha `3b57cb03…` = `refetch.tsv:158` |

## Trend verdicts

- **expansion: improved** — knowledge `.md` 94 → 95 (closure count), registry 211 → 213, S009 mined after queuing since
  round 1; K4 held.
- **quality: unprovable-but-better** — the verifier tool replaces a hand check and its two kill-firing defects are repaired
  with revision-pinned receipts, but post-scoring and with 15/36 mutation survivors and a whitelist forger on record.
- **discernment: improved** — C2 filed as an honest stop on the wave's findings; r82 routed defect 1 adjudicated with bytes
  (`R83ScoutNovelty` §2.5); all four sampled Gate decisions agreed on live re-open.

## Routed defects (lane fixes next round)

1. Docstring value grammar: state that numeric fields (`line`, `words`, `curl_rc`, `http`) are ASCII digits, so a future K2
   on numerals is unambiguous (the repair changed the code, not the documented form).
2. The r84 operability claim must score the repaired tool with a battery a whitelist cannot pass (fresh positives built
   from committed captures) and the nine lane-killable mutation survivors (`R83MutationTool` §4) as frozen kills.
3. Run `gate-records.py` on a `git archive` tree or document the dirty-worktree limit (`R83SentinelScope` R1); report a
   non-git `--repo` as a setup error, not a record failure (`R83ConnectorSiblings` R1).
4. Per-axis wording: a falsified claim's axis is not graded `improved` in SCORECARD; use `unprovable-but-better` or
   `unchanged` with the reason.

SHONEN: all four boxes `[~]`; operator note only — box 3 (`gate-records.py verify` on the lesson, `R83ExecRepro.md`) and
box 4 (`R83ConnectorSiblings.md`, `R83SentinelScope/sentinel.md` §2) look checkable by a non-author; promotion is
operator-owned.
