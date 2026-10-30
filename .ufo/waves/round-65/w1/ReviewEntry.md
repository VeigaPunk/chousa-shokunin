# ReviewEntry — round65 C2 review (trailer)

Full report: .ufo/waves/round-65/w1/ReviewEntry/report.md

Scope: review C2 proposed assertions directly from source openings (no sibling draft used).
All three pinned sources reopened in-seat; sha256 recomputed and matching frozen
source-openings.json (S154 git-cat-file.1.gz, S155 /usr/lib/python3.14/hashlib.py,
S156 round64 c1v3-before-full.txt). Lane HEAD confirmed at freeze f99de3bdf.

Verdict recommendation: C2's proposed assertions are admissible as scoped, quote-grounded
consistency/identity distinctions; no authenticity or entailment claim is admitted.

Admit candidates (with reasons): A1 object-content selection via `git cat-file blob
<rev>:<path>` (quote exact at OUTPUT section, line 505; ref line 21 confirms; "not working
tree" admitted only as labeled inference); A2 SHA256 binds digest to selected blob bytes
under the hash assumption, identifies no actor (hashlib.py:31–34 exact); A3 round64 before
receipt lacks self-contained REVISION/EXIT/SHA256 headers, provenance lives in round64
claims (line 1, BATTERY=FAIL tail, empty header grep all verified); A4 revision identity /
content digest / reported exit are distinct propositions, validator exit0 is consistency
only (synthesis of A1–A3 + ref exit semantics).

Reject candidates (overreach refusals): R1 structural 10/10 counter establishes truth or
entailment — refused (substring/index checks; boilerplate passes); R2 S156 proves the round64
receipt had no provenance — refused (only in-file header absence is shown); R3 cat-file
output authentic/trustworthy — refused (man page silent on trust; CAVEATS cover disk-size
reporting only); R4 round65 format proves execution authenticity — refused by construction
(body never hashed; replay with fabricated output passes); R5 hashlib digest provides
provenance — refused (bytes→digest contract only).

Isolated probe (informational, one run): c2-count.py → ENTRY_CHECKS=10/10 C2=PASS exit 0 on
current tree. Canonical verification remains L1's after integration.

Gaps: A1's working-tree exclusion rests on Git object-model background, not the quoted
sentence (entry labels it Inference — accepted with label); replace-refs/alternates not
verified against gitrevisions(7); S156 header-absence verified by pattern grep, not a frozen
shape oracle. No tool installs. Scratch /fast/scratch/hyaku/chousa-r65/ReviewEntry deleted.
