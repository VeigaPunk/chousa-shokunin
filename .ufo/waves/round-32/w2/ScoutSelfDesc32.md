# ScoutSelfDesc32 — self-description vs landed gate

Verdict: **BROKEN** (self-description). Mismatch count on disk: **11 false assertions in 8 sentences**. At landed commit `5d8a170` (before the uncommitted doc patch): **26**.

Gate checked: `tools/research-gate.sh` SHA-256 `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098` (matches the landed claim). Scratch clone `/fast/scratch/hyaku/chousa-r32/w2/ScoutSelfDesc32/lane` at `5d8a170795dcf48c3746a4f03dee9cfe32812834`.

```
timeout 600 bash tools/research-gate.sh --selftest
EXIT:0
RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)
ok-case 229 chain-exempt-resolvable
ok-case 230 chain-exempt-unresolvable
ok-case 231 chain-exempt-judgment
ok-case 232 chain-exempt-mixed
ok-case 233 c1lk-holder-blocks-append
ok-case 234 c1lk-second-append
ok-case 235 claims-r2-sha-nonstring
ok-case 236 claims-r2-line-nonstring
ok-case 237 claims-r2-endline
ok-case 238 claims-r2-span-stale
ok-case 239 claims-r2-ws-pin
ok-case 240 r2-hash-fault-shim
ok-case 241 claims-r2-nested-string
```

What the gate does (read in `tools/research-gate.sh`, pinned by those cases): exclusive `flock -x` covers the last-byte probe and the append (`:3274-3299`, cases 233–234). U-status hops (`unresolved`, `blocked-no-fetch`, `labelled-dead`) whose citation would verify print `observed=resolvable` and `FINDING CHAIN_EXEMPT_RESOLVABLE` (`:1947-1955`, cases 229–232). `rejected` / `not-applicable` stay unread. Non-string `"line"` / `"sha256"` are invalid, not absent (cases 235–236). End-line-only binding, span-before-stale, and hash-fault are selftest cases 237, 238, 240. v3 counters `corpus/evidence/round31/c1-count-v3.py` and `c2-count-v3.py` add `I2_nonstring_*` (TOTAL 132). Those counters were not executed.

Counting rule: a present-tense assertion the landed gate contradicts. A sentence a later sentence in the same file marks as a past-revision record is listed under retracted, not in the 11. Round-N measurement paragraphs ("Measured at … sha", `PASS (40 cases)` and the like) are not counted. `README.md` and `PROVINCE.md`: no such sentence.

Uncommitted (not at `5d8a170`; `git status` showed `M` on these three only): `SKILL.md` table `228`→`241` plus a round-32 counter row; `corpus/README.md` Round32 frontier disposition; `json-delimiter-r24.md` closing postscript. Line numbers below are the on-disk files.

## Live (on disk, unretracted) — 11

1. `SKILL.md:189-192` (one sentence, two assertions). "`observed` verified|anchor-missing|refused|invalid|exempt" and "`unresolved`/`blocked-no-fetch`/`rejected`/`labelled-dead`/`not-applicable` hops stay exempt but counted." The gate prints `observed=resolvable` for a resolvable U hop (case 229). `rejected`/`not-applicable` do stay exempt (case 231). The following sentence ("CLEAN iff every non-exempt hop verified") is not counted: a resolvable hop is a finding, so CLEAN still requires every non-exempt hop verified.
2. `SKILL.md:420-421`. "exempt (`unresolved`/`blocked-no-fetch`/…) hops are counted, never verified." Those hops are probed with the resolved-arm rules.
3. `corpus/README.md:314` (Known gaps). "exemption-truth and external-source limits stand unchanged." Exemption-truth changed; the other limits in that sentence were not re-checked.
4. `corpus/README.md:326-327` (Known gaps). "exemption is the record's own declaration, never verified." False for the three U statuses. Transitivity "remain unbuilt" in the same sentence was not re-checked.
5. `SCORECARD.md:1781`. `## Planned — round 32 (not started)`. The candidate is landed at `5d8a170` and the selftest above ran on it. No later scorecard section records that.
6. `SCORECARD.md:1784-1785` (clause of the candidates sentence). "a mutant the counter kills but the selftest does not" for end-line-only binding. Case 237 `claims-r2-endline` passed.
7. `SCORECARD.md:1785-1786` (same sentence, second clause). "`--json` appender serialization (Planned26)" still only a candidate. Cases 233–234 passed; the append block takes `flock -x`.
8. `SCORECARD.md:1798-1799` (clause). "a present non-string `"line"` or `"sha256"` treated as absent would still score 120/120 on both counters (no fixture class". Cases 235–236 expect `invalid` / "not a JSON string" / "sha256 malformed" and passed. Fixture classes exist in `c1-count-v3.py` (`I2_nonstring_line_value`, TOTAL 132) and `c2-count-v3.py` (`I2_nonstring_sha_value`, TOTAL 132). The v3 counters were not run, so the "120/120" half is [INFERENCE] from those files plus the selftest, not a counter receipt.
9. `SCORECARD.md:1801-1802` (same "Open, not fixed" sentence). "fail-open hashing and span-before-stale are killed by the counter but not the selftest." Cases 238 and 240 passed. The nested-key clause in the same sentence is still true (gate comment at `research-gate.sh:7340-7346`; Round32 disposition `:985`).
10. `SCORECARD.md:1803-1804`. "Planned round 32 adds these as fixture classes before data." The classes are in the landed selftest (235–241).

Not counted as still-true planned clauses: `## Claims` table `path:N` binding and the L0 fetch-scope item (`SCORECARD.md:1783-1786`; Round32 disposition `:984-987` still lists both).

## Retracted on disk, still worded (not in the 11)

These are the examples in the brief. A later sentence now marks them historical. They are false if that later sentence is ignored. They are **live at commit `5d8a170`**, because the retracting sentences are only in the uncommitted patch.

- `corpus/knowledge/json-delimiter-r24.md:66-71`. "(named debt, not fixed)"; "two operations with no lock"; "The gate assumes one writer per manifest"; "`flock` around probe + append is the candidate fix." The 16-appender blank-line measurement in the same bullet is a past receipt, not counted. Retracted at `:79-82` ("closed on gate `10f2fe12…`"; "kept as the round-24 record"). Four assertions.
- `corpus/README.md:360-361`. "exemption is record-declared and unverifiable". Round-3 frontier paragraph. Retracted by the uncommitted Round32 disposition `:978-981`, which quotes that phrase and records `CHAIN_EXEMPT_RESOLVABLE`.
- `corpus/README.md:846-847`. "Still open: concurrent appenders to one manifest". Round-24 frontier paragraph. Retracted by `:974-977` (flock held ground).
- `corpus/README.md:507`. "exemption truthfulness stays author-declared beyond the audited instances." Round-10 saturation paragraph. Same disposition supersedes it for the three U statuses. URL hops and `rejected`/`not-applicable` stay unread (`:981-984`).

## Landed-commit delta (HEAD `5d8a170`, not on disk now)

`git diff` of the three dirty files. These were current self-description at the landing commit:

- `SKILL.md:77-84` (8 rows). Each self-test cell said `PASS (228 cases)` as the command result. The on-disk rows say `PASS (241 cases)` and name cases 229–232, 233–234, and 235–241. That numbering matches the selftest. `:89` now says the rows read 241.
- The four json-delimiter assertions and the three corpus README frontier sentences above (no postscript, no Round32 disposition at HEAD).

HEAD mismatch count = 11 live + 8 case-count rows + 4 delimiter assertions + 3 frontier sentences = **26**.

## Not mismatches

- `README.md`, `PROVINCE.md`: no lock, exemption, case-count, or writer claim.
- `SCORECARD.md:1765` and `:1798` `PASS (228 cases)` inside the round-31 verdict: scoped to final gate `0bc318b3`. Consistent with 228 + 13 new cases. Not re-run on that gate.
- `SCORECARD.md:1374-1375` "flock candidate remains unlanded in r25 wave evidence": scoped to r25 evidence; `:1449` marks that planned heading historical. The sentence does not say the current gate is unlocked.
- `corpus/README.md:223-224` "appends by discipline, not construction: one `>>` per run": the write is still `O_APPEND` and prior bytes are not rewritten (case 233 checks the fragment line and the inode). The new fact is the lock, which that bullet does not deny by name. Not counted.
- `SKILL.md:192-193` CLEAN rule, as noted above.

## Limits

C1/C2 counters were not run (other seats own that surface). v3 counter totals are from the source, not a receipt. Nested `"line"`/`"sha256"` remains a carried violation, not a mismatch. The 241-row, Round32 disposition, and delimiter postscript are uncommitted; a later edit can move the line numbers. No packages installed.
