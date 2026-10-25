# ExecMirrorCensus — pre-append census mirror procedure (round 47, wave 1)

seat: L1Chousa47.ExecMirrorCensus (leaf executor) · date: 2026-10-25 · lane HEAD `a15610a5`
item: write `/tmp/chousa-r47-ExecMirrorCensus/mirror.sh` (copy corpus/, append rows directly
after the last S-row with no blank line, replace held S085, copy entries in, run
`scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md`); test with placeholder
S090–S094; prove E04 fires on an in-scope duplicate of S085's URL. Claims served: C3 (registry
rows for S085/S090–S094). No lane file, git index or jj state touched; no fetch, no install.

## Axes and kept moves
- **operability**: one command, inputs as files, exit = census exit, 2 = input refused.
- **calibration**: the gate is shown failing (E04, E11) and its boundary mapped (W04, supersedes).
- **depth**: placeholder anchors carry real capture offsets, each re-sliced byte-exact.

## Artefact (kept; the requested deliverable)
`/tmp/chousa-r47-ExecMirrorCensus/mirror.sh`: 121 lines, sha256 `6b16bfff…0994`
(`6b16bfffdc4c11fda369be4878e59dd1f8d9bbb779ac775b22c9ac795acf0994`), `bash -n` ok, `shellcheck`
silent. The full script is in this seat's final result to the L1; this report keeps only
its behavior to stay under 150 lines.
- `--out DIR` (must be empty or absent); `cp -a <lane>/corpus DIR/corpus`.
- `--replace FILE`: each row replaces the `## Registry` row with the same id. Refused (exit 2)
  unless the id matches exactly one row.
- `--rows FILE`: inserted right after the last `| S###` row inside `## Registry`. Every input
  line must match `^\| S[0-9]{3,} \|`; a blank line or CR is refused (exit 2). This is
  round-46 RevC3Rows F7.
- `--entry PATH` (repeatable) is copied to `DIR/corpus/knowledge/<basename>`.
- Mined used-by paths outside `corpus/` are copied from the lane when present. Today that is
  only `tools/quarantine-check.py` (S077). Without it, E11 would be a copy-scope artefact
  (round-45 mistake 3).
- Post-check: the header row through the last S-row must all be `|` lines. It prints the line
  range, row count, the next line and the sha256, then the census output and `census exit=N`.
Inputs kept beside it: `rows-s090-s094.txt` (`85544c81…`), `replace-s085.txt` (`9a89bfef…`),
`rows-e04.txt` (`ee08e5d6…`).

## Placeholder rows (11 cells, NF=13, `mined`, opened 2026-10-25, recheck 365d)
URLs are the six Context URLs. Scope cells come from staged S098/S099/S113–S115. Anchor and
teaches cells are marked `PLACEHOLDER`, so these rows are not for append. Each `char N` was
located in the `.qcache` capture and re-sliced (`t[o:o+len(q)]==q` True for all five):
S090 80040 `Definition 1: “Supporting evidence”:` (cache 4132ec1b…, 91084 B) · S091 827 `30,012`
(3749141b…) · S092 59949 `world-knowledge by basing your decisions` (b502d4c6…) · S093 5157
`7,675 annotated claim-evidence pairs` (44be8711…) · S094 21583 `0.792, indicating substantial`
(a9cf4170…). used-by: S090/S091 → `claim-support-test-r37.md`; S092–S094 → `…-amendment-2026-10-23.md`.
S085 replacement: the held row verbatim, with `, corpus/knowledge/claim-support-test-r37.md`
added to its used-by (NF=11). Entries are the staged stand-ins from
`/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`, because the lane
holds neither yet.

## Command log (verbatim, W04 lines trimmed where marked)
Run A, the requested test:
```
$ bash mirror.sh --out m-a --rows rows-s090-s094.txt --replace replace-s085.txt \
    --entry $K/claim-support-test-r37.md --entry $K/claim-support-test-r37-amendment-2026-10-23.md
mirror: used-by outside corpus/: tools/quarantine-check.py (copied)
mirror: /tmp/chousa-r47-ExecMirrorCensus/m-a/corpus/SOURCES.md registry lines 9-104 contiguous, rows=94, next line 105: ## Paths
mirror: sha256 01f14a5b2c96c4fa42ae55c8a8684d11ef1a5195d677fce86545ded9ea624aaf
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/tmp/chousa-r47-ExecMirrorCensus/m-a/corpus/SOURCES.md
census exit=0
```
**No E03, E04 or E11 lines.** The five W04 lines are already in the lane (same set as
round-46 ExecRegistryMirror). `diff lane mirror` shows `95c95` (S085) and `99a100,104` (S090–S094),
and nothing else. S094 sits at line 104 and `## Paths` at 105, with no blank line between them.

Run B, the E04 falsifier. S095 has S085's URL and S085's scope cell byte-for-byte, is `mined`,
and has no `supersedes`. Placed first in `rows-e04.txt`, followed by S090–S094:
```
$ bash mirror.sh --out m-b --rows rows-e04.txt --replace replace-s085.txt $E | rg -v W04
mirror: used-by outside corpus/: tools/quarantine-check.py (copied)
mirror: /tmp/chousa-r47-ExecMirrorCensus/m-b/corpus/SOURCES.md registry lines 9-105 contiguous, rows=95, next line 106: ## Paths
mirror: sha256 52fa75f27856f979101f8ba1baf7b16f5faafe2bce6a07d6071112991c0dc2d7
file	E04	S095 duplicate url fever.ai/dataset/fever.html within scope what a support verdict is bound to in the FEVER release format, and what that binding does not carry
census exit=1
```
**The gate can fail: E04 fires and the exit code is 1.**

Boundary controls on throwaway mirrors (deleted):
```
C  same S095, scope cell changed  -> file	W04	S095 duplicate url fever.ai/dataset/fever.html across scopes ; census exit=0
D  same S095, teaches "supersedes S085" -> (no S095 line) ; census exit=0
E  run A without --entry          -> file	E11	S085 missing used-by corpus/knowledge/claim-support-test-r37.md
                                     (also E11 for S090, S091 on -r37.md and S092, S093, S094 on -amendment-2026-10-23.md) ; census exit=1
F  --replace with id S199          -> mirror: replace S199 matched 0 registry rows ; mirror.sh exit=2
G  rows file with a blank line 2   -> mirror: rows-blank.txt:2 blank line (would split the table) ; mirror.sh exit=2
```
Lane untouched: `sha256(corpus/SOURCES.md)` =
`c69c75bd7719689cb71b307bc3bb22a2cec4ad1b328f4b8a5269b3676d7a6274` after all runs. `git status
--short corpus/ tools/` shows only the pre-existing `M corpus/evidence/round41/receipts/cells/cells.json`.

## Verdict
- **The procedure works.** Run A exits 0 with no E-code over 94 rows (89 held + S090–S094), with
  S085 replaced in place and the table contiguous.
- **The gate is not vacuous.** E04 is proven live by run B. E11 is proven live by control E,
  which also shows the `--entry` copy-in is load-bearing.

## Findings / risks for the L1
1. **E04 is scope-string keyed (control C).** A row with the same URL but a different `scope`
   cell gets only a W04, which never changes the exit code. The six real rows must keep a scope
   distinct from any held row at the same URL. Only S085's URL is held today (lane
   `SOURCES.md:95`). The other five URLs occur 0 times in the lane.
2. **The `supersedes S###` escape is unchecked (control D).** Any row whose `teaches` cell
   contains `supersedes S085` silences E04 while S085 stays `mined`. The census does not
   require the superseded row to be `rejected` (`sources-census.sh` E04 clause, the
   `teaches !~ /supersedes S[0-9]{3}/` test). This is a fleet-script property, so I did not
   modify the script and only report it.
3. The census reads neither the anchor cells nor the entry `S###` tokens. The stand-in entries
   still cite staged S097–S099/S113–S115. Re-run `mirror.sh` with the scribes' drafts and the
   real row file before append. C3's `ANCHOR_BOUND` leg, not this census, checks `char N`.
4. `--replace` rewrites any id it is given, not only S085. The held-S085 restriction is the
   caller's input discipline.

Not done (out of scope): no append to the lane, no row prose, no entry edits, no labrat
spawned, no tool installed. The throwaway mirrors m-a … m-g and the control inputs were deleted.
Kept: the script and the three input files above. Checks for the L1: re-run run A and run B
with the final row file.
