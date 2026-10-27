# R56ExecCollision — section-10 collision check, independent re-derivation

Seat R56ExecCollision (leaf). Item: reproduce the section-10 collision check independently, prove the guard on
my own indented fixture, check the four C2 URLs and ids S127-S130, derive the theme quarantine slice. Frozen
base `e5a3795`; round-56 files at lane commit `46e1758f`. Scratch `/fast/scratch/hyaku/chousa-r56/R56ExecCollision`
(TMPDIR set, removed at end). No tools installed; coreutils/grep/diff/python3 sufficed.

## 1. Re-derivation (0-3-space pattern), byte-for-byte

Frozen registry read out of git, never the live worktree (the live file gained the wave's own four C2 rows):

    git -C …/chousa-shokunin show 46e1758f:corpus/SOURCES.md > SRC-46e1758f.md   # 337 lines

Pattern used for both files: `^ {0,3}\| *S[0-9]+` (row-anchored: a leading pipe is required — see §2 trap).
Staged file: `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md` (120 lines).

| artifact | mine | recorded | bytes identical | sha256 |
|---|---|---|---|---|
| reg-ids | 126 ids, S001..S126 | 126 | yes (order preserved) | `f33ac6588a16b18a65a4d66a5570af2576e7be08ac7468237656464d73d70607` |
| staged-ids | 114 ids, S082..S195 | 114 | yes (order preserved) | `9ce3b9c30cd1115797315c6aea6f00fa45b4ff141a9aa630059afe3cc6b8e2f9` |
| collisions | 45 ids, S082..S126 contiguous | 45 lines | yes (order preserved) | `707e6aef9bd7f35d223f5afa4bdd4f2d47f0ada54d163eccc01d8fb2feeb04e8` |
| quarantine-slice | 24 lines | 24 lines | `diff` empty | `1ec5a29fb97afc5a334282e48b41bc3dd59312f0c7e85c37b60f77b392a464be` |
| guard-proof.txt | (fixture proof, §2) | 4 lines | n/a | `1aa60204212fda74139d37f54f7daa5723bd645e43e4b7668d11c42c2ab48d60` |

Observed: `exact-equal-bytes: True / order preserved: True` for all three id files, and my sha256 over the
regenerated strings equals the recorded files' sha256 exactly. No duplicate ids (`dups reg: 0 dups staged: 0`);
69 staged ids are not in the registry (114 − 45), so the staged remainder is free. Collisions are exactly the
closed interval S082..S126 (45 = 126 − 82 + 1).

## 2. Guard proof on my own indented fixture

My fixture (rows at 0, 2, 3, 4 and 5 leading spaces), extracted two ways:

    $ grep -oE '^ {0,3}\| *S[0-9]+' fixture.md | grep -oE 'S[0-9]+'
    S155
    S156
    S157
    $ grep -oE '^\| *S[0-9]+' fixture.md | grep -oE 'S[0-9]+'      # column-zero-only
    S155
    (end)

Reproduces the recorded guard-proof's behaviour (a two-space `| S155 |` row is visible to the 0-3 pattern
and invisible to a column-zero pattern) and adds its upper edge: the 4-space (`S158`) and 5-space (`S159`)
rows are dropped by the 0-3 pattern too, so the guard is tolerance-0-3, not indentation-agnostic.

Two calibration points, both measured:
- **Not exercised by the real data**: `grep -cE '^ {1,3}\| *S[0-9]+'` = 0 in the frozen registry, 0 live,
  0 in the staged append — every real id cell sits at column zero, so the 0-3 tolerance is safety margin,
  demonstrated only on the fixture.
- **The row anchor is load-bearing**: `^ {0,3}S[0-9]+` (no pipe) yields 130 matches in the frozen registry
  instead of 126, picking up four prose lines (157 `  S025 is a rejected HTTP analogy…`, 204 `  S047 page
  omits…`, 235 `  S029 reopened…`, 335 `S033 also supersedes S020…`). All four are below S082, so the
  *collision set* would still be 45, but the reg count would be wrong and any future prose sentence starting
  with an id would silently enter the list. Closing the id cell (`^ {0,3}\| *S[0-9]+ *\|`) gives 126 / 114.

## 3. C2 documents vs the lane registry (frozen rev 46e1758f)

`grep -Fc <url> SRC-46e1758f.md` for each of the four:

| URL (abbrev.) | frozen registry | live registry (`corpus/SOURCES.md`) |
|---|---|---|
| ttbz.org.cn/…/6387963976070960491020144.pdf (S127) | 0 | 1 — line 137, id S127 |
| ttbz.org.cn/…/6387963977456239722441041.pdf (S128) | 0 | 1 — line 138, id S128 |
| journal.china-pharmacy.com/…/129333664/… (S129) | 0 | 1 — line 139, id S129 |
| nhc.gov.cn/…/1732786237821_21413.pdf (S130) | 0 | 1 — line 140, id S130 |

At the frozen base none of the four documents is a lane row, and S127-S130 are unused:
`awk '/^ {0,3}\| *S[0-9]+/{print $2}' SRC-46e1758f.md | sort -V | tail -3` → `S124 S125 S126`;
`grep -cE '^ {0,3}\| *S(127|128|129|130) '` → 0. The live-tree delta is exactly those four ids:
`diff live.ids <(sort -u …/assimilation/reg-ids)` → `< S127 < S128 < S129 < S130`, nothing else; live has
130 unique ids over 130 rows, no duplicate ids. So the one live hit per URL is the wave's own new rows
(committed at lane HEAD `99eff0e`, not by this seat), not a pre-existing lane row. Held row S118 is present
at frozen line 128 and carries the bjhea.org.cn 2024-QC URL as stated.

## 4. Residual hazards found while reproducing (reported, not patched)

1. **Lane ids S127-S130 are numerically inside the staged id range.** Staged S127-S130 are four unrelated
   documents: `AVeriTeC Dataset` (fever.ai/dataset/averitec.html), `AVeriImaTeC` (arXiv:2505.17978v2),
   the withdrawn Japanese PRISMA-2020 checklist, and 上市药品临床安全性文献评价指导原则（试行） (gcpunion.org).
   At the frozen base reg∩staged = 45; after the lane writes S127-S130 it becomes 49, because staged still
   holds those four ids. The renumbering must therefore be carried as an explicit (staged id → lane id)
   pairing table; a plain id-ordered append would now collide on four rows it did not before.
2. **Staged S156 duplicates staged S169** (same URL `…/6387963977456239722441041.pdf`; the C2 entry takes
   S169 for lane S128), and the staged file holds other duplicate documents (by first URL: the fever.ai page
   ×2, `gs.sxu.edu.cn/…9e5cdd215a414bf6b5694912018de4c8.pdf` ×4, `medsci.cn…23e481c0052069d3` ×3, the bjhea
   2024-QC PDF ×2). Appending both members of the 编制说明 pair gives the lane two rows for one document.
3. **Staged S130 is the document the register already quarantines.** Its URL
   `http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc` is lane row **S124** at the frozen rev
   (line 134), and register line 56 quarantines that URL under the label `S125`, class `payload-absent`, its
   own note reading "cited source, companion URLs and local artifacts were all checked; the quote is in none
   of them", over 3 quoted spans naming 灰色文献. The register's label (S125) does not match the frozen
   registry's row for the same URL (S125 there is `m.cnpharm.com/201906/18/c280684.html`), so the slice must
   be matched **by URL**, never by id label. Consequence: adopting staged S130 would import a document whose
   quotes the census could not match.

## 5. Quarantine slice for the theme URLs (expected 0 rows — confirmed)

Operator recipe, run verbatim:

    awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
      /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md

→ 24 lines, `diff` against `…/round-56/assimilation/quarantine-slice` empty; 20 `payload-absent` rows
(S077 S080 S082 S084 S086 S088 S093 S094 S095 S096 S104 S105 S108 S110 S111 S112 S114 S116 S120 S125) and
4 "the gate block named no locator" rows (S100 S101 S102 S103), first line ` S077   `payload-absent` `.
Theme membership, counted in the whole register: `ttbz.org.cn` 0, `china-pharmacy.com` 0, `nhc.gov.cn` 0,
`bjhea.org.cn` 0, and per-token `6387963976070960491020144` 0, `6387963977456239722441041` 0, `129333664` 0,
`1732786237821_21413` 0 → **0 quarantined rows for any of the four C2 documents** (and 0 for the held S118
document). The only topical hit is `灰色文献` 1, which is the S125-labelled row described in §4.3 — a different
URL (gcpunion.org, lane S124), so it neither quarantines nor clears any C2 document.

Not run, by wave rule: builds, linters, tests, formatters; no network or live fetch; no lane write, no git/jj
mutation; no reads outside the on-disk captures and the named registries.

VERDICT: attacked the section-10 collision check — reg-ids (126), staged-ids (114), collisions (45) and the
24-line quarantine slice all reproduce byte-for-byte (sha256-equal) at 46e1758f, the 0-3-space guard holds on
an indented fixture with a documented 4-space edge and a load-bearing row anchor, and the four C2 URLs are
absent from the frozen registry with S127-S130 free — the check SURVIVES, with three reporting-only hazards
(id-range overlap with staged S127-S130, staged S156≡S169 duplicate, and staged S130 = the quarantined
gcpunion document).
