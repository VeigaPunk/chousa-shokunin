# R51W2DraftReportOutline — report sections 'Sources & frontier' and 'Trend verdicts'

Seat: scribe (draft only). Measured revision: wave-1 landing `4436e279b91d8d68fd439c9095695035fbeeab74`
(`git diff --name-only 4436e279 HEAD` lists only `.ufo/waves/round-51/{gen-w2-spec.py,w2-dispatch.json,
w2-run.err,w2-spec.json}`, so every counter input below equals the landing; the working tree's one tracked
modification is `.ufo/waves/round-51/w1/R51DraftSkillGates.md`, a w1 seat report no counter reads).
All counters run as `env -u ASSIMILATE_CITES python3 …` from `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

## Grounding commands and observed output

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md                      → 112
$ git show 9ec1751a:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'  → 106
$ git diff --numstat 9ec1751a 4436e279 -- corpus/SOURCES.md                                → 8  0
    (six S-rows S107–S112 plus `-` lines at :146 reading path and :295 round question; no row edited)
$ tiers by column 5: tip A 98 B 9 C 5 ; base A 93 B 8 C 5 ; statuses tip mined 88 queued 19 rejected 5
$ scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa              → exit 0, ok, 5×W04
    (S051 S053 S073 S074 S075, identical text to corpus/evidence/round51/census-start.txt, which reads exit=0)
$ wc -l .ufo/waves/round-51/assimilation/{collisions,reg-ids,staged-ids}                      → 25 / 106 / 114
    collisions S082–S106; S100–S102 staged URLs == lane URLs (grep -oE 'https?://[^ |]+' both sides)
$ git grep -l -e 検索式 -e 灰色文献 9ec1751a -- corpus/knowledge | wc -l                     → 0 ; HEAD → 3
$ c1-count.py                          → LEGS=5/5 C1=PASS exit 0
$ c1-supplement.py                     → SUPPLEMENT_LEGS=6/6 C1_SUPPLEMENT=PASS exit 0
$ c2-count.py                          → ENTRIES=3/3 BOUND=6/7 (min 5) REFUSED=1 NEW_GROUND=3/3
                                          QUOTE_ROWS=61 ON_BOUND=61/61 QUOTES_IN_SPAN/ENTRY/LESSON=61/61
                                          CAPTURE_BOUND=61/61 SUBSTANCE=PASS ANCHOR_BOUND=6/6
                                          INFERENCE_GROUNDED=3/3 C2=PASS exit 0
$ c3-count.py                          → CAP_ROWS=36 (base 36) POINTERS=74 (base 74)
                                          RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS exit 0
$ open-items-age.py /home/vgpnk/Projects/shokunin/.ufo/reports/round-50/chousa.md --round 51 → exit 1
$ open-items-age.py <stub with the line below> --round 51                                    → OPEN_ITEMS_AGE=PASS since=42 rounds=9
$ ls -l --time-style=long-iso …/.qcache | sort -k6,7 | tail -2 → 2026-10-24 23:26 *.raw (newest)
$ six capture keys (sha256(url)[:24]) .txt exist, chars 21216 / 39676 / 52208 / 50952 / 1675 / 25811
$ docx: 3a8b45977cd111e45e3980a5.raw 178056 B head PK\x03\x04 ; .txt 168952 chars, 72117 U+FFFD,
        'SRにおける文献検索期間' 0, '検索期間' 0 ('corpus/lessons/round-51.md:56')
$ counted rows under '## Mistakes' (`:10`)                                                    → 8
$ git ls-tree --name-only 4436e279 corpus/evidence/round51/                                   → no measure-after.txt
$ receipt-check.py corpus/evidence/round51/measure-r50-at-tip.txt --skill SKILL.md
      → RECEIPT_NO_REV …, SKILL_NO_PIN SKILL.md, RECEIPT_CHECK=FAIL exit 1
      (`SKILL.md:130` does carry `tool-rev: cf642c66… tool: tools/assimilate-rows.py`; the skill leg
       calls `header()` on the first five lines only — `receipt-check.py:64,119`)
$ c1-count.py --tool corpus/evidence/round51/controls/forge-dirname.py      → LEGS=5/5 C1=PASS
$ c1-supplement.py --tool corpus/evidence/round51/controls/forge-dirname.py → SUPPLEMENT_LEGS=1/6 FAIL
```

## Draft — intended lane path `/home/vgpnk/Projects/shokunin/.ufo/reports/round-51/chousa.md`

```markdown
## Sources & frontier

Command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`.

- **Round start:** exit 0, `ok`, the five pre-existing W04 warnings (S051, S053, S073, S074, S075) (`corpus/evidence/round51/census-start.txt`).
- **Round end:** exit 0, `ok`, the same five W04, measured at the wave-1 landing `4436e279`; the round-51 after-measurement does not exist at that revision (`git ls-tree … corpus/evidence/round51/`).
- **Rows:** 106 → 112 (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md`; `git show 9ec1751a:corpus/SOURCES.md | …` → 106). Tiers A 93→98, B 8→9, C 5→5; mined 82→88, queued 19, rejected 5. Added by tier: A S107 S108 S109 S110 S112; B S111. Rows touched old→new: none (`git diff --numstat` → `8 0`: six registry rows plus the `:146` reading path and `:295` round question).
- **Frontier:** three entries on ground the lane did not hold — 検索式 and 灰色文献 occur in 0 `corpus/knowledge` files at the base (`git grep -l … | wc -l` → 0) and in 3 at the tip. Credit is per document: the three entries rest on six registry rows S107–S112, and two of the six are articles in one journal (实验动物与比较医学 2025;45(4) and 45(1)), so neither the entry count nor a journal count measures the reuse.
- **Assimilation:** theme "Japanese/Chinese search records" from `merge/chousa/` (`MERGE-REPORT.md:29,32,37`). Section-10 collision check: 25 collisions (S082–S106) against 106 registry ids (`reg-ids`) and 114 staged ids (`staged-ids`); three are identity collisions (S100–S102 carry the same URLs as the lane rows) and 22 numbering. Guard proved on an indented-row fixture (`assimilation/guard-proof.txt`). Renumber by document: staged S109→S107, S110→S108, S116→S109, S117→S110, S119→S111, S126→S112; staged S125 refused, no lane id.
- **Refused document:** the national institute's submission form (staged S125) — its `.raw` is a ZIP (`PK\x03\x04`, 178,056 bytes), its `.txt` is those bytes decoded with replacement (168,952 characters, 72,117 U+FFFD), and the document's phrases occur 0 times in that form, so no span can bind (`corpus/lessons/round-51.md:56`).
- **considerthese:** `considerthese/2026-10-25.md` — the open-items-age proposal is mined as `open-items-age.py`; it exits 1 on the round-50 report and 0 on a report carrying `Open operator items: 8d77e6c1 since round 42 (9 rounds)`.
- **Freshness:** newest readable capture 2026-10-24 23:26 (host time, `.qcache`); the six documents' `.txt` forms hold 21,216 / 39,676 / 52,208 / 50,952 / 1,675 / 25,811 characters; no fetch (L0 `8d77e6c1` open).
- **Mined mistakes:** eight, in the lesson's `## Mistakes` (`corpus/lessons/round-51.md:10`).
- **Sourced claim:** C2 rests on S107–S112 — `ENTRIES=3/3 BOUND=6/7 (min 5) REFUSED=1 NEW_GROUND=3/3 QUOTE_ROWS=61 ON_BOUND=61/61 QUOTES_IN_SPAN/ENTRY/LESSON=61/61 CAPTURE_BOUND=61/61 SUBSTANCE=PASS ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=3/3 C2=PASS`, exit 0.

## Trend verdicts

- **expansion — improved.** Six new registry rows on ground the lane held none of (0 knowledge files naming 検索式 or 灰色文献 at the base, 3 at the tip), five tier A and one tier B, with three entries. Caveat: two of the six are articles in one journal, so six documents is six rows, not six journals and not three entries.
- **quality — improved, with the frozen counter's replay weakness named.** At the wave-1 landing all three counters pass (`LEGS=5/5 C1=PASS`; supplement `6/6`; `C2=PASS` with 61/61 quotes located inside span, entry, lesson and capture; `C3=PASS DANGLING=0` after four append-only SCORECARD corrections and one SHONEN pointer fix), and eight mistakes are recorded with the commands that fail. Reported, not repaired: the frozen C1 counter still scores a 94-line forge `LEGS=5/5 C1=PASS` (`c1-count.py --tool controls/forge-dirname.py`) where the post-freeze supplement scores it `1/6`; and `receipt-check.py`'s skill leg reads only SKILL.md's first five lines, so the Gates-row pin at `SKILL.md:130` prints `SKILL_NO_PIN` — QUALITY 84's check cannot see the pin it requires.
- **discernment — unprovable-but-better.** Every seat in both waves is a subagent this lane dispatched (`w1-spec.json` 48 items, `w2-spec.json` 41), so no verdict here is a non-author's. What improved is adversarial reading of the lane's own instruments: its frozen counter was shown to pass a tool implementing none of the behaviours, and the counterexample, the supplement and the C3 dot-class erratum are on disk. The closure should supply the non-author read: re-open S111's SinoMed record, the refused NIPH form, and the S109/S110 journal pair.
```

## What holds, what breaks

- Holds: the row/tier/status deltas, the census parity (start and end identical text), the collision split
  (25 = 3 identity + 22 numbering, plus a guard that proves the pattern choice), the renumber map, the
  refused-`.docx` ground, the six captures with the lesson's character counts, 61/61 quote binding in three
  places, and the considered proposal's two-sided check.
- Breaks, and is written into the draft's quality caveat rather than smoothed: the frozen C1 counter's forge
  replay (measured), and `receipt-check.py`'s skill leg being unable to read a Gates-row pin (measured:
  `SKILL_NO_PIN` while `SKILL.md:130` carries the header). Separately, `corpus/lessons/round-51.md:27`
  claims `corpus/evidence/round51/measure-after.txt` exists with a `tool-rev:` header; `git ls-tree 4436e279
  corpus/evidence/round51/` lists no such file and the only `tool-rev:` in the tree is inside a SKILL row.
  That is a reference-drift in the lesson, not in the counters.
- Not mine to settle: whether the after-measurement and the L1's final quality wording absorb these caveats.

## Touched surfaces, out of scope, tooling

- Wrote only this file. Scratch `/dev/shm/chousa-r51-R51W2DraftReportOutline/stub.md` created for one
  `OPEN_ITEMS_AGE=PASS` run and deleted; no lane file copied or linked.
- Read-only elsewhere: no production edit, no counter edit, no git index or jj state, no commit, no
  `/home/vgpnk/Projects/shokuknow` campaign tool, no network. No tool installed.

VERDICT: attacked the two sections' factual base — every number re-derived at `4436e279` (rows 106→112,
tiers 93/8/5→98/9/5, 25 collisions = 3 identity + 22 numbering, eight mistakes, 61/61 quotes, census exit 0
both ends, six captures present); expansion improved, quality improved with the frozen-counter forge
(`LEGS=5/5` for `forge-dirname.py`) and the `SKILL_NO_PIN` leg disclosed, discernment unprovable-but-better.
