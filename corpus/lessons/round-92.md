# Round 92 — the pins file is pinned like any other instrument, empty cells are not separators, and the tally scope is an ATX boundary (2026-11-08)

Base `d7780feff6e39ae74a2fd77fc9773c671b33da95` (round-91 landing + its non-author spot-check, admitted). Frozen
claims in `corpus/evidence/round92/claims.md` and `.ufo/waves/round-92/claims.json`; plan, pre-freeze repairs and amendments in `plans/round-92.md`.
Freeze F7 `7901eb238a8adc9b8d438dee7779140e28da6e62` (instruments, claims, pins); carrier C8 `9ab1dbece238ec162fde2a1c63d57c2371b6a35d` (six committed scored receipts + before receipts
at the freeze tree). Six earlier freeze/carrier pairs (incl. `bf12c30e`/`ddb5fdf4`, `85a2eeef`/`9722365f`,
`dc7056c4`/`e40bce1a`, `007d7ea7`/`d818f090`, `42e03378`/`16ccf769`) were superseded before any settled
scoring — their defects are Mistakes 1–2 and 7–10 in `plans/round-92.md` (§§Pre-wave freeze repair 1–2).
One v1 wave, 12 seats, see §Wave settlement.
## Gate

No registry row was written and no new source was opened this round; the sourced-claim requirement is satisfied
below via the S070 re-open and two rev-form Gate records.

The S070 source was re-opened from the installed page this round (registry row S070’s `mined` cells name
the file sha; the on-disk sha verified identical). It is not a lane-revision record, so it carries no
`rev=` field — see the bullet below for the located quote (`line=11 words=7`).

GATE-RECORD S001 rev=7901eb238a8adc9b8d438dee7779140e28da6e62 path=tools/research-gate.sh line=9010 words=4 quote=RESEARCH_GATE_SELFTEST: PASS (%d cases%s)

- **S070 re-opened** (`sha256sum(1)`, tier A, the installed page): `/usr/share/man/man1/sha256sum.1.gz`, sha256
  `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` — identical to the row's recorded sha; re-opened
  locally 2026-11-08. Decompressed line 11 is `Print or check SHA256 (256\-bit) checksums.` and its rendered form
  is "Print or check SHA256 (256-bit) checksums." (7 words). It grounds C1's digest rule, including the minus-self
  self-pin: the page says the tool prints or checks a digest, which is what the pin leg does with the pinned bytes.
  `R92SentinelScope.md` §7 and `R92ScoutRegistry.md` both re-opened it; this round's own gate record carries my
  access date. The S070 row's `teaches` cell (digest text + `--check` input) remains `mined`.
- **S001 re-opened** (`tools/research-gate.sh`, own-work, tier A): line 9010 PRINTS the one selftest-verdict line the
  C3 case-count leg depends on; the record above verifies at F6. The tool is unchanged this round
  (`git diff --quiet d7780fef..HEAD -- tools/` is verbatim at filing).
- **SOURCES.md census:** round start exit 0, 219 rows, five pre-existing `W04` warnings; round end exit 0,
  219 rows, same five `W04` warnings. No row added, no status change. The S070 row's anchor (decompressed line
  11) resolves in the installed page as before.

## Claim outcomes

- **C1 operability — verified on the wording narrowed by Amendments 1–4.** `control-driver-r92.py verify` prints
  `CONTROL_DRIVER_R92=PASS` with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` and
  `SELF_PIN OK rev=7901eb23 receipts_rev=9ab1dbec` (evidence: `after/c1-verify.txt`); the battery prints
  `FORGERY_REFUSED=3/3 POSITIVE=pass` (`after/c1-forgeries.txt`). Repairs over r91: `emit` without `--receipts`
  exits 2 (`emit requires an explicit --receipts` — previously exited 0 and overwrote the committed receipts),
  `PIN_DUPLICATE` prints `SETUP PIN_DUPLICATE` to stdout and exits 2 (previously exit 1 on stderr),
  `rel_for` refuses paths escaping the base, and the pins file self-pins by its minus-self digest
  (`R92ReviewerC2` F1/F2, `R92ReviewerC1` F1/F4, `R92SentinelScope` F2/F3; seeded by `R92ExecMutations` M1–M3
  kills and `R92SentinelScope` F4/F5). Before: the r91 driver has no such guard (emit defaulted silently,
  `PIN_DUPLICATE` exited 1) — see `evidence-before/c1-before.txt`.
- **C2 calibration — verified on the wording narrowed by Amendments 1, 5–7.** `CURATION_R92=PASS` with
  `LEGS_MEASURED=14/14 Q_SHAPE_FAIL=0 SOURCE_STATUS_OK=20/20 USED_BY_OK=20/20 TFREQ_OK=17/17 TFREQ_MAX_DF=3
  UNENTAILED_TERM=0 WARRANT_OK=17/17 DUP_QIDS=0` (`after/c2-counter.txt`); controls print
  `CONTROLS=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 DUPCOUNT_R91=1 DUPCOUNT_R92=1` with `PRIOR_REGRESSION=4/4`
  on the summary line and `FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` on the regression line (`after/c2-controls.txt`).
  Repairs over r91: an empty first cell is no longer skipped as a separator in either table (a quote row with a
  first-cell `""` now reaches QSHAPE; a first-position forged row is a data row unless it IS the literal
  `qid|source|quote` header), and decision rows are counted as the pipe-leading data rows the table holds
  (`R92ReviewerC2` F2–F4; seeded by `R92ExecMutations` M4/M5/M6/M8 kills). Before: the r91 counter prints
  `CURATION_R91=PASS` on all four S trees (`evidence-before/c2-before.txt`).
- **C3 freshness — verified on the wording narrowed by Amendments 8–9.** `SKILL_TALLY_R92=PASS` with
  `TALLY_ROWS=8 STALE_TALLIES=0/8 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283
  CASE_RANGE_OK=2/2 MISLABELED=0 OTHERS_OK=1 LEGS=3/3` (`after/c3-counter.txt`); controls print
  `CONTROLS=PASS OLDPROSE_REFUSED=1/1 PRIOR_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1` (`after/c3-controls.txt`).
  Repairs over r91: the section boundary is the next ATX heading of depth ≤ 2 at column 0 (`# ` or `## `) with a
  `SCOPE_BLEED` setup diagnostic on an unterminated scope, and the case enumeration itself is pinned
  (`len(^ok-case lines) == cases` with distinct numbers — the six `accepted=` lines included)
  (`R92ReviewerC3` A1/A3, `R92ConnectorSiblings.md` §5). Before: the r91 counter prints `SKILL_TALLY_R91=PASS`
  on the deleted-161 tree, document-wide and unpinned (`evidence-before/c3-before.txt`).

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| a frozen pin basis two commits stale (F1–F4) | F2 pins matched F1 blobs; `pin_at_rev` at `rev=F2` flagged the plans row moved by F2's own edit; same class twice more at F3/F4 | the L1's own verify at each re-freeze, before any settlement scoring | plans/round-92.md §§Pre-wave freeze repair 1–2; F5/F6 regenerate pins from the very commit that carries them and verify heads at once |
| a `SystemExit(string)` taken for exit 2 | `Read` of the r91 driver: bare string raises exit 1; the claim sentence (rule 6) named exit 2 | the wave's C1 reviewer/sentinel replicating the literal command | the raise now prints the SETUP line to stdout and raises `SystemExit(2)`; the battery asserts the new exit |
| a claim sentence wider than the code (emit, pin scope) | `R92ReviewerC1` F1–F3, `R92SentinelScope` F2/F5, R92ExecMutations F5–F7: only 7 of 16 pins are byte-checked; transitive scripts unseen; minus-self skips comments/blanks | the wave's independent executors/literal runs before the report | rules 5 and 8 narrowed to the enforced set (Amendments 2–3); limits 7–8 name the remainder |
| a shared first-cell filter wider than the shape test | `R92ReviewerC2` F2–F4: empty first cell skipped at any position in both tables; first-position `qid` forgery swallowed — via one literal example, `\| \|` | the wave's reviewer seat running full trees against the frozen line | empty cells are no longer separators; the quote header must be the literal `qid\|source\|quote` row |
| a summary-token denominator swap | `R92SentinelScope` F6 / `R92ExecC2Repro` Finding 2: the controls summary prints `PRIOR_REGRESSION=4/4`, the detail line says `7/7` | the wave's executors reproducing the summary line | the claim names the firing line (`FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7` on the regression line) instead of the summary |
| a section boundary written as a string search | `R92ReviewerC3` A1, `R92ConnectorSiblings` §5: `text.find("\n## ")` bleeds to EOF on a `# `-level or indented heading | the wave's C3 reviewer probing heading rewrites | the boundary is `re.search(r"\n#{1,2} ", …)` (depth ≤ 2 at column 0) with a `SCOPE_BLEED` setup exit |
| a verdict count trusted without its enumeration | `R92ReviewerC3` A3: the receipt's `^ok-case` lines were never counted (277 vs 283 because six lines are `accepted=`) | the wave's C3 reviewer drafting a duplicate-case receipt | the counter pins the enumeration (`len(^ok-case lines) == cases`, distinct numbers) |
| a battery name drift at the freeze | claims named `control-forgeries-r92.py` / `curation-r92-controls.py`; the committed pinned names are `forgeries-r92.py` / `curation-controls-r92.py` | three seats running the frozen commands verbatim at C5 | claims.md/claims.json corrected to the committed names during the freeze (Amendment 1) |
| a plan edit 2 commits after its pins generation | `5b7ab7f6` (plan note) moved `plans/round-92.md` after the pins table pinned it; F6 drops the plans row entirely | the L1's `verify` at the post-plan commit | the pins table has no plans row (16 rows); the plan is narrative, not scored bytes |
| a whole-file-hash self-pin considered and rejected | a two-pass placeholder hash cannot satisfy itself (`sha(file-with-digest) != digest`) | the L1's build-time probe (this round, the cursor's own `draft.md` noted it before building) | the minus-self digest (round 91's mechanism, retained) — the battery's pins-rewrite class proves the self-pin bites |

## Wave settlement

One v1 wave, 12 seats, 0 dead: 3 executor, 3 reviewer, 1 critic, 1 mutation-tester, 1 sentinel, 1 connector, 1 scout,
1 revenger — attack share 8/12 = 67 %, one connector seat. Results `w1-results.json`; reports and receipts under
`.ufo/waves/round-92/w1/`; the 24-row ledger `claim-falsification.tsv` passes the pre-file gate
(`PREFILE-FALSIFICATION: pass claims=3 rows=24 attack_seats=8 findings=0`, exit 0).

- **C1** — `R92ExecC1Repro`: verify PASS exact counts + SELF_PIN; forgeries 3/3; TMPDIR default; emit-guard
  fired as a frozen-text mismatch (Amendment 2). `R92ExecMutations`: M1–M3 killed (named codes gone; the
  residual rc-1 in M1/M2 is incidental fixture self-pin drift, attributed so). `R92ReviewerC1`: F1 emit exit-2
  false, F2 transitive scripts (narrowed, Amendment 3 + limit 7), F3 minus-self comment/blank blindness
  (narrowed, Amendment 3), F4 `PIN_DUPLICATE` exit 1 not 2 (wired, Amendment 4). `R92SentinelScope`: F1
  (names), F2 (emit), F3 (exit code), F4 (`rel_for` escape), F5 (7-of-16 on-disk scope — narrowed, limit 8),
  F6–F10 as above. `R92CriticClaims`: freeze integrity held (15 non-self pins = F5 blobs; minus-self matches);
  plan-wording "no scored run" falsified as literal history (narrowed to "no settled scoring"). `R92RevPrior`:
  r91 mechanisms re-derived by executing the r91 functions.
- **C2** — `R92ExecC2Repro`: counter 14/14 readings exact; batteries at real paths; decision count 11+6 and the
  minus-self digest independently re-derived; two-directional used-by complete on either entry.
  `R92ReviewerC2`: F2/F3/F4 (empty-cell, positional header, survivor counts — wired as Amendments 5–7), F5
  (TFREQ universe — narrowed), F6 (summary token — named the firing line), F7 (whitespace quote — refused by
  FLOOR, named limit stands). `R92ExecMutations`: M4/M5/M6/M8 killed (clean counter still PASS; the battery's
  named `LEG_FAIL` lines gone).
- **C3** — `R92ExecC3Repro`: 8/0/283 tallies; controls PASS; scoped others {161:1, 256:1} re-derived line by
  line; 215 confirmed out of section. `R92ReviewerC3`: A1 scope bleed (wired, Amendment 8), A3 uncounted
  enumeration (wired, Amendment 9), A2/A4 held. `R92ConnectorSiblings`: the fleet scan maps the same classes
  across 9 sibling lanes (read-only; nothing absorbed); C1 minus-self and C3 multiset pinning are unique
  fleet-wide.
- **Scout** — `S070` re-opened byte-exact (recorded sha still matches installed), sources S214/S018/S023/S215/
  S026/S031 all `mined` with exact-token `used-by` naming their citing entry, no drift; census exit 0 at 219 rows.

## Trends

- **expansion: unchanged** — registry 219 → 219 rows; no new `corpus/knowledge/` entry; the source work is two
  re-opens (S070, S001) and no fetch.
- **quality: improved** — three instruments re-frozen with guards ordered by ten falsification artifacts
  (emit guard, exit-2 pin refusal, containment, empty-cell skip, structural header, device count, TFREQ
  universe, ATX boundary, enumeration pin); mutation battery 9/9 kills + 1 surviving rename control proves
  behavioral detection, and every repaired class carries a red-before witness.
- **discernment: improved** — the freeze was cut six times (F1–F6) before the wave settled, each repair
  superseding pre-settlement pairs with the defect named in the plan; the wave's nine amendments were published
  before filing as narrowings or wired guards instead of filing the wider sentences; the `PRIOR_REGRESSION=4/4`
  summary and the missing-before-receipts sentence were named in the report rather than smoothed over.

## Routed work

1. **operability** — the driver now refuses `rel_for` escapes at setup, pins every `.sh`/`.py` command token
   on disk, self-pins by minus-self digest, refuses duplicate pin paths at exit 2, and gates `emit` on an
   explicit `--receipts`; the residual on-disk scope (7 of 16 pins) is a named limit awaiting a
   byte-check-all-pins revision (it would cost a v6 counter change and a re-freeze).
2. **calibration** — an empty first cell is no longer a separator in either table; the decision-count device
   reads rows the table holds; TFREQ's universe (rows whose qids resolve) is stated in the claim text.
3. **freshness** — the section boundary stops at any ATX heading of depth ≤ 2 (`# ` or `## `) and dies loudly
   on an unterminated scope; the `^ok-case` enumeration is pinned against the verdict count.
4. **carried debt** — the round-74 source-blind order oracle, QUALITY 173's successful-refused record form, the
   r80 backlog Gate ids. Untouched this round (named here, not silently dropped).
