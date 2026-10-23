# MutCounterC1 — counter-of-counter for C1 (grep pin), round 35 v2

Mutation tester, seed grid 3501 / 3517, 2026-10-23. All experiments in
`/tmp/hyaku/chousa-r35/w2/MutCounterC1`; artifacts copied to
`.ufo/waves/round-35/w2/MutCounterC1/`. No lane production file was edited.

## 0. Pins and one integrity event

| bytes | sha256 |
|---|---|
| committed counter `corpus/evidence/round35/c1-count.py` | `da207fd725658b84…ac715e3` (unchanged all session) |
| wave-base gate blob `e87c5d7:tools/research-gate.sh` | `1f2fb4f522d9a670…aaef617` (extracted to `pinned-gate.sh`; every scored "landed" row uses this copy) |
| base (round-34) gate | `a6307edf687ac0fb…562995b` (matches contract) |
| committed hardcoded control | `05bdf6543858a551…248a378` |

**The lane's working-tree gate changed mid-session, from another writer.** My
first receipt pinned `1f2fb4f5…` at 17:00:01. At 17:07:40 `tools/research-gate.sh`
was written; it now hashes `a47688518e509edb…0c38ad`. At 17:10
`git status --porcelain -- tools/research-gate.sh` printed ` M
tools/research-gate.sh`; at 17:13:57 the change was committed as
`b6f2c0db8de4047e6518f4232da2fd3c3954cf00` ("round-35: last wave seat
artifacts…"), so **HEAD is no longer the wave base `e87c5d7`** and the working
tree is clean for that path. The diff is 32 insertions/11 deletions in the pin
block (new `grep_pin_define`, timeout-bounded `--version`, PATH fallback
removed). My full matrix's nine `landed` rows carry `a4768851…` and are **not
evidence** under the contract. I re-ran the landed column against
`pinned-gate.sh` (§2, column "pinned"). The drifted bytes also score 9/9 intact
— observation only, not a claim measurement. This is reported, not adjudicated;
P1's "landed lane revision" now needs both a commit and a blob sha in its
receipt.

## 1. Method

Detector: the committed counter, copied verbatim to `c1-count.intact.py`; each
mutant removes exactly one requirement group from the copy (`diffs.txt`, 2–6
changed lines each; hashes in `hashes.txt`):

- **M1** S1 tripwire only; **M2** S2 tripwire; **M3** S3 output identity
  (leaves the `"not found"` string check); **M4** S4+S5 marker; **M5** S6 marker;
  **M6** S7+S8+S9 echo-field checks (leaves output identity and S9 tripwire);
  **M7** S9 tripwire (not in the ticket's list; added, see §3).

Wrong gates: all built by replacing **only** the pin block of the pinned
`1f2fb4f5…` blob; prefix/suffix bytes are identical (checked for all nine).
Each name is a real shortcut, not a broken patch:

- `V1` pins the first PATH grep (`type -P`), wrapper absolute — fails S1 only.
- `V2` sanitizes PATH instead of pinning; wrapper defined only on the override
  branch — fails S2 only (BASH_ENV function receives the default-path calls).
- `V3` scans PATH backwards, refuses when no PATH entry has grep — fails S3 only.
- `V4` plain `exit 2` for relative/missing overrides (no marker) — fails S4,S5.
- `V5` plain `exit 2` for the non-GNU stub (no marker) — fails S6.
- `V6` real pin/refusals, echo omits `source=` — fails S7,S8,S9.
- `V7` wrapper only on the default branch; override path falls back to bare
  `grep` — fails S9 only (BASH_ENV function fires only under override).
- `W2` **counterfeit**: hardcoded `GREP_BIN=/usr/bin/grep`, literal
  `GREP_PIN_VERSION='grep (GNU grep) 3.12-modified'`, no `--version` anywhere,
  "verifies" an override by string equality with `/usr/bin/grep`, canned echo.
  Gate sha `b4edf8a5710ec5cc…124f78`. `W2b` = same with a bogus literal
  ``GNU grep 0.0-not-a-real-version``.
- Committed `base` and `hardcoded` controls run as-is.

## 2. Matrix (score /9; seed 3501 unless noted; FULL = `matrix-s3501.log`)

| counter | pinned `1f2fb4f5` | base | hardcoded | W2 | V1 | V2 | V3 | V4 | V5 | V6 | V7 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| intact | **9** | 0 | 3 | **9** | 8 | 8 | 8 | 7 | 8 | 6 | 8 |
| M1 | 9 | 1 | 3 | 9 | **9** | 8 | 8 | 7 | 8 | 6 | 8 |
| M2 | 9 | 1 | 3 | 9 | 8 | **9** | 8 | 7 | 8 | 6 | 8 |
| M3 | 9 | 1 | 3 | 9 | 8 | 8 | **9** | 7 | 8 | 6 | 8 |
| M4 | 9 | 0 | 3 | 9 | 8 | 8 | 8 | **9** | 8 | 6 | 8 |
| M5 | 9 | 0 | 3 | 9 | 8 | 8 | 8 | 7 | **9** | 6 | 8 |
| M6 | 9 | 2 | 6 | 9 | 8 | 8 | 8 | 7 | 8 | **9** | 8 |
| M7 | 9 | 0 | 3 | 9 | 8 | 8 | 8 | 7 | 8 | 6 | **9** |

`intact` on seed 3517: pinned 9/9, W2 9/9, W2b 9/9; every Mk-on-its-Vk pair
also 9/9 (`matrix-s3517-key.json`). The pinned gate stays 9/9 under every
counter mutant — the removals do not weaken the real measurement.

Before/controls reproduce the claim record on 3501: base 0/9, hardcoded 3/9
(the claim's "before" and "cheapest control").

## 3. Load-bearing set and redundancy

**Every requirement group is load-bearing, with a named gate that skips the
work and still produces correct output/markers:**

| removal | wrong gate | why it only passes after removal |
|---|---|---|
| S1 tripwire | V1 | pins the PATH shim as its binary; shim logs each call, output identical |
| S2 tripwire | V2 | PATH sanitized, so S1 passes, but BASH_ENV `grep()` receives default-path calls |
| S3 output identity | V3 | PATH-order scan; with no grep on PATH it refuses (rc 2, message lacks "not found") |
| S4/S5 marker | V4 | refusals are plain `exit 2`; rc is the only discriminating clause |
| S6 marker | V5 | stub refused with a plain `exit 2` |
| S7/S8/S9 echo fields | V6 | real pin, echo has no `source=` |
| S9 tripwire (not in ticket list) | V7 | override branch calls bare `grep`; passes S2 and S7, fails S9 only |

**No scenario is redundant against these gates.** S1 and S3 are independent
(V1 fails S1, passes S3; V3 the reverse), and S9 is not implied by S2∧S7 (V7
passes both, fails S9). The ticket's removal taxonomy is one clause short:
S9's `empty_trip(trip2)` is a separate load-bearing requirement (M6+V7 stays
8/9; only M7+V7 reaches 9/9).

## 4. MEETS-grade finding: W2 meets P1 without verifying anything

`W2` scores **9/9 with the intact counter on both seeds**, while:

- it never runs `--version` (`grep -n -- --version gates/W2.sh` → only the
  comment at line 343), never resolves a default, and accepts any binary placed
  at `/usr/bin/grep` unverified;
- S4/S5 pass because its path-equality refusal is `exit 2` + the exact marker;
- S6 passes because it refuses the stub *without probing it*: the counter's S6
  criterion is `rc == 2 and "GREP_PROVENANCE" in err`; `stub_calls` is recorded
  but not scored (landed S6 shows `stub_calls: 1`, W2 shows `stub_calls: 0` —
  `receipts/intact__landed__s3501.json`, `receipts/intact__W2__s3501.json`);
- S7/S8/S9 pass because the echo is a literal (`W2b`, with
  `GNU grep 0.0-not-a-real-version`, still scores 9/9) and because S7/S9 use
  `REAL_GREP=/usr/bin/grep` as the override — the same path as W2's hardcoded
  default. "Honors the override" and "ignores the override" are
  indistinguishable here.

Behavioural counterfactual (`altprobe.txt`): a symlink `gnu-grep → /usr/bin/grep`
(same bytes, sha `19280b0e…fecf84`) at a different path. The pinned landed gate
accepts it, prints `path=…/altbin/gnu-grep source=override`, rc=1 and the same
CLAIM lines. W2 exits 2: `GREP_PROVENANCE refused: override is not the pinned
binary`. So W2 falsely refuses a legitimate GNU grep pin and scores full marks.

This is the same output-equivalence class C2 was built for, applied to C1: the
nine points score the *surface* (correct output, exit codes, marker and echo
substrings), not the claimed mechanism (resolve, verify, pin). Recommended
counter hardening (not applied — committed counter is read-only): S6 should
score `stub_calls == 0` on refusal **and** S7/S9 should override with a
distinct-path real GNU grep (symlink/copy), so path equality cannot fake
verification; the echo version should be checked against a run-time-derived
expected string for that path.

## 5. Limits

- W2 is a constructed shortcut. Its plausibility rests on "accept only the one
  known path", which is exactly what a hardcoded-pin implementer writes when
  override support is bolted on; the finding is a coverage gap in P1, not proof
  that any implementer would write it.
- Only C1's output counter is tested; the C2 witness (`mechanism-witness.py`)
  was not applied to C1 candidates — a trace witness would be the natural next
  probe for the W2 class.
- Fixture is the counter's three short-span claims; long-span/`slen` surfaces
  are out of scope. Two seeds only. The variant gates fail 2–4 of the gate's
  256 selftest cases (I did not enumerate them; [INFERENCE] pin cases), so the
  gate's own selftest was not used as a detector — P1's predicate is the
  counter.
- No network; no subagents; no package installs.

## 6. Restoration / non-interference

- Committed counter sha `da207fd7…ac715e3` before and after (re-hashed at
  17:10; `hashes.txt`); it was never written.
- Lane production files were only read; my writes are confined to
  `/tmp/hyaku/chousa-r35/w2/MutCounterC1/` and
  `.ufo/waves/round-35/w2/MutCounterC1/` (4.6 MB, no file >1 MiB, 108 receipts).
- The `tools/research-gate.sh` change is not mine: mtime 17:07:40, committed by
  another writer at 17:13:57 as `b6f2c0db`; I ran no git/jj write command and
  made no write under `tools/`. The only lane writes I made are the report and
  the artifact directory named above.

Reproduce: `python3 matrix.py 3501 full` in the scratch dir (needs
`pinned-gate.sh`, gates/, counters there); receipts carry each gate's sha256.
