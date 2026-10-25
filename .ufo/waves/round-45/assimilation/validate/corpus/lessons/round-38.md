# Round 38 — env-pin capture (operability) and receipt binding (calibration)

author: chousa L1 (waves 1+2 seat reports integrated; per-seat authorship kept in
`.ufo/waves/round-38/w{1,2}/`)
date: 2026-10-24
round: 38 (attempt 1)

Claims: C1 (operability, lowest axis 3/10) — the canonical pin capture's child runs
through ONE pinned absolute `env`, so a caller-exported `env` function cannot
interpose (frozen `corpus/evidence/round38/claims.md`; measured
`ENV_PIN_CAPTURE_MATCH` 2/7 → 7/7). C2 (calibration) — round-38 receipts bind
pre==post gate hashes, counter/expect/receipt digests, verified by a census-tied
verifier (measured `RECEIPT_BINDING_MATCH` 0/7 → 7/7). Both landed with narrowings
frozen as claims.md §Errata 1–13; the waves falsified the first freezing of both
surfaces and the integration closed what they found.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| vacuous — the frozen verifier certified self-consistency, not provenance: a re-bound legacy r37 receipt, a c1 receipt rerouted as c2 with the counter hash swapped to a public digest, a doctored `pin_rc`, and a zero-scenario receipt all verified `ok` | w1/CritC2Kill.md findings 1–3; w1/CritTextOverreach.md | none — no criterion required a receipt's rows to be tied semantically to the frozen table; digest agreement was the whole standard (QUALITY 55 lands this criterion) | claims.md §Erratum 2: verifier binds counter family + predicate, parses the expectation table, requires the exact frozen census with each `expect` tied, re-derives every `ok`; the four fixtures refuse by name in wave 2 (w2/W2CritLaundering) |
| scope — three c2 cells asserted the SUBJECT counter's exit code, coupling C2's predicate to C1's gate fix (base gate 4/7) and falsifying "c2 is gate-agnostic" on the frozen bytes | w1/ExecDoNothingCtl.md (seed 38202); w1/RevSeparability.md; w1/RevClaimsC2.md | none at the freeze; QUALITY 54 (assertion must match the name) was in force and not applied | claims.md §Erratum 4: cells assert receipt existence + verification only; a C2-only tree at 7/7 on the unfixed gate is separability, not a do-nothing path |
| survivor — the harness left `BASH_ENV` live: one caller startup file (unsetting the attack function, forging the refusal token) moved the committed 2/7 r37 control to 7/7 | w1/RevCounterC1.md finding 1 (seed 38219) | none — `base_env()` scrubbed the attack variables, never the startup channel | claims.md §Erratum 5: scenario env scrubs `BASH_ENV`/`ENV`/`SHELLOPTS`/`BASHOPTS` (later `POSIXLY_CORRECT`, `PYTHON*` — w2/W2RevC1Final, w2/W2RevC2Final), `/usr/bin/bash` pinned with timeouts, refusal observable anchored |
| survivor — tamper doctors never re-sealed: all three tamper cells were caught at the receipt self-digest and the named binding checks were unexercised; a verifier mutant dropping them scored 7/7 | w1/MutVerify.md; w1/RevCounterC2.md finding 5 | QUALITY 52 was in force and not applied at the freeze | claims.md §Erratum 3: `doctor()` re-seals for the counter/expect tampers; each cell asserts its exact refusal label; wave-2 mutant re-run: the counter/expect-checks-deleted verifier is caught at 4/7 (w2/W2ScribeKnowledgeC2) |
| scope — the c2 self-rewrite fixture interpolated the caller's `--gate` path unquoted into shell source (a gate filename carrying shell syntax executed as the counter user) | w1/SentScope.md finding 1 | none | claims.md §Erratum 8a: every interpolated path shlex-quoted; w2/W2RevErrata re-probed: metachar gate filename executes nothing |
| scope — both counters hashed the expectation table only at receipt time; a mid-run edit let a receipt bind bytes the scenarios did not score | w1/SentScope.md finding 2 | none | claims.md §Erratum 8b: pre-run hash, refuse with no receipt on mid-run change; w2 verified |
| process — the frozen claims file was edited in place after the freeze commit (the pre-dispatch LD_PRELOAD limit) instead of landing as an appended erratum | w1/ScribeSources.md finding 7 | QUALITY 4 (errata append-only) — disclosed | kept as claims.md §Erratum 1 with its disclosure sentence; the body is otherwise untouched |

Related wave-2 process notes, recorded not mined: Errata 9–13 continued the same
pattern (a wave finding closed pre-commit, disclosed to in-flight seats); the
seat-reported freeze-drift alerts (w1/ScribeKnowledgeC2, w1/SimpCounters F9,
w1/MutCounterC2, w2/W2SentScopeFinal) were the same integration observed from
leaf seats — the L1 answered each with the disclosure pattern, and the round
report names the who/when.

## Gate

Rows added this round: **S072** (GNU Bash Reference Manual `bash.info`, Node
"Shell Functions" 3.3 — exported functions delivered to child shell processes;
quote 21 words contiguous at decompressed lines 1461–1463: "Functions may be
exported so that child shell processes (those created when executing a separate
shell invocation) automatically have them defined"; file SHA-256
`cde1a336…588f`; opened locally 2026-10-24, no network) and **S073**
(`sha256sum(1)` — `supersedes S070 —` the `-c, --check` entry is a DESCRIPTION
`.TP` item, not a SYNOPSIS line; decompressed lines 19–20 under `.SH DESCRIPTION`
at line 8; quote 8 words at line 20: "read checksums from the FILEs and check
them"; file SHA-256 `93c17dffe9…403f`; re-opened locally 2026-10-24). Both opened
this round; the round's Gate records path, access date, and located quote per
contract v1 rule 1.

- S072's teaches grounds C1's premise (exported functions reach children); the
  `BASH_FUNC_name%%` transport encoding is NOT in bash.info and stays a wave
  measurement (w1/ScribeSources finding 3). S073's teaches corrects S070's
  anchor label only; S070 stays `mined` (its used-by citations remain valid).
- Status/used-by changes: S072 and S073 enter as `mined` with used-by
  `corpus/knowledge/env-pin-capture-r38.md` and
  `corpus/knowledge/receipt-binding-r38.md` respectively (both entries land in
  the same commit; the census `validate` exit 0 at round end confirms the
  binding). No old row's status/recheck/used-by changed.
- Rejected candidates (recorded): a second `bash(1)` man-page row for the
  SHELLOPTS paragraph — S068 holds that file and w1/ScribeSources verified the
  distinct-scope argument holds for S072's info-file row instead; the
  elided 22-word S072 quote from the w1 draft — replaced with the contiguous
  21-word fragment (w2/W2ScoutFrontier checklist).
- Census before → after: 71 rows (A 65/B 1/C 5; mined 48/queued 19/rejected 4)
  → 73 rows (A 67/B 1/C 5; mined 50/queued 19/rejected 4); `sources-census.sh
  validate --root /home/vgpnk/Projects/shokunin chousa` exit 0 both ends;
  standing W04 ×2 for S051/S053 plus a new standing W04 naming S073's URL shared
  with S070 (same manual, expected class).
- Receipts (round close, measured): the nine receipts under
  `corpus/evidence/round38/receipts/` verify `ok` against their bound gates and
  the SCORING counter (`c1-count.py` / `c2-count.py` — `subject_counter` is not
  the verify counter; w2/W2ScribeLesson finding 3). The two c1 base receipts
  bind their control gates (`a7d3922c…`, `9fcac047…`) and refuse the landed
  gate (`gate-sha256-mismatch`); counts c1 7/7 ×3 + bases 2/7 ×2, c2 7/7 ×3 +
  base 0/7. `verifier_sha256` is unbound (carried debt, claims.md §Errata 2/11).
- Selftest on the final bytes: `RESEARCH_GATE_SELFTEST: PASS (272 cases,
  0 skipped)`.
- Knowledge admitted: `corpus/knowledge/env-pin-capture-r38.md` (C1, cites
  S072) and `corpus/knowledge/receipt-binding-r38.md` (C2, cites S073);
  sourced-claim requirement: C1 rests on S072 opened this round. Non-author
  spot-check: pending the hyaku closure's (as every round).

## Correction (2026-10-24, round 39 — routed defects D3/D6)

- (D6a) Gate records, URLs per contract v1 rule 1: S072's canonical URL is
  `http://www.gnu.org/software/bash/` (printed at decompressed line 30 of
  `bash.info`); S073's is
  `https://www.gnu.org/software/coreutils/manual/coreutils.html#cksum-c`
  (printed as the roff tty-link at the anchored line). Both rows in
  `corpus/SOURCES.md` already carry them; they are copied here so the lesson
  record is complete.
- (D6b) Rejected-candidate wording: the rejected second `bash(1)` row was
  recorded as "for the SHELLOPTS paragraph"; the wave evidence
  (`w1/ScribeSources.md`) rejected `bash.1.gz` for the same sentence S068
  already holds (the BASH_ENV material). The rejection stands; the candidate
  description is corrected: it was a same-file same-sentence duplicate, not a
  distinct-scope row.
- (D3) Erratum count: this lesson's header and process notes above say
  "§Errata 1–12"/"Errata 9–12"; the frozen claims file carries 13 errata. The
  count is corrected here and in LOG.md/SCORECARD.md (round-39 landing).
