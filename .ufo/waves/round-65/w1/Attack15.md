# Attack15 — C1 frozen case traversal attack (round65)

Seat: Attack15 (leaf attack seat, lane chousa round65). Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd (lane HEAD, detached, verified). Base d6ed8155e9b4735639a2cf0a3e479c62f2056195. Scope: R65-C1 only. No production writes; all probes bounded and isolated in scratch (now deleted). Tools installed: none.

## Axes named

1. **Counter coverage vs. claim wording** — does the frozen 20-case traversal enforce everything the C1 claim sentence asserts?
2. **Forgery bypass near the frozen set** — can a malformed/forged receipt outside the 20 cases pass the reference validator?
3. **State dependence of detection** — is what the counter detects a property of the instrument or of the ambient repo state?

## Counterexample (constructed, outside the frozen 20)

Twelve receipts were crafted against BASE `d6ed8155…:SKILL.md` (blob sha256 `4355e16a…`, 172749 bytes; working-tree SKILL.md sha256 `2ccca333…`, 174299 bytes — lane tree is dirty at that path, +3 lines). Verdicts of the frozen reference validator `corpus/evidence/round65/controls/ref-receipt-pin.py`:

Accepted (rc=0), none of them in the frozen 20:
- `crlf.txt` — CRLF line endings (splitlines normalization)
- `notrail.txt` / `missing-trailing-nl-emptybody-marker.txt` — no trailing newline
- `leadblank.txt` — extra blank line at top of body
- `bodyrevision.txt` — a second `REVISION=<40hex>` line inside the body (parsed as body text)

Rejected (rc=1), also out-of-set: BOM prefix, `EXIT=00`, double-space digest separator, leading/trailing-space paths, working-tree digest (`wtdigest.txt`).

Plus the validator-class mutant `attack15-wt-pin-mutant.py` (reference with the `git cat-file` digest read replaced by a working-tree read; scratch copy only): it **passes** `wtdigest.txt` rc=0, i.e. a working-tree-hashing target is a live nearby bypass class.

## Does the frozen counter detect it?

- **Out-of-set malformed receipts: no, by construction.** `c1-count.py` presents only its frozen 20 receipts to the tool. CRLF/no-trailing-newline/blank-body/header-in-body deviations are never exercised; a target may accept or reject them and still score exactly 20/20.
- **Working-tree-hashing validator: yes, but incidentally.** Ran the frozen counter with `--tool` = the mutant: `CASES=17/20 C1=FAIL` (log: `attack15-mutant-counter.log`). The only three failures are `valid`, `nonzero-valid`, `max-exit` — precisely the rc=0 cases whose receipts pin the BASE-blob digest while the mutant hashes the dirty working tree. No frozen case pins a tree/blob mismatch; detection rests entirely on SKILL.md happening to be dirty vs BASE in this lane state. In a clean tree the same mutant scores 20/20 → C1=PASS while violating the claim's "Digest binds the Git blob … No working-tree hashing" sentence.
- Positive control: frozen counter vs. the reference validator itself → `CASES=20/20 C1=PASS`, rc=0 (so the traversal is satisfiable and the reference is consistent with its own frozen cases).

## Evidence

- `evidence-receipts/` — the 12 crafted receipts (unique seat names preserved).
- `attack15-wt-pin-mutant.py` — mutant validator (single-hunk diff vs reference; digest source only).
- `attack15-mutant-counter.log` — full counter run vs mutant.
- `attack15-hashes.env` — H_BASE (blob) vs H_WORK (working tree) sha256, the state difference that made detection incidental.
- Probe transcripts were run with `TMPDIR` inside scratch; counter `--work` dirs self-removed; scratch `/fast/scratch/hyaku/chousa-r65/Attack15` deleted on exit.

## Impacted axes

R65-C1 predicate fidelity only. C1=PASS continues to mean "matches the frozen 20-case interface sample", not "receipt parser is safe" and not "digest binding is enforced structurally". The claim text already narrows scope ("interface/consistency coverage, not … general parser safety"), which covers the out-of-set malformed receipts. The residual gap is narrower: the "No working-tree hashing" requirement is enforced by ambient dirty state, not by an instrumented case.

## Smallest safe correction

None to frozen bytes — counters, cases, and predicate are frozen and the mutant *is* caught in the current lane state. For L1 integration only: (a) when scoring the target, record alongside the C1 receipt that wt-hash detection rests on the lane tree being dirty at the cased path (`git hash-object SKILL.md` ≠ `git rev-parse BASE:SKILL.md`, confirmed this round), or weaken the claim sentence accordingly; (b) note that C1=PASS asserts nothing about receipts outside the frozen 20, including CRLF acceptance. No counter edit, no case addition, no scope expansion.

## Provenance honesty

Exit authenticity (a forged `EXIT=0` over failing output, or a blob digest binding content that was never the claimed tool's output) passes both validators by design — explicitly outside the claim ("not execution-authenticity claim"; round65 lesson S157 rejected as execution proof). Reported as a declared tradeoff bounding the meaning of C1=PASS, not as a defect.
