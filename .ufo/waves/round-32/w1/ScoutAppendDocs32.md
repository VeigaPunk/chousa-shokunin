# ScoutAppendDocs32 — C1 `--json` append docs

Read-only recon. Census: Python walk of `/home/vgpnk/Projects/shokunin/chousa-shokunin` excluding `.ufo`, `.git`, `.jj`, keeping lines that state `--json` append semantics or a concurrency limit. Raw hits: `.ufo/waves/round-32/w1/ScoutAppendDocs32/hits-priority.txt` (469) and `hits-other.txt` (65). Quotes below were re-read from the files. No installs. No counter runs. Confidence high on opened lines; `[INFERENCE]` marks the stale/fulfil reading only.

A flock-serialized append (exclusive flock held across the last-byte probe and the `>>`) **fulfils** the prescriptions and **makes present-tense** the “no lock / one writer / unlanded / still open / carried” sentences. It does **not** falsify “appends (`>>`, never rewrites) one JSON line” or the r24 delimiter rule. Append-only history: do not rewrite the stale sentences; a later sentence would supersede them. Frozen `corpus/evidence/round32/claims.md` and `c1-count.py` are not docs to patch.

## Fulfil — the prescription a landing discharges

- `SCORECARD.md:1371-1376` — `## Planned — round 26 (not started)`, item 1: “serialize cooperating `--json` appenders across the EOF probe plus append (`flock` candidate remains unlanded in r25 wave evidence); reproduce seeded-unterminated race before, then ≥10×16-writer same-precondition runs with no blank/invalid lines.” This is the round-25 registration the frozen claim cites. The same heading is later called historical, not closed: `SCORECARD.md:1449-1453` “Its appender-race item was carried, not implemented or claimed.”
- `SCORECARD.md:1300` “Remaining round-20 named debt, unclaimed: manifest concurrency (`flock`), …”
- `SCORECARD.md:1781-1786` `## Planned — round 32 (not started)`: “`--json` appender serialization (Planned26)”.
- `corpus/knowledge/json-delimiter-r24.md:71` “a `flock` around probe + append is the candidate fix.” (The clauses on `:66-70` are the stale half; see below.)
- `corpus/evidence/round32/claims.md:23-28` contract (frozen; fulfil, do not edit): the gate “takes an exclusive flock(2) on that open file, and holds it from before it reads the manifest's last byte until after its own line is written.” Same words in `corpus/evidence/round32/c1-count.py:9-16`.
- `corpus/evidence/round32/claims.md:20-21` “The fix was pre-registered at round 25 (`SCORECARD.md` Planned — round 26, item 1) and never landed.” Fulfils the “never landed” status; the paragraph is a frozen before-state.

## Stale as current status — unlocked, one writer, still open

Present tense or “still / carried / unlanded / not fixed”. A landed flock makes these false if left as the latest word.

- `corpus/knowledge/json-delimiter-r24.md:66-71` “Observation (named debt, not fixed): the probe and the append are two operations with no lock. … The gate assumes one writer per manifest; a `flock` around probe + append is the candidate fix.”
- `corpus/README.md:49` coverage cell: “the measured single-writer limit”.
- `corpus/README.md:846-847` “Still open: concurrent appenders to one manifest (one blank line in 1 of 3 sixteen-writer runs)”.
- `corpus/README.md:875` “Still unclosed: concurrent JSON appenders, filesystem races, …”
- `corpus/README.md:891` “Existing carried debts above remain open.” and `:907` “Previous round26 frontier admission correction and carried debts stay in force.” (They keep `:875` in force; they do not restate the mechanism.)
- `LOG.md:826` “Named debt: concurrent appenders (1 blank line in 1 of 3 sixteen-writer runs).”
- `LOG.md:866-868` “Unclaimed concurrency debt reproduced separately: 2/6 seeded sixteen-writer runs with a blank line (0/6 empty controls), invalid JSON=0; unlanded flock candidate retained in wave evidence, no closure claim.”
- `LOG.md:972-973` “Concurrent JSON-appender serialization is carried debt, not a second operability claim or an implied repair.”
- `corpus/lessons/round-24-verifier-spotcheck.md:17` “Debts: concurrent-append blank-line residual (1 in 3 runs at 16 writers); …”
- `corpus/lessons/round-25.md:20` “Concurrent appenders can add a blank line (1/3 runs at 16 writers) | carried, not a claimed fix; …”
- `corpus/lessons/round-25.md:31` “D-11 delimiter closure could obscure concurrent-append race | retained as open, separate from r24 delimiter fix | … no race patch integrated”.
- `corpus/lessons/round-26.md:7-8` “The planned concurrent-JSON-appender serialization is carried, not claimed alongside the closure-routed reader fix on the same axis.”
- `corpus/lessons/round-26.md:23` “Concurrent JSON appender race, … remain open | carried, not silently repaired …”
- `corpus/lessons/round-26.md:206-207` “The appender-race pointers belong to the r24 delimiter note/demo and r25 lesson/ExecAppendRace report, **not** a dedicated hardening-ledger row.” (Still true that hardening has no flock row; the “race” status is the stale part.)
- `corpus/evidence/round26-claims.md:15-19` “Plan item 1 (`--json` appender serialization) is **not** claimed this round: … It stays carried debt with its r24/r25 reproductions; this is a plan-vs-run disposition (QUALITY 11), not a closure.”
- `corpus/lessons/round-27.md:28` “JSON-appender race | Carried: not closed by these bounded repairs”.
- `corpus/lessons/round-27.md:119` “parent-root/race/appender debts … stay open.”
- `corpus/lessons/round-27-verifier-spotcheck.md:61` “The final gate is not promoted as … generic JSON-appender atomicity …” (A cooperating flock is not generic atomicity for non-cooperating writers. `[INFERENCE]` This sentence stays true unless someone claims flock closes every writer.)
- `corpus/evidence/README.md:1060` demo row: “16-writer concurrency runs (named debt)”.
- `corpus/evidence/json-r24-20261019T213117Z-demo.log:26` “## concurrency (named debt, not fixed): 16 parallel appenders x 3 runs …” and `:29` `run=3 … blank_lines=1`. Dated receipt of the r24 gate; the counts stay historical. The parenthetical “not fixed” is the status clause.

Rounds 28–31 lessons and `corpus/evidence/round31/claims.md` do not restate flock / JSON-appender / one-writer (grep, no matches). `SCORECARD.md:1785` is the latest plan pointer.

## Compatible — append semantics a flock must not contradict

No concurrency limit. Usage text does not mention flock, one writer, or a lock (`SKILL.md`, root `README.md`, `PROVINCE.md`, `corpus/QUALITY.md`: zero `flock`).

- Gate header `tools/research-gate.sh:196-197`: “`--json PATH` appends (`>>`, never rewrites) one JSON line: schema, UTC, record and gate SHA-256, per-section state/verdict/tallies, composed verdict.”
- Usage `tools/research-gate.sh:397-399`: “`--json PATH` appends (never rewrites) one JSON line recording UTC, record + gate SHA-256, per-section tallies and the composed verdict.”
- Probe comments `tools/research-gate.sh:3067-3071` and `:3185-3191`, write `printf '%s\n' "$line" >>"$JSON_ARG"` at `:3199`. They describe the delimiter, not a lock. Selftest comment `:5841-5847`: prior bytes stay byte-identical and “no blank line is written” for the single-writer cases 134–136.
- `SKILL.md:268-272`: “`--json PATH` appends (`>>`, never rewrites) one JSON line”. `SKILL.md:284-286`: first line “stayed byte-stable under a second append”. `SKILL.md:434-435`: “The manifest records a state at a revision: it appends, never rewrites or compares revisions”.
- `SCORECARD.md:254-256`: “`--json` APPENDS the verification state … (`>>` only, no rewrite path).”
- `corpus/README.md:223-226`: “The lane manifest appends by discipline, not construction: one `>>` per run to the named file, pre-existing foreign lines preserved unvalidated, never read back”. `[INFERENCE]` The gloss is rewrite/validation discipline, which flock keeps. Not listed as stale.
- `corpus/knowledge/json-delimiter-r24.md:9-14,28-38`: delimiter defect and “The prior bytes are never rewritten”. Those arms stay; only `:66-71` is the concurrency debt.
- `corpus/knowledge/verification-r16.md:83`: delimiter row “**closed r24**” (prefix `\n` when last byte is not `0a`). That closure is the delimiter, not the race (`round-25.md:31`, `round-26.md:206-207`). Do not treat it as already covering C1.
- `corpus/knowledge/verify-all-r6.md:114-123` and `corpus/lessons/2026-10-16-verify-all-composition.md:180-203,271-274`: one `>>`, one JSON line, no rewrite, foreign lines unvalidated, not an audit trail. The r6 note’s “`JSON_ARG` appears only in validation `:1737-1744` and this append” (`verify-all-r6.md:120-121`) is **already** stale against the current gate (last-byte read at `research-gate.sh:3193-3199`), independent of flock.

## Not the `--json` manifest

Do not close these by a C1 flock.

- `corpus/knowledge/verification-r16.md:37`: “Manifest append outside `--root` succeeds (no containment check on `--json` destination)”.
- `corpus/knowledge/metadata-screen-r25.md:118-120`: “Concurrent same-inode content writes” is the metadata reader, not `verify-all --json`.
- `LOG.md:644` and the SCORECARD planned lists at `:821`, `:1007`, `:1073`, `:1127`, `:1181`, `:1230` name the **delimiter** edge (closed r24), not flock. Flock does not reopen that edge.
- Root `README.md`: no `--json` / flock / manifest-append sentence.

## Limits

Census excluded `.ufo` (round-25 `ExecAppendRace.md` and `unlanded-append-race.patch` are wave evidence the production sentences already cite, not lane contract text). Did not run `c1-count.py`. Did not edit production files.
