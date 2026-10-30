# Probe05 — round65 wrong-revision receipt probe (scoped seat report)

Date: 2026-10-30. Lane freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Seat: Probe05 (leaf probe). Surface: **receipt revision vs caller-supplied `--revision`** only.
No full battery run; no production writes; no git mutations; one read-only `git -C` lane repo.

## Method

Built an isolated fixture set in scratch (`/fast/scratch/hyaku/chousa-r65/Probe05/`, since
deleted) and ran the frozen reference `corpus/evidence/round65/controls/ref-receipt-pin.py`
under argv shape identical to the C1 counter:

```
python3 -B <ref> --receipt <fixture.txt> --root <LANE> --revision <rev>
```

Expectations derived **independently from the frozen format contract** in
`corpus/evidence/round65/claims.md` (C1): header `REVISION` is full lowercase 40 hex and
"revision must equal caller-supplied `--revision`"; exit legend `0 consistent, 1 invalid,
2 usage/environment`. Mismatch therefore ⇒ invalid ⇒ exit 1, never 2 (the receipt is
well-formed; the environment is fine). Digest for the valid arm was computed directly
with `git cat-file blob d6ed8155e9b4735639a2cf0a3e479c62f2056195:SKILL.md | sha256sum`
= `4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a` (BASE =
`d6ed8155e9b4735639a2cf0a3e479c62f2056195`, the claims' base master, not the freeze rev).

## Fixtures and results (5/5 match derivation)

| Fixture | Receipt declares | Caller `--revision` | Expected | Actual | Stdout token |
|---|---|---|---|---|---|
| valid-control | BASE, digest@BASE | BASE | 0 | 0 | `RECEIPT_PIN=PASS` |
| wrong-rev-zeros | `0000…0` (40), digest@BASE | BASE | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| wrong-rev-other-commit | FREEZE `f99de3bd…`, digest@FREEZE (internally consistent) | BASE | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| wrong-rev-caller-side | BASE, digest@BASE (valid receipt) | `0000…0` | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |
| wrong-rev-uppercase | `D6ED8155…` (uppercase hex) | BASE (lowercase) | 1 | 1 | `RECEIPT_PIN=FAIL header/body` |

Driver verdict line: `PROBE05_WRONG_REVISION exits_all_match=True tokens_ok=True` (exit 0).

## Findings

1. **Wrong-revision is rejected in every direction** (declared-side or caller-side, synthetic
   or real alternate commit, case-folded). The reference enforces the contract point
   "revision must equal caller-supplied `--revision`" as a header-equality check that fires
   before any blob/digest work — an internally self-consistent receipt pinned at another
   real commit (`f99de3bd…`) still fails. This matches the counter's frozen
   `wrong-revision` case (`v.replace(BASE,'0'*40)` ⇒ exit 1).
2. **Exit-code legend holds**: all mismatches are exit 1 (`invalid`), none escalate to 2
   (`usage/environment`), confirming 2 is reserved for argv/environment failures.
3. **Token granularity note for L1**: all four invalid arms collapse to the same
   `RECEIPT_PIN=FAIL header/body` reason string, because revision equality is checked inside
   the shared header-validation branch. The frozen C1 counter only requires the
   `RECEIPT_PIN=FAIL ` prefix for rc≠0, so this is within contract; but the reason string
   does not distinguish wrong-revision from other header/body defects. No claim violation —
   flagging as an observation only.
4. Positive arm confirms the fixture harness itself is sound (control passes 0/PASS with
   identical argv), so the four exit-1 results are attributable to the revision surface.

## Evidence (this folder)

- `probe05-wrong-revision-driver.py` — fixture builder + runner (as executed).
- `probe05-fixture-*.txt` — the five receipts (fixture surface, one file each).
- `probe05-results.json` — per-fixture argv, expected/actual exit, stdout/stderr, derivation.

## Tooling / installs

None. Only system `python3`, `git`, `sha256sum` already present. No installs, no pacman
transactions, no network. `TMPDIR` pinned to scratch.

## Risks / blockers

- Probe covers the revision-identity surface only; it is not an oracle for the other 19 C1
  cases and was not run as a battery (per seat spec).
- Reference behavior observed, not the production `tools/receipt-pin.py` (absent at probe
  time — consistent with "production tool may not exist yet"); production acquisition is
  L1's integration step.
- Scratch `/fast/scratch/hyaku/chousa-r65/Probe05/` deleted after receipts were copied here.
