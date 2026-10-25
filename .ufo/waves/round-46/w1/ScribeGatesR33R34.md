# ScribeGatesR33R34 — Gates rows for r33 D2/D5 and r34 C3, plus the r30 harness

Seat: `L1Chousa46.ScribeGatesR33R34` (leaf). Lane commit at every run and write:
`c2f0e9d100c0d46633a6277b2fd51d2ac99678eb` (`git rev-parse HEAD`, lane root). No network, no
lane writes outside this file, no `git`/`jj` mutation, no tool installs.

## Item and inputs

Draft `## Gates` rows for `corpus/evidence/round33/d2-census.py`,
`corpus/evidence/round33/no-name-signals.sh`, `corpus/evidence/round34/self-audit.py`,
`corpus/evidence/round30/qr_harness.py`; decide the standing of the incidentally named `qris`.
Read first: `corpus/evidence/round46/claims.md` (C2 is this work), `SKILL.md:75-133` (row
conventions), `corpus/lessons/round-33.md:24,27`, `corpus/lessons/round-34.md:88`,
`SCORECARD.md:1859,1884,1947-1957`, `corpus/lessons/round-45.md:220` (D8).

What each instrument measured: `d2-census.py` is D2's *counting command* — it answers "how many
committed round-32 C1 receipts bind gate `10f2fe12`" and prints `21`, the number the round-33
correction put in `SCORECARD.md` (`lessons/round-33.md:24`; `SCORECARD.md:1859`).
`no-name-signals.sh` is D5's hygiene scan — it exits 1 on round 32 because
`w2/RerunC1b.md:31` quotes `pkill -x sleep` (`lessons/round-33.md:27`; `SCORECARD.md:1884`).
`self-audit.py` is round-34 attempt-2 C3 — a counted self-assessment audit over
`audit-set.json` with `audit-dispositions.md` (`lessons/round-34.md:88`; `SCORECARD.md:1957`);
D8 (`lessons/round-45.md:220`) named it as the verifier the frozen entry-point pattern missed.
`qr_harness.py` is the round-30 loopback harness — an internal child bootstrap that the
round-30 counters import (`SKILL.md:88`), not a standalone verdict-producing entry point.

## Decision on `qris`

No row, and no superseded note claiming a successor: `qris` names nothing in the lane. The
string occurs exactly once in the whole tree, in the dispatch generator itself:
`grep -rn "qris" --include=*.md --include=*.py --include=*.sh .` →
`.ufo/waves/round-46/gen-w1-spec.py:115`. It is a truncation of `qr_harness`, whose family is
already registered twice after this draft (the new `qr-harness` row and the pinned-values cell
of `quote-reopen` round-30 counters, `SKILL.md:88`). Writing a `qris` row would register a name,
not a path — exactly the row-truth gap C2 names as its limit, so it is recorded here instead.

## Runs (read-only; every one executed in this seat)

`python3 corpus/evidence/round33/d2-census.py --lane .` (exit **0**; default `--gate 10f2fe12`)
```
census lane: .
json paths listed by `git ls-files .ufo/waves/round-32 | grep json`: 1150 (1134 .json, 14 .jsonl skipped)
json objects parsed: 1107 | non-object/undecodable: 27 | index paths absent from HEAD: 0
C1 receipts anywhere in round-32 (label ^APPEND_SERIALIZED): 255
C1 receipts on gate 10f2fe12: 21
```
`bash corpus/evidence/round33/no-name-signals.sh .ufo/waves/round-32` (exit **1**)
```
HIT .ufo/waves/round-32/w2/RerunC1b.md:31 [doc; pkill] so it is counted as a concurrency-only pair. My cleanup `pkill -x sleep` in an early probe also
no-name-signals.sh: 1 hit(s), 480 candidate file(s), 1525 scanned file(s), 0 large file(s) skipped (> 16777216 B)
no-name-signals.sh: RESULT DIRTY (exit 1)
```
`bash corpus/evidence/round33/no-name-signals.sh --code-only tools/` (exit **0**)
```
no-name-signals.sh: 0 hits, 3 candidate file(s), 8 scanned file(s), 0 large file(s) skipped (> 16777216 B)
no-name-signals.sh: RESULT CLEAN (exit 0)
```
`python3 corpus/evidence/round34/self-audit.py` (lane root, defaults; exit **0**, 67 lines)
```
SET_SHA256=a77e4dc2e7d111f8cdb52eef37b5fc1b08c8df1b53925b8a849da9112b953390
AUDIT id=gate-head-digest MISMATCH sha256: digest 2cb04bddfd5601d7 != pinned a6307edf687ac0fb
AUDIT id=audit-tool-digest MISMATCH sha256: digest e9b0c93fea28dd96 != pinned 22a6822ca79f7f5e
SELF_AUDIT_MISMATCHES=2
  mismatch: gate-head-digest (NO DISPOSITION)
  mismatch: audit-tool-digest (dispositioned: superseded by audit-tool-digest-v3 ...)
SELF_AUDIT_UNDISPOSITIONED=1
```
60 `AUDIT id=… ok` lines; `audit-set.json` holds 62 checks (`checks=62`).

`python3 corpus/evidence/round30/qr_harness.py` (bare, exit **2**, prints `__doc__`).
Probe in `/tmp`: `… qr_harness.py boot MAP.json tool_ok.py verify --items items.tsv --registry registry.md`
→ `QUOTE_REOPEN	X1	VERBATIM`, exit **0**; same with `tool_usage.py` (returns 2) → exit **2**;
re-running the first map a second time → `FileNotFoundError: … map.json`, exit **1** (the boot
unlinks its map by design). Probe files were mine and lived only under `/tmp`.

Registration dry-run (the point of the draft): rows inserted after `SKILL.md:77` into a /tmp
copy, then `python3 corpus/evidence/round46/c2-count.py --skill /tmp/…/SKILL-dryrun.md --list`
```
ENTRY_POINTS=72 (tools=8 counters=50 named=70)
GATES_ROWS=34
REGISTERED=58/72
UNREGISTERED=14
C2=FAIL
```
Baseline without the rows (same command, real `SKILL.md`): `GATES_ROWS=30 REGISTERED=55/72
UNREGISTERED=17`, exit 1. Delta: +4 rows, +3 registered — the three named paths leave the
unregistered list (`d2-census`, `no-name-signals`, `self-audit`; `grep -c` for those names in
the dry-run output = 0); `qr_harness.py` was already covered by `SKILL.md:88`, so its row adds
contract, not coverage. The other 14 unregistered paths are outside this item.

## Draft rows (verbatim; 9 pipes ⇒ 8 cells, every row carries `exit`)

```
| `no-name-signals` (r33 D5) | check | `bash corpus/evidence/round33/no-name-signals.sh [--code-only] [--exclude PATH] [--max-bytes N] DIR...` | `exit 0` clean (`RESULT CLEAN`) · `exit 1` hits listed, one `HIT path:line [code-or-doc; cats] text` per hit (`RESULT DIRTY`) · `exit 2` usage or I/O error (`RESULT INCOMPLETE` / `RESULT DIRTY-INCOMPLETE`) | dirty control `.ufo/waves/round-32` → `1 hit(s)` at `w2/RerunC1b.md:31 [doc; pkill]`, exit 1; clean control `--code-only tools/` → `0 hits, 3 candidate file(s), 8 scanned file(s)`, exit 0 | measured at lane commit `c2f0e9d100c0d46633a6277b2fd51d2ac99678eb`, tool sha256 `453388d0ed6b1b567162614d3430192d26724aa08ee374422e0cc605b969cb95`: `1 hit(s), 480 candidate file(s), 1525 scanned file(s), 0 large file(s) skipped (> 16777216 B)`; reproduces `corpus/lessons/round-33.md:27` | `mktemp -d "$TMPDIR/no-name-signals.XXXXXX"`, removed by its EXIT trap; lane read-only | chousa |
| `d2-census` (r33 D2) | census | `python3 corpus/evidence/round33/d2-census.py [--lane DIR] [--gate PREFIX]` (defaults `$LANE` or `.`, gate `10f2fe12`) | `exit 0` census printed — a census, never a verdict · `exit 1` only an uncaught Python error (no defined verdict) · `exit 2` argparse usage error | reproduction control: `C1 receipts on gate 10f2fe12: 21` matches `corpus/lessons/round-33.md:24` and `SCORECARD.md:1859`; exclusions stay visible as `14 .jsonl skipped` and `27 non-object/undecodable`; a receipt whose `label` does not begin `APPEND_SERIALIZED` is not counted (source read, no mutant run) | measured at lane commit `c2f0e9d1…`, tool sha256 `fa6d963394075069dea2e9101feed202b47c1f8dab5ca89ce615383f83fc1cda`: `json paths listed … 1150 (1134 .json, 14 .jsonl skipped)`, `json objects parsed: 1107 … index paths absent from HEAD: 0`, `C1 receipts anywhere in round-32 …: 255`, `C1 receipts on gate 10f2fe12: 21` | read-only — committed `HEAD:` blobs through one `git cat-file --batch`, so a dirty worktree cannot move the count | chousa |
| `self-audit` (r34 attempt-2 C3) | census | `python3 corpus/evidence/round34/self-audit.py [--set PATH] [--lane DIR] [--dispositions PATH]` (defaults `corpus/evidence/round34/audit-set.json`, `.`, `corpus/evidence/round34/audit-dispositions.md`) | `exit 0` whenever the set was readable, whatever K is — it counts, it does not gate: prints `SELF_AUDIT_MISMATCHES=K` then `SELF_AUDIT_UNDISPOSITIONED=U` · `exit 1` uncaught error · `exit 2` argparse usage error | drift control is the live tree: `gate-head-digest` mismatches (`digest 2cb04bddfd5601d7 != pinned a6307edf687ac0fb`) → `SELF_AUDIT_UNDISPOSITIONED=1`, so the round-34 C3 predicate (`=0`) does not hold at HEAD while the exit stays `0` — the D8 reason this row exists | measured at lane commit `c2f0e9d1…`, tool sha256 `e9b0c93fea28dd96e9558398c6703306294961548edb8895aee267c1186f7c47`, `SET_SHA256=a77e4dc2e7d111f8cdb52eef37b5fc1b08c8df1b53925b8a849da9112b953390`, 62 checks: `SELF_AUDIT_MISMATCHES=2`, `SELF_AUDIT_UNDISPOSITIONED=1`, 60 `ok` lines; `audit-tool-digest` dispositioned (superseded by `audit-tool-digest-v3`), `gate-head-digest` NO DISPOSITION | read-only — `git show HEAD:<path>` reads; writes nothing | chousa |
| `qr-harness` (r30) | harness | `python3 corpus/evidence/round30/qr_harness.py boot MAP.json TOOL.py verify --items X --registry Y` (child bootstrap; bare invocation prints `__doc__` and exits 2; parent helpers `run_tool` and `Server` are imported by `corpus/evidence/round30/c1-count.py` and `c2-count.py`) | candidate's `main(argv)` return becomes the exit (`os._exit(rc)`, non-int → `2`); bare invocation `exit 2`; missing map `exit 1` (`FileNotFoundError`, observed) · verdict lines `QUOTE_REOPEN` tab-separated on stdout; an unrouted destination raises `ConnectionRefusedError(111, "harness: unrouted destination")` | probe candidate returning `0` → `QUOTE_REOPEN X1 VERBATIM`, exit `0`; probe candidate returning `2` → exit `2`; both from a /tmp workdir; the round-30 counters' own controls (`QUOTE_REOPEN_HEADLESS_MATCH=106/106`, `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`) were not re-run here | measured at lane commit `c2f0e9d1…`, tool sha256 `e2be0dd16da5b2bf03430772831763e56c6ff6dd6a44063bb05c909b284f50d4`; the batch's map file is unlinked at boot (the candidate never sees it), so each boot needs its own map — observed | the map's `log` path only (JSONL resolve/connect records) plus `__pycache__` beside the imported candidate; unlinks the map; loopback 127.0.0.1 server, no egress | chousa |
```

## Findings

1. **`self-audit.py` no longer holds its own round-34 predicate.** `SELF_AUDIT_UNDISPOSITIONED=1`
   at HEAD: `gate-head-digest` pins `a6307edf` (the round-34 landed gate) while the committed
   gate is `2cb04bddfd`. Exit is still `0` because the tool counts rather than gates — the exact
   shape D8 flagged. Its row therefore states the observed `=1`, not the round-34 `=0`.
   `audit-tool-digest` is dispositioned; `gate-head-digest` is not.
2. **`qr_harness.py` is a harness, not an entry point.** Bare invocation is exit 2; its real
   contract is `boot MAP TOOL verify …`, the child's return becomes the process exit, and the
   map file is deleted on boot, so a batch cannot reuse one map (observed `FileNotFoundError`,
   exit 1 — an exit code its header does not document for that case).
3. **`__pycache__` beside the candidate.** `importlib` writes `__pycache__` next to the imported
   candidate; safe only because counters copy the candidate into a temp dir. Noted in the
   harness row's write scope.
4. `no-name-signals.sh` fails closed on prose by design (the D5 disclosure itself is a hit), so
   the row's self-test records both the dirty and the clean control I ran.
5. Rows cover registration, not row truth — C2's named limit; the dry-run shows +3 coverage and
   nothing about whether a row's stated values are right.

Out of scope, untouched: the other 14 unregistered entry points, `tools/inference-ground.py`,
the two staged C3 entries, `SCORECARD.md`, `SKILL.md` itself. The rows above are a proposal for
the executor that owns the `SKILL.md` edit.

No installs, no upgrades, no pacman. Scratch `/tmp/chousa-r46-ScribeGatesR33R34/` removed.
