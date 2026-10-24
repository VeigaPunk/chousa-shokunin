# W2LabBashFn

## Verdict
High confidence: the exported `bash` function sees only five section shell-outs at line 3642; the PATH `bash` shim sees those five plus the capture invocation at lines 4003–4004, consistent with Erratum 6's correction.

## Evidence
- Axes: **operability** (executed, exact argv reachability); **calibration** (distinguishing capture from its section children).
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `8e93bc916527b3c21f0f702967fa65c3b4c31699`.
- `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` → `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`. Both probe modes separately recorded the identical pre-run and post-run hash.
- One paired probe, namespace seed **38473** (not randomized): `/tmp/chousa-r38-w2-bashfn-s38473.0sinNo/probe.py`. The two commands below were executed concurrently, not inferred from wave-1 reports.
- Harness invokes `/usr/bin/bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin <mode>/baseline.txt` with a minimal environment: `PATH=/usr/bin:/bin`, `LC_ALL=C`, and HOME/TMPDIR/PROBE_LOG beneath the probe directory. No BASH_ENV, ENV, SHELLOPTS, BASHOPTS, CHOUSA_* or RESEARCH_GATE_* is inherited.
- Logger appends NUL-delimited `BASHPID, PPID, PWD, BASH_SOURCE[0], BASH_SOURCE[1], BASH_LINENO[0], argc, argv...` to an absolute file; it emits nothing to the captured streams.
- Function variant sets `BASH_FUNC_bash%%='() { <logger>; /usr/bin/bash "$@"; }'`. PATH variant has no exported function and prepends a shim with absolute `#!/usr/bin/bash`, `<logger>`, then `exec /usr/bin/bash "$@"`.

Executed commands and observed output:
```text
python3 /tmp/chousa-r38-w2-bashfn-s38473.0sinNo/probe.py function
  rc=0; stdout="GATE_PIN: ok path=/tmp/chousa-r38-w2-bashfn-s38473.0sinNo/function/baseline.txt gate_sha256=37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d"
  stderr=""; baseline_exists=true; hit_count=5; unavailable_lines=[]
  all five hits: source="environment", caller="/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh", caller_line="3642"
python3 /tmp/chousa-r38-w2-bashfn-s38473.0sinNo/probe.py path
  rc=0; stdout="GATE_PIN: ok path=/tmp/chousa-r38-w2-bashfn-s38473.0sinNo/path/baseline.txt gate_sha256=37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d"
  stderr=""; baseline_exists=true; hit_count=6; unavailable_lines=[]
  all six hits: source="/tmp/chousa-r38-w2-bashfn-s38473.0sinNo/path/bin/bash"
```
Both baselines contain `RESEARCH_GATE: DRIFT (sections=5 run=5 absent=0 drift-sections=1 findings=1 drift=1)`; integrity is `refs=4 resolved=3 unresolved=1`. Neither contains `VERIFY_ALL_SECTION_UNAVAILABLE`.

Exact observed argv sets (arguments **excluding** the function/shim name, in encounter order; every listed array occurs once):
```json
["/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh","verify","record.md","--root","."]
["/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh","verify-claims","claims.jsonl","--root","."]
["/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh","verify-chain","record.md","--root","."]
["/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh","verify-sweeps","record.md","--root","."]
["/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh","verify-integrity","record.md","--root","."]
```
These are the **entire function set** and the PATH set's **last five**. The PATH set starts with this additional array, absent from the function set:
```json
["/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh","verify-all","record.md","--claims","claims.jsonl","--json","manifest.jsonl","--root","."]
```
Raw logs/results: `/tmp/chousa-r38-w2-bashfn-s38473.0sinNo/{function,path}/{argv.nul,result.json}`. Function cwd was `.../function/chousa-gate-pin.ng04K9`; PATH cwd was `.../path/chousa-gate-pin.M9SN8D`.

## Findings
1. **Observed, high confidence — function bypass at the capture boundary.** No `verify-all` hit, despite five later hits proving the function was actually imported. `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh:4001–4004` supplies `bash` as an argument to the pinned external env, not as a shell command name. With this probe's `/usr/bin:/bin` PATH, the capture uses the bash binary, not the exported function. The five function hits directly report caller line **3642**, inside `verify_all_section`; callers at **3759–3763** supply the five modes.
2. **Observed + source mapping, high confidence — PATH reaches both levels.** The shim's first argv matches the capture at **4003–4004** exactly. The other five match **3642**, with mode selection at **3759–3763**. Thus PATH affects the env-launched capture **and** the later bare-name section calls. Neither variant sees the initial `--pin`: the harness deliberately starts that process using the absolute `/usr/bin/bash` path. The shim's own absolute interpreter and forwarding command add no shim hits.
3. **Observed wording comparison, high confidence — Erratum 6 is the correct distinction.** `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/claims.md:223–226` says the original bash-named limit misidentified the vector and identifies **PATH resolution inside env** as the live capture witness. That matches the extra PATH `verify-all` event. Its parenthetical separately mentions a **suppressing bash function** producing `VERIFY_ALL_SECTION_UNAVAILABLE`; our function logs place that vector at the section shell-outs, not the capture launcher. We did not execute suppression or poisoning. The frozen **:130–133** sentence literally claiming an exported function shadows the capture's bare bash call is not what occurs; Erratum 6 corrects it. Source comments at `research-gate.sh:470–471` and **:8378–8379** retain that older call-site description.

## Limits
- This is the assigned passive argv probe only: no counters, new receipts, suppression, baseline poisoning, drift run, or gate selftest. Seed 38473 is a namespace label, not independent statistical replication.
- LSP is unavailable: `read xd://lsp` returned `No such tool: xd://lsp` (mounted devices: ast_edit, debug); no LSP status/request could be made. Source discovery used literal grep; call-site proof comes from the runtime function caller metadata and the displayed source, not a claimed semantic reference search.
- No tools installed or upgraded. No tracked source, git index, jj state, or fleet-root files were changed; only this report and files under the newly created `/tmp` directory were written. Probe modes create their output directories once; repeat in a fresh temporary root.
