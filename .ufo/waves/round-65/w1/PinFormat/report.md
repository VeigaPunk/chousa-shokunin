# PinFormat — round65 w1 seat report (draft, not shipping authority)

Freeze: f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd (lane HEAD verified; `cat-file -t` = commit).
Frozen claims file blob sha256 at freeze: b9dbca57f4ca1af351459410e1fb7793668fe647c20278d26765b85485ab2fc5 (equals working-tree file).
Reference validator `corpus/evidence/round65/controls/ref-receipt-pin.py` sha256 0719d7175da072454f514e0eea52b266f66c2246a085f4ea824793f634315fa2 (equals S157 pin).

## 1. Specimen final receipt (exact frozen header)

File: `pinformat-positive.receipt` (copied here):

```
REVISION=f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd
EXIT=0
SHA256=b9dbca57f4ca1af351459410e1fb7793668fe647c20278d26765b85485ab2fc5 corpus/evidence/round65/claims.md

PinFormat measured output
child-exit 0
```

Produced by `pinformat-specimen-driver-r65-PinFormat.py` (copied from scratch). Digest is sha256 of `git -C <lane> cat-file blob f99de3bd…:corpus/evidence/round65/claims.md`, not working-tree bytes.

## 2. EXIT versus tool invocation exit

- `EXIT=` in a receipt is the **reported exit of the measured child** (the thing being receipted), captured by the driver from the child process object.
- The **tool invocation exit** is the exit status of the driver or validator process itself.
- They are independent channels. Evidence: `pinformat-exit7.receipt` has `EXIT=7` while the driver's own invocation exit is 0 (lane transcript, leg 3: `driver-invocation-exit will be 0 regardless of reported EXIT`, `invocation-rc=0`). The reference validator then returns `RECEIPT_PIN=PASS` / invocation-rc 0 on it (leg 4): a nonzero reported EXIT is consistent, and the validator's exit 0 says nothing about whether the measured command passed.
- The validator's own exits are 0 (consistent), 1 (inconsistent/malformed), 2 (usage; leg 7 uppercase `--revision` gave argparse usage, rc 2). Note that the validator's exit 1 means the receipt is inconsistent, not that the measured command failed.

## 3. Test of the reference against the specimen (lane transcript)

Transcript: `pinformat-lane-legs-transcript.txt`; script `pinformat-run-lane-legs-r65.sh`. Commands run from scratch with explicit `TMPDIR`.

| Leg | Input | Validator result | Invocation rc |
|---|---|---|---|
| 2 | own positive specimen, `--revision` = freeze | `RECEIPT_PIN=PASS` | 0 |
| 4 | specimen with `EXIT=7` | `RECEIPT_PIN=PASS` | 0 |
| 5 | first digest nibble flipped | `RECEIPT_PIN=FAIL blob/digest` | 1 |
| 6 | caller `--revision` = d6ed8155… (base), header = freeze | `RECEIPT_PIN=FAIL header/body` | 1 |
| 7 | uppercase `--revision` | argparse usage error | 2 |
| 8 | header intact, body replaced by fabricated line | `RECEIPT_PIN=PASS` | 0 |
| 9 | CRLF line endings on the positive specimen | `RECEIPT_PIN=PASS` | 0 |
| 10 | absent receipt path | `RECEIPT_PIN=FAIL [Errno 2] …` | 1 |

Conclusion on the reference: it behaves as its docstring states for header/digest/revision inconsistency (legs 5, 6, 7, 10). It accepts any body under a valid header (leg 8), which is the expected limit.

## 4. Limitations found (cite these; they bound what C1 can and cannot show)

1. **Forged body passes (leg 8).** Any body under a consistent header validates. This is the authenticity gap the C2 entry names; C1 does not and cannot close it.
2. **Working-tree divergence is invisible (fixture leg).** In a scratch fixture (`pinformat-run-fixture-leg-r65.sh`, toplevel asserted to equal the fixture dir before the git commit), the receipt was drafted against the committed blob at `138e7aa7…` and the working file was then tampered (`working-sha e1182a43…`). The validator returned `RECEIPT_PIN=PASS` (`pinformat-fixture-leg-transcript.txt`). This confirms "no working-tree hashing" as intended but shows that a receipt validates even when the file on disk differs.
3. **CRLF accepted (leg 9).** The frozen format names exact LF-style header lines (`lines[0]`, `lines[1]`, …). The reference reads text with `splitlines()`, which strips CR, so CRLF-terminated headers pass. This is a leniency relative to a byte-exact reading of the format; no frozen case covers CRLF, so the 20/20 counter does not detect it. Reported, not fixed (no new claims per freeze).
4. **Argument-level checks only in `--revision`.** Caller revision is checked for 40 lowercase hex; header revision is only checked for equality with the caller value. A caller that supplies the wrong revision gets a header/body failure rather than a distinct message (leg 6). Not a defect against the frozen predicate.
5. **Self-generated body.** My own specimen body ("child-exit 0") is written by the same driver that wrote the header; it demonstrates format, not independent observation.
6. **Single lane revision only.** I validated only against the freeze revision and a fixture; I did not run the frozen 20-case counter (that is L1's single verification).

## 5. Tools installed / updated

None. No `pacman`, `uv`, `npm`, or binary installs were needed (Python 3 and git were already present). No service restarts, no system upgrades, no pacman transactions.

## 6. Writes and scope

- Scratch: `/fast/scratch/hyaku/chousa-r65/PinFormat/` (clone-free; one fixture git repo inside `fixture/`). Deleted before yield (see below).
- Output: this folder only (`.ufo/waves/round-65/w1/PinFormat/`) plus `.ufo/waves/round-65/w1/PinFormat.md`.
- No git/jj mutations in the lane. The fixture `git commit` was inside scratch after a `rev-parse --show-toplevel` assertion. Read-only `git -C <lane> cat-file` and `rev-parse` only against the lane.
- No production writes, no network fetches, no task/subagent dispatch.

## 7. Evidence files in this folder

- `pinformat-positive.receipt`, `pinformat-exit7.receipt`, `pinformat-digest-tampered.receipt`, `pinformat-forged-body.receipt`, `pinformat-crlf.receipt`, `pinformat-wt-divergence.receipt`
- `pinformat-lane-legs-transcript.txt`, `pinformat-fixture-leg-transcript.txt`
- `pinformat-specimen-driver-r65-PinFormat.py`, `pinformat-run-lane-legs-r65.sh`, `pinformat-run-fixture-leg-r65.sh`

## 8. Findings for L1 (notes, not shipping authority)

- For C1 the frozen 20 cases do not include CRLF, forged body, or working-tree-divergence cases; those are gaps in interface coverage, consistent with C1's own stated scope ("interface/consistency coverage"). Treat leg 8 and the fixture leg as reasons the C2 limits paragraph is necessary, not as C1 failures.
- The draft receipt's `EXIT` line is the measured child's exit; the reference validator does not check that field against any execution evidence, so `EXIT=0` in the receipt is not evidence the command passed.
