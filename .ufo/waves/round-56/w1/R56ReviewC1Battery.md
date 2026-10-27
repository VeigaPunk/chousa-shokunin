# R56ReviewC1Battery — C1 battery review

Reviewed the frozen claims, candidate battery at `46e1758f3d8a5d1bf30200d2ff7d909b0230feed`, pristine `c1-gate.py`, its `c1-count.py` harness, and landed `tools/build-spans.py`. No production or claim changes proposed.

## Empirical runs

Ran each violator with the requested pristine gate invocation, seed 7, per-leg 2, and its own empty `--work` directory under `/fast/scratch/hyaku/chousa-r56/R56ReviewC1Battery`; each returned 1/C1=FAIL as intended. Leg output:

```text
m1-quote-only-span.py
GENOLE=FAIL S901 span is not a slice of the defined form
OLEPIN=FAIL S921 span is not a slice of the defined form
REFUSE=PASS 4 cases
REGRESS=FAIL spans.tsv differs from round 54's

m2-span-beside-quote.py
GENOLE=FAIL S901 char
OLEPIN=FAIL S921 char
REFUSE=PASS 4 cases
REGRESS=FAIL spans.tsv differs from round 54's

m3-wrong-digest.py
GENOLE=FAIL S901 capture_sha256
OLEPIN=FAIL S921 capture_sha256
REFUSE=PASS 4 cases
REGRESS=FAIL spans.tsv differs from round 54's

m4-no-quote-lines.py
GENOLE=FAIL S901 QUOTE line
OLEPIN=FAIL S921 QUOTE line
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical

m5-extra-span-file.py
GENOLE=FAIL extra or missing span files
OLEPIN=FAIL extra or missing span files
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical

m6-manifest-on-refusal.py
GENOLE=PASS 2 docs, 4 quotes
OLEPIN=PASS 4 captures, 8 quotes
REFUSE=FAIL NOFORM: spans.tsv written
REGRESS=PASS r54 33 rows identical

m7-read-outside.py
GENOLE=FAIL rc=97 b"AUDIT_FORBIDDEN open '/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md'\\n"
OLEPIN=FAIL rc=97 b"AUDIT_FORBIDDEN open '/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md'\\n"
REFUSE=FAIL NOFORM: rc=97
REGRESS=FAIL rc=97 b"AUDIT_FORBIDDEN open '/home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md'\\n"
```

Oracle check: the driver edits H1/H2 into its gate copy and passes `R56_ORACLE` only for `oracle-*` entries (`c1-count.py`, `HARNESS`, `Runner.run`, entry construction). I applied those same harness edits to scratch gate copies. Oracle under that harness: `ENV_CHANGED tools/capture-text.py is not the pinned oracle` (exit 2). Same invocation with M8's digest clause removed: `GENOLE=PASS 2 docs, 4 quotes; OLEPIN=PASS 4 captures, 8 quotes; REFUSE=PASS 4 cases; REGRESS=PASS r54 33 rows identical; LEGS=4/4; C1=PASS; EXIT=0`.

Commands/evidence: each violator was invoked as `python3 <lane>/corpus/evidence/round56/c1-gate.py --tool <lane>/corpus/evidence/round56/battery/<file> --seed 7 --per-leg 2 --work <empty scratch dir>`. Full outputs were captured per run under the scratch path above; the leg lines are reproduced here. Oracle and M8-complement runs used scratch copies with the driver's H1/H2 harness edits and `R56_ORACLE=<lane>/corpus/evidence/round56/battery/oracle-m8-unpinned.py`.

## Review findings

- **Docstring overclaims one-behaviour isolation in m1–m3.** All three change the successful builder output in every run, including REGRESS: m1/m2 alter the first row and span file, m3 alters the digest cell. The observed `REGRESS=FAIL spans.tsv differs from round 54's` is an additional gate failure beyond the advertised slice/char/digest violation. Their intended M1/M2/M3 kill still comes from the corresponding GENOLE/OLEPIN reason; the counter's marker-based kill is not redirected. Consider the battery descriptions' “breaks exactly one behaviour” assertion false for these three entries. This is a calibration/coverage defect, not a reason to alter the frozen predicate.
- **m2 fallback:** `sys.exit("battery m2: …")` does exit nonzero (Python exits 1) if the longer beside-quote context is no longer than the quote or still contains it. It did not trigger in the empirical inputs: GENOLE/OLEPIN show the intended `S901 char`/`S921 char` reason. Builder `CONTEXT=80` and gate quote windows of 10–24 characters make that fallback unreachable for these long generated/pinned forms, but the code path itself is nonzero, not a successful fallback.

Other per-file checks: m1 advances offset by the quote's within-span index before replacing the span with the quote, so the offset points at the quote; m2 uses a matching absolute start offset for its adjacent slice; m3 changes only the digest cell; m4 filters stdout `QUOTE ` lines while leaving stderr/other stdout alone; m5 writes an orphan after the builder's cleanup; m6 writes a header-only manifest only after builder rc=1 on refusal; m7 opens the out-of-allowlist `SKILL.md` before builder execution. Each intended clause is the first relevant failing clause in its shown successful-build/refusal leg; m7's refusal wrapper reports `rc=97`, while its GENOLE/OLEPIN/REGRESS legs carry the hook marker. The oracle copy differs from `tools/capture-text.py` only by a trailing blank and its two-line M8 comment; SHA-256s observed: pinned `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`, copy `e86a52a62fffdb5fbc2b451bd31e5535642234f7f0647c5692ce2e0dba6d7e0a`.

Gate-vs-round-55-counter diff showed the hook additions `_posixsubprocess.fork_exec` and `os.chdir`, the docstring, and temp-prefix rename; the counter clauses/legs otherwise match. No `soffice.bin` process remained after the runs.

Residual risk / verification gaps: only the requested direct gate runs at seed 7 were performed, not the frozen two-seed random-triplicate driver; no claim about full C1 counter status. No source fetch or unrelated verification run.

VERDICT: R56 C1 battery entries m4–m7 and oracle M8 exhibit their intended isolated check failures; m1–m3 kill their intended clauses but additionally fail REGRESS, so their “exactly one behaviour” description does not survive review.
