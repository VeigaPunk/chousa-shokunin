# W2SimpSep

Seat: simplifier. Axes: operability, calibration, depth. Milestone: Round 44 wave 2. Bound not retuned. `corpus/evidence/round44/c1-count.py` and `c2-count.py` were not edited. No production file was written.

## Verdict

C1 does not read `disposition.tsv`. C2 does not read `parent-lifetime.receipt`.

The path constants are disjoint. C1's only data-file reads are the launcher log and the frozen name list. C2's only data-file reads are the disposition table and the 36 untracked report paths in `UNTRACKED`. Neither source names the other file. Neither imports the other.

`claims.md` lines 72–73 state the same split. This report checks that sentence against the counters. It does not rescore it.

## Path constants

`corpus/evidence/round44/c1-count.py` lines 22–24, and the defaults that feed the reads (lines 51–52):

```
LANE = pathlib.Path(__file__).resolve().parents[3]
RECEIPT = LANE / "corpus" / "evidence" / "round44" / "parent-lifetime.receipt"
NAMES = LANE / "corpus" / "evidence" / "round44" / "seat-names.txt"
ap.add_argument("--receipt", default=str(RECEIPT))
ap.add_argument("--names", default=str(NAMES))
```

`corpus/evidence/round44/c2-count.py` lines 18–19, and the defaults that feed the reads (lines 77–78):

```
LANE = pathlib.Path(__file__).resolve().parents[3]
TABLE = LANE / "corpus" / "evidence" / "round44" / "disposition.tsv"
ap.add_argument("--table", default=str(TABLE))
ap.add_argument("--root", default=str(LANE))
```

`parents[3]` is the lane root. The file lives at `corpus/evidence/round44/<counter>.py`, so `[0]` is `round44`, `[1]` is `evidence`, `[2]` is `corpus`, `[3]` is the repo. Resolved values:

```
C1_LANE /home/vgpnk/Projects/shokunin/chousa-shokunin
C1_RECEIPT /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/parent-lifetime.receipt
C1_NAMES /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/seat-names.txt
C1_CONST_NAMES ['LANE', 'NAMES', 'RECEIPT']
C1_HAS_TABLE False
C1_DISPOSITION_IN_RECEIPT False
C1_DISPOSITION_IN_NAMES False
C2_LANE /home/vgpnk/Projects/shokunin/chousa-shokunin
C2_TABLE /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/disposition.tsv
C2_TABLE_NAME disposition.tsv
C2_CONST_NAMES ['LANE', 'MODIFIED', 'TABLE', 'UNTRACKED']
C2_HAS_RECEIPT False
C2_PARENT_IN_TABLE False
C2_TUPLE_CROSS_HITS []
C2_TUPLE_RECEIPT_SUBSTR ['corpus/evidence/round41/receipts/cells/cells.json']
C2_UNTRACKED_LEN 36
C2_MODIFIED_LEN 3
```

C1 has no `TABLE`. C2 has no `RECEIPT`. `parent-lifetime.receipt` is not a member of `UNTRACKED` or `MODIFIED`.

Source pins, `sha256sum`:

```
9883df289447fbf52005f1fa6e1ca0ced44d1aba3b122b72345a6f0bf4043a6a  corpus/evidence/round44/c1-count.py
343ba2366e8b448062dfd262d23d8f3d4801bbea5936dbc7f4d8d7e19b8b26ad  corpus/evidence/round44/c2-count.py
```

## Read sites

Imports, from an AST walk. No `importlib`, no `subprocess`, no cross-import.

```
c1-count.py: from __future__ import annotations; argparse; pathlib; sys
c2-count.py: from __future__ import annotations; argparse; hashlib; pathlib; sys
```

C1 calls that can read:

```
L54: receipt = pathlib.Path(args.receipt)
L55: names_path = pathlib.Path(args.names)
L64: receipt.read_text(encoding="utf-8", errors="replace")
L74: names_path.read_text(encoding="utf-8")
```

Those two paths are the only `read_text` sites. `parse()` splits the receipt text. It does not open another file. The missing-file branch (line 56) stats `receipt` and `names_path` only.

C2 calls that can read:

```
L67: path.read_bytes()          # sha256(), called only from the UNTRACKED loop
L80: table = pathlib.Path(args.table)
L81: root = pathlib.Path(args.root)
L89: table.read_text(encoding='utf-8')
L99: path = root / rel          # rel from UNTRACKED
L102: path.read_text(encoding='utf-8', errors='replace')
```

The `MODIFIED` loop (lines 108–113) reads class and reason strings from the table row. It does not call `read_text`, `read_bytes`, or `is_file` on those three paths. So the one `receipt` substring in C2 is not a read, and it is not the launcher log:

```
62:    'corpus/evidence/round41/receipts/cells/cells.json',
```

## Negative search

Fixed-string and cross-name scans. Exit 1 with no lines means zero matches.

```
=== rg -n -F needles ===
corpus/evidence/round44/c2-count.py:19:TABLE = LANE / "corpus" / "evidence" / "round44" / "disposition.tsv"
---
corpus/evidence/round44/c1-count.py:23:RECEIPT = LANE / "corpus" / "evidence" / "round44" / "parent-lifetime.receipt"
=== c1 disposition / tsv / table (expect none) ===
C1_CROSS_NAME_MATCHES:0 exit:1
=== c2 parent-lifetime / parent_pid / RECEIPT (expect none) ===
C2_CROSS_NAME_MATCHES:0 exit:1
=== c2 substring receipt (not the launcher log) ===
62:    'corpus/evidence/round41/receipts/cells/cells.json',
```

`disposition.tsv` occurs once in the round-44 counters, as C2's `TABLE`. `parent-lifetime.receipt` occurs once, as C1's `RECEIPT`. An AST literal scan agrees: C1's only needle literal is `'parent-lifetime.receipt'`; C2's only needle literal is `'disposition.tsv'`.

`c3-count.py` is not this pair. Its constants are `ENTRY`, `SOURCES`, and `CACHE`. Needle scan for both filenames: `C3_NEEDLES:0`. It is not a hidden reader of either file.

## Default run

Scored commands are the bare counters (`claims.md` lines 26 and 57). No `--receipt` and no `--table`.

`strace -f -e trace=openat,newfstatat,statx`, then a count of the two names:

```
=== C1 strace names ===
C1_STDOUT_EXIT:0
520:newfstatat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/parent-lifetime.receipt", {st_mode=S_IFREG|0644, st_size=8637, ...}, 0) = 0
521:newfstatat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/seat-names.txt", {st_mode=S_IFREG|0644, st_size=969, ...}, 0) = 0
522:openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/parent-lifetime.receipt", O_RDONLY|O_CLOEXEC) = 3
523:openat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/seat-names.txt", O_RDONLY|O_CLOEXEC) = 3
=== C2 strace names ===
C2_STDOUT_EXIT:1
545:newfstatat(AT_FDCWD, "/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round44/disposition.tsv", 0x7ffe73cbd810, 0) = -1 ENOENT (No such file or directory)
-- c1 --
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS
-- c2 --
CONSISTENT=0/39
REVERIFIED=0/36
LEFT_NAMED=0/3
C2=FAIL table-missing
C1_disposition.tsv 0
C1_parent-lifetime.receipt 2
C2_disposition.tsv 1
C2_parent-lifetime.receipt 0
```

C1's passing run opened the receipt and the name list. It did not stat or open `disposition.tsv`. That file is absent (`EXISTS False` at the `TABLE` path), so a C1 that needed it could not have passed.

C2's default process stat'd `disposition.tsv`, got `ENOENT`, and exited at the `table-missing` branch (lines 82–87) before `table.read_text`. It did not stat or open `parent-lifetime.receipt`.

Limit, so the trace is not over-read: because the table is missing, this C2 process did not enter the `UNTRACKED` loop. The trace therefore does not exercise `path.read_text` on the 36 reports. Those reads are still bounded by the source. `path = root / rel` and `rel` comes only from `UNTRACKED`. That tuple's cross-hits against `parent-lifetime.receipt` and `disposition.tsv` are `[]`. The three `MODIFIED` paths are not opened at all.

## Bound

`--receipt` and `--table` are ordinary path arguments. A caller can point either flag at any file. The sources do not. The frozen counting commands do not. Separability here is the counters as written: constants, defaults, and the read sites those defaults feed.

C2's `C2=FAIL table-missing` is the missing-table control named in `claims.md` line 63. It is not a separability miss. C1 passed without that table. C2 failed without reading the launcher log.

## Axes

- Operability. C1's scored command reads `RECEIPT` and `NAMES` and prints `C1=PASS` while `disposition.tsv` is absent. C2's scored command stats `TABLE` and stops. The two commands do not share a read.
- Calibration. The split is the path constants and the read sites, not a prose label. The `receipts/cells/cells.json` substring is not the launcher log and is not read. The C2 open trace did not reach the report loop; the tuple check covers that loop. An override flag can be aimed anywhere; the defaults cannot.
- Depth. No knowledge entry, registry row, or capture was touched. `c3-count.py` names neither file, so it does not couple the pair.
