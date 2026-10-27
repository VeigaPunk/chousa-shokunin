# R57W1ExecControlsReRun — R57-C2 controls + before-state re-run (scratch; lane read-only)

Seat: R57W1ExecControlsReRun (executor, leaf). Item: rebuild the three C2 control fixtures with the frozen builder
into scratch, run the frozen counter against each, confirm the expected profile + `C2=FAIL` + exit 1, and build a
NOFETCH control from the freeze commit `c2f914c` expecting the before-receipt profile `VERDICTS=0/47 C2=FAIL`.
**No frozen predicate, target, counter, control or recipe was changed** — every mutation happened in my scratch
clone; the lane was only read. Scratch `/fast/scratch/hyaku/chousa-r57/R57W1ExecControlsReRun/` (307 MB) was
deleted before this report was yielded (§6). No tool installed/upgraded. Host `pdftotext version 26.08.0` satisfies
the counter's `ENV_CHANGED` guard.

## 0. Frozen files verified unmodified
```
$ git -C <lane> diff --stat c2f914c53201a8f8ee4fef823b82681051d55592 HEAD -- \
      corpus/evidence/round57/c2-count.py corpus/evidence/round57/controls/build-c2-controls.py
(empty = frozen files untouched)
$ git -C <lane> show c2f914c:corpus/evidence/round57/c2-count.py | sha256sum
d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9  -   # == worktree sha256 of the same file
$ git -C <lane> status --porcelain -- corpus/evidence/round57/c2-count.py corpus/evidence/round57/controls/
(empty = unmodified in the working tree too)
```
## 1. Fixture build (OUTDIR outside the lane)
```
$ python3 <lane>/corpus/evidence/round57/controls/build-c2-controls.py $S/ctl
EMPTY
JUNK
ALLFAIL
$ find $S/ctl -maxdepth 4 -type d | sort    # $S/ctl/{EMPTY,JUNK,ALLFAIL}/corpus/{captures,evidence/round57,lessons}
$ for n in EMPTY JUNK ALLFAIL; do printf "%s files=%s\n" $n "$(find $S/ctl/$n -type f | wc -l)"; done
EMPTY files=0     JUNK files=95   # 47 .raw + 47 .txt + refetch.tsv     ALLFAIL files=1  # refetch.tsv only
```
## 2. Controls against the frozen counter — every summary line
Method A (`--root` into the fixture, counter read from the lane):
```
$ python3 <lane>/corpus/evidence/round57/c2-count.py --root $S/ctl/EMPTY
SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL   exit=1
$ python3 <lane>/corpus/evidence/round57/c2-count.py --root $S/ctl/JUNK
SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 UNREACHABLE=0 BYTE_BACKED=47 CONSISTENT=47/47 FLAGGED=0/47 C2=FAIL   exit=1
$ python3 <lane>/corpus/evidence/round57/c2-count.py --root $S/ctl/ALLFAIL
SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=47 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL   exit=1
```
Method B (fixture overlaid into a scratch `git clone --shared` of the lane, counter run from the clone) — identical:
`captures=0 refetch=no → SET=47 VERDICTS=0/47 … C2=FAIL exit=1` (EMPTY) · `captures=94 refetch=yes →
SET=47 VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 … C2=FAIL exit=1` (JUNK) · `captures=0 refetch=yes →
SET=47 VERDICTS=47/47 REPRODUCED=0 UNREACHABLE=47 … C2=FAIL exit=1` (ALLFAIL).

Byte-for-byte match with the committed receipt `corpus/evidence/round57/controls/c2-controls.txt` (all three `SET=…`
lines identical to mine, each `exit=1`), and with the profiles the frozen claim states (EMPTY 0/47 · JUNK
REPRODUCED=0 DRIFTED=47 · ALLFAIL UNREACHABLE=47). **No control meets the target.** Rebuilding into a second OUTDIR
with new random bytes reproduced all three profiles exactly — JUNK's `.raw` digests differ build-to-build
(`001287c4…` sha `1b8cae17…` vs `eea04850…`), the profile does not.

## 3. NOFETCH control — the before state
```
$ git -C $S/lane checkout c2f914c53201a8f8ee4fef823b82681051d55592
HEAD=c2f914c53201a8f8ee4fef823b82681051d55592   toplevel=$S/lane
captures=0 refetch=no lesson=no
$ python3 $S/lane/corpus/evidence/round57/c2-count.py
SET=47 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 BYTE_BACKED=0 CONSISTENT=0/0 FLAGGED=0/0 C2=FAIL   exit=1
$ … --verbose   → 47× "CAPTURE S### <key> pin=… MISSING", 48 lines total, last line the SET=… summary
```
Identical to the committed `controls/c2-before.txt` (`SET=47 VERDICTS=0/47 … C2=FAIL`, `exit=1`). Independently, the
same profile was reproduced at the round base `6656f0770a1460d6ba73d9d2976f698a35311921` with the frozen counter
copied in over an otherwise-base tree.

## 4. Non-vacuity — the counter's PASS path is reachable (FAIL is not structural)
A 40-triple synthetic lane was built in scratch (5 REPRODUCED / 30 DRIFTED with `FRESHNESS-FLAG` lines / 5
UNREACHABLE) and run through a **copy** of the counter with only `SET_REV` and `SET_N` repointed — `MIN_REPRODUCED = 5`,
`MIN_BYTE_BACKED = 32`, the recipe and the flag rule untouched:
```
SET=40 VERDICTS=40/40 REPRODUCED=5 DRIFTED=30 UNREACHABLE=5 BYTE_BACKED=35 CONSISTENT=35/35 FLAGGED=30/30 C2=PASS   exit=0
```
Each floor bites on its own: the 5 reproduced raws replaced with junk → `REPRODUCED=0 … C2=FAIL` (exit 1); 4 drifted
captures dropped (35→31 byte-backed) → `BYTE_BACKED=31 … C2=FAIL` (exit 1); the `FRESHNESS-FLAG` lines deleted →
`FLAGGED=0/30 … C2=FAIL` (exit 1). Tampering one `.txt` inside the JUNK fixture → `CONSISTENT=46/47 … C2=FAIL`
(exit 1), i.e. the recipe-consistency check bites. **The counter can print PASS; the controls fail for their stated
reasons, not because the counter is stuck.**

## 5. Live lane state during the wave (read-only) and one workflow hazard found
The L1 landed the C2 after-receipt mid-wave (`e0e73e0`). Final live snapshot, counter run read-only against the lane:
```
$ python3 <lane>/corpus/evidence/round57/c2-count.py --root <lane>
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS   exit=0
```
Matching the commit message. The 5 DRIFTED are S083 S087 S113 S114 S121, all `absent=0` → `need_flag=0` →
`FLAGGED=0/0`; `corpus/lessons/round-57.md` does not exist in the lane and none is required while every DRIFTED
quote is still present.

**Hazard (workflow, not a claim defect — the counter is right, the data state was wrong):** at `a03824d` S105 was
permanently `MISSING` even though the lane held its bytes. `corpus/captures/e3ca8f4fdd15420b80096a75.raw`
(4 482 989 B, sha256 `d36191c72a5e007e0354b5160d207cffa9e59be86536c997a7dcff9db8ebcb6`) was committed by the
record-less wrap-up `b022b13`; no `refetch.tsv` row ever named those bytes, so the counter's
`ok[-1]["raw_sha256"] != sha(raw)` branch fired (`MISSING capture not the last successful attempt's bytes`).
Because the frozen predicate defines UNREACHABLE as *"no capture, and at least two failed attempts"*, that orphan
file made S105 unable to take any verdict. Proof, in the scratch clone at `a03824d`:
```
orphan .raw PRESENT + two failed rows 700 s apart → CAPTURE S105 … MISSING     (VERDICTS=43/47)
orphan .raw REMOVED + the same two rows           → CAPTURE S105 … UNREACHABLE (VERDICTS=44/47)
```
The L1 resolved it in `e0e73e0` by deleting the orphan bytes and adding attempt-2/3 rows (08:06:12Z, 08:30:12Z,
08:33:48Z; first→last spread 1656 s ≥ 600 s) — after which S105 reads UNREACHABLE and C2=PASS. Lesson for the lane's
tooling: **`capture-fetch.py` must remove a stale capture when a URL ends up unreachable**, or the triple strands as
MISSING forever. I did not change the tool or the predicate; this is reported for the L1 only.

## 6. Boundary checks (probes only; no lane state touched) and boundaries honoured
UNREACHABLE spacing is `>= 600 s` exactly: two failed rows 599 s apart → `MISSING`; 600 s → `UNREACHABLE`; 601 s →
`UNREACHABLE`. And a capture present on disk whose bytes match no successful row can never be UNREACHABLE (§5) —
the frozen predicate's "no capture" clause, confirmed by probe rather than by reading.
Only write: this report file. The lane repo was read only — `git status` there shows only the L1's own in-flight
changes plus this file; the frozen counter, builder and control receipts are untouched (§0). No fleet-root write
(`LOG.md`/`SCORECARD.md`/`MANIFEST.json` untouched), no sibling lane, no `shokuknow`. No network fetch by this seat
(`curl`/`wget` never invoked); all bytes read came from committed lane files. No `git commit/add/stash/checkout/reset/
push` outside my scratch clone — the checkouts and the synthetic-lane commit were inside `$S/lane` and `$S/vac/lane`
only, with `git rev-parse --show-toplevel` asserted to be the scratch dir before each. **Cleanup:** `$S` (307 MB)
removed with `rm -rf` before yield; nothing remains outside it.

VERDICT: the R57-C2 controls and before-state re-run **survived** — all three fixtures rebuilt and reproduced their
committed profiles exactly (EMPTY 0/47, JUNK REPRODUCED=0/DRIFTED=47, ALLFAIL UNREACHABLE=47, each `C2=FAIL` exit 1),
the NOFETCH clone at `c2f914c` reproduced the before receipt (`VERDICTS=0/47 C2=FAIL`), the counter's PASS path was
shown reachable so the failures are non-vacuous — with one workflow hazard reported (an orphan capture blocks the
UNREACHABLE verdict; the L1 already cleared it in `e0e73e0`, where the live counter prints `C2=PASS`).
