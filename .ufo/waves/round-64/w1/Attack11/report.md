# Attack11 — C2 mutants A07–A09

Axes: calibration (claimed detection versus observed detection), provenance (frozen versus supplemental bytes), operability (bounded reproducible receipts). Advisory evidence only; no judgment or production integration.

## Finding 1: A07 does not implement the described later-modification defect

Frozen claims lines 121–122 and generator lines 53–55 describe adding `M` to `--diff-filter=A` as moving the first-add read to a later modification. But both checker versions select `c[-1]` from newest-first `git log` output (`claims-audit-v2.py:159–162`). In the runner's exact linear R7 history (add both files, then modify target), `A` returns `[add]` and `AM` returns `[modify, add]`: both select `add`. The target still fires. The frozen R7 leg therefore cannot distinguish this mutant.

Evidence: `probe.py` executes the actual frozen source with only its git subprocess response replaced by that explicit two-commit output. Both BASE and A07 return `(True, 'first added with the claims file in add: target.txt')`. This is a **synthetic log-response probe**, not a claimed real scratch-repository run. Real read-only histories of the frozen claims and checker also select the same add hash under A and AM (each currently has one matching commit; these do not independently exercise a modification). A07 against real R2/R3/R4 produces the expected summaries with exits 1/1/0.

Impact: calibration and provenance. [INFERENCE] A07 survives the frozen matrix on this history shape, contradicting the C2 12/12 target rather than exposing only a new supplemental class. This seat did not run the complete matrix and does not claim an observed total. All matrix/selftest git fixtures inspected select the oldest entry; their ordinary add/modify histories do not expose this mutation.

Smallest safe correction: retain frozen bytes and report the miss honestly if the canonical run confirms survival. A separately named future/supplemental mutant must actually select a later modification (for example select the newest AM entry) and have its own before/after receipt. Do not rewrite A07 or credit a replacement kill to frozen C2.

## Finding 2: A08 is killed by diagnostic specificity, not the advertised pass

Generator lines 56–60 replace the unreadable-revision guard with `if False`; they do not return a pass. With failed `git show`, stdout is empty. The subsequent nonempty-needle test still fires (`claims-audit-v2.py:145–152`). Direct execution of the real failing git read gives:

- BASE: `(True, "revision 0000000000 unreadable: fatal: path 'SRC.md' does not exist in '00000000000000000000")`.
- A08: `(True, 'S138 not under `## Leads` of SRC.md at 0000000000')`.

The frozen C6 selftest explicitly requires `unreadable` in stdout (lines 340–349), so losing that diagnostic makes R1 fail. That is a legitimate kill under the frozen output contract (claims lines 180–182), but is not evidence that this mutant silently passes unreadable revisions. Real R2/R3/R4 continue to hold for A08 (exits 1/1/0).

Impact: calibration/provenance of the mutation class, not an independently demonstrated numerical claim failure. Smallest safe correction: disclose that this frozen mutant tests missing unreadable-revision diagnostics; use a distinct future mutant that explicitly returns `(False, ...)` on git-show failure to demonstrate the advertised fail-open class. Preserve frozen names and counters.

## Finding 3: A09 is genuinely detected

Minimal fixture: claims `anchor \`Missing\``, target `Present`, one `verbatim-heading` row. BASE exits 1 with one FLAG and `FLAGGED=1/1 AUDIT=FAIL`; A09 exits 1 with the same FLAG and `FLAGGED=0/1 AUDIT=FAIL`. The real R2 and R3 receipts likewise become `FLAGGED=0/2` and `FLAGGED=0/4` instead of the frozen expected 2/2 and 4/4; both exit 1. R4 remains `FLAGGED=0/4 AUDIT=PASS`, exit 0.

Impact: no defect found in this scoped kill. No correction needed for A09.

## Commands, provenance and bounds

Executed from `/fast/scratch/hyaku/chousa-r64/Attack11`:

`python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack11/probe.py`

Exit 0. Full captured stdout: `probe-output.txt`; stderr empty. The driver records exact commands/exits/stdout/stderr for nine real receipt invocations. Synthetic and real evidence are separately labeled. Git operations were read-only `show`/`log`; no fixture git init/add/config/commit or clone was run. Full runner/selftests were not invoked because their fixture code performs git mutations, forbidden to this seat. Scratch was deleted after collecting evidence.

Read-only `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:PATH` returned exit 0 and byte equality for all four measured paths:

| Artifact | SHA-256 prefix |
|---|---|
| gen-audit-mutants.py | 6e1055b28d315e32 |
| c2-mutrun.py | 0045787ee9de3974 |
| tools/claims-audit.py | d48247f9c77ac1e7 |
| tools/claims-audit-v2.py | db0e28dd4c033259 |

The named `controls/c2-mutrun-v2.txt` was absent when read; its absence alone is not a false-pointer finding because claims lines 20–21 allow pending receipts. No inherited C2 supplement was substituted. C1's supplied known frozen E12/E13 independently drawn-name mismatch remains an honest frozen failure; `c1-battery-supplement.py` is distinct and cannot repair that frozen result. C1 was not rerun or modified here; the preflight candidate was not treated as production.

Tools: existing Python 3.14.8; existing git. No tool install/update, network access, service operation, production edit, or frozen-input edit.

## Self-evaluation

Accuracy 4/5: real receipt results and byte equality recorded; A07 full-matrix survival remains explicitly inferred. Completeness 4/5: all three mutants attacked; mutation ban prevents full git-writing runner execution. Clarity 4/5: synthetic versus real evidence labeled, but report spans several layers of contract. Actionability 4/5: preserve freeze and use a newly named actual later-read mutant; canonical closure still needs its authorized run. Conciseness 4/5: detailed provenance adds length. Mean 4.0/5. Highest-impact improvement: authorized canonical A07 matrix execution with raw R7 stdout. User should agree the boundary between observed evidence and inference is explicit.
