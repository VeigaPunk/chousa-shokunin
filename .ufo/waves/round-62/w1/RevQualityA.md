# RevQualityA — round 62 w1 — draft QUALITY criterion: forger-battery gate for counters

Lane revision read: 388d153519a36a4c3f34d56d034870f032865a70. Claims sha256
a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc (verified by `sha256sum`).
Battery `corpus/evidence/round62/c1v2-battery.py` sha256 prefix `9afe00b917fb95e2`; v2 counter prefix `b7016fba91b03460` (matches claims).
Tools: none installed. No lane writes (battery run with `--work` in scratch; `-B`).

## Findings

1. **The proposed criterion duplicates criterion 119 in its rule.** Criterion 119 (`corpus/QUALITY.md:986`)
   already requires a frozen counter's control matrix to be run and committed before it binds data, and its
   matrix already includes a token forger, a naive guard, do-nothing stubs and a positive control. What the
   draft adds is the named forger families (profile differential, sandbox that removes the counter from the
   builder's view). Those are the round-62 battery's content, not a new rule. Recommendation: fold the
   battery command into 119's Check as an amendment; do not file a 124. `text_ready=no` as a new number.
   Criteria 98, 102, 106, 120 and 123 cover adjacent classes (oracle reach, call-counting forges, seed
   ordering, structural sweep); none names a forger battery with a profile differential.

2. **Red-before reproduces the claimed red state.** Command (lane root):
   `python3 -B corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round61/c1-count.py --work /fast/scratch/hyaku/chousa-r62/RevQualityA/bat61`
   Observed (`bat61.out`): all 12 forgers `counter_exit=0 want=1 MISS | LEGS=20/20 C1=PASS`;
   final line `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=0/12 STUBS_REJECTED=4/4 BATTERY=FAIL`, `exit=1`.
   This matches `controls/c1v2-before.txt` line 24.

3. **The same battery on the v2 counter passes.** Command as above with `--counter corpus/evidence/round62/c1v2-count.py`.
   Observed (`bat62.out`): landed 3/3 `LEGS=20/20 C1V2=PASS`; positives 4/4; forgers F01–F12 each
   `counter_exit=1 want=1 ok` (LEGS 10–19/20 `C1V2=FAIL`); stubs 4/4 (LEGS 1, 14, 11, 11 of 20);
   `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`, `exit=0`.

4. **Attack on the battery's Check: a counter that keys on the subject path passes.** I wrote a 6-line
   wrapper (`/fast/scratch/hyaku/chousa-r62/RevQualityA/path-keyed.py`): if `--builder` matches `/F\d\d/`
   exit 1, else exec the v2 counter. Battery run (`bat-pk.out`, wall time 44.76 s):
   `FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 LANDED=3/3 POSITIVES=4/4 BATTERY=PASS`, `exit=0`.
   Cause (read from `c1v2-battery.py` lines 139–180): each subject is written to `work/<name>/builder.py`
   with `<name>` = `F01`…`F12`, and the counter receives that path in `--builder`. A counter can read the
   subject name from its own argv, so the battery cannot tell a discriminating counter from one that
   only reads the forger's directory name. This is a hole in the frozen battery, not in the v2 counter's
   leg logic. Routed as a battery limit for a later round (randomise subject directory and builder names
   per run). Not closed here: the battery is frozen and I did not edit it.
   Consequence for the draft: its Check can fail against the round-61 counter and the null counters, but
   not against a counter that keys on argv.

5. **"Committed before binding" is not checkable by commit ancestry here.** `git -C <lane> log --format='%h %ad'
   -- corpus/evidence/round62/c1v2-battery.py corpus/evidence/round62/c1v2-count.py corpus/evidence/round62/claims.md`
   prints one commit, `388d153 2026-10-28 20:12:01 -0300` (claims, counter, battery, controls in one commit).
   The order "controls ran before binding" is therefore only evidenced by the receipt contents
   (`controls/c1v2-before.txt`, `null-counters.txt`), not by history. The draft's Check must not claim more.

## Draft criterion text (for 119 amendment, or 124 if the L1 rejects the merge)

**124. A counter that runs a candidate tool binds a claim only after a committed detection-forger battery
passes on it, and that battery does not hand the counter the subject's name through its own arguments.**
Round 61's C1 counter reached `LEGS=20/20 C1=PASS` for twelve forgers that detect the counter by cwd name,
environment keys, file names, parent or any process's command line, LANG, RLIMIT_FSIZE, stdin, or stdout
being a file, so a counter that runs every leg under one fixed profile can be read by a builder that
inspects that profile (`corpus/evidence/round62/controls/c1v2-before.txt` line 24:
`FORGERS_REJECTED=0/12 BATTERY=FAIL`). Check: `python3 -B corpus/evidence/round62/c1v2-battery.py --counter
<counter> --work <absent dir>` exits 0 with `BATTERY=PASS`; the battery's subject directory and builder names
are random per run (not checked by the current battery — see finding 4). Shown able to fail: on the
round-61 counter the same command prints `FORGERS_REJECTED=0/12 … BATTERY=FAIL`, exit 1 (`bat61.out`); on
`c1v2-count.py` it prints `BATTERY=PASS`, exit 0 (`bat62.out`). Named limit (finding 4): a counter that keys
on `--builder` path names prints `BATTERY=PASS`, exit 0 (`bat-pk.out`).

## Check run on the real evidence and on red-before

| state | command | observed | exit |
|---|---|---|---|
| red-before (round-61 counter) | battery `--counter corpus/evidence/round61/c1-count.py` | `FORGERS_REJECTED=0/12 … BATTERY=FAIL` | 1 |
| evidence (v2 counter) | battery `--counter corpus/evidence/round62/c1v2-count.py` | `FORGERS_REJECTED=12/12 … BATTERY=PASS` | 0 |
| attack (path-keyed wrapper) | battery `--counter …/path-keyed.py` | `FORGERS_REJECTED=12/12 … BATTERY=PASS` | 0 |

Both red and evidence states match the frozen claim's stated before/after strings. The attack row shows
the check passes a gamed counter, which is the reason for the battery amendment in finding 4.

## Verification gaps and limits

- Not run: the full v2 controls matrix (`controls/run-c1v2-controls.py`) and the null counters. Their receipts
  are committed (`controls/c1v2-controls.txt`, `null-counters.txt`); I cite them and did not re-run them.
- Not run: `c1v2-count.py` at fresh seeds (the 120/120 seed-stability check is outside this item).
- Battery wall time for the full round-61 and v2 runs was not measured (only the path-keyed run: 44.76 s).
- The battery's forgers and controls are authored by the lane that wrote the counter (claims, named overfit risk).
- Entailment of 119 vs. 124 is judged, not machine-checked; the duplicate call is my reading of the rule text.

## Scratch

`/fast/scratch/hyaku/chousa-r62/RevQualityA/` (bat61, bat62, bat-pk outputs and the wrapper) is removed
before yield. No lane file, git index or fleet file was changed.

VERDICT: CRITERION_CHECK_CAN_FAIL=yes duplicate_of=119 text_ready=no
