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
