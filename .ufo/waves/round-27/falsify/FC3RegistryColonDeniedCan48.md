# FC3RegistryColonDeniedCan48: C3 control `registry-colon-denied-canonical-alias`

Scope: round27 attempt1, falsification of one named item at landed `dd72641e574679c4f7882dd43de072b4c8892d6f`. Sandbox: `/tmp/chousa-r27-falsify-FC3RegistryColonDeniedCan48` (archive extract; no lane file edited). Gate sha256 `ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84` matches the pin. Axis: calibration (C3).

**Verdict: FALSIFIED (narrow).** The control does not discriminate the canonical-alias repair it names. Each single-site regression of that repair passes it. It fails only when both canonical denylist sites regress together, and then only when the fixture root sits outside a denylisted component. Denial itself holds: no colon-class under-refusal was found.

## Item and fix

- Control: `corpus/evidence/round27-regressions.py:176-179`. Alias `registry-alias.md` to `synthetic:fixture/.config/registry.md`; expects exit 2, `metadata registry refused: denylist`, zero `^RESEARCH_GATE: ` lines.
- Targeted production fix: `metadata_registry_load` canonical arm `tools/research-gate.sh:2394` (`is_denylist_fs_path "$canon"`) and fd-canonical arm `:2401` (`is_denylist_fs_path "$fdcanon"`). Base had `is_denylist_path` at base `:2375` and `:2382` (hunk `@@ -2372,14 +2391,14 @@`). The raw-arm change on the same line is the target of control `colon-denied-component`, not this one.

## Q1. Is the expectation derived from the contract, independent of gate code? Partly.

- Refusal of the canonical target: derived from `round27-claims.md` C3 ("no reading a denylisted synthetic path when a colon occurs earlier"; "complete filesystem paths"). Independent of gate code.
- Exit 2: the gate's own class (header `Exit: 0 CLEAN | 1 DRIFT | 2 setup/usage`, `research-gate.sh:386`; `die_usage` exits 2, `:390`). The contract names no refusal exit code. The sibling `entry-colon-denied-canonical-alias` (`regressions.py:194-195`) expects exit 1 for the same alias class, so the exit class is chosen per surface by the implementation.
- Substring `metadata registry refused: denylist`: copied from gate `:2426`. Gate-coupled; any wording change is a false mismatch.
- Zero `RESEARCH_GATE:` lines: setup-error convention, consistent with "no read, no verdict".
- Sound design: the target is a well-formed, readable registry, so refused-versus-read is observable. A read gives exit 0 or 1 and one record (seen in m-both).

## Q2. Does reverting the fix make the control fail for the intended reason?

Harness: `harness/target_control.py` is a statement-copied extraction of this one control (`regressions.py` lines 27-28, 31-44, 57, 60-67, 166-173, 176-179). It runs only the target plus sandbox probes. Variants are `tools/research-gate.<v>.sh`. `landed-instr` is the landed gate plus one env-gated log line after the `fdcanon=` assignment (`GATE_OPEN_LOG`; no effect when unset). Each mutant differs from `landed-instr` only at the listed line, and all pass `bash -n`.

| variant | change | target (exp rc 2, 0 records) | open log |
|---|---|---|---|
| landed-instr | none | PASS: rc 2, refusal text, 0 records | no refused target is ever opened |
| m-canon | `:2394` canonical to `is_denylist_path` | PASS (masked) | the target canonical file IS opened, then refused by the fd arm with identical text |
| m-fd | `:2401` fd to `is_denylist_path` | PASS (masked) | none |
| m-both | both canonical sites to `is_denylist_path` | FAIL: `exit 0 != 2`; refusal text missing; `RESEARCH_GATE` count 1 != 0 | target opened |
| m-canon-removed | canonical check deleted (raw and fd kept) | PASS (masked) | target and P1 opened before the fd refusal |
| m-full-only | helper drops the truncated arm | target PASS (refused via `/.config/`) | P1 and P4 now allowed |
| landed, `TMPDIR` under a `.config` dir | none | PASS for the wrong reason: every fixture refused (P2, P5, P7 rc 2) | none |
| m-both, `TMPDIR` under a `.config` dir | both canonical sites | PASS (VACUOUS; should fail) | none |

m-both fails for the intended reason. The gate ran a normal verify and read the denylisted registry: stdout `META entry=entry.md source=present verified_at=dated recheck=scheduled verdict=clean`. It is not a parse or setup error (`bash -n` rc 0). m-full-only is a literal complete-path reading. It passes the target, but P4 (the same fixture as sibling `legacy-env-anchor-refusal`, `regressions.py:170`) flips to rc 0 with one record, which would mismatch that sibling's expected 2 and 0.

## Q3. Counterexamples

- **CE-1 Single-site regressions are undetected.** Minimal: m-canon, m-fd, m-canon-removed (table above). The fd arm re-checks the opened file's canonical path with the same full-path helper and fires with the same message, so the control cannot tell which arm refused. The scout claim that it "exercises the `:2375` canon arm distinctly from the raw arm" (`.ufo/waves/round-27/build/ScoutPathCallers.md:118-121`) does not hold for the canonical arm.
- **CE-2 A denylisted target is opened while the control stays green.** m-canon-removed opens `…/synthetic:fixture/.config/registry.md` before refusing. The gate header (`research-gate.sh:252`) says "Opens: allowlist metadata only; denylist → SESSION_READ". The control checks outcome only. No content is parsed before refusal, so the round27 "no reading" wording is not violated; the header's "Opens" wording is.
- **CE-3 Environment vacuity.** The script does not pin `TMPDIR`, and `tempfile` honors it. With a temp root under a denylisted component, the raw arm refuses every path and m-both passes. The sibling `ordinary-colon-is-allowed` would also flag this environment (P5 refused), so the suite catches it only indirectly.
- **CE-4 Over-refusal of a colon-named canonical directory (calibration, not a bypass).** Alias to `…/notes.env:v2/registry.md` (valid registry, no denylisted component): rc 2 "denylist". Twin alias to `…/notes.env/registry.md`: rc 0, one record. Cause: the truncated arm matches `*.env` on the prefix `notes.env`. Against the literal "complete filesystem paths, not citation-anchor prefixes" this is wrong. Under the lane's legacy `X.env:anchor` policy it is consistent, since `regressions.py:170` requires refusal of `synthetic.env:1`. The control set has no allowed-side canonical colon case, so the tension is untested.
- **CE-5 Adjacent, not colon-class (outside C3).** Raw `…/.aws/credentials` (synthetic) is allowed, opened and parsed (rc 0, one record). The denylist covers the directory form `credentials/`, not the file `credentials`.

No colon-class under-refusal was found. Every probed colon-denied canonical or raw target (`synthetic:fixture/.config/…`, `synthetic:fixture.env`, `synthetic.env:1` raw and via alias, `notes.env:v2/…` raw and via alias) was refused. Under landed it was never opened.

## Commands and exit codes (sandbox only; no network)

1. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive dd72641e… | tar -x -C /tmp/chousa-r27-falsify-FC3RegistryColonDeniedCan48`: rc 0.
2. `sha256sum tools/research-gate.sh`: `ca39d14d…992f84` (match).
3. `git show 64eec5d4…:tools/research-gate.sh` into `base/` (diff only, base not executed); `diff -u base tools/research-gate.sh`: rc 1 (expected differences).
4. `bash -n` on landed and every variant: rc 0.
5. `python3 harness/target_control.py --gate tools/research-gate.sh --probes`: rc 0; target `errors: []`.
6. `python3 harness/target_control.py --gate <sandbox>/tools/research-gate.<v>.sh --probes --open-log <sandbox>/logs/<v>.open.log > results/<v>.json` for landed-instr, m-canon, m-fd, m-both, m-canon-removed, m-full-only: rc 0 each.
7. `TMPDIR=<sandbox>/envtmp/.config python3 harness/target_control.py --gate <sandbox>/tools/research-gate.{landed-instr,m-both}.sh --probes …`: rc 0 each.
8. Discarded run: the first pass used a relative `--open-log`. The instrumented redirect failed inside the gate's temp cwd (rc 1 on allowed probes). That was a harness defect, not a gate defect. All variants were rerun with absolute paths, and only the rerun is reported.

Not run: full `--selftest`; the whole `round27-regressions.py`; the unmodified base gate; network; mounts; `/proc` or process inspection; strace; debugger.

## What holds

- A joint canonical plus fd regression fails the control for the intended reason (m-both).
- The landed gate never opens a refused colon-denied target (open log).
- The target fixture is a valid readable registry, so refused-versus-read is observable.
- No colon-class under-refusal found.

## Limits

- The harness reproduces L1's landed PASS only as a baseline. It is not a substitute for L1's 58/58 run.
- m-both is a targeted revert of the two canonical sites, not the base gate.
- Host `readlink` reports version 0.8.0 (`/usr/bin/readlink`). Gate canonicalization was not cross-checked against GNU readlink.
- [INFERENCE, not testable within bounds]: (a) if `readlink -f /proc/$$/fd/N` returns empty, the fd arm refuses with the denylist text (`:2402`). That is a mislabel, not a bypass. (b) The registry loader has no device check; the claims path has one at about `research-gate.sh:1202-1228`. Bind-mount aliases are untested. (c) Denylist matching is case-sensitive, so a case-insensitive filesystem would bypass `.CONFIG`-style names.
- [INFERENCE] The same masking plausibly applies to control `colon-denied-component` under a raw-only revert, because the canonical arm equals the raw path for non-symlinks. Not run; sibling scope.

## Author-lane advice (not an outside admission)

1. Restate the control's claim. It verifies "canonical-or-fd refuses a colon-denied alias", not the canonical arm. If isolation matters, the gate needs an arm-distinct observable, such as an arm-specific refusal token or an open trace. That is a production decision.
2. Pin the fixture root: assert the temp root is denylist-free before running, or build it under a fixed scratch path. Add an allowed alias sibling in the same root so environment vacuity fails loudly.
3. Decide the `X.env:anchor` policy for directory components in canonical paths. Add the allowed-side control either way, and reconcile the contract wording with `legacy-env-anchor-refusal`.
4. Note in the control that exit 2 and the message are gate-convention coupling, not contract text.
5. Route the `credentials`-file gap (CE-5) to the denylist owner; it is outside C3.

Tooling: no installs or updates. Tools used: bash 5.3.20, Python 3.14.8, sha256sum, readlink 0.8.0, and read-only git object reads on the lane (archive, show, ls-tree, cat-file, diff --stat). The only lane-tree write is this report.
Erratum (appended after writing; no other text changed): the fd-arm reference in Limits (a) is `research-gate.sh:2401` in the landed gate. `:2402` is the instrumented sandbox copy (`landed-instr`), which shifts later lines by one.

Addendum (appended after writing; landed-instr only, `results/extra-landed.json`, `logs/extra-landed.open.log`): raw `synthetic:fixture/.config/registry.md` (P8) exit 2 with the denylist refusal; raw `synthetic:fixture.env` (P9) exit 2 denylist; alias to `synthetic:fixture.env` (P10) exit 2 denylist. None of the three is in the open log, which lists only allowed files. Q3's last paragraph named these two raw targets before they were probed; they are now verified by P8-P10.
