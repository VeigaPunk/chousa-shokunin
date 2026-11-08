# R86ReviewerClaims — C1 stated wording vs its instrument

Seat `R86ReviewerClaims`, leaf. Lane `chousa-shokunin`. Claim attacked: C1 `C1-BATTERY-R86` only.
Revisions: base `3bfb6885958ad4a674ad1896f70d1e836be609e4`; claim freeze `d0b1bd06872cdf0eeb03eccd099ff69ae6704307`;
landed bytes attacked `667a5d091dc46168ed95eda0ae7f19a9bcf139a2`. Instrument bytes: `gate-records-r86.py`
sha256 `20bc1a733bd6c79f428a16c564cdc49555d8f02c389307eb2c6a28ceeb106d66`, subject tool `tools/gate-records.py`
sha256 `fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287` (identical at base and landing; all
`instrument-pins.txt` file pins match at `667a5d09` — receipt `pins-check.txt`). Line numbers below are the pinned
counter's. Scratch: `/fast/scratch/hyaku/chousa-r86/R86ReviewerClaims/` (deleted before yield). No network call was
made; every check reads committed bytes and read-only `git cat-file`/`git show`. No tool installed or upgraded.

Receipts cited are copied into this folder
(`.ufo/waves/round-86/w1/R86ReviewerClaims/`). Every run below exited as stated; the counter's landed predicate run is
`exact-command-run.txt`.

## Primary run (K1)

Command (claims.md counting command with the `mktemp` parent moved into my seat scratch as the seat rules require;
only the scratch parent differs):

```sh
S=$(mktemp -d -p /fast/scratch/hyaku/chousa-r86/R86ReviewerClaims exactrun.XXXXXX) \
  && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 667a5d091dc46168ed95eda0ae7f19a9bcf139a2 | tar -x -C "$S" \
  && python3 -B "$S/corpus/evidence/round86/gate-records-r86.py" --root "$S" \
       --repo /home/vgpnk/Projects/shokunin/chousa-shokunin --work "$S"
```

Observed (`exact-command-run.txt`):

```
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1
GATE_RECORDS_R86=PASS
EXIT=0
```

The archive counter and tool at `667a5d09` hash to the two pins above (`d1-probe.txt` header, `pins-check.txt`).

## Clause findings

### Clause 1 — "generates the round-85 `D1` class (an admit record whose stored body arrived under HTTP 203, built from the committed `S021` PubMed refetch row and its capture) *inside* the frozen predicate" — HELD

Enforcement:
- `corpus/evidence/round86/gate-records-r86.py:236-280` `build_d1_203_admit()` builds the record from committed files:
  `:257` skips `curl_rc != "0" or http == "200" or txt_sha == "-"`; `:259` requires `sha256(url)[:24] == key`; `:261-265`
  requires the capture file and `sha256(body) == row.txt_sha`; `:270-275` derives the quote from the body; `:277-279`
  derives `tier=cells[3]`, `capture_sha256=h[:16]`, `words`, `quote`; `:280` returns expected code `REFETCH`.
- `:357` calls the builder in `main()`; `:359-362` appends it as `D1-203-admit` to `forged`; `:363` makes it part of
  `total_forged`.
- `:455-457` the predicate requires `d1 is not None and d1_refused == 1 and mut17 == 1`; `:451-454` prints
  `D1_FORGES={1 if d1 else 0} D1_REFUSED={d1_refused}/1 MUT17_KILLED={mut17}/1`. Landed line above shows
  `D1_FORGES=1 D1_REFUSED=1/1`.

Evidence the generated record is present and in-class: the in-memory instrumented run (`exact-set-scan.txt`) records
`g0354.md` as `FAIL` with codes exactly `["REFETCH"]` (the appended D1 file; `seen-full.json` isolates it with
`"is_d1": true`), and the direct builder probe (`d1-fields.txt`) prints the S021 record.

Not enforced by the code, and not hidden: the builder does not pin the S-id or the code `203`. `:257` admits any
`curl_rc=0`, non-200 row with a stored `txt_sha`. At landing this is forced by the committed data: every such row is
`203` (three of three — `S021` `refetch.tsv:165`, `S032` `:166`, `S022` `:171`; `awk` count `3 203`), and `S021` is the
first, so the produced instance is necessarily a 203 body and is `S021` (`d1-probe.txt`). The naming is positional,
not asserted; the claim's sentence is true of the generated artifact, and a future earlier non-200 row is a
different-tree risk, not a landing falsification (see Residual risk 2).

### Clause 2 — "built from the committed `S021` PubMed refetch row and its capture" — HELD

Field-by-field derivation, verified independently against the landing commit (`d1-fields.txt`; all reads via
`git show 667a5d09:<path>`):

| record field | committed source | observed |
|---|---|---|
| `url` | `corpus/evidence/round57/refetch.tsv:165` field 2 | `https://pubmed.ncbi.nlm.nih.gov/17638714/` |
| `capture` key | field 3 / `sha256(url)[:24]` | `58725f5e0ac436166546a5ec` (equal) |
| `fetched` | field 5 | `2026-11-08T02:15:39Z` |
| `http` (class) | field 7 | `203` |
| `capture_sha256` | field 9 `7070b59c…d4782ab` vs `sha256(capture)` | prefix `7070b59c3434b677` matches the full hash |
| `tier` | `corpus/SOURCES.md:31` cell 4 | `A` |
| `quote` / `words` | capture line 13, located by `:270-275` | `Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue.` / 10 |

The counter contains no literal D1 record text: every field is read from the row/registry/capture at `:257-279`; the
quote comes from the capture's own line scan (`:270-275`), matching plan repair 3. The row and capture are committed
bytes already at the base revision (`git show 3bfb6885:corpus/evidence/round57/refetch.tsv` prints the same 203 row),
so "committed" holds independent of the landing commit.

Same caveat as clause 1: the code selects by `:257`, not by `S021`; at landing the selected instance is `S021` (probe
output `D1_RESULT: ('S021', … 'REFETCH')`).

### Clause 3 — "computes the round-85 `M17` mutant from the subject tool's own bytes" — HELD

Enforcement: `:284-292` `build_mutant()` reads `tool_src`, `:287` `src.replace('r[6] == "200"', 'r[6].startswith("2")')`,
`:288-289` returns `False` and writes nothing if the bytes are unchanged; `:303` resolves the subject tool as `--tool`
or `root/tools/gate-records.py`; `:439` gates the mutant leg on `build_mutant(tool, mpath)`.

Independent probe (`mutant-probe.txt`):

```
OCCURRENCES of r[6] == "200": 1
build_mutant -> True
sha256 tool     : fe204539b9b549ef1c6092a3963d73c7772946b027ab07da19c89961817aa287
sha256 mutant   : c8291bbc6e06c2cf18d3395e6eb9d0c6b8a843e30d3198229b4420c8b23383f4
bytes differ    : True
```

`diff -u` of the two files shows exactly one changed line, the REFETCH success comparison at `tools/gate-records.py:238`;
the mutant contains one `r[6].startswith("2")` and zero `r[6] == "200"`.

Nothing-found leg: a synthetic tool in which `r[6] == "200"` was rewritten semantics-preservingly to
`r[6] in ("200",)` (all other subject behaviour identical) was passed as `--tool`; the counter printed
`MUT17_KILLED=0/1`, `GATE_RECORDS_R86=FAIL`, exit 1 (`nolit-run.txt`). So a substitution that finds nothing cannot be
scored as a kill, exactly as K4 states.

### Clause 4 — "the subject tool refuses the `D1` record with `REFETCH`" — HELD

Direct run of the subject tool on the builder-produced record (`d1-fields.txt`, `d1.md`):

```
GATE_RECORD …/d1.md:1 S021 FAIL REFETCH     (ORIG, exit 1)
```

Inside the battery the record is `g0354.md` and the instrumented scan shows its refusal set is exactly `["REFETCH"]`
(`exact-set-scan.txt`, `seen-full.json`). The counter's own accounting is `:406` `d1_refused = 0`, `:411` expected-code
membership, `:413-414` `if label == d1_label: d1_refused = 1`; the landed line reports `D1_REFUSED=1/1`.

Causality is isolated: the only textual difference between subject and mutant is the REFETCH success comparison, and
the same record flips from `FAIL REFETCH` (exit 1) to `OK` (exit 0) under the mutant — so the refusal is the 200-only
rule, not a co-incidental CAPTURE_SHA/QUOTE defect.

### Clause 5 — "the derived mutant — REFETCH success relaxed back to 2xx — accepts every positive and the `D1` record, so the battery kills it instead of surviving it" — HELD

Enforcement: `:436-448`: `:441-444` `mut_pos_ok = mrc == 0 and all(…OK…)` over the 15 frozen and 5 fresh positives
(this also requires the mutant run to exit 0 on all of them); `:445-447` re-runs the mutant on the D1 file and requires
verdict `OK`; `:448` `mut17 = 1 if (mut_pos_ok and mut_accepts_d1) else 0`; `:455-457` requires `mut17 == 1`. Landed
line: `MUT17_KILLED=1/1`.

"Kills it instead of surviving it" checked in the direct sense: using the derived mutant itself as the subject tool,
the battery prints `FORGED_REFUSED=354/355 … D1_REFUSED=0/1 MUT17_KILLED=0/1`, `GATE_RECORDS_R86=FAIL`, exit 1
(`mutant-as-subject.txt`). The mutant is therefore not survivable against the landed predicate. The derived mutant also
accepts the D1 record directly (`d1-fields.txt`, `MUT exit=0 … S021 OK`) and no other tool behaviour was changed
(`mutant-probe.txt` diff).

## Kill-rule assessment

- **K1 — HELD.** Predicate met at `667a5d09`, exit 0 (`exact-command-run.txt`). The `after/c1-after.txt` receipt at the
  landing commit shows the same field line.
- **K2 — HELD for the D1 record; instrument reads "expected code present", not exact set.** `:411` counts a refusal as
  expected when the frozen code is a member of the reported set, so an extra code on the D1 record would not be caught.
  At landing the D1 set is exactly `{REFETCH}` (above). Across the other 354 forges, 85/355 refusals carry additional
  codes by construction (e.g. `('LINE','REV')` x18, `('CAPTURE_KEY','CAPTURE_SHA','QUOTE_ABSENT','REFETCH')` x12;
  `exact-set-scan.txt`); the round-85 counter used the identical membership test at `gate-records-r85.py:339`, so this
  is inherited estate semantics, not a round-86 delta. If the fleet reads K2 as exact-set equality, that reading also
  fails the r85 instrument that printed `FORGED_REFUSED=354/354 … PASS` (`c1-k0b-frozen-instrument.txt`). Reported as
  residual risk, not as a landing falsification of C1's sentence.
- **K4 — HELD.** The mutant is derived from the subject tool's bytes (clause 3; one occurrence, sha change, single-line
  diff), a tool the substitution cannot change scores `0/1` (`nolit-run.txt`), and there is no post-scoring repair:
  the counter and tool hash to their pins at the landing commit, and the freeze commit `d0b1bd06` is the commit before
  the landing commit `667a5d09`. The estate is unchanged by the diff: `r85-vs-r86.diff` shows only the docstring, the
  two new functions, the `gr86-` temp prefix, the D1 append, the D1 counter, the mutant leg and the print/`passed`
  lines; `build_fresh_positives`, `mutations`, the empty-file leg and the SETUP leg are byte-identical. The 15 frozen
  positives' TSV is the r85-pinned file (`8c089828…` in both pin files). The fresh positives are identical at base and
  landing (S082, S083; S199, S200; S100 — `fresh-base-vs-landing.txt`), and the landing predicate reports
  `POSITIVE=15/15 FRESH_POSITIVE=5/5 EMPTY_REFUSED=1/1 SETUP=1/1`.

## Question (4): could a tool that hard-codes the D1 record's expected code pass the predicate?

No. The MUT17 leg only passes when the mutant derived from the tool's own bytes accepts the D1 record (`:445-448`). A
refusal keyed on the D1 identity (S-id/url/fetched/capture) lives outside the rewritten `r[6] == "200"` text, survives
the substitution unchanged, and keeps refusing D1, so `mut_accepts_d1` is false and `MUT17_KILLED=0/1`.

Demonstrated with a synthetic subject = the pinned tool plus a hard-coded `REFETCH` for
`sid == "S021" and fetched == "2026-11-08T02:15:39Z" and capture == corpus/captures/58725f5e0ac436166546a5ec.txt`
(`hardcode-run.txt`):

```
MUT17_NOT_RELAXED the mutant still refuses the D1 record
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=0/1
GATE_RECORDS_R86=FAIL
```

The hard-code satisfies the D1 leg (`D1_REFUSED=1/1`) but not the mutant leg, so the full predicate rejects it. The
only way to make the derived mutant accept D1 is to write the genuine 200-only comparison in the tool's bytes, which
is not hard-coding the expected code.

## Residual risk

1. **K2 set semantics.** `:411` is membership, not exact equality: a spurious extra code on the D1 record would pass
   `D1_REFUSED=1/1`. At landing the D1 refusal set is exactly `{REFETCH}`, and the membership test is unchanged from
   `gate-records-r85.py:339`; a strict exact-set reading would fire on 85 of the 355 estate refusals (and equally on
   r85), so it is an inherited instrument policy question rather than a round-86 landing defect.
2. **D1 identification is data-order dependent.** `:257` filters only `http == "200"`; the counter does not pin `S021`
   or `203`. At landing every rc0+stored-sha non-200 row is 203 (3/3) and `S021` is first, so the claim's instance is
   forced. The mutant leg additionally forces the instance to be 2xx (a 4xx/5xx body would make the mutant refuse D1
   and `MUT17_KILLED=0`), but a future 201/202 body earlier in `refetch.tsv` would pass both legs while falsifying the
   "203" wording. Not a landing falsification.
3. **Fresh positives are rebuilt, not frozen.** `build_fresh_positives()` reads the lane working tree with
   `git -C repo grep … corpus/lessons`, and the frozen counting command passes `--repo` as the lane path, not a pinned
   rev. At the landing tree the 5 fresh positives are identical to the base tree (`fresh-base-vs-landing.txt`), so the
   estate is unchanged in fact for this scoring; the field is not byte-pinned.
4. **No network / no writes.** Every check above read committed bytes, `git show`/`git cat-file` objects, or an
   extracted archive; the counting command's `--work "$S"` temp dir is created and removed by the counter (`:311`,
   `:461`). I made no GET.

## Verification gaps

- I did not re-verify the S216 capture's text; that is the source-grounding seat's object, not the instrument wording
  I was assigned (C1 K1/K2/K4).
- C2 untouched (n/a for this seat).
- The exact-set scan is an in-memory monkeypatch of the frozen counter's `run()` that records the parsed code sets; the
  counter bytes were not modified, and the instrumented run reproduces the frozen PASS line byte-for-byte
  (`exact-set-scan.txt` head, `seen-full.json`).

VERDICT: R86ReviewerClaims C1 held — at landing 667a5d09 the battery PASSes with D1 built from the committed S021/203 row and capture, the subject tool's D1 refusal is exactly REFETCH, and the bytes-derived M17 accepts all 20 positives plus D1 so the battery kills it (0/1 when the substitution finds nothing or the refusal is hard-coded).
