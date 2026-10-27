# Round 57 — frozen claims (chousa)

author: chousa L1 (hyaku run 9, agent `ChousaR57`)
date: 2026-10-27
base: `6656f0770a1460d6ba73d9d2976f698a35311921` (lane master at round start = the round-56 closure spot-check commit)

Claims are frozen one at a time, each in its own lane commit before any of its data exists: R57-C2 first (before any
fetch of this round), then R57-C1 and R57-C3 in later sections of this file, each naming its freeze commit in the
report. A section, once committed, is never edited; corrections are appended below it.

Egress: the campaign capture cache this lane's counters read (`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/`)
was deleted at about 02:16:49 -03 (L0 `a714799f`). The orchestrator's round-57 note directs: "Any claim needing
captures must re-fetch into lane-owned evidence (committed bytes + sha256) and say so". Fetch scope this round is the
approval table `corpus/evidence/round57/egress-approval.md` (credential-free GET of public documents only). L0
`8d77e6c1` stays open; the report says which fetches ran.

## R57-C2 — freshness: the lane's pinned captures re-fetched into lane-owned, digest-checked bytes

Axis: freshness ("skill claims re-verified against live surfaces; stale items flagged"). The surface it moves: the
lane's span manifests pin 47 captures by sha256 that exist nowhere on this host since the cache deletion, so no
pinned quote can be re-verified and no drift can be seen. After: each pinned capture has a verdict recomputed from
committed lane bytes.

**Frozen predicate (one sentence, = the `c2-count.py` docstring):**

for each of the 47 distinct (id, url, capture_sha256) triples pinned by the
spans manifests committed at SET_REV (every `corpus/evidence/**/spans.tsv`
with a `capture_sha256` column), the lane holds exactly one verdict
recomputed from committed bytes — REPRODUCED: a lane-owned capture
`corpus/captures/<key>.raw` (key = first 24 hex of sha256(url)), whose
sha256 equals the raw_sha256 of the triple's last successful attempt in
`corpus/evidence/round57/refetch.tsv`, has the pinned digest itself or a
`<key>.txt` beside it that has it; DRIFTED: such a capture exists and
neither digest equals the pin; UNREACHABLE: no capture, and at least two
failed attempts (curl_rc != 0, or http_code outside 200-299, or an empty
body) recorded at least 600 seconds apart — and every byte-backed capture is
CONSISTENT (its `.txt` equals the frozen campaign recipe applied to its
`.raw`: a `%PDF-` raw through `pdftotext -layout` 26.08.0 when that text is
non-blank, otherwise the raw decoded as UTF-8 with replacement and, when it
starts like HTML, the campaign's `html_to_text`), and every DRIFTED capture
on which some quote of a spans row pinned to that triple no longer occurs
in its defined text form (an OLE or zip raw: the stdout of
`tools/capture-text.py`; otherwise the `.txt`) is FLAGGED by the line
`- FRESHNESS-FLAG <id> <key> absent=<a>/<m>` in
`corpus/lessons/round-57.md` with the counter's own a and m — counted
`SET=47 VERDICTS=47/47 CONSISTENT=b/b FLAGGED=g/g` with REPRODUCED >= 5 and
BYTE_BACKED (REPRODUCED + DRIFTED) >= 32, printed `C2=PASS`.

Counter: `python3 corpus/evidence/round57/c2-count.py` (SET_REV = base). Kill rule: any other line, or exit != 0, at the
after-measurement = C2 not verified; no target, threshold or recipe changes after this commit.

Targets and where they come from (before data): REPRODUCED >= 5 is the round-56 closure's own live re-fetch, which
reproduced the forms of S118 and S127-S130 (`corpus/lessons/round-56-verifier-spotcheck.md`, C2 table) — a floor
known reachable, not a guess. BYTE_BACKED >= 32 is two thirds of the set, chosen before any round-57 fetch. The recipe
is the campaign's own (`quote-lint.py` `fetch()`/`html_to_text()`, sha256 `e864a01f26ac92fda281b1b04eaeb6c47b7cd843726b012511b8d980eff7b958`
at shokuknow `03d69cd9`), read, never run.

What the counter cannot prove (disclosed before data): DRIFTED and UNREACHABLE are attested by the fetch record; only
REPRODUCED is bound to the pin by a digest no forge can meet. A forge with five genuine captures and 27 random-byte
"drifted" ones would pass; the REPRODUCED count is printed separately for that reason and the wave attacks it.

Before (`controls/c2-before.txt`): `SET=47 VERDICTS=0/47 REPRODUCED=0 … C2=FAIL`, exit 1. Controls
(`controls/c2-controls.txt`, fixtures by `controls/build-c2-controls.py`): EMPTY `VERDICTS=0/47`; JUNK (random bytes,
recipe-consistent `.txt`, successful records) `VERDICTS=47/47 REPRODUCED=0 DRIFTED=47 FLAGGED=0/47 C2=FAIL`; ALLFAIL
(two failed attempts 700 s apart each) `VERDICTS=47/47 REPRODUCED=0 UNREACHABLE=47 C2=FAIL`. No control meets the target.

Separability: C2's counter reads only `refetch.tsv`, `corpus/captures/`, the round-57 lesson's FRESHNESS-FLAG lines,
the committed manifests at SET_REV and `tools/capture-text.py`; it never runs a gate, a probe or the span builder.

## R57-C3 — depth (sourced): the workflow standard's normative references chained to their own documents

Axis: depth (verifiable detail; citation chaining, the lane's own method). Lead: the round-56 closure's routed item 4
(`corpus/lessons/round-56-verifier-spotcheck.md` §6.4: S127 `2 规范性引用文件` names the national centre's instruments).
The surface it moves: the lane holds the standard (S127) and one of the seven documents its normative-reference
clause lists (S118); none of the others is held, and no entry says what the clause binds a user of the standard to.

**Frozen predicate (one sentence, = the `c3-count.py` docstring):**

the lane entry `corpus/knowledge/normative-reference-chain-china-r57.md`
exists, cites S127 as `source: S127 — <S127's first URL>` with S127's
`used-by` naming it, and holds `规范性引用文件` (absent from `corpus/knowledge`
at BASE_REV); `corpus/evidence/round57/c3/spans.tsv` carries an S127 row
whose quote contains `规范性引用而构成本文件必不可少的条款` (CLAUSE); of the
seven references S127's `2 规范性引用文件` lists (R1 the 2019 notice
〔2019〕80号, R2 the 2021 notice 〔2021〕16号, R3 the 管理指南 2021年版, R4-R6
the 抗肿瘤 / 心血管病 / 儿童 技术指南 2022年版, R7 the 质量控制指南 2024年版)
at least four are BOUND — some lane Registry row X other than S127, S128 and
S129 and whose first source-cell URL U is none of theirs, either new since
BASE_REV (`mined`, opened 2026-10-27) or held, whose `used-by` names the
entry and which the entry cites as `source: X — U`, whose lane-owned capture
`corpus/captures/<key(U)>` is the bytes of a successful attempt for (X, U) in
`corpus/evidence/round57/refetch.tsv`, whose DEFINED text form (an OLE or zip
`.raw` through `tools/capture-text.py` as at BASE_REV, else the `.txt`) holds
the reference's edition token (whitespace removed) and its title as a
HEADING (a line that, whitespace removed and one trailing `（…）`/`(…)`
dropped, ends with the title after a prefix of at most 16 characters holding
none of `《》.[]［］`), and for which the manifest carries at least two rows
of id X and URL U with the form file's digest, one of whose quotes holds that
title — and every reference not bound carries a line
`- UNBOUND R<k> sweep: <queries and hosts>` in the entry; every manifest row
is a quote of at most 25 whitespace words and 160 characters inside its span
file, the entry and the round-57 lesson, its span file the exact slice at the
recorded offset of the form whose digest is recorded and longer than the
quote; the round-51 `quote-substance-check.py` exits 0 on the manifest; every
`char N` of a new bound row's `anchor` cell (at least one) is a quote offset
of that id; the entry exits 0 under `tools/inference-ground.py` with this
manifest; and no `S###` token in the entry names a row other than S127 or a
bound row — counted `C3=PASS`.

Counter: `python3 corpus/evidence/round57/c3-count.py` (BASE_REV = round base). Kill rule: any `C3=FAIL` or exit != 0 at
the after-measurement = C3 not verified; no title, token, threshold or exclusion changes after this commit.

Target (before data): BOUND >= 4 of 7, chosen before any search for the six unheld documents; the held S118 alone
binds R7 (control HELD), so a do-nothing chain reaches 1. The heading rule was written after reading how S127, S128
and S129 print the titles (citations in 《》 or GB/T 7714 reference-list lines `….标题（…）[EB/OL]`); on the held
captures it finds a heading only in S118 (R7) and S130 (R3's title, without the `2021年版` token, so S130 cannot bind
R3) — pre-freeze checks of the rule, not measurements.

Before (`controls/c3-before.txt`): `ENTRY=no … BOUND=0/7 … C3=FAIL`, exit 1. Controls (`controls/c3-controls.txt`, by
`controls/build-c3-controls.py`): HELD (entry chained through S127's clause, S118 and S130 only, every quote real)
`BOUND=1/7 (R7:S118) … C3=FAIL`; CITER (HELD plus a new row on the explanatory note, which cites every title)
`BOUND=1/7 … C3=FAIL`.

Separability: C3 reads the registry, the entry, the lesson, its own manifest `corpus/evidence/round57/c3/spans.tsv`,
`refetch.tsv` and `corpus/captures/`; it never runs a gate, probe or builder. It shares the capture store with C2
(content-addressed by URL key): C3's documents are not in C2's frozen set of 47 except S127 and S118, whose C2 verdicts
do not depend on C3.
