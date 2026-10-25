# ExecCensus

Seat: executor. Milestone: Round 43 — attack the frozen absent-class split and the one local adoption.
Axes named: operability (the validate command runs and its exit is the script's own), calibration (exit 0 is warnings-allowed, not error-free; the last line is the `ok` row), depth (full stdout, the rule that emits that line, and whether the adopted S078 row is among the findings).

This seat did not retune the 1/2 bound, did not score C1/C2/C3, and did not edit lane production files.

## Command

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
```

Captured run: stdout to `/tmp/execcensus-stdout.txt`, stderr to `/tmp/execcensus-stderr.txt`. No `--out`. Stderr size: `0` bytes. `wc -l` of stdout: `6`.

## Exit code

`0`

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

## Full stdout (verbatim)

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

`sha256sum` of that stdout file:

```
95aee5df652e0086cc1e9ccb6a5dac228a6af6412eb2a0d5ec8bd23eecd39125  /tmp/execcensus-stdout.txt
```

`grep -c` of a tab-E pattern on that file printed `0`. An earlier run of the same command in this seat printed the same six lines and `EXIT_CODE=0`.

## What exit 0 and the last line mean

From `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`:

- Header: exit `0` is "clean or warnings"; W-codes never change status. Validate missing-registry is exit `2`. Exit `1` is E/overdue findings (or census missing).
- W04 is "same URL across scopes (warnings do not affect clean lanes)".
- In validate mode the script sets `lane_errors` only when a tab-`E`-code line is present, prints every `E`/`W` line, then emits `lane<TAB>ok<TAB>file` unless `lane_errors` is 1.
- Final status: exit `1` only if `findings=1` (an E-code on this mode) or a missing registry; otherwise exit `0`.

So the last line is the clean-lane marker, not a summary of zero findings. The five W04 lines are real warnings and do not fail this command. They are not the last line.

Do not substitute `.ufo/waves/round-43/assimilation/validate-census.txt`. That file's last line is `file	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-43/assimilation/validate/corpus/SOURCES.md` — a `--file` invocation, a different lane label, and a mirrored path. It is not this command's last line.

## Local adoption (scoped)

The file named on the `ok` line contains the adopted row (`corpus/SOURCES.md` line 88):

```
| S078 | Bramer, de Jonge, Rethlefsen, Mast, Kleijnen, A systematic approach to searching — Europe PMC full-text XML https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML (capture sha256 833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d; not fetched this round) | paper | A | how a search log is kept as a working document, distinct from a checklist of fields a log must carry | section 6 of the Europe PMC full-text XML, byte offset 17383 of the committed capture | Design and keep the complete search strategies in a log document rather than in the database, so the steps taken stay accountable and reproducible | mined | 2026-10-24 | 365d | corpus/knowledge/search-log-method-r39.md |
```

No stdout line names S078. The W04 ids are S051, S053, S073, S074, S075. `test -e` on `corpus/knowledge/search-log-method-r39.md` exited 0, which matches the absence of an E11 for that mined used-by path. This census does not check quote/capture agreement and does not apply rule R43-SPLIT.

`corpus/lessons/round-43.md` lines 64–66 record a round-start run of this same command as exit 0 with those five W04 ids, and say the round-end root command is recorded in the report. This file is that recording. The lesson text was not edited.

## Files changed

Only `.ufo/waves/round-43/w1/ExecCensus.md`.

## Remaining risks

- Treating exit 0 as "no duplicate URLs" is false. Five cross-scope duplicates remain and are warnings by the script's own contract.
- C1, C2, and C3 were not run here. An unrun check has not passed.
- The census does not prove the S078 quote is in the committed capture.

## Blockers

None.

Report: .ufo/waves/round-43/w1/ExecCensus.md
