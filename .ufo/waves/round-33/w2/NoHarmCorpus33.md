# NoHarmCorpus33 — no-harm on real claim inputs (wave 2, falsify C1)

Seat: `ChousaR33.NoHarmCorpus33`. Lane `chousa-shokunin`, HEAD `0fb300b` (round base
`2b9cc73`). Contract: `corpus/evidence/round33/claims.md` C1, design v2 (`:93-158`).

**Verdict: HOLDS.** Every committed claims JSONL verifies with identical stdout and exit
under base and landed, except the round-33 C1 counter/control fixtures, whose every changed
record is required by contract items 1–2; 0 changed records are unexplained. No falsifying
input found in the counter's blind spots (adversarial valid JSON, nested-only fields,
string content, duplicates, flat twins).

## Gates and method

- Base gate: `git show 2b9cc73:tools/research-gate.sh` →
  `/fast/scratch/hyaku/chousa-r33/w2/NoHarmCorpus33/gate-base.sh`, sha256
  `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` (matches round base).
- Landed gate: copied from the lane working tree at wave start →
  `.../gate-landed.sh`, sha256
  `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e`; confirmed equal to
  `git cat-file -p HEAD:tools/research-gate.sh` (same hash) after the runs.
- Every invocation: `bash <gate> verify-claims <claims-file> --root
  /home/vgpnk/Projects/shokunin`, stdout+stderr to a file, exit recorded, header `ts=`
  line excluded from the diff (the gate prints a timestamp).
- Corpus: `git ls-files '*.jsonl'` = **35 files** (runner
  `/fast/scratch/hyaku/chousa-r33/w2/NoHarmCorpus33/run-all.sh`, `timeout 900`, exit 0,
  48 s; 70 outputs under `.../out1/`). Scope check for non-JSONL inputs: the only committed
  `*.json` containing `"span"` is `.ufo/waves/round-29/build/MutateBlockInline/extra-inline.json`
  (a pretty-printed config); both gates print identical output on it (diff = ts line only).

## Result over the 35 committed files

Per-file rc and body diff: artifact `.ufo/waves/round-33/w2/NoHarmCorpus33/summary.tsv`
(columns: file, base_rc, landed_rc, claims, changed lines).

- **Exit codes identical for 35/35** (0/0 for the six `corpus/fixtures/*` claim fixtures,
  1/1 for the rest).
- **28/35 bodies byte-identical.**
- **7/35 differ**, all round-33 C1 fixtures (`.ufo/waves/round-33/w1/CtlC1*/…`,
  `…/w1/ExecC1Build/*`), never production inputs.
- Production fixtures, base == landed and rc 0 both:
  `corpus/fixtures/claims-r2.jsonl` `VERDICT_BEARING_CLAIMS=17/17` CLEAN;
  `claims-r9.jsonl` 10/10 CLEAN; `full-r6.claims.jsonl`, `full-r6-broken.claims.jsonl`,
  `integrity-r7.claims.jsonl`, `integrity-r7-broken.claims.jsonl` 3/3 CLEAN each;
  `corpus/evidence/verify-all-manifest.jsonl` 0/8 DRIFT both.
- `claims-r2` input-shape variants (CRLF; leading/trailing whitespace; interleaved `#`
  comments and blank lines; no final newline) are base==landed, 0 body diff, 17/17 each
  (`/fast/scratch/.../var-claims-r2-*.out`).

## Classification of the 215 changed CLAIM lines (artifact `changed-records.txt`)

An independent Python re-derivation (top-level fields from `json.loads` with a
duplicate-key hook) checked every changed record:

```
files_with_diffs=7 changed_records=215 nested_or_decoy=152 duplicate_read_key=63 violations=0
```

- **152** records have a nested/array value whose member name collides with a read field
  (`line`, `sha256`, `source`, `id`, `span`, `expect`, `marker`) and no duplicated read key.
  Landed prints the top-level `id`/`source`/`expect`; no nested `line`/`sha256`/`marker`
  leaks (no `mislocated`/`stale`/invalid caused by a decoy). Base prints the decoy
  (`observed=mislocated`, `stale`, `invalid`) or the decoy `id`/`source`.
  This is exactly contract item 1.
  Example: `.ufo/waves/round-33/w1/ExecC1Build/nested-decoy-probe.jsonl:4` (M4): base
  `observed=invalid` + `sha256 malformed` from `arr.deep[0].sha256`; landed
  `observed=refused` (top-level fields only).
- **63** records duplicate a top-level read key (`line` 20, `sha256` 20, `source` 20, `id` 3).
  Landed: `observed=invalid` + `FINDING … duplicate top-level key <k>`; identical duplicated
  `id` keeps `id=DI1`, differing/non-string `id` prints `id=lineN`
  (`dup-id-probe.jsonl`, as `claim-record-fields-r33.md` states). Contract item 2 v2.
- **0** changed records without nesting or a duplicated read key → contract item 4 holds on
  the committed corpus.

## Adversarial probes the counter does not generate (artifact `probe-summary.txt`)

Root `/fast/scratch/.../probe-root` with a real source `src/a.md`; same `--root` both gates.
- 45-record probe + 27 flat twins: every nested record's CLAIM line equals its twin's
  field-for-field; every duplicate read key invalid; nested-only `id`/`source`/`span`/
  `expect` never supplies a missing top-level field (landed: invalid/unproven, base: uses
  the nested value); nested-only `line`/`sha256`/`marker` change nothing.
- 120 random nested records carrying decoy names in random containers: 0/120 differ from
  their 120 flat twins (landed).
- 120 flat records with adversarial string content (`\"`, `\\`, trailing escaped backslash,
  `{ } [ ] : ,`, `\u007b…`, unicode): base vs landed 0/120 differ.
- 400 random valid JSON records (nested decoys, escapes, numbers, empty containers):
  `RESEARCH_GATE: CLEAN`, supported=400, invalid=0 → no valid object is falsely refused.
- Valid-JSON edge set (`a\"b` keys, empty key, `}]{\"` inside nested strings, surrogate
  pairs + `\u0000`, `1E+2`, tabs-as-whitespace, 50 nested members): landed CLEAN 14/14;
  base DRIFT 13/14 (V11, a nested `sha256` decoy) — landed fixes base, not breaks it.
- Malformed: 5/5 non-objects invalid on landed (base accepted 4/5).
- Duplicates file (18 lines): 14 invalid (12 duplicate read keys, duplicate `marker`,
  duplicated `marker_default` row), 3 valid, one `marker_default` row consumed; a
  `marker_default` default still applies to a later contradicted claim (Q15).
- `{}`/`{ }` and a UTF-8 BOM record: base == landed.

## Counter runs (kill rule; every run on a gate reported)

Landed revision gate `94a7be5a…`, `c1-count-v2.py` sha256 `cb354dd1…e514`, stdout
redirected, receipts in the wave dir:

| seed | gate sha256 in receipt | label | predicate_holds | receipt |
|---|---|---|---|---|
| 34111 | `94a7be5a…506e` | `TOPLEVEL_FIELD_MATCH=156/156` | true, gate_rc=1 | `c1-landed-pristine-seed34111.json` |
| 34112 | `94a7be5a…506e` | `TOPLEVEL_FIELD_MATCH=156/156` | true, gate_rc=1 | `c1-landed-pristine-seed34112.json` |
| 34103 (base gate) | `f4731885…f0` | `TOPLEVEL_FIELD_MATCH=60/156` | false | `c1-base-seed34103.json` |

Two earlier runs, **reported because they ran** (seed 34101, 34102, `--gate
tools/research-gate.sh`): both printed 156/156, but their receipts hash `fc08410e…` and
`45d76b4f…` — the lane working-tree gate was being rewritten by another process between
the two runs, so these are **not** runs on the landed gate and do not count for P1. Their
outputs are kept (`c1-landed-seed34101/34102.*`).

## Artifacts (all in `.ufo/waves/round-33/w2/NoHarmCorpus33/`, 388 KiB)

- `summary.tsv` (35-file table), `changed-records.txt` (215-record check),
  `probe-summary.txt` (probe counts + sha256 of the scratch outputs).
- `c1-landed-pristine-seed3411{1,2}.{json,out}`, `c1-base-seed34103.{json,out}`,
  `c1-landed-seed3410{1,2}.*` (moving-gate runs, reported above).
- `probes/` — the 11 adversarial claims inputs; `outs/` — 18 probe base/landed outputs.
- Scratch keeps the full per-file corpus run (`.../chousa-r33/w2/NoHarmCorpus33/out1/`,
  70 files, cited by `summary.tsv`) and `run-all.sh`.

## Risks / blockers

- **Lane working tree was mutated during wave 2**: `tools/research-gate.sh` is now
  `154f7d3d…` (`git diff --stat`: 113 insertions, 45 deletions vs HEAD) while HEAD stays
  `94a7be5a…`. I did not touch it. Any receipt that hashed the lane path rather than a
  pristine copy may name an uncommitted intermediate; the L1 should re-pin.
- Limits of this seat: `verify-claims` only (stdout+exit), no other mode; all probes are
  valid/invalid JSON lines I wrote, not new natural corpus. `claim_scan` still accepts
  non-JSON scalar tokens and missing commas/colons *inside skipped nested values*
  (`mal-smuggle.jsonl` X5/X6/X7/X11/X13/X15/X16) — same or stricter than base, explicitly
  outside P1 v2 (`claims.md` "Not claimed"), so no claim is made about it.
- No installs, no network, no lane writes; my artifacts total 388 KiB (no file >1 MiB).
