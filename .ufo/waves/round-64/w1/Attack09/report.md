# Attack09 — C2 A01/A02/A03 independent falsification

## Scope and axes
Calibration; instrument provenance; stdout-consumer operability. Advisory only: no admission, canonical judgment, integration, or production edits.

Read host rules and frozen claims first. Compared the frozen revision `bf40d99bda9eefdad3ed6276da077cfb24ba82f1` with inherited working bytes. Claims, generator, runner, v1 checker, v2 checker, and inherited audit probe all match exactly. Full SHA-256 values and all subprocess commands/stdout/stderr/exits are in `evidence.json`.

## Minimal counterexamples
Executed ten bounded CLI probes, concurrently in six threads, against scratch checkers copied from **committed** bytes and mutated using the frozen generator definitions. Each A01/A02/A03 anchor occurs exactly once in each checker. No selftest or full runner was invoked, because those create git fixtures and this seat prohibits git mutations.

Both v1 and v2 produce the same observations:

| Input / mutant | Exit | stdout | stderr |
|---|---:|---|---|
| Honest checker, missing anchor | 2 | `AUDIT_STALE R anchor not in claims file`; `FLAGGED=0/1 AUDIT=PASS` | empty |
| A01, same missing anchor | 0 | same as honest | empty |
| A02, same missing anchor | 0 | `FLAGGED=0/1 AUDIT=PASS` only | empty |
| Honest checker, missing verbatim heading | 1 | `FLAG R verbatim-heading …`; `FLAGGED=1/1 AUDIT=FAIL` | empty |
| A03, same heading | 1 | `FLAGGED=1/1 AUDIT=FAIL` only | `FLAG R verbatim-heading …` |

Missing-anchor fixture: claims `unrelated text.` and one TSV rule `R\tverbatim-heading\tclaimed\ttarget.md\t\tseat minimal`. Missing-heading fixture changes claims to ``claimed `MISSING`.``; target contains `present`.

**Finding:** No counterexample to the specified A01–A03 mutation descriptions or their distinguishability was found. These are real semantic/output mutations, not accidental patch failures. The inherited probe P09 explicitly demands exit 2 plus `AUDIT_STALE` (`audit-probe.py:88–90`), so it distinguishes A01 and A02. P03 demands a stdout `FLAG R verbatim-heading` (`:72–74`), distinguishing A03 despite its unchanged exit and summary. The runner actually places the mutant at the probe's `__file__`-derived checker path (`c2-mutrun.py:103–112`). The recorded v1 receipt reports precisely R5 failures for all three. This seat did **not** rerun R5 or establish the entire 12-mutant closure condition.

## Narrow weaknesses, not claim failures
1. **Provenance enforcement:** runner `:86` reads `target.read_bytes()`, not committed blobs, despite the predicate's “committed bytes” wording. A dirty target could therefore be scored. Current-vs-freeze equality was independently observed here, so this is not an observed contamination or C2 failure. Smallest safe correction: pin and compare measured target/generator/runner digests in the external closure receipt; any future enforcement belongs in a distinctly named successor, not a rewritten frozen runner.
2. **Stale stdout is deceptively green:** even the honest checkers print `AUDIT=PASS` while exiting 2 on a stale row. A stdout-summary-only consumer would miss it; this is existing behavior, not A01/A02 survival, because P09 checks the exit. Smallest safe correction: require consumers to inspect exit 2 and `AUDIT_STALE`; do not silently change frozen expected output.

The broader user-supplied C1 frozen E12/E13 independently drawn-name mismatch remains an honest frozen failure. No C1 execution or repair occurred here. `c1-battery-supplement.py` is a separate post-freeze supplement and cannot substitute for frozen C1 success; `ref-preflight-v3.py` is not production.

## Execution and boundaries
Command: `python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack09/probe.py`; driver exit **0**. Individual checker exits are preserved above and in JSON. Python **3.14.8**, existing `/usr/bin/python3`; no installs/updates, network, git mutations, clones, or production/frozen-input edits. Scratch `/fast/scratch/hyaku/chousa-r64/Attack09/` removed in `finally`; evidence records `scratch_removed: true`. The retained `probe.py` is the reproducible evidence driver, not production code.

Self-evaluation: accuracy 4/5 (minimal probes, not full R5); completeness 4/5 (assigned three mutants covered; whole C2 deliberately not claimed); clarity 4/5 (full commands in JSON); actionability 4/5 (external provenance correction identified, not implemented); conciseness 4/5 (separate boundedness disclosures retained). Overall 4.0/5. Primary improvement for an authorized closure runner: execute the unchanged full matrix with git-fixture authorization. User agreement expected because no partial probe is presented as full closure.
