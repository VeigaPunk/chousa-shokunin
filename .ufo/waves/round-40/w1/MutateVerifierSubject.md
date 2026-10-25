# MutateVerifierSubject — round-40 c2 receipt field mutations (`verifier_sha256`, `subject_counter_sha256`)

Assigned attack: on temporary copies only, alter a c2 receipt's `verifier_sha256`
and `subject_counter_sha256` **independently**; require the verifier's **named
refusals** for each mutation. Leaf seat; no subagent dispatch; no production
edits; the only lane write is this report.

Read at lane tip `6bc90e04ac60307befacd554f7eee2b7284e2652` (frozen after-measure
in `corpus/evidence/round40/measure-after.txt` was taken at `d164f88e`).
Frozen bindings: `corpus/evidence/round40/claims.md` §C1/§C2;
`corpus/evidence/round39/claims.md:88-98,119-122,179-183`.

## What was mutated and why this is a real coverage question

`corpus/evidence/round39/verify-receipts.py` re-derives two round-39 bindings:

- `:196-197` — `receipt["verifier_sha256"] != sha256_file(__file__)` →
  `VERIFY-FAIL: verifier-sha256-mismatch`;
- `:203-206` — `receipt["subject_counter"]` readable and
  `receipt["subject_counter_sha256"] == sha256_file(subject)` →
  `VERIFY-FAIL: subject-counter-sha256-mismatch`
  (`subject-counter-unreadable` when the path is missing).

The committed round-39 counter's `verifier-subject-rebind` cell exercises the
*reciprocal* shapes: a weakened verifier **copy** adjudicating an honest receipt
(cell 2) and a subject **path** re-point with the honest digest kept (cell 3,
`corpus/evidence/round39/c2-count.py:264-346`). It never mutates either
**receipt field** itself. A plausible defect — field mutation re-sealed so the
self-digest gate is passed — would therefore be uncovered by the committed
scenarios. That is the mutant this seat attacks.

## Detector (identical in every row)

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin
python3 -E corpus/evidence/round39/verify-receipts.py \
  --receipt <temp-copy.json> \
  --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh \
  --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/c2-count.py \
  --expectations /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/expectations.jsonl
```

This is the argv/env shape of the round-39 counter's `run_verify`
(`c2-count.py:116-122`, scrubbed env). Probe 2 additionally re-ran the two
headline mutants in the **exact C1-wrapper shape** used by
`corpus/evidence/round40/c1-count.py:30-34` (`sys.executable` without `-E`,
caller env, cwd = lane root) — identical results, so the refusals are not an
artifact of `-E` or env scrubbing.

Mutation construction (scratch `probe.py`): load the committed receipt, set
**one** field, recompute `receipt_sha256` with the verifier's canonical body
digest (`json.dumps(body, indent=2, sort_keys=True) + "\n"`), write the copy.
Every mutated copy therefore passes `receipt-self-digest` and reaches the
binding check — the refusal that follows is the named one, not the self-digest
gate. All copies and fixtures live only under
`/tmp/r40-mutate-verifier-scratch/`; lane files were opened read-only.

## Baselines (must pass, else a kill is inconclusive)

| Probe | Receipt | Actual | Verdict |
|---|---|---|---|
| B1 | `corpus/evidence/round39/receipts/c2-after-s39101.json` (lane bytes) | rc 0, `VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py` | BASELINE-OK |
| B2 | `corpus/evidence/round39/receipts/c2-after-s39121.json` (lane bytes) | rc 0, `VERIFY: ok receipt=c2-after-s39121.json …` | BASELINE-OK |
| B3/B4 | copies, canonical re-seal only, bindings untouched | rc 0, `VERIFY: ok …` (bytes identical to pristine) | CONTROL-OK |

No inconclusive rows. B3/B4 prove the harness's re-seal is byte-identical to
the committed sealing, so resealing cannot be blamed for any refusal below.

## Mutation matrix A — `verifier_sha256` field only (subject binding honest)

Expected detector for every row: exit 1 with `VERIFY-FAIL: verifier-sha256-mismatch`.

| Probe | Receipt | Mutated value | Copy SHA-256 (mutated) | Actual | Verdict |
|---|---|---|---|---|---|
| M1 | 39101 | digest of a **weakened verifier copy** (`280918f0…`, census refusal replaced by `pass`) | `0f8b77a411f2735479ee74e63af8c587074b2b2d8e215a996c59035633612469` | rc 1, `VERIFY-FAIL: verifier-sha256-mismatch` | KILLED |
| M2 | 39101 | one-nibble flip of the honest digest | `353a5368d61c258059b43a50810ab256d5e9fe827dd1199b10d5fa9c65a1d8e9` | rc 1, same refusal | KILLED |
| M3 | 39121 | digest of the **round-38 verifier bytes** (`33c7c87e…`) | `8bf5ae996b89ffb357222108da39c0c8308eaa7203403e363b4c7702b39df040` | rc 1, same refusal | KILLED |
| M5 | 39101 | cross-bound: digest of `round39/c1-count.py` (`91618e91…`) | `d7fbb9e480ede70829184ef179944d8f1140b4ee0314de55a9659a04e82a389e` | rc 1, same refusal | KILLED |
| M6 | 39101 | `null` (type confusion) | `7e5436b902013060845bb28f15f03c8ad0a5249c3810c9f0bd97c318bc469e4b` | rc 1, same refusal | KILLED |

## Mutation matrix B — `subject_counter_sha256` field only (verifier binding honest)

Expected detector for every row: exit 1 with `VERIFY-FAIL: subject-counter-sha256-mismatch`.

| Probe | Receipt | Mutated value | Copy SHA-256 (mutated) | Actual | Verdict |
|---|---|---|---|---|---|
| S1 | 39121 | digest of a **doctored `c1-count.py` copy** (`eb3c3228…`; subject path unchanged) | `fc1714ae170015099491eef0b7fed382704e7b550f447e9d1a80c9407ca8514e` | rc 1, `VERIFY-FAIL: subject-counter-sha256-mismatch` | KILLED |
| S2 | 39121 | one-nibble flip | `365cf2aff1b8f46885f6898b93f782f7b527f3fdeb27197e6c3f961507ce1e83` | rc 1, same refusal | KILLED |
| S3 | 39101 | same doctored-subject digest, **other active c2 receipt** | `a249f59400054a91f74ed7068b8234731f6070e4b32f078e5c98b152c725e9f6` | rc 1, same refusal | KILLED |
| S5 | 39121 | cross-bound: digest of `verify-receipts.py` (`1b6e0de6…`) | `9fcd8fcbfe4e0d8593573aa757bb41be0b82b5307b2332f45723476242c540ea` | rc 1, same refusal | KILLED |
| S6 | 39121 | `null` | `5b5410d2c740d0a340de47a799eaea6d0d184c54e04c815652e7431202e361bf` | rc 1, same refusal | KILLED |

Independence evidence (`diffkeys.txt`): the M1 exemplar changes exactly
`{receipt_sha256, verifier_sha256}` and the S1 exemplar exactly
`{receipt_sha256, subject_counter_sha256}` against the pristine body; every
other binding field is byte-identical. Each matrix leaves the other binding
honest, and no output contains the other family's refusal.

## Ordering controls (why re-sealing is required to see the named refusals)

| Probe | Mutation | Actual | Reading |
|---|---|---|---|
| M4 | `verifier_sha256` nibble flip, **not** re-sealed | rc 1, `VERIFY-FAIL: receipt-self-digest` | caught earlier at `:129`, not the binding |
| S4 | `subject_counter_sha256` nibble flip, not re-sealed | rc 1, `VERIFY-FAIL: receipt-self-digest` | same |
| M8 | both fields wrong, re-sealed | rc 1, `VERIFY-FAIL: verifier-sha256-mismatch` | deterministic order: `:196` before `:205` |

## Reciprocal / boundary probes

| Probe | Setup | Actual | Verdict |
|---|---|---|---|
| R1 | weakened verifier copy adjudicates the honest 39101 receipt | rc 1, `VERIFY-FAIL: verifier-sha256-mismatch` | KILLED — matches committed cell 2 |
| R2 | `subject_counter` re-pointed at doctored copy, honest digest kept, re-sealed | rc 1, `VERIFY-FAIL: subject-counter-sha256-mismatch` | KILLED — matches committed cell 3 |
| R4 | identical-bytes verifier copy (different path) adjudicates the honest receipt | rc 0, `VERIFY: ok …` | CONTROL-OK — content-addressed binding, path not bound (documented: verifier docstring, "receipt-path symlink identity is not bound") |
| R3 | subject path **and** digest both re-derived to the doctored copy, re-sealed | rc 0, `VERIFY: ok …` | CONTROL-OK — the **documented** round-37 F2 residual (`corpus/evidence/round39/claims.md:179-183`, verifier docstring "Re-pointing WITH a re-derived digest is a new self-consistent receipt"): a new self-consistent receipt, not a forgery of the old one. Not a coverage kill; no contract change proposed. |

## Restoration and lane integrity

- Each mutated copy was restored with the pristine source bytes immediately
  after its detector run and re-verified: every `*-restored` row is rc 0,
  `VERIFY: ok …`, and `sha256(restored) == sha256(pristine)` — e.g. M1
  `0f8b77a4…` → `c56c1770…` (pristine), S1 `fc1714ae…` → `72bb45da…` (pristine).
  Final scratch copy hashes equal the lane receipt hashes.
- Lane files were never written by this seat. Before/after hashes across the
  probe matrix are identical (`LANE_STATE` in `transcript.txt`, matching the
  pre-run `sha256sum`):
  - `corpus/evidence/round39/verify-receipts.py` `1b6e0de688deda7493db3af5397d1e5bbf1fcdf556d8e254acae3ac6a8496267` (git blob `4e4be706…`)
  - `corpus/evidence/round39/c2-count.py` `43849e9ab313dfb52e39fcead83db68b3887c9ae8da016d9c9191f881780f1fb` (blob `fe17f0d7…`)
  - `corpus/evidence/round39/c1-count.py` `91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5`
  - `corpus/evidence/round39/expectations.jsonl` `01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a`
  - `tools/research-gate.sh` `4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3` — the probe-time value, equal to `HEAD:tools/research-gate.sh`; a concurrent seat changed the worktree file after this matrix, see below
  - `corpus/evidence/round39/receipts/c2-after-s39101.json` `c56c17704c673a9fd4a8ddb15be07e31c684a854dbe432a7304b8bd5868ff743` (blob `6cc81601…`)
  - `corpus/evidence/round39/receipts/c2-after-s39121.json` `72bb45da25581f638646828b2ee3b8c85c303ff2f8390044c0284a527a4162e9` (blob `755a2260…`)
- Baseline C1 run at the probe tip (read-only): `python3 corpus/evidence/round40/c1-count.py`
  → all six rows `ok VERIFY: ok …`, `R39_ACTIVE_RECEIPTS=6/6`, exit 0
  (`c1count-baseline.txt`). This is the wrapper whose c2 rows my mutant copies
  are *not* part of; the lane population is untouched.
- `git status` at probe time showed only sibling seats' untracked reports and
  the pre-existing `M .ufo/waves/round-40/w1/swarm-registry.json`; this seat
  wrote nothing outside its report.

## Concurrent worktree change observed after the matrix (not this seat)

While finalizing this report, `tools/research-gate.sh` in the lane worktree was
modified by a concurrent actor (mtime `2026-10-24 04:23:46 -0300`, 10 s after
this report was first written): `git diff` shows +85 uncommitted lines headed
"capture-tool pins (round-41 C1)"; `HEAD:tools/research-gate.sh` is still the
probe-time `4253c187…` blob. Observed worktree hashes moved from `4253c187…` →
`3f3f122f8db8c7188aaa3cc4afa971f7240c4ff5f61ed3210176685879941ceb` →
`77791864e79cf80fbff57e2cca393facb44ca5d00bd2331466b912534f9ce841` (still
changing as this report closed).

Consequences measured, not fixed (outside this seat's item):

- The committed c2 receipts bind `gate_sha256` = `4253c187…`; under the
  modified worktree the verifier now refuses a **pristine** receipt with
  `VERIFY-FAIL: gate-sha256-mismatch` (`:216-222`), and
  `python3 corpus/evidence/round40/c1-count.py` prints
  `R39_ACTIVE_RECEIPTS=2/6` (the four `research-gate.sh`-bound active rows
  fail on the gate binding; the base-gate and mutenv-gate rows pass).
- The assigned refusals are unaffected: both field mutants still produce
  `verifier-sha256-mismatch` / `subject-counter-sha256-mismatch` in both argv
  shapes under the changed gate (`probe2-after-gate-change.txt`), because the
  binding checks at `:196-197` and `:203-206` precede the gate check. The
  restored copies now fail only on `gate-sha256-mismatch`, which itself
  confirms restoration is byte-exact and the receipts are unmodified.
- No action taken; flagged for the L1. C1's frozen after-state binds the
  committed bytes at `d164f88`/HEAD, so this is an environmental worktree
  change, not evidence about the frozen predicate.

## Artifacts

Scratch (temporary, disposable; not lane content):
`/tmp/r40-mutate-verifier-scratch/`

| File | SHA-256 | Content |
|---|---|---|
| `transcript.txt` = `transcript2.txt` (determinism re-run, byte-identical) | `389a744818d9b8643b77b08a1a37512be49423f0495d5f8ac9fa082f9440788f` | full probe matrix, 38 JSON rows + lane hashes |
| `probe.py` | `9d60fb6c6e66cd48b16e63fff1fcc7f4c8b83ceab124ea923af944754bf920ca` | mutation harness (baselines, M1–M8, S1–S6, R1–R4) |
| `probe2.py` / `probe2.txt` | `cb5c01da18edfb0ee1809d216411e024e317d8212aa52789e4058a1d450a445c` / `66c804d8295810bbfdc80bc87ea1534d8c0b11cf5ffed26ec4439be5dc07e016` | C1-wrapper-shape vs c2-shape fidelity, both mutants, both receipts |
| `diffkeys.py` / `diffkeys.txt` | `0d5b73e325e49a2e318dd8c0b1f968ca9367982010c2e184e54188ca5465f343` / `22e83e3f2fb3b92cee3524ef5f96c02bd931c7c07056299f37effc6ec5e22d6f` | changed-key sets proving independence |
| `c1count-baseline.txt` | `913fcae6dccb1034b8843df4e7172936a97e7a47f2c8d5e99d2573e229839d3a` | C1 counter 6/6 at the probe-time gate `4253c187…` |
| `probe2-after-gate-change.txt` | `2f1dbe1feeb8f61e023828a8a970912e7c1c04a46f0c04c8594683010f9d35e8` | both mutants re-run under the concurrently modified gate: named refusals still fire; restored copies fail only `gate-sha256-mismatch` |
| `verify-weakened.py` / `c1-count-doctored.py` | `280918f0…` / `eb3c3228…` | fixture bytes bound by M1 / S1 |

Resolvable lane pointers: verifier checks `corpus/evidence/round39/verify-receipts.py:129,196-197,203-206`;
commit-time counter cells `corpus/evidence/round39/c2-count.py:146-161,264-346`;
frozen expectation rows `corpus/evidence/round39/expectations.jsonl` (`verifier-subject-rebind`);
active population `corpus/evidence/round40/active-r39-receipts.tsv:3-8`;
wrapper `corpus/evidence/round40/c1-count.py:30-34`.

## Verdict

**No surviving mutant at the assigned points.** Both receipt fields refuse by
their exact named refusal when doctored and re-sealed, **independently**, on
both active c2 receipts (`c2-after-s39101.json`, `c2-after-s39121.json`), for
three value classes (other-artifact digest, minimal nibble flip, `null`), under
both wrapper argv shapes. Matrix totals: 13 refusals — 11 at the two named
bindings (5 `verifier_sha256`, 5 `subject_counter_sha256`, 1 both-wrong
ordering row) and 2 reciprocal (R1/R2); plus 2 pre-binding
`receipt-self-digest` refusals (M4/S4) recorded as ordering controls. 0
survivors, 0 inconclusive. Re-sealed field mutation is only visible after the
self-digest gate; without re-sealing it is refused earlier as
`receipt-self-digest`, so the committed counter's scenario set does not need the
field mutations to be safe, but their absence was an uncovered cell — now
measured. The single accepted receipt doctoring (R3) is the explicitly
documented F2 residual (fully re-derived self-consistent receipt), not a breach
of the frozen predicate; R4's acceptance is byte-identity, not a doctoring. No
contract or production change is proposed. Tooling: none installed or updated.
