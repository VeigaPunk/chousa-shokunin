# RerunC1b — C1 (verify-claims top-level reader) under stress, round 33 wave 2

Landed revision `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`; gate `tools/research-gate.sh`
SHA-256 `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e` (re-checked
with `sha256sum` before the runs and recorded by every receipt). Base gate extracted read-only
with `git show 2b9cc73aed30c2e2c95699db6617d9531ef49fb2:tools/research-gate.sh` (GIT_* unset);
its SHA-256 is `f4731885ac0f83076210be364fd443a4378ac88c3b3ef94b5bf1c9e380f003f0`, the frozen
base. Counter SHA-256 `cb354dd1b5bdf2540e2bf356d945e01cd3ce8207d66e7a1ec76f363650e6a514`.
No lane file was written; all writes are in `.ufo/waves/round-33/w2/RerunC1b/` and
`/fast/scratch/hyaku/chousa-r33/w2/RerunC1b/`.

## 1. Counting runs (kill rule honoured: receipt + redirected stdout for every run)

Command shape (lane root):
`python3 corpus/evidence/round33/c1-count-v2.py --gate tools/research-gate.sh --seed N --receipt <R>.json > <R>.out 2> <R>.err`
with `C1_TMP`/`TMPDIR` set as listed. Seeds are outside 3301-3373.

| run | env / axis | seed | exit | label | elapsed | receipt |
|---|---|---|---|---|---|---|
| r401 | `C1_TMP=/dev/shm/rerunc1b TMPDIR=/dev/shm/rerunc1b` (tmpfs) | 4101 | 0 | 156/156 | 3.365 s | `r401-tmpfs-4101.json` |
| r402 | intended 4× `timeout 120 yes` load — **instrumentation failed** (see §2) | 4102 | 0 | 156/156 | 5.168 s | `r402-load-4102.json` |
| r403 | `LC_ALL=C LANG=C` | 4103 | 0 | 156/156 | 5.033 s | `r403-localeC-4103.json` |
| r405 | `LC_ALL=C.utf8 LANG=C.utf8` | 4105 | 0 | 156/156 | 3.494 s | `r405-localeUtf8-4105.json` |
| r406 | 4 recorded `timeout 120 yes` PIDs (load; host loadavg 40.70) | 4106 | 0 | 156/156 | 12.185 s | `r406-loadrec-4106.json` |
| r407 | `LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8` | 4107 | 0 | 156/156 | 12.548 s | `r407-localeEnUS-4107.json` |

Every receipt: `gate_sha256=94a7be5a…`, `counter_sha256=cb354dd1…`, `gate_rc=1`,
`matched=156`, `total=156`, `predicate_holds=true`. All six `.out` files print the same 16
lines, SHA-256 `1eeb8be8062e53154648a1561adc741386d679d7a21ab05ae895e9a4936c31ab`;
the first line is `TOPLEVEL_FIELD_MATCH=156/156` and all 15 class rows are full
(`D1_duplicate_top_level 24/24`, `S1_flat_confusers 12/12`, `S2_nested_confusers 6/6`, …).
tmpfs proof: after r401 `ls -A /dev/shm/rerunc1b` was empty (the counter's `mkdtemp` root is
removed in its `finally`); I then removed the empty directory.

## 2. r402 — a run whose load axis I cannot claim

I first tried `for i in 1 2 3 4; do timeout 120 yes >/dev/null & P+=($!); done` inline. In this
tool's persistent shell `$!` came back empty (`load_pids=` and `ps` rejected an empty selector),
so no PIDs were recorded; the four jobs appeared later only in the tool's job table and
self-terminated at their 120 s `timeout` (`ps -eo pid,args | grep -E '[y]es$'` then printed
nothing). The counter run itself is valid (receipt + stdout retained, 156/156), but I report it
as *not* load-attributed. r406 replaces it with a foreground script
(`load-run.sh`, SHA-256 `48aec2b8…`) that records PIDs, runs the counter, then kills exactly
those PIDs: `load_pids=1582578 1582579 1582581 1582583`, `load average: 40.70`, afterwards
`ps -o pid,comm -p <those PIDs>` printed only the header and no `yes` remained. Note the host
already carried loadavg ≈ 40 from other seats, so 4 extra spinners are a marginal increment;
the honest signal is elapsed 12.185 s (loaded) vs 3.365 s (tmpfs, idle).

## 3. Contract probes on lines the counter never generates (base vs landed)

Harness `probe.py` (SHA-256 `38f13e57…`), 38 single-line fixtures, each with source
`src/a.md` = `Alpha SPAN omega.`; `bash <gate> verify-claims claims.jsonl --root <dir>`,
run under `LC_ALL=C` and `LC_ALL=en_US.UTF-8`. Outputs: `probe-land-C.txt`
(`9785a780…`), `probe-base-C.txt` (`0bfa8d3d…`), `probe-land-utf8.txt` (same hash as landed-C),
`probe-base-utf8.txt` (same hash as base-C) — **locale changed nothing, byte-for-byte**, and
`bash -c '[[ $'"'"'\u00a0'"'"' == *[[:space:]] ]]'` is false in C, C.utf8 and en_US.UTF-8, so
there is no NBSP trimming divergence.

Landed holds each counted clause on these inputs: nested `line` decoy in an object
(`p02`), in an array (`p03`), two levels deep (`p33`), nested-only `marker`/`sha256`/`expect`
(`p23`/`p24`/`p25`), nested duplicate key (`p39`), string confusers incl. escaped quotes and a
trailing backslash (`p06`, `p07`, and 2- and 4-backslash tails `p35`/`p36`), string holding
`} ] { [` (`p38`), duplicate `line` identical/differing (`p04`/`p05`), duplicate `id`
identical (`p22`, CLAIM line keeps `id=c1`), duplicate `marker` (`p28`), duplicate unread key
(`p40`), trailing comma (`p18`), two objects on one line (`p37`), `line` as object/number
(`p20`/`p21`), empty key (`p19`), UTF-8 values (`p27`). Base, on the same lines, reads the
nested decoy (`observed=mislocated line=9-9`, `p02`/`p03`/`p33`), accepts the duplicate as
`mislocated` (`p04`/`p05`), accepts a trailing comma (`p18`), reads the first of two objects
(`p37`) — the C1 delta is real and repeats on lines outside the counter's matrix.

Unknown keys are inert and safe: `we]ird`, `a}b`, `a"b` and `$(touch PWNED)` as member names
(`p13`–`p16`) all verify as `supported`, with no bash error, and the harness confirms no
`PWNED` file was created in the fixture root.

### Two gaps found, both uncounted and identical at base

**G1 — a line that is not valid JSON can still verify (fail-closed gap).**
Minimal line (bytes as written):

```
{"extra":truthy,"id":"c1","source":"src/a.md","span":"SPAN","expect":"supported"}
```

landed: exit 0, `CLAIM id=c1 expected=supported observed=supported source=src/a.md at=line:1
verdict=match`, `VERDICT_BEARING_CLAIMS=1/1` (`p08`; nested variant `p09` is the same). The
atom branch of `claim_scan` accepts any non-empty token up to a delimiter
(`tools/research-gate.sh:1218-1227`). `corpus/evidence/round33/claims.md` says the candidate
"is asked to fail closed" on lines that are not exactly one valid JSON object, and lists that
class under **Not claimed**; base behaves identically, so this costs nothing on 156/156 and is
not a C1 regression. Read fields are unaffected: `"expect":true` is `missing expect` and
invalid (`p26`).

**G2 — the marker-default shortcut runs before the duplicate check.**
Minimal line:

```
{"marker_default":"M","line":"1","line":"2"}
```

landed: exit 0, no `CLAIM` and no `FINDING` line, `VERDICT_BEARING_CLAIMS=0/0` (`p17`); base is
identical. The shortcut at `tools/research-gate.sh:1610-1614` only guards duplicated `id` and
`marker_default`, then `continue`s before the duplicate loop at `:1636-1643`. Contract item 2
says a repeated top-level read field makes the record invalid; if a `marker_default` row counts
as a claim record this is a break. It carries no `id`, `claims.md` says `marker_default` rows
are not counted, and the counter never generates them; the failure mode is silent ignore, not a
wrong verdict. Low severity, no C1 delta.

Also noted, unchanged at base and therefore out of the C1 delta: leading NBSP / NBSP-only line
are `not a JSON object` in both gates (`p31`/`p32`), BOM/trailing tab behave as trimmed
whitespace (`p30` supported).

## 4. Repairs, sources, knowledge (shape only, not executed here)

`corpus/SOURCES.md:72-73` carries S062 (RFC 8259, level A) and S063 (Python `json`, level A)
with body hashes and access date 2026-10-23; `corpus/knowledge/claim-record-fields-r33.md`
exists (4755 B) and cites both; D1 `corpus/evidence/round32/c2-count-v3.py` (19371 B), D2
`corpus/evidence/round33/d2-census.py` (6003 B) and D5
`corpus/evidence/round33/no-name-signals.sh` (7529 B) exist, and the D3 battery header is at
`.ufo/waves/round-33/w1/ExecNoHarmBase33/battery.sh:1-4`. These are existence/shape checks
only; running them is other seats' scope. No tools installed or updated.

## Verdict

**HOLDS** for the assignment's axes: on the landed gate the counter prints 156/156 on tmpfs,
under C / C.utf8 / en_US.UTF-8, and under 4 recorded CPU-load PIDs (six runs, six receipts,
exit 0, `predicate_holds=true`); locale does not change any probe verdict. The C1 contract is
obeyed on nested decoys, duplicates of all six counted keys, string confusers, and malformed
lines that start/end badly. The two defects above are real but fall in the design's
**Not claimed** class and are behaviour-identical at base, so they do not falsify C1.

Limits: host loadavg ≈ 40 from sibling seats makes the 4-way load marginal (r402's load
instrumentation failed and is reported as such); 38 hand-built probes, not exhaustive; no
concurrent counter runs; only UTF-8 (not malformed byte sequences) was exercised; every
verdict is from a run recorded here, nothing inferred beyond the marked `[INFERENCE]` reading
that marker_default rows are outside "claim record".
