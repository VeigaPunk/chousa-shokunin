# Attack10 — C2 mutants A04/A05/A06

Recommendation: no actionable C2 defect found in this assigned slice. Advisory only; this is not claim admission, integration, or reproduction of the complete 12-mutant closure predicate.

Axes: frozen-byte fidelity; mutation discrimination; zero production mutation.

## Findings, by severity

None against C2 A04–A06. Each frozen mutation applies exactly once to both frozen checker versions and produces the intended independently distinguishable error.

| Mutation | Minimal counterexample | Baseline, both versions | Mutant, both versions | Frozen matrix connection |
|---|---|---|---|---|
| A04 | JSON holds two items; claim says `count says 1 seats.` | exit 1, `FLAGGED=1/1 AUDIT=FAIL` | exit 0, `FLAGGED=0/1 AUDIT=PASS` | Observed R2 and R3 also change from exits 1 to 0, killing A04 directly in either matrix. |
| A05 | File has `## Planned`; claim quotes `planned` | exit 1, `FLAGGED=1/1 AUDIT=FAIL` | exit 0, `FLAGGED=0/1 AUDIT=PASS` | v2 selftest C5 uses the same case-only distinction (`tools/claims-audit-v2.py:329–338`). |
| A06 | JSON holds two items; claim says `count says v2 seats.` | exit 1, `FLAGGED=1/1 AUDIT=FAIL` | exit 0, `FLAGGED=0/1 AUDIT=PASS` | v2 selftest C9 uses true count 2 with only word-internal `v2` (`tools/claims-audit-v2.py:374–383`). |

A04 still emits its per-rule `FLAG` line: the mutation suppresses the accumulated count and failure exit, not the diagnostic print. That behavior is captured in evidence, not mistaken for a clean result. The frozen generator's actual edit is `fired += 1` → `fired += 0` (`gen-audit-mutants.py:42–46`); `run_audit` prints FLAG independently (`tools/claims-audit-v2.py:194–209`).

A05 edits only the literal span comparison (`gen-audit-mutants.py:47–49`; checker `:176–182`). A06 removes both numeric-token boundaries (`gen-audit-mutants.py:50–52`; checker `:121–127`). Their R2/R3/R4 outputs remain unchanged on both versions, consistent with those receipt legs alone not distinguishing these two classes. No complete v1 survivor claim is inferred from those three legs.

The frozen runner checks R1's selftest exit and summary (`c2-mutrun.py:148–150`). The v2 selftest immediately exits 1 when C5/C9's expectations fail. Thus the source connects the independently demonstrated errors to the frozen v2 R1 kill mechanism; the full selftest itself was not executed here.

## Frozen/current byte fidelity

Read-only `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:<path>` succeeded (exit 0) for all five inputs. Full bytes equal current inherited bytes, not merely matching prefixes:

| File | SHA-256 prefix |
|---|---|
| `corpus/evidence/round64/claims.md` | `bab186919f4518f3` |
| `corpus/evidence/round64/gen-audit-mutants.py` | `6e1055b28d315e32` |
| `corpus/evidence/round64/c2-mutrun.py` | `0045787ee9de3974` |
| `tools/claims-audit.py` | `d48247f9c77ac1e7` |
| `tools/claims-audit-v2.py` | `db0e28dd4c033259` |

Full digests and comparison results are in `evidence.json`. An initial read-only scoped `git diff` against that freeze also exited 0 with empty output. No production diff exists for these inputs at observation time.

## Executed probes and evidence

Command (exit 0):

```text
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack10/probe.py
```

The driver generated only A04/A05/A06 using the unchanged frozen generator. It ran 48 bounded checker subprocesses: two checker versions × (baseline plus three mutants) × (three minimal fixtures plus frozen receipt legs R2/R3/R4). Six concurrent workers; each subprocess timeout 30 seconds. No timeout occurred. Every command, cwd, stdout, stderr, and exit is retained in `evidence.json`; fixture contents and exact construction are in `probe.py`.

Observed receipt summaries on both versions:

- Baseline, A05, A06: R2 exit 1 `FLAGGED=2/2 AUDIT=FAIL`; R3 exit 1 `FLAGGED=4/4 AUDIT=FAIL`; R4 exit 0 `FLAGGED=0/4 AUDIT=PASS`.
- A04: R2 exit 0 `FLAGGED=0/2 AUDIT=PASS`; R3/R4 exit 0 `FLAGGED=0/4 AUDIT=PASS`.

## Residual risk and verification gaps

- Full `c2-mutrun.py`, R1/R5/R6/R7, and the checker selftests were not run: their fixture code performs git initialization/config/add/commit, contrary to this seat's no-git-mutations constraint. No claim of `AUDIT_MUTANTS_KILLED=12/12`, whole-matrix v1 survivors, or non-author closure is made.
- LSP unavailable: `read xd://lsp` returned `No such tool`. Therefore references/definition/diagnostics requests could not be made. Source inspection is textual evidence, complemented by the recorded bounded runtime probes, not represented as language-server proof.
- C1 is independently failed under its frozen rule because of the supplied known E12/E13 independently drawn fixture-name mismatch. This seat did not rerun, repair, or hide it. `c1-battery-supplement.py` is a distinct post-freeze supplement and cannot establish the frozen C1 pass. This is not a finding against the scoped C2 mutations.
- No supplement or `ref-preflight-v3.py` was treated as production. Only the exact frozen/current C2 instruments above were measured. No claim about unrelated runtime routing, resume preflights, or saturation is established by this slice.

## Hygiene and tools

Only seat report/evidence paths and `/fast/scratch/hyaku/chousa-r64/Attack10/` were written. No clone, git/jj mutation, network request, production edit, frozen-rule change, service restart, package installation, PATH modification, or sibling edit. Scratch was removed in the driver's `finally` block; recorded `scratch_removed=true`.

Existing Python 3.14.8 and existing Git were used; no tool installed or updated (channel/reason: not applicable).

## Self-evaluation

Accuracy 4/5: exact command/output and frozen byte checks; full-matrix inference is explicitly withheld. Completeness 4/5: all three assigned mutants probed on both versions; git-writing matrix legs intentionally not executed. Clarity 4/5: table separates observed errors from source-supported kill mechanism. Actionability 4/5: driver and raw evidence are reproducible; closure still belongs to L1. Conciseness 4/5: provenance and mutation restrictions add necessary detail. Overall 4.0/5. Highest-impact remaining verification is an authorized whole frozen matrix run, not a rule repair. The evidence and limitations should support the same assessment by the user.
