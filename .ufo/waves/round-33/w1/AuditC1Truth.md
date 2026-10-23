# AuditC1Truth — round 33 wave 1: independent truth audit of the C1 counter

Seat: ChousaR33.AuditC1Truth (leaf executor). Item: no candidate involved — audit the frozen C1
counter's fixture and hidden truth against an independently written verifier, on the **base** gate
(do-nothing control). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`, branch master, tip
`3b528b9a926dd53001a1f1da5df6be1c63fca3ca`.

## Identity and control-rule compliance

- `sha256sum corpus/evidence/round33/c1-count.py tools/research-gate.sh` (exit 0):
  `ab6b2ae24f6b402e66b583fa0021742204f12bdb4f1b056f8598cd63dc43e229` (counter; equals claims.md)
  and `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0` (gate; equals base).
- The counter was run **only** against the base gate (`tools/research-gate.sh`, `f4731885…`), never
  against a patch or candidate. No counter, gate, lane production file, jj or git index was written;
  read-only `git log/status` only. No network, no installs, no background processes (nothing to
  signal; no pkill/killall used). All experiments under
  `/fast/scratch/hyaku/chousa-r33/w1/AuditC1Truth/` with `C1_TMP`/`TMPDIR` set there.

## Counter runs (base gate, fresh seeds)

Command shape (exit 1 each, label printed):
`python3 corpus/evidence/round33/c1-count.py --gate tools/research-gate.sh --seed <n> --keep <scratch>/k<n> --receipt <...>/receipt-<n>.json`

| seed | label | receipt |
|---|---|---|
| 7331 | `TOPLEVEL_FIELD_MATCH=60/144` | `.ufo/waves/round-33/w1/AuditC1Truth/receipt-7331.json` |
| 7332 | `TOPLEVEL_FIELD_MATCH=60/144` | same dir, `receipt-7332.json` |
| 7333 | `TOPLEVEL_FIELD_MATCH=60/144` | same dir, `receipt-7333.json` |
| 7334–7338 | `TOPLEVEL_FIELD_MATCH=60/144` each | `/fast/scratch/hyaku/chousa-r33/w1/AuditC1Truth/receipt-7335.json`, `receipt-7338.json` (7334/7336/7337: see Observation O1) |

All eight runs reproduce the frozen "before" baseline (`60/144`) on seeds outside 3301–3303, and the
per-class vector is byte-identical on every seed: S1 12/12, F1 12/12; N1 6/12, N2 0/12, N3 6/12,
N4 6/12, N5 0/12, N6 6/12, N7 3/6, N8 3/6, N9 3/6, N10 3/6, N11 0/6; D1 0/12; S2 0/6. Receipts
carry `counter_sha256=ab6b2ae2…`, `gate_sha256=f4731885…`, `predicate_holds=false`, `matched=60`,
`misses=84`.

## Independent verifier (not the counter's code)

`verify_truth.py` (artifact dir) re-implements the derivation from first principles:
`json.loads(line, object_pairs_hook=Obj)` keeps **top-level pairs** so duplicates are visible;
a duplicated member among the seven contract read keys → `invalid`; sha256 computed over the source
**bytes** → `stale` on mismatch; span occurrences found by scanning the decoded file with the gate's
documented token-boundary rule (whitespace/punctuation delimiters, `-`/`'` only when not word-joining,
non-ASCII = word char) → `supported` iff a delimited occurrence spans exactly the named line,
`mislocated` if delimited occurrences exist but none spans it, `unsupported` if none exist. Nested
members are never consulted (only the top-level pairs list is read), duplicates anywhere below top
level are invisible to it by construction.

Result on **8 seeds × 144 = 1152 records**:

- **0 disagreements** with `truth.json`; disagreement count is **0 in each of the 15 classes**.
- Derived tallies equal truth tallies on every seed: supported 87, mislocated 21, stale 15,
  unsupported 9, invalid 12.
- **0 invalid-JSON lines** (1152/1152 parse; independent of the counter's own `assert` at
  `c1-count.py:317`, which only checks `isinstance(..., dict)`).
- Span occurrences are unambiguous: every record's top-level span occurs **0 or 1** times in its
  top-level source (distribution `{1: 125–127, 0: 9–11}`; the 0s are the 3 F1-unsupported, 6
  N8-top-source and 0–2 D1 source-diff records). No record has >1 distinct occurrence line range,
  so no truth class can hinge on which occurrence is first.

Evidence: `audit-out-8.json`, `occ-check.json`.

### Cross-check of the gate's raw output and the counter's scoring rule

`crosscheck.py` runs the base gate inside each kept fixture and re-scores its raw
`CLAIM`/`FINDING CLAIM_LINE_MISMATCH`/`FINDING CLAIM_SOURCE_REVISION_MISMATCH` lines with the
counter's stated rule, independently of the counter:

- re-scored match = **60/144 on all 8 seeds**, identical to every receipt;
- per-class re-score identical on all 8 seeds (same vector as above);
- the gate's `observed=` agrees with the independent derived truth on exactly **60** records —
  the flat-record classes F1 12/12 and S1 12/12 — and deviates on the nested/duplicate records,
  i.e. the base gate's failure is precisely the C1 behaviour, not a fixture artefact.
- gate exit 1 (`RESEARCH_GATE: DRIFT`) every run; 144 `CLAIM` lines printed each run.

Evidence: `crosscheck-8.json`.

### Determinism / fixture integrity

`reproduce.py` re-invokes the counter's `generate()` for seeds 7331 and 7335 into fresh dirs:
`claims.jsonl` SHA-256 and **all 160 source-file SHA-256** are identical to the kept fixtures
(`same_claims True`, `same_files True`). `--keep` copies the temp root only **after** the gate run
(`c1-count.py:380-384`), so the gate never sees `truth.json`; every record's top-level
`expect` is `"supported"` and no line contains a class/truth label (grep count 0 on all 8 seeds).

## Creation order vs class

Kept-fixture caveat: `shutil.copytree` preserves `st_mtime_ns` (copy2) but assigns **new inodes in
scan order**, so kept-copy inode order is copy order, not creation order. On reproduced live
fixtures (7331, 7335) live inode order == mtime order; in the kept copies mtime↔inode Spearman is
1.0 on 4/8 seeds but 0.484, −0.120, −0.812, 0.427 on the rest — the kept-copy inode order is
therefore not a second creation-order measurement and is **not** used as the test statistic.
`st_mtime_ns` is unique on all 160 files of every seed, so it recovers the write order.

- Per-seed Kruskal–Wallis over the 15 classes on mtime rank (158 classed files; 2 unreferenced
  D1-same files excluded): H = 25.615, 11.804, 23.470, 17.522, 8.265, 15.109, 11.657, 15.631;
  permutation p (10 000 draws) = 0.023, 0.637, 0.045, 0.231, 0.889, 0.369, 0.648, 0.337. The
  nominally small per-seed p's involve **different** classes each seed (N8, N4, N1/N7), i.e. they
  do not replicate.
- Replication test (`replication.py`, 2000 draws): per class, rank-biserial r of in-class vs
  out-class creation rank, averaged over the 8 seeds, against a within-seed label-permutation null.
  max |mean r| = **0.143**, family-wise permutation p = **0.465**. Largest per class: N9 +0.143
  (p 0.095, 6/8 same sign), N6 −0.101 (p 0.103), N4 +0.095 (p 0.118); full 15-class table in
  `replication-8.json`.

Verdict: source-file creation order is **uncorrelated with class**; no class carries an
order-encoded signal, and no per-class rank correlation survives replication. (The generator's
shuffled write order needs no further repair.)

## Verdict

**No counter defect found.** The C1 counter's hidden truth is independently reproducible from the
fixture bytes on 8 fresh seeds (1152/1152 records, 0 disagreements in all 15 classes), every line is
valid JSON, the truth is not visible to the gate, the fixture is deterministic, and the base-gate
baseline (60/144) plus its class signature reproduce exactly under an independent re-score. The
counter is fit to score control and candidate gates under the frozen P1 rule.

## Observations (not counter/claim defects, nothing patched)

- **O1.** The counter prints the label and per-class lines **before** writing the receipt
  (`c1-count.py:392` vs `:395`). Piping stdout to `head` broke the pipe on the per-class print and
  the receipt for seeds 7334/7336/7337 was lost (traceback, harness-masked exit). Labels, keeps and
  re-scores are intact; the three primary receipts are complete. Suggest future runs not pipe counter
  stdout. Reported, not repaired.
- **O2.** One gate run from the lane root took 40.7 s during high host load vs 2.6 s in fixture cwd
  under the crosscheck; cause not isolated, both far below the counter's 600 s timeout.

## Artifacts

Report dir `.ufo/waves/round-33/w1/AuditC1Truth/`: `receipt-7331.json`, `receipt-7332.json`,
`receipt-7333.json`; scripts `verify_truth.py`, `crosscheck.py`, `creation_order.py`,
`replication.py`, `reproduce.py`, `occ_check.py`; results `audit-out-8.json`,
`crosscheck-8.json`, `creation-order-8.json`, `replication-8.json`, `occ-check.json`.
Kept fixtures (scratch, not in the lane): `/fast/scratch/hyaku/chousa-r33/w1/AuditC1Truth/k7331…k7338`
(each 144-line `claims.jsonl`, `truth.json`, 160 `src/` files); `claims.jsonl` SHA-256 seed 7331
`78655118c28889d7be34d994…`, 7332 `a04e03fc4b9a029b5c5922cd…`, 7333 `1c72cbd6f6051fd774416ba8…`.
