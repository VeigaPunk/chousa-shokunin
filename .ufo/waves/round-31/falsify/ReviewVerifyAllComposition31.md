# ReviewVerifyAllComposition31
- Axes attacked: coverage (C1 line binding) and operability (C2 source pin).
- On tip `ee1024f` (`gate_sha256=c23d7537…`), `bash "$d/tools/research-gate.sh" verify-all record.md --claims claims.jsonl --json manifest-mixed-clean.jsonl --root .` (timeout 1200s, rc=1): claims verdict DRIFT, findings/drift=2/2; BND supported, MIS mislocated (`CLAIM_LINE_MISMATCH`), STL stale (`CLAIM_SOURCE_REVISION_MISMATCH`), native `1/3`; all other sections CLEAN.
- Manifest parsed as one JSONL object; claims tallies were `claims=3 supported=1 contradicted=0 unsupported=0 mismatched=2 unproven=0 refused=0 invalid=0 findings=2 drift=2`; no `mislocated`/`stale` tally keys; overall DRIFT with one drift section.
- No-new-field input on tip and base `be7b8d8` both returned rc=0; claims tallies matched exactly (`3` supported, other counters `0`), and manifest shape matched (expected `gate_sha256` value differs).
- Verdict: holds for coverage/operability composition; no actionable defect observed.
- Limits: LSP device unavailable (`xd://lsp` not mounted); no tools installed or network used.
