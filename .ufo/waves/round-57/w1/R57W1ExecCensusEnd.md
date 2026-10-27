# R57W1ExecCensusEnd — round-57 chousa census measurements (wave 1)

seat: `R57W1ExecCensusEnd` (executor) · date: 2026-10-27 · lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`
base `6656f0770a1460d6ba73d9d2976f698a35311921` · lane HEAD at measure `a03824d1a0c70278b33cca4ae4e2b8d6d9691e70`
freeze commits verified present: R57-C2 `c2f914c53201a8f8ee4fef823b82681051d55592`, R57-C3 `fd95724d56a33ad150cd263f8add2ce1f3425e6c`
(the dispatch text gives R57-C3 as `fd95724d56a33a150cd2638fadd2ce1f3425e6c` — 3 chars differ from the real object `fd95724d56a33ad150cd263f8add2ce1f3425e6c`; the real commit is the one in the lane, see `git rev-parse fd95724`.)

No tooling was installed or upgraded for this seat (bash/coreutils/gawk/git already present).

## 1. Maintained CLI census — `scripts/sources-census.sh validate --root … chousa`

```
$ cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa; echo "EXIT=$?"
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
```

`census` mode (same script) — for the FLEET aggregation line:

```
$ bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa
chousa	rows	130 … tier.A 106 tier.B 19 tier.C 5 … status.mined 106 status.queued 19 status.rejected 5
FLEET	rows	130 … FLEET.tier.invalid 0 FLEET.status.invalid 0 FLEET.missing	0
EXIT=0
```

`overdue` mode → 130 `cadence` lines (every recheck is symbolic/NNd; no ISO date due) → `EXIT=0`.
`bash scripts/sources-census.sh selftest` → `selftest ok`, `EXIT=0`.

## 2. Frozen manual census block (CORPUS.md §“SOURCES.md — where a shokunin learns”, lines 133–148), run from the lane root

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
# rows (spacing-tolerant)
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md        → 130   EXIT=0
# malformed rows — must print 0
awk -F'|' … NF!=13 …                                                            → 0     EXIT=0
# tier histogram
awk -F'|' … t=$5 …                                                               → A=106 B=19 C=5     EXIT=0
# status histogram
awk -F'|' … s=$9 …                                                               → mined=106 queued=19 rejected=5  EXIT=0
# duplicate ids — must print nothing
awk -F'|' … | sort | uniq -d                                                    → (empty)  EXIT=0
# enum violations and tier inflation — must print nothing
awk -F'|' … NF==13 … tier/status/kind/tier-inflation                             → (empty)  EXIT=0
# mined rows whose used-by paths do not exist — must print nothing
awk -F'|' … status==mined … | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done → (empty)  EXIT=0
```

**Cwd caveat (measurement artifact, not a lane defect).** The used-by existence check resolves
repo-relative paths against the *current directory*. Run from the fleet root the same block prints
`118` false `missing:` lines; run from the lane root it prints `0`. CORPUS.md says “run from the lane
root”, so the lane-root number is the contract-conformant one. The same trap applies to the CLI's
`--file` mode: `scripts/sources-census.sh:496` sets `dir_abs = dirname(file)/..`, so validating a bare
copy of `corpus/SOURCES.md` in a scratch dir emits 118 `E11 … missing used-by` findings. Reproduced
both ways, then reproduced as clean by mirroring the registry as `<mirror>/corpus/SOURCES.md` with
`corpus/knowledge`, `corpus/lessons`, `tools` alongside (then: same five W04, `file ok`, `EXIT=0`).

## 3. `grep -c '^| S'`

```
$ grep -c '^| S' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
130
EXIT=0
```
130 = the spacing-tolerant row count ⇒ every registry row sits at column zero with the literal `| S`
prefix. Supporting counts: rows with 1–3 leading spaces = 0; row-shaped lines outside `## Registry`
(E12) = 0; rows with `NF>13` = 0; id sequence `S001…S130` with no gaps and no duplicate ids.

## 4. Defect candidates for the L1 (every non-zero count)

**D1 — `S077`'s `used-by` names a file that does not cite the row (1 of 118 pairs).**
Contract: “`used-by` — repo-relative paths of the **knowledge entries or lessons citing the row**”.
`S077`'s cell is `tools/quarantine-check.py, corpus/lessons/round-42.md`.

```
$ awk -F'|' … status==mined … print id"\t"p …   # 118 (id, used-by path) pairs
$ grep -c 'S077' tools/quarantine-check.py   → 0
$ grep -c 'S077' corpus/lessons/round-42.md  → 6
$ grep -oE 'S[0-9]{3}' tools/quarantine-check.py | sort -u   → (no S### token at all)
```
`tools/quarantine-check.py` exists (so E11 and the manual existence check both pass) but cites no
`S###` id and is neither a knowledge entry nor a lesson — the only such path among all 118 pairs
(109 `corpus/knowledge/*`, 8 `corpus/lessons/*`, 1 `tools/*`). Introduced with the row in round-42
(`git log -S 'tools/quarantine-check.py' -- corpus/SOURCES.md` → `e0f4895`), unchanged since.
Evidence that no `S###` mined row is left uncited at all: every other mined row has ≥1 used-by path
whose text contains its own id (checked over all 118 pairs; the only failure is this one).
Not patched here — reporting only.

**D2 — the five `W04` warnings are pre-existing, unchanged, and are a URL-normalization artifact.**
`corpus/evidence/round57/census-start.txt` (frozen with the R57-C2 commit `c2f914c`) is
**byte-identical** to `corpus/evidence/round56/census-end.txt` and to my measurement:
```
sha256  09ce4a959ddba208da141bc97e872fd5eb36fd428390a1ecf8cf741853016207  corpus/evidence/round56/census-end.txt
sha256  09ce4a959ddba208da141bc97e872fd5eb36fd428390a1ecf8cf741853016207  corpus/evidence/round57/census-start.txt
```
Cause: `scripts/sources-census.sh:602` (`sub(/#[^ ]*$/,"",u)`) strips the URL fragment, so distinct
anchors on one page collide — S050/S051 (`#optional-tags` vs `#the-in-head-insertion-mode`),
S052/S053 (`#socket-timeouts` vs `#socket.create_connection`), S071/S073/S075 (`#env-u`/`#cksum-c`/
`#mktemp-d` of one coreutils manual), plus S074 (a `rejected` row that deliberately re-cites
`hashlib.html`, already held by S059). Exit is 0 (W-codes never change status), and the round-56
closure already recorded the same five. **No census regression this round.**
Latent sub-point worth the L1's attention: S073's `scope` cell says “the same scope as S070” but
writes different literal scope text, and the script's E04 key is `url SUBSEP scope` (literal), so the
`supersedes` exemption in `teaches` can never be reached for that pair — a false-negative in E04
detection, not a lane-data defect.

**D3 — the manual census's used-by check is cwd-sensitive** (see §2). Not a lane defect; a trap for any
seat that runs the frozen block from the fleet root and reads 118 as a failure count.

**Census is otherwise clean:** malformed 0, duplicate ids 0, enum violations 0, tier inflation 0,
mined-used-by-missing 0, no E-code of any kind in the CLI run (only the five standing W04), `rows`
identical at base `6656f07` (130) and at HEAD (130), `git diff --stat base HEAD -- corpus/SOURCES.md`
empty ⇒ **zero registry drift during round 57 wave 1 so far**.

## 5. Frozen-counter state observed at measure time (context, not my seat's claim)

```
$ python3 corpus/evidence/round57/c2-count.py
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS   EXIT=0
$ python3 corpus/evidence/round57/c3-count.py
ENTRY=no S127_CITED=no NEW_GROUND=no CLAUSE=no … BOUND=0/7 (min 4) … C3=FAIL                                                    EXIT=1
```
The C2 number moved **during** this seat's run (46/47 FAIL at ~08:33Z → 47/47 PASS at 08:36Z): the
L1's fetch pass appended attempt-2/attempt-3 rows to `corpus/evidence/round57/refetch.tsv` (file mtime
05:35:49 local, 107 rows at 08:36Z) — S105 gained a 3rd failed attempt, S133 an attempt-2 success
(`c4bedad5…` matching the stored raw). `refetch.tsv` is therefore a moving input; any receipt the L1
writes must be taken after the fetch pass settles. C3 is at its expected pre-build state (entry absent).

## 6. Scope / hygiene

Only writes: this report file, plus scratch under `/fast/scratch/hyaku/chousa-r57/R57W1ExecCensusEnd/`
(scratch deleted before yield — `rm -rf` on that directory, confirmed). No lane file, no fleet-root
tracked file, no sibling lane, no `shokuknow` file was written or modified; the lane's working tree
shows only the L1's own in-flight fetch artifacts and other seats' w1 reports. No git mutation
(`commit/add/stash/checkout/reset/push`) anywhere; the frozen counters were executed read-only and
never edited. No network fetch was performed — only committed bytes under `corpus/captures/` were read.

VERDICT: the round-57 chousa census (CLI validate, the frozen manual block, and `grep -c '^| S'`)
survives — exit 0 / 130 rows / zero malformed, duplicate-id, enum and dangling-used-by counts, byte-identical
to the round-56 close; the only non-zero findings are the five standing W04 duplicate-URL warnings (a
fragment-stripping artifact, pre-existing) and one genuine defect candidate, D1: S077's `used-by` cites
`tools/quarantine-check.py`, which exists but contains no `S###` id and is neither a knowledge entry nor a lesson.
