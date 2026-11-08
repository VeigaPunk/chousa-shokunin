# R91ReviewerC3 — C3 (freshness) wording-vs-code review

Seat `R91ReviewerC3`, lane chousa round 91. Frozen claim set at freeze **F3 `4d00d7519290569879f853d7122b82a927cda1f3`**,
tree attacked **carrier C3 `67954adc599bd605705d94a1ea7abb582491a907`**. `S=/fast/scratch/hyaku/chousa-r91/R91ReviewerC3`;
every clone/tree/fixture lived under `$S` and was deleted before yield. Nothing was written outside `$S` and
`.ufo/waves/round-91/w1/`; the lane was not edited; no network request was made; no tool was installed.

Clone: `git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo && git -C $S/repo checkout 67954adc599bd605705d94a1ea7abb582491a907`
(`rev-parse HEAD` = `67954adc…`). No LSP server is mounted in this session (`read xd://lsp` → `No such tool: xd://lsp`),
so caller/definition checks are literal reads plus executable reproducers — recorded as a verification gap, not
presented as semantic proof.

## Trees

- `$S/carrier` = `git -C $S/repo archive HEAD | tar -x -C $S/carrier` — C3 as committed: SKILL.md still carries the
  pre-round clause `r39 bash-pin cases 273–275 and r82 bash-pin-override cases 276–283`.
- `$S/landing` = the same archive plus the one-clause repair, exactly the sentence the control battery hard-codes as
  `OLD_CLAUSE`: `r39 bash-pin cases 273–275 (pin-bashenv, drift-bashenv) and r82 pin-override cases 276–283, of which
  bash-pin-override cases 282–283`. The lane's uncommitted SKILL.md is byte-identical (`cmp_exit=0`) and the
  worktree diff against C3 is `1 1 SKILL.md`.
- `$S/base` = archive of `265b8633b7e5d1da49da6fb948df9707373fb15c`; base SKILL.md == carrier SKILL.md
  (`git diff --numstat 265b8633..67954adc -- SKILL.md` is empty), so the carrier run is also a base run.
- Selftest receipt `corpus/evidence/round91/controls/selftest-r91.txt` was committed at the freeze and is untouched
  by C3 (`git diff --name-status 4d00d751..67954adc` names only the six `c1-*`/`c2-*` receipts); its sha256
  `9c29428160768524c77407eedd711200be53a1074e2a22fe9bab814ad3f5bb37` equals `instrument-pins.txt` line 8.

## Baseline — the landing predicate and controls reproduce exactly; the carrier does not

1. Carrier C3, C3 command:
   `cd $S/carrier && python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest corpus/evidence/round91/controls/selftest-r91.txt`
   → exit 1; `CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=276-283 derived=282-283`;
   `CASE_RANGE_FINDING MISLABELED=6 indices=276,277,278,279,280,281`;
   `CASE_RANGE_OK=1/2 MISLABELED=6 LEGS=1/2`; `SKILL_TALLY_R91=FAIL`
   (`receipts-R91ReviewerC3/c3-carrier-committed.txt`). This is the pre-landing state plan §Pre-freeze repair 9
   predicts, not a deviation: the frozen C3 predicate (a landing-revision PASS) is **not** met at C3, and the repair
   is deferred to the landing.
2. Carrier C3 controls:
   `cd $S/carrier && python3 -B corpus/evidence/round91/skill-tally-r91-controls.py --root . --work $S/work/controls-carrier`
   → exit 2; `SETUP repaired clause absent from SKILL.md — is this the landing tree?` — no `CONTROLS=` line
   (`…/c3-controls-carrier.txt`).
3. Repaired landing, C3 command:
   `cd $S/landing && python3 -B corpus/evidence/round91/skill-tally-r91.py --root . --selftest corpus/evidence/round91/controls/selftest-r91.txt`
   → exit 0; the frozen line appears verbatim and byte-exactly:
   `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`;
   `SKILL_TALLY_R91=PASS` (`…/c3-landing-predicate.txt`; verbatim check in `…/c3-predicate-line-check.txt`).
4. Repaired landing controls:
   `cd $S/landing && python3 -B corpus/evidence/round91/skill-tally-r91-controls.py --root . --work $S/work/controls-landing`
   → exit 0; `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`
   (`…/c3-controls-landing.txt`).
5. Claim **Before**: `cd $S/base && python3 -B corpus/evidence/round90/skill-tally-r90.py --root . --selftest corpus/evidence/round90/controls/selftest-r90.txt`
   → exit 0; `… OTHER_OCCURRENCES=3 SKILL_TALLY_R90=PASS` (`…/c3-r90-base-before.txt`); the swing fixture
   `$S/work/controls-landing/old-prose/SKILL.md` is byte-identical to `$S/base/SKILL.md` (`cmp_exit=0`), so the
   committed `controls/receipts/c3-before.txt` old-prose run is a base-prose run.

## The five assigned probes

Every probe below is a SKILL.md-only tree under `$S/probes/<name>/` (plus a receipt copy where named); the counter is
the landing copy `$S/landing/corpus/evidence/round91/skill-tally-r91.py`; the committed receipt is used unless a probe
says otherwise. Full stdout of every run is in `receipts-R91ReviewerC3/<name>.txt`.

### 1. Range extended past the case list — refused

Fixture: landing SKILL.md with the repaired clause replaced by
`r39 bash-pin cases 273–275 and bash-pin-override cases 282–299`.

```
python3 -B $S/landing/corpus/evidence/round91/skill-tally-r91.py --root $S/probes/p1-range-past --selftest $S/landing/corpus/evidence/round91/controls/selftest-r91.txt   # exit 1
CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=282-299 derived=282-283
CASE_RANGE_FINDING MISLABELED=16 indices=284,…,299
… CASE_RANGE_OK=1/2 MISLABELED=16 LEGS=1/2
SKILL_TALLY_R91=FAIL
```

Refused; the code is the generic `RANGE_MISMATCH` (no distinct "past-the-list" code), plus `MISLABELED=16`.
**Neutral** to the stated wording: a wrong extended range is refused.

### 2. Renamed case 282 plus a new name — names and numbers are both bound only weakly

- 2a rename `ok-case  282 bash-pin-override-missing` → `bash-pin-override-renamed` **and** add
  `ok-case  284 bash-pin-override-added exit=0` (receipt copy):
  `… --root $S/probes/p2a-family-add --selftest $S/probes/p2a-family-add/selftest.txt` → exit 1;
  `RANGE_MISMATCH:bash-pin-override claimed=282-283 derived=282-284`, `CASE_RANGE_OK=1/2 MISLABELED=0`;
  no mislabeled index — the added family name moved the max (`…/p2a-family-add.txt`).
- 2b same rename **and** add `ok-case  284 unrelated-new-case exit=0` → exit 0;
  `… CASE_RANGE_BASH_PIN=282-283 … CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=2/2`; `SKILL_TALLY_R91=PASS`
  (`…/p2b-unrelated-add.txt`). A new non-family name is invisible; `EXPECTED_CASES=283` is never compared with the
  284 ok-case lines.
- 2c renumber 282 → 300 (name kept) → exit 1; `RANGE_MISMATCH … claimed=282-283 derived=283-300`,
  `MISLABELED=1 indices=282` (`…/p2c-renumber.txt`).
- 2d duplicate in-family `ok-case  282 bash-pin-override-dup exit=0` (inside the span) → exit 0; PASS, `MISLABELED=0`
  (`…/p2d-inside-add.txt`).
- 2e the rename **only** (no addition) → exit 0; PASS, `CASE_RANGE_BASH_PIN=282-283`, `MISLABELED=0`
  (`…/p2e-rename-only.txt`).

Answer: the leg binds neither exact names nor the case count. It binds the family predicate (substring `bashenv`,
prefix `bash-pin-override`) and the family's min/max index. A prefix-preserving rename is invisible (2e), an
unrelated or inside-span addition is invisible (2b, 2d), a renumber or an out-of-span family addition is refused
(2c, 2a). **Falsifies named limit 1** ("a rename changes the binding loudly, by design"): the rename preserves the
prefix and the binding is unchanged.

### 3. Clause absent — `CLAUSE_MISSING` fires, unless the phrase survives elsewhere

Fixture: clause replaced by `r39 bash-pin cases 273–275 and r82 pin-override cases 276–283 (the two final cases are
the bash-pin override family)`.

```
python3 -B $S/landing/corpus/evidence/round91/skill-tally-r91.py --root $S/probes/p3-absent --selftest $S/landing/corpus/evidence/round91/controls/selftest-r91.txt   # exit 1
CASE_RANGE_FINDING CLAUSE_MISSING:bash-pin-override
… CASE_RANGE_OK=1/2 MISLABELED=0 LEGS=1/2
SKILL_TALLY_R91=FAIL
```

Fires as stated (`…/p3-absent.txt`). **But** p6 shows the refusal is document-wide, not row-scoped: with the same
absent row clause and a prepended line ``Round-90 historical note: the family read `bash-pin-override cases 282–283`.``,
the counter exits 0 with `CASE_RANGE_OK=2/2 MISLABELED=0` and no `CLAUSE_MISSING` (`…/p6-absent-row-quote.txt`).
So an absent Gates-row clause is tolerated whenever any other occurrence carries the phrase — **falsifies K4's
"an absent clause is tolerated" prohibition** in that form.

### 4. Historical tally edited — value invisible, deletion counted but not refused

- 4a change one `OTHER_OCCURRENCES` quote `PASS (256 cases, 0 skipped)` → `PASS (999 cases, 0 skipped)`:
  exit 0; `OTHER_OCCURRENCES=3`, `STALE_TALLIES=0/9`, `SKILL_TALLY_R91=PASS` (`…/p4a-hist-value.txt`). Not bound —
  consistent with named limit 3 ("historical quotations stay unbound and counted") for the tally leg.
- 4b delete one historical occurrence (`PASS (161 cases, 0 skipped)` → `a prior tally`): exit 0;
  `OTHER_OCCURRENCES=2`, `STALE_TALLIES=0/9`, `SKILL_TALLY_R91=PASS` (`…/p4b-hist-delete.txt`). The count changes but
  the verdict does not; K3's frozen `OTHER_OCCURRENCES=3` is enforced only by comparing the printed frozen line, never
  by the counter's PASS/exit.

### 5. The two clauses swapped — caught

Fixture: `r39 bash-pin cases 282–283 and bash-pin-override cases 273–275`.

```
… --root $S/probes/p5-swap --selftest $S/landing/corpus/evidence/round91/controls/selftest-r91.txt   # exit 1
CASE_RANGE_FINDING RANGE_MISMATCH:bashenv claimed=282-283 derived=273-275
CASE_RANGE_FINDING RANGE_MISMATCH:bash-pin-override claimed=273-275 derived=282-283
CASE_RANGE_FINDING MISLABELED=3 indices=273,274,275
… CASE_RANGE_OK=0/2 MISLABELED=3 LEGS=1/2
SKILL_TALLY_R91=FAIL
```

**Neutral**: caught (`…/p5-swap.txt`).

## Additional probes fired at the same wording

- **p2f — override interior gap.** SKILL.md claims `bash-pin-override cases 282–284`; receipt renames 283 to
  `pin-env-unrelated` and adds family name 284. Result: exit 0; `CASE_RANGE_FINDING MISLABELED=1 indices=283` but
  `CASE_RANGE_OK=2/2 MISLABELED=1 LEGS=2/2`, `SKILL_TALLY_R91=PASS` (`…/p2f-interior-gap.txt`). `ok_ranges` tests only
  endpoint equality and never `not mislabeled`, so the counter's own printed finding is not applied to the verdict.
- **p2g — bashenv interior gap.** Receipt renames 274 to `unrelated-drift-echo`; the landing clause still claims
  `273–275`. Result: exit 0; `CASE_RANGE_BASHENV=273-275 … CASE_RANGE_OK=2/2 MISLABELED=0`, `SKILL_TALLY_R91=PASS`
  (`…/p2g-bashenv-gap.txt`). No `MISLABELED` is computed for the `bashenv` clause at all, so a non-`bashenv` index
  inside the claimed range passes silently.
- **p7 — old prose accepted when quoted earlier.** Landing SKILL.md with the Gates row restored to the old clause
  `… r82 bash-pin-override cases 276–283 …` plus the prepended correct quotation:
  exit 0; `CASE_RANGE_BASH_PIN=282-283 … CASE_RANGE_OK=2/2 MISLABELED=0`, `SKILL_TALLY_R91=PASS`
  (`…/p7-oldprose-quote.txt`). This is literally K2's "r91 accepts the old prose" on that tree; the range regexes are
  `re.search` over the whole file, first match wins, and nothing requires the match to be the Gates row.
- **p8 — order sensitivity.** Correct Gates row plus an earlier wrong quotation
  (``…read `bash-pin-override cases 276–283` ``): exit 1; `RANGE_MISMATCH claimed=276-283 derived=282-283`,
  `MISLABELED=6` (`…/p8-wrong-quote-first.txt`). An earlier quotation defeats an honest row.
- **p9 — joint receipt+prose edit.** Gates row keeps the old clause; six receipt names 276–281 are renamed into the
  family. Result: exit 0; `CASE_RANGE_BASH_PIN=276-283 … CASE_RANGE_OK=2/2 MISLABELED=0`, `SKILL_TALLY_R91=PASS`
  (`…/p9-joint-edit.txt`). The receipt hashes `55d9602a0566e2ddaac679507631c8e5daa3f3b9581521722f474293a9a0666f`
  against pin `9c294281…` and nothing in the C3 path reads the pin (`…/p9-pin-unchecked.txt`); only
  `control-driver-r91.py` reads `instrument-pins.txt`, and only for its six expected rows' first script and the
  expectations file.
- **p10 — row reclassified as historical.** First Gates row made stale (`PASS (282 cases, 0 skipped)`) and its
  prefix changed from ``| `research-gate` `` to `| research-gate |`, so `current()` no longer selects it. Result:
  exit 0; `TALLY_ROWS=8 … OTHER_OCCURRENCES=4 STALE_TALLIES=0/8 … LEGS=2/2`, `SKILL_TALLY_R91=PASS`
  (`…/p10-reclassify.txt`). The tally leg binds rows by shape; a stale row that changes shape leaves the binding.

## Findings by severity

**F1 (high) — the case-range legs bind the first document-wide occurrence, not the Gates-row clause.**
Evidence p6, p7, p8: commands and lines above; receipts `p6-absent-row-quote.txt`, `p7-oldprose-quote.txt`,
`p8-wrong-quote-first.txt`. `BASHENV_RE`/`OVERRIDE_RE` are `re.search` over the whole SKILL.md; the code never tests
that the match lies on the `research-gate` row or that the phrase occurs once. Consequence: K4's absent-clause refusal
is bypassed by any surviving quotation (p6); the pre-round mislabeled prose is accepted when a correct quotation
appears earlier (p7); a correct row is refused when a wrong quotation appears earlier (p8). On the actual landing
tree the prefix occurs exactly once each (`c3-predicate-line-check.txt`), so the frozen line is not disturbed there,
but the leg's stated relation to the Gates row is not implemented. Narrowing to record: scope both searches to the
`research-gate` row's self-test cell (or require exactly one occurrence and fail on a second), and count range-phrase
occurrences, not only tally-shaped ones, if quotation is allowed.

**F2 (high) — `CASE_RANGE_OK` is endpoint equality, not set equality, and `MISLABELED` never fails the verdict.**
Evidence p2f (`…/p2f-interior-gap.txt`): prose 282–284 with 283 non-family → `CASE_RANGE_OK=2/2 MISLABELED=1 PASS
exit 0`; evidence p2g (`…/p2g-bashenv-gap.txt`): 274 non-`bashenv` → `CASE_RANGE_BASHENV=273-275 MISLABELED=0 PASS`.
`ok_ranges = not range_codes and claimed_env == derived_env and claimed_ovr == derived_ovr` omits `not mislabeled`,
and `mislabeled` is computed only for the override clause. This contradicts the tool's own leg-2 definition ("the
`r39 bash-pin` range equals the indices whose case name carries `bashenv`; the `bash-pin-override` range equals the
indices whose name starts with `bash-pin-override`"). Narrowing: compute claimed-set equality for both clauses and
include `not mislabeled` in `ok_ranges`; make `CASE_RANGE_OK` count set equality. The frozen literal `MISLABELED=0`
is the only current guard.

**F3 (medium) — the receipt population is neither counted nor pinned; a prefix-preserving rename is invisible.**
`CASE_RE` parses 277 of the receipt's 283 `ok-case` lines (196–200 and 223 print `accepted=` instead of `exit=`);
`names` is never compared with `EXPECTED_CASES - EXPECTED_SKIPPED`. Evidence: p2b (unrelated 284 added → PASS),
p2d (duplicate in-family 282 → PASS), p2e (rename-only → PASS), p9 + p9-pin-unchecked (joint edit → PASS with a
receipt hash that differs from the pin). This falsifies named limit 1's "a rename changes the binding loudly", and C3
carries no named limit for the receipt trust boundary (C1 limit 1 and C2 limit 5 carry the coherent-joint-edit limit;
C3's limit list does not). Narrowing: parse both `exit=` and `accepted=` forms, assert the parsed count equals the
verdict count, and either verify the receipt's `instrument-pins.txt` digest inside the C3 path or add the missing
named limit: "_the `--selftest` receipt is trusted caller-supplied committed bytes; a coherent joint edit of receipt
and prose survives_".

**F4 (low) — `OTHER_OCCURRENCES` and `TALLY_ROWS` are diagnostics, not verdict inputs; the current-row selector is
shape-based.** Evidence p4b (deletion → `OTHER_OCCURRENCES=2`, PASS exit 0) and p10 (stale row reclassified →
`TALLY_ROWS=8`, PASS exit 0). The deleted/renamed occurrence is visible in the printed line, so the frozen predicate
catches it externally; the counter's `PASS` does not. Narrowing: bind `other` to the expected 3 (or record the
occurrence identities), and fail when a `research-gate` row stops matching `current()` instead of silently
reclassifying it as historical (line 781's host note is already counted as a current tally by the substring rule —
carried from r90, not new).

**F5 (verification gap, disclosed by plan §9) — the frozen C3 predicate is satisfiable only on the post-wave landing,
which no commit carries.** Carrier C3 prints `SKILL_TALLY_R91=FAIL` (exit 1) and its controls exit 2 `SETUP`; the
repair is uncommitted at review time (`M SKILL.md`, `1 1 SKILL.md`, byte-identical to the battery's hard-coded
`OLD_CLAUSE`). Consequently: (a) the C3 controls predicate has never run against a committed round-91 tree; (b) the
battery hard-couples the landing wording — any byte difference from `OLD_CLAUSE` yields `SETUP` exit 2, a coupling
the frozen claim does not mention; (c) the `--selftest`-omitted fresh path (~6 min, `bash tools/research-gate.sh
--selftest`) was not exercised (not required by the item) and is an unrun check.

## Neutral / held observations

- p1, p3, p5 and p2a/p2c behave as the claim's refusal modes intend; p4a's value edit is unbound exactly as named
  limit 3 says for the tally leg.
- On the reconstructed landing, the frozen predicate line and the controls line are reproduced byte-for-byte with
  exit 0 (`c3-landing-predicate.txt`, `c3-controls-landing.txt`, `c3-predicate-line-check.txt`); `Before` holds on
  the base tree (`c3-r90-base-before.txt`). The headline C3 numbers are true where the claim runs them.
- Exit codes observed: 0 pass, 1 fail, 2 setup, as documented. `--selftest` is resolved against the CWD, not
  `--root` (visible in the probe runs); the frozen command's CWD is the root, so it is unambiguous there.
- `MISLABELED` is computed only when both a claimed and a derived clause exist, so a failing tree can print
  `MISLABELED=0` (p3); treat the number as diagnostic, not as evidence of a correct row.

## Residual risk

- The landing clause is uncommitted; this verdict is on the reconstructed landing (C3 + the exact lane worktree
  edit). If the landing differs by a byte, the controls exit 2 and the predicate would need re-running.
- The counter trusts `--selftest` bytes; p9 is a coherent joint edit, not a live defect at C3 (the C3 carrier does
  not touch the selftest receipt, and the six c1/c2 receipts are its only diff).
- No LSP was available; all caller/definition analysis is literal code reading plus the reproducers above.
- The fresh selftest path was not run (above).

## Receipts (copied to `.ufo/waves/round-91/w1/receipts-R91ReviewerC3/`)

`c3-carrier-committed.txt`, `c3-controls-carrier.txt`, `c3-landing-predicate.txt`, `c3-controls-landing.txt`,
`c3-r90-base-before.txt`, `c3-r90-on-carrier.txt`, `c3-predicate-line-check.txt`, `c3-lane-worktree-state.txt`,
`p1-range-past.txt`, `p2a-family-add.txt`, `p2b-unrelated-add.txt`, `p2c-renumber.txt`, `p2d-inside-add.txt`,
`p2e-rename-only.txt`, `p2f-interior-gap.txt`, `p2g-bashenv-gap.txt`, `p3-absent.txt`, `p4a-hist-value.txt`,
`p4b-hist-delete.txt`, `p5-swap.txt`, `p6-absent-row-quote.txt`, `p7-oldprose-quote.txt`, `p8-wrong-quote-first.txt`,
`p9-joint-edit.txt`, `p9-pin-unchecked.txt`, `p10-reclassify.txt`.

VERDICT: R91ReviewerC3 C3 fired — the frozen landing line and controls line reproduce exactly on the reconstructed landing, but CASE-RANGE's stated binding is not enforced: a non-family interior index PASSes at `CASE_RANGE_OK=2/2`, a prefix-preserving rename is invisible, range phrases bind any document occurrence (a quotation satisfies or defeats the row), and the unpinned receipt accepts a joint edit.
VERDICT: R91ReviewerC3 C1 n/a — not this seat's claim; the driver, forgeries and six receipts were not exercised.
VERDICT: R91ReviewerC3 C2 n/a — not this seat's claim; the curation counter and its controls were not exercised.
