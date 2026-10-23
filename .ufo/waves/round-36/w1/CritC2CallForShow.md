# Round 36 wave 1 — CritC2CallForShow (C2 critic: call-for-show, renamed/refactor control, recorder-read forge)

Role: UFO-FSD critic, leaf seat. Scope: attack C2's stated limit and the renamed control; independently re-derive P2 on fresh seeds.

## Verdict lines (one per scored attempt)

1. **CFS-call-for-show (seed 36331): NOT separated — `witness=pass`, attribution 9/9, output 9/9. Matches claims.md's stated limit verbatim; no defect, but confirms P2's 5/5 measures separation of the five named cheats only, not of every output-equivalent engine.**
2. **REFACTOR-deep (rename + argv-construction helpers, seed 36331): NOT killed — `witness=pass`, attribution 9/9, output 9/9; the committed counter's RENAMED arm also passes on fresh seeds 36331 and 36321. No false kill; C2 calibration holds.**
3. **FORGE-recorder-read (seed 36331): MEETS — P2-style scoring passes (`witness=pass`, `output_full=true`, attribution 9/9) with ZERO genuine span queries to the pinned engine. This is a real bypass of the witness's attribution, but it is exactly the limit claims.md states ("a gate that READS the recorder script can learn the log path and marker and forge records — active anti-instrumentation is out of scope"). Reproduced stated limit, not a new hole. P2 remains true as written; its reading must stay "separation of V1–V5 + no false kill on rename", never "all output-equivalent engines are caught".**

## Independent P2 re-derivation (committed counter, pinned gate)

Gate pin: `sha256sum tools/research-gate.sh` → `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` (matches the landed gate).

Command 1 (seed 36331):
```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=/tmp/hyaku/chousa-r36/w1/CritC2CallForShow/c2tmp timeout 1800 python3 corpus/evidence/round36/c2-count.py --seed 36331 --receipt .ufo/waves/round-36/w1/CritC2CallForShow/c2-s36331-committed.json
```
Exit 0. Deciding line:
```
WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass
  V1-python-exact        output=9/9 witness=fail attrib=1
  V2-env-keyed           output=9/9 witness=fail attrib=1
  V3-witness-forge       output=9/9 witness=fail attrib=1
  V4-one-call-for-show   output=9/9 witness=fail attrib=2
  V5-body-replaced       output=9/9 witness=fail attrib=1
  V6-renamed-matcher     output=9/9 witness=pass attrib=9
```
Receipt: gate_sha256 `a7d3922c…`, `predicate_holds: true`, landed attribution 9 records / `unattributed: []`, elapsed 15.71 s.

Command 2 (seed 36321, second fresh seed):
```
C2_TMP=…/c2tmp timeout 1800 python3 corpus/evidence/round36/c2-count.py --seed 36321 --receipt .ufo/waves/round-36/w1/CritC2CallForShow/c2-s36321-committed.json
```
Exit 0, identical deciding line (`5/5 5/5 pass pass`; V6 `witness=pass attrib=9`). Receipt `d6815f54…`, `predicate_holds: true`, elapsed 14.55 s.

## Attempt 1 — call-for-show engine (attack C2's stated limit)

Build: `CFS-call-for-show.sh` (artifact below). Both matchers still invoke the pinned recorder with the record's genuine `-a -z -b -o -P` pattern (stdout to /dev/null), then answer by python exact search (the counter's own accepted helpers), discarding grep's answer.

Scored through the committed counter's own machinery (imported, not edited) because the frozen battery has no CFS slot:
```
C2_TMP=/tmp/hyaku/chousa-r36/w1/CritC2CallForShow/c2tmp timeout 1800 python3 /tmp/hyaku/chousa-r36/w1/CritC2CallForShow/score-variants.py 36331 …/c2-s36331-variants.json
```
Exit 0. Deciding line:
```
CFS-call-for-show      output=9/9 witness=pass attrib=9/9 matcher_calls=11 recorder_calls=12 -> SURVIVES (not separated)
```
**Verdict: NOT separated, exactly as claims.md predicts.** The witness attributes every record (each span appears in a real matcher argv) and output equivalence holds. Implication for P2's reading: `WITNESS_PER_RECORD=5/5` certifies the five named round-35 survivors are caught; it cannot be read as "no other output-equivalent engine survives". The claims file says this in its Limits section; my run is a reproduction, not a refutation.

## Attempt 2 — legitimate refactor (false-kill hunt)

Two layers, both on seed 36331:

a) Committed counter's RENAMED arm (V6 = both matchers renamed, call sites intact): `witness=pass attrib=9` — shown in the two committed-counter runs above (seeds 36331, 36321).

b) Deeper refactor `REFACTOR-deep.sh`: matchers renamed (`tso_direct_x`/`tso_chunk_x`) **and** the argv construction moved into helpers (`tso_grep_offsets` / `tso_chunk_candidates`); the recorder-visible argv is unchanged. Same driver command, deciding line:
```
REFACTOR-deep          output=9/9 witness=pass attrib=9/9 matcher_calls=11 recorder_calls=12 -> SURVIVES (not separated)
```
**Verdict: no false kill.** The witness keys on argv patterns, not on source layout, so a behaviour-preserving refactor survives. C2's no-false-kill property holds beyond the counter's own rename control.

## Attempt 3 — forge the argv log from inside the gate (the stated anti-instrumentation limit)

Build: `FORGE-recorder-read.sh`. The engine (1) reads the pinned recorder script (`$GREP_BIN`), extracts the per-run marker and log path from its text, (2) replaces both matchers with python exact search so the pinned engine is **never queried for matching**, and (3) appends one forged NUL-delimited `-a -z -b -o -P -- <span-hex>` argv line per record to the witness log. Same driver command, deciding line:
```
FORGE-recorder-read    output=9/9 witness=pass attrib=9/9 matcher_calls=11 recorder_calls=12 -> SURVIVES (not separated)
```
Deciding evidence from the raw witness receipt (`.ufo/waves/round-36/w1/CritC2CallForShow/c2-s36331-variants.json` and `r-FORGE-recorder-read.json` in the scratch run dir): attribution 9/9, all kind `direct`; the only genuine recorder invocations were the `--version` pin probe and the `token_matcher_require` 'x' capability probes (`grep -a -z -b -o -P -- 'x'`, research-gate.sh:1820) — **zero genuine span queries**, yet full attribution and `output_full=true`.

**Verdict: MEETS — an output-equivalent engine that never queries the pinned engine passes P2-style scoring.** Per the assignment rubric this is the most valuable result, with the precise caveat: claims.md's Limits section states this exact bypass and declares active anti-instrumentation out of scope, so this confirms the frontier as disclosed rather than opening an undisclosed hole. The witness docstring is equally explicit ("it cannot stop a gate that READS the recorder script and forges log lines").

**Smallest safe corrections if the lane ever wants to close the forge** (not required for P2 as written): (i) have the witness open the log as an inherited fd (recorder writes to fd 3; the log path never appears in any file the gate can read) and pass the marker the same way — the gate then cannot learn either secret; (ii) or assert an exact recorder-call ledger (span queries + the one known capability probe + the one `--version` probe) so forged extras/count mismatches fail attribution. Option (i) is the robust one; (ii) is brittle against legitimate extra grep uses.

## Minor robustness note (not a claim defect)

`make_recorder` (tools/argv-witness.py) embeds the marker via printf's **format** string: the generated line is `printf 'W36CALL-…\n' 'W36CALL-…'`, so the marker's first in-script occurrence carries a trailing literal `\n` and the second (argument) occurrence is the clean one. Harmless today — `read_calls` splits on the clean `marker\n` token and ignores the rest — but my first forge attempt extracted the first occurrence and produced malformed lines that `read_calls` silently dropped (attribution 0/9, witness=fail). A gate-side forger must take the last occurrence. Consider emitting `printf '%s\n' 'MARKER'` (format fixed, marker only in the argument) to remove the ambiguity.

## Files opened (access date 2026-10-23)

- `.ufo/waves/round-36/w1-briefs/CritC2CallForShow.md` (this assignment)
- `corpus/evidence/round36/claims.md` (frozen claims, limits, repairs)
- `corpus/evidence/round36/c2-count.py` (committed counter, read in full)
- `tools/argv-witness.py` (committed witness, read in full)
- `tools/research-gate.sh` (lines 355–428 grep pin, 1708–1830 matcher functions, 1815–1822 probe)
- No production file modified; no git/jj write commands.

## Artifacts (all under `.ufo/waves/round-36/w1/CritC2CallForShow/`, sha256)

- `c2-s36331-committed.json` — `56864064c15b89d6776b995f1791015be3489d7e8d862c87610501f692641359` (committed counter, seed 36331, holds)
- `c2-s36321-committed.json` — `d6815f54ef667394f919fdcbec3d1577af897260afed20d25247eb5885755578` (committed counter, seed 36321, holds)
- `c2-s36331-variants.json` — `3bfdc7825ceaa7faff3afc23c515c47f722c5110b36cf48aeb29220fac7e923e` (critic driver receipt: CFS / REFACTOR / FORGE)
- `CFS-call-for-show.sh` — `f292c646180a8ac231f06fc68e577f93e9d4c127d9a2134fdc4de540a267cfd6`
- `REFACTOR-deep.sh` — `ff161c660bea816bcb3e94e0ea33d96f8e78476c3d64e39cd076bf6da29cdcad`
- `FORGE-recorder-read.sh` — `c43e2cf89e881d3c4bf3dbcaf8ad58e79c708a91d21fe02ff6c90ac59aec8886`
- `score-variants.py` — `1b24327d44b2549095a334f18d94253df2d927784b5fd098ddaa5700056d2a9d` (imports the committed counter; committed counter and witness untouched)

Scratch logs/gates: `/tmp/hyaku/chousa-r36/w1/CritC2CallForShow/c2tmp/r36crit-00008deb-s_jh2q9r/` (scored run dir; raw per-variant witness receipts `r-*.json`).

## Installs

None (no tools installed or updated this session).
