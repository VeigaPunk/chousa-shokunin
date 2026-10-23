# Round 31 — a claim's named line and the revision it read

Dates are UTC. Base `be7b8d8d54962286417465a305fd9a1a7b3b1525`. Rounds 29 and 30 both worked
`tools/quote-reopen.py`; this round does not touch it. Two claims, both on the local
claim-vs-source gate `tools/research-gate.sh verify-claims`:

- **C1 coverage** — a claim may name a line or line range (`"line"`); a span found elsewhere
  reads `mislocated`. Frontier item: "pairing a span's occurrence with a named pointer line"
  (`corpus/README.md` Round26 disposition), "location binding" (round 4).
- **C2 operability** (lowest scored axis) — `SKILL.md` checklist item 1's revision clause
  ("…and revision read") becomes runnable for every claim that carries a `"sha256"` pin of the
  exact source bytes; a changed source reads `stale`.

Frozen design: `corpus/evidence/round31/claims.md` (v1 at `d78d1889`, v2 at `8070f92b`, both
before any candidate was scored). Control receipts: `.ufo/waves/round-31/controls/` (v2 re-score
committed at `86188116`). Landed: C1 at `c17948a7`, C2 at `6d0ae19f`.

## Spot-check intake (round 30, `round-30-verifier-spotcheck.md:163-205`)

| Routed defect | Disposition in round 31 |
|---|---|
| D1 README and capabilities row contradict the C2 miss | dated corrections appended to `corpus/README.md` (Round30 disposition) and `SCORECARD.md` (Capabilities, round-30 change); drafted by ScribeD1 |
| D2 backlog diagnosis stated as fact | corrections in `corpus/lessons/round-30.md` and `SCORECARD.md` mark it `[INFERENCE]`; the 18 backlog-128 receipts are committed byte-exact with a manifest at `.ufo/waves/round-31/build/ExecD2Backlog/bl/` (they ran the frozen v4 counter with a scratch harness that adds only `request_queue_size = 128`; they show success under that harness, not the cause) |
| D3 "four controls" | correction in `corpus/lessons/round-30.md` (three control findings, two control-forced redesigns). The round-30 fleet report is not lane-writable; noted in the round-31 report |
| D4 C1 re-run count | correction in `SCORECARD.md` and the lesson: 35 distinct committed C1 after-receipts, 32 at 106/106 and 3 low-cap inconclusive; RerunC2B 20/23 (`.ufo/waves/round-31/build/ExecD4Rerun/`) |
| D5 v4 control maximum | correction in the lesson: overall 86/106, best no-reader 84/106 (`build/ExecD5Controls/`); the SCORECARD wording ("best C1 no-reader 84/106") was already accurate |
| D6 dead seat re-issued; refused seat's files | correction in the lesson: CriticS047Live → LiveS047After was a retry in the same role; `leak-map.py` and `metadata-audit.py` are unreviewed output of a refused seat |
| D7 S052 Gate error not mined | `## Mistakes` row below; QUALITY criterion 30 |
| D8 wrong pointers | corrections in the lesson (finding 13, not 7), `SCORECARD.md` (a second DiffToolB network run) and `corpus/lessons/round-25.md` (the D4 quote came through NCBI E-utilities). Report-only pointers (`7908ce2a`/`bf657822`, `dad857af`, 03:52Z) are fleet-report items, listed in the round-31 report |
| Carried | the L0 fetch-scope question (fleet `8d77e6c1`, unanswered: `build/ScoutOperatorL0.md`); quote-reopen items (resolver time, hop timers, MutHeadNoText, 2xx pages, IPv6, no `<head>`) stay carried — anti-loop |
| operator `*.md` teachings | none exist (`build/ScoutOperatorL0.md`) |

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A Gate quote was truncated and given a period not in the source (round 30, S052) | `corpus/lessons/round-30.md:47` and its correction; `.ufo/waves/round-30/falsify/AttackRowS052.md:3-15`; routed D7 | round-30 falsify re-open; no QUALITY rule | QUALITY 30: re-open every new Gate quote with `tools/quote-reopen.py` and admit only on `VERBATIM`; shown able to fail on the S052 input (`ABSENT`, exit 1) |
| A dead seat's task was re-sent in the same role while the report said none was retried (round 30) | `corpus/lessons/round-30.md` Seats and holds; spot-check `:65-69` | none | this round's seat accounting is checked by RevengerD6Retry31 against the dispatch files; no dead seat's task is re-sent |
| A count was stated without enumerating its receipts ("four controls", round 30) | spot-check `:42-51` | none | counts in this lesson cite the receipt directory they come from (QUALITY 27 shape) |
| An `[INFERENCE]` was restated as fact (backlog, round 30) | spot-check `:112`; `RerunC2B.md:45,57` | none | the D2 correction keeps the tag; mechanism claims in this round's prose carry the seat's tag |
| A counter drew sub-variants at random, so a gate that mishandles one kind passed the seeds that drew none (round 31 v1) | `controls/ChousaR31.CtlShortcutC2/` trim control 120/120 on seed 9002; `controls/MutOracleC2.md` trim mutant 120/120 on one seed | the pre-data control wave | v2 fixes every sub-variant count; the same control scores 118/120 on every seed (`controls/ChousaR31.CtlShortcutC2/v2/`). QUALITY 31 |
| A counter checked the verdict but not the finding the contract requires (round 31 v1) | CriticClaimDesign31 F2 (`controls/ChousaR31.CriticClaimDesign31.md`) | the control wave | v2 matches a claim only when the finding names exactly the claims with that verdict; no-reader 88/120 with findings, 30/120 without (`controls/CtlNoReaderC1/v2/`). QUALITY 32 |
| A shortcut met the C1 counter: binding by the span's first and last tokens only (round 31 v1) | `controls/CtlShortcutC1/endpoint-exact-seed93101{1,2,3}.json` 120/120 | the control wave | v2 adds inner-word damage with intact endpoints and wrong ranges that keep the true start or end line; endpoint-exact 112, start-only 116, end-only 102 (`controls/CtlShortcutC1/v2/`) |
| A seat's edit followed a path into the lane gate (round 31) | CriticSeparability31 edited its `v1/tools/research-gate.sh`, which reached the lane file; the lane gate held its C1 sketch from about 04:26:19Z until the seat restored the base bytes at 04:26:45.9Z (`claims.md` Disclosures) | the seat's own `git diff`; none in a rule | the falsify-wave context forbids symlinked or hard-linked copies and edits that reach the lane; the L1 checks the lane gate's SHA-256 before every scoring run |
| The L1 ran an uncommitted counter draft while a seat had changed the lane gate (round 31) | the L1 saw `LINE_BINDING_MATCH=84/120` from the lane gate at about 04:26:45Z; the base gate prints 50/120 | the L1's own surprise at an impossible score | disclosed in `claims.md`; no design change responds to it; measurements run only after `git diff --quiet -- tools/` and a SHA-256 check |

## Gate

Sources opened on 2026-10-23. Each quote is at most 25 words, copied from the opened bytes.

| Row | URL | Located quote | Verdict |
|---|---|---|---|
| S057 | https://www.rfc-editor.org/rfc/rfc5147.txt §2.2.3 "Line Position" | "Line position counting starts with zero, so the line position before the first line of a text/plain MIME entity has the line position zero" | admit, tier A (IETF RFC), mined; opened by the L1 (HTTP 200, 37422 bytes, SHA-256 `c8fff6f2…24f4`) |
| S058 | https://www.w3.org/TR/2016/REC-SRI-20160623/#does-response-match-metadatalist §3.3.5 | "If actualValue is a case-sensitive match for expectedValue, return true." | admit, tier A (dated W3C Recommendation), mined; opened by ScribeSrcSRI (HTTP 200, 89641 bytes, SHA-256 `947d942a…2c75`) |
| S059 | https://docs.python.org/3/library/hashlib.html#hashlib.hash.hexdigest | "Like digest() except the digest is returned as a string object of double length, containing only hexadecimal digits." | admit, tier A (Python docs), mined; opened by ScribeSrcHashlib (HTTP 200, 121928 bytes, SHA-256 `553f4f2a…af10`); the page does not say lowercase, so the lowercase rule is the lane's own |

Rejected fetch: `https://www.rfc-editor.org/rfc/rfc5147` answered 301 to
`https://www.rfc-editor.org/info/rfc5147/` with an empty body; ScribeSrcRFC5147 did not follow
it and drafted no quote. Same host, so the L1 opened the plain-text RFC instead (S057). Flip:
none needed.

Status changes to existing rows: none. New rows S057 to S059 enter as `mined`; S057 used by
`corpus/knowledge/line-binding-r31.md`, S058 and S059 by `corpus/knowledge/revision-binding-r31.md`.
On-release own-work rows that describe the gate (S001, S034-S036, S040-S043, S045) are re-read
by ScoutOnReleaseRows31 in the falsify wave.

## Census

Start (base): `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` →
`chousa ok`, exit 0, two W04 warnings; 56 rows, tier A 50 B 1 C 5, mined 33 queued 19 rejected 4
(`.ufo/waves/round-31/build/ExecCensusStart.md`). End: in the round-31 report and SCORECARD.

## Design history before data

v1 (`d78d1889`) went to a ten-seat control wave. Three controls broke it: a whitespace-trimming
validator met C2 on some seeds, an endpoint-only binder met C1 on every seed, and the counters did
not check the required findings. v2 (`8070f92b`) fixed sub-variant counts, added the finding
rule, scrubbed `CHOUSA_*` from the gate's environment, and froze the C2 wording and the SKILL.md
landing line. Every control was re-scored under v2 (`86188116`): C1 max 116/120 (start-line-only
binding, which misses the four wrong ranges that keep the true start on every seed), C2 max 118/120
(trim), disclosed oracles 120/120. CtlShortcutC1 proposed a v2.1 that makes all eight wrong
ranges keep the true start (start-only 112). The L1 kept v2: no control meets 120/120, the class
counts are fixed, so a start-only binder misses the same four claims on every seed and P1 rejects
it every time; a third version after the re-score would only widen the margin.
