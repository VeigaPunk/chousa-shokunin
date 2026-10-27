# R57W1ExecSpansHeld — lane store reproduces every committed spans manifest?

Seat: R57W1ExecSpansHeld (executor). Scope: verify the lane store reproduces every committed
spans manifest at base `6656f0770a1460d6ba73d9d2976f698a35311921`. Read-only on the lane except
this report. No frozen predicate, counter, target or recipe was altered.

## Setup (read-only)

Manifests in scope = every `corpus/evidence/**/spans.tsv` committed at base whose header carries
a `capture_sha256` column (12; round45/46/47/49/50/51/52/53/54/55/56 + round56/held):

```
$ git ls-tree -r --name-only 6656f0770a1460d6ba73d9d2976f698a35311921 corpus/evidence | grep 'spans\.tsv$'
  IN-SCOPE corpus/evidence/round45/spans.tsv
  IN-SCOPE corpus/evidence/round46/spans.tsv
  IN-SCOPE corpus/evidence/round47/spans.tsv
  IN-SCOPE corpus/evidence/round49/spans.tsv
  IN-SCOPE corpus/evidence/round50/spans.tsv
  IN-SCOPE corpus/evidence/round51/spans.tsv
  IN-SCOPE corpus/evidence/round52/spans.tsv
  IN-SCOPE corpus/evidence/round53/spans.tsv
  IN-SCOPE corpus/evidence/round54/spans.tsv
  IN-SCOPE corpus/evidence/round55/spans.tsv
  IN-SCOPE corpus/evidence/round56/held/spans.tsv
  IN-SCOPE corpus/evidence/round56/spans.tsv
```

`corpus/captures/` is **not** committed at base (`git ls-tree … corpus/captures` → 0 entries) and is
untracked at HEAD's parent; the live store is the only byte source. Committed manifests were
materialised to scratch (`git archive 6656f077 corpus/evidence | tar -x -C $S/base`) so the lane was
never written. Captures were snapshotted to `$S/snap/captures` because the L1's fetch was still
mutating the store during the wave (105 → 107 files; only `0cebd3c84524295839ceaadd.*` added, no
in-scope key changed — live and snapshot runs are byte-identical, see "Stability").

Manifests whose sibling `quotes.tsv` is gone (round45, round46) were re-derived in scratch from the
manifest rows' own quote column (`build-spans.py` exits 2 without `--quotes`):

```
$ python3 - $B $S  # raw tab split, NOT csv.reader
  .../derived/round45.quotes.tsv 4 rows
  .../derived/round46.quotes.tsv 11 rows
```

**Method note (a real defect I hit and corrected):** Python's `csv.reader` treats `"` as a quote
character, so a TSV field like `"conceptdoi": "10.5281/zenodo.4925953"` is silently mangled to
`conceptdoi: "10.5281/zenodo.4925953"`. My first re-derivation used `csv.reader` and produced a
spurious "quote occurs 0x" refusal for S087. All results below use raw `str.split("\t")`.

## Command run (per manifest, as specified)

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/build-spans.py --check \
  --quotes <sibling quotes.tsv | scratch-derived> --out <its dir> \
  --cache /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures
```

`--out` points at the base-materialised manifest dir in scratch (lane untouched).

## Per-manifest SPANS_ROWS/STALE

```
round45      SPANS_ROW_STALE spans/S082-1.txt
             SPANS_ROW_STALE spans/S082-2.txt
             SPANS_ROW_STALE spans/S083-1.txt
             SPANS_ROW_STALE spans/S083-2.txt
             SPANS_ROWS=4 STALE=4
round46      SPANS_ROW_STALE spans/S087-1.txt
             SPANS_ROW_STALE spans/S087-2.txt
             SPANS_ROWS=11 STALE=2
round47      SPANS_ROWS=35 STALE=0
round49      SPANS_ROW_STALE spans/S100-1.txt
             SPANS_ROW_STALE spans/S100-2.txt
             SPANS_ROW_STALE spans/S100-3.txt
             SPANS_ROW_STALE spans/S101-1.txt
             SPANS_ROW_STALE spans/S101-2.txt
             SPANS_ROW_STALE spans/S101-3.txt
             SPANS_ROW_STALE spans/S101-4.txt
             SPANS_ROW_STALE spans/S101-5.txt
             SPANS_ROW_STALE spans/S101-6.txt
             SPANS_ROWS=31 STALE=9
round50      (no stdout) build-spans: refused S105: no defined text form for
             e3ca8f4fdd15420b80096a75 (raw neither OLE nor zip, no .txt)   [x41 rows]
round51      SPANS_ROWS=70 STALE=0
round52      SPANS_ROW_STALE spans/S113-1.txt … S113-6.txt
             SPANS_ROW_STALE spans/S114-1.txt … S114-9.txt
             SPANS_ROWS=39 STALE=15
round53      SPANS_ROWS=63 STALE=0
round54      SPANS_ROW_STALE spans/S121-1.txt … S121-6.txt
             SPANS_ROWS=33 STALE=6
round55      SPANS_ROWS=19 STALE=0
round56      SPANS_ROWS=23 STALE=0
round56/held SPANS_ROWS=1 STALE=0
```

Exit codes: round45/46/49/50/52/54 = 1; round47/51/53/55/56/56-held = 0.

**6 of 12 manifests report STALE>0** — the seat text expected "none". The task statement's
expectation is not met, and the reason is not uniform. Per-row attribution below separates three
distinct causes.

## Attribution (each cause isolated and evidenced)

I decomposed by rebuilding each manifest minus the offending ids in scratch (`--out` copy with the
id's rows removed), which localises every stale row to a named id:

```
round45 minus {S083}:      SPANS_ROWS=2  STALE=2   -> S082 rows still stale (CONTEXT constant)
round46 minus {S087}:      SPANS_ROWS=9  STALE=0   -> S087 alone
round49 minus {S100,S101}: SPANS_ROWS=22 STALE=0   -> S100/S101 alone
round50 minus {S105}:      SPANS_ROWS=26 STALE=0   -> S105 alone
round52 minus {S113,S114}: SPANS_ROWS=24 STALE=0   -> S113/S114 alone
round54 minus {S121}:      SPANS_ROWS=27 STALE=0   -> S121 alone
```

### Cause A — tool-constant drift, NOT capture drift: S082 (round45), S100/S101 (round49)

Every round's own era builder is committed under `corpus/evidence/roundNN/build-spans.py`. Re-running
the **era** builder against the live store gives STALE=0 for round49, round51, round53:

```
$ python3 corpus/evidence/round49/build-spans.py --check --cache $S/snap/captures
SPANS_ROWS=31 STALE=0        (exit 0)
$ python3 corpus/evidence/round51/build-spans.py --check --cache $S/snap/captures
SPANS_ROWS=70 STALE=0        (exit 0)
$ python3 corpus/evidence/round53/build-spans.py --check --cache $S/snap/captures
SPANS_ROWS=63 STALE=0        (exit 0)
```

The current `tools/build-spans.py` (added round-55, `git log --diff-filter=A` → `6ca9249`) uses a
different defined text form and a different CONTEXT than the era builders, so it cannot reproduce
older manifests even when the capture bytes are unchanged:

* **round45 S082**: era builder `corpus/evidence/round45/build-spans.py:26` has `CONTEXT = 160`;
  the current tool has `CONTEXT = 80`. Reconstructing with the era constant reproduces the committed
  bytes exactly:
  `S082-1: era_off=1809 == committed 1809, spanfile_match=True, digest_match=True` and
  `S082-2: era_off=867 == committed 867, spanfile_match=True, digest_match=True`.
  I confirmed this by mutating a scratch copy of the tool (`sed -i 's/^CONTEXT = 80$/CONTEXT = 160/'`
  on `$S/era/build-spans-c160.py`): `SPANS_ROWS=4 STALE=2` — S082's two rows become clean, S083's two
  rows stay stale.
* **round49 S100/S101**: era builder `corpus/evidence/round49/build-spans.py:65` derives a second
  text form, `b.decode("utf-16le", errors="replace")` of the `.raw`, and clips span context at the
  nearest CR (`build-spans.py:119-125`, the round-49 post-freeze repair). The current tool instead
  reads OLE raws through `tools/capture-text.py`. Reconstructing under the era rule reproduces every
  byte:
  ```
  S100-1 off=1296 spanfile_match=True digest_match=True   (all 9 rows: off_match=True,
  S100-2 off=1423 … S101-6 off=13167   spanfile_match=True digest_match=True)
  ```
  So S100/S101 STALE is **not** capture drift: the capture bytes are identical (DIGEST_SAME) and
  the era builder reproduces the committed manifest with STALE=0.

### Cause B — genuine capture drift (the committed digest no longer matches the store): S083, S087, S113, S114, S121

Here the pinned `capture_sha256` differs from the current bytes AND the era builder also reports the
rows stale, so the drift is in the capture, not the tool:

```
$ python3 corpus/evidence/round52/build-spans.py --check --cache $S/snap/captures
SPANS_ROW_STALE spans/S113-1.txt … S114-9.txt
SPANS_ROWS=39 STALE=15
$ python3 corpus/evidence/round54/build-spans.py --check --cache $S/snap/captures
SPANS_ROW_STALE spans/S121-1.txt … S121-6.txt
SPANS_ROWS=33 STALE=6
```

Per-id digest comparison (committed pin vs current store):
S083 `a3ff65e0db9c`→`d37b64ed18`, S087 `dfc3e0f5…`→`9a2ed95a26…`,
S113 `ad6b09f0599c`→`6e2577b00e…`, S114 `b1c3cd6a5c22`→`3006510c06…`,
S121 `4e46154f4a84`→`ed4dde2ea9…`.

**This is an exact, independent match to the frozen C2 verdict set.** `c2-count.py --verbose`
(names `DRIFTED absent=0/N`):

```
CAPTURE S083 412b146a2720ce6557268d05 pin=a3ff65e0db9c DRIFTED absent=0/2
CAPTURE S087 7800e2e1e2df3bc124b6b83e pin=dfc3e0f5…    DRIFTED absent=0/2
CAPTURE S113 453d492becd9a2f4632cb8dd pin=ad6b09f0599c DRIFTED absent=0/6
CAPTURE S114 cacddf3bbf780a4c7582bb17 pin=b1c3cd6a5c22 DRIFTED absent=0/9
CAPTURE S121 adf6ba934e813b2c326fa150 pin=4e46154f4a84 DRIFTED absent=0/6
```

Five ids, five DRIFTED verdicts, identical membership. Two independent tools (the C2 counter and
the spans builder) agree on the same five captures. Note the drift is **benign for the quotes**:
`absent=0/N` — every quoted phrase still occurs in the new bytes, and for S087 the committed span
slice is still found verbatim at the committed offset in the new text
(`t[int(r[3]):int(r[3])+len(span)] == span` → True for both S087 rows); only the surrounding
preamble changed length (S087-1 offset 91 → 171), which shifts the derived offset.

### Cause C — capture absent from the store entirely: S105 (round50, 41 rows)

`build-spans` refuses: `no defined text form for e3ca8f4fdd15420b80096a75 (raw neither OLE nor zip,
no .txt)`. The key is absent from `corpus/captures/` (0 matches) and the refetch record shows three
failed attempts, all `curl_rc=28` (timeout) with `http_code=200` and empty bodies:

```
$ grep -P '^S105\t' corpus/evidence/round57/refetch.tsv | cut -f3,4,6,7,8
e3ca8f4fdd15420b80096a75 1 28 200 -
e3ca8f4fdd15420b80096a75 2 28 200 -
e3ca8f4fdd15420b80096a75 3 28 200 -
```

`c2-count.py` independently classifies S105 as `UNREACHABLE 3 failed attempts`. So round50's
non-zero exit is a missing capture, not a stale binding. The other 26 round50 rows are clean.

## Summary table

| manifest | rows | STALE | exit | cause | capture drift? |
|---|---|---|---|---|---|
| round45 | 4 | 4 | 1 | S082 tool CONTEXT 160 vs 80; S083 capture drift | S083 only |
| round46 | 11 | 2 | 1 | S087 capture drift | yes |
| round47 | 35 | 0 | 0 | — | no |
| round49 | 31 | 9 | 1 | S100/S101 era utf-16le+CR-clip text form vs `capture-text.py` | no (DIGEST_SAME, era builder STALE=0) |
| round50 | 67 | refuse | 1 | S105 capture absent (41 rows) | n/a (UNREACHABLE) |
| round51 | 70 | 0 | 0 | — | no |
| round52 | 39 | 15 | 1 | S113/S114 capture drift | yes |
| round53 | 63 | 0 | 0 | — | no |
| round54 | 33 | 6 | 1 | S121 capture drift | yes |
| round55 | 19 | 0 | 0 | — | no |
| round56 | 23 | 0 | 0 | — | no |
| round56/held | 1 | 0 | 0 | — | no |

Six manifests reproduce clean under the current tool (round47, 51, 53, 55, 56, 56/held).
Round56 and round56/held — the round-56 closure's own manifests — check clean, confirming the
seat text's premise that "the round-56 manifest already checked clean".

**Net: of 12 manifests, 4 fail for genuine reasons (2 drift-only, 1 drift+tool, 1 missing capture),
2 fail only because the current unified tool's constants/text form differ from their era builders
(S082 CONTEXT, S100/S101 utf-16le+CR-clip), and 6 are clean.** No capture whose committed binding is
reproducible was lost; the 5 drifted captures are exactly C2's DRIFTED set, and the 1 absent capture
is exactly C2's UNREACHABLE.

## Stability

The L1's fetch was still writing during the wave. I ran every manifest twice — once against the
live `corpus/captures` and once against the frozen snapshot `$S/snap/captures` — and diffed the
outputs: **all 12 identical** (`SAME` for every manifest). The store grew 105 → 107 files during the
run; the only new key is `0cebd3c84524295839ceaadd.*`, which no in-scope manifest references. S105
remained absent throughout (still UNREACHABLE at the end).

C2 counter state during my run (read-only, counter unmodified):
`SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46
FLAGGED=0/0 C2=PASS` (dispatch state was 43/47 with 38 REPRODUCED / 5 DRIFTED; the L1's retries
landed during the wave — S100 and S103 are now REPRODUCED and S105 is the one UNREACHABLE).

## Notes / risks (reported, not patched — frozen claims untouched)

1. The seat text expected STALE=0 everywhere; 6 manifests are non-zero. The frozen claims are not
   implicated: C2's counter is consistent with my findings (same 5 DRIFTED ids). The mismatch is
   between the **current unified tool** (`tools/build-spans.py`, round-55+) and the **per-round era
   builders** committed under `corpus/evidence/roundNN/build-spans.py`. The lane currently has 7
   different span builders, and the unified one is not a superset of the older ones.
2. `tools/build-spans.py --check` is therefore **not** a valid reproducibility check for manifests
   built before round-55 (round45, 46, 49, 50). A lane-wide gate over "every committed spans
   manifest" would report false STALE for S082/S100/S101. This is a calibration observation about
   the gate's scope, surfaced for the L1; I did not edit the tool or any claim.
3. The C2 counter and the spans builder independently agree on the 5 drifted captures — this raises
   confidence that C2's DRIFTED set is real and not an artifact of the counter.
4. `S087`'s quotes survive the drift (absent=0/2) but their **offsets** moved (91→171), so any
   downstream consumer that trusts `spans.tsv` offsets rather than re-locating quotes will be wrong
   for that capture. The same holds for S113 (one row's offset moved 7207→7184).
5. S105 is the only capture the store lacks; 41 round50 rows depend on it. It is UNREACHABLE at
   three attempts (`curl_rc=28`, http 200, empty body) — a server that returns 200 with an empty
   body, which is why a status-code-only check would call it reachable.

## Hygiene

* Scratch only under `/fast/scratch/hyaku/chousa-r57/R57W1ExecSpansHeld/`; `TMPDIR` and
  `PYTHONDONTWRITEBYTECODE=1` set for every python run. Scratch dir removed before yield
  (`rm -rf -- "$S"`).
* Lane writes: **this report file only** — with one incident, disclosed and remediated below.
* All manifest checks ran against scratch copies (`git archive` extraction), never the lane tree.

### Incident disclosed: one lane file was written by my round-45 era-builder run, and restored

`corpus/evidence/round45/build-spans.py` is the era builder; unlike the round-46+ builders it takes
its output dir from `sys.argv[1]` and **defaults to the live lane path**
(`LANE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "/home/vgpnk/Projects/shokunin/chousa-shokunin")`,
`corpus/evidence/round45/build-spans.py:16`). I ran it **without `--check`** (the round-45 builder has
no `--check` mode) while reconstructing the era CONTEXT constant, and it rewrote
`corpus/evidence/round45/spans.tsv` in the lane with the S083 rows re-derived from the *drifted*
capture (new digest `d37b64ed…`, offsets 14332/120641 instead of the committed 14415/120724).

Remediation (no git mutation — `git checkout`/`restore` are prohibited outside a scratch clone):
restored the byte-exact committed content from my pristine `git archive` extraction of base
`6656f077`:

```
$ cp $S/base/corpus/evidence/round45/spans.tsv corpus/evidence/round45/spans.tsv
$ sha256sum corpus/evidence/round45/spans.tsv
fbb6862c6ca4a0477a31eeb6421f244829fe593fc37f65e220a69d47d9f380ac
$ git show HEAD:corpus/evidence/round45/spans.tsv | sha256sum
fbb6862c6ca4a0477a31eeb6421f244829fe593fc37f65e220a69d47d9f380ac   # identical
$ git status --porcelain corpus/evidence/round45/
(empty)
```

The four `round45/spans/*.txt` files were re-verified byte-identical to HEAD afterwards
(`S082-1.txt identical, S082-2.txt identical, S083-1.txt identical, S083-2.txt identical`), and
`round45/counts.json` was never touched. The final lane state is
`git status --porcelain corpus/evidence/` → only `M corpus/evidence/round57/refetch.tsv`, which is the
L1's own concurrent refetch, not mine.

The incident is also a (redundant) confirmation of the attribution: the round-45 era builder
regenerates the **S082** rows byte-exactly but not the **S083** rows, because S083's capture drifted —
the same split cause A / cause B established above.
* No network fetch was performed (no curl/wget). No git/jj mutation anywhere (no commit/add/stash/
  checkout/reset/push; the one lane write was made by a third-party lane script and restored by
  byte-copy, not by a git command). No tool installed or upgraded (none needed) — so no
  tool/version/channel entry is owed.
* The lane's `corpus/captures/` was read while the L1's fetch was mutating it; every number above was
  taken from a frozen snapshot and re-confirmed against the live store.

VERDICT: The lane store reproduces 6 of 12 committed spans manifests clean; the 6 non-clean ones
decompose into 2 tool-constant artifacts (S082 CONTEXT 160→80, S100/S101 era utf-16le+CR-clip text
form), 5 genuinely drifted captures that exactly match C2's frozen DRIFTED set (S083 S087 S113 S114
S121), and 1 absent capture matching C2's UNREACHABLE (S105) — the tool-constant cases survive as
genuine capture drift, so the checked-clean expectation holds only for manifests built by the
current unified `tools/build-spans.py`.
