# ScoutC2Counter — C2 counter and argv witness

Axes: operability of the argv channel (who writes it, what a gate can read, how a record is keyed); calibration of the docstring’s numbers against the committed receipts. No engine was re-run. No MEETS bypass was produced.

Verdict: the counter’s separation rule matches the after receipts (`5/5`, both seeds, `predicate_holds=true`), and the before receipt is `WITNESS_PER_RECORD=2/5` with V2, V3, and V5 passing the legacy witness. The docstring’s “separates only 3/5 (V3 and V5 pass it)” is not supported by that receipt. The code does not hardcode 3; the sentence is stale relative to both the receipt and `corpus/evidence/round36/claims.md` lines 107–111.

Access date for every file below: 2026-10-23.

## (a) Witness channel

Writer. `tools/argv-witness.py` `make_recorder` (lines 199–213) writes a bash script at `<scratch>/rec/grep-recorder`. Each invocation appends one record, then `exec /usr/bin/grep "$@"`. The gate is what causes writes: `argv-witness.py` lines 319–325 put that script’s absolute path in `RESEARCH_GATE_GREP` and `CHOUSA_WITNESS_KEY=1`, then run `bash <gate> verify-claims`. The landed gate (`tools/research-gate.sh` lines 356–361, 389–416, 8208) resolves the override, accepts it only if `--version` contains `GNU grep` (the recorder’s `exec /usr/bin/grep --version` still does), and defines `grep() { "$GREP_BIN" "$@"; }`. Every later bare `grep` in that shell, including `token_matcher_require` (line 1820) and both matchers (lines 1745, 1774), is the recorder.

Record shape (script text, lines 208–210): a marker line, then each argv element as `%s\0`, then a newline. `read_calls` (lines 216–233) splits the log on `marker\n` and splits the first line of each part on NUL.

Where the name and marker come from. Both are drawn inside the witness, not passed to the gate. `main` builds `rng = random.Random(seed ^ 0x5EED)` (line 309) and passes it to `make_recorder`. The marker is `W36CALL-` plus 24 hex chars (line 204). The log basename is 12 random letters plus `.log` (line 205). Both strings are interpolated into the script body. They are not environment variables and not argv of the gate.

What the witness strips and sets. Lines 319–325 drop every inherited `CHOUSA_*` and `RESEARCH_GATE_*`, then set only `RESEARCH_GATE_GREP` (recorder path) and `CHOUSA_WITNESS_KEY=1`. Stderr is redirected to `<root>/_stderr.log` (lines 326–330) and never read back. Attribution uses only the log (line 332) and stdout claim lines (lines 333–337).

What the gate can read.

- From the environment, without opening a file: the recorder path (`RESEARCH_GATE_GREP`) and `CHOUSA_WITNESS_KEY=1`. Not the marker. Not the log path.
- If it opens `RESEARCH_GATE_GREP`: both, in plaintext in the script. The witness docstring (lines 27–30) and `claims.md` lines 126–127 state this: a gate that reads the recorder script can forge log lines. Active anti-instrumentation is out of scope. This seat did not build that gate.
- [INFERENCE] After `grep_pin_verify` (research-gate.sh lines 369–380), the log already contains one record whose first line is the marker, because `--version` is logged before any claim. A gate that finds and reads that log can learn the marker without parsing the script. Same class of anti-instrumentation; not demonstrated.

What the gate cannot make the witness honour. Forged `@@WITNESS@@` / PS4 text on stderr. The witness never scans stderr. A renamed matcher still attributes, because attribution does not look up function names.

`mechanism-witness.py` (the before battery) is a different channel: `bash -x`, `PS4` marker `@@WITNESS@@`, stamps counted on the first executable line of `tok_span_offsets_chunk` / `tok_span_offsets_direct` (lines 64–103, 258–295). It strips `CHOUSA_*` (line 258) and does not set `CHOUSA_WITNESS_KEY`. Pass is `stamps["chunk"] >= long_records` (line 295), a global count, not per record.

## (b) Per-record attribution key

`attribute` (`argv-witness.py` lines 275–288) keys on the record’s own span bytes, not the id, the temp dir, or the source-name scheme.

- Truth span: `meta["span"].encode("utf-8", "surrogateescape")` (line 280).
- A call counts only if its argv contains all of `-a -z -b -o -P` and one non-flag pattern (`matcher_patterns`, lines 260–272). `--version` is logged and ignored.
- `decode_matcher_pattern` (lines 248–257): a pure `\xHH` pattern is `direct` and must equal the whole span. A pattern of the form `(\xHH)(?=<pure \xHH…>)` is `chunk` and must equal `span[:4096]`. Anything else is dropped.
- First matching pattern wins; the label stored is `"direct"` or `"chunk"`.
- `witness == "pass"` iff every truth id is attributed (line 348). `unattributed` is `set(truth) - set(attrs)` (line 352).

The 4096 cutoff is the witness constant in that slice, matching the gate’s `TOK_CHUNK_BYTES=4096` (`research-gate.sh` line 1709). Dead-zone spans in the fixture are 32765–32767 bytes (`DZ_MIN`/`DZ_MAX`, lines 51–52); the one short class is 512–4096 (line 149) and is routed by the gate through the direct matcher because `TOK_DIRECT_SPAN_MAX=32764` (research-gate.sh lines 1708, 1726–1729).

Both after receipts: landed attribution is 8 `chunk` + 1 `direct`, `unattributed=[]`, `matcher_calls=11`. [INFERENCE] 11 = 8 long searches + one extra `tok_span_all` for the single `dz-line-bound` record (research-gate.sh lines 2016 and 2037) + the short direct search + `token_matcher_require`. Not traced live.

## (c) Variants — patch and why the stdout can still match

All six are built in `c2-count.py` `main` lines 235–242 from the gate text. Helpers are written under the counter’s temp dir (`HELPER_SRC` lines 59–69, `CHUNK_HELPER_SRC` lines 70–80). `bash -n` is recorded as `syntax_ok` and does not affect the predicate.

Output-equivalence here means `output_full`: 9/9 claim lines match the fixture classes, the gate exits 1, and a `RESEARCH_GATE: DRIFT` line is present (`argv-witness.py` lines 339–350). Boundary checks stay in `tok_span_at` / `tok_span_all`; the patches only change how offsets are produced. Receipts, not a fresh run, show `output_full=true` and `9/9` for V1–V5 on the before receipt and both after receipts, and for V6 on both after receipts.

V1 `python-exact`. `patch_offsets` (lines 112–125) inserts `EXACT_BRANCH` (lines 82–86) as the first statement after `local hay=$1 span=$2` in `tok_span_offsets`. If `${#span} > TOK_DIRECT_SPAN_MAX`, `python3` `bytes.find` prints non-overlapping offsets (`off = i + len(span)`) and `return 0`. Short spans still call `tok_span_offsets_direct`. The chunk matcher also emits non-overlapping confirmed spans (`resume=$((offset + slen))`, research-gate.sh lines 1768–1773), so a verbatim long span’s offset list matches. After receipts: `witness=fail`, attribution `{direct: 1}`, `matcher_calls=2` (the short span plus the require probe). Eight long ids are unattributed.

V2 `env-keyed`. Same insertion, `KEYED_BRANCH` (lines 88–92): the shortcut also requires `CHOUSA_WITNESS_KEY==1`. The argv witness always sets that (argv-witness.py line 325), so against this witness V2 behaves as V1. The legacy witness strips `CHOUSA_*` and does not set the key, so the branch stays inert, the real chunk function runs, and PS4 stamps pass. Before receipt: V2 `witness=pass`, `output_full=true`, `exit=0`. After receipts: `witness=fail`, same shape as V1 (`{direct: 1}`).

V3 `witness-forge`. `build_forge` (lines 165–172) applies V1’s branch, then inserts at line index 1 (so later line numbers shift by one) a loop of 360 `printf '@@WITNESS@@<gate>:<chunk-entry-line>'` to stderr. `chunk_entry_line(text)+1` is the shifted entry line the legacy stamp regex wants (`mechanism-witness.py` lines 269–280, pass if chunk stamps `>=` long records). Stderr forgeries do not change stdout verdicts. The argv witness ignores stderr, and the exact branch still skips the chunk grep, so V3 fails it the same way as V1. Before receipt: `witness=pass`. After: `witness=fail`, `{direct: 1}`.

V4 `one-call-for-show`. `ONCE_BRANCH` (lines 94–101): the first long span falls through to the real matcher and creates `$ROOT/.w36-once`; every later long span is answered by the python find and returns. One real chunk argv remains, so the global “8 stamps for 8 records” threshold fails, and per-record attribution fails for the other long ids. After receipts: `witness=fail`, attribution `{chunk: 1, direct: 1}`, `matcher_calls=3`. Before receipt: `witness=fail` (only one chunk stamp, need `>=` 8). This is not the discard-the-result call-for-show. A query of every record that ignores grep’s answer still attributes (argv-witness.py lines 27–28; claims.md lines 131–132). V4 kills the skip, not that survivor. Not demonstrated here as a new engine.

V5 `body-replaced`. `replace_body_grep` (lines 142–157) leaves `tok_span_offsets_chunk` in place and replaces only `grep -a -z -b -o -P -- "$pattern"` with `python3 <chunk_helper> "$chunk"`. The helper finds the 4096-byte chunk, steps by 1, and prints `offset:0\0`. The consumer uses only `${occurrence%%:*}` and then confirms the whole span (research-gate.sh lines 1768–1773). The real grep pattern is one literal byte plus a zero-width lookahead over the rest of the chunk (line 1767), so `-o` also reports every start offset. [INFERENCE] those two candidate streams match for a literal chunk with no NUL; the confirmation step is unchanged, so verdicts match. The function is still entered, so the legacy PS4 stamp passes. The chunk pattern never appears in a grep argv, so the argv witness does not attribute long spans. Before: `witness=pass`. After: `witness=fail`, `{direct: 1}`, `matcher_calls=2`.

V6 `renamed-matcher`. `build_rename` (lines 160–162) replaces `tok_span_offsets_chunk` → `tso_chunk_x` and `tok_span_offsets_direct` → `tso_direct_x` globally, call sites included. Behaviour is the same grep pipeline. The legacy witness looks up the old function names and, if either entry line is missing, returns `witness=unparseable` before running the gate (`mechanism-witness.py` lines 251–255), so `output_match=0` and `output_full` is absent. Before receipt: `witness=unparseable`, `output_full=null`, `output_match=0`, `exit=1`, `syntax_ok=true`. The argv witness never looks up those names. After receipts: `witness=pass`, `9/9`, attribution 8 chunk + 1 direct, `matcher_calls=11`, `unattributed=[]`.

## (d) Where the counter passes and fails

`c2-count.py`. Exit 2, no receipt: gate path missing (lines 200–202) or temp dir cannot be created (lines 206–208). Exit 1, receipt written: witness file missing, label `WITNESS_PER_RECORD=0/<n> battery=absent`, `predicate_holds=false` (lines 213–218; `return 1` runs `finally`). Exit 1: `TimeoutExpired` or `RuntimeError` (patch anchor missing), label `WITNESS_PER_RECORD=error` (lines 280–284, 290).

Otherwise the printed line is always emitted (lines 272–274). `predicate_holds` (lines 258–265) is true only when all of these hold:

- `separated == 5`. A swap counts only if `output_full` and `witness=="fail"` (lines 259–260). `witness=="pass"`, `"unparseable"`, `"error"`, or a non-full output does not separate. A broken patch cannot inflate the score.
- `output_equiv == 5`, i.e. all five swaps have `output_full` (line 258).
- Landed `attribution` is a dict and `unattributed == []` (line 231), and landed `witness=="pass"` (line 264). `attribution is None` records `landed_attrib=absent`; a dict that misses an id records `fail` (line 269).
- V6 has `output_full` and `witness=="pass"` (lines 261–262). `unparseable` is `renamed=fail`.

Exit 0 iff `predicate_holds`, else 1 (line 290).

`argv-witness.py` exit, which the counter stores as `exit`: 0 iff `witness=="pass"` and `output_full` (lines 372–373); 1 otherwise, including timeout (lines 363–366); 2 if the gate file is missing or the temp dir fails (lines 300–308). `output_full` needs matched==9 and gate rc==1 and a drift line (line 350). Witness pass does not require `output_full`; the counter applies them separately.

Observed on the committed receipts (see commands):

| run | separated | output_equiv | landed_attrib | renamed | holds |
|---|---|---|---|---|---|
| before legacy, seed 36001, gate `a4768851…`, witness `mechanism-witness.py` `9f537bfd…` | 2/5 (only V1, V4 `witness=fail`; V2, V3, V5 `pass`) | 5/5 | absent (`attribution=null`) | fail (`unparseable`) | false |
| after, seed 36001, gate `a7d3922c…`, witness `argv-witness.py` `e6832e0b…` | 5/5 | 5/5 | pass | pass | true |
| after, seed 36011, same gate and witness hashes | 5/5 | 5/5 | pass | pass | true |

Those two after seeds are the construction seeds named in `claims.md` lines 4–6, not this wave’s fresh seeds. This seat did not run 36301 or any other seed.

## (e) Docstring numeric claims, line by line

`corpus/evidence/round36/c2-count.py`:

- L8 `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` — supported by both `c2-after-s*.json` (`label`, `output_equiv`, `landed_attrib`, `renamed`).
- L10 `predicate_holds=true` on two seeds — supported by those two files (`predicate_holds: true`, seeds 36001 and 36011). “Fresh” is not a number; claims.md calls these construction seeds.
- L11 no committed run of this counter on the landed tree is lower — the two after receipts are not lower than 5/5. These three files do not inventory every committed run. Not treated as contradicted by them.
- L13 `separated == 5` and `output_equiv == 5` — supported (`matched` 5, `output_equiv` 5) on both after receipts.
- L18 the five engines print the same nine verdicts — supported: V1–V5 are `output_match=9` / `output_total=9` / `output_full=true` on all three receipts.
- L25 `360` forged stamps — not a field of any of the three receipts.
- L29 `8` stamps for `8` records, `QUALITY 49` — not a field of any of the three receipts.
- L31 gate `` `3e5648b8…` `` — not the gate hash in any of the three. Before is `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`; both after are `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.
- L38 `separates only 3/5 (V3 and V5 pass it)` — not supported. `c2-before-legacy-s36001.json` `label` is `WITNESS_PER_RECORD=2/5`, `matched` is 2. `witness=pass` on V2, V3, and V5; `witness=fail` only on V1 and V4. claims.md lines 107–111 state the 2/5 reading and why V2 passes (the legacy witness scrubs the key). The parenthetical “V3 and V5 pass” is true and incomplete; the count 3/5 is false.
- L38–39 a stub that always says pass separates `0/5` — not a result in these three receipts.
- L39 a stub that always says fail fails the landed gate — not a result in these three receipts. Landed `witness` in all three is `pass`.

`tools/argv-witness.py`:

- L7 `360` stamps and zero real chunk executions — not in the three receipts.
- L8 `8` stamps for `8` records, `QUALITY 49` — not in the three receipts.
- L14 first `4096` bytes — not stored in the receipts. Both after landed maps are 8 `chunk` + 1 `direct`, which matches eight long records and one short, but the cutoff itself is only in the source.
- L35 exit `0` — supported: landed `exit` is 0 on both after receipts (witness pass and `output_full`).
- L35 exit `1` — supported: V1–V5 `exit` is 1 on both after receipts.
- L35 exit `2` — not observed in the three receipts.

## Docstring numeric claims the named receipts do not support

Named set: `.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`, `c2-after-s36001.json`, `c2-after-s36011.json`.

1. `c2-count.py` line 38: “separates only 3/5”. The before receipt is 2/5; V2 passes as well as V3 and V5.
2. `c2-count.py` line 25: 360 forged stamps. No stamp count in the three receipts.
3. `c2-count.py` line 29: 8 stamps, 8 records, QUALITY 49. Absent from the three receipts.
4. `c2-count.py` line 31: gate prefix `3e5648b8`. Neither gate hash in the three receipts starts with that prefix.
5. `c2-count.py` lines 38–39: stub-pass separates 0/5. Not in the three receipts.
6. `c2-count.py` line 39: always-fail stub fails the landed gate. Not in the three receipts.
7. `argv-witness.py` line 7: 360 stamps, zero real chunk executions. Absent.
8. `argv-witness.py` line 8: 8 stamps, 8 records, QUALITY 49. Absent.
9. `argv-witness.py` line 14: the 4096-byte cutoff. Not a receipt field.
10. `argv-witness.py` line 35: harness exit 2. Not observed.

## Commands

1. Eval cell (python), completed, no error. Deciding print: before `label WITNESS_PER_RECORD=2/5` `matched 2`, V2/V3/V5 `witness=pass`, V1/V4 `witness=fail`, V6 `witness=unparseable`; both after files `WITNESS_PER_RECORD=5/5` `holds True` and every swap `witness=fail` with `out=9/9`.

```
python3 -c 'import json, pathlib
base = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/measure")
for name in ["c2-before-legacy-s36001.json","c2-after-s36001.json","c2-after-s36011.json","c2-stubfail-s36001.json","c2-stubpass-s36001.json"]:
    ...'
```

The stub files were summarized in that same cell and are not part of the support set above. They were not required for the 3/5 contradiction.

2. `sha256sum` plus a kind tally, cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`, exit 0. Deciding lines: `argv-witness.py` hashes to `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e` (equals both after `witness_sha256`); `mechanism-witness.py` hashes to `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` (equals the before `witness_sha256`); `research-gate.sh` hashes to `a7d3922c…` (equals both after `gate_sha256`); `base-gate-r36.sh` hashes to `a4768851…` (equals the before `gate_sha256`). Tally: both after landed maps are `{'chunk': 8, 'direct': 1}` with `matcher_calls` 11; V1 and V5 are `{direct: 1}`; V4 is `{chunk: 1, direct: 1}`; V6 is `{chunk: 8, direct: 1}`.

```
sha256sum tools/argv-witness.py tools/mechanism-witness.py corpus/evidence/round36/c2-count.py tools/research-gate.sh .ufo/waves/round-36/measure/c2-before-legacy-s36001.json .ufo/waves/round-36/measure/c2-after-s36001.json .ufo/waves/round-36/measure/c2-after-s36011.json .ufo/waves/round-36/controls/base-gate-r36.sh && python3 -c '...'
```

`c2-count.py` sha256 (not stored in the receipts): `3c699aab0614fff78f88d1b8570166439014a360ee378c0a143bf204a96e4362`.

## Files opened

- `corpus/evidence/round36/c2-count.py` (full)
- `tools/argv-witness.py` (full)
- `tools/mechanism-witness.py` (docstring, `matcher_entry_lines`, env/PS4, stamp pass rule)
- `tools/research-gate.sh` (grep pin 332–420; matcher 1706–1823; `tok_span_at` call 2016 and `tok_span_all` call 2037; `grep_pin_init` 8205–8208)
- `corpus/evidence/round36/claims.md` (C2, lines 66–132)
- `.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`
- `.ufo/waves/round-36/measure/c2-after-s36001.json`
- `.ufo/waves/round-36/measure/c2-after-s36011.json`
- `.ufo/waves/round-36/measure/c2-stubfail-s36001.json` and `c2-stubpass-s36001.json` (json summary only; outside the named support set)

## Artifacts

None under `.ufo/waves/round-36/w1/ScoutC2Counter/`. No installs. No gate, counter, witness, or receipt was modified.

## Verdict

The landed argv witness, as scored in the two after receipts, separates all five output-equivalent patches and passes the rename. The before receipt separates 2/5, not the 3/5 the counter docstring states. That is a docstring error, not a counter-logic error: `separated` is computed (c2-count.py lines 259–260) and the before receipt’s per-variant `witness` fields are the 2/5 result. No output-equivalent engine that still attributes every record was built in this seat.
