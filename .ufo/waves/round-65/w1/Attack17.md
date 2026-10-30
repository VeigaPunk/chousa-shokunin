# Attack17 — C1 frozen case `duplicate` attack (round65)

Seat: Attack17 (critic). Lane: chousa round65. Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` (lane HEAD re-verified at freeze after probes).
Scope: attack the frozen `duplicate` counter case — inspect the counter branch and the reference validator, construct nearby forged/malformed receipt bypasses *outside* the 20 frozen cases, and state whether the frozen counter detects them. Only bounded isolated probes against the frozen reference validator (`corpus/evidence/round65/controls/ref-receipt-pin.py`), the frozen counter run with `--tool` pointed at scratch, and read-only git. No frozen bytes altered, no production writes, no tests/batteries run.

## Verdict

**Two-layer result. (1) Receipt level: the frozen `duplicate` case's branch generalizes — every duplicate-header variant placed *before* the blank separator is rejected by the reference validator, so no in-header-block bypass exists near that case; but enforcement is purely positional (only `lines[0..3]` are checked), so every duplicate placed *after* the separator is accepted, including a full second forged header block. (2) Counter level: the 20 frozen cases are themselves duplicable — a lookup-table tool that memorizes the 20 receipts scores `CASES=20/20 C1=PASS` while accepting arbitrary forged receipts that merely claim the caller-supplied `--revision`. The frozen counter detects neither class: it hardcodes the 20 cases and never exercises any other input.**

## Evidence

Full transcript: `probe-results-attack17.txt`. Battery driver: `attack17-battery.py`. Memorizer: `attack17-memorizer-pin.py`.

### 1) Duplicate-adjacent battery — 15 candidates vs frozen reference validator

All bounded (timeout 20s), read-only `git -C … cat-file`, TMPDIR under my scratch. `UNEXPECTED=0`.

Rejected (`rc=1`, all `header/body` unless noted) — in-header-block duplicates and shape shifts:

| Candidate | Receipt shape | Result |
|---|---|---|
| control: frozen `duplicate` case itself | extra `EXIT=0` at separator slot | FAIL `header/body` rc=1 (matches frozen expectation) |
| `dup-revision-before-sep` | extra `REVISION=` at slot 3 | FAIL `header/body` |
| `dup-sha256-before-sep` | extra `SHA256=` at slot 3 | FAIL `header/body` |
| `dup-unknown-line-before-sep` | garbage line at slot 3 | FAIL `header/body` |
| `dup-two-exit-before-sep` | two extra `EXIT=0` lines at slots 3–4 | FAIL `header/body` |
| `sep-is-single-space` | separator = one space | FAIL `header/body` |
| `header-order-shuffled` | `REVISION/SHA256/EXIT` order | FAIL `header/body` |
| `exit-leading-zeros` | `EXIT=00` | FAIL `header/body` (regex `(?:0\|[1-9][0-9]{0,2})` rejects leading zeros) |
| `receipt-with-utf8-bom` | BOM before `REVISION=` | FAIL `header/body` |

Accepted (`rc=0 RECEIPT_PIN=PASS`) — duplicates after the separator (body is opaque):

| Candidate | Receipt shape | Result |
|---|---|---|
| `dup-exit-after-sep` | body line 1 = `EXIT=0` | PASS |
| `dup-revision-after-sep` | body line 1 = `REVISION=<base>` | PASS |
| `dup-sha256-after-sep` | body line 1 = `SHA256=<h> SKILL.md` | PASS |
| `dup-full-second-header-block` | valid header block + full forged second block in body (`REVISION=<base>`, `EXIT=1`, `SHA256=000…0 forged.md`) | PASS |
| `crlf-line-endings` | CRLF throughout | PASS (corroborates Attack11) |

The frozen `duplicate` case only exercises the extra-header-at-slot-3 shape. The validator rejects that whole in-block family (slot 3 must be blank; headers positionally ordered) but enforces nothing about header duplication beyond slot 3: anything after the first blank line is unvalidated output, so a second — forged — header block rides through.

### 2) Memorizer probe — the 20 frozen cases are duplicable

`attack17-memorizer-pin.py` (scratch tool, zero validation logic) reconstructs the 20 frozen receipts at runtime using the same construction as `c1-count.py` (`git cat-file <rev>:SKILL.md` → template → the 19 string mutations) and emits each case's canned exit/token. For any *other* receipt whose first line equals `REVISION=<--revision>` it returns `RECEIPT_PIN=PASS` exit 0 regardless of digest, path, or body — i.e., it admits forged receipts.

- `python3 -B corpus/evidence/round65/c1-count.py --tool <memorizer> --work <empty scratch>` → **all 20 cases PASS, `CASES=20/20 C1=PASS`, counter exit 0** (transcript lines 20–42).
- Differential on a forged receipt (`EXIT=0`, `SHA256=000…0 FORGED.md`, body `claimed output`; `evidence-forged-claim.txt`): memorizer → `RECEIPT_PIN=PASS` rc=0; reference validator → `RECEIPT_PIN=FAIL blob/digest` rc=1.

The frozen counter admits the memorizer — and with it a tool that validates nothing outside the frozen list — as a full C1 pass.

## Does the frozen counter detect them?

**No — by construction it cannot.** `c1-count.py` hardcodes exactly 20 cases; none of my 15 battery candidates (nor the forged claim) is among them, so the counter never feeds these inputs to any target. The predicate is defined solely over the frozen 20, so out-of-case behavior — post-separator forged header blocks, CRLF, and outright forged-receipt acceptance — is invisible to C1. Claims.md bounds the claim explicitly: "interface/consistency coverage, not a claim to cryptographic execution authentication or general parser safety." Under that bound this is a **tradeoff the canonical judge should accept at C1 level**, with the fixable defects below registered for a future round.

## Counter-branch observation (minor, code inspection)

`ok = returncode==rc and strip()==('RECEIPT_PIN=PASS' if rc==0 else strip()) and (rc==0 or startswith('RECEIPT_PIN=FAIL '))`. For `rc==0` the token check is exact-after-strip; for `rc!=0` it is an unstripped prefix test plus the tautology `strip()==strip()` — any bytes may follow the fail prefix. Returncode must still match, so this is not a forgery-admission vector, but the branch is asymmetric. Correction would be a counter change and is out of scope for this freeze.

## Fixable defect vs tradeoff

- **Tradeoff (canonical judge should accept):** opaque-body acceptance (post-separator duplicates, full forged header block in body, CRLF). Validator docstring says "exactly one of each header"; the code only enforces that positionally before the separator. Binding strength (digest ↔ blob at `--revision`) is unchanged; C1 predicate unaffected. Overlaps Attack11's appended-forged-body finding, independently reproduced from the `duplicate`-case angle.
- **Fixable defect — counter level (future round, NOT this freeze):** the predicate cannot distinguish a real validator from a 20-entry memorizer that also accepts forged receipts. Correction requires a held-out/generated case set (random digest/path/exit per run), which conflicts with this round's freeze rule; belongs in a new claim.
- **Fixable defect — validator level (future round, NOT this freeze):** if "exactly one of each header" is meant literally, reject body lines matching `^(REVISION\|EXIT\|SHA256)=` (one-line change) plus one new frozen case `forged-body-block` expecting rc=1. Do not touch frozen bytes.

## Constraints honored

- Bounded isolated probes only; read-only git (`git -C … cat-file`); TMPDIR and all evidence under `/fast/scratch/hyaku/chousa-r65/Attack17/`; no `/tmp` evidence.
- No installs used or needed (python3 + git only) — nothing to record.
- No network; no fleet/sibling/source-tree writes; only this folder + `w1/Attack17.md` written.
- Frozen validator, counter, controls, and claims bytes untouched; freeze `f99de3b…` intact (lane HEAD re-verified after probes; the `M`/`??` entries in `git status` predate this seat and are other seats'/L1's).
- Scratch deleted after evidence copied here.
