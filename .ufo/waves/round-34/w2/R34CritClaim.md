# R34CritClaim — claim-record adversarial review

## Scope and axes

Read-only review of the claim/exclusion record and committed control chronology, not a candidate execution, admission, or canonical runtime judgment. Paths below are relative to the lane unless absolute. The assigned candidate is `3026a4e5bb4c44c01982fd67bd0140df36384942`; concurrent lane work subsequently committed measurements as `934d7cb`.

**Named claim axis: operability.** `claims.md:17-32` names the existing `verify-claims` command, its argv-limit failure, and preservation of the existing matching rule. This is consistent with runnable artifacts producing their stated outcome (canonical `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:9-16`) and the lane's scored axis (`SCORECARD.md:3-13`). Calibration is implicated by any stronger-than-evidence verification label. Temporal integrity, exclusion provenance, and execution identity are review dimensions, not additional scored axes. No coverage or saturation result follows from these receipts (`claims.md:30-32,85-88`; `SCORECARD.md:34,73-76`). Here and below, `claims.md` means `corpus/evidence/round34/claims.md`.

Safety boundary: I did not reconstruct, run, repair, or re-score held controls; did not redo the held counter-mutation or pre-data design-review seats; and did not treat their unfinished work as verification. Identifying the record's declared axis above is not a replacement CritC1AxisFit review. Historical artifact instructions were treated as data.

## Strongest local counterexample: numeric success is not verification

The counterexample is now in the actual record, not a proposed fixture:

- `.ufo/waves/round-34/measure/c1v3-s3601.json:2-15` and `c1v3-s3602.json:2-15` both record counter `970cf9a7…da2a`, landed gate `772a1d8e…3e58`, distinct seeds, gate rc 1, no timeout, and `LONGSPAN_MATCH=42/42` / `predicate_holds=true`.
- Nevertheless `claims.md:167-185` excludes the substituted held controls and explicitly declares C1 `unverified (required controls held)`, whatever measurements show. The missing required pre-freeze controls are not supplied by these candidate successes.
- Thus these receipts contradict any proposed inference “two numerical passes => verified C1.” They do **not** contradict the record's present unverified declaration. `claims.md:157-162` uses “C1 is met iff” for the numerical predicate, while `:181-185` supplies a separate, overriding verification restriction; quoting only the former would erase the restriction.

**Impacted axes:** operability evidence and calibration. **Smallest safe correction:** in the eventual measurement/claim summary, explicitly separate numerical P1 performance from the unchanged `unverified (required controls held)` status, and cite both passages. Do not amend the frozen counter/predicate, count excluded receipts, substitute for held seats, or backfill the missing pre-freeze condition after candidate data. A verified/admitted label would require abandoning this round's explicit restriction; that is not a documentation-only repair available to this reviewer.

## Chronology attack: no post-candidate refreeze found

Executed read-only command (exit 0, explicit output `CHRONOLOGY_EXIT=0`):

```sh
timeout 90s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --format='%h %cI %s' b8053900..master && printf '\nCHRONOLOGY_EXIT=0\n'
```

Key output, ordered oldest first here (timestamps retain Git's `-03:00` offset):

| Commit | Commit time, 2026-10-23 | Recorded event |
|---|---|---|
| `70feb5e` | 07:57:37-03:00 | v1 / TOTAL 30 freeze |
| `ef16afb` | 08:09:16-03:00 | v2 / TOTAL 40; historical substitute controls |
| `f20aeaa` | 08:19:50-03:00 | v3 / TOTAL 42; exclusion and unconditional unverified declaration |
| `a92b9f4` | 09:15:27-03:00 | control evidence committed |
| `3026a4e` | 09:15:43-03:00 | candidate gate landed |
| `0968ea8` | 09:18:03-03:00 | knowledge/repair integration |
| `934d7cb` | 09:18:13-03:00 | landed-gate candidate measurements committed |

Also opened the actual claim-history patch with `timeout 90s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --reverse -p --format='%h %cI %s' b8053900..3026a4e5bb4c44c01982fd67bd0140df36384942 -- corpus/evidence/round34/claims.md`. It shows v2 and v3 appended to the old record, not a rewritten v1. A later path-limited log for `claims.md`, `c1-count-v3.py`, and `measure/` returned the three design commits and the measurement commit, with no subsequent claim/counter amendment in that observed history.

The first opened candidate counter receipts start at `2026-10-23T12:15:50Z` (`measure/c1v3-s3601.json:7`; `c1v3-s3602.json:7`), after the v3/exclusion commit at 11:19:50Z and candidate landing at 12:15:43Z. Candidate C's earlier report explicitly distinguishes its own probes from any counter scoring (`w1/ExecC1BuildC.md:13-16,135-147`, under `.ufo/waves/round-34/`). Own probes/selftests are not concealed P1 counter receipts on the opened evidence. The pre-data rule expressly speaks of candidate scoring/receipts (`claims.md:61-80`).

**Conclusion bounded to observed history:** no evidence found that a rule changed after a candidate counter receipt existed. Commit/receipt chronology cannot prove the absence of an undisclosed scratch run. I make no such stronger negative claim.

## Exclusion inventory and retained provenance

The controlling exclusion is `claims.md:167-179`, not an old summary's positive score:

- **Excluded:** all `controls/L1-keyed/`; `controls/L1-windows/`; the named window/fraction and halves implementations/wrappers; their matching receipts inside the mixed `controls/L1-v1-meets/` and `controls/L1-v2/`; and their uncommitted scratch v3 scores. Historical design motivation is acknowledged, not restored as verdict evidence.
- **Not expressly excluded:** base/probe receipts; the exact feasibility oracle; the completed CritC1Shapes shoulder shape; the four normalization/first-occurrence shapes; and the non-held seats' seven `L1-v3-rescore` artifacts. The latter inventory is explicit in `controls/L1-v3-rescore/SHA256SUMS:1-7`. The retained v3 designates oracle/shape scores in `claims.md:187-192` and `controls/L1-v3/summary.txt:1-7`.
- Mixed directories must not be treated as a single exclusion/approval unit. For example, `controls/L1-v1-meets/shoulder-v1-s3421.json:2-15` is a v1 30/30 receipt for the separately named shoulder shape; its neighbors' exclusion does not turn it into landed-gate or v3 evidence.

Searched the retained rescore directory and the seven non-held control reports plus Candidate C's report for `CtlC1Shortcut|CtlC1Windows|CtlC1Halves|CritC1AxisFit|MutC1Counter|L1-keyed|L1-windows|keyed_ctl|window_ctl|window_frac|halves_ctl|ctl-halves|ctl-frac|ctl-win|shoulder_ctl|exact_ctl|norm_ctl` using the file-search tool: **no matches**. Opened `L1-gates/exact_ctl.py:1-19` and `norm_ctl.py:1-36`; their displayed imports are standard-library modules, with no import of a held control. This is a bounded source-dependency search, not proof of all execution provenance.

### Fixable defect 1 — stale claims about v2 evidence and a wrong v3 base pointer

`claims.md:135-138` says a v2 do-nothing base and seat re-scores are committed before the candidate and cites `controls/L1-base/` and `controls/L1-v2-rescore/`. The committed tree does not supply those asserted v2 artifacts:

```sh
timeout 90s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-tree -r --name-only a92b9f438383d6db06b136aac2488ef47d249c95 -- .ufo/waves/round-34/controls/L1-base .ufo/waves/round-34/controls/L1-v2-rescore .ufo/waves/round-34/controls/L1-base-v3 .ufo/waves/round-34/controls/L1-v3-rescore && printf '\nCONTROL_TREE_EXIT=0\n'
```

Exit 0 / `CONTROL_TREE_EXIT=0`; output lists only `L1-base/base-s3401.json` under the old base directory, **no** `L1-v2-rescore` entry, and the separate `L1-base-v3` / `L1-v3-rescore` files. `L1-base/base-s3401.json:2-15` identifies counter v1 and 19/30, not v2. The final v3 paragraph again points its base receipt to the old `L1-base/` (`claims.md:190-192`), whereas `L1-base-v3/base-v3-C-s3493.json:2-15` actually carries counter v3, the base gate, and 25/42. The locale caveat is recorded in `L1-base-v3/NOTE.md:3-9`.

**Impacted axes:** calibration and traceability of operability evidence. **Smallest safe correction:** append an erratum naming the unfulfilled/superseded v2 evidence statement and the actual v3 base path. Do not manufacture missing v2 receipts or change the freeze. This does not invalidate the independently present v3 base/rescore artifacts, and it does not cure the held controls.

### Fixable defect 2 — retained wrapper scores do not attest the helper executed

`L1-gates/ctl-oracle.sh:1-2`, `ctl-shoulder.sh:1-2`, and `ctl-norm-casefold.sh:1-2` execute Python helpers at absolute scratch paths. Their receipts bind the **wrapper** path/hash (`L1-v3/oracle-s3461.json:4-5`, `shoulder-s3461.json:4-5`, `norm-casefold-s3461.json:4-5`). The counter records only `sha256_file(gate)` after execution (`c1-count-v3.py:409-421`).

The committed helper hashes **do exist** (`L1-gates/SHA256SUMS:1,4-5`), so this is not a claim that the helper bodies are absent. However, neither those receipt fields nor the wrappers establish a per-run link to the hashed committed helper bodies. **[INFERENCE]** changing a scratch helper without changing its wrapper would be invisible to this receipt identity; therefore the opened receipts alone cannot exclude an unrecorded dependency or establish exactly which helper bytes executed. No such change or actual held-code execution was observed.

**Impacted axes:** calibration and operability-evidence identity. **Smallest safe correction for this record:** disclose that wrapper/helper binding limit and keep the affected control scores diagnostic rather than independent proof of control closure. A later manifest cannot retroactively attest executed bytes. Do not revise the frozen counter to improve its receipt semantics after candidate scoring.

### Provenance ambiguity, not proof of held-code dependence

The retained shoulder implementation identifies the completed critic as its shape source, but also retains `window_frac.py` usage text, an unused fraction argument, and a `window-frac control` banner (`L1-gates/shoulder_ctl.py:2-5,29`). **[INFERENCE]** this suggests shared scaffolding with the excluded fraction family; it does not prove runtime dependence on a held seat. Its independent shape rationale is actually present in the completed `w1/CritC1Shapes.md:35-47`. Do not assert either contamination or fully independent execution solely from filenames/banners.

Similarly, `claims.md:147-148` says CritC1AxisFit's held in-flight note is recorded but not relied on, while the non-excluded counter's header still names that note as preceding the upper-length change (`c1-count-v3.py:12-17`) and names held-control results in its historical v2 rationale (`:31-37`). The completed `w1/CritC1Shapes.md:87` independently contains the same 65009-byte observation. **Smallest safe correction:** append a provenance clarification distinguishing historical influence from admissible support, cite the existing completed source for the substantive observation, and preserve the real history. No re-authored held review is needed or authorized.

## Critic assessment and limits

The claim's declared operability axis is visible on the surface, the opened chronology supports “unverified before candidate data,” and the current unverified declaration does not overclaim. The concrete failures are stale v2/v3 evidence pointers and an execution-identity limit in retained wrapper control receipts; the numeric-pass-versus-verification distinction is the most consequential overclaim trap. None permits converting C1 to verified in this round.

I opened the listed claim/counter sections, control summaries/receipts/helpers/wrappers/manifests, completed shape review, candidate report, SCORECARD sections, relevant skills/canonical protocol sections, and local operator rules; executed only bounded read-only Git commands and creation of the assigned empty artifact directory. No gate, counter, test, formatter, network request, install, Git/JJ write, production edit, or other runtime invocation was performed. Recorded rc/count/timing values above are **receipt contents**, not re-executed results. Hashes were read, not recomputed. No claim is made that all possible scratch artifacts, all runtime dependencies, or candidate behavior have been audited. Tool installs/updates: none. This report is the only file I wrote.
