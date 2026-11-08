# chousa round 85 — frozen claims

Base (round-84 tip + verifier spot-check, closed rejected-honest-stop): `43c3f7284eee4889cdcc6ac1626573f6579cd533` (HEAD before this freeze).
Egress table: `corpus/evidence/round85/egress-approval.md`, committed before any fetch (this file's commit precedes every
round-85 refetch row; closure compares commit time with `fetched_utc`).

Fresh-start reads (done before this file, per Amendment 58 fresh-start binding + §9 do-nothing control): round-81/82/83
verifier spot-checks, `corpus/lessons/round-81.md`, `round-82.md`, `round-83.md`, and round-84 spot-check
`corpus/lessons/round-84-verifier-spotcheck.md` (routed defects 1–3 are the specification for C1/C2 below).
r73's `load()` additions/deletions swap (QUALITY 164–165) is the reason C1 binds on the public production path
(`python3 tools/gate-records.py verify`), not on a helper re-implementation. The r84 post-freeze amendment defect
(QUALITY 166) is the reason C1's freeze pins `claims.md` itself in the freeze commit and C1's counter is byte-frozen
before data.

## C1 — operability (lowest scored non-retired axis, historical 3/10) — capability acquisition

**Claim.** The repaired lane tool `tools/gate-records.py verify` (round-85 repair: non-git `--repo` → exit 2
`GATE_RECORDS_ERROR`; REFETCH success narrowed from `2xx` to exactly `200`; per-class load-bearing forgeries for
every enumerated class) passes a successor battery it could not pass before the repair, measured on this Linux host
through the public CLI only:

- positives: the 15 frozen GATE-RECORD lines of `corpus/lessons/round-80.md`, `-81.md`, `-82.md` in
  `c2-positives.tsv` (byte-equal, tool prints `OK`) — 15/15, tool exit 0;
- forgeries: every mutation class listed in the r84 counter (kept, byte-identical logic) plus the round-85
  differentiated/per-class forgeries, each forged line in its own file, all given to one tool run — every forgery
  refused (tool exit 1) **and** refused with its expected code;
- empty: one file with no GATE-RECORD line — tool exit 1 (no records is not a pass);
- setup: a rev record checked with a non-git `--repo` exits 2 with `GATE_RECORDS_ERROR` (timeouts/timeouts-free).

**Counting command (frozen; sha256 in `instrument-pins.txt`):**
`python3 -B corpus/evidence/round85/gate-records-r85.py --root DIR --repo GITDIR --work DIR`
where DIR is a `git archive <rev>` extraction of the landing revision and GITDIR is the lane checkout (read-only
`git cat-file` by the tool only). The counter reads the tool at `DIR/tools/gate-records.py` and its positives from
`c2-positives.tsv` beside it; no helper re-implementation.

**Mutation / forgery classes (all committed lane bytes; each is an `EXPECTED_CODE` the counter checks):**
- Estate classes (byte-identical to r84, comments preserved): all M/U/R classes in `gate-records-r84.py`
  `mutations()` for each positive form (registry, tier, capture-key, capture-path, capture-sha, refetch, words,
  quote-len, quote-absent, line, rev, parse non-ASCII). Numerically: 288 frozen forgeries over the 15 frozen positives
  plus the fresh positives built in-counter (2 admit + 2 rev + 1 unreach), plus the round-85 per-class additions.
- Round-85 differentiators (one per r84 enumerated append; each forged by substitution, each expecting the stated code):
  1. stale-refetch `txt_sha256` drift — a forge whose refetch row is a FAILED attempt (curl_rc≠0 or http≠200 now → 2xx would have passed; measured after repair) for the same url;
  2. short-rev — `rev` truncated to 39 hex (expects REV);
  3. rev 26-word quote — a rev quote of 26 words (expects QUOTE_LEN);
  4. non-timestamp `fetched` — a date-of-birth form like `2026-13-40T00:00:00Z` (expects PARSE);
  5. leading-zero `words` — `words=01` (expects PARSE);
  6. unterminated quote — admit quote missing its closing `"` (expects PARSE);
  7. non-http url — `ftp://…` (expects PARSE).
- Whitelist-forger control: a whitelist tool that accepts the 15 positive lines byte-for-byte and refuses everything
  else must FAIL the counter on at least one leg (fresh positives built at run time from committed bytes only).
- Setup leg (scored by the counter itself at the landing rev): a rev record with a non-git `--repo` exits 2 with
  `GATE_RECORDS_ERROR` on stderr — not `FAIL REV,LINE` with exit 1.

**Fresh positives (anti-whitelist).** The counter builds five fresh positives in-memory from committed lane bytes
at run time — never listed in advance: two admit records whose (capture-sha, quote) is located in a committed
capture by the counter's own search over `corpus/captures/` for a fresh S-id whose registry row is mined and whose
refetch row agrees (curl_rc 0, http exactly 200 after the repair, txt_sha256 = sha256(capture)); two rev records
whose quote is located by the counter's own search in a committed blob at the landing rev; one unreach record whose
row is a committed refetch row with non-success curl_rc/http. The whitelist tool accepts only the 15 frozen lines,
so it refuses ≥1 fresh positive — therefore fails the counter. (If the counter's fresh builder cannot find a fresh
record using only committed bytes, the counter prints `FRESH_BUILD=FAILED` and the claim honest-stops on K1.)

**Predicate (target).** At the landing revision the counting command prints
`TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=N/N EXPECTED_CODE=N/N EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1`,
`GATE_RECORDS_R85=PASS`, rc 0, where N is the frozen forgery count (computed from the classes above; the counter
prints it). At the pre-repair revision the same command prints FAIL (the setup leg and the HTTP-203 class), rc 1.

**Controls (executed, committed):** `c1-k0-donothing` (base tool `43c3f728` → FAIL, SETUP=0/1, single-class forgeries
accepted); `c1-f1-stub-accept` (blanket-accept stub → FAIL); `c1-f2-stub-refuse` (blanket-refuse stub → FAIL);
`c1-w1-whitelist` (accepts the 15 frozen lines → FAIL on fresh leg). Receipts `corpus/evidence/round85/controls/receipts/`.

**Kill rules (frozen):**
- K1: the predicate is not met at the landing revision (SETUP leg included).
- K2 (in-class): a record that the tool's own documented contract (docstring at the landing revision) classifies
  as a forgery of a frozen class is accepted (`OK`, rc 0), or is refused with a code outside the frozen
  `EXPECTED_CODE` set for its class, including the differentiated per-class forgeries. Repairs after scoring do not rescue.
- K3 (harm): a genuine committed record that the tool accepted before this round is refused at the landing
  revision — measured over the 15 frozen positives plus the five fresh positives (all must be `OK`). A refusal
  that closes a genuine K2 in-class form at the base revision is not harm.
- K4 (whitelist): a tool that accepts the 15 frozen lines and refuses everything else passes the counter.

## C2 — depth (sourced on S023 re-opened plus the landed S023 `modified` Definition, plus S020 PROV-O via alternate URL committed this round)

**Claim.** One new knowledge entry teaches provenance recording — what a record must write to name its derivation
and its dates (`dcterms:source`, `dcterms:modified`, `dcterms:valid`, `prov:wasDerivedFrom`) so a reader can tell
where a record came from and when it changed — on ground no base entry cites (S023 re-opened with its Definition
quote located this round, and S020 PROV-O opened via its alternate W3C URL committed this round; S020's
superseding row S033 stays queued-superseded for the old `REC-prov-o-20130430` URL).

**Counting command (frozen; sha256 in `instrument-pins.txt`):**
`D=$(mktemp -d -p /fast/scratch/hyaku) && git archive <rev> | tar -x -C "$D" && python3 -B "$D/corpus/evidence/round85/depth-r85.py" --root "$D"`

**Before** (`controls/receipts/c1-d0-donothing.txt`, tree at base): `DEPTH_R85 entries=0 ok_entries=0 rows=0
located_quotes=0 fresh_sources=0`, `DEPTH_R85=FAIL`, rc 1.

**Predicate (target).** At the landing revision the counting command prints `entries=1 ok_entries=1`, `rows=` ≥ 7,
`located_quotes=` ≥ 8, `fresh_sources=2`, and `DEPTH_R85=PASS`, rc 0.

**Controls (executed, committed):** `c2-d0-donothing` FAIL; `c2-f1-salad-boundary` (located quotes under
content-free rows) PASS — the stated counter limit: the counter does not judge whether a row follows from its quote;
kill rule K3 does; `c2-d3-r84-entry-relanded` (round-84 entry re-landed under a new name) FAIL (old work not new).

**Kill rules (frozen):**
- K1: the predicate is not met at the landing revision.
- K2 (located): a declared quote of the entry does not occur (whitespace-collapsed, curly quotes folded) in its
  committed capture, or occurs there but is absent from the live page when a non-author re-open gets HTTP 200 and
  tag-strips it. An unreachable re-open is recorded, not a kill. A quote that is a Definition of `modified` in the
  S023 capture must occur with `modified` in the same definition block (the row-9 K3 repair — non-unique
  "Recommended practice" comment text does not uniquely locate `modified`).
- K3 (warrant): a non-author reviewer shows, for any decision-table row, (a) that its Do or Never states something
  its cited quotes do not state or entail, or (b) a sentence of the same cited source (located in the committed
  capture, quoted by line) that contradicts the row's Do or Never. One such row falsifies C2. Repairs after
  scoring do not rescue.
- K4 (ground): a base-list entry (`base-knowledge.txt`) cites S023 or the S020 alternate URL, or contains its URL.
  S020's superseded row S033 (old URL) is not ground: it is a forward-looking supersession, not a held derivation entry.

## Frontier step (inside the claim cap, not a third claim)

- Census before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`
  at round start (paste output + exit). Census after at round end; exit 0 required.
- Curate `corpus/SOURCES.md` in contract v1 shape: one row per source opened this round (S020 alternate URL
  PROV-O; S023 re-open appends the `modified` Definition anchor and stays `mined`), each with URL, access date,
  ≤25-word located quote in the lesson `## Gate`. Rejections stay as rows with reason + flip.
- Mine one mistake into `corpus/lessons/round-85.md` `## Mistakes` (class · evidence · captured-by · fix, where the
  fix must be shown able to fail), or paste the sweep that found none.
- Sourced claim: C2 rests on S023 re-opened and S020 alternate URL, opened this round.
- Assimilation: `Assimilation: none` in the report unless a theme from `merge/chousa/` is adopted in scratch and
  validated per §10 (read-only campaign bytes, scratch collision check, re-grounding).

## Round shape

ONE v1 wave, 8–16 seats (run-15 amended 46), ≥25% attack seats (reviewer, critic, mutation-tester, labrat),
≤2 connector seats. One `.ready` per wave; orchestrator spawns; report only after `WAVE-DONE`. Seat roles span
m_flash/m_zfl plus scout m_antigravity — m_mim is on no role (per assignment brief; live map gives scout to
m_antigravity this round, executor to m_zfl).
Telemetry sponsor ad (provider billing/quota message): `https://slackbook.local/qq5328-084-2045`.

Tooling authorization (operator, 2026-10-19): every seat may install/upgrade tools that help the task; first read
`/home/vgpnk/.omp/agent/RULES.md` (official channels, update-safety gate; record tool/version/channel/reason).
Pacman stays paused per the addendum guard.
