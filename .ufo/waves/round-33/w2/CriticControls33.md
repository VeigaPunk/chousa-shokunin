# CriticControls33 — pre-data shortcut coverage

## Scope, axis, verdict

**Axis: operability.** Review lenses are whether the control wave distinguishes top-level reading from fixture-specific extraction, and whether its evidence supports that distinction. These are not additional scored axes.

**Verdict: INCONCLUSIVE for landed C1; a concrete control-coverage objection is supported by static evidence.** [INFERENCE] A small, deliberately non-general extractor can match every generated v2 record without a JSON parser or a string-aware structural walk. No such extractor was implemented or scored here. This is not a measured 156/156 result, a landed-gate counterexample, a kill-rule miss, or a canonical judgment.

This was the assigned reasoning-only attack on the pre-data controls. Claims were read first, including governing Design v2. Paths below are relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

Abbreviations:
- **C**: `corpus/evidence/round33/claims.md`.
- **K**: `corpus/evidence/round33/c1-count-v2.py`.
- **S**: `.ufo/waves/round-33/controls/L1-v2-rescore/summary.txt`.
- **A**: `.ufo/waves/round-33/controls/L1-v2-rescore/CtlC1StripNested--control-a-s3341.json`.
- **H**: `.ufo/waves/round-33/w1/CtlC1StripNested/control-a.sh`.

## What the existing controls actually establish

- The full opened rescore summary contains no non-oracle 156/156 result; its highest non-oracle result is 142/156 for `c-differ-only` on seeds 3341/3342 (**S:1-68**, especially **23-28**). That control retains Python top-level readers and changes duplicate policy, so 142 is not a demonstrated ceiling for non-parsers (`w1/CtlC1DupPolicy.md:29-36`).
- The useful starting point is the much simpler regex-strip control: **130/156**, comprising every ordinary nested class, all flat records, and 4/6 nested-confuser records. Its only misses are **24 duplicate records plus 2 nested-confuser records** (**A:15-30,32-189**). The companion seed has the same class vector (`CtlC1StripNested--control-a-s3342.json:15-30`).
- Its implementation saves the outside braces, repeatedly deletes innermost objects and arrays by regex, and then uses the old raw-line field regexes (**H:1109-1143**). It has neither string-aware structure handling nor duplicate rejection; the control report explicitly says those parts were unchanged (`w1/CtlC1StripNested.md:19-23,60`).
- `CtlC1Shortcut` was registered (`w1/swarm-registry.json:98-107`), but **S:1-68** contains no score for it. The assignment's disclosed safety-filter hold therefore supplies no evaluated shortcut rejection. This review does not independently characterize that hold or claim to have searched every historical artifact.

## Concrete cheap shortcut: six literal masks + the existing regex strip + repeat counting

**[INFERENCE; construction, not an executed implementation.]** Keep the base source-resolution/content/hash verification and its output/exit behavior. Replace only field extraction and duplicate detection as follows:

1. Before stripping containers, replace the **six exact serialized string literals** `J(CONFUSERS[c])` with an innocuous string such as `"x"`. This is six literal substitutions, not a general string lexer. The six constants are public and fixed (**K:71-80,135-136**).
2. Apply the already tested control-a deletion loop (**H:1114-1121**). Do not validate the resulting text as JSON; retain the old field regexes (**H:1125-1143**).
3. Count literal string-valued occurrences of the seven read-key names in the remaining text; more than one means invalid, including identical values. Retain the record's id for the generated duplicate-id cases, which always agree (**K:94-95,243-267**).

Why this covers the entire generator, not merely one seed:

| Generator invariant | Consequence for this shortcut |
|---|---|
| Ordinary generated words use only the fixed alphabet; spans/claim text are combinations of those words; ids and source paths use fixed ASCII forms (**K:67,121-132,157-167,180-183,317-322**). | Those string bodies cannot contain braces, brackets, escaped quotes, or fake member syntax. |
| All exceptional structure-looking string bodies come from the six `CONFUSERS`, placed only under ignored keys (**K:73-80,268-282**). | Literal masking removes every string-contained bracket/brace before the string-unaware deletion loop sees it. No generated read value is changed. |
| Containers are attached under generated unknown keys, while the read fields at the root are simple strings (**K:139-148,182-197,200-242,268-298**). | After masking, every remaining bracket is structural. Removing nested containers cannot remove any root read field. Nested-only fields disappear, including numeric nested `line`. |
| Root serialization is always exactly `J(key) + ": " + value`, separated by `", "` (**K:322**). | An exact-format literal occurrence counter suffices. No general member-name or value grammar is needed. |
| The duplicate class contains two string-valued occurrences of its selected root key; duplicate ids are equal (**K:243-267**). | A raw count on the stripped text rejects all 24 counted duplicates without pair-preserving JSON parsing. |

Thus the restricted extractor returns the same read-field strings/presence and duplicate outcome as a genuine top-level reader **on every input the current generator can produce**. Keeping downstream verification then preserves the oracle's counted observations and drifting exit. Existing feasibility receipts demonstrate 156/156 with those genuine top-level results (`controls/L1-design-v2/c1v2-oracle-s3312.json:3-32` and `c1v2-oracle-s3313.json:3-32`); the oracle builder changes only readers and duplicate rejection (`controls/L1-design/mk-oracle.py:2-3,7-40`). The counter checks observed statuses, two finding sets, exit 1, and DRIFT—not how fields were extracted (**K:362-391**).

**Predicted result [INFERENCE]: 156/156 on every seed**, provided downstream behavior is retained. The observed 130/156 vector independently localizes the needed changes: mask the confusers without changing read values, and reject the 24 duplicates. Fresh ids, member order, filenames, and shuffled file creation do not vary the six literals or this grammar (**K:307-332**). This shortcut uses no hidden truth, class labels, receipt access, or seed prediction. It still reads sources; the objection is specifically to evidence for *top-level parsing*, not to the source-reading controls.

## Minimal structural counterexample to the proposed shortcut

**[INFERENCE; not run against base, landed, or a mutant.]** Suppose local `src/a.md` contains:

```text
alpha beta gamma delta.
other words.
```

Use this valid record, with no top-level `line`:

```json
{"id": "c", "source": "src/a.md", "span": "alpha beta gamma delta", "expect": "supported", "meta": {"note": "}", "line": "2"}}
```

The one-character string `"}"` is not one of the six literal masks (**K:73-80**). Control-a's first object substitution stops at the brace *inside that string*, deleting `{"note": "}` but leaving `", "line": "2"}` in its working text (**H:1114-1121**). The raw reader then sees exactly one `line="2"` (**H:1125-1143**), so repeat counting does not save it. With the unchanged line-binding verifier, the predicted observation is **mislocated**, plus `CLAIM_LINE_MISMATCH`, rather than supported (line-binding behavior: `tools/research-gate.sh:1743-1767`).

The contract instead says that nested `line` changes nothing and `}` inside a string is never structure (**C:29-38**). It therefore requires supported for this source/record relationship. This is a concrete counterexample to the *shortcut's generality*, not evidence that the landed scanner has this defect. Base-versus-landed outputs were not executed or measured here.

## Smallest safe correction and interpretation

1. Preserve frozen v2, TOTAL, P1, and the kill rule (**C:120-129**). Do not retrofit the counter after candidate data, and do not present an unexecuted shortcut as a recorded passing control.
2. State the actual evidence boundary: the listed controls miss; that does **not** establish that cheap fixture-specific extractors cannot pass. In particular, string-unaware stripping and duplicate omission were tested together, but the masked-and-repeat-counted combination above was not scored in the opened summary.
3. The smallest additional falsification case for this channel is the record above, paired with its version without `meta`, asserting unchanged observation and findings. Legal whitespace reserialization is another independent discriminator for an exact-`": "` shortcut (**K:322**); neither check needs to alter the frozen 156-record predicate.

This is an evidence-coverage limitation and a potential fixable extractor defect, not an established landed defect. Whether the finite control portfolio warrants the broader operability claim belongs to the canonical judge. A repair must not hard-code the six strings: the invariant to preserve is the contract's string/content and root-membership distinction (**C:29-38**).

## Commands, provenance, and limits

Executed shell commands, both exit **0**, cwd lane root:

```sh
timeout 10s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w2/CriticControls33
timeout 10s sha256sum corpus/evidence/round33/c1-count-v2.py tools/research-gate.sh .ufo/waves/round-33/controls/L1-v2-rescore/summary.txt
```

Hash output:

```text
cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514  corpus/evidence/round33/c1-count-v2.py
94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e  tools/research-gate.sh
29888beb805c4ae088154d8398196f184835cc91817c2008a853f9069cc2c61e  .ufo/waves/round-33/controls/L1-v2-rescore/summary.txt
```

All other evidence was opened with read/search tools at the cited paths/lines. **Counter/gate/test invocations by this seat: zero; new scoring receipts: none.** Accordingly there is no undisclosed landed-counter run. No implementation, production edit, Git/JJ write, network access, install/update, background process, or process signal occurred. The scoped report is the only file written. D1-D5 repairs, sources, knowledge, and quality rows were not independently evaluated in this controls-only assignment.
