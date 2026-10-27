# R57W1ExecRefetchAudit — honesty audit of the L1's round-57 fetch record

seat `R57W1ExecRefetchAudit` · wave r57-w1 · lane `chousa-shokunin` · 2026-10-27. Read-only audit of
`corpus/evidence/round57/refetch.tsv` + the store it claims, plus scratch reproductions of the frozen
counters. Only this report was written; no network fetch; no frozen counter, control, recipe, capture or
record edited. Snapshots (the L1 is still appending live): HEAD `e0e73e0` = 101 rows; LIVE = 129 rows,
sha256 `fb4e95ff1ac4fdbf1127c5c4cc9b255b741179d3a906ba8710b2da8cf4000096`.

## 1. The seven checks

| # | check | result |
|---|---|---|
| 1 | header is exactly the 9 frozen columns | **PASS** (`id,url,key,attempt,fetched_utc,curl_rc,http_code,raw_sha256,txt_sha256`) |
| 2 | chronological; per-(id,url) attempts 1..n, n≤3 | **PASS** — 0 chronology violations, 0 numbering violations |
| 3 | `key` == `sha256(url)[:24]` | **PASS** — 0 mismatches over every row |
| 4 | success rows' digests == committed `<key>.raw`/`<key>.txt` | **PASS** on the last successful attempt of every pair (47/47 HEAD, 57/57 LIVE, 0 mismatches); **3 anomalies** (A1) |
| 5 | failure rows: `raw_sha256='-'`, plausible rc/http | **PASS** on digests — 0 failure rows carry a digest; rc/http anomaly (A2) |
| 6 | every `(id,url)` is a pinned triple or an approved URL | **PASS** for all 47 pinned; **22 extras** (A3) |
| 7 | no URL exceeds 3 attempts | **PASS** — max exactly 3, one pair (S105); 53 pairs at 2, 20 at 1 (LIVE) |

Per-URL attempt counts: `3` → S105 `https://gs.sxu.edu.cn/docs/2025-03/9e5cdd215a414bf6b5694912018de4c8.pdf`
only; `2` → 53 pairs; `1` → 20 pairs (the new C3 candidates S131–S136 + mirrors). At HEAD: 3→S105, 2→46,
1→6. The cap is enforced by the tool (`tools/capture-fetch.py:MAX_ATTEMPTS = 3`; `main()` skips at `n>=3`).

## 2. Anomalies (reported, not patched — the claim is frozen)

**A1 — three attempt-1 rows assert a digest the store no longer holds (benign cause).** S111/S113/S114
attempt 1 succeeded with `a65d33c3f4ac…`, `18201d555f05…`, `fe77ace1f4a3…`; attempt 2 of the same URLs
returned *different* bytes and `append_row()` overwrites `<key>.raw/.txt` per URL key, so attempt-1 bytes
left the store. The rows are truthful; the bytes remain in git (`git show f9736a3:corpus/captures/42bac8830527d6f1bb125c49.raw | sha256sum`
== `a65d33c3f4ac436f…` == the recorded attempt-1 digest; likewise `453d492becd9…`, `cacddf3bbf78…`). The
store is a per-URL slot, not a per-attempt archive, so `refetch.tsv` alone cannot re-verify attempt-1
rows. No falsification.

**A2 — 11 failure rows carry `curl_rc=28` with `http_code=200`.** `28` = `CURLE_OPERATION_TIMEDOUT`;
`200` is the status line curl had received when the 15 s `--max-time` cut the body. `fetch_one()` stores
bytes only when `rc == 0 and 200 <= code <= 299`, so these rows correctly show `raw_sha256='-'`/
`txt_sha256='-'` — the tool did **not** keep a truncated body and call it a capture. Plausible and honest.
Other shapes: `22` = curl HTTP-error code (412/404/503 from `nhc.gov.cn`'s bot-challenge and the
`web.archive.org` mirrors), `35`/`60` = TLS errors, `92` = HTTP/2 stream error. Tool-side nit only: a
200 received-but-not-stored is not distinguished in the row.

**A3 — 22 `(id,url)` pairs are neither of the 47 pinned triples nor literally named in
`corpus/evidence/round57/egress-approval.md`** (the C3 lead documents S131–S136 and their mirrors: the
2019/2021 notices, the 2021 management guideline, `hnysfww.com`/`takarabiomed.com.cn` copies,
`web.archive.org` wrappers). The egress table's second scope row does authorise "open of a public
document a registered source cites by name … after the document's URL is located by a search", so they
are inside the approval — but its record column requires "the new row's lesson `## Gate` line" and "the
query and the chosen URL in the lesson `## Gate`", and **`corpus/lessons/round-57.md` does not exist**
(`ls` → no such file): the approval's recording requirement is unmet for every extra row. Also,
`web.archive.org/web/2024/…` wrappers are different URLs from the documents and were fetched as such
(rows exist for wrapper *and* origin, 412 for the origin).

**A4 — three committed store `.raw` files have no record row and no `.txt`; two are C3-relevant.**
`53a92273a452a58f28368691.raw`, `d473754a0cbf8d3095255d5a.raw`, `d8b4f8f8829b813f16227893.raw` are
tracked at HEAD (added by `b022b13`) with no `refetch.tsv` row and no `.txt`. Their URLs are recoverable
by key: `d473754a…` = `https://www.hnysfww.com/data/article/1656481023744041713.pdf` (抗肿瘤药品临床
综合评价技术指南 2022年版 = R4), `d8b4f8f8…` = `…/1656481067585283603.pdf` (儿童药品临床综合评价技术
指南 2022年版 = R6), `53a92273…` = the 2021 NHC gazette (URL named in
`.ufo/waves/round-57/w1/R57W1ScoutR2Gaz.md`). The frozen C3 predicate requires a bound row's capture to
be "the bytes of a successful attempt for (X, U) in `refetch.tsv`", so these **cannot** bind R4/R6 as
they stand: the missing part is the record+registry+manifest wiring, not the bytes — `pdftotext -layout`
of all three holds the needed titles/tokens (R4/R6 hit "2022年版"+titles; the gazette hits 〔2019〕80号,
〔2021〕16号, 2021年版).

**A5 — the S105 capture was deleted, and that deletion is what turned `VERDICTS=43/47` into `47/47`.**
Commit `e0e73e0` ("record-less wrap-up S105 bytes removed") deletes
`corpus/captures/e3ca8f4fdd15420b80096a75.raw` (4,482,989 B). Reproduced in scratch:

```
A: HEAD store (S105 .raw absent)       → VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 C2=PASS (exit 0)
B: same store + deleted .raw restored → VERDICTS=46/47 … C2=FAIL (exit 1)
                                       "CAPTURE S105 … MISSING capture not the last successful attempt's bytes"
C: B + recipe .txt beside it          → VERDICTS=46/47 … C2=FAIL (exit 1)
pre-deletion tree a03824d (git archive) → VERDICTS=43/47 … C2=FAIL (exit 1)
```

The deleted bytes are the **pinned** capture: `pdftotext -layout` of the recovered file hashes to
`2197abe27dad4a681b33bee7a6a93a46681968bc8ee88cc0c674eaccdd84f71e` — exactly the `capture_sha256` S105
carries in every spans row at SET_REV — and yields 38174 chars, matching the round-50 record. Recoverable
from git (`b022b13`, `e0e73e0^`). So S105 was not UNREACHABLE in substance: the pinned bytes were in hand.
But the counter awards UNREACHABLE only when **no** file exists at the key, and REPRODUCED only when the
file's digest equals the *last successful attempt's* `raw_sha256`; all three S105 attempts failed
(`rc=28`), so no row could name those bytes — deleting the file is what let the counter print
`UNREACHABLE=1`. This is a **state** change the L1 chose, not a counter change; it is disclosed in the
commit subject and named in `R57W1ReviewFrontier.md`, `R57W1ExecC2Recompute.md`, `R57W1ScribeLesson.md`.
Those bytes are also the lane's only copy for that pin, and three committed lane documents cite the key
(`corpus/knowledge/cnki-citation-check-r40.md`, `citation-matching-semantics-r41.md`,
`corpus/lessons/round-50-verifier-spotcheck.md`).

**A6 — three S105 facts a reader would take away wrongly.** (i) the 3-attempt cap was exhausted with
attempt 3 only 216 s after attempt 2 (gaps 1440 s, 216 s), so attempt 3 alone did not meet the
`>= 600 s` spacing the predicate names; the first→last span (1656 s) is what satisfies it. (ii) all
three rows are `rc=28/http=200`: the server *did* answer 200 — the failure is a truncated body, not an
unreachable host, so "UNREACHABLE" here means "the recipe could not finish the body in 15 s". (iii) the
counter's UNREACHABLE branch keys on file *absence*, so S105's verdict is decided by store state, not by
the fetch record.

## 3. Controls and separability (read-only, in scratch)

Frozen artifacts are byte-identical to their freezes: `c2-count.py` at `c2f914c` == HEAD ==
`d6885bae2e8485e28f7d6e1fa59de7a0b3639ee0a242c71baf4c8ba753cb35f9`; `c3-count.py` at `fd95724` == HEAD
== `c565ce4a78b439411dc6e088bc5f8a92781888fe895f2ee9b43170867c1e6e33`; `build-c2-controls.py`,
`c2-before.txt`, `c2-controls.txt`, `build-c3-controls.py` unchanged. Controls rebuilt from the frozen
builder and re-run: EMPTY `exit=1 VERDICTS=0/47 REPRODUCED=0 DRIFTED=0 UNREACHABLE=0 C2=FAIL`; JUNK
`exit=1 VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 FLAGGED=0/47 C2=FAIL`; ALLFAIL `exit=1 VERDICTS=47/47
REPRODUCED=0 DRIFTED=0 UNREACHABLE=47 C2=FAIL`. No control meets the target — the counter is not vacuous;
`controls/c2-before.txt` still reads `VERDICTS=0/47 … C2=FAIL`. Live runs: `c2-count.py` → `VERDICTS=47/47
REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` (exit 0);
`c3-count.py` → `ENTRY=no … BOUND=0/7 … C3=FAIL` (exit 1). My independent re-derivation of the 47
verdicts (pin vs. the last successful attempt's `raw_sha256` **or** `txt_sha256`) reproduces the counter
exactly: REPRODUCED 41, DRIFTED [S083,S087,S113,S114,S121], UNREACHABLE [S105], MISSING 0 — the dispatch
brief's "5 DRIFTED = S083 S087 S113 S114 S121, absent=0" is confirmed, and `FLAGGED=0/0` holds because
every DRIFTED capture has `absent=0`, so no FRESHNESS-FLAG is owed (the missing lesson file does not
break C2; it would break C3's `in_lesson` check).

## 4. Calibration notes for the L1 (no target/counter change proposed)

- C3's four-of-seven target looks reachable from bytes already on disk: titles+edition tokens appear in
  `b27ffd2f0161104c6a28c9f5` (S127, all seven), `6f545e6c16b6b568ea3f591b` (R3 heading OK),
  `16fe8487aa97b98576a0dbac` (S118, R7 heading OK), `a476f4128186c7976671ab54` (R1,R2,R3 headings OK),
  `de34c41f76e5a5c0e1f4d1a2` (R1), plus A4's two orphan `.raw`s (R4, R6) and the
  `9695437cac165bb4b6145deb` form (R4/R5/R6 titles, no heading hit). What is missing is the
  record+registry+manifest wiring, and `corpus/SOURCES.md` currently has **zero** `^| S13[1-9] ` rows, so
  no candidate id exists in the Registry yet.
- The 15 s recipe timeout, not unreachability, is the operative failure mode for the large Chinese PDFs:
  every `rc=28`+`http=200` row is a body cut mid-transfer, so a larger `--max-time` would likely convert
  several pending C3 candidates — a fact about the recipe's behaviour; the recipe is frozen. Also, a
  success row can carry an empty text form (`c71776bc3084de059b84569d.raw` → 2 chars;
  `ad3010d2aee49a95e0c7cb0b.txt` → 0), worth knowing before a quote is anchored there.

## 5. Housekeeping

Tools: none installed or upgraded; `pdftotext 26.08.0`, `Python 3.14.8`, `git 2.56.0` all pre-existing (as
the frozen recipe/counter require). No pacman transaction attempted (host-wide pause respected). Scratch
`/fast/scratch/hyaku/chousa-r57/R57W1ExecRefetchAudit/` (audit script, HEAD/LIVE/SNAP copies, control
fixtures, recovered S105 bytes, 3 counter reproductions) **deleted** before finalising. Writes by this seat:
**only** this report. Fleet root clean (`git -C /home/vgpnk/Projects/shokunin status --porcelain` → empty).
No lane file, frozen counter, control, capture or record modified; no git/jj mutation run anywhere. No
external network fetch made — only committed captures and a git-restored copy of one deleted file were read.

VERDICT: attacked `refetch.tsv` on all seven axes (header, chronology/attempt-cap, key derivation,
digest-vs-store, failure-row plausibility, scope-vs-egress, per-URL attempt counts) — all seven PASS with
no falsified row, but the audit FALSIFIES one surrounding claim: the `C2=PASS` receipt is produced by
deleting the pinned S105 capture (its `pdftotext` digest equals the S105 pin) so the counter's
file-absence branch prints `UNREACHABLE=1`, and 22 extra record rows outside the 47 pinned triples have no
`## Gate` record because `corpus/lessons/round-57.md` does not exist.
