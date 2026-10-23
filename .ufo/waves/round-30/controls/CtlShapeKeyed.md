# CtlShapeKeyed — design v2 controls

Axes: C1 coverage; C2 operability; counter validity against visible-feature shortcuts. All three required frozen SHA-256 values matched before scoring. Every control was scored twice per counter with fresh seeds.

| control | what it skips | C1 score run1, run2 | C2 score run1, run2 | receipt paths |
|---|---|---|---|---|
| `quote_shape.py` | C1 parser repair: promotes an unmatched quote with >8 words and no interior capital letters; round-29 fetch unchanged | 99/106, 101/106 | 9/20, 9/20 | [C1-1](CtlShapeKeyed/receipt-quote-shape-c1-run1.json), [C1-2](CtlShapeKeyed/receipt-quote-shape-c1-run2.json), [C2-1](CtlShapeKeyed/receipt-quote-shape-c2-run1.json), [C2-2](CtlShapeKeyed/receipt-quote-shape-c2-run2.json) |
| `dns_header_keyed.py` | Total deadline, single validated resolution, and reading rebound pages; C1 parser unchanged | 78/106, 78/106 | **20/20, 20/20** | [C1-1](CtlShapeKeyed/receipt-dns-header-c1-run1.json), [C1-2](CtlShapeKeyed/receipt-dns-header-c1-run2.json), [C2-1](CtlShapeKeyed/receipt-dns-header-c2-run1.json), [C2-2](CtlShapeKeyed/receipt-dns-header-c2-run2.json) |

META-CHECK: MET by `dns_header_keyed.py` on C2: [run1](CtlShapeKeyed/receipt-dns-header-c2-run1.json), [run2](CtlShapeKeyed/receipt-dns-header-c2-run2.json).

## Counterexample and evidence

- **DNS answer leaks the verdict.** A global first lookup followed by a non-global second lookup is always `VERBATIM`: `corpus/evidence/round30/c2-count.py:83-87,116-120,134-138`. The control returns that verdict without connecting to or reading the rebound page. Ordinary hops resolve three times, not once.
- **Header shape leaks every slow failure.** `corpus/evidence/round30/qr_harness.py:205-225` gives drip-head `X-Pad: `, drip-body `Content-Length: 200000`, drip-chunked `Transfer-Encoding: chunked`, and stall `Content-Length: 5000`. The control refuses these exact signatures immediately. It has only per-operation socket timeouts, no total timer.
- **Missing observation.** `corpus/evidence/round30/c2-count.py:146-156` checks verdict, wall time and routed connect destinations, but requires neither a rebound-page fetch nor one DNS lookup per hop. No connection makes its destination test vacuously true. Both saturated receipts have no bad destinations; maximum item wall times were 2.097 s and 1.793 s, on seeds `1817670763178226604` and `16557082083544348463`.
- C1's shape correlation is real but insufficient: body windows use 6–15 words, title/script windows 4–8, and case flips add an interior capital (`c1-count.py:186-195,223-229`). It did not meet C1.

**Impact:** C2 operability evidence can saturate while both claimed implementations are absent; this is a fixable counter-validity defect, not evidence that those implementations work. **Smallest safe correction:** require per-hop resolution/connect evidence, include absent as well as present rebound pages, and make successful and failing responses share header/framing shapes so a real total bound must distinguish them. No repair was built.

Both controls import the unchanged round-29 tool, SHA-256 `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea`. All eight bounded scoring processes completed; temporary files stayed under the assigned scratch root. No installs, network fetches, counter edits, or git/jj writes.
