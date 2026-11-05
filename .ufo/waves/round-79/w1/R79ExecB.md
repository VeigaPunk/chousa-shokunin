# R79ExecB — C2 reproduction (both directions + controls) from committed bytes

Lane: chousa round 79. Seat: leaf executor. Scope: reproduce the four C2 runs named in the
seat spec against frozen revision `ee70e6df19fe43b1b384166cf5d360c3b99dafe2` (round-78 lane
tip) and the current worktree. No lane/fleet mutation, no commits, no tooling installed
(authorization unused — stock `python3` 3.14.8 sufficed). Scratch
`/fast/scratch/hyaku/chousa-r79/R79ExecB/` created, used only for the control battery's
`--work` mirrors, and deleted before this report was finalized.

## Result: all four predicates reproduced exactly, zero deviations

| run | command (abridged) | expected | observed | exit | receipt |
|---|---|---|---|---|---|
| (a) BEFORE | `selfcheck-v2.py --lane <lane> --rev ee70e6df… --digests` | `SELFCHECK2=FAIL unresolved=3/3`, S1=168, S2=116, S3=73, 3 DIGEST lines | identical | 1 | `.ufo/waves/round-79/w1/R79ExecB/a-before-selfcheck2-rev-digests.txt` |
| (b) AFTER | `selfcheck-v2.py --lane <lane>` (worktree) | `SELFCHECK2=PASS unresolved=0/3` | identical | 0 | `.ufo/waves/round-79/w1/R79ExecB/b-after-selfcheck2-worktree.txt` |
| (c) predecessor | `round78/selfcheck.py --lane <lane> --rev ee70e6df…` | `SELFCHECK=PASS unresolved=0/3` | identical | 0 | `.ufo/waves/round-79/w1/R79ExecB/c-v1-before-rev.txt` |
| (d) controls | `selfcheck-control.py --lane <lane> --work <scratch>/mirrors --base ee70e6df…` | `CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2` | identical | 0 | `.ufo/waves/round-79/w1/R79ExecB/d-control-mirrors.txt` |

All receipt paths above are relative to the lane root
`/home/vgpnk/Projects/shokunin/chousa-shokunin`.

## Predicate lines, verbatim

(a) BEFORE, at base rev with digests — all three classes unresolved, one DIGEST line each:

```
DIGEST correction: SKILL.md:168 cells=7 digest=e6e751ec67878243
CHECK S1-skill-registry FAIL header_cells=8 malformed=[168] repairs=[] unresolved=[168]
DIGEST supersedes: 116 digest=ae134338138ad3e0
CHECK S2-quality-pointers FAIL criteria=49 missing=[116] superseders={} unresolved=['116:corpus/evidence/round59/claims.md']
DIGEST erratum: round-77.md:73 digest=7f2d54a7eb33df54
CHECK S3-lesson-mistakes FAIL mistakes_width=4 stranded=[73] errata=[] unresolved=[73]
SELFCHECK2=FAIL unresolved=3/3
```

exit 1. S1 row 168, S2 criterion 116, S3 round-77 line 73 — exactly the three classes the
frozen claims.md names.

(b) AFTER, current worktree:

```
CHECK S1-skill-registry ok header_cells=8 malformed=[168] repairs=[168] unresolved=[]
CHECK S2-quality-pointers ok criteria=50 missing=[116] superseders={116: [149]} unresolved=[]
CHECK S3-lesson-mistakes ok mistakes_width=4 stranded=[73] errata=[73] unresolved=[]
SELFCHECK2=PASS unresolved=0/3
```

exit 0. Each class is resolved by a repair line (168 repaired; 116 superseded by 149; 73
erratum).

(c) predecessor round-78 counter on the same base bytes:

```
CHECK S1-skill-registry ok
CHECK S2-quality-pointers ok
CHECK S3-lesson-mistakes ok
SELFCHECK=PASS unresolved=0/3
```

exit 0 — the old counter cannot see what the successor sees, as claimed.

(d) control battery (work contained in scratch):

```
CASE hollow v1 rc=0 SELFCHECK=PASS unresolved=0/3
CASE hollow v2 rc=1 SELFCHECK2=FAIL unresolved=3/3
CASE window v1 rc=0 SELFCHECK=PASS unresolved=0/3
CASE window v2 rc=1 SELFCHECK2=FAIL unresolved=3/3
CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2
```

exit 0. Both false-green channels (hollow repair line; newer `## Round-<n> addition` block
hiding an earlier criterion) reach PASS on the predecessor and are refused by the successor —
matching the frozen `controls/selfcheck-control-before.txt` description.

## Instrument integrity

`sha256sum` over the three instruments I executed matches the frozen digest table in
`corpus/evidence/round79/claims.md` exactly:

- `corpus/evidence/round79/selfcheck-v2.py` → `b99ccee5b20bb29c2e0ab83e6db39ba038b5ab501c1e7e1630054a5f88ffeed2`
- `corpus/evidence/round79/selfcheck-control.py` → `00cf811a686e885d7c426c0b6d9ad4c17308e42cb3d9d937d6f200deb9f4499d`
- `corpus/evidence/round78/selfcheck.py` → `f5acdd825ab7dcafa1385ad2b9a6c22df848c4e856947746cd006c22837bf9af`

## Findings

None. Every predicate line, unresolved class, and exit code matches the frozen claim set.
No post-freeze deviation to report; nothing repaired (frozen artifacts untouched; all
receipts written into my own output folder).

## Housekeeping

- Files written: the four receipts above plus this report — nothing else outside scratch.
- Scratch `/fast/scratch/hyaku/chousa-r79/R79ExecB/` (mirrors: `mirror-hollow`,
  `mirror-window`, both git toplevels verified under scratch) deleted before yield.
- No tool installs/updates performed; pacman guard respected trivially.
