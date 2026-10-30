# SourceReject — S157 rejection-row candidate (round65, freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd)

## Verdict

CONFIRM the S157 rejection row. The strongest own-work docstring candidate in the freeze is the module docstring of `corpus/evidence/round65/controls/ref-receipt-pin.py`: it asserts behavior (exact header format, revision equality, blob-digest binding, exit contract) but the file contains no test, fixture, or execution record — 25 lines of validator implementation only. A docstring is author intent; it cannot prove that any command ran or that bytes and result were bound by an actual process.

## Recommended row (registry 11-cell schema)

| id | source | own-kind | tier | scope | location | reason+flip | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S157 | Receipt validator reference docstring — corpus/evidence/round65/controls/ref-receipt-pin.py | own-work | C | implementation intent as a candidate source of execution proof | module docstring first sentence, line 2, freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd | REJECTED: intent text cannot prove execution authenticity; flip: independent process evidence binding command, bytes and result | rejected | 2026-10-30 | on-release | — |

Located quote (7 words, ≤25), verbatim at freeze line 2:

> `Validate receipt header consistency, not execution authenticity.`

## Evidence (all observed this seat, read-only)

- Freeze blob: `git -C chousa-shokunin show f99de3b…:corpus/evidence/round65/controls/ref-receipt-pin.py` — line 1 shebang, line 2 opens the module docstring with the quoted first sentence; period-terminated sentence is exactly 7 words (`cut -d'.' -f1 | wc -w` → 7).
- Blob sha256 at freeze = `0719d7175da072454f514e0eea52b266f66c2246a085f4ea824793f634315fa2`, equal to `corpus/evidence/round65/source-openings.json` S157 `sha256`; working-tree file hashes identically and `git status --porcelain` on it is empty (no drift).
- The docstring asserts: format `REVISION/EXIT/SHA256+path`, "Revision must equal --revision and digest binds the named blob at that revision, not working bytes", exit codes `0 consistent; 1 inconsistent/malformed; 2 usage/environment`, "Read-only Git". None of this is demonstrated inside the file; behavior evidence lives only in separate executed artifacts (claims.md controls: before 0/20 exit1, positive 20/20 exit0, always-pass 3/20, always-fail 17/20, both exit1).
- Candidate survey of the freeze's other own-work files: `c1-count.py` has a docstring but it is the frozen measurement predicate itself, evidenced by the four named controls, and not a candidate *source* for an execution-proof claim; `c2-count.py` has no docstring; `always-pass.py`/`always-fail.py` are 2-line controls. `ref-receipt-pin.py` is the only own-work docstring offered as a knowledge source this round (source-openings S157).
- Precedent class matches: S137 (tools/build-spans.py docstring), S141 (candidate-openat2-probe.py docstring), S153 (ref-preflight-v3.py docstring) — all own-work, tier C, "REJECTED: …docstring states intent…; flip: …". S157 is the round65 instance.

## Consistency with drafted laneside rows

The working-tree drafts (SOURCES.md line 167; lessons/round-65.md Gate row; corpus/README.md line 1342 context) already carry this row. Independent re-derivation from the frozen bytes agrees on path, tier C, location ("module docstring first sentence"), quote, reason and flip. Flip wording is coherent with the lane frontier line (README.md:1343): an authenticated command/result binding and outside re-execution are what a local header-consistency validator does not supply.

## Confidence and limits

High confidence on quote location, word count, hash identity and the intent-not-proof reason (directly observed). Inference: tier C follows the S137/S141/S153 precedent, not a written tier rule I located. Not established here (out of seat scope): whether the validator's behavior holds — that is R65-C1's counter, run by L1. No git mutations, no writes outside `w1/SourceReject/`, no scratch residue.
