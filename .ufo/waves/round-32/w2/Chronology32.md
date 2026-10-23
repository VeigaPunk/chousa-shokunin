# Chronology32 — round-32 chronology falsification

**Verdict: HOLDS, scoped to the committed chronology through `5d8a170795dcf48c3746a4f03dee9cfe32812834`.** No reproduced counterexample: none of the named candidate/build-gate counter receipts precedes the last control commit; neither v2 counter changes after a candidate receipt. This is not an admission or a behavioral judgment.

**Axes attacked:** C1 operability and C2 coverage, specifically the provenance of their frozen measurements. The applicable freeze and sequencing statements are `corpus/evidence/round32/claims.md:99-103,119-125,184-189`.

## Commands and immutable scope

The requested command was run read-only, exit 0:

```text
timeout 120 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --format='%H %cI %s' 7a7259f0ad41a68068131bfa422a829db9fd1b55..5d8a170795dcf48c3746a4f03dee9cfe32812834
```

The corresponding `git log -p ... -- corpus/evidence/round32/`, the counter-only raw history, the gate/measurement history, the pinned evidence inventory, and `git cat-file --batch` reads also exited 0. Exact invocations and exit codes: `Chronology32/commands.json:1-74`. Full requested history output: `Chronology32/commit-log.txt`; full round32 diff history: `Chronology32/round32-history.patch`.

The receipt audit used committed blobs, not a potentially changing worktree: 1,162 files under `controls/`, `w1/`, and `measure/`; all 778 JSON files parsed; 508 top-level counter receipts identified by `gate_sha256`, `utc`, `counter_sha256`, `matched`, and `total`. All JSON dictionaries were also recursively searched for the four named gate hashes under `gate_sha256`/`gate_sha`. There were exactly four matching references, all the measurement receipts below. Evidence: `Chronology32/chronology-audit.json:2-19,66-90`; reproducible input identities: `Chronology32/committed-inventory.tsv`; receipt metadata: `Chronology32/receipt-index.json`.

## Observed ordering

Times below are normalized to UTC from the requested **committer** `%cI` values, not filesystem modification times. Source: `Chronology32/timeline.tsv:2-11` and `Chronology32/commit-log.txt`.

| Event | Commit | UTC on 2026-10-23 |
|---|---|---|
| Design v1 | `4111607c857bc29ff31883bc095ae00afb527e50` | 06:09:40Z |
| Design v2 | `3d586d3ae2818193e51a4b2d9e6190157165c319` | 06:59:48Z |
| Control/oracle/build evidence | `f43dd5a3a78d33d3d16a56e8a8e90325a094de04` | 07:13:17Z |
| Last control evidence | `a065845a5bdaf803b14dc7c7837a7a947e39c7db` | 07:20:56Z |
| Candidate gate | `0f96bc1c815f6600b5f1b5cae6d41f4a7a4bc28c` | 07:21:04Z |
| Measurement commit | `5d8a170795dcf48c3746a4f03dee9cfe32812834` | 07:25:26Z |

All four candidate receipts bind gate SHA-256 `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`, which also hashes identically in the candidate and measurement commits (`Chronology32/frozen-hashes.json:26-37`). Their recorded starts are:

| Receipt under `.ufo/waves/round-32/measure/` | Recorded UTC | Recorded score | Original evidence |
|---|---|---|---|
| `after-c2-s32011.json` | 07:21:14Z | 132/132, true | file lines 4-15 |
| `after-c2-s32012.json` | 07:21:22Z | 132/132, true | file lines 4-15 |
| `after-c1-s32001.json` | 07:21:31Z | 24/24, true | file lines 5-15 |
| `after-c1-s32002.json` | 07:23:15Z | 24/24, true | file lines 5-15 |

Thus the earliest candidate receipt starts **18 seconds after** the last control commit, and **10 seconds after** the candidate commit (`Chronology32/timeline.tsv:5-7`). Here `utc` is the counter's captured start time, not its receipt-write time: `corpus/evidence/round32/c1-count-v2.py:311,358-363` and `c2-count-v2.py:296,369-374`.

The named build hashes `3144a46f…`, `2a21aa43…`, and `82470e57…` have **zero** matching JSON receipts in this pinned inventory (`Chronology32/chronology-audit.json:12-19`). Their identities were opened in `w1/ExecC1Build.md:3-13`, `w1/ExecC2Build.md:3-10`, and `w1/ExecR2Selftest31.md:16-26` (all paths relative to `.ufo/waves/round-32/`). The C1/C2 executor reports explicitly distinguish self-verification from counter scoring; those report sentences are corroborative, not the basis for the absence result.

## Counter-freeze attack

**No v2 counter modification appears after any candidate receipt in the requested committed history.** The counter-only log contains exactly their two additions at design v2, with no later entries (`Chronology32/counter-history.txt:1-4`). The complete round32 diff history adds `r31-repairs.md` in the candidate commit but does not edit either v2 counter there (`Chronology32/round32-history.patch`).

Frozen and landed SHA-256 values match, and match all four candidate receipt counter identities:

- C1: `e6bf95313ad603ff75e03bb64fbe5a2689a9dfe9bc4c0715a21012383508d891` — `Chronology32/frozen-hashes.json:2-12`; candidate receipt files lines 5.
- C2: `8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a` — `Chronology32/frozen-hashes.json:14-24`; candidate receipt files lines 4.

## Correction and limits

**Smallest safe correction: none indicated by this chronology attack.** No chronology defect or axis harm was reproduced. The evidence supports the stated order and counter immutability within the pinned record only.

Commit timestamps and receipt UTC fields are locally recorded metadata, not independently attested wall-clock proof. This review cannot exclude unrecorded executions, transient uncommitted historical edits, or receipts outside the pinned `controls/`, `w1/`, and `measure/` inventory. It does not assess gate semantics, source-row accuracy, or overall claim admission. No counter, gate, selftest, network request, package install/update, or background job was run by this seat; all subprocesses completed synchronously. Only this report and bounded artifacts under `w2/Chronology32/` were written.
