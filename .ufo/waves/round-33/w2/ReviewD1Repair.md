# ReviewD1Repair — review of the D1 repair (round-32 C2 counter v2 → v3)

Seat: ChousaR33.ReviewD1Repair, wave 2 (FALSIFY), round 33. Independent review of
`corpus/evidence/round32/c2-count-v3.py` (sha256 `6f362ece…a9fa`) vs
`c2-count-v2.py` (sha256 `8ec1a1ed…23c8a`). Counter copies and gate copies lived
under `/fast/scratch/hyaku/chousa-r33/w2/ReviewD1Repair/`; artifacts under
`.ufo/waves/round-33/w2/ReviewD1Repair/`.

## Verdict: repair HOLDS — no change to what the counter measures

The diff (`v2-v3.diff`, 6 hunks) changes only fixture write order, timestamp
stamping, one stdout banner line, and the receipt schema. Everything the counter
scores on is byte-identical, and on a fresh seed the v3 fixture scores 132/132 on
the landed gate while the round-32 metadata control falls to 91/132.

## Evidence

### 1. Unchanged measurement surface (diff-level)

- `TOTAL = 132` (v3:92 = v2:74), `CLASS_COUNTS` block byte-identical
  (`sed -n '/^CLASS_COUNTS/,/^assert/p'` on both → `CLASS_COUNTS_IDENTICAL`),
  `U`, `J`, `KINDS`, `LINE_RE`, `FIND_RE`, `FINDING_ID`, `GATE_TIMEOUT_S`,
  `sha256_file`, `Gen`, `source_body` unchanged.
- The entire matching/scoring block (`observed, dup, named` … `shutil.copytree`,
  v2:311-356 vs v3:347-393) is byte-identical: `MATCHING_IDENTICAL`. Record
  checks (rc∈{0,1}, rc==1 required, exactly one `RESEARCH_GATE: DRIFT`, no stray
  FINDING hops), the exactly-one-CHAIN-line rule, the findings-list rule, and
  `holds = matched == TOTAL` all unchanged.
- Labels unchanged: `EXEMPT_AUDIT_MATCH=%d/%d` (v3:400), per-class `%s %d/%d`,
  `RECORD_CHECKS=`, receipt `label`/`predicate_holds`/`per_class`/`misses`.
- CLI unchanged: `--gate/--seed/--receipt/--keep` (v3:309-313).
- Actual diff content: (a) docstring naming D1; (b) `put_file` defers writes —
  `planned.append((directory, n, body))` (v3:204-211); (c) after the unchanged
  `rng.shuffle(hops)`/`rng.shuffle(sources)`, `rng.shuffle(planned)` then writes
  each file and stamps `os.utime(ns=(rand atime, rand distinct mtime))` from a
  class-independent range 2020-01-01…2027-01-15Z (v3:280-295); (d) record file
  gets the same stamp treatment (v3:304); (e) new first stdout line
  `COUNTER c2-count-v3 schema=chousa-r32-c2-receipt/v3 metadata_decoupled: true`
  (v3:399) and receipt `"schema": "chousa-r32-c2-receipt/v3"` +
  `"metadata_decoupled": true, "write_order_shuffled": true` (v3:406-407).
- Consumers: `ExecNoHarmBase33/battery.sh:217,223` pins `c2-count-v2.py` and
  `has ... 'EXEMPT_AUDIT_MATCH=132/132'` — the battery is unaffected because it
  runs v2, and v3's banner is prepended, not substituted, so `grep`-style
  `EXEMPT_AUDIT_MATCH` consumers still match. No lane script expects the label
  as line 1.

### 2. Runs executed (fresh seeds 9001/9002; C2_TMP=TMPDIR=scratch; prlimit --nproc=2000 --as=4G; timeout 900)

| command | exit | result |
|---|---|---|
| `python3 c2-count-v3.py --gate <lane-copy>/tools/research-gate.sh --seed 9001 --receipt v3-landed-s9001.json --keep keep-s9001` (gate sha `94a7be5a…506e`) | 0 | `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, all 16 classes full |
| same, `--gate <metadata-control-copy>/tools/research-gate.sh` (sha `79c4f44e…` = byte-identical round-32 attack) `--seed 9002` | 1 | `EXEMPT_AUDIT_MATCH=91/132`; R1 4/12, R2 5/12, R3 2/12; every file-citing class degraded |

Receipts/stdout: `v3-landed-s9001.json` (`predicate_holds: true`,
`gate_rc: 1`, `misses: 0`) and `v3-meta-s9002.json` in
`.ufo/waves/round-33/w2/ReviewD1Repair/`. Reproduces the w1 executor's 96/95
result (`.ufo/waves/round-33/w1/ExecD1CounterV3/receipts/v3-metadata-s733{1,2}.json`)
and the w1 defect reproduction (v2 + same control = 132/132 twice,
`v2-metadata-s733{1,2}.json`).

### 3. Order-independence audit (`audit-order.py`, committed counter loaded unmodified; write order captured via `open` wrapper; class recovered from record+truth). Seeds 9003, 9004. Full JSON: `audit-order.json`.

- 108 root source files + 6 `outside/` + 1 record; 0 unmapped, 0 shared paths;
  record is write #115 (last); 108/108 distinct mtimes.
- For each of six orderings — actual write order, mtime, ctime, inode, name,
  readdir — top-36 contains 9–16 of the 36 resolvable files (chance ≈ 12) and
  never equals the positive set; max same-class run ≤ 3 (v2 gave runs of 12).
- Spearman(write order, mtime) = −0.031 / −0.054 → stamped mtimes carry no
  creation signal. Kept fixture (seed 9001): mtimes spread 2020-01-28→2026-12-29,
  atimes 2020-02-05→2027-01-07, all distinct.
- `--keep` caveat noted: `copytree` rewrites inodes/ctimes in the kept copy, so
  the inode column was audited on a live `generate()` (same FS, xfs); mtime/
  name/readdir in the kept copy are faithful.

### 4. Same-seed v2↔v3 equivalence (seed 9006, both `generate()`)

`truth` dicts identical; all 108 source basenames identical with identical
bodies; Sources and Chain tables identical (record diff = only line 0, the H1
phrase, because v3 consumes extra rng draws for stamps). So for a fixed seed the
*measurement input* (citations, anchors, bodies, truth) is unchanged; only file
order on disk, timestamps, and the record's decorative name/H1 differ — exactly
the claimed scope.

### 5. What the counter measures — delta assessment

- Removed channel (intended): creation order = class order. Under v2 the first
  36 files written were exactly the resolvable set; metadata-control exploited
  it for 132/132 without opening a source. Under v3 it scores 91/132 (chance).
- New consumption of rng after `shuffle(sources)` shifts only the record's H1
  phrase and filename — no truth-bearing content.
- No gate-visible behaviour change: a correct gate scores 132/132 (landed
  `94a7be5a`, seed 9001, record checks ok).

## Residual risk / gaps

- File *size* is weakly class-correlated (per-class means 199–296 B, overlapping
  ranges; top-36 by size holds 7–15/36 positives — chance is 12). Pre-existing in
  v2, not an ordering channel, cannot reproduce the fixed attack. [measured]
- Record file is still written last (highest birth/ctime on a live FS); it is
  identifiable, but its path is already the gate's argv — no truth leak.
- Directory mtimes reflect generation end uniformly; no class signal.
- `metadata-control.sh:35` still comments "Generator creates R1, R2, R3 …
  before every negative" — false for v3, but it is a frozen round-32 artifact.
- atime stamping uses one extra rng draw per file; on filesystems ignoring
  atime this is moot. Single-seed `--keep` audited per the assignment (plus two
  in-process seeds); behaviour is structural, not seed-dependent, but only 3
  seeds were exercised by this seat.

## Compliance

No lane/fleet file edited; no git/jj writes; no installs (none needed — RULES.md
constraint observed, zero installs to record); `c1-count-v2.py` was never run
(kill rule not triggered); no processes signalled; all writes bounded to my
artifact dir and `/fast/scratch/hyaku/chousa-r33/w2/ReviewD1Repair/`; commands
under `timeout`; `df -h /fast` checked (180G free). Commands quoted above with
exit codes; everything not directly observed is marked or omitted.

Report: .ufo/waves/round-33/w2/ReviewD1Repair.md
