# DiffToolB — round 29 N-version differential

**Verdict: HOLDS for the scoped differential; C1 was not falsified by this probe.** The independent implementation was present. There were **0 verdict disagreements across all 40 frozen fixture items and all 33 held-out items**. Both implementations matched every frozen fixture label: **40/40 each**. This does not establish the separate frozen `130/130` predicate, which this seat did not run or change.

Axes: operability, frozen-contract conformance, differential agreement, exact restoration/no harm.

## Execution and actual output

Working directory for every execution: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

```text
timeout --kill-after=5s 600s python3 .ufo/waves/round-29/falsify/DiffToolB/run-differential.py
```

Batch exit: `0`. It ran the following four independent processes concurrently; the receipt records each fully expanded command:

```text
timeout --kill-after=5s 590s python3 <DiffToolB>/guarded-run.py <trace> <implementation> verify --items <items> --registry corpus/SOURCES.md
```

`<implementation>` was the unchanged `tools/quote-reopen.py` or `.ufo/waves/round-29/build/ExecToolB/quote-reopen-b.py`. `<items>` was the frozen fixture or `DiffToolB/held-out-3col.tsv`. The 3-column copy was checked byte-for-text against all original rows with only `origin` removed; it contains all 33 items.

| Run | Exit | Rows, in input order | VERBATIM | ABSENT | TOO_LONG | NO_SOURCE | UNREACHABLE |
|---|---:|---:|---:|---:|---:|---:|---:|
| Landed, fixture | 1 | 40 | 14 | 20 | 3 | 3 | 0 |
| Independent, fixture | 1 | 40 | 14 | 20 | 3 | 3 | 0 |
| Landed, held-out | 1 | 33 | 26 | 3 | 0 | 0 | 4 |
| Independent, held-out | 1 | 33 | 26 | 3 | 0 | 0 | 4 |

Exit `1` is required by the frozen contract whenever any item is not `VERBATIM`; it is not a run failure. All four stderr files were empty. Longest initial execution: `14.136 s`.

**Every item where verdicts disagree: none.** Details are descriptive and intentionally differ between implementations; they were not compared as verdicts. Full per-item outputs, summary lines, commands, timings, before/after hashes and comparisons are in [differential-receipt.json](DiffToolB/differential-receipt.json) and the four `*.stdout` / `*.stderr` files beside it.

## Contract diagnosis and limits

- The 40 frozen labels agree with both implementations. Neither implementation needs to be preferred over the other on any tested item.
- Both held-out runs return `ABSENT` for `h05`, `h20`, `h21`. `h05` is the supplied summary-not-verbatim item. The two PubMed requests returned HTTP `203` HTML challenge pages, so those outcomes are not evidence that the intended articles lack the quotes.
- Both return `UNREACHABLE` for `h10`, `h13`, `h24`, `h29`. `h10` and `h29` have excluded `application/pdf` content types; `h13` returned HTTP `403`. Those three refusals follow frozen contract lines 95–97.
- **Network-boundary caveat for `h24`:** the registry RFC URL returned `301` to `https://www.rfc-editor.org/info/rfc9111/`, which is not a source-column URL. The required exact-URL guard blocked that follow-up before sending it. Thus `h24` establishes agreement under the assignment's network bounds, not behavior after an unrestricted redirect. It is not reported as a tool defect.
- The other 26 held-out items were `VERBATIM` in both runs. Held-out agreement is not independent ground-truth labeling or proof against shared bugs.
- The wrapper executes the actual implementation files with `runpy`, preserving their CLI/file identity. It allows only GET to exact fragment-stripped registry source URLs, records response status/headers/body captures, removes proxy variables, and disables bytecode writes. No forbidden redirect target was fetched. Explicit `--registry` was used; other registry-resolution paths were not tested.

## One required scratch-only mutation probe

**Mutant:** `/fast/scratch/hyaku/chousa-r29/w2/DiffToolB/tools/quote-reopen.py:55`, changing only `MAX_WORDS = 25` to `MAX_WORDS = 26`.

**Expected detector:** the same 73-item fixture/independent-held-out agreement detector on pristine, mutated and restored bytes. A 26-word quote would expose this defect: the frozen contract requires `TOO_LONG` before fetching. These fixed sets have no 26-word item; their recorded word counts run from 5–23 and 34–35. This detector is diagnostic, not a re-scaled C1 predicate.

Commands, each from the lane root:

```text
timeout --kill-after=5s 600s python3 .ufo/waves/round-29/falsify/DiffToolB/mutation-detector.py pristine
timeout --kill-after=5s 600s python3 .ufo/waves/round-29/falsify/DiffToolB/mutation-detector.py mutated
timeout --kill-after=5s 600s python3 .ufo/waves/round-29/falsify/DiffToolB/mutation-detector.py restored
```

| Bytes | Detector output | Detector exit | Verifier exit |
|---|---|---:|---:|
| Pristine | `DETECTOR_MATCH=73/73` | 0 | 1 |
| Mutated | `DETECTOR_MATCH=72/73` | 1 | 1 |
| Restored | `DETECTOR_MATCH=73/73` | 0 | 1 |

**Mutation verdict: INCONCLUSIVE, not killed.** The only mutant-run miss was `h14`: expected `VERBATIM`, observed `UNREACHABLE`. Its captured OpenAI response was HTTP `403`; pristine and restored runs matched. That is a live-response variation, not evidence that the length defect was detected. [INFERENCE] The missing 26-word boundary case leaves this specific defect unexercised by these 73 items; no contract or fixture change is proposed.

SHA-256 evidence:

```text
pristine/restored 72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea
mutated           16a09a301b5d8f09f4d33ae1fad9a7fea421b64b361e08a39b8c8bd4fd1e6275
independent B     37dc4ae35983ff5e91124907886b8600b409b3664dd261071f56f339e1562505
```

Exact restoration was additionally established by `timeout 10 cmp` between scratch and landed source, and between pristine and restored stdout; the final hash/compare command group exited `0`. Frozen claim/counter/fixture, registry, held-out input and independent implementation hashes were unchanged at the final check. Detailed phase commands, scores, hashes and transport evidence are in `pristine.receipt.json`, `mutated.receipt.json`, `restored.receipt.json`, `*.network.json` and [restoration-evidence.json](DiffToolB/restoration-evidence.json).

No production source, sibling file, index or jj state was written. No git/jj write command, subagent, detached job, service, other runtime, install or update was used. All launched execution processes were reaped, with process-group cleanup attempted in `finally` blocks. No repair or corpus row was added: this seat reports evidence only.
