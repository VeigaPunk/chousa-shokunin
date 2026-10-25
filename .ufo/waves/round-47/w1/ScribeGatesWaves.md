# ScribeGatesWaves — round 47 wave 1 (C2 calibration, wave-control rows)

Item: draft SKILL.md `## Gates` rows for `.ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh`,
`.ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py`, `.ufo/waves/round-35/repairs/slen-probe.sh`,
`tools/mechanism-witness.py`; find who names each; run each once read-only on a /tmp copy; show
the paths leave UNREGISTERED under `corpus/evidence/round47/c2-count.py --root <tmp> --list`.

Verdict: **done.** Four rows (one per instrument family) drafted; on the spliced /tmp copy all four
paths leave UNREGISTERED (`UNREGISTERED=25 → 21`, `REGISTERED=67/92 → 71/92`), `DANGLING=0`,
ENTRY_POINTS stays 92 = FLOOR. `C2` stays FAIL on the 21 paths outside my item. No lane file other
than this report was written.

Tree: `git -C <lane> archive master | tar -x -C /tmp/chousa-r47-ScribeGatesWaves/lane`, master =
`a15610a59aaeaf43b79ccc650acee4bd4da00341` (HEAD). `receipt-binding.py` needs git history, so it ran on
`git clone -q --no-local <lane> /tmp/.../clone` (HEAD `a15610a5…`). bash 5.3.20, Python 3.14.8, LANG en_US.UTF-8.

## Who names each path, which leg reaches it, gate or probe

| path | sha256 | leg | named by (lane, master) | role |
|---|---|---|---|---|
| mask-gate.sh | `ae7d4bfc7ac1d262590dd5014e8abdbbea102266551891b4910666116440e0cd` | check-named | `corpus/QUALITY.md:311` (crit 40 "Shown able to fail"); `corpus/evidence/round34/audit-set.json:274` (`bind-mask-9401`); `.ufo/waves/round-34/w1/ExecE2Counter.md:54`; `.ufo/waves/round-45/w2/RevRowR33.md:21` | **historical control**, does not gate: research-gate copy + CONFUSERS mask, built by `mk-mask-gate.py` |
| receipt-binding.py | `230441acc1103d350780507c36993d87d550ea4b6602a373ad081dcf744c5943` | check-named | `corpus/QUALITY.md:324` (crit 42 `Check:`); `corpus/evidence/round34/claims-a2.md:125`; `corpus/knowledge/claim-record-fields-r33.md:89`; `corpus/lessons/round-34.md:32`; `SCORECARD.md:1942` | **gates** QUALITY 42 |
| slen-probe.sh | `0938c4c21e9b4e311a6786204f954a6a7351e861c3597db665db0ce47988ce60` | check-named | `corpus/QUALITY.md:372` (crit 47 `Check:`); `corpus/knowledge/bash-local-expansion-r35.md:8,12,42,76`; `corpus/lessons/round-35.md:30`; `SCORECARD.md:2002` | **gates** QUALITY 47 (a probe used as a criterion check) |
| tools/mechanism-witness.py | `9f537bfde0dd53f2240af149e1b7a03fd0a0f372ee1fa1a32e94044115a252b3` | A (`tools/`), also SKILL outside Gates (`SKILL.md:635`) and dependence (`corpus/evidence/round35/c2-count.py:133` default `--battery`; `round36/c2-count.py:37`) | `corpus/evidence/round35/claims.md:70`, `round36/claims.md:106` | tool; **superseded** for per-record attribution by `tools/argv-witness.py` (r36 row `SKILL.md:99`) |

Leg attribution computed by importing the frozen counter's own `load_r46`/`existing_named`/`outside_gates`
on the /tmp tree (`/tmp/.../legs.py`, deleted):
```
.ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh  QUALITY
.ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py  QUALITY
.ufo/waves/round-35/repairs/slen-probe.sh  QUALITY
tools/mechanism-witness.py abc  SKILL-outside-Gates
NAMED_BY tools/mechanism-witness.py <- corpus/evidence/round35/c2-count.py
NAMED_BY tools/mechanism-witness.py <- corpus/evidence/round36/c2-count.py
```

**Finding F1 (row-parse defect, load-bearing).** `tools/mechanism-witness.py` already HAS a Gates row
(`SKILL.md:100`), but the counter splits on every `|`: the verdict cell `WITNESS=pass|fail|unparseable|timeout`
splits the row into 11 cells, so cell 4 is `` `WITNESS=pass`` with no `exit`, and the row registers nothing.
My row 4 below is a **replacement for line 100**, not an extra row; it carries no `|` inside any cell.
The same defect hits `SKILL.md:114` (`round24–27 counting instruments`, `\|` in the entry cell →
14 cells), which is why its round-24–27 paths stay UNREGISTERED. `ScribeGatesChecks` confirmed both splits.
Agreed split of work: my row 4 fixes line 100 (they will not draft a row for it); line 114 is outside both
our items and **goes to Main as an open row-repair item**. Scan over Gates rows 78–118: only lines 100 and 114
have ≠8 cells. Separately, rows 80–87 (`research-gate` verbs) have 8 cells but no `exit` word in cell 4
(they write `` `0` clean ``), so they register nothing under the r47 cell rule. `tools/research-gate.sh`
is registered only because other rows (e.g. round-41 counters) name it in an entry cell with `exit`. **[INFERENCE: harmless today; fragile.]**

## Runs (all on /tmp copies; verbatim, trimmed)

```
$ cd /tmp/.../lane; C1_TMP=… LC_ALL=C python3 corpus/evidence/round33/c1-count-v2.py --gate .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh --seed 4733 --receipt …/mask-s4733.json
TOPLEVEL_FIELD_MATCH=156/156          (all 15 classes full)        exit=0 elapsed=22s   receipt gate_rc=1
$ … python3 .ufo/waves/round-34/w1/ExecE2Counter/c1-count-v3.py --gate …/mask-gate.sh --seed 4733 --receipt …
TOPLEVEL_FIELD_MATCH=154/156
  S2_nested_confusers 4/6             misses: 2x truth=supported observed=invalid    exit=1 elapsed=22s
  (v3 counter sha256 bd81aeea199c460be3afbec0f15116b5ddfe8330b45f35b37568d1665e43d9cc)
$ bash .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh        → prints header … "Exit: 0 CLEAN | 1 DRIFT | 2 setup/usage"  exit=2

$ cd /tmp/.../clone; python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py . .ufo/waves/round-33
COMMITTED_GATE_BLOBS 48 / COMMITTED_WAVE_SH_BLOBS 457 / COMMITTED_BLOB_HASHES 491
UNBOUND .ufo/waves/round-33/measure/final/fz-90212.json b2c07eda…   (also fz-90213, fz-90214)
UNBOUND …/NoHarmCorpus33/c1-landed-seed34101.json fc08410e… ; …/c1-landed-seed34102.json 45d76b4f… ; …/ProbeTypes33/c1-landed-s4202.json 45d76b4f…
UNBOUND …/FuzzDiff33/full-90214.json, …/ProbeLongLines33/c1-v2-seed5187.json (45d76b4f…), …/ReviewC1Diff/c1-v2-s4117.json b808e9b5…
TOTAL_RECEIPTS 1060  TOTAL_WITH_GATE_HASH 975  TOTAL_BOUND 966  TOTAL_UNBOUND 9  TOTAL_UNBOUND_LANDED_FINAL 6  TOTAL_UNBOUND_OTHER 3  TOTAL_NO_GATE_HASH 85     exit=1
$ diff <committed census-round33.txt minus REPO lines> <this run>  → only the three blob-count lines differ (committed 40/175/210)
$ … receipt-binding.py . .ufo/waves/round-34
TOTAL_RECEIPTS 478  TOTAL_WITH_GATE_HASH 400  TOTAL_BOUND 390  TOTAL_UNBOUND 10  TOTAL_UNBOUND_LANDED_FINAL 0  TOTAL_UNBOUND_OTHER 10     exit=0
$ python3 …/receipt-binding.py      → "error: the following arguments are required: repo, receipts"  exit=2

$ TMPDIR=… bash .ufo/waves/round-35/repairs/slen-probe.sh tools/research-gate.sh      (gate 2cb04bdd…fc34)
SLEN_PROBE offsets=1 first=5          exit=0
$ … slen-probe.sh .ufo/waves/round-35/repairs/base-gate.sh                          (a6307edf…)
SLEN_PROBE offsets=0 first=           exit=1
$ … slen-probe.sh          → "line 16: $1: unbound variable"  exit=1
$ … slen-probe.sh /nonexistent → "slen-probe: gate not found: /nonexistent"  exit=2

$ LC_ALL=C python3 tools/mechanism-witness.py --gate tools/research-gate.sh --seed 4741 --tmp … --json …
WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)    exit=0 elapsed=2s  (json: gate_rc 1, drift true, entry lines chunk 1971 direct 1949, 2.52 s)
$ … mechanism-witness.py --gate .ufo/waves/round-34/w2a2/MutC2Keyed/ctl4-fixedkey.sh --seed 4741 …   (92ed87c9…)
WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)    exit=0
$ C2_TMP=… LC_ALL=C python3 corpus/evidence/round35/c2-count.py --gate tools/research-gate.sh --battery tools/mechanism-witness.py --seed 4741 --receipt …
WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass
  K1-python-exact  output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}
  K2-root-keyed    output=9/9 witness=fail stamps={'chunk': 0, 'direct': 1}      exit=0 elapsed=8s
$ python3 tools/mechanism-witness.py --gate /nonexistent → "mechanism-witness: gate not found: /nonexistent"  exit=2
```

Findings from the runs:
- **F2** `ctl4-fixedkey.sh` is **not** a discriminating control for the r35 witness (passes 9/9 on seed 4741);
  the discriminating controls are the K1/K2 engines that `corpus/evidence/round35/c2-count.py` builds itself.
  The self-test cell says so.
- **F3** QUALITY 42 (`corpus/QUALITY.md:327`) says round 33 lists "five wave-2 `c1-landed` receipts". Observed:
  three `c1-landed` receipts carry the landed label; `full-90214.json` and `c1-v2-seed5187.json` are
  the other two wave-2 UNBOUND rows with the same gate hashes, and they count as unlabelled. Wording drift only; the exit-1 claim holds.
- **F4** Existing row `SKILL.md:100` claims an xtrace file of ~310 MB per run. I did not measure the size.
  The run took 2.5 s; the replacement row drops the size figure and does not assert one.
- Observed `exit 1` on no-arg `slen-probe.sh` (from `set -u`), not exit 2; the row states that.

## Draft rows (verbatim; rows 1–3 go after `SKILL.md:118`, row 4 replaces `SKILL.md:100`)

```
| `round-33 shortcut-mask control` (r47 registration) | instrument | `bash .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh verify-claims <claims-file> --root DIR`, driven by `python3 corpus/evidence/round33/c1-count-v2.py --gate .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh --seed N --receipt OUT.json` | historical control, does not gate: a research-gate copy with the six `CONFUSERS` masked and nested `{...}`/`[...]` regex-stripped (built by `.ufo/waves/round-33/w2/L1ShortcutMask/mk-mask-gate.py`), cited by QUALITY 40 as the shortcut a fixed-list counter cannot kill; its own exits are the research-gate contract (`exit 0` CLEAN · `exit 1` DRIFT · `exit 2` setup/usage, bare invocation prints the header and exits 2); under the round-33 v2 counter it prints `TOPLEVEL_FIELD_MATCH=156/156` exit 0, which is the counter's miss, not a pass of the control | the per-seed confuser counter `python3 .ufo/waves/round-34/w1/ExecE2Counter/c1-count-v3.py --gate .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh --seed 4733` kills it: `TOPLEVEL_FIELD_MATCH=154/156` (`S2_nested_confusers 4/6`, two `supported` records observed `invalid`), exit 1 | measured on `git archive` of lane commit `a15610a59aaeaf43b79ccc650acee4bd4da00341` (wave-1 `ScribeGatesWaves`, `LC_ALL=C`, seed 4733): mask gate sha256 `ae7d4bfc…40e0cd`, gate_rc 1; v2 counter `cb354dd1…` 156/156 exit 0; v3 counter `bd81aeea…` 154/156 exit 1; committed receipts `mask-s3391.json`/`mask-s3392.json` (156/156) and round-34 `mask-s9401.json` (155/156) | verify-claims: zero writes; the counters write their `C1_TMP` temp dir and `--receipt` only; no network | chousa |
| `receipt-binding` census (QUALITY 42, r34; r47 registration) | check | `python3 .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py <repo> <receipts-dir> [--gate-path tools/research-gate.sh] [--waves-prefix .ufo/waves/] [--json-out PATH]` (repo must be a git checkout: it runs `git rev-list --all` and `git cat-file --batch`) | gates QUALITY 42: `exit 0` no UNBOUND receipt carries a landed/final label (`TOTAL_UNBOUND_LANDED_FINAL 0`; unlabelled `UNBOUND` lines are still listed) · `exit 1` at least one UNBOUND receipt under `measure/` or with `landed`/`final` in its name · `exit 2` argparse usage (`the following arguments are required: repo, receipts`) | `.ufo/waves/round-33` fails it: `TOTAL_UNBOUND 9` `TOTAL_UNBOUND_LANDED_FINAL 6` (`measure/final/fz-9021{2,3,4}.json` gate `b2c07eda…` plus three `c1-landed` receipts), exit 1; `.ufo/waves/round-34` passes: `TOTAL_RECEIPTS 478` `TOTAL_UNBOUND 10` `TOTAL_UNBOUND_LANDED_FINAL 0`, exit 0 | measured on a `git clone --no-local` of lane commit `a15610a59aaeaf43b79ccc650acee4bd4da00341` (wave-1 `ScribeGatesWaves`): tool sha256 `230441ac…5943`; `COMMITTED_GATE_BLOBS 48` `COMMITTED_WAVE_SH_BLOBS 457` `COMMITTED_BLOB_HASHES 491`; the round-33 `UNBOUND` lines and totals equal the committed `census-round33.txt` (its blob counts 40/175/210 are the round-34 history) | read-only; writes only `--json-out` when given; no network | chousa |
| `slen-probe` (QUALITY 47, r35; r47 registration) | check | `bash .ufo/waves/round-35/repairs/slen-probe.sh GATE` (GATE a research-gate copy such as `tools/research-gate.sh`; it extracts the gate's chunk-matcher block, sources it and calls `tok_span_offsets_chunk` directly with a decoy visible `span`) | gates QUALITY 47: `exit 0` `SLEN_PROBE offsets=1 first=5` (the matcher reads its span length from its parameter) · `exit 1` any other offset count (`SLEN_PROBE offsets=0 first=`, the coupled one-statement `local` form), or no argument (`set -u`: `line 16: $1: unbound variable`) · `exit 2` gate not found (`slen-probe: gate not found: PATH`) or the extracted block does not parse | the round-34 base gate `.ufo/waves/round-35/repairs/base-gate.sh` (`a6307edf…`) fails it: `SLEN_PROBE offsets=0 first=`, exit 1 | measured on `git archive` of lane commit `a15610a59aaeaf43b79ccc650acee4bd4da00341` (wave-1 `ScribeGatesWaves`): probe sha256 `0938c4c2…ce60`; landed gate `tools/research-gate.sh` `2cb04bdd…fc34` → `SLEN_PROBE offsets=1 first=5`, exit 0 | its own `mktemp -d` under `TMPDIR`, removed by its EXIT trap; no network | chousa |
| `mechanism-witness` (r35; r47 row repair) | tool | `python3 tools/mechanism-witness.py --gate PATH [--seed N] [--json OUT] [--tmp DIR]` | round-35 aggregate trace witness, superseded for per-record attribution by `tools/argv-witness.py` (r36); kept as the default `--battery` of `corpus/evidence/round35/c2-count.py` and the before-control of `corpus/evidence/round36/c2-count.py`: `exit 0` `WITNESS=pass OUTPUT=9/9` (chunk stamps at least the long-record count, gate exit 1 with DRIFT) · `exit 1` `WITNESS=fail`, `WITNESS=unparseable` (matcher entry lines not found), `WITNESS=timeout`, or output short of 9/9 · `exit 2` gate not found (`mechanism-witness: gate not found: PATH`) or temp-dir error | `python3 corpus/evidence/round35/c2-count.py --gate tools/research-gate.sh --battery tools/mechanism-witness.py --seed 4741` → `WITNESS_SEPARATED=2/2 OUTPUT_EQUIV=2/2 LANDED_WITNESS=pass`, exit 0: keyed engines K1-python-exact and K2-root-keyed print output 9/9 but `witness=fail` (`chunk=0`); NOT killed: `.ufo/waves/round-34/w2a2/MutC2Keyed/ctl4-fixedkey.sh` (`WITNESS=pass OUTPUT=9/9`, exit 0, seed 4741); limits per `corpus/evidence/round35/claims.md` erratum (aggregate threshold, per-record coverage not measured) | measured on `git archive` of lane commit `a15610a59aaeaf43b79ccc650acee4bd4da00341` (wave-1 `ScribeGatesWaves`, `LC_ALL=C`, seed 4741): tool sha256 `9f537bfd…52b3`; landed gate `2cb04bdd…fc34` → `WITNESS=pass OUTPUT=9/9 STAMPS chunk=9 direct=1 (long records=8)`, exit 0, matcher entry lines chunk 1971 / direct 1949, 2.5 s | its own temp dir (`--tmp`, `WITNESS_TMP` or `TMPDIR`) holding the xtrace file, removed on exit; writes `--json` when given; no network | chousa |
```
Row check (split on `|` the counter's way): each row `cells 8`, `exit` in cell 4, starts `| `, ends ` |`.

## Registry effect (frozen counter, run from the /tmp lane)

```
$ python3 corpus/evidence/round47/c2-count.py --root /tmp/…/lane --list          (unmodified archive)
UNREGISTERED_PATH .ufo/waves/round-33/w2/L1ShortcutMask/mask-gate.sh
UNREGISTERED_PATH .ufo/waves/round-34/w1/ExecE4Census/receipt-binding.py
UNREGISTERED_PATH .ufo/waves/round-35/repairs/slen-probe.sh
… UNREGISTERED_PATH tools/mechanism-witness.py
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7)  FLOOR=92  GATES_ROWS=36  REGISTERED=67/92
UNREGISTERED=25  DANGLING=0  MISMATCHES=25  C2=FAIL   exit=1
$ python3 corpus/evidence/round47/c2-count.py --root /tmp/…/lane-rows --list     (line 100 replaced, rows 1–3 after 118)
ENTRY_POINTS=92 (abc=84 dependence=+1 check_named=+7)  FLOOR=92  GATES_ROWS=39  REGISTERED=71/92
UNREGISTERED=21  DANGLING=0  MISMATCHES=21  C2=FAIL   exit=1
$ diff <before --list> <after --list>
1,3d0 < …mask-gate.sh  < …receipt-binding.py  < …slen-probe.sh ;  25d21 < tools/mechanism-witness.py
```
The before run equals `corpus/evidence/round47/controls/c2-before.txt` tree A. The 21 remaining paths
(round-38/39/41 base gates, round24–27 instruments, round29/30/32 checks, the round-47 counters) belong to sibling items.

## Limits, tooling, scope
- Every value above was run once in this seat, except where a committed receipt is cited by path.
  I did not re-derive the per-record truth of the witness, and did not re-check row truth beyond the observed runs (c2-count docstring: "row truth stays a reader's check").
- `/usr/bin/time` is absent, so the first mask and witness launches exited 127 before running. I re-ran them with `date` timing.
  Nothing was installed (pacman is paused; not needed). The Read tool refused small files (5.9 KB, 13.7 KB)
  as "exceeds 100000 characters", so I read those through shell slices.
- Out of scope, not done: editing lane `SKILL.md` (rows are drafts), fixing `SKILL.md:114`, any fetch or network use.
- Scratch `/tmp/chousa-r47-ScribeGatesWaves/` (archive, clone, spliced copy, receipts) was deleted before finishing.
- By the end of my run, `git status` showed working-tree `M` on `corpus/evidence/round47/c2-count.py` and
  `tools/inference-ground.py`. Another seat made those edits; I did not. All values above are measured on
  committed master `a15610a5…` and need a re-run once those edits land.
