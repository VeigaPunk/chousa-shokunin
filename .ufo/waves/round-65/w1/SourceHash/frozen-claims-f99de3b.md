# Round65 frozen claims — 2026-10-30

Base master d6ed8155e9b4735639a2cf0a3e479c62f2056195. No wave seat has scored this round. The L1 considered but did not declare the round64 battery/mutation continuation: those require independently validated oracles first. Exactly two claims follow; the preliminary uncommitted planning does not freeze any others.

## C1 — operability (lowest numeric axis, historical 3/10)

Acquire a receipt-header consistency validator at tools/receipt-pin.py. Predicate R65-C1: CASES=20/20 C1=PASS iff all frozen receipt-consistency cases match their exact exit and token.
Counter: python3 corpus/evidence/round65/c1-count.py --work <fresh-dir>.
Before controls/c1-before.txt: absent target, CASES=0/20 exit1. Positive controls/c1-positive.txt:20/20 exit0. Always-pass 3/20 and always-fail 17/20, both exit1. Target 20/20 exit0. The reference is available prefreeze and is not a hidden answer. This is interface/consistency coverage, not a claim to cryptographic execution authentication or general parser safety. Numeric score remains historical 3/10.
Format: exactly ordered REVISION full lowercase 40 hex, EXIT decimal 0..255, SHA256 full lowercase 64 hex plus canonical relative POSIX path, empty separator, nonempty output. Digest binds the Git blob at the declared revision; revision must equal caller-supplied --revision. No working-tree hashing. 0 consistent,1 invalid,2 usage/environment. No changes to old frozen counters.

## C2 — depth, sourced

A knowledge entry corpus/knowledge/receipt-identity-r65.md distinguishes object identity, content digest, reported exit and execution authenticity. Sources opened this round: installed git-cat-file(1), /usr/lib/python3.14/hashlib.py, and round64's before receipt (S154–S156); the lesson records quotes and source limitations. Predicate R65-C2: ENTRY_CHECKS=10/10 C2=PASS iff the ten structural sourced-entry checks in c2-count.py hold. Counter python3 corpus/evidence/round65/c2-count.py. Before ENTRY_CHECKS=0/10 exit1; target10/10 exit0. This structural counter cannot establish entailment; source/claim reviews remain separate. Do-nothing (no entry, no rows) is the before control and fails. A boilerplate entry could pass; no semantic-quality claim rests on this counter alone.

## Freeze and kill rule

Counters, predicate, denominator and target remain unchanged after this freeze. A missed target is unprovable/not admitted, not rewritten. Wave seats return independent drafts/attacks; only L1 integrates and commits. Round64's minor registry/provenance items are supporting corrections, not additional claims. Source census start exit0,153 rows; lane .ufo/waves/round-65/census-start.txt.
