# Seat SourceHash — chousa lane round65 (scoped findings)

Assignment: re-open `/usr/lib/python3.14/hashlib.py` lines 27–34, verify digest semantics; no authenticity inference. Read frozen claims; verify the freeze. Read-only.

## Digest semantics (observed)

`/usr/lib/python3.14/hashlib.py` lines 27–34, Python 3.14.8: `update()` repeated calls ≡ single call on the concatenation; `digest()` returns the digest of bytes passed so far as `bytes`; `hexdigest()` returns a hex-only string of double length; `copy()` returns an independent clone. Probe in scratch confirmed all five properties for SHA-256 (concatenation equivalence, `bytes` return, 64 lowercase hex chars == `digest().hex()`, clone independence, defined empty-input digest `e3b0c442…b855`).

Boundary: a digest binds only the exact byte sequence passed to `update()` — content identity. It implies nothing about authorship, execution, exit codes, or origin. No authenticity inference drawn.

## Freeze verification (observed)

- Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` = "round-65: freeze receipt identity claims and controls" (2026-10-30 11:33:03 -0300).
- Frozen `corpus/evidence/round65/claims.md` is byte-identical to the working-tree copy; SHA256 `b9dbca57f4ca1af351459410e1fb7793668fe647c20278d26765b85485ab2fc5` both sides (content identity only).
- Exactly two claims: C1 operability (receipt-header consistency validator, R65-C1 20/20, digest binds the Git blob at the declared revision, no working-tree hashing, exits 0/1/2) and C2 depth/sourced (knowledge entry, R65-C2 10/10, structural only, no entailment). Freeze/kill rule section is not a claim.
- Freeze tree pins `c1-count.py` `f43bf9f5…`, `c2-count.py` `2d642e72…`, `controls/` tree `6ef7411e…`. Truncated C2 line recovered in full.

Cross-read (inference): C1's blob-digest binding and lowercase-64-hex format exactly match verified hashlib semantics; C2's object-identity/content-digest/exit/authenticity split is consistent with the digest boundary above.

Confidence high. Unknowns: none for the assigned question; counter internals and entry text not inspected (out of scope, L1 verifies).

Full detail: `.ufo/waves/round-65/w1/SourceHash/report.md` (evidence: `hashlib-r65-probe.txt`, `frozen-claims-f99de3b.md`).
