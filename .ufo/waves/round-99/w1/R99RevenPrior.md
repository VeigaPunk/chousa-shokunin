# R99RevenPrior — falsify findings on C1 and C2 (round 99, seat R99RevenPrior)

Attacked tree: F `d41f4cd8b857c6de683e7be5c5e8125b32763a8e`, a `git clone --shared` checked out at F in
`/fast/scratch/hyaku/chousa-r99/R99RevenPrior/repo` (`rev-parse --show-toplevel` asserted equal). Base `47ed34fa785288837f84cde9db15c41300854a78`.
Tools installed: none. No network. No lane or fleet mutation. Scratch removed before yield.

Correction to the prior turn: an earlier turn said this report was written. It was not, because scratch was deleted first.
The R32 run in that earlier turn also used a round-98 mutant file whose canary differs from F, so it was invalid. Both are
redone below; the invalid receipts are marked SUPERSEDED.

## Q1 — QUALITY 229 at F; the challenge captures; the blind spot

Commands (cwd = repo at F):

1. The 229 loop over captures cited as `capture=corpus/captures/<hex>.txt` in `corpus/knowledge/*.md` and `corpus/lessons/*.md`
   (28 keys) prints nothing. Receipt `R99RevenPrior-q229_F.txt`.
   Blind spot: the round-98 S230 key appears in `corpus/lessons/round-98.md:39` as prose (`capture key b5b8d050eea0c638e95ba674`), not as a `capture=` token, so the loop's selector never reaches it.
2. The same pattern `Checking your browser|Cookies must be enabled|Just a moment|reCAPTCHA` over every `corpus/captures/*.txt` (100 files) prints 4 hits, exit 0:
   `0954149536aaad411000e1fb`, `58725f5e0ac436166546a5ec`, `b5b8d050eea0c638e95ba674`, `ff9013bd7d9387e45cd6e000`.
   Receipt `R99RevenPrior-q229_all.txt`.
   **Misses:** `b90988847e704a08aabc8321` (S234, "Client Challenge"; confirmed, the pattern has no such phrase) and
   `712ec7bb981a9669a6921db7` (12 words, Chinese WeChat verification page: 环境异常 / 当前环境异常，完成验证后即可继续访问 / 去验证).
3. Classification of all 25 captures at F with normalized length ≤300 words (`R99RevenPrior-short_captures.txt`,
   `R99RevenPrior-classify.txt`, `R99RevenPrior-q1_classify_normed.txt`, `R99RevenPrior-wordcounts.txt`):
   - Challenge pages (8, by reading): `0954149536aaad411000e1fb`, `58725f5e0ac436166546a5ec`, `ff9013bd7d9387e45cd6e000`
     (pubmed "Cookies must be enabled", 18 words each); `b5b8d050eea0c638e95ba674` (S230 reCAPTCHA, 23 words);
     `b90988847e704a08aabc8321` (S234 "Client Challenge", 37 words); `712ec7bb981a9669a6921db7` (zh verification, 12 words).
     That is 5 English-marker pages and 1 Chinese page — 6 in total; the 6th is the one neither detector sees.
   - Empty (0 bytes): `0cebd3c84524295839ceaadd`, `ad3010d2aee49a95e0c7cb0b`.
   - Stub: `52db06f9e0e2eaf35bbdb321` (1 word, a dublincore URL line).
   - Documents: the remaining 17 (e.g. `be74dca6a3590698cb736e59`, 25 words, a Chinese news item — not a challenge page).
   Note: `712ec7bb…` is referenced by `corpus/evidence/round57/refetch.tsv` (row S131, a mp.weixin.qq.com GET, HTTP 200) and by no GATE-RECORD (grep over `corpus/` at F).
4. `tools/gate-records.py` `is_challenge` at F (`R99RevenPrior-q1_all_is_challenge.txt`): True on exactly the five English-marker pages above; False on `712ec7bb…`; False on every document. Short-document false refusal (limit b) is not exercised by committed data: the only ≤200-word captures that carry a marker are the five challenge pages.

**Why the prior rule missed S234.** Two instruments existed before round 99 and neither reached gate records:
- QUALITY 229 is a four-phrase lexical floor, not wired into `gate-records.py`, and has no "Client Challenge" phrase.
- `tools/quarantine-check.py` (base `47ed34fa`, receipt `R99RevenPrior-quarantine-base.txt`) already carries `INTERSTITIAL_MARKERS` containing `client challenge`, `checking your browser before accessing`, `captcha`, `验证码`, `请开启javascript`, and `capture_kind()` classifies on them. It is scoped to the wave-4 quarantine slice; `gate-records.py` never calls it. A literal grep confirms `client challenge` is in S234's capture (count 1). It does not contain `环境异常`, so it misses `712ec7bb…`.
So C1's "new" is the wiring into the gate, not the marker knowledge. The round-99 CHALLENGE marker list is a near-copy of the quarantine list and is not cited as such.

## Q2 — did any base instrument refuse a GATE-RECORD quoting a challenge capture?

Base tool = `git show 47ed34fa:tools/gate-records.py`, run as a standalone file.
- Forged GATE-RECORD for S230 (capture `b5b8d050eea0c638e95ba674`, sha256 `4f25f0b1…`, quote "Checking your browser before accessing"):
  base → `GATE_RECORD … S230 OK`, `GATE_RECORDS files=1 records=1 ok=1 fail=0`, exit 0 (`R99RevenPrior-q2_base_forged230.txt`).
  F → `S230 FAIL CHALLENGE`, exit 1 (`R99RevenPrior-q2_F_forged230.txt`). **Base admits it; F refuses it.** This is the round-98 defect reproduced.
- Forged GATE-RECORD for S234 (capture `b90988847e704a08aabc8321`, sha256 `c42ccd00…`):
  base → `FAIL CAPTURE_KEY,REFETCH,WORDS`, exit 1; F → `FAIL CAPTURE_KEY,CHALLENGE,REFETCH,WORDS`, exit 1
  (`R99RevenPrior-q2_base_forged234.txt`, `…q2_F_forged234.txt`). **At base the S234 record is refused, but by REFETCH/WORDS, not by a challenge check.** The battery's claim that base admits all seven challenge records rests on the battery's own constructed records (`corpus/evidence/round99/before/c1-base.txt`, `BASE_NEG_ADMITTED=7/7`), not on a production S234 record. I did not construct a base-admissible S234 record.
- `tools/research-gate.sh verify-metadata` on the forged S230 record: `DRIFT`, three META findings, all about missing `source`/`verified-at`/`recheck` (`R99RevenPrior-q2_resgate230.txt`). It never reads captures; it is not a challenge check.
- `grep -l 'challenge\|reCAPTCHA\|Just a moment' tools/*.py tools/*.sh` at F: `gate-records.py` (F) and `quarantine-check.py` (base content). Only quarantine-check has a challenge-marker list at base.
- Answer: **no base instrument refuses a challenge-capture GATE-RECORD**; the base gate admits the S230 forged record (exit 0).

## Q3 — quotation-error rates already in a lane file at base?

`git grep -n -i -E 'quotation (error|accura)|misquot|citation error' 47ed34fa -- corpus tools SKILL.md` → 37 lines, exit 0 (`R99RevenPrior-q3_base_grep.txt`).
- Zero hits for a published or measured citation-failure rate. `git grep -i "quotation error"` at base over corpus/tools/SKILL.md → no output.
- The 37 hits are `misquote` as a per-row class of the lane's own absent quotes: `tools/absent-split.py` (round 43), `corpus/evidence/round43/absent-split.tsv`, `corpus/lessons/round-43.md`, `round-44`, `round-48`, `round-57`, `round-65`, and the `S093` row of `citation-version-binding-r37.md`.
- So C2's literal "no knowledge entry contains 'quotation error'" holds. Its "new province ground" framing does not mention that the lane already classes its own absent quotes as misquote vs not-carried with a ratio bound (`absent-split.py`). That is a different unit (lane quotes, not a literature rate); it is an unacknowledged neighbour, not a contradiction.

## Q4 — R32 (verify-line whitespace)

Mutant: one site in the F tool, `f"SEARCH_RERUN {r['id']} rev=` → `f"SEARCH_RERUN  {r['id']} rev=` (python `str.count == 1` asserted; `MUTANT_SITES=1`).
Files: `R99RevenPrior-r32-on-F-selftest.txt`.

| check | F tool | R32 on F tool | receipt |
|---|---|---|---|
| `python3 -B tools/search-rerun.py --selftest` | exit 0, `PASS cases=67/67` | exit 0, `PASS cases=67/67` | `R99RevenPrior-r32-on-F-selftest.txt` |
| `corpus/evidence/round95/rerun-controls-r95.py --root <F clone> --work <scratch> --tool <tool>` | exit 0, `RERUN_CONTROLS=PASS` | exit 1, `RERUN_CONTROLS=FAIL`, 12 `CASE … FAIL` lines | `R99RevenPrior-r95-F-baseline.txt`, `R99RevenPrior-r95-R32-on-F.txt` |

- Not caught by the round-98 self-test: confirmed (`cases=67/67`, exit 0).
- Caught by round-95, as the round-98 seat's §3 said. The mechanism is incidental. The positive leg still passes (it checks only `SEARCH_RERUN: CLEAN` and `rev_match=8/8`). `strict-tree` and every forgery leg fail because the battery selects lines by prefix (`startswith("SEARCH_RERUN Q")`, `startswith(f"SEARCH_RERUN {qid} ")`); with two spaces the selection is empty. No leg asserts the exact verify-line shape.
- `[INFERENCE]` A mutant that changes only spacing inside the line after the prefix (e.g. a trailing space before `rev=`) would likely survive the round-95 battery, since it still matches the prefix; not run.
- **Proposed next-round rule (round 100):** the round-95 battery parses every `SEARCH_RERUN` line with an exact-form regex
  `^SEARCH_RERUN (Q[1-9][0-9]*) rev=(MATCH|DRIFT) tree=(SAME|CHANGED) recorded=[0-9]+ at_rev=[0-9]+ at_tree=[0-9]+( [A-Za-z_,]+)?$`,
  requires the count of matching lines to equal the record's row count, and fails on any non-matching line. Fixtures: the R32 double space,
  a trailing-space mutant and a tab mutant. Also: the self-test never calls `verify` (its docstring says so), so a self-test case that runs `verify` on a fixture record is the missing kill.

## Claim checks

**C1 `C1-GATE-CHALLENGE-R99`.**
- Numbers: the battery's stated counts were not re-run by me at F (that is the main agent's counting command). I did run the F tool on the battery inputs I could reach: `is_challenge` agrees with my hand classification on every ≤300-word capture (above). Held on that.
- The `before` receipt was not re-run by me; I verified the base tool's behaviour on S230 and S234 separately (above).
- **Wording overstated.** `claims.json` `type` says the gate "refuses a record whose capture is an interstitial challenge page". `712ec7bb981a9669a6921db7` at F is an interstitial verification page (12 words, Chinese), committed, and the F tool admits any record that cites it (`is_challenge` False). Named limit (a) ("in other words") covers it, but the claim's wording does not say so.
- **Coverage narrower than the committed set.** The battery's three committed NEG captures are S230 (`b5b8`), S229 (`0954`), S234 (`b909`) (battery lines 43–45 and 137). At F there are five English-marker challenge captures (`58725…` and `ff90…` are also pubmed cookie walls) that the battery does not use. No GATE-RECORD cites them (grep over `corpus/knowledge` and `corpus/lessons` at F).
- Novelty: the marker knowledge pre-existed in `quarantine-check.py` (see Q1).

**C2 `C2-ENTRY-R99`.**
- `python3 -B corpus/evidence/round99/entry-controls-r99.py --root .` at F → `QUOTES=23/23 FIELD=9/9 IDENTITY=2/2 WARRANTS=8/8 NUMBERS=6/6 TOPIC=1/1 NUMBERS_SOURCED=6/6 BASE_TOPIC_HITS=0 BASE_ENTRY=absent FORGERY_REFUSED=10/10 ACCEPTED=2/2`, `ENTRY_CONTROLS_R99=PASS`, exit 0 (`R99RevenPrior-c2_controls_F.txt`). Held.
- "No knowledge entry contains 'quotation error' at base": `git grep` at base → nothing. Held.
- Not run by me: the gate-record count, the metadata check and the rerun check on the entry. The decision-row faithfulness (K5, reviewer-judged) and the S236 quotes against the capture were not checked by me.
- Unacknowledged neighbour: `absent-split.py` (Q3).

## Receipts (all under `.ufo/waves/round-99/w1/`, prefix `R99RevenPrior-`)

Q1: `q229_F.txt`, `q229_all.txt`, `s234.txt`, `short_captures.txt`, `classify.txt`, `q1_classify_normed.txt`, `q1_all_is_challenge.txt`, `q1_false_refusal_scan.txt`, `wordcounts.txt`, `quarantine-base.txt` (copy of base `tools/quarantine-check.py`).
Q2: `q2_base_forged230.txt`, `q2_F_forged230.txt`, `q2_base_forged234.txt`, `q2_F_forged234.txt`, `q2_base_round98.md.txt`, `q2_resgate230.txt`.
Q3: `q3_base_grep.txt`.
Q4: `r32-on-F-selftest.txt`, `r95-F-baseline.txt`, `r95-R32-on-F.txt`, `r95_line_checks.txt`. SUPERSEDED (round-98 mutant file, invalid as an R32 test): `r32_selftest.txt`, `r32_selftest_wrap.txt`, `r95_on_R32.txt`.
C2: `c2_controls_F.txt`, `F_selftest.txt`.

Command exit codes of note: base forged S230 exit 0; F forged S230 exit 1; F round-95 baseline exit 0; R32 round-95 exit 1; R32 selftest exit 0.

## Verdicts

VERDICT: R99RevenPrior C1 fired — the wording "refuses a record whose capture is an interstitial challenge page" is false as stated: committed `712ec7bb981a9669a6921db7` (12-word zh verification page) at F is admitted by the F tool, and the battery covers three of the five committed English challenge captures; the numbers and the base-tool S230 admission hold.
VERDICT: R99RevenPrior C2 held — `ENTRY_CONTROLS_R99=PASS` (exit 0) at F and the phrase "quotation error" is absent at base; decision-row faithfulness (K5) and the gate/metadata/rerun counts were not checked by me.
