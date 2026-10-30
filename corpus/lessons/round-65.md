# Round65 — receipt consistency is not execution proof

author: chousa L1 ChousaR65
Date: 2026-10-30. Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd against base d6ed8155e9b4735639a2cf0a3e479c62f2056195. Exactly two claims: C1 operability, C2 depth (sourced). No earlier planning suggestion is a frozen claim.

## Gate

Admit corpus/knowledge/receipt-identity-r65.md narrowly: interpreting lane-owned research receipts, not general orchestration or cryptographic attestation. Reject the inference that a matching header proves an execution. Outside non-author spot-check remains required; wave seats dispatched by this lane are still lane-authored evidence. Suggested sample: admit S155 and reject S157.

| row | URL/path opened 2026-10-30 | location and <=25-word quote | decision |
|---|---|---|---|
| S154 | file:///usr/share/man/man1/git-cat-file.1.gz | Git2.56.0 manual dated2026-09-27, OUTPUT: `If <type> is specified, the raw (though uncompressed) contents of the <object> will be returned.` | A for object-content output only |
| S155 | file:///usr/lib/python3.14/hashlib.py | Python3.14.8 module documentation line 31 (bullet spans 31–32): `Return the digest of the bytes passed to the update() method` | A for installed digest semantics |
| S156 | corpus/evidence/round64/controls/c1v3-before-full.txt | line1 `LEG CLEAN clean ok ok`; line44 is the failed aggregate | B for receipt text, not historical execution authenticity |
| S157 | corpus/evidence/round65/controls/ref-receipt-pin.py | module docstring first sentence: `Validate receipt header consistency, not execution authenticity.` | rejected C as execution proof; flip independent command/bytes/result binding |

Registry:153->157 rows; new A2/B1/C1, mined3/rejected1. No held status/recheck/used-by cells changed. Search question: what does a receipt's digest actually establish? Local installed manual/module and lane evidence only; identified4,screened4,included3,excluded1; stop because these settle object/digest interpretation, not execution proof. No network fetch or live-target approval assumed.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| Before receipt relies on surrounding provenance instead of self-contained headers | round64 verifier-spotcheck section5 item3; corpus/evidence/round64/controls/c1v3-before-full.txt:1,44 | none requiring this exact format; QUALITY42 supplied a broader binding rule | receipt-pin introduces a narrow in-file revision/exit/blob-digest consistency check. Red-before uses retained r64 receipt; twenty-case controls also fail on missing headers. It does not authenticate output or retrospectively repair the old receipt. |
| Evidence-only counters lack explicit gate-registry disposition | round64 verifier-spotcheck section5 item2 | gate registry completeness duty | SKILL.md appended evidence-only honest-stop exemption naming r64 c3-count, supplement and runner; old failed predicates unchanged. No new general detector claimed. |
| A fixed-case black-box counter cannot distinguish a parsing validator from an argv-keyed lookup table (reviewer demo scored 20/20 without parsing receipts) | .ufo/waves/round-65/w1/ReviewFreeze/c1-boundary-probes.txt and findings 1–5; Attack05/13/16 nearby-forgery probes | none frozen — claims.md scopes C1 to interface/consistency coverage, not general parser safety | the landed tools/receipt-pin.py was written from the frozen format contract and read by the L1 before admission (ReviewFreeze's recommendation); wave-2 review seats re-read the landed implementation; a successor freeze could add implementation-independent negative cases |
| The validator answered every environment fault with a receipt verdict (exit 1) although the frozen contract assigns "2 usage/environment" | wave-2 `R65R01.md` finding F1 and `R65C01.md` finding 1 — missing `git`, a non-repository `--root` and an unreadable receipt all exited 1 | the frozen contract sentence "0 consistent,1 invalid,2 usage/environment" (`corpus/evidence/round65/claims.md` C1) | `tools/receipt-pin.py` now separates the taxonomy: an explicit environment probe (`git -C ROOT rev-parse --git-dir`) and an OSError branch return exit 2 with `RECEIPT_PIN=ERROR` on stderr, while receipt-content defects keep exit 1; re-measured at the new tip, CASES=20/20 C1=PASS exit 0 |
| A structural sourced-entry counter attests an entry's shape, not its substance: a 9-line boilerplate entry plus three stub registry rows and a README mention also score 10/10 | wave-2 `R65C03.md` (boilerplate control ENTRY_CHECKS=10/10 exit 0) and `R65M02.md` (M5b 116-byte token stub 10/10; M6 cites non-existent ids S1549/S1559/S1569 and still 10/10; M2a–M2c strip a source id from the header and survive) | none frozen — claims.md concedes "a boilerplate entry could pass"; the round-sizing rule (a target must be unreachable by a do-nothing control) does bind | C2 is reported unprovable / not admitted on its counter; the entry stays landed with its three sources re-opened and reviewed; QUALITY criterion 131 records the rule; a successor freeze needs a semantic counter (per-id citation reconciliation against `corpus/SOURCES.md` and non-empty claim bodies) so the after-state is do-nothing-unreachable |

## Prior closure routed items

1. Literal frozen C1 output appended to Gates table in adjacent historical-instrument row; no rewrite of historical measurements.
2. Three historical instruments explicitly exempted as evidence-only honest-stop artifacts; successors cannot treat them as admission passes.
3. New validator and revision/exit-bearing prefreeze controls; final receipts also carry blob digest. The old before receipt remains unmodified.
4. Report pointers explicitly identify lane repo unless stated fleet.
5. SHONEN remains four author assertions; no promotion review manufactured.
6. Prior consideration correction remains intact. No sibling edits.

## Assimilation and considerthese

Assimilation: none. No staged source/knowledge appended. Round42 already adjudicated the quarantine-first slice; package remains read-only. No collision check is used to justify an append because none occurs.

CT-20261026-4 (independent CJK quote spot-check) remains carried without implementation credit: lane-dispatched review cannot supply outside independence or daily cadence. This round adds no second proposal implementation.

## Attempt-2 continuation (2026-10-30, ChousaR65a2)

Attempt 1 (ChousaR65) froze these claims at f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd, ran the before
measurements and wave w1 (64 seats, dispatched 11:47 -03), drafted the corpus edits above, and died at
12:08 -03 without committing or filing a report. This attempt inherits and re-verifies: all four row
digests in corpus/evidence/round65/source-openings.json re-verified byte-exact against the installed
or committed files, and each quote re-located (S154 OUTPUT sentence in the Git 2.56.0 man page, S155
lines 31–32, S156 lines 1 and 44, S157 docstring first sentence). tools/receipt-pin.py was implemented
this attempt from the frozen format contract; the frozen counters measure CASES=20/20 C1=PASS exit 0
and ENTRY_CHECKS=10/10 C2=PASS exit 0 (receipts corpus/evidence/round65/controls/c1-after.txt and
c2-after.txt), while the do-nothing stubs stay at 3/20 and 17/20. Wave-1 attack seats found only
fixed-case-oracle coverage boundaries inside the claims' disclaimed scope; the third Mistakes row
above records the sharpest of them.

## Boundaries and continuation

C1's frozen counter enumerates twenty cases, not universal input correctness. C2 checks structure and citations, not entailment. Generic testing belongs adjacent to tameshi; dispatch/receipt lifecycle to kumitate. This lane's work is the interpretation and checking of its own research evidence. Open fetch-scope and receipt-identity L0 questions remain unanswered and are routed around with local reads only.

L1 boundary probes on the landed validator (`corpus/evidence/round65/controls/l1-boundary-probes.txt`): a CRLF receipt is accepted (universal-newline read plus `splitlines()`), while `EXIT=00`, a `./`-prefixed path and a whitespace-only body are refused, a bad `--revision` exits 2 and an absent receipt exits 1. The frozen 20 cases pin no byte-exact line endings, so CRLF acceptance is a disclosed behaviour of the landed tool rather than a measured failure — w1 ReviewFreeze finding 1 anticipated it. A successor freeze could pin byte-exactness; this round does not rewrite the frozen counter.

## Wave-2 falsify findings (2026-10-30, 32 seats dispatched, 29 reported, 3 released un-settled)

Wave-2 attacked the landed bytes at 9672a2e: re-runs of both frozen counters (R65E01–R65E08), four reviews
(R65R01–R65R04), four critics (R65C01–R65C04), two mutation tests (R65M01, R65M02), eight scouts, four
scribes and two connectors. Findings that changed the round:

1. C1's sizing holds — the always-pass stub reaches only 3/20 and the always-fail stub 17/20 (R65C03), so
   the 20/20 target is unreachable by a do-nothing control. The frozen counter reproduces byte-for-byte at
   the tip (R65E01) and the landed validator passes 20/20.
2. The frozen oracle under-pins the contract: 11 behavioural mutants of the validator, 6 killed and 5
   survived (R65M01). Every survivor is a coverage gap of the frozen case list, not a defect of the shipped
   validator — the pristine tool rejects all four live probes. The `..` guard is an equivalent mutant
   (git refuses every `..` path in `rev:path` syntax).
3. The exit taxonomy deviated from the frozen contract: environment faults returned 1 instead of 2
   (R65R01 finding F1, R65C01 finding 1). Fixed this round — see the Mistakes row; re-measured at the tip.
4. C2's counter attests shape, not substance: a boilerplate entry also scores 10/10 (R65C03, R65M02). C2 is
   therefore reported unprovable / not admitted on its counter; see the SCORECARD round-65 verdict.
5. Two cosmetic location imprecisions in the knowledge entry's located quotes were corrected (the
   git-cat-file quote's `<object>` notation; the hashlib quote's span, line 31 rather than 31–32) after
   R65R02 re-opened all three sources and found no misquote and no overreach in the four claims.
6. The registry rows S154–S157 conform to the CORPUS.md contract (R65R03: 11 columns, tier scope, located
   anchors, reciprocal used-by, the rejected row keeping reason and flip).
