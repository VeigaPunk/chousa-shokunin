# FC3GluedBeforeTerminal37 — C3 `glued-before-terminal`

**Verdict: HOLDS for the named control, within this bounded probe. Targeted mutant: KILLED.** A nearby clean-ID cardinality blind spot was demonstrated; no landed-gate counterexample was found in the 12 fixtures below. This is author-lane advice, not admission of C3 or of the round.

## Axes and scope

- **Calibration:** derive the expected IDs from the declared grammar, challenge consumed-text occurrence identity, and distinguish observable failures from clean-ID blind spots.
- **Operability:** require ordinary metadata output and a semantic finding, not syntax/setup failure, to kill the mutant.
- **Freshness:** bind measurements to revision `dd72641e574679c4f7882dd43de072b4c8892d6f`; date/freshness repairs themselves are outside this assignment.

Only sandbox `/tmp/chousa-r27-falsify-FC3GluedBeforeTerminal37` was mutated. The lane's production files, index and history were not changed. This requested report is the sole lane write.

## 1. Is the expectation independent?

**Yes, as an expectation derivation, not as proof of the author's historical process.** `corpus/evidence/round27-claims.md:15` requires standalone ASCII S-ids without invented or duplicate occurrences. The pre-existing explicit boundary declaration is `corpus/evidence/round26-claims.md:132–141`: `S` plus at least three digits, with ASCII alphanumeric/underscore boundaries. `corpus/knowledge/registry-link-r26.md:23–29` declares the missing-row/not-mined/backlink semantics.

The assigned fixture (`round27-regressions.py:151–164`) is:

```text
source: see S001S002 and S001
verified-at: 2026-01-02 checked synthetic fixture
recheck: 90d

## Claim
synthetic
```

```text
| id | status | used-by |
|---|---|---|
| S001 | mined | corpus/knowledge/entry.md |
| S002 | queued | — |
```

`S001S002` is one glued ASCII word and contributes no ID. The final `S001` is the only genuine occurrence; its row is mined with the exact backlink. Therefore exit **0**, no `META_SOURCE_NOT_MINED source_id=S002`, and no `META_SOURCE_` findings follow from the declaration without consulting gate implementation. These are exactly the shipped tuple and count predicates, not weaker substitutes.

The scoped detector parses the regression script with Python AST, extracts only the named literal tuple and its unchanged `observe()` function, and runs those exact assertions. It does not execute the whole regression script. Nearby expected occurrences use the independent grammar `(?<![A-Za-z0-9_])S[0-9]{3,}(?![A-Za-z0-9_])`, not gate output or its tokenizer.

## 2. Targeted production mutation and actual output

The historical production function was read with the following command, exit **0**, without executing the old gate:

```sh
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 64eec5d41c7cf7f17f5ce1e968e28b3769952596:tools/research-gate.sh
```

One mutation replaced only occurrence iteration in `metadata_registry_check_source()` (`tools/research-gate.sh:2499–2532`) with that historical regex/rescan mechanism. The landed `local LC_ALL=C`, registry relations, finding emission, and all other functions were retained. The changed mechanism was:

```sh
local source_scan=$1 source_id_re='(^|[^[:alnum:]_])(S[0-9]{3,})([^[:alnum:]_]|$)'
local source_id source_match found_id=0 used_by token matched i
# Keep the landed local LC_ALL=C and existing relation checks.
while [[ $source_scan =~ $source_id_re ]]; do
  source_id=${BASH_REMATCH[2]}
  source_match=${BASH_REMATCH[0]}
  # Existing, unchanged relation checks execute here.
  source_scan=${source_scan#*"$source_match"}
done
```

This is a description of the surgical substitution, not a second executable gate. It replaces the landed whole-word iteration and full-token S-id test; no relation check was stubbed.

On the original source, the regex finds the terminal match ` S001`, but prefix removal consumes the *earlier* identical substring inside ` S001S002`. The residual begins `S002`, inventing a standalone queued occurrence.

| Same detector / same named fixture | Gate exit | Source findings | Detector result |
|---|---:|---|---|
| Pristine | 0 | none | matched |
| Mutated | 1 | one `META_SOURCE_NOT_MINED`, `source_id=S002` | failed as intended |
| Restored | 0 | none | matched |

Key mutant stdout, with empty stderr:

```text
META entry=entry.md source=present verified_at=dated recheck=scheduled verdict=drift
FINDING META_SOURCE_NOT_MINED severity=warn surface=metadata obs=entry=entry.md source_id=S002 registry row is not mined
METADATA_COMPLETE=1/1
RESEARCH_GATE: DRIFT (entries=1 complete=1 findings=1 drift=1)
```

The exact original assertions reported `exit 1 != 0`, S002 not-mined count `1 != 0`, and total source-finding count `1 != 0`. Thus **KILLED for the intended invented-ID reason**, not exit2, a parse error, or a failed fixture setup.

## 3. Nearby coverage counterexample, not a landed defect

Change only the source to:

```text
source: see S001S001 and S001
```

Keep the original registry. This has exactly one real `S001`. **Pristine, mutated and restored all return exit0 with `findings=0 drift=0`.** The clean-ID observation cannot reveal duplicated validation of a fully valid row: this individual neighbor survives the same mutant.

A paired fixture changes only S001's registry status to `queued`, keeping that source and backlink identical. Expected cardinality is one warning. Actual results:

| Fixture | Pristine | Mutated | Restored |
|---|---|---|---|
| `see S001S001 and S001`, S001 mined | exit0, 0 findings | exit0, 0 findings | exit0, 0 findings |
| Same source, S001 queued | exit1, 1 S001 warning | exit1, **3 S001 warnings** | exit1, 1 S001 warning |

This makes the otherwise invisible duplicate-occurrence defect observable. It is a coverage limitation of clean-only diagnostic assertions, **not** evidence that the landed implementation duplicates IDs. The assigned `glued-before-terminal` fixture itself is not vacuous against this mutant: its deliberately queued S002 exposes the invented ID. Advice: retain such queued/missing-row cardinality witnesses when extending this control family; a neighboring all-clean result alone cannot establish occurrence identity.

The unchanged scoped detector covered 12 fixtures per phase: the named input; terminal punctuation; glued-only/no real ID; queued terminal; two queued terminal occurrences; missing terminal; underscore-glued terminal text; next-line terminal; two real terminal IDs; the same-ID clean neighbor; its queued witness; and the original source with S001 queued. Pristine/restored: **0/12 mismatches**. Mutated: **4/12 mismatches** (named input, underscore neighbor, and the two queued S001 witnesses). No broader parser, resource, or C1/C2 conclusion follows.

## Commands, bounds, and restoration evidence

Sandbox creation, exit **0**:

```sh
mkdir /tmp/chousa-r27-falsify-FC3GluedBeforeTerminal37 && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e574679c4f7882dd43de072b4c8892d6f | tar -x -C /tmp/chousa-r27-falsify-FC3GluedBeforeTerminal37
```

Executed with cwd `/tmp/chousa-r27-falsify-FC3GluedBeforeTerminal37`, each outer timeout 120 seconds:

```sh
python3 probe_glued_before_terminal.py pristine                    # exit 0
# Apply the one sandbox-only mutation described above.
python3 probe_glued_before_terminal.py mutated                     # exit 1
# Restore the three edited spans to their original bytes.
python3 probe_glued_before_terminal.py restored && sha256sum tools/research-gate.sh corpus/evidence/round27-regressions.py probe_glued_before_terminal.py
# exit 0
```

Each gate subprocess has a **15-second timeout**, `LC_ALL=C`, `CHOUSA_STRICT=0`, and other inherited `CHOUSA_*` variables removed. For the named case its exact command is:

```sh
bash /tmp/chousa-r27-falsify-FC3GluedBeforeTerminal37/tools/research-gate.sh verify-metadata /tmp/chousa-r27-falsify-FC3GluedBeforeTerminal37/probe-fixtures/glued-before-terminal/corpus/knowledge/entry.md --root /tmp/chousa-r27-falsify-FC3GluedBeforeTerminal37/probe-fixtures/glued-before-terminal --registry /tmp/chousa-r27-falsify-FC3GluedBeforeTerminal37/probe-fixtures/glued-before-terminal/registry.md
```

Its cwd is the named case's fixture root. Complete argv, fixture hashes, stdout, stderr and assertions for all cases are in sandbox `probe-pristine.json`, `probe-mutated.json`, and `probe-restored.json`.

SHA-256 evidence:

```text
Gate pristine/restored:
ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84
Gate mutated:
e9010c0a6fbea14a6d2cbee97e5e9fdfc63eef11443e66c176a9072b1473c6cc
Unchanged original regression script:
5afea7863f2b052ba54a46cf2faf88f863d76c61d3d2cf45e091f92bc526a5df
Unchanged scoped detector across all three runs:
5a2c3bec0e612383d2cde875b20ca1c5ee9f57d0ebf8ec2bccf654180fc668e3
Named entry, identical across all three runs:
1c79d6c2e7fe597738abe1468f352a97711ad041036b178d2ab6ca789e031ad8
Named registry, identical across all three runs:
afa16571baf17406917e51a45f4ab9da099b847c95d44b29f502f6656d71e8e7
Clean/queued same-ID neighbor entry, identical in every phase:
146cbc87b126d5249890da88af0b6855583c2de70cb6e6988a04e885ff83f024
Queued same-ID witness registry, identical in every phase:
7d3c9689a40d5b73ac64785a4c9b852931e598065c0995abb69ce4f4d1750f77
```

Exact gate-byte restoration is established by the original hash returning, followed by the same detector returning its pristine results. No second mutant was attempted. No full selftest or whole regression suite, network, external target, host secret read, live-process inspection, debugger, subagent or background job was used. No tools were installed/updated. Existing runtimes: GNU Bash **5.3.20(1)-release**, Python **3.14.8** (`bash --version && python3 --version`, exit0).
