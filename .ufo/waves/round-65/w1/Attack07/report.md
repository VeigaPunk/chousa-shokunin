# Attack07 — C1 frozen-case no-exit attack (round 65)

Seat: Attack07 (UFO-FSD critic, leaf). Lane root: `chousa-shokunin`. Freeze: `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Method: bounded isolated probes only, all under scratch `/fast/scratch/hyaku/chousa-r65/Attack07/` (deleted on exit). Frozen bytes untouched; git used read-only with explicit `-C`. No tool installs were needed (python3 stdlib only).

## Target inspected

- Frozen counter `corpus/evidence/round65/c1-count.py` (blob `f43bf9f5…` at freeze). Fixed 20-case battery; grades a target `tools/receipt-pin.py` (currently absent — confirmed `CASES=0/20 C1=FAIL missing-target`, exit 1, zero cases executed; matches claimed before-control).
- Reference validator `corpus/evidence/round65/controls/ref-receipt-pin.py` (blob `9cf660f0…`). Read-only git oracle. Claimed contract: exit 0 consistent / 1 invalid / 2 usage/environment.

## Counter branch inspection (no-exit case)

- `no-exit` (case 7 of 20) removes the `EXIT=0\n` header line; expected rc 1.
- The `ok` expression contains a tautology: `q.stdout.strip()==('RECEIPT_PIN=PASS' if rc==0 else q.stdout.strip())` — for the 17 fail cases the comparison is `stdout==stdout`, always true. Not exploitable (returncode and the separate `startswith('RECEIPT_PIN=FAIL ')` check still gate), but the fail-branch token check is weaker than it appears.
- No frozen case exercises exit 2; the "usage/environment" tier is ungraded by the frozen battery.
- The battery is a fixed literal list; anything not in the 20 is invisible to the counter by construction.

## Attack: nearby forged/malformed receipts outside the no-exit case

Reconstructed the canonical valid receipt `v` exactly as the counter builds it (REVISION=BASE, EXIT=0, SHA256 of `git cat-file blob d6ed8155…:SKILL.md`, blank separator, body). Built 20 nearby variants (no-exit neighborhood: separator/line-discipline tampering, EXIT-value forgeries, conflicting duplicate EXIT, NUL injection, encoding tricks) plus 3 environment probes. Evidence: `attack07-probe-results.json`, `attack07-falsepass-*.txt`.

### Result — reference validator false-PASSes 6 malformed receipts

| Variant | Reference result |
|---|---|
| VT (`\x0b`) separators between all header lines | **PASS rc=0** |
| FF (`\x0c`) separators | **PASS rc=0** |
| Lone CR (`\r`) separators | **PASS rc=0** |
| NEL (U+0085) separators | **PASS rc=0** |
| NUL byte inside body | **PASS rc=0** |
| CRLF everywhere | **PASS rc=0** |
| EXIT= / EXIT= 0 / EXIT=00 / EXIT=0x0 / EXIT=+0 / exit=0 / conflicting duplicate EXIT / trailing tab / NUL after value | FAIL rc=1 (all detected) |
| separator-is-space, body-before-headers, unknown header, BOM, tab before path, UTF-16LE | FAIL rc=1 (all detected) |
| env: unreadable receipt, missing receipt, git off PATH | FAIL rc=1 — **never exit 2** |

Root cause: `text.splitlines()` splits on VT/FF/CR/NEL/LS/PS, so a receipt that is *not* LF-line-structured at all still parses into the expected 5 "lines"; and body content is only checked for `strip()` non-emptiness, so NUL bytes pass. The documented exit-2 tier is unreachable in practice: every OSError (receipt unreadable/missing, git missing) is caught and mapped to exit 1.

Programmatic check: zero text overlap between the 20 variant receipts and the 20 frozen case texts — the bypass family is strictly outside the battery.

## Does the frozen counter detect it?

**No.** The frozen counter executes only its 20 fixed cases; my forged receipts are outside that set, so the counter never runs them and cannot flag them (evidence: overlap check above). Furthermore, a target cloned from the reference semantics would falsely PASS these same malformed receipts **while still scoring CASES=20/20**, so the frozen battery cannot distinguish a strict target from a lenient one outside its 20 cases.

## Impacted axes

- **C1 (operability, scored predicate):** the 20-case grade is still executable, so this does not by itself block a 20/20 target. But the receipts are the round's operability artifact, and the accepted-malformed family sits at the claim's own boundary: claims.md disclaims "general parser safety" yet scopes "interface/consistency coverage" — a receipt whose physical line discipline is forged is arguably a header-consistency violation, not merely parser hardening. L1 must classify.
- **Exit-2 tier:** documented but dead in the reference and ungraded by the counter; any target that never returns 2 still passes.
- **C2 / freeze-kill rule:** untouched; counters/predicate frozen, so no retrofit possible this round.

## Smallest safe correction (advisory — no frozen bytes changed)

1. Reference/target: parse with `text.split('\n')` only (or explicitly normalize CRLF→LF then split on LF), rejecting any `\r`, VT, FF, NEL, LS, PS in header lines; reject NUL/C0 controls in headers and body. This closes the false-PASS family at its root.
2. Map environment failures (receipt unreadable/missing, git unavailable) to exit 2 per the documented contract, and add a frozen-style case for it in a future round's counter.
3. Counter note for future rounds: the fail-branch token check tautology (`stdout==stdout`) should be a real comparison; harmless today because returncode still gates.

## Verdict for L1

The splitlines/NUL leniency is a **fixable defect** in the reference validator, not a fundamental tradeoff; but under the round-65 freeze it cannot affect the frozen 20-case predicate, and the claim's parser-safety disclaimer partially covers it. Recommend: let C1 grading proceed against the frozen counter, adopt corrections 1–2 for the delivered target, and record this attack as supporting evidence for the next round's counter expansion.

## Tooling record

No installs or updates performed; probes used system python3 stdlib only.
