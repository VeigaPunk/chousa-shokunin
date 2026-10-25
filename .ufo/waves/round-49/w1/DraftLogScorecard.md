# DRAFT — round 49 wave 1, seat DraftLogScorecard

Role: UFO-FSD scribe. Deliverable: drafted round-49 `LOG.md` / `SCORECARD.md` entries (text in this report only) with placeholders where after-measurements are not yet known. No production file, git index, jj state, or sibling lane was written; scratch none created (nothing to delete).

## Behavior (every claim grounded below)

Read (via `read`):
- `skill://godspeed` → SKILL.md (axes/naming; no clarifying questions).
- `~/.omp/agent/RULES.md` lines 1-14: channel order; pacman transactions PAUSED host-wide; record installs. **No install performed** (none needed: read-only drafting; tool/version/channel = n/a).
- `LOG.md:-30` → lines 1750-1796 = round-47 + round-48 entries (shape source); file is 1796 lines (`wc -l` → 1796 / 2560).
- `SCORECARD.md:2528-2560` (round-48 verdict, axis rows, trends); `:2500-2528` (§Capabilities table rows, round-47); `:raw:2545-2545` (full C1 row).
- `corpus/evidence/round49/controls/c1-before.txt`: `TOOL=absent C1=FAIL` exit 1; `BASE_REV=414a2ec6cde05a921dbdd9e02e7ae56b0db647ef`; control `copy-tool.py` `SETS_PASS=0/3`, GUARD `COLLISIONS=[] FAIL`, PIPE `CELLS=13 FAIL`, census E01/E03/E04/E09 on every set.
- `corpus/evidence/round49/controls/c2-before.txt`: `ENTRIES=0/2 BOUND=0/9 (min 7) INFERENCE_GROUNDED=0/2 QUARANTINE_VERDICTS=0/5 (S082,S084,S086,S095,S096) C2=FAIL` exit 1; control `REF_ID_UNBOUND=11 C2=FAIL`.
- `corpus/evidence/round49/claims.md`: R49-C1 predicate/docstring (lines 20-32), target/kill rules (42-46); R49-C2 predicate (50-69), target (78), kill rule (80-82), admission rule (89-91); separability 13-16; no-fetch 8-10; first package-adoption round 12-13.
- `corpus/evidence/round49/c1-count.py` (docstring lines 2-31: tool interface, exit 0/1/2; `LANE`/`PKG=/home/vgpnk/Projects/shokuknow/merge/chousa`, `BASE_REV` pins).
- `corpus/evidence/round49/c2-count.py` (docstring 2-31: `--lane-only`; `CACHE`/`REGISTER` read-only paths; cheapest-shortcut refusers).
- `.ufo/waves/round-49/assimilation/adopt/renumber.tsv`: S087→S096 … S103→S104 (9 maps, all `append`); `append.md` rows S096-S104; `collisions` = S082-S095; `staged-ids` S082-S195; `reg-ids` S001-S095 (base registry 95 rows); `corpus/knowledge/{aggregator-vs-source-r36,citation-count-semantics-r37}.md` (source/verified-at/recheck/ground/observation/inference/unknown shape).
- `merge/chousa/` (read-only): `SOURCES.append.md` 145.5 KB, `knowledge/`, `amendments/`.
- Glob: `evidence/round49/` has claims.md, c1/c2-count.py, build-spans.py, controls/ (no `spans.tsv`, no `measure-after.txt` yet — after-state unmeasured → placeholders); `lessons/` has no round-49.md yet; `tools/assimilate-rows.py` **present** (candidate).

Ran (`bash`):
- `wc -l …/LOG.md …/SCORECARD.md` → 1796 / 2560.
- `git -C …/chousa-shokunin log --oneline -4` → `6594092 round-49: C1 candidate tools/assimilate-rows.py (section-10 adopter: by-document renumber, census-schema rows, 0-3-space collisions)` on `fe740e7 round-49: freeze claims C1 … and C2 …` on `414a2ec round-48 …`; `status` shows only ` M corpus/QUALITY.md` + untracked wave files (candidate is HEAD; landed hash = `<landed-hash>`).

## Gates

- Frozen claims at `fe740e7838b338d17fec9338c909557e6e7fed7d`: never propose changing predicate/target/counter/control.
- Only write: this report. No `edit`/`write` elsewhere; no counters run (executor-owned; would write /tmp mirrors — the counter's tempfile use is outside my write license).
- No network / live fetch (L0 `8d77e6c1` open); reads limited to on-disk captures.
- Leaf seat: no subagents, no background jobs (none used).

## Touched surfaces

Read-only: as listed above. Written: this file only.

## Out-of-scope

Counters not run (before receipts quoted instead); lesson not drafted; `spans.tsv`/`measure-after.txt` not produced; no installs; no scripts written.

## Findings — draft entries

### DRAFT: `LOG.md` entry (append after line 1796)

```markdown
## Round 49 — 2026-10-25 (derived-index theme adoption by document; section-10 adopter)

Claims froze in `corpus/evidence/round49/claims.md` at `fe740e7838b338d17fec9338c909557e6e7fed7d`, after the pre-candidate controls: R49-C1 `TOOL=absent C1=FAIL` exit 1 (`controls/c1-before.txt`); R49-C2 `ENTRIES=0/2 BOUND=0/9 INFERENCE_GROUNDED=0/2 QUARANTINE_VERDICTS=0/5 C2=FAIL` exit 1 (`controls/c2-before.txt`). Candidate `tools/assimilate-rows.py` at `65940928cc9332b386bcbca92571451cc4374cbe`; landed at `<landed-hash>`; archive-after receipt in `corpus/evidence/round49/measure-after.txt` binds the measured tool sha and command outputs.

- **C1 operability** (lowest scored axis, 3/10; capability acquisition): `tools/assimilate-rows.py` turns a frozen set of staged campaign entries into an append block and rewritten entries that pass the fleet census on a scratch mirror of the lane registry at BASE_REV, renumbering every cited staged id BY DOCUMENT (held URL → the lane's existing id; new URL → the next lane id, contiguous from the base maximum) with one simultaneous substitution, appending exactly the rows the entries cite (status `mined`, opened 2026-10-25, census-valid recheck, `used-by` naming the citing entries), reporting the section-10 0-3-space id collisions, and rewriting escaped-pipe staged cells to 11-cell rows. `c1-count.py` runs sets A (this round's theme), B (collision-chain entry), C (held rows) plus GUARD and PIPE on scratch mirrors; package inputs sha256-pinned (a changed package exits 2). Before `TOOL=absent`; do-nothing control `controls/copy-tool.py` (byte-exact append, identity map): `SETS_PASS=0/3 GUARD COLLISIONS=[] FAIL PIPE CELLS=13 FAIL`, census E01/E03/E04/E09 on every set. After `<C1-after>` (target `SETS_PASS=3/3`, GUARD PASS, PIPE PASS, `C1=PASS` exit 0); kill rule: any set/GUARD/PIPE leg failing, a census E-code on any mirror, or harness/env exit 2. Tag plumbing (QUALITY 64); capability row only if the after-measurement passes in this round.
- **C2 depth / assimilation** (sourced): the theme "a citation index's data is a derived artefact" adopted BY DOCUMENT as `corpus/knowledge/aggregator-vs-source-r36.md` and `corpus/knowledge/citation-count-semantics-r37.md`, re-grounded on nine on-disk captures under the read-only `.qcache`; staged ids S087,S088,S089,S091,S092,S100,S101,S102,S103 → lane S096..S104 (`renumber.tsv`). Before `ENTRIES=0/2 BOUND=0/9`; control: the staged entries copied unchanged into a scratch root with the lane registry fail `REF_ID_UNBOUND=11 C2=FAIL` (staged ids name lane rows of OTHER documents). After `<C2-after>` (target `BOUND>=7` with `BOUND+REFUSED=9`; every `S###` token bound or the held S003; `spans.tsv` via `build-spans.py` with ≥2 quote rows per bound id, each quote ≤25 whitespace words and ≤160 characters, inside its span file, inside the citing entry and inside the round-49 lesson, each span file the exact slice of the capture text form at the recorded offset with the recorded file digest, and longer than its quote; every `char N` in a bound row's `anchor` cell at a located quote offset; both entries exit 0 under `tools/inference-ground.py`; `corpus/lessons/round-49.md` carries a `refused-doc` line for each refused document and a re-check verdict line for each absent-defect-register row on a theme URL, with no bound document `fabricated`/`unverifiable`; `QUARANTINE_VERDICTS=5/5` (S082,S084,S086,S095,S096)) → `C2=PASS` exit 0. Tag ground (QUALITY 64); the counter measures binding and presence, not entailment.
- **Calibration / record corrections**: C1's counter never reads the lane's adopted entries and C2's counter never runs the tool (claims.md:13-16) — the two claims are causally separable; base pinned at `414a2ec6…` (`BASE_REV` in both counters). Neither counter's pass overrules the external closure's spot-check of the Gate verdicts (claims.md admission rule).
- **Frontier / SOURCES**: first package-adoption round under addendum section 10 (claims.md:12-13); staged package `merge/chousa/` (`SOURCES.append.md` ≈145.5 KB, `knowledge/`). Section-10 collisions reported by the adopter: S082–S095 (`adopt/collisions`). Registry 95 → 104 if the nine theme rows append as S096–S104.
- **Waves**: round-49 wave 1 (build + first falsifiers); seats and reports retained under `.ufo/waves/round-49/`.
- **Inherited**: the three modified R40/R41 JSON paths remain from round 48 (LOG.md:1794); L0 `8d77e6c1` (fetch scope) remains open — no external live fetch; no tool installs.
```

### DRAFT: `SCORECARD.md` entry (new section after line 2560; capabilities row into §Capabilities)

```markdown
## Round 49 verdict — 2026-10-25 (derived-index theme adoption by document; section-10 adopter)

R49-C1/C2 were frozen at lane commit `fe740e7838b338d17fec9338c909557e6e7fed7d` before wave-1 scoring. The tool change landed at `<landed-hash>` (candidate `65940928cc9332b386bcbca92571451cc4374cbe`); final measurements over its archive are in `corpus/evidence/round49/measure-after.txt`. No external fetch; L0 `8d77e6c1` remains open.

| claim / axis | before → after | counting command | verdict | tag |
|---|---|---|---|---|
| C1 operability (lowest scored axis, 3/10; capability acquisition): the section-10 adopter turns staged campaign entries into a census-passing append block and rewritten entries — by-document renumber, mined/opened/recheck/used-by cells, 0-3-space collision report, escaped-pipe fix | `TOOL=absent C1=FAIL` exit 1 (`controls/c1-before.txt`) → `<C1-after>` (target `SETS_PASS=3/3`, GUARD PASS, PIPE PASS, `C1=PASS` exit 0); control `copy-tool.py`: `SETS_PASS=0/3 GUARD COLLISIONS=[] FAIL PIPE CELLS=13 FAIL`, census E01/E03/E04/E09 on every set | `python3 corpus/evidence/round49/c1-count.py` | **verifies** iff `<C1-after>` meets target; any set/GUARD/PIPE failure, census E-code or env exit 2 fails it | plumbing |
| C2 depth (sourced): the theme "a citation index's data is a derived artefact" adopted BY DOCUMENT as the two lane entries, re-grounded on nine on-disk captures | `ENTRIES=0/2 BOUND=0/9 INFERENCE_GROUNDED=0/2 QUARANTINE_VERDICTS=0/5 C2=FAIL` exit 1 (`controls/c2-before.txt`) → `<C2-after>` (target `BOUND>=7` with `BOUND+REFUSED=9`, `C2=PASS` exit 0); control: staged entries copied unchanged `REF_ID_UNBOUND=11 C2=FAIL` | `python3 corpus/evidence/round49/c2-count.py` (and `--lane-only`) | **verifies** iff `<C2-after>` meets target | ground |

The numeric operability scale remains 3/10 (its round-1 observable counts three archived inputs, not these new tests). C1's counter never reads the lane's adopted entries and C2's counter never runs the tool (claims.md:13-16); neither pass overrules the external closure's spot-check of the Gate verdicts (claims.md admission rule).

| axis | verdict | evidence |
|---|---|---|
| operability | **pending `<C1-after>`** | `controls/c1-before.txt` `TOOL=absent`; target at claims.md:42-44 |
| depth | **pending `<C2-after>`** | staged entries re-grounded by document (`adopt/corpus/knowledge/`); binding and presence counted, not entailment (claims.md:84) |
| calibration | **unchanged** | no new numeric self-assessment claim; `BASE_REV` receipts pinned in both counters |
| coverage | **pending Gate** | province/QUALITY-bar/coverage-map credit judged per entry in the lesson Gate (claims.md:84) |
| freshness | **unchanged** | every source is an on-disk capture under read-only `.qcache` (claims.md:8-10); no live fetch |
| adjacency | **unchanged** | no sibling lane touched; draft only |

Trends: expansion **pending** (two knowledge entries staged; admission depends on `<C2-after>` and the lesson Gate); quality **unchanged**; discernment **unchanged** pending the closure's independent spot-check of the round-49 Gate verdicts.

## Capabilities (add row to §Capabilities table)

| Capability | What it can now do | Evidence pointer | First-working round |
|---|---|---|---|
| section-10 row adopter (assimilate-rows) | turns a frozen set of staged campaign entries into an append block and rewritten entries that pass the fleet census on a scratch mirror of the lane registry: by-document renumber (held URL → existing id; new URL → next lane id contiguous from the base maximum), one simultaneous substitution, `mined`/opened/recheck/`used-by` cell schema, section-10 0-3-space collision report, and escaped-pipe staged-cell rewrite to 11 cells | `tools/assimilate-rows.py`; `corpus/evidence/round49/c1-count.py`; `corpus/evidence/round49/controls/copy-tool.py` | 49 (only if `<C1-after>` passes) |
```

## Artifact paths

Report: `.ufo/waves/round-49/w1/DraftLogScorecard.md` (this file). Source grounds: `corpus/evidence/round49/{claims.md,c1-count.py,c2-count.py,controls/c1-before.txt,controls/c2-before.txt}`; `.ufo/waves/round-49/assimilation/adopt/{renumber.tsv,append.md,collisions,staged-ids,reg-ids,corpus/knowledge/*}`; `LOG.md`; `SCORECARD.md`; `~/.omp/agent/RULES.md`; `/home/vgpnk/Projects/shokuknow/merge/chousa/`.

VERDICT: built the round-49 LOG/SCORECARD entry drafts plus capabilities-table row for `assimilate-rows` (placeholders `<C1-after>` `<C2-after>` `<landed-hash>`, exact counting commands and before receipts named, six axis rows kept) — drafts delivered; no measurements claimed.
