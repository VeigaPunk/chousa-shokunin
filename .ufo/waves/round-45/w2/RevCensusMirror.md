# RevCensusMirror — round 45 wave 2 review

Seat: L1Chousa45.RevCensusMirror (leaf, reviewer)
Item under attack: wave-1/L1 census artifacts — mirror SOURCES.md at
`.ufo/waves/round-45/assimilation/validate/corpus/SOURCES.md` vs live registry
`corpus/SOURCES.md`; S082–S084 rows; E03/E04 absence; 84-row registry.
Verdict: **HOLDS** (narrowed: 5 W04 warnings are present in both files, per
contract warning-only, exit 0).

## 1. validate --file (mirror)

Command:
```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file \
  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-45/assimilation/validate/corpus/SOURCES.md
```
Output (verbatim), exit code:
```
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-45/assimilation/validate/corpus/SOURCES.md
RC=0
```
No E01–E12 findings (no `E03`, no `E04`). Exit 0 = clean-or-warnings per usage.

## 2. validate --root (live registry via conf lane)

Command:
```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
```
Output (verbatim), exit code:
```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
RC=0
```
`chousa` resolves to `chousa-shokunin` via `shokunin.conf` LANES (line 67:
`chousa|chousa-shokunin|…`). No E03/E04, no E-codes at all. W04 set is
identical to the mirror's.

## 3. S082–S084 mirror vs live

Cell-level parse (split on `|`, trim; full 13-cell rows incl. `teaches`/
`used-by`): all three rows **IDENTICAL** between mirror and live registry.
- S082: IDENTICAL
- S083: IDENTICAL
- S084: IDENTICAL

## 4. Row count (0–3-space pattern)

- Pattern count on committed bytes (5e8c7ad2f7b8254d83358820286e3d12ca4672d1
  archive): `grep -cE '^ {0,3}\| S[0-9]{3,} ' corpus/SOURCES.md` → **84**.
- Census tool on live file: `file rows 84`; tier A=78, B=1, C=5;
  status mined=60, queued=19, rejected=5; FLEET rows=84, missing=0; RC=0.
- Python parse (same 0–3-space pattern): live 84, mirror 84, IDs S001–S084.
- Live `corpus/SOURCES.md` is byte-identical to the committed tree copy
  (`cmp -s` → RC 0), so the 84-row count holds at the commit too.

## Evidence pointers
- Script row pattern/indent rule: `scripts/sources-census.sh:40-42` (0–3
  spaces), `row_pass` `:606-694` (E03 at 641, E04 at 646-649), exit table
  `:16-18`, validate main `:737-746`.
- Mirror: `.ufo/waves/round-45/assimilation/validate/corpus/SOURCES.md`
  (S082 line 92, S083 line 93, S084 line 94; 84 rows).
- Live: `corpus/SOURCES.md` (S084 line 94; 84 rows).
- Wave-1 recorded census: `.ufo/waves/round-45/assimilation/validate-census.txt`
  — identical 5×W04 + ok + exit 0; my reruns match it exactly.
- Conf lane: `shokunin.conf:67`.

## Residual risk / gaps
- W04 (URL duplicated across scopes: S051/S053/S073/S074/S075) is present in
  both mirror and live; by contract W-codes never change status — flagged, not
  a defect in the claim.
- No network/live fetches performed (none needed); no lane/registry writes;
  scratch `/tmp/chousa-r45-RevCensusMirror` deleted.
