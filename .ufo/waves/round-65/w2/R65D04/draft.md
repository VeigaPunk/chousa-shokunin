# Round65 report — draft SHONEN section and limitations paragraph (seat R65D04, scribe)

Draft only. `SHONEN.md` was not edited. Lane tip observed read-only at `a6b6f9396a825558edd1fdddaa2b43cb5f0a6bfe`
(`9171732` w1 results, `9672a2e` after-measurements + SCORECARD verdict, `0a85189` implementation, `f99de3b` freeze).

Marker rule applied: `[x]` only where a **named non-author** verified the box; `[~]` for a lane assertion.
No such non-author exists for round 65 — there is no `corpus/lessons/round-65-verifier-spotcheck.md`
(`ls corpus/lessons/ | grep -c 'round-65-verifier'` → `0`) and no fleet `chousa.md` under `.ufo/reports/round-65/`.
Wave-2 seats are lane-dispatched and therefore lane-authored evidence (`corpus/lessons/round-65.md:8`).
All four boxes therefore stay `[~]`, exactly as the round-64 closure left them
(`corpus/lessons/round-64-verifier-spotcheck.md:77`).

---

## Draft `## SHONEN` (four lines, one per box)

- [~] Decision tables/error patterns/checklists/sources: `SKILL.md` `## Decision table` (L13), `## Error patterns` (L41), `## Checklist (executable)` (L67), `## Gates` (L79), plus the round-65 rows `receipt-pin` (L159) and `round65 claim counters` (L160); cited sources S154–S157 in `corpus/SOURCES.md:164–167`; sourced entry `corpus/knowledge/receipt-identity-r65.md`. Author assertion — no non-author verifier for round 65.
- [~] End-to-end work executed/logged: `LOG.md` Round 9 archive verification and `corpus/fixtures/archives-r9/` (r25 explicit-root hold battery) remain the standing end-to-end pointers; this round's landing is recorded in `SCORECARD.md` `## Round65 verdict` (L3074) and `corpus/lessons/round-65.md`, but `LOG.md` carries **no round-65 section** at tip `a6b6f93` (last heading `LOG.md:2023` = Round64 attempt2) — the L1 must land the LOG entry before the report points at one. Author assertion; no non-author verifier.
- [~] Executable without oral context: `bash tools/research-gate.sh --selftest`; round-65 additions run without oral context — `python3 corpus/evidence/round65/c1-count.py --work DIR` (re-run by this seat at tip `a6b6f93`: `CASES=20/20 C1=PASS`, exit 0) and `python3 corpus/evidence/round65/c2-count.py` (`ENTRY_CHECKS=10/10 C2=PASS`, exit 0), and `python3 tools/receipt-pin.py --receipt FILE --root LANE --revision FULL_HASH` with the literal exit map and `RECEIPT_PIN=PASS|FAIL` tokens (`SKILL.md:159`). Author assertion; no non-author verifier for round 65.
- [~] Province accuracy/no bleed: `PROVINCE.md` unchanged since `3282042` (2026-10-14) — `git diff d6ed8155e9b4735639a2cf0a3e479c62f2056195 a6b6f9396a825558edd1fdddaa2b43cb5f0a6bfe -- PROVINCE.md` is empty; scope routing recorded at `corpus/lessons/round-65.md:58` (generic testing → tameshi, dispatch/receipt lifecycle → kumitate) and in `.ufo/waves/round-65/w1/ConnectScope/report.md`; no sibling write. Author assertion — box 4 explicitly awaits the outside verifier (`corpus/lessons/round-64-verifier-spotcheck.md:77`).

## Draft limitations paragraph (round-65 limits, named)

Round 65 establishes header/blob **consistency**, not execution authenticity, and its limits are the same
limits the frozen claims already declared. (i) *Fixed-case oracle boundary*: C1's frozen counter enumerates
twenty named interface cases (`corpus/evidence/round65/c1-count.py:16`), not universal input correctness —
`corpus/evidence/round65/claims.md:7` scopes it to "interface/consistency coverage", and the counter is
black-box enough that an argv/basename-keyed lookup table scored `CASES=20/20 C1=PASS` without parsing any
receipt (`.ufo/waves/round-65/w1/ReviewFreeze/c1-boundary-probes.txt`, `robust.basename-gamer`;
recorded at `corpus/lessons/round-65.md:25`); the frozen cases also pin no byte-exact line endings, so the
landed validator's CRLF tolerance is a disclosed interface behaviour, not a measured failure
(`corpus/evidence/round65/controls/l1-boundary-probes.txt`, `crlf -> exit=0`) — re-verified by this seat on the
landed tool (`printf 'REVISION=d6ed8155…\r\nEXIT=0\r\nSHA256=<sha> SKILL.md\r\n\r\nmeasured output\r\n'` then
`python3 -B tools/receipt-pin.py --receipt <crlf> --root . --revision d6ed8155…` → `RECEIPT_PIN=PASS`, exit 0).
(ii) *Forged-body limit*: the
digest binds the named Git blob, never the receipt body — `tools/receipt-pin.py:10–12` states "Header
consistency is NOT execution authenticity", `corpus/knowledge/receipt-identity-r65.md:16` states that a person
can write an arbitrary body and `EXIT` alongside a genuine blob digest, and the wave-1 forgery probe
`.ufo/waves/round-65/w1/Attack04/attack04-p3-forged-body.receipt` (body `forged: all checks green`) is
`ACCEPTED-BYPASS` by the reference validator (`attack04-probe-results.json`, probe `p3-forged-body`); this seat
re-verified the same bypass on the **landed** tool — a receipt carrying the genuine `SKILL.md` blob digest at
base `d6ed8155` but the body `forged: all checks green` returns `RECEIPT_PIN=PASS`, exit 0;
`corpus/QUALITY.md:1014` (criterion 130) records the same bound. (iii) *Execution authenticity remains
unproven*: there is no command/body binding, signature, trusted timestamp or process attestation, so a
`RECEIPT_PIN=PASS` proves only that the receipt is self-consistent with a caller-selected blob; the intent
docstring was itself rejected as execution proof (`corpus/SOURCES.md:167`, S157), and no receipt-identity debt
from round 1 is closed. (iv) *Two L0 questions are still open and were routed around, not answered*: the
fetch-scope ruling `8d77e6c1` (fleet `.ufo/l0-questions.md:136` and `:140`) and receipt identity
(`.ufo/l0-questions.md:51`, open as an in-lane debt since round 1) — this round used local reads only
(`corpus/lessons/round-65.md:58`). (v) *No outside spot-check exists*: round-65 seats are lane-dispatched and
count as lane-authored evidence (`corpus/lessons/round-65.md:8`), the suggested outside sample — admit S155,
reject S157 — has not been taken by a non-author, and the round-64 closure's own operator note keeps all four
SHONEN boxes at `[~]` (`corpus/lessons/round-64-verifier-spotcheck.md:77`). Nothing in this round is a
promotion review, and no SHONEN box was upgraded.
