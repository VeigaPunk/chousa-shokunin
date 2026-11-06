# R82ReviewerGate — round 82, C1 gate-change review (scoped findings)

Diff reviewed: `57c0d16..b4a41d2 -- tools/research-gate.sh SKILL.md` (170+/12−). Full detail, commands and evidence: `.ufo/waves/round-82/w1/R82ReviewerGate/review.md`; every cited command output is a receipt file under `.ufo/waves/round-82/w1/R82ReviewerGate/receipts/` (record bytes under `receipts/records/`).

## Defects by severity

**F1 CRITICAL — C1 K2 firing.** Duplicate `##` headings: `load_sections` resets `SEC_BODY[$sec]` on every heading, so the first block's rows vanish for the structure check, the rejection loop and the new negative-resolution map alike.
- `r-dup-rejections.md` (empty-flip R1 in first `## Rejections`): landed item-4 Run line exits 0, `REJECTIONS_OK=1/1` CLEAN → in-class K2(b) record passes (receipts/r-dup-rejections.post.txt).
- `r-dup-claims.md` (negative N1, sweep `SW9` undeclared, in first `## Claims`): landed item-2 Run line exits 0 → in-class K2(c) record passes (receipts/r-dup-claims.post.txt, positive-controls.txt).
- Pre-existing parser behavior, but K2 is frozen over landing-revision behavior → fires. Fix direction: concatenate same-name bodies or refuse duplicate headings.

**F2 HIGH — C1 K3 firing.** `where=n/a,lib/x.md` (whitespace-free comma set): base 5d792e1e Run line exits 0 (verified, CLEAN); landed refuses `SWEEP_LOCATION_ABSENT unclassifiable location naming`, exit 1. The cell is not a declared-vocabulary value, so no K2 form applies → harm. Cause: comma-branch keeps junk tokens (gate:2758-2768) + `have_junk` invalidates the whole sweep; whitespace-sensitive (`n/a, lib/x.md` passes). Receipts: r-where-mixed.runline-base5d792e1e.txt / .post.txt.

**F3 MEDIUM — C1 K3 firing (per the frozen letter).** Negative claim whose sweep is carried by a `## Negatives` row (id = claim id, real `where`) is refused (`SWEEP_NEGATIVE_UNRESOLVED`) whenever a `## Sweeps` section also has rows; base passes. K2(c)'s own parenthetical "(and no `## Negatives` sweep row carries it)" puts this out of class. Cause: Negatives rows join `SWEEP_ROWS` only when Sweeps has zero rows (gate:2938-2945), so `SW_IDS`/`SW_CLAIMS` never see the carrier. Caveat recorded: if the lane reads "carries it" narrowly, this becomes a class-boundary decision — behavior observed is exact either way. Receipts: r-mixed-negatives.*.

**F4 MEDIUM — over-broad reject-heading match (in-class per letter; blast-radius flag).** A differently-schemed table under any heading containing "reject" (`## Rejected claims` with claim/status columns) is parsed as a rejections table and refused (`missing=reason,flip section=Rejected claims`, exit 1; base exit 0). Claimed by K2(b)'s letter; a column-schema guard or narrower heading match would shrink it. Also: `## Rejections` + `## REJECTIONS` are both matched → same rows counted twice. Receipts: r-rejected-claims-schema.*.

**F5 LOW.** Exact-case id matching refuses `sw1` vs `SW1` (consistent with verify's exact-case claim_id matcher; in-class per letter). Header/SKILL wording "a sweep row this mode re-ran" is loose: an exempt sweep row (e.g. `blocked-no-fetch`) resolves a claim without re-run (r-neg-exempt CLEAN both trees) — harmless direction. Unused `local w` in `sweep_is_placeholder` (gate:2697). `see_above`→`seeabove` is spec-faithful (vocabulary says "removing `_`"), do not "fix".

## Held clean

Locale C/C.UTF-8/en_US.UTF-8 identical on 16 probes incl. `—`/`–`/`…` (locale-matrix.txt); verify-all verdicts byte-identical pre/post on 16/16 sweeps/rejection fixtures (verifyall-fixtures.txt); `--json` schema unchanged (json-parity.txt, j-*.jsonl); manifest positives all CLEAN at landing (positive-controls.txt); the five new selftest cases are revert-sensitive (st1–st4 CLEAN/exit-0 at 57c0d16 while asserting rc=1 + new finding ids; st5 passes both) and landing selftest is `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)` rc=0; SKILL.md Run command spans byte-identical pre/post so the counter's FROZEN_RUNLINE check is unaffected; every new SKILL.md/header sentence verified against observed behavior.

## Kill-rule tally

- K2 fired: F1 (both receipts exit 0 on in-class forms at b4a41d2).
- K3 fired: F2, F3 (passed at 5d792e1e, refused at b4a41d2, no K2 form carried).
- K1/K4: no evidence against the predicate gathered (counter receipts belong to the counter seats); landing selftest satisfies K4's constraints.

Tooling: nothing installed or upgraded (bash/python3 sufficed). No network, no lane/fleet mutation; scratch `/fast/scratch/hyaku/chousa-r82/R82ReviewerGate` deleted before yield; the two permitted selftest runs were both spent on the landing tree (identical PASS).

VERDICT: R82ReviewerGate C1 fired — duplicate-##-heading records carrying K2(b)/(c) forms still pass the frozen Run lines at b4a41d2 (K2), and two K2-free shapes (a mixed `where` set containing a placeholder token; a Negatives-carried negative beside a non-empty `## Sweeps`) are newly refused (K3).
