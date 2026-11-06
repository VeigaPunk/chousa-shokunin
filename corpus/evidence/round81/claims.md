# Round 81 — frozen claims (fresh start)

Base (round-80 lane tip, closed `rejected-honest-stop`): `378fda82dc2cbcc555a0565052cc408121813cef`.
Prefreeze controls commit (precedes this file): `f7929f877e6fd54f4dc5ce7f993da46bc7df43f9`.
This file is frozen at its own commit. Nothing below is amended after any seat scores; a rule changed later is not
this round's rule.

## Fresh-start reads (run-15 Amendment 46)

Read before declaring: MANIFEST closure rows 1288 (r78), 1294 (r79), 1314 (r80) and
`corpus/lessons/round-78-verifier-spotcheck.md`, `round-79-verifier-spotcheck.md`, `round-80-verifier-spotcheck.md`.
Root failures: r78 — the battery's answer key was reachable by a normalizer that scores nothing (kill rule fired);
r79 — a payload-decoding forger identified every subject; r80 — the drawn-set predicate was draw-dependent
(`r80a-after-v7-run1.txt:216` FAIL vs PASS draws) and the grounding counter passed a planted record it never opened.
Common cause: ten rounds spent hardening the lane's own forger batteries, each frozen predicate falsified by the next
forger, with depth/coverage/freshness/adjacency `unchanged` throughout. This round leaves that surface and declares
claims on domain ground, each with committed do-nothing and forgery controls run through the frozen counter before
any candidate data exists.

## C1 — depth (sourced): two knowledge entries on research-method ground the lane does not hold

Surface moved: `corpus/knowledge/` (entry set; 92 files at base). Topics: citation searching per the TARCiS statement
(S203, S204), and correction/retraction status of a cited work before reuse (S205, S206, S207). No base entry names
TARCiS; no base entry is about erratum/retraction linking.

**Predicate (one sentence, same as the counter's exit-0 condition):** at the landing revision,
`python3 -B corpus/evidence/round81/depth-r81.py --root <tree of that revision>` prints `DEPTH_R81=PASS` and exits 0,
i.e. at least two `corpus/knowledge/*-r81.md` entries each cite >= 2 rows opened 2026-11-06 (status `mined`, used-by
naming the entry), carry >= 3 quote lines all located verbatim (whitespace-collapsed, <= 25 words) in that row's
capture whose sha256 matches its 2026-11-06 `refetch.tsv` success row, cite >= 2 distinct such rows, carry a Markdown
table with >= 3 body rows, and share no located quote or bytes with each other.

Counting command (lane root; scratch per §7):
`D=$(mktemp -d -p /fast/scratch/hyaku) && git archive <rev> | tar -x -C "$D" && python3 -B corpus/evidence/round81/depth-r81.py --root "$D"; rm -rf "$D"`

Before (control receipts, base tree): `controls/c1-k0-donothing.txt` — `DEPTH_R81 entries=0 fresh_rows=0
located_quotes=0`, `DEPTH_R81=FAIL`, rc=1. Target after: `DEPTH_R81=PASS`, rc=0, entries >= 2.

Forgery controls (all rc=1 as expected, `controls/`): f1 unregistered id (`P2-quote-cites-non-fresh-S999`), f2 one
word altered (`P2-absent`), f3 row opened on another date (`P1-fresh-rows=0`), f4 duplicated entry
(`P4-duplicate-bytes`), f5 capture bytes not matching their fetch record (`P2-no-fetch-record`), f6 no table
(`P3-no-table`), f7 overlong quote (`P2-quote-words=48`). Positive control `c1-pos-two-entries.txt` rc=0 (two control
entries on control rows S901–S904) — the counter can pass.

**Kill rules (fire → honest stop, never a narrowed target):** (K1) the counting command at the landing revision prints
anything but `DEPTH_R81=PASS` rc 0; (K2) a live re-open of any counted quote (`tools/quote-reopen.py verify` for the
HTML rows; one curl GET plus `pdftotext` for S203) reports `ABSENT` — the capture is then not what the URL serves
(`UNREACHABLE` is recorded, not fired); (K3) a non-author or attack seat shows a counted entry asserting, in a decision
table row, something its cited located quote contradicts.

Stated limits: the counter trusts committed capture bytes and their fetch record (K2 is the check on them); it measures
grounding and form, not whether the decision table is wise — that is the reviewer's and the closure's judgment.

## C2 — operability (lowest scored non-retired axis, historical 3/10): the executable checklist runs

Surface moved: `SKILL.md` `## Checklist (executable)`. At base, items 2 (negative claim carries its sweep), 4 (rejected
source keeps reason and flip-condition) and 5 (every web quote re-opened) carry no `Run:` line — AXES.md operability:
"A checklist item can be run and produces the stated outcome".

**Predicate:** at the landing revision,
`python3 -B corpus/evidence/round81/checklist-run.py --root <tree of that revision>` prints
`CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` and `CHECKLIST=PASS` and exits 0 — every one of the six items carries a Run line,
and the Run lines of items 2, 4 and 5 produce their stated outcome on the frozen fixtures
(`checklist-fixtures/`: item 2 and item 4 pass/fail pairs differing in exactly one defect; item 5 an unregistered id).

Before: `controls/c2-k0-donothing.txt` — `CHECKLIST_RUN=3/6 DISCRIMINATE=0/3`, `CHECKLIST=FAIL`, rc=1.
Target after: `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3`, rc=0.

Forgery controls (`controls/`): g1 `true <record.md>` lines (6/6 runnable, `DISCRIMINATE=0/3`, rc=1); g2 `… || true`
(`1/3`, rc=1); g3 no placeholder (`1/3`, rc=1); g4 an item deleted (denominator refused, rc=2); g5 the wrong gate mode
`verify-chain` (`1/3`, rc=1). Positive `c2-pos-candidate.txt` rc=0 on `controls/c2-candidate-SKILL.md`.

**Kill rules:** (K1) the counting command at the landing revision prints anything but the predicate line rc 0;
(K2) an attack seat builds a record carrying exactly the item-2 or item-4 defect in a form the item text names (a
negative claim with no named location; a kept rejection with no flip-condition) on which the landed Run command exits
0 — the Run line then does not produce the stated outcome.

Stated limit (before data): item 5's leg is a fail leg only (its pass leg needs a live fetch); items 1, 3, 6 are counted
from their Run line only.

## Sourced claim (§2b.4)

C1 rests on rows S203–S207, each opened this round (refetch.tsv 2026-11-06T18:44Z). S208 (the TARCiS erratum, BMJ
2024;387:q2458) answered HTTP 403 and lands as a rejected row with its flip condition.

## Instruments (sha256 at the prefreeze controls commit)

- `depth-r81.py` `10c989c0a59f94d88e03b0972378fd178bc6ee62e55bb580998751c3f2daa1e9`
- `checklist-run.py` `66ca8c97c597f4b4b538322654e98f1ca83ebdde3b5d44c2b5d0bd63f295bbc2`
- `run-controls.sh` `c1942bb92fc4901efcc8e82a8679c1d776fc0061f012c39afd4ea331f27ea65c`
- fixtures: item2-pass `d9f1aa51…`, item2-fail `5f9b89d1…`, item4-pass `64183e47…`, item4-fail `b7a45309…`, item5-fail `bf53d570…`

Causal separability: C1 is verifiable with SKILL.md untouched; C2 with `corpus/knowledge/` untouched.
