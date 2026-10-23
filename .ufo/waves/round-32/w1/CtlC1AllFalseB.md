# CtlC1AllFalseB — C1 all-false / junk controls

## Result and axes

**Operability:** all four requested controls **MISSES** on both completed fresh-seed runs: `APPEND_SERIALIZED=0/24`, exit 1, `predicate_holds=false`. **Coverage:** the counter rejects these four invalid append behaviors across all four trial classes; this does not establish complete C1 coverage or any C2 result. No control reached `MEETS-TARGET` and no candidate implementation was scored.

Paths below use:

- `L=/home/vgpnk/Projects/shokunin/chousa-shokunin`
- `S=/fast/scratch/hyaku/chousa-r32/w1/CtlC1AllFalseB`
- `A=$L/.ufo/waves/round-32/w1/CtlC1AllFalseB`

Read `corpus/evidence/round32/claims.md` first, then both frozen counter docstrings. The binding C1 behavior is at `claims.md:23-28`; target at `claims.md:36-40`. Read the append implementation at `tools/research-gate.sh:3159-3203` and C1 checking, execution, cleanup and receipt logic at `c1-count.py:109-133,157-248,251-330`.

## Provenance and construction

`timeout 30 sha256sum tools/research-gate.sh corpus/evidence/round32/c1-count.py corpus/evidence/round32/c2-count.py` (cwd `$L`, exit 0) produced:

```text
0bc318b3e74ac0ad45f4b34154e886d84aebf44673612afab6de5e0b0ff11258  tools/research-gate.sh
9e787e80b215f6522335c639d5e1b2e60d0a5812b83a9760daf8be9f78415885  corpus/evidence/round32/c1-count.py
b6626b2cb81b2aeaf66a8ff11a06c030612bf4e264dc128f290021c4aa71f54c  corpus/evidence/round32/c2-count.py
```

The gate hash equals the BASE hash frozen in `claims.md:3-4`. `timeout 30 git show 4111607c857bc29ff31883bc095ae00afb527e50:corpus/evidence/round32/c1-count.py | timeout 30 sha256sum` (exit 0) returned the same C1 counter hash. All eight completed receipts independently record that counter hash on line 3 and the scratch gate hash on line 5.

Created only the assigned scratch and artifact directories, then ran four `timeout 30 cp -- tools/research-gate.sh "$S/<control>.sh"` commands, chained with `&&` (exit 0). Applied only the following scratch append-block changes; production files and counters were not edited:

| Control | Scratch change / evidence | SHA-256 |
|---|---|---|
| (a) `no-append.sh` | Replaced the delimiter probe and append with `: # Negative control: never write the manifest.` (`$S/no-append.sh:3185`). Other verify-all work still runs. | `7e98299ae624a258fd370fc94f5115c60224c7a533d8b195ceee88a4a43e8e2a` |
| (b) `junk-line.sh` | Inserted `line='junk-not-json'` after JSON construction; kept the BASE delimiter probe and append (`$S/junk-line.sh:3185`). | `6c2053e16366bff23289de4c221f6661eee21034092648a661f16175474aa4bd` |
| (c) `always-newline.sh` | Replaced the entire probe and conditional prefix with `line=$'\n'$line`; kept the BASE append (`$S/always-newline.sh:3185-3190`). | `61e2e1122c0dbfa2caf1d01bec3ce7c6dd110da14853cf7cce6b3759e87692d6` |
| (d) `rewrite-rename.sh` | Opens the manifest for append, takes `flock -x` on that descriptor before the BASE last-byte probe, copies the complete manifest to `mktemp`, writes the next line there and `mv -f`s it over the manifest before closing the locked descriptor (`$S/rewrite-rename.sh:3185-3219`). | `1623967376676c6c490acc170d08d0094da1c8aeec931030b92d2a96e3f689c0` |

Hashes were observed with `timeout 30 sha256sum` over those four exact paths (exit 0). The rename control deliberately keeps an actual exclusive flock on the originally opened manifest through the rename; it does not preserve that inode as the pathname's identity.

## Commands and completed scores

All counter executions used cwd `$L`, with `C1_TMP=$S`, `C2_TMP=$S`, `TMPDIR=$S`, and `PYTHONDONTWRITEBYTECODE=1`. Four controls were scored concurrently, two seeds sequentially per control. The two missing no-append runs were subsequently replaced by two concurrent fresh-seed executions with the higher bounded process limit described below.

Exact expanded commands, exit codes and captured stdout/stderr are retained in:

- [initial-run-log.json](CtlC1AllFalseB/initial-run-log.json): initial eight executions, including two failed no-append executions.
- [replacement-run-log.json](CtlC1AllFalseB/replacement-run-log.json): two completed replacement executions.

Command shape actually executed, with the literal paths and seeds expanded in those logs:

```sh
timeout --signal=INT --kill-after=15 400 \
  prlimit --nproc=2000 --as=4294967296 \
  python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round32/c1-count.py \
  --gate "$S/<control>.sh" --seed <seed> \
  --receipt "$A/<control>-s<seed>.json"
```

Only the two completed no-append replacements used `--nproc=8192` instead of 2000. Every completed run had solo `ref_rc=0`, counter exit 1, and the following recorded counts:

| Control | Fresh seed | Count | F_unterminated | L_empty | L_terminated | L_unterminated | Verdict |
|---|---:|---:|---:|---:|---:|---:|---|
| no-append | 660714253 | 0/24 | 0/12 | 0/4 | 0/4 | 0/4 | MISSES |
| no-append | 1849101119 | 0/24 | 0/12 | 0/4 | 0/4 | 0/4 | MISSES |
| junk-line | 4002894681 | 0/24 | 0/12 | 0/4 | 0/4 | 0/4 | MISSES |
| junk-line | 1772269673 | 0/24 | 0/12 | 0/4 | 0/4 | 0/4 | MISSES |
| always-newline | 709508655 | 0/24 | 0/12 | 0/4 | 0/4 | 0/4 | MISSES |
| always-newline | 3365157087 | 0/24 | 0/12 | 0/4 | 0/4 | 0/4 | MISSES |
| rewrite-rename | 2769961969 | 0/24 | 0/12 | 0/4 | 0/4 | 0/4 | MISSES |
| rewrite-rename | 2735497235 | 0/24 | 0/12 | 0/4 | 0/4 | 0/4 | MISSES |

Every completed stdout begins `APPEND_SERIALIZED=0/24`, followed by those four per-class lines. The full per-trial lines, including exact failure names, are in [trial-lines.txt](CtlC1AllFalseB/trial-lines.txt), derived from the unmodified receipt arrays without another gate execution. SHA-256 of that artifact: `f5693b52a6c066aa447d249e9a4d3385c8af597b9b1f884ce60d19c682ce5a79`.

| Control / seed | Receipt under `$A` | `trial-lines.txt` lines |
|---|---|---|
| no-append / 660714253 | [no-append-s660714253.json](CtlC1AllFalseB/no-append-s660714253.json) | 3-33 |
| no-append / 1849101119 | [no-append-s1849101119.json](CtlC1AllFalseB/no-append-s1849101119.json) | 35-65 |
| junk-line / 4002894681 | [junk-line-s4002894681.json](CtlC1AllFalseB/junk-line-s4002894681.json) | 67-97 |
| junk-line / 1772269673 | [junk-line-s1772269673.json](CtlC1AllFalseB/junk-line-s1772269673.json) | 99-129 |
| always-newline / 709508655 | [always-newline-s709508655.json](CtlC1AllFalseB/always-newline-s709508655.json) | 131-161 |
| always-newline / 3365157087 | [always-newline-s3365157087.json](CtlC1AllFalseB/always-newline-s3365157087.json) | 163-193 |
| rewrite-rename / 2769961969 | [rewrite-rename-s2769961969.json](CtlC1AllFalseB/rewrite-rename-s2769961969.json) | 195-225 |
| rewrite-rename / 2735497235 | [rewrite-rename-s2735497235.json](CtlC1AllFalseB/rewrite-rename-s2735497235.json) | 227-257 |

## Counterexamples, evidence, smallest safe correction

1. **Never writing is not serialization.** Both no-append receipts report `no-final-newline` in all 24 trials, `gate-lines=0/8` in all 12 L trials and `gate-lines=0/16` in all 12 F trials (receipt trial arrays; `trial-lines.txt:3-65`). The hold check alone is insufficient, but the existing output-count and termination checks reject the shortcut. Smallest safe correction to this behavior: perform the required append under the manifest's exclusive lock; no predicate change is indicated by this control.
2. **Junk is not a JSON receipt.** Each junk run has 16 `invalid-json-line` failures, eight `prefix-rewritten` failures and 12 `appended-under-cooperating-lock` failures (`trial-lines.txt:67-129`). The latter eight prefix failures arise when the cooperating fragment is no longer at the required seed prefix; the counter returns early on that failure (`c1-count.py:165-167`). Smallest safe correction: retain the genuine JSON object and append it with locked delimiting, rather than merely writing any line.
3. **Blind newline-prefixing is not delimiting.** Both always-newline runs have `blank-line` in all 12 F trials plus all four L_unterminated trials; all 12 L trials also wrote under the cooperating lock (`trial-lines.txt:131-193`). Smallest safe correction: decide the delimiter from the last byte while holding the required lock, instead of always prefixing a newline.
4. **A correct original-inode flock does not make rename append-only.** This is the strongest identity counterexample. All 24 L trials across the two rename receipts fail solely with `inode-changed`; no L trial has an under-lock-write failure. All 24 F trials lose lines (7-15 observed JSON gate objects out of 16). The inode check fires in 19 and 20 total trials respectively, so neither run relies only on its JSON syntax check (`trial-lines.txt:195-257`; examples: first receipt trial 1 at lines 31-39, second receipt trial 0 at lines 21-29). [INFERENCE] Replacing the pathname splits future writers across inode-based locks; holding the old lock cannot protect the replacement. The C1 contract explicitly forbids this tradeoff (`claims.md:27-28`). Smallest safe correction: append on the locked manifest descriptor; do not replace the file. No admission or Rust judgment is made here.

No tested control escaped the frozen target. These scores support rejection of these four behaviors only, not a claim that the counter proves arbitrary code obeys flock or never transiently rewrites bytes.

## Harness finding and limits

Two initial no-append attempts did not produce receipts and are **not** counted as completed 0/24 scores:

- Seed 3070279110: exit 2, stderr `c1-count: trial 15 harness error: BlockingIOError(11, 'Resource temporarily unavailable')`.
- Seed 3469348936: exit 1, uncaught `BlockingIOError: [Errno 11] Resource temporarily unavailable` from the solo `subprocess.run` at counter line 278; no score or receipt.

Both used `--nproc=2000`; commands and complete stderr are preserved in `initial-run-log.json`. Raising the bounded limit to 8192 and using new seeds yielded the two completed no-append receipts above. [INFERENCE] User-wide RLIMIT_NPROC pressure caused the launch errors; no valid process-count measurement was obtained. An auxiliary `timeout 30 ps -u vgpnk -L -o lwp= | timeout 30 wc -l` probe printed `ps: unsupported option '-L'` and `0`; that zero was ignored.

**Fixable counter defect, not a control pass:** the docstring promises exit 2 for harness errors (`c1-count.py:44-45`), but the solo launch only catches `TimeoutExpired` (`c1-count.py:277-286`) and the observed resource failure exited 1 without a receipt. Smallest maintenance correction would be to classify solo-launch `OSError` as a harness error, not a predicate miss. Also [INFERENCE], partial failure inside `launch` can lose its local list before assignment to the caller (`c1-count.py:113-120,214`), so cleanup deserves ownership-preserving handling. Neither defect was patched; the frozen counter remains unchanged. Reported the observed error evidence to `ChousaR32A2.MutC1CounterB`.

Before writes, `timeout 30 df -h /fast` (exit 0) showed 236G available. Final `timeout 30 stat -c '%n %s bytes'` over the four scratch gates and three derived logs (exit 0) reported gates of 305811-307209 bytes and logs of 1632-14831 bytes; each is below 1 MiB. Each receipt is also below 1 MiB. Final `timeout 30 pgrep -af '/fast/scratch/hyaku/chousa-r32/w1/CtlC1AllFalseB/(no-append|junk-line|always-newline|rewrite-rename)\.sh'` exited 1 with no output: no matching control processes remained. Normal counter cleanup also kills/waits outstanding writer groups (`c1-count.py:123-133,246-247`).

No network, installs, production edits, counter edits, git/jj writes, candidate scoring, selftest, C2 execution, or other runtime invocation. Retained scratch gates and scoped receipts/logs as review evidence. No broader gate correctness or canonical lane verdict is asserted.
