# Draft12 — inherited round64 disposition

## Scope and axes

Read-only provenance review; axes: freeze fidelity, execution-evidence fidelity, and closure completeness. No claim is admitted by this report. Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Frozen reference: `bf40d99bda9eefdad3ed6276da077cfb24ba82f1`. Observed history tip: `34cbd847fa374ce7baa61147209b5772212a3d64` (a historical observation, not a lock against concurrent L1 changes).

## Provenance and behavior

| Commit | Observed surfaces | Disposition |
|---|---|---|
| `759c6cbef4cf9cdc81b68afc709f3b82ecd1a9d9` | round63 verifier spot-check | Base named by frozen claims. |
| `92a084175f9534296527b77a2b7fe38560b96b18` | 21 files, 2621 insertions: claims, seven pinned instruments, audit TSV, baseline/control receipts | Actual instrument-and-claims freeze commit. These are inherited frozen inputs, not unfinished code to repair in place. |
| `bf40d99bda9eefdad3ed6276da077cfb24ba82f1` | audit TSV R5 changed; `audit-r64-postfreeze.txt` added | Assignment's frozen reference, but the commit describes its own audit change as post-freeze. Claims/instruments were not changed by this commit. |
| `34cbd847fa374ce7baa61147209b5772212a3d64` | 12 files, 2596 insertions/5 deletions: G02 production repair, separate candidate, supplement, erratum, sourced entry, registry/index/lesson and wave metadata | Post-freeze implementation and documentation, not part of the frozen instruments. Presence is not a passing measurement. |

### Frozen leftovers: preserve, disclose, do not silently repair

1. **C1 frozen fixture failure.** Existing `controls/c1v3-before-full.txt:38-44` records E12/E13/E14 failing and `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`. The receipt is inherited, not executed by Draft12; claims records its original exit as 1. Static comparison shows frozen E12 and E13 independently call `tag()` for the created filename and the README target. Their supposed benign row can therefore point to a different, nonexistent file. This is a frozen-instrument defect, not evidence that a conforming checker should accept phantom links. Full frozen C1 success cannot be honestly substituted with a supplemental pass.
2. **C1 supplement is distinct.** `c1-battery-supplement.py` differs only by storing one shared `t = tag()` per E12/E13 fixture and reusing it in both names. This is a post-freeze repair, not permission to overwrite `c1-battery-v3.py`, its expectations, or its kill rule.
3. **C3 frozen relocation expectation is wrong by inspection.** `c3-count.py:86` creates `.../lane-copy/corpus/evidence/round65`, the same component depth as the original instrument folder; line 91 expects `mirror.parent / needs[0]`. Instruments derive their root using `HERE.parents[2]`, which names `lane-copy`, not `round65.parent` (`evidence`). This is a static arithmetic finding, not a newly executed C3 failure. The inherited erratum explicitly requires any resulting frozen FAIL be reported.
4. **C3 enumeration is narrower than “every.”** `c2-mutrun.py:49-53` also derives LANE from `__file__` and asserts `corpus/SOURCES.md`, but frozen C3 lists only the v3 battery, receipt runner and counter itself. Preserve the frozen list and disclose the mismatch; widening the list after data would change the claim.
5. **Frozen receipts remain baselines, not after-verdicts.** `controls/c2-mutrun-v1.txt` records `AUDIT_MUTANTS_KILLED=6/12`, survivors A05/A06/A07/A08/A10/A11; claims records original exit 1. `controls/c3-before.txt` records a raw CLEAN failure with `BATTERY=PARTIAL`, `raw-exit=0`, then `SHIFT_MUTANT_UNNAMED=1/1`, `shift-exit=0`. Do not upgrade the PARTIAL exit 0 into full battery success.

### Unfinished closure and nonfrozen work

- **Production versus candidate:** commit 34cbd84 modifies `tools/lane-preflight.py`; `controls/ref-preflight-v3.py` remains a separately committed candidate, NOT production. Erratum item 2 says the inherited candidate matches `p.stem` rather than the full `.md` name and has a narrower mirror regex. The observed production diff instead uses `p.name`, recursive inventory, normalization, phantom checks, UTF-8-safe reporting and regular-file `--work` usage exit 2. This describes landed source changes only, not proven conformance or a green C1.
- **C1 after closure remains evidentiary work:** three frozen landed runs, null control results, v2 cross-check twice and full preflight must be reported according to the unchanged kill rule. The frozen E12/E13 mismatch must remain an honest failure; the supplement cannot admit C1.
- **C2 is implemented but not established by this seat:** `tools/claims-audit-v2.py`, generator and runner are frozen. Its 12/12 mutation result, expanded selftest and fault-leg outcomes require actual receipts. Draft12 ran none of them and does not infer their outcomes from code or the target text.
- **C3 has a sourced entry, not a demonstrated counter pass:** S150 is installed Python source rather than the proposed docs; S152 is the frozen counter source rather than successful probe output. These substitutions are explicitly disclosed by the lesson and erratum. S153 is rejected as a docstring-only correctness source. The entry lacks a `## Gate` heading; lesson `## Gate` holds the row-level access/admit/reject material and says outside non-author spot-check is pending. Frozen claims requires the entry admitted with Gate rows or a sourced-leg unprovable outcome; outside closure must resolve this, not infer it from lane-authored prose.
- **After receipts were not in the inspected controls inventory:** `c1v3-landed-runs.txt`, `c1v2-on-v3tool.txt`, `audit-v2-selftest.txt`, `c2-mutrun-v2.txt`, `c3-after.txt`, `preflight-full-run-r64.txt`. This is a point-in-time inventory observation, not an assertion that concurrent seats cannot produce independent evidence.
- **Closure docs are not finished in inherited commit 34cbd84:** its touched list excludes LOG.md, SCORECARD.md, QUALITY.md and SKILL.md. Targeted searches found no round64 entry in LOG.md or SKILL.md, and SCORECARD.md still has `## Planned — round 64 (not started)` at line 3022. Lesson line 41 explicitly defers all three verdicts to post-wave SCORECARD/report. No criterion, capability, numeric score or outside closure is established here.
- **Other inherited leftovers are deliberately routed:** lesson says assimilation none/package adoption closed, quarantine/collision checks to be re-derived read-only, and considerthese is one lesson pointer rather than a claim. Round63 sibling G04/G05 receipt exists, but prior zero-wave floor is not retroactively met by later dispatch metadata.

## Audit conflict retained verbatim

Observed bf40d99 R5 replacement:

```text
-R5\tgit-first-commit\tFrozen before any after-measurement\tcorpus/evidence/round64/c1-battery-v3.py,tools/claims-audit-v2.py,corpus/evidence/round64/c2-mutrun.py,corpus/evidence/round64/c3-count.py,corpus/evidence/round64/run-receipts-v3.py,corpus/evidence/round64/gen-audit-mutants.py\t\tfreeze: instruments land in the pre-freeze commit, the claims file in the freeze commit
+R5\tgit-first-commit\tFrozen before any after-measurement\tcorpus/evidence/round63/claims-a2.md,tools/claims-audit.py\t\tfreeze: the round-63 instruments predate this claims file; R5 target corrected after the directory commit landed instruments and claims in one freeze commit (lesson mistake row)
```

The audit receipt says exactly `FLAGGED=0/5 AUDIT=PASS`; it applies to the re-pointed TSV, not the original six round64 instrument targets. It is inherited execution text, not Draft12's execution. Canonical judge retains disposition authority.

Assignment path conflict, verbatim: `Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft12/ (report.md)` versus `Report: write your scoped findings to .ufo/waves/round-64/w1/Draft12.md`. Both explicitly named output paths are supplied: this full report and the trailer-path index.

## Executed static commands and outcomes

All shell commands used cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`; no fixture driver, counter, checker, test, runtime, network fetch or installation was invoked.

1. `git --no-pager log -18 --format='%H %s'` — exit 0; observed tip and freeze lineage listed above.
2. `git --no-pager show --stat --oneline 92a084175f9534296527b77a2b7fe38560b96b18 bf40d99bda9eefdad3ed6276da077cfb24ba82f1 34cbd847fa374ce7baa61147209b5772212a3d64` — exit 0; respective totals 21 files/2621 insertions, 2 files/2 insertions/1 deletion, 12 files/2596 insertions/5 deletions.
3. `git --no-pager show 34cbd847fa374ce7baa61147209b5772212a3d64 -- tools/lane-preflight.py corpus/README.md corpus/SOURCES.md` — exit 0; production G02 and S150–S153/index changes inspected.
4. `git --no-pager show bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/audit/audit-r64.tsv corpus/evidence/round64/audit/audit-r64-postfreeze.txt` — exit 0; R5 replacement and receipt inspected.
5. `git --no-pager diff --name-status bf40d99bda9eefdad3ed6276da077cfb24ba82f1 -- corpus/evidence/round64/claims.md corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/gen-audit-mutants.py corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/c3-count.py corpus/evidence/round64/run-receipts-v3.py corpus/evidence/round64/controls/root-shift-mutant.py tools/claims-audit-v2.py` — exit 0, no output: no differences against frozen reference for those paths at inspection.
6. `git --no-pager diff --no-index -- corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/c1-battery-supplement.py` — exit 1 (expected diff-found status); only shared-nonce E12/E13 changes shown.
7. `sha256sum corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/gen-audit-mutants.py corpus/evidence/round64/c2-mutrun.py corpus/evidence/round64/c3-count.py corpus/evidence/round64/run-receipts-v3.py corpus/evidence/round64/controls/root-shift-mutant.py tools/claims-audit-v2.py` — exit 0; outputs below match frozen prefixes.
8. `git --version` — exit 0, `git version 2.56.0`; existing host binary, read-only provenance reason, no install/update channel used.

```text
4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2  corpus/evidence/round64/c1-battery-v3.py
6e1055b28d315e32a3d43ee0866f9c32b78470899826f1d29c8c3707610a4191  corpus/evidence/round64/gen-audit-mutants.py
0045787ee9de39749e1dd06739259cd5f0a494865c921edbed91cfd86249a8c9  corpus/evidence/round64/c2-mutrun.py
465a8c5efbb870f73c7c6306c813c4fe35f4ccaf5a996a56ab71d4da5feec682  corpus/evidence/round64/c3-count.py
0f3cfae75f711f17251174a2e123321040c91394497bafe4a64c9148d7c3abd7  corpus/evidence/round64/run-receipts-v3.py
f0f9b26083ff62c35b9d54fe5bf7733f233c496368a5a62a3da02dbbb3f89175  corpus/evidence/round64/controls/root-shift-mutant.py
db0e28dd4c0332591b8898feb727f23a0e80b6e2ad29cbf0a6237d35a4d0b88d  tools/claims-audit-v2.py
```

Read-tool evidence: host RULES first, then frozen claims; godspeed/self-evaluation skills; round64 erratum, lesson, sourced entry, controls inventory and inherited baseline receipts; counter lines 28–39/76–103 and c2-mutrun lines 44–56. Specialized grep inspected LOG/SCORECARD/SKILL round64 references. No shell exit applies to reader calls. Scratch reader returned `Path '/fast/scratch/hyaku/chousa-r64/Draft12/' not found`; no scratch or clone was created, so nothing required deletion.

## Gates, touched surfaces, limits

Authorization honored: no pacman, PATH writes, service restart, git/jj mutation, sibling edit, commit, push, dispatch, production edit or frozen-input modification. Only Draft12 report artifacts written. No new behavioral checks were authorized by this review item; none run. Static findings and inherited receipts remain advisory and do not supply outside non-author closure. L1 alone integrates production and canonical judge decides conflicts.

Self-evaluation (1–5): accuracy 4 (point-in-time observations, no reruns); completeness 4 (inherited lineage covered, live after-work deliberately excluded); clarity 4 (frozen and unfinished separated); actionability 4 (exact missing closure surfaces identified, no execution authority assumed); conciseness 4 (command ledger retained for audit). Average 4.0. Highest-impact handoff: retain frozen failures, keep supplement/candidate provenance separate, and bind final outcomes to authentic wave/closure receipts.

Artifacts: `.ufo/waves/round-64/w1/Draft12/report.md`; `.ufo/waves/round-64/w1/Draft12.md`.
