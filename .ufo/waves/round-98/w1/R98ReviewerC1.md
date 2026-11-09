# R98ReviewerC1 — C1 correctness review (tools/search-rerun.py at F)

Seat: R98ReviewerC1. Tree: clone at F `aac826848dda5029ba459568b29d9a92176dc2b6`, base `98b8177c1e8b39cdf1167928e4f5d609f6fa81b6`.
Scope: the C1 change only (selftest cases r17–r34, guard canary g00, EQUIVALENT e1–e3, oracles incl. hash-of-self, battery BASE reads). C2 not reviewed (out of assigned slice).

## Methodology

- Read the diff (`tools/search-rerun.py`, 170 lines) and `corpus/evidence/round98/selftest-controls-r98.py` (314 lines) in full, plus the R97 probe (37 mutants) and the R97/R96 battery literals at BASE.
- Ran the real `--selftest` (PASS 67/67) and `selftest-controls-r98.py --no-regression` (PASS, exit 0) against the scratch clone.
- Probed every r17–r34 case by calling the real functions directly, attacked the canary with 5 hand mutants, proved r28's zero-git claim with a `subprocess.run` spy + audit hook + strace, proved e3 equivalence exhaustively + fuzz, audited the hash-of-self oracle, verified all BASE reads byte-for-byte, and re-ran the K3 harm leg independently.

## Findings by severity

### S1 (severity: low; observation, not a fired verdict) — canary docstring overclaims exception coverage

`tools/search-rerun.py:676-681` says the canary fails "a guard or summary that … lets an exception escape, …". Mechanically, `_guard_canary`'s failing set raises `ValueError` inside a case and `RuntimeError` only in set-up. Narrowing the inner per-case guard from `except Exception` to `except ValueError` therefore passes the canary AND the full selftest:

- Command: `python3 -B attack/canary_attacks.py` → `=== inner-valueerror-only: applies 1 times` → `rc=0 last='SEARCH_RERUN_SELFTEST: PASS cases=67/67'`.
- Receipt: `.ufo/waves/round-98/w1/R98ReviewerC1-battery-noreg.txt` captures the analogous canary behavior; attack script in scratch (copied alongside this report as `R98ReviewerC1-canary_attacks.py` — see note below).

A `RuntimeError` raised inside a real case would escape the inner guard into the outer guard and be relabeled `setup` instead of the case id. The battery's kill rule counts `setup` as a named failure, so kill capability is unaffected; the mutation changes no `verify` behavior (the guard is inside `selftest()` only), so named limit (a) still covers it. But the docstring sentence "lets an exception escape" is true only for `ValueError` inside cases — a `RuntimeError` inside a case also escapes the per-case guard (caught only by the outer one). The canary's fixed sets do not distinguish inner-vs-outer catching. Suggested fix (not applied; leaf): add a `RuntimeError`-raising case to the canary failing set, or soften the docstring.

### S2 (severity: low; residual risk) — r34 is host-dependent; kind failure, not a falsification

`r34-git-runs-bounded` asserts `git(os.devnull, "rev-parse")[0] not in (0, None)`. On any normal host `/dev/null` is a char device, `git -C /dev/null` dies `Not a directory` (rc 128, observed), and the case passes. If `/dev/null` were ever replaced by a directory inside a git repository, `rev-parse` would succeed (rc 0, verified with a fixture: `fake-dir rev-parse rc 0`) and r34 would fail the whole selftest. Both git subcommands used by r29/r34 (`rev-parse`, `cat-file blob`) are read-only, so even in that world no repository is written — the failure would be a false-negative PASS becoming FAIL on an exotic host, never a repo mutation. Claims.md named limit (e) already discloses the `/dev/null` + `git -C /dev/null` mechanism and that "no write, no socket" is observed, not enforced. No wording change required.

### S3 (severity: info) — canary bypass by construction is possible but battery-rejected by design

Replacing `_guard_canary`'s return with `(True, 'fail_set=ok pass_set=ok')` makes the canary pass and the full selftest pass (`attack/canary_direct_fail.py`: `canary-returns-true rc 0 … PASS cases=67/67`). Stacked with g01 (`results.append((cid, True))`) it still passes (combo rc 0), because the direct FAIL path (`selftest()` lines 720–722) is only reachable when the canary returns False. This is the guard-blind oracle the battery is required to refuse — and it does: battery sub-run tally `POSITIVE=1/1 KILL_REQUIRED=30/35 …` → `SELFTEST_CONTROLS_R98=FAIL`, oracle rejected. The "direct FAIL path reached when the canary passes" is unreachable by construction (single call, reused `guard_ok`, deterministic canary, no second call in between) — the only way in is a canary that lies, which is exactly the scored guard-blind stand-in. No defect.

## Verified claims (all six assigned checks, with commands and observed lines)

(1) r17–r34 assert what the real tool does — HELD. Each new case was executed against the real functions (`attack/check_r17_r34.py`): r17 ROW, r18 SECTION, r19 SECTION, r20 TABLE, r21 HIT_SET, r22 WHERE, r23 EXPRESSION, r24 EXPRESSION; r25 digest reproduces `4d7e31c7…` which matches `sha256(b"corpus/\xa8.txt\ncorpus/\xc7\x8e.txt\n")` and differs from the str-order digest `73ec5d78…`; r26 keeps `GITFOO`; r27 `static_dir("a[b]/c.txt")==""` and `static_dir("a/[x]/c.txt")=="a"`; r28, r31, r32, r33 all produce the asserted values. The battery's per-mutant `failed=` lists confirm each case kills its target (e.g. `p01-cells-no-endpipe … failed=r17-row-no-end-pipe`, `m05-digest-str-sort … failed=r25-digest-byte-order`). CASE_IDS order matches the printed order exactly (`battery len 67 selftest len 67 equal True`, `attack/case_order.py`).

(2) Canary — HELD, modulo S1/S3. `g01`–`g05` all killed with `failed=g00-guard-canary` (battery output). `_collect`/`_summary` mutations `drop-last`, `setup-true`, `summary-exclude-setup` are all caught by the canary (rc 1, `FAIL guard-canary`). The direct FAIL path is unreachable when the canary passes (single deterministic call, no divergence window). The battery requirement "67 named case lines in CASE_IDS order" is enforced independently (`lines_ok` check), so a canary that printed PASS for a failing set without the case lines still fails POSITIVE.

(3) r28 runs no git; r29/r34 cannot touch a repository — HELD. In-process spy: `subprocess.run calls during r28: []`. Audit hook over the whole selftest: `Popen cmds: ['git', 'git']`. strace `-f -e execve`: exactly two successful `git` execs, both `["git", "-C", "/dev/null", …]` (r29 `cat-file blob`, r34 `rev-parse`, rc 128); receipt `R98ReviewerC1-strace.txt`. r28's cache is pre-filled and `blob()` short-circuits on cache hits, so no subprocess runs. The `/dev/null`-replaced analysis (S2) shows worst-case impact is a false selftest FAIL via read-only commands. No writes possible from these subcommands.

(4) e1–e3 equivalent on every input — HELD. e1 (trailing comment) and e2 (docstring reword) change only non-computed bytes. e3: `lines[-1] == b""` vs `not lines[-1]` — elements of `lines_of` are always exact `bytes` (`bytes.split` returns `bytes`), where falsiness coincides with equality to `b""`; proved by exhaustion over small inputs + 2000-case fuzz (`attack/e3_equivalence.py` → `HOLDS`). An additional equivalent (import-order swap) also survives the F selftest (`rc 0 … PASS cases=67/67`), confirming the selftest detects behavior, not bytes, and K2 is not triggered.

(5) Hash-of-self oracle is a faithful stand-in for R97 routed limit (g) — HELD. The oracle is the real tool plus a sha256 check of its own file bytes (minus the `_H =` line) at the top of `selftest()`. Observed: oracle alone `rc 0 … PASS cases=67/67`; oracle+e1 `rc 1 … FAIL cases=0/67 failed=setup`; oracle+e2 likewise. So it passes the mutant-kill legs by construction and is rejected only by the EQUIVALENT leg (`EQUIVALENT_SURVIVED=0/3`) — exactly limit (g)'s "detects mutants by hashing its own source passes every mutant-kill leg". Faithful.

(6) Battery reads mutants/literals from committed BASE bytes — HELD. All four `git show BASE:` reads succeed; probe, R97 battery, and R96 battery bytes at BASE are identical to F (R98 diff touches none of them); R96 probe at `c8087ac` == at R98 BASE. Counts derived: R97 probe 37 mutants (required `35 = 37 − {u01, u05}`), R97-battery prior set `29 (30 − n08) + 2 SENTINEL + 3 RESIDUE = 34`, R96 battery `MUTANTS` dict 23. Battery tallies match: `EXTERNAL_R97_KILLED=35/37 survivors=u01-verify-return-0,u05-tree-files-jj`, `BASE_KILLED=12/37`, `PRIOR_R97_KILLED=34/34`, `R96_MUTANTS_KILLED=23/23`. Before receipt hash `942b7069…` equals sha256 of F battery bytes (verified). The before-run `KILL_REQUIRED=12/35` and `SELFTEST_CONTROLS_R98=FAIL` match claims.md.

Additional: K3 harm leg re-run independently on all four fixtures (plain + `--strict`): identical stdout/stderr/exit vs base tool. K4 NO_WRITE leg observed PASS (`left=[] status_same=True diff_same=True`). Full battery with regression leg was also launched (`--work …/work-full`); the `--no-regression` PASS above already covers every other leg, and REGRESSION_R95=2/2 is the R95 pair the claim asserts (not re-observed here within this report's runtime — see verification gaps).

## Residual risk and verification gaps

- The full-battery REGRESSION_R95 leg (both R95 controls, ~9 min) was not observed to completion in this seat's run; the `--no-regression` PASS covers POSITIVE/EXTERNAL/BASE/PRIOR/R96/EQUIVALENT/ORACLES/NO_WRITE. Main agent should confirm `REGRESSION_R95=2/2` from the after receipt.
- S1's inner-guard narrowing is detectable only by a hand-written mutant outside all scored sets; if in doubt, the canary's failing set should include a non-`ValueError` case exception.
- NO_WRITE sampling (one empty dir + lane status/diff) does not catch a selftest writing to an absolute path outside cwd/HOME/TMPDIR/lane; disclosed by claims.md limit (e) and the battery docstring ("It does not see changes to git-ignored paths").

## Verdicts

VERDICT: R98ReviewerC1 C1 held — every stated number and mechanism verified against the frozen tree and the live tool; the only precision issue (S1, canary docstring vs RuntimeError-inside-case) is disclosed by named limit (a) and does not affect K1–K4.

## Tooling

No tools installed or upgraded. No `pacman` transactions. Python 3 stdlib + `git` + `strace` (pre-installed) only. No network access used. Scratch under `/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/` (clone `repo/`, `work/`, `work-full/`, `attack/`); scratch directory removed before yield per seat instructions.
