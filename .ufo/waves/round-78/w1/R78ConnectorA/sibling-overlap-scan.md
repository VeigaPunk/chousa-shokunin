# R78ConnectorA — sibling-overlap scan (read-only, round 78)

Seat: `R78ConnectorA`. Lane: `chousa-shokunin`. Root read: `/home/vgpnk/Projects/shokunin`.
Nothing outside this wave folder was written. No lane, fleet or `corpus/` byte was touched.
No tool was installed (tooling record: none; `python3 -B` and `sha256sum` only).

Frozen predicate set read first: `corpus/evidence/round78/claims.md` (C1 = forge-battery v5,
C2 = selfcheck, instruments pinned at `93e0432e`). QUALITY 141–145, 137, 29, 36 read in full.

## Question

Does another lane already hold a criterion for

- **(i)** a verification harness printing an invertible answer key or a strippable subject identity,
- **(ii)** a receipt a child process can append to,
- **(iii)** a self-assessment registry row whose cell count does not match its header?

Answer: **yes for all three.** None of chousa's 143/144/145 is a new class. What differs is
strength and surface, and the differences run in both directions.

## Method (fail-closed, red-tested)

Instrument: `receipts/scan.py` — 3 concept classes × declared regex sets over every sibling
`corpus/QUALITY.md` (chousa excluded: it is the scanned lane), plus 12 named quotes verified
whitespace-normalised against the lane file that carries them. A zero-hit class is *not* a clean
verdict (it is `NO-EVIDENCE`, exit 1); an unresolved quote is `UNVERIFIED`, exit 1.

| run | command | exit | verdict line |
|---|---|---|---|
| green | `python3 -B scan.py --fleet /home/vgpnk/Projects/shokunin` | 0 | `SIBLING_SCAN=PASS classes_hit=3/3 zero_hit=none unverified=0` |
| red-1 (zero-hit class) | same, `--fleet <scratch>/red-fleet` (two lanes only) | 1 | `SIBLING_SCAN=FAIL classes_hit=2/3 zero_hit=ii unverified=11` |
| red-2 (fabricated quote) | `python3 -B scan-red2.py --fleet …` | 1 | `QUOTE=UNVERIFIED … id=KQ999` / `SIBLING_SCAN=FAIL … unverified=1` |

Receipts: `receipts/scan.out`, `red1.out`, `red2.out`, `SHA256SUMS`. The instrument is shown able
to fail on both of its own limbs (zero-hit class, unresolved quote), so a green scan is a result,
not a shape.

## (i) Invertible answer key / strippable subject identity — four sibling rows

**Closest: `tsukuroi-shokunin` QUALITY **90** (`corpus/QUALITY.md:177`, R42-OBSERVED-CHANNEL)**

> "A counter that holds no answer key is scored against every channel through which the scored
> code can see it is being watched, and a verdict binding matches an asserted line, not a mention"

It then enumerates the channels — "the override environment, the process identity (uid/euid,
groups), the fixture data's fixed values (package names, padding grammar), the namespace's own
traces (mount table, bind targets, stub text)" — and requires a "watched" variant per channel that
"must read below the target", plus the anchored-verdict-line rule.

**`kengaku-shokunin` QUALITY **Q38** (`:1027`)**

> "a content leg's verdict key is produced by executing the pinned source over generated end states
> and is stored nowhere in the counter; a key read off the instrument's own map, or off the source's
> prose, is a copyable answer"

with the in-file statement "STATES is a generator, not an answer key: no verdict is stored in this
file" (`:1035`).

**`souji-shokunin` QUALITY **Q102** (`:258`)**

> "whose fixtures leak the case (directory names, commit messages, fixed digests) does not
> discriminate a tool that memorises them"

requiring a HIDDEN-CASE audit over "scenarios the counter does not hold (opaque names, fresh
salts, …)" with a memorising control that must fail.

**`mori-shokunin` QUALITY **8** (`:15–16`)** — the earliest, weakest form: "enumerates the channels
or inputs tested; untested classes are named residuals", "if any encodes which scenario is running,
there is a sniffer channel".

## (ii) A receipt a child process can append to — three sibling rows

**Closest and strictly stronger: `kasegi-shokunin` QUALITY **R39** (`:351`)**

> "A receipt … is only ever the unedited tee of one observed run: one invocation writes it once and
> nothing appends to it or edits it afterwards, so its bytes are that invocation's stdout+stderr in
> the order printed"

with the consequence "a receipt composed of two runs … is not a receipt, and the result it carried
is discarded while the claim it served reads `report-only`".

**`kaidoku-shokunin` QUALITY **120** (`:193`)** — "a receipt never grants a write destination"
(a receipt is attacker-controlled input, not an instruction; the reader copies only into its own
scratch). Sibling **127** extends it to read destinations.

**`kama-shokunin` QUALITY **KQ106** (`:521`)** — "binds the answering process by a value the tool
cannot write: `/proc/<pid>/exe` re-hashed to the pinned binary, its argv, and the origin of the
listening descriptor", and "it must reject replays of the committed forgeries".

## (iii) Registry row whose cell count does not match its header — four sibling rows

**Exact class: `mado-shokunin` QUALITY **132** (`:943`)**

> "A registry row carries the table's own column count, and the append is gated by the table's
> census, never by the shape of the row above it by eye."

Shown able to fail by "a 12-field row (a separate quote column) into the 11-column registry … the
frozen census flagged `E01 fields=12` on every new row".

**`kaidoku-shokunin` QUALITY **117** (`:190`)** — "a table census declares the logical-column
mapping and accepts an over-count row only for named filed paths … it names a blank
purpose/verdict/self-test/write/owner cell instead of passing it".

**`kaidoku-shokunin` QUALITY **111** (`:180`)** — "a declared inventory is not its own population":
a registry that *is* the lane's self-assessment is censused from an independent population, and
"a control that compares the table with itself must be shown **green at the base while the defect
exists**".

**`tsukuroi-shokunin` QUALITY **92** (`:181`)** — "exactly one header row" per machine-readable
table (header duplication, not cell count); **64** (`:131`) covers cell-shape selftests.

Counter-example inside the same class: `mori-shokunin` **118** (`:970`) records as a *limit* that
"a nine-cell row passes" its own auditor — a sibling whose rule is weaker than the class, not a
precedent.

## Verdicts on chousa's 143 / 144 / 145

### 143 — `corpus/QUALITY.md:1046` (and its successor 145 at `:1052`)

Three conjuncts, judged separately:

1. **"no invertible answer key" — distinct construction, narrower coverage.** No sibling states
   the positive rule ("the printed digest is of the seed, not of the permutation"; the salted copy
   is rewritten, not suffixed). tsukuroi 90 and souji Q102 approach the same failure from the
   channel/hidden-case side. But 143's channel set is the four forgers a1/a2/a7/a5d —
   trailing-salt strip, `/proc/<ppid>/cmdline`, order-from-digest, detached append. It has **no
   uid/euid/groups variant, no override-environment variant, no fixture-fixed-value variant, and
   no mount-table/namespace variant**, all of which tsukuroi 90 names. **143 is weaker than
   tsukuroi 90 on channel enumeration and must not be absorbed as covering those channels.**
2. **"no receipt a child can append to" — weaker than kasegi R39.** 143/145 implement *detection*
   (`RECEIPT_LINES` trailer + exit-code authority) and 145's own Limits say "Line-count detection
   closes append; a forger that truncates the receipt is not detected by it". R39 forbids the
   append outright and demotes a two-run receipt to `report-only`. **Must not be absorbed as
   R39's equal.**
3. **"predicate bound to the exit code" — distinct.** tsukuroi 90's anchored-verdict-line rule is
   the same family (bind, never substring), but it binds a *report/answer line*; chousa binds the
   exit code plus a trailer. No sibling row states the exit-code-plus-trailer binding.

### 144 — `corpus/QUALITY.md:1050`

1. **"creates and deletes only its own run directory" — same mechanism as the siblings, and weaker
   on reuse.** `kama` **KQ112** (`:534`) requires the *opposite* policy: "refuses a `--work` that
   already holds files (exit 2, `work-reused`, nothing scored) and creates every scenario directory
   exclusively"; `kasegi` **R89** (`:494`) requires "a `--work .` run refuses". chousa's v5 accepts
   a pre-populated `--work` and reuses it. **144 is weaker than KQ112/R89 on the reuse/refusal leg
   and must not be absorbed as covering it** — and KQ112's refusal policy cannot be absorbed into
   144 without changing what `survived=yes` exercises (see the measured hole below).
2. **"maps every setup failure to its could-not-evaluate exit" — distinct.** No sibling row grades
   the *exit code* of the unwritable-`--work` and `--work`-is-a-file cases. KQ112/R89 grade the
   refusal, not its exit mapping. This conjunct is chousa's own, and its receipt
   (`unwritable_exit=2 file_exit=2`, no traceback) is the only measured instance in the fleet.
3. `souji` **Q86** (`:216`, FIFO/`O_NONBLOCK`/`fstat` write envelope) is adjacent but governs the
   tool's own output path, not a caller-named work directory.

### 145 — `corpus/QUALITY.md:1052`

145 is 143's frozen successor and is *narrower in wording* ("no verdict line a child can append"
instead of "no receipt a child can append to") with three recorded limits.

- **Weaker than kasegi R39** on the append leg (detect ≠ prevent) — same as 143.2.
- **Weaker than souji Q102** on the identity leg: Q102 requires an audit over inputs the counter
  does not hold plus a memorising control that must fail; 145's identity leg is a per-run interior
  statement with a positive control only.
- **Weaker than tsukuroi 90** on channel enumeration (same gap as 143.1).
- **Distinct from kengaku Q38** on surface: Q38 forbids a stored key in the *inner content leg*
  and requires the key be produced by executing the pinned source; 145 forbids a printed key in the
  *outer battery*. Neither implies the other. 145's concrete construction (interior statement, never
  a strippable suffix) is not stated by any sibling.
- **Distinct overall** on the trailer/exit-code binding (see 143.3).

### C2's S1 class (scan item (iii)) is outside 143–145 but is the weakest of the three

`corpus/evidence/round78/selfcheck.py:99–128` compares each `## Gates` row's cell count to the
header's and honours a lexical `correction: SKILL.md:<line>` escape. It does **not** declare the
logical-column mapping, does **not** name a blank owner/purpose/verdict cell, and does **not** gate
the append. `mado` 132 and `kaidoku` 117 hold the stronger, append-time form of the same class;
`kaidoku` 111 holds the population rule the instance check lacks. **The instance repair is a
narrower thing than those rows and must not be absorbed as their equal** — and chousa must not mint
a 146 restating 132/117.

## Measured hole in `work-contract.py` (reported as a limit, not a repair)

`work-contract.py:83` scores `ok = survived and rc_b == 2 and not traceback_b and rc_c == 2 and not
traceback_c` — **`rc_a` is never read**. Case A therefore passes for a battery that *refuses* the
pre-populated `--work` and scores nothing. Measured with a stub that refuses any non-empty `--work`
(kama KQ112 shape) and reads no matrix:

```
python3 -B corpus/evidence/round78/work-contract.py --battery <scratch>/stub-reuse-refusing-battery.py --work <scratch>/wc-probe
# exit: 0
CASE A rc=2 sentinel_survived=yes dir_exists=yes
CASE B rc=2 traceback=no stderr_first=stub: cannot create --work: [Errno 13] Permission denied…
CASE C rc=2 traceback=no stderr_first=stub: --work is not a directory
WORK_CONTRACT=PASS survived=yes unwritable_exit=2 file_exit=2
```

Receipt: `receipts/wc-probe.out` (exit 0), stub `receipts/stub-reuse-refusing-battery.py`. This is a
shortcut control that *meets* the target — the class `kama` **KQ118** (`:549`) rejects ("a committed
shortcut control that skips the claimed work … the counter's cheapest do-nothing control meets the
target"). The instrument is frozen at `93e0432e` and C1's predicate comes from `forge-battery.py`,
not from this control, so this is a **post-freeze limit of a supporting receipt**, never a repaired
predicate and never a defect of the frozen sentence.

## Risks

- Absorbing tsukuroi 90 / kasegi R39 / mado 132 as if chousa 143–145 were their equal would
  silently widen the claim: none of the three covers uid/env/mount-table channels, append
  prevention, or append-time gating.
- Absorbing kama KQ112's refusal policy into 144 would make Case A pass without exercising the run
  path *by design* rather than by accident.
- The scan's negative results ("no sibling row for X") are bounded by its declared regex set; they
  are scope statements, not proofs of absence.

## Verification

| command | exit | receipt |
|---|---|---|
| `python3 -B scan.py --fleet /home/vgpnk/Projects/shokunin` | 0 | `receipts/scan.out` |
| `python3 -B scan.py --fleet <scratch>/red-fleet` | 1 | `receipts/red1.out` |
| `python3 -B scan-red2.py --fleet /home/vgpnk/Projects/shokunin` | 1 | `receipts/red2.out` |
| `python3 -B corpus/evidence/round78/work-contract.py --battery <stub> --work <scratch>` | 0 | `receipts/wc-probe.out` |
| `sha256sum -c SHA256SUMS` (in `receipts/`) | — | `receipts/SHA256SUMS` |
