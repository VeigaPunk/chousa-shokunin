# R55DraftC1Rows — C1 registry and coverage draft

Scope: draft integration text only. No lane production files edited. Frozen C1 at `corpus/evidence/round55/claims.md:47` was treated as immutable.

## Source facts and exercised check

- `tools/build-spans.py:1-34` defines OLE/zip `.raw` through imported `tools/capture-text.py`; otherwise `.txt`; neither defined form means refusal. The `.txt` sidecar is not used for OLE/zip. It documents the exact CLI and exits.
- `tools/build-spans.py:157-183` implements `--check` by re-deriving and comparing manifest rows and span-file bytes against `DIR`; it writes nothing. This is a comparison against persisted expected values, so classify as **gate**, not probe. No separate self-test command exists; `--check` is an artifact comparison, not a fixture self-test.
- `corpus/evidence/round55/c1-measure-after.txt` reports command `python3 corpus/evidence/round55/c1-count.py --work /fast/scratch/hyaku/chousa-r55/R55ExecC1Runs/measurement` and four results: each has `GENOLE=3/3 OLEPIN=4/4 REFUSE=6/6 REGRESS=1/1 LEGS=4/4 C1=PASS` (three unseeded plus seed 7), exit 0. This is the recorded counter result, not a run performed by this seat.
- I exercised the tool separately in scratch (round-54 33-row quote input; not the C1 audit-hook/count test):

```text
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --quotes /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/quotes.tsv --out "$S/out" --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache
python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py --quotes /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round54/quotes.tsv --out "$S/out" --cache /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache --check
```

Observed: first command completed successfully and emitted 34 lines (33 `QUOTE` rows plus summary); second printed `SPANS_ROWS=33 STALE=0`. `$S` was a private directory under `/fast/scratch/hyaku/chousa-r55/R55DraftC1Rows` and removed by the shell trap.

## Draft SKILL.md row

The table schema is `SKILL.md:76-79`. Neighboring row excerpts matched:

- `SKILL.md:139`: “`capture-text` (OLE `.doc`, round 54; supersedes the round-52 row … by name)” — tool row records its text-form dispatch and refusal behavior.
- `SKILL.md:140`: “`chousa round-54 counters and checks` | gate” — bundled round counters/builders are registered as gates; its builder exit contract is explicit.

Proposed row (insert after the round-54 counters row):

```markdown
| `build-spans` (round 55; shared builder supersedes per-round variants) | gate | `python3 tools/build-spans.py --quotes Q.tsv --out DIR [--cache C] [--check]` | `0` built (`SPANS_ROWS=n WRITTEN=n`) or `--check` current (`SPANS_ROWS=n STALE=0`, no writes) · `1` refused row or stale/missing/extra manifest or span file · `2` usage/env | none (no dedicated self-test; `--check` compares against an existing output directory) | `--check` compares against `DIR/spans.tsv` and `DIR/spans/*.txt`; C1 regression reference is `corpus/evidence/round54/spans.tsv` and its span files; C1 expected offsets are generated in counter memory, not persisted | build: writes `DIR/spans.tsv` and `DIR/spans/` only (removes orphan `S###-N.txt` files there); `--check`: read-only; no network | chousa |
```

## Draft SCORECARD capability row

Neighboring row matched: `SCORECARD.md:2770-2773`, capability-table columns `Capability | What it can now do | Evidence pointer | First-working round`; its OLE text-form capability names behavior and points to measurement evidence.

```markdown
| OLE-aware shared span builder | Builds and checks quote spans using each capture's defined text form: OLE/zip `.raw` through `tools/capture-text.py`, never its `.txt` sidecar; otherwise `.txt`; refuses absent forms and quotes not occurring exactly once | `corpus/evidence/round55/c1-measure-after.txt` (four recorded C1 passes, including REGRESS); `python3 corpus/evidence/round55/c1-count.py`; `tools/build-spans.py` | 55 |
```

## Draft corpus/README.md coverage-map line

Neighboring coverage row matched: `corpus/README.md:1170` (`../tools/capture-text.py`), whose behavior is summarized with round-54 claim/counter/measurement pointers. Round-54 text at `corpus/README.md:1175` explicitly identifies the old per-round builder's UTF-16LE fallback.

```markdown
| `../tools/build-spans.py` | Round-55 capability: derives and checks spans from defined capture forms, dispatching OLE/zip `.raw` through `tools/capture-text.py`; non-OLE/non-zip captures use `.txt`. Supersedes the per-round `corpus/evidence/round5x/build-spans.py` variants whose non-zip `.raw` fallback decoded OLE as UTF-16LE; those historical files remain evidence, not the current builder | `corpus/evidence/round55/claims.md` C1; `corpus/evidence/round55/c1-count.py`; `corpus/evidence/round55/c1-measure-after.txt` |
```

## Limits / out of scope

- The standalone check above validates the round-54 quote set against newly built scratch output only; it does not establish the frozen C1 legs, audit-hook behavior, or independent C1 counter execution.
- No self-test is asserted. The report does not propose changes to frozen claims, target, counter, control, product files, or any other seat's report.
- No tool installation or external fetch was performed.

VERDICT: Drafted the C1 gate registry row, capability row, and coverage-map line; scratch build/check returned 33 rows with `STALE=0`, and the recorded C1 measurement reports 4/4 passing runs.