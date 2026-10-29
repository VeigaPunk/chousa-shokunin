# Round 63 — SKILL.md rows (draft by ScribeSkillRows)

Placement: each row goes after the last row of its table (SKILL.md line 27 for the Decision table, line 53 for
Error patterns, line 153 for Gates). Draft only; the L1 integrates. Every cell traces to
`corpus/evidence/round63/controls/c2-positive-entry.md` (cited as Q1–Q9, Claims 1–5, Limits) or to the docstring of
`corpus/evidence/round63/controls/pos-ref-preflight.py`, except where marked UNTRACED.

## (a) Decision table — append after line 27

| Pin a citation to a revision of a git artifact (r63) | the full 40-hex object name, checked with `git rev-parse --verify "$VAR^{commit}"` (Q1, Q7; `corpus/knowledge/git-revision-identity-r63.md`, rows S142, S143, S144); a tag peeled to its commit with `^{commit}` (Q3); `<rev>:<path>` to pin a file's bytes, with the commit recorded beside it (Claim 3) | a tag's own id where the commit is meant (Claim 1, Q8); a leading substring or abbreviation as the pin (Claims 2, 4); a blob name as the commit it was read from (Claim 3); a short prefix without its candidate list (Claim 5, Q6 `--disambiguate`) | the full commit object name, verified, and the git version the reading rests on (Limits: the pages and probe are git 2.56.0; other versions may differ) |

## (b) Error patterns — append after line 53

| a citation holds a branch name or a short hash where a commit is meant (r63) | a leading substring names an object only while no other object in the repository shares its prefix, so it can stop resolving after later objects arrive (Claim 2; Q1, Q2, Q9); the default abbreviation length comes from configuration and differs between machines (Claim 4; Q5); a branch name is outside the object-name form quoted in Q1, and how a branch resolves is marked [INFERENCE] in the entry's Limits: re-resolve to the full 40-hex name with `git rev-parse --verify` before citing (Q7), and list every candidate with `--disambiguate` if a prefix must stay (Claim 5; Q6) |

## (c) Gates — append after line 153

| `tools/lane-preflight.py` (r63) | gate | `python3 tools/lane-preflight.py [--root DIR] [--fleet DIR] [--work DIR] [--skip G08[,G..]] [--only G01[,G..]]` | `0` every gate that ran passed · `1` at least one gate FAILED · `2` usage, or no gate failed but one could not run (ENV); a gate that could not run is never counted as a pass; summary `PREFLIGHT=<passed>/<run> FAILED=<ids\|none> ENV=<ids\|none> SKIPPED=<ids\|none>` | battery `python3 corpus/evidence/round63/c1-battery.py --tool tools/lane-preflight.py --fleet <fleet root> --work <dir>` must print `BATTERY=PASS` (UNTRACED: named in `corpus/evidence/round63/claims.md` C1, not in the two sources) | gate ids G01 census · G02 knowledge-index · G03 lesson-gate · G04 shonen-pointers · G05 scorecard-paths · G06 freeze-selftest · G07 assimilate-selftest · G08 gate-selftest; G01 runs `validate --file ROOT/corpus/SOURCES.md` from `--fleet DIR/scripts`, else `$SHOKUNIN_ROOT/scripts`, else `ROOT/../scripts` | no write outside `--work` (default: a fresh directory under `$HYAKU_SCRATCH`, else `$TMPDIR`, removed on exit); no network | chousa |

Untraced in this draft (counted in the seat report): (1) the battery command and its `BATTERY=PASS` expectation in the
Gates row; (2) the `tools/` directory prefix of the tool path, which the docstring writes as `lane-preflight.py`.
