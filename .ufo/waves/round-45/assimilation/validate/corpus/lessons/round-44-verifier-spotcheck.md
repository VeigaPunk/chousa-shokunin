# Round 44 verifier spot-check — chousa

author: hyaku closure (non-author integrator, @m_swe)
date: 2026-10-24
reviewer identity: `Kimi fresh closure agent` (fresh, non-author; no subagents dispatched; no external fetch; no tools installed)
lane repo measured at: `44aaf33cd37e2583fff13397f5a4b60a011ec1ab` (pushed tip; `jj-lane.sh state` → `ahead=0 behind=0`, `local=remote=44aaf33c…`, `head=detached`, branch `master`)
base: `e6983f6e242c7b82bd9a9c5ee170257624e8f109`
report: `.ufo/reports/round-44/chousa.md`, fleet commit `6b403b305a0b33b6834a32038b312f062e5bdd8b`

Claim counters were re-executed from a `git archive 44aaf33c… | tar -x -C /tmp/chousa-r44-tip` tree, so every measurement below is over committed bytes at the cited revision. The lane working copy was not checked out and was not edited except for this file.

## Step-1 conformance

- Report committed in the fleet repo under the lane identity:
  `git log --format='%an <%ae> %H' -- .ufo/reports/round-44/chousa.md` →
  `chousa-shokunin <chousa@shokunin.local> 6b403b305a0b33b6834a32038b312f062e5bdd8b`. Porcelain on that path empty. PASS.
- `SHONEN` heading present (report lines 255–270) with four `[~]` lines, one per box; `SHONEN.md` carries exactly four boxes. No `[x]` written by the lane. PASS.
- Cited lane hashes exist and are ancestors of `refs/heads/master` (never `@{u}`): `043f19a1db91288947493d9f879e61e7a9f07241` (freeze), `b603302c0a0c064fcaef3da672a3f0b465f9f448` (landing), `6254b4d859830ff27c7b44d7b2567c2f9f96255a` (36 inherited reports), `9b108fdb56316cba5fe02db8ee62c65608fbd41a` (oversize seat log), `78aa1fd2a6ede8a2d886d98e780705386425495a` (post-commit counters), `44aaf33cd37e2583fff13397f5a4b60a011ec1ab` (tip). Every one carries `chousa-shokunin <chousa@shokunin.local>`; base `e6983f6e…` is `protocol-shokunin <protocol@shokunin.local>`. Fleet commit `44479ed61c426dedd6093852cf03cd0e96344715` (L0 append) exists under the same lane identity. PASS.
- Pushed: `jj-lane.sh state` → `branch=master local=44aaf33c… remote=44aaf33c… ahead=0 behind=0 head=detached`;
  `git ls-remote origin refs/heads/master` → `44aaf33cd37e2583fff13397f5a4b60a011ec1ab`. PASS.
- Prompt `.ufo/prompts/chousa-round-44.md` (478 lines) carries the template contract: §1 MISSION/AXES binding, §2 claims, §2b frontier step, §3 L2 floor, §4 report contract (report path, one SHONEN line per box, commit-hash citation), §5 commit-then-push, push scope, L0 side channel, §6 hyaku addendum; lane write scope named at line 259, report-lands-last at line 325. PASS.
- Not a marker: work performed, evidence pointers, landed hashes, before→after measurements, Sources & frontier, Trend verdicts, SHONEN. PASS.
- Dispatch digest copied from `.ufo/watchdog.log` (mutable):
  `2026-10-24T21:36:37-03:00 launch chousa round=44 pgid=3105723 driver=hyaku-inline attempt=1`
  `2026-10-24T22:53:23-03:00 complete chousa round=44; hyaku-inline attempt=1`

### Uncommitted paths (driver verify warned 3)

`git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain` → exactly three `M` lines and no `??`:

- `M .ufo/waves/round-40/w1/swarm-registry.json`
- `M .ufo/waves/round-41/w1/swarm-registry.json`
- `M corpus/evidence/round41/receipts/cells/cells.json`

These are exactly the three `left-named` rows of `corpus/evidence/round44/disposition.tsv` (reason `not hunk-verified`) — inherited r40/r41 paths named in the disposition table, not new round-44 work. Nothing under `corpus/evidence/round44/`, `corpus/knowledge/`, `corpus/lessons/round-44.md`, `tools/` or `.ufo/waves/round-44/` is dirty. PASS: no uncommitted round-44 work. Left untouched; the operator's r43 ruling on the inherited tree stays open.

## Claims — re-measured by me at the tip

### C1 operability — re-measured, improved

```
$ python3 corpus/evidence/round44/c1-count.py
N_SPAWNED=64/64
N_REAPED=64/64
PARENT_PID_MATCH=1/1
ZERO_PIDS=0
NAMES_MATCH=64/64
C1=PASS            (exit 0)
```

Committed receipt `corpus/evidence/round44/parent-lifetime.receipt`: 64 `spawn` lines, 64 `reap` lines, `start parent_pid=3226659` … `end parent_pid=3226659 epoch=1792889282 n_spawned=64 n_reaped=64`. Second complete receipt `.ufo/waves/round-44/w3/parent-lifetime.receipt`: `n_spawned=32 n_reaped=32`, same start/end pid. Wave-2 receipt `.ufo/waves/round-44/w2-parent-lifetime.receipt` carries 5 `reap` lines and **no** `end` line — truncated, and the lane does not count it.

Do-nothing controls, all re-run by me, all exit 1:

| control | observed | exit |
|---|---|---|
| `--receipt /tmp/nonexistent.receipt` | `C1=FAIL receipt-missing` | 1 |
| `controls/pids0.receipt` | `C1=FAIL` | 1 |
| `controls/prose.receipt` | `C1=FAIL prose` | 1 |

The launcher itself was not executed by me; the committed evidence is the receipt plus `w3/W3ExecSelftest.md` (selftest exit 0, receipt `n_spawned=2 n_reaped=2`). Evidence-verified where stated, re-measured where a counter was available.

### C2 calibration — re-measured, improved

```
$ python3 corpus/evidence/round44/c2-count.py
CONSISTENT=39/39
REVERIFIED=36/36
LEFT_NAMED=3/3
C2=PASS            (exit 0)
```

`disposition.tsv` carries exactly 39 data rows: 36 `reverified-commit` + 3 `left-named`. The counter re-derives each of the 36 digests against the committed bytes, so the report's "36 committed" count is reproduced, not copied. Controls: `controls/all-left.tsv` → `REVERIFIED=0/36`, `C2=FAIL`, exit 1; missing table → `C2=FAIL table-missing`, exit 1.

### C3 depth — re-measured, improved, with an evidence defect

```
$ python3 corpus/evidence/round44/c3-count.py
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS            (exit 0)
```

Control: `--entry /tmp/nonexistent-entry.md` → `C3=FAIL entry-missing`, exit 1. The quote itself was re-located by me in the capture: `constitutes a promise that the resource state` occurs exactly once at byte offset 14896 (file sha256 `c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc`, 107130 bytes).

**Defect D1.** That capture is not a committed artifact. It is
`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt`, and
`git -C /home/vgpnk/Projects/shokuknow check-ignore -v` returns
`.gitignore:5:.ufo/waves/corpus-expansion-1/.qcache/`; `git ls-files` lists no capture and
`git log --all -- <path>` is empty, so it was never tracked. The report, the lesson and both knowledge entries call it a "committed capture". `c3-count.py` hardcodes that out-of-lane path, so C3 is not reproducible from the lane tree alone. The quote is real and located; the word "committed" is not true. Routed as D1.

### Auxiliary counter (QUALITY 62) — re-measured

`errata-count.py --file controls/errata-two.txt` → `ERRATA=2`, exit 0; `--file controls/errata-zero.txt` → `ERRATA=0`, `ERRATA_COUNT=FAIL`, exit 1. The criterion is shown able to fail. `considerthese/` is unchanged between base and tip (`git diff --stat … -- considerthese/` empty).

## Item 10 — adoption re-checked

- Adopted entries: `corpus/knowledge/citation-version-binding-r36.md` and `…-r37.md`; adopted rows S079, S080, S081. Registry count by the report's own command: base `78`, tip `81`; the base→tip diff of `corpus/SOURCES.md` is three added rows (all tier A) plus the round-44 search-log paragraph — no pre-existing row touched.
- Ids bound by document: staged `merge/chousa/SOURCES.append.md` line 7 is **S079 = PRISMA-S**, line 9 is **S081 = RFC 7089** (landed as lane S079, −2), line 19 is **S091 = WARP FAQ** (landed lane S080, −11), line 20 is **S092 = E2867** (landed lane S081, −11). No constant shift reproduces the landing. The staged ids are listed in the committed `assimilation/staged-ids`; the lane's `S077` guard note also holds — `S077` occurs exactly once in the staged append, inside the S093 row's cell (line 21).
- Rejects re-opened independently (see spot-check table): staged S082 and S093 reached neither `corpus/SOURCES.md` nor the knowledge entries; `grep -niE '7714|samr|portico|std\.samr' corpus/SOURCES.md` returns only the round-44 search-log line that names the exclusion.
- Validate-before-append: `assimilation/validate-census.txt` → five W04, no E03/E04, `validate_exit=0`; the committed mirror `assimilation/validate/corpus/SOURCES.md` is present. Re-checked independently by `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, five W04 (S051, S053, S073, S074, S075), `chousa ok`. PASS.
- Coverage map: `corpus/README.md` gained exactly two rows (the two adopted entries). PASS.

## Wave shape and seat accounting — judged for honesty, not for admissibility

Committed settle tables (`.ufo/waves/round-44/{w1,w2,w3}-settle.tsv`) re-read by me:

| wave | seats | outcome rows counted by me | report's claim | match |
|---|---:|---|---|---|
| w1 | 64 | 64 `dead`, exit 1; the string `Cannot combine --prompt with --auto.` appears 64 times | 64 dead, 0 reports | yes |
| w2 | 32 | 31 `report` + 1 `dead` (`W2ScribeQ62`) | 31 reports, 1 dead | yes |
| w3 | 32 | 9 `report` (5 exit 0 + 4 exit 124) + 23 `dead` (exit 124) | 9 reports, 23 dead, 27 killed of which 4 had reported | yes |

Round total 128 seats, 40 reports, 88 seats without a report — reconciled from committed bytes. Nothing is credited that did not happen: wave 1's receipt is counted only as a launcher receipt ("its 64 seats produced no work"), the truncated wave-2 receipt is excluded from parent-lifetime evidence, and the 88 unreported seats are not credited. The addendum's shape rules were read verbatim: 32–128 seats per round, default **two** v1 waves (or one v2 wave), and "The §3 L2 floor is met inside wave 1 (or inside the single v2 wave)". The lane used three v1 waves, names the deviation as a deviation, and routes the admissibility question to the operator at `.ufo/l0-questions.md:148` (`chousa | round-44`).

**Honesty judgement: honest.** The shape and the all-dead wave 1 are disclosed, quantified and uncredited rather than smoothed over, and the operator ruling is requested rather than assumed. One sentence overreaches and is routed as D3: "§3 L2 floor: met inside waves 2 and 3" asserts compliance the addendum does not grant (wave 1 ran zero seats). The admissibility question itself — whether a mass-failure wave counts against the 128-seat ceiling — is the operator's L0 ruling; this closure does not answer it.

## Per-axis verdicts (measured, not asserted)

| axis | verdict | evidence I re-derived |
|---|---|---|
| operability | **improved** | C1 counter re-run at the tip: 64/64, 64/64, 1/1, exit 0; three do-nothing controls exit 1; committed receipt and second complete wave-3 receipt. |
| calibration | **improved** | C2 counter re-run at the tip: 39/39, 36/36, 3/3, exit 0; all-left and missing-table controls exit 1; the 36 digests were re-derived against the committed bytes. |
| depth | **improved** | C3 counter re-run at the tip: 1/1, 1/1, 1/1, exit 0; quote located by me at offset 14896. Evidence defect D1 noted; the axis is not harmed. |
| coverage | **improved** | registry 78 → 81 by the report's counting command, reproduced at base and tip; three tier-A rows; two entries on ground the coverage map did not hold; coverage map +2 rows. |
| freshness | **unchanged** | capture mtimes re-read: RFC 2026-10-23 20:33:05, WARP 20:36:10, E2867 20:36:20 (−0300), all before the launch 2026-10-24T21:36:37−03:00. `SCORECARD.md` grades freshness **unchanged**, not improved; the base→tip diff carries no freshness improvement. Not harmed. |
| adjacency | **unchanged** | no sibling lane absorbed; the staged package was read-only — the fleet-root sweep found no chousa round-44 file outside the lane tree (the four untracked root files are an OMP config and three web pages, mtime 18:07, none naming chousa or round-44). |

No axis is harmed. No exploratory claim was declared, so no `unprovable-but-better` ruling was needed.

## Discernment spot-check (LEARNING.md — checked from outside)

Sample: one admit and one reject re-opened from source, plus the second admit pair and the second reject. Each source was re-opened at this review; agreement is recorded with a reason.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| lane S079 / `citation-version-binding-r36.md` (RFC 7089) | admit | `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt` | **agree** | quote `constitutes a promise that the resource state` occurs once, at byte offset 14896, exactly as the entry states; the entry cites `source: S079` and not `source: S081`; the row's URL is the RFC 7089 URL. The capture is untracked/ignored — see D1. |
| lane S080 / `citation-version-binding-r37.md` (WARP FAQ) | admit | `…/.qcache/5f54e82c87a76eefdc9a0d35.txt` | **agree** | file sha256 `a7e46e274b0784f81426bdc602785b03db1fa87f8f34916097d42ff36cac8dc8` matches the lesson; the 8-word quote `National institution websites are archived once per month` occurs once at offset 6425 (≤25 words). |
| lane S081 / `citation-version-binding-r37.md` (NDL E2867) | admit | `…/.qcache/0034b800811072de3980e85b.txt` | **agree** | file sha256 `d2a58e70eb8a2b4e42836c0b3df5035c67a45bbce71c412cbcd2bfb155d4848f` matches the lesson; the anchor token `warp.ndl.go.jp/web/20250102112233` occurs once at offset 2604. |
| staged S082 (SAMR record for GB/T 7714-2025) | reject | `corpus/evidence/round43/absent-split.tsv` line 2 (`S082 not-carried`) and `merge/chousa/SOURCES.append.md` line 10 | **agree** | the row was not fetched this round and the flip (a text capture holding issued and effective dates as one contiguous span) was not met; nothing from that row entered the registry or the entries. |
| staged S093 (Portico preservation page) | reject | `corpus/evidence/round43/absent-split.tsv` line 6 (`S093 misquote`) and `merge/chousa/SOURCES.append.md` line 21 | **agree** | a partial overlap is not the register's sentence and the four-factor flip was not met; no Portico row or entry exists. The `S077` collision claim also holds: `S077` occurs exactly once in the staged append, inside the S093 row's cell. |

Four of four decisions agree with the lane's gate. No disagreement, so no new QUALITY criterion is owed from this sample.

## Trend verdicts (with the evidence each rests on)

- **expansion: improved** — three new mined rows (registry 78 → 81, all tier A), two new knowledge entries on ground the coverage map did not hold, coverage map +2 rows, one lesson carrying five mined mistakes, one new launcher tool, QUALITY 62 and 63. Counts re-derived by me at base and tip.
- **quality: improved** — three frozen counters with six failing do-nothing controls, all re-run by me and all exit 1; mutation-probe evidence committed by the lane; QUALITY 62 shown able to fail (2 → exit 0, 0 → exit 1). The limits the lane names (the C2 counter cannot see a coordinated two-file edit; reason text checked only for non-emptiness) are named, not hidden.
- **discernment: improved** — the lane's own grade was `unchanged` pending an external spot-check, which is the honest pending state; this non-author spot-check has now run and agrees with the gate on both admits and both rejects (table above), which is the LEARNING.md criterion for `improved`.

## Routed defects — the lane must fix these next round

- **D1 (evidence).** The RFC/WARP/E2867 captures are untracked, gitignored files in the campaign tree (`shokuknow/.gitignore:5`); the report, the lesson and both entries call them "committed capture", and `c3-count.py` hardcodes that out-of-lane path, so C3 is not reproducible from the lane tree alone. Commit the bytes (or the needed span plus its digest) into the lane's own corpus, or reword to "on-disk capture" and cite the sha256 as the identity.
- **D2 (gate registry).** `SKILL.md`'s Gates table has no row for this round's counters (`corpus/evidence/round44/c1-count.py`, `c2-count.py`, `c3-count.py`) nor for the new gate `tools/parent-lifetime.sh`; the last registry rows are the r37/r38/r39 counters and the r35/r36 witnesses. PROTOCOL §Gate standard (Delivery) grades a gate conformant only when its registry row exists at the lane's registry home.
- **D3 (L2 floor wording).** The report states "§3 L2 floor: met inside waves 2 and 3"; the addendum places the floor inside wave 1 (or inside the single v2 wave) and wave 1 ran zero seats. Restate the floor's location or name the deviation; the seat accounting itself is accurate and uncredited.
- **D4 (minor numbers).** The E2867 capture mtime is 2026-10-23 20:36:20 (−0300), reported as 20:37; the lesson dates the launch 2026-10-24T21:47:59−03:00 while the driver digest and the report say 21:36:37−03:00. Neither changes the freshness grade — all captures predate the launch — but the figures should agree.
- **D5 (open lane items).** Lesson mistakes 4 and 5 stay unfixed: the launcher exits 0 on a malformed dispatch (`n_spawned=0`) and its 420 s timeout killed 27 of wave 3's 32 seats. QUALITY 63 requires the next launcher to size its timeout per wave and record it in the receipt.
- **D6 (inherited tree).** The three modified JSONs stay uncommitted pending the operator's r43 L0 ruling; they are the named `left-named` rows, so this is no new debt and the closure did not touch them.

Operator note: the round's SHONEN boxes 1, 2 and 4 (decision tables and cited sources, an end-to-end task logged in `LOG.md`, no cross-domain bleed) look checkable by a non-author on the evidence above; box 3 carries the open D2 registry-row gap. Promotion remains operator-owned and was not exercised. The lane's L0 line `.ufo/l0-questions.md:148` stays open; this closure does not answer it.
