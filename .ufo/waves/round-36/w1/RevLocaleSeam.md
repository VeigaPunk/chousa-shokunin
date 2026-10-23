# RevLocaleSeam — round 36 wave 1, locale seam (repair R4) review

Access date for all opened files: 2026-10-23. Lane: /home/vgpnk/Projects/shokunin/chousa-shokunin at master=700bd5fcbf9abc118a6a0f078d51a2e7460c2878 (read `git rev-parse master`). All artifacts under `.ufo/waves/round-36/w1/RevLocaleSeam/`; scratch under /tmp/hyaku/chousa-r36/w1/RevLocaleSeam/ (lab/). No lane production file was modified; no git/jj writes; no installs performed (none needed).

## Gate identity

```
sha256sum tools/research-gate.sh .ufo/waves/round-36/controls/base-gate-r36.sh
→ a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  tools/research-gate.sh
→ a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad  .ufo/waves/round-36/controls/base-gate-r36.sh
```
Both match the wave's pins. Exit 0.

## 1. Scope check of `json_unescape` (R4)

Read `tools/research-gate.sh:1442-1515` (accessed 2026-10-23): `json_unescape()` is lines 1442-1507; the scope is exactly

- L1457 `local LC_ALL=C`
- L1458 `export LC_ALL`

Leak test (decides "covers the decode and not the caller's variables"):

```
export LC_ALL=en_US.utf8; f() { local LC_ALL=C; export LC_ALL; echo "inside:$(bash -c 'echo $LC_ALL')"; }; f; echo "after-f:[$(bash -c 'echo $LC_ALL')]"
→ inside:C
→ after-f:[en_US.utf8]      (exit 0)
```

Children spawned while the function runs see `C`; after return the caller's value is restored — no leak. All 10 production call sites (L1881, 1888-1890, 1906-1910, 1918, 1931) are command substitutions, so the scope dies with the subshell and never touches the main shell's environment.

Decode byte-identity battery (extracted function via `awk '/^json_unescape\(\)/{f=1} f{print} f&&/^}$/{exit}' tools/research-gate.sh > lab/ju.sh`; ju.sh sha256 `1f1a7105e1195c7e0cc69c64f47cac576582a8f4e5eff69d9b004731ea93e83c`; 11 cases incl. `\u00e9`, `\u00C9`, `\u07ff`/`\u0800` boundary, lone + paired surrogates, `\u0000`, malformed `\u12g4`, trailing backslash, `\b\f\n\r\t\/\"\\`) run under 7 environment shapes (`env -i` unset, LC_ALL=C, LC_ALL=C.UTF-8, LC_ALL=en_US.utf8, LANG=en_US.utf8, LC_CTYPE=en_US.utf8, LC_ALL=POSIX): all 11 sha256 digests identical across all 7 shapes (`battery.out`, exit 0). Spot decodes under LC_ALL=C: `\u00C9`→`c3 89`, pair `\ud83d\ude00`→`??`, lone `\udd7f`→`?`, `\u12g4`→literal `\u12g4`, boundary `\u07ff`→`df bf`, `\u0800`→`e0 a0 80`. **The decode is locale-independent by construction, and the scope does not leak.**

Adjacent decode-semantics note (not locale): `\u0041\u0000\u0042` decodes to length 2 (`AB`) — bash cannot hold NUL, so `\u0000` silently vanishes. The escaped-NUL guard exists only on the sha256 path (L1930-1931, L1944); span/id/marker/expect paths are unguarded, so a span containing `\u0000` could match NUL-less text. Pre-existing r31 design; recorded as an adjacent observation, not a locale finding.

## 2. Sweep of other locale-sensitive constructs (the L1457 scope does not cover these)

Findings table (line · construct · locale exposure · covered?):

| Line(s) | Construct | C-locale environment changes the answer? | Covered by a test? |
|---|---|---|---|
| 1442-1507 + 1457-1458 | `json_unescape` in `LC_ALL=C` scope | No — byte-identical across 7 shapes (battery) | Yes — selftest cases 257-258 (`claims-locale-c`, `claims-locale-boundary`, gate L8041+) |
| **1015** | `grep -qiE 'window_mode:[[:space:]]*external\|…'` (Meta scan) via pinned wrapper under **caller** locale | **YES — demonstrated end-to-end**: `[[:space:]]` matches U+1680/U+3000 under en_US.utf8, not under C (pinned GNU grep: `cls.txt` → C=0, en_US=2; the 2 bytes are `e1 9a 80`, `e3 80 80`). `window_mode:　external` + approved URL pointer: C → `EXTERNAL_WITHOUT_APPROVAL crit`, ROLL=DRIFT, rc=1; en_US.utf8 → CLEAN, rc=0 | **No** — no selftest exercises window_mode with a unicode space |
| **1019** | `grep -qiE 'fetch=external\|…\|window_mode[[:space:]]*[|][[:space:]]*external'` | Same class: `[[:space:]]` around `\|` flips `WINDOW_EXTERNAL` on U+1680/U+3000 (mechanism proven at 1015; no separate end-to-end run) | No |
| 762 | `line_has_mark() { grep -qiE "$DEAD_MARK_RE" … }` | `-i` folding is locale-dependent: `écaf` pattern vs `Écaf` text → pinned GNU grep NOMATCH under C, MATCH under en_US.utf8. A flip needs a non-ASCII char folding into a pattern word (DEAD_MARK_RE at L760 is ASCII words; glibc folds U+0130 İ→i) — reachable in principle, none demonstrated | No |
| 1083 | `grep -qiE "$AGG_ERE"` (L325: `aggregator\|wikipedia\|…`) | Same `-i` mechanism (`WİKİPEDİA`→`wikipedia` under UTF-8 only) — in-principle | No |
| 1930, 1944 | `${sha_raw,,} != *'\u0000'*` | No on valid records: `escok` (L1274 `^\\(["\\/bfnrt]\|u[0-9A-Fa-f]{4})`) admits only lowercase `\u`, and no non-ASCII lowercases into `\u0000`. `${s,,}` itself IS locale-divergent (microbench: `ÉİⅠＡ` → C keeps all, en_US folds to `éiⅰａ`) — unreachable here | n/a (safe by parser) |
| 2541 | `${k,,} =~ $re` (`flip\|falsif\|reversal\|counter`) | No C-vs-en_US divergence for ASCII regex on valid rows; latent tr_TR `I`→`ı` (no tr_TR locale installed here — untested) | No |
| 674, 694, 706, 932, 1030, 1065, 1105, 1107, 2141, 2144, 2365, 2694 | `tr 'A-Z' 'a-z'` | Identical C vs en_US for ASCII input (byte ranges); tr_TR range-expansion latent — untested (locale absent) | No |
| 900, 1512 | `n=${n//[[:space:]]/}` | No — inputs are wc/tr digit output. (Bash classes ARE divergent for U+0085/U+1680/U+3000 — mechanism proven — but these sites see digits only) | n/a |
| 851, 2080, 2131, 2240 | `printf '%.80s'` context/obs truncation | No — bash builtin `%.Ns` precision is byte-based: `printf '%.10s'` on `é`×45 → 10 bytes under BOTH C and en_US.utf8 (exit 0). Gate-level ctx path not exercised (span-not-found branch emits `context=-`); microbench only | n/a |
| 1253, 1723-1724, 1735-1736, 1757-1758, 1780-1781, 1802-1803, 3001, 3050, 3075, 3197, 3202-3204, 3272, 3522, 4045, 933 | `LC_ALL=C`-pinned (claim_scan, span matchers, source tokens, sort -u, scope_norm) | No — pinned | Yes (257-258 exercise the decode path through these) |
| 327-330 | `date +%Y-%m-%dT%H:%M:%SZ` | No — explicit numeric format, no locale names [INFERENCE from format string] | n/a |

Host grep caveat that shaped the sweep: bare `grep` here is the uutils shim (`grep is a shell builtin`; `grep --version` → `pi-uu-grep 0.2.0`; `/usr/bin/grep --version` → `GNU grep 3.12-modified`). All sweep evidence above uses `/usr/bin/grep` — the same binary the gate pins through its L359 wrapper (`grep() { "$GREP_BIN" "$@"; }`), which passes the **caller's** locale through; an early bare-`grep` run gave opposite results and was discarded.

## 3. Fresh-seed re-derivation (context task)

```
C1_TMP=…/c1tmp python3 corpus/evidence/round36/c1-count.py --seed 36301 --receipt …/w1/RevLocaleSeam/c1-s36301.json   → exit 0, ENGINE_SWAP_CANARY=14/14, predicate_holds=true, gate_sha256=a7d3922c…, S12-locale-c PASS (c_obs=utf8_obs={L1:[supported,match]}, both rc 0)
C2_TMP=…/c2tmp WITNESS_TMP=…/wtmp python3 corpus/evidence/round36/c2-count.py --seed 36311 --receipt …/w1/RevLocaleSeam/c2-s36311.json → exit 0, WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass, predicate_holds=true, gate_sha256=a7d3922c…
```
(First attempts exited 2/1 — counter temp dirs and receipt dir did not exist; created `…/c1tmp c2tmp wtmp` and `.ufo/waves/round-36/w1/RevLocaleSeam/`, then reran clean as above. The 14/14 and 5/5 batteries themselves succeeded identically in the failed-receipt runs.)

## MEETS-class finding (most valuable result)

**The gate's verdict is a function of the caller's locale on the landed gate (a7d3922c…), via L1015 — the same environmental-dependence class S12/R4 closed for the decode.** Same record, same gate, same epoch, only the environment differs:

```
cd lab && CHOUSA_NOW_EPOCH=1700000000 LC_ALL=C LANG=C bash <lane>/tools/research-gate.sh verify rec/r.md --root rec
→ rc=1; FINDING EXTERNAL_WITHOUT_APPROVAL severity=crit … ; RESEARCH_GATE: DRIFT (findings=1 …)
CHOUSA_NOW_EPOCH=1700000000 LC_ALL=en_US.utf8 LANG=en_US.utf8 … same command
→ rc=0; RESEARCH_GATE: CLEAN (findings=0 …)
```
(`rec/r.md` = record with Meta `| window_mode:　external |` (U+3000), Approval row `external/all/approved`, Sources row S1 → `https://example.invalid/a`. Receipts: artifacts `win-C.txt` / `win-en_US.utf8.txt`; diff shows exactly the one finding + roll lines changed.)

Why it matters: a caller who happens to run under a UTF-8 locale gets CLEAN for a record that drifts under C — the approval gate (an external-window decision) flips on an invisible byte class. It is NOT a C1/C2 kill: S12's counter fixture (café span, verify-claims) never touches window_mode, and my fresh-seed runs still print 14/14 and 5/5 with `predicate_holds=true`. It sits precisely in the claims.md stated limit ("the locale arm … says nothing about locale-sensitive behaviour outside `json_unescape`") — this run demonstrates that limit is live, with line 1015 (and the same construct at 1019) as the named open seam. Repair direction (not measured, repairs carry no claim): pin `LC_ALL=C` around the L1015/L1019 scans, as every other locale-sensitive site already does.

## Verdict

**Seam closed for the decode** (R4 verified: byte-identical decode across 7 locale environments × 11 escape cases, `LC_ALL=C` scope correct and non-leaking, selftests 257-258 cover it); **open exposures: L1015 demonstrated verdict-flipping (U+1680/U+3000 in `window_mode:[[:space:]]*external`, untested), L1019 same class, L762/L1083 `-i` folding in principle; `${sha_raw,,}`/`${k,,}`/`tr` latent only under exotic locales (untestable on this host).**

## Artifacts (all under `.ufo/waves/round-36/w1/RevLocaleSeam/`, sha256)

- `c1-s36301.json` `a6562aa8696d01026d628dd4153108b9293f42e8cab0b11f91b4001b76432d58` — C1 fresh-seed receipt (36301)
- `c2-s36311.json` `987522dbdcc7d60d0df0dbc81a6c067de00796c8bb65d487f2eb1b6ee79de3c1` — C2 fresh-seed receipt (36311)
- `win-record.md` `548e0fd1a4e16575117503bc6fe1fb983f7e9332f215063cb8d3fc266c36f4ec` — verdict-flip fixture
- `win-C.txt` `6eab8aa3416a9f5cdb332fadacd8defebce5015425a6f6ccd9a2e45a51ea17c3` / `win-en_US.utf8.txt` `d54d664f7a358f3b97084ed3840dba9b5420de038ac0d2d23875f7edd699b56d` — the two gate runs
- `battery.out` `b02ac03919b50a97fa3f7a07e2eddc48482adf5a169fe4276ce9a15730030a41` — decode battery digests
- `cls.txt` `a79fd7867e5dd6ebc1eb4eeaac523bb39fa6c79ccd14afbefb34355e46880e4a`, `fold.txt` `3927055e9d0d38633601f7cd4515627a5d7bf468d2ae26187b1f8679acdfd990` — class/folding probes

Large intermediates stay in /tmp/hyaku/chousa-r36/w1/RevLocaleSeam/lab/ (ju.sh, out-*.txt, ctx-*.txt, err-*.txt).

## Residual risk and verification gaps

- L1019, L762, L1083 divergences are mechanism-proven (direct pinned-grep probes) but not demonstrated end-to-end through the gate; L851/2080/2131/2240 cleared by microbench only (gate ctx path not exercised).
- tr_TR/`${k,,}`/`tr` latent exposures untestable here (locale not installed; no locale generation attempted — out of bounds).
- The window_mode flip was observed on one fixture at one epoch; no sweep across records — a single demonstrated flip is sufficient for the finding, saturation not claimed.
