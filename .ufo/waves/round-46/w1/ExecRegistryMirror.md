# ExecRegistryMirror — pre-append registry mirror and census falsifiers

seat: L1Chousa46.ExecRegistryMirror (leaf executor) · date: 2026-10-25
item: build the pre-append mirror (corpus/ + tools/ + the two drafted entries + the five
S085–S089 registry rows), validate it with the fleet census, and validate the live lane.
claims served: R46-C3's registry rows (S085–S089 binding) and R46-C2's premise that the
registry absorbs new rows without duplicate ids/urls. No lane production file touched.

## Axes (named before acting) and moves kept

- **calibration** — the mirror must survive the real validator, not a hand check. Kept: run
  `sources-census.sh validate --file`, plus two negative controls that make E11 fire, so
  exit 0 is proven non-vacuous.
- **operability** — one reproducible move: copy, append, validate. No lane state, no git/jj,
  no network.
- **depth** — every row anchor names a capture character offset I opened this round. Kept:
  all eleven offsets verified by `grep -abo` and read back with `dd` before writing.

## Mirror

- root `/tmp/chousa-r46-ExecRegistryMirror/` (kept; it is the requested artefact)
- `cp -a corpus tools` from `/home/vgpnk/Projects/shokunin/chousa-shokunin/`
- two entries copied into `corpus/knowledge/`; registry 84 + 5 = 89 rows
  (`## Registry` line 7, `## Paths` line 101)
- `sha256(corpus/SOURCES.md)` = `0ef863659b09027a31e7d3b098e53df9cccc4f44b6988d41205f52a45b5d7fcc`
- `sha256(tools/quarantine-check.py)` = `8e74549db67a9f2db07e40289a0a7df32f430688fa721be3163cb478d3783dbf`

### Stand-in provenance (stated explicitly)

The wave reports of **ScribeEntryBase / ScribeEntryAmend are absent**. `.ufo/waves/round-46/w1/`
now holds 16 sibling reports but neither of those seats, and no report in it carries a
`source: S08[5-9]` line. So the two entries are **stand-ins**, copied verbatim from the staged
package `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/`:
`evidence-pool-versioning-r39.md` (89 lines) and `-amendment-2026-10-23.md` (83 lines).
Consequence, named as risk: the stand-ins still carry staged ids **S120–S122 / S127–S128**,
not S085–S089; that re-binding is the scribes'/span-builder deliverable, not mine. The census
does not read entry `S###` tokens, so this does not affect the E-code result.

### Rows appended to the mirror's `## Registry`

| id | document | kind | used-by |
|---|---|---|---|
| S085 | FEVER Dataset page — https://fever.ai/dataset/fever.html | dataset | corpus/knowledge/evidence-pool-versioning-r39.md |
| S086 | FEVER NAACL 2018 PDF — https://aclanthology.org/N18-1074.pdf | paper | corpus/knowledge/evidence-pool-versioning-r39.md |
| S087 | FEVER Zenodo record 4925954 — https://zenodo.org/api/records/4925954 | dataset | corpus/knowledge/evidence-pool-versioning-r39.md |
| S088 | AVeriTeC dataset page — https://fever.ai/dataset/averitec.html | dataset | corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md |
| S089 | AVeriMaTeC — https://arxiv.org/html/2505.17978v2 | paper | corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md |

All five `mined`, opened `2026-10-25`, recheck `365d`, NF=13 (11 columns). Row text is re-bound
**by document**, never by staged-id arithmetic.

## Capture binding (no fetch; `sha256(url)[:24].txt` cache, all five printed EXISTS)

`5a631adb18988a1a2421ce75` S085 (4146 B) · `1c15b611118dee97e4105fcf` S086 (60153 B) ·
`7800e2e1e2df3bc124b6b83e` S087 (5676 B) · `b73f7e8dd5b0ace740e48046` S088 (12775 B) ·
`78761b633aee2289e5874ce9` S089 (126093 B); cache dir
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`.

Offsets quoted in the rows: S085 2360 (`A list of evidence sets`), 1271 (`Pre-processed
Wikipedia Pages`); S086 1869 (`0.6841`), 5547 (`31.75`), 5855 (`16.82`), 5942 (`12.15`),
6755 (`95.42`), 6776 (`72.36`), 20546 (`3.4.3 Validation by the Authors`); S087 172 (`doi`),
186 (`conceptdoi`), 4937 (`wiki-pages.zip`, the first of seven `"key":` entries); S088 3929
(`An archive.org link for the source url`), 3185 (`Where possible, an archive.org link`),
2904 (`Our best estimate`), 1080 (`four labels`); S089 3047 (`temporally constrained evidence
annotation`), 3230 (`0.742`), 3265 (`74.7`), 1840 (`arXiv:2505.17978v2`), 1867 (`07 Oct 2025`).
Correction from opening the capture: S086's 31.75/16.82/12.15 percentages sit in the
**Introduction** (before `2 Related Works` at char 8898), and `3.1` is `Task 1 - Claim
Generation`, not an evidence-retrieval section; the row anchors cite offsets, not a section
name the capture does not support.

## Command log

1. Mirror validation (the requested command):
```
$ bash scripts/sources-census.sh validate --file /tmp/chousa-r46-ExecRegistryMirror/corpus/SOURCES.md
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/tmp/chousa-r46-ExecRegistryMirror/corpus/SOURCES.md
EXIT=0
```
No E03/E04/E11/E12. The five W04 lines are pre-existing in the lane and inherited verbatim;
W-codes do not change exit status.

2. Live fleet census (read-only):
```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
```

3. E03/E04 branch: neither fired, so no ids to name. Independent scan: normalizing every URL
   in the mirror (`s#^scheme://##`, lowercase, strip `#frag` and trailing `/`) and listing
   duplicates returns only the five pre-existing pairs above; each of the five new URLs occurs
   exactly once. No id collision is possible (S085–S089 > S084) and the validator's `seen[id]`
   pass reported nothing.

4. E11 branch: not reported, so no mirror fix was needed. It would have fired if a used-by
   target were absent, and the registry does have a `tools/` used-by —
   `S077 -> tools/quarantine-check.py, corpus/lessons/round-42.md`. The mirror carries it
   (`cp -a tools`), which is why E11 stayed silent: the round-45 mistake-3 dependency.

   Negative control A — the same mirror with the two stand-in entries deleted:
```
file	E11	S085 missing used-by corpus/knowledge/evidence-pool-versioning-r39.md
file	E11	S086 missing used-by corpus/knowledge/evidence-pool-versioning-r39.md
file	E11	S087 missing used-by corpus/knowledge/evidence-pool-versioning-r39.md
file	E11	S088 missing used-by corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md
file	E11	S089 missing used-by corpus/knowledge/evidence-pool-versioning-r39-amendment-2026-10-23.md
EXIT=1
```
   Negative control B — the same mirror with only `tools/quarantine-check.py` deleted:
```
file	E11	S077 missing used-by tools/quarantine-check.py
EXIT=1
```
   Both ran on throw-away `/tmp` copies, since deleted; the main mirror still hashes `0ef8636…`.

## Verdict

- **Mirror: EXIT=0** on the real validator over 89 rows including the five new ones; no E-code.
- **Live lane: EXIT=0**, unchanged by this seat (read-only run).
- No E03/E04/E11/E12 anywhere; the E11 mechanism is nonetheless proven live by two negative
  controls, one isolating the round-45 `tools/quarantine-check.py` dependency.
- The five rows are document-bound: capture filename, size and quote offsets are recorded per
  row and were re-derived from the on-disk cache, not from the staged rows.

## Risks / limits (for the L1)

1. The mirror's two entries are **staged stand-ins**, not wave-1 drafts, and still carry
   S120–S122/S127–S128. Re-run the same validate command when the drafts land; E11 catches a
   missing `used-by` target, nothing catches a stale id inside the entry text.
2. Row-grounding was spot-verified (eleven offsets), not re-derived for all row prose; the
   census does not measure row truth (C2's named limit).
3. No fetch, no install, no pacman; writes only under `/tmp` and this report.

Pointers: mirror `corpus/SOURCES.md:95-99` (new rows), `:7`, `:101`; validator
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:567` (E11), `:641` (E03), `:649`
(E04), `:500-501` (`--file` root resolution).
