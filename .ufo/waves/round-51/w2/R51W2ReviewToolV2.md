# R51W2ReviewToolV2 — wave-2 attack on `tools/assimilate-rows.py` v2 (round 51)

Diff `git -C … diff 2a3389da 4436e279 -- tools/assimilate-rows.py` (43+/14-), docstring L1-83, body L124-492. No
`lsp` device is mounted (`read xd://lsp` → "No such tool"), so caller/definition checks are runtime repros plus line
reads. Scratch `/dev/shm/chousa-r51-R51W2ReviewToolV2/` (removed). No tool installed; counters run `env -u ASSIMILATE_CITES`.

Baseline at the tip (what holds):
```
$ python3 corpus/evidence/round51/c1-count.py --seed 51
SELFTEST_DEFAULT=PASS · LEGACY_ALL=PASS rc=0 · SOURCE_ONLY=PASS map=['S757','S782'] appended=1 bodyonly=[['corpus/knowledge/e.md','S582']] all_rc=0 · PIPE_IDENTITY=PASS d1=ok d2=ok · REGISTRY_STRUCTURE=4/4 · LEGS=5/5 · C1=PASS
$ python3 corpus/evidence/round51/c1-supplement.py → SHAPE/MUTATION/CROSS_ENTRY/SOURCE_LINE/UNKNOWN_SRC/CLASH=3/3 · LEGS=6/6 · C1_SUPPLEMENT=PASS
$ python3 tools/assimilate-rows.py --staged …/merge/chousa/SOURCES.append.md --knowledge …/merge/chousa/knowledge \
    --registry corpus/SOURCES.md --opened 2026-10-25 --out $S/live --entry <three staged entries>
COLLISIONS=31 · WARN×5 (S097,S105,S106) · CITED=7 APPEND=1 HELD=6 · BODYONLY=5 · rc=0
renumber: S109→S107 · S110→S108 · S116→S109 · S117→S110 · S119→S111 · S126→S112 (all held) · S125→S113 append
```
Same-identity rerouting holds: the held map is exactly S109→S107 … S126→S112; S125 (the `.docx`) is the single
`append` and the lane refused it by hand — the tool has no docx rule, so its own output would have violated C2's
refusal clause if pasted.

## Wave-1 F1-F7 re-check at v2
**F1 HIGH cross-entry bleed — FIXED.** `a.md` cites S010, `b.md` mentions it only in its body (`f1`): `$ … --entry
corpus/knowledge/a.md --entry corpus/knowledge/b.md` → `rc=0 CITED=1 APPEND=1 BODYONLY=1`; `renumber S010→S003
append`; `bodyonly b.md S010`; `append used-by corpus/knowledge/a.md`; `OUT b.md` keeps `S010`. L465
`subst(tx, set(source_ids(tx)))` and L467-471 are right.

**F2 MEDIUM ambient `all` — changed shape: disclosed, not fixed.** `round50/c1-count.py` → `BASELINE=FAIL rc=1 ·
R49_REGRESSION=FAIL · LEGS=3/5 · C1=FAIL`; with `ASSIMILATE_CITES=all` → `SELFTEST_DEFAULT=FAIL · LEGS=4/5`; `round49`
→ `SETS_PASS=3/3 C1=PASS`; `ASSIMILATE_CITES=all … --selftest` → `SELFTEST=FAIL findings=36 expected=27`. Docstring L69-74
states exactly this and the claims call it "not part of the predicate (disclosed)"; the frozen C1 needs only an explicit
`--cites all`, which passes. No C1 violation.

**F3 MEDIUM `source_ids` scan — FIXED for the three cited shapes, narrowed to one header form.** Tail token
`source: S010 — … (supersedes S011)` → `CITED=1`, S011 unrenumbered, `cited-id-check.py` → `CITED_IDS=PASS rows=1`
(wave 1: `FAIL rows=2`); mid-body `source:` under `#### Observation` → not cited; same-line repeat → one
`renumber.tsv` row. Capitalised `Source:` still `CITED=0 APPEND=0 BODYONLY=1`; new holes N3/N4, side effect N7.

**F4 MEDIUM silent non-staged `source:` ids — FIXED for source lines.** `f4_999` → `rc=1 REFUSED … source id S999 is
neither a staged row nor a lane Registry row`; `f4_ownwork` (`source: S001` = lane row) → `rc=0`, S001 left unchanged,
S003 appended; `f4_minted` (`source: S003` = minted this run) → `rc=1` with the *same* message. Residuals: N5, N1.

**F5 LOW twin URL + invalid recheck — STILL PRESENT.** `f5` (two entries, one URL, second `recheck=INVALID_RECHECK`) →
`rc=0 CITED=2 APPEND=1 HELD=1`, `renumber S011→S003 held`, `used-by a.md, b.md`; the invalid recheck is never refused
because L437 `if action != "append": continue` precedes L455-462. `held` still covers a same-run twin though docstring
L24-27 defines it as "a Registry row already carries".

**F6 LOW refusal ordering/coverage — STILL PRESENT.** `f6` prints `REFUSED entry missing: …` **before** the two
registry lines (`REFUSED registry has no ## Registry heading`, `REFUSED registry rows outside …`; L375 vs L381,
rc=1); `f6b` (same registry, no `--entry`) → `rc=0 COLLISIONS=0`.

**F7 LOW helper asymmetries — PARTIAL.** `pipe_free`/`ASSIMILATE_CITES` halves fixed/disclosed; `GREP_RE` vs
`ROW_RE` (L99-100) untouched and now bites harder (N6a/N6b). Real registry `grep=112 row=112 grep-only=[] max=112`
→ both latent today.

## New defects the fix introduced
**N1 HIGH — a lane id that is also a staged id is classified as staged, so an own-work citation is silently
renumbered and the appended row claims the wrong `used-by`.** L383-386 tests `i in staged` before `i in base`
and docstring L21-23 only says "neither … nor …", so the precedence is unstated.
```
$ … (ownwork_url: registry S001 = own-work lane artifact; staged S001 = a different doc with a URL;
       entry "source: S001 — corpus/knowledge/chain-resolution-r3.md — lane-local own work")
rc=0 stdout='COLLISIONS=1 / CITED=1 APPEND=1 HELD=0'
renumber S001→S003 append example.test/campaign-doc · OUT e.md "source: S003 — corpus/knowledge/chain-resolution-r3.md"
append: | S003 | Campaign doc … | used-by corpus/knowledge/e.md
```
This is the live package's shape — 31 staged ids collide with lane ids, and staged S105-S108 are own-work rows
(`grep -nE '^\| S(10[5-8]) ' SOURCES.append.md` → "own-work … (lane-local artifact)"). Re-running the adopter on
the **landed** entries therefore refuses, because those rows carry no URL:
`$ … --knowledge . --entry corpus/knowledge/japanese-search-record-r38.md …` → `rc=1 REFUSED S107: staged row
names no http(s) URL / REFUSED S108: …`. Loud today, one URL in an own-work staged row from rewriting `source: S107`.

**N2 MEDIUM — a refusal leaves the previous run's `renumber.tsv`/`append.md` in a reused `--out`, so the frozen
"no `renumber.tsv` and no `append.md`" clause is observably false** (nothing is cleared before writing). `$ … --out
stale/out` (good) → `rc=0`, files written; then the staged row made 2 cells → `rc=1 REFUSED S010: staged row has 2
cells, not 11`, yet `renumber.tsv: S010 S003 append example.test/new-a` and `append.md: | S003 | New A …` survive. The
counter is immune (fresh `mkdtemp` per leg); the D3 wording is not.

**N3 MEDIUM — an entry whose provenance header sits below a `####` line cites nothing, silently.** L176
`if line.startswith("####"): break` stops first:
`$ … (n_h4: "#### Provenance" then "source: S010 …")` → `rc=0 CITED=0 APPEND=0 HELD=0 BODYONLY=1`; `renumber.tsv`
header only, `bodyonly e.md S010`, `OUT e.md` unchanged. A citation becomes a body-only mention with no refusal
and no WARN — the same silent-degradation class as F3.3.

**N4 MEDIUM — a fenced example header above the real header is cited, appended and rewritten inside the fence** (no
fence awareness): an entry whose prose shows a fenced block holding `source: S011 — https://example.test/ex — section`
above its real `source: S010` line → `rc=0 CITED=2 APPEND=2`, `renumber S010→S003 · S011→S004`, and the fenced text in
`OUT e.md` becomes `source: S004 — https://example.test/ex — section`.

**N5 LOW — a body token equal to a *minted* id that is not a staged row is left unchanged with no record**; the source-id
refusal has no body counterpart and L469 filters `if i in staged`. `$ … (a.md cites S010→S003, b.md body "mentions S003
only (not a staged row)")` → `rc=0 BODYONLY=0`, `bodyonly.tsv` header only, no `bodyclash.tsv`, no `WARN`, `OUT b.md`
still reads `S003`. The staged cases hold: `n_clash2` (body S003 is staged and equals the minted id) → `bodyclash.tsv b.md
S003` + `WARN corpus/knowledge/b.md: body-only staged id S003 is also a lane id and reads as that row`; `clash_base`
(staged id = a base row) → same WARN; F1's shape gives no clash because S010 stays a staged id.

**N6 LOW — the minted-id refusal at L425-431 is unreachable dead code, though L21-23 advertises it.** Every minted
id is `max(base)+1, +2, …` (L405) so `minted ∩ base = ∅`; L383-386 already refuses every source id `not in staged
and not in base` and L395 returns before L425. An instrumented copy (`HIT2` marker at L430) fired 0 times over the
lane selftest (27 findings), the live package and all 27 scratch packages; `f4_minted` prints the L386 message and no
fixture covers the L430 text. **N6a/N6b:** a `| S005 (note) |` registry row is GREP-only, so base max stays
S004 and the run mints S005 — `f7_collide` → `renumber S010→S005 append`, `append | S005 | New A …`, `collisions`
empty while `reg-ids` already lists S005 (duplicate lane id); the mirror case refuses a legitimate own-work
citation — `f7_ownwork` (`source: S005`) → `rc=1 REFUSED … S005 is neither a staged row nor a lane Registry row`.

**N7 LOW — `bodyonly.tsv` lists header-line non-citations.** `source: S010 … (supersedes S011)` writes `bodyonly e.md
S011` and `BODYONLY=1` though S011 is on the header line, not in the body (f3tail); any header tail token inflates `BODYONLY`, and no landed entry has one (body tokens for all three: `[]`).

## What else holds
- `SOURCE_RE` forms: `source:S010`, `source:\tS010`, `source:   S010` → `CITED=1 APPEND=1`; `source: **S010**` and a
  one-space-indented header → `CITED=0 BODYONLY=1` (documented "the id right after `source:`"; `cited-id-check.py` L29
  `^source: {staged}\b` agrees). A refusal still writes only `reg-ids`/`staged-ids`/`collisions` (f4_999).
- Landed entries cite `[S107,S108] / [S109,S110,S111] / [S112]` with body tokens `[]` — no token but a bound id.
- `--cites all` on the live package → `rc=1 REFUSED S105: staged row names no http(s) URL / REFUSED S106: …` (legacy
  mode is fixture-only; documented as round-50 behaviour, so not a claim failure).

VERDICT: attacked adopter v2 on 27 built packages plus two live-package runs — F1/F3.1/F3.2/F3.4/F4 are fixed
and the frozen C1 (5/5), the supplement (6/6) and the held map hold, but F5/F6 and the `GREP_RE`/`ROW_RE` split
persist, and the fix introduced one HIGH (own-work lane id that is also a staged id gets renumbered, N1), two
MEDIUM operability holes (stale output on refusal N2, `####`-above-header silent no-op N3), a fence-rewriting case
(N4), a silent body-token class (N5) and one advertised refusal that cannot fire (N6).
