# R52W2ExecCensusFinal — census and registry integrity at `e769c03`

Attacked: the round-end census claim, rows S113–S116 as claims, the `used-by` ↔ `source:` binding,
the anchor cells, the lesson's `## Census` numbers, and lane hygiene at the commit. No install
(pacman paused; nothing needed). Scratch `/fast/scratch/hyaku/chousa-r52/R52W2ExecCensusFinal`
(clone at base + four mutant registries) removed at exit; this file is my only write.
## 1. Census validate — exit 0, five W04, all pre-existing
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0:
```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```
No E line. The same command as `validate --file` on a clone at `00f8c7f5` prints the same five W04
and `ok`, exit 0 → round 52 introduced none. `census --file`: rows 116, tier.A 100, tier.B 11,
tier.C 5, invalid 0, status.mined 92, status.queued 19, status.rejected 5, missing 0.
`overdue --root … chousa`: exit 0, 116 `cadence` lines, **0** `overdue` lines.
## 2. Manual one-liners (lane root, CORPUS.md §'SOURCES.md')
rows `116`; malformed `0`; tiers `A=100 B=11 C=5`; statuses `mined=92 queued=19 rejected=5`;
duplicate ids → no output; enum violations → no output; mined `used-by` → no `missing:` line.
Base `00f8c7f5`: rows `112`, malformed 0, `A=98 B=9 C=5`, `mined=88 queued=19 rejected=5` — so
+4 rows (2 A, 2 B), +4 mined, queued/rejected untouched, matching `round-52.md:141` ("112 → 116
… A S114 S115; B S113 S116"). Ids ascend S001…S116 (order awk: no output); every row-shaped line
is inside `## Registry` (11–126; `## Paths` at 128).
## 3. Byte identity of S001–S112
`git diff --numstat 00f8c7f5 e769c03 -- corpus/SOURCES.md` → `4 0`. Stronger: `git show
00f8c7f5:corpus/SOURCES.md` vs head with the four `| S11[3-6] |` lines deleted → `diff` empty,
`cmp` clean, 322 lines each. Only four rows were inserted; no old row's `status`, `recheck` or
`used-by` moved (rule 2 holds; `round-52.md:141` "Rows touched old → new: none" is true). Base max
id S112 → S113–S116 are the next unused, never reused.
## 4. The four rows as claims
Each NF=13, no `|` in a cell; kind `docs`; tiers S113 B, S114 A, S115 A, S116 B; status `mined`;
opened `2026-10-26`; recheck `180d`; `used-by` exactly one path. The four URLs occur nowhere else
in SOURCES.md (host grep → lines 123–126 only; `## Leads` names none). First source-cell URL =
archive copy (S116), `.docx` (S115), portal record (S113), journal page (S114). Cell claims
re-opened in the read-only cache (`key = sha256(url)[:24]`, `read_text`):
| row | anchor claim | observed | spans.tsv digest |
|---|---|---|---|
| S113 | `.txt` UTF-8, 8804 chars | 8804 chars, 14135 B | `ad6b09f0…` = file sha256 |
| S114 | `.txt` UTF-8, 6179 chars | 6179 chars, 11676 B | `b1c3cd6a…` = file sha256 |
| S115 | text form 19682, raw `16fc8c55` | `capture-text.py` 19682; `build-spans.docx_text` 19682, byte-equal; raw sha256 `16fc8c55…`, 178056 B | `16fc8c55…` = raw sha256 |
| S116 | `.txt` UTF-8, 5328 chars | 5328 chars, 10106 B; `.raw` 343301 B | `93558b6d…` = file sha256 |
- **S114, not number-drift:** raw byte decode gives 7585 chars, `read_text` 6179 (1406 CRLF pairs;
  7585 − 1406 = 6179). The counter's text form is the universal-newline read, so 6179 is right.
- **S115 sidecar** ("not this document's text") true: 168952 chars, `文献検索` 0, 72117 U+FFFD, as
  `round-52.md:52`. **S116 original** key `f3dbe2fe59a684b1b94cfadc` holds only `.fail` (6 B, `rc=28`).
- **Anchors, independently:** all 18 `char N` (5+4+5+4) re-resolved without c2-count's arithmetic —
  that offset in the text form begins a spans.tsv quote of the same id, 18/18 true (S115 8996 →
  `SRにおける文献検索期間について明記する。`; S116 592 → `それぞれの情報源が最後に調べられた日付を記載する`).
## 5. Binding, trio and C2 replay
`source:` S115 → `japanese-search-record-niph-form-r52.md:3`; S116 →
`japanese-prisma-item-wording-r40.md:3`; S113 → `chinese-prisma-s-reception-r52.md:3`, S114 → same
file `:4`; each row's `used-by` names exactly that entry, and no other knowledge entry carries
`source: S11[3-6]`. The trio leads each entry at lines 3–5 (Chinese 3–6, two `source:` lines), the
lane's existing shape (`search-log-method-r39.md` 3–5); CORPUS.md sweep `grep -rlE '^[-* ]*recheck *:'`
lists all three (lane-wide 70/74; the four exceptions are pre-existing r8–r34 files). Replay
`c2-count.py`: `ENTRIES=3/3 BOUND=4/4 REFUSED=0 BOUND_IDS=S113,S114,S115,S116 REF_ID_UNBOUND=0
QUOTE_ROWS=38 CAPTURE_BOUND=38/38 SUBSTANCE=PASS ANCHOR_BOUND=4/4 INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=1/1 C2=PASS`, exit 0.
## 6. The clean pass is not vacuous
Mutant registries in scratch (symlinked `knowledge/`, `lessons/`, `tools/` so E11 resolves),
`validate --file`: duplicate id → `E03 S115 duplicate id` exit 1; tier → `E06 S113 tier=E` exit 1;
`used-by` retargeted → `E11 S114 missing used-by corpus/knowledge/does-not-exist.md` exit 1;
`recheck` cleared → `E09 S115 recheck=` exit 1. Every class the clean registry lacks is detected.
## 7. Differences found
**D1 — reference-drift: the round-end census receipt is absent.** `round-52.md:140` cites
`corpus/evidence/round52/measure-after.txt`; it does not exist (`ls corpus/evidence/round52/`;
`find .ufo/waves/round-52 -name '*census*' -o -name '*measure*'` → none), while rounds 40/41/45/46/47
each ship theirs. The claim is true — only the receipt is missing. Intended lane path
`corpus/evidence/round52/measure-after.txt`, content = §1's transcript verbatim (five W04, `ok`,
`exit=0`) plus the row count from §2 (`116`), under the line
`# at lane tip e769c03738d08c36109556ebf301a1db0dcf143d, 2026-10-26, seat R52W2ExecCensusFinal`.

**D2 — contract rule 5: `## Search log` has no round-52 note.** `grep -n 'Round 52'
corpus/SOURCES.md` → exit 1; no `2026-10-26` text outside rows 123–126; last bullet is
`SOURCES.md:299` (Round 51), while rounds 30–51 each logged their bounded search, cache-only
re-openings included (43, 44, 45, 49, 50, 51). Intended lane path `corpus/SOURCES.md`, after line 299:
```
- Round 52 (2026-10-26): question — which Japanese and Chinese documents state what a systematic
  review's search record must carry, read BY DOCUMENT from the round-51 refusal set? Where: the
  campaign capture cache only (`.qcache`, captures written 2026-10-23); no URL fetched (L0
  `8d77e6c1` open); `merge/chousa/` read-only. Identified 4 documents behind the three claimed
  entries, screened 4, included 4 (S113 梅斯医学 portal record, S114 中国全科医学 PRISMA 2020
  checklist page, S115 the NIPH `.docx` via `tools/capture-text.py`, S116 the archived Japanese
  PRISMA 2020 table), excluded 0; S113 is a second carrier of covered ground, so coverage credit
  is three by document. Stop rationale: each entry needs one document that states the wording,
  and every other candidate was decided in the round-51 Gate.
```
**D3 — named risk (not a breach): S113–S116 mean two things in lane prose.** Uniqueness holds
(base max S112) and the counters read only the Registry section (`c2-count.registry()`,
`inference-ground --registry`), so nothing breaks — but the strings already exist with other
meanings: `lessons/round-47.md:184-185` (`S113 → S092, S114 → S093, S115 → S094`, package ids),
`lessons/round-51.md:299` (package numbering), `round-51.md:75,86` and `evidence/round51/claims.md:89`
(register rows), `lessons/round-42.md:68-69` (package ids). Append-only forbids editing them; keep
qualifying new prose (`register S120`, "package S116").
**D4 — minor curation: `## Paths` stops before the new documents.** `SOURCES.md:150` ends S107 →
S108 → S112, S109 → S110 → S111; S114/S115/S116 continue that exact sequence. No rule requires a
row in a path; recorded so the L1 can extend the line.
**D5 — hygiene: five untracked debris files at the lane root**, not mine: `forge.out` 202 B,
`naive.out` 383 B, `sup-forge.out` 187 B, `sup-naive.out` 274 B (counter/control stdout — `forge.out`
holds `REAL=PASS rc=0 count=1 … chars=21`, `LEGS=9/9`, `C1=PASS`), `s115form.txt` 48936 B — all
20:24–20:28, all unknown to `git ls-files`. The wave-1 stray-redirect mistake recurring, now in the
lane; any `git add -A` would land them.
## VERDICT
Attacked the round-end census claim, the four rows, their anchor cells and the `used-by` binding:
the registry is clean at `e769c03` (validate exit 0, five pre-existing W04, 116 rows, 0 malformed,
0 duplicate ids, 0 enum violations, 0 missing `used-by`, S001–S112 byte-identical to base, 18/18
anchors and all digests re-resolved, C2 replay PASS, trio first in all three entries) — with five
differences for the L1: D1 the cited `measure-after.txt` does not exist, D2 the rule-5 round-52
Search-log note is missing, D3 the new ids collide textually with package/register ids, D4 `## Paths`
is not extended, D5 five untracked debris files sit at the lane root.
