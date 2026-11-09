# R100MutantsC2 — mutation test of the C2 instrument (`corpus/evidence/round100/entry-controls-r100.py`)

Attacked tree: shared clone at F `6d4e8487ee6a16823c24a8e085c6559b92b9fec8` under `/fast/scratch/hyaku/chousa-r100/R100MutantsC2/repo` (removed after run). Scratch SHA `650370b96fc2fddf9f3f250fe94a35154db4a13854f316755846bd620138b533` before AND after (receipts `R100MutantsC2-before-hash.txt` / `R100MutantsC2-after-hash.txt`; `git status` clean, rc=0). Pristine run: `ENTRY_CONTROLS_R100=PASS` rc=0 (receipt `R100MutantsC2-pristine.txt`). No network, no production edits, no other seat's files.

## Detector
Each mutant: one-site edit of a pristine copy, run `python3 -B corpus/evidence/round100/entry-controls-r100.py --root .` from the clone; KILLED iff output carries `ENTRY_CONTROLS_R100=FAIL` or `ENTRY_CONTROLS_SETUP` (exit 1/2), else SURVIVED (rc=0, PASS). Per-mutant receipts `R100MutantsC2-m*.txt` carry hashes + full output; summary `R100MutantsC2-mutant-summary.txt`.

## Mutants (24; 13 killed, 11 survived)
KILLED: m01 norm→identity, m02 NUM losing leading `-?` and `%`, m03 token-membership→substring of warrant text, m04 NUMBERS reading only Do cells, m06 FRESH not checking `## Update` content, m07 FRESH not checking `updates:` path, m13 base leg inverted, m17 QUOTES unbounded length, m18 WARRANTS blank-lane accepted, m20 norm without whitespace collapse, m24 numerals case-insensitive substring, plus m06/m07 fresh mutants.
SURVIVED (all printed the identical pristine PASS line with `FORGERY_REFUSED=13/13 ACCEPTED=2/2`):
- m05 NEVER accepting any cell (`nev_ok += True`) — the battery's own f12 (Never with a numeral) still refuses via NUMBERS, so NEVER=8/8 never binds on the pristine entry.
- m08 FIELD `in` instead of `==` for U0 (`norm(t) in norm(rec["title"])`) — no pristine quote is a proper substring of the title, so the check is equivalent on this entry but would admit a truncated title quote.
- m09/m10/m23 IDENTITY dropping pmcid, volume, or doi — removing a conjunct never fails while the capture is correct; IDENTITY only binds via forgery f8 (wrong pmid). A wrong-pmcid/wrong-volume capture would still pass IDENTITY=2/2.
- m11 TOPIC made case-insensitive / m12 TOPIC reduced to one phrase — TOPIC is a two-phrase substring probe (`46 studies`+`16.9%`); both weaker forms still hold on the pristine text.
- m14 forgery wrapper counting even non-applying replacements as refused (`bad = not passes(...)` without `changed and`) — all 13 built-in forgeries in fact apply (verified by import: f1–f13 all `changed`), so the mutant is equivalent on this battery but would inflate a vacuous forgery.
- m15 ACCEPT inverted (`ok = (t==text) or passes(...)`) — the two ACCEPT variants a1/a2 both pass anyway, so the inversion is invisible here.
- m16 `passes` accepting n==0 (`k==v` without `v>0`) — no leg is 0/0 on this entry, so invisible.
- m19 FIELD without the `s=="S238"` source check for U0 — U0's text equals the title either way.
- m21 QUOTES without the capture-field check (length-only) — QUOTES alone is field-blind by design; FIELD carries the field check, so this is a leg-independence observation, not a hole in the conjunction.
- m22 FRESH without the `updates:` file-existence check — the file exists in the clone, so invisible; a dangling `updates:` path would pass FRESH.

All 13 built-in forgeries verified to actually apply (`changed` for f1–f13) — no silent no-op among them here.

## Entry forgeries (7; `R100MutantsC2-entry-forgery-detail.txt`, gate receipts `R100MutantsC2-gate-g*.txt`)
Ran `score()`/`passes()` imports against the pristine entry and `tools/gate-records.py verify` (rc=0) on g1/g2/g5 files:
- g1 Do reversing its warrant with NO numeral ("no action is needed … solved" for row 8): controls PASS, gate PASS (`GATE_RECORDS files=1 records=17 ok=17 fail=0`). This is covered by C2 named limit (b)/(the entry's own Named limits para: "a paraphrase can still narrow or widen a quote's meaning … not checked") — the sentence only claims numerals are tokens, which holds.
- g2 number in the right form but the wrong sense ("25%" from U11's N=25 inserted as a rate): controls FAIL via NUMBERS 24/25, gate still PASS (gate checks locate-only). Refused by the instrument, as claimed.
- g3 U9 quote truncated to its prefix (still a located substring, dropping the slope clause the Do cites): controls FAIL via NUMBERS 19/24. Refused, as claimed.
- g4 `## Update` naming the entry + S238 but stating the opposite (rejected/superseded): controls PASS (FRESH is name-substring only). Covered by the entry's Named limits? The claims sentence says the Update "names the new entry and S238, so the stale 2015 reading is flagged" — naming is exactly what FRESH checks; an opposite-claiming section is a human-reading overreach, not an instrument falsehood. Noted as a coverage gap, not a falsification.
- g5 "one rater" for "two independent raters" (no numeral): controls PASS. Same paraphrase limit — the sentence claims numeral-token equality, which holds.
- g6 warrant swapped to an unrelated quote on a no-numeral row (row 5 Do "about half" now warranted by U13): controls PASS, because NUMBERS is empty (spelled-out quantity, named limit (b)) and WARRANTS only checks id-exists + non-blank Lane. Coverage gap for sense, within stated limits.
- g7 dropping `%` (`8.0%`→`8.0`): controls FAIL via NUMBERS 23/24 (form checked exactly). Refused, as claimed.

No forgery falsifies a C2 sentence as stated: every survivor falls inside named limit (b) ("numerals as tokens; spelled-out quantities and a paraphrase's sense are not checked") or the entry's own stated paraphrase limit, and every numeral-perturbing forgery is refused. The surviving mutants are component-weakness findings (IDENTITY/NEVER/TOPIC/FRESH-subchecks/forgery-wrapper/ACCEPT/`passes` vacuity) — detection requires a forgery that bites the weakened site, and the built-in battery bites most of them only through crossed legs (e.g. f12 via NUMBERS). None makes the frozen PASS line or the cited counts false on the pristine entry.

## Falsification check on C2 sentences
- "8 decision rows whose every Do/Never numeral is a token of that row's own warrant quotes" — holds on the pristine entry (NUMBERS=24/24, NEVER cells carry no numerals); g2/g7 show the instrument refuses form/sense-perturbed numerals.
- "14 located quotes (U0-U13) plus J1/J2 … `## Update` names the new entry and S238" — holds (QUOTES=16/16, FIELD=16/16, FRESH=1/1); g4 shows FRESH is a name check, which is exactly the claim's wording.
No C2 sentence was found false as stated. Findings are coverage/coverage-equivalence notes, not kill-rule hits under C2's own limits.

VERDICT: R100MutantsC2 C2 held — 13/24 instrument mutants killed, 11 survived without falsifying any C2 sentence (all survivors lie inside named limit (b) or are equivalent on the pristine entry), and numeral-perturbing entry forgeries remain refused; no falsification.
