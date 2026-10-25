# R50ReviewQuarMap — re-do the absent-defect-register sweep (wave 2, falsify)

Attacks: the round-50 Gate claim that the chousa slice of the campaign
absent-defect register holds 24 rows, that zero name a theme URL, that the
counter's `QUARANTINE_VERDICTS=0/0` is therefore vacuous, and that recording
the sweep is the honest Gate record.

## 1. The slice reproduces: 24 rows

Command (the assigned one, verbatim; `R` = the read-only register):

```
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
$ awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5, $6}' "$R" | wc -l
24
```

Observed rows: 20 `payload-absent` rows (S077, S080, S082, S084, S086, S088,
S093, S094, S095, S096, S104, S105, S108, S110, S111, S112, S114, S116, S120,
S125) plus the 4 never-checked rows (S100`–S103`, whose `$6` reads
`#### Gate — S100` …, not a URL — register lines 269–272). The slice pattern
catches both register tables because both place lane/round/id/class at the
same pipe positions. The register's own `## By lane` table (register line 238)
records `chousa | 20` — the absent-section count, consistent: 20 + 4 = 24.
`grep -c '`chousa`'` over the whole file = 25 = these 24 + the By-lane line.
The lesson's "24 data rows" (corpus/lessons/round-50.md:117) reproduces.

## 2. Theme-URL sweep: 0, slice and whole file

```
$ awk … '{print $6}' "$R" | grep -c -e 'gs.sxu.edu.cn' -e 'rwxy.seu.edu.cn' -e 'bs.bnu.edu.cn' -e 'chaxin.las.ac.cn'
0
$ grep -c -e 'gs.sxu.edu.cn' -e 'rwxy.seu.edu.cn' -e 'bs.bnu.edu.cn' -e 'chaxin.las.ac.cn' "$R"
0
```

Zero over the slice's URL column and zero over the whole register file, so no
normalisation (case, trailing slash, percent-encoding) can raise the count:
the four hosts appear nowhere. Both reproduce the lesson verbatim.
Slice hosts (16 distinct, `grep -oE 'https?://[^/]+'`): doi.org, std.samr.gov.cn,
support.nii.ac.jp, www.jstage.jst.go.jp (×2), www.ncpssd.cn, xuebaobangong.jmu.edu.cn,
aclanthology.org (×3), ojs.aaai.org, www.zcmu.edu.cn, jc.hit.edu.cn, arxiv.org,
www.slarc.org.cn (×2), www.sinomed.ac.cn, c2h.niph.go.jp, www.gcpunion.org.
None is a theme host.

## 3. Register ids are pre-remap campaign ids — checked for the touched rows

`/home/vgpnk/Projects/shokuknow/lanes/chousa/ID-REMAP.md`: staged ids were
renumbered at packaging (lane registry ended at S081; staged rows became
S082–S195, per-round map). The register's `id` column is the PRE-remap
campaign-corpus id — round-48 lesson line 50 says so ("This is the campaign
register id, distinct from lane own-work S095"). Cross-checking the slice by
URL against `merge/chousa/SOURCES.append.md`: register S104 = staged S109
(kenkokyoiku J-STAGE PDF), S105 = staged S110 (jaohfa), S111 = staged S116
(slarc EN id=5290), S112 = staged S117 (slarc CN id=5237, verified
`| S117 | … slarc.org.cn/dwyx/CN/…id=5237`), S125 = staged S130 (gcpunion).
The four never-checked S100–S103 are campaign rows citing lane-local
artifacts (staged S105–S108 own-work rows), not URLs.

Touched-set check (round-50 `.ufo/waves/round-50/assimilation/renumber.tsv` +
lesson line 39): adopted documents are staged S118/S124/S135/S136 (lane
S104–S106), refused S145, body-id citations removed S076/S109/S111.
Cross-checking every slice URL against those: **one hit** — register S104's
URL is staged S109's document (the kenkokyoiku J-STAGE article). The round
touched S109 only by deleting its body-only citation token from the adopted
entries; the document itself was never adopted or refused, and the register
row is a campaign-corpus row, so it stays quarantined under round-48's
verdict (round-48 lesson line 52: `present`). No slice row names any of the
four theme documents. No register row is a lane S104–S106 row — the ids
collide numerically but name different documents in different id spaces.

Theme-adjacent in topic but NOT host or document (for the record):
zcmu.edu.cn S095 (CNKI 他引频次 doc), sinomed.ac.cn S114, slarc.org.cn S111/S112,
ncpssd.cn S086 — all quarantined campaign rows, none touched this round.

## 4. QUARANTINE_VERDICTS=0/0 is vacuous — confirmed, and the Gate wording is honest

Counter logic (corpus/evidence/round50/c2-count.py:228–242): it re-derives the
slice from the register (`'`chousa`' in f[1]`, `round[0-9]+` in f[2], `S[0-9]+`
in f[3], len>6), keeps rows whose `url_of(f[5])` normalises into the four
theme URLs (`theme` map, lines 60–63, 228), then harvests `VERDICT_RE` lines
from the lesson only for those ids; `ok` requires `len(verdicts)==len(reg_ids)`
(line 265). With `reg_ids={}` the conjunction is trivially satisfied:
0==0 and `blocked=0`. So the leg can only ever print `0/0` today — vacuous by
construction, exactly as the lesson says. The frozen claim (claims.md:74–76)
does say "a re-check verdict line for each absent-defect-register row on a
theme URL (the sweep prints how many there are)": with zero such rows the
obligation discharges to the sweep, and the Gate records the sweep command
chain and both `0` outputs (lesson:117) — falsifiable, replayable, and it
correctly declines to print a verdict table that would have no rows. Honest.

"round 48 holds their 24 verdicts" verified: corpus/lessons/round-48.md:40–65
lists all 24 slice ids (S077–S125 absent rows + S100–S103 never-checked rows)
with verdicts and per-row report pointers; tally line 67: 16 present,
8 absent-as-written, 0 unverifiable, S093 disputed.

## 5. Findings (no defects against the claim)

- F0 (note): the lesson's verbatim slice prints `{print $4, $5}` while its
  prose and the assigned command reference the `$6` URL column; output count
  is unaffected (24 either way) and the sweep grep is over `$6` as stated.
  Cosmetic only.
- F1 (note): register never-checked rows carry a stray backtick on the id
  (` S100`` `) and `#### Gate — S100` as the "cited source" cell — register
  formatting artifact, inherited by the slice; cannot collide with a theme
  URL (no `http` substring).
- F2 (note): `.ufo/waves/round-50/assimilation/renumber.tsv` still contains
  the pre-Gate adopter line `S145 S107 append` for the refused BNU manual;
  landed state is consistent — `append.md` has only S104–S106 and
  `grep -c 'bs.bnu.edu.cn' corpus/SOURCES.md` = 0. Scratch artifact, not a
  registry defect.
- Peer flag (R50ReopenRowS105), RETRACTED by the peer: spans.tsv `offset` is
  the span-block start `max(0, off − CONTEXT)` with CONTEXT=80
  (build-spans.py:44,119; docstring 17–18/25), not the quote position — the
  peer re-verified all 55 rows, 0 mismatches. No defect; this leg reads the
  register and lesson only (counter lines 228–242), never spans.tsv anyway.

VERDICT: attacked the absent-defect-register sweep and the quarantine-verdict leg — survived; the 24-row slice, the 0 theme-URL count (slice and whole file), the vacuity of `QUARANTINE_VERDICTS=0/0`, the "round 48 holds the verdicts" pointer, and the honest "the record is the sweep" Gate wording all reproduce; only cosmetic notes (register backtick artifacts, `$5`-vs-`$6` slice wording, stale pre-Gate renumber line, campaign-vs-staged id offset worth a reader note).
