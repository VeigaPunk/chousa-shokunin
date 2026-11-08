# R93RevPrior — round 93 BEFORE-state reconstruction (independent, committed bytes only)

Seat: `R93RevPrior` (revenger, L1 ChousaR93, lane `chousa`, round 93).
Assigned surface: reproduce, from committed bytes, the BEFORE state the three frozen claims rest on
(C1 operability, C2 calibration, C3 freshness), then diff that reconstruction against every `Before`
paragraph of `.ufo/waves/round-93/claims.md` and report disagreements with exact lines.

Revisions used:

| role | revision |
|---|---|
| base | `206226dc9d9baef620e7d3d30bdac5f9194a459f` |
| freeze F2 | `b7241252c2358613d3b22b7d0454d98c56dab373` |
| carrier C2 (tree attacked) | `754b62fb6adc60e44e12375af5461a0ebe302994` |

Provenance / method

```
mkdir -p /fast/scratch/hyaku/chousa-r93/R93RevPrior
git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r93/R93RevPrior/repo
git -C /fast/scratch/hyaku/chousa-r93/R93RevPrior/repo checkout 754b62fb6adc60e44e12375af5461a0ebe302994
git -C .../repo rev-parse --show-toplevel   # -> .../R93RevPrior/repo
git -C .../repo rev-parse HEAD              # -> 754b62fb...
```

Every counter and every instrument was read from that C2 clone (or from the lane's committed working
tree, which is identical for the files used); every fixture is a `git clone --shared` of it, each with
`rev-parse --show-toplevel` asserted before any mutation. No network, no `sudo`, no package manager
transaction, no tool install, no production edit, no commit. All trees/work dirs lived under
`/fast/scratch/hyaku/chousa-r93/R93RevPrior` and were removed before this report was written.
Receipts cited below are copied into `.ufo/waves/round-93/w1/receipts-r93revprior/` (paths are
lane-relative); the scripts that built the fixtures and ran the cases are in
`.ufo/waves/round-93/w1/receipts-r93revprior/provenance/`.

---

## C1 BEFORE (operability) — the r92 driver on the round-93 fixtures

The r92 driver is `corpus/evidence/round92/control-driver-r92.py` as carried at C2 (byte-identical to
round 92, pinned by the r92 table row `2ff309e9…`).

### (i) `pin_report`'s wanted set — `PINNED_FILES=7`

Source lines (C2 bytes):
`corpus/evidence/round92/control-driver-r92.py:279` `def pin_report(rows, root, expected, pins_path)`,
`:285` `wanted = {}`, `:286-292` one entry per source file a row executes, `:293`
`wanted[rel_for(root, expected)] = "expectations"`, `:294` `wanted[rel_for(root, pins_path)] = "pins"`.

Command (driver loaded as a module; its own `read_expected` / `pin_report` / `instrument_rels` /
`read_pins` / `rel_for`; root = C2 clone):

```
python3 -B - <<'EOF'
import importlib.util
S=".../R93RevPrior/repo"
spec=importlib.util.spec_from_file_location("r92", S+"/corpus/evidence/round92/control-driver-r92.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tag, exp, pins in ((("round92-table"), ...round92/controls/expected.tsv, ...round92/instrument-pins.txt),
                       (("round93-table"), ...round93/controls/expected.tsv, ...round93/instrument-pins.txt)):
    rows=m.read_expected(exp); codes, checked = m.pin_report(rows, S, exp, pins)
    ...
EOF
```

Receipt: `.ufo/waves/round-93/w1/receipts-r93revprior/fn-pinreport-both-tables.txt`.

Observed (6 rows execute **5 distinct** files — `c1-harm` and `c1-harm-setup` both execute
`corpus/evidence/round90/harm-recheck-r90.py`):

```
wanted(7): corpus/evidence/round89/curation-r89-controls.py, corpus/evidence/round89/curation-r89.py,
           corpus/evidence/round89/gate-records-r89.py, corpus/evidence/round89/mutate-r89.py,
           corpus/evidence/round90/harm-recheck-r90.py,
           corpus/evidence/round92|93/controls/expected.tsv, corpus/evidence/round92|93/instrument-pins.txt
codes=[]
[round92-table] RECEIPT PINS OK 7/16 pinned files byte-identical; PINNED_FILES=7; rows never compared=9
[round93-table] RECEIPT PINS OK 7/22 pinned files byte-identical; PINNED_FILES=7; rows never compared=15
```

Full-driver confirmation on the r92 fixture set at C2 (`--rev F`, no `--repo`):

```
python3 -B <tree>/corpus/evidence/round92/control-driver-r92.py verify --root <tree> \
  --work <scratch>/w92-r92set --rev b7241252c2358613d3b22b7d0454d98c56dab373 \
  --expected <tree>/corpus/evidence/round92/controls/expected.tsv \
  --receipts <tree>/corpus/evidence/round92/controls/receipts \
  --pins <tree>/corpus/evidence/round92/instrument-pins.txt
```

Receipt: `.../receipts-r93revprior/r92-own-fixtures-7of16.txt`; exit **1**; lines

```
RECEIPT PINS OK 7/16 pinned files byte-identical
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=0/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=FAIL
```

`PIN_OK=0/6` is itself instructive: r92's only per-receipt "pin" is the `# computed_against=` header
matched against `--rev`, and the round-92 receipts name revision `7901eb23…`, so the r92 driver cannot
PASS on its own fixture set at any later revision.

### (ii) no `receipt_pins`; the committed receipts are unpinned in the no-`--repo` form

```
$ grep -c receipt_pins corpus/evidence/round92/control-driver-r92.py                       -> 0
$ grep -c 'PIN_DISK_MISMATCH\|RECEIPT_MISMATCH\|RECEIPT_UNPINNED\|RECEIPT_PINS' <same file> -> 0
```
(`.../receipts-r93revprior/static-checks.txt`.) `pin_report` never looks at the receipts directory; the
six r93 receipt rows of the r93 pins table are simply outside `wanted` and are counted as
"never compared" (15-row list in `fn-pinreport-both-tables.txt`).

Tampered-receipt case, on a scratch clone at C2 (one appended comment line, header untouched):

```
git clone --shared .../repo t-tr && git -C t-tr checkout 754b62fb...
printf '# tampered\n' >> t-tr/corpus/evidence/round93/controls/receipts/c2-prior-landing.txt
python3 -B t-tr/corpus/evidence/round92/control-driver-r92.py verify --root t-tr \
  --work <scratch>/w-receipt-tamper-norepo --rev b7241252... --receipts-rev 754b62fb... \
  --expected t-tr/corpus/evidence/round93/controls/expected.tsv \
  --receipts t-tr/corpus/evidence/round93/controls/receipts \
  --pins t-tr/corpus/evidence/round93/instrument-pins.txt
```

Receipt `.../c1-receipt-tamper-norepo.txt`; exit **0**:

```
RECEIPT c2-prior-landing OK committed+exact+pin+fresh
RECEIPT PINS OK 7/22 pinned files byte-identical
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=PASS
```

Tampered unexecuted pinned instrument (`corpus/evidence/round93/curation-controls-r93.py`, one appended
comment line), same invocation: exit **0**, `.../c1-instr-tamper-norepo.txt`:

```
RECEIPT PINS OK 7/22 pinned files byte-identical
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=PASS
```

So both forgeries the claim names are accepted at rc 0 by the r92 driver **when `--repo` is omitted**.

**Disagreement with the claim's wording.** `claims.md:17` says "the committed receipts are read but
pinned nowhere". At the code level that is too strong: `control-driver-r92.py:330-332`

```
    base = [(rel_for(root, __file__), rev), (rel_for(root, expected), rev)]
    base += [(rel_for(root, os.path.join(receipts, f)), receipts_rev)
             for f in sorted(os.listdir(receipts)) if f.endswith(".txt")]
```

byte-compares every receipt file in `--receipts` against its blob at `--receipts-rev` whenever `--repo`
is supplied. I ran that form:

* pristine C2 clone + r93 fixtures + `--repo` → exit **1**, `.../c1-pristine-repo.txt`:
  `RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round93/controls/receipts/{all six}.txt@b7241252…`
  and `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=7 CONTROL_DRIVER_R92=FAIL`.
* receipt-tampered clone + `--repo` → exit **1**, `.../c1-receipt-tamper-repo.txt`: `SELF_DRIFT` names
  `…/receipts/c2-prior-landing.txt@754b62fb…` **plus** the other five at `@b7241252…`.

So under `--repo` r92 does pin receipt bytes (and simultaneously refuses the pristine tree, because its
`pin_at_rev` walks the r93 table's six receipt rows at `--rev`, where the receipts carry different
bytes). The accurate statement is: *r92 has no receipt pin rows and no `receipt_pins`; receipt bytes are
compared only inside the optional `--repo` self-pin, and the only invocation in which a tampered receipt
prints PASS (rc 0) is the one without `--repo`.* The battery's own note at
`corpus/evidence/round93/forgeries-r93.py:84-87` gives the reason for dropping `--repo` as "a revision
that never held them" — that reason is factually wrong: `git cat-file -e F2:corpus/evidence/round93/controls/receipts/c2-prior-landing.txt`
returns 0 (all six receipts exist at F2); `git diff --stat F2 C2` shows the six receipts rewritten
(2 lines each, the `computed_against` header) plus the pins table (`.../static-checks.txt`). The
invocation delta is real and produces a real discrimination gap, but it should be stated as an
invocation delta, not as an absent blob.

### (iii) defaults are `HERE`-relative; a `--root <archive>` run exits non-zero `escapes base`

```
71:DEFAULT_EXPECTED = os.path.join(HERE, "controls", "expected.tsv")
72:DEFAULT_RECEIPTS = os.path.join(HERE, "controls", "receipts")
73:DEFAULT_PINS     = os.path.join(HERE, "instrument-pins.txt")
374/375/376      ap.add_argument("--expected"|"--receipts"|"--pins", default=DEFAULT_…)
154:        raise SystemExit(f"SETUP path escapes base: {path} vs {base}")
```

Command (lane driver — its `HERE` is the lane's round-92 directory — with `--root` naming a C2 archive and
no explicit paths):

```
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round92/control-driver-r92.py \
  verify --root <scratch>/t-derive --work <scratch>/w-derive --rev b7241252… --receipts-rev 754b62fb…
```

Receipt `.../c1-derive-escapes-base.txt`; exit **1**; last line:

```
SETUP path escapes base: /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round92/controls/expected.tsv vs /fast/scratch/hyaku/chousa-r93/R93RevPrior/t-derive
```

(The six earlier `PIN_MISMATCH:7901eb23…` lines come from the lane's round-92 receipts being scored
against `--rev`; the refusal itself is the `escapes base` SystemExit at line 154.) This reproduces the
derivation class exactly.

---

## C2 BEFORE (calibration) — r92 on a whitespace-quote tree

Trees built by this seat (not by the control battery): `corpus/SOURCES.md`, the two routed entries, and
symlinks to `corpus/captures` + `corpus/evidence/round57`; entry A's row
`| Q2 | S214 | "date when each source was last searched or consulted." |` (line 23) replaced by
`| Q2 | S214 | " " |` (space tree) and `| Q2 | S214 | "\t" |` (tab tree). Builder:
`.../provenance/build_c2c3.py`.

```
cd <tree> && python3 -B corpus/evidence/round92/curation-r92.py --root .
cd <tree> && python3 -B corpus/evidence/round93/curation-r93.py --root .
```

| tree | r92 receipt | r92 exit | r92 key fields |
|---|---|---|---|
| pristine mirror | `c2-r92-pristine-mirror.txt` | 0 | `CURATION_R92=PASS`, `LEGS_MEASURED=14/14`, `Q_SHAPE_FAIL=0`, `Q_ROWS=20`, `QUOTES_LOCATED=20/20` |
| ws-space | `c2-r92-ws-space.txt` | 1 | `Q_SHAPE_FAIL=0`, `LEGS_MEASURED=10/14`, `WARRANT_OK=16/17`, `TFREQ_OK=16/17` |
| ws-tab | `c2-r92-ws-tab.txt` | 1 | identical to ws-space |

Legs that fired on the whitespace trees (r92, both trees):

```
LEG_FAIL FLOOR search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
LEG_FAIL WARRANT 16/17 width_fail=0 count_bad=0
LEG_FAIL TFREQ 16/17 max_df=3<=3
LEG_FAIL VERDICT fields_hold=0 legs_ok=10/13
```

`Q_ROWS=20` and `QUOTES_LOCATED=20/20` on the forged tree: the whitespace cell is counted as a located
quote (empty normalisation matches every capture), and the short-quote conjunct inside FLOOR is what
fires — the shape leg is green.

Contrast (r93 on the same bytes, `c2-r93-ws-space.txt`/`c2-r93-ws-tab.txt`, exit 1):

```
Q_ROWS=19 Q_SHAPE_FAIL=1 Q_WSQUOT=1 ...
LEG_FAIL QSHAPE search-transparency-reporting-r84.md quote=<whitespace>
LEG_FAIL WSQUOTE search-transparency-reporting-r84.md Q2
```

`grep -c Q_WSQUOT corpus/evidence/round92/curation-r92.py` → **0** (no such field anywhere).
Detector witness at r92:229 vs r93:229 (`.../static-checks.txt`):

```
cell='" "'   r92=None              r93='quote=<whitespace>'
cell='"\t"'  r92=None              r93='quote=<whitespace>'
cell='""'    r92='quote=<empty>'   r93='quote=<empty>'
```

**Disagreement with the claim's enumeration.** `claims.md:69-70` lists the downstream refusals as
`LEG_FAIL FLOOR`, `LEG_FAIL WARRANT`, `LEG_FAIL TFREQ`. Both whitespace runs also print
`LEG_FAIL VERDICT fields_hold=0 legs_ok=10/13` — a fourth leg. "refuses the tree only downstream" is
correct; the enumeration is incomplete (and the `LEGS_MEASURED=10/14` figure is the honest one).

---

## C3 BEFORE (freshness) — r92's frozen `EXPECTED_OTHERS` and an invisible tail tally

Frozen literal, `corpus/evidence/round92/skill-tally-r92.py:108`:

```
108:    EXPECTED_OTHERS = {("161", "0"): 1, ("256", "0"): 1}
```

Scoped to the `## Gates` section only (`:79-92`); the tail tallies are outside it —
`SKILL.md:640` `` `PASS (215 cases, 0 skipped)` `` in the Round27 subsection (heading `SKILL.md:634`)
and `SKILL.md:781` `` Selftest `PASS (283 cases, 0 skipped)` on this host ``.

Trees: `c3/clean/SKILL.md` (verbatim C2 copy) and `c3/t215/SKILL.md` (that single line's `215` → `214`,
one occurrence asserted), plus `c3/t215del/SKILL.md` (the whole line removed). Selftest receipt is the
committed `corpus/evidence/round93/controls/selftest-r93.txt` (so the tool is never run).

```
python3 -B corpus/evidence/round92/skill-tally-r92.py --root <tree> --selftest corpus/evidence/round93/controls/selftest-r93.txt
```

Receipts `c3-r92-clean.txt`, `c3-r92-tail-215-to-214.txt`, `c3-r92-tail-215-line-deleted.txt`; **all
three exit 0** and print the identical line:

```
TALLY_ROWS=8 STALE_TALLIES=0/8 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=2 CASE_RANGE_BASHENV=273-275 CASE_RANGE_BASH_PIN=282-283 CASE_RANGE_OK=2/2 MISLABELED=0 OTHERS_OK=1 LEGS=3/3
SKILL_TALLY_R92=PASS
```

`OTHER_OCCURRENCES=2` is exactly `{161, 256}`; neither `215` nor `283` is observable, so a change or
deletion of the `215` tail is invisible at rc 0. (On the committed full tree C2, r92 also prints PASS —
`out-full-c2-r92-tally.txt`.)

---

## (d) Diff against `claims.md` `Before` paragraphs, line by line

| claims.md | text | reconstruction | verdict |
|---|---|---|---|
| 15-16 | r92 on the round-93 fixture set prints `RECEIPT PINS OK 7/16 pinned files byte-identical`, `PINNED_FILES=7` | reproduced byte-for-byte (`r92-own-fixtures-7of16.txt`; function-level also 7 with the r93 table, `fn-pinreport-both-tables.txt`) | agrees |
| 16-17 | "nine pinned instruments are never compared on disk" | 16 − 7 = 9 unchecked rows with the r92 table (15 unchecked with the 22-row r93 table) | agrees (table-relative) |
| 17 | "the committed receipts are read but pinned nowhere" | no `receipt_pins`, no receipt rows in `pin_report`'s wanted set — but `self_pin` (r92:330-332) byte-pins every receipt at `--receipts-rev` when `--repo` is given; the tampered receipt is refused rc 1 in that form and accepted rc 0 without it | **disagrees on wording**; the class (a PASS reachable with receipts unpinned) holds only for the no-`--repo` invocation |
| 18-19 | "a tampered copy of an unexecuted pinned instrument and a tampered committed receipt each verify `CONTROL_DRIVER_R92=PASS` (rc 0)" | both reproduced at rc 0 (`c1-instr-tamper-norepo.txt`, `c1-receipt-tamper-norepo.txt`) | agrees |
| 18, 71, 120 | "Measured in `corpus/evidence/round93/evidence-before/{c1,c2,c3}-prior-accepts.txt`" | at C2 the directory does not exist in any commit (`git log --all` count 0, `ls-tree` count 0); in the lane working tree it is untracked (`??`) and held only `.keep` (content `placeholder`) when this seat first listed it at 11:11; `c2-prior-accepts.txt` and `c3-prior-accepts.txt` appeared untracked at 11:11:42/11:11:51 (mid-wave, another seat), and `c1-prior-accepts.txt` is still absent | **citation does not resolve against the frozen tree** |
| 67-68 | r92 on the round-93 tree: `CURATION_R92=PASS` with `LEGS_MEASURED=14/14`, `Q_SHAPE_FAIL=0` | reproduced on the C2 clone (`out-full-c2-r92-curation.txt`, exit 0) and on the pristine mirror | agrees |
| 69-70 | on the `" "` tree r92 reports `Q_SHAPE_FAIL=0` and refuses only downstream, naming FLOOR/WARRANT/TFREQ | `Q_SHAPE_FAIL=0` reproduced on both space and tab trees; legs fired: FLOOR, WARRANT, TFREQ **and VERDICT** | agrees in substance; **enumeration incomplete** |
| 71-72 | "the shape test strips whitespace before stripping quotes, so the inner space survives its cell" | exact: r92 `if not cells[2].strip().strip('"')` (line 229) sees `" "` → `" "` → `" "` unchanged at the ends; r93 inserts `.strip()` after quote removal | agrees |
| 116-118 | `EXPECTED_OTHERS = {("161","0"):1, ("256","0"):1}` over `## Gates` only; `215` (Round27 subsection) and `283` (host line) invisible | literal at line 108; 215 at SKILL.md:640 under the heading at :634; 283 tail at :781; `OTHER_OCCURRENCES=2` | agrees |
| 118-119 | deleting the `215` tail line leaves `SKILL_TALLY_R92=PASS` (rc 0) | reproduced by deletion (rc 0) and by `215`→`214` (rc 0) | agrees |

### Adjacent observation (outside this seat's assigned surface, after-state, not scored here)

The machine form `.ufo/waves/round-93/claims.json` states control predicates that the after
instruments cannot print: C2 `"FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4"` and C3
`"TAIL_REFUSED=1/1"`. `corpus/evidence/round93/curation-controls-r93.py:173-175` prints
`CONTROLS=… CARRIED_REFUSED_BOTH={n}/4 WS_NAMED={n}/2 WS_SHAPE_GREEN_R92=… DUPCOUNT_…=… PRIOR_REGRESSION=…`,
and `corpus/evidence/round93/skill-tally-r93-controls.py:116-124` prints `TAIL_REFUSED={0..2}/2`;
neither prints `FORGERY_REFUSED=4/4`, `PRIOR_ACCEPTED=4/4` or `TAIL_REFUSED=1/1`. `claims.md`'s own
predicates (lines 92-96, 128-129) match the instruments; `claims.json`'s do not. The freeze pair is
therefore internally inconsistent at the predicate level; the L1 should decide which form governs
before the predicate is checked mechanically.

---

## Residuals / limits of this reconstruction

1. Every number above comes from the C2 clone; the lane working tree currently also carries untracked
   wave output (its `evidence-before/` contents changed while this seat was running), so a later
   working-tree re-run need not reproduce the same `git status` lines.
2. C1's `PASS` in the no-`--repo` form is only reachable because `--repo` is optional; the claim's own
   counting form uses `--repo`, under which the r92 driver refuses even the pristine carrier. The
   discrimination gap is real, but it is an invocation-delta gap, not a "no pin code exists" gap.
3. Pinned-byte reasoning is limited to each file's own bytes (the claims' named limit 3). I did not
   re-open `S070`; the digest rule itself was not re-verified by this seat.
4. The r92 full-driver runs take ~65-90 s each because the fresh legs execute the round-89 batteries;
   all six cases were run from scratch copies, never from the lane tree.

VERDICT: R93RevPrior C1 held — the r92 prior state reproduces (PINNED_FILES=7 of 16; tampered receipt and unexecuted pinned instrument each PASS rc 0 in the no-`--repo` form; default-path `--root` run exits 1 `escapes base`), but `claims.md:17`'s "pinned nowhere" is contradicted by r92 `self_pin` whenever `--repo` is supplied and the before-receipt for C1 is absent from the frozen tree.
VERDICT: R93RevPrior C2 held — on a self-built whitespace-quote tree r92 prints `Q_SHAPE_FAIL=0` and refuses only downstream (FLOOR, WARRANT, TFREQ, plus an unlisted VERDICT), and no `Q_WSQUOT` field exists in the r92 source; claims.md's leg enumeration is merely incomplete.
VERDICT: R93RevPrior C3 held — `EXPECTED_OTHERS` is the frozen literal at r92:108 and both a `215`→`214` edit and deletion of the SKILL.md:640 tail line leave `SKILL_TALLY_R92=PASS` at rc 0.
