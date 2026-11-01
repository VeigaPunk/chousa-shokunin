# Round 66 — frozen claims (frozen at commit A, against base 4f784d9ee29ee7423d6c63bb2ba501d8ecb1ccee)

Frozen 2026-10-31 by chousa L1 (round 66). Three claims, distinct axes, causally
separable. Host adaptations declared up front: this Windows host has `python`
(3.13.15) and no `python3`, so every frozen command runs `python`; prior rounds'
`python3` receipts are cited as committed evidence, not re-run as written. The
round dispatch context bounds fetches to public read-only (WebSearch/WebFetch,
`gh`/`git` public reads); the open L0 fetch-scope questions from r40/r65 remain
unanswered and nothing beyond public read-only is fetched. No wave is dispatched:
this host has no batched AgentSwarm surface, §3 of the round contract makes
read-only helpers optional, and every verdict below rests on committed counters,
controls and receipts (the round-63 attempt-2 precedent, disclosed).

## C1 — calibration: SCORECARD receipt-attribution corrections (r65 verifier spot-check routed items 1, 2, 4, 5, 6)

Before (receipt `controls/before-c1-greps.txt`, at base): SCORECARD's round-65
verdict table says "After (measured at `0a851898`)" while both r65 after-receipts
pin `REVISION=1df2af73a79d038edf0b62ebc5691cb579ca3445` and no r65 measurement
receipt names `0a851898`; the depth per-axis line claims "depth improved
**narrowly** on the landed entry" against a claim the closure graded `unprovable`;
the axes table's operability row shows last-change round 1 with no note that the
numeric score is deliberately frozen; the newest capabilities heading is a bare
`## Capabilities` (line 3101) against the lane's `## Capabilities (round-N
addition)` convention; `source-openings.json` records S155's location as
"module documentation31-32" where the corrected entry and lesson say line 31.

Frozen counting commands (lane root; before → after):
1. `grep -c 'After (measured at `+backtick+`0a851898`+backtick+`)' SCORECARD.md` → 1 → 0
2. `grep -n '^## Capabilities$' SCORECARD.md | tail -1` → `3101:## Capabilities` → no bare heading at a line above 3105; `grep -c '^## Capabilities (round-65 addition)$' SCORECARD.md` → 0 → 1
3. `grep -c 'depth improved \*\*narrowly\*\* on the landed' SCORECARD.md` → 1 → 0 AND `grep -c "depth unprovable on the claim's counter" SCORECARD.md` → 0 → 1
4. `grep -c 'deliberately frozen at the historical' SCORECARD.md` → 0 → ≥1 (in the axes-table row)
5. `grep -c '"location": "module documentation31-32"' corpus/evidence/round65/source-openings.json` → 1 → 0 AND `python -c "import json;json.load(open('corpus/evidence/round65/source-openings.json',encoding='utf-8'))"` stays exit 0, and all four `sha256` fields unchanged (digest pins untouched; only the location string is corrected).

Sizing: a do-nothing control leaves the wrong pin, the bare heading, the
overreaching depth wording, the unexplained frozen score, and the wrong S155
location in place. Falsifiable: each command above flips state only if the edit
lands. Axis: calibration (SCORECARD entries match observed repo state — AXES.md).

## C2 — operability: semantic sourced-entry counter (capability acquisition; closes the r65 routed successor item "per-id citation reconciliation against corpus/SOURCES.md and non-empty claim bodies")

Before (receipts `controls/before-old-counter-boilerplate.txt`,
`controls/before-new-counter-boilerplate.txt`,
`controls/before-real-entry-clone.txt`; plus committed r65 wave evidence
`R65C03.md`/`R65M02.md`): the frozen r65 counter `c2-count.py` scores a 9-line
boilerplate entry + 3 stub registry rows + a README mention `10/10 PASS` —
reproduced on this host inside a scratch clone at base (`ENTRY_CHECKS=10/10
C2=PASS`, exit 0) — and no per-id reconciliation counter exists.

After: `corpus/evidence/round66/c2-semantic-count.py` (9 checks: TRIO,
IDS_DEFINED, MINED, USED_BY, TIER, ANCHOR, BODY_CITES, CLAIMS, LIMITS; exit 0
PASS / 1 predicate-fail / 2 usage-environment, with `LANE_REVISION`,
`ENTRY_SHA256`, `REGISTRY_SHA256` in every receipt). Frozen commands (lane root):
- `python corpus/evidence/round66/c2-semantic-count.py --entry corpus/knowledge/receipt-identity-r65.md` → `SEMANTIC=9/9 C2SEM=PASS` exit 0
- `python corpus/evidence/round66/c2-semantic-count.py --entry corpus/evidence/round66/controls/boilerplate-entry.md` → exit 1 (`SEMANTIC=6/9`, USED_BY+CLAIMS+LIMITS fail)
- registered variant `--registry corpus/evidence/round66/controls/boilerplate-registered-registry.md` → exit 1 (`SEMANTIC=7/9`; fully registered, fails the CLAIMS/LIMITS floors)
- token stub `--entry corpus/evidence/round66/controls/token-stub.md` → exit 1 (`SEMANTIC=0/9`)
- arm mutants m1–m6 → exit 1 with the named arm failing (m1 USED_BY; m2 IDS_DEFINED; m3 MINED; m4 TIER; m5 CLAIMS; m6 LIMITS)

Sizing: the recorded do-nothing class (boilerplate, registered or not; token
stub) cannot reach 9/9 — measured, not asserted. Disclosed limits: the floors
are minimal (a filler author who registers real mined rows, re-points used-by,
and writes ≥2 long claim items and ≥2 limit lines still passes — entailment
stays with the non-author reviewer, per the QUALITY-131 residual). Axis:
operability (new runnable artifact), the lane's lowest-scored non-retired axis.

## C3 — freshness: host-source drift recorded and re-anchored via a canonical pinned upstream (capability acquisition, sourced on rows opened this round)

Before (receipt `controls/before-host-pins.txt`, at base):
`python corpus/evidence/round66/host-pins.py` → `PINS_PRESENT=0/2`
(`P01 /usr/share/man/man1/git-cat-file.1.gz absent`, `P02
/usr/lib/python3.14/hashlib.py absent`), `GIT_VERSION=git version
2.55.0.windows.3`, `GIT_PIN_MATCH=no` against the 2.56.0 manual pinned by S154;
no drift record exists (`ls corpus/knowledge/host-source-resolution-r66.md`
fails); registry rows 157. The r65 local pins are unresolvable on this host and
nothing in the lane records that or the hop to a canonical surface.

After: the drift record `corpus/knowledge/host-source-resolution-r66.md` (cites
rows opened this round: S158 canonical upstream `git-cat-file.adoc` at pinned
commit `50fe5cc63f9cd6e89b87a2c9ccf96a444f4cfdb7` with committed capture bytes
+ sha256, quote re-opened `VERBATIM` by `tools/quote-reopen.py`; S159 this
round's own drift receipt; S160 rejected — the versioned git-scm.com HTML page,
rejected as an anchor source because its content moves with releases without a
pin); registry rows 157 → 160 (`bash scripts/sources-census.sh` row count and
validate exit 0 at round end). Frozen commands (lane root):
- `python corpus/evidence/round66/host-pins.py` → same drift values, now cited by the entry
- `ls corpus/knowledge/host-source-resolution-r66.md` → exists
- `grep -c '^| S158 |' corpus/SOURCES.md` → 1; same for S159, S160
- `sha256sum corpus/evidence/round66/captures/git-cat-file-50fe5cc6.adoc` → `3a8971e70ef50cc4b8c7b06c5696b382b30b4765303ab4dd986b140cd75cc847` (matches the pre-landing capture)
- `python tools/quote-reopen.py verify --items <gate tsv>` → `verbatim=1` exit 0 for the S158 quote

Sizing: a do-nothing control cannot record the drift, land the capture, or
register the canonical re-anchor — absence stays absence. Axis: freshness
(drift detection against the current host; citation-chain hop resolution).
