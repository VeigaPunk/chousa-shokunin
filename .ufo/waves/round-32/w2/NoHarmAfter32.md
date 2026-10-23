# NoHarmAfter32 — round-32 wave-2 no-harm battery on the landed gate

Seat `ChousaR32A2.NoHarmAfter32`. Lane revision **`5d8a170795dcf48c3746a4f03dee9cfe32812834`**, gate
`tools/research-gate.sh` SHA-256 **`10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`**
(equals the lane file and claims.md's candidate hash). Scratch clone
`/fast/scratch/hyaku/chousa-r32/w2/NoHarmAfter32/lane` (`git status --porcelain` → 0 lines after all
runs; HEAD unchanged). Comparator: `.ufo/waves/round-32/w1/ExecNoHarmBase32/` (gate `0bc318b3…`,
rev `4111607c…`). Every run below names gate + revision in its log's first line.

## Battery (all named targets, all matched)

| run | exit | landed result | w1 base result |
|---|---:|---|---|
| `--selftest` (timeout 1800) | 0 | `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)` | PASS (228) |
| first 228 `ok-case` lines | — | sha256 `a88730646704c3567c51258c9ed892b715b441b224f003a239d086ca1e44d924`; `cmp` vs w1 list → identical | `a8873064…` |
| full 241 case list | — | `7ee6b24c…` (`selftest.cases`) | 228 lines |
| `verify-claims corpus/fixtures/claims-r2.jsonl --root <fleet>` | 0 | `VERDICT_BEARING_CLAIMS=17/17`; CLEAN | 17/17 |
| `verify-chain corpus/fixtures/chain-r3.md --root <fleet>` | 0 | `RESOLVED_HOPS=17/22`; CLEAN | 17/22 |
| `verify-chain corpus/fixtures/chain-r3-broken.md --root <fleet>` | 1 | `RESOLVED_HOPS=1/2`; DRIFT | 1/2 |
| round-1 observable (SCORECARD `## Planned` `python3 -c`, verbatim; `research/` copied to the clone's parent so `../research` resolves) | 0 | `VERDICT_BEARING_EXPORTS=3/3` | 3/3 |
| r31 `c1-count.py` seeds 32/33 | 0/0 | `LINE_BINDING_MATCH=120/120` both | 120/120 |
| r31 `c2-count.py` seeds 32/33 | 0/0 | `REVISION_BINDING_MATCH=120/120` both | 120/120 |
| r31 `c1-count-v3.py` seeds 34/35 | 0/0 | `LINE_BINDING_MATCH=132/132` both | (not in w1) |
| r31 `c2-count-v3.py` seeds 34/35 | 0/0 | `REVISION_BINDING_MATCH=132/132` both | (not in w1) |

`<fleet>` = `/home/vgpnk/Projects/shokunin` (explicit `--root`, as assigned; fixtures' sources are
fleet-root-relative). Logs: `claims-r2.log` `1d8edbbf…`, `chain-r3.log` `d07dc948…`,
`chain-r3-broken.log` `85552a5f…`, `observable2.log` `d4463714…`, `selftest.log` `ef61997d…`.
Landed vs base gate on the chain fixtures (base copy run in the same scratch): per-hop lines
byte-identical; the only stdout delta is the timestamp and the added ` resolvable=0` token in the
summary (`base-chain-r3.log` `a90ed312…`, `base-chain-r3-broken.log` `fd72ffaa…`). The reason a first
observable attempt printed `0/3` is recorded below under "disclosures" — my setup error, re-run
correct.

## Frozen predicates, run as committed counters (real data)

`TMPDIR`/`C1_TMP`/`C2_TMP` pointed at scratch outside the lane root; `prlimit --nproc=8000`;
`timeout 900`; cwd = clone root so the default `--gate tools/research-gate.sh` is the landed gate.

| run | exit | output | receipt (my dir) |
|---|---:|---|---|
| `corpus/evidence/round32/c1-count-v2.py --seed 3301` | 0 | `APPEND_SERIALIZED=24/24`, `predicate_holds=true` | `c1-v2-s3301.json` `d21da1d9…` |
| same `--seed 3302` | 0 | `APPEND_SERIALIZED=24/24`, `predicate_holds=true` | `c1-v2-s3302.json` `087c9b99…` |
| `corpus/evidence/round32/c2-count-v2.py --seed 3401` | 0 | `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, `predicate_holds=true` | `c2-v2-s3401.json` `98bc8454…` |
| same `--seed 3402` | 0 | `EXEMPT_AUDIT_MATCH=132/132`, `predicate_holds=true` | `c2-v2-s3402.json` `073c4671…` |

Every receipt names `gate_sha256=10f2fe12…`, `counter_sha256` `e6bf9531…` (C1 v2) / `8ec1a1ed…`
(C2 v2). **No run below target.** One honest note: a first C2 seed-3401 invocation exited 2 because
my report directory did not yet exist for `--receipt` (counter printed `132/132` then
`--receipt failed: FileNotFoundError`); it wrote no receipt and was immediately re-run receipted
(logs `c2-v2-s3401b.log`; the failed invocation is superseded, not hidden).

## Contract probes the counters do not cover

1. **Manifest edges** (`c1-edges.log` `2fbfcb94…`): absent manifest created by `verify-all --json`
   → 1 line, valid JSONL; inode `709863046`; appended an unterminated fragment, second run →
   prefix bytes unchanged (`cmp`), same inode, 3 lines all `json.loads`-valid, zero blank lines.
2. **Exempt arm, independent fixture** (`exempt-edge.log` `621bf4bf…`, record `exempt-edge.md`):
   hop 1 `unresolved` with a resolvable line anchor → `observed=resolvable`, exactly one
   `FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=1`, exit 1, `resolvable=1`;
   hops 2/3 `rejected`/`not-applicable` with the same resolvable citation → `observed=exempt`, no
   finding, `anchor=- at=-`; hop 4 `unresolved` anchor absent → exempt. Matches the contract
   sentence.
3. **Refusal classes under U** (`bigroot.log` `f221befd…`): 8.4 MB source (over the read cap),
   `/etc/hostname` (out of corpus), `S9` (undeclared id) → all `observed=exempt` with no
   `CHAIN_SOURCE_*`/`CHAIN_ANCHOR_*`/`CHAIN_CITATION_*` finding; a small local control hop flagged
   `resolvable`. Matches gate doc `:109-114` and claims.md C2 contract.

## Finding (outside every predicate, reproducible): flock-less host loses the whole verify-all report

A PATH farm of `/usr/bin` minus `flock` (3725 symlinks; `command -v flock` → none), same record,
same `--root`:

- landed gate: exit **2**, stderr only `research-gate: flock(1) unavailable; manifest not written: …`,
  **no `SECTION` lines and no `RESEARCH_GATE:` verdict**, manifest not created (`nf-landed.out` `d245aa61…`);
- base gate `0bc318b3` in the identical PATH: exit **1**, full 5-section report, `RESEARCH_GATE: DRIFT…`,
  1 manifest line (`nf-base.out` `8e92b428…`).

The gate doc (`tools/research-gate.sh:214-216`) discloses "a host without flock(1) refuses to write
the manifest rather than append unlocked" but is silent that the mode also suppresses the report and
exits 2. claims.md C1's frozen contract closes with "Nothing else in `verify-all` changes" — on a
flock-less host that clause is false (stdout and exit code change, not just the append). Neither
round-32 counter can see this: they only run where `flock(1)` exists. Direction is fail-closed and
the severity is low on this host and in every receipt, but the doc sentence understates the
behavior and the contract clause does not authorize it.

## Second observation (disclosed format delta)

`verify-chain`'s summary line gained ` resolvable=N` (`tools/research-gate.sh:1987`; documented at
`:120` and in usage `:379-382`). Per-hop output is byte-identical to base on both fixtures; an exact
field-list consumer of `RESEARCH_GATE:` sees one new token. Disclosed, recorded for reviewers.

## False sentences checked

- claims.md §No harm: every value confirmed as tabulated (claims 17/17, chain 17/22 CLEAN, broken
  1/2 DRIFT, observable 3/3, r31 v2 120/120 each).
- w1 `ExecNoHarmBase32` table: all six values reproduced on the landed gate.
- Gate doc `:214-216`: true about the manifest, understated about the report (Finding above).

## Verdict

**HOLDS** on every named battery target and on both frozen predicates: C1 v2 `24/24` on two fresh
seeds, C2 v2 `132/132` on two fresh seeds, no lower run on this revision. One contract-gap finding
outside the predicates (flock-less host suppresses the report; C1's "nothing else changes" clause
fails there) and one disclosed output-format delta. If L1 reads C1's no-other-change clause
absolutely, that clause is broken on flock-less hosts; P1/P2 themselves are not.

## Limits and disclosures

- No judge/axis scoring, no candidate build, no lane/jj/git writes. Clone HEAD `5d8a1707`, clean.
- No network; no tools installed. `/fast` 214 G free; the 8.4 MB probe file was removed.
- The `pgrep` for leftover processes shows other seats' runs (`MutC2Gate`, two foreign selftests);
  none of my commands were still running (each printed its exit code).
- C1 counter runs are slow (~113-117 s each) because of the 300 ms strace delays; C2 ~26-54 s.
- My first observable attempt failed 0/3 because I copied `research/` into the clone instead of its
  parent (`../research` did not resolve); corrected with the tree at the parent, logged as
  `observable2.log`. Environment note only, not a gate result.
- No `--json` concurrency beyond the C1 v2 counter's own trials and my sequential edge test.

Artifacts in this directory: the 4 candidate receipts, 4 counter stdout logs, 8 r31 receipts, 8 r31
logs, selftest log + case list, fixture logs, base-gate comparison logs, and the three probe logs
(all < 1 MiB, 176 K total).
