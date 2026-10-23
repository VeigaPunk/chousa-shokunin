# Per-record argv attribution: query is not use

Lane: chousa. Round 36 (C2). Tool: `tools/argv-witness.py`.

source: S069 (GNU `grep(1)` manual, `-b`/`-o` byte-offset and only-matching semantics; source row pending in the registry), `.ufo/waves/round-36/measure/c2-after-s36001.json`, `.ufo/waves/round-36/measure/c2-after-s36011.json`, `.ufo/waves/round-36/measure/c2-before-legacy-s36001.json`, `.ufo/waves/round-36/measure/c2-stubpass-s36001.json`, `.ufo/waves/round-36/measure/c2-stubfail-s36001.json`, and `tools/argv-witness.py`.
verified-at: 2026-10-23 (the two landed receipts pin gate SHA-256 `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` and witness SHA-256 `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e`). These receipts are the L1 construction runs on seeds 36001 and 36011, not the wave's fresh independent re-derivations.
recheck: on-release (`python3 corpus/evidence/round36/c2-count.py --seed N --receipt F`; use fresh seeds and retain the receipt's gate and witness hashes).

## Channel and rule

The witness substitutes a distinct-path GNU-reporting recorder through `RESEARCH_GATE_GREP`. The recorder writes a per-invocation NUL-delimited argv record to a log; its random log name and marker are embedded in the recorder script, not passed in the gate's environment. It then `exec`s `/usr/bin/grep`. The witness recovers the matcher query from that out-of-band log rather than trusting the gate's stderr or its own diagnostic text.

A record is attributed only when its own span occurs in a matcher-shaped argv containing `-a -z -b -o -P`. For a dead-zone span, the queried value is its first 4096 bytes; otherwise it is the complete span. S069 is the intended source for the GNU grep option semantics: `-b`'s offset is a byte offset (and with `-o`, the offset is for the matched part), while `-o` selects only the matching part. This describes the grep channel, not evidence that the gate used grep's answer: the witness compares argv patterns and the separate output oracle checks output.

## Legacy witness survivors (before)

The legacy baseline is `.ufo/waves/round-36/measure/c2-before-legacy-s36001.json` (base gate SHA-256 `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`, round-35 `tools/mechanism-witness.py`). Each V1–V5 variant produced full output, 9/9; the legacy witness only separated two of the five.

| Variant | Legacy witness | Round-36 witness, `c2-after-s36001` |
|---|---|---|
| V1 — python-exact | fail (killed) | fail; 1/9 records attributed |
| V2 — environment-keyed | pass (survived) | fail; 1/9 attributed |
| V3 — witness-forge | pass (survived) | fail; 1/9 attributed |
| V4 — one-call-for-show | fail (killed) | fail; 2/9 attributed |
| V5 — body-replaced | pass (survived) | fail; 1/9 attributed |

The new counter's post-run receipts report all five variants output-full and separated (5/5) on each construction seed; landed attribution passes, and the renamed control passes. The stub controls are guardrails: the always-pass stub scores 0/5 and fails P2; the always-fail stub scores 5/5 on separation but fails landed and renamed arms, so also fails P2.

## Renamed control and false kills

V6 renames the matcher helpers without changing the intended behavior. The legacy receipt calls it `unparseable`; the round-36 receipt records full output (9/9), all nine records attributed, and `pass`. A witness that treats private helper names as the behavioral contract can falsely reject a semantics-preserving rename; this control checks that calibration does not demand those names.

## Limits

- Attribution proves the pinned matcher was queried for each record, not that its result was used. A call-for-show engine that queries for every record and discards every answer can still pass if it preserves the expected output. The V4 mutation is a one-call control, not this per-record bypass.
- A gate that reads the recorder script can learn the log path and marker and forge records. Active anti-instrumentation is out of scope.
- The `-b`/`-o` manual semantics describe GNU grep's channel; they do not strengthen argv attribution into proof of result use.
- The cited `c2-after-*` receipts are the disclosed construction seeds, not the independent fresh-seed re-derivation.

## Registry note

At drafting time, the opened committed `corpus/SOURCES.md` ends at S068; S069 is not yet present there. The S069 citation above is therefore a pending registry link, not a claim that the row has already been admitted. Add/verify that row before admitting this entry.
