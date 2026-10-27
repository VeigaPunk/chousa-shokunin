# C2QualityReviewer — bounded quality review

## Finding: critical false-positive admission gate

The current C2 counter passes the unchanged base state despite the frozen predicate requiring base failure because no round-60 entry exists. The independent local invocation recorded in `C2Critic.md:7-12` returned `C2=PASS`, exit 0, with `RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1`. The counter selects the pre-existing `corpus/knowledge/citation-count-semantics-r37.md` (`corpus/evidence/round60/c2-count.py:8,13`), and checks generic phrases rather than round-60 note identity or its exact bounded observation (`C2Critic.md:14`). This does not meet `corpus/evidence/round60-claims.md:15-18`'s required new-entry observation, no-overreach, metadata, disposition, and base-fail conditions. A PASS therefore cannot establish the claimed depth improvement; C2 is not admissible on this evidence.

## Additional defect: mixed-root inputs

The `--root` under test supplies the raw capture and entry, but the form is loaded from the script checkout's fixed `ROOT/.ufo/waves/round-60/s101-open.txt` (`C2CounterAudit.md:18`; independently reported in `C2Critic.md:16`). A copied lane root is consequently not an isolated test fixture; external workspace state can affect its verdict. This conflicts with the frozen `<lane-copy>` predicate.

## Quality boundary and disposition

The offline S101 evidence establishes only the bounded bibliographic type/carrier notation; it does not establish current validity or CNKI implementation (`C2Critic.md:20-22`; frozen claim line 15). The safe disposition is **unprovable / do not admit C2** until the counter requires the specific round-60 artifact and tests exact observation, prohibited overreach, metadata, declared disposition, and base failure using inputs all rooted in `--root`. Do not weaken the frozen predicate to accommodate the pre-existing entry.

## Freeze integrity note

The assignment-provided immutable claim SHA is `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; local `sha256sum` of the untouched frozen file returned `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. The file was not modified. The discrepancy's cause cannot be established from these observations; resolve freeze identity before treating the supplied digest as matching the available bytes.

Scope: report-only review of frozen C2 claim, current counter and prior local counterexample evidence. No external fetch or source/fleet writes; no commits or git/jj mutations. Scratch requirement: `/fast/scratch/hyaku/chousa-r60/C2QualityReviewer/`.