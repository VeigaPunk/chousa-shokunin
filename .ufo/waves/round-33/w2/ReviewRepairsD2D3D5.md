# ReviewRepairsD2D3D5 — re-run of D2 census, D3 header check, D5 signal check (round-33 wave 2)

Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`, tip `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`
(`git log -1 --format=%H`), landed gate `tools/research-gate.sh` SHA-256
`94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e` (`sha256sum`, matches landed hash).
No `c1-count-v2.py` runs by this seat → kill-rule receipt obligation not triggered. No installs.
Artifacts: `.ufo/waves/round-33/w2/ReviewRepairsD2D3D5/jq-recount.txt` (255 rows, `gate_prefix\tpath`).

## D2 — receipt census (`corpus/evidence/round33/d2-census.py`)

Command: `python3 corpus/evidence/round33/d2-census.py --lane /home/vgpnk/Projects/shokunin/chousa-shokunin` → exit 0.

Output (verbatim key lines):
- `json paths listed by git ls-files .ufo/waves/round-32 | grep json: 1150 (1134 .json, 14 .jsonl skipped)`
- `json objects parsed: 1107 | non-object/undecodable: 27 | index paths absent from HEAD: 0`
- `C1 receipts anywhere in round-32 (label ^APPEND_SERIALIZED): 255`
- `C1 receipts on gate 10f2fe12: 21`
- `all gates seen` table: `10f2fe12   21   <- target`, `f4731885    3`

Expected 21 / 3 → matches.

Independent verification (jq over committed blobs, not the census code):
`git ls-files .ufo/waves/round-32 | grep json | grep '\.json$'` → 1134 paths; per path
`git show HEAD:$p | jq -r 'select(type=="object") | select((.label|type)=="string") |
select(.label|startswith("APPEND_SERIALIZED")) | (.gate_sha256|tostring|.[0:8])'` → 255 rows
(full TSV in `ReviewRepairsD2D3D5/jq-recount.txt`). Counts: `10f2fe12`=21 (same 21 paths the
census lists), `f4731885`=3 (`measure/final/c1-s3210{1,2}.json`, `w2/RerunC1b/rerunc1b-fs-tmpfs.json`),
all other gates identical to the census table. Census semantics verified: contents read from
`HEAD:` blobs (worktree edits cannot shift the count), `label` must be a string with prefix
`APPEND_SERIALIZED` (d2-census.py:106-107), gate key is `gate_sha256` truncated to 8 (:110).
The 2 listed paths that are neither `.json` nor `.jsonl` are `w1/MutC1CounterB/{counter,gate}-json-object.patch`
(name contains "json"; correctly outside both buckets: 1134+14+2=1150). **HOLDS.**

## D3 — battery revision header (QUALITY.md:293-298)

Check `awk '/^=== RUN/{exit} /gate_sha256=/{g=1} /lane_revision=/{r=1} END{print (g&&r)?"HEADER_OK":"HEADER_MISSING"}'`:

- `.ufo/waves/round-32/measure/final/battery.out` → `HEADER_MISSING` (expected; `grep -n
  'gate_sha256\|lane_revision\|=== RUN'` on the file returns nothing — fields absent entirely,
  not merely misplaced). Head is bare result rows (`EXEMPT_AUDIT_MATCH=132/132` first line).
- `.ufo/waves/round-33/measure/battery-candidate/battery.out` → `HEADER_OK`; first lines carry
  `# round-33 W1 no-harm battery (D3 revision-bound header)`, `lane_revision=eb179ec3…`,
  `gate_sha256=52f07c74…` before any `=== RUN`.
- `.ufo/waves/round-33/w1/ExecNoHarmBase33/battery-base.out` → `HEADER_OK`;
  `lane_revision=e3e24ec8…`, `gate_sha256=f4731885…` (base gate correctly named).
- Emitter `w1/ExecNoHarmBase33/battery.sh:54-58` prints header lines before all result rows
  (`printf` of `# round-33 W1 no-harm battery`, `lane_revision=`, `gate_sha256=`).

**HOLDS** — fail/pass demonstrations both reproduce.

## D5 — signals by name (`corpus/evidence/round33/no-name-signals.sh`)

`bash corpus/evidence/round33/no-name-signals.sh .ufo/waves/round-32` → **exit 1** (expected).
1 hit: `.ufo/waves/round-32/w2/RerunC1b.md:31 [doc; pkill]` — the report's own prose quoting
its past `pkill -x sleep` cleanup (the documented D5 incident, lessons/round-32-verifier-spotcheck
.md:168-169). Classification: prose describing an executed signal; `[doc]` kind is correct
(fail-closed on prose per script header lines 22-26; `--exclude` is the adjudication path).

`bash corpus/evidence/round33/no-name-signals.sh .ufo/waves/round-33/w1` → exit 1, **47 hits**.
Breakdown — none is a live command in a tool that runs:

- `w1/ExecD5Check/fixtures/dirty/` (14 hits): inert self-test fixtures. `scripts/run.sh:3-5`
  `[code; …]` are literal `pkill -f`, `killall`, `kill -TERM $(pidof python3)` lines inside a
  fixture script that exists only to be flagged (ExecD5Check.md documents it as the dirty-fixture
  battery); `reports/seat.md:2-11`, `data/receipt.json:1`, `fixtures/names/*`, `fixtures/prose/*`
  are synthetic text. Not executed — fixtures have no runner; they are scanned bytes.
- `w1/ExecD5Check/no-name-signals.sh` (10 hits `[code]`): the checker's own committed copy —
  regex literals and doc lines flag themselves. Documented self-hit; `--exclude` adjudicates.
- `w1/ExecD5Check.md` (10 hits `[doc]`): prose quoting the rule, the fixture table, and the
  round-32 incident (`pkill -x sleep` reference at :5, :73).
- `w1/AuditC1Truth.md:16`, `w1/ExecD1CounterV3.md:120`, `w1/ScribeQuality33.md:4`,
  `w1/ScribeQuality33/quality.md:40-41` (8 hits `[doc]`): prose attestations quoting the rule
  ("no `pkill`/`killall`/`pgrep`-based kills") or citing the D5 incident.

Real signals by name outside inert fixtures: **zero**. Every `[code]` hit is inside
`ExecD5Check/` (fixtures + the script copy). All other hits are `[doc]` prose, which the script
documents as intentionally indistinguishable and fail-closed. The D5 check itself operates as
specified: exit 1 lists hits with kind tags; exit-0 path verified earlier on `tools/`
(QUALITY.md:305). **HOLDS.**

## Residual risk / limits

- D5 documented limits stand (script header :28-30): aliasing, token concatenation, `command
  pkill`, busybox, SSH-wrapped kills, multi-line pipelines evade detection — inspected lines only.
- Census counts committed `HEAD` bytes; a receipt tracked but modified uncommitted would still
  count the committed version (correct per D2's standard; 0 index-absent paths seen).
- I ran no `c1-count-v2.py` (kill-rule seeds/receipts not applicable to this ticket).

## Verdict

D2 HOLDS (21/3 reproduced by census and independent jq). D3 HOLDS (HEADER_MISSING on round-32,
HEADER_OK on both round-33 battery outputs; emitter verified). D5 HOLDS (round-32 exit 1 with the
expected prose hit; w1 exit 1 with 47 hits, all prose citations or inert self-test fixtures — no
real signal-by-name in live artifacts).
