# ScribeKnowledgeC1

## Verdict
C1 re-derived independently at fresh seed 38251 (landed 7/7, base 2/7); all four checked committed receipts verify; knowledge-entry draft included, but S072 has no committed SOURCES row yet.

## Evidence

Read-only lane checks from `/home/vgpnk/Projects/shokunin/chousa-shokunin`:

```text
$ git rev-parse master
504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f
$ sha256sum tools/research-gate.sh .ufo/waves/round-37/controls/base-gate-r37.sh corpus/evidence/round38/{c1-count.py,c2-count.py,verify-receipts.py,expectations.jsonl,claims.md}
37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  tools/research-gate.sh
a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  .ufo/waves/round-37/controls/base-gate-r37.sh
da1d915b51801fd6d25ebf857318afc87c08c4876dd25fe4055fdede1ede3f74  corpus/evidence/round38/c1-count.py
bc325cf4785f62ef3eeca3ea2d8a61094822a0c4345f07ae314c408cf6507818  corpus/evidence/round38/c2-count.py
756f186c3487461b9c29de5ebbb4b91392706ecc4b5ff8f3a83d482fcaf27605  corpus/evidence/round38/verify-receipts.py
7cd5d824b4f927329927679f53c747edff0b6c405ff98d1701619519b2eaebc9  corpus/evidence/round38/expectations.jsonl
5950f87e690ff1fb9b232e238d231d0c12f3920591a5d02f2c89741cda107687  corpus/evidence/round38/claims.md
```

Fresh-seed re-derivation I executed (seed **38251**; `C1_TMP=/tmp/r38-scribe-c1.B3Bc6Q`, created before the run; receipts under `/tmp`, nothing written to the lane):

```text
$ C1_TMP=/tmp/r38-scribe-c1.B3Bc6Q python3 corpus/evidence/round38/c1-count.py --gate tools/research-gate.sh --seed 38251 --receipt /tmp/r38-scribe-c1.B3Bc6Q/c1-verify-s38251.json
PASS hold-plain / hold-fn-benign / env-fn-echo-scrub / env-fn-root-move / env-fn-suppress / env-override-missing / env-override-fake
ENV_PIN_CAPTURE_MATCH=7/7   (exit 0; matched=7, predicate_holds=True, gate_sha256_pre==post=37e2b996…d27d,
counter_sha256=da1d915b…3f74, expect_sha256=7cd5d824…ebc9, receipt_sha256=f8c942fd…4630)
$ same counter --gate .ufo/waves/round-37/controls/base-gate-r37.sh --seed 38251
FAIL env-fn-echo-scrub (echo_lines=1, drift_line='GATE_DRIFT: -GATE_GREP'); FAIL env-fn-root-move (foreign-root drift);
FAIL env-fn-suppress (pin_rc=2, pin_file=False); FAIL env-override-missing / env-override-fake (pin_rc=0, pin_file=True)
ENV_PIN_CAPTURE_MATCH=2/7   (exit 1)
```

Committed-receipt verification I re-executed (`corpus/evidence/round38/verify-receipts.py`, receipts in `corpus/evidence/round38/receipts/`):

```text
c1-base-s38001     VERIFY: ok receipt=c1-base-s38001.json gate=base-gate-r37.sh counter=c1-count.py
c1-after-s38001    VERIFY: ok receipt=c1-after-s38001.json gate=research-gate.sh counter=c1-count.py
c1-after-s38011    VERIFY: ok receipt=c1-after-s38011.json gate=research-gate.sh counter=c1-count.py
c2-after-s38101    VERIFY: ok receipt=c2-after-s38101.json gate=research-gate.sh counter=c2-count.py
```

S072 source bytes (`/usr/share/info/bash.info.gz`, sha256 `cde1a3366897684b0a86fe553687e31d070b7839b19ca98186ffc6e0e105588f`):

```text
$ zcat /usr/share/info/bash.info.gz | awk 'NR>=1461 && NR<=1464'
1461: enabled).  Functions may be exported so that child shell processes
1462: (those created when executing a separate shell invocation) automatically
1463: have them defined with the ‘-f’ option to the ‘export’ builtin (*note
1464: Bourne Shell Builtins::).  The ‘-f’ option to the ‘unset’ builtin (*note
$ grep -c '| S072 ' corpus/SOURCES.md   ->   0
```

## Draft: `corpus/knowledge/env-pin-capture-r38.md`

```markdown
# Pinned env — a caller function named `env` cannot move a pin baseline

Lane: chousa. Round 38 (C1, operability — the lowest scored axis, 3/10). Surface: `tools/research-gate.sh` (`gate_canonical_capture`, the `--pin` / `--drift` contract), `corpus/evidence/round38/c1-count.py`.

source: S072 (GNU Bash manual, `bash(1)` — `/usr/share/info/bash.info.gz`, Node `Shell Functions` (3.3), decompressed lines 1461–1464: “Functions may be exported so that child shell processes … automatically have them defined with the ‘-f’ option to the ‘export’ builtin”, quote at 1461–1464; bash 5.3.020-1; file SHA-256 `cde1a336…588f`; row opened this round, integration pending); frozen design `corpus/evidence/round38/claims.md` §C1 (claim, P1, kill rule, before-measurement); receipts `corpus/evidence/round38/receipts/c1-{base-s38001,after-s38001,after-s38011}.json`; counter `corpus/evidence/round38/c1-count.py`.
verified-at: 2026-10-24 (landed gate SHA-256 `37e2b996…d27d`; `ENV_PIN_CAPTURE_MATCH=7/7` on seeds 38001, 38011, and wave seeds 38211, 38231)
recheck: on-release (`python3 corpus/evidence/round38/c1-count.py --gate tools/research-gate.sh --seed <n>` → `7/7` with `predicate_holds=true`; any run below 7/7 against the landed gate kills the claim)

## What changed

Round 37 closed the `BASH_ENV` startup-file channel, but the capture child still spawned through a BARE `env`, and bash exports shell functions into the environment of every child as `BASH_FUNC_<name>%%`, which a child bash imports before its body runs. A caller-exported function named `env` therefore received the capture call itself and could (1) re-add `CHOUSA_GREP_PIN_ECHO`: the baseline embeds a `GATE_GREP:` line and a later plain `--drift` reports phantom `-GATE_GREP`; (2) re-add `CHOUSA_ROOT`: the capture runs against a foreign root; (3) suppress the capture (`() { :; }`): `--pin` exits 2 and no baseline exists. The capture child now runs through ONE pinned absolute `env` (`ENV_BIN`), resolved with no PATH consultation (default `/usr/bin/env` then `/bin/env`, each probed for a `GNU coreutils` `--version`) and overridable only via `RESEARCH_GATE_ENV`, which must be an absolute path to a regular executable reporting GNU coreutils; anything else is refused (exit 2, `ENV_PROVENANCE`) before any record is read. An absolute-path call is not subject to function lookup, so the exported function never receives the capture call.

## The seven scenarios (counter `c1-count.py`)

`hold-plain` and `hold-fn-benign` pin the capture contract and a benign forwarding `env` function (the gate must be unharmed by it); `env-fn-echo-scrub`, `env-fn-root-move` and `env-fn-suppress` plant the three attacks through `BASH_FUNC_env%%`; `env-override-missing` and `env-override-fake` demand exit 2 `ENV_PROVENANCE` and no baseline. Every attack cell asserts pin_rc=0, the baseline present, zero `GATE_GREP: ` lines, and a later plain drift reporting `GATE_DRIFT: none`. Base gate `a7d3922c…` scores 2/7 (the two holds pass; the five separation cells fail exactly as the vulnerability predicts); landed gate `37e2b996…` scores 7/7 on every committed and wave receipt.

## Frozen observable

2/7 → 7/7. Base: `receipts/c1-base-s38001.json` (`matched` 2, `predicate_holds` false). Landed: `receipts/c1-after-s38001.json` and `receipts/c1-after-s38011.json` (`matched` 7, `predicate_holds` true, `gate_sha256_pre` == `gate_sha256_post` == `37e2b996…`); wave re-derivation on fresh seeds 38211/38231 scored 7/7 (`.ufo/waves/round-38/w1/ExecC1Rederive.md`). A do-nothing lane commit cannot reach 7/7: the base gate is the exact pre-round bytes and runs the same seven scenarios.

## Named limits (verbatim from claims.md §Limits, frozen)

- C1 pins the capture's `env` invocation only. A caller-exported function named `bash` can still shadow the capture's bare `bash` call (the planned-list parent-function class); the grandchild `bash` lookup is the next witness, carried debt.
- C1's env pin does not scrub the loader environment of the `env` child — the Erratum-6 class on a second binary: an unprivileged `LD_PRELOAD` active for `/usr/bin/env` could strip the `-u` flags before they apply. The claim is function-export/PATH independence of the capture's env invocation, not loader hermeticity; the `env -u LD_PRELOAD …` scrub is carried debt with Erratum 6's fix direction.
- C1 does not cover `SHELLOPTS=noexec` (demonstrated again on the landed gate: `SHELLOPTS=noexec bash tools/research-gate.sh --pin P` exits 0 with no baseline): bash applies `-n` before the gate body executes, so no in-body fix exists — a pre-startup boundary would be a separately specified tool, carried debt per the round-37 residual.
- C1's provenance is self-reported like the grep pin: a binary that lies about `--version` is out of this check's reach.
```

## Findings

1. **C1 holds on a fresh seed I executed myself.** Seed 38251: landed `37e2b996…` 7/7, base `a7d3922c…` 2/7 same seed; the five base failures reproduce the frozen separation exactly (echo → 1 `GATE_GREP:` line + `-GATE_GREP`; root → foreign-root drift; suppress → pin_rc 2, no file; both overrides ignored → pin_rc 0). Pointers: `corpus/evidence/round38/claims.md:25-70`; `/tmp/r38-scribe-c1.B3Bc6Q/c1-{verify,base}-s38251.json`.
2. **Committed receipts bind and verify.** All three committed C1 receipts plus `c2-after-s38101` return `VERIFY: ok`; the C1 after-receipts carry pre==post gate `37e2b996…`, `counter_sha256=da1d915b…`, `expect_sha256=7cd5d824…`, and a self-consistent `receipt_sha256`. Pointer: `corpus/evidence/round38/receipts/`.
3. **The mechanism is observed, not inferred.** `env_pin_init` consults no PATH (only `/usr/bin/env`, `/bin/env`), `env_pin_verify` requires a `GNU coreutils` `--version` line, `RESEARCH_GATE_ENV` is validated (absolute, regular, executable, GNU-reporting) with every failure going through `env_pin_refuse` → exit 2 `ENV_PROVENANCE`, and the capture subshell invokes `"$ENV_BIN" -u … bash "$SELF" …`. An absolute-path command is not a function-lookup candidate, which flips all three `BASH_FUNC_env%%` cells. Pointers: `tools/research-gate.sh:466-521,3988-4015`; `corpus/evidence/round38/c1-count.py:95-160`.
4. **BLOCKER for integration: S072 is not a committed row.** `grep -c '| S072 ' corpus/SOURCES.md` → `0`; the table ends at S071. The drafted entry cites S072, so `verify-metadata --registry` would fail closed unless the S072 row lands in the same integration (ScoutSources owns its text). Pointer: `corpus/SOURCES.md:81`.
5. **The dispatch-stated S072 anchor is off by one.** The spec prompt says “decompressed lines 1460-1463”; the observed exported-functions sentence spans **1461–1464** (`zcat | awk 'NR>=1461 && NR<=1464'`). The row and entry should use the observed span; 1460 carries the tail of the preceding `extdebug` sentence.
6. **The benign-function hold is load-bearing, not padding.** `hold-fn-benign` (`() { /usr/bin/env "$@"; }`) passes on both gates, so 7/7 is not bought by rejecting every exported function — only the interposing shapes flip. Pointer: `corpus/evidence/round38/expectations.jsonl:2`; scenarios 2–5 of `c1-base-s38001.json` / `c1-after-s38001.json`.
7. **Wave re-derivation agrees.** ExecC1Rederive reports base 2/7 and landed 7/7 on seeds 38211 and 38231, both after-receipts `VERIFY: ok`. Pointer: `.ufo/waves/round-38/w1/ExecC1Rederive.md` (wave seeds, not mine).
8. **No-harm battery has no execution evidence this wave.** `ExecNoHarm.md` explicitly did not run `--selftest`, `verify-claims`, `verify-chain`, broken `verify-all`, or the archives check; its claim is fingerprint-only. The claims' `PASS (272 cases, 0 skipped)` selftest is contract-only in this report.

## Limits

- I drafted the entry only; I did not write `corpus/knowledge/env-pin-capture-r38.md`, did not touch SOURCES.md, and ran no mutating git/jj command.
- The entry's wave-seed sentence and S072 provenance depend on wave artifacts (ExecC1Rederive report; uncommitted S072 row), not committed lane bytes — the only two non-listed sources, both required by the assignment.
- I did not run the gate selftest, the C2 predicate, or the no-harm battery; C2 appears only as the one verified `c2-after-s38101` receipt.
- My fresh-seed receipt lives in `/tmp/r38-scribe-c1.B3Bc6Q/`; it is not committed and should not be cited as lane evidence after this session.
- No tools were installed or upgraded; no pacman transaction attempted.
