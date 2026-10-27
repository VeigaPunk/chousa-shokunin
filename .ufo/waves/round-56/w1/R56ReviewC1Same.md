# R56ReviewC1Same — same-sentence audit of R56-C1

## Findings

**No actionable predicate/implementation mismatch found in scope.** The frozen predicate in `claims.md:55-75` and the `c1-count.py` docstring (`:4-25`) are identical after removing the docstring-only lead-in (normalized 238 words each). Clauses (i)–(iii) map to candidate-vector comparison (`c1-count.py:195`), the M1–M9 kill logic (`:209-263`), and the two-seed probe check (`:264-282`).

- Candidate requires both seeds to have `(exit 0, PASS×4)` (`c1-count.py:195`; `LEG_RE`/vector construction at `:102-139`).
- For M1–M8, the base G run must contain a marker at both seeds (`:247-248`), and the same leg must fail with that marker in the base and three additional G runs, then pass in three mutant runs (`:209-232`, `:249-256`). M8 checks G stdout for `ENV_CHANGED` and mutant stdout absence (`:203-225`). M9 uses the first G vector, three G runs and three mutant runs, and allows success at either seed (`:217-220`, `:238-245`).
- `MARKER` regexes (`c1-count.py:86-96`) match the gate’s returned reasons: M1 `judge` slice reason (`c1-gate.py:279-280`); M2 `S<n> char` (`:281-282`); M3 `S<n> capture_sha256` (`:269-270`); M4 `S<n> QUOTE line` (`:283-284`); M5 `extra or missing span files` (`:285-287`); M6 `spans.tsv written` (`:327-338`). M7’s regex matches the audit hook’s `AUDIT_FORBIDDEN open|os.listdir|os.scandir <path>` stderr (`c1-gate.py:95-114`), surfaced in `judge`’s nonzero-return reason (`:250-251`). M8 matches `env_fail`’s exact stdout line, `ENV_CHANGED tools/capture-text.py is not the pinned oracle` (`:123-125`, `:450-451`). M9 intentionally has no marker (`c1-count.py:85-98`); its extra edit removes the second control-character guard as well as the primary newline guard (`c1-gate.py:157-169`).
- Parsed counter edit anchors M1–M9 (including M9’s EXTRA anchor), H1 and H2 each occur exactly once in both `round55/c1-count.py` and `round56/c1-gate.py`. H1/H2 substitutions are the declared lane pin and `R56_ORACLE` override (`c1-count.py:65-68`); the same edited source is used for G and mutants (`:145-178`).
- Probe files implement their named actions: P1 uses `_posixsubprocess.fork_exec` then the lane builder (`probes/p1-forkexec.py:1-20`); P2 changes directory, opens lane `tools/` as dirfd, reads `../SKILL.md`, then invokes the builder (`probes/p2-dirfd.py:1-24`). `parents[4]` resolves to the lane root for these probe paths. The counter’s DENIED test requires exit 1, all four FAIL legs, and a per-leg `AUDIT_FORBIDDEN` or `rc=97` substring at both seeds (`c1-count.py:264-278`). `refused_ok` returns only `rc=97` for non-1 exits (`c1-gate.py:327-334`), so accepting either marker is necessary and consistent.
- Run directories use `secrets.token_hex(8)` (`c1-count.py:117-126`); the six G/mutant runs are shuffled (`:197-213`). The three pre-freeze fixes disclosed in `claims.md:21-30` are present: M9 drops both guards (`c1-count.py:98`, gate `:168-169`); DENIED accepts `AUDIT_FORBIDDEN` or `rc=97` (`c1-count.py:273-275`); and marked-leg, randomized 3+3 checks are enforced at both seeds (`:209-256`). The JUNK builder contains the alternating FLIP forge (`controls/build-c1-junk.py:1-40`).

## Receipt provenance and reproduction

`git show 41c58925580af6be22049f13cfde234c5475b858:<path>` bytes for the claims, counter, gate, probes, controls receipts/builders, round-55 counter, and builder matched the lane working-tree bytes. Receipt-bound hashes also matched: gate `e3cb3ec5…4971`, round-55 counter `5506f240…8906`, builder `1ed2650a…80bf6`. Thus the executed counter/gate bytes were the frozen bytes; the candidate battery is intentionally later (candidate commit `46e1758`).

Replayed the frozen counter with explicit empty `--work` directories under `/fast/scratch/hyaku/chousa-r56/R56ReviewC1Same`; rebuilt round-55 controls and JUNK there. Commands were the receipt commands with `$LANE` expanded to `/home/vgpnk/Projects/shokunin/chousa-shokunin`, `$S` to the scratch path, and `--work $S/w-{before,hook,junk,empty}` added. Observed summaries:

```
before:  CANDIDATE=2/2 KILLED=1/9 DENIED=0/2; RUNS=22; C1=FAIL; exit 1
HOOKONLY: CANDIDATE=2/2 KILLED=1/9 DENIED=2/2; RUNS=24; C1=FAIL; exit 1
JUNK:     CANDIDATE=2/2 KILLED=1/9 DENIED=2/2; RUNS=36; C1=FAIL; exit 1
EMPTY:    CANDIDATE=2/2 KILLED=1/9 DENIED=2/2; RUNS=12; C1=FAIL; exit 1
```

These counts and verdicts match `controls/c1-before.txt` and `controls/c1-controls.txt`; the M9 random order strings vary, as expected. The before receipt’s probe runs stop after seed 7 fails DENIED; this is consistent with the counter’s early break (`c1-count.py:269-276`). The three pre-freeze fixes therefore are evidenced in the frozen bytes and the receipts reproduce.

## Residual risk and verification gaps

- LSP device/status was unavailable in the provided tool inventory; this review used direct file reads and literal anchor counting, not semantic LSP references/definition/diagnostics.
- I did not rerun the full candidate battery; this seat’s audit targeted predicate fidelity and frozen receipt provenance. No build/test/lint was run.

VERDICT: R56-C1 same-sentence audit survived; the predicate, counter mechanics, probes, and frozen control receipts are consistent, with no actionable in-scope finding.
