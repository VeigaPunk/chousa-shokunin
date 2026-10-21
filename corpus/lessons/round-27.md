# Round27 — repair representations without relaxing the verdict (2026-10-21)

Base master64eec5d41c7cf7f17f5ce1e968e28b3769952596; round27 attempt1 only.
L1 ChousaR27 holds the planner/integration seat. The opening lane state was
clean; no earlier round27 work or wave was inherited. Prior coordinator
provider churn belongs to round26 and is retained in its lesson, not retried.

Declared claims: C1 operability (lowest measured axis): fix the actual three
usage selftests; C2 freshness: repair ASCII/calendar input handling and
nonrecursive decimal normalization; C3 calibration: repair registry state,
S-id occurrence identity and filesystem-path representation. Exact scope:
`corpus/evidence/round27-claims.md`. No round28 activity.

## Spot-check intake

The operator reports round26 rejected-harmed, fleet rounds[414], streak1:
selftest FAIL3/187 and C2/C3 falsified. The committed round26 lesson and
falsifier reports are accepted ground truth. No old failure was rerun merely
to confirm it. No separate round26-verifier-spotcheck lesson or operator-*
teaching was present in the lane glob at opening. Outside closure remains
orchestrator-owned; lane-dispatched reviewers are not outside verifiers.

| routed issue | disposition | evidence |
|---|---|---|
| Three usage assertions reject their own help text | C1 repairs record recognition, retains cases/exit2/diagnostic/no-verdict requirements | S040; r26 FNoTrade115–137; usage helper |
| Locale-dependent CLI dates and recursive zero normalization | C2 repairs both representations, adds independent synthetic controls | S041; r26 FDateAsOfUsage75–86 and FDateHugeCadence34–44 |
| Stale table columns, consumed-text rescan, citation-pointer predicate on raw path | C3 repairs actual consumers, not just a fixture or public claim | S042; three named registry reports |
| Registry memory/time amplification; broader Markdown grammar; entry-reader time; filesystem races; JSON-appender race | Carried: not closed by these bounded repairs; no universal resource/read-safety claim | r26 lesson R26-M10/M11; r25 appender receipts |
| Stale source-line locator and source rejection quote quality | Carried rather than rewriting earlier evidence; this round's sources are exact local reports and current production functions | r26 lesson smaller findings; no external fetch |

## Mistakes

| id | class | evidence pointer | captured-by | fix / shown-to-fail basis |
|---|---|---|---|---|
| R27-M1 | wrong representation: help phrase mistaken for verdict record | r26 FNoTrade115–137, shared FAIL3/187 | original shared PASS hold; QUALITY17 | anchored record recognition; preserve all original cases and independently reject wrong exit, missing diagnostic and actual verdicts; S040 |
| R27-M2 | input-domain mismatch: locale regex versus arithmetic decimal | r26 FDateAsOfUsage75–86 | declared ASCII date contract; QUALITY17 | helper-local ASCII validation and Unicode-date controls; S041 |
| R27-M3 | recursive normalization before safe-magnitude bound | r26 FDateHugeCadence34–44 | QUALITY18; declared no-termination contract | stack-safe leading-zero normalization; long-zero and all-zero controls; S041 |
| R27-M4 | stale parser state crosses table boundary | r26 FRegistryHeaderless41–49 | named-header contract; QUALITY17 | fresh columns after breaks and matching delimiter width; positive/negative reordered-column controls; S042 |
| R27-M5 | token rescan loses occurrence identity | r26 FRegistryIdBoundary28–45 | standalone-ID contract; QUALITY17 | exact token iteration; independent finding cardinality rather than code-set comparison; S042 |
| R27-M6 | filesystem path treated as citation pointer | r26 FRegistryRegistryDeny23–30 | declared refusal contract; QUALITY17 | separate raw-filesystem predicate and citation wrapper; synthetic temporary paths only, no host/live-process probing; S042 |

The red-before observations remain committed in the r26 receipts above.
`round27-mechanisms.py` separately counts the exact historical code mechanisms
without executing a failed gate. At base its claim totals are C1=1/C2=2/C3=5
(the last is two parser mechanisms plus three raw-path call sites). This is
a lexical probe, not a proof of behavioral correctness or an admission gate.
The final independent synthetic regressions and full selftest own after
verdicts; changed implementation spelling alone never counts as a fix.

## Gate

New rows were opened locally this round, access2026-10-21. There was no
external network, live target, host-secret or live-process probe.

| row | source path / located quote (at most25 words) | scope |
|---|---|---|
| S040 | `.ufo/waves/round-26/falsify/FNoTrade.md:126–128`: “the predicate is unsatisfiable for any usage exit, and the failure is deterministic rather than flaky.” | reported usage-harness cause; code at `metadata_asof_usage_case` opened too |
| S041 | `.ufo/waves/round-26/falsify/FDateHugeCadence.md:42–44`: “Bash's extglob `+(0)` longest-prefix match recurses in proportion to the run length.” | reported zero-prefix normalization cause; date helpers and locale report opened too |
| S042 | `.ufo/waves/round-26/falsify/FRegistryHeaderless.md:45`: “a non-pipe line sets `header_candidate=0; continue` but does not reset `id_col`/`status_col`/`usedby_col`.” | reported stale-column cause; ID and raw-path reports opened too |

Rows S040–S042 are new tierA own-work rows, initially mined because this
lesson cites them. Existing rows' status/recheck/used-by cells are unchanged;
there are no unlogged old→new mutations. Old S035/S036 rows describe declared
policy, not current trustworthy capability; r26 withdrawal addenda remain.

Admit as bounded repair evidence: the three reported causal diagnoses,
subject to the new failing controls and final execution receipts. Reject:
“a green registry/date screen proves source truth”, “input-byte cap is a
whole-parser resource budget”, and “repair retroactively admits round26”.
Flip: directly establish the respective stronger property with independent
scoped evidence; these local parser controls do not establish it. No new
knowledge coverage or repertoire capability is counted merely from source
row growth. Outside admit/reject spot-check remains for fresh non-author
closure, never self-awarded.

## Build review dispositions

- `CriticHarness`: accepted. All new selftest calls follow original187;
  C1 adds a positive usage/help control and first-line DRIFT rejection, not
  only three negative predicates. The independent C1 scenarios also reject
  missing helper commands, so infrastructure errors cannot masquerade as
  successful negative controls.
- `CriticMeasurement` / `ConnectFailures` / `CriticFrontier`: the initial
  base-regression proposal was superseded before any baseline gate execution
  by the claims' Measurement clarification. The before side is the exact
  accepted r26 behavior receipts plus the safe source-mechanism count; no
  green/red new-suite comparison over the old crashing gate is claimed.
  New long all-zero and131072-zero fixtures were unmeasured at baseline.
  Final outputs bind both script and gate hashes. Old r26 differential
  agreement remains limited to its actual ASCII/set-of-code population.
- `CriticPathScope`: accepted monotonicity constraint. A complete-filesystem
  predicate must add full-path matching without losing old `.env:1` refusal;
  the citation wrapper remains unchanged. Direct source-path input at
  `claim_source_path` is a filesystem input (it opens the complete `src`,
  unlike a citation pointer), so it and its canonical target belong to this
  cutover too. Scouts' contrary classification of that site was rejected
  after reading1125–1155. No host files were used to settle the distinction.
- `CriticRegistryTokens` / `ScoutRegistryReader`: preserve one finding per
  genuine occurrence, not one per distinct id. Streaming token extraction
  avoids introducing the gate's already-documented slow negated-class
  substitution. Finding/output volume and used-by reparsing remain limits.
- `ReviewSourceAdmission`: the draft S040 quote's escaped pipe was not exact;
  it was replaced before landing by a shorter exact quote at126–128.
  Local source openings: L1 plus `ScribeSourceUsage`, `ScribeSourceDates`,
  `ScribeSourceRegistry` and `ScoutIntake`; their reports retain the locations.
  S040–S042 record reported diagnoses. Their proposed repair rules are lane
  inferences, not source-backed proof of passing behavior; the final controls
  must establish those outcomes.
- `CriticRegistryGrammar`: carried, not silently fixed. The checker remains
  a first-named-line-pair table scanner, not the source-census grammar or a
  full Markdown parser. Fenced/indented/commented examples, duplicate header
  names/keys, body-row header shapes, escaped pipes, adjacent tables and
  Unicode whitespace differences retain their disclosed grammar limits.
  Snapshot input-byte caps do not establish memory/time or race safety.

Remaining r26 debts are not lost through the narrower repaired population:
31 no-report falsifiers remain historical incomplete coverage (including the
missing mutation seat); source/span location pairing, receipt identity and
the round12 Receipt L0, parent-root/race/appender debts, S025 quote quality,
and public-source mutability stay open. No capability or retrospective r26
admission is inferred. S035/S036's original implementation anchors are
pinned to r26 production0e9784bd52eca456b24d0bc40921480a47f91a2b; opening
the same function name after r27 is a new observation, not those old bytes.

Additional in-round mistake R27-M7: an L1 text edit used stale inferred line
numbers in the newly written regression script and temporarily replaced
scenario-list rows. The edit tool's parse guard rejected its syntax; L1
re-read60–115 and corrected only the displayed region before execution.
Captured-by: editing contract and tool parse guard, not a passing runtime
test. A similar draft lesson-table row displacement was corrected from
the displayed edit result. These are not fabricated test passes or ignored
warnings; final behavioral evidence must come from the corrected committed
bytes. See the final script hash in its regression receipt.

## Coordinator overlap and misroot (same attempt)

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| R27-M8 | duplicate writer: a replacement L1 was spawned while the original was alive | `history://ChousaR27R2` opening (“died 16min in on Devin weekly quota”); original ChousaR27 kept running and integrating | prompt rule “never restart a duplicate writer”; one-integration-owner wave context | detected by ChousaR27 from an unexpected gate-content change plus `proc://`; R2 stopped on message and yielded; ChousaR27 kept ownership. R2's uncommitted outputs were inspected and kept: union merge of the three executor clone trees as `tools/research-gate.sh` (sha256 ca39d14d…92f84, replacing L1's partial in-tree merge), the narrowed C3 stale-state mechanism pattern, and sandbox receipts. Nothing was committed or dispatched twice. All after-measurements are re-taken on the helper-landed revision, not on either writer's working copy. |
| R27-M9 | misroot: seat report written relative to fleet root | `ReviewDateCalendar` wrote `/home/vgpnk/Projects/shokunin/.ufo/waves/round-27/build/ReviewDateCalendar.md` | wave context's absolute-path rule (relative `Report:` trailer) | R2 copied it byte-exact into the lane path (cmp-verified, sha256 cd07ab85…) and removed only that fleet copy; reported here. |

R2 also found executor patch files not directly applicable on the moving
tree (`ExecUsage.patch` context at6235; `ExecRegistry.patch` corrupt at
its line334), so the clone trees, not the patch files, are the integration
inputs. The original L1's earlier dev-tree run (gate sha3e26c746…) is not a
receipt for the committed bytes.

Parent correction (Main IRC, 2026-10-21): ChousaR27 did die at about
15m50s on a Devin weekly-quota stream error and was revived as the same
identity; it did not observe the gap from inside its own session. Main had
already spawned ChousaR27R2 before seeing the revival, so the two-writer
overlap is parent-caused, not an R2 or seat fault. R2's union merge
(sha256 ca39d14d…92f84) overwrote ChousaR27's partial in-tree usage edit.
ChousaR27's earlier citation of gate sha3e26c746… described a transient
working copy, not the bytes now in the lane; only the helper-landed blob
`dd72641e574679c4f7882dd43de072b4c8892d6f:tools/research-gate.sh`
(ca39d14d…, verified equal to the archived measured tree) is cited.
ReviewDateCalendar's fleet-root write is seat-scope debt (R27-M9), not a
lane-authored file at the fleet root.
