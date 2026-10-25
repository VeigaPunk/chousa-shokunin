# W2ExecCensus

Seat: executor. Milestone: Round 44 wave 2 — genuine seats after the usage-error wave.
Axes named: operability (the assigned validate command runs, and the exit is the script's own), calibration (exit 0 is warnings-allowed, not error-free; the last line is the `ok` row), depth (full stdout, the rule that emits each W04, and which earlier row actually armed that URL).

This seat did not retune frozen claims, did not score C1/C2/C3, did not run `c2-count.py`, and did not edit lane production files.

## Command

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
```

Clean capture: stdout `/tmp/w2execcensus-stdout.txt`, stderr `/tmp/w2execcensus-stderr.txt`. No `--out`. Stderr size: `0` bytes (`wc -c -l` → `0 0`). Stdout: `6` lines, `528` bytes. An earlier invocation in this seat printed the same six script lines and `EXIT_CODE:0`; that first transcript mixed a wrapper `echo` into the same stream, so the figures below are the split capture.

Script sha256 (this run):

```
3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30  /home/vgpnk/Projects/shokunin/scripts/sources-census.sh
```

That digest string is the one recorded in `.ufo/waves/round-35/w2/ExecCensus.md`. This seat did not re-hash that older report's copy of the script.

## Exit code

`0`

Not exit `2`. Exit `2` is the script's usage/env/missing-registry class (`sources-census.sh` header, lines 16–18; `missing_error` at line 804). This invocation found the registry and was not a usage error.

## Warnings (verbatim)

Five lines. `grep -c` of a tab-`W` pattern: `5`. `grep -c` of a tab-`E` pattern: `0`. No W01, W02, or W03.

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
```

`cat -A` of the whole stdout, so the separators are visible:

```
chousa^IW04^IS051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes$
chousa^IW04^IS053 duplicate url docs.python.org/3/library/socket.html across scopes$
chousa^IW04^IS073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes$
chousa^IW04^IS074 duplicate url docs.python.org/3/library/hashlib.html across scopes$
chousa^IW04^IS075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes$
chousa^Iok^I/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md$
```

`sha256sum` of that stdout file:

```
95aee5df652e0086cc1e9ccb6a5dac228a6af6412eb2a0d5ec8bd23eecd39125  /tmp/w2execcensus-stdout.txt
```

That digest equals the stdout digest recorded in `.ufo/waves/round-43/w1/ExecCensus.md`. This seat did not reopen that round's `/tmp` file.

`cmp -s` of this stdout against lines 1–6 of `corpus/evidence/round44/receipts/census-start.txt` printed `CMP: stdout identical to census-start.txt lines 1-6`. Line 7 of that receipt is `exit=0` (`cat -A` → `exit=0$`). That seventh line is not script stdout. Do not treat the receipt file as this command's output.

## Last line

```
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

`od -An -tx1` of that line, including the trailing newline:

```
 63 68 6f 75 73 61 09 6f 6b 09 2f 68 6f 6d 65 2f
 76 67 70 6e 6b 2f 50 72 6f 6a 65 63 74 73 2f 73
 68 6f 6b 75 6e 69 6e 2f 63 68 6f 75 73 61 2d 73
 68 6f 6b 75 6e 69 6e 2f 63 6f 72 70 75 73 2f 53
 4f 55 52 43 45 53 2e 6d 64 0a
```

The two separators are tabs (`09`). The line ends in `0a`.

The path on that line is the live registry. `sha256sum` of it this run:

```
1d4c5004beb48a4e3ba67715cd342d406f159f238de91407fe412a9d09209a7c  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain=v1 -- corpus/SOURCES.md` printed nothing (`wc -l` of that status: `0`). `git rev-parse --short HEAD` printed `043f19a`. `git diff --numstat -- corpus/SOURCES.md` printed nothing. This `ok` is not a dirty mid-wave append. This seat did not commit.

## What exit 0 and the last line mean

From `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`:

- Header (lines 16–18): exit `0` is "clean or warnings". W-codes never change status. Exit `1` is E/overdue findings (or census-mode missing). Validate missing-registry is exit `2`.
- Line 33: `W04 same URL across scopes (warnings do not affect clean lanes)`.
- Validate mode (lines 737–745): `lane_errors` is set only when a tab-`E` line is present. Every `E`/`W` line is printed. Then `lane<TAB>ok<TAB>file` is emitted unless `lane_errors` is 1.
- Final status (lines 803–806): exit `1` only if census-mode missing, `missing_error`, or `findings=1`. Otherwise exit `0`. W04 does not set `findings`.

So the last line is the clean-lane marker, not a summary of zero findings. The five W04 lines are real warnings and do not fail this command. They are not the last line.

W04 is emitted at line 645, on the later row only:

```
if (u!="" && (u in url_seen) && !(scope_key in url_scopes))
  printf "%s\tW04\t%s duplicate url %s across scopes\n",lane,id,u
```

`url_of` (lines 600–605) takes the first `http(s)` URL in the source cell, strips a trailing fragment and a trailing slash, and strips the scheme. Same URL plus the same scope string is not W04. That case is E04 (lines 646–649), and E04 is suppressed when the later row is `rejected` or its teaches cell matches `supersedes S[0-9]{3}`.

A seat-side gawk using that same condition, run on the file named by the `ok` line, wrote five lines. `cmp -s` against the census W lines printed `CMP: rederived W04 lines identical to census W lines`. That re-derivation is not a second census mode. It is a check that the five warnings are the across-scope hits, not a missed E04 set.

## What each warning is pairing

The warning names the later id, not the earlier one. Scope strings below were compared by splitting the live registry rows; `scope_equal=False` for every pair listed.

| warning id | normalized URL | earlier row that put that URL in `url_seen` | why this is W04, not E04 |
|---|---|---|---|
| S051 | `www.w3.org/TR/2017/REC-html52-20171214/syntax.html` | S050 (`#optional-tags` stripped) | scope strings differ; S051 teaches does not say supersedes |
| S053 | `docs.python.org/3/library/socket.html` | S052 (`#socket-timeouts` stripped) | scope strings differ |
| S073 | `www.gnu.org/software/coreutils/manual/coreutils.html` | S071 (`#env-u` stripped) | scope strings differ from S071 |
| S074 | `docs.python.org/3/library/hashlib.html` | S059 | scope strings differ; status is `rejected`, which would also suppress E04 |
| S075 | same coreutils URL | S071 (S073 has already been seen too) | scope strings differ from both S071 and S073 |

S074 still warns. W04 does not read status. A rejected duplicate across scopes is a warning, not a failure.

S070 does not arm the coreutils URL. Its source cell is a local man path and contains no `http(s)` URL. The probe of that cell printed `url_of=[]` and `source_has_https=no` (`NF=13`). The cell text, from the live registry:

```
GNU coreutils `sha256sum(1)` manual — `/usr/share/man/man1/sha256sum.1.gz`
```

S073's scope string is also not equal to S070's. The round-41 disposition (`corpus/evidence/round41/w04-dispositions.tsv`) says S073 shares S070's page URL. That sentence is not what this parser matched. The census line is not evidence that S070's source cell contains `coreutils.html`. S073's teaches cell does contain `supersedes S070`, which would suppress E04 if a prior non-rejected row had already recorded the same URL and the same scope. That is a different gate from the W04 that fired.

Same-URL supersede rows S029–S033 are silent in this stdout. Their teaches cells contain `supersedes S0NN`, and their scope strings match the earlier row, so neither W04 nor E04 fires. A first join in this seat that ignored scope and the supersedes exemption listed them; that join was wrong and is not a census finding.

`corpus/evidence/round41/w04-dispositions.tsv` names the same five warning ids (S051, S053, S073, S074, S075). This seat did not run `python3 corpus/evidence/round41/c2-count.py`. An unrun check has not passed. Do not read this report as `W04_DISPOSITIONED=5/5`.

## What this command did not count

Validate mode does not print a row count. A separate `grep -c '^| S[0-9]'` on the file named by the `ok` line printed `78`. A separate registry parse printed `last=S078`, `status.mined=54`, `status.queued=19`, `status.rejected=5` (54+19+5=78). Those figures are not census stdout.

No E11 appeared. That means `usedby_findings` (lines 538–570), which checks `used-by` only for `mined` rows, printed nothing. This seat did not walk those paths itself.

Not run, so not passed: `overdue`, `shared`, `census` (the count mode), `selftest`, `--file`, and the round-41 C2 counter. `corpus/evidence/round44/claims.md` has no census or W04 predicate; this run does not retune one.

## Files changed

Only `.ufo/waves/round-44/w2/W2ExecCensus.md`.

## Remaining risks

- Treating exit 0 as "no duplicate URLs" is false. Five cross-scope duplicates remain and are warnings by the script's own contract.
- Treating the warning id as the only holder of that URL is false. The earlier row is S050, S052, S071, or S059, and the warning does not name it.
- Joining S073's warning to S070 by the disposition sentence joins a fact the parser did not see.
- C1, C2, and C3 were not run here.

## Blockers

None.

Report: .ufo/waves/round-44/w2/W2ExecCensus.md
