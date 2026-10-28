# ScoutC2RowsCensus

Axes: operability (validate exit on the inserted registry), depth (SOURCES contract fields), calibration (counts only from the commands below).

## Findings

The four frozen rows in `corpus/evidence/round61/controls/c2-positive-rows.txt` (sha256 `721a108b8fa058eb3d228cd36620b32743c7071eae6ba9b0553da4e080d701dc`, claims prefix `721a108b…d701dc`) are shape-clean. Each line splits to NF=13 (11 cells). Ids S134–S137 are unique and are the next ids after contiguous S001–S133 (133 ids, no gaps, no duplicates).

| id | kind | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|
| S134 | docs | A | mined | 2026-10-28 | on-release | `corpus/knowledge/derived-output-safety-r61.md` |
| S135 | docs | A | mined | 2026-10-28 | on-release | same path |
| S136 | own-work | B | mined | 2026-10-28 | 180d | same path |
| S137 | own-work | C | rejected | 2026-10-28 | 180d | `—` (U+2014) |

`opened` is a real ISO date and is not after UTC today `2026-10-28`. Kind, tier, and status sit in the contract enums. No row is `community` at tier A. No cell contains `|`. S137 `teaches` matches `REJECTED: <reason>; flip: <condition>` (289 characters). S134–S136 `teaches` do not open with `REJECTED:`. S137's em dash is U+2014, the same character as S008's `used-by`.

Paths named in the source cells exist: `/usr/share/man/man2/open.2.gz`, `/usr/share/man/man2/rename.2.gz`, `.ufo/waves/round-56/w1/R55W2SentBuilder.md`, `tools/build-spans.py`.

S134 and S135 are `docs` and their `source` cells contain no `http` URL (installed man paths). `sources-census.sh` emits no E-code for a missing URL. `claims.md` already records that those rows carry no URL.

Rows appended inside `## Registry`, immediately after S133, on a scratch lane (other entries symlinked to the lane; cwd = that lane root): `validate` exits 1. The only new codes are E11 for S134, S135, and S136, each `missing used-by corpus/knowledge/derived-output-safety-r61.md`. The manual awk prints `missing:` for that path three times. No E01–E10, no E12, and no new W01/W02/W03/W04. The five pre-existing W04 lines are unchanged. Warnings alone leave exit 0: the real registry validates 0 with those same W04 lines.

A scratch-only probe planted a zero-byte file at that used-by path (realpath stayed under the scratch dir; `corpus/knowledge/derived-output-safety-r61.md` stayed absent on the lane). `validate` then exited 0 and printed `file ok` plus the same five W04 lines. The manual missing check printed nothing. The probe only satisfies `[ -e ]`.

## Census

`sources-census.sh census` and the CORPUS.md manual awk agree.

| | before | after |
|---|---|---|
| rows | 133 | 137 |
| tier | A=106 B=22 C=5 | A=108 B=23 C=6 |
| status | mined=109 queued=19 rejected=5 | mined=112 queued=19 rejected=6 |
| invalid | tier 0, status 0 | tier 0, status 0 |
| W-codes | W04 S051, S053, S073, S074, S075 | same five; no new W |
| validate | exit 0 | exit 1 |

Delta is S134 A/mined, S135 A/mined, S136 B/mined, S137 C/rejected. Census mode exits 0 on both files (`FLEET.missing=0`). `CENSUS_EXIT` below is the `validate` exit on the rows-only scratch copy. Malformed rows 0 both sides. Duplicate ids empty. Enum and tier-inflation lines empty.

Lane `corpus/SOURCES.md` sha256 stayed `ed8802350271e39f663361e501598f1476b464f599e592a14e76904e44f3a5aa`. Scratch `/fast/scratch/hyaku/chousa-r61/ScoutC2RowsCensus` was removed after the runs.

## Evidence

Before, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`, UTC date `2026-10-28`:

- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md` → exit 0; `file W04` for S051, S053, S073, S074, S075; `file ok`.
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md` → exit 0; `file rows 133`; `tier.A 106`; `tier.B 22`; `tier.C 5`; `status.mined 109`; `status.queued 19`; `status.rejected 5`; fleet tier/status invalid 0; `FLEET missing 0`.
- CORPUS.md manual awk, same cwd: `rows=133`, `malformed=0`, `tier=A=106 B=22 C=5`, `status=mined=109 queued=19 rejected=5`, dupes empty, enums empty, missing empty.

After, cwd `/fast/scratch/hyaku/chousa-r61/ScoutC2RowsCensus/lane`, copy of `corpus/SOURCES.md` plus the four lines (4 added lines, 0 removed):

- `validate --file` that copy → exit 1; the five W04 lines plus `file E11 S134`, `S135`, `S136` missing the knowledge path. No `file ok`.
- `census --file` that copy → exit 0; `rows 137`; `tier.A 108`; `tier.B 23`; `tier.C 6`; `status.mined 112`; `status.queued 19`; `status.rejected 6`.
- Manual awk: `rows=137`, `malformed=0`, `tier=A=108 B=23 C=6`, `status=mined=112 queued=19 rejected=6`, dupes empty, enums empty, three `missing: corpus/knowledge/derived-output-safety-r61.md`.
- Probe `validate` after the zero-byte used-by file → exit 0; five W04 lines; `file ok`. Manual missing empty.

VERDICT: CENSUS_EXIT=1 rows=133->137 findings=E11:S134,E11:S135,E11:S136
