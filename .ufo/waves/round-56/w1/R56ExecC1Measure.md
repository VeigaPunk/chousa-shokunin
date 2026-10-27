# R56ExecC1Measure — independent re-measurement of R56-C1 (operability, build-spans gate)

Seat R56ExecC1Measure (leaf, no dispatch). Candidate `46e1758f3d8a5d1bf30200d2ff7d909b0230feed`; predicate
`corpus/evidence/round56/claims.md` §R56-C1, untouched — findings are reported, never patched. Scratch
`/fast/scratch/hyaku/chousa-r56/R56ExecC1Measure/` (removed; receipts pasted here). No network, no lane write except this
report, no install (`/usr/bin/time` absent — timing is `date +%s.%N`; `pacman` untouched).

## 1. Identity — every measured file equals the candidate commit's blob

```
$ for f in corpus/evidence/round56/{c1-gate.py,c1-count.py} $(git ls-tree -r --name-only $REV corpus/evidence/round56/{battery,probes});
  do printf '%s %s\n' "$(sha256sum $f|cut -c1-16)" "$(git show $REV:$f|sha256sum|cut -c1-16)"; done
e3cb3ec576459255 e3cb3ec576459255  gate           5eba634ffb9138a7 5eba634ffb9138a7  count
a6ee9dcb86c18748 a6ee9dcb86c18748  m1-quote-only-span.py        136adc6086815068 136adc6086815068  m2-span-beside-quote.py
583b66bd5352c685 583b66bd5352c685  m3-wrong-digest.py            e94e9e37ea2d692d e94e9e37ea2d692d  m4-no-quote-lines.py
e4f9cb777ee7cd38 e4f9cb777ee7cd38  m5-extra-span-file.py         255d95fc8c4aac33 255d95fc8c4aac33  m6-manifest-on-refusal.py
316955f567d9ff6b 316955f567d9ff6b  m7-read-outside.py            e86a52a62fffdb5f e86a52a62fffdb5f  oracle-m8-unpinned.py
a1fe89a1e657bb3e a1fe89a1e657bb3e  probes/p1-forkexec.py         3244dc2067208426 3244dc2067208426  probes/p2-dirfd.py
```
All 12 equal (re-checked after the measurements: `post-run mismatches=0`). Battery = exactly the 8 tracked entries on
disk (7 violators + the oracle copy), probes = 2, no stray `*.py`, no untracked file under `round56/` before my runs.
Supporting pins: `tools/build-spans.py` `1ed2650af28ea8e3…` = at `46e1758` = `c1-before.txt`'s builder line;
`tools/capture-text.py` `2c0140bc04029c8f…` = the gate's `CAPTURE_TEXT_SHA` (`c1-gate.py:16`); `diff tools/capture-text.py
battery/oracle-m8-unpinned.py` = `458a459,461` three comment lines only (behaviour same, digest differs = the M8 lever);
`diff round55/c1-count.py round56/c1-gate.py` = 21 lines, three hunks (docstring; `BAD` gains
`"_posixsubprocess.fork_exec", "os.chdir"` at `c1-gate.py:95`; mkdtemp prefix) — round 55's counter plus exactly those
two events, as claimed.

## 2. Pass 1 — `python3 corpus/evidence/round56/c1-count.py --work $S/w1/work`

```
gate=…/round56/c1-gate.py sha256=e3cb3ec5764592553b8601a1718bb5d07fd8c9991de9f4128482d41ffd4e4971
builder=…/tools/build-spans.py sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6
battery m1…m7 sha256=a6ee9dcb…136adc60…583b66bd…e94e9e37…e4f9cb77…255d95fc…316955f5… (as §1)
battery oracle-m8-unpinned.py sha256=e86a52a62fffdb5fbc2b451bd31e5535642234f7f0647c5692ce2e0dba6d7e0a
CANDIDATE=2/2 seed7=(0, 'PASS', 'PASS', 'PASS', 'PASS') seed56=(0, 'PASS', 'PASS', 'PASS', 'PASS')
MUTANT M1 NO_SLICE KILLED by m1-quote-only-span.py: seed 7 order GGmmmG: leg GENOLE G='S901 span is not a slice of the defined form' mutant=PASS | seed 56 order mGGmmG: leg GENOLE G='S901 span is not a slice of the defined form' mutant=PASS
MUTANT M2 NO_CHAR KILLED by m2-span-beside-quote.py: seed 7 order mmGGGm: leg GENOLE G='S901 char' mutant=PASS | seed 56 order mmGmGG: leg GENOLE G='S901 char' mutant=PASS
MUTANT M3 NO_SHA KILLED by m3-wrong-digest.py: seed 7 order GmmGmG: leg GENOLE G='S901 capture_sha256' mutant=PASS | seed 56 order GmmGGm: leg GENOLE G='S901 capture_sha256' mutant=PASS
MUTANT M4 NO_QUOTE KILLED by m4-no-quote-lines.py: seed 7 order mGGmmG: leg GENOLE G='S901 QUOTE line' mutant=PASS | seed 56 order mmmGGG: leg GENOLE G='S901 QUOTE line' mutant=PASS
MUTANT M5 NO_EXTRA KILLED by m5-extra-span-file.py: seed 7 order GGmGmm: leg GENOLE G='extra or missing span files' mutant=PASS | seed 56 order GmGmGm: leg GENOLE G='extra or missing span files' mutant=PASS
MUTANT M6 REF_TSV KILLED by m6-manifest-on-refusal.py: seed 7 order mmGGGm: leg REFUSE G='NOFORM: spans.tsv written' mutant=PASS | seed 56 order mGmGGm: leg REFUSE G='NOFORM: spans.tsv written' mutant=PASS
MUTANT M7 ALLOW_ROOT KILLED by m7-read-outside.py: seed 7 order mGmGmG: leg GENOLE G='rc=97 b"AUDIT_FORBIDDEN open \'/home/vgpnk/Projects/shokunin/chousa-shokunin/SKIL' mutant=PASS | seed 56 order GGmGmm: …(same)
MUTANT M8 NO_ORACLE_SHA KILLED by oracle-m8-unpinned.py: seed 7 order GmmGmG: G=('ENV', 2) mutant=(0, 'PASS', 'PASS', 'PASS', 'PASS') | seed 56 order GmmmGG: G=('ENV', 2) mutant=(0, 'PASS', 'PASS', 'PASS', 'PASS')
MUTANT M9 WIN_NL KILLED by CANDIDATE: seed 7 order mGGGmm: G=(0, 'PASS', 'PASS', 'PASS', 'PASS') mutant=(1, 'FAIL', 'FAIL', 'PASS', 'PASS')
PROBE P1 FORKEXEC DENIED seed7=(1, 'FAIL', 'FAIL', 'FAIL', 'FAIL') seed56=(1, 'FAIL', 'FAIL', 'FAIL', 'FAIL')
PROBE P2 DIRFD DENIED seed7=(1, 'FAIL', 'FAIL', 'FAIL', 'FAIL') seed56=(1, 'FAIL', 'FAIL', 'FAIL', 'FAIL')
RUNS=124
CANDIDATE=2/2 KILLED=9/9 DENIED=2/2
C1=PASS      exit=0   WALL=144.2s
```

## 3. Pass 2 — same command, fresh `--work $S/w2/work`

```
CANDIDATE=2/2 seed7=(0, 'PASS', 'PASS', 'PASS', 'PASS') seed56=(0, 'PASS', 'PASS', 'PASS', 'PASS')
MUTANT M1 NO_SLICE KILLED by m1-quote-only-span.py: seed 7 order mGGmGm: leg GENOLE G='S901 span is not a slice of the defined form' mutant=PASS | seed 56 order GmmGmG: same reason, mutant=PASS
MUTANT M2 NO_CHAR KILLED by m2-span-beside-quote.py: seed 7 order GGGmmm: leg GENOLE G='S901 char' mutant=PASS | seed 56 order GmGGmm: leg GENOLE G='S901 char' mutant=PASS
MUTANT M3 NO_SHA KILLED by m3-wrong-digest.py: seed 7 order mGGmmG: leg GENOLE G='S901 capture_sha256' mutant=PASS | seed 56 order GmmGGm: leg GENOLE G='S901 capture_sha256' mutant=PASS
MUTANT M4 NO_QUOTE KILLED by m4-no-quote-lines.py: seed 7 order GmGGmm: leg GENOLE G='S901 QUOTE line' mutant=PASS | seed 56 order mGGmGm: leg GENOLE G='S901 QUOTE line' mutant=PASS
MUTANT M5 NO_EXTRA KILLED by m5-extra-span-file.py: seed 7 order mGGmGm: leg GENOLE G='extra or missing span files' mutant=PASS | seed 56 order mGmGmG: leg GENOLE G='extra or missing span files' mutant=PASS
MUTANT M6 REF_TSV KILLED by m6-manifest-on-refusal.py: seed 7 order mGmGmG: leg REFUSE G='NOFORM: spans.tsv written' mutant=PASS | seed 56 order mGmmGG: leg REFUSE G='NOFORM: spans.tsv written' mutant=PASS
MUTANT M7 ALLOW_ROOT KILLED by m7-read-outside.py: seed 7 order GmmmGG: leg GENOLE G='rc=97 b"AUDIT_FORBIDDEN open \'/home/vgpnk/Projects/shokunin/chousa-shokunin/SKIL' mutant=PASS | seed 56 order GmGmGm: …(same)
MUTANT M8 NO_ORACLE_SHA KILLED by oracle-m8-unpinned.py: seed 7 order GmmGGm: G=('ENV', 2) mutant=(0, 'PASS', 'PASS', 'PASS', 'PASS') | seed 56 order GmmmGG: G=('ENV', 2) mutant=(0, 'PASS', 'PASS', 'PASS', 'PASS')
MUTANT M9 WIN_NL KILLED by CANDIDATE: seed 7 order mmmGGG: G=(0, 'PASS', 'PASS', 'PASS', 'PASS') mutant=(1, 'FAIL', 'FAIL', 'PASS', 'PASS')
PROBE P1 FORKEXEC DENIED seed7=(1, 'FAIL', 'FAIL', 'FAIL', 'FAIL') seed56=(1, 'FAIL', 'FAIL', 'FAIL', 'FAIL')
PROBE P2 DIRFD DENIED seed7=(1, 'FAIL', 'FAIL', 'FAIL', 'FAIL') seed56=(1, 'FAIL', 'FAIL', 'FAIL', 'FAIL')
RUNS=124    CANDIDATE=2/2 KILLED=9/9 DENIED=2/2    C1=PASS   exit=0   WALL=196.4s
```
Verdicts identical to pass 1, every printed `order` different (per-kill six-run order is `random.shuffle`d over
`secrets.randbits(64)`, `c1-count.py:212-216`). Wall spread (144.2 vs 196.4 s) is host contention: a sibling seat's
`soffice.bin` (profile under `…/chousa-r56/R56CritC1Forge/…`) was converting documents during pass 2.

## 4. Round-55 counter as gate, round-56 battery

```
$ python3 corpus/evidence/round56/c1-count.py --gate corpus/evidence/round55/c1-count.py --work $S/w3/work
gate=…/round55/c1-count.py sha256=5506f240c53ff83c7c17b7252c7627871b4b1af7c1ca739b461fdbcc32048906
CANDIDATE=2/2 seed7=(0,'PASS','PASS','PASS','PASS') seed56=(0,'PASS','PASS','PASS','PASS')
MUTANT M1..M9 → KILLED (both seeds; M9 at seed 7 by CANDIDATE)
PROBE P1 FORKEXEC NOT_DENIED seed7=(0,'PASS','PASS','PASS','PASS')
PROBE P2 DIRFD NOT_DENIED seed7=(0,'PASS','PASS','PASS','PASS')
RUNS=122   CANDIDATE=2/2 KILLED=9/9 DENIED=0/2   C1=FAIL   exit=1   WALL=291.2s
```
Both probes run 4/4 legs PASS under the unhooked counter → the two bypasses are real, not asserted.

## 5. Causal decomposition (each row measured here or in a frozen receipt)

| gate | battery | KILLED | DENIED | receipt |
|---|---|---|---|---|
| round 55 | round-55 controls | 1/9 | 0/2 | `controls/c1-before.txt` |
| round 55 | round 56 | **9/9** | 0/2 | §4 |
| round 56 | round-55 controls (HOOKONLY re-run, `$S/w4`, RUNS=24, WALL=81.3s) | 1/9 | **2/2** | reproduced `c1-controls.txt` |
| round 56 | round 56 | **9/9** | **2/2** | §2, §3 |

Battery alone lifts kills 1→9; the two hook events alone lift denies 0→2; only both meet the target. `M9` is killed in
all four rows by `CANDIDATE` (`(1,FAIL,FAIL,PASS,PASS)` vs `(0,PASS×4)`) — the claim's movement is the other eight
mutants plus the two probes, exactly as stated.

## 6. Side-effect checks

- Hashes after all runs: `post-run mismatches=0` for the 11 C1 files; `git status --porcelain` shows no modification I could have made. One snapshot (after pass 1) carried a sibling edit, ` M corpus/lessons/round-55.md`, gone by the last check (HEAD had advanced to `99eff0ec`, the L1's C2 commit, which left every C1 input byte-identical — §1).
- `pgrep -af 'soffice.bin.*R56ExecC1Measure'` → `none-of-mine` after passes 2 and 3; no `soffice.bin` with a profile under my scratch survived (the gate's own LibreOffice conversion uses `-env:UserInstallation` inside each run dir, which lives under `--work`).
- Every `--work` was a freshly created empty dir under my scratch (`w1`…`w4`); run dirs are `secrets.token_hex(8)` named (`c1-count.py:190`) and removed by the driver.

## 7. Calibration notes and residual risk (reported, not patched)

1. **M9's kill is single-seed** (`seed 7` in all four rows; the driver stops at the first hit, `c1-count.py:249-256`). The frozen predicate says "at some seed", so it passes as written; a two-seed reading would make it a partial kill.
2. **M9 is the documented near-equivalent mutant** (second newline guard dropped via `EXTRA`, `c1-count.py:60`) and is killed by the landed builder, not a violator: "9/9" = 8 battery kills + 1 builder kill, as the claim itself says.
3. **M8's vector is coarsened** to `('ENV', rc)` (`c1-count.py:205-208`), comparing stdout-marker presence, not legs; observed `G=('ENV',2)` vs `mutant=(0,PASS×4)` at both seeds, so no ambiguity here, but a non-`ENV_CHANGED` failure of the oracle-sha clause would be invisible.
4. **Kill attribution rests on the frozen `MARKER` regexes** and on the mutant passing the leg G fails (`c1-count.py:239-241`); printed G reasons are the mutated clauses' own text and the mutant side prints `mutant=PASS` in all eight battery kills. Re-running HOOKONLY (§5) confirms an alternating/copying battery still scores 1/9.
5. **Battery and driver are candidate, not frozen** (claims.md: written after the freeze); this measures operability at `46e1758`, not a frozen battery. Wall time is host-noisy (81–291 s); `RUNS=` is the stable quantity (124/124/122/24).

VERDICT: R56-C1 re-measured at `46e1758` — the frozen driver returns `CANDIDATE=2/2 KILLED=9/9 DENIED=2/2 C1=PASS`
(exit 0) in two independent 124-run passes with disjoint random orders (144.2 s, 196.4 s), the round-55 counter with the
same battery returns `KILLED=9/9 DENIED=0/2 C1=FAIL` (122 runs, 291.2 s), so the two added hook events are what close
the probes and the battery is what closes the kills: the claim SURVIVED, with M9's single-seed kill and the unfrozen
battery recorded as scope caveats.
