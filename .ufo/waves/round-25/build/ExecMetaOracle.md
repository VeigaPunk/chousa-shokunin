# Round 25 — independent metadata oracle

## Scope and retained evidence
- Implemented a standalone stdlib Python 3 oracle from the registered spec only: `corpus/evidence/round25-claims.md:20-49`. Did not read the new bash implementation.
- Clone base observed with `git -C /tmp/chousa-r25-ExecMetaOracle rev-parse HEAD`: `b820e4e40ce52deedf53b191140cd7b08ddda929`.
- Script: `/tmp/chousa-r25-ExecMetaOracle/corpus/evidence/round25-meta-oracle.py:1-200`; parsing/status policy at `:56-156`; CLI/path/exit handling at `:159-200`.
- Complete per-entry stdout, including each `META`/`FINDING` line, summary and captured exit code, is retained in `round25-meta-oracle.normal.out` and `round25-meta-oracle.strict.out` in the clone (56 lines each; SHA-256 below).

## Runs and prediction
- Normal command: `env -u CHOUSA_STRICT python3 /tmp/chousa-r25-ExecMetaOracle/corpus/evidence/round25-meta-oracle.py /tmp/chousa-r25-ExecMetaOracle/corpus/knowledge`; observed `METADATA_COMPLETE=25/28`, `RESEARCH_GATE: DRIFT`, `EXIT_CODE=1`.
- Normal named drift entries exactly matched registration: `archives-verified-r9.md`, `audit-r11.md`, `gate-baseline-r8.md`; each has only `META_RECHECK_ABSENT`. Other info findings do not drift normally. Prediction holds for normal mode.
- Strict command: `CHOUSA_STRICT=1 python3 /tmp/chousa-r25-ExecMetaOracle/corpus/evidence/round25-meta-oracle.py /tmp/chousa-r25-ExecMetaOracle/corpus/knowledge`; observed `METADATA_COMPLETE=25/28`, `RESEARCH_GATE: DRIFT`, `EXIT_CODE=1`.
- Strict mode marks 24/28 entries drift: the 3 absent-recheck warnings plus 21 unscheduled-info entries; four scheduled entries remain clean. Thus the named-only prediction does not hold under strict mode, as expected from the spec's strict promotion of info.
- Full output files are the exact per-entry oracle transcripts; only the required normal/strict invocations were run. No production-gate comparison or selftest was run.

## Spec ambiguities resolved
- Fence grammar is unspecified: recognize Markdown-style backtick/tilde fences, at most 3 leading spaces; close with the same marker, at least its opening length, and whitespace only. Heading match is literal column-zero `## ` outside a fence.
- Duplicate metadata keys are unspecified: first key wins. Source is absent if missing or blank; blank `verified-at` is undated; blank `recheck` is unscheduled, not absent. A present `recheck` key counts for completeness even if its value is blank.
- Values are outer-trimmed; continuation lines are joined with newlines. Whitespace-only lines terminate values. Key detection ignores fenced lines; continuation text may include them.
- Verified-at uses the requested `YYYY-MM-DD` prefix shape without calendar validation. A recheck date must be an exact, valid ISO calendar-date token; `<N>d` uses ASCII digits (including zero), and `on-release` is case-sensitive.
- `META_RECHECK_ROOT_PARENT` matches an unquoted whitespace-delimited `--root ..` pair anywhere in the recheck value; `--root=..` does not match. The CLI accepts `--root PATH`, but v1 specifies no effect for that option, so the oracle does not use it.
- Files are read as UTF-8 with LF line splitting and one trailing CR removed; directory candidates are direct, case-sensitive `.md` file children, sorted by filename bytes. The spec does not define encoding, bare-CR files, or symlink semantics.
- Output order is each entry's `META` followed by its findings, then completeness and `RESEARCH_GATE: CLEAN|DRIFT`; invalid input reports a diagnostic to stderr and exits 2 without partial output. Spec leaves exact order/diagnostic text unspecified.

## Files written in private clone (SHA-256)
- `corpus/evidence/round25-meta-oracle.py` — `97059aa6e7044b9b95aa0f0bcf174777efd75f3e77da0c2a53cfebda60ec5aa1`
- `corpus/evidence/round25-meta-oracle.normal.out` — `d5da873981d8546080f4fc264b949e6613c0bbe63e7e0c594715f07d0bff3f03`
- `corpus/evidence/round25-meta-oracle.strict.out` — `0826f33bb391656a48dc4977590ac697db25ecb9934a21665f5a1fb2534bccf2`

No installs. No blockers. The oracle makes explicit edge-case choices where spec v1 is silent; do not treat its untested error-path choices as production-gate observations.

VERDICT: Normal-mode prediction holds exactly; strict mode retains 25/28 completeness and promotes info findings, producing 24/28 drifting entries.
