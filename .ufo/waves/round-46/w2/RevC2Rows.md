# RevC2Rows — round-46 wave 2: five r46 Gates rows judged for truth

Target: `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`, archived read-only to
`/tmp/chousa-r46w2-RevC2Rows` (`git archive d09fc8e7 | tar -x`); rows read from that archive's
`SKILL.md:113-117`. Mid-wave HEAD moved (`git reflog`: `d09fc8e` → `3807537` → `e50b388`, both
"export from jj"), so row-level conclusions are taken on the d09 archive; live-tree runs are
labelled. Each entry ran once, read-only (write options omitted: `--json`, `--output`, and
build-spans' write mode).

| row | SKILL.md | verdict |
|---|---|---|
| `round24–27 counting instruments` | :113 | **wrong cell** (exit contract; 3 witnesses) |
| `round33–34 census instruments` | :114 | **true** |
| `qr-harness` | :115 | **true** |
| `inference-ground` | :116 | **wrong cell** ("one FINDING line per bullet") |
| `chousa round-46 counters` | :117 | **wrong cell** (build-spans exit 2; stale pins) |

## F1 — :113 exit contract false; verdicts are labelled harness failures

Cell: "counts, never verdicts: each prints its own tallies and exits 0 on a readable tree, exit
1 on a harness failure and exit 2 on usage, as each script's own header states".

A — exit 1 on a readable tree:
```
$ bash /tmp/chousa-r46w2-RevC2Rows/corpus/evidence/round25-measure.sh /tmp/chousa-r46w2-RevC2Rows
== holds: selftest, drift vs r12 baseline, r1 archive observable
RESEARCH_GATE_SELFTEST: PASS (275 cases, 0 skipped)
GATE_DRIFT: +resolvable drift
rc=1
```
Measurements completed (`STALE_RESTATEMENTS=0` precedes), yet `set -euo pipefail` aborts on
`--drift`'s 1, so the r1-archive leg never runs. The exit 1 is a **gate-vs-r12-baseline drift
verdict**; the script's header (`round25-measure.sh:11`) says "Exit 0 means the measurements
completed".

B — exit 1 on expectation mismatch, at the d09 gate:
```
$ python3 .../round27-falsify-controls.py --gate .../tools/research-gate.sh
MISMATCH C3 source-scanner-fault--oE ../residual/ResTokenPrefilter missing 'META_SOURCE_SCAN_FAILED'; count '^FINDING META_SOURCE_SCAN_FAILED\b': 0 != 1
MISMATCH C3 source-scanner-fault--xE ../residual/ResTokenPrefilter missing 'META_SOURCE_SCAN_FAILED'; count '^FINDING META_SOURCE_SCAN_FAILED\b': 0 != 1
rc=1
```
Its header (`round27-falsify-controls.py:5`): "Exit0 every expectation matched; exit1 mismatch;
exit2 setup" — so "as each script's own header states" is self-refuting, as for
`round27-regressions.py:4`. Class confirmed in code: `round25-meta-differential.sh`
`sys.exit(0 if total > 0 and agree == total else 1)`, `round26-date-differential.sh`
`raise SystemExit(1)`, `round26-registry-differential.sh` `sys.exit(0 if ... else 1)`,
`round27-regressions.py` `raise SystemExit(int(summary['mismatches'] != 0))`. Seven of ten
scripts exit 1 on a disagreement about the gate, i.e. on a verdict.

C — usage error returns 1, not 2: `$ python3 .../round27-mechanisms.py` → `IndexError: list
index out of range`, `rc=1` ("`round27-mechanisms.py:13` reads `sys.argv[1]` unchecked); the
declared exit 2 is unreachable.

The ten pinned digests in this row are correct at d09 (e.g. `a878e14faa7e…`,
`ab9462e1d687…`).

## F2 — :117 build-spans' declared exit 2 does not exist

Cell: "build-spans exit `0` written or `--check` clean (`SPANS_ROWS=11 STALE=0`), exit `1`
stale, exit `2` missing capture or absent quote".
```
$ python3 .../corpus/evidence/round46/build-spans.py --check --cache /tmp/.../emptycache3
build-spans: no capture /tmp/chousa-r46w2-RevC2Rows/emptycache3/5a631adb18988a1a2421ce75.txt
rc=1
```
`build-spans.py:62` `raise SystemExit(f"build-spans: no capture {cap}")` → status 1; `main()`
returns only 0/1 (`:99`, `:108`); absent quote takes the same route. Only argparse usage is 2.
The stale leg is true: a mutated `capture_sha256` gives `SPANS_MANIFEST_STALE` /
`SPANS_ROWS=11 STALE=1`, rc 1.

## F3 — :117 pinned digests name no committed blob

Cell: "sha256 c1 `96833e22b0eb…`, build-spans `d41b1e5a090d…`". At d09: `c1-count.py`
`819287e2075c3f5b…`, `build-spans.py` `b5c4d83bc9a32639…`. `96833e22` is the 07:27:37
intermediate edit (`.ufo/waves/round-46/w1/ExecCounterRun.md:76`); `d41b1e5a` the 07:24
bare-span revision (`w1/ReviewerC3Spans.md:10`). The row contradicts the file it cites:
`corpus/evidence/round46/measure-after.txt:3` records "c1 819287e2075c3f5b … build-spans
b5c4d83bc9a32639".

Happy paths are true at d09: c1 `TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS` rc 0;
c2 `ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=35 REGISTERED=72/72
UNREGISTERED=0 C2=PASS` rc 0; c3 and `--lane-only` the nine declared lines (`CAPTURE_BOUND=11/11`
vs `skipped`) rc 0; c1 `--root <empty>` rc 2 `no-fixtures`; c2 `--root <empty>` rc 2
`no-entry-points`; c2 with Gates rows stripped → `UNREGISTERED=48 C2=FAIL` rc 1.

## F4 — :116 "one FINDING line per bullet" false (d09 bytes)

Cell: "exit `1` findings, one `FINDING` line per bullet
(`INF_SECTION_ABSENT`/`INF_UNCITED`/`INF_UNGROUNDED`/`INF_TOKEN_NOT_IN_SPAN`)".
```
$ python3 tools/inference-ground.py --entry .../junk-uncited.md --spans .../spans.tsv \
    --counts .../counts.json --root .../inference-ground-r46
GROUND entry=junk-uncited.md section=1 bullets=1 tokens=1 grounded=0
FINDING INF_UNCITED bullet=1 token=''
FINDING INF_TOKEN_NOT_IN_SPAN bullet=1 token='the release ships a frozen pool'
GROUND: FAIL
rc=1
```
One bullet, two `FINDING` lines; `junk-borrowed.md` likewise (`bullets=1`, two
`INF_TOKEN_NOT_IN_SPAN`); `junk-ungrounded.md` one. Other clauses hold: positives rc 0 with
`GROUND: PASS`; usage and a missing entry rc 2; `c1-count.py --tool <always-pass>` reproduces
`POSITIVE_PASS=3/3 JUNK_KILLED=0/3 CANARY=fail` rc 1 exactly as `controls/c1-controls.txt`.

## True rows — evidence

**:114** d2-census rc 0 with `C1 receipts on gate 10f2fe12: 21`; `no-name-signals.sh
--code-only tools/` → `0 hits … RESULT CLEAN (exit 0)`, on `.ufo/waves/round-32` → `1 hit(s) …
RESULT DIRTY (exit 1)`, `--bogus` and a non-directory → rc 2; `self-audit.py` prints
`SELF_AUDIT_MISMATCHES=2` then `SELF_AUDIT_UNDISPOSITIONED=1`, rc 0 — "predicate does not hold
at HEAD while the exit stays 0" is exact. (d2-census/self-audit need the git repo, so they ran
on the live tree before the HEAD move.)
**:115** bare → docstring rc 2; missing map → `FileNotFoundError` rc 1; probe returning 0 →
`QUOTE_REOPEN^IX1^IVERBATIM$` (`cat -A`, tabs) rc 0; returning 2 → rc 2; returning `"0"` → rc 2;
`93.184.216.34` → `ConnectionRefusedError: [Errno 111] harness: unrouted destination`;
`__pycache__` left beside the imported candidate.

## Gaps / non-findings

- C3's "exit 1 any leg short" and C1's "a positive failing" legs were read from code, not run.
- Live `e50b388` prints `ENTRY_POINTS=73`: that commit's `SCORECARD.md:2480` names
  `corpus/evidence/round46/build-spans.py`; d09 prints 72. Not a claim defect (target ≥ 71,
  `UNREGISTERED=0`), but the row's cited after-state belongs to d09 and `measure-after.txt` was
  rewritten by the later commit.
- :116's pin `819f83eb…` is correct for the landing commit; the current HEAD tool is
  `3018b1d2…` (11451 B). The false clause reproduces on both byte sets; the pin no longer names
  the current file.
