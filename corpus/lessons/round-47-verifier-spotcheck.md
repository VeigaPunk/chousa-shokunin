# Round 47 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_flash)
date: 2026-10-25
lane: chousa-shokunin · lane round: 47 · base `9a9f94dbcb010eca6636886e53950f38ca806329` → tip `900c72eca0f4f4d5bdfbd2c9c25cc8c149f88561`

## 1. Conformance (step 1)

- **Report identity chain.** `git -C …/shokunin log --format='%an %H %s' -- .ufo/reports/round-47/chousa.md`:
  1. `f82d64f2f7ebd4319c1828772f267581072fff86` — `chousa-shokunin` — "round-47: chousa report";
  2. `35b91714722fd2314c6b22839c446a116d1a5ffb` — stray commit, author/committer `t <t@t>`, subject `t` (snapshot committing 822,830 deletions fleet-wide, report path among them);
  3. `c159aaee3b977b69e3cc406d6ce97f9fdd9dd7e9` — `chousa-shokunin` — "round-47: chousa report (hyaku sweep: L1 returned without committing; attribution defect)"; diff vs its parent is exactly +188 report lines, and the report bytes equal `f82d64f2`'s (empty diff between the two report commits).
  **Attribution defect recorded:** the lane's L1 did not land the report itself; final report bytes were fleet-swept by the orchestrator (`c159aaee`) after uncommitted edits, with a non-lane `t@t` commit in between. Content is the lane's report; attribution is swept.
- **SHONEN heading:** present, one line per box, 4 boxes, all `[~]` with pointers that resolve at `900c72ec` (SKILL.md `## Gates`; LOG.md `## Round 47`; `corpus/evidence/round47/measure-after.txt`; `.ufo/waves/round-47/w1/ScoutProvinceFit.md`). No `[x]` non-author check — promotion assessment remains to a fresh non-author (operator-owned).
- **Cited lane commits:** all 10 cited hashes exist and are ancestors of branch `master` (`git merge-base --is-ancestor` PASS on 22a44b8b, a15610a5, 980fe43f, 7fb9a232, 3d2a0637, 1fc5ed19, 02d95d32, b8bc06c6, 11ead577, 900c72ec).
- **Pushed / leftover:** `jj-lane.sh state` → branch master local=remote=`900c72ec…` ahead=0 behind=0. `git status --porcelain` shows exactly the three inherited left-named r40/r41 JSON paths (`.ufo/waves/round-40/w1/swarm-registry.json`, `round-41/w1/…`, `corpus/evidence/round41/receipts/cells/cells.json`) — pre-existing, not round-47 work.
- **Prompt contract:** the dispatched `.ufo/prompts/chousa-round-47.md` carries template sections 1–5 verbatim plus addendum §6; all five child-lane items present (report path, commit-before-report ordering, SHONEN heading, commit-hash citation, write scope).
- **Census:** `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, 94 rows, same five W04 (S051/S053/S073/S074/S075). No malformed rows (NF=13 check prints 0).
- Marker vs report: real report, committed work, resolvable hashes → status `ok`.

## 2. Claims (step 2) — re-measured, not evidence-verified

Counter re-runs (my own) over `git archive 900c72ec` into /tmp (counters with `--root <archive>`):

- **C1** `python3 corpus/evidence/round47/c1-count.py` → `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 CANARY=pass R46_COUNTER=pass R46_ENTRIES=2/2 C1=PASS` exit 0 — matches reported after. Before-control `controls/c1-before.txt` committed and matches (`0/3 JUNK_KILLED CANARY=fail C1=FAIL`).
- **C2** `python3 corpus/evidence/round47/c2-count.py --root <archive> --list` → `ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=51 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS` exit 0; freeze-time counter (blob from 22a44b8b) → `ENTRY_POINTS=93 REGISTERED=93/93 MISMATCHES=0 C2=PASS` exit 0. Matches `measure-after.txt`; the earlier wave-2 recordkeeping defects (93/93 slot mix, phantom 92/92, untracked measure-after pointer at 1fc5ed1) are resolved at tip (measure-after.txt is tracked in `900c72ec`; scorecard rows 2506–2507 state 94/94 and 93/93).
- **C3** `python3 corpus/evidence/round47/c3-count.py` and `--lane-only` → every leg full in both modes (`QUOTE_ROWS=35 CAPTURE_BOUND=35/35 ANCHOR_BOUND=6/6 INFERENCE_GROUNDED=2/2 QUARANTINE_VERDICTS=4/4 QUARANTINE_ABSENT_ADOPTED=0 C3=PASS`; `--lane-only` `CAPTURE_BOUND=skipped`) exit 0; `build-spans.py --check` → `SPANS_ROWS=35 STALE=0`. Wave-2 entry overclaims (amendment "measures pool-dependence", base "error rate of this order") are corrected/qualified in the tip entries.

**C1 ruling (named non-author reviewer, chousa round 47).** The frozen predicate verifies; the axis move does not. Held-out evidence (committed wave-2 reports): `HeldOutB` kills 4/12 genuine natural flips, misses 8/12; `HeldOutA` refuses 2/12 correctly-reasoned bullets (exit-level 3/12 incl. a05, an over-refusal of a common construction) vs 0 before; `MutC1Refined` — 5/7 refinement mutants survive the frozen counter; `CritC1Claim` shows the post-fix semantics silently diverge from the frozen sentence (clause-bound look-back narrows "among the three span words before it" and widens acceptance; the documented "double negation still passes" survivor is now refused; the tuning set 5/10 is not held-out). Real capability gain (D7 body now exits 1; 4/12 flips killed; 0 exit changes on the lane's 63 real entries) at a real, unmeasured-in-practice precision cost. **Ruling: trade → operability harmed.** The round fails "no axis harmed"; C2/C3 are separable and verify on their own counters.

## 3. Per-axis verdicts

| axis | verdict |
|---|---|
| operability | **harmed** (trade; C1 — capability real, precision cost measured 2–3/12 false refusals, 8/12 misses, 5/7 mutants survive) |
| calibration | **improved** (C2 re-measured; 8 real mismatches closed; final scorecard numbers correct) |
| depth | **improved** (C3 re-measured both modes; entries re-grounded, overclaims corrected) |
| coverage | **improved** (SOURCES 89→94 rows opened+mined; census exit 0; coverage map +2) |
| freshness | **unchanged** (captures dated 2026-10-23, predate launch 2026-10-25T08:25:52−03:00) |
| adjacency | **unchanged** (no sibling holds the ground) |

## 4. Discernment spot-check (step 3) — re-opened from committed captures, no live fetch

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| `claim-support-test-r37.md` entry (S090 grounding) | admit | capture `4132ec1b265e60624523251f.txt` (sha256(URL)[:24] of aclanthology.org/2026.findings-acl.19.pdf) | agree | `∼22% of claims in Wikipedia lead sections` and `of claims in the article body are unsupported` occur verbatim at chars 1526 / 1669 as stated |
| `claim-support-test-r37-amendment-2026-10-23.md` entry (S092 anchors) | admit | capture `b502d4c6a6ee023bee6f8531.txt` (arxiv.org/html/1803.05355) | agree | `For the first two classes, the annotators also recorded the sentence(s)` at char 2849 and `95.42% precision and 72.36% recall in evidence retrieval` at char 6601 occur verbatim |
| `citation-count-semantics-r37.md` (staged S100) | reject | capture `b539a80218080da56a75b624.txt` | agree | decodes to 762,265 chars with 308,430 U+FFFD; raw 801,280 bytes fail utf-8/utf-16/gbk/gb18030/big5 — lossily decoded OLE, byte-faithful flip unmet |
| `search-log-fields-r36.md` (register S077, PRISMA-S DOI) | reject | capture `01f657b3d0ab045c494b3f92.txt` (doi.org/10.1186/s13643-020-01542-z) | agree | capture is a 267-byte "Client Challenge" page, not the article; round-43 flip unmet |
| SOURCES row S092 quote | check | same capture as above | agree | quote is 11 words (≤25), located, matches at char 2849 |

All four sampled gate decisions (2 admits, 2 rejects) agree with the re-opened sources; the S092 row quote is valid.

## 5. Trend verdicts

- **expansion — improved:** two admitted knowledge entries on ground the coverage map did not hold (support definition, annotator decision rule, per-step reliability), each citing mined rows S090–S094 opened this round; census 89→94 exit 0.
- **quality — improved:** three counters pass over committed bytes against committed do-nothing controls (re-measured); nine mined mistakes each with a fix shown able to fail; wave-2 entry/scorecard corrections landed before tip. Caveat: the C1 frozen-counter fixture coverage gap (5/7 refinement mutants survive) is a real test-coverage defect, routed below.
- **discernment — improved:** the outside spot-check agrees with the gate on sampled admits and rejects (table above); wave-2 seats also agreed with every admit and both rejects they attacked. The C1 axis-score miscalibration (self-claimed "improved" vs held-out trade) is recorded under the C1 ruling, not a corpus-gate disagreement.

## 6. Routed defects (lane must address next round)

1. **C1 precision side:** document the refusal class in the tool docstring Named limit (`nonexistent`-type unlisted absence words, negator beyond 3/2 windows, `non-` vs `un-`) and add the held-out precision fixture set as a counted leg (round-48 planned row already names it — keep).
2. **C1 frozen counter coverage:** add fixtures so the ref counter kills the five surviving refinement mutants (implicit negators, `un-` prefix, repeated figure occurrences, nested counts keys).
3. **SCORECARD/lesson:** once ruled, the operability verdict should read harmed/trade, not "improved, disputed"; the capability row's figure leg should say fixture-only in lane practice; the stale "double negation still passes" survivor statement is already corrected in the tip scorecard — keep it corrected.
4. Carried: round-39/40 receipts failing `gate-sha256-mismatch` since round 41; L0 `8d77e6c1` fetch-scope question open.
5. Note for operator (not lane debt): report attribution was fleet-swept (`c159aaee`; stray `t@t` commit `35b91714` sits between lane report and sweep). SHONEN boxes all carry resolvable pointers; a fresh non-author could check them (promotion is operator-owned).

## 7. Commands run (decisive output)

`git log --format='%an %H %s' -- .ufo/reports/round-47/chousa.md`; `git merge-base --is-ancestor <hash> master` ×10; `jj-lane.sh state`; `git status --porcelain`; `sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` (exit 0); `git archive 900c72ec | tar -x -C /tmp/chousa-r47-verify` then `c1-count.py` / `c2-count.py --list` / freeze `c2-count.py` / `c3-count.py` / `c3-count.py --lane-only` / `build-spans.py --check` (all exit 0); capture re-open via sha256(URL)[:24] keys in `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/` at stated char offsets; S100/S077 capture byte checks. No installs; scratch `/tmp/chousa-r47-verify` `/tmp/chousa-r47-freeze` removed before return.
