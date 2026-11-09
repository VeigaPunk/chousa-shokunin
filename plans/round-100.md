# chousa round 100 — plan (L1 `ChousaR100`)

Base `929c784c63a1fd17961d21742101b2b109b7b8ff` (round-99 landing plus its non-author spot-check). No earlier attempt
of round 100 (`.ufo/watchdog.log`: one `launch chousa round=100 … attempt=1` line); lane clean at start (`jj-lane.sh
state`: ahead=0 tracked=0 untracked=0); nothing inherited.

## Load and inputs

Read: the round prompt (`.ufo/prompts/chousa-round-100.md`, §1-§8 and amendments through 65), SCORECARD `## Planned —
round 100`, `corpus/lessons/round-99.md`, `corpus/lessons/round-99-verifier-spotcheck.md`, `plans/round-99.md`,
`.ufo/waves/round-99/w1/R99SentinelC1.md` (F-1, F-4), `R99MutantsC1.md` (13/28 survivors, 6 battery loosenings),
`tools/gate-records.py`, `corpus/evidence/round99/*`, QUALITY 126, CORPUS.md registry rules, AXES.md (freshness).
Fresh-start rule: not bound (MANIFEST closures r92-r99 admitted).

Round-99 spot-check routed defects:
1. `after-f2/c1-all.txt` control label corrected by hand — not repeated: every round-100 receipt is a command's own
   output written by redirection (`corpus/evidence/round100/before/*`), no receipt edited after its run.
2. C1 limits the wave measured — this round's C1: rev path spelling (`R99SentinelC1` F-1, routed limit (d)), per-marker
   and 199/200/201 fixtures (`R99MutantsC1` m02-m14), whole-blob rev fixture with a non-marker line (`R99SentinelC1`
   F-4), SETUP instead of a crash on a missing capture (receipt `before/c1-setup.txt`: round-99 battery
   FileNotFoundError, round-100 battery exit 2). The six battery loosenings b1/b3/b4/b6/b7/b8: the round-100 NEG/POS
   legs keep the verdict-and-rc conjunction; their mutation is a wave item, not a claim.
3. S235's flip condition and the 2025 update's Europe PMC record — lane GETs this round (S237: 500 ×3; S238: 200,
   admitted; S239: 500 ×3). S235's flip stays unmet by the lane.
4. Seat hygiene — wave context requires seat-prefixed receipts; the L1 uses `edit`/python writes, not `sed -i`.
5. Fleet tier question (index-record abstracts) — unchanged; S238 graded B under the lane's carrier rule, as S236.

## Claims (frozen in `.ufo/waves/round-100/claims.md`)

- C1 operability (lowest axis): rev records judged by capture object identity (`tools/gate-records.py`
  `rev_capture_text`, `capture_oids`), battery `corpus/evidence/round100/challenge-controls-r100.py`.
- C2 freshness: `corpus/knowledge/quotation-error-update-r100.md` answers the round-99 entry's `recheck: on-release`
  (S238, opened this round) and the round-99 entry gains `## Update`; controls
  `corpus/evidence/round100/entry-controls-r100.py`.

Pre-freeze design change P0: the first C1 draft normalized the path (`posixpath.normpath`) and also matched object
ids; the object-id match subsumes the normalization (every git-resolvable spelling resolves to the same object), so the
draft was cut to identity only before P. The battery's first run at the draft showed oracle o12 (`norm` dropped inside
`is_challenge`) surviving, because the url/admit branch passes pre-normalized text; rev leg r11 (a capture whose marker
is split by a newline and a tab) was added before P and kills it (`before/c1-candidate.txt`).

Routes (approval table `corpus/evidence/round100/egress-approval.md`, written before the first GET; `refetch.tsv` rows
S237-S239).

## Wave

One v1 wave, 12 seats (`.ufo/waves/round-100/build_spec.py` → `w1-spec.json` → validated `w1-dispatch.json`). The L1
holds the canonical planner seat (the validator refuses `planner`). No residual call planned.

## Freeze

P = `9683523467a1be9a9c46972f9b92bed26f44750d` (pre-freeze build: tool, battery, entry, controls, rows S237-S239).
Pre-freeze controls ran on a clean shared clone at P and landed in R = `6f837487be6cf686bcee16902299dba34ec7f063`
(`corpus/evidence/round100/before/`: `c1-base.txt` FAIL exit 1, `c1-candidate.txt` PASS exit 0 with
`ORACLES_REJECTED=12/12`, `c1-setup.txt` exit 2, `c2-base.txt` exit 2, `c2-prelink.txt` FAIL exit 1,
`c2-candidate.txt` all exit 0).
F = the commit that first carries `claims.md`; recorded here by the commit after it.
