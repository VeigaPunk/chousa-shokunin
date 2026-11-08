# R85CriticClaims — adversarial claim review (round 85)

Axes: **operability of `tools/gate-records.py verify`** (predicate = `GATE_RECORDS_R85=PASS`
via `corpus/evidence/round85/gate-records-r85.py`), **depth of provenance entry**
(predicate = `DEPTH_R85=PASS` via `corpus/evidence/round85/depth-r85.py`),
**kill-rule coverage / K2–K4 falsifiability**, **freeze discipline / counter immutability**,
**cheap-control gameability**, **thinness / new-ground redundancy**.
Tooling: no installs; pacman untouched per guard; python3 stdlib + git only.

All checks below were run in scratch under `/fast/scratch/hyaku/chousa-r85/R85CriticClaims/`
(`git archive` trees at 64803d33362f50cf9094e91fc3a4a07216c563ca = landing bytes;
43c3f728… base; 5d0b9413 freeze; 02df67db amendment). Every receipt cited was copied
to `.ufo/waves/round-85/w1/R85CriticClaims/`.

## 1. Controls adequacy

### C1 cheap controls (counter = `gate-records-r85.py` at landing bytes, `--root landing --repo <lane>`)

| control | command | observed line + rc | verdict |
|---|---|---|---|
| construction-keyed tool (filename `gNNNN.md`/`fresh%02d.md`, `Zyzzyva`, blind-accept everything else) | `python3 -B gate-records-r85-landing.py --root …/landing --repo … --tool tool-construction.py --work …/w-construction` | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=120/354 EMPTY_REFUSED=0/1 RC=3/4 SETUP=0/1` `GATE_RECORDS_R85=FAIL` rc 1 | receipt `c1-construction.txt` |
| registry+refetch-only tool (no tier/capture/quote/line/parse checks beyond sid + one refetch-row existence) | same, `--tool tool-regref.py` | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=37/354 EXPECTED_CODE=24/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=0/1` `GATE_RECORDS_R85=FAIL` rc 1 | receipt `c1-regref.txt` |
| `capture_sha256=`-only tool (accepts iff line contains `capture_sha256=`) | same, `--tool tool-capshaonly.py` | `TOOL=present POSITIVE=10/15 FRESH_POSITIVE=2/5 FORGED_REFUSED=78/354 EXPECTED_CODE=0/354 EMPTY_REFUSED=1/1 RC=2/4 SETUP=0/1` `GATE_RECORDS_R85=FAIL` rc 1 | receipt `c1-capshaonly.txt` |
| wrapper = pristine landing tool + hard-coded non-git `--repo` → `GATE_RECORDS_ERROR`/exit 2 passthrough | same, `--tool tool-wrapper.py` | `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1` `GATE_RECORDS_R85=PASS` rc 0 | receipt `c1-wrapper.txt` |

Reading: the judgment of "gameable" is **narrow**. The construction-keyed, registry+refetch-only and
capsha-only tools all **FAIL** — the battery's `EXPECTED_CODE` leg (354/354 required) and the
`POSITIVE`/`FRESH_POSITIVE` legs block superficial acceptance. The wrapper **PASSES**,
but it shells out to the pristine production tool itself, so it is not a *cheaper* control:
it presupposes the repaired implementation. Whether the claim *text* still verifies when a
cheaper control passes: **the text does not claim "no cheaper tool can pass"**; it claims
the production path (`python3 tools/gate-records.py verify`) passes a battery it could not
pass before the repair, with K4 defining the whitelist as "accepts the 15 frozen lines and
refuses everything else" — the wrapper is neither. **Verdict on (1) for C1: no cheap control
PASSes; the battery is not shown gameable.** The wrapper result is recorded for completeness:
a verification that runs `subprocess` on the pristine tool inside a counter-scored tool file
would itself need an out-of-band rule to exclude; no such rule is needed to hold C1, because
the production bytes are what is scored, not an arbitrary `--tool` path.

### C2 cheap controls (counter = `depth-r85.py` at landing bytes)

Costs were built by copying the landing tree into `work/c2-<name>/` and replacing only the
new-entry file.

| control | command | observed line + rc | verdict |
|---|---|---|---|
| content-free-rows entry (same 7 located quotes, Do/Never = "keep good notes… write nothing at all ever… never note any time…", B1 declared limit) | `python3 -B c2-salad/…/depth-r85.py --root …/c2-salad` | `ENTRY provenance-recording-r85.md ok=yes rows=6 quotes=7/7 fails=-` `DEPTH_R85 entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3` `DEPTH_R85=PASS` rc 0 | receipt `c2-salad.txt` |
| round-84 entry re-landed with fresh `source:` line (new file `search-transparency-r85.md`, source prepended S215/S026/S024, old quotes) | `python3 -B c2-reland/…/depth-r85.py --root …/c2-reland` | `ENTRY search-transparency-r85.md ok=no rows=11 quotes=0/12 fails=E3,E4,E6,E7` `DEPTH_R85 entries=1 ok_entries=0 rows=11 located_quotes=0 fresh_sources=0` `DEPTH_R85=FAIL` rc 1 | receipt `c2-reland.txt` |
| quotes from captures, rows cite wrong source (Warrant S-ids swapped S215↔S026) | `python3 -B c2-wrongsrc/…/depth-r85.py --root …/c2-wrongsrc` | `ENTRY provenance-recording-r85.md ok=no rows=6 quotes=7/7 fails=E2` `DEPTH_R85 entries=1 ok_entries=0 rows=6 located_quotes=7 fresh_sources=3` `DEPTH_R85=FAIL` rc 1 | receipt `c2-wrongsrc.txt` |

Reading: the salad control **PASSes** — this is the *declared* counter limit (claims.md §C2
"Controls": "kill rule K3 does [judge whether a row follows from its quote]"). The counter
cannot falsify row-warrant; only K3 can. The re-landed round-84 control **FAILs** (E3/E4/E6/E7:
old quotes are not fresh-located, not novel) and the wrong-source control **FAILs** (E2).
**The do-nothing control cannot reach the target** (`entries=0 … fresh_sources=0`,
`DEPTH_R85=FAIL` rc 1 at base/freeze/amend epochs; see §4). Whether the claim text still
verifies when the salad control passes: **yes** — the text *discloses* this as a control
(`c2-f1-salad-boundary … PASS — the stated counter limit`), so the PASS does not falsify the
claim; it merely shows `E1–E7` are not a comprehension measure. **Verdict on (1) for C2: no
*undisclosed* cheap control PASSes.**

## 2. Claim–predicate alignment

### C1: all docstring checks + setup leg + three repairs

Docstring codes at landing (`tools/gate-records.py:29-44`): `PARSE, REGISTRY, TIER,
CAPTURE_PATH, CAPTURE_KEY, CAPTURE_SHA, REFETCH, WORDS, QUOTE_LEN, QUOTE_ABSENT, REV, LINE`.
Instrumenting `mutations()` over the 15 frozen positives + 5 counter-built fresh positives
gives the `EXPECTED_CODE` histogram (receipt `histogram.txt`): `LINE=18 REV=18 WORDS=30
PARSE=120 QUOTE_LEN=30 REGISTRY=12 TIER=12 CAPTURE_PATH=12 CAPTURE_SHA=24 REFETCH=18
QUOTE_ABSENT=24 CAPTURE_KEY=12`, total 330, plus 24 `M03/M17` = **354**. Every one of the
12 docstring checks has at least one forgery expecting it — **none is unforged**. The setup leg
is counter-scored (`SETUP=1/1` requires exit 2 + `GATE_RECORDS_ERROR`), and the landing run
prints `SETUP=1/1` (receipt `c1-landing-rerun.txt`); the base tool prints `SETUP=0/1` with
`EXPECTED_CODE=342/354` (receipt `c1-base-tool.txt`) — the do-nothing control fails only on
the setup leg and the 12 `D4` calendar-clock forgeries (base ACCEPTs `M19/M20` Arabic-Indic
http/curl_rc + wrong-code `D4` → `REFETCH` instead of `PARSE`).

**The three repairs, one alignment defect:**

* **Setup leg (non-git `--repo` → exit 2):** covered. Landing tool `main()` rejects non-git
  `--repo` with `GATE_RECORDS_ERROR` before any per-record `FAIL REV,LINE`; counter checks
  both rc and stderr.
* **Calendar-valid `fetched`:** covered. Landing `parse()` calls `_valid_ts()` (`strptime`);
  `D4-non-timestamp-fetched` (`2026-13-40T00:00:00Z`) expects `PARSE` and the base tool
  returns `REFETCH` instead (WRONG_CODE ×12 in `c1-base-tool.txt`).
* **REFETCH narrowed 2xx → exactly 200:** **the predicate does not measure it.** Counter
  differentiator `D1-stale-refetch-txt-sha-drift` is a forge whose `capture_sha256` is a
  FAILED-attempt txt_sha for the same URL. The counter builds it only when `url in
  failed_txt`, where `failed_txt` = rows with `curl_rc=="0" and http!="200" and txt_sha!="-"`.
  At landing, **zero of the 12 admit URLs have such a row**, so `D1` appends **0 forgeries**:
  `354 == 330 + 24`, no `D1` (receipt `histogram.txt`). A direct `203` probe (`curl_rc=0
  http=203 words=0 quote=none`) returns `FAIL REFETCH` from **both** base and landing tools
  (because `fetch` found no matching refetch row for that S-id/url, not because the
  `startswith("2")` vs `== "200"` branch diverged). The base tool therefore still scores
  `FORGED_REFUSED=354/354` identical to landing on this axis. **The claim sentence's
  central "2xx → 200" repair is asserted, not fired: no forgery in the 354 would be
  accepted by the base tool and refused by the landing tool on that ground.**
  Counterexample: base `gate-records.py:247` `kv["http"].startswith("2")` vs landing
  `=="200"`; the only forgery that could separate them would need a committed `http=203`
  refetch row whose `txt_sha256` matches the capture bytes — none exists among the 12 admit
  positives (the 3 `0/203` rows in `refetch.tsv` cover S021/S032/S022, none is an admit
  positive). **Impacted axis: C1 K2 "differentiated per-class forgeries" — one of the seven
  enumerated r85 differentiators (claim item 1) is vacuous.** Smallest safe correction:
  disclose `D1=0` in claims (or add one `203`-admit forgery by pointing a positive's
  refetch row at a `203` row via counter-constructed S-id pairing); do not add it silently
  after scoring.

No other docstring check lacks a forgery. `EMPTY_REFUSED=1/1`, `RC=4/4 ` (`RC_ORIG`/`RC`/`SETUP`
all counter-scored) are measured, not asserted.

### C2: "teaches provenance recording"

`fresh_sources=3`/`rows>=6`/`located_quotes>=7` measure **ground** (3 fresh mined registry
rows whose captures/refetch rows verify and whose quotes locate), **coverage** (E6), and
**numerosity** (E1/E3) — they do **not** measure "teaches provenance recording", and the
claims file says so explicitly (B1 limit: "the counter does not judge whether a row follows
from its quote; kill rule K3 does"). Is `fresh_sources=3`/`rows>=6`/`located_quotes>=7`
reachable by the do-nothing control? **No**: `entries=0 ok_entries=0 rows=0
located_quotes=0 fresh_sources=0`, `DEPTH_R85=FAIL`, rc 1 (receipt `c2-d0-donothing.txt`
committed; re-run at freeze/amend trees this session returns identical FAIL). A *content-free*
but *grounded* new entry does reach it (§1, salad `PASS` rc 0) — that is the declared
boundary control, not the do-nothing control. **Verdict on (2): C1 alignment defect on the
203 leg (vacuous D1); C2 alignment is disclosed, not hidden.**

## 3. Thinness

### C1 — real capability, with one redundant-vs-existing check

* vs the lessons' hand "Location command" (`corpus/lessons/round-81.md:31`,
  `round-82.md:64`): those were per-record copy-paste `grep`-style checks (one per admitted
  row, `<key>`/`<quote>` substituted by hand). The tool mechanizes registry + capture +
  refetch + git-blob join across all 15 records in one CLI with a single summary and
  per-code output. It is a real capability acquisition (hand-per-row → one unattended,
  code-attributed command), not the same check re-typed.
* vs `tools/quote-reopen.py`: that tool re-opens located quotes against the **live** source
  (fetch, head-boundary, ≤25 words) and reports `VERBATIM/ABSENT/UNREACHABLE`. It does **not**
  check registry tier, capture path/key/sha, refetch success, or git-blob line/rev — so the
  registry/capture/refetch/git join is **not** redundant with it. **Redundant leg:**
  `WORDS`/`QUOTE_LEN` word-counting duplicates `quote-reopen`'s `MAX_WORDS=25` gate in
  spirit, but the redundancy is bounded and the `WORDS` leg is additionally tied to
  `LINE`/`QUOTE_ABSENT` in a way `quote-reopen` is not.
* **Verdict:** C1 is thin in the D1/200-only sense only (§2); it is not a relabel of the
  hand command or of `quote-reopen.py`.

### C2 — new ground (K4)

`corpus/evidence/round85/base-knowledge.txt` (96 base entries): none of S215/S026/S024
appears as an S-id in any base `source:` line, and none of their URLs appears in any base
entry text (checked programmatically; quote: `S215 in base_text? False`, etc.). The PROM
coincidence to note for a reviewer: `metadata-screen-r25.md` already cites **PROV-O S033**
(the superseded `REC-prov-o-20130430` URL) for `prov:wasDerivedFrom` +
`prov:generatedAtTime`/`prov:invalidatedAtTime`, and `search-transparency-reporting-r84.md`
already teaches DCMI `source`/`modified` via S023 with rows "Recording what a resource
derives from" (Q9) and "Recording when a resource changed" (Q10). C2's new entry re-states
the derivation/bounds facets under fresh S215 (W3C *alternate* `https://www.w3.org/TR/prov-o/`
URL — not S033's `REC-…` URL), adds S026 FAIR R1.2 facets (Q5/Q6 — the *only* genuinely
new conceptual ground) and S024 `lastReviewed` (Q7). Conceptually: **derived-from and
generation/invalidation are re-grounded, not new; provenance facets (how/why/by-whom/credit)
and lastReviewed are new.** K4 as written (S-id/URL ground) **holds**; content-overlap
with `metadata-screen-r25.md`/`search-transparency-reporting-r84.md` is real but is not a
kill rule in the frozen text. **Verdict:** C2 is thin on derivation/bounds, new on facets/
lastReviewed; K4 fires only on the S-id/URL test, which passes.

## 4. Freeze discipline

| rev | committer | what changed vs previous |
|---|---|---|
| `5d0b9413` freeze | 2026-11-08 00:54:30 -0300 | frozen `claims.md` + counters + egress table + controls |
| `02df67db` amendment | 2026-11-08 01:17:16 -0300 | `corpus/evidence/round85/claims.md` (C2 re-pointed S020/S023 → S215/S026/S024; rows≥7→≥6, located≥8→≥7, fresh=2→3), `depth-r85.py` (section parser: header-case + heading-skip fix), `instrument-pins.txt` (depth sha `516345e7…` → `8ff164eb…`, claims sha), plus SOURCES/captures/refetch + the entry itself |
| `64803d33` landing | 2026-11-08 01:31:25 -0300 | `tools/gate-records.py` (the 3 repairs), `gate-records-r85.py` **+2 lines** (`kv_set` returns `None` if the key is absent — fixes a `re.sub` silent no-op / TypeError path), `instrument-pins.txt` (gate counter sha `931b5ed7…` → `62496d36…`, + tool sha), `after/` receipts, lesson/plan/claims.json |

Assessment:

* **The amendment `02df67db` is disclosed** (plans/round-85.md Amendments 1–3) and occurred
  *before* the first scored after-receipts (`amend/corpus/evidence/round85/after/` does not
  exist; the entry already PASSes at `02df67db` — re-run at amend tree: `DEPTH_R85
  entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3` `DEPTH_R85=PASS`). This is
  the same shape as the r84 QUALITY-166 defect (post-freeze amend rewriting frozen bytes),
  mitigated only by explicit disclosure. The freeze commit's `claims.md` is therefore not
  the bytes scored.
* **Post-scoring counter-byte change (defect): `gate-records-r85.py` changed after the
  amendment and *in* the landing commit that contains the scored after-receipts.**
  The diff `02df67db…64803d33` adds the `kv_set` absent-key guard **and re-pins**
  (`instrument-pins.txt`: `gate-records-r85.py` `931b5ed7…` → `62496d36…`). Because the
  `after/c1-after.txt` PASS receipt is committed in the *same* commit (64803d33) as the
  changed counter, the scored receipt cannot be attributed to a counter byte that existed
  before scoring. `depth-r85.py` did **not** change after the amendment (`8ff164eb…` at both
  `02df67db` and `64803d33`); `claims.md` did **not** change after the amendment
  (`080ded8f…` at both). **The guard is claimed in the receipt as part of the landing
  instrument — a predicate/instrument that changed in the same commit as the first scored
  PASS is the r84 defect class (retroactive re-pin).** Smallest safe correction: re-score
  with the pre-landing counter (`931b5ed7…`) or disclose that the `kv_set` guard landed
  with the PASS and that the quoted PASS is against `62496d36…`, with a before/after
  receipt pair.
* **Egress discipline holds**: every `2026-11-08T03:x` refetch row (ROUND_START
  `2026-11-08T03:54:30Z`) post-dates the freeze committer time `00:54:30-03:00`
  (= `03:54:30Z` — wait: freeze is `2026-11-08T03:54:30Z`, so rows at `03:54:40Z`+ are after;
  rows stamped `02:13–02:21Z` are pre-freeze and correctly excluded).

## Counterexample, evidence, axes, smallest correction

* **Counterexample (operability axis, §2):** the base tool scores
  `FORGED_REFUSED=354/354 EXPECTED_CODE=342/354` (receipt `c1-base-tool.txt`) and lands the
  full 354 refusal count; the 12-item delta is entirely `D4` calendar-fetched + `M19/M20`
  Arabic-Indic digits. The headline "REFETCH success narrowed from `2xx` to exactly `200`"
  has **no behavioral witness** in the battery because `D1=0`. The claim sentence is
  therefore wider than its predicate.
* **Evidence:** receipts `c1-base-tool.txt`, `c1-landing-rerun.txt`, `histogram.txt`
  (D1 count = 0, total 330+24=354), `c1-construction.txt`, `c1-regref.txt`,
  `c1-capshaonly.txt`, `c1-wrapper.txt`, `c2-salad.txt`, `c2-reland.txt`, `c2-wrongsrc.txt`,
  `c2-landing-rerun.txt`.
* **Impacted axes:** C1 K2 (differentiated per-class forgeries — item 1 vacuous);
  C1 thinness (200-only leg is asserted, unwitnessed); freeze discipline (counter byte
  changed in landing commit alongside scored receipt). C2 axes: none fired by this review
  (K4 ground holds, do-nothing unreachable, reland/wrong-src fail as designed; salad PASS is
  the declared B1 limit).

Report: write your scoped findings to .ufo/waves/round-85/w1/R85CriticClaims.md

VERDICT: R85CriticClaims C1 fired — D1 (203→200) differentiator has zero forgeries so the 2xx→200 repair is asserted but unwitnessed by the 354-forgery predicate.
VERDICT: R85CriticClaims C2 held — cheap controls fail or are the disclosed salad boundary, do-nothing cannot reach the target, and K4 ground (no S215/S026/S024 in base) verifies.
VERDICT: R85CriticClaims C1 fired — gate-records-r85.py changed and was re-pinned in the same landing commit (64803d33) that first committed the scored PASS receipt, so the predicate byte postdates scoring.
VERDICT: R85CriticClaims C2 held — re-landed round-84 entry and wrong-source entry FAIL the counter (E3/E4/E6/E7 and E2 respectively), while the disclosed content-free salad PASS is the stated B1 counter limit, not a falsification.
VERDICT: R85CriticClaims C1 held — construction-keyed, registry+refetch-only and capture_sha256-only cheap controls all FAIL the counter, so the battery is not shown gameable by any cheaper tool.
