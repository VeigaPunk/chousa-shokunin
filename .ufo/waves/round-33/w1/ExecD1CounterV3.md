# ExecD1CounterV3 — C2 counter v3 (metadata decoupled) + control-only battery

Round 33, wave 1, lane `chousa-shokunin` @ `3b528b9a926dd53001a1f1da5df6be1c63fca3ca`.
Routed defect: D1, `corpus/lessons/round-32-verifier-spotcheck.md:152-158` — the round-32 C2
counter wrote the 36 resolvable sources first, so a control that ranked files by
mtime/inode scored 132/132 without opening a source.

## Verdict

- **D1 is repaired in a new counter, and the repair is shown by the exact control that
  exploited it.** `.ufo/waves/round-33/w1/ExecD1CounterV3/c2-count-v3.py` decouples fixture
  metadata from truth; the committed `w2/CriticAxis32/metadata-control.sh` (byte-identical,
  sha256 `79c4f44e…`) scores **132/132 on both seeds under v2** and **96/132 and 95/132 under
  v3**. The criterion is now able to fail.
- **Controls only.** The landed gate `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`
  was never invoked by this seat, and neither counter was edited (`c2-count-v2.py` still
  `8ec1a1ed…`). No candidate C1/C2 implementation was scored.
- No lane production file was modified. Everything below lives under
  `.ufo/waves/round-33/w1/ExecD1CounterV3/` (~0.5 MiB, largest member the 265 KiB round-31 gate copy) and scratch
  `/fast/scratch/hyaku/chousa-r33/w1/ExecD1CounterV3/`.

## What v3 changes (5 hunks, 44 changed lines; `v2-v3.diff`)

1. Docstring: v3 header naming D1 and the mechanism.
2. `generate()` now **plans** every source (`put_file` appends `(directory, name, body)` and
   returns the name) instead of writing it inside the class loop; the class loop therefore
   fixes bodies but no longer fixes write order.
3. After the hops/sources shuffles: `rng.shuffle(planned)` then write every file in that
   shuffled order, and immediately stamp `os.utime(path, ns=(atime, mtime))` with both values
   drawn from `randrange(2020-01-01T00:00:00Z, 2027-01-15T08:00:00Z)` in ns, mtime forced
   distinct. Record file also gets an independent random stamp.
4. First stdout line is now
   `COUNTER c2-count-v3 schema=chousa-r32-c2-receipt/v3 metadata_decoupled: true`.
5. Receipt: `schema` → `chousa-r32-c2-receipt/v3`, plus `"metadata_decoupled": true` and
   `"write_order_shuffled": true`.

Unchanged, as required: the 16 CLASS_COUNTS and `TOTAL = 132`, `source_body()` modes, the
matching rule (record checks + exactly-one-line-per-hop + finding list), per-class output,
`EXEMPT_AUDIT_MATCH=n/132`, CLI flags. Counter sha256
`6f362ece2e5e04c92212ee5a3547a69a6742c5658fd7ebc41688b68043e5a9fa`; `py_compile` ok.

## Fixture-shape audit (no gate invoked; `fixture-audit.out`)

Audit imports `generate()` with `sys.dont_write_bytecode`, parses the record as the control
does, and maps each hop to its on-disk path:

```
seed=7331 files_root=108 outside=6 truth=132 classes={'resolvable': 36, 'verified': 12, 'exempt': 84}
  top36_by_mtime: positives_in_top36=13/36  same_set_as_positives=False  distinct_mtimes=108/108
  top36_by_inode: positives_in_top36=12/36  same_set_as_positives=False
seed=7332 files_root=108 outside=6 truth=132 classes={'resolvable': 36, 'verified': 12, 'exempt': 84}
  top36_by_mtime: positives_in_top36=12/36  same_set_as_positives=False  distinct_mtimes=108/108
  top36_by_inode: positives_in_top36=16/36  same_set_as_positives=False
```

108 root files + 6 out-of-corpus files = 114; the remaining 18 hops own no file (E2 6, E3 6,
E6 6). Under v2 the top-36 by mtime *was* the 36 positive sources; under v3 it is a random
subset (chance rate 36/108 = 1/3).

## Control battery

Counter invoked as
`C2_TMP=<scratch>/tmp TMPDIR=<scratch>/tmp python3 <counter> --gate <control>/tools/research-gate.sh --seed <s> --receipt <file>`.
Seeds 7331/7332 are fresh (not 3301-3303, not round-32's 32320021/32320022).

| # | control (sha256) | counter | seed | matched | gate rc | record checks | counter exit |
|---|---|---|---|---|---|---|---|
| a | `metadata-control.sh` `79c4f44e…` | v2 | 7331 | **132/132** | 1 | ok | 0 |
| a | `metadata-control.sh` `79c4f44e…` | v2 | 7332 | **132/132** | 1 | ok | 0 |
| a | `metadata-control.sh` `79c4f44e…` | **v3** | 7331 | **96/132** | 1 | ok | 1 |
| a | `metadata-control.sh` `79c4f44e…` | **v3** | 7332 | **95/132** | 1 | ok | 1 |
| b | mtime-only ranking `c3b7db95…` | v3 | 7331 | 96/132 | 1 | ok | 1 |
| b | inode-only ranking `4705be10…` | v3 | 7331 | 95/132 | 1 | ok | 1 |
| c | no-reader (isfile) `8e430e6c…` | v3 | 7331 | 78/132 | 1 | ok | 1 |
| c | no-reader (isfile) `8e430e6c…` | v3 | 7332 | 78/132 | 1 | ok | 1 |
| d | round-31 gate `7a7259f0` `0bc318b3…` | v3 | 7331 | 0/132 | **0** | fail: gate-rc=0, drift-summary-lines=0 | 1 |
| d | round-31 gate `7a7259f0` `0bc318b3…` | v3 | 7332 | 0/132 | **0** | fail: same | 1 |

Receipts: `receipts/v2-metadata-s7331.json`, `…s7332`, `v3-metadata-s7331.json`,
`v3-metadata-s7332.json`, `v3-mtime-s7331.json`, `v3-inode-s7331.json`,
`v3-noreader-s7331.json`, `v3-noreader-s7332.json`, `v3-r31-s7331.json`, `v3-r31-s7332.json`
(all `predicate_holds: false` except the two v2 controls, which hold).

**Defect reproduction (a, v2).** Same control gate (`gate_sha256 79c4f44e…`), fresh seeds,
**132/132 twice**, exit 0 — exactly the round-32 finding, reproduced on seeds never used in
round 32. Under v3 the same bytes fall to 96 and 95: the `R1/R2/R3` classes, which scored
12/12 each for the metadata shortcut, drop to 4/12, 4/12, 5/12 and 4/12, 3/12, 5/12 — the
chance rate of picking a random third of the files.

**Variants (b).** With distinct random mtimes the "mtime then inode" key and the "mtime only"
key coincide (96/132), while "inode only" is 95/132: neither creation-order signal carries a
class label any more, because write order is shuffled and inodes follow write order.

**No-reader (c).** 78/132 on both seeds, deterministic: it is right on R1–R3 (36), F1 (12),
E5 (12) and on E2/E3/E6 (18) where no target file exists, and wrong on every class where the
file exists but the anchor decides — E1 0/12, E4 0/6, E7 0/6 (no boundary check), E8–E12
0/6 each. A gate that equates "file exists" with "anchor verified" cannot reach the label.

**Round-31 gate (d).** `git show 7a7259f0:tools/research-gate.sh` (sha `0bc318b3…`, 6982
lines) exits **0** and prints `RESEARCH_GATE: CLEAN`; its 120 U hops are all
`observed=exempt`, including the 36 resolvable ones — the pre-audit do-nothing. Because the
counter's record check requires rc 1 and one DRIFT line, it scores 0/132 rather than 96/132
with record fail. Witness, `receipts/r31-raw.stdout:2,134-135` (kept fixture, seed 7331):

```
CHAIN hop=ha3b516bb status=blocked-no-fetch observed=exempt source=fc00e992124.md anchor=- at=- verdict=exempt
RESOLVED_HOPS=12/132
RESEARCH_GATE: CLEAN (hops=132 verified=12 exempt=120 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
```

## Compliance

- Control rule: no run against the landed gate `f4731885…`; C1 (`c1-count.py`) untouched and
  unrun. Final gate `tools/research-gate.sh` read only via `sha256sum`/`git`.
- `c2-count-v2.py` unmodified (`sha256 8ec1a1ed44f1d3971a73eeace677cbedd0187563bea063ec6b680261dbb23c8a`
  re-checked after the wave). No counter patched.
- Metadata control copied byte-identically (`cmp`-equivalent sha match with
  `.ufo/waves/round-32/w2/CriticAxis32/metadata-control.sh`, and with the round-32 receipt's
  `gate_sha256 79c4f44e…`); variants differ only in the sort key.
- Process hygiene (D5): no background jobs started, no `pkill`/`killall`/`pgrep`-based kills;
  every command bounded with `timeout` (300–900 s); all fixtures under
  `/fast/scratch/hyaku/chousa-r33/w1/ExecD1CounterV3/tmp` with `C2_TMP`/`TMPDIR` set.
- No network, no installs, no git/jj writes, no lane or fleet files touched.

## Limits

- v3's ability to **admit** a correct gate is untested in this wave by design (controls only).
  The fixture is structurally v2's (same record, same class generators, same counts; only the
  write/stamp order changed), and two independent gates parse it cleanly (record checks `ok`,
  132 CHAIN lines), but the L1's post-control scoring is the first run of a real gate on it.
- The metadata shortcut still scores at chance, not zero, under v3 (≈1/3 of positives land in
  the random top-36). That is the correct behaviour of a counter that grades a gate, not of a
  fixture that punishes one.
- `metadata-control.sh` carries an inline comment claiming the generator writes R1–R3 first.
  That claim is now false for v3 by construction; the file is a frozen round-32 artifact and
  was not edited.
