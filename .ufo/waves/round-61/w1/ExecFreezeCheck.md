# ExecFreezeCheck — freeze-check.py (round 61 w1)

Candidate: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-61/w1/ExecFreezeCheck/freeze-check.py`
(sha256 `d43c6845ebcd2081b15e47bc2f3c46b6964b7bca098639a9cabf79e533e91cfa`, 502 lines). No labrat spawned, no install, no
git/jj call, nothing written outside my directory, report and scratch (scratch removed).

## Findings

1. **The check exists and separates the two historic failures.** `freeze-check.py --claims C --dispatch D --spec S --ready R`
   runs 8 checks and exits 0 only if all pass (1 on any fail, 2 on usage error). Output is `CHECK <ID> PASS|FAIL <detail>`
   per check, then `FAILED_CHECKS=` and `FREEZE_CHECK=PASS|FAIL`.
   CLAIMS_NONEMPTY, CONTEXT_DIGEST (whole 64-hex token in `taskCall.context`; prefix or 65-hex run does not count),
   DIGEST_STRAY (any other 64-hex token in spec bodies, task bodies or either context), CONTEXT_SPEC_EQ, NAMES,
   BODY_RENDER, READY_DISPATCH (names an existing file that is the `--dispatch` file), READY_IDENT (lane/round/wave vs
   `dispatch.wave == <lane>-r<round>-<wave>`, spec.wave, and location `round-<r>/<wave>-dispatch.json`).
   Advisory `WARN ORDER` when spec/dispatch mtime is newer than ready (never changes the exit; mtimes do not survive checkouts).
2. **Rendering rule inferred from real pairs** (not from the validator source, which I did not read — INFERENCE of the rule,
   measured fit): task = `/skill:godspeed\n\n` (only if the body does not already start with `/skill:`) + body (`prompt`, else `item`;
   `{{item}}` substituted into `spec.template` when present) + `\n\nLane bounds: leaf member — no subagent dispatch` +
   (` except your single labrat.` for role executor, else `.`) + `\nJudged on: ` + axes (item axes, else spec axes) +
   (`\nMilestone: ` + spec.milestone when set) + `\n\nReport: write your scoped findings to <reportDir>/<name>.md`.
   Measured over all 44 spec+dispatch pairs under `.ufo/waves` (rounds 32–61): **42/44 reproduce byte for byte**
   (every item). The two that do not: round-59 w1 (0/66, the spec rewrite) and round-57 w2 (0/8: task == bare body, no wrapper;
   it would be flagged by the check; no lesson claims this was a fault — unexplained, not investigated).
3. **Real-file runs** (CLI, not fixtures):
   - round 61 live triple → exit 0, 8/8 PASS, claims sha `9afec8d4…ce0acec` found in context, 64/64 bodies render-equal.
   - round 60 live pair, claims `corpus/evidence/round60-claims.md` (sha `65721569…018d1`) → **exit 1**,
     `FAILED_CHECKS=CONTEXT_DIGEST,DIGEST_STRAY`: the round-60 context carries **no** 64-hex digest at all (so the QUALITY 116
     "digest in the dispatch context" requirement was also unmet, not only the wrong constant in prompts), and 128 tokens
     (64 spec + 64 dispatch) are `09d8053f…`. BODY_RENDER/NAMES/READY pass there, as the lesson implies.
   - round 59 live pair, claims path its context named (absent) → exit 1,
     `FAILED_CHECKS=CLAIMS_NONEMPTY,CONTEXT_DIGEST,DIGEST_STRAY,BODY_RENDER`, `0/66 dispatch tasks equal the rendered spec
     items`, plus `WARN ORDER spec +152s vs ready` (the lesson's post-ready rewrite, visible as mtime on this checkout).
4. **Selftest** (`--selftest`, optional `--lane-root`, `--work`): 34 fixtures built in a fresh temp dir from the real
   round-59/60/61 files (copied, then mutated; the lane is only read), each run as a child `python3 -B freeze-check.py …`;
   a case passes only if exit code **and the exact failing-check set** match. Result:
   `SELFTEST 34/34 pass`, `VERDICT: FREEZE_CHECK=34/34 red_before_exit=1` (the red-before = fixture R1, the real round-60 pair).
   Cases: green G1 real r61 triple; G2 round-60 pair with digest repaired in every prompt and context (exit 0 — shows the fix flips
   the verdict); G3 foreign digest with matching `--allow-digest`. Red: R1 real r60; R2 prompts fixed/context lacks digest;
   R3 context fixed/prompts still 09d8…; R4 real r59 + absent claims; R5 real r59 spec rewrite with claims otherwise fine
   (only BODY_RENDER fails); M01 empty claims; M02 claims +1 byte after dispatch; M03 claims absent; M04/M05 foreign or
   one-nibble-off uppercase digest in one prompt; M06 prefix-only digest; M07 65-hex run; M08 one spec item reworded;
   M09 all items rewritten; M10 task body extended; M11 lane-bounds line altered; M12 task missing; M13 task extra;
   M14 order swapped; M15 agent≠role; M16 context differs; M17 spec axes changed; M18 ready file missing; M19 ready names a copy;
   M20/M21/M22 ready round/wave/lane wrong; M23 empty dispatch path; M24 ready not JSON; M25 round as string; M26 wrong allow-digest.
5. **The selftest can fail** (mutating the checker, scratch copies, same selftest): forcing BODY_RENDER to PASS →
   `SELFTEST 25/34 pass` (R4, R5, M08–M13, M17 fail); forcing DIGEST_STRAY to PASS → `28/34 pass` (R1, R3, M02, M04, M05, M26 fail).
   Default-mode selftest cleans its temp dir (scratch listing empty after).

## Limits / calibration

- Exit 0 does not prove the claims are *good*; it proves the artifacts handed over are bound to one claims byte-string,
  the spec equals what was rendered, and ready points at that dispatch. It cannot see a spec rewritten **and** re-rendered, or
  a claims file edited before the digest is computed.
- The BODY_RENDER rule is a fit to 42 historic pairs, not the validator's source; a validator change in rendering will show as
  a false FAIL (loud), not a false PASS — unless the new rendering coincides with the old on every item.
- DIGEST_STRAY follows the item text literally ("no other 64-hex token … differs"): it also fails prompts that deliberately cite another
  64-hex hash. In the 44 historic task sets, 64-hex tokens occur in 6 pairs (rounds 32 w2, 33 w1, 36 w1, 43 w1, 44 w3, 60 w1 — task
  bodies only; I did not check whether those were deliberate cites or errors), so a deliberate foreign digest needs
  `--allow-digest <hex64>` (exact, repeatable, explicit).
  Only whole 64-hex tokens count: 40-hex commit ids and 8-hex prefixes in prompts are not compared (INFERENCE: a wrong commit id
  would pass).
- ORDER is advisory only; the check does not preserve spec/dispatch digests across time (QUALITY 118's "preserve the exact validated spec
  bytes and digest before ready" still needs a digest recorded by the L1 at render time; this check only compares spec against
  dispatch at the moment it is run).
- Round-57 w2's 0/8 render mismatch is reported as measured; I did not look for why.

## Receipts
```
python3 -B freeze-check.py --selftest         → SELFTEST 34/34 pass ; exit 0
live r61 CLI → FREEZE_CHECK=PASS exit 0 ; live r60 CLI → exit 1 (CONTEXT_DIGEST,DIGEST_STRAY) ; live r59 CLI → exit 1 (4 checks)
render fit: 44 pairs, 42 byte-exact, misses round-57/w2 (0/8) and round-59/w1 (0/66)
```

VERDICT: FREEZE_CHECK=34/34 red_before_exit=1
