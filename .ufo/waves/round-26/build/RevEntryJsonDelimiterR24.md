# Freshness review — `json-delimiter-r24.md`

- Scope: round 26 / attempt 1 only. Private clone `/tmp/chousa-r26-RevEntryJsonDelimiterR24-3`; observed base `f361d12e44687841e30ec35710ddb366c6f795e0`.
- Recheck (cwd = private clone root): `bash tools/research-gate.sh --selftest` → exit 0; `RESEARCH_GATE_SELFTEST: PASS (161 cases, 0 skipped)`. Cases 134–136 passed, including unreadable-manifest refusal; no `--root` is used/needed by this selftest command.
- Freshness: `verified-at: 2026-10-19`; `recheck: 90d`. [Inference] Scheduled due date is 2027-01-17; as-of 2026-10-21 is before it. The requested spot-check nevertheless re-ran the check.

## Source and claim checks

- Reopened S013 at https://jsonlines.org/ on 2026-10-21. §3 still contains verbatim: “Including a line terminator after the last JSON value in a file is strongly recommended but not required.” §2 still says “a blank line is not.” §3 still states CRLF is supported because surrounding whitespace is ignored. These match the entry’s cited anchors/quotes (entry lines 17–19, 42–44, 61–63).
- Registry at private base `corpus/SOURCES.md:11,23`: S001 and S013 remain tier A, mined, and used-by names this entry; S001 scope is the r24 gate behavior, S013 scope is JSON Lines requirements.
- S001 historical landing verified: `git show 6572827:tools/research-gate.sh | sha256sum` → `752e4e382ed77c06ac5030ce2179c7ca524934f86fd2a6b25ef946ab027ac553`, matching the entry’s `752e4e38…`. Historical gate anchors in `/tmp/chousa-r26-RevEntryJsonDelimiterR24-3-gate-r24.sh`: setup refusal 2375–2376; delimiter implementation 2490–2508; cases/oracle 5166–5196.
- Receipt checks match entry claims: `json-r24-20261019T213117Z-demo.log:14-16` before/after invalid-line counts; `:18-25` last-byte and write-only controls; `:26-40` concurrency and m1–m3 outcomes. `...-selftest.log:134-137` records cases 134–136 and PASS (136); `...-battery.log:1-2` says ALL IDENTICAL; `...-drift.log:1-2` says `GATE_DRIFT: none`, exit 0.
- `LOG.md:818-819` supports the round-24 opening’s delimiter defect and the prior truncated-baseline disposition; `corpus/lessons/round-24.md:77-82` supports the L2 write-only repro and the case-135 oracle history.

## Findings

- Low / QUALITY 7: `corpus/knowledge/json-delimiter-r24.md:20` (“an appender must not assume it”) is a sound operational inference from S013’s optional final terminator, but is not explicitly labelled as an inference. The concrete gate behavior is independently supported by S001; this is a scope/label clarity note, not stale source text or a false gate claim.

## Residual risk and verification gaps

- Historical pre-round object `b5d0f93d` was absent from the private clone (`git cat-file -t b5d0f93d` → `fatal: Not a valid object name`); the before-state remains evidenced by the demo receipt (`:13-14`), not a fresh checkout of that object.
- Entry lines 72–74’s GNU-grep/NUL explanation is present in the historical gate comment (`:5166-5167`) and lesson (`round-24.md:80-82`); my bounded probe on `{"prior":true}\0\n{"schema":1}\n` returned bare `grep -c '^$'` = 0 and `grep -a -c '^$'` = 0, so that specific behavior was not independently reproduced here. The assigned selftest did pass case 135.
- LSP is not mounted (`read xd://lsp` returned “No such tool”); literal search was used only to locate anchors, then source lines were read directly. No caller/definition/diagnostics claim is made.
- Installs: none.

VERDICT: re-verifies — cited source text and gate behavior remain current; no stale or false claim identified.