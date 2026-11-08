# R91ReviewerC1 — C1 (operability) sentence-vs-code review

Seat `R91ReviewerC1` (leaf). Lane `chousa-shokunin`, round 91. Claim under review: **C1** only.
Base `265b8633b7e5d1da49da6fb948df9707373fb15c`; freeze `F3 = 4d00d7519290569879f853d7122b82a927cda1f3`;
carrier `C3 = 67954adc599bd605705d94a1ea7abb582491a907`. The attacked tree is a `git clone --shared` of the lane at
C3 under `/fast/scratch/hyaku/chousa-r91/R91ReviewerC1/repo` (scratch deleted at yield; every input and output
cited below is copied into `.ufo/waves/round-91/w1/R91ReviewerC1-receipts/`).

Method: read `corpus/evidence/round91/claims.md` C1 (clauses 1–8 + named limits) and `control-driver-r91.py`
line by line, then built the smallest fixture per clause. All fixtures are synthetic roots under my scratch dir;
the driver is the frozen one (`sha256 49102204fa9698df97f2f8ac467468ee57dff1a358e934d52654821cd880b40c`, identical
at F and C3). No network, no installs, no tool changes. Exact argv for every fixture, with the scratch paths
used, is in `R91ReviewerC1-receipts/F-exact-commands.txt`.

## Control run on the frozen tree

| # | command | exit | observed |
|---|---|---|---|
| R0 | `python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --rev 4d00d751… --receipts-rev 67954adc… --work <scratch>/work` (cwd = C3 clone) | **0** | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=6 CONTROL_DRIVER_R91=PASS`, `RECEIPT SELF_PIN OK rev=4d00d751… receipts_rev=67954adc…`, `RECEIPT PINS OK 6/16 pinned files byte-identical` |
| R1 | the same command **verbatim as frozen**, with no `--work` | **2** | `error: the following arguments are required: --work` |
| R2 | `python3 -B corpus/evidence/round91/control-forgeries-r91.py --work <scratch>/forgery-work` (cwd = C3 clone) | **0** | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` |

Receipts: `R91ReviewerC1-receipts/F1-canonical-with-work.txt`, `F1-frozen-command-verbatim.txt`,
`F7-forgeries-real-r90.txt`. K3: after R0, `git status --porcelain` on the receipts dir, driver, expected.tsv and
pins is empty (`K3-receipts-untouched.txt`) — `verify` itself writes only under `--work`.

Identity: the scoring bytes in the lane working tree equal the C3 clone byte for byte (driver, expected.tsv,
instrument-pins.txt, all six scored receipts; `identity-lane-vs-C3.txt`), and all 16 pin rows match the on-disk
sha256 in the clone (`F6-pins-16-disk.txt`). The canonical result therefore transfers to the lane tree.

**Bottom line:** the six counters do print on C3 — but only with a `--work` argument the frozen sentence does not
name, and clauses 1, 2, 4, 5, 6, 7 and 8 describe the code more broadly than it is. C1 is fired as written.

---

## Findings by severity

### F1 — the frozen command is not runnable (blocks the literal K1 predicate) — HIGH

Clause: the C1 sentence's command. `corpus/evidence/round91/claims.md` C1 and
`.ufo/waves/round-91/claims.json` `C1.counting_command` both print:

```
python3 -B corpus/evidence/round91/control-driver-r91.py verify --root . --repo . --rev F --receipts-rev C
```

`control-driver-r91.py` declares `--work` with `required=True` (argparse). Running the frozen command in the C3
clone exits **2** with `the following arguments are required: --work`; it never reaches the predicate. With
`--work <scratch>/work` added it exits 0 with exactly the claimed counters (R0).

- Command: verbatim above, cwd = C3 clone. Exit **2**.
- Receipt: `R91ReviewerC1-receipts/F1-frozen-command-verbatim.txt` (plus the working form in
  `F1-canonical-with-work.txt`).
- Amendment the L1 must record: append `--work <scratch work dir>` to the C1 command in `claims.md`,
  `claims.json` (`sentence`, `counting_command`) and the wave text, and state that the work dir must lie outside
  `controls/receipts/`. A9 (`F-fixtures-A1-A9-A11-A12.txt`) shows `verify` prints PASS while writing
  `fresh-c1-x.out` under a receipts subdir when `--work` names one, so the amendment must also carry K3's
  "outside the receipts" condition.

### F2 — `CONTROL_DRIVER_R91=PASS` is not gated on `EXACT_OK` — HIGH

Clause 1 / the field conjunction. In `main()` the verdict is

```
passed = (findings == 0 and committed_ok == len(rows) and pin_ok == len(rows)
          and fresh_ok == len(rows))
```

(`control-driver-r91.py:404-405`); `exact_only` (the post-fresh re-read of the committed receipts,
`:396-403`) is **not** in it. Fixture A15: committed `receipts/b.txt` is invalid (`B=0`), row `a`'s fresh run
overwrites it with a valid receipt before row `b` is read, row `b`'s fresh run restores the invalid committed
bytes, and the re-read counts 1/2.

- Command: the `A15` line in `R91ReviewerC1-receipts/F-exact-commands.txt` (cwd = the fixture; no `--repo`).
  Exit **0**.
- Observed: `COMMITTED_OK=2/2 EXACT_OK=1/2 PIN_OK=2/2 FRESH_OK=2/2 … CONTROL_DRIVER_R91=PASS`.
- Receipt: `R91ReviewerC1-receipts/F-fixtures-A10-A15.txt` (line `A15-exact-gap-no-repo`) and
  `F-fixture-inputs.txt` §A15.
- Same under the full `--repo` form in A10a: `EXACT_OK=1/2` with `CONTROL_DRIVER_R91=PASS` (see F3).
- Amendment: either include `exact_only == len(rows)` in `passed`, or state that `EXACT_OK` is a diagnostic
  re-read and `PASS`/exit 0 are gated on `COMMITTED_OK`, `PIN_OK`, `FRESH_OK` only. As frozen, the sentence's
  "prints PASS … with EXACT_OK=6/6" is not enforced by the token or the exit code.

### F3 — clause 1's read order is false; a committed receipt can be scored from a fresh run — MEDIUM-HIGH

Clause 1 says "every receipt is read from disk before any fresh run". The verify loop reads row *i*'s receipt and
then runs row *i*'s instrument in the same iteration (`control-driver-r91.py:330-369`), so rows *2…n* are read
after row *1*'s fresh run. Fixture A10 (two rows; `a`'s command overwrites `receipts/b.txt`; `b`'s command prints
`B=1`):

- A10a, **with `--repo`**, `b`'s fresh run restores the committed bytes after `b` was read:
  `RECEIPT b OK committed+exact+pin+fresh`, `RECEIPT SELF_PIN OK …`, `COMMITTED_OK=2/2 EXACT_OK=1/2 … CONTROL_DRIVER_R91=PASS`,
  exit **0**. The committed `b.txt` is `B=0`/`marker=committed`; the bytes row `b` validated were row `a`'s fresh
  output. The final bytes equal the blob ("final b.txt equals committed bytes: True"), so SELF_PIN passes — and
  the exact-leg re-read that did see the invalid committed bytes (`EXACT_OK=1/2`) is not gated (F2).
- A10b, with `--repo`, no restore: `SELF_PIN FINDING SELF_DRIFT …/receipts/b.txt@<Y>`, exit **1**. SELF_PIN is
  the real cross-row protection, not clause 1's ordering.
- A10c, **without `--repo`**: `COMMITTED_OK=2/2 … CONTROL_DRIVER_R91=PASS`, exit **0**; after the run `b.txt`
  says `B=1` — the committed `B=0` file was never read. This is the K4 class "a committed receipt is not read",
  reachable in the documented no-`--repo` form.
- Commands/receipts: `F-fixtures-A10-A15.txt` lines `A10a/A10b/A10c`; inputs in `F-fixture-inputs.txt` §A10.
- Amendment: replace clause 1's first half with "each row's receipt is read from disk immediately before that
  row's own fresh run; the driver itself writes only under `--work`", and add "with `--repo`, `SELF_PIN` compares
  every `receipts/*.txt` to its blob at `--receipts-rev` after the fresh legs". The landing six rows do not write
  receipts, so the landing count is not moved — but the stated mechanism is not the one that protects it.

### F4 — clause 5's "the first file … names as its script" is not the code's rule — MEDIUM-HIGH

`instrument_rel()` (`control-driver-r91.py:119-128`) takes the first whitespace token that, after `@ROOT@`
substitution, **is absolute and ends `.py` or `.sh`**. It does not know which token is executed, and it does not
substitute `@WORK@`.

- A5: row `bash @ROOT@/fx-tool` (script without a suffix), the file listed and hash-correct in pins →
  `RECEIPT PINS FINDING INSTRUMENT_UNPINNED:c1-x`, exit **1**. The sentence reads this as satisfied (the first
  file the command names as its script is listed and its sha matches), so the code refuses a state the sentence
  reads as accepted.
- A13: row `cat @ROOT@/data.py && bash @ROOT@/real.sh` → `instrument_rel` returns `data.py` (a `cat` operand); the
  executed script `real.sh` is unpinned. Replacing `real.sh` with a same-output stub (sha `41d483d6…` →
  `579d4abd…`) still prints `CONTROL_DRIVER_R91=PASS`, exit **0**. This is the round-90 R3 "instrument stub"
  class, bypassed by putting a data operand first; named limit 3 says "the pin names the script a row's command
  mentions first", which is not this rule — `data.py` is not a script and `real.sh` is the only script.
- Receipts: `F-fixtures-A1-A9-A11-A12.txt` `A5`; `F-fixtures-A10-A15.txt` `A13a/A13b`; inputs in
  `F-fixture-inputs.txt` §A5/§A13.
- Amendment: state the lexical rule — "the pinned file is the first whitespace token in the instrument that is
  absolute after `@ROOT@` substitution and ends `.py` or `.sh`, whether executed, a data operand or a redirect
  target; the executed script may be unpinned; a script without one of those suffixes is `INSTRUMENT_UNPINNED`" —
  and extend named limit 3 to cover a data operand that precedes the executed script.
- Landing note: the six committed rows escape this only because each first script-suffixed token is its executed
  script; `c1-harm`'s `@WORK@/harm/base-tool.py` is skipped solely because `instrument_rel` does not substitute
  `@WORK@` (incidental, not a stated rule).

### F5 — clause 6's receipt test is a literal substring, not the header parse — MEDIUM-HIGH

Clause 6: "a `.txt` file that parses as a receipt (a `# case=` header) and that no expected row scores is
`UNSCORED_RECEIPT`". The scan tests `if "# case=" not in body` (`control-driver-r91.py:378`) while the driver's
own parser is `header_multi()` (`:102-114`, any `# \(key)=(value)` with a stripped key).

- Committed-at-carrier evasion (full `--repo` form): `receipts/evil.txt` with `#  case=evil` (two spaces) is
  parsed by `header_multi` as `{'case': ['evil'], …}`, has no literal `# case=` substring, is committed at
  `--receipts-rev`, and the run prints
  `COMMITTED_OK=1/1 … CONTROL_DRIVER_R91=PASS`, exit **0**, with `UNSCORED_RECEIPT` absent. SELF_PIN passes
  because the file is in the carrier blob. Command/revs in `F-fixtures-unscored-committed.txt`; inputs in
  `F-fixture-inputs.txt` §C1-unscored.
- False positive (no `--repo`): `receipts/raw.txt` containing the off-column text `note # case=fake here` is
  flagged `RECEIPT raw FINDING UNSCORED_RECEIPT`, exit **1**, although `header_multi(raw) == {}` — the sentence
  reads this file as raw evidence, not a receipt.
- Receipts: `F-fixtures-A1-A9-A11-A12.txt` `A8a/A8b`; `F-fixtures-unscored-committed.txt`.
- Amendment: define the receipt test as "`header_multi(text)` contains a non-empty `case` key" and use that test
  in the scan, or state the literal substring and its `#  case=` false negative / off-column false positive. The
  landing carrier has no such file, but the clause's stated mechanism is what a carrier forgery would target.

### F6 — the pin table is not blob-bound; only 6 of 16 rows are disk-checked — MEDIUM

Clause 7 / clause 5. `pin_report()` checks on disk only the distinct row instruments plus `controls/expected.tsv`
(6 files) and prints `checked/len(pins)` — the canonical line is `RECEIPT PINS OK 6/16 pinned files byte-identical`
(`PINNED_FILES=6`). `self_pin()` hashes every row of the pins file at `--rev` (`pin_at_rev`, `:242-253`) but never
hashes **the pins file itself** against a blob. `read_pins()` is a dict, so duplicate rows are last-wins.

- A11: a copy of the C3 tree with `instrument-pins.txt` rewritten from 16 rows to 7 (the 6 wanted files plus the
  driver; `claims.md`, `claims.json`, `plans/round-91.md`, the selftest receipt and the four other r91
  instruments dropped) prints `RECEIPT PINS OK 6/7 … RECEIPT SELF_PIN OK … COMMITTED_OK=6/6 … PINNED_FILES=6
  CONTROL_DRIVER_R91=PASS`, exit **0**. The pins file on disk differs from its blob at F and nothing notices.
- B1/B2: `tool.sh` pinned twice, wrong hash first then correct → PASS (`PINNED_FILES=2`); correct first then wrong
  → `INSTRUMENT_PIN_MISMATCH:tool.sh`, exit 1. The wrong first row is silently ignored.
- Receipts: `F6-pins-table-canonical.txt`, `F6-pins-trimmed.txt`, `F6-duplicate-pins.txt`, `F6-pins-16-disk.txt`.
- Amendment: state the exact blob-bound scoring set ({driver, `controls/expected.tsv` at `--rev`;
  `controls/receipts/*.txt` at `--receipts-rev`}), add a named limit "`instrument-pins.txt` is not self-pinned;
  only the rows it contains are hashed (at `--rev`); deleting pin rows for files no row uses is invisible; a
  duplicated path is last-wins", or pin the pins file in a successor. The 10 non-wanted pins are checked at
  `--rev` only; a dirty on-disk copy of any of them is invisible.

### F7 — clause 8's "unchanged r90 driver" is not enforced by the battery — MEDIUM

`control-forgeries-r91.py:26` resolves `R90` to `corpus/evidence/round90/control-driver-r90.py` inside the tree
and runs it; nothing hashes or pins that file (`grep -c control-driver-r90 instrument-pins.txt` = 0). With r90
replaced by `import sys; sys.exit(0)`, the battery still prints

```
FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass
```

exit **0** — the exact frozen clause-8 line, while the "prior driver" is a stub. At landing the adjective is
factually true (`git diff base..C3 -- corpus/evidence/round90/control-driver-r90.py` is empty), but the instrument
cannot tell, and the lane working tree's r90 is unbound.

- Receipt: `F7-forgeries-stub-r90.txt` (stub content + output); history/pin evidence inline.
- Amendment: pin `corpus/evidence/round90/control-driver-r90.py` and have the battery check it, or add a named
  limit "the prior leg runs the r90 file at that tree path, unbound; `PRIOR_ACCEPTED` measures whatever is there".

### F8 — header/body lexing: indented `#` lines are body, not headers/comments — MEDIUM-LOW

`header_multi()` recognises only lines beginning exactly `# ` at column 0 (`:106`); `body_tokens()` skips only
lines beginning `#` at column 0 (`:92`). Consequently an indented `#` line is body text. Full `--repo` fixture:
the committed receipt carries valid `# exit=0` headers, an indented ` # exit=1`, and `   # FOO=1` as the only
source of the required token:

- `C1-indented-lines-full-form`, exit **0**: `COMMITTED_OK=1/1 EXACT_OK=1/1 PIN_OK=1/1 FRESH_OK=1/1
  CONTROL_DRIVER_R91=PASS`, no `HEADER_DUPLICATE`, no `TOKEN_MISSING`; SELF_PIN OK because the file is committed.
- No-`--repo` siblings: A7 (` # exit=1` beside `# exit=0`) PASS; A6a (`   # FOO=1`) PASS; A6b (column-0
  `# FOO=1`) FAIL with `TOKEN_MISSING:FOO`.
- Receipts: `F-fixtures-indented-lines.txt`; `F-fixtures-A1-A9-A11-A12.txt` `A6a/A6b/A7`.
- Amendment: state the lexical rule in clauses 2 and 4: a header is a column-0 `# ` line with `=`; any line whose
  first character is `#` is neither body nor header; any line with leading whitespace is body text, so an
  indented `# ...` line can supply a whole required token and does not count as a duplicate header.

### F9 — integer-value grammar is unstated; `+0` refused, ` 0`/`-0`/`00` accepted — LOW

`INT_RE = -?[0-9]+` (`:47`); `check_headers` strips the header value then fullmatches. A2: `# exit=+0` with row
exit 0 → `EXIT_MISMATCH:+0!=0`, exit **1**. A2b: `# exit= 0` → PASS, exit **0**; `-0` and `00` also pass.
The sentence only says the value "equals the row's", which under numeric equality would accept `+0`.

- Receipts: `F-fixtures-A1-A9-A11-A12.txt` `A2/A2b`.
- Amendment: state the canonical form — after stripping, the value must fullmatch `-?[0-9]+` and its integer must
  equal the row's (so `+0` is refused, ` 0`/`-0`/`00` accepted).

---

## The six assigned attempts

| attempt | fixture / command | observed | verdict |
|---|---|---|---|
| 1. duplicate `# expected_exit=` with the **same** value | A1, `verify` on `fx/dup-eq` | `HEADER_DUPLICATE:expected_exit=0`, exit 1 | **held** — "exactly once" is honoured for column-0 headers (association with F8) |
| 2. a row whose command names two scripts (`bash first.sh && python3 real.py`) | A3 / A3b | pinning `first.sh` PASSes (unpinned `real.py` executes); pinning only `real.py` → `INSTRUMENT_UNPINNED:first.sh`, exit 1 | **held as F3-narrowed** — the first script-suffixed token is pinned; named limit 3 covers the second, but see F4 for data operands and suffixes |
| 3. pinned script reads a second, unpinned data file | A4 | `tool.sh` pinned, `data.txt` unpinned; editing `data.txt` (EXTRA=1→2) leaves `CONTROL_DRIVER_R91=PASS` | **held** — named limit 5 exactly |
| 4. `PINNED_FILES=6/16` | R0 canonical | `RECEIPT PINS OK 6/16 pinned files byte-identical`, `PINNED_FILES=6` | **not a clause-5 falsification** — clause 5 scopes to the rows' instruments + expectations (6); recorded as F6 (the other 10 are rev-checked only; the table itself is unbound) |
| 5. `self_pin` without `--repo` | A12 | PASS, exit 0, no `SELF_PIN` line at all; no blob comparison | **held for the frozen command** (it passes `--repo`); if clause 7 is read unconditionally, amend it: SELF_PIN and every blob comparison exist only with `--repo` |
| 6. `# exit=` with a leading `+` or spaces | A2 / A2b | `+0` → `EXIT_MISMATCH:+0!=0` exit 1; ` 0` → PASS exit 0 | **refused for `+0`, accepted for spaces**; recorded as the F9 grammar narrowing |

## Kill-rule checks

- **K1** — the literal frozen command is not met (F1, exit 2). The predicate's *content* is met at C3 with
  `--work` (R0: all four counters 6/6, exit 0; SELF_PIN names F and C).
- **K2** — held for the committed r90: R2 prints `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`, exit 0.
  F7 shows the prior leg is unbound, not that the committed discrimination is wrong.
- **K3** — held after R0: the receipts dir, driver, expected.tsv and pins are byte-unchanged (`git status` empty).
  A9 shows the invariant depends on `--work` being outside `controls/receipts/`.
- **K4** — the individual skips are refused: B3 `TOK=10` under required `TOK=1` → `TOKEN_DETACHED:TOK=10` plus
  `PREDICATE_SHORT:NUM=0<1`, exit 1; B4 missing receipt → `MISSING_RECEIPT` + `PIN_MISSING`, exit 1. But F2/F3
  show the *pass* can still be printed while its own exact re-read disagrees (A10a `EXACT_OK=1/2`, A15
  `EXACT_OK=1/2`), and A10c shows a committed receipt never read without `--repo`.

## Named limits — honoured vs falsified

1. coherent joint edit survives — **honoured as disclosed**; it is the umbrella over F3/F4/F6/F7 (each fixture
   needs a harness-level edit), but none of those fixtures edits a pin to fake a hash.
2. whole-token matching binds one field per token — **honoured** for tokens (`B3`); F8 is about which lines are
   body, not about substring matching.
3. the pin names the script the command mentions first; a second unpinned script is not seen — **falsified as
   worded**: F4 (a data operand can be named first; a suffixless executed script is refused; the executed script
   can be unpinned and substituted).
4. the self-pin detects a moved byte inside a named commit, not rewritten history — **honoured** (self_pin reads
   `git show <rev>:<path>`).
5. the driver cannot see a pinned script that reads data outside its own bytes — **honoured** (A4).

## Residual risk / verification gaps

- All fixtures are synthetic roots; none of the landing six rows exercises F4 (each row's first script-suffixed
  token is the executed script; the `c1-harm` `@WORK@/.../base-tool.py` token is skipped only because
  `instrument_rel` does not substitute `@WORK@`). The findings are about the stated rules, not a moved landing
  row.
- F3's with-`--repo` FAIL path (A10b) shows SELF_PIN is the real cross-row backstop; the restore variant (A10a)
  passes because SELF_PIN compares the final bytes, not the bytes read. Only a read-time comparison or per-row
  hashing would close it.
- Without `--repo`, `verify` performs no blob comparison at all (A12) and still prints PASS; the frozen command
  supplies `--repo`, so this is a scope note, not a landing kill.
- The 10 non-wanted pin rows are rev-checked only; a dirty on-disk copy of `claims.md`, `plans/round-91.md`, the
  selftest receipt or the four other r91 instruments is invisible (F6). The pins file itself is unbound.
- The prior leg of clause 8 is unbound (F7); at landing it is historically unchanged, but the battery cannot
  detect substitution.
- No network was used; no tool was installed or upgraded; no host service or sysctl was touched; no lane or fleet
  commit was made. Scratch (`/fast/scratch/hyaku/chousa-r91/R91ReviewerC1`) was deleted at yield; the receipts
  below are the durable copies.

## Amendments the L1 must record in `plans/round-91.md`

1. **Command**: add `--work <scratch dir outside controls/receipts/>` to the C1 command in `claims.md`,
   `claims.json` (`sentence`, `counting_command`) and the wave text (F1).
2. **Clause 1 read order**: "each row's receipt is read from disk immediately before that row's own fresh run;
   the driver itself writes only under `--work`; with `--repo`, `SELF_PIN` compares every `receipts/*.txt` to its
   blob at `--receipts-rev` after all fresh legs" (F3).
3. **PASS gating**: either gate `passed` on `exact_only == len(rows)` or state that `EXACT_OK` is diagnostic and
   `PASS`/exit 0 are gated on `COMMITTED_OK`, `PIN_OK`, `FRESH_OK` (F2).
4. **Clauses 2 and 4 lexical rule**: header = column-0 `# ` line with `=`; any line starting `#` at column 0 is
   not body; any line with leading whitespace is body text, so an indented `# ...` line can carry a whole token
   and is not a duplicate header (F8).
5. **Clause 2 integer grammar**: after stripping, the value must fullmatch `-?[0-9]+` and equal the row's integer
   (`+0` refused; ` 0`/`-0`/`00` accepted) (F9).
6. **Clause 5**: the pinned file is the first whitespace token that is absolute after `@ROOT@` substitution and
   ends `.py` or `.sh`, whether executed, a data operand or a redirect target; the executed script may be
   unpinned; a suffixless script is `INSTRUMENT_UNPINNED`; extend named limit 3 accordingly (F4).
7. **Clause 6**: the receipt test is `header_multi(text)` containing a non-empty `case` key (the literal `# case=`
   substring evades on `#  case=` and false-positives on off-column mentions) (F5).
8. **Clause 7**: name the exactly blob-bound set ({driver, `controls/expected.tsv` at `--rev`;
   `controls/receipts/*.txt` at `--receipts-rev`}) and add a named limit for the unbound `instrument-pins.txt`
   (not self-pinned; only listed rows are hashed at `--rev`; only the 6 wanted files are disk-checked; duplicate
   rows are last-wins) (F6).
9. **Clause 8**: the prior leg runs `corpus/evidence/round90/control-driver-r90.py` at the tree path, unbound by
   any pin; `PRIOR_ACCEPTED=6/6` measures whatever file is there (F7).
10. **Clause 7 without `--repo`**: SELF_PIN and all blob comparisons exist only with `--repo` (A12); state the
    condition if the clause is meant to be unconditional.

VERDICT: R91ReviewerC1 C1 fired — the frozen command omits the required `--work` (exit 2) and clauses 1/2+4/5/6/7/8 are wider than control-driver-r91.py (read order and PASS gating, lexical header/body, first-token pin, substring unscored scan, unbound pin table, unbound r90 prior), while the six counters themselves print `CONTROL_DRIVER_R91=PASS` with the frozen field values on C3 when `--work` is supplied.
