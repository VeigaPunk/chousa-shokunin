# Round 29 — CriticNoHarm

## Verdict and counterexample

**HOLDS — scoped baseline-preservation/no-harm review.** Attempted counterexample: the new capability passes its own counter while an existing command, knowledge entry, source identity or admission rule regresses. The requested probes found no such regression. This is not a C1 judgment, admission decision, or exhaustive certification of the new tool.

| Axis | Verdict | Evidence and boundary |
|---|---|---|
| operability | NOT-HARMED | The exact SCORECARD.md:29 counter prints `VERDICT_BEARING_EXPORTS=3/3`; the existing gate's SHA256 matches the required digest. No existing executable changed in the committed diff. |
| coverage | NOT-HARMED | All 45 existing source rows remain unchanged; 4 new rows, S046–S049, produce 49 rows. No existing knowledge entry is changed; the only knowledge change is a new file. Manual census finds no malformed rows, duplicate ids or missing mined used-by paths. |
| depth | NOT-HARMED | The baseline tree lists 32 existing Markdown knowledge entries; none occurs in the changed-path inventory. Existing SOURCES cells and QUALITY criteria 1–22 are preserved byte-for-byte by the addition-only diff. This checks retained detail, not the correctness of every new statement. |
| freshness | NOT-HARMED | No existing knowledge provenance header, source opened/recheck cell, or existing recheck executable is rewritten. The new entry explicitly names page drift/no-snapshot limits. No broader freshness improvement is inferred. |
| calibration | NOT-HARMED | Existing QUALITY criteria 1–22 and the original narrow 3/10 score remain intact; the original runnable observable still gives 3/3. The new entry distinguishes location from support/truth and explicitly records the S047 extraction limit. Uncommitted SKILL.md additions are disclosed separately below rather than attributed to the audited commit. |
| adjacency | NOT-HARMED | No existing hard boundary or province refusal is rewritten. The new entry/source scopes distinguish source semantics from lane policy and explicitly retain the live-fetch approval question as unresolved. This review made no network requests and does not resolve that policy question. |

**Smallest safe correction:** no production correction is justified by these preservation probes. Keep the frozen claim, counter and fixtures unchanged. For accurate provenance, distinguish the committed 296-path inventory from the separately observed, uncommitted SKILL.md additions; do not present this review as proof of C1, authorization, or round admission.

## Scope and command evidence

All commands ran to completion, with a command timeout no greater than 600 s. No background job, server, subagent, installation, Git/JJ write, index change, or production-file edit was started. The only authored lane artifact is this report. Tools installed/updated: none.

Audited identities, from `timeout 600 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse 6c5eb146 master HEAD` (exit 0):

```text
6c5eb1466f2b8abbd3de576389037f435016d07b
b18b3ec9d8a01f966dd81991615bac27df6d66a1
b18b3ec9d8a01f966dd81991615bac27df6d66a1
```

### Requested committed diff and gate identity

Commands (both exit 0):

```sh
timeout 600 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --stat 6c5eb146 master
timeout 600 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --name-only 6c5eb146 master
```

The stat summary is **296 files changed, 157216 insertions(+)**, with no deletions. The complete, unabridged changed-path list is included below; the stat display itself abbreviates some long paths.

Command (exit 0):

```sh
timeout 600 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
```

Output:

```text
ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
```

This is the exact required SHA256. The gate is absent from the committed changed-path inventory, and the working-tree comparison below reports no gate change.

### Original operability observable

Copied from SCORECARD.md lines 28–30 and executed from the lane root, with the requested 600 s timeout (exit 0):

```sh
timeout 600 python3 -c 'import subprocess; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify","../research/deep-research-2026-09-28/"+n,"--root",".."],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))'
```

Output:

```text
VERDICT_BEARING_EXPORTS=3/3
```

This checks all 3 named archive inputs for exit 1 and exactly 1 full DRIFT summary each; it is not the full gate selftest.

### Protected records: additions only

Commands (each exit 0):

```sh
timeout 600 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --no-ext-diff --no-color --unified=4 6c5eb146 master -- corpus/knowledge corpus/SOURCES.md corpus/QUALITY.md corpus/lessons/round-28.md LOG.md SCORECARD.md considerthese/2026-10-22.md
timeout 600 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --no-ext-diff --numstat 6c5eb146 master -- corpus tools AXES.md SKILL.md
timeout 600 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin ls-tree -r 6c5eb146 -- tools/research-gate.sh corpus/knowledge corpus/QUALITY.md corpus/SOURCES.md SKILL.md
```

The production/corpus numstat output is:

```text
29	0	corpus/QUALITY.md
4	0	corpus/SOURCES.md
303	0	corpus/evidence/round29/c1-count.py
179	0	corpus/evidence/round29/claims.md
126	0	corpus/evidence/round29/prose-check.py
41	0	corpus/fixtures/quote-reopen-r29/items.tsv
41	0	corpus/fixtures/quote-reopen-r29/labels.tsv
104	0	corpus/knowledge/quote-reopen-r29.md
4	0	corpus/lessons/round-28.md
440	0	tools/quote-reopen.py
```

The full patch shows:

- `corpus/knowledge/quote-reopen-r29.md` is a **new file**; none of the 32 baseline Markdown knowledge entries is modified or removed.
- `corpus/SOURCES.md` adds exactly S046–S049 before `## Paths`. No cell of any existing row is edited, and no source id is replaced or reused.
- `corpus/QUALITY.md` appends 29 lines after the end of criterion 22: the round-29 heading and criteria 23–25. Criteria 1–22 are untouched.
- `LOG.md`, `SCORECARD.md` and `corpus/lessons/round-28.md` each append a 4-line D3 correction; their historical text is retained.

Additional boundary command (exit 0):

```sh
timeout 600 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --no-ext-diff --no-color --numstat master -- SKILL.md corpus tools AXES.md LOG.md SCORECARD.md
```

Output:

```text
3	0	SKILL.md
```

Thus the inspected working tree has 3 pending SKILL.md additions beyond the audited commit, not represented in the 296 committed paths. The observed additions name the quote command in the decision table, checklist and gates table. Existing hard-boundary text remains present at SKILL.md:48–58. No tracked corpus/tool working-tree difference was reported by this scoped command; untracked files are not inventoried by it.

### Maintained SOURCES validator

Command (exit 0):

```sh
timeout 600 bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
```

Output:

```text
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

### Frozen CORPUS.md manual census

Opened the fleet `CORPUS.md:131–147`; the lane has no own CORPUS.md. Ran its census commands from the lane root. The column-zero assumption is stated in CORPUS.md:150–155. Results:

| Manual check | Exit | stdout |
|---|---:|---|
| rows (line 135) | 0 | `49` |
| malformed rows (line 137) | 0 | `0` |
| tier histogram (line 139) | 0 | `A=43 B=1 C=5 ` |
| status histogram (line 141) | 0 | `mined=26 queued=19 rejected=4 ` |
| duplicate ids (line 143) | 0 | empty |
| enum violations / tier inflation (line 145) | 0 | empty |
| missing mined used-by paths (line 147) | 0 | empty |

Exact simple commands:

```sh
timeout 600 grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
timeout 600 awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
timeout 600 awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
timeout 600 awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
timeout 600 awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | timeout 600 sort | timeout 600 uniq -d
```

The two remaining manual script bodies below were each executed with `subprocess.run(["timeout", "600", "bash", "-c", body], cwd=lane, capture_output=True, text=True, timeout=600)`; both returned exit 0, empty stdout and empty stderr:

```sh
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md

awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```

## Limits

- C1's 130-item live counter was not rerun by this seat; the assignment here was the original operability and lane no-harm checks. No conclusion about C1 follows from the 3/3 archive observable.
- No full gate selftest, new-tool conformance/security test or source-teaches verification was run. Existing rejected-round defects are not treated as newly repaired or newly caused.
- NOT-HARMED is bounded to the retained existing surfaces and requested structural/operability probes. Additions-only does not by itself establish factual accuracy, authorization, or publication completeness of new material.
- The committed diff is pinned to the master value printed above. Pending SKILL.md additions are disclosed separately. Concurrent or later edits and untracked files are outside that committed inventory.
- An initial broad recursive CORPUS.md glob timed out; a narrower top-level glob located the fleet document. Initial lane-local CORPUS.md and AXES.md reads returned not found; the shared fleet documents were then located and opened. These did not block any requested check.

## Complete committed changed-path inventory

Source: the successful `timeout 600 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --name-only 6c5eb146 master` call above; 296 paths, in its output order. These paths were listed, not all opened or independently verified.

```text
.ufo/waves/round-29/build-dispatch.json
.ufo/waves/round-29/build-spec.json
.ufo/waves/round-29/build/ConnectorPlanWalk.md
.ufo/waves/round-29/build/ConnectorPlanWalk/pre-data-probe.json
.ufo/waves/round-29/build/ConnectorSiblings.md
.ufo/waves/round-29/build/ConnectorSiblings/recorded-seeds.txt
.ufo/waves/round-29/build/CriticProvince.md
.ufo/waves/round-29/build/CriticRuntimeVariants.md
.ufo/waves/round-29/build/CriticRuntimeVariants/audit.py
.ufo/waves/round-29/build/CriticRuntimeVariants/extractor-diffs.json
.ufo/waves/round-29/build/CriticRuntimeVariants/fetch-manifest.json
.ufo/waves/round-29/build/CriticRuntimeVariants/mislabeled-variants.json
.ufo/waves/round-29/build/CriticRuntimeVariants/reference.py
.ufo/waves/round-29/build/CriticRuntimeVariants/result.json
.ufo/waves/round-29/build/ExecOfflineTest/quote-reopen-offline-test.py
.ufo/waves/round-29/build/ExecOfflineTest/ref_run.txt
.ufo/waves/round-29/build/ExecOfflineTest/wrong_casefold_run.txt
.ufo/waves/round-29/build/ExecOfflineTest/wrong_rawgrep_run.txt
.ufo/waves/round-29/build/ExecOfflineTest/wrong_run.txt
.ufo/waves/round-29/build/ExecProseCheck.md
.ufo/waves/round-29/build/ExecProseCheck/clean-sample.md
.ufo/waves/round-29/build/ExecProseCheck/exclusions-sample.md
.ufo/waves/round-29/build/ExecProseCheck/prose-check.py
.ufo/waves/round-29/build/ExecTool.md
.ufo/waves/round-29/build/ExecTool/quote-reopen.py
.ufo/waves/round-29/build/ExecTool/receipt-v3-delivered.json
.ufo/waves/round-29/build/ExecTool/receipt-v3-run1.json
.ufo/waves/round-29/build/ExecTool/receipt-v3-run8.json
.ufo/waves/round-29/build/ExecTool/selftest.py
.ufo/waves/round-29/build/ExecToolB/__pycache__/quote-reopen-b.cpython-314.pyc
.ufo/waves/round-29/build/ExecToolB/quote-reopen-b.py
.ufo/waves/round-29/build/ExecToolSelfAudit.md
.ufo/waves/round-29/build/ExecToolSelfAudit/audit_reference.py
.ufo/waves/round-29/build/ExecToolSelfAudit/check_contract_lists.py
.ufo/waves/round-29/build/ExecToolSelfAudit/classify_divergences.py
.ufo/waves/round-29/build/ExecToolSelfAudit/contract_model.py
.ufo/waves/round-29/build/ExecToolSelfAudit/probe_details.py
.ufo/waves/round-29/build/ExecToolSelfAudit/probe_live_pages.py
.ufo/waves/round-29/build/ExecToolSelfAudit/probe_materiality.py
.ufo/waves/round-29/build/ExecToolSelfAudit/probe_registry_ambiguity.py
.ufo/waves/round-29/build/ExecToolSelfAudit/probe_structure_hazards.py
.ufo/waves/round-29/build/MutateBlockInline.md
.ufo/waves/round-29/build/MutateBlockInline/baseline.json
.ufo/waves/round-29/build/MutateBlockInline/extra-inline.json
.ufo/waves/round-29/build/MutateBlockInline/fetch.json
.ufo/waves/round-29/build/MutateBlockInline/matrix.tsv
.ufo/waves/round-29/build/MutateBlockInline/only-p-br.json
.ufo/waves/round-29/build/MutateBlockInline/restored-after-extra-inline.json
.ufo/waves/round-29/build/MutateBlockInline/restored.json
.ufo/waves/round-29/build/MutateBlockInline/summary.json
.ufo/waves/round-29/build/MutateBlockInline/witnesses.json
.ufo/waves/round-29/build/MutateCounter.md
.ufo/waves/round-29/build/MutateCounter/1-mutated.receipt.json
.ufo/waves/round-29/build/MutateCounter/1-mutated.result.json
.ufo/waves/round-29/build/MutateCounter/1-mutated.stderr.txt
.ufo/waves/round-29/build/MutateCounter/1-mutated.stdout.txt
.ufo/waves/round-29/build/MutateCounter/1-pristine.receipt.json
.ufo/waves/round-29/build/MutateCounter/1-pristine.result.json
.ufo/waves/round-29/build/MutateCounter/1-pristine.stderr.txt
.ufo/waves/round-29/build/MutateCounter/1-pristine.stdout.txt
.ufo/waves/round-29/build/MutateCounter/1-restored.receipt.json
.ufo/waves/round-29/build/MutateCounter/1-restored.result.json
.ufo/waves/round-29/build/MutateCounter/1-restored.stderr.txt
.ufo/waves/round-29/build/MutateCounter/1-restored.stdout.txt
.ufo/waves/round-29/build/MutateCounter/2-mutated.receipt.json
.ufo/waves/round-29/build/MutateCounter/2-mutated.result.json
.ufo/waves/round-29/build/MutateCounter/2-mutated.stderr.txt
.ufo/waves/round-29/build/MutateCounter/2-mutated.stdout.txt
.ufo/waves/round-29/build/MutateCounter/2-pristine.receipt.json
.ufo/waves/round-29/build/MutateCounter/2-pristine.result.json
.ufo/waves/round-29/build/MutateCounter/2-pristine.stderr.txt
.ufo/waves/round-29/build/MutateCounter/2-pristine.stdout.txt
.ufo/waves/round-29/build/MutateCounter/2-restored.receipt.json
.ufo/waves/round-29/build/MutateCounter/2-restored.result.json
.ufo/waves/round-29/build/MutateCounter/2-restored.stderr.txt
.ufo/waves/round-29/build/MutateCounter/2-restored.stdout.txt
.ufo/waves/round-29/build/MutateCounter/3-mutated.receipt.json
.ufo/waves/round-29/build/MutateCounter/3-mutated.result.json
.ufo/waves/round-29/build/MutateCounter/3-mutated.stderr.txt
.ufo/waves/round-29/build/MutateCounter/3-mutated.stdout.txt
.ufo/waves/round-29/build/MutateCounter/3-pristine.receipt.json
.ufo/waves/round-29/build/MutateCounter/3-pristine.result.json
.ufo/waves/round-29/build/MutateCounter/3-pristine.stderr.txt
.ufo/waves/round-29/build/MutateCounter/3-pristine.stdout.txt
.ufo/waves/round-29/build/MutateCounter/3-restored.receipt.json
.ufo/waves/round-29/build/MutateCounter/3-restored.result.json
.ufo/waves/round-29/build/MutateCounter/3-restored.stderr.txt
.ufo/waves/round-29/build/MutateCounter/3-restored.stdout.txt
.ufo/waves/round-29/build/MutateCounter/4-mutated.receipt.json
.ufo/waves/round-29/build/MutateCounter/4-mutated.result.json
.ufo/waves/round-29/build/MutateCounter/4-mutated.stderr.txt
.ufo/waves/round-29/build/MutateCounter/4-mutated.stdout.txt
.ufo/waves/round-29/build/MutateCounter/4-pristine.receipt.json
.ufo/waves/round-29/build/MutateCounter/4-pristine.result.json
.ufo/waves/round-29/build/MutateCounter/4-pristine.stderr.txt
.ufo/waves/round-29/build/MutateCounter/4-pristine.stdout.txt
.ufo/waves/round-29/build/MutateCounter/4-restored.receipt.json
.ufo/waves/round-29/build/MutateCounter/4-restored.result.json
.ufo/waves/round-29/build/MutateCounter/4-restored.stderr.txt
.ufo/waves/round-29/build/MutateCounter/4-restored.stdout.txt
.ufo/waves/round-29/build/MutateCounter/5-mutated.receipt.json
.ufo/waves/round-29/build/MutateCounter/5-mutated.result.json
.ufo/waves/round-29/build/MutateCounter/5-mutated.stderr.txt
.ufo/waves/round-29/build/MutateCounter/5-mutated.stdout.txt
.ufo/waves/round-29/build/MutateCounter/5-pristine.receipt.json
.ufo/waves/round-29/build/MutateCounter/5-pristine.result.json
.ufo/waves/round-29/build/MutateCounter/5-pristine.stderr.txt
.ufo/waves/round-29/build/MutateCounter/5-pristine.stdout.txt
.ufo/waves/round-29/build/MutateCounter/5-restored.receipt.json
.ufo/waves/round-29/build/MutateCounter/5-restored.result.json
.ufo/waves/round-29/build/MutateCounter/5-restored.stderr.txt
.ufo/waves/round-29/build/MutateCounter/5-restored.stdout.txt
.ufo/waves/round-29/build/MutateCounter/6-mutated.receipt.json
.ufo/waves/round-29/build/MutateCounter/6-mutated.result.json
.ufo/waves/round-29/build/MutateCounter/6-mutated.stderr.txt
.ufo/waves/round-29/build/MutateCounter/6-mutated.stdout.txt
.ufo/waves/round-29/build/MutateCounter/6-pristine.receipt.json
.ufo/waves/round-29/build/MutateCounter/6-pristine.result.json
.ufo/waves/round-29/build/MutateCounter/6-pristine.stderr.txt
.ufo/waves/round-29/build/MutateCounter/6-pristine.stdout.txt
.ufo/waves/round-29/build/MutateCounter/6-restored.receipt.json
.ufo/waves/round-29/build/MutateCounter/6-restored.result.json
.ufo/waves/round-29/build/MutateCounter/6-restored.stderr.txt
.ufo/waves/round-29/build/MutateCounter/6-restored.stdout.txt
.ufo/waves/round-29/build/MutateCounter/7-mutated.receipt.json
.ufo/waves/round-29/build/MutateCounter/7-mutated.result.json
.ufo/waves/round-29/build/MutateCounter/7-mutated.stderr.txt
.ufo/waves/round-29/build/MutateCounter/7-mutated.stdout.txt
.ufo/waves/round-29/build/MutateCounter/7-pristine.receipt.json
.ufo/waves/round-29/build/MutateCounter/7-pristine.result.json
.ufo/waves/round-29/build/MutateCounter/7-pristine.stderr.txt
.ufo/waves/round-29/build/MutateCounter/7-pristine.stdout.txt
.ufo/waves/round-29/build/MutateCounter/7-restored.receipt.json
.ufo/waves/round-29/build/MutateCounter/7-restored.result.json
.ufo/waves/round-29/build/MutateCounter/7-restored.stderr.txt
.ufo/waves/round-29/build/MutateCounter/7-restored.stdout.txt
.ufo/waves/round-29/build/MutateCounter/mutations.json
.ufo/waves/round-29/build/MutateCounter/page-replay.json
.ufo/waves/round-29/build/MutateCounter/report.md
.ufo/waves/round-29/build/RevengerGateSpan.md
.ufo/waves/round-29/build/RevengerGateSpan/gate-stderr.txt
.ufo/waves/round-29/build/RevengerGateSpan/gate-stdout.txt
.ufo/waves/round-29/build/RevengerGateSpan/probe.jsonl
.ufo/waves/round-29/build/RevengerGateSpan/probe.md
.ufo/waves/round-29/build/RevengerGateSpan/probe.py
.ufo/waves/round-29/build/RevengerGateSpan/run-log.txt
.ufo/waves/round-29/build/ReviewFixtureAbsentEdits.md
.ufo/waves/round-29/build/ReviewFixtureAbsentSplice.md
.ufo/waves/round-29/build/ReviewFixtureEdgeClasses.md
.ufo/waves/round-29/build/ReviewFixtureEdgeClasses/check_edge_classes.py
.ufo/waves/round-29/build/ReviewFixtureEdgeClasses/report.md
.ufo/waves/round-29/build/ReviewFixtureEdgeClasses/run-2026-10-23.log
.ufo/waves/round-29/build/ReviewFixtureVerbatimA.md
.ufo/waves/round-29/build/ReviewFixtureVerbatimA/sel.tsv
.ufo/waves/round-29/build/ReviewFixtureVerbatimB.md
.ufo/waves/round-29/build/ScoutCustodyVocab.md
.ufo/waves/round-29/build/ScoutCustodyVocab/attribute.py
.ufo/waves/round-29/build/ScoutCustodyVocab/lexicon.py
.ufo/waves/round-29/build/ScoutCustodyVocab/report.md
.ufo/waves/round-29/build/ScoutCustodyVocab/sweep.tsv
.ufo/waves/round-29/build/ScoutCustodyVocab/sweep.tsv.detail.txt
.ufo/waves/round-29/build/ScoutCustodyVocab/sweep2.py
.ufo/waves/round-29/build/ScoutGateQuotes.md
.ufo/waves/round-29/build/ScoutGateQuotes/held-out.tsv
.ufo/waves/round-29/build/ScoutRegistryFetch.md
.ufo/waves/round-29/build/ScoutRegistryFetch/registry-fetch.tsv
.ufo/waves/round-29/build/ScoutRegistryFetch/registry_fetch.py
.ufo/waves/round-29/build/ScoutRegistryFetch/registry_fetch_more.py
.ufo/waves/round-29/build/ScoutRegistryFetch/report.md
.ufo/waves/round-29/build/ScoutSpotcheckRoutes.md
.ufo/waves/round-29/build/ScribeKnowledge.md
.ufo/waves/round-29/build/ScribeKnowledge/quote-reopen-r29.md
.ufo/waves/round-29/build/ScribeMistakes.md
.ufo/waves/round-29/build/ScribeMistakes/report.md
.ufo/waves/round-29/build/ScribeQuality.md
.ufo/waves/round-29/build/ScribeQuality/report.md
.ufo/waves/round-29/build/ScribeRepairD3.md
.ufo/waves/round-29/build/ScribeSkillRow.md
.ufo/waves/round-29/build/ScribeSrcHtmlParser.md
.ufo/waves/round-29/build/ScribeSrcTextFragments.md
.ufo/waves/round-29/build/ScribeSrcTextQuote.md
.ufo/waves/round-29/build/ScribeSrcUax15.md
.ufo/waves/round-29/build/SentinelFetchBounds.md
.ufo/waves/round-29/build/SentinelFetchBounds/probe_fetch_bounds.py
.ufo/waves/round-29/build/SentinelFetchBounds/probe_output.txt
.ufo/waves/round-29/build/swarm-registry.json
.ufo/waves/round-29/controls/CtlAlwaysAbsent/control.py
.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-seed2.json
.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-v2-seed2.json
.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-v2.json
.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-v3-run2.json
.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt-v3.json
.ufo/waves/round-29/controls/CtlAlwaysAbsent/receipt.json
.ufo/waves/round-29/controls/CtlAlwaysAbsent/report.md
.ufo/waves/round-29/controls/CtlAlwaysVerbatim/control.py
.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt-seed2.json
.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt-v2-seed2.json
.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt-v2.json
.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt-v3-run2.json
.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt-v3.json
.ufo/waves/round-29/controls/CtlAlwaysVerbatim/receipt.json
.ufo/waves/round-29/controls/CtlAlwaysVerbatim/report.md
.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/control.py
.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt-seed2.json
.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt-v2-seed2.json
.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt-v2.json
.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt-v3-run2.json
.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt-v3.json
.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/receipt.json
.ufo/waves/round-29/controls/CtlCasefoldNoBoundary/report.md
.ufo/waves/round-29/controls/CtlIdKeyed/control.py
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-seed2.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-v2-seed2.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-v2-verbatim-seed2.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-v2-verbatim.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-v2.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-v3-run2.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-v3-verbatim-run2.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-v3-verbatim.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt-v3.json
.ufo/waves/round-29/controls/CtlIdKeyed/receipt.json
.ufo/waves/round-29/controls/CtlIdKeyed/report.md
.ufo/waves/round-29/controls/CtlJunk/control-binary.py
.ufo/waves/round-29/controls/CtlJunk/control.py
.ufo/waves/round-29/controls/CtlJunk/receipt-binary-seed2.json
.ufo/waves/round-29/controls/CtlJunk/receipt-binary.json
.ufo/waves/round-29/controls/CtlJunk/receipt-seed2.json
.ufo/waves/round-29/controls/CtlJunk/receipt-v2-binary-seed2.json
.ufo/waves/round-29/controls/CtlJunk/receipt-v2-binary.json
.ufo/waves/round-29/controls/CtlJunk/receipt-v2-seed2.json
.ufo/waves/round-29/controls/CtlJunk/receipt-v2.json
.ufo/waves/round-29/controls/CtlJunk/receipt-v3-binary-run2.json
.ufo/waves/round-29/controls/CtlJunk/receipt-v3-binary.json
.ufo/waves/round-29/controls/CtlJunk/receipt-v3-run2.json
.ufo/waves/round-29/controls/CtlJunk/receipt-v3.json
.ufo/waves/round-29/controls/CtlJunk/receipt.json
.ufo/waves/round-29/controls/CtlJunk/report.md
.ufo/waves/round-29/controls/CtlLabelKeyed/control-v2.py
.ufo/waves/round-29/controls/CtlLabelKeyed/control-v3.py
.ufo/waves/round-29/controls/CtlLabelKeyed/control.py
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-seed2.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-seed2.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed-freshseed-L1.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed-seed2.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2-warmed.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v2.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v3-contrast-run2.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v3-contrast.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v3-run2.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v3-warmed-run2-corrected.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v3-warmed-run2.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v3-warmed.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt-v3.json
.ufo/waves/round-29/controls/CtlLabelKeyed/receipt.json
.ufo/waves/round-29/controls/CtlLabelKeyed/report.md
.ufo/waves/round-29/controls/CtlNoReader/control-verbatim.py
.ufo/waves/round-29/controls/CtlNoReader/control.py
.ufo/waves/round-29/controls/CtlNoReader/receipt-seed2.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-v2-seed2.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-v2-verbatim-seed2.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-v2-verbatim.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-v2.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-v3-run2.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-v3-verbatim-run2.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-v3-verbatim.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-v3.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-verbatim-seed2.json
.ufo/waves/round-29/controls/CtlNoReader/receipt-verbatim.json
.ufo/waves/round-29/controls/CtlNoReader/receipt.json
.ufo/waves/round-29/controls/CtlNoReader/report.md
.ufo/waves/round-29/controls/CtlRawGrep/control.py
.ufo/waves/round-29/controls/CtlRawGrep/receipt-seed2.json
.ufo/waves/round-29/controls/CtlRawGrep/receipt-v2-seed2.json
.ufo/waves/round-29/controls/CtlRawGrep/receipt-v2.json
.ufo/waves/round-29/controls/CtlRawGrep/receipt-v3-run2.json
.ufo/waves/round-29/controls/CtlRawGrep/receipt-v3.json
.ufo/waves/round-29/controls/CtlRawGrep/receipt.json
.ufo/waves/round-29/controls/CtlRawGrep/report.md
.ufo/waves/round-29/controls/before-do-nothing-v2.json
.ufo/waves/round-29/controls/before-do-nothing-v3.json
.ufo/waves/round-29/controls/before-do-nothing.json
.ufo/waves/round-29/measure/after-run1.json
.ufo/waves/round-29/measure/after-run2.json
LOG.md
SCORECARD.md
considerthese/2026-10-22.md
corpus/QUALITY.md
corpus/SOURCES.md
corpus/evidence/round29/c1-count.py
corpus/evidence/round29/claims.md
corpus/evidence/round29/prose-check.py
corpus/fixtures/quote-reopen-r29/items.tsv
corpus/fixtures/quote-reopen-r29/labels.tsv
corpus/knowledge/quote-reopen-r29.md
corpus/lessons/round-28.md
tools/quote-reopen.py
```
