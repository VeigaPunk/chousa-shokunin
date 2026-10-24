# CritNoexec
## Verdict
The inherited-noexec debt is reproduced; no tested in-body mitigation executes, but the frozen command needs an `env` prefix to reproduce literally from Bash.

## Evidence
Axes: **operability** (false success, absent/stale baseline) and **calibration** (exact invocation and observed bytes).
Fresh fixture namespace/seed: **38231**; no C1/C2 counter was run. Workspace: `/tmp/chousa-r38-CritNoexec-38231.2TnBaK`.
Commands were re-executed with PATH=/usr/bin:/bin, LC_ALL=C, HOME and TMPDIR equal to that workspace; no inherited SHELLOPTS/BASH_ENV except where explicitly injected.

```text
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master
504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f
git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show master:tools/research-gate.sh | sha256sum
37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  -
sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /usr/bin/bash
37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
c14c8f498f3be96f076ceb07d65dba584a86dca3c86b5dce65ed0f6cae73358d  /usr/bin/bash
/usr/bin/bash --version
GNU bash, version 5.3.20(1)-release (x86_64-pc-linux-gnu)
python3 /tmp/chousa-r38-CritNoexec-38231.2TnBaK/run-review.py
```
The last command ran all observations below and printed each exact argv, exit, stdout/stderr strings, and before/after file state (including SHA-256 for existing files).

Requested environment, absolute landed gate, exact requested target:
```text
/usr/bin/env SHELLOPTS=noexec /usr/bin/bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin /tmp/ne.txt
exit=0; stdout=""; stderr=""; /tmp/ne.txt absent before AND after
```
The same command targeting `/tmp/chousa-r38-CritNoexec-38231.2TnBaK/missing-baseline.txt` produced the same exit/streams/absence.
With `/tmp/chousa-r38-CritNoexec-38231.2TnBaK/stale-baseline.txt`, it instead left the existing 21 bytes unchanged: SHA-256 before=after=`61e86b55ae26e3272b5eb9f1e021b4226603b86febd14a54a0941a6fc77f3e4a` (`STALE_BASELINE_38231\n`), exit=0 and both streams empty.

In-body attempts, all fixtures under the absolute workspace above:
```text
/usr/bin/env SHELLOPTS=noexec /usr/bin/bash /tmp/chousa-r38-CritNoexec-38231.2TnBaK/early-check.sh /tmp/chousa-r38-CritNoexec-38231.2TnBaK/early-check-noexec.txt
/usr/bin/env SHELLOPTS=noexec /usr/bin/bash /tmp/chousa-r38-CritNoexec-38231.2TnBaK/reexec-guard.sh /tmp/chousa-r38-CritNoexec-38231.2TnBaK/reexec-guard-noexec.txt
/usr/bin/env SHELLOPTS=noexec /usr/bin/bash /tmp/chousa-r38-CritNoexec-38231.2TnBaK/disable-noexec.sh /tmp/chousa-r38-CritNoexec-38231.2TnBaK/disable-noexec-noexec.txt
/usr/bin/env SHELLOPTS=noexec /usr/bin/bash /tmp/chousa-r38-CritNoexec-38231.2TnBaK/reexec-payload.sh /tmp/chousa-r38-CritNoexec-38231.2TnBaK/reexec-payload-noexec.txt
EACH: exit=0; stdout=""; stderr=""; target absent before AND after
/usr/bin/bash -n /tmp/chousa-r38-CritNoexec-38231.2TnBaK/disable-noexec.sh /tmp/chousa-r38-CritNoexec-38231.2TnBaK/explicit-minus-n.txt
exit=0; stdout=""; stderr=""; target absent before AND after
```
`early-check.sh` begins with `if [[ ":$SHELLOPTS:" == *:noexec:* ]]; then printf 'NOEXEC_REFUSED\n' >&2; exit 2; fi`.
`reexec-guard.sh` tests the same condition and would print `REEXEC_ATTEMPTED`, then `exec /usr/bin/env -u SHELLOPTS /usr/bin/bash -c ...`.
`disable-noexec.sh` begins with `set +n`; `reexec-payload.sh` begins with the unconditional `exec ... bash -c ...` itself.
Positive controls without noexec: early-check printed `BODY_EXECUTED\n`; unconditional re-exec printed `REEXEC_CHILD\n`; both exited 0 and created their respective 9-byte baseline files.

Startup preflight attempt (PREFLIGHT_MARKER set to the absolute workspace's `preflight-noexec.marker`):
```text
/usr/bin/env SHELLOPTS=noexec BASH_ENV=/tmp/chousa-r38-CritNoexec-38231.2TnBaK/preflight.env /usr/bin/bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin /tmp/chousa-r38-CritNoexec-38231.2TnBaK/preflight-noexec-baseline.txt
exit=0; stdout=""; stderr=""; preflight marker AND baseline absent before/after
```
`preflight.env` starts with `printf 'BASH_ENV_ENTERED\n' >&2`, checks noexec and would exit 2, then writes a marker. Without noexec, invoking early-check.sh with this same BASH_ENV printed stdout=`BODY_EXECUTED\n`, stderr=`BASH_ENV_ENTERED\n`, exit=0, and created both marker and baseline.

Working pre-startup correction (not an in-body fix):
```text
/usr/bin/env SHELLOPTS=noexec /usr/bin/env -u SHELLOPTS /usr/bin/bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin /tmp/chousa-r38-CritNoexec-38231.2TnBaK/scrubbed-baseline.txt
exit=0; stderr=""; baseline absent -> present, 2989 bytes
stdout="GATE_PIN: ok path=/tmp/chousa-r38-CritNoexec-38231.2TnBaK/scrubbed-baseline.txt gate_sha256=37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d\n"
```
Literal assignment spelling from Bash (target kept inside the authorized workspace):
```text
/usr/bin/bash -c 'SHELLOPTS=noexec bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh --pin /tmp/chousa-r38-CritNoexec-38231.2TnBaK/literal-bash-baseline.txt'
exit=0; baseline absent -> present, 2989 bytes
stderr="/usr/bin/bash: line 1: SHELLOPTS: readonly variable\n"
stdout="GATE_PIN: ok path=/tmp/chousa-r38-CritNoexec-38231.2TnBaK/literal-bash-baseline.txt gate_sha256=37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d\n"
```
`readlink -f /usr/bin/sh` returned `/usr/bin/bash`; `type -a dash busybox zsh` found none. Merely spelling the launcher `sh` does not fix this host's readonly-assignment issue.
`/usr/bin/bash -c 'help set'` reports verbatim: `-n  Read commands but do not execute them.` and `noexec       same as -n`.

## Findings
1. **Operability counterexample: exit 0 proves no pin work.** The gate returns success without creating a missing baseline, emitting `GATE_PIN`, or replacing stale bytes. Grounding: requested-environment and stale-baseline observations above; `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh:4129-4162` normally captures, writes, then prints success. Noexec bypasses all three. A caller accepting exit 0 alone is unsafe; accepting mere pre-existing file presence is also unsafe.
2. **No safe in-body correction for this invocation.** The early check, `set +n`, conditional/unconditional re-exec, and BASH_ENV-file preflight all execute nothing under inherited noexec; positive controls show the fixtures work without it. Grounding: fixtures and executed commands above; gate's named comment at `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh:469-472`. These are unreachable execution-time repairs, not merely incorrectly positioned checks. Intentionally breaking Bash syntax is not a safe correction because it would break ordinary invocations too.
3. **Calibration defect in the literal reproduction, not in the exclusion.** `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/claims.md:140-144` says verbatim: `SHELLOPTS=noexec bash tools/research-gate.sh --pin P` “exits 0 with no baseline”. In a Bash caller that exact assignment instead reports the readonly error and executes a successful real pin. The semantic limit is reproduced only when SHELLOPTS is actually supplied in the child's environment. Smallest safe documentation correction: append an erratum giving `env SHELLOPTS=noexec bash ...` and “creates no baseline; leaves an existing baseline unchanged; stdout/stderr empty”. Frozen claim bytes must not be silently edited.
4. **Carried debt is the honest maximum for the unchanged explicit-Bash interface.** The demonstrated real repair is launch-side `env -u SHELLOPTS /usr/bin/bash ...`, before Bash imports its options, not code inside research-gate.sh. Grounding: scrub control above and the explicit boundary at claims.md:142-144. This does not require claiming a second tool already exists. Changing the canonical launch boundary would require separately specified caller/interface work; no identity/provenance claim should be made for an unshipped wrapper. C1 already excludes noexec; this review does not adjudicate C1/C2 or their frozen counters.

## Limits
No repo edits except this report; all fixtures and generated baselines are in the owned temporary directory. `/tmp/ne.txt` stayed absent. No tools installed, no counters/selftests/judges invoked, no alternate agent runtime, no spawns or background jobs. The finite mitigations and Bash's documented noexec semantics support the in-body conclusion; this is not an exhaustive survey of every possible external launcher, privileged mode, or hostile Bash binary. Canonical claim/tradeoff judgment remains with the Rust judge.
