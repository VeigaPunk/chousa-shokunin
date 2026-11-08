# chousa — round 92: plan and amendments

L1 `ChousaR92`. Base `d7780feff6e39ae74a2fd77fc9773c671b33da95` (round-91 landing + its non-author spot-check at
`d7780fef`). Frozen claims: `corpus/evidence/round92/claims.md` (prose) and `.ufo/waves/round-92/claims.json`
(machine form the pre-file gate reads). A `narrowing` cell in `.ufo/waves/round-92/claim-falsification.tsv` resolves
to a section here.

## Inputs — round 91's routed defects and the SCORECARD r92 plan

`corpus/lessons/round-91-verifier-spotcheck.md` §8 routed defects:

1. **operability** — gate `passed` on `EXACT_OK`; strip leading whitespace in the header test; pin the executed
   script (a `script=` column or execute only the pinned path); make `instrument-pins.txt` self-pinned and refuse a
   duplicated path (`PIN_DUPLICATE`); resolve `--expected`/`--receipts`/`__file__` against the base they are read
   from; add `--work` with a `TMPDIR` default; move Amendment 10's external pre-step into the procedure text; make
   `emit` require an explicit `--receipts`; run the fresh legs under `bash -c` with a scrubbed environment.
2. **calibration** — run QSHAPE before the shared first-cell filter; pin decision-row width and count per entry;
   tokenise the `used-by` cell; add two-directional `source_link` assertions; correct the docstring df numbers
   (5 and 8 under 24 units).
3. **freshness** — scope both regexes to the Gates-table cell; bind the r82 block range or drop it; pin the
   historical multiset so a deleted quote changes the verdict; bind exact case names and the case count; add selftest
   receipt to the on-disk pin set; make the controls accept the landing clause by regex.
4. **carried debt** — the round-74 source-blind order oracle, QUALITY 173's successful-refused record form, the r80
   backlog Gate ids. Untouched this round (named in the report, not silently dropped).

## What is frozen and what is not

* **Frozen (claim sentences, predicates, kill rules):** `corpus/evidence/round92/claims.md` + `.ufo/waves/round-92/claims.json`.
  Predicate tokens are the same sentence in the plan, the same condition in the counter's code and the same label in
  the receipt.
* **Not frozen:** the prose restatements in the SCORECARD; any measurement not named in a claim sentence.
* **Before states:** measured by the r92 batteries themselves (`FORGERY_REFUSED=3/3` with r91 mechanism
  attestation for C1 — the r91 verifier cannot PASS a fixture because it pin-checks against the real table,
  so no PRIOR_ACCEPTED=6/6 is claimed for C1; `PRIOR_ACCEPTED=4/4` for C2; `PRIOR_ACCEPTED=1/1` + carried
  refusals for C3). Before receipts land in `corpus/evidence/round92/controls/receipts/c{1,2,3}-before.txt`.

## Pre-wave freeze repair 1 (F2) — pins content must exist at the freeze revision

*Superseded by §Pre-wave freeze repair 2 (F4) before any scored run.*

The F1 commit `bf12c30e` froze the instruments and the claims but did not carry
`corpus/evidence/round92/instrument-pins.txt` (the pins are generated from the F1 commit's own blobs), so
`SELF_PIN` at `rev=F1` would have named a file the revision does not carry — the same defect class as r91's
`16332cc0`→`f6a05a2e`. F2 adds the pins table (generated from the F1 blobs, then carried in this commit) and
supersedes F1 as the freeze revision **before any scored run**. No claim sentence, predicate, kill rule or
target changed; the pins table is data, and its contents are re-derived from the F1 blobs below (the same
instrument-pins generation procedure as r91). F2's pins table pinned the F1 blobs and therefore
matched the F1 tree, but `pin_at_rev` compares each pinned digest against the blob at `--rev`: at `rev=F2`
the pins file is the file the F2 commit carries, whose self row is the minus-self digest of the F1 rows —
the F2 pins table and the F2 tree agree, so F2 self-pinned cleanly under `pin_at_rev(F2)` **except** for the
driver file itself, whose bytes at F2 differ from the pinned F1 sha (the F2 commit changed nothing in the
driver — the sha mismatch came from the *plans/round-92.md* edit that F2 also carried, whose sha is pinned).
F3 repairs exactly this: the pins table is regenerated from the F3 tree (not the F1 tree), and the driver is
unchanged between F2 and F3 except for the S5 self-pin exclusion already frozen. Two amendments to the
process (not to any claim): (a) the driver now excludes the pins file from `pin_at_rev`'s whole-blob leg and
checks its own digest by the minus-self rule against the blob at `--rev`; (b) the pins table is generated from
the commit it will be checked against, so both legs compare the same tree. Superseded freeze/carrier pairs
`bf12c30e`/`ddb5fdf4` (receipts against the F2 pins) and `85a2eeef`/`9722365f` are superseded **before any
scored run and before the wave**; their defects are in §Pre-wave freeze repair 2. No claim sentence, predicate,
kill rule or target changed.

## Damages found while building (before the freeze)

These were built and tested in scratch before anything was committed; no measurement was taken on an unfrozen
instrument.

1. **A self-referential sha pin is unsatisfiable as a whole-file hash.** The first fixture design ("write a
   placeholder, hash, rewrite") cannot verify (`sha(file-with-digest) != digest`). The frozen design is the
   minus-self-row digest: the pins file pins the sha256 of its own rows with the self row removed. A rewritten
   non-self row breaks it; the self row is outside its own hash by construction (battery case pins-rewrite).
2. **The fixture battery's prior control cannot PASS for r91.** r91's `verify` always pin-checks and, in the
   lane, reads the real pins table; in a probe layout the default file is absent. The r92 battery therefore
   attests the prior mechanism (source-level: last-wins `read_pins`, first-token `instrument_rel`, no pins-file
   entry in `pin_report`) instead of printing a fabricated `PRIOR_ACCEPTED=6/6`.
3. **The do-nothing control fired.** A first C1 design kept the six r91 classes as the claimed discrimination;
   the probe showed r91 already refuses all six (its own round's work). They were removed from the frozen
   battery and the claim says so.
4. **C2's regression reference pointed at a battery that does not take `--counter`.** The r91 controls have no
   `--counter` flag (only the r90 controls do, via its own alias writer). The frozen controls replay the r90
   battery with a verdict-token alias, exactly as r91 did.
5. **A fifth C2 leg was missing from the count.** The counter grew from 13 to 14 legs (USED_BY); the first
   run printed `LEGS_MEASURED=13/14`-style failures before the freeze. `EXPECTED_LEGS=14` is frozen.
6. **C3's others multiset initially counted document-wide.** The 215 tail tally sits after `## Round26` (outside
   `## Gates`); the first draft pinned `{161,215,256}` and failed on the clean tree. The frozen multiset is the
   in-section two `{161,256}` and the 215 tally is a named limit.

## Pre-wave freeze repair 2 (F4) — pin rows must be generated from the commit they are checked against

F2's pins table pinned the F1 blobs and therefore matched the F1 tree, but `pin_at_rev` compares each pinned
digest against the blob at `--rev`. F3 fixed the driver's self-pin leg (pins file excluded from the whole-blob
comparison, checked by its minus-self digest against the blob at `--rev`) but kept the F1-era pins rows, so
at `rev=F3` the plans row mismatched by exactly the plan-note edit the same commit carried. The pins were
regenerated from the F3 tree; the same failure recurred because the new pins commit was checked at `rev=F3`
with an older pins file. **F4 (freeze `007d7ea7`, carrier `d818f090`)** generates the pins table from the
commit that will carry it: `007d7ea7` carries the pins file, the receipts were emitted against that commit,
and the verify confirms `SELF_PIN OK` and `PIN_OK=6/6`. The three earlier pairs are superseded **before
any scored run**: `bf12c30e`/`ddb5fdf4` (no pins file at the freeze), `85a2eeef`/`9722365f` (F1-era pins at
the F2 tree), `dc7056c4`/`e40bce1a`/`007d7ea7` (plan row regenerated late). Defects: F1 — reuse of a pin
basis two commits stale (never caught by a pre-freeze self-check, because the self-check itself compared the
wrong revisions); F2/F3 — the same class twice. The fix: the pins-generation command pins the very commit
named `--rev`, and the verify runs once before the carrier commit. **No claim sentence, predicate, kill rule
or target changed in F2–F4.**

## Amendments

Wave settles at F5/C5. Amendments 1–9; each names its artifact and the enforceable property the claim now states.

1. **Instrument filename correction** (artifact: `R92SentinelScope.md` F1, `R92ReviewerC2.md` F1,
   `R92ExecC1Repro.md` F1). The frozen battery names were `control-forgeries-r92.py` and
   `curation-r92-controls.py`; the committed pinned names are `forgeries-r92.py` and
   `curation-controls-r92.py`. `claims.md`/`claims.json` now name the committed files. No predicate token
   moved. *Narrowing: the path strings.*
2. **`emit` guard** (artifact: `R92ReviewerC1.md` F1, `R92ExecC1Repro.md` §(c)(ii), `R92SentinelScope.md`
   F2). Rule 8 said `emit` without `--receipts` exits 2; the driver had a silent default: `emit` ran exit 0
   and rewrote the committed receipts. The guard is now wired (`CONTROL_DRIVER_R92=SETUP emit requires an
   explicit --receipts`, exit 2). Verified at C6.
3. **On-disk pin scope narrowed** (artifact: `R92ReviewerC1.md` F2/F3, `R92SentinelScope.md` F5). Rule 5
   read as "every pinned file is byte-checked". Enforced: the executed scripts (all tokens) + expected + pins
   file (7 of 16 pinned rows) are byte-checked on disk; the other nine pins are blob-checked at `--rev` by
   SELF_PIN. The minus-self digest is over the non-comment, non-blank rows. Named limits 7–8 record the
   remainder. *Narrowing: rule 5 + limits 7–8.*
4. **`PIN_DUPLICATE` exit code** (artifact: `R92ReviewerC1.md` F4, `R92SentinelScope.md` F3). The raise was
   `SystemExit(message)` → exit 1 on stderr. Rule 6 said exit 2. The raise now prints
   `SETUP PIN_DUPLICATE path=…` to stdout and raises `SystemExit(2)`; the battery asserts `rc=2` for this
   class. Verified at C6 (`OK dup-pin-path: r92 rc=2`).
5. **Empty-first-cell and structural-header filtering** (artifact: `R92ReviewerC2.md` F2–F4). `data_lines`
   and `quote_lines` skipped empty-first-cell rows as separators; the quote header was swallowed
   positionally. An empty cell is no longer a separator (only all-dash/colon/space non-empty cells are),
   and the quote-header skip now requires the literal `qid|source|quote` row. A first-line forged row is a
   data row and reaches QSHAPE.
6. **Decision-row device count stated** (artifact: `R92ReviewerC2.md` F4): the pin counts pipe-leading data
   rows the table holds (11+6); wrong-width rows are `DECISION_WIDTH`, never a drop.
7. **TFREQ universe narrowed** (artifact: `R92ReviewerC2.md` F5): TFREQ covers decision rows whose named
   qids all resolve; an unresolved row is a `WARRANT` failure.
8. **Tally boundary regex** (artifact: `R92ReviewerC3.md` A1, `R92ConnectorSiblings.md` §5): the section
   boundary is now the next ATX heading of depth ≤ 2 at column 0 (`# ` or `## `), with a `SCOPE_BLEED`
   setup diagnostic when unterminated.
9. **Case-enumeration pin** (artifact: `R92ReviewerC3.md` A3): the counter requires `len(^ok-case lines) ==
   cases` with distinct case numbers (the six `accepted=` lines included).

## Do-nothing control (must not reach the after-state)

* C1: the r91 driver on the three S fixtures accepts each (mechanism attestation: `read_pins` last-wins,
  `instrument_rel` first-only, no pins-file entry in `pin_report`); no receipt/PASS is claimed from it.
* C2: the r91 counter prints `CURATION_R91=PASS` on all four S forged trees.
* C3: the r91 counter prints `SKILL_TALLY_R91=PASS` on the deleted-161 tree.
