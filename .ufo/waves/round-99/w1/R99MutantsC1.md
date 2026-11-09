# R99MutantsC1 — mutation test of the C1 change (seat R99MutantsC1)

F = `d41f4cd8b857c6de683e7be5c5e8125b32763a8e` (shared clone at $S/repo), BASE = `47ed34fa785288837f84cde9db15c41300854a78`.
Testee F tool sha256 `e92c4526d5fca2f12d9fd05838ce2af52fe761f8a507a5465b28fd196fb4b3c1`,
base tool `905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60`,
battery `6f354228607e6170798fad4004342398de6666d244e948e140f2718b58d0a5c1`.
Detector: `python3 -B corpus/evidence/round99/challenge-controls-r99.py --root $S/repo --work $S/w/<id> --tool <mutant> --no-oracles` (oracles are patches of the F tool, so they cannot be applied to mutants). `--no-oracles` drops ORACLES_REJECTED=0/0. Baseline on F: PASS exit 0, on base `NEG_REFUSED=0/7` FAIL exit 1 (receipts R99MutantsC1-baseline-f.txt, R99MutantsC1-baseline-base.txt).

KILLED = battery FAIL (exit 1), SURVIVED = battery PASS (exit 0). 28 one-site tool mutants, each applied exactly once (count asserted in generator).

## Tool-mutant table (28)

| id | mutation | battery tally line | verdict |
|---|---|---|---|
| m01-drop-cookies-must | drop `"cookies must be enabled",` | NEG=6/7 PROD=3/4 | KILLED |
| m02-drop-checking-you | drop `"checking your browser",` | 7/7 4/4 4/4 | SURVIVED |
| m03-drop-recaptcha | drop `"recaptcha",` | 7/7 4/4 4/4 | SURVIVED |
| m04-drop-client-chall | drop `"client challenge",` | 7/7 4/4 4/4 | SURVIVED |
| m05-drop-a-required-p | drop `"a required part … couldn't load",` | 7/7 4/4 4/4 | SURVIVED |
| m06-drop-just-a-momen | drop `"just a moment",` | 7/7 4/4 4/4 | SURVIVED |
| m07-drop-verify-you-a | drop `"verify you are human",` | NEG=6/7 | KILLED |
| m08-drop-enable-javas | drop `"enable javascript and cookies to continue",` | 7/7 4/4 4/4 | SURVIVED |
| m09-drop-attention-re | drop `"attention required",` | NEG=6/7 | KILLED |
| m10-drop-ddos-protect | drop `"ddos protection",` | 7/7 4/4 4/4 | SURVIVED |
| m11-drop-are-you-a-ro | drop `"are you a robot",` | 7/7 4/4 4/4 | SURVIVED |
| m12-le-to-lt | `<=`→`<` | 7/7 4/4 4/4 | SURVIVED |
| m13-max-199 | 200→199 | 7/7 4/4 4/4 | SURVIVED |
| m14-max-201 | 200→201 | 7/7 4/4 4/4 | SURVIVED |
| m15-max-1000 | 200→1000 | POS=3/4 | KILLED |
| m16-no-norm-challenge | drop `norm(` inside is_challenge | 7/7 4/4 4/4 | SURVIVED |
| m17-no-lower | drop `.lower()` | NEG=0/7 PROD=0/4 | KILLED |
| m18-any-to-all | `any(`→`all(` | NEG=0/7 PROD=0/4 | KILLED |
| m19-and-to-or | `and`→`or` | POS=2/4 HARM=23/25 | KILLED |
| m20-no-admit-call | delete admit-branch `is_challenge` call | NEG=0/7 PROD=2/4 | KILLED |
| m21-no-rev-call | delete rev-branch call | PROD=2/4 | KILLED |
| m22-cap-noop-rev | `CAP_RE.fullmatch(...) and` → `True and` in rev branch | 7/7 4/4 4/4 | SURVIVED |
| m23-challenge-only-when-quote-absent | CHALLENGE only when quote absent, admit branch | NEG=0/7 PROD=2/4 | KILLED |
| m24-rev-challenge-only-when-line-bad | rev CHALLENGE only when LINE fails | PROD=2/4 | KILLED |
| m26-case-fold-swap | `.lower()`→`.casefold()` | 7/7 4/4 4/4 | SURVIVED |
| m27-first-marker-only | `any(m in t …)`→`CHALLENGE_MARKERS[0] in t` | NEG=1/7 PROD=1/4 | KILLED |
| m28-slice-first-5-markers | `CHALLENGE_MARKERS[:5]` | NEG=4/7 | KILLED |
| m29-negated-length | `<=`→`>=` | NEG=0/7 POS=3/4 PROD=0/4 | KILLED |

Killed 15 / survived 13. Full outputs: R99MutantsC1-t-m*.txt.

## Survivor classification (equivalent vs uncovered; C1-clause impact)

Post-norm marker presence on the fixtures (receipt R99MutantsC1-probes.txt):
S230 (23w): checking-your-browser + recaptcha; S229 (18w): cookies; S234 (37w): client-challenge + a-required-part (the latter only after norm collapses the capture's internal newline — raw-lowered S234 hits only client-challenge).
CF (28w): just-a-moment + enable-javascript; TURN (21w): verify-you-are-human; ATTN (33w): attention-required; ARTICLE (381w): recaptcha + just-a-moment; SHORT (28w): none.

- **m02, m03 (drop checking/recaptcha): UNCOVERED, not equivalent.** S230 carries both markers and n7 is S230 upper-cased, so either single drop is masked. Dropping both would kill the battery. Clauses at risk: the "11 frozen markers" sentence — see overall verdict below.
- **m04 (drop client-challenge): UNCOVERED.** S234 also carries a-required-part post-norm, so n3/PROD survive on the second marker. A short page carrying only client-challenge (e.g. no sentence 2) would be admitted by the mutant but refused by F. So the battery does NOT show client-challenge is live.
- **m05 (drop a-required-part): UNCOVERED.** No fixture carries it alone; S234's second marker masks. Same clause as m04.
- **m06, m08 (drop just-a-moment / enable-javascript): UNCOVERED.** CF carries both; each masks the other.
- **m10, m11 (drop ddos-protection / are-you-a-robot): UNCOVERED, no fixture hits them at all.** No NEG fixture contains either; a page carrying only one would pass the mutant and fail F. Dead-by-battery markers.
- **m12 (`<=`→`<`), m13 (199), m14 (201): FIXTURE-EQUIVALENT, boundary untested.** NEG word counts are 18–37, POS p3 is 381 and p1/p2 are 307–8455, so no fixture sits at 199/200/201. Direct probe on F: 200w page with marker → `is_challenge=True`, 201w → False (P2/P5 in probes). So the boundary is correct in F but the battery never tests it — a tool that refused `<=199` or `<=201` would still print PASS. Does not make the C1 sentence false (the "at most 200 words" wording is correct for F), but the battery does not enforce it.
- **m16 (drop norm inside is_challenge): UNCOVERED, provably non-equivalent.** Admit branch passes already-normed text (norm idempotent, P6), but the rev branch passes raw `"\n".join(lines)`. Probe: `"Release\nnotes.  Just   a   moment\nplease wait now"` → F True, m16 False; curly-apostrophe marker-5 text with doubled spacing → F True, m16 False (P3). Non-equivalent behaviour on the rev path, uncovered by the battery (its two rev fixtures have no intra-marker double spacing).
- **m22 (CAP_RE→True in rev branch): UNCOVERED, non-equivalent.** F gates rev-CHALLENGE on the path being a capture; m22 checks every rev blob. Divergence: a rev record on a non-capture short marker-carrying file — refused by m22, admitted by F. The battery's only rev fixtures are S230/S229 capture paths, so this is invisible. Does it falsify a C1 clause? The sentence says "a rev record whose path is `corpus/captures/<24 hex>.txt` fails" — F honours that, and does not claim non-capture rev paths are admitted. Named limit (d) does disclose "a rev record whose path is not under corpus/captures/ is not checked". So the mutant goes beyond (d)-disclosed behaviour, but the claim does not forbid it. Held, not fired, on this point.
- **m26 (lower→casefold): NOT equivalent, just uncovered on ASCII fixtures.** casefold turns ß into `ss`, so `"jußt a moment".casefold()` contains a marker where `.lower()` does not (P4). Equivalent on every fixture (all ASCII) but not equivalent in general. Named limit (c) discloses no NFKC (covers full-width/zero-width), but ß→ss is a casefold artefact, not NFKC — still, F's sentence says "lower-cased", so the claim is true for F.

## Battery-mutant table (8 mutants, run against F tool and base tool)

Batteries run as `python3 -B <bmutant> --root $S/repo --work $S/wb/<id>[-base]` (F run without `--no-oracles`, base run with `--tool base --no-oracles`). Outputs R99MutantsC1-b-*.txt.

| id | mutation | F tool | base tool | class |
|---|---|---|---|---|
| b1-neg-rc-only | NEG `good = rc==1 and v=="CHALLENGE"` → `rc==1` | PASS exit 0 | FAIL exit 1 | SURVIVING loosening |
| b2-pos-count-2 | final `ok` requires `posok==2` instead of `len(pos)` | FAIL exit 1 | FAIL exit 1 | tightening, fails F (POS=4/4 vs demanded 2) — correctly rejects an over-strict battery |
| b3-harm-stdout-only | HARM `eq=(rc,stdout)==` → `stdout==` | PASS exit 0 | FAIL exit 1 | SURVIVING loosening |
| b4-oracle-missing-rejected | missing oracle site counts as rejected | PASS exit 0 | FAIL exit 1 | SURVIVING loosening |
| b5-prod-2 | final `ok` requires `prodok==2` | FAIL exit 1 (ORACLES_REJECTED=4/5) | FAIL exit 1 | Over-strict on F; also weakens the oracle legs (o4 passes prodok=2 under the mutant, so ORACLES_REJECTED drops to 4/5 — detected only via that side effect) |
| b6-pos-rc-only | POS `good=rc==0 and v=="OK"` → `rc==0` | PASS exit 0 | FAIL exit 1 | SURVIVING loosening |
| b7-oracle-always-rejected | `rejected += 1` unconditionally | PASS exit 0 | FAIL exit 1 | SURVIVING loosening |
| b8-neg-verdict-ok-accepted | NEG accepts `v in (CHALLENGE,OK)` | PASS exit 0 | FAIL exit 1 | SURVIVING loosening (base still FAILs on PROD) |

Six of the eight battery mutants keep printing PASS for the F tool while printing FAIL for the base tool: the battery's kill-rule sensitivity is real (it catches the base tool even when loosened) but the strictness lives in a few comparisons — verdict-string equality (b1/b6/b8) and the oracle-rejection counter (b4/b7) and HARM rc inclusion (b3) — and loosening any one of them is invisible.

Concrete K-rule gaps:
- **b1/b8 vs K1** ("any NEG admitted, or failing with a code other than CHALLENGE alone"): under b1, a NEG record failing with QUOTE_ABSENT alone (rc=1) would print PASS. K1 is enforced by the string comparison `v == "CHALLENGE"`, which only works because the verdict parser returns the full code tail — loosening that one comparison opens K1.
- **b6 vs K2**: a POS record FAILing (rc≠0) is still caught by rc, but a POS record that prints OK-shell with a non-OK verdict line is not a real case (rc would still be 0). Harmless in practice; listed for completeness.
- **b3 vs K3**: I scanned base-vs-F on all 25 HARM files — stdout and rc both identical on every file today, so there is no live divergence the rc inclusion currently catches. But K3's wording ("stdout or exit code differs") is enforced only because `eq` includes rc; a future tool that changes rc but not stdout would pass under b3. The C1 claim's K3 is true of the battery as shipped.
- **b4/b7 vs K4**: a tool whose oracle patch site no longer applies (`SITE-MISSING`) is neither scored rejected — it is skipped and the run FAILs by shortfall only if the candidate is otherwise scored... actually b4 counting missing as rejected is the dangerous direction: a tool that removes/renames the oracle site would be counted as rejecting an oracle it never ran. As shipped (F tool → 5/5), b4 prints PASS; the gap is latent, triggered by a tool that changes the oracle strings.
- **b5**: lowering the PROD demand to 2 lets o4 (scratch-only) pass the oracle leg (ORACLES_REJECTED=4/5) — caught only because the full run also requires 5/5. The product of a weakened demand + a complete oracle set still fails, but for the wrong reason.

Restoration: nothing in the shared clone or the lane was mutated — all mutants were fresh files under scratch/bmutants; the F tool and battery in $S/repo were only read. No production files written. Scratch $S to be removed before yield.

## What does this do to the C1 sentence?

The sentence is true as a description of `is_challenge` (verified: 200w→True, 201w→False, lower-casing, marker set). The enforcement gaps are in the *battery*, not in F tool vs sentence — except one wording point: **no NEG fixture isolates the markers `"ddos protection"`, `"are you a robot"`, `"a required part of this site couldn't load"`, or `"client challenge"` (and `"checking your browser"`, `"recaptcha"`, `"just a moment"`, `"enable javascript and cookies to continue"` are only present in pairs). The sentence lists the check as "contains one of the 11 frozen CHALLENGE_MARKERS" — the battery shows 7 of the 11 do real work on at least one NEG/PROD case (cookies, verify, attention, and the pairs), and 4 do no isolated work. I judge this a coverage shortfall, not a false sentence: the sentence does not claim each marker is individually exercised, and named-limit (a)/(e) disclose the lexical limits and the five-patch oracle set. The verdict word is therefore *held* on C1 wording, with the uncovered-marker and boundary findings recorded — they falsify only a stronger reading ("the battery shows every marker is live"), which the claim does not make.

VERDICT: R99MutantsC1 C1 held — F tool matches the C1 sentence, but 13/28 one-site mutants survive (incl. all boundary/threshold and 8/11 marker drops) and 6/8 loosened batteries still print PASS for F while FAIL for base.
Report: .ufo/waves/round-99/w1/R99MutantsC1.md
