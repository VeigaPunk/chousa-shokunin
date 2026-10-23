# Round 35 — ScribeLessonMistake

Behavior: Drafted the round-35 `## Mistakes` row only; no lane production file changed.

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| Bash same-statement `local` derived assignment reads the caller's dynamically scoped value: `local hay=$1 span=$2 slen=${#span}` computes `slen` before assigning `span`, so a caller's different `span` length silently governs confirmation | `.ufo/waves/round-35/repairs/base-gate.sh:1632`; `corpus/lessons/round-34-verifier-spotcheck.md:86`; `corpus/evidence/round35/claims.md:114-122`; `.ufo/waves/round-35/repairs/slen-probe.sh:5-14,27-33` | Round-34 non-author verifier spot-check, routed defect 4 (`corpus/lessons/round-34-verifier-spotcheck.md:1-6,81-87`); it was not caught by a counter or selftest (assignment scope) | Proposed QUALITY 45: sweep every `local` line for derived expansions referencing names assigned in the same declaration; split dependent declaration and assignment. Shown able to fail: the frozen design records the reproducer `bash -c 'f(){ local a=$1 b=${#a}; echo $b; }; f hello'` → `0` (`corpus/evidence/round35/claims.md:117`) and records the probe's before/after offset distinction (`claims.md:120-122`; probe definition `slen-probe.sh:13-14,27-33`). The assignment supplies base `offsets=0` / landed `offsets=1`; inferred from those documented results, not independently re-run here. |

Gates: No command, counter, selftest, or probe was executed by this scribe; no gate was scored. Sources were read 2026-10-23. `corpus/QUALITY.md:336-344` shows QUALITY 44 as the latest criterion; QUALITY 45 above is a proposal, not an edit.

Touched surface: this report only. Out of scope: `corpus/lessons/round-35.md`, `corpus/QUALITY.md`, all production code, C1/C2 re-derivation, and all tests. No installs. Artifact: `.ufo/waves/round-35/w2/ScribeLessonMistake.md`.
