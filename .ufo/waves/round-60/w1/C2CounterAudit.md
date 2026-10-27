# C2 counter audit — counterexample and smallest safe correction

## Counterexample

The frozen C2 predicate says the base must fail because no round-60 entry exists, and the counter must verify the *new entry's exact observation and no overreach* against S101. Yet the current counter exits 0 on the unmodified base state:

```text
$ python3 corpus/evidence/round60/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work /fast/scratch/hyaku/chousa-r60/C2CounterAudit/work
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
EXIT=0
```

This is a false-positive witness to the critical admission predicate. `ENTRY` in `corpus/evidence/round60/c2-count.py:8,13` points at the already-existing `corpus/knowledge/citation-count-semantics-r37.md`, not any round-60-specific entry. `scoped` at line 18 checks only that the pre-existing entry contains `#### Unknown` and the generic S101 version-limit phrase; it does not check a new note, its observation, nor overreach. `metadata` at line 17 similarly checks only broad substrings. The pinned form quote (`EXPECTED`) occurs in the existing entry's cited S101 section and establishes neither that the entry changed this round nor that the intended new note is grounded. Thus the base passes, directly contradicting the frozen base-fails requirement (round60-claims.md:15).

## Additional path/provenance defect

The CLI accepts `--root` and computes `raw` and `entry` from it, but `form` is always `ROOT/'.ufo/waves/round-60/s101-open.txt'` (round60/c2-count.py:7,13), where `ROOT` is the script checkout. Running against a separate lane copy therefore mixes that copy's raw capture and entry with the original checkout's form. A digest match does not repair the authority mix: the form does not come from the `--root` under test. This defeats the frozen predicate's `<lane-copy>` isolation and makes the result dependent on external workspace state.

## Evidence chain / scope

- The claim SHA named in the assignment, `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`, does **not** match the frozen-claims file bytes observed here: `sha256sum` returned `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. I did not change the frozen file. Treat this as a freeze-integrity discrepancy to reconcile before relying on the claimed assignment digest.
- The existing knowledge entry is already S101-cited and contains its scope limitation (`corpus/knowledge/citation-count-semantics-r37.md:5,74-80`). This confirms the counter is re-checking pre-existing content rather than proving the round's newly claimed correction.
- The committed offline S101 rendering independently states the type/carrier item at `corpus/evidence/round59/s101-open.txt:245-268`; in particular, 14.2(c) names `文献类型及载体类型标志`, and 14.3.4 describes bracketed type/carrier notation. This supports the bounded source observation only; it says nothing about present-day validity or CNKI implementation.
- The current counter run also prints `RAW_PIN=1`, `FORM_PIN=1`, `QUOTE=1`, `METADATA=1`, `LIMIT=1` (`c2-count.py:9-21`), demonstrating these checks all pass while the round-60-specific admission requirement is not established.

## Impacted axes

- **Depth (claimed):** the evidence gate does not enforce the claimed source-to-note reasoning or prevent unsupported wording; a false PASS can admit ungrounded or unchanged material.
- **Calibration / discernment:** a counter verdict of PASS overstates what was verified, contrary to the frozen claim's explicit unknowns and base-fail criterion.
- **Operability:** `--root` does not fully isolate inputs, so a lane-copy invocation can silently read another checkout's source form.

## Smallest safe correction

Make the round-60 artifact identity explicit and mandatory: point `ENTRY` at the specifically named new round-60 note (or require a frozen round-60 marker/diff against the base), and inspect that note's exact observation and prohibited overreach against pinned S101 quote locations. Then execute the base fixture and require nonzero before accepting any target PASS. Derive `FORM` from the CLI `root` and pin/check its bytes within that same root, rather than consulting script-global `ROOT`. With the currently observed state, the safe verdict is **unprovable / do not admit C2** until a genuine new note passes that gate; do not repair the counter by weakening the predicate.
