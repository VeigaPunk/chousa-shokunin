# RevEntryCitationChainFidelityR24 — freshness re-verification (round 26, 2026-10-21)

Seat: ChousaR26.RevEntryCitationChainFidelityR24-3. Target: corpus/knowledge/citation-chain-fidelity-r24.md at live lane (working tree, base f361d12e44687841e30ec35710ddb366c6f795e0). Axes: (A) recheck command runs at prereg base with explicit fleet root; (B) web anchors still carry quoted text verbatim; (C) entry claims match cited rows/anchors (QUALITY 2/7/8). Read-only; clone /tmp/chousa-r26-RevEntryCitationChainFidelityR24 (branch r26-RevEntryCitationChainFidelityR24, HEAD = f361d12e44687841e30ec35710ddb366c6f795e0, matches prereg base).

## A. Recheck run (QUALITY 13) — PASS, matches entry's round-25 erratum

- Command, clone cwd `/tmp/chousa-r26-RevEntryCitationChainFidelityR24`, base f361d12e…:
  `SHOKUNIN_ROOT=/home/vgpnk/Projects/shokunin bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root /home/vgpnk/Projects/shokunin`
  → `RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)`, `RESOLVED_HOPS=17/22`, **EXIT=0** (1.45 s wall for both runs below).
- Control (header base-line form, same clone): `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..` → `RESEARCH_GATE: DRIFT (… refused=17 … findings=17 drift=17)`, 17× `FINDING CHAIN_SOURCE_OUT_OF_CORPUS … outside allowed roots`, **EXIT=1**. Exactly the entry's r25 erratum claim (citation-chain-fidelity-r24.md:91-96: clone+`--root ..`=DRIFT 17 refused, explicit fleet root=CLEAN exit 0). Placement erratum re-verifies live.
- Freshness clock: header `recheck: 90d` from verified-at 2026-10-19 → due 2027-01-17; not overdue 2026-10-21. SOURCES rows S003/S005 at 365d → due 2027-10-19.

## B. Web anchors re-opened 2026-10-21 — all quotes present verbatim

- S005 https://aclanthology.org/2025.acl-long.1534.pdf (markit text extract of live PDF):
  - §4 p.31790: "Assessing citation fidelity requires measuring how faithfully a citation reflects the original findings of the cited work." — verbatim ✓
  - §6 p.31793: "scientific claims can evolve or degrade, as they are repeatedly paraphrased, summarized, or reinterpreted in subsequent research" — verbatim ✓
  - Figure 1 fn 1 p.31786: "The low-fidelity citation case overstates conclusions by failing to accurately specify the study population." — verbatim ✓
  - §Limits numbers check: "approximately 13 million citation sentence pairs" ✓; supervised 1–5 score ✓ (§4.1); 0.06 intermediary effect ✓ (Figure 5 caption p.31793 / Results pp.31793-31794); S2ORC ✓ (§3.1).
- S003 https://hapgood.us/2019/06/19/sift-the-four-moves/ (live HTML): "trace the claim, quote, or media back to the source, so you can see it in it's original context" and "get a sense if the version you saw was accurately presented" — both verbatim incl. the page's own "it's" typo, in section "Trace claims, quotes, and media back to the original context" ✓.

## C. Claims vs cited rows/anchors (QUALITY 2, 7, 8)

- SOURCES.md:13 S003 and :15 S005 — both tier A, status `mined`, `used-by` names `corpus/knowledge/citation-chain-fidelity-r24.md` (S003 also lists contextual-source-admission-r24.md) → QUALITY 6 header claim in the entry's erratum table is true.
- Local anchors verified: chain-resolution-r3.md:134 "the mode never parses meaning"; :133-137 hop-6 four-vs-five-axes disagreement (entry cites :133-136 — range end one line short of the sentence's last line, cosmetic); :257-258 "By design, not debt: semantic support … outside this mode" (entry cites :258, the sentence's tail line). anchor-boundaries-r4.md:131 "Not semantic support, not agreement, not context." All quoted text matches.
- Fixture: corpus/fixtures/chain-r3.md hop 6 (A:54→S2 quote "Track five axes separately…", note "A names four at A:54, B names five at B:57") matches line 9's and the erratum's use of it; hops 18-22 exempt/blocked as the entry describes.
- SKILL.md decision row (entry cites SKILL.md:19): "chain with each hop's anchor verified or marked unresolved" + never-column "stopping at a summary of the citation" — present verbatim in the decision table.
- QUALITY 7 scoped tier: S005-scoped observations (13M pairs, 0.06, 1–5 scorer) kept separate; web-chain transfer and checklist≈model mapping labelled inference (entry §Limits) ✓. QUALITY 8: `resolved` kept distinct from `faithful` throughout ✓. Erratum's Part A/Part B falsifier split is coherent with line 9 left as written (append-only, QUALITY 4) ✓.

## Findings

1. LOW (documented tension, no action required this round): QUALITY 13's named screen `grep -nE '^recheck:.*--root +"?[^/$"]' corpus/knowledge/citation-chain-fidelity-r24.md` exits 0 today — it hits the preserved base header line 5 (`--root ..`), which the r25 erratum (lines 91-96) supersedes with `--root "$SHOKUNIN_ROOT"`. The screen cannot see supersession, so the entry keeps tripping a check whose substance it now satisfies. Resolvable only by rewriting line 5 (conflicts with append-only QUALITY 4) or teaching the screen about superseded commands — L1/scribe's call, not made here.
2. Cosmetic: entry cites chain-resolution-r3.md:133-136 for the hop-6 passage; the sentence completes at :137. Anchor still resolves; quote verbatim.

No installs. No files written in the clone (read-only checks; git metadata only). No live-lane writes except this report.

VERDICT: re-verifies — recheck CLEAN exit 0 at base with explicit fleet root (base-line `--root ..` DRIFT control matches erratum), all web quotes verbatim 2026-10-21, claims match mined tier-A rows and local anchors.
