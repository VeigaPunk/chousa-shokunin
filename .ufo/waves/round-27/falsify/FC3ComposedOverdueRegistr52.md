# FC3ComposedOverdueRegistr52 — falsify `composed-overdue-registry`

Target: `corpus/evidence/round27-regressions.py` line 199 (control name `composed-overdue-registry`), C3.
Landed revision: `dd72641e574679c4f7882dd43de072b4c8892d6f` (`master`), gate sha256
`ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` (matches assigned gate sha).
Sandbox: `/tmp/chousa-r27-falsify-FC3ComposedOverdueRegistr52` (`git archive` of the revision).
No installs. No network, host files, /proc inspection, strace, mounts, or debugger. Full `--selftest`
and the whole regression script were not run (L1 owns them); only single gate invocations and
surgical mutants of the sandbox copy.

## Verdict

**FALSIFIED** as a C3 repair-discriminating control.

The control's declared expectation is contract-derived and correct (part 1 HOLDS), but the control
has **zero discriminating power over every round-27 C3 repair**, and it is **vacuous on the
registry-application half of the composition it is named for**. Its required output is reproduced
byte-for-byte by the pre-repair gate and by mutants that revert each C3 fix or remove the registry
screen entirely. Its only live sensitivity is the C2 calendar arithmetic (90d → 2026-04-02) and the
absence of spurious source findings.

## Part 1 — Is the expectation derived from the declared contract, independent of gate code?

HOLDS. The fixture is `source: S001`, `verified-at: 2026-01-02 …`, `recheck: 90d`, registry
`| S001 | mined | corpus/knowledge/entry.md |`, `--as-of 2026-10-21`. Contract (round27-claims C3 +
`SKILL.md:474-483`, r26-claims "composition clarification"): both opt-in screens apply to one
verdict; decoded cadence adds calendar days; equality is current, strictly later is overdue; a mined
row whose used-by names the entry yields no source finding; one `RESEARCH_GATE:` verdict.

Independently recomputed:
`python3 -c "from datetime import date,timedelta; print(date(2026,1,2)+timedelta(days=90))"` →
`2026-04-02`; `2026-10-21 > 2026-04-02` → overdue. The expected literals
`due=2026-04-02 freshness=overdue`, `META_RECHECK_OVERDUE`, 0 `META_SOURCE_` findings and one
verdict all follow from that contract. Only the output-field spelling (`due=`, `freshness=`,
`RESEARCH_GATE: `) is gate-interface syntax, and that syntax is itself declared in
`SKILL.md:474-476`. No expectation bug found.

## Part 2 — Mutation evidence: does reverting the targeted fix make the control fail?

No. Baseline control facets are `RC=1`, `DUE_LINE=1`, `OVERDUE_LINE=1`, `META_SOURCE_COUNT=0`,
`VERDICT_COUNT=1`. Every one of the following mutants leaves all five identical (control stays
green). Mutants are copies of the landed gate only.

| mutant | production change | control facets | control result |
|---|---|---|---|
| `m_header` | landed `metadata_registry_load` replaced with 64eec5d body (no header-cell reset, no separator-width check) | RC=1, due/overdue=1, source=0, verdict=1 | **green** |
| `m_token` | landed `metadata_registry_check_source` replaced with 64eec5d rescan loop | same | **green** |
| `m_deny` | registry/entry fd-canonical denylist checks reverted to `ptr_file_part`-only semantics (64eec5d) | same | **green** |
| `m_nocheck` | `metadata_registry_check_source` call removed from `verify_metadata` (`:` in its place) | same | **green** |
| `m_ignore_registry` | both `metadata_registry_load` and the check call removed — `--registry` silently ignored | same | **green** |
| `m_date_offbyone` | `amount=$((10#$digits - 1))` in `metadata_add_days` | `DUE_LINE=0`, RC=1 | fails (intended) |

Key transcript:

```
$ GATE=.../work/base-gate.sh ./compose.sh          # base gate sha c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6
... due=2026-04-02 freshness=overdue ... RC=1 META_SOURCE_COUNT=0 VERDICT_COUNT=1 DUE_LINE=1 OVERDUE_LINE=1
$ GATE=.../work/mutants/m_ignore_registry.sh ./compose.sh
... RC=1 META_SOURCE_COUNT=0 VERDICT_COUNT=1 DUE_LINE=1 OVERDUE_LINE=1
$ GATE=.../work/mutants/m_date_offbyone.sh ./compose.sh
... RC=1 ... DUE_LINE=0 OVERDUE_LINE=1
```

The base gate blob is byte-identical at both `0e9784bd52eca456b24d0bc40921480a47f91a2b` and
`64eec5d41c7cf7f17f5ce1e968e28b3769952596` (`sha256 c2c813f1…`), i.e. the revision where r26 measured
FAIL3/187. The control was already green where C3 was broken: its fixture exercises none of the
three reported C3 failures (clean named header, single standalone `S001`, colon-free non-denylisted
registry path). Its green at `dd72641e` is inherited baseline, not after-repair evidence.

Counter-mutant check (the C3 fixes are real and other controls do discriminate):

```
header-break-blank fixture: target rc=2 "metadata registry has no table…" | m_header rc=1 (no message)
"see S001S003 and S001":   target rc=1, 1 finding (overdue only)     | m_token rc=1, 2 findings incl ROW_MISSING S003
colon-denied-component:    target rc=2 "metadata registry refused: denylist" | m_deny rc=1 (registry read)
```

Each sibling control would record a mismatch for the intended reason under the corresponding
mutant. `composed-overdue-registry` is the outlier.

### Vacuity, sharpest form

`composed-overdue-registry` requires **zero** `META_SOURCE_` findings, so any under-checking is
invisible to it. With `m_ignore_registry` (the exact composition violation the r26/r27 contract
forbids — "Neither flag is silently ignored"), a *headerless* registry that must exit 2 instead
yields `RESEARCH_GATE: DRIFT … RC=1`; the control still sees all four required facets and stays
green. The paired control `composed-current-queued` (queued row → positive `META_SOURCE_NOT_MINED`)
uses the same shared fixture and **does** fail under both `m_ignore_registry` and `m_nocheck`
(expects rc1/NOT_MINED=1, gets rc0/CLEAN/NOT_MINED=0). So the control file contains one
discriminating composed control and one non-discriminating one; only the positive-finding shape
discriminates.

## Part 3 — Nearby same-class input where the gate is wrong or the control is vacuous

**(a) Control vacuity (proved above).** Disabling or ignoring `--registry` leaves it green. This is
a same-class input gap: the suite has no overdue + *source-defect* composition at all.

```
$ grep -n "USEDBY\|ROW_MISSING" corpus/evidence/round27-regressions.py   → no matches
```

Among all 58 persisted controls (C1 6, C2 21, C3 31), no control asserts a true
`META_SOURCE_USEDBY_MISSING` or `META_SOURCE_ROW_MISSING`. The C3 claim "exact used-by rules remain"
rests on the gate's own `--selftest` (`metadata-registry-used-by-path`, gate line 6236), not on the
"independent" suite. I probed the gate directly and it composes those cases correctly
(`overdue+queued`, `overdue+missing`, `overdue+usedby-mismatch` each emit both findings, findings=2,
drift=2, one verdict; `as-of == due` → current/clean; `due+1` → overdue). So this is a persisted-
control coverage gap, not a gate defect.

**(b) Gate divergence from the declared used-by derivation (inherited, medium confidence).** The
r26 spec-v1 correction says used-by is "an exact repo-relative entry path, derived relative to
`--root` (only leading `./` is normalized)". `verify_metadata` derives `entry_path` from
`fdcanon` (the canonical opened inode), so a lexical entry path through a symlink is rejected:

```
# entry invoked as <root>/corpus/knowledge/entry.md where <root>/corpus/knowledge -> ../real/knowledge
| S001 | mined | corpus/knowledge/entry.md |   → FINDING META_SOURCE_USEDBY_MISSING … RC=1
| S001 | mined | real/knowledge/entry.md     |   → no source finding … RC=1 (overdue only)
# entry invoked as <root>/link.md -> corpus/knowledge/entry.md
| S001 | mined | link.md                     |   → FINDING META_SOURCE_USEDBY_MISSING … RC=1
| S001 | mined | corpus/knowledge/entry.md   |   → no source finding … RC=1
```

The gate demands the canonical target in both directions, while the documented rule derives the
path relative to `--root` from the entry as rooted. The base gate (`c2c813f1…`) emits the same
`USEDBY_MISSING`, so this is **inherited**, not introduced by round 27; the fd-canonical binding is
also the gate's deliberate security posture elsewhere. Report as a contract/implementation wording
divergence to resolve, not as a r27 regression. Confidence: medium (INFERENCE about the lexical vs
canonical reading of "derived relative to --root").

## Limits

- Did not run `bash tools/research-gate.sh --selftest` or `python3 corpus/evidence/round27-regressions.py`
  in full (bounds; L1 owns them). Mutants were judged only against the exact control fixture and
  the three sibling fixtures named above, re-implemented from the script's own code.
- Base comparison is `64eec5d` (gate byte-identical to the r26-failing `0e9784b`), not a re-run of
  the r26 receipt.
- Symlink counterexample is synthetic and inherited from base; no lane production file was touched.
- No numeric resource/alloc claims; no claim about the other 57 controls beyond the three sibling
  fixtures exercised.

## Author-lane advice

1. Make `composed-overdue-registry` a positive composition control: use a queued/missing/used-by-
   mismatch row while overdue and assert both `META_SOURCE_*` and `META_RECHECK_OVERDUE`, two
   findings, `drift=2`, one verdict. If the intent is only no-false-positive, rename it (e.g.
   `composed-overdue-clean-registry`) and keep a positive companion.
2. Add independent positive controls for `META_SOURCE_ROW_MISSING` and
   `META_SOURCE_USEDBY_MISSING`; currently the persisted suite asserts neither, and the used-by rule
   is only exercised by the gate's own selftest.
3. Resolve the used-by derivation wording: either compare against both the rooted lexical path and
   the canonical target, or amend the contract to say the canonical target relative to `--root` is
   required. Do not leave "exact repo-relative path" asserting a lexical rule the code does not
   implement.
