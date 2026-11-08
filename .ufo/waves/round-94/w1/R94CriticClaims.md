# R94CriticClaims — round-94 wording attack (lane chousa, wave w1)

Seat: critic. Scope: compare every noun/quantifier of the three frozen claim sentences with what the three
instruments and their batteries enforce. No lane edit, no production edit, no integration, no other runtime
invoked, no fleet/state write.

**Audit target (as assigned):** claims frozen at F `41038ed7c40cffc4cf86d649a6ba433c4b9eec1a`, carried by
C `352924bbea624caf3771ef291be98fd4ec679dda` (F + six control receipts + the 34-row pins table).

**Revision identity (must be read before any verdict).** During this audit the lane advanced past the
assigned carrier to a second freeze and carrier, and the frozen artefacts were amended:

| revision | commit | what it is |
|---|---|---|
| F | `41038ed7` | the freeze I audited |
| C | `352924bb` | the carrier I audited (34-row table, `forgeries-r94.py` = `f7dd794e`) |
| F2 | `4cbaed6cc15f4cd1008b6ab6294ffe6894f3dfec` | "round-94: freeze F2 — wave-forced amendments (Unicode punctuation class + CJK control, TAIL_OWNER_UNMAPPED, dead code removed, s1 dropped, prior acceptance measured), measurement wrapper" |
| C2 | `f276d7fb890f6f3057cc85aacd18f5a735e0d975` | "round-94: carrier C2 — six receipts emitted at F2 and the 35-row role-bearing pins table" |

Consequences measured: F2 rewrites `.ufo/waves/round-94/claims.md` (C2 and C3 sections cite sibling findings;
C1 text unchanged), rewrites all six receipts, repins every instrument, and changes the pins table to 35 rows
(14 covered + 21 driver). The F/C identity is therefore not the lane's live identity; §4 maps each fire to
the F2 amendment. Everything measured below at F/C is labelled as such; the two C2 spot-checks I ran are
labelled C2.

Trees used:

- `S=/fast/scratch/hyaku/chousa-r94/R94CriticClaims`
- `$S/repo` — `git clone --shared`, checkout `352924bb` (C); `git -C "$S/repo" rev-parse --show-toplevel`
  printed `$S/repo`.
- `$S/base` — `git clone --shared`, checkout `0f3f84d`; `git -C "$S/base" rev-parse --show-toplevel`
  printed `$S/base`.
- Fixtures under `$S/c1/*`, `$S/c2/*`, `$S/c3/*`, `$S/basework*`; fresh-leg `--work` always outside the
  tree being scored (an in-root `--work` makes `gate-records-r89.py` print `SETUP 0/1`; my first base run
  did exactly that and was discarded as a harness error, not a finding).
- Installations this round: none (system `python3`, `git`).
- Mutation fixtures are copied with the receipts (`R94CriticClaims-c1mut.py`, `R94CriticClaims-c1base.py`,
  `R94CriticClaims-c2-curation-r94-nopunct.py`) so every mutated run is reproducible from the copied files;
  scratch is deleted before yield.

## 0. Predicates measured (baseline before the wording attack)

At the assigned carrier C:

| claim | command (from the frozen claim) | rc | receipt | observed line |
|---|---|---|---|---|
| C1 verify | `python3 -B corpus/evidence/round94/control-driver-r94.py verify --root . --repo . --rev 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a --receipts-rev 352924bbea624caf3771ef291be98fd4ec679dda --work <scratch>` | 0 | `R94CriticClaims-c1-verify.txt` | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS` |
| C1 battery | `python3 -B corpus/evidence/round94/forgeries-r94.py --root . --repo . --rev <F> --receipts-rev <C> --work <scratch>` | **1** | `R94CriticClaims-c1-forgeries.txt` | **`FORGERIES=FAIL FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass`** — fire F7 |
| C2 counter | `python3 -B corpus/evidence/round94/curation-r94.py --root .` | 0 | `R94CriticClaims-c2-curation.txt` | `... LEGS_MEASURED=16/16` / `VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=17/17` / `CURATION_R94=PASS` |
| C2 controls | `python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work <scratch>` | 0 | `R94CriticClaims-c2-controls.txt` | `CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` |
| C3 counter | `python3 -B corpus/evidence/round94/skill-tally-r94.py --root . --selftest corpus/evidence/round94/controls/selftest-r94.txt` | 0 | `R94CriticClaims-c3-tally.txt` | `... TAIL_TALLIES=2 TAIL_OWNED_OK=2/2 OTHERS_OK=1 TAIL_OK=1 LEGS=4/4` / `SKILL_TALLY_R94=PASS` |
| C3 controls | `python3 -B corpus/evidence/round94/skill-tally-r94-controls.py --root . --work <scratch>` | 0 | `R94CriticClaims-c3-controls.txt` | `CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1 STALE_REFUSED_BOTH=1/1 TAIL_ADDED_REFUSED=1/1 HIST_UNGROUNDED_REFUSED=1/1` |

At F2/C2 (live lane, spot-checks only):

| check | command | rc | receipt | observed line |
|---|---|---|---|---|
| C1 verify at C2 | same verify with `--rev 4cbaed6c… --receipts-rev f276d7fb…`, run at the lane root | 0 | `R94CriticClaims-c1-verify-C2.txt` | `PINNED_FILES=35/35 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS`; `RECEIPT SELF_PIN OK rev=4cbaed6c… receipts_rev=f276d7fb…` |
| C2 controls at C2 | `curation-controls-r94.py --root . --work <scratch>` at the lane root | 0 | `R94CriticClaims-c2-controls-C2.txt` | `CONTROLS=PASS ... PUNCT_SHAPE_GREEN_R93=1/1 CJK_SILENT=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` |
| C1 battery at C2 | `forgeries-r94.py --root . --repo . --rev 4cbaed6c… --receipts-rev f276d7fb… --work <scratch>` at the lane root | 0 | `R94CriticClaims-c1-forgeries-C2.txt` | `FORGERIES=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass` |

`grep -cE '^[0-9a-f]{64}'` on the C table = 34, on the C2 table = 35; `grep -c '  driver  '` = 20 and 21
respectively, so the claim's `m` is 14 at both carriers. The dispatch brief's fixed `PINNED_FILES=34/34` is
stale at C2 (the live value is 35/35); the claim text itself is parameterised (`n` = the table's data-row
count), so this is an orchestrator-line staleness, not a claim fire.

Write-safety of `verify` (C1 K3 second clause): before/after `sha256sum` over
`corpus/evidence/round94/controls/receipts` + `.ufo/waves/round-94`, and `git status --porcelain`, were
identical (`R94CriticClaims-c1-tree-before.sha`, `-tree-after.sha`, `-status-before.txt`,
`-status-after.txt`, combined in `R94CriticClaims-c1-verify-writecheck.txt`, rc 0 run). Fresh outputs went
to the outside `--work` dir only.

## 1. Sentence → enforcement map, per claim

Line numbers are the F bytes (the assigned instrument). "C2" rows are the F2 instruments.

### C1 `C1-DRIVER-R94`

| sentence assertion | enforced at / measured | verdict |
|---|---|---|
| Before: "the landed 23-row table scores `CONTROL_DRIVER_R93=PASS`" | reproduced on `$S/base`: `RECEIPT PINS OK 23/23 ... CONTROL_DRIVER_R93=PASS`, rc 0 (`R94CriticClaims-c1-base-r93.txt`; run without `--repo`, matching the before receipt's missing `SELF_PIN` line) | bound |
| Before: "but 18 of its rows carry no role" | the base table is two-column: 23/23 rows carry no role; the base expected rows execute 5 instruments, so 18 = the **non-executed** population (23 − 5) | **unbound** (fire F1) |
| Before: "with the two round-93 claims rows removed ... `PINNED_FILES=21/21` and still `CONTROL_DRIVER_R93=PASS`" | reproduced: `RECEIPT PINS OK 21/21 ... PINNED_FILES=21/21 RECEIPT_PINS=6/6 CONTROL_DRIVER_R93=PASS`, rc 0 (`R94CriticClaims-c1-base-r93-claims-dropped.txt`) | bound |
| After: "every row is `<sha256>  <role>  <path>` with role ∈ {instrument, expectation, receipt, claims, driver}" | `control-driver-r94.py:73-101` (3 whitespace fields, `SHA_RE`, `role in ROLES` at `:50`); the literal double-space is not enforced (`split()`), cosmetic | bound |
| After: "the role sets are checked in both directions" | `:290-336`: instrument `:302-308`, receipt `:320-326`, claims `:328-335` (two loops each); expectation `:311-317` (one set-inequality covering both directions) | bound |
| After: "role=instrument is exactly the instruments the expected rows execute" | executed = `instrument_rels` over the expected `instrument` column (`:141-151`, `.py`/`.sh` absolute/`@ROOT@` tokens); set equality `:307` | bound (named limit 3) |
| After: "role=expectation is exactly the expectations file" | single path from `--expected`, `:311-317` | bound — fixed path, not a derived set |
| After: "role=receipt is exactly the committed receipts" | `os.listdir(receipts_dir)` `:320-326` + `receipt_pins` `:181-208` + per-receipt blob at `--receipts-rev` in `self_pin` `:404-453` | bound |
| After: "both claims files carry role=claims" | fixed constant `CLAIM_PATHS` (`:51`) compared as a set (`:328-335`); extra row → dangling, missing → missing | bound — fixed pair, not a derived directory scan (the claim does not overstate it) |
| After: "A two-column row is `SETUP PIN_SCHEMA` (exit 2)" | `:88-90`; measured `SETUP PIN_SCHEMA row is not ...`, rc 2 (`R94CriticClaims-c1-mut-schema-two-column.txt`) | bound |
| After: "an unknown role `SETUP PIN_ROLE_UNKNOWN` (exit 2)" | `:92-95`; measured, rc 2 (`R94CriticClaims-c1-mut-role-unknown.txt`) | bound |
| After: "a dangling or missing member of a covered role is `PIN_ROLE_DANGLING` / `PIN_ROLE_MISSING` (exit 1)" | instrument/receipt do; **expectation yields `PIN_ROLE_MISMATCH`** (`:311-317`), measured both empty and extra | **unbound** (fire F2) |
| After: "`driver` rows are byte-checked but carry no coverage invariant (named limit 2)" | `covered` excludes driver `:299`; the pin walk still hashes them `:366-384` | bound |
| Predicate: "PASS requires findings==0, … `checked==len(pins)`, `rchecked==rtotal>0`, and role_codes empty" | `:601-604` (`roles_ok = not role_codes and role_ok == role_total and role_total > 0`) | bound |
| Predicate: "`PINNED_FILES=n/n` … and `m` its non-driver row count" | `:606-608`; C 34/34 and 14/14, C2 35/35 and 14/14 | bound (parameterised) |
| Predicate: "both printed as full ratios, so a deleted or invented row moves the number rather than hiding" | measured: removing a driver row → `33/33 … 14/14`, **no code names the row**, only `RECEIPT SELF_PIN FINDING SELF_DRIFT …instrument-pins.txt@352924bb`; inventing one → `35/35 … 14/14` likewise; rc 1 in both | bound literally (n moves); see O1 |
| Predicate: "plus `RECEIPT SELF_PIN OK rev=<F> receipts_rev=<C>`" | measured in both verify receipts | bound |
| Predicate: "The battery prints `FORGERIES=PASS FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass` (exit 0)" | at C the battery prints `FORGERIES=FAIL …` and exits 1: `FAIL s1-schema-two-column: r93 rc=0 r94 rc=0 needles=SETUP PIN_SCHEMA`; every quoted counter still matches, only the verdict token/exit differ | **unbound at C** (fire F7); F2 drops the s1 case (see §0) |
| Predicate: "the four refusals … each scored PASS by the r93 driver on the two-column projection" | `forgeries-r94.py:113-142` requires `rc_old == 0` per case; `prior` is the same expression as `role_forgeries` in F (`:196-199`), so 4/4 implies r93 rc 0 but the two counters are not independent (fixed at F2: `old_rcs`) | bound (coupled at F) |
| Predicate: "the do-nothing form … (SCHEMA_PRIOR_ACCEPTED, r93 rc 0 → r94 PIN_SCHEMA rc 2)" | `:150-158`; the s0 case passes in the F battery run | bound |
| K1 "the predicate not met at the landing revision" | **the battery half of the predicate is not met at C** (§0) | **kill-rule condition observed at C**; F2 changes the battery bytes; C2 battery measured in §0 |
| K2, K4 | battery fixtures d1–d4; `covered` excludes driver; `INSTRUMENT_UNPINNED` `:355-360` refuses an expected row that executes nothing; `role_claims` is read from the table | bound |
| K3 "or `verify` writes under the receipts or claims directories" | measured unchanged tree/status | bound |
| Named limit 1 (joint edit) | admitted; the carrier self-pin is the outer ring | bound |
| Named limit 2: "a deleted driver row is `PIN_MISSING`-class only" | **row removed** → no `PIN_*` code, `33/33`, only the carrier `SELF_DRIFT`; **row's file deleted** → `PIN_MISSING path=…`, `33/34`, rc 1 | **unbound for the row reading** (fire F3) |
| Named limits 3, 4 | roles read the table only; `ROLES` is a closed literal | bound |

### C2 `C2-CURATION-R94`

| sentence assertion | enforced at / measured | verdict |
|---|---|---|
| Before: "on a tree whose Q2 quote cell is '—', r93 prints `Q_SHAPE_FAIL=0`" | reproduced: `... Q_SHAPE_FAIL=0 Q_WSQUOT=0 ...`, rc 1 (`R94CriticClaims-c2-x1-r93.txt`) | bound |
| Before: "has no `Q_PUNCTQUOT` field" | no `PUNCT` token anywhere in the r93 source or on either X tree's output | bound |
| Before: "refuses the tree only downstream (`LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`)" | reproduced: `LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`, **and `LEG_FAIL VERDICT fields_hold=0 legs_ok=12/14`** (also in the cited before receipt) | **unbound as an enumeration** (fire F6; "only downstream" holds) |
| Before: "Its `locates()` compares the quote as a substring, so '—' 'locates' any capture that contains an em dash" | `round93/curation-r93.py:210-211`; direct call `locates("—", "before — after") = True` | bound |
| After: "`q_shape_violation` refuses a quote cell with no alphanumeric character as `quote=<punctuation>`" | `curation-r94.py:252-267`, `PUNCT_RE` `:110`, return `:264`; direct call = `quote=<punctuation>` | bound |
| After: "the class is counted on the located-quote population before the shape filter (`Q_PUNCTQUOT`)" | `:378-381` counts on **every three-cell row before the shape filter and before source resolution**; X1 measured `QUOTES_LOCATED=19/19 Q_ROWS=19 Q_SHAPE_FAIL=1 … Q_PUNCTQUOT=1` — the counted Q2 row is the shape-refused row and is never in the located population; the claim's own named limit 1 states the correct population | **unbound / self-contradictory** (fire F4); **amended at F2** (§4) |
| After: "`locates()` returns False for a punctuation-only quote" | `:219-222`; direct call = `False`; witness `punct-locate-silent` | bound |
| After: "leg 16 (PUNCTQUOT) makes deleting the class change the verdict through the `EXPECTED_LEGS` arity tripwire (15 → 16)" | `EXPECTED_LEGS = 16` `:109`, `LEG_FAIL ARITY` `:608`; scratch copy with the leg append removed: `LEG_FAIL ARITY expected=16 measured=15`, rc 1 (`R94CriticClaims-c2-arity-nopunct.txt`) | bound |
| After: "`witness()` grows to 17 rows with both directions … plus `locates(…) is False`" | `:283-311`, returns `17/17`; row present at `:308` (18 rows at F2, CJK row added) | bound at F |
| After: "r93 fails those trees too, but it cannot name the cause" | r93 rc 1 on both X trees; **no** r93 output token names the class. Caveat: r93 prints `WARRANT_UNLINKED … warrant=Q2 (S214) resolved=0/1` — it names the affected row/effect, not the class | bound |
| Predicate: counter line + `VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=17/17` | reproduced verbatim | bound |
| Predicate: "The controls print `CONTROLS=PASS … PUNCT_SHAPE_GREEN_R93=1/1 PRIOR_REGRESSION=7/7`" | the printed line interposes `DUPCOUNT_1=1/1`; the quoted string does not occur. Same at F2 (F2 adds `CJK_SILENT` but still quotes around `DUPCOUNT_1`) | **unbound verbatim** (fire F5; persists at F2) |
| Predicate: "r94 refuses each at the shape leg with `quote=<punctuation>`, `Q_PUNCTQUOT=1` and `LEG_FAIL PUNCTQUOT`" | X1 measured all three; battery needles assert them for x1/x2 | bound |
| Predicate: "while r93 reports `Q_SHAPE_FAIL=0` on the same bytes (re-derived every run)" | battery re-runs `OLD` on both X trees and requires `Q_SHAPE_FAIL == "0"` | bound |
| K3, K4 | positive `20/20`, `17/17`, floors 13/13 and 7/7; arity probe | bound |
| Named limit 1 | placement measured; named limit text correct in both F and F2 | bound |
| Named limit 2 | shared expression; deletion force = arity (measured); note `fields_hold` also carries `not punct_quote_rows` `:572` | bound (limit slightly understates the force) |
| Named limits 3, 4 | `locates` is line-agnostic; decision-width is observability | bound |

### C3 `C3-TALLY-R94`

| sentence assertion | enforced at / measured | verdict |
|---|---|---|
| Before: "`TAIL_DECLARED = {('215','0'):1, ('283','0'):1}` over everything after `## Gates`" | `round93/skill-tally-r93.py` tail scan over the literal | bound |
| Before: "Moving the 215 tally … leaves `TAIL_OK=1` and `SKILL_TALLY_R93=PASS`" | reproduced: `TAIL_TALLIES=2 … TAIL_OK=1 LEGS=4/4`, `SKILL_TALLY_R93=PASS`, rc 0 (`R94CriticClaims-c3-moved-r93.txt`) | bound |
| After: "each tail tally is declared with the substring of the heading that owns it (`TAIL_OWNED`)" | `skill-tally-r94.py:166-169` | bound |
| After: "the nearest preceding ATX heading of every occurrence is recorded" | `:171-179` (`^#{1,6} ` + space; each occurrence appended to `tail_owners`) | bound |
| After: "a moved tally fires `TAIL_OWNER_MISMATCH` (a duplicated or deleted one `TAIL_OWNER_COUNT`)" | `:180-191`; measured moved-215 `TAIL_OWNER_MISMATCH … owner=### Round 36 … declared=Round27 repair/status correction`; double-215 `TAIL_OWNER_COUNT tally=215 observed=2 declared=1` | bound |
| After: "so `TAIL_OK` now requires both the multiset and the owners" | `:192 tail_ok = tail_counts == TAIL_DECLARED and head_ok and not owner_codes`; moved-215: multiset **equal** (`LEG_FAIL TAIL declared={('215','0'):1,('283','0'):1} observed={('215','0'):1,('283','0'):1}`), owners fail, `TAIL_OWNED_OK=1/2`, `TAIL_OK=0`, rc 1 — **no path where the multiset passes and the owners fail without moving `TAIL_OK`** | bound |
| After: "`TAIL_OWNED_OK` prints the ratio" | `:258`; `2/2` clean, `1/2` moved | bound |
| Predicate: `LEGS=4/4 TAIL_OK=1 TAIL_OWNED_OK=2/2 TAIL_TALLIES=2 TALLY_ROWS=8 STALE_TALLIES=0/8 HIST_DERIVED=2/2 HIST_PRESENT=2/2 CASE_RANGE_OK=2/2 MISLABELED=0` | reproduced (all fields; some ordering/extra fields differ, none contradicted) | bound |
| Predicate: controls line `CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1` | actual line has exactly that prefix plus three trailing fields; `prior` is computed independently from `old_rcs` | bound |
| Predicate: moved trees / double / heading-alias | battery `case()` checks both rc's and needles; measured moved-to-heading `TAIL_OK=1`, `SKILL_TALLY_R94=PASS`, rc 0 (`R94CriticClaims-c3-moved-to-heading.txt`) | bound |
| K3, K4, named limits 1–4 | scans are disjoint; `owned_ok` from observed headings; declaration literal is the closed set | bound |

## 2. WORDING_FIRES=7

**F7 (C1, predicate-level — highest severity).** "The battery prints `FORGERIES=PASS FORGERY_REFUSED=4/4
PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass` (exit 0)"
— at the assigned carrier the battery exits **1** and prints `FORGERIES=FAIL FORGERY_REFUSED=4/4
PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass`, with
`FAIL s1-schema-two-column: r93 rc=0 r94 rc=0 needles=SETUP PIN_SCHEMA` and the r94 excerpt
`RECEIPT PINS OK 34/34 …`. The F battery's `s1` case is structurally unpassable: `case(…, None, 2,
["SETUP PIN_SCHEMA"])` routes `mutate=None` through `write_r94` (three-column table), so r94 scores it
(rc 0) and the expected two-column refusal (rc 2) can never occur; `ok = all(results.values())` then flips
the verdict token. Every quoted counter matches — only `FORGERIES=` and the exit code do not.
Command: the C1 battery command in §0; receipt `R94CriticClaims-c1-forgeries.txt` (rc 1).
At F2/C2 the same command with `--rev 4cbaed6c… --receipts-rev f276d7fb…` prints
`FORGERIES=PASS … POSITIVE=pass` and exits 0 (`R94CriticClaims-c1-forgeries-C2.txt`, rc 0): the claim's
line becomes true only after the s1 case is dropped — i.e. only on bytes the assigned carrier does not
hold.
Smallest correction: drop the impossible case (as F2 does) or write the two-column shape inside it.

**F1 (C1, narrative).** "the landed 23-row table scores `CONTROL_DRIVER_R93=PASS` — but 18 of its rows
carry no role, so a row for a file nothing executes (`curation-controls-r93.py`) is indistinguishable from
an instrument row"
— the base table has no role column on any row (23/23; the before receipt itself says "rows with a role
column = 0"); 18 is the count of rows no expected row executes (23 − 5).
Command: `git show 0f3f84d:corpus/evidence/round93/instrument-pins.txt | grep -cE '^[0-9a-f]{64}'` → `23`;
`git show 0f3f84d:corpus/evidence/round93/controls/expected.tsv` → 6 cases, 5 distinct instruments.
Receipt: `R94CriticClaims-c1-base-r93.txt` (rc 0).
Smallest correction: "18 of its 23 rows name files no expected row executes".

**F2 (C1).** "a dangling or missing member of a covered role is `PIN_ROLE_DANGLING` /
`PIN_ROLE_MISSING` (exit 1)"
— for the covered role `expectation` both a missing and an extra member yield `PIN_ROLE_MISMATCH`:
`PIN_ROLE_FINDING PIN_ROLE_MISMATCH role=expectation pins=none expected=corpus/evidence/round94/controls/expected.tsv`,
rc 1; and `… pins=corpus/evidence/round94/census-start.txt,corpus/evidence/round94/controls/expected.tsv
expected=…`, rc 1. The claim's own battery d3 asserts this code. The F2 driver diff touches only the
function signature, not this branch, so it persists at F2.
Command: §0 C1 verify with the table mutated by `c1mut.py expectation-relabel-receipt` /
`expectation-extra`.
Receipts: `R94CriticClaims-c1-mut-expectation-relabel-receipt.txt`,
`R94CriticClaims-c1-mut-expectation-extra.txt`.
Smallest correction: "…is `PIN_ROLE_DANGLING` / `PIN_ROLE_MISSING` for instrument and receipt, and
`PIN_ROLE_MISMATCH` for expectation (exit 1)".

**F3 (C1, named limit 2).** "so a deleted driver row is `PIN_MISSING`-class only"
— on the row reading (the reading the claim's own Before/After use, "a deleted … row"), **no `PIN_*` code
is emitted**: `RECEIPT PINS OK 33/33 pinned files byte-identical`, `PIN_ROLES_OK=14/14`, and the only
finding is `RECEIPT SELF_PIN FINDING SELF_DRIFT
corpus/evidence/round94/instrument-pins.txt@352924bbea624caf3771ef291be98fd4ec679dda`, rc 1. Only
deleting the row's *file* gives `RECEIPT PINS FINDING PIN_MISSING
path=corpus/evidence/round94/make-pins-r94.py` (`PINNED_FILES=33/34`, rc 1).
Command: §0 verify with `c1mut.py driver-drop-make-pins`; and with
`rm corpus/evidence/round94/make-pins-r94.py` in the clone (scratch, restored afterwards).
Receipts: `R94CriticClaims-c1-mut-driver-drop-make-pins.txt`,
`R94CriticClaims-c1-mut-driver-file-deleted.txt`.
Smallest correction: "a deleted driver *file* is `PIN_MISSING`; a removed driver *row* emits no code and
moves only `PINNED_FILES`' denominator".

**F4 (C2, After) — amended at F2.** "the class is counted on the located-quote population before the
shape filter (`Q_PUNCTQUOT`)"
— measured at F on the dash tree: `QUOTES_LOCATED=19/19 Q_ROWS=19 Q_SHAPE_FAIL=1 … Q_PUNCTQUOT=1`; the
counted Q2 row is the shape-refused row (`Q_SHAPE search-transparency-reporting-r84.md
quote=<punctuation> row=| Q2 | S214 | "—" |`) and is never located. The instrument counts every three-cell
row before the shape filter and before source resolution (`:378-381`), which is what the same claim's
named limit 1 says. As written the sentence contradicted both the code and its own limit. **F2 replaces
the sentence with "counted on every three-cell quote row before the shape filter … pre-qid, pre-source,
pre-location" and adds "the count is the class population, not the located population (Amendment 2,
R94ReviewerC2 F1)" — the amendment independently confirms this fire.**
Command: `curation-r94.py --root <x1-punct-dash>`, rc 1.
Receipt: `R94CriticClaims-c2-x1-r94.txt`.
Smallest correction (applied at F2): the F2 wording.

**F5 (C2, predicate, cosmetic; persists at F2).** F: "The controls print `CONTROLS=PASS
CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 PRIOR_REGRESSION=7/7`
(exit 0)". F2: "… `PUNCT_SHAPE_GREEN_R93=1/1 CJK_SILENT=1/1 PRIOR_REGRESSION=7/7` (exit 0)".
— the F line prints `… PUNCT_SHAPE_GREEN_R93=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` (rc 0) and the F2
line prints `… PUNCT_SHAPE_GREEN_R93=1/1 CJK_SILENT=1/1 DUPCOUNT_1=1/1 PRIOR_REGRESSION=7/7` (rc 0); in
both cases the quoted string does not occur because `DUPCOUNT_1=1/1` interposes. All quoted tokens hold.
Commands: the C2 controls command at C and at C2 (§0).
Receipts: `R94CriticClaims-c2-controls.txt`, `R94CriticClaims-c2-controls-C2.txt`.
Smallest correction: include `DUPCOUNT_1=1/1` (or say "prints, among others,"). The orchestrator's
dispatch line repeats the omission.

**F6 (C2, Before, cosmetic; persists at F2).** "refuses the tree only downstream (`LEG_FAIL FLOOR`,
`LEG_FAIL WARRANT`)"
— the same tree prints three downstream LEG_FAIL lines, including `LEG_FAIL VERDICT fields_hold=0
legs_ok=12/14`, in the cited before receipt and in the reproduction. "Only downstream" holds; the
parenthetical is not the full set. The r93 counter is byte-identical at C and C2 (same pin hash), and the
F2 claims did not change the Before sentence.
Command: `round93/curation-r93.py --root <x1-punct-dash>`, rc 1.
Receipt: `R94CriticClaims-c2-x1-r93.txt`.
Smallest correction: add `LEG_FAIL VERDICT` to the parenthetical.

## 3. Observations that are not fires (claim-strength notes)

**O1 (C1, the strongest strength note).** The C1 predicate is self-referential on `n`:
`PINNED_FILES=n/n` and `PIN_ROLES_OK=m/m` with `n`, `m` taken from the table itself (`:606-608`;
`m = len(covered)`). Measured: a table with a driver row removed prints `33/33` and `14/14` and passes
every ratio check; only the fixed `--receipts-rev` carrier self-pin makes the run fail (`SELF_DRIFT`). If
such a table were committed at the carrier (named limit 1), the claim's own predicate would be met at
33/33 while the brief's `34/34` fails. The frozen predicate does not pin `n`; the dispatch brief does, and
at C2 the brief's 34/34 is already stale (live 35/35). Smallest safe correction (claim-level, no code
change): state `n`/`m` explicitly in the predicate, or add a coverage invariant for the driver set.

**O2 (C2, evidence fidelity).** The cited before receipt
`corpus/evidence/round94/evidence-before/c2-prior-accepts.txt` is an abridged capture: the same r93
counter on the same class of tree prints unconditionally `TEACHES_FLAGGED S024 …`,
`WARRANT_UNLINKED … warrant=Q2 (S214) resolved=0/1`, and `VERDICT fields_hold=0 legs_ok=12/15
DETECTOR_WITNESS=13/13`; all three lines are absent from the committed file (diff of
`R94CriticClaims-c2-x1-r93.txt` vs the receipt). Nothing in the claim depends on the absent lines and the
claim does not call the file verbatim, so this is not a fire — but the file is a filtered excerpt, not the
counter's output.

**O3 (C2, "cannot name the class").** r93 names the affected row and effect
(`WARRANT_UNLINKED … row=Reporting when a source was searched warrant=Q2 (S214) resolved=0/1`) but never
the punctuation shape; no r93 output token contains `PUNCT` and the shape leg is green on both X trees.
The classification discrimination is real: r94 names the class (`Q_PUNCTQUOT=1`, `LEG_FAIL PUNCTQUOT`),
r93 does not.

**O4 (C1, "both directions" scope).** The `claims` and `expectation` populations are **fixed paths**, not
derived sets: `CLAIM_PATHS` (`:51`) and the single `--expected` path (`:311-317`); `instrument` and
`receipt` are derived (expected.tsv / receipts dir). The claim's nouns do not overstate this ("both claims
files", "the expectations file"), and the extra-row direction is enforced: claims-extra →
`PIN_ROLE_FINDING PIN_ROLE_DANGLING role=claims path=corpus/evidence/round94/census-start.txt`, `12/15`,
rc 1; claims-drop → `PIN_ROLE_MISSING role=claims …`, `12/13`, rc 1. Consequence: a new claims artefact in
the round directory would not be required unless the constant is edited in the same commit (named limit
4's shape, applied to claims).

**O5 (C3, the asked path).** No path exists where the multiset passes and the owners fail without moving
`TAIL_OK`: `tail_ok` ANDs `not owner_codes` (`:192`), and the moved tree proves it (`TAIL_TALLIES=2`,
multiset equal, `TAIL_OWNED_OK=1/2`, `TAIL_OK=0`). The only way to keep `TAIL_OK=1` is to satisfy the
owner substring — measured, the heading-alias fixture passes; that is named limit 1 and is disclosed (F2
strengthens the limit text: the fixture renames the owner heading, it does not move the tally).

**O6 (C1, named limit 2's list).** The parenthetical "(the driver, the batteries, the leg table, the
selftest capture)" does not enumerate the driver rows: at C the table carries 20 driver rows (round-93
batteries, three evidence-before captures, the self row); at C2 it carries 21 (the measurement wrapper
`scripts/measure-all-r94.sh` is a driver row). Illustrative, not counted.

**O7 (battery counters).** In F, `prior` is the same expression as `role_forgeries` (`forgeries-r94.py`
lines 196-199), so `PRIOR_ACCEPTED` measures fixture success, not an independent r93 acceptance rate
(enforced through the conjunction, but not independent). F2 fixes this (`old_rcs`). The C3 analogue
`MOVED_PRIOR_ACCEPTED` was already independent (`skill-tally-r94-controls.py:186-188`).

## 4. Revision identity — F/C vs F2/C2 (impact on any verdict)

1. The claims file named by the assignment (F) is not the live claims file: F2 rewrites the C2 and C3
   sections (citing `R94ReviewerC2 F1/F2/F4`, `R94ReviewerC3 F2/F4`, `R94ExecC2Repro`), adds
   `CJK_SILENT`, moves the witness to 18 rows, adds `TAIL_OWNER_UNMAPPED`, and rewrites the C2 population
   wording. The C1 text is unchanged.
2. The pins table is a different table: 35 rows, 21 driver (C2) vs 34 rows, 20 driver (C). Every round-94
   driver and every receipt hash changed; the six case instruments (round89/round90) and the six round-93
   drivers are byte-identical across C and C2. The six receipts were re-emitted at F2 and repinned at C2.
   The C1 claim's parameterised predicate is satisfied at C2 (`35/35`, `14/14`, rc 0) and was satisfied at
   C (`34/34`, `14/14`, rc 0) — but the *battery* half was not satisfied at C (F7).
3. The battery bytes are not the bytes the claim was written against: F2 drops the `s1-schema-two-column`
   case and measures `prior` independently. The C1 claim's quoted `FORGERIES=PASS … (exit 0)` is measured
   **true at F2/C2 (rc 0) and false at F/C (rc 1)** — the line holds only on bytes the assigned carrier does
   not hold. Whether the wave's amendment process admits this is an integrator/judge call; as measured, the
   claim became true by changing the instrument after the claim, not by the evidence moving.
4. The r93 instruments and the before receipts are unchanged across F→F2 (same pin hashes), so the C1/C2/
   C3 before-state measurements remain comparable.
5. My fires F1/F2/F3/F5/F6 reproduce at F2 at the level of text (C1 text unchanged; F2's C2 controls line
   still omits `DUPCOUNT_1`; the C2 Before sentence is unchanged; the F2 driver's role branch is unchanged
   except its signature) and at the level of measurement where I ran it (C2 controls, C2 verify). F4 is
   amended at F2. F7 is fixed at F2 by construction (s1 dropped).

## 5. What I did not run

- The **C2 battery** was run (rc 0, line in §0); no gap there.
- The **C2 tally counter/controls** at F2: the F2 diffs add `TAIL_OWNER_UNMAPPED` and rename the
  heading-alias fixture; my C3 measurements are on the F bytes. No C3 fire depends on F2.
- Mutation probes at C2 for F2/F3/F1: the F2 driver diff changes no logic in `read_pins`/`role_report`
  beyond the signature, and the C1 claims text is unchanged; the C measurements carry the finding.

## 6. Impacted axes

- C1 operability: F7 is a predicate failure at the assigned carrier (battery exit 1), plus wording fires
  F1/F2/F3. The verify half of the predicate is green at both carriers; the role mechanism itself is sound
  (all four role fixtures, the schema refusals, the carried refusals and the positive pass in the F run).
- C2 calibration: F4 (population) is a real wording defect already amended at F2; F5/F6 are cosmetic
  predicate-text defects that persist. The classification force (r94 names the class, r93 does not)
  reproduces at both carriers.
- C3 freshness: held; no fire, and the asked counterexample (multiset passes / owners fail / TAIL_OK
  stays 1) does not exist.

VERDICT: R94CriticClaims C1 fired — the assigned carrier's battery exits 1 with FORGERIES=FAIL while the frozen claim quotes FORGERIES=PASS (exit 0), and three further C1 sentences are unbound as written (the 18-row role count, the expectation role's PIN_ROLE_MISMATCH code, and named limit 2's PIN_MISSING-class claim).
VERDICT: R94CriticClaims C2 fired — the F sentence counts the class on a population that excludes the counted row (amended at F2 after an independent sibling finding), and the predicate line still quotes around DUPCOUNT_1=1/1 at F2; the classification force itself reproduces.
VERDICT: R94CriticClaims C3 held — measured on the moved tree, the multiset passes and the owner failure drives TAIL_OK=0, so no unbound path exists; all C3 predicates reproduce.
