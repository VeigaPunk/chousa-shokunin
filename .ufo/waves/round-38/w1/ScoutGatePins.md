# ScoutGatePins
## Verdict
Source audit complete: one production `ENV_BIN` dispatch, no bare production `env` or wrapper-bypassing `grep`; other capture/bootstrap/verifier tools remain unpinned. Axes: operability, calibration.
## Evidence
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `504c1d2a1257a9ac6e5d752dcaf3f0bb0a35d05f`.
- `sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` → `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d`.
- `/usr/bin/shfmt --version` → `v3.14.1`; `/usr/bin/shfmt -ln bash -tojson`, stdin opened read-only on the absolute gate path above → rc=0, stderr empty, JSON output 33734543 bytes. Initial filename-form attempt refused `--to-json can only be used with stdin`; corrected stdin invocation succeeded.
- Executed Python traversal of that JSON: visit `CallExpr.Args[0]`, exclude Bash `compgen -b` builtins, declared functions, slash-qualified/dynamic names; retain function ancestry. Observed `direct external bare sites=379 tools=32`; classifications `P=8 R=7 C=69 S=295`; literal `env` command heads=31, all S; `grep` command heads=74, all wrapper calls or the deliberate selftest replacement, not external bypasses.
- Separately parsed constant `bash -c` bodies and shell fixture heredocs through the same parser; inspected launcher argv, timeout-array dispatch and trap strings. Supplemental sites are listed below, not included in 379.
- `read xd://lsp` → `No such tool: xd://lsp. Mounted devices: ast_edit, debug.` No semantic server/device was available; findings use syntax-tree plus literal source/call-chain evidence, not LSP semantic proof.
- Seeds: not applicable; no counter, gate mode, selftest, build or formatter rewrite was executed. No installations/updates.
## Findings
1. **Inventory convention (high confidence).** Every line number below is in `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`. C=capture-channel, including subprocess verifier callees; P=pin/bootstrap/drift machinery outside capture; R=record-verification-only metadata or shared CLI help; S=selftest-only. C verifier helpers also serve ordinary record verification; P bootstrap also runs in capture children. Classes describe source reachability, not proof that every branch executes on the fixed fixture. Repeated `2949` means two invocations on that line.

| Bare tool | C | P | R | S |
|---|---|---|---|---|
| basename | — | — | — | 4288,5012,5226,7611 |
| bash | 3642 | — | — | 6778,6806,6881,7145,7693,8201,8217,8323,8339,8354,8383,8403,8422,8441,8456 |
| cat | 2094,2390,3942,3945 | — | 531 | 4247,4254,4261,4264,4267,4270,4274,4284,4289,4297,4309,4878,6161,6175,6208,6225,6240,6359,6465,6607,6619,6627,6635,6644,6653,6666,6675,6689,6706,6710,6740,6791,6819,6831,6909,6919,6928,6938,6947,6956,6973,6982,6991,7000,7009,7050,7087,7092,7104,7121,7229,7240,7251,7260,7269,7275,7305,7315,7393,7408,7425,7443,7464,7501,7681,7698,7719,7805,7821,7928,7936,7944,7951,7963,7971,7980,8190,8245,8269 |
| chmod | — | — | — | 6523,6528,6761,6799,7876,8173,8251,8275,8454 |
| cp | — | — | — | 4545,5897,6754,6789,6790 |
| cut | 2155,2314 | — | — | 5408,7480,7483,7485 |
| date | — | 327,328,329,330 | — | — |
| dirname | 3686 | 312 | — | — |
| env | — | — | — | 4323,4360,4390,4420,4450,4875,5383,5738,5772,6524,6579,6850,7027,7177,7200,7560,7881,8134,8152,8176,8202,8220,8253,8277,8297,8324,8338,8355,8388,8407,8427 |
| flock | 3839 | — | — | — |
| head | 1063,2155,2314 | — | — | 5911,5912,6348 |
| id | — | — | — | 6557 |
| ln | — | — | — | 5962,5976,5977,6302,6319,6335,6396,6445,6736,6751,6755,7340 |
| locale | — | — | — | 7151 |
| mkdir | 3939 | — | — | 4241,5909,5961,6005,6060,6301,6317,6333,6379,6395,6443,6464,6486,6493,6500,6506,6705,6723,6733,6759,6788,6908,7049,7304,7314,7337,7392,7874,8171,8239,8352,8420 |
| mktemp | 3991 | — | — | 4228,4231 |
| mv | — | — | — | 6439 |
| od | 1793,3853 | — | — | 7763 |
| paste | — | — | — | 6594 |
| python3 | — | — | — | 5399,6540,7734,7765 |
| readlink | 891,1640,2667,2671,2846 | 309 | 3163,3170,3395,3403 | — |
| realpath | 2669 | — | — | — |
| rm | 3996,4020 | — | — | 7680,8174,8199,8321,8381 |
| sed | 717,751,762,1007,1008,1010,1794,2127,2159,2319,3727,3929 | 4050 | — | 4342,4374,4404,4434,4464,4544,4884,5408,5419,5473,5475,5750,5790,5811,5825,5867,5874,5876,5899,6048,6290,6438,6535,6538,6551,6594,6602,6866,6888,6903,7044,7192,7222,7579,7728,7729,7743,7774,7775,7907,8145,8162,8190,8213,8218,8228,8266,8289,8309,8334,8348,8365,8399,8417,8437,8450,8465 |
| sha256sum | — | — | — | 5408,7480,7483,7485 |
| sleep | — | — | — | 7699,7714 |
| sort | — | 4125 | — | — |
| stat | 974,975,1678,1698 | — | 3173,3406 | 7679,7732,7753,7762 |
| tail | 3853 | — | — | 7763,8343 |
| tr | 751,771,783,1009,1032,1107,1142,1163,1182,1184,1245,1588,1793,2159,2221,2224,2234,2319,2445,2774,2949,2949,3004,3033,3048,3853 | — | — | 5396,5911,5912,6348,6530,7726,7757,7763,8037 |
| unshare | — | — | — | 6006,6019,7892 |
| wc | 976,1588 | — | — | 5396,6530,7726,7757 |

2. **Launcher/deferred-code supplement (high confidence).** Bare executable names passed to another program are not shell command heads, but remain external lookup surfaces. Include these in the named-limits audit:

| Surface | Class and exact lines |
|---|---|
| `bash` executable argv to pinned env | C:4003 |
| `bash` executable argv to bare env/unshare/optional timeout | S:4326,4363,4393,4423,4453,4877,5386,5740,5775,6006,6019,6526,6582,6852,7029,7179,7202,7562,7673,7704,7883,7892,8136,8154,8179,8202,8220,8256,8280,8299,8324,8338,8355,8388,8407,8427 |
| `timeout` array / `env` beneath it | S:`timeout` selected at 7669 and dispatched at 7671,7702; bare `env` target at 7671,7702 |
| EXIT trap `rm` | S:4230,4239 |
| Executed `bash -c` literals | S:`mount`6007,6020,7893; `stat`6008 twice; `env`6022,7894; `bash`6024,7896,8387,8406,8426 |
| Executed shell fixture heredocs | S:`rm`6795; `ln`6796; `flock`7684; `sleep`7690; `cat`8247,8271 |
| `/usr/bin/env bash` shebangs | P:1 if directly executable (ignored by `bash "$SELF"`); S:generated script string6760, heredocs6792,7122. `env` itself is absolute; its `bash` target is bare. |

3. **What each class witnesses (source-grounded potential, not reproduced attacks).** C launch sites witness interpreter-selection dependence (`bash`3642/4003); C fixture sites witness temp/fixture bytes and cleanup dependence (`mktemp`3991, `mkdir`3939, `cat`3942/3945, `rm`3996/4020); C normalizer witnesses baseline-byte dependence (`sed`3929). C shared verification tools witness parsing/matching/locator/source-identity/manifest dependence: `sed`/`tr`717–1245, `readlink`891/1640, `stat`1678/1698, `od`1793, `cat`2094/2390, `realpath`2669, `flock`3839. Diagnostic `head`/`cut`2155/2314 and nonempty-manifest `tail`/`od`/`tr`3853 are conditional branches, not assertions that the untouched canonical fixture executes them. Size fallback `stat`974/975 and `wc`976 is likewise conditional (caller1704).
4. **P/R/S boundaries (high confidence).** P witnesses SELF/root/clock setup dependence (`readlink`309, `dirname`312, `date`327–330) and drift-report field extraction/order (`sed`4050, `sort`4125); these are not reopened bare-`env` dispatches. R witnesses metadata pathname/opened-object/size/link checks (`readlink`3163/3170/3395/3403, `stat`3173/3406) or help delivery (`cat`531), not the canonical fixture's verification modes. S witnesses harness/tool/fixture dependence only; it is not a production C1 counterexample. `run_selftest` is confined to4225–8475 and selected at8555.
5. **No external grep bypass / no bare production timeout (high confidence).** `grep_pin_define`359 installs `grep() { "$GREP_BIN" "$@"; }`; init416/8534 precedes every real mode. None of the74 parsed `grep` heads is prefixed with `command`/`env` to bypass it; selftest7379 deliberately substitutes a return-2 function. Capture checks4005–4007 and drift scan4052 therefore use the wrapper. Pin probes call absolute `$to`379/487, selected only from `/usr/bin/timeout` or `/bin/timeout`377–378/485–486; absence uses candidate directly380/488. These are not remaining bare `timeout` sites. Hash invocations442/450 similarly use the absolute selection434; remaining bare `sha256sum` sites are S only.
6. **The r38 env pin has exactly one operational dispatch site (high confidence).** `ENV_BIN` is initialized473, assigned519, and invoked only4001 in `gate_canonical_capture`; callers are `run_pin`4131 and `run_drift`4206. `env_pin_init`8537 runs eagerly for every valid non-help mode, including each verifier subprocess; it probes candidates at487/488 via `env_pin_verify`507/515, but those are version probes, not another `$ENV_BIN` application. All31 literal bare `env` heads remain S; supplemental S env sites are7671/7702/6022/7894.
7. **Precise named interpreter limit (source fact + inference).** The observed chain is capture3988 → pinned env4001 with bare target argv `bash`4003 → `verify_all`3671 → section dispatch3759–3763 → shell-resolved `bash`3642. [INFERENCE]4003 is GNU env's executable/PATH lookup, not a Bash function lookup; an imported function named `bash` has its concrete shell-interposition witness at3642. This refines the wording at470–471 and `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round38/claims.md:130–133` without claiming a C1 predicate failure. The pin is narrower than shell/loader/utility hermeticity (same claims file134–146).
8. **Additional nonexternal lookup controls.** `command -v` is a Bash builtin, not itself an external invocation: C2668(realpath),3830(flock); S5398/6539/7733/7764(python3),6004(unshare),7669(timeout),7675(flock). Shell builtins and caller redefinition of internal functions remain outside this external-tool census.
## Limits
- Static syntax/call-chain audit only; no dynamic interposition, predicate score, selftest tally, or exploit reproduction is asserted. Source reachability includes conditionals; R help can also occur on capture error paths.
- No LSP device was mounted; no semantic references/definition results are claimed. No source, index, jj state, fleet file, or sibling report was changed; only this assigned report was written.
