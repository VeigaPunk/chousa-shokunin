# Round 91 — the receipt header is single-valued and its instrument is pinned; the quote table is counted by shape and source status; the case range re-derives from the tool's names (2026-11-08)

Base `265b8633` (round-90 landing + its non-author spot-check). Frozen claims in `corpus/evidence/round91/claims.md`
and `.ufo/waves/round-91/claims.json`; plan, pre-freeze repairs and amendments in `plans/round-91.md`. Freeze
`4d00d7519290569879f853d7122b82a927cda1f3` (F3); receipts carrier `67954adc599bd605705d94a1ea7abb582491a907` (C3).
Two earlier freeze/carrier pairs (`160b658b` / `d02a950f`, then `37831ce8` / `b8fc99a1`) were superseded before any
scored run and before the wave — their defects are Mistakes 1–2 and 8, plan §§Pre-wave freeze repair 1–2. One v1 wave, 12 seats, see §Wave settlement.

## Gate

One registry row was **re-opened** this round, one repo-local source was recorded with a rev-form Gate record, and no
new row was written.

GATE-RECORD S001 rev=4d00d7519290569879f853d7122b82a927cda1f3 path=tools/research-gate.sh line=9010 words=4 quote=RESEARCH_GATE_SELFTEST: PASS (%d cases%s)

- **S070 re-opened** (`sha256sum(1)`, tier A, the installed page): `/usr/share/man/man1/sha256sum.1.gz`, sha256
  `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` (unchanged from the row's recorded sha), opened
  locally 2026-11-08; decompressed line 11 is `Print or check SHA256 (256\-bit) checksums.` and its rendered
  form is "Print or check SHA256 (256-bit) checksums." (7 words; the quote is the rendered form, not a literal
  substring of the raw roff — `R91ScoutRegistry` finding, Gate wording corrected). It grounds
  C1's digest-pin rule: a pin is a printed/checked digest of the bytes, not a policy.
- **S001 re-opened** (`tools/research-gate.sh`, own-work, tier A): line 9010 is the one selftest verdict printer the
  C3 case-range leg reads its `ok-case` names from; the record above verifies at F3. The tool is unchanged this round
  (`git diff --quiet F3..HEAD -- tools/` empty at filing).
- **S221 was attempted and refused.** The planned new row (the IR textbook's document-frequency definition,
  `https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-term-weighting-1.html`) was opened through
  `tools/capture-fetch.py` after the egress table commit `7b19dd0b`; the fetch returned `curl rc=28` and no bytes
  (`refetch.tsv` row `S221 … 28 000 - -`). No row is written for a fetch with no bytes, and the term-frequency rule is
  measured from the lane's own entries instead. `grep -c '| S221 |' corpus/SOURCES.md` → 0.
- No other fetch. Registry 219 → 219 rows; census start (this round) exit 0 at 219; census end (filed with the round)
  exit 0 at 219, same five pre-existing `W04` warnings.

## Claim outcomes

- **C1 operability — verified on the wording narrowed by Amendments 7, 9, 10 and 15–22.** `control-driver-r91.py verify --root . --repo . --rev F3 --receipts-rev C3`
  prints `CONTROL_DRIVER_R91=PASS` with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` and
  `RECEIPT SELF_PIN OK rev=F3 receipts_rev=C3`; `control-forgeries-r91.py` prints
  `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`. Before: `PRIOR_ACCEPTED=6/6` — the r90 driver accepts all six
  classes (duplicate `# exit=`/`# computed_against=`, substituted instrument, relaxed expectations, missing
  `# expected_exit=`, unscored receipt). Evidence: `after/c1-verify.txt`, `after/c1-forgeries.txt`,
  `controls/receipts/c1-before.txt`.
- **C2 calibration — verified on the wording narrowed by Amendments 1–6 and 14.** `curation-r91.py --root .` prints `CURATION_R91=PASS` with
  `LEGS_MEASURED=13/13 Q_ROWS=20 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17
  TFREQ_MAX_DF=3 UNENTAILED_TERM=0 WARRANT_OK=17/17 DUP_QIDS=0`; `curation-r91-controls.py` prints
  `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R90=2 DUPCOUNT_R91=1 PRIOR_REGRESSION=7/7`. Before:
  r90 accepts all four tree forgeries and appends one unentailed row twice. Evidence: `after/c2-counter.txt`,
  `after/c2-controls.txt`, `controls/receipts/c2-before.txt`.
- **C3 freshness — verified on the wording narrowed by Amendments 8 and 11–13, 23–24.** `skill-tally-r91.py --root . --selftest controls/selftest-r91.txt`
  prints `SKILL_TALLY_R91=PASS` with `CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2
  MISLABELED=0 LEGS=2/2`; `skill-tally-r91-controls.py` prints `CONTROLS=PASS OLDPROSE_REFUSED=1/1
  PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1`. Before: the base `SKILL.md` clause said `bash-pin-override cases
  276–283` while cases 276–281 are `pin-env-fn-*`/`env-pin-override-*`/`pin-bash-path-shim`; r90 printed PASS because
  it never bound the range. Evidence: `after/c3-counter.txt`, `after/c3-controls.txt`,
  `controls/receipts/c3-before.txt`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a frozen expectation row lost an option in transcription | the first emit/verify at F printed `c1-harm-setup FINDING TOKEN_MISSING:HARM_RECHECK_ERROR`; the receipt body was argparse's `--repo` error, not the tool's own setup error (the r90 row carries `--repo`) | the freeze's own first emit, before the wave; the row was copied from round 90 by hand | row names `--repo @ROOT@`; freeze re-cut as F2 before any scored run; the receipt now prints `HARM_RECHECK_ERROR base-tool missing` |
| an "unscored receipt" leg flagged raw evidence files | the first verify at F printed `RECEIPT c1-before FINDING UNSCORED_RECEIPT` for the three before receipts | the verify's own output on the freeze tree | a file is an unscored receipt only when it carries a `# case=` header; the `extra-receipt` forgery still carries one and is still refused (M3 kills the leg) |
| a frequency guard whose document set cannot fail it | the first TFREQ design measured DF over the located quotes only; every non-stopword term there has DF ≤ 2, and the first forgery (`resource`) failed the *r90* warrant leg too because `resource` is a stopword (`PRIOR_ACCEPTED=0/1`) | the control battery's own positive-or-prior leg, before the freeze | documents are the entry's located quotes plus its decision rows; `DF_MAX=3` is the measured maximum of the legitimate rows' selected terms; the forgery shares only `source` (df 7), which r90 accepts and r91 refuses |
| a summary expression that cannot run | the first C3 summary raised `TypeError: 'int' object is not iterable` on `sum((a)+(b))` | the counter's own first run | `int(a)+int(b)`; the summary line is exercised before the freeze |
| a verdict parser keyed on line start | the C3 controls read `no-verdict` because the counters print `SKILL_TALLY_R9x=` at the end of the summary line | the controls' first run | match the token anywhere in the line; the final standalone line and the summary line both bind |
| a prior battery's line parser treated as an interface | `curation-r90-controls.py --counter r91` printed `no-verdict` for every case, because it only recognises `CURATION_R9[0-8]=` | the regression leg's first run | score the prior battery through a generated alias that runs r91 and renames only its verdict token; the alias is written in scratch and named in the controls header |
| two C1 clauses were wider than the code | reading `instrument_rel()` and the `UNSCORED_RECEIPT` parse test against the frozen sentence before the wave: "every file a row's command names" (the code takes the first) and "a `.txt` receipt" (the code requires a `# case=` header) | reading the code against its own sentence before any seat scored | plan §Pre-wave freeze repair 2 narrowed both clauses; F3/C3 re-cut |
| a frozen counting command omitted a required flag again | `R91ExecMutations`/`R91CriticClaims`/`R91SentinelScope` ran the frozen C1 text verbatim: argparse `--work` error, exit 2 | the wave's literal run; QUALITY 195's rule already names it | Amendment 7 adds `--work <scratch>`; the external pre-step of Amendment 10 is now part of the procedure |
| the pin table was read last-wins and was not itself pinned | `R91ConnectorSiblings` finds `read_pins()`'s `pins[path] = sha`; `R91CriticClaims` deletes a pin row and the driver still prints PASS | the connector's cross-lane scan and the critic's no-work control | Amendment 22 narrows the duplicate-path state; Amendment 10 makes the pins file an external pre-step; both routed to r92 |
| a quote's word count miscounted again | the S001 rev record's first draft said `words=5`; `tools/gate-records.py` printed `FAIL WORDS` (four tokens) | the same check that certifies the record | corrected to 4 before the lesson was committed; Mistake row 5 of round 90 repeats |
| a placeholder expression left in a detail string | the QSHAPE leg's `rows=` detail was a dead `sum(1 for _ in [])` placeholder | the first clean-tree run's summary | `rows={len(source_rows)}`; the number is printed and counted |

## Spot-check intake (round 90's routed defects)

| # | item | disposition |
|---|---|---|
| 1 | C2 reclaim: count/refuse a non-`Q` row, cross-check status/used-by, term-frequency warrant guard | closed by C2 (QSHAPE, SOURCE, TFREQ; four forgeries refused where r90 accepts) |
| 2 | C1 residues: duplicate header keys, instrument pin, `SELF_PIN` both revisions, fixtures, path base | closed by C1 (HEADER_DUPLICATE, INSTRUMENT pins, `rev=`+`receipts_rev=`, six-class battery, `BASES` line) |
| 3 | harm row is a self-comparison | closed: `c1-harm` reads the base tool from `265b8633`, not `master`; the row can move if the tool changes |
| 4 | ledger classification (`neutral` vs `falsifies-wording`) and amendment numbers in `narrowing` | conformance; this round's ledger names amendment numbers, see §Wave settlement |
| 5 | freeze-pin defect not recorded in the plan | plan now records F/C as superseded pre-wave and why |
| 6 | citation precision (attach values to the receipt that prints them) | C1/C2/C3 before-lines cite the battery receipts that print `PRIOR_ACCEPTED`/`DUPCOUNT`, not a derived marker |
| 7 | clause (a) is per row | named limit 3 in C1 |

## Wave settlement

One v1 wave, 12 seats, 0 dead: 3 executor, 3 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 connector, 1 scout,
1 revenger — attack share 8/12 = 67 %, one connector seat. Results `w1-results.json`; reports and receipts under
`.ufo/waves/round-91/w1/`; the 34-row ledger `claim-falsification.tsv` passes the pre-file gate
(`PREFILE-FALSIFICATION: pass claims=3 rows=34 attack_seats=8 findings=0`).

- **C1** — `R91ExecC1Repro` reproduces the frozen values from a clean clone and flags the dual-base asymmetry
  (Amendment 9); `R91ExecMutations` finds the missing `--work` in the frozen command (Amendment 7) and kills M1–M4,
  surviving only the rename control M11; `R91RevPrior` re-derives the six r90 acceptances; `R91ReviewerC1` falsifies
  clause 1's mechanism, the `EXACT_OK` gate, the lexical pin rule and the header lexing (Amendments 15–21);
  `R91CriticClaims` demonstrates the instrument-substitution state and the unpinned pins file (Amendment 10) and the
  `--work` omission; `R91SentinelScope` runs the printed form verbatim (exit 2), proves the verify path writes
  nothing, and routes `emit`'s write scope, the `bash -lc` profile leak and the checkout requirement;
  `R91ConnectorSiblings` maps last-wins parsers across seven sibling lanes and finds `read_pins()` carrying the same
  class (Amendment 22).
- **C2** — `R91ExecC2Repro` reproduces the counter, the controls and `DF_MAX=3`; `R91ReviewerC2` falsifies item 1's
  "every data row" (first-cell filter, Amendment 1), item 2's `used-by` (substring, Amendment 2), item 4's five-cell
  and two-term states (Amendment 3) and item 5's df number (5, not 7; Amendment 4), and routes the decision-row count,
  the `source_link` witness and the Situation-cell scope; `R91CriticClaims` fires the same first-cell class in the
  decision table.
- **C3** — `R91ExecC3Repro` and `R91SentinelScope` reproduce the landing predicate and controls; `R91ReviewerC3`
  finds the prefix-preserving rename invisible (Amendment 11), the document-wide clause binding (Amendment 12) and
  the historical-quote deletion (Amendment 13); `R91SentinelScope` finds the shipped clause's r82 block range unbound
  (Amendment 23) and the selftest receipt outside the on-disk pin set (Amendment 24); `R91CriticClaims` holds C3 on
  the repaired tree and shows a rename moving the derived range.
- **Scout** — `R91ScoutRegistry` finds no registry/capture/row-count drift; the S070 quote is the rendered roff form,
  and the Gate wording is corrected; the S221 attempt is recorded and no row exists.

## Trends

- **expansion: unchanged** — registry 219 → 219 rows; no new `corpus/knowledge/` entry; the source work is a re-open
  and a refused fetch.
- **quality: improved** — three instruments hardened with red-before witnesses re-derived by independent seats (six
  forgery classes; four tree forgeries plus the double count; the mislabelled case range), the verify path proven
  write-free over the whole tree, and ten criteria mined (QUALITY 203–210).
- **discernment: improved** — the freeze was re-cut twice before the wave; the wave fired on all three claims and the
  lane published 24 amendments, each naming its artifact and the narrower property, instead of filing the wider
  sentences; two HIGH classes (instrument substitution, unpinned pins file) are named limits with a routed repair.

## Routed work

1. **operability** — gate `passed` on `EXACT_OK`; strip leading whitespace in the header test; pin the executed script
   (a `script=` column or execute only the pinned path); make `instrument-pins.txt` self-pinned and refuse a
   duplicated path (`PIN_DUPLICATE`); resolve `--expected`/`--receipts`/`__file__` against the base they are read
   from; add `--work` with a `TMPDIR` default; move Amendment 10's external pre-step into the procedure text and make
   `emit` require an explicit `--receipts`; run the fresh legs under `bash -c` with a scrubbed environment.
2. **calibration** — run QSHAPE before the shared first-cell filter; pin the decision-row width and count per entry;
   tokenise the `used-by` cell; add two-directional `source_link` assertions; correct the docstring df numbers (5 and 8
   under 24 units).
3. **freshness** — scope both regexes to the Gates-table cell; bind the r82 block range or drop it; pin the
   historical multiset so a deleted quote changes the verdict; bind exact case names and the case count; add the
   selftest receipt to the on-disk pin set; make the controls accept the landing clause by regex.
4. **carried debt** — the round-74 "source-blind order oracle", QUALITY 173's successful-refused record form, the r80
   backlog Gate ids.





