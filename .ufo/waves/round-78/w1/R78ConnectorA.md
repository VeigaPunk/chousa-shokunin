# R78ConnectorA — sibling-overlap scan (leaf, read-only)

**Seat:** R78ConnectorA · **Wave:** round-78/w1 · **Lane:** chousa-shokunin
**Scope:** does another lane already hold a criterion for (i) a harness printing an invertible
answer key or a strippable subject identity, (ii) a receipt a child can append to, (iii) a
self-assessment registry row whose cell count misses its header — and which of chousa's
143/144/145 are weaker than a sibling rule, which are distinct.
**Writes:** `.ufo/waves/round-78/w1/R78ConnectorA/` (receipts + `sibling-overlap-scan.md`) and
this file. Lane tree, `corpus/`, `tools/`, sibling lanes and the fleet repo untouched.
**Tooling record:** none installed (no pacman, no `uv`, no PATH writes); `python3 -B` + `sha256sum`.
**Frozen set read first:** `corpus/evidence/round78/claims.md` (C1 forge-battery v5, C2 selfcheck,
instruments at `93e0432e`); QUALITY 141–145, 137, 29, 36.

## Answer: yes for all three

Closest rows, with the quote each carries (line = `corpus/QUALITY.md` in that lane):

| class | lane | id | line | quote |
|---|---|---|---|---|
| i | tsukuroi | **90** (R42-OBSERVED-CHANNEL) | 177 | "A counter that holds no answer key is scored against every channel through which the scored code can see it is being watched, and a verdict binding matches an asserted line, not a mention" |
| i | kengaku | **Q38** | 1027 | "a content leg's verdict key is produced by executing the pinned source over generated end states and is stored nowhere in the counter" |
| i | souji | **Q102** | 258 | "whose fixtures leak the case (directory names, commit messages, fixed digests) does not discriminate a tool that memorises them" |
| i | mori | **8** | 16 | "if any encodes which scenario is running, there is a sniffer channel" |
| ii | kasegi | **R39** | 351 | "one invocation writes it once and nothing appends to it or edits it afterwards" |
| ii | kaidoku | **120** (→127) | 193 | "a receipt never grants a write destination" |
| ii | kama | **KQ106** | 521 | "binds the answering process by a value the tool cannot write" |
| iii | mado | **132** | 943 | "A registry row carries the table's own column count, and the append is gated by the table's census, never by the shape of the row above it by eye" |
| iii | kaidoku | **117** | 190 | "a table census declares the logical-column mapping and accepts an over-count row only for named filed paths" (and "names a blank … owner cell instead of passing it") |
| iii | kaidoku | **111** | 180 | "a declared inventory is not its own population" |
| iii | tsukuroi | **92** | 181 | "exactly one header row" |
| — | kama | **KQ112** | 534 | "refuses a `--work` that already holds files (exit 2, `work-reused`, nothing scored)" |

## Which of 143/144/145 are weaker, and which are distinct

**143 (QUALITY.md:1046)**
- *Weaker than tsukuroi 90* on channel coverage: tsukuroi demands per-channel "watched" variants for
  override environment, uid/euid/groups, fixture fixed values and namespace traces; chousa's four
  forgers (a1 salt-strip, a2 `/proc/<ppid>/cmdline`, a7 order-from-digest, a5d detached append)
  cover none of the identity/env/mount-table channels. **Do not absorb as equal.**
- *Weaker than kasegi R39* on append: 143 says "no receipt a child can append to" but implements a
  line-count trailer (detection); R39 forbids the append and demotes a two-run receipt. **Do not
  absorb as equal.**
- *Distinct:* the positive construction "the printed digest is of the seed, not of the permutation;
  the salted copy is rewritten rather than suffixed" exists in no sibling row, and the
  exit-code-plus-trailer binding is not tsukuroi 90's anchored-line rule.

**144 (QUALITY.md:1050)**
- *Weaker than kama KQ112 / kasegi R89* on the reuse leg: v5 accepts a pre-populated `--work`,
  whereas KQ112 refuses it and R89 requires "`--work .` refuses". **Do not absorb as equal**, and do
  not absorb KQ112's refusal policy into 144 — it would satisfy `survived=yes` without exercising
  the run path (measured below).
- *Distinct:* the could-not-evaluate exit mapping for an unwritable `--work` and a `--work` that is
  a regular file (`unwritable_exit=2 file_exit=2`, no traceback) is graded by no sibling row.

**145 (QUALITY.md:1052)**
- *Weaker than kasegi R39* (append: detect ≠ prevent), *weaker than souji Q102* (no hidden-case
  audit, positive control only), *weaker than tsukuroi 90* (channel set).
- *Distinct from kengaku Q38*: Q38 forbids a stored key in the inner content leg and requires it to
  be produced by executing the pinned source; 145 forbids a printed key in the outer battery.
  Neither implies the other; 145's interior-statement construction is stated nowhere else.
- *Distinct* on the trailer + exit-code binding.

**C2's S1 (scan item iii, outside 143–145)** — `selfcheck.py:99–128` compares row cells to the
header and honours a lexical `correction: SKILL.md:<line>`; it declares no logical-column mapping,
names no blank owner cell, and gates no append. mado 132 / kaidoku 117 hold the stronger append-time
form; kaidoku 111 holds the population rule. **The instance repair must not be absorbed as their
equal, and no 146 should restate them.**

## Measured limit found while answering (report, do not repair)

`work-contract.py:83` never reads `rc_a`: `ok = survived and rc_b == 2 and not traceback_b and
rc_c == 2 and not traceback_c`. A battery that *refuses* a pre-populated `--work` (KQ112 shape) and
scores nothing passes Case A.

```
python3 -B corpus/evidence/round78/work-contract.py --battery <scratch>/stub-reuse-refusing-battery.py --work <scratch>/wc-probe
# exit: 0
CASE A rc=2 sentinel_survived=yes dir_exists=yes
CASE B rc=2 traceback=no stderr_first=stub: cannot create --work: [Errno 13] Permission denied: …
CASE C rc=2 traceback=no stderr_first=stub: --work is not a directory
WORK_CONTRACT=PASS survived=yes unwritable_exit=2 file_exit=2
```

Receipt `R78ConnectorA/receipts/wc-probe.out`; stub `receipts/stub-reuse-refusing-battery.py`
(sha256 `68ce0d22…cbe0`). Class: kama KQ118 — a shortcut control that skips the claimed work and
meets the target. C1's predicate is `forge-battery.py`'s, so this is a **post-freeze limit of a
supporting control**, never a repaired predicate and never a defect of the frozen sentence.

## Verification (all fail-closed, exits recorded)

| command | exit | receipt |
|---|---|---|
| `python3 -B scan.py --fleet /home/vgpnk/Projects/shokunin` | 0 → `SIBLING_SCAN=PASS classes_hit=3/3 zero_hit=none unverified=0` | `receipts/scan.out` |
| same over a two-lane red fleet (class ii absent) | 1 → `SIBLING_SCAN=FAIL classes_hit=2/3 zero_hit=ii` | `receipts/red1.out` |
| `python3 -B scan-red2.py --fleet …` (fabricated quote) | 1 → `QUOTE=UNVERIFIED … KQ999` | `receipts/red2.out` |
| `python3 -B corpus/evidence/round78/work-contract.py --battery <stub> --work <scratch>` | 0 | `receipts/wc-probe.out` |

The scan is shown able to fail on both limbs (zero-hit class, unresolved quote), so the green run is
a result and not a shape. Every cited quote is `QUOTE=VERBATIM` in `scan.out`. Scratch
`/fast/scratch/hyaku/chousa-r78/R78ConnectorA/` deleted at yield; receipts copied first.

## Limits of this scan

- "No sibling row for X" is bounded by the declared regex sets in `receipts/scan.py`; it is a scope
  statement, not proof of absence.
- Row strength was judged by reading each cited row whole, not by keyword hit alone; rows not cited
  (e.g. kagi QM*, tabi 55/56, tameshi 93) were inspected only at head level.
- No sibling lane's `SKILL.md` registry or evidence tree was scored; only `corpus/QUALITY.md` was in
  scope.
