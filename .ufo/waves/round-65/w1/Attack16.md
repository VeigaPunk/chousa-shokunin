# Attack16 — C1 frozen-case bypass attack (seat-scoped summary)

Verdict: the frozen 20-case absolute is real but porous. I constructed 28 nearby
forged/malformed receipts outside the frozen 20; zero overlap with the frozen case set.

- **22 classes the frozen counter never runs** (reference rejects, counter-silent):
  leading-zero/double-zero/trailing-space/tab/0255/+1/hex/space-prefix exits,
  whitespace or tab separator line, whitespace-only body, UTF-8 BOM, digest line with
  no path / double space / space-path / tab separator, uppercase revision,
  revision trailing/leading space, path trailing slash, path dot-prefix, empty file.
  Strongest: `EXIT=007` — survives any `int()`-only exit parse; frozen counter stays 20/20.
- **4 classes even the reference admits** (rc=0): CRLF, CR-only, body header-smuggling,
  NUL-in-body — spec leniency, not C1 failures; parser-differential hazard for downstream
  consumers only.
- **Blob-binding discrimination is incidental**: frozen `valid` case only distinguishes
  working-tree hashing because the tree is dirty at BASE (`SKILL.md` 2ccca333… ≠ blob
  4355e16a…); no structural case enforces "no working-tree hashing".
- Reported-exit forgery (valid digest + EXIT=0 over a failing run) is outside C1's
  declared consistency scope — recorded, not attacked.

Frozen-counter detection: undetected by construction for all 22; freeze forbids adding cases.
Smallest safe correction: future-round extended counter (8 named cases), record CRLF/
parser-differential as reference limitation in the knowledge entry; no frozen-byte changes.

Inputs: claims.md, c1-count.py, controls/ref-receipt-pin.py (HEAD == freeze f99de3bdf,
verified read-only). `tools/receipt-pin.py` absent (before control). Probes: 28 single-shot
validator invocations, no battery. Evidence: `Attack16/report.md`,
`Attack16/attack16-ref-probe-results.json`, `Attack16/attack16-fixtures/` (28 receipts).
Scratch `/fast/scratch/hyaku/chousa-r65/Attack16` deleted; no installs needed.
