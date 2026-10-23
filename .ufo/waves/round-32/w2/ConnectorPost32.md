# Post-landing sibling scan (round 32, C1/C2)

**Verdict: HOLDS — no sibling-lane consumer found; round-32 changes do not break any lane.**

## What was scanned
All 21 `*-shokunin` lanes (excluding `chousa-shokunin` itself), production paths only (`.ufo/` and `.git/` excluded), for:
- consumption of chousa `verify-all --json` manifests;
- parsing of `verify-chain` summary lines (`RESOLVED_HOPS=`, `RESEARCH_GATE: … resolvable=`);
- vendored copies of `tools/research-gate.sh`.

## Evidence
1. `grep -RIl "research-gate" --exclude-dir=.ufo --exclude-dir=.git --exclude-dir=.tower .` → only `./chousa-shokunin/corpus/knowledge/*` (chousa itself) plus fleet `./LOG.md`, `./MANIFEST.json`. No lane production file references chousa's gate. (`grep … | grep -v '^./chousa-shokunin/'` empty.)
2. `grep -RIl "research-gate.sh" --exclude-dir=.ufo --exclude-dir=.git --exclude-dir=.tower .` → only `./LOG.md`, `./MANIFEST.json` (fleet-level), no lane.
3. `find . -path '*/.ufo' -prune -o -name 'research-gate.sh' -print` → only `./chousa-shokunin/tools/research-gate.sh` and `./.tower/jj-probe/chousa-shokunin/tools/research-gate.sh` (stale probe, sha256 `b5d0f9…` vs landed `f47318…`; not a lane).
4. `grep -rn "verify-chain\|verify-all" …` in non-`.ufo` lane files → only `game-dev-3d-shokunin/reports/*` which invoke that lane's own `scripts/verify_all.sh`, not chousa's.
5. Lanes that mention chousa in production files (`game-dev-2d/3d`, `kengaku`, `kake`, `lore`) do so only as method provenance (`chousa-shokunin/SKILL.md`, `corpus/knowledge/*`), not as gate consumers (e.g. `game-dev-3d-shokunin/corpus/QUALITY.md:5`, `lore-shokunin/PROVINCE.md:27`).

## Compatibility assessment
- C1 (flock-serialized manifest append): output bytes/format unchanged (JSONL, one object/line, inode preserved); only ordering/locking changes. No consumer to break; any external JSONL reader unaffected.
- C2 (`verify-chain` gained `resolvable=N` in the `RESEARCH_GATE:` summary, plus `observed=resolvable` lines only for false unavailability marks): existing consumers that grep `^RESOLVED_HOPS=` or `RESEARCH_GATE: … findings=… drift=…` still match; the appended token is additive. `.ufo` recheck commands (kaika-w3, kagi `ConnChousa`) reference `RESOLVED_HOPS=`/exit codes, not the new token, so they remain valid.
- No lane vendors `research-gate.sh`; the only non-lane copy is the stale `.tower` probe.

## Limits
- `.ufo/` wave artifacts and sandboxes (e.g. kagi round-28 sandboxes) contain historical clones/references but are not production consumers and were not executed by this scan.
- No network access used.

Report written once at `.ufo/waves/round-32/w2/ConnectorPost32.md`.
