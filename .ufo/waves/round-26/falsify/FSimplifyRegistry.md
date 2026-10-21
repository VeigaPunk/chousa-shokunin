# FSimplifyRegistry — round26 attempt1, author-lane advice

## Scope and axes

Read-only review of C3 fd snapshot/registry parsing, with bounded fixtures only. Axes: calibration (registry relations, not source truth), refusal parity, allocation shape, maintainability/one authority. No production changes or sandbox code mutations; no deletions made. No outside judgment, admission, freshness, or field-readiness claim.

Immutable target: `0e9784bd52eca456b24d0bc40921480a47f91a2b`; claim base: `ba3333254dd337658a4f25e7a9471f9cf4e4567e`. Private clone: `/tmp/chousa-r26-falsify-FSimplifyRegistry`. The live claims/QUALITY and measured-revision receipt were read first. All 13 receipt input hashes independently match the private clone. Gate SHA-256: `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6`. No moving-tree behavior was graded.

## Findings / bounded deletion candidate

1. **One low-risk candidate, not applied:** remove only `source_value=$1` from `local source_value=$1 entry_path=$2 entry_base=$3` in `tools/research-gate.sh:2473`. The helper independently initializes `source_scan=$1` on the next line and never reads its local `source_value`. Literal reference search found the meaningful `source_value` reads/writes in the caller `verify_metadata`, which must stay. The helper's only function call in its body is `emit_finding`; inspection at 392–402 shows it does not read `source_value`. This is a proposed dead binding deletion, **not a semantically proven no-caller result or a tested improvement**. Bash dynamic scoping is the tradeoff; do not delete the caller's similarly named variable or historical patch evidence.
2. **Do not delete the duplicated reader safeguards.** Registry 2374–2405 and entry 2582–2616 currently implement the same ordered checks: lexical/canonical denylist; one open fd; fd-canonical denylist; fd regular-file/stat-format validation; link count; stat byte cap; cap+1 bounded NUL-delimited read; post-read byte cap; NUL/read outcome; close fd. `LC_ALL=C` is set in both functions. No safeguard drift was found by source comparison; small NUL/multilink fixtures exercise parity below. Stat cap and post-read cap are not duplicate authorities: the latter catches growth after stat. Path and fd checks likewise cover different identities. Registry refusal intentionally exits usage 2, while entry refusal emits critical drift and exits 1. Removing either copy without a fully specified shared fd snapshot contract would harm the refusal axis; extracting a new helper is outside this read-only bounded-deletion task.
3. **No entry array materializes body lines.** `verify_metadata` 2631–2682 reads the scalar snapshot line by line and stops at the first unfenced `## ` (2656). Its arrays `files`, `candidates`, and `metadata_lines` (2540) grow with entry count, not body lines. Snapshot/header values remain byte-dependent scalars: this is not constant-memory parsing. Registry `cells` (2367, 2422–2423) is replaced for each row and scales with row width; used-by tokens (2476, 2489) scale with that cell's comma count. Registry maps (2408, 2437–2438) intentionally scale with distinct valid registry ids; there is no universal claim that all registry arrays are independent of registry row count. After a table ends at a non-pipe line (2412–2415), later prose is not parsed. Arbitrarily deleting cells/maps would harm table-column/first-id semantics.
4. **Preserved contract:** standalone S+3-or-more digit ids; first duplicate id wins; name-located columns; exact root-relative used-by paths with leading `./` normalization; metadata continuations/fences; NUL/multilink refusals. The existing differential agrees on 48 entries, but that does not establish citation support, scope sufficiency, claim truth, or the entire criterion-6 admission bar.

### Semantic-reference limitation

`read xd://lsp` returned `No such tool: xd://lsp`; its mounted-device list has no LSP route. There was no server to warm up, query status, or retry. The fallback was literal `functions.grep` for `source_value`, helper names and emitter definition, followed by source inspection. These are textual evidence only, never semantic-reference proof. Therefore no deletion is approved as proven, and no deletion was executed.

## Commands, exits, and bounded evidence

Commands used to establish the immutable sandbox (exit 0):

```sh
git clone --shared --no-checkout /home/vgpnk/Projects/shokunin/chousa-shokunin /tmp/chousa-r26-falsify-FSimplifyRegistry && git -C /tmp/chousa-r26-falsify-FSimplifyRegistry checkout --detach 0e9784bd52eca456b24d0bc40921480a47f91a2b
```

From that clone (exit 0):

```sh
git rev-parse HEAD && sha256sum tools/research-gate.sh corpus/evidence/round26-registry-differential.sh corpus/evidence/round26-registry-oracle.py
```

Observed revision exactly as above; differential digest `852a764870f71e7247005f2b91d6864cbe0ba6527098f2c35536466117e676e9`; oracle digest `6b2d135c01a8f41b914fb248af35567828336a1a69190560c5df4a07b40f1d78`. Python hashlib comparison against every receipt input returned true for all 13.

Narrow existing check, cwd private clone (exit 0):

```sh
bash corpus/evidence/round26-registry-differential.sh /tmp/chousa-r26-falsify-FSimplifyRegistry
```

Raw output:

```text
OUT_OF_CONTRACT_ESCAPED_PIPE=excluded (CORPUS contract v1 forbids | inside a cell)
REGISTRY_DIFF_SUITE=r24plus 5/5
REGISTRY_DIFF_SUITE=pop29 29/29
REGISTRY_DIFF_SUITE=adversarial 14/14
REGISTRY_DIFF_AGREE=48/48
```

Fresh fixture driver: `/tmp/chousa-r26-falsify-FSimplifyRegistry/review_registry.py`. Command `python3 review_registry.py` (cwd private clone) initially exited 1 because `/usr/bin/time` is absent:

```text
FileNotFoundError: [Errno 2] No such file or directory: '/usr/bin/time'
```

The driver was adjusted, not the gate: uses `os.wait4` rusage and monotonic elapsed time, wraps each gate call in `timeout 20s`. Second invocation exited 0. No tools were installed/updated. Every actual child command was:

```sh
timeout 20s bash /tmp/chousa-r26-falsify-FSimplifyRegistry/tools/research-gate.sh verify-metadata /tmp/chousa-r26-falsify-FSimplifyRegistry/review-fixtures/entry.md --root /tmp/chousa-r26-falsify-FSimplifyRegistry --registry /tmp/chousa-r26-falsify-FSimplifyRegistry/review-fixtures/registry.md
```

Fixture sequence and actual child exits:

| Fixture | Exit | Observed result |
|---|---:|---|
| Valid 4-line header + body heading | 0 | clean |
| Same header + 65,536 newline body bytes | 0 | output byte-identical to control |
| Same header + 65,536-byte long-line body | 0 | output byte-identical to control |
| Registry NUL appended | 2 | expected usage refusal, `metadata registry refused: nul` |
| Entry NUL appended after body heading | 1 | expected critical entry refusal, `reason=nul unparsed` |
| Entry has second hard link | 1 | expected critical entry refusal, `reason=multilink unparsed` |
| Registry has second hard link | 2 | expected usage refusal, `metadata registry refused: multilink` |
| Registry table, blank/heading, then 1,024 fake queued rows | 0 | clean; later body not parsed |

The three body/control stdout digests were all `81057505c66d6fc66f2188553b731f4657e6d38da8241ecfa4262f7d01219b35` (runs occurred within one timestamp second; no normalization). Observed wait4 RSS KiB / elapsed seconds: control 15,928 / .018; newline 16,452 / .018; long-line 16,452 / .018. Small-shape RSS is noisy and can include launcher/inherited high-water effects; it is supporting observation, not a proof of the 8 MiB C1 prediction or a global memory budget. Structural source inspection supplies the narrower no-body-line-array observation.

All exact commands, exits, expected statuses, hashes, RSS and raw stderr are retained in `review-fixtures/results.json`; full per-fixture stdout/stderr are retained as `<fixture>.stdout` and `<fixture>.stderr` in that sandbox directory. Expected negative controls are not regressions. The raw entry failure lines are:

```text
FINDING META_ENTRY_REFUSED severity=crit surface=metadata obs=entry=entry.md reason=nul unparsed
FINDING META_ENTRY_REFUSED severity=crit surface=metadata obs=entry=entry.md reason=multilink unparsed
```

No full selftest/build/lint/formatter, date differential, full measurement probe, 8 MiB amplification fixture, mutation test, external research, or agent delegation was run. A mistaken read of `corpus/CORPUS.md` returned not found; subsequent sandbox glob found no CORPUS.md, so no assertions here rely on an unavailable local copy. The claim's append-only contract correction and the differential's declared pipe exclusion define this report's tested scope.

## Shared-tree protection and stopping point

Only this scoped report was written in the lane. Production reads used the shared tree solely for initial documents/hash identity; all execution and fixtures used the immutable private clone. A `git ls-files -z` inventory plus SHA-256 of 510 existing tracked regular files was captured before checks and recomputed after checks: zero changed/missing tracked file bytes. All 13 initially hashed live inputs also matched their receipt values. This is byte-identity evidence for tracked files, not a claim that concurrently produced untracked peer reports or Git metadata were frozen. No lane index/jj/runtime/config/routing writes were issued.

Stop here: the next substantive deletion would remove live parsing/storage or a distinct refusal defense, harming calibration or operability. The sole dead-binding candidate remains unmodified and unproven by LSP; there is no claimed simplification improvement to ship.
