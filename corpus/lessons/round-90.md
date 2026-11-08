# Round 90 — the control receipt is verified as committed bytes; the curation verdict prints on the passing path; the skill tallies re-derive (2026-11-08)

Base `f54a45ed` (round-89 landing + its non-author spot-check). Frozen claims in `corpus/evidence/round90/claims.md`
and `.ufo/waves/round-90/claims.json`; plan, pre-freeze repairs and Amendments 1–10 in `plans/round-90.md`. Freeze
`8d9893b4`; receipts carrier `9bad1201`; capture commit `aa7d4223`. One v1 wave, 13 seats, 0 dead.

## Gate

One source was opened this round, one registry row was written, and three historical quotes were left untouched.

GATE-RECORD S220 url=https://man7.org/linux/man-pages/man1/grep.1.html fetched=2026-11-08T09:52:31Z tier=A decision=admit capture=corpus/captures/e6ec761219e8044b0e9e067a.txt capture_sha256=5a5e69c56413ba682b1609cba2baacafb393ff6821d5b752938efc390fd12823 words=10 quote="Select only those matches that exactly match the whole line."

- **S220** (GNU grep(1), "Matching Control", `-x , --line-regexp`): the located sentence grounds the receipt
  driver's whole-token rule — `-x` selects a match only when the whole line matches, so a required receipt value must
  equal one body token rather than occur inside a longer one. Opened at the committed capture (man7.org, HTTP 200,
  curl rc 0); the capture is committed at `aa7d4223`, which is after the wave tree `9bad1201`, so a verifier at the
  wave tree cannot read it (recorded by `R90ReviewerC1` F4).
- **S219 is reserved, not written.** The first attempt used `S219`; adding a real row at that id displaces the
  round-89 control battery's mirror row inside the parsed registry and one case stops being accepted by the prior
  counter (`PRIOR_ACCEPTED_FORGERY=6/7`, re-derived by `R90ScoutRegistry`). The row lands at `S220`. The failed
  gnu.org attempt (curl rc 28, no bytes) stays in `refetch.tsv` under `S219` and is not a registry row; the egress
  table records both attempts.
- **No other fetch.** `corpus/evidence/round57/refetch.tsv` gained the S219 failure row and the S220 success row only.
- Registry 218 → 219 rows; `git diff <base> <landing> -- corpus/SOURCES.md` is the one added S220 row (no in-place
  status/recheck/used-by change to an old row). Census exit 0 at start (218) and end (219), same five pre-existing
  `W04` warnings.
- Verified: `python3 -B tools/gate-records.py verify --root . --repo . corpus/lessons/round-90.md` →
  `GATE_RECORDS files=1 records=1 ok=1 fail=0`, exit 0 (the first draft said `words=11`; the gate printed
  `FAIL WORDS` and the count was corrected to 10 before landing — Mistakes 5).

## Claim outcomes

- **C1 operability — verified on the wording narrowed by Amendments 2, 3, 4, 7 and 9.** Scored commands (the
  corrected command is Amendment 7):
  `CONTROL_DRIVER_R90=PASS` with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` and `SELF_PIN OK`, exit 0;
  `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`, exit 0. Before: the round-89 driver passes its own rows and
  accepts all six forgery fixtures (`FORGERY_REFUSED=0/6`; `c1-prior-driver.txt`). The wave falsified the
  un-narrowed clauses (b)/(f)/(g) for duplicate headers (last-wins) and an instrument substitution
  (`R90ExecC1Forge`); those states are now named limits 4–6 and the round-91 repairs are named in
  Amendments 4 and 9. Evidence: `after/c1-verify-freeze.txt`, `after/c1-verify-landing.txt`,
  `after/c1-forgeries-freeze.txt`, `after/c1-forgeries-landing.txt`.
- **C2 calibration — honest stop.** The three commands reproduce the frozen lines at `9bad1201`
  (`CURATION_R90=PASS`, `LEGS_MEASURED=10/10`, `VERDICT fields_hold=1`, `DETECTOR_WITNESS=8/8`; mutants
  `MUTANTS_KILLED=10/10 … PRIOR_R89_SURVIVORS=2/2`; controls `CONTROLS=PASS FORGERY_REFUSED=7/7
  PRIOR_REGRESSION=7/7`), but the frozen kill rule K2 fires: `R90ExecC2Forge` F1/F2 build tree forgeries the full
  kit accepts at exit 0 (a quote row outside the parser's `Q`/3-cell shape; a cited source's `mined` → `rejected`
  status flip). A kill rule is not a wording clause and cannot be rewritten after a seat has scored (§9), so the
  claim **does not verify as frozen**; its enforceable property is published in Amendment 8 and the repairs are
  routed.
- **C3 freshness — verified on the wording narrowed by Amendments 1 and 10.** `SKILL_TALLY_R90=PASS`, exit 0:
  `TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3`; the before receipt
  prints `STALE_TALLIES=9/9 EXPECTED_CASES=283` (exit 1). Evidence: `after/c3-after.txt`,
  `controls/receipts/c3-before.txt`, `controls/selftest-r90.txt`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a registry id free in the registry but carried by a committed fixture | `R90ScoutRegistry`: adding a real `S219` row makes the r89 control battery's SUP case stop being accepted by r88 (`PRIOR_ACCEPTED_FORGERY=6/7`) | none — the census checks columns and duplicate URLs, not fixture string literals | row moved to `S220`; reservation recorded in `plans/round-90.md` §Pre-freeze 6; QUALITY 196 names the sweep |
| a freshness rule bound historical quotes as if current | first `skill-tally-r90.py` receipt read `TALLY_ROWS=12 STALE_TALLIES=12/12` (256/161/215 included) | the claim's own before receipt, read line by line | the rule binds only the eight Gates-table `research-gate` rows plus the host-note `Selftest` line; `OTHER_OCCURRENCES=3` printed; QUALITY 197 |
| two writers produced one receipt | the first `c3-before.txt` held two interleaved runs (`TALLY_ROWS=9` and `TALLY_ROWS=12`) | the receipt did not parse as one run | reran alone and re-read; QUALITY 198 |
| a refactor left the per-item loop around a quantified predicate | `R90ReviewerC2` F5 / `R90ExecC2Forge` observation 1: one unentailed row prints twice and the first label names a term the row does not contain | none on the clean tree (`UNENTAILED_TERM=0`), a probe tree prints `UNENTAILED_TERM=2` for one row | QUALITY 201; the loop deletion is routed to round 91 (post-freeze instrument change refused) |
| the L1 handed the scribe a word count it had not measured | the scribe's `GATE-RECORD S220 … words=11` draft; `gate-records.py` printed `FAIL WORDS` | `tools/gate-records.py` (the same check that certifies the record) | count the quote before writing the record; the corrected `words=10` record prints `OK` — Mistakes row 5, QUALITY 189's before/after discipline |
| the frozen counting command omitted a required argument | `R90MutBattery` F1: the C1 command text without `--work` exits 2, no verdict line | the wave's mutation seat, running the frozen text verbatim | Amendment 7 carries the full command; the instrument is unchanged (QUALITY 195's class) |
| the L1's wave context named a command form the driver's own self-pin rejects | `R90SentinelScope` F1: `--root <lane> --repo <clone>` prints `CONTROL_DRIVER_R90=FAIL` on correct bytes because scoring paths resolve against `--repo` | none until the sentinel ran the dispatch text verbatim (the claim's own command is `--root . --repo .`) | the report cites only the claim's form; `build_spec.py`'s wording is named in the report; QUALITY 202 and the round-91 path-base repair |

## Spot-check intake (round 89's routed defects)

| # | item | disposition |
|---|---|---|
| 1 | C2 after-line quotes an unprinted token | closed by C2's printed line (the claim still honest-stops on K2, but the token now exists on the passing path) |
| 2 | attack-share arithmetic 7/12 vs 6/12 | this round's wave: six attack seats of thirteen (46%); the ledger's count is the checkable value |
| 3 | work-performed frontier bullet undercount | the report states the measured counts (six mistakes, QUALITY 196–201) |
| 4 | Amendment 8's `LEGS_MEASURED=8/9` vs `8/8` | the r90 summary counts the full ten-leg set; the r89 receipt prints `8/8` |
| 5 | `SKILL.md` tallies stale at 275 | C3; nine cells and the host note now 283 with the r82 case range |
| 6 | carried debt | (d) control-driver discipline → C1 (and its round-91 residue); (e) detector witness → C2 (the two survivors die; the reviewer's relocations are Amendment 5/8); (a) round-74 order oracle, (b) QUALITY 173, (c) r80 Gate ids — carried unchanged |
| 7 | named limits stay named | C1 limits 1–6, C2 limits 1–4, C3 limits 1–2 are in the frozen text and Amendments 4/9/10 |

## Wave settlement

13 seats (5 executor, 2 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 scout, 1 connector, 1 scribe; attack share
6/13 = 46%), 0 dead. Findings and their disposition:

- **C1** — `R90ReviewerC1` F1/F2/F6 and `R90ExecC1Forge` F1/F2/F5 falsified the un-narrowed header/pin/fresh clauses
  (Amendments 2–4); `R90MutBattery` F1 falsified the frozen command's missing `--work` (Amendment 7) and F2/F3 named
  the fixture-coverage limits (Amendment 9). The claim verifies on the narrowed wording; its numbers reproduce.
- **C2** — `R90ExecC2Forge` F1/F2 (tree forgeries the full kit accepts) fire the frozen K2, so the claim honest-stops
  (Amendment 8); `R90ReviewerC2` F1/F4 narrowed the `LEG_FAIL WITNESS` and before-receipt clauses (Amendments 5–6).
- **C3** — `R90ExecC3Tally` O1 corrected the historical labels (Amendment 1); `R90MutBattery` C3 narrowed the
  expected-number clause to the before+landing pair (Amendment 10).
- **Sentinel disclosures** — (F1) the dispatch text's `--root <lane> --repo <clone>` form fails `self_pin` (the
  claim's own `--root . --repo .` is unaffected; QUALITY 202, routed); (F2) the freeze commit's receipts carry the
  provisional `f8fa55ec` pin and are re-emitted at the carrier `9bad1201` before any scored run, so a verifier must
  read the receipts at the carrier; (F4) the S220 capture is not tracked at the carrier and lands at `aa7d4223`, so
  the Gate record verifies from that commit onward.
- **Critic / mutation battery** — C2's B6 constant-witness and C3's file-read mutants survive only as printed-field
  gaps (named limits); the frozen tokens reproduce in every seat that ran them.

## Trends

- **expansion: unchanged** — no new `corpus/knowledge/` entry; the one registry row (S220, mined) grounds C1's rule and
  is cited by `corpus/evidence/round90/claims.md`, not by a knowledge entry.
- **quality: improved** — C1 and C3 verified with red-before witnesses (six forgery classes accepted by r89 and
  refused by r90; nine stale tallies re-derived), and the round's own wave findings became QUALITY 196–201. C2's
  instrument gains are reported but not admitted: the claim honest-stopped.
- **discernment: improved** — the wave fired C1's overstatement, C2's kill rule and two instrument defects the clean
  tree hid; the lane narrowed C1/C3, honest-stopped C2, and recorded every deviation here and in Amendments 1–10.
EOF
