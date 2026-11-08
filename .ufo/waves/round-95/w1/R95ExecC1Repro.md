# R95ExecC1Repro — C1 clean-tree reproduction + independent re-derivation (round 95)

Seat: R95ExecC1Repro. Tree: carrier C `d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1`
(F `d6429e02bb4807bdb4cc26cd35f62f3c5c5dc7d2` plus the five scored receipts).
Clone: `/fast/scratch/hyaku/chousa-r95/R95ExecC1Repro/repo` (shared clone, checkout C).
Base for re-derivation: `7b2373586fb70f0ead6446c671fcc8b546d3e687`, materialised
read-only with `git archive <base> corpus/captures | tar -x -C $S/base` (90 captures).
Tooling: nothing installed; used system python3 and GNU grep 3.12
(`/usr/bin/grep --version` → `grep (GNU grep) 3.12-modified`).

## (a) Both C1 counting commands from `$S/repo`

Commands (from claims.md C1 predicate):

- `python3 -B tools/search-rerun.py verify corpus/fixtures/search-rerun-r95.md --root .`
- `python3 -B corpus/evidence/round95/rerun-controls-r95.py --root . --work $S/work`

Receipts:
- verify stdout+exit → `.ufo/waves/round-95/w1/R95ExecC1Repro-c1-verify.txt`
- controls stdout+exit → `.ufo/waves/round-95/w1/R95ExecC1Repro-c1-controls.txt`

Observed verify (verbatim, exit 0):

```
SEARCH_RERUN Q1 rev=MATCH tree=CHANGED recorded=7 at_rev=7 at_tree=8 TREE_CHANGED
SEARCH_RERUN Q2 rev=MATCH tree=CHANGED recorded=2 at_rev=2 at_tree=3 TREE_CHANGED
SEARCH_RERUN Q3 rev=MATCH tree=CHANGED recorded=3 at_rev=3 at_tree=4 TREE_CHANGED
SEARCH_RERUN Q4 rev=MATCH tree=SAME recorded=1 at_rev=1 at_tree=1
SEARCH_RERUN Q5 rev=MATCH tree=SAME recorded=14 at_rev=14 at_tree=14
SEARCH_RERUN Q6 rev=MATCH tree=CHANGED recorded=1 at_rev=1 at_tree=2 TREE_CHANGED
SEARCH_RERUN Q7 rev=MATCH tree=SAME recorded=0 at_rev=0 at_tree=0
SEARCH_RERUN Q8 rev=MATCH tree=CHANGED recorded=1 at_rev=1 at_tree=2 TREE_CHANGED
SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=3/8 findings=0
SEARCH_RERUN: CLEAN
exit:0
```

Verdict lines: `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8` and
`SEARCH_RERUN: CLEAN` — both present, byte-equal to the corresponding lines in
`corpus/evidence/round95/after/c1-verify.txt` (diff VERIFY_SAME). The after-receipt's
header says `computed_against F=... tree_equals_F_for_measured_paths=yes`; the only
F→C delta is the five receipts + `measure-r95.sh` (`git diff F C --stat`), which do
not touch `tools/search-rerun.py`, the fixture, or the capture store, so the equality
claim is consistent.

Observed controls tail (verbatim, exit 0, wall 29s — see (d)):

```
POSITIVE=1/1 STRICT_TREE=1/1 FORGERY_REFUSED=8/8 PRIOR_ACCEPTED=8/8 SETUP_REFUSED=12/12 CLONE_TREE=2/2 DO_NOTHING_REFUSED=1/1 ORACLES_REJECTED=3/3
RERUN_CONTROLS=PASS
exit:0
```

Verdict lines: both present, byte-equal to `corpus/evidence/round95/after/c1-controls.txt`
(diff CONTROLS_SAME), including every CASE line (`positive`, `strict-tree`, 8 forgeries
each with a `prior-*` research-gate acceptance, 12 setup refusals, `clone-edit`,
`clone-symlink`, `do-nothing-base`, 3 oracles all `ok`).

Note on interpretation (not a falsification): the verify run at C reports
`tree_same=3/8` — five searches show `TREE_CHANGED` because the S222 capture
`corpus/captures/1a8c36c4c24444967bd9c3ce.txt` (added after base) contains `PRISMA-S`,
`exactly as run`, `deduplicat`, the Q6 regex and the Q8 regex. I confirmed this by
running the same greps on the carrier tree: Q1 at_tree=8 vs at_rev=7, the eighth file
being the S222 capture. The claims sentence correctly separates rev-match (exit 0)
from tree change (exit 0 unless `--strict`), so `CLEAN` with `TREE_CHANGED` lines is
the stated behaviour, not a drift of the record.

## (b) Independent re-derivation of the 8-row record

Method: in `$S/base` (base-revision captures only), for each row I ran GNU grep myself:
`/usr/bin/grep -l -F -e '<expr>' corpus/captures/*.txt | LC_ALL=C sort` for fixed,
`/usr/bin/grep -l -P -e '<expr>' corpus/captures/*.txt | LC_ALL=C sort` for regex,
then `wc -l` and `sha256sum` of the sorted list. Receipt:
`.ufo/waves/round-95/w1/R95ExecC1Repro-derive.txt` (script + output).

Row-by-row, recorded vs mine (all 8 agree; Q1/Q5 recorded as digests, verified by sha256):

| id | engine | expression | recorded hits | mine hits | recorded hit_set | mine sha256 |
|---|---|---|---|---|---|---|
| Q1 | fixed | `PRISMA-S` | 7 | 7 | sha256:69cfc059…00dc1 | 69cfc05988a6ea78b149d8027c0c0405171429c1aff812090b6aed4da1a00dc1 ✓ |
| Q2 | fixed | `exactly as run` | 2 | 2 | c52a1f15…, c9d1e74c… | list identical ✓ |
| Q3 | fixed | `deduplicat` | 3 | 3 | 0ae65ac0…, c52a1f15…, f2489455… | list identical ✓ |
| Q4 | fixed | `検索者` | 1 | 1 | 62be15a4… | list identical ✓ |
| Q5 | fixed | `检索` | 14 | 14 | sha256:df36eb98…94878bd | df36eb9846e2017f68ca2d0ce5c5fff09ee332edca5394c89218fb40794878bd ✓ |
| Q6 | regex | `[Ss]earch(es)? (was|were) (run|conducted)` | 1 | 1 | c52a1f15… | list identical ✓ |
| Q7 | fixed | `Client Challenge` | 0 | 0 | - | empty ✓ |
| Q8 | regex | `last search(ed)?` | 1 | 1 | a640b15a… | list identical ✓ |

The record's hits, hit sets and both digests are exactly what GNU grep 3.12 finds on
the base-revision capture store. (My first ad-hoc pipeline mis-counted due to
`$(...)` word-splitting on multibyte paths; the file-based derivation above supersedes
it and is the one in the receipt.)

## (c) New 3-search record, recorded with GNU grep, tool agrees

I wrote my own record (`.ufo/waves/round-95/w1/R95ExecC1Repro-new-record.md`) with
3 NEW searches over `corpus/captures/*.txt` at base, all recorded by running
`/usr/bin/grep -l -F|-P … | LC_ALL=C sort` in `$S/base` first:

- Q1 fixed `cochr` → 10 hits, explicit file list
- Q2 regex `systematic (review|reviews)` (filed as `systematic (review\|reviews)`) →
  22 hits, `sha256:4a0aa4d09446e72136aeeecb30eecf724974f7f597197db922467d7a4a5554aa`
- Q3 fixed `ZXQNONEXISTENTPHRASE-9876` → 0 hits, hit_set `-`

Tool run `python3 -B tools/search-rerun.py verify $S/new-record.md --root .` from
`$S/repo` (verbatim, exit 0):

```
SEARCH_RERUN Q1 rev=MATCH tree=CHANGED recorded=10 at_rev=10 at_tree=11 TREE_CHANGED
SEARCH_RERUN Q2 rev=MATCH tree=CHANGED recorded=22 at_rev=22 at_tree=23 TREE_CHANGED
SEARCH_RERUN Q3 rev=MATCH tree=SAME recorded=0 at_rev=0 at_tree=0
SEARCH_RERUN_SUMMARY searches=3 rev_match=3/3 tree_same=1/3 findings=0
SEARCH_RERUN: CLEAN
exit:0
```

The tool agrees with my independently recorded counts and digests on all three,
including: the `|`-containing regex (the `\|` markdown escaping round-trips through
`cells()` and `re.compile`), a zero-hit row, and a hit_set given as an explicit
comma-joined list rather than a digest. At-tree counts are rev+1 for Q1/Q2 because
the S222 capture also contains `cochr` and `systematic review(s)` — again the stated
`TREE_CHANGED` behaviour.

Deliberately NOT probed (out of assigned PLA scope, would touch production files):
symlink/untracked tree-walk behaviour, socket/write audit, rev-blind mutants — those
are exercised by the battery in (a), which passed unchanged.

## (d) Timing

- One verify run on the committed 8-search record: `real 0m0.519s` (user 0.525s).
- Full controls battery (a): wall 29s (user 45s, sys 16s) — dominated by its 8
  forgery + 3 oracle sub-runs, not by a single verify.

## Findings

No falsification found in C1 as stated. The predicate lines reproduce byte-equal at
C; the 8-row record re-derives exactly under GNU grep at base; 3 new searches (fixed,
regex-with-`|`, zero-hit) re-run clean. The two claims-sentences' named limits hold
on the evidence: Python `re` vs GNU `-P` agreement is demonstrated on the 2 regexes
(Q6, Q8) plus my Q2 `systematic (review|reviews)`, per-line matching is the tool's
implementation, and `TREE_CHANGED` is reported separately from rev drift. No kill
rule triggers: no forgery accepted, no write/socket/outside-root read observed in
the passing battery, no constant stand-in passes.

VERDICT: R95ExecC1Repro C1 held — verify and battery verdict lines byte-equal the after receipts, the 8-row record re-derives exactly under GNU grep at base, and 3 new fixed/regex/zero-hit searches re-run CLEAN.
