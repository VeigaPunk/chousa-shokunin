# ScoutMistakesThisRound — round 62, wave w1 — mistake mining

Lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Base `8607de8` (20:12:01), freeze `388d153`, wave spec `d173d14`.
Read-only. No edits to frozen paths, no git mutation (`git status` only refreshes the index stat cache).

## Findings: defects the freeze left (stale statements and latent defects)

1. **Seat count is wrong.** `claims.md` "Wave shape": "one v2 wave `w1`, 64 seats". `w1-spec.json` has 66 items;
   `w1-dispatch.json` `counts` = `{spawn: 66, total: 66}`; commit `d173d14` says "validated v2, 66 seats". The 64 in the
   claims matches `policy.waveMinLanes` (64), not the seat count. Stale.
2. **"The lane's only scored axis" is contradicted.** `claims.md` C1 says operability is "the lane's only scored axis".
   `w1-spec.json` `axes` = `[operability, coverage, calibration]`; the same claims file targets coverage for C2; the
   round-61 verifier lesson scores depth, quality, discernment, expansion. Stale.
3. **"200 MiB address-space limit" is true only for the plain profile.** `c1v2-count.py:283` plain returns `AS_LIMIT`
   (200 MiB); `c1v2-count.py:291` neutral returns `AS_LIMIT + secrets.choice(range(0, 25)) << 20`, i.e. 200–224 MiB.
   The claims text ("under a 200 MiB address-space limit") and the counter docstring (`c1v2-count.py` lines 11, 44)
   both say 200 MiB for every run. Stale in claims and docstring; the counter behaviour itself is unchanged.
4. **Reversed control statement.** `claims.md` C1: "`null-pass.py` (always exit 0) accepts 0/12 forgers and 0/4 stubs".
   `controls/null-counters.txt`: `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=0/4 BATTERY=FAIL`.
   So null-pass accepts 12/12 forgers and 4/4 stubs (it rejects 0 of each). Stale.
5. **Miscited source.** `claims.md` "Round 61's closure (`corpus/lessons/round-61-verifier-spotcheck.md`, routed defects
   1 and 2) is the reason for claim C1". In that file routed item 1 is the C1 counter; routed item 2 is the
   `research-gate.sh --selftest` commit, unrelated to C1. The forgeable-by-detection finding (CritC1Sniff, CritC1Detached,
   CritC1Rss) is Mistake 2 in `corpus/lessons/round-61.md:36`, which the claims never cite. Stale citation.
6. **Latent footgun in a frozen control runner.** `controls/run-c1v2-controls.py` lines 88–97: `work.mkdir(exist_ok=True)`,
   no absent-or-empty check, and `finally: shutil.rmtree(work)`. Passing a populated directory as `--work` deletes it.
   The sibling `run-c2v2-controls.py` lines 42–44 refuses a non-empty `--work`. Not editable (frozen); route to next round.

## Fixed on the way (verified in the current tree)

7. **X04 pattern.** Lead's note: the X04 mutant broke stdin handling until its pattern was rewritten. Current state:
   `run-c1v2-controls.py:62` asserts `src.count(old) == 1`; the pattern matches once in `c1v2-count.py:302-306`
   (`rfd, stdin = None, subprocess.DEVNULL`); receipt `controls/c1v2-controls.txt` shows X04 KILLED with F09 accepted, expected ok.
   Not re-run (C1 battery is seat work and heavy); pattern count checked with a read-only Python `count`.
8. **C2 positive control, census E11.** Lead's note: the first positive failed E11 because the mirror lacked knowledge files.
   Current `run-c2v2-controls.py:47-48` copies `corpus/` ignoring only `captures`, `evidence`, `fixtures`, so `knowledge/` is in.
   Re-run in scratch (below): `positive` PASS, `C2V2_CONTROLS_UNEXPECTED=0`.
9. **"A claim sharing no words with its quote."** Not reconstructible: the repo has one commit per artifact and no draft
   history. Current counter requires at least 2 shared 5+-letter words per claim (`c2v2-count.py:199-204`); the `junk-claim`
   variant (`run-c2v2-controls.py:98`) FAILs. Not counted.

## Claim-statement audit (what matches)

- Digests (16-hex prefixes, `sha256sum FILE | cut -c1-16`): `claims.md` a3193ebd328919e2 (lead's full digest begins
  a3193ebd328919e2 ✔); `c1v2-count.py` b7016fba91b03460 ✔; `c2v2-count.py` 817d5fc0b94e9fc8 ✔; `tools/build-spans.py`
  c366492005ce304a ✔. `c1v2-battery.py` 9afe00b917fb95e2 (no digest claimed).
- Counts that match: 20 legs (`LEG_NAMES`, 20 entries); twelve forgers F01–F12 with the 11 detection classes listed in the
  claims mapping to `SNIFFS` one-to-one; four stubs; four positives (`pos-ref.py`, `pos-indep1..3.py`); three landed copies;
  ten C1 mutants (`X01–X08, X10, X12`, `CONTROLS_UNEXPECTED=0`); 14/14 probe facts (`candidate-openat2-probe.txt`
  `PROBE_FACTS=14/14`); 18 C2 single-defect variants plus absent, no-entry-rows, positive and non-sequitur (22 lines, all OK).
- Before-receipts match: `c1v2-before.txt` `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL` exit 1;
  `c2v2-before.txt` `ENTRY=0/1 … CENSUS=1/1 C2=FAIL` exit 1.
- `grep -rl openat2 corpus/knowledge` at base: nothing, rc=1 (`git grep` on `8607de8`) ✔.
- Installed sources: `/usr/share/man/man2/openat2.2.gz` and `/usr/include/linux/openat2.h` exist; `/var/lib/pacman/local`
  lists `man-pages-6.19-1` and `linux-api-headers-7.2-1` ✔ (pacman not invoked).
- `corpus/lessons/round-61-verifier-spotcheck.md`, `corpus/evidence/round61/c1-count.py` exist ✔.
- `S138` "lead recorded in `## Leads`": the Leads bullet exists (unnumbered, "named by wave seat RevC2Claim1 (round 61)");
  no `| S138 |` registry row at base. Loose linkage, not counted as a contradiction.
- Historical "3/10 operability": `corpus/README.md:1025,1035` "round-1 scale (operability 3/10, delta 0)" ✔.

## Commands run and observed output

- `git -C <lane> log --stat 8607de8..HEAD` → `d173d14` (6 files, wave spec) and `388d153` (25 files, freeze).
- `sha256sum … | cut -c1-16` → digests above.
- `TMPDIR=$S python3 -B corpus/evidence/round62/c2v2-count.py` → `ENTRY=0/1 … CENSUS=1/1 C2=FAIL`, exit 1 (matches before).
- `TMPDIR=$S python3 -B corpus/evidence/round62/controls/run-c2v2-controls.py --work $S/c2ctl` → 22 lines, all `OK`,
  `C2V2_CONTROLS_UNEXPECTED=0`, exit 0 (49.9 s; scratch removed by the runner).
- `git -C /home/vgpnk/Projects/shokunin status --porcelain` → 45 entries: 40 ` A` (intent-to-add: 37 under `.scratch/`, plus
  `o.bin`, `oldrep1.out`, `oldrep2.out`), 1 ` M` (`.scratch/goal-20261028-hyaku-run11.md`), 4 `??`
  (`lane3/`, `.scratch/closure-r54/lane/`, `.scratch/closure-r54/work-c2-base/clone/`, `.scratch/closure-r54/work-c2/clone/`).
  Lane `git status --porcelain`: `?? .ufo/waves/round-62/w1.ready.partial`, `?? .ufo/waves/round-62/w1/` only.

## Fleet-root misroot check

- Non-tracked or invisible strays at `/home/vgpnk/Projects/shokunin`: `D=/fast/scratch/hyaku/` (empty tree, 12:07),
  `tools/` (empty, 20:00:16), `ok/` (empty, 10-25), `lane3/` (nested git repo, 14:59), `.scratch/closure-r54/` (12:55),
  `.scratch/kasegi-r44/` (16:27), `o.bin` (10-27), `oldrep1.out`/`oldrep2.out` (10-28 09:10/09:11).
- All predate the round-62 base commit (20:12:01). None carries a round-62 name or path. Fleet-root commits in the window
  (`42576cc9` `.ufo/prompts/chousa-round-62.md`, `33203a2b`, `MANIFEST.json` updates) are by hyaku (orchestrator), not a seat.
- Attribution to a round-62 seat or L1: none. `misroot_files=0` for this round. The 40 intent-to-add entries and 4 untracked
  clones are fleet-root index and tree state from earlier work; the orchestrator should clear them. I did not touch them.

## Counts

- THIS_ROUND_MISTAKES = 8: six left by the freeze (findings 1–6) and two fixed on the way (7–8). Item 9 not counted.
- stale_claim_statements = 5 (findings 1–5).
- misroot_files = 0 (attributable to this round).

VERDICT: THIS_ROUND_MISTAKES=8 stale_claim_statements=5 misroot_files=0
