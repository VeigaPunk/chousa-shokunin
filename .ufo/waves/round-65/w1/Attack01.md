# Attack01 — R65-C1 attack report (seat draft, not shipping authority)

## Verdict on the frozen C1 case

The frozen case is **valid**: frozen counter `c1-count.py` and reference validator
`controls/ref-receipt-pin.py` are mutually consistent on all 20 frozen cases
(reproduced `z0`/`z1` exactly: frozen-valid → `RECEIPT_PIN=PASS` exit 0;
frozen-duplicate construction → `RECEIPT_PIN=FAIL header/body` exit 1). This matches the
prefreeze positive control `controls/c1-positive.txt` (20/20). Frozen bytes verified
unmodified: working-tree sha256 of `c1-count.py` (`454286e8…d3dae`), `ref-receipt-pin.py`
(`0719d717…15fa2`), and `claims.md` (`b9dbca57…2fc5`) all equal their blobs at freeze
commit `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`. Lane HEAD == freeze commit.

## Nearby forged/malformed receipts outside the one frozen case — does the frozen counter detect them?

**No.** The counter only executes its 20 fixed cases; every variant below is outside the
frozen set, so `CASES=20/20 C1=PASS` would still print while the target accepts malformed
input. Probed against the frozen reference (bounded, isolated, receipts in scratch only):

| Probe | Construction | Reference verdict | Frozen counter detects? |
|---|---|---|---|
| a1 body-header-smuggle | Valid 4 header lines, then duplicated `REVISION`/`EXIT`/`SHA256` lines inside the **body** | **PASS exit 0** | No — not a frozen case |
| a2 crlf | Same bytes, CRLF line endings | **PASS exit 0** | No — not a frozen case |
| a3 leading-blank-body | Extra blank line as first body line | **PASS exit 0** | No — not a frozen case |
| a4 trailing-header-line | `EXIT=0` appended after the body | **PASS exit 0** | No — not a frozen case |
| b1 forged README receipt | Real `README.md` blob digest at BASE, fabricated body, `EXIT=0` | **PASS exit 0** | No — by design (consistency only) |
| b2 forged nonzero exit | Real `SKILL.md` digest, fabricated transcript, `EXIT=7` | **PASS exit 0** | No — by design (`nonzero-valid` is frozen-valid) |

a1–a4 violate the reference's own docstring contract ("Exactly one of each header, in that
order" + canonical separator/body) yet pass: the validator only inspects `lines[0..3]` and
body non-blank, never header uniqueness inside the body, line-ending canonicality, or body
shape. The frozen `duplicate` case only covers the variant that displaces the separator;
the strictly-stronger smuggle into the body is unguarded.

b1/b2 are **forged provenance accepted by design** — the claim explicitly disclaims
execution authentication, so these are scope boundaries, not C1 defects. But they prove
`RECEIPT_PIN=PASS` carries no execution evidence; scoring must not read it that way
(relevant to C2's identity/digest/authenticity distinction).

Strictness spot checks (all correctly rejected, no trivial regex hole): `EXIT=00`,
`EXIT=+0`, dot-segment path `corpus/./…` (FAIL `path`), backslash path (FAIL `blob/digest`).

## Stronger attack: the counter leaks its answer through the filename

The frozen counter writes each case to `--work/<case-name>.txt` and passes that path via
`--receipt`. The 20 case names (`valid`, `wrong-digest`, `duplicate`, …) are frozen in
`c1-count.py`, and the expected verdict per name is public. A target that never parses the
receipt — a 6-line filename-keyed oracle printing `PASS` for `{valid, nonzero-valid,
max-exit}` and `FAIL …` otherwise — satisfies the counter's exact acceptance check
(`returncode==rc` and the PASS/FAIL token match) on every case. Demonstrated in probe
`d1` against representative cases (`valid`, `wrong-digest`, `duplicate`, `no-body`): all
four would count PASS with **identical receipt content**, only the filename varying.
The counter therefore cannot distinguish a real header-consistency validator from a
filename oracle; `CASES=20/20` is not evidence the target parses anything.

## Impacted axes

- **C1 operability (historical 3/10)**: PASS-token meaning is weaker than the predicate's
  name suggests — 20/20 admits (i) malformed-receipt acceptance (a1–a4) and (ii) a
  non-parsing keyed oracle (d1). Fixable coverage/oracle-binding defects, not a tradeoff
  to reject; the frozen counter itself is unaffected and remains runnable as frozen.
- **Counter authority**: single frozen authority, consistent with its reference — no
  duplicate-authority or identity change found in frozen bytes.
- **Provenance/depth (C2 boundary)**: b1/b2 confirm receipts are self-asserted; only
  blob-digest binding is verified. Consistent with the claim text; no overclaim in C1
  itself, but downstream readers must not treat PASS as authenticity.

## Smallest safe correction (for L1 consideration; frozen bytes unchanged)

1. Counter: write case receipts under opaque random names (e.g. `case-<uuid>.txt`) so the
   filename carries no verdict signal (closes d1), and add a1–a4-shaped variants (body
   smuggle, CRLF, blank-body-prefix, trailing header) as rejection cases (closes the
   malformed-accept gap). Per the freeze/kill rule this cannot replace the frozen counter
   — at most a round-66 proposal; the frozen counter stands for R65.
2. Target (seat-side, allowed now): implement `tools/receipt-pin.py` stricter than the
   reference — enforce header uniqueness anywhere in the file, LF-only canonical form, and
   body shape — while keeping all 20 frozen expectations; stricter acceptance of the frozen
   reject cases is safe only if exit/token stay `RECEIPT_PIN=FAIL …`/1.

## Evidence

- `attack01-probes.json` — full probe transcript (16 cases, exit/stdout per case).
- `attack01-probe.py.txt` — exact probe driver (reproducible; receipts were scratch-only,
  scratch deleted after copy).
- Freeze verification: HEAD `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`; frozen-file sha256
  match working tree (listed above). No frozen bytes altered; no production writes; no
  tools installed this seat.
