# R53ConnCrossClaim — cross-claim / cross-fleet pattern (wave 1)

Seat: R53ConnCrossClaim (leaf). Read-only lane work; the only experiment is in my scratch
`/fast/scratch/hyaku/chousa-r53/R53ConnCrossClaim/`. No tools installed. Frozen claims read at
`corpus/evidence/round53/claims.md:1-143`; commits checked: HEAD `6365f15` (wave-1 dispatch),
candidate v4 `32aab5e` (parent of HEAD), freeze `a6ff732`, base `5b55013` (all present, `git cat-file -t`).

## Q1 — W04 vs twin: same defect? registry-level check?

Evidence A — current W04 state (census validate, exact row parser, exit 0):
```
$ sources-census.sh validate --today 2026-10-26 --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	.../corpus/SOURCES.md   (exit=0)
```
All five have recorded dispositions (`corpus/evidence/round41/w04-dispositions.tsv:4-8`): S051/S053/S075
same-page-distinct-section, S073 supersede-row-required (correction for S070), S074 retained-rejected-duplicate.
Census-identity URL repeats in the registry (python over SOURCES.md using the script's own url_of,
`sources-census.sh:600-605`): S050/S051, S052/S053, S059/S074, S071/S073/S075, S019/S029, S020/S033,
S021/S032, S022/S030, S024/S031. W04 fires only when the repeat changes scope; supersede pairs with the
same scope are silent (E04-exempt, `sources-census.sh:644-649`). W04 = **committed-registry state,
contract-sanctioned, warning-only (never fails the lane)**.

Twin (adopter v4) = **intake-time collapse**: a second staged row whose URL this run already minted maps to
the same lane id, no append (`tools/assimilate-rows.py:26-34,483-493`). So W04 and twin are not the same
defect: W04 is a permitted multi-row registry state; twin prevents a package from *creating* one. They share
the identity axiom (URL = document identity) and meet at `held`.

Evidence B — the meeting point is silent on multi-carrier registries. The `held` map is
`held.setdefault(u, sid)` over all registry rows sorted by id (`assimilate-rows.py:475-479`): when a URL is
carried twice (a W04 state) the lowest-numeric carrier wins, nothing surfaced. Experiment (scratch fixture:
registry with S070+S075 both carrying the coreutils URL, staged S200/S201 citing it):
```
$ python3 tools/assimilate-rows.py --staged … --knowledge … --registry … --opened 2026-10-26 --out … --entry corpus/knowledge/e.md
COLLISIONS=0 CITED=2 APPEND=0 HELD=2 TWIN=0 BODYONLY=0   (exit=0)
$ cat out/renumber.tsv
S200	S070	held	www.gnu.org/software/coreutils/manual/coreutils.html
S201	S070	held	www.gnu.org/software/coreutils/manual/coreutils.html
```
No warning that two registry rows carry the URL; both collapse to S070. The registry-level duplicate check
exists (census E04/W04) but runs outside the adopter and only over committed bytes.

Recommendation (one bounded proposal, no predicate/axis change): give v4's twin identity rule a
registry-level face — in the `held` pass, when n>1 registry rows carry the same census URL, still hold to the
first (unchanged mapping, unchanged counts) but emit one stderr `WARN` listing the carriers, exactly like the
existing bodyclash WARN (`assimilate-rows.py:561-562`); optionally print `HELD_MULTI=<n>` on the count
line. Intended lane path `tools/assimilate-rows.py` (draft below; L1 integrates):
```python
# after the held loop (assimilate-rows.py:475-479)
carriers = {}
for sid in sorted(base, key=num):
    u = url_of(pipe_free(base[sid][1])) if len(base[sid]) > 1 else ""
    if u:
        carriers.setdefault(u, []).append(sid)
        held.setdefault(u, sid)
multi = {u: ids for u, ids in carriers.items() if len(ids) > 1}
for u, ids in sorted(multi.items()):
    print(f"WARN url {u} carried by {','.join(ids)}; holding to {held[u]}", file=sys.stderr)
```

## Q2 — other lanes' section-10 adopters and the twin-label defect

`grep -rln 'SOURCES.append.md' /home/vgpnk/Projects/shokunin/*-shokunin/tools /home/vgpnk/Projects/shokunin/*-shokunin/corpus/evidence | head` → only **kama** tools (`round37/round38-statement-audit.py`) and chousa evidence.
Only chousa has an adopter (`chousa-shokunin/tools/assimilate-rows.py`; no sibling tools dir has an
assimilate/renumber tool). kama's counter reads the staged package directly at pinned absolute lines
(`kama-shokunin/tools/round38-statement-audit.py:33,39` `STAGED_LINES=(9,13,14,15,16)`, used at
`:76-83`): it labels nothing, so the twin-label defect class (base mislabels `held` with no registry row,
cf. `claims.md:66-67` before control) cannot exist there. Closest sibling mechanism is tameshi's pre-adoption
guard, whose `held` dedupes colliding staged ids to the registry id, form-insensitively
(`tameshi-shokunin/tools/staged-id-guard.py:21-24,65-67`) — correct held semantics, but no same-run twin
concept. Cross-fleet staged packages carry many repeated census URLs (scan over `/home/vgpnk/Projects/shokuknow/merge/*/SOURCES.append.md` with the census url_of): e.g. mori 15 dup groups, kumitate 17, mado 15, kagi 18, tameshi 3 (incl. 43 rows under github.com/VeigaPunk/tameshi-shokunin), chousa 10 (incl. the C2 pair S185/S195 — both carry byte-identical `https://www.bjhea.org.cn/.../1736907153935975.pdf`, lines 110/120). No sibling grep `twin` in tools/corpus (only kotodama `.d2.yml` fixtures). Verdict: the twin-label defect is unique to chousa's adopter; siblings never label, so they cannot exhibit it; v4 fixes the only instance.

## Q3 — representation variance in other frozen counters

Variance is a live fleet class; siblings handle it unevenly:
- chousa round-50 frozen counter treated a **2-space-indented registry row as a mutant** (`round50/c1-count.py:11,107` P1 expects `DIFF missing COLLISIONS S011,S012`, exit 1); round-53 C1 is the first to randomize representation *inside* the frozen counter (`round53/c1-count.py:96-105,138-142`: scheme, trailing slash, host case, 0-3 indent, `##`+space/tab).
- tameshi documents the column-zero blindness as a defect and fixes it: `staged-id-guard.py:14-16` ("the column-zero pattern misses an indented row"), ROW_RE `^ {0,3}\|` (`:65`), proof fields `column0_collisions`/`column0_miss` (`:52,280`).
- souji: `souji-registry-agreement.py:13` notes 4+space/tab-indented rows are silently ignored; ROW `^ {0,3}\|` (`:27`) + INDENTED detector (`:46,68-69`).
- kotodama is column-zero-blind: `check-row-fragments.py:41` `ROW_RE = ^\|\s*(S\d+)` — no 0-3 indent.
- kama's frozen counter is the opposite design: byte/line-pinned (`round38-statement-audit.py:33-39,76-83`), zero variance tolerance.
- tsukuroi headings accept 0-3 spaces and `[ \t]+` (`check-registry-coverage.py:52-54`), matching the census parser (`sources-census.sh:40-42,609`). My own naive URL scan (keeping fragments/trailing slash/scheme) missed the true repeat set — the census's `url_of` normalization (`sources-census.sh:600-605`) is the fleet identity standard; comparisons should reuse exactly it.

## One recommendation (consolidated)

Adopt census `url_of` + the 0-3-space/`[ \t]` row grammar as the shared identity axiom everywhere and add
the multi-carrier `WARN` (Q1) to the adopter's held pass; both are additive and touch no frozen predicate
(C1 counters still count HELD/TWIN identically; C2 untouched).

VERDICT: attacked the W04-vs-twin relationship (same URI axiom, different layers: committed registry state vs intake collapse), demonstrated with a scratch dual-carrier run that v4's held pass silently picks one carrier, found the twin-label defect confined to chousa (siblings have no labeler; kama pins lines, tameshi guards collisions), and mapped representation-variance handling across sibling counters — one bounded proposal: registry-level multi-carrier WARN reusing census url_of.
