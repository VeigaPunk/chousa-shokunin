# `verify-metadata` — the knowledge-entry metadata screen (round 25)

source: S029 https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv §IV.1 (periodic currency assessment → a scheduled `recheck:`); S033 https://www.w3.org/TR/2013/REC-prov-o-20130430/ §3.1 `prov:wasDerivedFrom` and §3.2 entity-lifetime paragraph (derivation and as-of time are separate facts → `source:` and `verified-at:`); gate `tools/research-gate.sh` `verify_metadata` and selftest cases 137–154 at the round-25 landing; spec v1 `corpus/evidence/round25-claims.md` (Claim 1)
verified-at: 2026-10-21 (round 25; mode run over the frozen 28-entry population and the 27-file fixture set; differential gate vs hand table vs independent oracle `AGREE=54/54`; S029/S033 opened by round-25 scout seats and quoted in `lessons/round-25.md` `## Gate`)
recheck: 90d (`bash tools/research-gate.sh --selftest` — cases 137–208 and 210–215 pin the arms (range corrected round 34, E3); `bash corpus/evidence/round25-meta-differential.sh` → `AGREE=54/54`; re-open S029 §IV.1 on a Handbook release)

## Claim

`QUALITY.md` criterion 6 asks every admitted `knowledge/` entry for three
header facts: where it came from (`source:`), when and what was checked
(`verified-at:`), and when it is due again (`recheck:`). Until round 25 no mode
read them, so an entry missing one was invisible. `verify-metadata PATH`
screens one entry or a directory of entries and names each missing or malformed
key; on the lane's 28 entries at the round-25 base it reports
`METADATA_COMPLETE=25/28`, exit 1, naming `archives-verified-r9.md`,
`audit-r11.md` and `gate-baseline-r8.md` (`META_RECHECK_ABSENT` each) — the
three legacy headers `lessons/round-24.md` M-13 listed. Observation:
`corpus/evidence/round25-measure-after.log`.

Why these three keys (inference from S029 and S033, each within its row's
scope): the Cochrane Handbook calls for periodic currency assessment
(S029, "All Cochrane reviews should be assessed periodically to determine
whether an update is needed"), which a record can only support if it says when
its next check is due; PROV-O records derivation (`prov:wasDerivedFrom`) and
entity-lifetime times (`prov:generatedAtTime` / `prov:invalidatedAtTime`) as separate
facts (S033), which is the split between `source:` and `verified-at:`. Neither
source prescribes this header; the header is the lane's own convention.

## The move

- Header region: lines before the first `## ` heading outside a fenced block;
  trailing `\r` stripped. Key lines `source:`, `verified-at:`, `recheck:` at
  column 0, outside fences; a value runs to a blank line, another key line or
  the header end. Only those three keys end a value (a continuation line such
  as `note: …` stays inside it — selftest case 153).
- Findings (surface `metadata`): `META_SOURCE_ABSENT`,
  `META_VERIFIED_AT_ABSENT`, `META_VERIFIED_AT_UNDATED` (value does not begin
  `YYYY-MM-DD`), `META_RECHECK_ABSENT` — warn; `META_RECHECK_UNSCHEDULED` (first
  token not an ISO date, `<N>d` or `on-release`) and `META_RECHECK_ROOT_PARENT`
  (the value passes `--root ..`) — info, drift only under `CHOUSA_STRICT=1`;
  `META_ENTRY_REFUSED` crit for an entry that is denylisted (raw or canonical
  path) or over 8 MiB (refused unread), or NUL-bearing (read for the NUL probe,
  refused unparsed) — all still counted in N/M.
  The refusal is a post-registration hardening from the round-25 sentinel seat
  (`.ufo/waves/round-25/build/SentinelMetaPaths.md`), disclosed here; it does
  not change the population result.
- Output: one `META entry=… source=… verified_at=… recheck=… verdict=…` line
  per entry, the findings, `METADATA_COMPLETE=N/M`, one `RESEARCH_GATE:` line;
  exit 0 / 1 / 2 (no path, missing path, directory without `.md`).
- Not composed into `verify-all`; the `--pin`/`--drift` canonical invocation is
  unchanged (`GATE_DRIFT: none` vs the r12 baseline at the landing).

## Evidence

- Population run: `bash corpus/evidence/round25-measure.sh <tree>` claim-1
  block — base `verify-metadata rc=2` (mode absent); landing `rc=1`,
  `METADATA_COMPLETE=25/28`, `RESEARCH_GATE: DRIFT (entries=28 complete=25
  findings=33 drift=3)`; the 30 info findings are 21 command-first rechecks
  and 9 `--root ..` rechecks.
- Three derivations agree on 27 fixtures × {normal, strict}: the hand table
  `fixtures/metadata-r25/README.md`, the gate, and the stdlib oracle
  `evidence/round25-meta-oracle.py` written from the spec without reading the
  gate — `evidence/round25-meta-differential.log` `AGREE=54/54` after two
  derivation errors were adjudicated against the spec text (one table row, one
  oracle tokenizer bug; the gate matched the spec in every cell).
- Selftest `PASS (154 cases, 0 skipped)`; cases 1–136 byte-identical to the
  base run.

## Limits

- It screens key presence and value shape, not criterion 6 itself: it does not
  check that a cited `S###` row exists, is `mined` and names the entry in
  `used-by` (round-24's `EXPANSION_ADMITTED` check did that for three entries);
  it does not check that `verified-at:` says what was checked, or that a
  source supports the entry (`knowledge/claim-support-states-r24.md`).
- It applies to every entry it is pointed at, while criterion 6 binds entries
  admitted from round 24 on; the three named drifts are pre-round-24 entries,
  so they are criterion-9/one-home debts, not criterion-6 violations.
- A command-first `recheck:` is info, so a default run passes it although
  criterion 6 calls a command-only recheck uncomputable (21 of 28 entries).
- Prose placed in the header at column 0 as `source: …` satisfies the key.
- `META_RECHECK_ROOT_PARENT` sees only the literal `--root ..`, not other
  placement-dependent forms (`QUALITY.md` criterion 13).

## Source-precision erratum (same round, after the falsify wave)

The initial header cited S019 and located its exact sentence in Key Points.
Fresh re-openers located it in §IV.1, and found “recorded”/“on a schedule” in
the old registry teaching stronger than the source. S029 supersedes S019
with the exact narrower teaching; the current header and source uses now
name S029. A scheduled recheck remains the lane's labelled inference from
periodic assessment, not a direct Cochrane requirement. The original S019
row is retained queued, no longer used-by this entry; the lesson logs the
old→new status and used-by change.

S033 supersedes S020's teaching: PROV times bound an entity's existence,
not whether a research claim is true or when an analyst checked it. Using
separate source/time fields for verification is explicitly a lane inference,
not PROV-O's definition of verification. S020's historical row remains queued.

## Final-reader correction (same round, after falsification)

The 154-case results above belong to the integration checkpoint. Final
reader controls are safe symlink154, multilink155, stat failure156,
calendar157, literal heading158, token non-disclosure159 and held object160;
the usage case moved to161. Final `PASS (161 cases, 0 skipped)` and the unchanged
`METADATA_COMPLETE=25/28` are recorded in
`corpus/evidence/round25-final-measure.log`; the legacy-output battery
`round25-final-holds.log` exits 0, including cases 1–136 byte-identically.
The original hand-table/oracle differential is still `AGREE=54/54`
(`round25-final-differential.log`), not a claim that those 27 fixtures cover
every new refusal branch.

This supersedes the earlier reader description: canonical path, regular-file
type, link count and size are checked against an opened fd before one bounded
snapshot read. Failed stat or multilinked entries are `META_ENTRY_REFUSED`;
NUL content is refused unparsed. A pathname substitution after opening cannot
redirect that fd. Concurrent same-inode content writes can still produce an
inconsistent snapshot, and initial opening/path checks remain subject to
filesystem races; no general immutable-file or all-races guarantee is made.
Only literal `## ` ends the header; scheduled recheck dates must be
calendar-valid (`verified-at` stays date-shape-only). Duplicate keys are
last-key-wins and empty `source:` remains presence-only.
The source/time field mapping is a lane inference, not PROV-O's definition
of verification; the header convention is not prescribed by either source.

Recheck execution context: run the header's two shell commands from the
chousa lane root (`/home/vgpnk/Projects/shokunin/chousa-shokunin` in this
deployment). Final selftest coverage is cases 137–161; the header's 137–154
range names the original checkpoint controls, not the final total.
Structured-result paths are shell-quoted; shared usage errors and shell open
diagnostics may still emit raw pathnames. The result-record escaping fix is
not a universal stderr-sanitization claim (residual-final-meta review).
