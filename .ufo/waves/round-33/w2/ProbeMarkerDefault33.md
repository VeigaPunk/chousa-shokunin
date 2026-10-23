# ProbeMarkerDefault33 — `marker_default` rows under the landed `claim_scan` gate (C1, W2 FALSIFY)

Item: probe the *uncounted* `marker_default` surface of C1 (flat row; nested in an object/array/deep
container; duplicated; a row carrying both `id` and `marker_default`; a default followed by
contradicted claims), base vs landed vs the python feasibility oracle, against
`corpus/evidence/round33/claims.md` and `corpus/knowledge/claim-record-fields-r33.md`.

**Verdict: HOLDS for the counted claim (P1 v2 re-verified 156/156 on fresh seeds 4231/4232), and the
`marker_default` surface obeys contract item 1 (a nested member changes nothing) on every variant
measured. One defect found (F1): a default row that repeats a *non-`marker_default`* read key is
accepted silently, contradicting the unqualified duplicate rule in `claims.md:34-36`,
`claim-record-fields-r33.md:23-26,51` and the landed gate's own comment at `tools/research-gate.sh:1608-1609`.
Base and oracle behave the same, so it is not a regression and cannot flip a verdict; it is a
text-vs-code defect on an input the counter does not generate.**

## 1. What I ran

Gate copies (hashes in `MANIFEST.txt`), each byte-checked against the lane objects:

| reader | sha256 | source |
|---|---|---|
| base | `f4731885…003f0` | `git show 2b9cc73a:tools/research-gate.sh` → `/fast/scratch/hyaku/chousa-r33/w2/ProbeMarkerDefault33/base-gate.sh` |
| landed | `94a7be5a…78506e` | copy of lane `tools/research-gate.sh` (tip `0fb300b5`) |
| oracle (feasibility, never a candidate) | `930a2075…677a9` | `.ufo/waves/round-33/controls/L1-design/oracle-gate.sh` |

Fixture root `.ufo/waves/round-33/w2/ProbeMarkerDefault33/fixtures/root/`: `src/a.md`
(`9828afe3…2c35`, span `alpha bravo charlie` on line 2, markers `ZZMARK`/`OWNMARK` on that line) and
`src/m.md` (`8bdfb579…6130`, same span, marker `a}b{c]d`). 31 claims files, one per case.

Command per case and reader (all saved under `outs/<case>.<reader>.{out,rc}`):

```
env -u CHOUSA_ROOT -u CHOUSA_CLAIMS -u CHOUSA_STRICT timeout 120 \
  bash <reader-gate.sh> verify-claims fixtures/<case>.jsonl --root fixtures/root
```

Every exit code was checked to agree with the printed verdict (`RESEARCH_GATE: CLEAN` ⇔ rc 0,
`DRIFT` ⇔ rc 1); `rc/verdict mismatches: none`. (One intermediate batch captured `printf`'s status
instead of the gate's; those six cases were re-run with `bash … > out; echo $? > rc` and the
tables below use the corrected values.)

Snapshot note: lane commit `4c076a0` (06:09:25) captured this directory mid-run, before that
correction. Its copies of `u-claim-dup-default.landed.rc` and `v-default-dup-marker-key.landed.rc`
read `0` while their committed `.out` files already print `RESEARCH_GATE: DRIFT`; the working-tree
versions (`1`) are the correct evidence, as are the regenerated `case-matrix.md`/`differential.tsv`.
`git diff --name-only HEAD -- .ufo/waves/round-33/w2/ProbeMarkerDefault33` lists the 16 affected
paths (the six `.out` diffs are the `ts=` header only); this report file is untracked. Integrate the
working tree, not `HEAD`, for those paths.

Counter re-run on the landed gate, fresh seeds, receipts required by the kill rule, stdout to a file:

| seed | command | stdout | receipt | receipt sha256 |
|---|---|---|---|---|
| 4231 | `python3 corpus/evidence/round33/c1-count-v2.py --gate tools/research-gate.sh --seed 4231 --receipt .ufo/waves/round-33/w2/ProbeMarkerDefault33/c1-landed-s4231.json` | `TOPLEVEL_FIELD_MATCH=156/156` (rc 0) | `c1-landed-s4231.json` (`predicate_holds=true`, `gate_sha256=94a7be5a…`, `counter_sha256=cb354dd1…`) | `82e33e43…9936e5ad` |
| 4232 | same, `--seed 4232` | `TOPLEVEL_FIELD_MATCH=156/156` (rc 0) | `c1-landed-s4232.json` (`predicate_holds=true`) | `7d9e2c8f…9dd47dd33` |
| 4233 | same with `--gate …/base-gate.sh` (base, not a landed run) | `TOPLEVEL_FIELD_MATCH=60/156` (rc 1) | `c1-base-s4233.json` (`matched=60`, `gate_sha256=f4731885…`) | — |

Both landed runs are recorded whatever they printed; both printed 156/156. Per-class: all 15 classes
full, `D1_duplicate_top_level 24/24`. Base 60/156 reproduces the L1 v2 before figure exactly.
Environment: bash 5.3.20(1), python 3.14.8. No installs, no network, no background jobs.

## 2. F1 — duplicate read key on a default row is silently accepted (the finding)

Minimal input file (case `i-default-dup-line.jsonl`), bytes as run:

```
{"marker_default":"ZZMARK","line":"1","line":"2"}
{"id": "i1", "source": "src/a.md", "span": "alpha bravo charlie", "expect": "contradicted"}
```

| reader | output | rc |
|---|---|---|
| base `f4731885` | `CLAIM id=i1 … observed=contradicted … verdict=match` + `RESEARCH_GATE: CLEAN (… claims=1 … invalid=0 …)` | 0 |
| landed `94a7be5a` | identical: only the claim `i1=contradicted`, `claims=1 … invalid=0`, `RESEARCH_GATE: CLEAN` | 0 |
| oracle `930a2075` | identical | 0 |

No `CLAIM id=line1 … observed=invalid`, no `FINDING CLAIM_RECORD_INVALID … duplicate top-level key
line`. The first line is consumed as a default row; its duplicated `line` is discarded unread.
Same result (landed, rc 0, CLEAN) for a duplicated `span` (`o-default-dup-span`, rc 0), `sha256`
(`r-default-dup-sha`, rc 0), `expect` (`s-default-dup-expect`, rc 0) and `marker`
(`t-default-dup-marker`, rc 0), and for a default row that also carries a non-string `id`
(`aa-default-nonstring-id-dup-line`: `{"marker_default":"ZZMARK","id":5,"line":"1","line":"2"}` → rc 0, CLEAN).

What the written rules say:

- `corpus/evidence/round33/claims.md:34-36` (contract item 2): “A read field that occurs more than
  once among the top-level members makes the record `invalid` (`CLAIM_RECORD_INVALID`), whether or
  not the values agree”.
- `corpus/knowledge/claim-record-fields-r33.md:23-26`: “A read field that appears more than once
  among the top-level members makes the record `invalid` … even when the values agree”; and
  `:51`: “Never repeat a read key at the top level; the record is refused, not resolved.”
- `tools/research-gate.sh:52` (usage header): “a repeated top-level read field makes the record
  invalid”.
- `tools/research-gate.sh:1608-1609` (the code's own comment): “a marker-default row has a top-level
  "marker_default" string and no top-level "id" string; **a duplicated read field is never such a
  row**.” The branch that follows (`:1610-1613`) checks duplicates for `id` and `marker_default` only
  and `continue`s before the duplicate loop at `:1622`, so a duplicate of `line`, `sha256`, `source`,
  `span`, `expect` or `marker` never disqualifies a default row.

The rule is applied asymmetrically, which is why this reads as an oversight rather than a design
choice: a duplicated `marker_default` on the same row shape *is* refused
(`v-default-dup-marker-key`: `{"marker_default":"ZZMARK","marker_default":"NOPE"}` → landed
`CLAIM id=line1 … duplicate top-level key marker_default`, rc 1), and a *claim* row with a duplicated
`line` is refused (`w-asymmetry`: claim `x1` → `observed=invalid`, rc 1, in the same file where the
default row above is accepted).

Impact: none on P1 (default rows are uncounted — `c1-count-v2.py:68` lists `marker_default` only in
`READ_KEYS`; no class generates one) and none on base→landed behavior (identical), and no verdict can
change from the dropped duplicate (the only field a default row contributes is `marker_default`, and
its duplication is refused). Under the gate usage header's “a `{"marker_default":…}` line sets the
default contradiction marker and is not a claim” (`tools/research-gate.sh:48-49`), and
`claims.md:80` (“Not claimed. `marker_default` rows (read by the same helpers, not counted)”), item 2
does not reach default rows and the defect is in the *text* (knowledge entry, usage header, code
comment); read literally from `claims.md:34`, item 2 is violated by the two lines above.
Suggested fix for the L1 (not applied — lane files are out of scope for this seat): check
`json_dup` for all seven read keys before the default-row branch (or move the branch after the
duplicate loop), and add an `r33-top-*` selftest case. The selftest has `r33-top-dup-line`
(`tools/research-gate.sh:7591-7600`) for a claim row but no default-row duplicate case: `grep -n
marker_default tools/research-gate.sh` shows only `:48`, `:1116`, `:1608-1622`, `:1781`, `:3925`
(the flat default fixture in the counting case), `:4566`.

## 3. F2 — nested `marker_default`: landed is right, base is wrong (confirmation)

Every nested *container* placement of `marker_default` is ignored by the landed reader and used as
the default by the base reader (base's unanchored regex matches the first occurrence anywhere on the
line); a `marker_default` spelled inside a string is read by neither:

| case | input line 1 | base | landed | oracle |
|---|---|---|---|---|
| `c-nested-default-obj` | `{"meta":{"marker_default":"ZZMARK"}}` | default set → claim `c1=contradicted`, CLEAN | `line1` invalid (missing id) + `c1=unproven` (`no marker defined`), DRIFT rc 1 | same as landed |
| `c2-nested-default-arr` | `{"meta":[{"marker_default":"ZZMARK"}]}` | `c2=contradicted`, CLEAN | `line1` invalid + `c2=unproven`, rc 1 | same |
| `c3-nested-default-deep` | `{"a":{"b":[{"marker_default":"ZZMARK"}]}}` | `c3=contradicted`, CLEAN | `line1` invalid + `c3=unproven`, rc 1 | same |
| `h-nested-before-top` | `{"meta":{"marker_default":"NOPE"},"marker_default":"ZZMARK"}` | first hit is the nested `NOPE` → `h1=unproven`, DRIFT | top-level `ZZMARK` wins → `h1=contradicted`, CLEAN | same as landed |
| `m-nested-id-default` | `{"meta":{"id":"nested"},"marker_default":"ZZMARK"}` | nested id makes it a claim → `id=nested … missing source`, `m1=unproven`, DRIFT | default row → `m1=contradicted`, CLEAN | same |
| `c5-nested-id-array` | `{"meta":[{"id":"nested"}],"marker_default":"ZZMARK"}` | `id=nested … invalid`, `c5=unproven`, DRIFT | `c5=contradicted`, CLEAN | same |
| `n-default-then-nested-override` | flat `ZZMARK`, then `{"meta":{"marker_default":"NOPE"}}` | second line overrides the default with `NOPE` → `n1=unproven`, DRIFT | second line invalid (`line2`, missing id), default stays `ZZMARK` → `n1=contradicted`, DRIFT (on the invalid line only) | same |
| `c4-default-in-string` | `{"note":"\"marker_default\": \"ZZMARK\""}` | not read (escaped) | not read (string content) | same |
| `q-nested-after-top` | top-level `ZZMARK`, nested `NOPE` after | `q1=contradicted` | `q1=contradicted` | same |
| `k-default-trailing-garbage` | `{"marker_default":"ZZMARK"}{}` | default applied → `k1=contradicted`, CLEAN | `line1` invalid (`not one well-formed JSON object`) + `k1=unproven`, rc 1 | same as landed |

So C1's item 1 extends coherently to the default-row surface, and the landed gate also refuses a
malformed line that the base silently used to set the default.

## 4. F3–F5 — other measured behaviors

- **F3 duplicated `marker_default` is now refused, declared-stricter.** Claim row
  `u-claim-dup-default` (`{"id":"u1",…,"marker_default":"AAA","marker_default":"BBB"}`): base and
  oracle accept it (`u1=supported`); landed `u1=invalid`, `duplicate top-level key marker_default`,
  rc 1. Default row `v-default-dup-marker-key`: base takes the first value (`v1=contradicted`),
  oracle the last (`v1=unproven`), landed refuses both. This matches design v2 (“invalid by the
  implementation … not counted”) and shows why fail-closed matters: first-wins and last-wins disagree
  on the same bytes.
- **F4 precedence of `id` over `marker_default` is undocumented.** `f-both-id-and-default` (claim with
  `id` + `marker_default` ZZMARK, then a contradicted claim): both gates and the oracle verify `f1` as
  a claim (`observed=supported`), never set the default, and `f2` is `unproven`. The knowledge entry
  says `marker_default` is read “on default rows” but does not state that a claim row carrying it
  silently loses it; a researcher could read `{"id":…,"marker_default":…}` as setting a default.
  Behavior is identical base/landed — documentation gap only.
- **F5 default rows are not claims in the summary.** In every default-row case the summary counts only
  the claim line (`claims=1` for a two-line file), base and landed alike; `marker_default` on a
  default row is the only field consumed (`m=${marker:-$default_marker}`, `:1778`), a per-claim
  `marker` overrides it (`g2` with `OWNMARK` → contradicted), and a default set mid-file applies only
  to later lines (`z-default-after-claim`: `z1` before the default → unproven, `z2` after →
  contradicted). A bracket-bearing marker works (`l-default-bracket-marker`, `a}b{c]d` → contradicted).

## 5. Full case matrix

All 31 cases × 3 readers, with rc, CLAIM observations and findings: `case-matrix.md` and
`differential.tsv` in the artifact directory. Highlights not covered above: flat default row
(`b`, CLEAN contradicted), identical duplicated default (`d`: base contradicts, landed refuses the row
and the claim is unproven — landed's refusal is item 2 working), differing duplicated default (`e`:
base picks `NOPE` and reports “declared marker not found”, oracle picks `ZZMARK` and contradicts,
landed refuses), non-string `marker_default` (`p`: all three invalid), duplicated `id` on a default
row (`j`: all three invalid, id kept when identical), differing duplicated `id` on a claim
(`x`: landed `id=line1`, oracle `id=x3` — landed follows the knowledge entry), duplicated `marker` on
a claim (`y`: landed invalid, base contradicts).

## 6. Limits

- 31 hand-built cases, one 3-line source per marker; no fuzzing of `marker_default` values (no NUL,
  non-ASCII or 64 KiB markers), no escaped key spellings (`"marker_default"` with `\u`), no default
  row larger than ~60 bytes. `claim_scan` cost was not measured here.
- The oracle is a feasibility reference only; its `json.loads` last-wins reading differs from landed
  by design (F3, `x`), so it is not a candidate.
- The finding hinges on how item 2's “the record” is read for a default row; both readings are stated
  in §2, and the artifact that is unambiguously falsified is the knowledge entry's unqualified
  sentence (`:23`, `:51`) and the gate comment at `:1608-1609`.
- Nothing in the lane was modified; all inputs/outputs are in
  `.ufo/waves/round-33/w2/ProbeMarkerDefault33/` (932 KB, largest file 12.5 KB) and scratch
  `/fast/scratch/hyaku/chousa-r33/w2/ProbeMarkerDefault33/`. No processes left; no installs; no
  network.

## 7. Risks / blockers

- None blocking. If the L1 wants a committed counter for this surface, the minimal class is a default
  row with a duplicated non-`marker_default` read key followed by a contradicted claim, truth
  `invalid` for that row — but claims.md:80 excludes `marker_default` rows from C1's counted set, so
  the repair is text-or-code, not a new class.
