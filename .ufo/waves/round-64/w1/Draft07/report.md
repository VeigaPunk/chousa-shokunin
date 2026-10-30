# Draft07 — round63 routed defects → round64 receipt coverage

## Behavior and axes

Documentary review only. Axes: operability (correct gate denominator and sibling evidence), calibration (execution versus dispatch versus claim), depth (durable provenance). No score change or closure verdict is asserted. Frozen claims were read before other lane artifacts. All paths below are relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

## Findings: routed defects 1–4

| Round63 routed item | Observed round64 coverage | Remaining gap / disposition |
|---|---|---|
| 1. Unreceipted on-sibling verification | `corpus/evidence/round64/controls/sibling-g0405.txt:1–33` contains kagi, kake, tameshi sections. Each records G04/G05 PASS, `PREFLIGHT=2/2 FAILED=none ENV=none SKIPPED=G01,G02,G03,G06,G07,G08`, `exit=0`. G05 pointer counts are 7, 36, 18; G04 is 0 pointers in each. Frozen claims lines 85–87 explicitly route this receipt; lesson lines 29–31 acknowledges it. | Documentary receipt gap repaired locally. The receipt lacks the exact executable command, timestamp, tool digest and sibling revisions: do not upgrade this review into a fresh sibling execution or verified committed provenance. No sibling run was performed here. |
| 2. Stale report `PREFLIGHT=5/5` | `corpus/lessons/round-64.md:31` explicitly supersedes 5/5 with the historical final 8/8 receipt. Opened `corpus/evidence/round63/controls/preflight-full-run-final.txt:1–10`: G01–G08 PASS, `PREFLIGHT=8/8 FAILED=none ENV=none SKIPPED=none`, `rc=0`. Five ordinary gates plus three selftests explains the denominator. | Historical figure reconciled without rewriting the historical report. Lesson names the receipt descriptively rather than its full path; use the exact durable path above in closure. Round64 claims lines 82–84 name a distinct proposed `controls/preflight-full-run-r64.txt`; that file was not present in the inspected round64 artifact inventory. The historical 8/8 must not stand in for a round64 full run. |
| 3. L2 floor unmet, attacks routed | `w1-dispatch.json:16–19` declares spawn=64/resume=0/total=64. The spec assigns C1 forgery/judge attacks to Attack01–06 and C2 mutant/selftest/parser/summary attacks to Attack11–16 (among other seats). Frozen claims lines 250–259 require one 64-seat wave, non-author counter reruns and fresh attacks. Lesson line 31 does not retroactively claim round63 met its floor. | Manifest/seat contracts establish intended routing, not completed executions. Dispatch member entries inspected have `agentId:null` and `item:null`; no attack completion or mutation success follows from the manifest. Current initial artifact inventory contained no Attack*/report.md or Counter*/report.md, although some fixture/probe artifacts existed and peers were working. Gather settled reports with command, stdout/stderr and exits; distinguish v3 frozen versus supplement, v1 versus v2, fresh forgery versus authored mutant set. Entailment remains a receipt requirement, not discharged by this scribe. Prior round zero-seat history remains unchanged. |
| 4. Scratch-path provenance | Frozen round64 claims use durable lane-relative receipt paths; `corpus/lessons/round-64.md:31` says scratch paths identify execution locations, not durable evidence. Opened historical durable `corpus/evidence/round63/controls/c1-on-fixed-tool.txt:1–6`: three `CLEAN=1/1 DEFECTS=15/15 BENIGN=6/6 BATTERY=PASS` lines, each run rc=0. | Cite this committed-location copy, not deleted scratch as the evidence artifact. Scratch may remain command context. No historical claim file was rewritten and this seat did not inspect commit history, so local presence is not independent proof of commit inclusion. Future final receipts must carry durable output paths and measured-byte identity. |

## Frozen gates and limits

- C1 is not admitted: `claims-erratum.md:5` reports E12/E13 independently generated filename/link identities. A conforming checker rejects those phantom rows, preventing the frozen full-pass target. `c1-battery-supplement.py` is a distinct post-freeze instrument; its pass cannot replace the frozen failure. This seat did not rerun either battery or independently derive fixture behavior.
- `controls/ref-preflight-v3.py` remains candidate, not production. Erratum line 6 discloses stem-versus-full-name and mirror-regex limits. No candidate result proves landing of `tools/lane-preflight.py`.
- Erratum lines 7–8 disclose C3 relocation arithmetic mismatch and omitted `c2-mutrun.py`; do not erase these by treating source admissions or planned receipts as frozen counter success.
- Frozen C1 still requires unmodified battery ×3 at landing, null FAILs, and v2 cross-check ×2. Frozen C2 requires its 12/12 matrix, reproduced v1 survivors, selftest and fault leg. Frozen C3 requires its exact counter line and sourced-leg disposition. This review supplies none of those executions.
- Inspection was a live local snapshot while the wave was running, not a final absence audit. Files can arrive later; absence here means absent from the observed inventory only. No outside non-author closure authority is claimed.

## Commands, outcomes, and provenance

No shell commands, probes, test runs, builds, runtime invocations, network requests or git/jj commands were executed by this seat. Therefore there are no newly exercised process exit codes. The rc/exit values above are exact receipt content, not this seat's executions.

Read-only tool operations: `read` on `/home/vgpnk/.omp/agent/RULES.md`, `skill://godspeed`, `skill://agent-self-evaluation`; lane `claims.md`, round63 spotcheck, round64 erratum and lesson, sibling receipt, historical final preflight and compatibility receipt, wave dispatch/spec; `glob` on round64 artifacts and the two historical receipt names; `grep` on routing/provenance phrases. Reads succeeded. Initial broad glob requested limit 240 and tool clamped it to 200; its returned inventory was small and no unobserved artifacts are claimed. JSON queries for nonexistent `.tasks`/`.keys` and `.item` returned null; corrected exploration used root `keys` and inspected actual `prompt` fields. These nulls were not execution evidence.

Tools installed/updated: none. Scratch directory and live clones: none created; no cleanup required. Touched surfaces: only this report and the explicitly requested trailer report alias. Production, frozen inputs, operator inputs and sibling files intentionally unchanged. No subagent dispatch.

## Assignment path conflict (verbatim)

“Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft07/ (report.md); no production edits.”

“Report: write your scoped findings to .ufo/waves/round-64/w1/Draft07.md”

The folder report holds the detailed mapping; the explicit trailer path holds a concise findings report linking it. No contract or judgment is changed by either report.

## Self-evaluation

Accuracy 4/5: receipt facts separated from executions; live snapshot lacks independent committed-byte verification. Completeness 4/5: all four routed defects mapped, with ongoing attack receipts intentionally not promoted. Clarity 4/5: status and missing evidence explicit, but provenance caveats lengthen the table. Actionability 4/5: exact durable pointers and receipt requirements provided; final closure belongs to L1/integrator. Conciseness 4/5: repeated gate cautions prevent misattribution but could be shorter. Mean 4.0/5. Highest-impact improvement for final integrator: attach settled attack receipts and final measured-byte identities, then retain historical-versus-current denominator distinction. User should agree this is documentary mapping, not new verification.

Report: .ufo/waves/round-64/w1/Draft07.md
