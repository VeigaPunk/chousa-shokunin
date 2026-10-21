# CriticFrontier — round27 admission-claim attack

Seat `ChousaR27.CriticFrontier` (critic, leaf). Author-lane advice, not outside admission.
Base observed: `64eec5d41c7cf7f17f5ce1e968e28b3769952596`. Static reads only: no gate,
selftest, regression, differential or census execution; no network; no installs.

Assigned item: attack the admission claims. Fixes must not retroactively admit r26, and
the sourced own-work quote must be opened this round.
Proposal under attack (working tree at 11:37–11:38 -0300): `corpus/SOURCES.md` S040–S042 and the
Round27 search-log entry, `corpus/lessons/round-27.md`, `corpus/evidence/round27-{claims.md,
regressions.py,mechanisms.py,census-before.json,mechanisms-before.json}`, and
`.ufo/waves/round-27/patches/ExecUsage.patch`.

Holds that survived attack: r26 is fixed as `admitted:false, verdict:"rejected-harmed"` in the
fleet `MANIFEST.json` rounds[414]. The lane-side texts that say "not admitted" remain untouched:
SCORECARD.md:1446–1500, SKILL.md:500–516, README "admission correction", and the withdrawal
addenda in `recheck-due-r26.md:46` and `registry-link-r26.md:43`. S040–S042 pin base
`64eec5d4`, a commit that exists only after r26 landed. This is a valid round discriminator.
The S041 and S042 Gate quotes are verbatim at `FDateHugeCadence.md:42–44` and
`FRegistryHeaderless.md:45`. Lesson lines 61–74 already reject "repair retroactively admits
round26" and keep S035/S036 out of grounding. The r26 receipts are committed: `git ls-files`
lists all 27 FDate/FRegistry/FNoTrade reports.

## Counterexamples

### CF1 — C1 counting control cannot reach 0 mismatches honestly (blocking)
- Evidence: `round27-regressions.py:70` extracts only the text matching
  `^  metadata_asof_usage_case\(\).*?^  }\n`. `ExecUsage.patch` makes that function call
  `metadata_asof_usage_accepts`, which it defines as a separate sibling. The extracted script
  therefore lacks the predicate, so the call becomes `command not found`. The `if` is false and
  every scenario is rejected. [INFERENCE from static reading; not run.]
- Effect: `correct-usage-with-help` and `nonrecord-mention-is-not-verdict` mismatch with
  failures=1 instead of 0. The four reject controls "pass" because of a missing function, not
  for their stated reason. That violates QUALITY17 ("fails for that reason, not a parse error").
  Editing the script after a baseline run would change the pre-registered counting command.
- Axes: operability (C1 after-claim), calibration of the measurement.
- Smallest correction: before any baseline run, either inline the predicate in
  `metadata_asof_usage_case`, or make the extractor also capture every
  `metadata_asof_usage_*` helper it calls. In either case, exit 2 (setup) when a helper the
  extract calls is absent. Record the change as a pre-measurement amendment.
  Separately, the patch's selftest controls cover a CLEAN verdict only. Claim C1 says
  "actual CLEAN/DRIFT verdict fails", so add a DRIFT control.

### CF2 — the "baseline skip via committed r26 receipt" covers neither exact skipped input
- Evidence: the claims (lines 22–23) require running the script unchanged on a base archive
  without rerunning the crash, but the script has no skip option. At base, two cases reach the
  crashing `${digits##+(0)}` strip: `leading-128k-zeros` (131,072 zeros + `90d`) and
  `allzero-128k` (131,072 zeros + `d`). The claims name a single "baseline item".
  `FDateHugeCadence.md:46–53` observed the crash for `0…090d` cadences at 128,000 and
  192,000 zeros, but never at 131,072 zeros and never for an all-zero cadence.
- Effect: citing the receipt as the baseline for `allzero-128k` (or the exact 131,072 shape)
  is false provenance. Running the script unchanged on base would rerun the crash, which the
  claims forbid.
- Axes: freshness (C2 before/after), calibration.
- Smallest correction: add `--baseline-skip NAME[,NAME]`. Emit the skipped names in the JSON
  summary with the receipt pointer `FDateHugeCadence.md:53`, and exclude them from the
  before-mismatch count. Label `leading-128k-zeros` as "[INFERENCE] same mechanism, nearest
  observed shapes 128,000/192,000 zeros", and `allzero-128k` as "baseline unmeasured", not
  "baseline failing". `baseline-identity.json`'s `unsafe_or_reported_failures_rerun:false`
  covers only the mechanism probe and must not be reused for a regression baseline.

### CF3 — tier-A own-work rows teach repair rules their sources mark as inference
- Evidence: the source reports describe themselves as advisory: "Author-lane advice only; not
  an outside judge" (`FRegistryRegistryDeny.md:3`; `FDateHugeCadence.md:3`). S040's teaching
  "Count verdict records by their record grammar…" rests on `FNoTrade.md:129`, which the
  report labels `[INFERENCE]`. The S041 and S042 teachings ("Validate ASCII input in the same
  representation…", "Reset parser state at boundaries, retain occurrence identity…") are
  prescriptions. The reports state failures.
- Effect: the scope cells say "reported…", which is correct, but the `teaches` cells turn
  inferences into tier-A learning (QUALITY3/7). If any r27 note later cites S040–S042 as
  support that the repairs work, that collapses "source states the diagnosis" into "the fix is
  correct" (QUALITY8).
- Axes: calibration.
- Smallest correction: add an append-only note in SOURCES.md saying the S040–S042 teachings
  are lane inferences drawn from reported diagnoses. Repair correctness rests only on the r27
  regression/selftest receipts and outside closure, never on S040–S042.

### CF4 — "opened this round" is not provable from `opened`; the S040 quote is not verbatim; S035/S036 anchors drift
- Evidence: `opened` is 2026-10-21 for S034–S039 (r26) and S040–S042 alike. The census only
  rejects future dates (E08, `scripts/sources-census.sh:660–662`). The only proof that a row
  was opened this round is therefore the base pin plus a verbatim Gate quote.
  The lesson's S040 quote drops the source's backticks and renders the pipe as a literal
  `\u007c`. The source reads `` `die_usage` (`:390`) … `usage`, … `CLEAN|DRIFT` ``
  (`FNoTrade.md:125–126`). This is the R25-M9 failure class (a paraphrased Gate quote).
  The lesson also does not name the seats that opened the sources, which r26's lesson did.
  S035/S036 anchors are unpinned ("tools/research-gate.sh metadata date helpers",
  "metadata_registry_load and metadata_registry_check_source"). Once r27 lands, they silently
  resolve to the repaired code, so the withdrawn r26 rows appear to ground working code.
- Axes: calibration, freshness.
- Smallest correction:
  - Replace the S040 quote with a pipe-free verbatim span: `FNoTrade.md:127–128`, "So the
    predicate is unsatisfiable for any usage exit, and the failure is deterministic rather
    than flaky."
  - In the Gate, name the seats that opened the sources (ScribeSourceUsage/Dates/Registry, or
    L1 itself).
  - Append a SOURCES.md note pinning the S035/S036 implementation anchors to measured
    `0e9784bd` (gate SHA-256 `c2c813f1…`). Make no cell edits.

### CF5 — the initial source census was recorded after the registry changed
- Evidence: `round27-census-before.json` has mtime 11:37:43, 30 s after `SOURCES.md` gained
  S040–S042 at 11:37:13. It has no `observed_at` and no tree or blob identity. Its counts come
  from the static ScoutSourceCensus parse. Its `exit:0`/`ok` output cannot be attributed to
  the pre-edit tree, while the round template requires the census to run "at round start".
- Axes: calibration (frontier conformance).
- Smallest correction: cite `round26-census-end.json` as the r27 initial census. It was
  observed at 2026-10-21T14:20:39Z with 39 rows (A33/B1/C5; mined16/queued19/rejected4), and
  `SOURCES.md` is unchanged from `0e9784b` to `64eec5d` (base blob `5e961aff`). Alternatively,
  rerun validate on an isolated fleet-shaped root that holds blob `5e961aff`, recording time
  and blob. Expected final census: 42 rows, A36/B1/C5, mined19/queued19/rejected4.
  ScoutSourceCensus's 40-row projection is stale.

### CF6 — spot-check intake omits routed debts, so a narrow repair can read as closing the C2/C3 modes
- Evidence: `rounds[414].routed_defects` lists "incomplete31 falsify assignments", registry
  oracle gaps, parent-root/receipt/source-span pairing debt and round12 Receipt identity L0.
  The S025 outside spot-check also routed its used-by omission as debt. None of these has a
  row in the `round-27.md` intake table (QUALITY14 requires one row per debt).
  `falsify-final-reconciliation.json` shows that the 31 seats that never reported include
  C2/C3 surfaces: FDateZeroCadence, FDateCentury1900, FDateMinimum, FDateZeroPadded,
  FDateEquality, FDateInvalidDue, FDateEvent, FDateOtherModes, FDateComposedFlags,
  FRegistryReorderColumns, FRegistryMultipleIds, FRegistryQueued, FMutateC3Killed,
  FSeparability, plus the FHeader×8, FMemory×4 and FReader×4 seats and FRecordAudit.
- Effect: controls written by the planner partly overlap these shapes but do not replace
  independent falsification. No QUALITY17 mutation kill is planned for the new C2/C3 controls.
  An r27 "after" therefore supports only "the six named counterexamples no longer reproduce
  and the new controls pass". It does not support "the C2/C3 modes are verified", and it gives
  no basis for revising r26.
- Axes: freshness, calibration (admission scope).
- Smallest correction:
  - Add carried rows for each omitted routed item.
  - Keep SKILL.md:500–509 and the r26 withdrawal addenda verbatim. Record r27 status only as
    append-only addenda that cite the r27 measured revision.
  - Do not add S040–S042 to the r26 notes' `source:` headers, and do not change their
    `verified-at:`.
  - Add no repertoire or `capabilities_added` entry.
  - In SCORECARD r27, use 39 rows / 32 knowledge files as the expansion baseline. Do not
    restate r26's frozen-control gains (0/29→29/29, 0/6→6/6, 0/5→5/5) as r27 deltas.

## Unrun checks (L1, after integration)
- `python3 corpus/evidence/round27-regressions.py --gate tools/research-gate.sh` on the final
  tree, and on a base archive with CF2 skips declared.
- `bash tools/research-gate.sh --selftest`: the 187 original identities plus the new controls.
- `scripts/sources-census.sh validate --root <fleet> chousa` at the end (expect 42 rows).
- Static `git diff 64eec5d --` over SKILL.md, SCORECARD.md:1446–1500,
  `corpus/knowledge/*-r26.md` and `corpus/README.md`: additions only, no deletions.

Tool installs/updates: none.
