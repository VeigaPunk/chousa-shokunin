# CritC1Shapes — frozen C1 shortcut-shape review

Access date: 2026-10-23. Scope: read-only adversarial review of frozen design v1, not a candidate review or a runtime judgment. No code, gate, counter, shell command, or other runtime was executed. No production files, counter, Git/JJ state, or receipts were changed. This report is the only artifact written. No tools were installed.

## Axes and evidence boundary

**Named scored axis: operability.** This is the lane's sole scored axis (`SCORECARD.md:3-13`); the canonical definition is runnable artifacts producing their stated outcome (`/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/AXES.md:9-16`). Equality, boundary correctness, line binding, and honest measurement are dimensions of this review, not newly invented scored axes. False claims of full verification would also implicate calibration; that is a risk, not an axis verdict here.

Frozen C1 requires 32768..65536-byte delimited occurrences, rejection of missing/nonadjacent/glued spans, exact named start/end lines, and preserved short verdicts (`corpus/evidence/round34/claims.md:34-43`). P1 requires two fresh 30/30 runs and no committed lower run (`:55-63`). The counter's declared limitations must not become implicit expansions of the claim (`:85-88`).

Evidence notation below:

- **C** = `corpus/evidence/round34/c1-count.py`.
- **G** = `tools/research-gate.sh`.
- **F** = `corpus/evidence/round34/claims.md`.
- All conclusions about controls and probabilities are **[INFERENCE]**, derived from the opened code, not measured scores. Probabilities assume ordinary independent-looking random draws and no accidental alternative matching occurrence. An arbitrary deliberately selected seed need not follow that model.
- **D** = a class forces a mismatch for the stated shortcut, independently of its random content, under the generator's intended truth model.
- **P** = a class catches it only probabilistically; formula/estimate given.
- **U** = no generated discriminating example for the specified regression; changing the seed does not repair that missing distinction. U is not an observed 30/30 receipt.

Two located quotes, each under 25 words:

> “Change one letter at a letter offset in [lo, hi] to a different letter.” — C:138-143, accessed 2026-10-23.

> “Short spans (64..4096 bytes) keep their verdicts.” — F:43, accessed 2026-10-23.

## Important control-construction qualification

The raw base still has E2BIG in **both** helpers: G:1563-1578 and :1590-1605. Merely adding a line-binding shortcut, normalizing case, or adding a guard to that base cannot produce 30/30: it leaves the original long search broken. Likewise, replacing only `tok_span_at` leaves `tok_span_all` broken at G:1827.

The one-line changes below are **control-seat mutation specifications**, not applied or tested shell patches. `MATCH := ...` means replace the literal-occurrence predicate in a scratch control's shared search body, used by both helpers. `w` is an original-length candidate window; `s` is the span; `n=len(s)`; offsets and outer boundary/line checks remain original unless the row explicitly changes them. `OCC := ...` changes occurrence generation instead. This preserves the identity of the counterexample rather than accidentally testing truncated endpoints or broken line arithmetic. A seat must implement the described scratch reader; an undefined helper name is not an implementation.

Exact one-line hook locations in the base are G:1806 (`if <control_at> "$hay" "$span"; then`) and G:1827 (`done < <(<control_all> "$hay" "$span")`). Whole-record controls can instead replace the dispatch at G:7834 with a scratch control reader. Those hooks must not be mistaken for a complete one-line C1 repair. The tables name the minimal behavioral line each control should change.

## Highest-priority counterexamples

### 1. Two unmutated shoulder bands: systematic partial verification

Long head mutations occur only at 0..63, tail mutations only at n−64..n−1, and middle mutations only at 8192..n−8192 inclusive (C:166-174). Therefore a control can compare only:

`MATCH := w[:64]==s[:64] && w[8192:n-8191]==s[8192:n-8191] && w[-64:]==s[-64:]`

It ignores **16,255 bytes** per long span: offsets 64..8191 (8,128 bytes) and n−8191..n−65 (8,127 bytes). Every generated letter mutation is nevertheless examined. Every long-split insertion point is also inside the examined middle: n≥33000 and k lies in [n/4,3n/4), so 8192<k<n−8192 (C:175-181). Glue and line checks can remain correct. Thus no class deliberately exposes the omitted bands (**U**); fresh seeds only change bytes inside the same coverage geometry.

**Strongest local counterexample specification:** use the same source/record construction but change one letter at offset 4096 or n−4096. Those offsets are within the C1 length/one-letter-change contract (F:35-39), outside every long mutation class, and outside the control's examined bytes. Such a record would be wrongly supported. This is a counterexample specification, not an executed fixture.

**Smallest safe correction:** the real matcher must compare all bytes, not three probes. For pre-data counter design, sample single-letter mutations over all letter offsets, including both shoulders; do not patch frozen v1 here. A shoulder-blind control receipt is the useful next evidence.

### 2. Fixed independent halves: random split placement usually hides non-adjacency

`OCC := occurrences(s[:m]) paired with occurrences(s[m:]), m=n//2, with no adjacency/distance requirement`

Check the true *outer* boundaries only; do not require token boundaries at the artificial half-cut. Line controls can enumerate prefix starts and use the original span newline count. This control checks all letter identities but not assembly into one occurrence.

The generator's split is at a **random separator**, not the control's midpoint (C:175-181). Usually one queried half crosses the inserted filler and is absent, so the shortcut returns the correct unsupported verdict for the wrong reason. The split exposes missing adjacency only when its separator is at/adjacent to the control cut and the replacement outer separator agrees, or through an accidental alternative occurrence.

Approximation: mean word length is 5.5, separator spacing about 6.5 bytes (C:108, :115-121). The eligible middle-half contains roughly n/13 separators. The two positions adjacent to the half-cut are separators with expected total 2/6.5; matching replacement separator contributes about 1/2 (C:131-132). Therefore a split record exposes this control with probability about **2/n**, not probability one. With two split records around 50,000 bytes, detection is about **0.00008 per seed**, so this component survives about **99.992%** of seeds; two independent fresh seeds still survive about **99.984%**. These estimates exclude anchor collisions and implementation/output faults.

By contrast, a control that somehow splits at the **generator's actual k**, checks both pieces anywhere, and ignores adjacency is **D**-caught by both long-split records. Calling both implementations merely “independent halves” conceals this difference.

**Smallest safe correction:** require consecutive offsets from the same candidate occurrence. To test the broken assembly operation, construct source gaps/permutations at the control's seam as well as random gaps. This is pre-data design advice, not a frozen-counter edit.

### 3. Order-insensitive fingerprints: single substitutions are unusually easy negatives

`MATCH := anchors_and_original_length && sum_bytes(w)==sum_bytes(s)`

A single changed lowercase letter changes the sum by a nonzero integer in −25..25 (C:138-143). Thus an unmodded sum, a sum modulo >25, XOR, full byte histogram, or word multiset can distinguish the original aligned window from **every generated one-letter mutation**, without proving byte order. With short endpoint anchors, preserved boundaries/lines, and a distance/length check that rejects the inserted gap, this is a plausible near-certain 30/30 shortcut. Other accidental candidate windows make its absolute success probability implementation-dependent; there is no defensible measured decimal here.

**Counterexample specification:** inside an unanchored interior region, swap two different letters; for stronger histograms, swap two distinct equal-length words. Length, separators, endpoint anchors, byte sum, XOR, byte histogram, and the word multiset are unchanged, but the span is not verbatim. No class performs a balanced edit or permutation (C:154-206). **U** for that missing distinction.

**Smallest safe correction:** fingerprint as a filter, then compare candidate bytes exactly. Adding more single-letter mutants cannot test order sensitivity. A cryptographic/rolling hash followed by exact equality is not this shortcut and should not be rejected as one.

## Shortcut catalogue

The catalogue covers the observable shortcut dimensions: disposition priors, lengths, examined bytes/content transforms, occurrence assembly, boundaries/lines, metadata/test awareness, and output/provenance. Their compositions are also shortcuts; arbitrary programs cannot be finitely enumerated as individual implementations.

### A. Labels, length classes, and fixed counts

Class totals derived from C:75-91: long = 9 supported + 13 unsupported + 2 mislocated; short = 3 supported + 3 unsupported. Overall = 12/16/2. All records nevertheless carry `expect=supported` (C:225).

| Shape | One-line control mutation | Defeat / per-seed estimate | Evidence |
|---|---|---|---|
| Do nothing / reject every long span | `MATCH := false` for n≥32768 | **D**: 11 long non-unsupported records miss; short-exact ceiling 19/30. This is the frozen base expectation, not a new run. | F:65-71; C:75-89 |
| Accept every long span / trust `expect` | `MATCH := true` for n≥32768; or `observed := expect` | **D**: 13 long unsupported + 2 mislocated miss if all long dispositions become supported; with short exact, 15/30. Trust-expect for all rows gives 12/30. | C:75-89, :225, :295-298 |
| Accept only narrow edge band without searching | `if 32768<=n<=32900: supported` | **U** for that branch: only long-edge occupies this range; every edge record is supported. Alone atop broken base it improves only the edge cases, not 30/30. It can be composed with another shortcut. | C:155-174, :176, :183, :186, :189 |
| Single-line long span automatically supported | `if '\n' not in s: supported` | **U** for this branch: the only deliberately newline-free long class is long-verbatim-1l. Other long classes force a newline through `Gen.span`. No single-line long negative exists. | C:124-129, :154-199 |
| Refuse the untested top of the contract | `if n>65009: unsupported` | **U**, zero deliberate detection: `text` overshoots its requested target by at most 9 bytes, and every non-edge long target is ≤65000. Lengths 65010..65536 are absent. | C:111-125, :155-189; F:35 |
| Refuse selected unsampled lengths / lookup a length-to-label table | `observed := label_by_length[n]` | **P**, not deterministic protection. Positive and negative distributions overlap, but a seed need not contain contradictory labels at identical lengths. Fresh lengths frustrate memorization; they do not prove that length was unused. A precise success probability depends on the table/rule. | C:124-125, :154-206 |
| Fixed quotas / record-order labels | `observed := next_from_fixed_label_multiset` | **P**. Idealized blind allocation of 12/16/2 labels: 1/[30!/(12!16!2!)] = 1/13,233,463,425 ≈7.56e−11 per seed, plus correct finding placement. Not zero. | C:75-91, :214-215, :295-298 |
| Exploit 24/6 split and the four line-bearing rows | `observed := quota_by(is_short,has_line)` | **P**. With no content work: 1/[C(6,3) C(20,7) C(4,2)] = 1/9,302,400 ≈1.08e−7. With exact short handling and automatic edge/single-line positives: 1/[C(16,3) C(4,2)] = 1/3360 ≈2.98e−4. These are illustrative quota guesses, not optimal classifiers. | C:75-89, :157-165, :188-205, :214-227 |
| Globally choose “unsupported” except the known-positive structural tags | `if edge_or_singleline: supported; else unsupported` | **D** for this specific rule: at least long-verbatim-ml and line-bound remain wrong, as do mislocated rows. Structural tags alone do not identify all truth. | C:75-89, :154-199 |

The class split and `expect` value are recognizable signatures of this test, not secret labels. Even a roughly 0.99992-survival shortcut is not made safe by two seeds; independent success probabilities multiply, not become zero.

### B. Which bytes are actually examined

For aligned sampling below, retain original-length boundaries and line coordinates. Truncating `span` itself before invoking the base helpers also changes right-edge and newline semantics; that is a different, more broken control.

| Shape | One-line control mutation | Defeat / per-seed estimate | Evidence |
|---|---|---|---|
| Prefix-only ≤8192 bytes | `MATCH := w[:64]==s[:64]` | **D**: all 2 tail + 3 middle mutations leave that prefix unchanged, so their original aligned windows are falsely accepted. | C:169-174 |
| Suffix-only ≤8191 bytes | `MATCH := w[-64:]==s[-64:]` | **D**: both head + all 3 middle mutations leave that suffix unchanged. | C:169-174 |
| Prefix+suffix only, even with distance checked | `MATCH := w[:64]==s[:64] && w[-64:]==s[-64:]` | **D**: all 3 middle mutations are missed. Distance checking can reject splits but cannot repair this. | C:166-181 |
| Fixed/random sparse byte sampling | `MATCH := all(w[i]==s[i] for i in sampled_offsets)` | **P** unless an entire mutation class is omitted, then **D**. If head/tail are fully covered and middle coverage fractions are q1,q2,q3, chance all 3 middle mutants are caught is approximately q1·q2·q3. Equal q gives q³: q=.01 → 1e−6 pass through the mutation classes; q=.99 → .970299. | C:138-143, :166-174 |
| Shoulder-blind three-region comparison | `MATCH := head64_equal && middle[8192:n-8191]_equal && tail64_equal` | **U** for omitted-byte verification; see highest-priority finding 1. | C:166-181 |
| Compare first/last line only, or special-case multiline | `MATCH := selected_lines(w)==selected_lines(s)` | Usually **P** for random mutation positions; exact rate depends on which lines are retained. First-line-only also reduces to a prefix and misses tail/middle unless a second bug rejects positives. Single-line negatives are absent, so the single-line accept branch is **U**. | C:117, :124-129, :154-174 |
| Only longest word / a few vocabulary words | `MATCH := chosen_tokens(s) occur in source` | **D** if fixed endpoint windows exclude all middle edits; otherwise **P** according to sampled mutation coverage. Long-split defeats mere all-word set membership **D** because every original word is still present across its two halves. | C:138-143, :175-181 |
| Ignore identity of lowercase letters; compare separator/word-length masks | `MATCH := map_letters_to_x(w)==map_letters_to_x(s)` | **D**: all 7 long letter mutations preserve the mask. All 3 short mutants do too if the shortcut touches short spans. Separator statistics alone cannot detect a letter substitution. | C:108-143, :166-174, :203-206 |
| Compare only lengths, newline/space counts, or letter-vs-separator counts | `MATCH := length_and_separator_statistics(w)==...` | **D** for the same 7 long mutants: substitutions retain all those quantities. | C:138-143, :166-174 |
| Byte sum / XOR / histogram / unordered words plus anchors | `MATCH := anchors && fingerprint(w)==fingerprint(s)` | **U** for order sensitivity; single-letter mutation classes actually make this shortcut look good. Absolute 30/30 probability depends on spurious windows and alignment. See finding 3. | C:138-143, :154-206 |
| Ignore whitespace identity or collapse separator runs | `MATCH := normalize_ws(w)==normalize_ws(s)` | **U** for whitespace equality: no negative changes only space/newline, and no negative inserts only separator whitespace. The split inserts ≥300 bytes of letter-containing filler, not a mere separator. Correct coordinate remapping is needed for line rows. | C:117-132, :166-181, :188-206 |
| Case-insensitive long comparison | `MATCH := lower(w)==lower(s)` | **U**: all fixture letters are lowercase; changed letters are different lowercase letters. A case-only mismatch is never generated. This can violate verbatim matching on ASCII-letter inputs, unlike explicitly excluded non-ASCII content. | C:92, :108, :138-143; F:35-39, :85-88 |
| Vocabulary/grammar eligibility instead of generic input support | `if span has token length outside 2..9: unsupported` | **U**: spans always consist of 2..9-letter vocabulary words with single space/newline separators and letter endpoints. Any unsupported branch for longer ASCII words, uppercase words, repeated separators, or edge whitespace is unexercised. Non-letter/non-ASCII source cases are explicitly outside the counted C1 claim, not newly measured harm. | C:108-129; F:85-88 |
| Reject “novel” words rather than compare bytes | `MATCH := every_span_word_is_in_source_dictionary` | Standalone **D** on split, and often glue. With separate topology/boundary checks, mutation rejection is only **P**: the changed word can be another real vocabulary word. Under the approximate 4000-word/8-length model, membership probability for length L is 1−exp(−500/26^L); letter-weighting L/44 gives about 2.6% membership across lengths before source-coverage adjustment. Thus this composite might correctly reject all 7 long mutants roughly 83–85% of seeds, not guaranteed. This estimate is heuristic and correlated draws weaken the independence assumption. | C:108, :138-143, :166-187 |

Source-wide vocabulary is not explicitly written out, but words repeat within and across the 30 sources (C:108-121, :210-223). A detector can learn it from the fixture; randomized spelling does not remove the shared finite-vocabulary signal.

### C. Assembly, positions, and source topology

| Shape | One-line control mutation | Defeat / per-seed estimate | Evidence |
|---|---|---|---|
| Generator-aligned pieces anywhere | `MATCH := occurs(s[:k]) && occurs(s[k+1:])` | **D** on both split rows if k is the actual generator split; no adjacency is checked. | C:175-181 |
| Fixed midpoint halves anywhere | `MATCH := occurs(s[:n//2]) && occurs(s[n//2:])` | **P**, approximately 2/n detection per split row; see finding 2. Mutation classes do not expose assembly because both halves collectively check every byte. | C:166-181 |
| Fixed K chunks, independently present, unordered or only loosely ordered | `MATCH := all(occurs(chunk) for chunk in fixed_partition(s))` | **P**. A random gap usually damages one queried chunk and is correctly rejected. With b control seams in the middle-half split region, exposure is roughly 2b/n per split row, assuming long unique chunks. Short chunks may recur elsewhere and raise false-accept probability. No class deliberately permutes intact control chunks. | C:175-181 |
| Prefix and suffix anywhere, no distance requirement | `MATCH := occurs(head64) && occurs(tail64)` | **D** from middle mutants even before split analysis; both unchanged anchors exist. The split also preserves both anchors **D**. | C:169-181 |
| Prefix+suffix at correct distance, unchecked interior | `MATCH := endpoints_equal && end-start==n` | **D** from 3 middle mutants; rejects generator splits but is still not a full comparison. Combine with a byte sum and it becomes the order-blind shape above. | C:169-181 |
| Search only generously padded records / reject tight source | `if len(hay)-n<403: unsupported` | **U**: ordinary sources contain two fillers of ≥200 bytes, two separators, and final newline; other constructions have even more excess. No span touches BOF/EOF. A source exactly equal to its span is a valid C1 case but absent. | C:134-135, :154-206; G:1525-1550 |
| Impose a small whole-source cap / limited search prefix | `if len(hay)>140000: unsupported` | **U**: largest possible fixture is the two-copy line source, ≤138050 bytes: 2·65009 + 2·3009 + 2009 + 5. The base permits sources up to 8 MiB; large-source long matches are not represented. | C:111-125, :134-135, :188-192; G:72-74 |
| Cache observed solely by source path, ignoring span/line | `observed := cached_by_source[path] or evaluate_once()` | **U** for cache-key correctness: one source per record, so no normal cache reuse is challenged. Filename collision probability is approximately C(30,2)/2^64 ≈2.36e−17 per seed; collisions overwrite files and are not a principled cache control. | C:218-239 |
| Reject mixed/multiple alternatives or process only one raw occurrence | `OCC := selected_occurrence_only` | **U** for mixed valid/glued occurrences: glue records contain only a glued occurrence; line records contain two delimited copies. Some selected-occurrence policies are caught by line-bound; others are not, below. | C:182-199 |

All fixture files end with a newline and all spans start/end with a letter (C:111-129, :154-206). No fixture tests a span beginning/ending with a separator, a span at file boundaries, or a long source region beyond this small padded geometry. These are missing distinctions, not evidence that a candidate actually mishandles them.

### D. Boundaries and line binding

| Shape | One-line control mutation | Defeat / per-seed estimate | Evidence |
|---|---|---|---|
| Boundary-blind substring match | At G:1572 and :1599, `boundary_ok := true` | **D**: 2 left-glued + 2 right-glued records falsely supported. | C:182-187 |
| Ignore only one edge | `boundary_ok := right_ok` or `left_ok` | **D**: the corresponding 2 glued records. | C:182-187 |
| Either edge suffices | `boundary_ok := left_ok || right_ok` | **D**: every glue record retains the other good boundary. | C:182-187 |
| Treat only lowercase letters as word characters | `boundary_ok := outside_char not in a..z` | **U** beyond fixture alphabet: all tested glue is lowercase. Digits, uppercase neighbors, joiner rules, and EOF/BOF transitions are not exercised by these long controls. The base has richer boundary semantics. | C:182-187; G:1506-1550 |
| Reject immediately on a glued first hit, never try a later delimited hit | `OCC := fail_if_first_raw_hit_glued` | **U**: no generated file combines an earlier glued hit with a later valid hit. | C:182-199; G:1553-1555 |
| Ignore `line`, or force requested coordinates | `bound := true` | **D**: both long-line-wrong records must be mislocated and carry the finding. | C:188-199, :295-298 |
| All line-bearing claims mislocated | `bound := false` when line present | **D**: both line-bound records name an actual occurrence. | C:188-199 |
| Enumerate only the first occurrence | At G:1827, `OCC := first_delimited_only` | **D**: both line-bound records name the second occurrence. | C:193-196 |
| Enumerate only the last occurrence | At G:1827, `OCC := last_delimited_only` | **U** for completeness: every bound row names the second/final occurrence; every wrong row names neither. This wrong policy can match all four line rows deterministically. | C:192-199 |
| Check start line only | At G:1820, `[[ $l1 == "$line_n" ]]` | **U**: wrong rows shift both endpoints by +1, while bound rows match both. No valid-start/wrong-end row exists. | C:193-199; G:1820 |
| Check end line only | At G:1820, `[[ $l2 == "$line_m" ]]` | **U** for the symmetric reason. | C:193-199; G:1820 |
| Check only range width | `bound := line_m-line_n == newline_count(span)` | **D**: wrong rows preserve range width exactly. | C:197-199 |
| Special-case the precise wrong-line pattern | `bound := line_n != first_start+1` | **U** once a short anchor locates first_start: wrong rows use precisely +1; second starts ≥first_start+3 because the span has ≥1 newline and mid has ≥2. Does not generally verify named lines. | C:124-129, :190-199 |
| Guess bound from large/small requested N | `bound := line_n > newline_count(span)` | **P**: bound rows always pass this inequality; wrong rows usually fail because their head filler is short, but not guaranteed. Exact probability depends on separator realization. Random line positions do not eliminate their highly different distributions. | C:117, :134-135, :190-199 |

A partial repair of `tok_span_at` only is a distinct **D** control: `tok_span_all` still uses the long argv pattern, so two line-bound records cannot bind (G:1590-1605, :1811-1827; F:73-79). That control is not evidence against the last-only or one-endpoint holes.

### E. Metadata, test awareness, and oracle substitution

| Shape | One-line control mutation | Defeat / per-seed estimate | Evidence |
|---|---|---|---|
| Hardcode IDs, filename order, JSON key order, creation order, or mtimes | `observed := lookup(metadata)` | **P**, not a deterministic semantic defense. IDs/names are random; plan/files/keys shuffled; mtimes random. Blind label success follows quota probabilities above under the idealized model. No simple metadata bit is a dependable truth label. | C:214-239 |
| Recognize fixture root/name/shape, run a special path only there | `if root_prefix && count==30 && all_expect_supported: use_fixture_classifier` | **U** for path equivalence: every counter invocation has the root prefix, `claims.jsonl`, mode, and same 30-record shape. Recognition alone does not reveal truth; pair it with any surviving content/line shortcut. | C:214-242, :258-276 |
| Reproduce generator truth from a known seed instead of searching | `observed := replay_generator_truth(known_seed,id)` | **U** once the seed is known: the counter does not test which authority produced the labels. An explicitly supplied seed is in the invoking command's arguments, not intentionally passed to the gate. Access via process/environment state would be environment-dependent, untested here, and is not needed for the shoulder/halves findings. Default seed is from os.urandom and not an argv seed. | C:210-243, :249-253, :274-276 |
| Import/copy the counter's generation logic as the gate's authority | `reader := fixture_generator_oracle` | Same oracle-substitution risk; random content does not protect against regenerating the generator when seed/state is available. This is duplicate authority/false evidence, not a real C1 reader. No such operation was performed. | C:151-243, :295-298 |
| Read the `--keep` truth file during gate execution | `observed := truth_json[id]` | **D** for this simple attempted leak: `truth.json` is created only after subprocess completion and scoring. It is not written beside live claims. | C:268-277, :280-310 |
| Rely on CHOUSA_* seed/oracle injection | `reader := environment_oracle` | The harness removes CHOUSA_* variables (**D** for that exact channel); other environment/process state is not sandboxed by this code. Do not claim the gate is hermetic from this filter alone. | C:274-276 |
| Substitute a flat-fixture-only JSON reader / ignore other expectations | `reader := flat_lowercase_fixture_parser` | **U** for general reader correctness: generated records have only ordinary flat fields, randomized keys, supported expectation, and optional valid line string. C1's counter cannot replace the separately routed E2 parser-confuser counter or other no-harm evidence. Contradiction-marker behavior is explicitly not counted. | C:225-230; F:9-14, :85-88 |

### F. Output-only shortcuts and false provenance

The score parser validates recognized IDs' `observed` and the mismatch-finding set, not a complete gate transcript (C:93-94, :280-305).

| Shape | One-line control mutation | Defeat / per-seed estimate | Evidence |
|---|---|---|---|
| No reader, junk stdout, CLEAN/rc0, setup rc2, timeout | Replace G:7834 with `exit 0`, junk, or a non-reading stub | **D**: all rows score none unless rc=1 and a stdout line begins `RESEARCH_GATE: DRIFT`; missing IDs also score none. | C:272-293 |
| Print all three possible dispositions per ID | `emit supported; emit unsupported; emit mislocated` | **D**: duplicate recognized CLAIM IDs score none. | C:288-293 |
| Emit correct observed labels but no line findings | `emit_claims_only` | **D**: the two mislocated rows fail. Emit a mismatch finding for every row instead and all 28 non-mislocated rows fail the finding-set condition. | C:295-299 |
| Emit synthetic minimal claims from a fixture classifier, not the gate reader | `reader := emit_labels_and_two_mismatch_ids; rc:=1` | **U** for execution provenance once truth is inferred. `expected`, `source`, `at`, `verdict`, summary counts, and non-line findings are not compared. One correct CLAIM per ID plus the right finding set suffices. | C:93-94, :280-305; G:1889-1903 |
| Fake or duplicate summary text / extra unknown IDs / duplicate findings | `summary := "RESEARCH_GATE: DRIFT..."` | **U** for transcript integrity: any matching summary prefix suffices; extra unknown CLAIM IDs and duplicated mismatch findings are not penalized. This does not itself solve hidden truth. | C:280-291, :295-298 |
| Bind a receipt to different on-disk gate bytes than those executed | `receipt_identity := post_run_file_hash` | **U** for measurement binding: C:325 hashes the gate after execution, not before-and-after with an immutable executed blob check. Concurrent mutation is a provenance risk, not an observed event. It does not by itself make a bad score 30/30, and E4 explicitly requires committed-byte binding separately. | C:275-277, :321-329; `corpus/lessons/round-33-verifier-spotcheck.md:168-171` |
| Cherry-pick lucky seeds / hide lower scratch runs | `publish := only_successful_receipts` | The counter itself cannot enforce the committed-run history condition. P1's no-committed-lower-run rule is external and does not turn low detection probability into semantic completeness. No suppressed runs are alleged. | F:55-63; C:316-338 |

## Smallest safe corrections and authority boundary

1. **Implementation:** full original-span equality at every candidate, both outer boundaries, and enough occurrences to satisfy both named line endpoints. Chunking is safe when chunks are tied to consecutive offsets of the same occurrence; a checksum is safe as a rejection filter followed by exact equality. Do not label legitimate stdin/file/streaming transfer of the full literal a shortcut merely because it avoids argv (F:19-43; G:1553-1607).
2. **Pre-data controls:** prioritize shoulder-blind comparison, fixed-midpoint independent halves, and anchor+sum/histogram; then last-only enumeration, start-only/end-only line binding, edge-band accept, single-line accept, and upper-length refusal. These address systematic blind distinctions that the existing obvious accept/prefix/suffix/glue controls do not cover (F:73-80; tables above).
3. **Counter-design advice only:** unrestricted mutation positions, boundary-length negatives, single-line negatives, balanced/permuted interiors, intentional control seams, first/last/mixed occurrences, and independently wrong line endpoints would close the identified distinctions. I did not amend the frozen counter. F:80 routes an actually successful 30/30 control back to design v2 before candidate data; static review alone is not that receipt.
4. **No-harm/measurement:** C1 30/30 cannot attest other expectations, modes, full parser behavior, large sources, or immutable execution identity. Keep E1–E5 and their receipts separate; do not count repairs as a second C1 authority (F:9-14, :85-88; round-33 spot-check:155-173).

The proposed shortcuts trade required equality/line semantics for less work; they are not harmless optimizations under C1. Conversely, explicitly unclaimed non-ASCII/non-letter behavior is a scope limitation, not by itself a C1 miss. This critic does not admit, reject, integrate, score a candidate, or make a canonical Rust judgment.

## What was opened; limits

Read F:1-94 first, then C:1-210 including its docstring, then C:210-342; G:1505-1630, :1680-1885, :1-105, :1885-1905, :7800-7857, and helper locations :292, :448, :1139, :1369-1375. Opened the relevant SCORECARD, round-33 routed defects, Godspeed/UFO/Shokunin skills, canonical protocol/mission/axes/corpus/learning sections, and operator RULES. File-search/read outputs supplied the cited lines; no shell command exit codes exist for this review.

No actual control score, runtime, candidate behavior, hash verification, or probability measurement is claimed. Logical pass estimates assume correct control plumbing, no unintended alternative occurrence, and completion within the counter's 1500-second gate bound (C:73, :275-279). No runtime bound was tested. No control receipts were produced. The frozen hashes in F:3-7 were read, not independently recomputed.
