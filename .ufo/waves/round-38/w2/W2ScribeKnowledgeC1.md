# W2ScribeKnowledgeC1

## Verdict
Final `env-pin-capture-r38.md` drafted against the integrated revision `8e93bc91…`: P1 `7/7` (my seed 38411) and P2 `7/7` (my seed 38421) re-derived, all nine committed receipts `VERIFY: ok`, and the entry now records both delivery mechanisms, the M3/M4-class unmeasured half, the **live** `date` sibling witness versus the **inert** `grep`/`sha256sum` names, the PATH `bash` shim, the narrowed Erratum-6 reading and the pre-registered r39 cells.

## Evidence
Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`, read-only; scratch `T=/tmp/r38w2scribe.8y6kzlcg` (created first). No lane write except this report; no installs/upgrades; no mutating git/jj.

```text
$ git rev-parse master                       -> 8e93bc916527b3c21f0f702967fa65c3b4c31699
$ sha256sum tools/research-gate.sh corpus/evidence/round38/{c1-count.py,c2-count.py,verify-receipts.py,expectations.jsonl,claims.md}
37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  tools/research-gate.sh
790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221  c1-count.py
414a7a10571263e781137fcbb0fb4e16bd9dbb9a44fda4931d9fe4d67cc403e3  c2-count.py
b63e7e200b88022f6747e4b628cb6b251187ad95f5b33d2b6b4b14e08d5cf952  verify-receipts.py
d34f17353fec83ed2e7b78b41cebcd2a6d309a85d724dbf1097cf6a17afaf8aa  expectations.jsonl
2bc82126e316bbbf8ddace4d7f0cb61c1cde52cce9c36e27545f2bdb1ae6e23d  claims.md
$ sha256sum .ufo/waves/round-3{7,8}/controls/base-gate-r3{7,8}.sh
a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  base-gate-r37.sh
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  base-gate-r38.sh
$ grep -n '| S072 \|| S073 ' corpus/SOURCES.md ; grep -c '^| S' corpus/SOURCES.md  -> no match ; 71
$ ls corpus/knowledge | grep -i r38                                                  -> (empty)
$ sha256sum /usr/share/info/bash.info.gz     -> cde1a3366897684b0a86fe553687e31d070b7839b19ca98186ffc6e0e105588f
$ zcat /usr/share/info/bash.info.gz | sed -n '1459,1464p'
1461  enabled).  Functions may be exported so that child shell processes
1462  (those created when executing a separate shell invocation) automatically
1463  have them defined with the ‘-f’ option to the ‘export’ builtin (*note
1464  Bourne Shell Builtins::). …
$ zcat … | sed -n '1305,1310p'               -> node header 1307, "3.3 Shell Functions" 1309
$ zcat … | grep -n 'BASH_FUNC'               -> (no output)
```

My re-derivations (fresh seeds, existing `C1_TMP`/`C2_TMP`; receipts under `$T`):

```text
$ C1_TMP=$T/c1 python3 corpus/evidence/round38/c1-count.py --gate tools/research-gate.sh --seed 38411 --receipt $T/c1/s38411.json
PASS ×7  ENV_PIN_CAPTURE_MATCH=7/7  C1_EXIT=0
$ C2_TMP=$T/c2 python3 corpus/evidence/round38/c2-count.py --gate tools/research-gate.sh --seed 38421 --receipt $T/c2/s38421.json
PASS ×7  RECEIPT_BINDING_MATCH=7/7  C2_EXIT=0   (in-run refusals: counter-sha256-mismatch / expect-sha256-mismatch / receipt-self-digest)
$ for f in corpus/evidence/round38/receipts/*.json; do verify-receipts.py --receipt $f --gate <bound> --counter <bound>; done
c1-after-s38001, c1-after-s38011, c1-after-s38351, c1-base-s38001, c1-base2-s38003, c2-after-s38101,
c2-after-s38111, c2-after-s38371, c2-base-s38101   -> 9/9 VERIFY: ok (identity chosen from each receipt's own gate/counter hashes)
```

Witness matrix, executed by me on the landed gate `37e2b996…` (pin, then clean `--drift`; `echo` = `GATE_GREP: ` lines in the pinned file):

| witness (delivery) | marker hits | echo | drift | verdict |
|---|---|---|---|---|
| raw `BASH_FUNC_env%%` echo function (counter channel) | 0 | 0 | `GATE_DRIFT: none` rc 0 | blocked |
| real `export -f env` echo function | 0 | 0 | none rc 0 | blocked |
| `export -f date` forwarding + echo | 14 | 1 | `-GATE_GREP` rc 1 | **live** |
| `export -f grep` forwarding + echo | 0 | 0 | none rc 0 | inert |
| `export -f sha256sum` forwarding + echo | 0 | 0 | none rc 0 | inert |
| `export -f bash` forwarding (marker only) | 5 | 0 | none rc 0 | sections only |
| PATH `bash` shim re-adding echo | 6 (w2 log) | 1 | `-GATE_GREP` rc 1 | **live** |
| clean control | – | 0 | none rc 0 | hold |
| r38 base control, same seven | – | 0 | none rc 0 | hold |
| base + raw `env` function | – | 1 | `-GATE_GREP` rc 1 | fails as frozen |

## Findings
1. **C1 and C2 hold on the integrated bytes, and the committed receipt set grew from six to nine.** My seeds 38411/38421 give `7/7` both; the nine receipts include the r38 base control `c1-base2-s38003` (binds `9fcac047…`) and fresh-seed `c1-after-s38351` / `c2-after-s38371`. Pointers: `corpus/evidence/round38/receipts/`; `corpus/evidence/round38/claims.md:225-236` (P1 unchanged). Same-seed overlap with `W2ExecC1Final.md` (38411) and `W2ExecC2Final.md` (38421) is label-level only — not independent replication (Erratum 6d).
2. **Both delivery mechanisms are blocked; the knowledge entry must say so with two observations.** Raw `BASH_FUNC_env%%` and real `export -f` both leave echo 0 / `GATE_DRIFT: none`; the raw form still fails on the base control (echo 1 / `-GATE_GREP`). Mechanism: `env_pin_init` (`tools/research-gate.sh:494-521`) resolves only `/usr/bin/env`,`/bin/env`, and the capture invokes `"$ENV_BIN"` (`:3999-4004`) — an absolute path is not a function-lookup candidate.
3. **`date` is a live sibling witness; `grep` and `sha256sum` are not — calibration correction to the assignment's framing.** A forwarding+echo `date` function produces 1 embedded `GATE_GREP:` line and a phantom `-GATE_GREP` drift on the landed gate (14 invocations); the same shape for `grep` and `sha256sum` produced **zero** invocations because those binaries are already pinned absolutely (`GREP_BIN` `:348-413`, `sha256_pin_bin` `:432-449`). Pointer: my matrix above; `W2ScoutResidual.md` finding 3 reaches the same “do not label grep/sha256sum vulnerable” conclusion.
4. **The `bash` name splits: function vs PATH.** An exported `bash` function is invoked 5× only at the section shell-out (`research-gate.sh:3642`), never at the capture; a PATH shim named `bash` reaches the capture through `env`'s execvp and poisons the landed baseline (my run: echo 1 / `-GATE_GREP` rc 1). `W2LabBashFn.md` records the same 5-vs-6 argv split. This is Erratum 6(c)'s narrowed reading and the entry's wording.
5. **M3/M4's unmeasured half is confirmed on final bytes.** `MutGateC1.md` (w1) shows M3 (delete the absolute-path refusal) and M4 (hardcode `/usr/bin/env`, ignoring a valid override) each score c1 `7/7`, c2 `7/7`, selftest PASS; `W2RevC1Final.md` finding 1 independently shows an unconditional-override-refusal mutant scoring `7/7` on integrated bytes. So the fixture measures rejection of *bad* overrides only; the positive override and the relative-override refusal class are unasserted.
6. **Ambient channels can still flip the printed predicate with gate bytes unchanged.** `W2RevC1Final.md` findings 2-3: `POSIXLY_CORRECT=1` and a bad `TMPDIR` each take the landed gate from `7/7` to `2/7` (GNU grep's `--` handling at `:4008`; `mktemp` at `:3988`). Under the literal kill rule these are false kills; the entry must qualify “clean caller environment” and carry them as r39 cells.
7. **S072 is still not a committed row, and the knowledge file does not exist yet.** `corpus/SOURCES.md` has 71 rows ending at S071; `corpus/knowledge/` has no r38 entry. The drafted entry cites S072 by path (anchor 1461–1464, verified by me), so integration must land the row or the entry must drop the citation. Also, `bash.info` never documents `BASH_FUNC_*` (grep empty) — the encoding stays an r38 measurement, never a citation.
8. **The integrated artifacts have new hashes; w1 report hashes are stale.** Counter/verifier/expectation/claims bytes all changed in the integration (`790407…`, `414a7a…`, `b63e7e…`, `d34f17…`, `2bc821…`); the gate is byte-identical (`37e2b996…`). The entry and any later citation must use the integrated values (confirmed identical to `W2ScoutResidual.md` and `W2ExecC1Final.md`).
9. **Gate selftest and no-harm are contract-cited, not re-run here.** `W2ExecNoHarmFinal.md` records `RESEARCH_GATE_SELFTEST: PASS (272 cases, 0 skipped)` and the claims/chain/archive batteries; I did not re-execute them, so the entry attributes them to that report.
10. **A concurrent wave-2 integration landed in the worktree while I worked; my numbers are the master bytes.** At read time `git diff master` showed: gate `+6` lines (`unset POSIXLY_CORRECT` inserted between `grep_pin_init` and `env_pin_init`, closing W2RevC1Final finding 2 on the gate side), `c1-count.py` `+1` (`POSIXLY_CORRECT` added to `base_env()`'s scrub list — counter side of the same channel), `verify-receipts.py` `+21` (`KNOWN` strict-schema/`unknown-field`, `scenario-row-malformed`, `*-type-mismatch`), `claims.md` `+41` (Errata 9-11), and `receipts/` mid-regeneration (`c1-after-s38001.json` deleted, both base receipts modified). Worktree hashes at that read: gate `0447ad14…`, c1 `a48e5b22…`, verifier `33c7c87e…`, claims `3d7e61c7…`. None of those edits are mine; every measurement here was taken against `37e2b996…`/`790407…`/`b63e7e…`, so the entry's `recheck: on-release` must run on the released bytes.

## Limits
- Seeds 38411/38421 duplicate two wave-2 seats' labels; my runs are independent executions, not extra seed diversity (Erratum 6d).
- `POSIXLY_CORRECT`/`TMPDIR` channels are cited from `W2RevC1Final.md`, not re-executed by me; the `env`-PATH shim is cited from `W2ScoutResidual.md` (my PATH witness is the `bash` shim only).
- `LD_PRELOAD`, `SHELLOPTS=noexec` and the M3/M4 mutants are cited from wave reports (`MutGateC1.md`, `CritNoexec.md`, `CritC1Kill.md`); no preload library or mutant gate was rebuilt.
- I drafted the entry only: `corpus/knowledge/env-pin-capture-r38.md`, `corpus/SOURCES.md` and `corpus/lessons/round-38.md` were not written; no lane, jj, git-index or fleet mutation.
- No tools installed or upgraded; no pacman transaction attempted (host-wide pause observed).

## Draft: `corpus/knowledge/env-pin-capture-r38.md`

```markdown
# Pinned env — a caller function named `env` cannot move a pin baseline

Lane: chousa. Round 38 (C1, operability — the lowest scored axis, 3/10). Surface: `tools/research-gate.sh` (`gate_canonical_capture`, the `--pin` / `--drift` contract), `corpus/evidence/round38/c1-count.py`.

source: S072 (GNU Bash Reference Manual, `bash.info` — `/usr/share/info/bash.info.gz`, Node `Shell Functions` (3.3), node header line 1307, heading 1309, exported-functions sentence 1461–1464 with the quote at 1461–1463: “Functions may be exported so that child shell processes … automatically have them defined with the ‘-f’ option to the ‘export’ builtin”; Bash Edition 5.3, 18 May 2025, installed `bash 5.3.20-1`; file SHA-256 `cde1a336…588f`; the manual contains no `BASH_FUNC` string, so the `name%%` encoding is an r38 measurement, not a citation; registry row not yet committed — 71 rows end at S071); the lane gate `tools/research-gate.sh` (predicate measured on `37e2b996…d27d`; the wave-2 integration then added `unset POSIXLY_CORRECT` — recheck on the released bytes); frozen design `corpus/evidence/round38/claims.md` (§C1/P1/kill rule/Errata 1–11); receipts `corpus/evidence/round38/receipts/` (construction, wave and two control families, regenerated by the wave-2 integration); counter `corpus/evidence/round38/c1-count.py` (`790407…2221` at measurement); expectations `corpus/evidence/round38/expectations.jsonl` (`d34f17…f8aa`); wave reports `.ufo/waves/round-38/{w1/MutGateC1.md,w1/RevErrataCtx.md,w1/ExecEnvFnHarness.md,w2/W2ExecC1Final.md,w2/W2RevC1Final.md,w2/W2LabBashFn.md,w2/W2ScoutResidual.md}`.
verified-at: 2026-10-24 (gate `37e2b996…`; `ENV_PIN_CAPTURE_MATCH=7/7` on seeds 38001, 38011, 38211, 38231, 38251, 38351, 38411, 38431; both base controls `a7d3922c…`/`9fcac047…` 2/7; `RECEIPT_BINDING_MATCH=7/7` on the landed gate, r37-counter control 0/7; nine committed receipts `VERIFY: ok` on those bytes)
recheck: on-release (`python3 corpus/evidence/round38/c1-count.py --gate tools/research-gate.sh --seed <n>` under a clean caller environment → `7/7` with `predicate_holds=true`; any run below 7/7 against the landed gate kills C1)

## What changed

Round 37 closed the `BASH_ENV` startup-file channel, but the capture child still spawned through a BARE `env`. Bash exports shell functions to every child as `BASH_FUNC_<name>%%`, which a child bash imports before its body runs; a caller-exported function named `env` therefore received the capture call itself and could (1) re-add `CHOUSA_GREP_PIN_ECHO` — the baseline embeds a `GATE_GREP:` line and a later plain `--drift` reports phantom `-GATE_GREP`; (2) re-add `CHOUSA_ROOT` — the capture runs against a foreign root; (3) suppress the capture — `--pin` exits 2 and no baseline exists. The capture child now runs through ONE pinned absolute `env` (`ENV_BIN`): `/usr/bin/env` then `/bin/env`, no PATH consultation, `--version` must report `GNU coreutils`; a `RESEARCH_GATE_ENV` override must be absolute, a regular executable file and GNU-reporting, else exit 2 `ENV_PROVENANCE` before any mode runs. An absolute-path command is not a function-lookup candidate, so the named function never receives the capture call.

## Two delivery mechanisms, both measured

- raw `BASH_FUNC_env%%` in the parent environment (the counter's channel, `c1-count.py:60-70,131-147`): landed gate `pin_rc=0`, 0 `GATE_GREP:` lines, `GATE_DRIFT: none`; base gate 1 line and `-GATE_GREP`.
- real `export -f env` in a parent bash, then `exec bash gate --pin`: identical landed hold, identical base failure (`w1/ExecEnvFnHarness.md`).
The hold does not depend on one encoding.

## What it does NOT cover — measured on the same bytes

- Only the NAME `env` at one absolute call site is bypassed. A parent-exported forwarding `date` function still poisons the landed baseline (1 embedded `GATE_GREP:` line, `--drift` rc 1 `-GATE_GREP`, 14 invocations) — the `BASH_FUNC_*` channel is untouched (`w1/RevErrataCtx.md`, `w2/W2ScoutResidual.md`). A `grep` or `sha256sum` function is NOT a witness: those names are already pinned absolutely (`GREP_BIN`, `sha256_pin_bin`) and were invoked zero times in a marker probe.
- An exported `bash` function is imported and invoked 5× at the section shell-out (`research-gate.sh:3642`), never at the capture; a suppressing one pins a crit-severity `VERIFY_ALL_SECTION_UNAVAILABLE` baseline while `--pin` exits 0. The capture is reached through a PATH shim named `bash` instead: 1 echo line, `-GATE_GREP` rc 1 (`w2/W2LabBashFn.md`).
- PATH independence of the env pin, hostile drift, and the override accept/relative-refusal halves are pre-registered r39 cells, not measured coverage.
- No loader scrub for the `env` child (`LD_PRELOAD`), no `SHELLOPTS=noexec` coverage (bash applies `-n` before the body; no in-body fix), and provenance is self-reported (`--version` substring).

## The seven scenarios and the frozen observable

`hold-plain`, `hold-fn-benign` (a benign forwarding `env` function must be harmless), `env-fn-echo-scrub`, `env-fn-root-move`, `env-fn-suppress`, `env-override-missing`, `env-override-fake`. Every cell asserts `pin_rc`, baseline presence, zero `GATE_GREP:` lines and a later clean drift of `GATE_DRIFT: none`; both override cells assert exit 2 and the anchored `research-gate: ENV_PROVENANCE refused:` stderr. Base `a7d3922c…` 2/7 (`receipts/c1-base-s38001.json`), actual pre-round-38 gate `9fcac047…` 2/7 (`receipts/c1-base2-s38003.json`), landed `37e2b996…` 7/7 (`c1-after-s38001/s38011/s38351.json`). Seeds label the receipt only; the run is deterministic (Erratum 6d).

## The unmeasured half the mutants expose

Single-edit gate mutants `M3` (delete the undefined-absolute-path refusal) and `M4` (hardcode `/usr/bin/env` at the capture, ignoring a valid override) each score c1 7/7, c2 7/7 and the shipped selftest PASS (`w1/MutGateC1.md`); on integrated bytes an unconditional-override-refusal mutant also scores 7/7 (`w2/W2RevC1Final.md`). The fixture therefore proves rejection of bad overrides, not that a valid override selects the capture binary, and not the refusal *reason* for a relative override. An ambient `POSIXLY_CORRECT=1` moved the landed gate from 7/7 to 2/7 with its bytes unchanged (GNU grep stops treating `--` as end-of-options); the wave-2 integration closes it on both sides — the gate now `unset POSIXLY_CORRECT` before `env_pin_init`, and `base_env()` scrubs it — while a bad `TMPDIR` still moves the verdict (`mktemp -d "${TMPDIR:-/tmp}/chousa-gate-pin.XXXXXX"`), so the kill rule presumes a clean caller environment with a usable temp base.

## Pre-registered r39 cells (proposed, not implemented)

`env-path-independent` (PATH `env` shim; kill the `command env` mutant), `capture-bash-path` (PATH `bash` shim, record the extra `verify-all` argv), `capture-date-export` (sibling `date` function with marker — the export-scrub cell), `drift-env-function` (hostile drift-only injection must still report `GATE_DRIFT: none`; the eighth scenario), `env-override-honored` (accepted absolute override must appear as the capture argv — kills M4), `env-override-relative` (exact “override is not an absolute path” refusal — kills M3), `env-loader-scrub` (`LD_PRELOAD` on `env` with a hook canary), `verifier_sha256` bound into c2 receipts, plus a `TMPDIR` scrub/refusal cell (the one ambient channel still open after the wave-2 integration). Catalogue and cheapest shapes: `w2/W2ScoutResidual.md` findings 1-12.
```
