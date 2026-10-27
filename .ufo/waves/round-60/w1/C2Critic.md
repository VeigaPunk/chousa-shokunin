# C2Critic — counterexample against frozen C2

## Counterexample

The strongest available local counterexample is the base-state invocation: the existing `c2-count.py` exits successfully even though the frozen claim explicitly requires the base to fail because no round-60 entry exists.

```text
$ python3 corpus/evidence/round60/c2-count.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --work /fast/scratch/hyaku/chousa-r60/C2Critic/work
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
exit=0
```

Evidence: `corpus/evidence/round60-claims.md:15-18` requires an exact new-entry observation, boundedness against source, citation/metadata, scorecard disposition, and base failure. But `corpus/evidence/round60/c2-count.py:8,13` selects the already-existing `corpus/knowledge/citation-count-semantics-r37.md`; lines 17-18 check only generic metadata and two broad phrases. The target observation and round-specific identity are not asserted, nor is scorecard disposition checked. Thus an unchanged prior entry yields `PASS`, falsifying the critical base-fails predicate. This is not a semantic test of the proposed correction.

A second reproducible design weakness is root mixing: the CLI resolves raw capture and entry beneath `--root` (counter line 13), but `form` is fixed to the script checkout's `ROOT/.ufo/waves/round-60/s101-open.txt` (lines 7,13). A copied lane root therefore does not supply all tested inputs; its verdict can depend on another checkout's form. This violates the stated `<lane-copy>` isolation. `S101Reopen.md:12` independently describes the same path binding.

## Evidence and scope boundary

- The captured source text is locally pinned by `corpus/evidence/round57/refetch.tsv:66` to S101 URL `https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc`, capture id `6dc68fd6b32ce9c8dfcebce8`, SHA-256 `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3`. No live fetch was performed.
- Existing entry `corpus/knowledge/citation-count-semantics-r37.md:67-86` already contains the S101 selection/format discussion and explicit unknowns, including the quote limit. Presence of a quote at rendered form line 245 (`c2-count.py` output) proves neither a new correction note nor that note's no-overreach property.
- `S101Reopen.md:9-13` reports the bounded offline observations and historic capture linkage. It explicitly does not establish present-day validity, authenticity at origin, or CNKI implementation. Those are not supported conclusions.
- Freeze integrity discrepancy: assignment supplies expected SHA `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440`; local `sha256sum corpus/evidence/round60-claims.md` observed `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1`. File was not modified. Cause/timing cannot be determined from available evidence.

## Impacted axes

- **Depth (claimed):** no enforced correspondence from the new claim's exact source-grounded observation to a new note; overreach is not actually tested.
- **Calibration / discernment:** false `PASS` overstates what was verified and contradicts the explicit base-fails condition.
- **Operability:** `--root` is not a closed input boundary because the text form is loaded from the script checkout.

These are defects in the C2 verification predicate, not evidence that S101's offline capture is false. The canonical judge should reject admission if the required counter result is trusted as written; the underlying knowledge claim may still be useful if separately verified.

## Smallest safe correction

Bind `ENTRY` to the specifically named round-60 correction artifact (or an equivalent frozen round-60 identity/diff against the base); assert its exact observation and prohibited overreach against the pinned source spans; check the required declared disposition; and derive the text form from the same `--root`. Exercise the base fixture and require nonzero before a target result is considered. Until these gates and the actual note pass, report C2 as **unprovable / not admitted**, not PASS. Do not weaken the frozen predicate to accommodate the existing entry.

## Evidence boundary

Read-only examination of the frozen claim, local counter, existing cited entry, offline capture/rendering references, and prior lane evidence; one local counter invocation. No edits to lane/source material, no network access, no commit or git/jj mutation. Scratch was `/fast/scratch/hyaku/chousa-r60/C2Critic`.
