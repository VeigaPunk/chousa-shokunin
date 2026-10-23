# ScoutSkillTally — SKILL.md self-test tallies vs commit 707da818

Read-only. Clone `/fast/scratch/hyaku/chousa-r34-a2/w2/ScoutSkillTally/repo` at `707da8184a0fc4d10ab3f17271556cdf364f0af5` (2026-10-23). Gate blob `tools/research-gate.sh` sha256 `a6307edf687ac0fb1b0b08bf7f0518b3fbc310fa9924b970aa3654612562995b` (prefix `a6307edf687ac0fb`). Lane worktree HEAD at inspection was `fe3db76c` and was not scored. No installs.

## Verdict

Case-range strings in the gates table match the 256 numbered cases the committed gate prints. The round-34 counter rows match the committed receipts they name. One tally string does not: every current self-test cell writes `PASS (256 cases)` and the gate prints `PASS (256 cases, 0 skipped)`.

## Selftest (re-run)

Command (exit 0, wall 48.43 s, `TMPDIR` under the scratch dir):

`timeout 1800 bash tools/research-gate.sh --selftest`

Stdout sha256 `5311643cc95e6358a9fd513ec8ba67b944617e7d7da2f8df1c4d33d1f0c75c12` (258 lines, stderr empty). Byte-identical to committed `.ufo/waves/round-34/measure-a2/selftest-a2.log` and `measure-a2/battery/selftest.log`. Copy: `.ufo/waves/round-34/w2a2/ScoutSkillTally/selftest.out`.

Last lines:

```
ok-case  252 claims-longspan              exit=1
ok-case  253 claims-longspan-line         exit=1
ok-case  254 claims-deadzone              exit=1
ok-case  255 claims-deadzone-line         exit=1
ok-case  256 claims-deadzone-edge         exit=1
RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)
```

256 unique numbers, 1..256, zero skips, zero FAIL lines. Dead-zone cases are 254–256. Long-span cases are 252–253.

## Case ranges (all match)

Mapped from `ok-case` lines (artifact `case-map.txt`, sha256 `70ed8572d0a8923d2925e744a83ae8f0ff72c5384c57cfa7cf5f85829b714a3f`).

| SKILL.md string | Produced names | Match |
|---|---|---|
| claims 21–30 and 41–42 (`:78`) | 21–28 `claims-*`, 29–30 `setup-claims-*`; 41–42 `claims-boundary-*` | yes |
| chain 31–40 and 43–44 (`:79`) | 31–38 `chain-*`, 39–40 `setup-chain-*`; 43–44 `chain-*-boundary` | yes |
| sweeps 45–54 (`:80`) | 45–52 `sweeps-*`, 53–54 `setup-sweeps-*` | yes |
| integrity 65–73 (`:81`) | 65–71 `integrity-*`, 72–73 `setup-integrity-*` | yes |
| verify-all 55–64 and 74 (`:82`) | `tall` → `verify-all` (`research-gate.sh:5158`); 55–64 fixture names; 74 `all-dangling.md` (`:5502`) | yes |
| `--json` 134–136 (`:82`) | `json-unterminated-manifest`, `json-nul-terminated-manifest`, `json-unreadable-manifest` | yes |
| r32 manifest lock 233–234 (`:82`) | `c1lk-holder-blocks-append`, `c1lk-second-append` | yes |
| metadata 137–208 and 210–215 (`:83`) | 137–208 and 210–215 are `metadata-*` | yes |
| 209 is a claims-surface control (`:83`) | 209 `claims-registry-colon-deny`, issued by `tclaims` (`research-gate.sh:7130`) | yes |
| pin/drift 75–85 (`:84`) | 75 `pin-clean`, 76–81 `drift-*`, 82–85 `setup-pin*` / `setup-drift*` | yes |
| r31 line 216–219, pin 220–228 (`:78`) | `c1-pass-bound` … `c1-pass-no-line`; `claims-sha-absent` … `claims-sha-crlf` | yes |
| r32 exempt 229–232 (`:79`); gap 235–241 (`:78`) | `chain-exempt-*`; `claims-r2-*` plus `r2-hash-fault-shim` | yes |
| r33 top 242–248, post 249–251 (`:78`) | `r33-top-*`; `r33-post-literals/nul-dup/escapes` | yes |
| r34 long 252–253, dead-zone 254–256 (`:78`) | `claims-longspan`, `claims-longspan-line`; three `claims-deadzone*` | yes |

## String that does not match

`PASS (256 cases)` (SKILL.md gates self-test cells, 9 occurrences, lines 77–84; historical parenthetical line 92: "round 34: they now read `PASS (256 cases)`").

Produced and committed logs: `RESEARCH_GATE_SELFTEST: PASS (256 cases, 0 skipped)`.

Cause, observed in the committed script (`research-gate.sh:5787` sets `SKIPPED=0`; `:7900`):

`printf 'RESEARCH_GATE_SELFTEST: PASS (%d cases%s)\n' "$cases" "${SKIPPED:+, $SKIPPED skipped}"`

`0` is non-empty, so the suffix is always printed when nothing was skipped. The count 256 is right; the banner text in SKILL.md drops `, 0 skipped`. SKILL.md contains zero copies of `PASS (256 cases, 0 skipped)`. Round-25's historical line 94 still records the suffix (`PASS (161 cases, 0 skipped)`).

## Related committed comment (not a SKILL cell)

`research-gate.sh:7824` says C1 cases 252–254; `:7857` says C2 cases 255–257. The run numbers those five cases 252–256. The comments overshoot by one and would imply 257 cases. SKILL.md:78 has the numbers the run prints.

## Counter rows

C1, SKILL.md:89. Committed receipts:

- before, gate `43a1af35ca66…4346`: `LONGSPAN_MATCH=25/42` seed 3493, `gate_timed_out=false`, elapsed 234.924 s (`controls/L1-base-v3/base-v3-C-s3493.json`); `0/42` seeds 3491 and 3492, `gate_timed_out=true`, elapsed 1501.449 s and 1501.775 s. Matches "25/42 (`LC_ALL=C`), 0/42 by the 1500 s bound".
- landed `772a1d8e…3e58`: `LONGSPAN_MATCH=42/42`, `predicate_holds=true`, seeds 3601, 3602, 3603 (`measure/c1v3-s3601.json`, `c1v3-s3602.json`, `c1v3-s3603-utf8.json`). The `×3` matches that trio.

Not a contradiction: three more committed receipts on the same gate also print `42/42` (seeds 4211, 5177, 6301, `.ufo/waves/round-34/w2/R34RerunC1v3/`). `×3` does not enumerate them. `R34ReviewPatchC.md` names seeds 912345678 and 912345679 at 42/42; those receipt blobs are not in the commit (`git ls-tree` has no `912345678`).

C2, SKILL.md:90. Only six `DEADZONE_MATCH` receipts in the commit, all counter sha256 `8c0def4d…2173`:

- before, gate `772a1d8e…3e58`: `21/37`, `predicate_holds=false`, seeds 5011 and 5023 (`measure-a2/c2-before-s5011.json`, `c2-before-s5023.json`).
- landed `a6307edf…995b`: `37/37`, `predicate_holds=true`, seeds 5011, 5023, 5033, 5047 (`measure-a2/c2-after-s*.json`).

No committed C2 run below 37 other than the two before receipts. The `×4` and the before `21/37` match.

Verdict-map `exit 0` is the counter process, not `gate_rc`. Both counters `return 0 if holds else 1` (`c1-count-v3.py` just above `sys.exit(main())`; `c2-count.py` the same). Receipts with `predicate_holds=true` also store `gate_rc=1` (the gate's DRIFT). Counters were not re-executed here. [INFERENCE] a true predicate implies counter exit 0; that exit code is not stored in the receipt.

## Limits

Did not re-run `c1-count-v3.py` or `c2-count.py`. Case identity is the selftest's own `ok-case` names plus the `tall` / `tclaims` call sites cited above, not a second semantic pass over each fixture. Network: none.
