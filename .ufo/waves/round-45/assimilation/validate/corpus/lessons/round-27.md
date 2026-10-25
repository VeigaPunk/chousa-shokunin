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

## Host crash and replacement coordinator (same attempt)

The host omp session froze and was killed (SIGHUP, 2026-10-21 13:10:51 -03).
ChousaR27 and every live seat died with it; ChousaR27's last tool call
(16:10:53Z) was a falsify-collection wait. Replacement L1 `ChousaR27-2`
(session 3) inherited the held claim27/attempt1 and reconstructed state only
from durable evidence: lane tip `dd72641e…` (pushed, ahead0), the untracked
falsify-wave files, the build/falsify registries and seat transcripts.

Seat accounting (registries vs report files): build64 = 58 reports + 6 dead
no-report (ReviewDateUnknown, ReviewRegistryBreak, ReviewPathSynthetic,
ScribeQuality, ScribeScorecard, ConnectSibling); falsify64 = 63 reports + 1
dead (IntegSourceGate, scribe; its transcript ends `Request was aborted` at
the host kill). The falsify task call was cap-refused ten times
(12:00–12:27 -03) and spawned all 64 on attempt 11; refusals spent no seats.
The 73 `ChousaR27R2.*-4` transcripts all carry a `Kotodama round 50` goal
(that identity's later assignment), so ChousaR27R2 spent no chousa seats.
Dead seats were neither replaced nor re-issued. Round total so far 128.

Inherited and re-verified: dd72641e (gate ca39d14d…, re-hashed), its
landed-measurement receipts (selftest PASS210 reproduced in a fresh archive),
63 falsify reports (read and triaged below). Inherited and moved out, not
committed: `.ufo/waves/round-27/work/` (three executor nested-git clone
sandboxes, 28 MB) → `/tmp/chousa-r27-work-archive`, with HEAD/sha manifest
`.ufo/waves/round-27/work-manifest.json`. Discarded: nothing else.

## Falsify-wave dispositions (63 reports at dd72641e)

Landed-gate counterexamples, all repaired at `cb895a2bdd259eb38bec29ef70011d8211a508b5`
(gate sha a6bc2855…2386); each repair has a control red on dd72641e and green after
(`.ufo/waves/round-27/post-falsify/fc-before.stdout` 4/26 mismatches →
`fc-after.stdout` 0/26):

| id | class | evidence pointer | captured-by | fix / shown-to-fail basis |
|---|---|---|---|---|
| R27-M10 | introduced regression: width-equality repair counted `\|`-split fields, so a GFM-valid escaped-pipe header was refused (and a 4/5 table accepted) | FC3ValidTable27 §3A/B (S043) | QUALITY17 positive no-trade controls had no escaped-pipe shape; captured only by the falsify wave | width counts cells after removing `\|`; controls `escaped-pipe-width`/`-overwide` red on dd72641e (exit2/exit0), selftest 211–212 |
| R27-M11 | introduced cost regression: per-token bash loop over every alphanumeric token (12–34× on token-dense sources) | IntegTokenCost §3 (S043) | none (no cost control); falsify wave | `grep -xE 'S[0-9]{3,}'` prefilter before the loop; end-to-end dense 4 MiB entry 68240 ms → 409 ms, base 64eec5d timed out at 300 s (`post-falsify/timing.log`) |
| R27-M12 | fail-open: usage helper accepted when its record matcher errored | FC1CorrectUsageWithHelp00 line7 (S043) | none; falsify wave | fail closed on grep exit>1, one shared predicate; control `matcher-fault-fails-closed` red on dd72641e (exit0), selftest 215 |
| R27-M13 | inherited quadratic: `${line%$'\r'}` on unbounded lines made admissible 4 MiB cadences take >60 s | FC2Allzero128K07 line18, FC2HugeMagnitude08 §3 (S043) | C2 "without termination" read only at 128 KiB | test-then-substring strip at both read loops; `scale-4mib-leading-zeros` red on dd72641e (timeout124), 827 ms after |

Control-strength findings (no landed-gate counterexample; about 40 reports):
vacuous or non-discriminating controls (C-locale date tokens, leap rows, max/overflow
spans, positive tables, single-leg denylist sites, C1 mutants). Accepted as coverage
debt; 22 of the 26 new controls in `corpus/evidence/round27-falsify-controls.py`
encode their killing inputs (mixed outer pipes, delimiter after blank, consulted-row
twin, Gregorian-invalid `--as-of`, one-significant-digit and 8–19-digit cadences,
raw-leg-only registry/entry/claims refusals with `reason=denylist`, indented and
column-0 non-verdict records, different-diagnostic and exit0 rejections). Those 22
pass on dd72641e too: they strengthen the suite, they are not repair evidence.
`round27-regressions.py` is unchanged (sha 5afea786…).

Open, not repaired — C3 clause conflict: FC3ColonDeniedSuffix46,
FC3LegacyEnvAnchorRefusal47, FC3ClaimsLegacyEnvAnchorR57, FC3PlainDeniedComponent44
(C-A) and FC3EntryColonDeniedCompon50 (CX4) show `is_denylist_fs_path` keeps the
citation-prefix arm (`ptr_file_part`) beside the new complete-path arm, so
`notes.env:v2/registry.md` and `synthetic.env:1` are still refused by prefix. The
frozen clause says "inspect complete filesystem paths, not citation-anchor prefixes".
The r26 failure class (an earlier colon hiding a denylisted complete path) is closed;
the raw-prefix over-refusal is base-identical. Residual reviewer ResC3Clause
later found a new claims-canonical prefix refusal (see below). Dropping the
arm narrows the inherited refusal set; that does not by itself prove a
secret-path exposure. The L1 retained the frozen negative controls.
C3's negative clause is therefore **not met**; filed as an L0 question, not redefined.

Other residuals recorded, not silently treated as fixes: BOM-prefixed registry
now exits2 (was1; GFM oracle finds no table) is an intentional evaluation-class
change; `|-|` short delimiters, fenced tables and body-row headers are
base-identical grammar limitations (FC3ValidTable27 §3C). The full selftest is locale-sensitive —
with `LC_ALL=C` exported, 10 claims/verify-all cases fail on dd72641e and on
cb895a2 alike (`post-falsify/selftest-before-here.log` was rerun under UTF-8 and
passed 210). R27-M14 (L1 tooling slip): a first gate edit used offsets from a
stale window and displaced two hunks; the edit result display showed it and the
next edit restored them before any run; `bash -n` and `git diff` confirmed.

## Gate (post-falsify source row)

| row | source path / located quote (≤25 words) | scope |
|---|---|---|
| S043 | `.ufo/waves/round-27/falsify/FC3ValidTable27.md:59`: “so the header counts 5 cells against 4 delimiter cells.” | escaped-pipe width regression; also IntegTokenCost.md:20, FC2Allzero128K07.md:18, FC1CorrectUsageWithHelp00.md:7 (cost, CR strip, matcher-error reports) |

S043 is a new tierA own-work row opened 2026-10-21, status mined, used-by this
lesson; no existing row's status/recheck/used-by changed. Census
`sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`: start exit0
(39 rows; A33 B1 C5; mined16 queued19 rejected4) → end exit0 (43 rows; A37 B1 C5;
mined20 queued19 rejected4).

## Residual review and final repair dispositions

The post-crash integrated work exposed fewer than64 distinct new attack items.
One ordinary batched call of8 read-only seats (5 reviewer,3 critic) therefore
covered the four repairs and their controls, rather than padding a new wave.
It was cap-refused15 times and spawned8 on attempt16
(`.ufo/waves/round-27/residual/attempts.log`, `dispatch.json`).
This makes136 dispatched seats total, not a new64-seat wave. No dead item was
reissued. Their immutable reports target cb895a2; follow-up checks explicitly
name candidate digests and do not silently turn that checkpoint green.

| id | class | evidence | captured-by | fix / shown-to-fail basis |
|---|---|---|---|---|
| R27-M15 | width-only correction left header/body indexes on the naive split: escaped pipe before status could turn queued into mined and emit false CLEAN | ResControlsSuite §5, ResWidthFix F1–F3 | criterion21 positive syntax was incomplete; residual reviewers | one shared escape-preserving split now owns indexes, width and body cells; added queued/mined twins, escaped body and terminal-header controls; original cb895a2 stays recorded as falsified |
| R27-M16 | prefilter introduced another scanner-failure point; suppressed grep faults became informational NO_ROW_ID and false CLEAN | ResTokenPrefilter F1/F2 and follow-up | criterion22 initially covered usage only; residual reviewer | capture/check tokenizer and filter separately, return exactly one META_SOURCE_SCAN_FAILED crit on either fault; two independent option-specific fault controls, no NO_ROW_ID emitted on fault |

Shared split: double literal backslashes, reduce only the escaped-pipe
sequence, then `read -a` without `-r`; optional terminal outer pipe is not
removed when escaped. This preserves raw non-pipe backslashes while making
header and data column indexes agree. ResWidthFix tested2256 exhaustive
rows and51 fixtures against cmarkgfm2025.10.22/markdown-it-py4.2.0:
the candidate matches cell count/text; one-dash delimiter remains an
explicit inherited limitation, not a claim of full GFM parsing.
The bounded122 KiB bundle is preserved at
`.ufo/waves/round-27/residual/width-oracle-bundle/` before scratch cleanup.

The single-stage `grep -w` alternative was rejected before landing:
ResTokenPrefilter showed GNU and the agent-shell Rust grep disagree on Unicode
word boundaries even with LC_ALL=C. Separate byte-oriented stages keep the
old boundaries and make both exit statuses observable. A pipeline alone can
hide first-stage error2 behind last-stage no-match1. Follow-up evidence
`residual/scanner-followup.json` binds gate ac1315dd…;1005 source values
retain identical findings and exits, tokenizer/filter/missing-grep faults
each produce one crit. Token capture is8 MiB-input-bounded, not a whole-process
RSS budget. Dense2 MiB cost224.75 ms vs cb895a2 209.25 ms is a disclosed7.4%
trade relative to the faulty intermediate, while dd72641e took16253.01 ms.

ResC3Clause confirms C3 is partially falsified, including a **new** over-refusal:
claims alias `plain.md -> k.env:1` read at base but refused by the new canonical
prefix arm. The earlier paragraph calling prefix behavior wholly inherited
is superseded by this finding. Removal would narrow the base refusal set,
not prove a secret-file exposure; nevertheless changing the frozen negative
controls to erase this result is not this round's resolution. C3 stays
not met and no-harm is not established. ResNoHarm also records new canonical
ancestor-sensitive claims refusals; these are disclosed, not called unchanged.

ResControlsSuite reproduces26/4 mismatches at dd72641e and26/0 at cb895a2.
Three are deterministic correctness failures; the fourth (4 MiB cadence)
is a60-second timeout, not a wrong computed result: with600 seconds it
completed correctly in67.38 seconds. Timing depends on host load; the final
control is a scale/operability witness, not an invariant4-failure baseline.
ResReceipts independently reproduces all checkpoint commands, but flags
historical `corpus/evidence/round27-*-after.*` as dd72641e receipts. They are
retained unchanged; final evidence is separately pinned under
`.ufo/waves/round-27/final/`. Its timing disagreement (base completes in64 s
versus L1's observed300-second timeout) is preserved, not silently corrected.

Tooling: ResWidthFix installed cmarkgfm2025.10.22, markdown-it-py4.2.0
(dependencies cffi2.1.1, pycparser3.11, mdurl0.1.2) and uv-managed CPython3.15.0
via official PyPI/uv `uv run --with`, for independent GFM oracles.
Other residual seats and the replacement L1 installed nothing.
The host /tmp ENOSPC notice led to moving the executor archive onward to
`/fast/scratch/hyaku/chousa-r27/work-archive`; the historical manifest's first
destination remains unchanged. Round-owned scratch is removed at landing.

R27-M17 — coordinator scope debt: the residual ResControlsSuite item asked
for a base run of the new suite, contrary to the frozen measurement
clarification's instruction not to rerun reported base failures through a
new wrapper. The critic's instrumented25-control base run (long-token crash
case skipped) is retained as an out-of-contract diagnostic, not admitted
before evidence. Captured-by: comparing the item with
`round27-claims.md:25–36`, not a green tally. The report's before side remains
the accepted r26 receipts and non-executing mechanism count; no baseline
failure rerun can replace that authority.

## Final immutable measurement and landing hygiene

Measured production4f48419425f5165a8f950e1db4c0a781cf845d40,
gateac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765.
`final/identity.json` (under `.ufo/waves/round-27/`) binds argv, cwd,
UTF-8 environment, exits and hashes: mechanisms0/0/0; original58 controls
zero mismatches; final32 controls zero mismatches; selftest PASS215,
no skips; original210 case identities unchanged, legacy161 SHA unchanged;
date9024/9024, registry48/48, metadata54/54, drift none, r1 observable3/3.
The full final suite ran once after all residual seats completed.
C3 is nevertheless partially falsified; negative prefix controls retained.

Fleet misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`,
no pathspec) found no new chousa report misroot; other lanes' report/state
and watchdog changes were left alone. The chousa L0 line was concurrently
swept into fleet72a724b5db6b4a261c0999b64a7fc1ee6d4326a3,
authored kama-shokunin; that attribution is recorded, not rewritten.
Build/falsify deaths are7 total; original errors and malformed/truncated
transcript counts are retained in `inherited-final-reconciliation.json`.
All8 new residual seats reported, no provider death or replacement.

Cleanup: completed round-owned `/tmp/chousa-r27-*` and
`/fast/scratch/hyaku/chousa-r27` removed (du before cleanup:1.5 GiB total),
without touching other lanes. The122 KiB oracle bundle was copied into the
lane, its manifest cmp-verified, then the duplicate ~/.cache copy removed.
No claim is made that the now-removed experimental sandbox paths remain
live; retained scripts/results, reports and pinned git revisions own evidence.
