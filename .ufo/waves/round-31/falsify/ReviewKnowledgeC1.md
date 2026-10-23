# ReviewKnowledgeC1 — falsify `corpus/knowledge/line-binding-r31.md` (round 31, WAVE 2)

Verified against lane tip ee1024fd (clone `/fast/scratch/hyaku/chousa-r31/w2/ReviewKnowledgeC1/clone`, checked out ee1024fd, GIT_* env unset). Gate behavior exercised by running `bash clone/tools/research-gate.sh verify-claims root/claims.jsonl --root root` (20-claim matrix, docs/s1.txt + CRLF s2.txt). No tools installed (none needed). No network used; S057 checked against the frozen L1 local copy `/fast/scratch/hyaku/chousa-r31/rfc5147.txt` (37422 bytes, SHA-256 `c8fff6f2…24f4` — matches the L1 receipt in `corpus/lessons/round-31.md:53`).

## Confirmed by execution (all hold)

- L13–18 contract vs gate: all 10 invalid forms tested — `"0"`, `"04"`, `"3,5"` (RFC style), `"3 5"`, `"4-4"`, `"9-3"`, `"3-"`, `"3-04"`, JSON number `3`, `""` → `observed=invalid`, `FINDING CLAIM_RECORD_INVALID severity=warn surface=claims`, exit 1. Matches gate regex `^[1-9][0-9]*$` / `^([1-9][0-9]*)-([1-9][0-9]*)$` with M>N (`tools/research-gate.sh:1483-1500`).
- L20 (worked examples 1–3, reproduced exactly on lines 3/9/4/8/20/21): later occurrence binds (`"line":"9"` → supported, `at=line:9`); no line → `at=line:3` (first only); glued copy on named line → mislocated (`first_delimited_occurrence=line:3`); `"20"` mislocated / `"20-21"` supported `at=lines:20-21`; line 99 past EOF → mislocated; span absent + line → `unsupported`, no CLAIM_LINE_MISMATCH; bound retains verdict (expect=unsupported → supported + CLAIM_SPAN_UNEXPECTED); CRLF file counted by newlines (`"line":"2"` binds); unknown key `"foo"` ignored. Finding text matches verbatim: `FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=<id> …`.
- L22 RFC conversion CORRECT: §2.2.3 quote verbatim (RFC lines 413–415); §5 example states `line=10,20` "identifies lines 11 to 20", so `line=3,5` → gate lines 4–5 = `"line":"4-5"`, as written.
- L3–5 header: verify-metadata CLEAN — `META entry=line-binding-r31.md source=present verified_at=dated recheck=scheduled verdict=clean`, `METADATA_COMPLETE=1/1`, exit 0. All four cited knowledge files exist; r24:11 defines state (3) "the source states (or contradicts) the claim at a named anchor" as cited on L34.
- L38 Result: fresh seed 77123 run `python3 corpus/evidence/round31/c1-count.py --seed 77123 --receipt …/ReviewKnowledgeC1/c1-receipt-seed77123.json` → `LINE_BINDING_MATCH=120/120`, receipt `matched=120 total=120 predicate_holds=true`, `counter_sha256=c3aca35da30e…`.

## Findings

1. **MEDIUM — L4 and L38: dangling citation "SCORECARD.md, section 'Round 31'".** At tip ee1024fd, SCORECARD.md contains no such section (`grep -c LINE_BINDING_MATCH` → 0; only `## Planned — round 31 (not started)` at SCORECARD.md:1730, listing unrelated pre-pivot candidate ideas). The measured result lives only in `.ufo/waves/round-31/measure/` and falsify receipts. Two lines point readers to a section that does not exist in the landed tree.
2. **LOW — L40–41: Limits list does not mirror claims.md "Not claimed" v2 tail.** Missing: "that the first occurrence is the cited one" (substance covered in L20) and "(v2) sha256 optional / absence is not drift" (C2-scoped, but the list already includes the C2 item "git-revision binding"). Header claims to be the claims.md list.
3. **INFO — L20: finding quote pins `severity=warn`; frozen v2 contract says `severity=warn|crit`.** The landed gate emits warn only (single emit site, `tools/research-gate.sh:1564`), so the file is accurate to behavior, just narrower than the contract wording.

## Verdict

**holds.** Every behavioral statement about the landed gate verified by execution (20/20 matrix rows agree with the file); RFC 5147 conversion correct; metadata header passes verify-metadata. One citation defect (F1) and one completeness nit (F2) to fix in the entry — none touch the gate, counter, or P1.

## Residual risk / gaps

Contradicted+marker interaction with `"line"` not executed (state-3 path untested here). S057 not re-fetched over the network; checked against the frozen local copy whose size/SHA match the L1's opened-bytes record (permitted: "most seats need no network"). Huge line values (>2^63) only reasoned from code (string compare; `[[ $l1 -eq $l2 ]]` operates on gate-internal values, not the claim field).
