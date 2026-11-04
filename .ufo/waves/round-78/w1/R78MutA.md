# R78MutA — closure-removal twins on the round-78 battery (measured, not asserted)

Seat: R78MutA (mutation tester, leaf). Round 78, wave 1.
Frozen predicate set: `corpus/evidence/round78/claims.md` (read first; C1/C2 unchanged by this seat).
Frozen instrument under mutation: `corpus/evidence/round78/matrix-battery-v5.py`,
sha256 `5545a4718690a80e5d3d6611e43132fdd5cb4dcd67e87be9a27ed44c032b5af0` — matches the
claims.md digest table, re-hashed on this host before and after every run (see §Restoration).
Detector: `corpus/evidence/round78/forge-battery.py`,
sha256 `ba98db41e0c82ba0ff3b7cb4259764fcfb85c54b17137da02655ee751f1c5143` — unchanged.

No frozen instrument was edited. Every twin is a scratch copy; the lane tree was read only.

## 1. Method

Scratch: `/fast/scratch/hyaku/chousa-r78/R78MutA` (deleted before yield, §Restoration).

A twin must (a) keep the frozen file **name** `matrix-battery-v5.py`, because the a2/a7
forgers locate the battery through `/proc/<ppid>/cmdline` with the matcher
`matrix-battery-v\d+\.py$` — renaming the twin would close that channel by accident and
silently turn two REFUSED verdicts into REFUSED-for-the-wrong-reason; and (b) keep
`LANE = HERE.parents[2]` resolving to a tree that has `corpus/evidence/round7{4,5,6}` and
`round78/forgers/`. Both are satisfied by a mirror:

```
/fast/scratch/hyaku/chousa-r78/R78MutA/mirror/<twin>/corpus/evidence/round78/matrix-battery-v5.py
                                                  .../round78/forgers      -> symlink, lane (read only)
                                                  .../round74,round75,round76 -> symlink, lane (read only)
```

Generator: `R78MutA/gen.py` (copied verbatim into this folder). Each mutation is an exact
anchor replacement (`assert text.count(old) == 1`), so a twin differs from the frozen bytes
only in the named leg; diffs are in `R78MutA/mutants/<twin>.diff`.

Detector invocation, identical for every row (forge-battery defaults: `--runs 1`,
`SETTLE=26`, `--matrix-timeout 300`; no per-twin tuning):

```
python3 -B corpus/evidence/round78/forge-battery.py \
    --battery /fast/scratch/hyaku/chousa-r78/R78MutA/mirror/<twin>/corpus/evidence/round78/matrix-battery-v5.py \
    --work /fast/scratch/hyaku/chousa-r78/R78MutA/fb/<twin>.w
```

**Twins are working batteries, not broken ones.** Before scoring, each twin was run on the
lane's legitimate matrix:

```
python3 -B mirror/<twin>/corpus/evidence/round78/matrix-battery-v5.py \
    --matrix corpus/evidence/round76/loader-matrix-v3.py --work smoke/<twin> --runs 1
```

→ exit 0 and `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED` for all six
twins (`R78MutA/receipts/smoke-*.out`). So any flip below is attributable to the removed leg,
not to a twin that refuses everything.

**Baseline on this host, same invocation** (`receipts/PRISTINE.txt`, exit 0):
`FORGE_BATTERY=PASS forgers_handled=4/4 positive=1/1`, with a1/a2/a7 `REFUSED` (rc=1,
receipt_lines=113, trailer ok), a5d `DETECTED` (receipt_lines=139, integrity BAD) and the
positive `ACCEPTED` — byte-for-byte the same verdict shape as the committed
`corpus/evidence/round78/controls/forge-battery-after-v5.txt`.

## 2. Table (see `R78MutA/table.md` for the rendered form)

| twin | mutation | diff lines | sha256 | forge exit | a1 | a2 | a7 | a5d | pos | handled | flips |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PRISTINE | — | 0 | `5545a471…` | 0 | REFUSED | REFUSED | REFUSED | DETECTED | ACC | 4/4 | — |
| M1 | `--print-order` forced on, quiet leg intact | 1 | `e335d708…` | 0 | REFUSED | REFUSED | REFUSED | DETECTED | ACC | 4/4 | **none** |
| M1B | M1 + ORDER line emitted when produced (flushed) | 5 | `f0844665…` | 0 | REFUSED | REFUSED | REFUSED | DETECTED | ACC | 4/4 | **none** |
| **M2** | interior inert statement → round-77 trailing `# salt <hex>` | 3 | `a34b4de0…` | 1 | **FORGED** | **FORGED** | REFUSED | DETECTED | ACC | **2/4** | a1, a2 |
| **M3** | `RECEIPT_LINES` trailer removed | 1 | `842a8210…` | 1 | REFUSED | REFUSED | REFUSED | **FORGED** | ACC | **3/4** | a5d |
| M4 | per-subject RUN lines emitted when produced (flushed) | 4 | `0f6b1600…` | 0 | REFUSED | REFUSED | REFUSED | DETECTED | ACC | 4/4 | **none** |
| **M5** | M1 + ORDER **and** RUN lines emitted when produced | 7 | `33f55b23…` | 1 | REFUSED | REFUSED | **FORGED** | DETECTED | ACC | **3/4** | a7 |

Positive control `ACCEPTED` in all seven rows: no blanket-refusal artefact anywhere.
`forgers_handled` drops below 4/4 in M2 (2/4), M3 (3/4), M5 (3/4).

### M1 — `--print-order` forced on (the ORDER digest returns)

Mutation (`mutants/M1.diff`), one line in `main()`: `a.print_order = True` after
`ap.parse_args()`. Both `score()` call sites already take `a.print_order`, so the twin prints
`MATRIX ORDER <i> <sha256>` for the matrix and for each of the three oracles (receipt 113 →
117 lines) — but through the **buffered** list, i.e. after the whole scoring loop.
**Verdict: flips nothing; 4/4 PASS.** The a7 log records `no ORDER line readable` on all 13
invocations (`logs/M1-forger-calls.log`). A printed order line that appears after the child
has been judged is not an answer key.

### M1B — ORDER line at round-77 *timing*, quiet leg otherwise intact

Mutation: M1 plus `print(text, flush=True)` in `emit` and the ORDER line moved from
`buffered.append(...)` to `emit(...)` (`mutants/M1B.diff`). This is the minimal twin in which
the digest is genuinely readable while the child runs.
**Verdict: still flips nothing; 4/4 PASS** — but for a different, measurable reason: the a7
log shows the digest *was* read and the permutation *was* recovered (`perm digest=3a472f6c1df4
secs=8.4`), yet every one of its 26 invocations computed `position=0 subject=constant-fail
positive=False`. a7 derives its position from the count of `MATRIX RUN …` lines already on the
receipt; the QUIET leg buffers those, so `seen` is always 0 and the recovered permutation buys
nothing. The order digest is **necessary but not sufficient**.

### M2 — interior salt replaced by the round-77 trailing `# salt` line

Mutation (`mutants/M2.diff`): `salted_copy`'s interior-statement insertion replaced by
round-77 v4's exact `target.write_bytes(source.read_bytes() + f"\n# salt {hex}\n")`.
**Verdict: a1 and a2 both FORGED; handled 2/4, exit 1.**
Evidence: a1's battery run exits 0 and its receipt ends
`RECEIPT_LINES=113` / `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`
(`forger-receipts/M2--a1-trailing-salt-strip.receipt`); a2's log shows
`ppid_cmdline_battery=…/mirror/M2/…/matrix-battery-v5.py contract_lines=12
subject_sha=909987ce… positive=True` and `…9334721a… positive=True`
(`logs/M2-forger-calls.log`). Both forgers strip the same marker before hashing, so **one
leg carries two forgers**: the identity leg is the load-bearing leg for a1 *and* a2. This
reproduces round 77's `rcpt-a1`/`rcpt-a2` class exactly.

### M3 — `RECEIPT_LINES` trailer removed

Mutation (`mutants/M3.diff`): the single `emit(f"RECEIPT_LINES={_LINES + 2}")` line deleted
(receipt 113 → 112 lines).
**Verdict: a5d FORGED; handled 3/4, exit 1.** a5d's receipt (138 lines, trailer absent)
ends with the appended `BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED`
and `read_receipt` returns `integrity=None` → `FORGED`, i.e. round 77's `rcpt-a5d` class
restored by one deleted line. Note the side effect: with no trailer, *every* row reads
`integrity=n/a`, including the positive control, which is still `ACCEPTED` (acceptance does
not require the trailer) — the trailer's whole cost falls on the appending child.

### M4 — per-subject lines printed immediately instead of buffered

Mutation (`mutants/M4.diff`): the `MATRIX RUN …` line moved from `buffered.append(...)` to
`emit(...)` and `emit` flushes (`print(text, flush=True)`), so the position channel is real;
the ORDER leg is untouched (still off).
**Verdict: flips nothing; 4/4 PASS** (113 lines, same as pristine). a7 logs `no ORDER line
readable` 13× — a visible RUN count with no permutation to index it is not an answer key.
`--print-order` is not passed by forge-battery, so M4 alone leaves a7 exactly as closed as
pristine.

### M5 — ORDER and RUN both at round-77 timing (the full round-77 print regime)

Mutation (`mutants/M5.diff`): M1 + flushed ORDER line + flushed RUN line = v4's printing.
**Verdict: a7 FORGED; handled 3/4, exit 1.** a7's log shows the permutation recovered
(`perm digest=dda8e18c00c7 secs=8.9`, well inside the battery's own 285 s enumerator cap)
and positions 0…12 recovered in order (`position=0 subject=constant-fail` … ), with exactly
2 `positive=True` of 26 calls — both positives classified. Its battery run exits 0 and the
receipt ends `RECEIPT_LINES=117` / `BATTERY=PASS forgers_rejected=11/11 positive=2/2
oracle=REJECTED` (`forger-receipts/M5--a7-printed-order-digest.receipt`). Round 77's
`rcpt-a7` class returns the moment both halves of the print regime return.

**Load-bearing attribution for a7:** the leg is a *pair*. ORDER-line presence (M1, M1B) and
immediate RUN printing (M4) each flip nothing on their own; together (M5) they flip a7. So
the closure is "no invertible answer key **and** no per-subject line while subjects run" —
removing either half alone is not a regression, and a future twin that removes only one of
them must be reported as a no-flip, not as a pass for the leg.

## 3. Frozen v5 closure-removal flags (direct, not through forge-battery)

```
python3 -B corpus/evidence/round78/matrix-battery-v5.py \
    --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR --no-permute
# exit 1
BATTERY=FAIL forgers_rejected=11/11 positive=2/2 oracle=MISS

python3 -B corpus/evidence/round78/matrix-battery-v5.py \
    --matrix corpus/evidence/round76/loader-matrix-v3.py --work DIR --no-content
# exit 0
BATTERY=PASS forgers_rejected=11/11 positive=2/2 oracle=REJECTED
```

Receipts: `R78MutA/receipts/flags-no-permute.txt`, `flags-no-content.txt`,
`flags-no-content-2.txt`, `flags-no-content-3.txt` (three repeats, exit 0 and the identical
predicate line each time).

- `--no-permute` is **red as documented**: `ORACLE block-position MISS positive=2/2
  forgers_rejected=11/11` → `oracle=MISS` → `BATTERY=FAIL`. The permutation leg is
  load-bearing exactly as QUALITY 141 states.
- `--no-content` is **green**: the content leg flips nothing in the scored oracle set at these
  salts. The three committed oracles are all refused by the permutation leg (block-position
  needs the fixed order; summary-only and contract-table script "the first four calls PASS"
  and the positives land at fresh positions per run — under `--no-content` block-position is
  refused on the marks leg, `positive=0/2 forgers_rejected=8/11`). This does not falsify C1:
  claims.md already records the content leg as "a shape requirement, not the predicate". It
  is reported as a **coverage finding**: `matrix-battery-v5.py`'s docstring presents
  `--no-content` among the "closure-removal twins (mutation evidence)", which a reader can
  take to mean it is a red state; measured, it is not. Any future closure-removal claim for
  the content leg needs a matrix that survives the permutation leg and fails only on shape —
  none of the three committed oracles is that matrix.

## 4. Findings beyond the assigned twins (reported, no instrument edited)

1. **The a2 `CONTRACT`-via-`/proc/<ppid>/cmdline` leak is not closed by any of the three
   closures.** In every row a2 reads the battery's own source path from the parent's cmdline
   and lifts all 12 contract lines (`contract_lines=12` in all seven logs). a2 is REFUSED
   only because the identity leg denies it a positive classification; M2 shows that when the
   identity leg is removed, the cmdline leg alone is enough for a FORGED verdict. The
   contract is public by design (content leg), so this is a shape exposure rather than a
   secrecy break — but it means the a2 verdict is *not* evidence that the cmdline channel is
   closed.
2. **One leg, two forgers.** M2 flips a1 and a2 together: both strip `\n# salt ` before
   hashing, so a single closure-removal costs 2/4. `forgers_handled` therefore over-weights
   the identity leg relative to the receipt leg (M3: 1/4). A count of 4/4 is not four
   independent legs.
3. **M3 shows acceptance tolerates a missing trailer.** Removing `RECEIPT_LINES` leaves the
   positive control ACCEPTED (`integrity=n/a`), so the trailer only ever penalises a child
   that appends — consistent with claims.md's recorded limit ("a truncated receipt is not
   detected by the trailer").
4. **M1B/M4 are the discriminators future rounds should keep**: they isolate "digest exists"
   from "digest is timely" and "line exists" from "line is timely". Both are cheap (one
   `emit`/`flush` edit) and both must stay green.

## 5. Limits of this measurement

- One detector run per twin (`--runs 1`, `SETTLE=26`), as the frozen detector defaults.
  The channels that decided each row are deterministic given the twin (no ORDER line, no
  trailer, strippable salt, buffered position count), and the a7 rows are corroborated by its
  own call log; the only stochastic surface is a7's 8–9 s permutation enumeration, which
  succeeded in both rows where a digest was readable.
- The twins were scored at the frozen salts and the frozen oracle set. They say nothing
  about a matrix that reads subject content semantically (claims.md's own limit) and nothing
  about a receipt truncator (M3's limit).
- The lane tree carries other seats' concurrent round-78 edits (`LOG.md`, `SCORECARD.md`,
  `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/lessons/round-78.md`,
  `.ufo/waves/round-78/`). None is mine; `corpus/evidence/round78/*` shows no modification
  and its hashes are unchanged (§Restoration).

## 6. Restoration and hygiene

- Frozen instrument hashes, before and after every run on this host:
  `matrix-battery-v5.py` = `5545a4718690a80e5d3d6611e43132fdd5cb4dcd67e87be9a27ed44c032b5af0`
  (claims.md value), `forge-battery.py` = `ba98db41e0c82ba0ff3b7cb4259764fcfb85c54b17137da02655ee751f1c5143`.
  No frozen byte was written; the twins exist only as scratch copies and as copies under
  `R78MutA/mutants/` for the record.
- Scratch `/fast/scratch/hyaku/chousa-r78/R78MutA` deleted after the receipts were copied
  into this folder; `ls /fast/scratch/hyaku/chousa-r78` shows the seat directory gone.
- No network, no subagents, no lane or fleet git/jj mutation, no commits, no writes outside
  `.ufo/waves/round-78/w1/R78MutA/` and this report.
- **Tooling:** nothing installed or upgraded (no pacman, no `uv tool`, no PATH writes).
  Used as found: `python3` 3.14.8, `cc` with OpenSSL 3 headers (forge-battery builds its
  `perm` enumerator into its own `--work`), git 2.56.0 (read-only `status`/`rev-parse`).
