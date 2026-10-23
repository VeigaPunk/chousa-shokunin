# ScoutGrepSites — command-word `grep` sites in `tools/research-gate.sh`

Gate sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` (matches the landed pin). Read 2026-10-23. No `egrep`, `fgrep`, `command grep`, `\grep`, or `sh -c`. The three `\beval\b` hits are a comment (line 871) and the strings `model eval` / `llm eval` (line 882), not `eval` commands. The three `bash -c` bodies (5867 `ns_probe`, 5880 `ns_run`, 7006 locale probe) contain no `grep`.

**Invocation sites: 68.** Every one is a bare `grep` (or `LC_ALL=C grep`) in this shell, so `grep()` at line 351 pins it: the body is `command "$GREP_BIN" "$@"` with `GREP_BIN=/usr/bin/grep`. One execution of line 6733 is not pinned: the selftest subshell at 7240 replaces the function (`grep() { return 2; }`). That stub does not exec, so it is not a PATH leak. No other site bypasses the wrapper.

## Proof

Shim `/tmp/hyaku/chousa-r35/w2/ScoutGrepSites/shim/bin/grep` (sha256 `f9f13cad8f129e433ca37827075a2294d86aa63f2770390bbca7b5cf0910e65c`) appends to `TRIPWIRE` then `exec /usr/bin/grep`. `BASH_ENV` `/tmp/hyaku/chousa-r35/w2/ScoutGrepSites/bashenv.sh` logs each bare `grep` with `type -t` and `declare -f` (`set -o functrace`).

Control, clean bash, no function: `env -i PATH="$SHIM:/usr/bin:/bin" TRIPWIRE=... bash --noprofile --norc -c 'printf hello | grep hello'` → trip lines=1 (`argv=hello`). The shim fires when PATH is actually used.

P1 — selftest, shim first on `PATH`, `TMPDIR` under the scratch dir:

```
env BASH_ENV=.../bashenv.sh PATH="$SHIM:$PATH" TRIPWIRE=.../proof/selftest/trip CHLOG=.../proof/selftest/ch \
  bash --noprofile --norc tools/research-gate.sh --selftest
```

rc=0. `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`. Trip file sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes). CHLOG sha256 `d71b48e8f5c74a4272d3dc07b9cb15b6d3daab09be1a6f2129cd4f72828a460c` (2870 lines, all `type=function`): `wrapper` 2868, `shadow` 2. The 1434 lines at source line 351 are bash re-entering DEBUG on the function definition with the caller's command; xtrace of the body is `command /usr/bin/grep`, not a second site. Call-site wrapper events (1434) match that echo count.

P2 — line 688 is not reached by selftest (only when `## Question` is a table and no prose). `verify` of `proof/qtable/rec.md` → rc=1, trip 0 bytes, CHLOG `site line=688 kind=wrapper ... cmd=grep -c .`

P3 — pin init, no `BASH_ENV`, `PS4='+L${LINENO}:' bash -x` on `verify` of a missing file: rc=2, trip 0, `command -v grep` count=0, trace has `/usr/bin/grep --version` then `GREP_BIN=/usr/bin/grep`. `--help` rc=0 and `--not-a-flag` rc=2 both exit before `grep_pin_init` (line 8039); trip 0 and CHLOG empty.

Process-substitution LINENO: bash -x reports the direct-matcher grep as `+++L1675:grep -a -z -b -o -P -- "$regex"` then `+++L351:command /usr/bin/grep` (claims xtrace, trip 0). The command text is line 1687, inside `tok_span_offsets_direct` which opens at 1675. The chunk matcher is the same: CHLOG line 1690, command `grep -a -z -b -o -P -- "$pattern"`, source line 1716.

## Site table

Hits are P1 call-site counts unless noted. Pin `wrapper` means `declare -f` contained `command "$GREP_BIN"` and the tripwire stayed empty.

| line | function | mode | shell context | pin | hits |
|-----:|----------|------|---------------|-----|-----:|
| 688 | section_nonempty_prose | verify / verify-all | `$( )`, pipeline, `\|\|` | wrapper | 1 (P2) |
| 718 | line_has_mark | verify / verify-all | simple, here-string | wrapper | 4 |
| 942 | verify_record | verify / verify-all | pipeline (`head \| grep`) | wrapper | 57 |
| 966 | verify_record | verify / verify-all | simple | wrapper | 57 |
| 971 | verify_record | verify / verify-all | simple, here-string | wrapper | 44 |
| 975 | verify_record | verify / verify-all | simple | wrapper | 57 |
| 1039 | verify_record | verify / verify-all | simple, here-string | wrapper | 53 |
| 1687 | tok_span_offsets_direct | verify-claims / verify-chain | process substitution, pipeline | wrapper | 162 |
| 1716 | tok_span_offsets_chunk | verify-claims / verify-chain | process substitution, pipeline | wrapper | 9 |
| 1762 | token_matcher_require | verify-claims / verify-chain | pipeline | wrapper | 121 |
| 2017 | verify_claims | verify-claims / verify-all | `$( )`, pipeline, `\|\|` | wrapper | 8 |
| 2176 | chain_nearest | verify-chain / verify-all | `$( )`, pipeline, `\|\|` | wrapper | 2 |
| 3144 | metadata_registry_check_source | verify-metadata | `$( )`, pipeline, `LC_ALL=C`, `\|\|` | wrapper | 13 |
| 3146 | metadata_registry_check_source | verify-metadata | `$( )`, pipeline, `LC_ALL=C`, `\|\|` | wrapper | 13 |
| 3507 | verify_all_section | verify-all | `$( )`, here-string, `\|\|` | wrapper | 96 |
| 3513 | verify_all_section | verify-all | `$( )`, here-string | wrapper | 96 |
| 3524 | verify_all_section | verify-all | `$( )`, here-string, `\|\|` | wrapper | 20 |
| 3525 | verify_all_section | verify-all | `$( )`, here-string, `\|\|` | wrapper | 18 |
| 3526 | verify_all_section | verify-all | `$( )`, here-string, `\|\|` | wrapper | 18 |
| 3527 | verify_all_section | verify-all | `$( )`, here-string, `\|\|` | wrapper | 22 |
| 3529 | verify_all_section | verify-all | `$( )`, here-string, `\|\|` | wrapper | 96 |
| 3567 | verify_all | verify-all | `$( )`, `\|\|` | wrapper | 22 |
| 3568 | verify_all | verify-all | `$( )`, `\|\|` | wrapper | 22 |
| 3867 | gate_canonical_capture | pin / drift | `$( )`, `\|\|` | wrapper | 7 |
| 3868 | gate_canonical_capture | pin / drift | `$( )`, `\|\|` | wrapper | 7 |
| 3869 | gate_canonical_capture | pin / drift | `$( )`, `\|\|` | wrapper | 7 |
| 3913 | gate_drift_scan | drift | `$( )`, pipeline, `\|\|` | wrapper | 12 |
| 4188 | tcase | selftest | `$( )`, here-string, `\|\|` | wrapper | 39 |
| 4225 | tclaims | selftest | `$( )`, here-string, `\|\|` | wrapper | 61 |
| 4226 | tclaims | selftest | `$( )`, here-string, `\|\|` | wrapper | 61 |
| 4255 | tchain | selftest | `$( )`, here-string, `\|\|` | wrapper | 14 |
| 4256 | tchain | selftest | `$( )`, here-string, `\|\|` | wrapper | 14 |
| 4285 | tsweeps | selftest | `$( )`, here-string, `\|\|` | wrapper | 12 |
| 4286 | tsweeps | selftest | `$( )`, here-string, `\|\|` | wrapper | 12 |
| 4315 | tintegrity | selftest | `$( )`, here-string, `\|\|` | wrapper | 7 |
| 4316 | tintegrity | selftest | `$( )`, here-string, `\|\|` | wrapper | 7 |
| 5248 | tall | selftest | `$( )`, here-string, `\|\|` | wrapper | 11 |
| 5249 | tall | selftest | `$( )`, here-string, `\|\|` | wrapper | 11 |
| 5265 | tall | selftest | simple, `\|\|` | wrapper | 2 |
| 5266 | tall | selftest | simple, `\|\|` | wrapper | 2 |
| 5267 | tall | selftest | simple, `\|\|` | wrapper | 2 |
| 5268 | tall | selftest | simple, `\|\|` | wrapper | 2 |
| 5602 | tpin | selftest | `$( )`, here-string, `\|\|` | wrapper | 1 |
| 5637 | tdrift | selftest | `$( )`, here-string, `\|\|` | wrapper | 7 |
| 5901 | tnscase | selftest | `$( )`, here-string, `\|\|` | wrapper | 2 |
| 5902 | tnscase | selftest | `$( )`, here-string, `\|\|` | wrapper | 2 |
| 6394 | r24_case | selftest | `$( )`, `\|\|` | wrapper | 3 |
| 6396 | r24_case | selftest | pipeline, `\|\|` | wrapper | 2 |
| 6444 | metadata_case | selftest | `$( )`, here-string, `\|\|` | wrapper | 29 |
| 6714 | metadata_asof_case | selftest | `$( )`, here-string, `\|\|` | wrapper | 14 |
| 6733 | metadata_asof_usage_accepts | selftest | `$( )`, here-string, `\|\|` | wrapper; 1/11 shadow | 11 |
| 6743 | metadata_asof_usage_case | selftest | `$( )`, here-string, `\|\|` | wrapper | 10 |
| 6892 | metadata_registry_case | selftest | `$( )`, here-string, `\|\|` | wrapper | 18 |
| 7042 | run_selftest | selftest | `$( )`, here-string, `\|\|` | wrapper | 1 |
| 7043 | run_selftest | selftest | `$( )`, here-string, `\|\|` | wrapper | 1 |
| 7065 | metadata_registry_finding_count_case | selftest | `$( )`, here-string, `\|\|` | wrapper | 3 |
| 7066 | metadata_registry_finding_count_case | selftest | `$( )`, here-string, `\|\|` | wrapper | 3 |
| 7070 | metadata_registry_finding_count_case | selftest | `$( )`, here-string, `\|\|` | wrapper | 1 |
| 7424 | tchain_audit | selftest | `$( )`, here-string, `\|\|` | wrapper | 4 |
| 7425 | tchain_audit | selftest | `$( )`, here-string, `\|\|` | wrapper | 4 |
| 7426 | tchain_audit | selftest | `$( )`, here-string, `\|\|` | wrapper | 4 |
| 7427 | tchain_audit | selftest | `$( )`, here-string, `\|\|` | wrapper | 4 |
| 7428 | tchain_audit | selftest | `$( )`, here-string, `\|\|` | wrapper | 4 |
| 7572 | run_selftest | selftest | simple | wrapper | 3 |
| 7590 | run_selftest | selftest | pipeline, `\|\|` | wrapper | 1 |
| 7591 | run_selftest | selftest | `$( )`, `\|\|` | wrapper | 1 |
| 7620 | run_selftest | selftest | `$( )`, `\|\|` | wrapper | 1 |
| 7621 | run_selftest | selftest | `$( )`, `\|\|` | wrapper | 1 |

Selftest helpers above are nested inside `run_selftest`. `line_has_mark` runs from `check_pointer` (verify_record source and claim rows). `verify-all` reaches the verify/claims/chain/sweeps/integrity functions by re-invoking `bash "$SELF"`, which calls `grep_pin_init` again in the child; those children were under the same shim and wrote no tripwire bytes.

## Bystanders (not in the 68)

| line | what | pin |
|-----:|------|-----|
| 351 | `grep()` definition. Body `command "$GREP_BIN" "$@"` is the pin sink (absolute). | pin-sink |
| 361 | `grep_pin_verify`: `"$cand" --version`. xtrace: `/usr/bin/grep --version`. | absolute probe |
| 364, 381, 393, 1763 | strings containing `GNU grep` / the refusal text | bystander |
| 384 | candidate list `/usr/bin/grep /bin/grep`, not executed as a command word | bystander |
| 388 | `command -v grep` fallback. Not reached when `/usr/bin/grep` verifies (P3, count 0). | lookup, not an invocation |
| 5867, 5880, 7006 | `bash -c` scripts with no `grep`. 5880 `exec`s `bash "$NS_SELF"`, which re-pins. | bystander |
| 7240 | subshell `( grep() { return 2; }; metadata_asof_usage_accepts ... )`. Not an invocation. The invocation is 6733, and for this call `kind=shadow` (also echoed at LINENO 7240). Tripwire stayed empty. | shadow of the wrapper |

Finding: line 7240 is the only wrapper bypass. It is a selftest double that makes line 6733 return 2 without exec. It does not resolve `grep` through PATH.

## Limits

Selftest did not execute line 688; P2 did. Bash attributes process-substitution greps to the function's opening line (1675, 1690); the command text identifies 1687 and 1716. `command -v grep` was not executed on this host because `/usr/bin/grep` reports GNU grep. Logs: `/tmp/hyaku/chousa-r35/w2/ScoutGrepSites/proof/`.
