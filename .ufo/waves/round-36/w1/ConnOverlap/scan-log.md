# ConnOverlap scan log — chousa round-36 wave 1 (2026-10-23)

Seat: ConnOverlap (leaf, godspeed). Read-only everywhere; no counters/gate/witness
executed; no git/jj writes; no network; no installs (nothing to record under the
tooling directive).

## Shell commands (verbatim)

1. `ls -1d /home/vgpnk/Projects/shokunin/*/ 2>/dev/null`
   exit code 2 (a stray `bash: /` entry); printed the 30 fleet dirs used as the
   repo list (23 sibling *-shokunin dirs incl. `mori-shokukin`/`tameshi-shokukin`
   typo variants, `kaidoku-sh2`, plus non-repo dirs `reports/ research/ scripts/
   local/ templates/ scratch/ dir/`).
2. `cd /home/vgpnk/Projects/shokunin && du -sm -t 1 *-shokunin kaidoku-sh2 2>/dev/null | sort -rn`
   backgrounded by the harness; killed at 300 s ("error: interrupted") — sizing
   only, abandoned in favour of per-repo greps.
3. `mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ConnOverlap && ls -1 /home/vgpnk/Projects/shokunin/mori-shokunin/.ufo`
   exit 0; mori `.ufo` = interactive-sessions, reports, round-2..round-11, waves,
   worktrees.
4. `ls -1 .../mori-shokunin/.ufo/worktrees 2>/dev/null; echo ---; du -sm .../worktrees`
   ls printed `round-18`, `round-19`; du backgrounded, result never consumed.
5. `ls -1 .../worktrees/round-19 | head -20; echo ---; ls -1 .../worktrees/round-18 | head -20`
   exit 0 (temporary shell): r19 = ContentGate{,Actual,Sparse},
   FreezeMetadata{,Actual,Sparse}, RegressionHarness{,Actual,Sparse};
   r18 = DispatchLedger, FreezeOrder, MutDispatchLedger, MutFreezeOrder,
   MutRetentionGate, RetentionGate — mori's own r18/r19 gate-fixture worktrees.

## Grep-tool runs (pattern → scope → result; all with gitignore=false)

P1 = `argv-witness|ENGINE_SWAP_CANARY|WITNESS_PER_RECORD|RESEARCH_GATE_GREP|mechanism-witness`
P1+PS4 = P1 + `|PS4`

- P1+PS4, whole fleet root: TIMEOUT (30 s).
- P1+PS4, 10-repo group (kotoba, kotodama, kake, kama, kumitate, mado,
  mori-shokunin, mori-shokukin, tameshi-shokunin, tameshi-shokukin): TIMEOUT ×2.
- P1+PS4, 10-repo group (kagi, kaidoku, kaidoku-sh2, kasegi, kengaku, revenger,
  souji, tabi, tsukuroi, lore): completed; ALL hits are kaidoku `PS4` —
  seat-file names `PS4.md` (luna rounds) and one session transcript mentioning
  them (229 matched files; first 20 displayed). Decisive PS4-free rerun below.
- `canary` (case-insensitive), 8-repo group (kotoba, kotodama, kake, kama,
  kumitate, mado, mori-shokunin, tameshi-shokunin): completed; signal hits =
  kotoba r23/r37 tripwire+strace canaries (V3.md, M9.md), mori r37 canary
  references; noise = Canary Islands (kotodama), bun canary builds (kake r44).
- P1, per-repo: kotoba `No matches`; kotodama `No matches`; kake `No matches`;
  kama `No matches`; kumitate `No matches`; mado `No matches`;
  tameshi-shokunin `No matches`; mori-shokukin `No matches`;
  tameshi-shokukin `No matches`.
- P1, (audio; game-dev-2d; game-dev-3d): completed; ONLY audio
  `corpus/fixtures/measure_audio.py:39009` (+ 9 verbatim copies under
  corpus/live/r9[267]*) matching the substring "mechanism-witnessed" in a
  docstring. No file named mechanism-witness/argv-witness; no other tokens.
- P1, decisive rerun of the kaidoku group (same 10 repos, no PS4):
  `No matches` (complete, unpaginated) — closes the 229-file PS4 question.
- P1, mori-shokunin scoped: tools+corpus `No matches`; .ufo/waves `No matches`;
  .ufo/reports `No matches`; .ufo/interactive-sessions `No matches`;
  .ufo/round-2..round-11 (one call, 10 paths) `No matches`;
  .ufo/worktrees/round-18 `No matches`; .ufo/worktrees/round-19 TIMEOUT ×2;
  worktrees/round-19/tools+corpus `Path not found` (worktrees are gate-fixture
  trees, not repo snapshots at that level). RESIDUAL: r19 fixture worktrees
  (ContentGate/FreezeMetadata/RegressionHarness families) not fully scanned.
- P1, fleet root `.ufo/reports`: `No matches` (this run was P1 without PS4 —
  the earlier P1+PS4+`|canary` run on the same path completed and its mechanism
  hits are chousa-only: round-35/chousa.md:23,36,111-115,197,231,260-266).
- P1, fleet root `.ufo/waves` + `.ufo/prompts` + `.ufo/state`: `No matches`.
- P1, chousa-shokunin (baseline): completed; hits only inside chousa —
  .jj op_store commit record ("round-36 freeze: engine-swap canary counter …
  per-record argv witness"), .ufo/waves/round-35/* (gen-w2-spec.py:20,39;
  controls/c2-base-s3501.json:2; final/c2-s35{29,39}.json:2;
  measure/c2-after-s35{01,17}.json:2; w2/ConnectorOverlap.md; CritC2AxisFit.md;
  CritClaimSizing.md + controls), tools/mechanism-witness.py,
  tools/argv-witness.py, corpus/evidence/round36/{claims,c1-count,c2-count}.*
  and round-35 counterparts.
- `witness|PS4=|canary` (case-insensitive), tools/ dirs group A (kotodama only
  present; kotoba/kake/kumitate have no tools/ — skipped-missing notice):
  kotodama hits are domain prose ("witness" in culture packets), no PS4=, no
  canary.
- `witness|PS4=|canary`, tools/ dirs group B (tameshi, kaidoku, souji,
  tsukuroi; kagi/kasegi/kengaku/revenger/tabi/lore have no tools/): hits =
  tameshi bash-witness-study.py / witness-metadata.py / registry.json witness
  rows / mutate-and-run.sh GIT_DIR canary arm (:1883-1909) / registry-check.py
  canary; souji CANARY_* leak fixtures (impl-42/47/48, souji-census.sh);
  tsukuroi `no-canary` exec-eval arm (boot-chain-audit.sh:1174-1191). NO PS4=
  anywhere.
- `PS4=`, sibling corpus/scripts dirs (kotoba, kake, kumitate/scripts, kama,
  mado/tools, kotodama, mori, tameshi): `No matches`.
- Glob `reports/` (fleet root): no files (empty). Glob mori `.ufo`: structure
  only. Glob mori worktrees: TIMEOUT (5 s, incomplete — superseded by listings).

## Files opened (read tool, 2026-10-23)

- skill://godspeed
- .ufo/waves/round-36/w1-briefs/ConnOverlap.md
- corpus/evidence/round36/claims.md (:1-157)
- corpus/evidence/round36/c1-count.py (:1-48)
- corpus/evidence/round36/c2-count.py (:1-45)
- tools/argv-witness.py (:1-63)
- tools/mechanism-witness.py (:1-43)
- chousa PROVINCE.md (whole)
- tameshi-shokunin/PROVINCE.md (whole)
- tameshi-shokunin/corpus/knowledge/witness-equivalence-rule.md (whole)
- kumitate-shokunin/PROVINCE.md (whole)
- kengaku-shokunin/PROVINCE.md (whole, some lines truncated by reader)
- audio-shokunin/corpus/fixtures/measure_audio.py (:38994-39048)
- chousa .ufo/waves/round-35/w2/ConnectorOverlap.md (via grep excerpts :12-100)
