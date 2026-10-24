# Round 41 — capture-invocation pinning and W04 dispositions

author: chousa L1 (host-mapped seat: no live L2 dispatch surface; wave prepared for the orchestrator)
date: 2026-10-24
round: 41 (attempt 1)

## Claims and measurements

- **C1 operability (lowest scored axis, 3/10):** every external invocation attributable to the canonical pin/drift capture — parent capture functions, startup, and the captured `verify-all` child — resolves through the frozen pin table (14 names, r35-wrapper pattern), the child runs under one fixed `CAP_CHILD_PATH`, and `LD_PRELOAD`/`LD_LIBRARY_PATH` are scrubbed. `python3 corpus/evidence/round41/c1-count.py --gate .ufo/waves/round-41/controls/base-gate-r41.sh` → `CAPTURE_PIN_MATCH=1/12` (`.ufo/waves/round-41/controls/control-before.txt`) → `python3 corpus/evidence/round41/c1-count.py --gate tools/research-gate.sh` → `CAPTURE_PIN_MATCH=12/12` (`corpus/evidence/round41/measure-after-c1.txt`, receipts `corpus/evidence/round41/receipts/cells/cells.json`).
- **C2 calibration:** every W04 duplicate-URL warning carries a committed, evidence-resolving disposition. `python3 corpus/evidence/round41/c2-count.py` with the TSV absent → `W04_DISPOSITIONED=0/5` (`.ufo/waves/round-41/controls/c2-control-before.txt`) → with `corpus/evidence/round41/w04-dispositions.tsv` → `5/5` (`corpus/evidence/round41/measure-after-c2.txt`). The five warnings are advisory and semantically correct (same-page different-section pairs ×3 — S075 joined the coreutils page at a different anchor this round, required supersede row, retained rejected duplicate); the contract keeps `source`/`scope` immutable, so dispositions record the reason rather than editing rows.
- No-harm: `bash tools/research-gate.sh --selftest` → `PASS (275 cases, 0 skipped)` on the landed gate; the one in-flight failure (`metadata-stat-unavailable`) was the selftest's own PATH-shim simulation made unreachable by the `stat` pin and was repaired to simulate through `RESEARCH_GATE_STAT` (shown able to fail: the case fails red before the fixture change when the stub is not GNU-reporting).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| mechanism-regression — a selftest attack simulation depended on the PATH surface the claim closes: `metadata-stat-unavailable` PATH-shimmed `stat`, but the r41 pin resolves `stat` absolutely | `FAIL-case metadata-stat-unavailable rc=0/1` on the first landed selftest run (275-case battery) | none — the pin change predates any criterion tying selftest fixtures to the surface they simulate | Re-route the simulation through the documented override `RESEARCH_GATE_STAT` with a GNU-reporting stub; red-before: the non-reporting stub is refused `STAT_PROVENANCE`, the reporting stub restores `reason=stat unparsed` (selftest PASS 275/275 after) |
| provenance-attestation — a live-access claim carried no byte receipt and a seat self-authorized egress from its dispatch item (r40 wave finding, dispositioned here because the artifacts are append-only) | `.ufo/waves/round-40/w1/SentinelFetchScope.md` F1/F2; `ScoutHashSource.md:7,32`; `corpus/lessons/round-40-verifier-spotcheck.md:38` | `corpus/QUALITY.md` had no access-receipt criterion → new criterion 57 | Wave-spec seat contract now forbids egress and names only installed/committed sources (`.ufo/waves/round-41/w1-spec.json` context); r41 search log restores the registered-hosts/open-L0 clause (F3 remediation); integrator/operator owns the fleet-report side (F3 notes it, never edited lane-side) |
| measurement-target — a counter grading a mutable worktree can disagree with the pinned commit a report cites (r40 wave finding) | `.ufo/waves/round-40/w1/ReviewActivePopulation.md`, `ReviewReplacementBindings.md`: r40 counter 6/6 on committed HEAD vs 2/6 on a worktree carrying r41's in-flight gate edits | `corpus/QUALITY.md` had no revision-pin criterion → new criterion 58 | r41 counters pin the measured surface explicitly (`--gate PATH`, receipts record the gate path); the r40 counter lineage is routed as a defect for its next owner — not falsification of r40's admitted round |
| inventory-discovery — the "bare mktemp/sed" carried candidate understated the real surface: instrumentation counted 20 parent/child PATH-resolved calls across pin+drift (728 in pin alone) | `.ufo/waves/round-41/claims.md` measured-surface paragraph; trap-run logs reproduced by ScoutTrapInventory item | none — the claim was sized before instrumentation existed | The frozen pin set is the union of the *measured* name set (14 names), not the two carried names; claims.md records the run so the scope is re-derivable |

## Gate

### Candidate and admitted

The admitted knowledge entry is `corpus/knowledge/capture-path-pin-r41.md`: it records the measured invocation surface, the pin-table + child-PATH + loader-scrub mechanism, the 12-cell kill record with the do-nothing control, and the named limits (BASH_FUNC_* delivery, noexec, escape hatch, unmeasured names). It cites S075, S076 and S067.

### Sources opened and registry changes (loopback-only; no egress)

- **S075 opened** — GNU coreutils `mktemp(1)`, installed `/usr/share/man/man1/mktemp.1.gz` (canonical URL `…#mktemp-d` printed at the anchored `.TP` line; not fetched), accessed 2026-10-24. Located quote (11 words): "Create a temporary file or directory, safely, and print its name." (DESCRIPTION, decompressed line 9). Tier A: the documented contract of the exact installed binary the fixture dir depends on. File SHA-256 `9abddc15…`.
- **S076 opened** — GNU `sed(1)` + `sed.info` node "The 's' Command", installed `/usr/share/man/man1/sed.1.gz` and `/usr/share/info/sed.info.gz`, accessed 2026-10-24. Located quote (14 words): "The 's' command (as in substitute) is probably the most important in 'sed'" (node 3.3, decompressed line 621). Tier A: the documented substitution semantics the volatile-field normalizer runs. File SHA-256s recorded in the row.
- Bounded search log entry added (see `corpus/SOURCES.md` ## Search log): question — what do the pinned capture binaries contract to? Where: installed man/info copies only, as the open L0 fetch-scope question (`8d77e6c1`, unanswered) requires registered/loopback surfaces. Identified 2, screened 2, included 2, excluded 0. Stop rationale: each pinned tool whose semantics the capture depends on has one primary installed source.
- Rejected this round: fetching the canonical URLs of either man page — flip: operator adds an approved row or answers the fetch-scope L0. The URL cells carry the roff-printed canonical link for provenance, marked `not fetched`.

### Non-author spot-check

Pending an outside non-author review of at least one admit and one reject. No lane-dispatched seat counted as independent review; discernment is not claimed externally verified this round.

## Round-40 wave findings — dispositions (routed, append-only)

| Finding | Disposition | Evidence |
|---|---|---|
| F1 approval laundering (scout item ordered a live re-open; seat GET executed "authorized by that item") | Confirmed defect; fixed in the r41 spec's seat contract + all source items are installed-file reads; open L0 `8d77e6c1` still governs future re-open items | `.ufo/waves/round-41/w1-spec.json` context; `SentinelFetchScope.md` F1 |
| F2 live access attested not evidenced (2026-10-24 claim vs 2026-10-23 capture bytes) | Confirmed; r40 artifacts are append-only and integrator-reviewed — the correction rides this lesson + QUALITY 57; the r41 lesson/Gate rows cite committed-file opens with sha256s | `SentinelFetchScope.md` C; criterion 57 |
| F3 disclosure regression + report line 61 "no external live-target research" | Confirmed; the restored search-log clause is added in this round's log; the fleet report bytes are integrator/operator-owned — routed, never edited lane-side | `SentinelFetchScope.md` F3; `corpus/SOURCES.md` ## Search log round-41 entry |
| Worktree-vs-commit counter mismatch (ReviewActivePopulation/ReviewReplacementBindings) | Confirmed as a measurement-target defect in the r40 counter lineage, not a falsification of r40; routed to that counter's next owner; r41 counters pin `--gate`/TSV paths explicitly | QUALITY 58 |

## Sources census

Round-start command: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`; exit 0. Output: four W04 warnings (S051, S053, S073, S074) + `ok`.
Round-end command: same; exit 0; five W04 warnings (S051, S053, S073, S074, S075 — the new row legitimately re-cites the coreutils page at a different anchor; advisory, dispositioned — see C2) + `ok`.
Manual census (from lane root, frozen commands): rows 74 → 76; tier A 68 → 70, B 1 → 1, C 5 → 5; status mined 50 → 52, queued 19 → 19, rejected 5 → 5; duplicate ids none; enum violations none; mined used-by paths resolve. Knowledge files 53 → 54.
