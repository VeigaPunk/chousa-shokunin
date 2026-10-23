# MutWitnessBypass2 — witness bypass family 2 (round 35, w2)

Scope: attack C2's mechanism witness with three bypass shapes, scored by the committed
`tools/mechanism-witness.py`. Read-only on all lane files; every mutant is a scratch copy.
Scratch: `/tmp/hyaku/chousa-r35/w2/MutWitnessBypass2/` (gates, helper, receipts, logs).
Artifacts: `.ufo/waves/round-35/w2/MutWitnessBypass2/` (patches, receipts, fd trace).
No installs were needed.

Pinned inputs (re-derived at start and after every run; unchanged):
- `tools/research-gate.sh` sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` (landed, C1-echo gate)
- `.ufo/waves/round-35/repairs/base-gate.sh` sha256 `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`
- `tools/mechanism-witness.py` sha256 `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3`
- `corpus/evidence/round35/c2-count.py` sha256 `557fdbf0bd793a6589fcb28fbc0a589db9145be0ae3c92790041fe8ebd907171`
- `corpus/evidence/round35/claims.md` sha256 `48e094b4245ba604feb93604d43e2f7532e12032708fcdf2582021bdd9fb4d72`

Detector command (the battery's own CLI; receipt records `gate_sha256`):
`timeout 900 python3 tools/mechanism-witness.py --gate <mutant> --seed N --json <r> --tmp <scratch>/tmp`.
C2 end-to-end: `timeout 1800 python3 corpus/evidence/round35/c2-count.py --gate <mutant> --battery /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py --seed N --receipt <r>`
(note: the counter's default `--battery` is CWD-relative, so I pinned the absolute committed path;
same sha256 as the default when run from the lane root).

Baseline (landed gate, seed 3501): `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)`,
exit 0, `gate_sha256=1f2fb4f5…`, elapsed 8.34 s (`r-landed-3501.json`).

## Results

| probe | gate sha256 (prefix) | witness output | exit | verdict |
|---|---|---|---|---|
| landed baseline | `1f2fb4f522d9` | WITNESS=pass OUTPUT=9/9 chunk=9 direct=1 | 0 | baseline pass |
| (a1) honest mechanism + `exec 2>/dev/null` around dispatch | `5a0e9570c8e8` | WITNESS=fail OUTPUT=9/9 chunk=0 direct=0 | 1 | trace lost; false-fail |
| (a2) K1 shortcut + redirect only inside branch | `c54a730c8c3c` | WITNESS=fail OUTPUT=9/9 chunk=0 direct=1 | 1 | **killed** |
| (b) python-exact inserted at top of `tok_span_offsets_chunk` | `47fb429398f9` | WITNESS=pass OUTPUT=9/9 chunk=9 direct=1 (3501, 3517) | 0 | **bypassed** |
| (b2) python-exact replaces only the chunk grep/confirm body | `3e5648b8d0e5` | WITNESS=pass OUTPUT=9/9 chunk=9 direct=1 (3501, 3517) | 0 | **bypassed, strongest** |
| (c) synthetic `tok_span_offsets_chunk "$span" "$span"` then ignore | `843fdf55b090` | WITNESS=pass OUTPUT=9/9 chunk=9 direct=1 (3501, 3517) | 0 | **bypassed, disclosed** |

C2 counter runs:
- landed: `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass`, `predicate_holds=true`, exit 0 (`c2-landed-s3501.json`, gate `1f2fb4f5…`).
- **b2: same label and `predicate_holds=true` on seeds 3501 and 3517** (`c2-b2-s3501.json`, `c2-b2-s3517.json`; gate `3e5648b8…`, landed `{"witness":"pass","output_full":true,"stamps":{"chunk":9,"direct":1}}`).
- a1: `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=fail`, `predicate_holds=false`, exit 1 (`c2-a1-s3501.json`) — the honest gate is killed.

## (a) `exec 2>/dev/null` before the branch — does the trace still reach the witness's file?

No inside the redirect; yes after restoration.

Minimal proof: `bash -x -c 'exec 3>&2 2>/dev/null; echo inside; exec 2>&3 3>&-; echo after' 2>fd-trace.log`
→ stdout `inside`/`after`, stderr trace exactly `+ exec` + `+ echo after` (20 bytes; sha256 `d73e9d61…`).
The `echo inside` xtrace line is written to the redirected fd2 and never reaches the file.
At gate scale, a1 (landed matcher body byte-identical, only fd2 silenced around the dispatch) gives
correct output 9/9 with `chunk=0 direct=0`: the mechanism ran, the witness saw nothing.
Restoration works: a2 opens the redirect before routing and restores before the original `else`;
the short-verbatim record then reaches `tok_span_offsets_direct` and is stamped (`direct=1`), while
the long-span shortcut leaves `chunk=0`. **Verdict: (a) is not a bypass — it is killed, because the
witness requires positive stamps and a redirect can only remove them.** Side finding (calibration):
an honest gate that quiets fd2 across the matcher dispatch is falsely failed by the battery
(`c2-a1` → `LANDED_WITNESS=fail`); neither claims.md nor the witness docstring states that the
witness depends on the gate not redirecting its own stderr.

## (b) python exact search INSIDE `tok_span_offsets_chunk` — passes; P2's text does NOT cover it

b2 keeps the landed chunk entry line (`matcher_entry_lines` reports `chunk=1699, direct=1677`,
identical to landed; `patch-b2-body-swap.diff`) and replaces only the `while … grep -a -z -b -o -P`
confirmation body with `printf '%s' "$hay" | python3 span_search.py "$span"; return 0`.
The helper is `hay.find(span, off)` with `off = i + len(span)` — exact, non-overlapping,
left-to-right, the same outputs on the fixture (9/9 on both seeds). Because the function is
entered once per long record and its first executed line is unchanged, every stamp is earned:
`chunk=9` for 8 long records. The witness's pass condition is only
`stamps["chunk"] >= long_records` (`mechanism-witness.py:295`), where a stamp is counted solely by
`BASH_SOURCE == gate && LINENO == entry-line` (`:274-279`, entry-line detection `:80-101`) — it
never observes the function body or the grep call.

End-to-end this is the MEETS result: with b2 as the candidate gate, the committed C2 counter prints
`WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass` and `predicate_holds=true` on both
seeds. The identical predicate output is produced by a gate whose chunk mechanism no longer exists.
P2's kill rule only checks output-full variants and a landed witness pass; it never pins the
candidate gate's sha to the landed blob, and the receipt faithfully records `3e5648b8…`.

**Does P2's text already cover it? No.** The frozen limit (`corpus/evidence/round35/claims.md:106-109`,
accessed 2026-10-23) says: "A trace witness cannot distinguish an engine that knows it is traced, or
that calls the chunk matcher once for show and ignores its result. The witness rules out
fingerprint-and-shortcut engines, never active anti-instrumentation". b2 is neither trace-aware nor
a "once for show" call, and it is not fingerprint-keyed: it is a plain body-level reimplementation
whose entry call is genuine. The docstring states the same two limits
(`tools/mechanism-witness.py:26-30`). The disclosed class covers (c), not (b). The witness's real
coverage is call-site discipline ("was the function entered?"), not "did the chunk+confirm mechanism
run?"; P2's prose ("separate … from the landed dead-zone mechanism") is therefore broader than the
battery. Suggested wording for a future claim (not applied; lane read-only): "the witness certifies
entry into `tok_span_offsets_chunk` once per long record; a candidate that replaces the function body
with an equivalent exact search passes both the witness and the output check."

## (c) chunk matcher on a synthetic hay, result ignored — passes; text already covers it

`c` calls `tok_span_offsets_chunk "$span" "$span" >/dev/null` once per long record (synthetic
hay equal to the span, at least one occurrence at 0), then answers from the python exact search on
the real hay. Output 9/9, `chunk=9 direct=1`, witness pass on seeds 3501/3517 — exactly the class
claims.md:107 names ("calls the chunk matcher once for show and ignores its result"). **Not a new
hole**: a one-line synthetic call per record buys a pass. It confirms the pre-data limit was
accurate and cheap, and it is the control that (b) improves on by removing even the synthetic call.

## Restoration / lane integrity

No lane file was written: every mutant is a copy under `/tmp/hyaku/chousa-r35/w2/MutWitnessBypass2/`
with its own receipt-pinned sha256. After all runs, re-derived hashes equal the start values above
(gate `1f2fb4f5…`, witness `9f537bfd…`, c2-count `557fdbf0…`, c1-count `da207fd7…`, claims.md
`48e094b4…`, base-gate `a6307edf…`). Mutants were never installed anywhere; scoring always passed an
explicit `--gate`/`--battery` path. Both scratch counters used `TMPDIR`/`C2_TMP` under the scratch dir;
the witness's fixture roots were removed by the tool itself.

## Limits

- One fixture class set (8 long + 1 short), seeds 3501/3517 only; b2 equivalence is shown by the
  witness's own output check (9/9 twice), not by the lane's full 37-record suite. [INFERENCE] that the
  python search is contract-equivalent on every other record shape; the two argument cases it must
  satisfy (exact occurrence, non-overlap left-to-right) match `find` semantics.
- b2 needs `python3` on PATH, as the counter's own K1/K2 do; the landed gate needs only grep.
- a1's "honest mechanism" is asserted from source identity of the chunk body plus 9/9 output; the
  redirect makes an independent trace impossible by construction, which is the finding itself.
