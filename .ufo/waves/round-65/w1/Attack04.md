# Attack04 — C1 no-revision neighborhood attack (round 65, seat critic draft)

Seat: Attack04 (leaf critic, chousa lane). Date 2026-10-30. Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`, base `d6ed8155e9b4735639a2cf0a3e479c62f2056195`.
Frozen bytes inspected (never altered, read-only execution only):
- counter: `corpus/evidence/round65/c1-count.py` (20 frozen cases, exact exit + token match)
- reference validator: `corpus/evidence/round65/controls/ref-receipt-pin.py` (docstring self-scopes: "header consistency, not execution authenticity")
- claim text: `corpus/evidence/round65/claims.md` C1; lesson gate `corpus/lessons/round-65.md` ("Reject the inference that a matching header proves an execution").

## Verdict

The frozen `no-revision` case is robust — every header-presence mutation adjacent to it is rejected. But the reference validator accepts **4 nearby malformed/forged receipts that no frozen case covers**. The frozen counter does **not** detect them: it awards `CASES=20/20 C1=PASS` to a validator exhibiting all four laxnesses (reproduced in scratch, evidence below). This is a coverage gap plus declared non-goals, **not** a provenance break and **not** grounds to reject C1: the claim already scopes itself to "interface/consistency coverage, not a claim to cryptographic execution authentication or general parser safety."

## Probe results (bounded, isolated; scratch only; ref executed read-only)

| probe | family | ref rc | ref stdout | verdict |
|---|---|---|---|---|
| p1 doubled separator (`\n\n\n` before body) | malformed framing | 0 | RECEIPT_PIN=PASS | **ACCEPTED-BYPASS** |
| p2 NUL-only body | malformed body | 0 | RECEIPT_PIN=PASS | **ACCEPTED-BYPASS** |
| p3 valid headers + forged body text | forgery | 0 | RECEIPT_PIN=PASS | **ACCEPTED-BYPASS (declared non-goal)** |
| p4 genuine receipt + concatenated 2nd receipt in body | framing ambiguity | 0 | RECEIPT_PIN=PASS | **ACCEPTED-BYPASS** |
| p5 uppercase revision hex | near no-revision | 1 | RECEIPT_PIN=FAIL header/body | rejected-ok |
| p6 revision + trailing space | near no-revision | 1 | RECEIPT_PIN=FAIL header/body | rejected-ok |
| p7 leading blank line | near no-revision | 1 | RECEIPT_PIN=FAIL header/body | rejected-ok |
| p8 `EXIT=00` leading zero | near overflow | 1 | RECEIPT_PIN=FAIL header/body | rejected-ok |
| p9 tab as separator | near no-separator | 1 | RECEIPT_PIN=FAIL header/body | rejected-ok |
| p10 body = single space | near no-body | 1 | RECEIPT_PIN=FAIL header/body | rejected-ok |
| p11 two spaces digest/path | near path-canonical | 1 | RECEIPT_PIN=FAIL blob/digest | rejected-ok |

Root causes in `ref-receipt-pin.py`: (a) separator check is only `lines[3]==''` — nothing pins the body to start at `lines[4]` nonempty; (b) body nonemptiness is `strip()`-based, so control-only bodies pass while the frozen `no-body` case only covers the empty body; (c) the body is self-reported and unauthenticated — nothing binds output bytes to any execution (explicitly disclaimed); (d) trailing bytes after the body are opaque "output", so a second receipt block concatenates without detection.

Overlap check: none of the four accepted receipts equals any of the 20 frozen case texts (asserted programmatically, `False x4`). Counter reproduction: `CASES=20/20 C1=PASS` against the frozen ref in this seat's scratch work dir.

## Impacted axes and classification

- **C1 (frozen counter)**: undetecting by construction — the 20 cases are frozen and exclude these shapes. Counter still meaningfully blocks always-pass (3/20) and always-fail tools; the gap is strictness, not scoring integrity.
- **Forgery axis (p3, p4)**: declared non-goal. Claim text, ref docstring, and lesson gate all disclaim execution authenticity. A fixable defect only if any seat later overclaims "receipt proves execution" — L1 should slap that down in integration.
- **Parser-safety axis (p1, p2)**: real laxness, small blast radius (digest still binds the named blob at the pinned revision in every accepted case; no false provenance is created). Tradeoff the judge may accept given the in-claim disclaimer.

## Smallest safe correction

Zero frozen-byte changes (kill rule). For the to-be-acquired `tools/receipt-pin.py` target only: optionally tighten to `len(lines) >= 5 and lines[4] != ''` and require the body to contain at least one printable character — this keeps all 20 frozen cases green while closing p1/p2. For future counters (not this freeze): add doubled-separator, control-only-body, and concat-tail cases. No C1 scoring change is warranted; no counter/predicate/target rewrite is requested.

Environment note (out of scope, recorded): the ref resolves `git` from inherited PATH; the counter invokes targets with the inherited environment. Same trust domain as the rest of the lane tooling; not a C1 defect.

## Evidence (this seat's w1 folder)

- `attack04-probe-results.json` — machine-readable probe table
- `attack04-p*.receipt` — the 11 crafted receipts (4 accepted, 7 rejected)
- `attack04-counter-run.txt` — frozen counter 20/20 reproduction vs frozen ref

All probes ran in `/fast/scratch/hyaku/chousa-r65/Attack04/` (deleted on exit, no /tmp evidence, no production writes). No tools installed. Read-only git used with explicit `-C`. Lane repo HEAD verified at freeze `f99de3bd…` before probing; scratch deleted after receipts copied.
