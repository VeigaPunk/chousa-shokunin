# Seat SourceHash — chousa lane round65 (w1 scout)

Assignment: re-open `/usr/lib/python3.14/hashlib.py` lines 27–34, verify digest semantics; no authenticity inference. Read frozen claims; verify the freeze. Read-only.

## 1. Digest semantics — observed facts

Source read: `/usr/lib/python3.14/hashlib.py` lines 27–34 (module docstring block shown as lines 26–37; Python 3.14.8, `hashlib.__file__` = `/usr/lib/python3.14/hashlib.py`).

Docstring semantics, verbatim-in-substance:
- `update(data)`: repeated calls are equivalent to a single call with the concatenation of all arguments.
- `digest()`: returns the digest of the bytes passed to `update()` so far, as a `bytes` object.
- `hexdigest()`: like `digest()` but returned as a string of double length, containing only hexadecimal digits.
- `copy()`: returns a copy (clone) of the hash object, for efficient computation of digests sharing a common initial substring.

Empirical probe (isolated, scratch `TMPDIR=/fast/scratch/hyaku/chousa-r65/SourceHash`, python3 3.14.8) — all True:
- `update(b'ab'); update(b'cd')` ≡ single `update(b'abcd')` (concatenation equivalence).
- `digest()` returns `bytes`.
- `hexdigest()` is `str`, length 64 for SHA-256, lowercase hex only, and equals `digest().hex()`.
- `copy()` is an independent clone: mutating the clone leaves the original's digest unchanged.
- Empty-input digest is well-defined (SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`).

Semantic boundary (the assignment's "no authenticity inference"): a digest binds only the exact byte sequence passed to `update()`. It is content identity. It carries no information about who produced the bytes, whether any program executed, what exit code a run reported, or whether the bytes came from the working tree, a Git object, or elsewhere. Equality of two digests establishes byte-identity of content, nothing more.

## 2. Frozen claims — verification

- Freeze commit `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` — "round-65: freeze receipt identity claims and controls", 2026-10-30 11:33:03 -0300 (read-only `git -C ... log -1`, `ls-tree`).
- `git -C ... show f99de3b...:corpus/evidence/round65/claims.md` is byte-identical to the working-tree `corpus/evidence/round65/claims.md`: SHA256 `b9dbca57f4ca1af351459410e1fb7793668fe647c20278d26765b85485ab2fc5` for both (content identity only, per §1 — not an authenticity statement).
- Exactly two claims confirmed: **C1** operability (`tools/receipt-pin.py`, predicate R65-C1 20/20, format REVISION/EXIT/SHA256/path, exits 0/1/2, digest binds the Git blob at the declared revision, no working-tree hashing) and **C2** depth/sourced (`corpus/knowledge/receipt-identity-r65.md`, predicate R65-C2 10/10, structural counter only, no entailment claim). The trailing "Freeze and kill rule" section is not a claim.
- Freeze tree also pins: `c1-count.py` blob `f43bf9f582c99b89dd0632a73310e638ff8b9a83`, `c2-count.py` blob `2d642e72f05b96b0fad3dfef184bf0f9eecc8b3c`, `controls/` tree `6ef7411e7f02c074b91b84ce19c973160189da8d`.
- First read of claims.md truncated at 768 chars; the truncated C2 line was recovered raw in full (knowledge entry sources: installed git-cat-file(1), `/usr/lib/python3.14/hashlib.py`, round64 before receipt S154–S156).

## 3. Cross-read vs claims (inference, labeled as such)

- C1's "Digest binds the Git blob at the declared revision" is exactly the verified hashlib semantics: byte-identity of blob content at a revision; consistent with "No working-tree hashing" and with the absence of any authenticity claim ("This is interface/consistency coverage, not a claim to cryptographic execution authentication").
- C1's "SHA256 full lowercase 64 hex" matches the verified `hexdigest()` behavior (64 lowercase hex chars).
- C2's four-way distinction (object identity / content digest / reported exit / execution authenticity) is supported by §1: `digest()`/`hexdigest()` cover only content identity of bytes handed to `update()`; exit codes and execution are orthogonal facts.

Confidence: high for all observed items (direct source read + probe + read-only git). Remaining unknowns for this seat: none for the assigned question. Counter internals (`c1-count.py`, `c2-count.py`) and the knowledge-entry text itself were not inspected — out of scope; L1 verifies.

## Bounds honored

- Read-only git with explicit `-C` only; no mutations/commits/pushes; no network fetches; no sibling or production writes; no subagents.
- Writes limited to this folder: `report.md`, plus evidence `hashlib-r65-probe.txt` (probe output) and `frozen-claims-f99de3b.md` (byte-identical frozen copy), and the seat trailer file `w1/SourceHash.md`.
- Scratch `/fast/scratch/hyaku/chousa-r65/SourceHash` deleted after receipts were copied to this folder. No `/tmp` evidence. No tool installs (none needed).
