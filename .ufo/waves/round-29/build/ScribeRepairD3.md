# Round 28 census correction

## Evidence and scope
- Read `corpus/evidence/round29/claims.md` first, then the routed note at `corpus/lessons/round-28-verifier-spotcheck.md:50-54,125-126`.
- Read-only command `git -C /home/vgpnk/Projects/shokunin show b4b338e9 --stat`: exit 0; commit `b4b338e92ca483b92079f8a2486b77024bf76847`; 42 files changed, 11,598 insertions, 7 deletions.
- Read-only command `git -C /home/vgpnk/Projects/shokunin show b4b338e9:.ufo/waves/hyaku/chousa28-negative-records/parent-census.json`: exit 0. Witness fields: `at=2026-10-22 02:49:09.859760 UTC`; `actual_safe_commit=7c87b9734eb71985e19767af36d57dff89536521`; `argv=bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`; recorded `exit=0`; `stdout="chousa\tok\t/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md\n"`; `stderr=""`. The limits field says this was a common census on canonical safe records, not a full claim C 1, unsafe-hypothesis, oracle, source-truth, or privacy certification.
- A case-insensitive search for `census` in the five requested files found the stale Round 28 status at `LOG.md:1177`, `SCORECARD.md:1587`, and `corpus/lessons/round-28.md:57`. `LOG.md:1178` is adjacent pending-scope wording; the witness confirms a scoped invocation, but does not establish who arranged it. The scorecard wording about permission is likewise not settled by this execution record.
- Other hits are historical or describe future work: `LOG.md:827,1138`; `SCORECARD.md:1257,1276,1558`; `corpus/README.md:54,58,127,928`; `SKILL.md:569`; and `corpus/lessons/round-28.md:63`. They do not state that the Round 28 end census did not run.

## Draft appends — do not replace earlier text

### Append to `LOG.md`
2026-10-23 correction: This entry said no end census had been produced and left its scope as pending. The fleet witness records `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`, run at 2026-10-22 02:49:09.859760 UTC on the recorded safe commit; the command exited 0 and printed `chousa\tok\t/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`. This corrects the run-status record only. The Round 28 verifier note routed this as defect D 3 at `corpus/lessons/round-28-verifier-spotcheck.md:50-54,125-126`.

### Append to `SCORECARD.md`
2026-10-23 correction: This scorecard said no end census was authorized at that stage. The fleet witness records `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`, run at 2026-10-22 02:49:09.859760 UTC on the recorded safe commit; the command exited 0 and printed `chousa\tok\t/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`. The witness establishes execution, but does not identify who arranged it; this correction records the run without deciding that question. The Round 28 verifier note routed this as defect D 3 at `corpus/lessons/round-28-verifier-spotcheck.md:50-54,125-126`.

### Append to `corpus/lessons/round-28.md`
2026-10-23 correction: This lesson said no end census had run and left it awaiting a safe-record update and scoped request. The fleet witness records `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa`, run at 2026-10-22 02:49:09.859760 UTC on the recorded safe commit; the command exited 0 and printed `chousa\tok\t/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`. This corrects the run-status record only. The Round 28 verifier note routed this as defect D 3 at `corpus/lessons/round-28-verifier-spotcheck.md:50-54,125-126`.

## Gates and touched surfaces
No product files, frozen claim, counter, fixture, lane VCS state, or index were changed. No tool was installed. No C 1 measurement or other verification gate was run; this report verifies only the specified fleet witness. The sole written artifact is `.ufo/waves/round-29/build/ScribeRepairD3.md`.
