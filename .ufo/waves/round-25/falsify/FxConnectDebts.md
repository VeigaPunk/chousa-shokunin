# FxConnectDebts — round 25 integrated intake review

## Evidence
- Used private-clone HEAD `e93ac711f885a10d44fdd80a1734997419595b5a` (`git rev-parse HEAD`); this is the full checkpoint, not `0fc037e` or the gate-only `d8c8cff`.
- `corpus/lessons/round-25.md:20-31` covers D-1–D-11 (some rows are grouped) and the three prior-verifier debts at `:20-23`; no D-number is absent. The mapping is semantically sound except the qualifications below.
- D-1–D-3: frozen counts rederive `66→0` and `15→0` (`corpus/evidence/round25-measure-before.log:5-21`; `round25-measure-after.log:40-56`). Scorecard keeps the narrow operability score at 3/10 and the 3/3 observable (`SCORECARD.md:6-13`; `round25-claims.md:1343-45`).
- D-4/S006: old Gate wording is a paraphrase (`lessons/round-24.md:53`); new append-only quote at `lessons/round-25.md:94-99` exactly matches S006 §3.3.1 (“Link Works assesses URL accessibility without LLM inference”; source line 133 at `https://arxiv.org/html/2605.06635v1`). The r24 lesson remains unchanged.
- D-11/concurrency: r24 receipt has one blank line in run 3 of three 16-writer runs (`evidence/json-r24-20261019T213117Z-demo.log:26-29`); separate seeded r25 test is 2/6 vs 0/6 empty controls, with no pooling or patch (`.ufo/waves/round-25/build/ExecAppendRace.md:7-10,24`). `SCORECARD.md:1300-1303` still says concurrency is unclaimed; intake `:20,31` preserves that distinction.
- D-7/SHONEN: intake `:28` accurately supersedes the map’s carry with the later canonicalization: `SHONEN.md:5-12` uses `[~]` pointers explicitly marked lane assertions/no non-author verifier; round-25 lesson `:101-107` says the independent sample remains unperformed. No `[x]` or outside closure is claimed.
- D-5: “9 entries” in intake `:21` means nine files, consistent with the 21 `--root ..` occurrences enumerated at `.ufo/waves/round-25/build/ReviewRecheckRoot.md:26-35`; the two counts are different units.
- Original verifier is untouched: blob `7eccfc9a24c9f987a2039087bcd886fd3343c073` at `0fc037e`, `d8c8cff`, and `e93ac711`. `round-24.md` is likewise the same blob `bf92c26fe73d783c73086f7331250bdf897e7be3` across those pins.

## Omissions / calibration caveats
- D-6 is carried, but intake `round-25.md:27` says the historical log was “corrected.” The original quota rationale remains at `corpus/SOURCES.md:75-78`; the appended note explicitly says the historical defect is “retained, not rewritten” and gives the new stop rule (`SOURCES.md:97-103`). This is an append-only clarification, not a correction to the original log; the status verb overstates the change.
- D-10 is acknowledged but not carried in the map’s required open state. `ConnectorSpotcheckMap.md:18` says keep it open until its dated commit window is re-derived. The intake instead says the r24 header is “superseded” (`round-25.md:30`), while the header records pre-landing `ab19cff` and uncommitted edits (`round-24.md:3-6`). QUALITY 10 requires commit-window bounds and remeasurement (`QUALITY.md:43-45`); `grep` for `git log|--since|--until|commit window|re-measur|remeasur` in `round-24.md` returned no matches. No rederivation is linked, so “superseded” must not be read as closure.

## Checkpoint packaging (preserve both failures)
- Lesson records both misses at `round-25.md:112-133`. Independently measured gate SHA prefixes: `0fc037e=752e4e38`; `d8c8cff=e93ac711=63a39282`.
- Evidence README Git blob is identical at `0fc037e` and `d8c8cff` (`1701914bf418cf556aa54e8e0056e4f123a0c387`) and changes at full pin `e93ac711` (`9de288e1a706a3e7ce894c196c37c6d11bb65855`). Thus d8c8cff corrected the gate only; e93ac711 is the first complete pin used here.

## One bounded move
- **Axis: calibration.** Make one focused wording update to the Spot-check intake: describe D-6 as an appended clarification with the old log retained, and keep D-10 explicitly open pending a cited commit-window re-derivation. Leave the r24 lesson and original verifier untouched. This preserves historical evidence while preventing a carried debt from reading as closed.
- Risk: an external, pinned re-derivation not present in this checkpoint could make D-10’s open status stale; none is linked by the reviewed intake or map. No other axis is implicated by the wording-only move.
- Verification: after any integration, confirm D-6 wording matches `SOURCES.md:97-103`, D-10 either remains open or cites the required `git log --since/--until` window and remeasurement, and verifier blob remains unchanged. No gate/selftest was run by this read-only seat.

VERDICT: All D1–D11 have intake rows and the named S006, concurrency, SHONEN, and packaging joins check out; D-6 action wording overstates its correction, and D-10 lacks the map-required open/rederived status. Installs/updates: none.