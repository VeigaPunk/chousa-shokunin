# R57W1ScribeQuality — QUALITY criteria draft (Q111–Q113) + store/record audit

Seat: scribe (leaf, no dispatch). Assignment: draft `corpus/QUALITY.md` criterion text for the three mistake
classes the round exposes, each with the check that would have caught it, citing the lesson row; report behaviour,
gates, touched surfaces, out-of-scope, findings. Frozen inputs read first: `corpus/evidence/round57/claims.md`
(R57-C2 freeze `c2f914c5…`, R57-C3 `fd95724d…`), `corpus/QUALITY.md:957-961` (criteria 106–110 = house shape).
No predicate, target, counter, control or recipe was edited; the only lane write is this file. Scratch
`/fast/scratch/hyaku/chousa-r57/R57W1ScribeQuality/` (deleted before yield, §Scratch).

## What I ran (the evidence base for every claim below)

1. Lane tip at my run: `e0e73e0` (C2 after-receipt), i.e. one commit ahead of the dispatch's `f9736a3`.
   `python3 corpus/evidence/round57/c2-count.py` at `2026-10-27T05:44:21-03:00` →
   `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS`, exit 0.
   Matches the receipt's commit message; C2 is PASS on the tree I read.
2. Store-vs-record audit over committed trees (git object level, `git ls-tree` vs `git show <rev>:refetch.tsv`):
   ```
   f9736a3: ROWS=47 ROWKEYS=47 STOREKEYS=50 ORPHAN=3:['53a92273…','d473754a…','d8b4f8f8…']
              BYTES_BUT_ALL_FAILED=3 [('02aefcf5…','S103'),('e3ca8f4f…','S105'),('28750bcd…','S106')]
   e0e73e0: ROWS=101 ROWKEYS=53 STOREKEYS=50 ORPHAN=3  SUCCESS_ROW_NO_BYTES=0  BYTES_BUT_ALL_FAILED=0
   HEAD   : ROWS=101 ROWKEYS=53 STOREKEYS=50 ORPHAN=3  SUCCESS_ROW_NO_BYTES=0  BYTES_BUT_ALL_FAILED=0
   ```
   Working tree, same audit against `corpus/captures/*.raw` on disk:
   `DISK_KEYS=55 REC_KEYS=66 ROWS=118 ORPHAN=1 ['53a92273…'] STORE_BUT_RECORD_DENIES=2 (d473754a→S135, d8b4f8f8→S136,
   both with 2 failed attempts each) BYTES_STALE=0 RECORD_ONLY_SUCCESS_NO_BYTES=0`.
3. Provenance of the orphans: `git log --diff-filter=A -- corpus/captures/<k>.raw` → all four record-less files
   (`53a92273…`, `d473754a…`, `d8b4f8f8…`, `e3ca8f4f…`) were added by `b022b13` ("hyaku run9 wrap-up: remaining
   round-57 captures", 04:47:39), and `git show --name-status b022b13` shows **14 capture files added and
   `refetch.tsv` not touched**: the round's first byte commit carried no record at all.
   The three are PDFs (`file`): 1 203 711 B (31 pp, v1.4), 1 486 070 B (66 pp), 1 285 794 B (68 pp) = 3.98 MB.
   `53a92273…` has no row at any revision; its URL is recoverable *only* by brute-forcing sha256[:24] over 95 URLs
   scraped from the round's reports → `https://www.nhc.gov.cn/bgt/201807sgf/202109/5e18d6d8d86e405bad64dd4a8b666310/files/1733795726978_35780.pdf`
   (`.ufo/waves/round-57/w1/R57W1ScoutR3.md:22`). None of the three is in the frozen 47 (`SET_KEYS=47`, intersection empty).
4. Same-commit byte/row pairing per commit (`git show --name-status <rev>` vs that rev's `refetch.tsv`):
   ```
   b022b13: CAPTURES_ADDED=14 REC_ROWS_AT_REV=0   SUCCESS_KEYS=0  ADDED_WITHOUT_SUCCESS_ROW=14
   f9736a3: CAPTURES_ADDED=43 REC_ROWS_AT_REV=47  SUCCESS_KEYS=43 ADDED_WITHOUT_SUCCESS_ROW=0
   e0e73e0: CAPTURES_ADDED=4  REC_ROWS_AT_REV=101 SUCCESS_KEYS=47 ADDED_WITHOUT_SUCCESS_ROW=0
   WORKTREE: SUCCESS_ROWS_NO_TRACKED_BYTES=7 ['0cebd3c8…','6f545e6c…','9695437c…','a476f412…','ad3010d2…','c71776bc…','d2a1cf3d…']
   ```
   `6f545e6c…` = S133 attempt 2, `curl_rc=0 http=200 raw=c4bedad5…` at `2026-10-27T08:35:01Z`, 17 s **after**
   `e0e73e0` (05:34:44 local): its rows and its bytes are both still uncommitted (`git ls-files` → empty for both).
5. Root-resolution behaviour of the tool (`tools/capture-fetch.py`): root is `HERE = Path(__file__).resolve().parent`,
   `LANE = HERE.parent` (:47-48), `EVID`/`REC`/`STORE` derived from `LANE` (:49-51); there is **no** assertion that
   `LANE` is a git toplevel, `read_records()` returns `[]` silently when `REC` is absent (:95-96), and `main()`
   `mkdir(parents=True, exist_ok=True)`s the derived `EVID`/`STORE` before writing (:186-187). A copy of the landed
   tool placed at a wrong root (`$S/misroot/tools/capture-fetch.py`) run with `--status`:
   `pairs=0 rows=0` / `exit=0` — no root line, no error, indistinguishable from an empty record.
   Parent arithmetic on the real path: `HERE.parent.parent = /home/vgpnk/Projects/shokunin/chousa-shokunin` (lane, landed
   shape), `p.parents[2] = /home/vgpnk/Projects/shokunin` (**fleet root**), `Path.cwd().parents[1] = /home/vgpnk`.
   The counter's shape for an empty/misrooted record is the committed before-receipt
   `corpus/evidence/round57/controls/c2-before.txt`: `SET=47 VERDICTS=0/47 … C2=FAIL`, `exit=1`.
6. Telemetry of the round: `git status --porcelain` at my run = 31 entries — 2 modified (`corpus/evidence/round45/spans.tsv`,
   `corpus/evidence/round57/refetch.tsv`), 1 deletion (`w1.ready.partial`), 10 untracked captures (the in-flight fetch),
   the rest wave reports/`w1.ready.dispatched`. No fleet-root write: `git -C /home/vgpnk/Projects/shokunin status
   --porcelain` → empty; `/home/vgpnk/Projects/shokunin/corpus` does not exist.

## Findings (reported, not patched — the L1 adjudicates)

- **F1 — a pin was rewritten in the working tree (freshness-integrity, the round's most consequential item).**
  `corpus/evidence/round45/spans.tsv` (mtime 05:41:52) is modified but **not committed**; the diff replaces S083's two
  pinned digests and offsets with the drift values:
  ```
  -S083 … a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f  14415  spans/S083-1.txt  we cache all pages used as evidence in the internet archive
  -S083 … a3ff65e0db9cc4f2178932ce53965e4cba60c6aab0ba3b1d4ce40020a8a7cf8f  120724 spans/S083-2.txt  Archive.org returns a 404 page for these
  +S083 … d37b64ed18a860f8e7795b8dcc1b808e788f0643e4936f9dbcaf6e61bbf3b101  14332  spans/S083-1.txt  …
  +S083 … d37b64ed18a860f8e7795b8dcc1b808e788f0643e4936f9dbcaf6e61bbf3b101  120641 spans/S083-2.txt  …
  ```
  If this lands, S083's DRIFTED becomes a *pre-baked* REPRODUCED: the pin is the only digest C2 cannot forge, and
  rewriting it after the fetch erases the drift the claim exists to expose. The frozen counter is immune today —
  it loads manifests by `git show SET_REV:<path>` (`corpus/evidence/round57/c2-count.py:87,92`), and my 05:44 run still
  reads `DRIFTED=5` — so this is a data-integrity defect, not a claim defect. Check the L1 should run before receipt:
  `git diff --stat HEAD -- 'corpus/evidence/**/spans.tsv'` must be empty (it is non-empty now, 2 insertions/2 deletions).
- **F2 — a named record that does not exist.** `f9736a3`'s message says "misroot sweep of the tool's first run recorded
  in the round lesson"; `git ls-tree -r --name-only HEAD -- corpus/lessons | tail -3` → `round-55.md`,
  `round-56-verifier-spotcheck.md`, `round-56.md`. `corpus/lessons/round-57.md` is absent from the tree and from the
  status. The only surviving trace of the misroot is the commit message; Q111's evidence below is therefore split into
  *observed* (tool shape, arithmetic, counter shape) and *attested-only* (the incident itself).
- **F3 — the in-flight fetch is the live Q113 test.** 7 success rows in the working `refetch.tsv` have no tracked bytes
  (§4). `6f545e6c…` (S133) is the sharpest: a `rc=0 http=200` row whose `.raw`/`.txt` sit untracked in the store. If the
  L1 commits `refetch.tsv` in one commit and the captures in another, the round creates a second-generation version of
  the `b022b13` defect with the sign flipped (claim without bytes instead of bytes without claim).
- **F4 — `REPRODUCED` is what carries C2; the other 6 verdicts are attested.** 41/47 digest-bound, 5 DRIFTED +
  1 UNREACHABLE attested by `refetch.tsv` alone (claims.md discloses this). My audit adds: all 5 DRIFTED are `absent=0`,
  so no FRESHNESS-FLAG line is required and none exists; `FLAGGED=0/0` is correct, not vacuous-by-omission.
- **F5 — cosmetic residue, not a lane write.** `corpus/evidence/round57/__pycache__/c3-count.cpython-314.pyc`
  (27 069 B, 05:41:44) — another seat imported the C3 counter as a module; `.gitignore:3` (`corpus/**/__pycache__/`) keeps
  it out of status. My own runs were `python3 <script>` as `__main__` (no pyc).

## Draft — QUALITY criteria for round 57 (append as `## Round-57 additions (appended 2026-10-27; criteria 1–110 unchanged)`)

House shape follows 106–110: bold sentence · evidence with file:line and receipt · `Check:` command · `Shown able to fail (ran)`.

**111. A tool that writes derived paths resolves its repo root from its own file's location and refuses a root that is
not that file's git toplevel.** Round 57's re-fetch tool derives `LANE = HERE.parent` from `__file__`
(`tools/capture-fetch.py:47-48`) and its first run wrote under a counted-parent root instead, which lands on the fleet
root (`Path('…/chousa-shokunin/tools/capture-fetch.py').parents[2]` = `/home/vgpnk/Projects/shokunin`; a cwd-relative
`parent` count from the fleet root reaches `/home/vgpnk`) — the tool carries no root guard, so nothing could fire, and
the defect was caught by the counter's empty-record shape, not by the tool: `controls/c2-before.txt` is
`SET=47 VERDICTS=0/47 … C2=FAIL`, exit 1. The landed tool still has no root assertion: `read_records()` returns `[]`
silently when `REC` is missing (`:95-96`) and `main()` `mkdir`s the derived `EVID`/`STORE` (`:186-187`).
Lesson row: R57-M1 (`round-57.md` ≥Mistakes row 1; at draft time the file is uncommitted — F2).
Check: `<lane>/tools/capture-fetch.py --status` prints one line `root=<lane> record=<lane>/corpus/evidence/round57/refetch.tsv
store=<lane>/corpus/captures` and exits 2 unless `git -C <root> rev-parse --show-toplevel` equals `<root>`; a run with
`--id/--url` additionally refuses (exit 2) when `REC`'s parent does not already exist inside that toplevel.
Shown able to fail (ran): a copy at `/fast/scratch/hyaku/chousa-r57/R57W1ScribeQuality/misroot/tools/capture-fetch.py`
run with `--status` → `pairs=0 rows=0`, `exit=0`, no root line, nothing to distinguish it from an honest empty record;
the proposed check fails there for exactly that reason.
Named limit: the incident itself is attested only by the dispatch item and `f9736a3`'s message — no committed receipt.

**112. A capture byte is evidence only together with its fetch-record row; the store and the record are judged as one
set, in both directions.** Row `b022b13` committed 14 capture files and left `refetch.tsv` untouched, so three PDFs
whose fetch is written down nowhere are committed evidence: `53a92273a452a58f28368691.raw` (1 203 711 B),
`d473754a0cbf8d3095255d5a.raw` (1 486 070 B), `d8b4f8f8829b813f16227893.raw` (1 285 794 B) — `ORPHAN=3` at `f9736a3`,
`e0e73e0` and `HEAD`. The first can be attributed only by brute-forcing sha256[:24] over 95 URLs from the round's
reports (`R57W1ScoutR3.md:22`), i.e. by a coincidence the lane cannot rely on; the other two later acquire rows that
record **two failed attempts each** (`--status`: `d473754a… S135 attempts=2 fails=2`, `d8b4f8f8… S136 attempts=2 fails=2`)
while the store holds a readable PDF — the record then denies bytes the store has. The converse defect is the same unit
seen from the other side: `S105`'s record-less bytes made the triple permanently `MISSING` until the L1 deleted them
(sibling receipt `R57W1ExecControlsReRun.md` §5: orphan present → `MISSING`, removed → `UNREACHABLE`).
Lesson row: R57-M2 (`round-57.md`; draft at `R57W1ScribeLesson.md`).
Check: a lane tool `corpus/evidence/round57/store-record-audit.py` (to be landed; my inline form of it is the audit in
§2) — for every `corpus/captures/<key>.{raw,txt}`
in the tree a row with that `key` and a successful attempt (else `ORPHAN`); for every successful row, the key's `.raw`
in the same tree (else `RECORD_ONLY`); for every key, the last successful row's `raw_sha256` = sha256 of the `.raw`
(else `BYTES_STALE` / `STORE_BUT_RECORD_DENIES` when no attempt succeeded); exit 1 on any nonzero class.
Shown able to fail (ran, inline form of the same audit): committed `ORPHAN=3` at `f9736a3`/`e0e73e0`/`HEAD`, working tree
`ORPHAN=1 STORE_BUT_RECORD_DENIES=2`.

**113. A commit that adds capture bytes adds their attempt rows in the same commit, and a commit that adds a successful
row adds its bytes.** `b022b13` added 14 capture files with `REC_ROWS_AT_REV=0` (`ADDED_WITHOUT_SUCCESS_ROW=14`), which
is how the orphans of 112 were born; the two later fetch commits pass the same test (`f9736a3` 43/43 paired,
`e0e73e0` 4/4 paired). The rule is what makes a counted claim checkable without reconstructing history: `REPRODUCED`
rests on "the last successful attempt's `raw_sha256` equals these bytes", and that sentence is only true if the row and
the bytes entered the lane together. Lesson row: R57-M3 (`round-57.md`).
Check: for each commit touching `corpus/captures/`, `python3 corpus/evidence/round57/store-record-audit.py --commit <rev>`
compares `git show --name-status <rev>` capture additions against `<rev>:corpus/evidence/round57/refetch.tsv` and exits 1
naming each key added without a successful row in the same commit (and each success row added without its `.raw`);
at wave time it must also be run on the working tree before the L1 commits (`--worktree`), because in-flight rows and
bytes are exactly the case it exists for.
Shown able to fail (ran): `b022b13 → ADDED_WITHOUT_SUCCESS_ROW=14`; `f9736a3 → 0`; `e0e73e0 → 0`; working tree →
`SUCCESS_ROWS_NO_TRACKED_BYTES=7` (S133's `6f545e6c…` among them).

## Gates / touched surfaces

- Gates run: the frozen C2 counter once (read-only, `C2=PASS`, §1). I did **not** run C3 (its entry does not exist yet),
  and I ran no build/lint/test — the scribe assignment does not ask for them.
- Lane writes: this file only. `git status` after my runs shows the same 31 entries as §6 plus this report
  (the 2 modified files are the L1's/carried over, not mine: `round45/spans.tsv` F1, `refetch.tsv` F3).
- Frozen artifacts untouched: `c2-count.py`, `c3-count.py`, `controls/build-c*-controls.py` and the four receipts are
  unmodified in status; no `git add/commit/checkout/reset/stash/push`, no jj mutation, no network fetch by this seat.
- Out of scope, deliberately: the C3 entry/URL curation (scout seats), the C2 predicate or target (frozen), the
  `capture-fetch.py` behaviour itself (finding F3/Q111 are routed to the L1, not patched), the quarantine hand-check
  (other seats), the round-57 lesson file (the L1 authors it; my draft text above supplies the three lesson rows).

## Scratch

`/fast/scratch/hyaku/chousa-r57/R57W1ScribeQuality/` held `audit.py`, `head_audit.py`, `keys.py`, `q113.py` and the
`misroot/` copy of the tool; deleted before yield (`rm -rf --`), no scratch left, nothing under `/tmp`, no tool installed
or upgraded this seat.

VERDICT: drafted Q111 (root resolved from the tool's own file, refusing a non-toplevel root — tool-shape and counter-shape observed, incident attested-only), Q112 (bytes and record as one evidence unit — `ORPHAN=3` observed red-handed at three revisions), Q113 (bytes and rows in one commit — `b022b13 → 14/14` unpaired) and reported the two live hazards the drafts are built on (uncommitted S083 pin rewrite `F1`; 7 in-flight success rows without tracked bytes `F3`) — the drafts survive; C2's `PASS` is reproduced on the tree I read, with the pin-rewrite caveat named rather than patched.
