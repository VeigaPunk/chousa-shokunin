# R54W2ExecCensus — census and misroot attack (leaf, chousa round 54, wave 2)

Tip attacked `447cf7ed4dc1a3708518b99e9a5e62e177c11ce9`; the lane HEAD moved during the seat (`178667d` → `25abbe8`), but
`git rev-parse <rev>:corpus/SOURCES.md` = `8417d0d33a5ac88ff5bc51f64cf10db6f43224ce` at all three revs, so every number below
is the tip's. Scratch `/fast/scratch/hyaku/chousa-r54/R54W2ExecCensus/` removed at exit; nothing installed; the only non-scratch write is this report.

## 1. Maintained census — command, output, exit

```
$ bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
```

`--today` defaulted to `date -u +%F` = `2026-10-27`; `--today 2026-10-26` gives identical output (exit 0), so no E08
(future `opened`) exists. `census` mode: `chousa rows 123 · tier.A 104 · tier.B 14 · tier.C 5 · status.mined 99 ·
status.queued 19 · status.rejected 5`; `FLEET rows 3440` and the per-lane rows sum equals it (`lane_sum=3440
FLEET=3440 equal=1`).

## 2. Frozen CORPUS.md census awks (run from the lane root, as the contract requires)

| check | observed |
|---|---|
| `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` | `123` |
| malformed rows `NF!=13` | `0`; single NF value `NF=13 rows=123` |
| tier histogram | `A=104 B=14 C=5` (sum 123) |
| status histogram | `mined=99 queued=19 rejected=5` (sum 123) |
| duplicate ids (`sort \| uniq -d`) | *empty* |
| enum violations / tier inflation | *empty* |
| mined used-by paths that do not exist | *empty* |

No row-shaped line sits outside `## Registry` (section-tracked awk: no output). Ids are `S001`…`S123`, 123 distinct,
no gap (`checked 123 ids`, no GAP line).

## 3. Non-vacuity (a clean result is worth only what the check can fail)

`bash scripts/sources-census.sh selftest` → `96` `killed` lines, `0` `SURVIVED`, last line `selftest ok`, exit 0. Mutant
copies in scratch (lane files untouched) through `validate --file` fire `E12 S121 row outside Registry section` (row appended
after `## Paths`), and inside Registry `E03 S123 duplicate id` + `E06 S123 tier=Z` + `E11 S123 missing used-by
corpus/knowledge/absent-mutant.md`, exit 1; separately all 110 used-by entries are regular files (no `NOT-A-FILE`).

## 4. Round-54 delta and append-only compliance

`grep -c` rows: BASE `c49ffc6` = `120`, freeze `5a1a206` = `120`, tip = `123`. `diff <BASE>:corpus/SOURCES.md
corpus/SOURCES.md` → `added=3 removed=0`; added ids exactly `S121 S122 S123`. Fields: `S121 kind=docs tier=A
opened=2026-10-26 recheck=180d`, `S122` identical, `S123 kind=docs tier=B …`; all three `mined`, `used-by` =
`corpus/knowledge/source-type-taxonomy-r36.md` (S121, S122) and `…-r37.md` (S123), all targets present. No existing row
touched: `S101`'s `used-by` is `corpus/knowledge/citation-count-semantics-r37.md` at BASE and at tip, and r36/r37 carry
`source: S121 — https://std.samr.gov.cn/…`, `source: S122 — http://openstd.samr.gov.cn/…`, `source: S123 —
https://xuebaobangong.jmu.edu.cn/…` with no `S101` token at all (grep `'S[0-9]{3}'` over both files yields only
S121/S122/S123) — E3's cut holds.

## 5. First-source-cell URL uniqueness (the C2 "exactly one row" leg, census face)

Each theme URL occurs once in the whole registry (`grep -oE 'https?://[^ |]+' corpus/SOURCES.md | grep -E
'samr\.gov\.cn|jmu\.edu\.cn'` → `1` each); per-row URL count in the source cell is `S121 urls=1`, `S122 urls=1`,
`S123 urls=1`, and no other row carries them, so "the FIRST source-cell URL is the document's URL" resolves to one row
per document. The script emits no E04; the five W04 are pre-existing.

## 6. Reverse citation integrity (stronger than E11, which tests existence only)

All 110 used-by path entries / 99 mined rows name their row, with one pre-existing exception:
`NO-CITATION: tools/quarantine-check.py does not name S077`. S077's row is byte-unchanged BASE→tip (`diff`: empty) and
its paired lesson `corpus/lessons/round-42.md` names `S077` six times, so the row is cited — but a tool is neither a
knowledge entry nor a lesson under the contract's `used-by`. Pre-existing, not round-54, not mine to rewrite.

## 7. Misroot check (read-only; nothing moved or deleted)

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain -uall
?? .ufo/reports/round-45/kengaku.md
?? .ufo/waves/round-51/w2/T51W2Read14.md
```

| untracked path | chousa | `round-54` | `R54` | verdict |
|---|---|---|---|---|
| `.ufo/reports/round-45/kengaku.md` | `0` | `0` | `0` | kengaku round-45 report (mtime 23:47, sibling's live write) — not chousa round 54 |
| `.ufo/waves/round-51/w2/T51W2Read14.md` | `0` | `0` | `0` | tameshi round-51 seat report — not chousa round 54 |

No `round-54` dir under the fleet root's `.ufo/waves/` (round-54 waves live in the lane), and no untracked or ignored
fleet path carries chousa round-54 content. Fleet `.ufo/reports/round-54/` holds `kake, kotoba, kotodama, kumitate`
plus a **tracked** `chousa.md` (commit `86023b97`, ancestor of HEAD) whose census block ("Start: exit 0, five
pre-existing W04", "Rows: 120 → 123", "Added by tier: A S121, S122; B S123", "Rows touched old→new: none") matches
§1/§4 exactly. One tracked fleet file, `.scratch/goal-20261026-hyaku-run9.md`, showed ` M` on one snapshot and clean on
the next — a live sibling edit, left alone.

## 8. Misroot hazard in the census itself

The frozen used-by awk resolves paths against the cwd; the maintained script resolves them against the lane dir
(`[ ! -e "$dir/$path" ]`). From the fleet root the frozen awk prints **110** false `missing: corpus/…` lines; from the
lane root, **0** — so the block is valid only from the lane root, and neither receipt records the cwd for its
`grep -cE … corpus/SOURCES.md` line.

## 9. Receipt vs independent run

`diff <(sed -n '2,7p' corpus/evidence/round54/census-end.txt) <my validate stdout>` → identical; the receipt adds
`$ grep -cE … → 123`, which my run reproduces. Bounds: `census-end.txt` is absent at the assigned tip `447cf7e`
(`git cat-file -e 447cf7e:…` → fatal/ABSENT) and present from `25abbe8`. It carries 2 of the 7 CORPUS.md census
commands (validate + row count); the other five are run in §2 and are clean but sit in no receipt.

## Findings (none blocks C1/C2; all outside my write scope)

1. Census at the tip is clean: exit 0, `ok`, five pre-existing W04 only, the same set at BASE — round 54 added no warning.
2. Append-only held: `added=3 removed=0`, S121–S123 only, tiers A/A/B, all `mined`, `used-by` = r36/r36/r37, entries
   carry the matching `source:` lines, S101 untouched (E3).
3. Receipt gap: round-end receipt carries validate + row count, not the five integrity awks, and its row-count line is
   cwd-silent although the frozen used-by awk is cwd-dependent (110 false misses from the fleet root).
4. Pre-existing contract deviation: S077 `used-by` names `tools/quarantine-check.py`, which does not name S077.
5. Misroot: the fleet root carries two untracked sibling-lane reports (kengaku r45, tameshi r51); neither names chousa
   round 54, so no chousa round-54 artifact is misrooted there.

VERDICT — attacked the round-54 census at 447cf7e (maintained validate, the seven frozen CORPUS.md awks, non-vacuity
via selftest and mutants, append-only delta, S121–S123 first-URL uniqueness, reverse citation integrity) and the fleet
root's misroot state; all census numbers and the append-only/used-by integrity held, with only receipt-completeness, a
cwd hazard and the pre-existing S077 tool used-by surviving as findings.
