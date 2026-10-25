# Attack31 — C1 fixture semantics

**Scope:** probe the proposed R48 correct-bullet precision set and its operational meaning. No production edits; all scratch removed. No network or installs.

## Evidence and measured behavior

The proposal is implemented as `corpus/evidence/round48/precision-count.py:11-23,39-52`: twelve hard-coded bodies (p01–p06, a01–a06), generated as one inference bullet each with fixed quote/source. It counts only return code 0 as pass. SCORECARD plan (`SCORECARD.md:2531-2534`) describes held-out correct bullets and conflicting-polarity spans; this script contains only correct-bullet cases, not a conflicting-polarity/flip control.

Commands run from lane root:

- `python3 corpus/evidence/round48/precision-count.py` → p01 PASS, p02 PASS, p03 REFUSED, p04 REFUSED, p05 PASS, p06 PASS; a01 PASS, a02 PASS, a03 PASS, a04 PASS, a05 REFUSED, a06 PASS; `CORRECT_BULLETS_PASS=9/12`, exit 1.
- `python3 corpus/evidence/round48/precision-count.py --tool /tmp/chousa-r48-Attack31/tools/acceptall.py` where control unconditionally exits 0 → all twelve PASS; `CORRECT_BULLETS_PASS=12/12`, exit 0. Thus this counter, considered alone, awards the maximum score to a tool that never rejects any polarity flip: unsafe acceptance / inadequate specificity.
- Same command with an unconditional exit-1 control → all twelve REFUSED; `CORRECT_BULLETS_PASS=0/12`, exit 1. Reject-all is detected; accept-all is not.
- `python3 -c` importing `tools/inference-ground.py` and checking its helpers observed `is_neg('nonexistent') == False`, `is_neg('cannot') == True`, `is_neg('unrecorded') == True`; this confirms the listed lexical distinction, not a semantic parser.

The nine correct accepts and three refusals reproduce HeldOutA's stated result and classes (`.ufo/waves/round-47/w2/HeldOutA.md:12-17,29-35`): p03 uses unlisted `nonexistent`; p04 puts `cannot` beyond the three-word look-back; a05's `not` is close to the quoted phrase's `build` stem even though it denies a different build-date proposition. These are false refusals given the supplied case rationales. The current tool documents a fixed window and lexical limits (`tools/inference-ground.py:59-62,317-347`); these examples are therefore observed boundary behavior, not proof of general semantic interpretation.

## Scope/control attack

R47 already demonstrates why precision and flip sensitivity must be paired: the frozen C1 count is 3/3 positives and 3/3 junks, but HeldOutB measured only 4/12 natural flips killed (`corpus/lessons/round-47.md:145-149`; details `.ufo/waves/round-47/w2/HeldOutB.md:16-46`). The R48 precision script's 12 correct cases are not a substitute for a negative control leg. An accept-all tool earns 12/12 on this gate; if the precision count is treated as evidence of overall C1 operability or false-refusal correction, that inference is unsafe. It is only a correct-case pass count.

The current corpus gives grounded control material: S901 span is `the release ships a frozen pool of pages; no revision is recorded per sentence`; S902 is `the archived copy is dated at build time; a placeholder value is not an archive link` (`corpus/fixtures/inference-ground-r47/spans/S901-1.txt`, `S902-1.txt`). Existing counterexamples are `junk-flip-asserted.md`, `junk-flip-denied.md`, `junk-flip-figure.md`; `c1-count.py:15-18,37-46,77-79` requires the flip finding as well as exit 1. Those controls must remain separately scored if a combined C1 acceptance predicate is proposed.

## Verdict and limits

**Observed:** current tool refuses 3/12 of the listed correct bullets; unconditional accept scores 12/12 on the precision gate, while unconditional refuse scores 0/12. **Unsafe acceptance:** precision gate alone permits no-op acceptance and does not establish flip detection. **Unsafe rejection:** p03, p04, a05 are concrete correct-case false refusals. **Not established:** whether these twelve examples are a representative/independent held-out sample; they are embedded in the counter source and use fixed spans, quotes, and source IDs. Do not describe their count as a population false-refusal rate without a defined sampling frame. A complete combined claim needs separately retained polarity-flip controls, the measured precision result, and explicit treatment of correct-vs-flip cases; no new predicate is frozen here.

Commands/evidence above are local only. `rm -rf /tmp/chousa-r48-Attack31` executed; report is the only lane write.
