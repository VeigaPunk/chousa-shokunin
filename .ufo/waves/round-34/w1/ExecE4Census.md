# ExecE4Census — routed repair E4 (measurement binding), round-34 wave 1

Seat: `ChousaR34.ExecE4Census`. Date: 2026-10-23. Lane repo:
`/home/vgpnk/Projects/shokunin/chousa-shokunin` (jj-colocated, branch `master`, tip
`70feb5eacc959eb98071461fe89f0b892c0810d8`). Scope: routed repair **E4** only —
`corpus/lessons/round-33-verifier-spotcheck.md:168-171`:

> **E4 (measurement binding).** Extend QUALITY 41 to measurements: never cite a receipt whose
> `gate_sha256` is not a committed blob, and re-run any measurement after a scratch edit. Five
> wave-2 receipts are labelled `c1-landed` on uncommitted states (`NoHarmCorpus33`, `ProbeTypes33`,
> `ProbeLongLines33`). Rename them or annotate them as non-revision.

I did **not** touch lane production files (`tools/`, `corpus/`, `SCORECARD.md`, `LOG.md`,
`SKILL.md`, `README.md`, `PROVINCE.md`), the lane jj state or the lane Git index. No `git`/`jj`
write command was run. I ran **no** `c1-count.py` against any candidate implementation of C1, so
the wave's control rule is respected.

## What I built

`receipt-binding.py` — a read-only census tool (sha256
`230441acc1103d350780507c36993d87d550ea4b6602a373ad081dcf744c5943`).

It walks a directory tree of JSON receipts, reads each receipt's `gate_sha256` (and the gate path
it names), and compares that digest against the set of sha256 digests of:

* every committed blob of `tools/research-gate.sh` across `git -C <repo> rev-list --all`
  (40 distinct blobs), and
* every committed `*.sh` blob under `.ufo/waves/` (controls, mutants, mask gates, committed
  scratch-gate copies) — 175 distinct blobs, 210 distinct digests in total.

A receipt whose digest is in that set is **bound** (it names bytes that exist in repository
history). A receipt whose digest is absent is **unbound**: it was measured on bytes that were
never committed, so it cannot be cited as evidence for a landed claim. Output is one
`UNBOUND <path> <gate_sha256>` line per finding followed by totals; the exit status is **1** if
any unbound receipt carries a landed/final label (path under `measure/`, or file name containing
`landed`/`final`), else **0**. `--json-out` writes the same census as JSON.

Fallback detail: 341 round-33 receipts carry only `gate_sha256_before`/`gate_sha256_after` rather
than `gate_sha256`. The tool falls back to those (and reports a receipt unbound if *neither*
digest is bound), so there is no blind spot; in round 33 every one of those before/after digests
is bound.

## Runs (commands, exit codes, output)

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py . .ufo/waves/round-33 \
      --json-out .ufo/waves/round-34/w1/ExecE4Census/census-round33.json
   → census-round33.txt, R33_EXIT=1
$ python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py . .ufo/waves/round-32
   → census-round32.txt, R32_EXIT=1
$ python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py . .ufo/waves/round-33/w2/ProbeEscapes33
   → (no output beyond totals), CLEAN_EXIT=0
```

Artifacts (all inside my own directory `.ufo/waves/round-34/w1/ExecE4Census/`, 152 KiB total):

| file | sha256 |
|---|---|
| `receipt-binding.py` | `230441acc1103d350780507c36993d87d550ea4b6602a373ad081dcf744c5943` |
| `census-round33.txt` | `bb69d50489896bfb75fc4493e491a5a741d462d685c0755823d7b1f3f59623e9` |
| `census-round33.json` | `80d209c829db8358c012958b26f2a1aa469d764debbac1b273cdd649ba470f06` |
| `census-round32.txt` | `3267adaf8dbef3221b1412baa35b8378fc35b170fdb7d9b02faec64ca95589ca` |
| `non-revision-receipts.md` | `6f0dc84cdfa75d8552431cbb39a546bfebd426bbf9326da0b07a80749427af01` |

### Round-33 census result (`census-round33.txt`, exit 1)

```
COMMITTED_GATE_BLOBS 40
COMMITTED_WAVE_SH_BLOBS 175
COMMITTED_BLOB_HASHES 210
UNBOUND .ufo/waves/round-33/measure/final/fz-90212.json b2c07edae3a4e2beed90ad51ee06f27515c6aec82ee26651feca5118d6579b4b
UNBOUND .ufo/waves/round-33/measure/final/fz-90213.json b2c07edae3a4e2beed90ad51ee06f27515c6aec82ee26651feca5118d6579b4b
UNBOUND .ufo/waves/round-33/measure/final/fz-90214.json b2c07edae3a4e2beed90ad51ee06f27515c6aec82ee26651feca5118d6579b4b
UNBOUND .ufo/waves/round-33/w2/NoHarmCorpus33/c1-landed-seed34101.json fc08410ea00f28ab2921ba344c4f38c223541ec40336708a44650643bfe405d1
UNBOUND .ufo/waves/round-33/w2/NoHarmCorpus33/c1-landed-seed34102.json 45d76b4fc7c572c61a31b47608303c02e4c65b392b2824aa7561bda2834e3044
UNBOUND .ufo/waves/round-33/w2/ProbeTypes33/c1-landed-s4202.json 45d76b4fc7c572c61a31b47608303c02e4c65b392b2824aa7561bda2834e3044
UNBOUND .ufo/waves/round-33/w2/FuzzDiff33/full-90214.json 45d76b4fc7c572c61a31b47608303c02e4c65b392b2824aa7561bda2834e3044
UNBOUND .ufo/waves/round-33/w2/ProbeLongLines33/c1-v2-seed5187.json 45d76b4fc7c572c61a31b47608303c02e4c65b392b2824aa7561bda2834e3044
UNBOUND .ufo/waves/round-33/w2/ReviewC1Diff/c1-v2-s4117.json b808e9b5e6d3b34473d96dc07a9ce5c6c30695722ece14c83217e7f1e88e55e4
TOTAL_RECEIPTS 1060
TOTAL_WITH_GATE_HASH 975
TOTAL_BOUND 966
TOTAL_UNBOUND 9
TOTAL_UNBOUND_LANDED_FINAL 6
TOTAL_UNBOUND_OTHER 3
TOTAL_NO_GATE_HASH 85
TOTAL_UNPARSEABLE_JSON 0
```

**The E1 able-to-fail case is caught.** `measure/final/fz-9021{2,3,4}.json` are listed as UNBOUND
on gate digest `b2c07eda…9b4b` — the scratch state the spot-check names
(`corpus/lessons/round-33-verifier-spotcheck.md:74`, "matches no committed blob"). Independent
confirmation that the digest is in no committed blob of any kind (not merely no gate revision): I
hashed every blob reachable from `git rev-list --all --objects` (9772 objects with paths, of which
8201 are blobs) and `b2c07eda…` appears in none of them. The receipts also
carry **no** `gate` path at all — only the orphan digest — so the digest is the sole binding
evidence and it does not resolve.

**The five wave-2 `c1-landed` receipts the spot-check names are all caught.** Filtering the round-33
census to receipts carrying the frozen counter `cb354dd1…` yields exactly five unbound wave-2
receipts, and they are precisely the five the spot-check's kill-rule census calls "three
never-committed worktree states: `45d76b4f` ×3 (156), `fc08410e` ×1 (156), `b808e9b5` ×1 (0)"
(`corpus/lessons/round-33-verifier-spotcheck.md:70`, repeated at `:146`):

| receipt | gate_sha256 | label | utc |
|---|---|---|---|
| `w2/NoHarmCorpus33/c1-landed-seed34101.json` | `fc08410e…` | `TOPLEVEL_FIELD_MATCH=156/156` | 09:10:09Z |
| `w2/NoHarmCorpus33/c1-landed-seed34102.json` | `45d76b4f…` | `TOPLEVEL_FIELD_MATCH=156/156` | 09:10:31Z |
| `w2/ProbeTypes33/c1-landed-s4202.json` | `45d76b4f…` | `TOPLEVEL_FIELD_MATCH=156/156` | 09:10:27Z |
| `w2/ProbeLongLines33/c1-v2-seed5187.json` | `45d76b4f…` | `TOPLEVEL_FIELD_MATCH=156/156` | 09:10:30Z |
| `w2/ReviewC1Diff/c1-v2-s4117.json` | `b808e9b5…` | `TOPLEVEL_FIELD_MATCH=0/156` | 09:10:50Z |

A sixth wave-2 receipt, `w2/FuzzDiff33/full-90214.json`, is also unbound on `45d76b4f…` but
carries no counter digest, so it falls outside the spot-check's counter-filtered census; the
spot-check lists it separately at `:75`.

All four distinct digests (`45d76b4f…`, `fc08410e…`, `b808e9b5…`, `b2c07eda…`) are absent from
all 8201 committed blobs in the repository. Cross-check: the lane's own seat reports already disclose
three of them — `ProbeTypes33.md:34` prints `45d76b4f…` in bold, `ProbeLongLines33.md:101-120`
(F2) explains that a default-`--gate` run hashes the live worktree, `FuzzDiff33.md:60` says the
same digest is "**working-tree state, not in any commit**", and `ReviewC1Diff.md:15` marks
`b808e9b5…` "(NOT landed)". E4 is therefore a *labelling* defect (the receipts are cited as landed
evidence) rather than a hidden measurement — the digests were disclosed but the citations were not
corrected.

**No landed-evidence receipt is affected.** `measure/final/c1v2-s370{1,2}.json` and
`measure/final/c2v3-s370{3,4}.json` bind `43a1af35…4346`, which *is* the committed tip blob
(`git rev-parse HEAD:tools/research-gate.sh` → `eebec67f1304c6bf4ecc162aa703a7e1ec135643`,
`git show HEAD:tools/research-gate.sh | sha256sum` → `43a1af35…`). They are bound and remain
citable. 966 of the 975 gate-digest-bearing round-33 receipts are bound.

### Round-32 census result (`census-round32.txt`, exit 1) — beyond the routed scope, reported

Same census over `.ufo/waves/round-32/`: 381 unbound receipts, of which **18** carry a landed/final
label (16 × `cf1f234e…` under `w1/MutC1CounterB/final-newline-*`, 2 × `3ceb0a80…` under
`w2/RerunC2b/c2-landed-run{A,B}.json`). Only 19 `*.sh` files under round 32 were ever committed,
so nearly every wave-2 mutant/probe gate copy lives in scratch only; the 363 non-labelled rows are
mutant/attack evidence, not landed claims. This is the same class of defect one round earlier and
is routed to the lane as an observation, not a change I made.

## Annotation file

`non-revision-receipts.md` (in my directory) drafts the annotation text. It lists **every** UNBOUND
receipt with its hash and the disposition sentence *non-revision (uncommitted gate bytes); not
evidence for any landed claim* — all 9 round-33 rows individually (with gate path, label, counter
digest and utc), the 18 round-32 landed/final rows individually, and all 381 round-32 rows in a
per-receipt appendix (409 rows carry the disposition sentence). It also proposes the repair wording
the lane can commit as the QUALITY-41 extension.

## Evidence index (path:line)

* E4 routing text: `corpus/lessons/round-33-verifier-spotcheck.md:168-171`.
* E1 able-to-fail statement: `corpus/lessons/round-33-verifier-spotcheck.md:160-167`; the
  spot-check's own finding that `b2c07eda…` "matches no committed blob" is at `:106`.
* Seat-level disclosures of the unbound digests: `.ufo/waves/round-33/w2/ProbeTypes33.md:34`,
  `.ufo/waves/round-33/w2/ProbeLongLines33.md:101-120`,
  `.ufo/waves/round-33/w2/FuzzDiff33.md:60`, `.ufo/waves/round-33/w2/ReviewC1Diff.md:15`.
* Bound tip blob: `git rev-parse HEAD:tools/research-gate.sh` → `eebec67f13…`; digest
  `43a1af35ca668fe535fcef1e68b0c64bbba3eada59c7a23181f591901fca4346`.

## Verdict

E4 is **reproduced and mechanised**. The census tool exits 1 on the round-33 tree and names
exactly the receipts the routed defect describes: `measure/final/fz-9021{2,3,4}.json` on
`b2c07eda…` (E1's able-to-fail case) and the five wave-2 `c1-landed`/never-committed receipts.
All four offending digests are provably absent from every committed blob in the repository. The
annotation file supplies the "non-revision" wording the lane needs, and the tool is the
re-runnable check that keeps QUALITY 41 honest after any future scratch edit.

## Limits and risks

* The census binds a receipt by **digest only**. A receipt whose digest happens to equal some
  committed blob (e.g. `263ffb9d…`, committed as
  `.ufo/waves/round-33/w2/ProbeNestedOnly33/gate-worktree-263ffb9d.sh`) is reported bound even
  though the *path* it names was scratch at run time. Digest binding is the weaker-but-correct
  test E4 asks for; path binding is a stricter variant the lane may want as QUALITY 41b.
* The `landed`/`final` label test is lexical (path segment `measure`, or file name containing
  `landed`/`final`), so it can miss a receipt that claims "landed" only in its prose label. In
  round 33 the two receipts whose prose labels say `NOT landed` (`ReviewC1Diff`) are correctly not
  counted as landed evidence.
* Round-32 numbers are outside the routed scope; I report them as an observation only and did not
  modify round-32 bytes.
* I did not run the gate, the counters or the fuzz harness, and did not run `c1-count.py` against
  any C1 candidate — per the wave's control rule and PROTOCOL §Gate standard.
* No tool was installed for this seat (none needed; the census is stdlib Python 3).
