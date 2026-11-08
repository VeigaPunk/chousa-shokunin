# R93ExecC1Repro — round-93 C1 (operability) reproduction from a clean carrier tree

Seat: `R93ExecC1Repro` (leaf executor). Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Claim freeze F2 `b7241252c2358613d3b22b7d0454d98c56dab373`; carrier C2
`754b62fb6adc60e44e12375af5461a0ebe302994`, cloned with
`git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo` and
`git -C $S/repo checkout 754b62fb6adc60e44e12375af5461a0ebe302994`; `git -C $S/repo rev-parse HEAD`
= `754b62fb…`, `git -C $S/repo rev-parse --show-toplevel` = `$S/repo`, working tree clean
(`git status --porcelain` 0 lines) before and after every run. Scratch
`S=/fast/scratch/hyaku/chousa-r93/R93ExecC1Repro` (removed before yield). No network, no tool
installs, no lane/fleet git mutation, no production edits.

## Instruments measured

| instrument | disk sha256 | pins-table row |
|---|---|---|
| `control-driver-r93.py` | `ad0f60ee…` | `ad0f60ee…` MATCH |
| `forgeries-r93.py` | `cd81b9e7…` | `cd81b9e7…` MATCH |
| `curation-controls-r93.py` (the unexecuted pinned instrument used in (c)) | `fe7dceba…` | `fe7dceba…` MATCH |

Pins table `corpus/evidence/round93/instrument-pins.txt`: 22 rows; independent recomputation of the
minus-self digest gives `2733d572…` = the self row, while the whole-file sha is `09e85ae0…` (receipt
`R93ExecC1Repro-hashes.txt`). That confirms the self row is the minus-self digest, not a whole-file
sha (K4's self-row clause).

---

## (a) Clean-tree verify — `CONTROL_DRIVER_R93=PASS` (exit 0)

Command (from `$S/repo`):

```
python3 -B corpus/evidence/round93/control-driver-r93.py verify --root . --repo . \
  --rev b7241252c2358613d3b22b7d0454d98c56dab373 \
  --receipts-rev 754b62fb6adc60e44e12375af5461a0ebe302994 --work $S/verify
```

Receipt: `R93ExecC1Repro-a-verify.stdout.txt`. **Exit code 0.** Observed stdout (verbatim):

```
BASES root=/fast/scratch/hyaku/chousa-r93/R93ExecC1Repro/repo repo=/fast/scratch/hyaku/chousa-r93/R93ExecC1Repro/repo
RECEIPT c1-gate-r89 OK committed+exact+pin+fresh
RECEIPT c1-mutants-r89 OK committed+exact+pin+fresh
RECEIPT c1-harm OK committed+exact+pin+fresh
RECEIPT c1-harm-setup OK committed+exact+pin+fresh
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT c2-prior-controls OK committed+exact+pin+fresh
RECEIPT PINS OK 22/22 pinned files byte-identical RECEIPT_PINS_OK=6/6
RECEIPT SELF_PIN OK rev=b7241252c2358613d3b22b7d0454d98c56dab373 receipts_rev=754b62fb6adc60e44e12375af5461a0ebe302994
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS
```

Field-by-field against the frozen predicate:

| expected | observed | |
|---|---|---|
| `CONTROL_DRIVER_R93=PASS`, exit 0 | `CONTROL_DRIVER_R93=PASS`, exit 0 | MATCH |
| `COMMITTED_OK=6/6` | `COMMITTED_OK=6/6` | MATCH |
| `EXACT_OK=6/6` | `EXACT_OK=6/6` | MATCH |
| `PIN_OK=6/6` | `PIN_OK=6/6` | MATCH |
| `FRESH_OK=6/6` | `FRESH_OK=6/6` | MATCH |
| `PINNED_FILES=22/22` | `PINNED_FILES=22/22` | MATCH |
| `RECEIPT_PINS=6/6` | `RECEIPT_PINS=6/6` | MATCH |
| `RECEIPT SELF_PIN OK rev=<F> receipts_rev=<C>` | `RECEIPT SELF_PIN OK rev=b7241252… receipts_rev=754b62fb…` | MATCH |

The driver half of C1 holds at C2 on this host.

## (b) Forgery battery — frozen predicate **not met** (exit 1 in both modes)

Command (from `$S/repo`):

```
python3 -B corpus/evidence/round93/forgeries-r93.py --root . --repo . \
  --rev b7241252c2358613d3b22b7d0454d98c56dab373 \
  --receipts-rev 754b62fb6adc60e44e12375af5461a0ebe302994 --work $S/forge
```

Expected: `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass`, exit 0.
Observed: **exit 1; the summary line is never printed on the host interpreter**, and under a
non-default interpreter it prints `FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1
POSITIVE=fail`.

### (b.1) Host `python3` (3.14.8): crash at archive extraction

Receipt: `R93ExecC1Repro-b-forge-py314.stdout.txt`. **Exit code 1**, 24-line traceback ending:

```
    tf.extractall(dest)
tarfile.AbsoluteLinkError: '.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep' is a link to an absolute path
```

`forgeries-r93.py` line 51 calls `tf.extractall(dest)` with no filter. In Python 3.14,
`TarFile.extraction_filter` is `None` and `_get_filter_function(None)` returns `data_filter`
(`/usr/lib/python3.14/tarfile.py:2444-2448`), and the carrier commits two absolute symlinks
(`.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep` -> `/bin/false`;
`.ufo/waves/round-84/w1/R84ExecForge/forge/linkcap.txt` -> `/fast/scratch/hyaku/...`), so the
extraction is refused before any forgery is built. A direct probe on the same `git archive` output
shows `filter=None` and `filter='data'` both fail with `AbsoluteLinkError` while `filter='tar'`
succeeds (`R93ExecC1Repro-b-rootcause-tarfilter.txt`). The battery produces no
`FORGERY_REFUSED=` line at all.

### (b.2) Diagnostic interpreter 3.13.16: runs, then fails its own controls

Receipt: `R93ExecC1Repro-b-forge-py313.stdout.txt` (invoked as
`/home/vgpnk/.local/bin/python3.13 -B corpus/evidence/round93/forgeries-r93.py …`; Python 3.13 only
avoids the 3.14 default data filter — it is not the frozen interpreter). **Exit code 1**, verbatim
summary:

```
FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail
```

The two forgery lines show the r93 refusal itself works, but the battery cannot count it because the
r92 prior-acceptance conjunct is false for an unrelated reason:

```
FAIL unexecuted-instrument: r93 rc=1 (PIN_DISK_MISMATCH path=corpus/evidence/round93/curation-controls-r93.py), r92 rc=1 accepted=False
FAIL receipt-body: r93 rc=1 (RECEIPT_MISMATCH:c2-prior-landing), r92 rc=1 accepted=False
FAIL derive-from-root: r92 rc=1 (escapes base), r93 rc=1
FAIL positive: r92 rc=1 r93 rc=1
```

Root cause: `archive()` extracts `git archive <receipts-rev>` into `<work>/pristine`, and the
drivers are then run with `--root <tree>` and **no `--repo`**; the expected rows' instruments
receive `@ROOT@` = the extracted tree, and two of them use it as a git repository
(`c1-gate-r89` passes `--repo @ROOT@`; `c1-harm` runs `git -C @ROOT@ show 265b8633…`). An extracted
archive has no `.git`, so those fresh legs fail on every tree (pristine included):

```
RECEIPT PINS OK 22/22 pinned files byte-identical RECEIPT_PINS_OK=6/6 | COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=4/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=FAIL   (derive run)
… COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=4/6 PINNED_FILES=21/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=FAIL   (forgery runs)
… COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=4/6 PINNED_FILES=7 CONTROL_DRIVER_R92=FAIL                    (r92 side)
```

The two failing fresh legs are `c1-gate-r89` and `c1-harm`; their work outputs are quoted in
`R93ExecC1Repro-b-rootcause-nogit.txt` (`GATE_RECORDS_R89=FAIL`, and
`fatal: not a git repository (or any parent up to mount point /)`), and direct reruns on the same
archive tree reproduce exit 1 (`gate-records-r89.py`) and exit 0 (`mutate-r89.py` — so only the two
git-dependent legs fail). No enclosing repository exists above the scratch `--work`
(`/fast/scratch/...` → `fatal: not a git repository`), so ambient git discovery cannot rescue it.

Consequence: the frozen battery cannot print `FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1
POSITIVE=pass` from the frozen command. On the host interpreter it dies at setup; on 3.13 its
positive control (`POSITIVE=pass`), its r92 prior acceptance (`PRIOR_ACCEPTED=2/2`) and its
`DERIVE_OK` (which requires r93 rc 0 on the same archive tree) are all false. This is the C1-K1
condition ("predicate not met at the landing revision").

Note: the r93 refusals themselves are not the failure — the r93 per-forgery lines carry exactly
`PIN_DISK_MISMATCH path=corpus/evidence/round93/curation-controls-r93.py` and
`RECEIPT_MISMATCH:c2-prior-landing`. The broken conjuncts are the fixture's controls, and the 3.14
crash is independent of them.

## (c) Pin-walk discrimination on a real clone — holds

Because the battery's archive root is not a usable repository, the same tamper classes were
replayed inside two real clones (`cp -a` of the C2 clone; each toplevel asserted equal to the
fixture dir before mutation). Full commands and byte provenance:
`R93ExecC1Repro-c-tamper-provenance.txt`.

1. **Unexecuted pinned instrument.** `corpus/evidence/round93/curation-controls-r93.py` pinned
   `fe7dceba…`, tampered to `cb0f274f…` by appending
   `# tamper: one appended byte-or-line beyond C2`. The instrument is not executed by any
   `expected.tsv` row.
   - r93: `… control-driver-r93.py verify --root . --repo . --rev F --receipts-rev C` →
     **exit 1**, receipt `R93ExecC1Repro-c-tamper-inst-r93.stdout.txt`:
     ```
     RECEIPT PINS FINDING PIN_DISK_MISMATCH path=corpus/evidence/round93/curation-controls-r93.py
     COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=21/22 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=FAIL
     ```
   - r92 on the same tree: `… control-driver-r92.py verify --root . --work … --rev F
     --receipts-rev C --expected corpus/evidence/round93/controls/expected.tsv --receipts
     corpus/evidence/round93/controls/receipts --pins corpus/evidence/round93/instrument-pins.txt`
     → **exit 0**, receipt `R93ExecC1Repro-c-tamper-inst-r92.stdout.txt`:
     ```
     RECEIPT PINS OK 7/22 pinned files byte-identical
     COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=PASS
     ```
   So the tamper is caught by r93's full pin walk (21/22) and invisible to r92 (it pins only its
   seven wanted rows). Note the r93 self-pin line still prints OK here: the instrument is caught by
   `pin_report`'s disk comparison, which is the intended detector; the self-pin binds the driver,
   expectations and receipts, not each instrument.

2. **Committed receipt body.** `corpus/evidence/round93/controls/receipts/c2-prior-landing.txt`
   pinned `b336ba2e…`, tampered to `da343517…` by appending
   `# tamper: appended comment in a committed receipt`.
   - r93: **exit 1**, receipt `R93ExecC1Repro-c-tamper-rcpt-r93.stdout.txt`:
     ```
     RECEIPT PINS FINDING PIN_DISK_MISMATCH path=corpus/evidence/round93/controls/receipts/c2-prior-landing.txt,RECEIPT_MISMATCH:c2-prior-landing
     RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round93/controls/receipts/c2-prior-landing.txt@754b62fb6adc60e44e12375af5461a0ebe302994
     COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=21/22 RECEIPT_PINS=5/6 CONTROL_DRIVER_R93=FAIL
     ```
   - r92 on the same tree: **exit 0**, receipt `R93ExecC1Repro-c-tamper-rcpt-r92.stdout.txt`:
     ```
     RECEIPT PINS OK 7/22 pinned files byte-identical
     COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=PASS
     ```

(c) therefore holds: the r93 pin walk is not self-satisfying and genuinely discriminates against
r92 on both tamper classes. The C1 failure is confined to the battery instrument.

## (d) `verify` writes nothing — holds

Receipts `R93ExecC1Repro-d-receipts-before.sha.txt` / `…-d-receipts-after.sha.txt` and
`R93ExecC1Repro-d-no-writes.txt`:

- `sha256sum corpus/evidence/round93/controls/receipts/*.txt` before and after the (a) run:
  `diff` empty, `RECEIPTS_BYTE_STABLE=yes` (all six digests unchanged).
- `git status --porcelain` in the clean C2 clone after the run: **0 lines**.
- Receipt mtimes unchanged (clone time `2026-11-08 11:10:17`, verify ran later).
- Files written by the run exist only under `--work` (`$S/verify`: six `fresh-*.out` plus
  `harm/base-tool.py`); nothing under the receipts directory.

---

## Findings

**F1 (claim-breaking, C1-K1).** The frozen battery command exits 1 and does not print
`FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass` at C2. Two independent causes,
both in `forgeries-r93.py` as frozen:

- **F1a — extraction crash on the host interpreter.** `archive()` calls `tf.extractall(dest)`
  with no filter; Python 3.14's default `data_filter` refuses the two absolute symlinks committed
  in the carrier (`.ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep` → `/bin/false`, and
  `.ufo/…/round-84/…/linkcap.txt` → `/fast/scratch/...`). Exit 1 with
  `tarfile.AbsoluteLinkError`; no forgery runs. Direct evidence:
  `R93ExecC1Repro-b-forge-py314.stdout.txt`, `…-b-rootcause-tarfilter.txt`.
- **F1b — archive root is not a repository, so the battery's own controls cannot pass.** The
  battery extracts a `git archive` (no `.git`) and runs the drivers without `--repo`; the
  `@ROOT@` instruments `c1-gate-r89` and `c1-harm` need git history. Both drivers score
  `FRESH_OK=4/6` on the pristine archive, so `POSITIVE=fail`, `PRIOR_ACCEPTED=0/2` (r92 rc 1 on the
  same tree regardless of the tamper) and `DERIVE_OK=0/1` (r93 rc 1 on the pristine tree). Evidence:
  `R93ExecC1Repro-b-forge-py313.stdout.txt`, `…-b-rootcause-nogit.txt`. This is not fixed by the
  3.14 filter alone: with 3.13 the battery runs but still cannot print its frozen line on the
  frozen `--work` (outside any repository).

**F2 (not a finding against the driver).** On a real clone at C2 the r93 driver prints the exact
frozen verify line (`PINNED_FILES=22/22 RECEIPT_PINS=6/6`, self-pin `rev=F receipts_rev=C`, exit 0),
refuses both tamper classes with `PIN_DISK_MISMATCH` / `RECEIPT_MISMATCH` (exit 1), and writes
nothing. r92 accepts both tampers on the same bytes (`PINS OK 7/22`, `PINNED_FILES=7`, exit 0), so
the (c) discrimination the claim asserts is real — it is the battery wrapper, not the pin walk,
that fails.

**F3 (observation, [INFERENCE]).** None of the six committed receipts captures the battery's own
stdout; the six are expected-row inputs (`c1-gate-r89`, `c1-mutants-r89`, `c1-harm`,
`c1-harm-setup`, `c2-prior-landing`, `c2-prior-controls`). The freeze therefore committed a battery
whose success was never receipted, which is consistent with the crash surviving freeze; this repro
is the first recorded execution and it fails.

## Risks and limits of this repro

- The frozen command names `python3`; on this host that resolves to `/usr/bin/python3` = 3.14.8
  (`which -a python3`). Python 3.13.16 was used only as a diagnostic to separate the tarfile crash
  from the fixture-logic failure; it is not the scored interpreter.
- The 3.13 run emitted a `DeprecationWarning` from `extractall` about the 3.14 default filter,
  confirming the same code path.
- C1 named limit (3) (instruments reading data outside their own bytes) is not implicated: the
  frozen instrument bytes match their pin rows; the failure is fixture construction and interpreter
  behaviour.
- No network request, no package install or upgrade, no sudo, no host service, no host sysctl; no
  lane/fleet git state was mutated (all mutation happened in scratch copies whose
  `rev-parse --show-toplevel` was asserted first). Scratch
  `/fast/scratch/hyaku/chousa-r93/R93ExecC1Repro` was deleted before yield.

## Receipts copied into this wave folder

- `R93ExecC1Repro-a-verify.stdout.txt` — (a) clean verify stdout, exit 0.
- `R93ExecC1Repro-b-forge-py314.stdout.txt` — (b) frozen battery on host `python3` 3.14.8, exit 1
  (AbsoluteLinkError, no summary line).
- `R93ExecC1Repro-b-forge-py313.stdout.txt` — (b) same battery under 3.13.16, exit 1
  (`FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail`).
- `R93ExecC1Repro-b-rootcause-tarfilter.txt` — extraction-filter probe, committed symlink inventory.
- `R93ExecC1Repro-b-rootcause-nogit.txt` — archive-root git absence, failing fresh legs, ambient probes.
- `R93ExecC1Repro-c-tamper-provenance.txt` — clones, toplevel assertions, appended bytes, shas, commands.
- `R93ExecC1Repro-c-tamper-inst-r93.stdout.txt` / `…-c-tamper-inst-r92.stdout.txt` — instrument tamper,
  r93 exit 1 vs r92 exit 0.
- `R93ExecC1Repro-c-tamper-rcpt-r93.stdout.txt` / `…-c-tamper-rcpt-r92.stdout.txt` — receipt tamper,
  r93 exit 1 vs r92 exit 0.
- `R93ExecC1Repro-d-receipts-before.sha.txt`, `…-d-receipts-after.sha.txt` — identical receipt digests.
- `R93ExecC1Repro-d-no-writes.txt` — git status, mtimes, `--work` contents.
- `R93ExecC1Repro-hashes.txt` — C2/F revisions, interpreters, pinned bytes, minus-self recomputation.

VERDICT: R93ExecC1Repro C1 fired — the frozen verify half holds exactly (CONTROL_DRIVER_R93=PASS, exit 0, COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=22/22 RECEIPT_PINS=6/6, SELF_PIN rev=b7241252… receipts_rev=754b62fb…), but the frozen battery cannot print FORGERY_REFUSED=2/2 PRIOR_ACCEPTED=2/2 DERIVE_OK=1/1 POSITIVE=pass and exits 1: on host python3 3.14.8 it crashes at tf.extractall(dest) on the committed absolute symlink .ufo/waves/round-35/w2/MutGrepShimPath/shims/b/grep (tarfile data filter), and under 3.13.16 its extracted-archive root has no .git, so c1-gate-r89 and c1-harm fresh legs fail, giving FORGERY_REFUSED=0/2 PRIOR_ACCEPTED=0/2 DERIVE_OK=0/1 POSITIVE=fail; the driver's pin walk itself is sound, since on real clones r93 refuses both tamper classes (PIN_DISK_MISMATCH, RECEIPT_MISMATCH; exit 1) while r92 accepts both (exit 0) and verify writes nothing.
