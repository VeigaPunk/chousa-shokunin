# Round 30 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_opus)

Date: 2026-10-23 UTC (host clock UTC-3). Runtime model string exposed to this closure session:
`anthropic/claude-opus-5-5` (reached through the configured `task` route; no model parameter was
passed). Three read-only seats re-checked parts of the evidence: ChronoR30 (critic), ReceiptsR30
(reviewer) and CorrectionsR30 (reviewer). None died, and none was re-sent. They are named where
their findings are used. Driver digest, copied from `.ufo/watchdog.log` (lines 806 and 815):

```
2026-10-22T23:39:45-03:00 launch chousa round=30 pgid=1886412 driver=hyaku-inline attempt=1
2026-10-23T00:50:45-03:00 complete chousa round=30; hyaku-inline attempt=1
```

## Decision

**Status `ok`, not admitted (`rejected-honest-stop`).** The round declared two claims.
C1 (coverage: pages that omit `</head>`) verifies on its frozen predicate. C2 (operability: fetch
bounds under slow senders and DNS rebinding) does not. The frozen kill rule needs
`QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`, and the landed tool printed 26/27 on 3 of 44 fresh-seed
runs. The lane reported this as a miss and did not re-scale the counter. That is the honest
outcome. No axis is harmed. The admission rule is that every claim verifies, so the round is not
admitted. I did not weigh the lane's earlier admit.

Rulings on the orchestrator's questions:

1. **Did every design change come before data? Yes.** The first data seat is
   `build/ExecC1Head/c1-run1.json` at 2026-10-23T03:22:04Z (106/106, a pre-landing candidate). The
   earliest committed build receipt is CriticD3Classes at 03:16:26Z, but it scores round-29
   mutants, not a candidate. Every design commit is earlier:
   - v2 `6b1c5177` at 02:53:45Z
   - C2 v3 `bf657822` at 03:02:04Z, with its claims note `7908ce2a`
   - wording `dad857af` at 03:03:08Z and `00cf2365` at 03:03:17Z
   - v4 `abfdf932` at 03:07:40Z
   - wording `60d51f79` at 03:13:52Z

   The build spec is `a0bc50b7` at 03:14:29Z. Since `60d51f79`, the C1 counter (`5b312d84…`),
   the C2 counter (`0a59e373…`), the harness (`e2be0dd1…`) and `claims.md` are byte-identical
   (`git log 60d51f7..b9ed43c6` on these paths is empty).

   One count is wrong. The report (`:81`) and the lesson (`:135-136`) say "four controls forced
   pre-data redesigns". The receipts show three control findings and two control-forced
   redesigns:
   - CtlShapeKeyed met C2 v2 20/20, which forced v3.
   - CtlNoReader reached 104/106 on C1, which forced v4.
   - CtlTrivialC2 and CriticClaimDesign30 found the slow-ok terminator gap, which also went into
     v4.

   v2 came from the L1's own read (lesson `:29`). The wording commits changed no counter or
   harness byte. This is routed as D3. It does not change the chronology, and it does not change
   the status.
2. **Are the three round-29 mutants killed? Yes,** on the landed tool and the frozen C1 counter:
   MutR29Order 104/106, MutR29SkipScript 66/106, MutR29Casefold 86/106
   (`falsify/MutR29*/`, ReceiptsR30). Each has pristine and restored runs at full score. A new
   survivor, MutHeadNoText, scores 106/106. The lane discloses it and carries it.
3. **Containment.**
   - The whatwg redirect is disclosed. ReviewContractV2 followed the redirect once, to
     html.spec.whatwg.org. The disclosure is `build/ReviewContractV2.md` finding 13 (lines 185-195,
     and 238-243). The lesson (`:57`) cites "finding 7", which is the wrong number (D8).
   - The misrooted ConnectorKagiPin report was moved correctly. The lane copy landed at
     `b9ed43c6`. The fleet path `.ufo/waves/round-30/` is absent, and
     `git -C <fleet> log --all -- .ufo/waves/round-30` is empty, so it was never committed to the
     fleet.
   - Dead seats: the report says "holds, not retried", which is not accurate. CriticS047Live died
     on HTTP 429 in the build wave. Its task (round-29 tool on S047 with the round-29 Gate quote
     and two more body sentences) was re-issued in the falsify wave as `LiveS047After`. It used
     the same `critic` role (`build-dispatch.json` vs `falsify-dispatch.json`), and this was not
     disclosed as a retry (D6). No dead seat's task was re-sent under a different role.
   - My own re-opens touched only registered hosts: docs.python.org, and www.w3.org with
     `--max-redirs 0`.

## Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| report landed by the lane | `git log --format='%an %H %cI' -- .ufo/reports/round-30/chousa.md` | `chousa-shokunin 54c617b1086734bc2550774191c532bd20ced2fb 2026-10-23T00:50:30-03:00` | pass |
| SHONEN heading, one line per box | report `## SHONEN`; `git show b9ed43c6:SHONEN.md \| grep -cE '^\s*- \[[ x~]\]'` | 4 report lines `[~]`, 4 boxes, all `[~]`; SHONEN.md and PROVINCE.md unchanged this round | pass |
| cited hashes exist and are ancestors of `master` | `git merge-base --is-ancestor <h> master` for f42906d7, 6b1c5177, bf657822, 7908ce2a, dad857af, 00cf2365, abfdf932, 60d51f79, a0bc50b7, 33dd643f, bd43bd53, 49b2aa30, 0dc6e81c, a9d3a05a, fc97f43b, b9ed43c6, a3a3710e | all are commits, all are ancestors | pass |
| fleet L0 commit | `git cat-file -t 8d77e6c1` in the fleet; ancestor of fleet HEAD | commit by `chousa-shokunin`, ancestor | pass |
| lane pushed, clean | `jj-lane.sh state …`; `git status --porcelain` | `ahead=0 behind=0 local=remote=b9ed43c6…`; porcelain empty | pass |
| remote | `git ls-remote origin refs/heads/master` | `b9ed43c64e373b98176dd6e03f0c8259c21122fb` | pass |
| prompt carries template contract | every literal line of `templates/round-prompt.md` (140 lines; 105 non-empty lines without placeholders) is found in `.ufo/prompts/chousa-round-30.md` | 0 missing | pass |
| census at closure | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` | `chousa ok`, exit 0, two W04 warnings (S051/S050 and S053/S052 share a page URL) | pass, as reported |
| diff shape | `git diff --numstat a3a3710e b9ed43c6` | 605 files, 154712 insertions, 19 deletions; all 19 deletions are in `tools/quote-reopen.py` (+135/−19); every lane record file is insertion-only (CorrectionsR30). S050/S055 SOURCES edits change rows added this same round (`a9d3a05a` → `fc97f43b`) | pass |

Conformance defects (status-neutral):
- The report heading says "report 03:52Z", but the report commit is 03:50:30Z. The report states
  a time later than its own commit.
- The report cites `7908ce2a` as "C2 v3", but the counter and harness bytes for v3 are in
  `bf657822`.
- The report's work-items list omits `dad857af`.
- The other defects are routed below.

## Claims — re-check against `b9ed43c6`

Both claims are **evidence-verified, not re-executed**. The counters run a lane-owned loopback
harness around a candidate. Under §Gate standard (Closure consequence), the integrator verifies the
committed evidence and does not execute a sibling's measurement machinery. These were plain reads
of committed bytes:

| Check | Command | Observed |
|---|---|---|
| tool identity | `git show b9ed43c6:tools/quote-reopen.py \| sha256sum`; `git diff --quiet 49b2aa30 b9ed43c6 -- tools/` | `47a657e72f38…222a1201`, equal to the reported `47a657e7…1201`; tools identical to `49b2aa30` |
| frozen design | sha256 of the counters and harness at `33dd643f`, `bd43bd53`, `49b2aa30`, tip | C1 `5b312d84…`, C2 `0a59e373…`, harness `e2be0dd1…` at every revision (matches `claims.md:25-27`) |
| C1 before | jq over `controls/before-c1-v4-run{1,2}.json` | 78/106 each, round-29 tool `72a3ad47…`, frozen hashes |
| C1 after | jq over every C1 receipt carrying tool `47a657e7…` | 14 runs: `measure/after-c1-run{1,2}` 2, RerunC1A/B/C 9, `CriticClaimsAfter/c1-run{1,2,3}` 3, all 106/106. 18 more landed receipts are 106/106. 3 low-resource-cap attempts are 106/0, each disclosed as inconclusive. **Met.** The report's "9 … and 14 in CriticClaimsAfter" double-counts: CriticClaimsAfter's 14/14 already includes the 9 and the 2 (D4) |
| C2 before | jq over `controls/before-c2-v4-run{1,2}.json` | 12/27 each, round-29 tool, frozen hashes |
| C2 after | same tally for C2 | 44 runs: measure 2, RerunC2A 5, RerunC2B 23, RerunC2C 5, CriticClaimsAfter 9. 41 at 27/27; 3 at 26/27 (`RerunC2B/run2`, `run4`, `extra16`). Each miss is a slow-ok item answered `UNREACHABLE`, 0.068 s, 0.066 s and 0.062 s after its DEADLINE, with `bound_ok` true and no unvalidated destination. **Not met** under the frozen kill rule, as reported |
| rev A | `measure/revA-c2-run1.json` | 24/27 on tool `0150361a…`, the `33dd643f` blob; fixed at `bd43bd53` |
| v4 controls | tally of the receipts carrying the v4 counter hashes (ChronoR30) | 61 receipts, all `predicate_holds=false`. Best C2 is 18/27 (wall cutoff 3.8 s), as reported. Best C1 is **86/106** (`CtlParseShortcuts/receipt-skip-nothing-v4.json`), not the reported 84/106; 84 is the best no-reader control (D5) |
| backlog diagnosis | `qr_harness.py:147-149`, `c2-count.py:197`; `git ls-tree` | The backlog of 5 is supported by committed code (`ThreadingTCPServer` default queue, `max_workers=len(specs)`). The 18/18 backlog-128 receipts exist only in `/fast/scratch/hyaku/chousa-r30/w2/RerunC2B/bl/`. `RerunC2B.md:45,57` tags the mechanism `[INFERENCE]`, but the lesson (`:102-104`) and the report (`:58`) state it as fact (D2) |
| no harm | `git diff --quiet a3a3710e b9ed43c6 -- tools/research-gate.sh`; SCORECARD diff | gate unchanged; the round-29 counter scored 130/130 on the landed tool (`falsify/NoHarmR29Counter.md`). The SCORECARD diff is insertions only: D1/D2 dated corrections, Round 30 table (C1 met, C2 "not met (miss under the kill rule)"), operability 3 → 3, a capabilities row. No axis score is lowered |
| D1–D6 repairs | CorrectionsR30 | D1 SCORECARD correction cites the DiffToolB network receipt (8 GET, 8 × 200). D2: `rerun-check.py` (local reads only) prints `RERUN_RECEIPTS=5/6`, exit 1. D4 is appended at `lessons/round-25.md:264-269`. D5 is appended at `lessons/round-29.md:123` onward. D6 manifest: the 3 hashes that round 29 states match, and the 4 committed copies match the manifest. QUALITY 26-29 each cite `lessons/round-30.md` |

## Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| coverage | improved | C1 verifies: 78/106 → 106/106 on 14 landed runs under the frozen v4 predicate, with the frozen bytes unchanged after `60d51f79` |
| operability | unchanged | C2 missed its frozen predicate (26/27 on 3 of 44). The round-1 scale is 3 → 3. No harm: `research-gate.sh` unchanged, round-29 counter 130/130 |
| depth | unchanged | not claimed; new knowledge entry and SKILL rows, insertions only |
| freshness | unchanged | not claimed; the S052, S055 and S050 fixes are to rows opened this round |
| calibration | unchanged | The miss is reported honestly and the predicate is kept as frozen. Several overstatements were not caught before the report: the C2 held-ground row in README, four controls, the C1 run count, the backlog diagnosis stated as fact, and "not retried". All are routed defects. None contradicts SCORECARD or SHONEN state |
| adjacency | unchanged | the kotodama `reopen-quote.py` adjacency is reported, not absorbed (`falsify/ConnectorKagiPin.md`); PROVINCE unchanged |

## Discernment spot-check

Source: `corpus/lessons/round-30.md` `## Gate`. I re-opened each page on 2026-10-23 with Python
`urllib`, extracted the text with `html.parser` (script and style dropped), and applied NFKC and
whitespace folding.

| Item | Gate decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S053 | admit | https://docs.python.org/3/library/socket.html (200, 309740 B) | agree | quote found verbatim in `create_connection`, 22 words; continues "until a connection succeeds" |
| S055 | admit | https://docs.python.org/3/library/ssl.html (200, 359936 B) | agree | quote found verbatim, 10 words; the corrected teaches cell (no address-validation claim) matches the page |
| S056 | admit | https://docs.python.org/3/library/ipaddress.html (200, 146106 B) | agree | quote found verbatim under `is_global`, 17 words; the row's "100.64.0.0/10" exception is on the page |
| S050 | admit | https://www.w3.org/TR/2017/REC-html52-20171214/syntax.html (200, 4415303 B, SHA-256 `1db65aefdde4…`, equal to the Gate's `1db65aef…`) | agree | quote found verbatim in Optional tags, 23 words |
| S051 | admit | same page | agree | quote occurs twice: under "An end tag whose tag name is "head"" and under "Anything else", which is the branch the Gate names |
| S052 | admit (Gate quote corrected in the lane's falsify wave) | socket.html | agree with the admit and the correction | The Gate's original quote ends "…for the socket." and is **absent**: the page continues "(they raise a timeout exception)…". The corrected 17-word quote is found verbatim. This Gate error is not mined in `## Mistakes` (D7) |
| undated `https://www.w3.org/TR/html52/` URL | reject | `curl -D - --max-redirs 0` on `/TR/html52/syntax.html` → 301 to `/TR/html/syntax.html` → 307 to `https://html.spec.whatwg.org/multipage/syntax.html` | agree | it redirects to an unregistered host while the L0 fetch-scope question is open; the lane used the dated W3C snapshot (S050) instead |
| "C2 at 27/27 shows the tool is safe on the real network" | reject (inference) | `corpus/evidence/round30/claims.md` §Not claimed (`:213-219`) | agree | the counter is loopback-only plain HTTP; TLS, IPv6, resolver time and per-hop provenance are listed as not claimed |

SOURCES row check: the S053 row (`corpus/SOURCES.md:63`) has scope "not a guarantee of DNS
pinning". Its teaches cell ("resolves a host name itself and tries each address") matches the
page. Its ≤25-word quote is the Gate quote above (22 words), verified. The census matches the
report: rows 49 → 56, tier A 43 → 50, mined 26 → 33, `chousa ok`, exit 0, two W04 warnings.

## Trend verdicts

- **expansion: improved.** Pages that omit `</head>` are new held ground, measured by C1. The new
  entry `knowledge/quote-reopen-r30.md` cites mined tier-A rows S050-S056. The knowledge entry
  states the C2 miss. The README coverage map overclaims C2 (D1), but README is not an admitted
  entry.
- **quality: unprovable-but-better.** D1, D2, D4, D5 and D6 are repaired, append-only.
  QUALITY 26-29 each have a lesson and a shown-able-to-fail check. One Gate quote (S052) failed its
  re-check this round and was marked with a dated correction, so this is not `harmed`. The
  `improved` condition ("no admitted entry failing its re-check") is still not met.
- **discernment: improved.** The outside spot-check agrees with the Gate on six admits and two
  rejects. For S052 it agrees with the admit and with the lane's own correction. The calibration
  overstatements are routed below.

## Routed defects (lane fixes next round)

1. **D1 (medium): README contradicts the miss.** `corpus/README.md:942-948` ("Round30 frontier
   disposition") says C2 fetch bounds moved to held ground (12/27 → 27/27). Append a dated
   correction: C2 missed under the kill rule, so only the pages without `</head>` are held. Also
   fix the capabilities-row evidence pointer that still gives `c2-count.py → 27/27`.
2. **D2: Backlog diagnosis stated as fact.** The lesson (`:102-104`) and the report (`:58`) say the
   listen queue "overflowed". The seat tags it `[INFERENCE]` (`RerunC2B.md:45,57`). The 18/18
   backlog-128 receipts are in `/fast/scratch` only. Append a correction marking it inferred, and
   commit the `bl1..18.json` receipts (or their hashes and paths). A next C2 counter version that
   sets `request_queue_size` must be declared before data, as a new version; never edit the
   frozen v4 bytes.
3. **D3: "Four controls forced pre-data redesigns"** (report `:81`, lesson `:135-136`). The
   receipts show three control findings and two control-forced redesigns (v3; v4 for C1 and C2).
   v2 came from the L1's read. Append a correction.
4. **D4: C1 re-run count.** "9 in RerunC1A/B/C, 14 in CriticClaimsAfter" (report `:57`) implies
   25 runs. CriticClaimsAfter's 14 already includes the 9 and the 2 measure runs. Correct it with
   `rerun-check.py` (QUALITY 27). Also correct `CriticClaimsAfter.md:31` "RerunC2B 17/20" to the
   committed 20/23.
5. **D5: v4 C1 control maximum.** The report says 84/106, but the committed maximum is 86/106
   (`CtlParseShortcuts/receipt-skip-nothing-v4.json`). 84 is the best no-reader control.
6. **D6: Undisclosed re-issue of a dead seat.** CriticS047Live (HTTP 429) was re-issued as
   LiveS047After (same `critic` role, same task core) while the report says "not retried". Record
   it as a retry, or keep dead seats dead. Also, CriticHarnessIntegrity refused, but its
   `leak-map.py` and `metadata-audit.py` landed at `abfdf932` with no report, and
   `ReviewQuality30.md:44` counts `leak-map.py` as a control. Mark those files as unreviewed
   output of a refused seat.
7. **D7: S052 Gate error not mined.** Add a `## Mistakes` row (non-verbatim Gate quote, caught by
   the falsify re-open), and add a QUALITY criterion if none caught it.
8. **D8: Wrong pointers and low notes.**
   - ReviewContractV2 "finding 7" should be finding 13.
   - The report cites `7908ce2a` for C2 v3; the counter bytes are `bf657822`. Its work items omit
     `dad857af`.
   - The report time "03:52Z" postdates the report commit (03:50:30Z).
   - The D1 SCORECARD block says "one DiffToolB run only", but `landed-heldout.network.json` is a
     second run.
   - The D4 quote came through NCBI E-utilities, an unregistered host, with no bytes kept.
9. **Carried (operator or later rounds):**
   - the L0 fetch-scope question (fleet `8d77e6c1`)
   - resolver and dial time outside DEADLINE
   - uncancelled hop timers
   - the MutHeadNoText survivor
   - 2xx challenge pages, IPv6, and pages without a `<head>` start tag

SHONEN: all 4 boxes are `[~]` with pointers. Box 3 (`python3 corpus/evidence/round30/c1-count.py`
runs without oral context) is checkable by a non-author. The other three need a reviewer's
reading of SKILL.md and PROVINCE.md. Promotion is operator-owned, and this closure does not grant
it.

Tools installed or updated by this closure: none.
