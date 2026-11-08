# chousa round 84 — frozen claims

Base (round-83 tip, closed `rejected-honest-stop`): `408ae68f9e445fc911f713d5bbb3a64dda1ab9fe` (HEAD before this freeze).
Egress table: `corpus/evidence/round84/egress-approval.md`, committed before any fetch (this file's commit precedes every
round-84 refetch row; closure compares commit time with `fetched_utc`).

Fresh-start reads (done before this file, per Amendment 58 fresh-start binding + §9 do-nothing control): round-81/82/83
verifier spot-checks, `corpus/lessons/round-81.md`, `round-82.md`, `round-83.md`. r83's routed defects 1–4 are the
specification for C1 below; r73's `load()` additions/deletions swap (QUALITY 164–165) is the reason C1 binds on the
public production path (`python3 tools/gate-records.py verify`), not on a helper re-implementation.

## C1 — operability (lowest scored non-retired axis, historical 3/10) — capability acquisition

**Claim.** The repaired lane tool `tools/gate-records.py verify` (post-scoring repair `c7d29e1c`, ASCII digit classes,
rev-quote `"` boundary) passes a successor battery it could not pass before the repair, measured on this Linux host
through the public CLI only:

- positives: the 15 frozen GATE-RECORD lines of `corpus/lessons/round-80.md`, `-81.md`, `-82.md` in
  `c2-positives.tsv` (byte-equal, tool prints `OK`) — 15/15, tool exit 0;
- forgeries: every mutation class listed below applied to every positive of its form, each forged line in its own
  file, all given to one tool run — every forgery refused (tool exit 1) **and** refused with its expected code;
- empty: one file with no GATE-RECORD line — tool exit 1 (no records is not a pass).

**Counting command (frozen; sha256 in `instrument-pins.txt`):**
`python3 -B corpus/evidence/round84/gate-records-r84.py --root DIR --repo GITDIR --work DIR`
where DIR is a `git archive <rev>` extraction of the landing revision and GITDIR is the lane checkout (read-only
`git cat-file` by the tool only). The counter reads the tool at `DIR/tools/gate-records.py` and its positives from
`c2-positives.tsv` beside it; no helper re-implementation.

**Mutation / forgery classes (all committed lane bytes; each is an `EXPECTED_CODE` the counter checks):**

1. The nine lane-killable mutation survivors of `R83MutationTool` §4.1 (probes at
   `.ufo/waves/round-83/w1/R83MutationTool/probes/`): stale-refetch `txt_sha256` drift (M03, expect REFETCH);
   short-rev (M11, expect REV); unreach-claims-success (M24, expect REFETCH); rev 26-word quote (M27, expect
   QUOTE_LEN); non-timestamp `fetched` (M30/M36, expect PARSE); leading-zero `words` (M31, expect PARSE);
   unterminated admit quote (M34, expect PARSE); non-http(s) `url` (M35, expect PARSE).
2. Non-ASCII numerals per numeric field (QUALITY 164): `line=1٢` (Arabic-Indic 2), `words=7٣`, `curl_rc=0٤`,
   `http=٢00` — each forged by substitution into a genuine record of the matching form, each expecting PARSE.
3. Whitelist-forger control (r83 routed defect 2): a whitelist tool that accepts the 15 positive lines byte-for-byte
   and refuses everything else must FAIL the counter on at least one forgery or positive leg (the counter's fresh
   positives are built in the counter from committed captures, not listed in advance — see below).
4. Setup leg: a rev record checked with a non-git `--repo` (a scratch directory with no git history) must exit 2
   with `GATE_RECORDS_ERROR` on stderr — not `FAIL REV,LINE` with exit 1 — at the landing revision. This leg is
   scored by the wave's executor seat through the public CLI (K2 wording covers it if the tool still misreports).

**Fresh positives (anti-whitelist).** The counter builds five fresh positives in-memory from committed lane bytes at
run time — never listed in advance: two admit records whose (capture-sha, quote) is located in a committed capture
by the counter's own search over `corpus/captures/` for a fresh S-id whose registry row is mined and whose refetch
row agrees (curl_rc 0, http 2xx, txt_sha256 = sha256(capture)); two rev records whose quote is located by the
counter's own search in a committed blob at the landing rev; one unreach record whose row is a committed refetch
row with non-success curl_rc/http. The whitelist tool (control 3) accepts only the 15 frozen lines, so it refuses
≥1 fresh positive — and therefore fails the counter. (If the counter's fresh builder cannot find a fresh record
using only committed bytes, the counter prints `FRESH_BUILD=FAILED` and the claim honest-stops on K1: the battery
itself is not load-bearing.)

**Predicate (target).** At the landing revision the counting command prints
`TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=N/N EXPECTED_CODE=N/N EMPTY_REFUSED=1/1 RC=4/4`,
`GATE_RECORDS_R84=PASS`, rc 0, where N is the frozen forgery count (computed from the classes above; the counter
prints it). At the pre-repair revision (`81b81173`, pre-`c7d29e1c`) the same command prints FAIL (the ASCII-digit
and quote-boundary legs were the reason for the repair), rc 1 — a do-nothing control that cannot be reached by
changing nothing.

**Controls (executed, committed):** `c2-k0-donothing` (pre-repair tool `81b81173` → FAIL, EXPECTED_CODE 262/288);
`c2-f1-stub-accept` (blanket-accept stub → FAIL); `c2-f2-stub-refuse` (blanket-refuse stub → FAIL);
`c2-f3-stub-quote-only` (the round-83 quote-only stub, `controls/stub-quote-only.py` → FAIL, 71/198 in r83);
`c2-w1-whitelist` (accepts the 15 frozen lines, refuses all else → FAIL on the fresh-positives leg).
Receipts `corpus/evidence/round84/controls/receipts/`.

**Kill rules (frozen):**
- K1: the predicate is not met at the landing revision.
- K2 (in-class): a record that the tool's own documented contract (docstring at the landing revision) classifies
  as a forgery of a frozen class is accepted (`OK`, rc 0), or is refused with a code outside the frozen
  `EXPECTED_CODE` set for its class. The setup leg (non-git `--repo` exit 2 vs `FAIL REV,LINE` exit 1) counts as
  K2 if the tool misreports it. Repairs after scoring do not rescue.
- K3 (harm): a genuine committed record that the tool accepted before this round is refused at the landing
  revision — measured over the 15 frozen positives plus the five fresh positives (all must be `OK`). A refusal
  that closes a genuine K2 in-class form at the base revision is not harm.
- K4 (whitelist): a tool that accepts the 15 frozen lines and refuses everything else passes the counter.

## C2 — depth (sourced on S214, S018, S023 opened this round)

**Claim.** One new knowledge entry teaches search-transparency reporting — what a PRISMA 2020 checklist/flow
requires a review to record about its search (database, platform, full strategy, dates) so identification,
screening and inclusion stay auditable — on ground no base entry cites (S214, S018, S023, all queued before this
round; S017 was fetched but reverted to queued because its landing page carries no quotable checklist text).

**Counting command (frozen; sha256 in `instrument-pins.txt`):**
`D=$(mktemp -d -p /fast/scratch/hyaku) && git archive <rev> | tar -x -C "$D" && python3 -B "$D/corpus/evidence/round84/depth-r84.py" --root "$D"`

**Before** (`controls/receipts/c1-d0-donothing.txt`, tree at base): `DEPTH_R84 entries=0 ok_entries=0 rows=0
located_quotes=0 fresh_sources=0`, `DEPTH_R84=FAIL`, rc 1.

**Predicate (target).** At the landing revision the counting command prints `entries=1 ok_entries=1`, `rows=` ≥ 7,
`located_quotes=` ≥ 8, `fresh_sources=1`, and `DEPTH_R84=PASS`, rc 0.

**Controls (executed, committed):** `c1-d0-donothing` FAIL; `c1-d1-r81-filler` (the round-81 filler pair as new
entries) FAIL; `c1-d3-r83-entry-relanded` (the round-83 entry re-landed under a new name: old work re-declared)
FAIL; `c1-b1-salad-boundary` (located quotes from S214 under content-free rows) PASS — the stated counter limit:
the counter does not judge whether a row follows from its quote; kill rule K3 does.

**Kill rules (frozen):**
- K1: the predicate is not met at the landing revision.
- K2 (located): a declared quote of the entry does not occur (whitespace-collapsed, curly quotes folded) in its
  committed capture, or occurs there but is absent from the live page when a non-author re-open gets HTTP 200 and
  tag-strips it. An unreachable re-open is recorded, not a kill.
- K3 (warrant): a non-author reviewer shows, for any decision-table row, (a) that its Do or Never states something
  its cited quotes do not state or entail, or (b) a sentence of the same cited source (located in the committed
  capture, quoted by line) that contradicts the row's Do or Never. One such row falsifies C2. Repairs after
  scoring do not rescue.
- K4 (ground): a base-list entry (`base-knowledge.txt`) cites S214, S018, or S023 or contains their URLs.

## Frontier step (inside the claim cap, not a third claim)

- Census before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
  at round start (paste output + exit). Census after at round end; exit 0 required.
- Curate `corpus/SOURCES.md` in contract v1 shape: one row per source opened this round (S214 checklist PDF,
  S018 survey abstract, S023 DCMI terms; S017 landing page fetched but reverted), each with URL, access date,
  ≤25-word located quote in the lesson `## Gate`. Rejections stay as rows with reason + flip.
- Mine one mistake into `corpus/lessons/round-84.md` `## Mistakes` (class · evidence · captured-by · fix, where the
  fix must be shown able to fail), or paste the sweep that found none.
- Sourced claim: C2 rests on S214, S018, S023, opened this round.
- Assimilation: `Assimilation: none` in the report unless a theme from `merge/chousa/` is adopted in scratch and
  validated per §10 (read-only campaign bytes, scratch collision check, re-grounding).

## Round shape

ONE v1 wave, 8–16 seats (run-15 amended 46), ≥25% attack seats (reviewer, critic, mutation-tester, labrat),
≤2 connector seats. One `.ready` per wave; orchestrator spawns; report only after `WAVE-DONE`. Seat roles span
m_flash/m_zfl plus scout m_antigravity — m_mim is on no role (per assignment brief; live map gives scout to
m_antigravity this round, executor to m_zfl).

Tooling authorization (operator, 2026-10-19): every seat may install/upgrade tools that help the task; first read
`/home/vgpnk/.omp/agent/RULES.md` (official channels, update-safety gate; record tool/version/channel/reason).
Pacman stays paused per the addendum guard.
