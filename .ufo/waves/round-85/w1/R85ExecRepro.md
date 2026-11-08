# R85ExecRepro — lane chousa round 85 reproduction (C1 K1, C2 K1, C2 K4 legs)

Seat: `R85ExecRepro` (leaf executor). Root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Revisions: base `43c3f7284eee4889cdcc6ac1626573f6579cd533`; freeze `5d0b94139ae8baf60d6f630715bc495f0a93b448`;
landing `64803d33362f50cf9094e91fc3a4a07216c563ca` (attacked bytes).
Scratch: `/fast/scratch/hyaku/chousa-r85/R85ExecRepro/` (deleted before yield; every cited receipt copied to
`.ufo/waves/round-85/w1/R85ExecRepro/` first).
Tools: `python3` 3.14.8, `git` 2.56.0 (system; no installs — nothing needed beyond the stdlib).

## (a) Instrument identity — all 6 pins MATCH at landing

Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 64803d33362f50cf9094e91fc3a4a07216c563ca:<path> | sha256sum`
Receipt: `.ufo/waves/round-85/w1/R85ExecRepro/a-pins-sha.txt`.

| path | expected (instrument-pins.txt) | got at landing | verdict |
|---|---|---|---|
| `corpus/evidence/round85/gate-records-r85.py` | `62496d36…c3a1d22` | `62496d36…c3a1d22` | MATCH |
| `corpus/evidence/round85/depth-r85.py` | `8ff164eb…b3724` | `8ff164eb…b3724` | MATCH |
| `corpus/evidence/round85/c2-positives.tsv` | `8c089828…f3c6` | `8c089828…f3c6` | MATCH |
| `corpus/evidence/round85/base-knowledge.txt` | `b2c21b25…5da` | `b2c21b25…5da` | MATCH |
| `corpus/evidence/round85/claims.md` | `080ded8f…b7a5` | `080ded8f…b7a5` | MATCH |
| `tools/gate-records.py` | `2de79722…03beb` | `2de79722…03beb` | MATCH |

No mismatch. [INFERENCE: none needed — direct byte comparison.]

## (b) BEFORE / AFTER — both predicates reproduce

Pristine base `43c3f728` contains **no** `corpus/evidence/round85/` directory at all (verified:
`git ls-tree -r --name-only 43c3f728 -- corpus/evidence/round85/` → empty). Per seat instruction, the
before-run carried the two counters **and** their two frozen data files (`c2-positives.tsv`,
`base-knowledge.txt`) byte-exactly from landing `64803d33` into the base tree; the lane data the counters
read (`corpus/SOURCES.md`, `corpus/evidence/round57/refetch.tsv`, `corpus/captures/`, lesson files,
knowledge entries) are each revision's own bytes. Copied shas verified equal to the pins (gate `62496d36…`,
depth `8ff164eb…`, tsv `8c089828…`, base-knowledge `b2c21b25…`).

Depth (C2):
- base: `DEPTH_R85 entries=0 ok_entries=0 rows=0 located_quotes=0 fresh_sources=0`, `DEPTH_R85=FAIL`, **rc 1** — matches the seat's expected before-value.
- landing: `ENTRY provenance-recording-r85.md ok=yes rows=6 quotes=7/7 fails=-`,
  `DEPTH_R85 entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3`, `DEPTH_R85=PASS`, **rc 0** — matches the claims predicate (`entries=1 ok_entries=1`, `rows≥6`, `located_quotes≥7`, `fresh_sources=3`).
Receipt: `b-depth.txt`.

Gate (C1):
- base: `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=342/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=0/1`,
  `GATE_RECORDS_R85=FAIL`, **rc 1** — 12 `WRONG_CODE … D4-non-timestamp-fetched … expected=PARSE got=REFETCH`
  (one per frozen admit: S203, S204, S205, S206, S207, S008, S209, S210, S211, S028, S082, S083) — the pre-repair
  calendar-invalid `fetched=2026-13-40T00:00:00Z` was misclassified as REFETCH instead of PARSE, and the setup leg fails.
- landing: `TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=354/354 EXPECTED_CODE=354/354 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1`,
  `GATE_RECORDS_R85=PASS`, **rc 0** — matches the claims predicate verbatim, including `354/354`, `RC=4/4`, `SETUP=1/1`.
Receipts: `b-gate-base.txt`, `b-gate-landing.txt`.

Repair diff confirmed (base-tool vs landing-tool `tools/gate-records.py`): added `import datetime` +
`_valid_ts` (calendar `fetched` via `strptime`); REFETCH admit row `http 2xx` → `http == "200"` and unreach
`success` `startswith("2")` → `== "200"`; non-git `--repo` → `GATE_RECORDS_ERROR …` on stderr + exit 2
(before: falls through to per-record `FAIL REV,LINE`, exit 1).

## (c) Control legs re-run — all three named legs byte-identical to their receipts

Protocol: each control was re-run at the bytes committed for it — freeze tree `5d0b9413` + freeze counter
(shas `931b5ed7…06afb`, `516345e7…259dcf`) — because the control receipts carry the freeze-era forgery
total `378` (see finding F1 below; a landing-counter re-run cannot reproduce it, by construction).

1. `c1-k0-donothing`: `python3 -B <freeze>/corpus/evidence/round85/gate-records-r85.py --root <freeze>
   --repo <lane> --tool <base-tool from 43c3f728:tools/gate-records.py, sha 6e7a76f8…> --work <scratch>` →
   output **byte-identical (38 lines)** to `controls/receipts/c1-k0-donothing.txt` once the harness's
   trailing `gate rc=1` line is stripped; stripped receipt ends `GATE_RECORDS_R85=FAIL` and the rerun exits 1.
   Summary: `… FORGED_REFUSED=354/378 EXPECTED_CODE=342/378 … SETUP=0/1` — matches. Receipt: `c1-k0-donothing-rerun.txt`.
2. `c2-d0-donothing`: `python3 -B <freeze>/corpus/evidence/round85/depth-r85.py --root <freeze>` →
   **byte-identical** to `controls/receipts/c2-d0-donothing.txt` (2 lines + harness `depth rc=1`).
   Also identical when the landing counter runs on the base tree (`b-depth.txt` base half). Receipt: `c2-d0-freeze.txt`.
3. `c1-accept-stub` (seat's `c1-accept-stub`; claims file calls it `c1-f1-stub-accept`): stub bytes are
   **not committed** (only receipts). Reconstructed from the receipt's signature — a tool that exits 0 with
   no per-record output yields exactly `POSITIVE=0/15 FRESH_POSITIVE=0/5 FORGED_REFUSED=0/378 … EMPTY_REFUSED=0/1 RC=2/4 SETUP=0/1`
   — and the rebuilt stub reproduces `c1-accept-stub.txt` **byte-identically** (380 lines + harness trailer).
   Same signature check for `c1-refuse-stub.txt` (exit-1/no-output stub): also byte-identical. Receipts:
   `c1-accept-stub-rerun.txt`, `c1-refuse-stub-rerun.txt`.

Contrast run (documented, not the control protocol): landing counter + base tool on the landing tree gives
`FORGED_REFUSED=354/354 EXPECTED_CODE=342/354 … SETUP=0/1 FAIL rc 1` (12 D4 WRONG_CODEs, 0 M19/M20 NOT_REFUSEDs).
Receipt: `c1-k0-landing-counter.txt`.

### F1 — measurement note (not a kill of either claim): freeze-era forgery total 378 vs landing 354

The 24-forgery delta is `M19-http-arabic-indic` + `M20-curl-rc-arabic-indic` on the 12 admit positives
(stamping `http`/`curl_rc` onto admit lines, which carry neither key). The **freeze** counter's `kv_set`
returns the line unchanged when the key is absent, so each "forgery" was byte-identical to its positive and
every tool (correct ones included) "NOT_REFUSED" it — 24 NOT_REFUSED lines in the freeze receipts for
non-forgeries. `git diff 02df67db 64803d33 -- corpus/evidence/round85/gate-records-r85.py` shows the
landing only adds `if not re.search(...): return None` in `kv_set`, which drops those 24 non-forgeries from
the scored set (`378 → 354`). Evidence: `grep -c M19|M20` = 24 in `c1-k0-donothing.txt` and
`c1-accept-stub.txt`, 0 in the landing-counter run; the landed counter file/claims/pins all agree on 354
and the claims state the count only as "N/N (computed from the classes; the counter prints it)", i.e. the
counter is authoritative. The landing counter still refuses all 354 real forgeries; the fix removes
counter-bug artifacts, it does not hide a tool failure. I do **not** fire C1 K1/K2 on F1.
Separately, K4's whitelist control receipt (`c1-whitelist-stub.txt`) is byte-identical (minus trailer) to
`c1-refuse-stub.txt`, and no whitelist stub bytes are committed, so that control cannot be re-validated
from committed bytes; I did not re-run it as a named leg (this seat names only k0, c2-d0, accept-stub).
My independent whitelist reconstruction (accept the 15 byte-exact lines, refuse everything else) scores
`POSITIVE=15/15 FRESH_POSITIVE=2/5 … GATE_RECORDS_R85=FAIL rc 1`, i.e. it fails on the fresh leg as the
claims require — but this is a reconstruction, not a re-run of the committed control; receipts in scratch
only (`c1-whitelist-rerun.txt`), not copied (unreproducible probe).

## (d) C1 predicate through the public CLI at landing

`python3 tools/gate-records.py verify --root <landing-tree> --repo <lane> corpus/lessons/round-85.md`
(cwd `/home/vgpnk/Projects/shokunin/chousa-shokunin`) →
`GATE_RECORD corpus/lessons/round-85.md:14 S215 OK`, `:15 S026 OK`, `:16 S024 OK`,
`GATE_RECORDS files=1 records=3 ok=3 fail=0`, **exit 0**. Receipt: `d-c1-cli-exact.txt`.
(From fleet-root cwd the relative FILE resolves outside the tree and prints
`GATE_RECORDS_ERROR missing corpus/lessons/round-85.md` rc 2 — a host-cwd artifact of this seat's cwd,
not a tool defect; from the tree cwd the same command gives the same 3-OK result.)

## (e) Exit contract — all four expectations met (landing tool; base tool contrast)

| case | landing tool | base tool | expected |
|---|---|---|---|
| file with no record | `records=0`, rc **1** | `records=0`, rc **1** | 1 |
| one OK + one FAIL (`CAPTURE_SHA`) | `ok=1 fail=1`, rc **1** | — (same path) | 1 |
| missing FILE argument | argparse usage on stderr, rc **2** | same, rc **2** | 2 |
| non-git `--repo` (rev record) | empty stdout, stderr `GATE_RECORDS_ERROR not a git repo: <dir>`, rc **2** | `FAIL LINE,REV`, rc **1** (old behavior) | 2 + `GATE_RECORDS_ERROR` on stderr |

Also checked: nonexistent FILE path → stderr `GATE_RECORDS_ERROR missing <file>`, rc 2 (not via argparse).
Receipts: `e-exit-contract.txt`, `e-stderr-final.txt`.

## Verdicts

- **C1 K1 (predicate at landing): HELD.** Counter prints the predicate line verbatim (`354/354`, `RC=4/4`, `SETUP=1/1`, `GATE_RECORDS_R85=PASS`, rc 0); before-run fails with `SETUP=0/1` + 12 D4 wrong-codes + rc 1. Public CLI gives 3 OK, exit 0. Controls re-run byte-identical under their committed freeze protocol. F1 (378→354) is a counter-artifact drop, not a tool failure — no K2 fire.
- **C2 K1 (predicate at landing): HELD.** `DEPTH_R85 entries=1 ok_entries=1 rows=6 located_quotes=7 fresh_sources=3`, `DEPTH_R85=PASS`, rc 0; before `entries=0 … FAIL` rc 1; `c2-d0-donothing` byte-identical both ways.
- **C2 K4 (ground): not attacked by this seat** (no K4 check assigned to R85ExecRepro; no finding).

VERDICT: R85ExecRepro C1 held — before FAIL/SETUP=0/1 vs landing PASS 354/354 verified from committed bytes with byte-identical controls.
VERDICT: R85ExecRepro C2 held — before entries=0 FAIL vs landing entries=1 PASS verified from committed bytes with byte-identical do-nothing control.
