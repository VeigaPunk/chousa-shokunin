# Round 57 — verifier spot-check (closure, non-author)

author: hyaku closure (non-author integrator, @m_opus)
date: 2026-10-27
lane: chousa; round 57; base 6656f0770a1460d6ba73d9d2976f698a35311921; tip 5dc18607730a73e0a30ad938a20dbfaa37461f1c
report: .ufo/reports/round-57/chousa.md (fleet commits 01286956298ae2e6671fa8dbc541fc36bafc7a82 → f47fa39aa557fb8da8863ddf214836d55b1c7472, both author chousa-shokunin <chousa@shokunin.local>)
method: five read-only re-check seats (2 executors, 2 reviewers, 1 critic) plus integrator re-derivation; lane-owned counters c2-count.py / c3-count.py were NEVER executed (closure consequence, PROTOCOL §Gate standard) — every tally below was re-derived from committed bytes with independent commands.

## 1. Step-1 conformance

| check | result |
|---|---|
| Report committed by lane identity | PASS — `git log --format='%an %ae' -- .ufo/reports/round-57/chousa.md` → `chousa-shokunin chousa@shokunin.local` on both report commits |
| SHONEN heading, one line per box | PASS — `## SHONEN` present with 4 `[~]` lines (all asserted-by-author, no non-author `[x]`) |
| Cited lane commits exist + ancestor of branch | PASS — all 12 cited commits (c2f914c5, fd95724d, f9736a39, e0e73e0f, a03824d1, f31a91be, a8d4e7da, 1c9626ef, 3010e753, 75004f0a, f3ecb764, 5dc18607) pass `git merge-base --is-ancestor <hash> master` |
| Lane repo clean + pushed | PASS — `jj-lane.sh state` → branch=master local=remote=5dc18607 ahead=0 behind=0 tracked=0 untracked=0; `git status --porcelain` empty |
| Prompt carries template contract | PASS — all 5 round-level items (MISSION/AXES binding; L2 ≥8 one batched call matching MISSION.md §L2 concurrency; commit-then-push; push scope; L0 side channel) and all 5 child-lane items (report path+filename; commit-before-report ordering incl. pre-report ls-remote gate; SHONEN heading requirement; landed-hash-only citation rule; lane write scope) present in .ufo/prompts/chousa-round-57.md; route-table source named, no hardcoded aliases |
| Commit-before-report | PASS for the filed report — final lane tip 5dc18607730a committed 07:03:26-03:00; operative report f47fa39aa5 committed 07:10:03-03:00 citing it (defect D-a below on the superseded first filing) |
| Report is a real report, not a marker | PASS — all required sections present, evidence pointers throughout, hash citations |

## 2. Claim re-checks (re-measured, not evidence-verified)

### R57-C2 freshness — VERIFIED (re-measured; lane gate never executed)

Independent re-derivation over committed bytes at 5dc18607730a (own scripts in /tmp, git show/cat-file/ls-tree only):

| token | reported | observed | verdict |
|---|---|---|---|
| SET | 47 | 47 distinct (id,url,capture_sha256) triples pinned by 12 spans manifests at SET_REV 6656f07 | agree |
| VERDICTS | 47/47 | 0 MISSING of 47 (all ids present in refetch.tsv) | agree |
| REPRODUCED | 41 | 41 (pin == sha256(.raw) or sha256(.txt)) | agree |
| DRIFTED | 5 | 5 — S083 S087 S113 S114 S121, absent=0 each | agree |
| UNREACHABLE | 1 | 1 — S105, 3 failed attempts (rc=28) ≥600 s apart, no capture | agree |
| BYTE_BACKED | 46 | 46 | agree |
| CONSISTENT | 46/46 | 46/46 — own recipe re-implementation (pdftotext 26.08.0 / html_to_text / UTF-8 / OLE-zip decode) byte-equal to committed .txt AND to ledger txt_sha256 | agree |
| FLAGGED | 0/0 | 0 FRESHNESS-FLAG lines in the round-57 lesson; vacuous (need_flag=0) | agree |
| before receipt | C2=FAIL all-zero | `git show c2f914c5:…/c2-before.txt` prints zeros/FAIL; blob a8fc3824 byte-identical at freeze and tip | agree |
| freeze integrity | counters frozen pre-data | c2-count.py blob b1895cd9 identical at c2f914c5 and tip; fetches began only at f9736a39 (after the 02:42 freeze) | agree |

Caveats carried (disclosed by the lane, confirmed by the seat): FLAGGED=0/0 is vacuous — no committed after-state exercises the flag leg; S105 UNREACHABLE is record-level (the deleted capture is recoverable at e0e73e0^ and regenerates the pin exactly — freshness understated, not overstated).

### R57-C3 depth (sourced) — VERIFIED (re-measured; lane gate never executed)

Independent re-derivation at a8d4e7da and tip 5dc18607730a:

| token | reported | observed | verdict |
|---|---|---|---|
| ENTRY | yes | corpus/knowledge/normative-reference-chain-china-r57.md present (blob 6b4b6f92 identical at both revs) | agree |
| S127_CITED / NEW_GROUND / CLAUSE | yes | entry opens `source: S127 — <S127 first URL>`; clause sentence is spans row S127-1; `git grep 规范性引用文件` at base rc=1 | agree |
| BOUND | 4/7 (R1:S131 R2:S132 R3:S133 R7:S118) | 4/7, same four pairs; S128/S129 excluded per counter EXCLUDED | agree |
| SWEPT | 3/3 | R4/R5/R6 each carry a `- UNBOUND R<k> sweep:` block with queries + hosts | agree |
| QUOTE_ROWS | 10 | spans.tsv 10 data rows; quotes.tsv 10 | agree |
| IN_SPAN/IN_ENTRY/IN_LESSON/SHORT/CONTEXT/CAPTURE_BOUND | 10 each | 10/10 each — every span quote ∈ span ∈ capture .txt; max quote 3 whitespace words / 36 chars | agree |
| SUBSTANCE | PASS | tools/quote-substance-check.py rc=0, IDS=5 QUOTES=10 FAILURES=0 | agree |
| ANCHOR_BOUND | 3/3 | S131 271/352, S132 68/1036, S133 19/54 == quote offsets | agree |
| INFERENCE_GROUNDED | yes | tools/inference-ground.py rc=0 | agree |
| STRAY_IDS | - | entry S-ids exactly {S118,S127,S131,S132,S133} | agree |
| before receipt | C3=FAIL | `git show fd95724d:…/c3-before.txt` prints ENTRY=no BOUND=0/7 C3=FAIL exit=1; entry/spans/quotes absent at fd95724d and base; blob byte-identical at freeze and tip | agree |
| freeze integrity | frozen pre-data | c3-count.py blob bff9de03 identical at fd95724d and tip; claims.md unchanged | agree |
| raw↔record binding | genuine fetches | for all 5 manifest (id,url): sha256(.raw) == the successful refetch.tsv raw_sha256 for that URL (4/4 bound + S127 held); no forge pattern in committed rows | agree |

Counter-integrity caveat (lane-disclosed, evidence-verified): the W2 critic's A1a/A1b provenance forge reaches C3=PASS on a fabricated refetch row + replayed bytes — the frozen counter's success leg checks record self-consistency only. The committed state does not exercise the hole (sidecar-audits.md §4: 5/5 PROVENANCE_CONSISTENT=YES, re-run as L1). This is a defect routed for a future re-freeze, not a falsification of this round's measured data.

### Exploratory-claim check

No exploratory claim was declared; both claims are measured. Not applicable.

## 3. No axis harmed (diff 6656f077 → 5dc18607730a)

- SCORECARD.md: single pure-append hunk. freshness → improved (C2 receipts); depth → improved (C3 receipts); coverage → improved narrowly (47 pinned captures lane-owned; census 130→133); calibration → improved (D1 landed; S077 used-by contract fix; QUALITY 111–113); operability → unchanged (gate untouched); adjacency → unchanged (0 contested overlaps). No numeric score invented; operability stays 3/10. Capabilities table +1 row ("Digest-pinned freshness re-fetch", round 57) — demonstrated running by C2 itself.
- LOG.md: append-only (zero deletion lines); Round-57 entry cites existing commits and on-disk pointers.
- Planned-row caveat CONFIRMED: base "## Planned — round 57" named build-spans hardening / process-boundary probes / gate-clause battery / S101 carrier-alphabet leg / grey-literature r41/r48 — NOT R57-C2/R57-C3. Carried honestly in SCORECARD, LOG and the lesson; routed to operator via L0 2c6edbab.
- Fleet root clean of chousa strays: only kake/mado files untracked (other lanes'); the 86-file misroot verified swept byte-exact.
- SHONEN.md byte-identical base→tip (diff --quiet exit 0) — no non-author marks.

## 4. Discernment spot-check (LEARNING.md — the outside check)

| item | gate decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S131 (nmgyyxh repost, 2019 notice R1) | admit, tier B | committed capture 788d2e2f….txt AND live URL (HTTP 200) | AGREE | both manifest quotes verbatim at named anchors (char 271 title, char 352 文号 国卫药政函〔2019〕80号), each unique; anchor math reproduces through the frozen reconstruction; teaches cell grounded by exactly these quotes |
| S132 (catcm repost, 2021 notice R2) | admit, tier B | committed capture a476f412….txt | AGREE | document title + operative sentence `为进一步贯彻落实党中央、国务院关于健全药品供应保障制度的决策部署` present verbatim; ≤25 words |
| S133 (tcmevidence mirror, 2021 指南 R3) | admit, tier B | committed capture 6f545e6c….txt | AGREE | title `药品临床综合评价管理指南` (char 19) and edition `2021 年版试行` (char 54) present verbatim |
| gcpunion R1 repost (key de34c41f…) | refuse, no row | committed capture de34c41f….txt AND live URL (HTTP 200) | AGREE | stated reason holds: full title prints 3× (offsets 7/517/671 committed; count=3 live), so the frozen unique-occurrence heading rule cannot bind; refetch line 129 documents fetch-without-row, consistent with refused-not-unopened |

Sample = 3 admits + 1 reject, all re-opened (2 also live), all agree. Census validator re-run by the integrator: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, five pre-existing W04 duplicate-URL warnings only (S051/S053/S073/S074/S075 rows byte-identical at base — predate round 57). Census receipts census-start.txt/census-end.txt byte-identical (sha256 09ce4a95…), exit=0. SOURCES rows 130 → 133 confirmed (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'` → 130 at 6656f077, 133 at tip); S077/S118/S127 used-by old→new exactly as the lesson logs.

## 5. Trend verdicts (integrator, non-author)

- **expansion — improved.** One new knowledge entry on uncovered normative-reference-chain ground, citing three new mined rows (S131–S133) opened and quoted this round; all three verified genuine; README Round57 frontier map advanced. The forgeable-counter caveat limits counter generality, not this entry's groundedness.
- **quality — improved.** 47 pinned captures carry lane-owned record-backed verdicts (CONSISTENT 46/46 re-derived); routed D1 landed as an append-only corrections block (one stale 表 10 instruction fixed to 表7, nine legitimate mentions preserved); S077 used-by contract defect fixed; QUALITY 111–114 capture four mistake classes with executable red-state evidence; no admitted entry failed its bar this round.
- **discernment — improved.** The outside spot-check (this file, §4) agrees with the gate on every sampled admit and the sampled reject, with the sources re-opened — the LEARNING.md criterion for improved is met on a 4-item sample. The lane self-graded `unchanged` because same-lane wave seats cannot count; the integrator's check is the record.

## 6. Routed defects and caveats (for the lane / operator next round)

1. **(lane, conformance)** Filed-report rewrite: the first committed report (01286956298) was rewritten in place by f47fa39aa5 instead of an appended erratum naming the superseded text; v1 also cited tip 75004f0a before that commit existed (orphaned at filing time; the operative report's citation resolves). PROTOCOL: a filed report is a record — corrections append, never rewrite. Fix next round: erratum-append discipline.
2. **(operator ruling, L0 2c6edbab open)** The lowest-axis/plan obligation is unmet: lowest non-retired axis operability 3/10 was not worked, and the round-56 planned row did not name R57-C2/R57-C3 (freezes were in-round attempt 1). Claims verify and no axis is harmed, so closure admits with this deviation named; grandfather-vs-reject is the operator's call via the open L0 question.
3. **(lane, conformance)** W2 residual was 8 seats, not policy-validated as a 64–128-seat wave, and its role mix (mutation-tester/sentinel) exceeded the residual wording's "reviewer/critic seats". Self-flagged in the report; the v2-validator refusal and the hand-shaped v1 schema are recorded. Total round 73 seats (W1 65 + W2 8).
4. **(lane, counter integrity — recurrence RW-1)** The frozen c3-count.py provenance leg is forgeable (A1a/A1b reach C3=PASS on a fabricated success row + replayed bytes). Committed state is genuine (5/5 provenance audit) and the report discloses this; a future re-freeze must bind each manifest (id,url) to an independently authenticated fetch receipt, or treat the record as self-attestation.
5. **(lane, hygiene — resolved, recorded)** An unidentified-writer file (attempt3-sidecar-audits.md, identity ChousaR57a3) appeared mid-round; correctly handled by L1 re-derivation under own authorship, never adopted. Keep the restore-from-branch rule for future strays.
6. **(fleet, pre-existing)** Five W04 duplicate-URL warnings remain unremediated (predate round 57; out of this round's scope).

## 7. Closure verdict basis

Every declared claim re-measures clean against committed bytes at 5dc18607730a; gate/counter evidence verified without executing the lane's gates; no owned axis harmed; the spot-check agrees with the gate on admits and rejects. Admitted, with defects 1–6 routed above.
