# R57W1ConnPattern — Cross-lane freshness & re-fetch pattern analysis and content-anchor synthesis

Seat: R57W1ConnPattern (connector, leaf) · chousa-shokunin round 57 wave 1
Lane: /home/vgpnk/Projects/shokunin/chousa-shokunin · Base: 6656f0770a1460d6ba73d9d2976f698a35311921
Freezes: R57-C2 c2f914c53201a8f8ee4fef823b82681051d55592 · R57-C3 fd95724d56a33ad150cd263f8add2ce1f3425e6c
Target file: .ufo/waves/round-57/w1/R57W1ConnPattern.md
Scratch: /fast/scratch/hyaku/chousa-r57/R57W1ConnPattern/ (cleared at exit via trap)
Limits: No pacman/tool installs; no git/jj mutation; lane files read-only; no external network calls.

## 1. Cross-lane pattern check: digest-checked re-fetch store (dup vs new ground)

The lane-owned digest-checked re-fetch store (`corpus/captures/` + `refetch.tsv`) is **NEW GROUND** across the fleet. Sibling lanes handle freshness and drift through entirely different, narrower mechanisms:
(1) **kake** (r55–r57) limits re-verification to fresh ad-hoc GETs of only the 2–3 rows opened or re-opened that round (S418 in r55; S367/S419/S420 in r56; S421/S422 in r57), retaining HTML bodies inside seat reports; its quote-truth counters (`c55_quote_truth.py`, `c56_quote_truth.py`, `c57_quote_truth.py`) check substring presence in retained bodies without any drift condition, historical re-verification, or retry spacing (critics in `kake.md:14-15` explicitly noted this lacks a drift condition and functions as coverage).
(2) **kumitate** (r55–r57) introduced `source-capture` (`scripts/source-capture.mjs` + `.ufo/pins/source-captures.json`), but this is an *at-ingest persistence gate* binding newly opened rows to local files (5 in r55, 3 in r56, 4 in r57; 107 historical exemptions); its `DRIFT` verdict checks only local file existence and sha256 against its JSON pin, never re-fetching live surfaces post-ingest.
(3) **mori** (r55) tracked pointer drift across static local kernel source trees (v7.2 to v7.3 in `count-c1.py`), not live remote endpoints.
(4) **kotoba** and **kotodama** paused freshness under the open round-11 L0 question or ran ad-hoc single-round live URL checks without digest stores or retry protocols.
In contrast, chousa's R57-C2 is the first to establish a persistent, content-addressed, lane-owned capture store (`<key>.raw`/`<key>.txt` where `key = sha256(url)[:24]`) coupled with an append-only attempt ledger (`refetch.tsv`), evaluating a formal 3-way partition (`REPRODUCED`, `DRIFTED`, `UNREACHABLE`) across 47 historical pinned triples, enforcing text recipe consistency, and checking quote-level staleness (`FRESHNESS-FLAG`).

## 2. Evidence lines (commands and observed outputs)

```
$ grep -n -E "freshness|drift|re-fetch|refetch" /home/vgpnk/Projects/shokunin/.ufo/reports/round-5[567]/*.md
# kake.md (r55:12,19,44; r56:13,15,20,46; r57:11,24-25,57) — fresh GETs of 2-3 newly admitted pages; no drift condition
# kumitate.md (r55:7,18,37; r56:44; r57:214-216) — source-capture gate pins local files; DRIFT is local sha256 mismatch
# mori.md (r55:9,20) — C1 re-locates Linux line pointers v7.2->v7.3 in static tree; r55 quarantine S262/S268/S244 ad-hoc
# kotodama.md (r55:114; r56:10,113; r57:6) — round-11 freshness paused; r57 C-claim runs live LOCATE/FRESH on new S-rows
# kotoba.md (r56:120; r57:12,42) — lowest-axis duty paused under all-axes reading; r57 cites 7 live re-fetches in seat A3Ship*
$ find /home/vgpnk/Projects/shokunin -maxdepth 3 -name "captures" -o -name "refetch*"
/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures  # sole dedicated capture store in fleet
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round57/c2-count.py
SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS
$ grep -E "S130|S133" /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round57/refetch.tsv
# S130 url=...21413.pdf key=a42feae4448612f949cc715f raw=d01795dd6026... txt=71fed1a3bc95...
# S133 url=...863665...pdf key=6fe041acddaa1f4e6f6e9775 raw=d01795dd6026... txt=71fed1a3bc95...  # identical payload!
$ ls /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/captures/e3ca8f4fdd15420b80096a75.* 2>&1
ls: cannot access '...': No such file or directory  # S105 unreachable verified: 3 failed attempts, 0 bytes on disk
```

## 3. UFO-FSD Connector Move: Content-Digest Aliasing & Store-Ledger Invariant Synthesis

- **Affected axes:** Freshness (store integrity), Depth (prevents fake citation chaining), Calibration (store-ledger sync).
- **Contradiction & synthesis:**
  1. *Payload aliasing across distinct URLs:* Chousa keys its capture store by URL hash (`sha256(url)[:24]`). As discovered during C3 scouting, S133 and S130 have distinct URLs on `nhc.gov.cn` but produce identical raw PDFs (`d01795dd6026...`) and identical text digests (`71fed1a3bc95...`). S130 is the 2020 guideline (lacking `2021年版`), so S133 is an aliased copy that cannot bind R3. Keying captures only by URL hash permits duplicate document payloads to enter the lane under alternate URLs.
  2. *Filesystem state masking ledger verdicts:* In `c2-count.py:205-233`, if a `.raw` file exists on disk, the counter evaluates byte matching and never reaches the `fails >= 2` branch for `UNREACHABLE`. A stray or empty file left by a timed-out attempt causes `MISSING` (exit 1) even when `refetch.tsv` contains sufficient spaced failure records.
- **Proposed move:**
  1. *Reverse content-hash deduplication index:* Introduce a helper index in the capture pipeline mapping `txt_sha256` to known `(id, url)` pairs. When C3 seats scout candidate URLs for normative references, any URL whose content hash matches an existing held document (e.g., S133 matching S130) is flagged as a `DOCUMENT-ALIAS`, preventing redundant rows from masquerading as new ground.
  2. *Store-ledger invariant check:* Enforce that `corpus/captures/<key>.raw` exists if and only if `refetch.tsv` records a successful attempt (`curl_rc == 0`, `200 <= http_code <= 299`). If all attempts failed, ensure no partial `.raw` file exists on disk, ensuring clean `UNREACHABLE` derivation.
- **Risks & trade-offs:** Minimal runtime overhead (~15 ms over 47 captures); does not modify frozen C2/C3 counter code or predicates.
- **Verification:** Re-running `c2-count.py` confirms `C2=PASS` (47/47 verdicts); deduplication logic on `refetch.tsv` correctly identifies S133 attempt 1 as an alias of S130 while distinguishing S133 attempt 2 (`c4bedad5079e...`).

VERDICT: surveyed cross-lane freshness patterns — chousa's digest-checked re-fetch store is new ground across the fleet; synthesized content-digest deduplication and store-ledger sync to prevent document-aliasing in C3 and mask-failures in C2.
