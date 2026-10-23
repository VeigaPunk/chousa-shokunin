# ExecPinModeSweeps — verify-sweeps under the grep pin

Access date: 2026-10-23. Axes: operability and calibration.

## Verdict on the assigned target

**No difference between the clean and grep-shimmed runs.** All four environments returned exit 0, CLEAN, `VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3`, empty stderr and zero-byte PATH/function tripwires. The relative override was refused with exit 2 and empty stdout. This is a measured no-change result, not a C1/P1 kill or a surviving 9/9 engine control.

Important calibration limit: **this fixture's sweeps path never invokes matcher grep**. The pre-pin gate also passes all four environments with empty tripwires. Empty tripwires here cannot establish matcher-call pinning. The committed C1 counter uses verify-claims, not verify-sweeps (`corpus/evidence/round35/c1-count.py:87-96`), so this observation does not invalidate that counter's chosen surface.

## Pinned inputs and command

Artifact paths below are relative to `.ufo/waves/round-35/w2/ExecPinModeSweeps/`, abbreviated `A/`.

- `A/pinned/tools/research-gate.sh`: extracted from revision `e87c5d7ea2dbf3730b36a3961de3f06261d015e4`; SHA256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617`.
- Pre-pin comparison: scratch clone at `08be4c9e3a4ebe55d915ce4761c81854286c23ae`, gate SHA256 `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b`.
- Committed fixture: `corpus/fixtures/sweeps-r5.md`, SHA256 `025352b75b7b109147fee8b8eb13b4f74eaa1550489e83166ce1dd59cfb14907`; `git ls-files` confirmed tracking.

Executed command (exit 0):

```sh
timeout 120 bash /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-35/w2/ExecPinModeSweeps/pinned-receipt.sh
```

The script runs each gate as `env -i HOME=... PATH=... TMPDIR=... /usr/bin/timeout 600 bash GATE verify-sweeps FIXTURE --root REPO`. Reproduction requires the scratch shim/symlink farm created by `A/harness.sh`; retained receipt is `A/final-receipt.out`.

| Environment | Exit | Summary | PATH / function tripwire bytes | Stderr |
|---|---:|---|---:|---|
| Clean PATH | 0 | VERIFIED_SWEEPS=1/2 REJECTIONS_OK=3/3 | 0 / 0 | empty |
| Logging grep first on PATH | 0 | same | 0 / 0 | empty |
| BASH_ENV grep() function | 0 | same | 0 / 0 | empty |
| Symlink-farm PATH without grep | 0 | same | 0 / 0 | empty |

All four stdout hashes after removal of the volatile timestamp field were `263a11519823d874b7df1d5ade6833b200285408a02c5ba436aa101d415f2eab`. The pre-pin gate returned the same four results and the same normalized hash.

Refused override results, same pinned gate and fixture:

| Override | Exit | Stdout | Refusal reason following `research-gate: GREP_PROVENANCE refused:` |
|---|---:|---:|---|
| `bin/grep` | 2 | 0 bytes | override is not an absolute path (candidate=bin/grep) |
| `/nonexistent/x` | 2 | 0 bytes | override is not a regular file (candidate=/nonexistent/x) |
| Absolute non-GNU stub | 2 | 0 bytes | override does not report GNU grep: <no version> |

The non-GNU stub writes its version to stderr, which the gate suppresses; `<no version>` is therefore expected for this stub. Explicit `/usr/bin/grep` was accepted, exit 0. Default echo printed `GATE_GREP: path=/usr/bin/grep source=default version="grep (GNU grep) 3.12-modified"`.

## Mechanism and calibration

A pinned-gate `strace -f -qq -e trace=execve` run on verify-sweeps retained exactly one grep exec: `/usr/bin/grep --version` (`A/pin-census-verify-sweeps.txt`). This is the provenance probe at pinned-gate lines 358-365. The sweeps body at lines 2561-2749 uses shell glob expansion and path guards, not matcher grep. The earlier base-gate census recorded zero grep execs for this mode.

`A/refusal-ordering.sh` additionally ran a local sweeps-mode analogue of the nine C1 scenarios: pinned gate `SWEEPS_PIN_MATCH=9/9`; pre-pin gate `3/9`, failing S4-S9. This is **not the committed C1 counter or P1 evidence**. It shows that the sweeps-mode S1/S2/S3 observations do not discriminate the pin: the unpinned gate passes them too. The refusal/echo scenarios provide the discrimination.

With a bad override and a nonexistent record, the pinned gate reports provenance refusal while the base reports record-not-found. This verifies diagnostic ordering, not absence of file opens; no open-trace claim is made. Pinned `--help` still exits 0 with usage and no refusal.

## Additional bounded findings

### Existing default PATH fallback is dead (confirmed, already repaired elsewhere)

Pinned-gate line 351 defines a `grep()` shell function before initialization at line 8039. Its line-388 `command -v grep` returns `grep`, not an absolute filename; lines 389-390 therefore cannot accept the result. The line-393 refusal mentions PATH even though the fallback cannot discover a PATH executable.

Command: `timeout 900 bash A/dead-path-fallback.sh` (script exit 0). In a private user/mount namespace, both fixed candidates were replaced by non-GNU stubs and a copied GNU grep was placed first on PATH. Pinned gate: exit 2, empty stdout, refusal saying no GNU grep at the fixed locations or on PATH. Namespace control without replacement: exit 0, normal sweep summary. Exact receipt: `A/attack3.out`.

This corroborates sibling `MutGrepShimPath.md`; it is not a new surviving defect in final bytes. The concurrently hardened worktree `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` removes this fallback. The appended claim erratum explicitly records that repair (`corpus/evidence/round35/claims.md:172-181`).

### Non-grep PATH dependencies remain (outside C1's declared surface)

Command: `timeout 600 bash A/pinned-realpath-attack.sh` (script exit 0); receipt `A/f4b.out`.

- On the committed sweep fixture, a `realpath` shim returning `/` changes exit 0/CLEAN/1-of-2 verified to exit 1/DRIFT/0-of-2 verified, with two OUT_OF_CORPUS findings.
- On a scratch-only fixture naming a nonexistent absolute location outside ROOT, a `readlink` shim reporting ROOT changes exit 1/refused to exit 0/CLEAN/`VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1`. No external file content was read. The pre-pin gate also returned this false CLEAN under that shim: inherited behavior, not a pin regression.

Thus grep pinning does not make sweeps verdicts independent of all PATH-resolved tools. This does **not** kill the expressly grep-scoped C1 claim and is not a C2/P2 bypass.

## Evidence ledger and limits

Retained small receipts, SHA256:

- `A/final-receipt.out`: `11bde78d799f7fe3b2154f01676fd80be40225176aedf05b55e7a2af3f62c546`
- `A/ordering.out`: `11826f96d8b7234e36fb12a27c2b27a64267527b8b56911e52783812b9dadf7c`
- `A/attack3.out`: `10b68a18e74097e4034944c7e00b64e08eddd1d2d4b2828411bea44b0cc29f66`
- `A/f4b.out`: `83267f9943652afed389cea3a5bdfa1308b2cc3a106bab557bc7234a46cb903c`
- `A/pin-census-verify-sweeps.txt`: `4455b11edc4609eb0fe5a4e860fa582a746c04ad29e63cb52d1b9d14748dbf2f`

All raw scratch files remain under `/tmp/hyaku/chousa-r35/w2/ExecPinModeSweeps/`. Early exploratory harnesses had reporting/path-construction bugs and some addressed the drifting worktree; they are superseded by the explicitly pinned receipts above. They must not be used to score either gate. `A/discriminating-surface.sh` initially omitted S9's echo flag; `A/refusal-ordering.sh` corrected it. The final pinned-receipt presentation error was corrected before retaining the clean receipt.

Changed files: this exclusive report and experiment artifacts under `A/` only; no production file edits, commits, index changes, network access, installs, build, lint, formatter or selftest runs. LSP tooling was unavailable in the supplied tool inventory; no symbol refactor was attempted. No C2 counter, witness battery or slen probe was executed by this seat; their source/context was opened only. No MEETS control is claimed. No blocker remains for the assigned sweeps measurement.
