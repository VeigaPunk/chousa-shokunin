# R94ScoutSources — source opening + bounded planning data-walk (round 94, chousa)

Seat: scout, leaf. Assignment: (a) open the two sources C1 cites; (b) data-walk the pins table for the
planner (every pinned file by role with size and sha256, and which pinned files no instrument reads at run
time); (c) check the three r94 instruments for an unused import or a dead branch.

Everything below was measured on committed bytes. Tree: `git clone --shared
/home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo` then `git -C $S/repo checkout
352924bbea624caf3771ef291be98fd4ec679dda`; `git -C $S/repo rev-parse --show-toplevel` == `$S/repo`, `HEAD` ==
`352924bb…`, worktree clean before any run. Scratch `S=/fast/scratch/hyaku/chousa-r94/R94ScoutSources`
(removed before yield). No network, no lane mutation, no fixture repo was needed.

Receipts: `.ufo/waves/round-94/w1/R94ScoutSources/` (listed in §6).

---

## 1. (a) The two sources C1 cites

### 1.1 S070 — installed `sha256sum(1)`

| field | value |
|---|---|
| file | `/usr/share/man/man1/sha256sum.1.gz` |
| registry row | `corpus/SOURCES.md:80` |
| file sha256 | `93c17dffe9f25d56291113d566a7de3ff65c29f8cc32c381801c49cf27e8403f` (identical to the row) |
| located line | decompressed **line 11** |
| exact quote (raw roff) | `Print or check SHA256 (256\-bit) checksums.` |
| exact quote (rendered) | “Print or check SHA256 (256-bit) checksums.” — 7 words |

Command: `sha256sum /usr/share/man/man1/sha256sum.1.gz && zcat /usr/share/man/man1/sha256sum.1.gz | sed -n '11p'`
(receipt `a1-s070-sha256sum-man.txt`).

Line 11 sits under `.SH DESCRIPTION` (line 8), not `.SH SYNOPSIS` (line 5, body 6–7 with no option entries) —
the label correction S073 already records, and the round-94 registry row does not repeat the old
SYNOPSIS claim.

**Does it ground its claim sentence?** Partly, and only as far as the row says. The registry cell is
“`sha256sum` prints or checks SHA256 (256-bit) checksums, and `--check` reads checksums from files rather
than computing a policy”, and the row's scope cell explicitly disclaims the validation rule (“not a
validation policy (the 64-lowercase-hex rule is this lane's choice)”). The C1 claim sentence that cites it —
“`S070` (installed `sha256sum(1)`, re-opened: the digest text the pin discipline rests on)” — is grounded
for *what a digest is*; it is **not** grounding for the pins table's format, the role column, or the
`--check` verification protocol. That is correctly scoped and no overreach was found.

### 1.2 S221 — installed `git-clone(1)`, `-s, --shared`

| field | value |
|---|---|
| file | `/usr/share/man/man1/git-clone.1.gz` (registry row names the canonical URL `https://git-scm.com/docs/git-clone`, page not fetched this round) |
| registry row | `corpus/SOURCES.md:233` (added this round, tier A, status `mined`) |
| file sha256 | `b3fd695ca3aeb5b315c0f87071972bfbebacc3cfaeb9a920075953dbded3802a` (identical to the row) |
| option head | decompressed **line 96**: `\fB\-s\fR, \fB\-\-shared\fR`; body lines 98–100 |
| located sentence | decompressed **line 100**: `to share the objects with the source repository\&. The resulting repository starts out without any object of its own\&.` |
| exact quote | “The resulting repository starts out without any object of its own” |
| word count | **11** tokens (`The resulting repository starts out without any object of its own`) |

Command: `sha256sum /usr/share/man/man1/git-clone.1.gz && zcat /usr/share/man/man1/git-clone.1.gz | cat -n | sed -n '96,124p'`
(receipt `a2-s221-git-clone-man.txt`). The NOTE paragraph at decompressed lines 104–124 also carries the
“`git repack` without `--local` … will copy objects … It is safe, however, to run `git gc`, which uses the
`--local` option by default” passage, i.e. the page grounds the seat-wide rule “never repack a shared clone”
as well as the “no objects of its own” sentence.

**Does it ground its claim sentence?** Yes. The claim sentence is “a `--shared` clone ‘starts out without any
object of its own’, which is why every battery fixture is a shared clone and never a citable archive”, and the
installed page states it verbatim at line 100. The inference the lane draws from it (a fixture tree is not
self-contained, so the source must keep its objects) is also supported by the NOTE and the `repack` paragraph
in the same option block. Tier A and the scope cell (“what a `--shared` clone stores … not Git's general
safety”) are consistent with what was read.

**But the lane's own `GATE-RECORD` for this source does not verify** — see finding **F2**. The source is
sound; the record written for it is not.

---

## 2. (b) Data-walk: the pins table for the planner

### 2.1 The table and its self-pin

```
$ cd $S/repo
$ grep -cE '^[0-9a-f]{64}' corpus/evidence/round94/instrument-pins.txt
34
$ sha256sum corpus/evidence/round94/instrument-pins.txt
6b2c5579794e0dc797671b49ef43b84b3848b7be2acac763501c1ebad294f1c4
```

The self row field is `498873a97c523fe89b9298c4fbf80387f60c106add0d32d2dcd08e8a7f80c2ee`, which equals
the sha256 of the 33 other rows joined in file order — the minus-self binding holds. Non-`driver` (covered)
rows: **14**; `driver` rows: **20**.

### 2.2 Every pinned file, grouped by role

Command (receipt `b-pins-datawalk.txt`):

```
$ python3 -B -   # walk corpus/evidence/round94/instrument-pins.txt, stat+sha256 each path under C
```

**role=instrument (5)** — every file an expected row executes

| path | size | sha256 |
|---|---|---|
| corpus/evidence/round89/curation-r89-controls.py | 12344 | fd54ab3cbc1c0ef9d64e7c586db6068e3afb3675d6274328e34c32b2bbf20d4b |
| corpus/evidence/round89/curation-r89.py | 16412 | 2c063f8bfab6922d199546494d2545f495b05ab9350a7379e1b7f4cde8939f4b |
| corpus/evidence/round89/gate-records-r89.py | 39022 | f34f59c87c08c11d762a1ae702251183eb72a27f7728504882e64ce24e6d2103 |
| corpus/evidence/round89/mutate-r89.py | 12982 | 10b43d8a69bfd56308320c7843291c2f425562a35d89aa9a360478d5b284c8eb |
| corpus/evidence/round90/harm-recheck-r90.py | 3516 | 4967755433f19b8ca5f070dcae377ba23989ae6c7971afa4d9936b06c3b3d3c8 |

**role=expectation (1)**

| path | size | sha256 |
|---|---|---|
| corpus/evidence/round94/controls/expected.tsv | 1940 | f62921b60ceed00fe147350d433c16fe18a17c00af369e7416030592f06562d7 |

**role=receipt (6)** — the committed control receipts

| path | size | sha256 |
|---|---|---|
| .../controls/receipts/c1-gate-r89.txt | 513 | 2499c186983ca0fde85c4e978a31667eadaf20dbddb93020abb3c2751c6c34b0 |
| .../controls/receipts/c1-harm-setup.txt | 200 | e847619bf01290c9375aeab95ab6b5fa5ac4f909062fb3b690306e4197cdfcdc |
| .../controls/receipts/c1-harm.txt | 163 | 52d880aec409d6a938d408f365985fe146515e563348a3eead4f843df867a4f3 |
| .../controls/receipts/c1-mutants-r89.txt | 2565 | 4584dab34d0e3df67e0806754cd796e46b9bd61eca15c1c4bd89f5f6a353ed6a |
| .../controls/receipts/c2-prior-controls.txt | 1767 | 6caa462da523f9c9bc1ffc773fe6154f0adbec3773fdea2cb79ca30c416dcd60 |
| .../controls/receipts/c2-prior-landing.txt | 530 | 21819ebc18d333333b151ec82d635d024b2515abb224dd9e5c579c32bd4e7b74 |

**role=claims (2)**

| path | size | sha256 |
|---|---|---|
| .ufo/waves/round-94/claims.json | 7756 | 089383c37929b109770330f7319b7ae312fa97a56a5535c4e345d93d8964a60c |
| .ufo/waves/round-94/claims.md | 12463 | 9d197d72bb29d16ed8b4bd92661ef7809dc8bb7199acfccfbc2fa6581e38996e |

**role=driver (20)** — byte-checked, no coverage invariant

| path | size | sha256 |
|---|---|---|
| corpus/evidence/round94/control-driver-r94.py | 28057 | 5ee9c1f93def25eb4a266bda4b68de3fc797b28037725ba873ba65668903532b |
| corpus/evidence/round94/curation-r94.py | 30170 | 4b9ce115e3700a7ec998c77128ad176b326ac6c126a0019709fad46eb29df144 |
| corpus/evidence/round94/skill-tally-r94.py | 15187 | da49d06896bc683ea782a72261021b9890c24c14694a39498315b6b48d8cd880 |
| corpus/evidence/round94/forgeries-r94.py | 10828 | f7dd794e3434bf0aa57b55cc491b60e87b68da0bcea85cacc4392318923a5d81 |
| corpus/evidence/round94/curation-controls-r94.py | 11419 | 79b76fdc14e9bc4c24e5b36e4b0076a4f0547b8a0f4afe3d81df4d0d9de0378f |
| corpus/evidence/round94/skill-tally-r94-controls.py | 10236 | 76840a4180c66f36713741f64bb31c283ed505a82e7ee5bda85af14fe66065a6 |
| corpus/evidence/round94/make-pins-r94.py | 5088 | 0638ed0a33236cfc548a3239dd6910594c2789079a6a743ea8a92174424f42f2 |
| corpus/evidence/round94/controls/legs.txt | 129 | 98731d3a9036e6806d72b6cf99550067f247b6321450e9f2b48a02ff63ac7cf9 |
| corpus/evidence/round94/controls/selftest-r94.txt | 14130 | 9c29428160768524c77407eedd711200be53a1074e2a22fe9bab814ad3f5bb37 |
| corpus/evidence/round94/evidence-before/c1-prior-accepts.txt | 974 | def717f1d314c55d1256ee2063785b64fa38b82e2e122b768eba9ef1f2b8653a |
| corpus/evidence/round94/evidence-before/c2-prior-accepts.txt | 873 | 8d2583c0d4780b7aa71790a762adf4e6f6d7a1dc772ef8aac7066db07b84c44d |
| corpus/evidence/round94/evidence-before/c3-prior-accepts.txt | 512 | 30329063f2d8fc35caaee4e3e73de999da29ac26a01d4b08b33830148b0cbcd7 |
| corpus/evidence/round93/control-driver-r93.py | 24695 | 732e6dffb0796176a6aefac091f67cf2440ca54c7c6e2b4b808d6897a0112dc2 |
| corpus/evidence/round93/curation-r93.py | 27488 | 6c3c58df40b0023c7344137b36279e3f329eb695f1f5f964937823c4752101d8 |
| corpus/evidence/round93/skill-tally-r93.py | 13202 | 54dfdd39a19577b3e185369ad72c1443070d44de946e1b57f86de348b9e89807 |
| corpus/evidence/round93/forgeries-r93.py | 9092 | c0beb9855289efa4d86eafd18f76fd2e8f2524eb234cc392d71c969d554ff749 |
| corpus/evidence/round93/curation-controls-r93.py | 10215 | 07b0be563e50225f784a81f7002fdb4475a13e4b518597fe4c19c37375729251 |
| corpus/evidence/round93/skill-tally-r93-controls.py | 7468 | 6cc56191fc0c321379e7d6325335c437bf03c730f83277edeaa2aa6dec0b0ef0 |
| corpus/evidence/round93/controls/legs.txt | 119 | c03774389e483de7d2d64d44b71291c5cfae3ff4df62a5e33de092d9b89f3142 |
| corpus/evidence/round94/instrument-pins.txt | 4174 | 498873a97c523fe89b9298c4fbf80387f60c106add0d32d2dcd08e8a7f80c2ee (minus-self) |

All 34 rows reproduce on disk at C. The pins table's own row is on the minus-self digest; every other row is
the plain file digest.

### 2.3 Which pinned files are NOT read by any instrument at run time

Method: (i) a static scan for every pinned path/basename across all 424 `.py`/`.sh` files under
`corpus/evidence/` and `tools/` (receipt `b-static-references.txt`); (ii) five completed
`strace -f -e trace=openat,open` runs of the scored commands — `control-driver-r94 verify`, `curation-r94`,
`skill-tally-r94`, and both control batteries — with the opening pid recorded per path (receipt
`b-runtime-reads-any-pid.txt`). Every one of the
34 paths is opened at least once, but for four of them the *only* reader is the pin walk's own `sha256_file`
call inside `control-driver-r94.py` — no instrument, and no battery, opens them for its own work:

| pinned file | role today | who opens it | what it actually is |
|---|---|---|---|
| `corpus/evidence/round94/evidence-before/c1-prior-accepts.txt` | driver | pin walk only (static scan: referenced only by `make-pins-r94.py`'s `DRIVERS` list, lines 40–42) | a prior-state evidence receipt |
| `corpus/evidence/round94/evidence-before/c2-prior-accepts.txt` | driver | pin walk only (same) | a prior-state evidence receipt |
| `corpus/evidence/round94/evidence-before/c3-prior-accepts.txt` | driver | pin walk only (same) | a prior-state evidence receipt |
| `corpus/evidence/round94/make-pins-r94.py` | driver | pin walk only; **no** scored command executes it (static scan: the string `make-pins-r94` appears in `.py`/`.sh` only inside that file itself) | the generator that produces the pins table |

That is the answer to “which pinned files are NOT read by any instrument at run time”: **exactly these four,
and all four carry `role=driver`** — the one role with no coverage invariant (named limit 2). The other 16
`driver` rows are live: the six r94 instruments and six r93 instruments are executed as processes by the
scored commands and their batteries, `controls/legs.txt` (both rounds) is read by the curation counters,
`controls/selftest-r94.txt` is read by `skill-tally-r94.py --selftest`, and `instrument-pins.txt` is read by
the driver.

Planner-relevant shape, stated without recommending an implementation:

- three of the four are **evidence**, not harness — the role enum has no `evidence`/`before` member, so a
  prior-state receipt and the driver itself are today indistinguishable in every way the role leg checks;
- the fourth is the **generator** of the table that pins it — a self-referential row that no coverage
  invariant can reach, since `driver` rows are excluded from both `ok` and `covered` by construction
  (`role_report`, `covered = [rel for rel, _r in roles.items() if _r != "driver"]`);
- the class is exactly the C1 defect one level in: round 94 taught the table to say *what a row is*, and four
  rows still answer “harness” to a question whose honest answer is “evidence” or “tool”.
- any new role widens `ROLES` (`control-driver-r94.py:50`), the `role_report` set legs (lines 290–336) and
  `make-pins-r94.py`'s `add()` calls in the same commit (named limit 4 of C1) — and `make-pins-r94.py` is
  itself pinned, so the generator and the table move together.

Live-`driver` note for the planner: `corpus/evidence/round93/forgeries-r93.py` and
`corpus/evidence/round93/control-driver-r93.py` are executed *by the r94 forgeries battery*, not by the
`verify` command; the pin walk sees them only as bytes, which is correct but means a break in the r93
instruments is visible only through the battery.

---

## 3. (c) Unused imports and dead branches in the three r94 instruments

Command: `~/.local/bin/pyflakes <f>` (pyflakes 4.0.3 on CPython 3.14.8), plus
`~/.local/bin/ruff check --no-cache --isolated --select F,B,SIM,PLE,RET,ARG,C4 --target-version py313`, plus an
AST scan for unreferenced module-level defs, constant conditions and statements after a jump. Receipts
`c-lint-deadcode.txt`. `python3 -m pyflakes` is not installed in the system interpreter; the `~/.local/bin`
wrapper is (already present on this host, nothing installed this round).

**Unused imports: none.** pyflakes exits 0 on all three files, and the AST import/name cross-check reports an
empty unused set for each. Negative control: a two-line probe with an unused `import os` is caught
(`'os' imported but unused`, rc 1), so the clean result is a measurement, not a silent no-op.

**Dead branches:**

| file:line | symbol | what it is |
|---|---|---|
| `control-driver-r94.py:153` | `def instrument_rel(row, root)` | **zero call sites**. Docstring says “kept for compatibility; pinning uses `instrument_rels`”. Nothing in the tree imports `control-driver-r94` as a module (`grep` for `import control_driver` finds nothing), so the compatibility claim has no holder. Inherited: `control-driver-r93.py:141` has the same dead def. |
| `curation-r94.py:196` | `def table_rows(lines, width)` | **zero call sites**. Its docstring role in the module header (line 19) describes the *r93 defect* it used to implement (silently dropping a wrong-width row); the S2 repair routes decision rows through `data_lines()` + `DECISION_WIDTH` (`curation-r94.py:403-407`) and never calls it. Inherited: `curation-r93.py:187` has the same dead def. |
| `control-driver-r94.py:290` | parameter `pins` of `role_report(...)` | **unused argument** (ruff `ARG001`): the role leg never reads a digest, only `roles`. |
| `skill-tally-r94.py:142` | loop variable `receipt` | **unused** (ruff `B007`); the same name is used in the *previous* loop at line 131, so the second loop's binding is vestigial. Inherited: `skill-tally-r93.py:135` has the identical pattern. |
| `control-driver-r94.py:213` | `env = {...}; return env` | `RET504` (unnecessary assignment); inherited from `control-driver-r93.py:201`. |

No constant-condition `if`, no `while False`, and no statements after a `return`/`raise`/`continue`/`break`
in any of the three. The remaining ruff hits are `SIM115` (bare `open(...)` without a context manager, 8
occurrences) and `SIM102`/`SIM905` style nits, all present in the r93 counterparts as well — i.e. the round
carried a codebase style forward rather than introducing a new class.

Dead-branch verdict for the planner: **no dead branch affects a leg.** `instrument_rel` and `table_rows` are
inherited dead weight (they are in the r93 instruments too, and both rounds pin those files), and neither is
reachable from a predicate. They are cleanup candidates, not correctness risks — but they are pinned under
`driver`, so deleting them is a table-moving commit, not a free edit.

---

## 4. Findings (each: command, receipt, observed line, exit code)

### F1 — C1: the forgeries battery does not meet its predicate at the carrier C

```
$ cd $S/repo            # HEAD = 352924bbea624caf3771ef291be98fd4ec679dda
$ python3 -B corpus/evidence/round94/forgeries-r94.py --root . --repo . \
    --rev 41038ed7c40cffc4cf86d649a6ba433c4b9eec1a \
    --receipts-rev 352924bbea624caf3771ef291be98fd4ec679dda --work "$S/work/c1forg"
...
FAIL s1-schema-two-column: r93 rc=0 r94 rc=0 needles=SETUP PIN_SCHEMA
OK   s0-schema-prior: r93 rc=0 (two-column table scores) r94 rc=2 (PIN_SCHEMA)
OK   positive: r94 rc=0
FORGERIES=FAIL FORGERY_REFUSED=4/4 PRIOR_ACCEPTED=4/4 SCHEMA_REFUSED=1/1 SCHEMA_PRIOR_ACCEPTED=1/1 CARRIED_REFUSED=2/2 POSITIVE=pass
$ echo $?
1
```

Receipt `b-c1-forgeries-at-C.txt`. The frozen C1 predicate requires this command to print `FORGERIES=PASS …
POSITIVE=pass` and exit 0; it prints `FORGERIES=FAIL` and exits 1. Every *integer* in the predicate line is
green — which is exactly why the defect is invisible to a reader who greps the predicate tokens.

Cause, read from the committed bytes: `case()` (line 127) always writes the table with `write_r94(...)` at
line 131 before running the r94 driver (the two-column form is written only for the *r93* call, line 133).
The `s1-schema-two-column` case (line 171) therefore passes a **three-column** table to the r94 driver and
asks it for `rc=2`; the driver correctly exits 0. Proof that the driver is right and the fixture is wrong:

```
$ python3 -B corpus/evidence/round94/control-driver-r94.py verify --root . --repo . \
    --rev 41038ed7…  --receipts-rev 352924bb… --pins "$S/work/schema/two-column-pins.txt" --work …
SETUP PIN_SCHEMA row is not `<sha256>  <role>  <path>`: 'fd54ab3cbc1c0ef9d6…  corpus/evidence/round89/curation-r89-controls.py'
$ echo $?
2
```

(receipt `b-c1-schema-twocol-proof.txt` — the same 34 rows projected to two columns, self row re-digested).
Second half of the cause: `schema_ok` (line 177) — and therefore the printed `SCHEMA_REFUSED` and
`SCHEMA_PRIOR_ACCEPTED` — is computed from the *separate* `s0-schema-prior` block, not from the
`s1-schema-two-column` case, so the integer that is supposed to witness the s1 case is decoupled from it.
The verdict token comes from `ok = all(results.values())` (line 215), which is the only place the failure
shows. The defective case is in the freeze F itself (`git show F:…forgeries-r94.py` line 171) and unchanged
at C. Separately, uncommitted work at the lane root has already deleted that line
(`git status` → ` M corpus/evidence/round94/forgeries-r94.py`, ` M …/make-pins-r94.py`, `?? …/after/`) — that
patch is **not** in C and does not change this measurement.

I did not run the remainder of C1's counting command twice: the `verify` half meets its predicate at C.

```
$ python3 -B corpus/evidence/round94/control-driver-r94.py verify --root . --repo . \
    --rev 41038ed7… --receipts-rev 352924bb… --work "$S/work/c1verify"
COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 PINNED_FILES=34/34 RECEIPT_PINS=6/6 PIN_ROLES_OK=14/14 CONTROL_DRIVER_R94=PASS
$ echo $?
0
```

(receipt `b-c1-driver-verify-at-C.txt`; `PINNED_FILES=34/34` matches the 34 data rows and `PIN_ROLES_OK=14/14`
the 14 non-`driver` rows, i.e. both ratios are full and neither can hide a deleted row.)

### F2 — Gate: the S221 `GATE-RECORD` fails the lane's own unchanged validator

```
$ python3 -B tools/gate-records.py verify --root . --repo . corpus/lessons/round-94.md
GATE_RECORD corpus/lessons/round-94.md:15 S221 FAIL PARSE
GATE_RECORDS files=1 records=1 ok=0 fail=1
$ echo $?
1
```

Receipt `d-gate-records-on-round94-lesson.txt`. The round-93 lesson verifies clean on the same tree
(`GATE_RECORD corpus/lessons/round-93.md:22 S001 OK`, `records=1 ok=1 fail=0`, rc 0), so this is not a
tool-wide regeneration artifact.

The record written at `corpus/lessons/round-94.md:15` is

```
GATE-RECORD S221 path=/usr/share/man/man1/git-clone.1.gz sha256=b3fd695c…3802a opened=2026-11-08 words=10 quote=The resulting repository starts out without any object of its own
```

Its key set is `{path, sha256, opened, words}`, which is none of the three forms `tools/gate-records.py`
documents and implements (`url/admit`, `url/unreach`, `rev` — see the module docstring, lines 20–27, and the
`parse()` key-set dispatch at lines 120–141). Across all 15 lessons carrying records, the key-set histogram
is 24 × url/admit, 9 × rev, 1 × url/unreach, and this single row — so the round introduced a fourth form that
the unchanged tool refuses by design. Two independent defects in the same line:

1. **shape**: no legal form exists for “a local file with no commit and no URL”; the round invented one
   rather than extending the tool (and the tool is explicitly unchanged this round);
2. **count**: `words=10`, but the quote has **11** whitespace-separated tokens (`wc -w` on the sentence →
   11). `check()` computes `n = len(quote.split())` and compares it to `kv["words"]` (lines 213–217), so
   even a new `path=` form would refuse this record as `WORDS`.

Why it is invisible: `tools/research-gate.sh` does not invoke `tools/gate-records.py` (no match in
9010+ lines), and neither does anything under the fleet's `scripts/`. `corpus/evidence/round94/controls/expected.tsv`
row `c1-gate-r89` runs `gate-records-r89.py` as a **battery** (`GATE_RECORDS_R89=PASS LEG_REREAD=16/16
CROSSCHECK=15/15`), not a lesson scan. So the round-94 Gate block is not read by any scored command. This is
the “unrun check has not passed” class, and it is the one thing in the Gate block that this seat can measure.

### F3 — Gate: `census-end.txt` is cited but absent from the tree

`corpus/lessons/round-94.md` §Gate states “Census exit 0 before (`corpus/evidence/round94/census-start.txt`)
and after (`corpus/evidence/round94/census-end.txt`), 219 → 220 rows”.

```
$ git -C $S/repo cat-file -e 352924bbea624caf3771ef291be98fd4ec679dda:corpus/evidence/round94/census-end.txt
fatal: path 'corpus/evidence/round94/census-end.txt' does not exist in '352924bbea…'
$ echo $?
128
```

`git ls-tree -r HEAD -- corpus/evidence/round94/` lists `census-start.txt` and nothing else census-shaped, and
the file is also absent from the lane worktree. The *number* is independently checkable and checks out:

```
$ git show 0f3f84da:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,} '   → 219
$ git show 352924bb:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,} '   → 220
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa W04 S051 … / S053 … / S073 … / S074 … / S075 …  ; chousa ok ; exit 0
```

so the after-state claim is true and its receipt is missing — a citation defect, not a false claim. The
`census-start.txt` that *is* committed contains the five `W04` lines and the `ok` line, i.e. the same shape.

### F4 — Observation, not a defect: `refetch.tsv` already carries an `S221`

`corpus/evidence/round57/refetch.tsv:189` is `S221  https://nlp.stanford.edu/IR-book/html/htmledition/tf-idf-term-weighting-1.html  64fdb414…  1  2026-11-08T11:05:29Z  28  000  -  -`
— the round-91 fetch that returned `curl rc=28` with no bytes and therefore wrote no registry row
(`corpus/lessons/round-91.md`: “No row is written for a fetch with no bytes … `grep -c '| S221 |'
corpus/SOURCES.md` → 0”). Round 94 then assigned `S221` to `git-clone(1)`, so one id now names two sources
across the two files. Nothing scores this: `scripts/sources-census.sh` never reads `refetch.tsv` (no
`refetch` match in 806 lines), and 26 other ids show the same registry-vs-refetch URL divergence (mirrors,
archive.org, later attempts), so this is the lane's normal retry log, not a forged row. Recording it because
a future reader cross-checking an `S221` record against `refetch.tsv` will land on the Stanford URL.

### F5 — C2 and C3 meet their predicates at C (measured, not asserted)

```
$ python3 -B corpus/evidence/round94/curation-r94.py --root .
... Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 Q_ROWS=20 WARRANT_OK=17/17 TFREQ_OK=17/17 DUP_QIDS=0 LEGS_MEASURED=16/16
VERDICT fields_hold=1 legs_ok=16/16 DETECTOR_WITNESS=17/17
CURATION_R94=PASS                                    rc=0

$ python3 -B corpus/evidence/round94/curation-controls-r94.py --root . --work "$S/work/c2ctl"
CONTROLS=PASS CARRIED_REFUSED_BOTH=4/4 WS_NAMED=2/2 PUNCT_NAMED=2/2 PUNCT_SHAPE_GREEN_R93=1/1 PRIOR_REGRESSION=7/7   rc=0

$ python3 -B corpus/evidence/round94/skill-tally-r94.py --root . --selftest corpus/evidence/round94/controls/selftest-r94.txt
TALLY_ROWS=8 STALE_TALLIES=0/8 TAIL_TALLIES=2 TAIL_OWNED_OK=2/2 HIST_DERIVED=2/2 HIST_PRESENT=2/2 CASE_RANGE_OK=2/2 MISLABELED=0 LEGS=4/4
SKILL_TALLY_R94=PASS                                 rc=0

$ python3 -B corpus/evidence/round94/skill-tally-r94-controls.py --root . --work "$S/work/c3ctl"
CONTROLS=PASS CARRIED_REFUSED=6/6 MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2 DOUBLE_REFUSED=1/1 HEADING_ALIAS_ACCEPTED=1/1   rc=0
```

Receipts `c2-curation-at-C.txt`, `c2-controls-at-C.txt`, `c3-tally-at-C.txt`, `c3-controls-at-C.txt`. The C2
classification sentence is confirmed on the same bytes: `x1-punct-dash` and `x2-punct-dots` are refused by
both counters at rc 1, while the control prints `punct-classification: r93 Q_SHAPE_FAIL=0 on both punctuation
trees` — r93 fails them downstream and cannot name the class, exactly as claimed. The C3 discrimination is
confirmed the same way: `moved-tail-215` and `moved-tail-283` score `r93 rc=0 … PASS` and `r94 rc=1 … FAIL`,
and `moved-to-heading` scores rc 0 on both (named limit 1, measured rather than hidden).

One calibration note on C2 that is inside no named limit: the S1 repair routes *Located-quote* rows through
`quote_lines()` (header + separator skip only, `curation-r94.py:177-194`), but the *decision-table* path still
collects through `data_lines()` (line 403), which drops any row whose first cell is literally `qid`,
`Situation`, or empty (`curation-r94.py:167-175`). `DECISION_COUNTS` (lines 85-89) catches a *deletion* of
such a row, because the per-entry count falls; a *substitution* that keeps the count would not be caught by
that leg. Not a kill-rule hit — the count pin does move on the simple forgery — but the S1 class is only
half-closed, and the surviving half is unnamed.

---

## 5. Limits of this seat

- Nothing was installed or upgraded this round; `pacman` was not invoked. `pyflakes 4.0.3` and `ruff 0.17.2`
  were already present at `~/.local/bin`; `strace` 6.x is the distro package. No network was used.
- `python3 -m pyflakes` is unavailable in the system interpreter (`No module named pyflakes`); the scan used
  the `~/.local/bin` wrapper and was validated with a negative control.
- The runtime-read map in §2.3 comes from `strace -f` on five scored commands plus a static scan of all 424
  `.py`/`.sh` files. The forgeries battery was traced only in part (killed once the static evidence and the
  untraced full run were in hand), so the `r93` instruments that only the battery executes are classified
  from `forgeries-r94.py`'s `OLD`/`NEW` call sites and the static scan, not from a complete trace.
- I did not modify any lane file. `forgeries-r94.py` at C is byte-identical to F (`sha256
  f7dd794e3434bf0aa57b55cc491b60e87b68da0bcea85cacc4392318923a5d81`); the lane worktree's uncommitted edits
  to `forgeries-r94.py` and `make-pins-r94.py`, and the empty untracked `after/`, are the L1's, and are
  reported here but not evaluated.
- F1 is measured on the carrier C. Whether C or a later commit is the “landing revision” the claim's K1
  names is the planner's call; at C the predicate does not hold.

---

## 6. Receipts copied into this folder

| file | what it holds |
|---|---|
| `a1-s070-sha256sum-man.txt` | S070 file sha256, decompressed line 11 raw, lines 8–14 and 54–58, rendered quote word count |
| `a2-s221-git-clone-man.txt` | S221 file sha256, decompressed lines 96–124, located sentence + line, 11-token count, the lane's GATE-RECORD line |
| `b-c1-driver-verify-at-C.txt` | `control-driver-r94.py verify` at C — full output, rc 0 |
| `b-c1-forgeries-at-C.txt` | `forgeries-r94.py` at C — full output including `FAIL s1-schema-two-column` and `FORGERIES=FAIL` |
| `b-c1-schema-twocol-proof.txt` | the driver refusing a genuine two-column table with `SETUP PIN_SCHEMA`, rc 2 |
| `b-pins-datawalk.txt` | the 34 rows by role with size and on-disk sha256, plus the table's full and minus-self digests |
| `b-runtime-reads-any-pid.txt` | per-path opener list from the six strace runs |
| `b-static-references.txt` | every static reference to each pinned path across 424 `.py`/`.sh` files |
| `c-lint-deadcode.txt` | pyflakes (3 clean + negative control), ruff (r94 vs r93), AST dead-def/constant/jump scan |
| `c2-curation-at-C.txt` | `curation-r94.py --root .` at C |
| `c2-controls-at-C.txt` | `curation-controls-r94.py` at C, including the `punct-classification` line |
| `c3-tally-at-C.txt` | `skill-tally-r94.py --selftest …` at C |
| `c3-controls-at-C.txt` | `skill-tally-r94-controls.py` at C, including both moved-tail cases |
| `d-gate-records-on-round94-lesson.txt` | `tools/gate-records.py verify` on `corpus/lessons/round-94.md` — `FAIL PARSE`, rc 1 |

Scratch `/fast/scratch/hyaku/chousa-r94/R94ScoutSources` was removed before yield; nothing was written under
`/tmp`, and no fixture git repo was created (none was needed).

---

VERDICT: R94ScoutSources C1 fired — at carrier C the frozen C1 forgeries battery prints `FORGERIES=FAIL` and exits 1 because its `s1-schema-two-column` fixture feeds the r94 driver a three-column table (`forgeries-r94.py:171` with `case()`'s `write_r94` at line 131) and the printed `SCHEMA_REFUSED` comes from the unrelated `s0-schema-prior` block, so the integer witness stays green while the verdict fails; the `verify` half meets its full predicate at C.
VERDICT: R94ScoutSources C2 held — `curation-r94.py` and `curation-controls-r94.py` print every frozen token with exit 0 at C, and the classification sentence re-derives (`PUNCT_SHAPE_GREEN_R93=1/1`, both punctuation trees refused by r94 at the shape leg); only the unnamed half of the S1 class in the decision-table path is left open.
VERDICT: R94ScoutSources C3 held — `skill-tally-r94.py` and its controls print every frozen token with exit 0 at C, and both moved-tail trees are refused by r94 while r93 accepts them (`MOVED_REFUSED=2/2 MOVED_PRIOR_ACCEPTED=2/2`).
VERDICT: R94ScoutSources n/a — the two C1 sources both open verbatim at their cited lines and ground their claim sentences, but the lane's `GATE-RECORD` for S221 fails the unchanged `tools/gate-records.py` (`FAIL PARSE`, rc 1, key set and `words=10` vs 11 tokens) and the cited `census-end.txt` is absent from the tree, both outside the three frozen predicates.
