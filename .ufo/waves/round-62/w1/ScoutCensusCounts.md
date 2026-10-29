# ScoutCensusCounts — round 62 w1 — pre-computed census

Seat: scout (leaf). Run at lane HEAD `d173d144bbf55403d091115b5a6ec73a721dd95c`; freeze commit
`388d153519a36a4c3f34d56d034870f032865a70` verified as ancestor (`git merge-base --is-ancestor`, exit 0);
`claims.md` sha256 full digest matches the wave context (`a3193ebd…866bc`). Lane root below =
`/home/vgpnk/Projects/shokunin/chousa-shokunin`. No writes outside this report; scratch dir created then deleted.

## BEFORE census (observed, chousa lane)

| metric | value |
|---|---|
| rows | 137 |
| malformed rows (NF≠13) | 0 |
| tier histogram | A=108 B=23 C=6 |
| status histogram | mined=112 queued=19 rejected=6 |
| duplicate ids | none |
| enum violations / tier inflation | none |
| dangling mined used-by paths | none |
| `sources-census.sh validate` | exit 0, lane `ok` |
| W04 list (duplicate url across scopes) | S051, S053, S073, S074, S075 |
| `corpus/knowledge/*.md` count | 83 |
| entries carrying `recheck:` | 79 |
| knowledge entries naming `openat2` | 0 |
| max row id | S137 ⇒ S138–S140 absent |

## PROJECTED AFTER (if S138, S139, S140 land + one entry `openat2-resolve-r62.md`)

Assumption (frozen C2 predicate): S138 tier A, S139 tier A, S140 tier B; all three status `mined`,
`opened` 2026-10-28, `used-by` names the entry; the entry carries the `source:`/`verified-at:`/`recheck:` trio.

| metric | before | after | delta |
|---|---|---|---|
| rows | 137 | **140** | +3 |
| tier.A | 108 | **110** | +2 (S138, S139) |
| tier.B | 23 | **24** | +1 (S140) |
| tier.C | 6 | 6 | 0 |
| status.mined | 112 | **115** | +3 |
| status.queued | 19 | 19 | 0 |
| status.rejected | 6 | 6 | 0 |
| knowledge `*.md` | 83 | **84** | +1 |
| entries carrying `recheck:` | 79 | **80** | +1 |
| malformed rows | 0 | 0 | — |
| validate exit | 0 (`ok`) | 0 (`ok`) | C2 CENSUS gate requires exit 0 |
| W04 list | 5 ids | 5 ids [INFERENCE] | new rows cite local paths (man page, header, own-work file), no URL collision with the 5 existing W04 pairs expected |

L1 comparison line: after landing, the same commands must print `140` rows, `A=110 B=24 C=6`,
`mined=115 queued=19 rejected=6`, `84` knowledge files, `80` recheck carriers, validate exit 0.

## Evidence (command → observed output)

1. Freeze check:
   `sha256sum <lane>/corpus/evidence/round62/claims.md` →
   `a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc  …claims.md`;
   `git -C <lane> merge-base --is-ancestor 388d153… HEAD && echo IS-ancestor` → `freeze commit IS ancestor of HEAD`;
   `git -C <lane> rev-parse HEAD` → `d173d144bbf55403d091115b5a6ec73a721dd95c`.
2. The item's command: `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` →
   five `chousa	W04	…` lines (S051, S053, S073, S074, S075), then
   `chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`, `exit=0`.
   (W04 = same URL across scopes; warnings do not affect the clean `ok`.)
3. Manual CORPUS.md awk lines against `<lane>/corpus/SOURCES.md` (verbatim lines from the
   `### Census` block, CORPUS.md lines 130–147): rows → `137`; malformed → `0`;
   tier hist → `A=108 B=23 C=6`; status hist → `mined=112 queued=19 rejected=6`;
   dup ids / enum violations / dangling used-by → all empty.
4. Knowledge counts: `find <lane>/corpus/knowledge -name '*.md' | wc -l` → `83`;
   CORPUS.md canonical `grep -rlE '^[-* ]*recheck *:' --include='*.md' <lane>/corpus/knowledge | wc -l` → `79`
   (anchored `^recheck *:` variant also `79`).
5. Pre-landing posture: max id `S137` + empty dup check ⇒ S138–S140 absent (row ids unique, append-only);
   `grep -rl openat2 <lane>/corpus/knowledge | wc -l` → `0`;
   lead recorded at `corpus/SOURCES.md` line 326: `openat2(2) — installed /usr/share/man/man2/openat2.2.gz
   (Linux man-pages 6.19) … not opened as a row`.

Note for L1: the C2 counter's CENSUS gate runs `scripts/sources-census.sh validate --file
ROOT/corpus/SOURCES.md` with cwd=ROOT and needs exit 0; the lane validates clean today with the 5 W04
warnings, so the after-state passes that gate iff the three new rows are well-formed (E-codes fail it, W-codes don't).

VERDICT: BEFORE_ROWS=137 PROJECTED_AFTER=140
