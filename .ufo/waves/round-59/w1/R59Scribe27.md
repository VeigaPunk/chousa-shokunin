# R59Scribe27 — round-59 Gate/Mistakes wording, from the round-58 lesson and spot-check

Seat: scribe (leaf; no dispatch, no fetch, no install). Axes: **depth** (primary), operability/calibration (subject matter).
Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`, HEAD `af8c0a460d087cbfb8245fb9326608783ccc510b`.
Item: "Read round58 lesson and spotcheck, draft evidence-backed round59 Gate/Mistakes or report wording. No writes except your report; do not claim checks unrun."

Writes: this file only. Scratch `/fast/scratch/hyaku/chousa-r59/R59Scribe27/` (form render, span-boundary probes, RSS probes, census sets), removed before yield. No git/jj/index write, no fleet/sibling/shokuknow/considerthese write, no counter/claim edit, no spawn. No install was performed; `~/.omp/agent/RULES.md` was therefore not needed (tooling directive binds "before any install").

Report: `.ufo/waves/round-59/w1/R59Scribe27.md`

---

## 0. Precondition — the lane context's frozen claims file does not exist

The lane context says to read `corpus/evidence/round59/claims.md` before work. Measured this seat:

```
$ find . -path ./.git -prune -o -path '*round59*' -name 'claims.md' -print
(no output)
$ find corpus/evidence/round59 -type f -printf '%s\t%TY-%Tm-%Td %TH:%TM\t%p\n'
535  2026-10-27 15:12  corpus/evidence/round59/census-start.txt
958  2026-10-27 15:14  corpus/evidence/round59/controls/c1-before.txt
$ ls .ufo/waves/round-59/            # w1.ready.dispatched and w1-results.json: absent
$ git status --porcelain
?? .ufo/waves/round-59/
?? corpus/evidence/round59/
```

So round 59 has **no frozen predicate at the named path** and no tracked round-59 byte. Every Gate sentence below is therefore an obligation, not an observation of an after-state; I do not invent a claim body. This is the same precondition `R59Scribe26` and the Scouts record; I re-measured it rather than citing them.

---

## 1. Inputs read (and which bytes they are)

| Input | Identity |
|---|---|
| `corpus/lessons/round-58.md` | 39 lines; `## Gate` + 1 `## Mistakes` row + spot-check/considerthese intake |
| `corpus/lessons/round-58-verifier-spotcheck.md` | 38 lines; author "hyaku closure", two admit/reject samples, routed defects |
| `corpus/evidence/round58/claims.md` | 25 lines; C1/C2 frozen predicates; C1 target `must print C1=PASS and exit 0` (line 9) |
| `corpus/evidence/round58/c1-count.py` | 406 lines, sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f` |
| `corpus/evidence/round58/controls/build-spans-r55.py` | sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` |
| `tools/build-spans.py` | sha256 `1ed2650a…0bf6` — **same bytes as the pinned r55 control** |
| `tools/capture-text.py` | sha256 `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` |
| `corpus/evidence/round58/controls/{c1-before,c1-controls,c1-control-build}.txt` | 958 B / 1,500 B / 135 B, read whole |
| `corpus/QUALITY.md` criterion 115 | line 974, read raw |
| `SCORECARD.md` | line 7: `operability | 3` (lowest numeric non-retired axis) |
| `corpus/SOURCES.md` | 133 rows (`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`) |

---

## 2. Measurements executed this seat

Numbers below are outputs I produced; reads-only claims are labelled. Where a check was **not** run, §10 says so.

### M1 — the round-59 "before" receipt is a byte copy, not a round-59 measurement

```
sha256sum corpus/evidence/round58/controls/c1-before.txt corpus/evidence/round59/controls/c1-before.txt
2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe  …/round58/controls/c1-before.txt
2c9bbe5446ae4f733bf17a2836cc1b32e823fc8bc287d3da42801b948cfaebfe  …/round59/controls/c1-before.txt
diff … → rc 0 (empty)
stat → both 958 B; round59 mtime 2026-10-27 15:14:30.645295308 -0300
```

The file names no command, builder, counter or revision; it is 16 lines of legs + `SUMMARY` + `C1=FAIL` + `EXIT=1`, with `DENIED=0/0`.

### M2 — the candidate builder is the baseline: three identities, one digest

```
git show b13ca7b5…:tools/build-spans.py | sha256sum  → 1ed2650a…0bf6
sha256sum tools/build-spans.py                       → 1ed2650a…0bf6
sha256sum corpus/evidence/round58/controls/build-spans-r55.py → 1ed2650a…0bf6
git log --oneline -8 -- tools/build-spans.py
6ca9249 round-55: C1 candidate — tools/build-spans.py reads every capture through its defined text form …
```

Round 58's diff (`git diff --stat b13ca7b5… HEAD`) is evidence, controls and lessons only; `tools/build-spans.py` was not touched. So C1's "before" builder, C1's declared target, and C1's discrimination control are **one artifact**; no hardened builder exists at the tip.

### M3 — the frozen aggregate, extracted and run (S1–S7)

Lines 389–394 were taken from the frozen file and executed in-process on synthesized leg strings (no counter run end-to-end, no lane write):

```
389 ok_pass = all(l.endswith("(pass)") or l.endswith(")") and f"{FAIL}" not in l and "=pass" in l for l in ok_legs)
390 ok_pass = all(("=pass" in l) for l in ok_legs)          # 389 is dead
391 ref_pass = all(("=PASS" in l) for l in ref_legs)
392 integrity = any(l == "BEFORE_FOREIGN=deleted" for l in legs)
393 denied_pass = (denied == total) if total else True
394 verdict = "PASS" if (ok_pass and ref_pass and integrity and denied_pass) else "FAIL"
```

| scenario | legs | frozen verdict | one-token fix (`=PASS`→`=pass`) |
|---|---|---|---|
| S1 every leg satisfied, lowercase emitters | all `=pass` | **FAIL** (`ref_pass=False`) | **PASS** |
| S2 same legs, uppercase token (no emitter can print it) | all `=PASS` | PASS | — |
| S3 refusal + `(target-dir-written!)` suffix | `SYMLINK_OUT=pass(refused)(target-dir-written!)` | FAIL | **PASS** ← certifies a write-through |
| S4 rc=0, target dir empty (override) | `SYMLINK_OUT=pass(refused)` | FAIL | **PASS** ← certifies a non-refusal |
| S5 pinned baseline not destructive | `BEFORE_FOREIGN=kept` | **FAIL** (`integrity=False`) | FAIL |
| S6 `--controls` absent | `denied=0,total=0` | PASS branch (`denied_pass=True`) | PASS |
| S7 the committed round-59 receipt's 13 leg lines | as committed | FAIL | FAIL |

Token inventory: `PASS = "pass"` (:51); every emitter interpolates the constant (`:147`, `:160`, `:207`, `:223`, `:234`) or hardcodes lowercase (`:315`); the only uppercase literals `=PASS` are at `:377` (parsing a child counter's verdict), `:378` (`CONTROL_*=PASS(!)`, a leg name outside `ref_legs`), `:391`, `:399`. Therefore `ref_pass` is False for **every** leg list → `C1=PASS` is statically unreachable, and `REFUSE=0/7` at `:399` is arithmetically forced.

### M4 — `expect_refuse` behaviour, executed from the AST-extracted function

```
rc=0                          -> SYMLINK_OUT=fail(rc=0, expected refusal)
rc=1, reason absent           -> SYMLINK_OUT=fail(rc=1, reason ['SYMLINK'] absent in …)
rc=1, reason ok, path absent  -> SYMLINK_OUT=fail(<path> was touched/removed)
rc=1, reason ok, path present -> SYMLINK_OUT=pass(refused)
```

`:157-160`: the `forbidden_touch` loop fails when the path **does not exist**. For `SYMLINK_OUT` the passed path is `real/"spans.tsv"` (`:232`), which only a *writing* builder creates — so a correct refusal is scored a failure, and `pass(refused)` requires the forbidden file to exist. The two lines at `:233-236` then overwrite the verdict `pass(refused)` whenever the target dir is empty, and otherwise append `"(target-dir-written!)"` to a string that still contains `=pass`.

### M5 — span formula: the false-FAIL window is `0 < off < 160`, not `0 < off < 80`

Builder `:142` `start = max(0, off - CONTEXT)`, `:143` `span = text[start : off+len(quote)+CONTEXT]`, written at `:149`.
Counter `:133` `start = max(0, form.find(quote) - CONTEXT)`, `:136` offset test, `:138` `span = form[offset : offset+len(quote)+min(CONTEXT, offset)+CONTEXT]`.

`offset` is the *span start*, so the correction term is `min(80, max(0, off-80))`, which is 0 for every `off ≤ 160`. Executed boundary probe (synthetic `.txt` cache, 16-char quote, candidate builder in scratch):

| quote offset `off` | manifest offset | builder span len | counter span len | equal |
|---|---|---|---|---|
| 0 | 0 | 96 | 96 | **yes** |
| 26 | 0 | 122 | 96 | no |
| 79 | 0 | 175 | 96 | no |
| 80 | 0 | 176 | 96 | no |
| 155 | 75 | 176 | 171 | no |
| 159 | 79 | 176 | 175 | no |
| 160 | 80 | 176 | 176 | **yes** |
| 161 | 81 | 176 | 176 | **yes** |
| 200 / 320 | 120 / 240 | 176 | 176 | **yes** |

So a *correct* builder fails `expect_ok` for any quote at `0 < off < 160`; passing needs `off = 0` or `off ≥ 160`. This refines the round-58 finding (which stated the boundary at `CONTEXT`) and constrains any positive-control fixture.

### M6 — the FAT_RAW leg cannot certify a size bound, and no bound exists

Fixture (`c1-count.py:283-295`): 8-byte OLE magic, then `truncate(80 MiB)`. Builder path (`tools/build-spans.py:74-82`): `raw.is_file()` → read 8-byte head → head is OLE → `b = raw.read_bytes()` (whole file, no cap) → `capture-text.text_form` → OLE parser refuses `ole-malformed: sector shift 0, mini shift 0` (the bytes after the magic are zeros).

Executed with the candidate builder and scratch fixtures:

```
1 MiB OLE-headed  : rc=1  maxrss(children)=36,236 KiB (~35.4 MiB)  "ole-malformed: sector shift 0, mini shift 0"
80 MiB OLE-headed : rc=1  maxrss(children)=185,332 KiB (~181.0 MiB) same message
```

`grep -n '1024\|size\|st_size' tools/build-spans.py` → no match: there is no 64 MiB cap. `capture-text.py`'s `MAX_PART = 256*1024*1024` (`:78`) bounds inflated OPC parts, not the OLE file. The refusal in the receipt is the OLE parser **after** an unbounded read, so `FAT_RAW`'s expected `SIZE` reason is unreachable and C1's claim point (4) ("raw reads are bounded at 64 MiB") is contradicted at the tip.

### M7 — the receipt's refusal ids are the intended fixtures

`key(url) = sha256(url)[:24]` (`c1-count.py:72-73`); computed: doc7 → `f4088c6d6da1f4763182a51d` (FIFO), doc8 → `a172f04219497476db868414` (devzero symlink), doc5 → `f96cbd6d82dbae8a8e2c6223` (FAT). All three match the receipt, so the failure texts are attributable to the fixtures built, not to a stray key.

### M8 — S101 re-opened offline (defined form re-derived, not copied from the round-58 record)

```
python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
  → rc 0, 27,012 characters (47,356 UTF-8 bytes), sha256 a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867
以并[文献类型标识/载体类型标识]表示 → `并以[文献类型标识/载体类型标识]表示`: offset 797, count 1, 19 characters, 1 whitespace token
12 frozen quotes: 12 rows, 12 unique, occurrence counts all 1
offsets [315, 330, 590, 683, 734, 781, 797, 838, 965, 993, 1460, 11723]
line-start anchors exactly {315, 330, 993} → 3/3 (the frozen floor, no margin)
```

### M9 — census: warning set identical, wrapper not byte-identical

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md → 133
round58/census-end.txt: 9 lines, carries "Command: …" + blank + "EXIT=0"
round59/census-start.txt: 7 lines, carries "exit=0"; sha256 09ce4a959ddba208da141bc97e872fd5eb36fd428390a1ecf8cf741853016207
warning lines (5 W04 + the `chousa ok` line): identical sets (diff empty)
```

So the round-58/round-59 census *result* is unchanged, but the two files are **not** byte-identical; wording that calls them identical is wrong about the artifact while right about the outcome.

---

## 3. Findings (reported, not fixed)

**F1 — carried receipt, and the before-state is the candidate itself.** `round59/controls/c1-before.txt` is sha256-identical to `round58/controls/c1-before.txt` (M1) and, because `tools/build-spans.py` is unchanged since `6ca9249` (M2), the receipt's legs also describe the *current* candidate. That is not a before-state: one artifact is before, candidate and control. Record it `CARRIED`, never `BEFORE`. Flip: a receipt naming its command, builder digest and revision and regenerable from round-59 bytes.

**F2 — `C1=PASS` cannot be printed, for any builder.** Emit side is lowercase (`:51,:147,:160,:207,:223,:234,:315`); scan side is uppercase (`:391`, summary `:399`). M3: all-pass legs → `REFUSE=0/7`, `C1=FAIL`; the only strings that satisfy `:391` are `:377/:378`, which are not in `ref_legs`. The dead first `ok_pass` (`:389`) shows the safe teeth are the reassigned `:390`; the refusal teeth were never re-derived. The round-58 lesson's cite list (`51,160,223,234,391,399`) is accurate but incomplete: it omits `:232-236` (F3/F4), `:389` and `:392` (F5).

**F3 — `forbidden_touch` is inverted.** `:157-160` fails when the path is *absent*. With `real/"spans.tsv"` as the "forbidden" path (`:232`), a refusal that writes nothing scores `fail(… was touched/removed)`, and `pass(refused)` is reachable only when the file exists. Executed (M4).

**F4 — the `SYMLINK_OUT` override certifies non-refusals, and the suffix does not fail.** `:233-236`: an empty target dir rewrites *any* verdict to `pass(refused)` — including `rc=0` acceptance (S4) — and a non-empty target appends `"(target-dir-written!)"` to a string that still contains `=pass` (S3). Consequence: **flipping the token, the obvious repair, turns both into PASS** (M3 S3/S4). The suffix must be a failure token, and the verdict must be derived from `rc ≠ 0 ∧ reason named ∧ target untouched`; the empty-dir rewrite must go.

**F5 — `integrity` requires the control to be destructive.** `:392` demands `BEFORE_FOREIGN=deleted`. With candidate == pin (M2) the receipt's `BEFORE_FOREIGN=deleted` is the candidate's own behaviour, not independent evidence that the leg discriminates; and a round-59 freeze that pins its *hardened* builder as the baseline makes `integrity=False` (S5). A positive-control freeze needs two distinct builders: the candidate under test and a destructive pin, with different digests.

**F6 — the FAT_RAW leg certifies nothing about size.** The fixture's 8-byte header routes to the OLE parser; the refusal reason is `ole-malformed`, not `SIZE`; the builder reads the 80 MiB whole (181.0 MiB peak) and has no cap at all (M6). C1's claim point (4) is false at the tip, and the leg that was supposed to test it tests the parser instead. Flip: a builder that measures size before reading, and a fixture with a *well-formed* header so the size path is the only refusal available; the receipt must show `SIZE` **and** a peak-RSS bound.

**F7 — the span formula's false-FAIL window is twice the documented one.** `:138` uses `min(CONTEXT, offset)` where `offset` is the span start, so any quote at `0 < off < 160` makes a correct builder fail (M5). A positive-control fixture must place every quote at `off = 0` or `off ≥ 160`, or the counter's term must be `min(CONTEXT, form.find(quote))`.

**F8 — `DENIED=0/0` is a default-true leg.** `:393` with `--controls` default `None` (`:169`) prints `DENIED=0/0` and is credited (QUALITY 103). The round-59 receipt ran without controls, so the deny leg is unexercised in the only pre-data artifact.

**F9 — a spot-check count is mislabelled.** `round-58-verifier-spotcheck.md:26` calls the S101 quote "19 whitespace-delimited words". Measured (M8): 19 **characters**, **1** whitespace-delimited token. The lane's own `s101-open.txt` already says "19 characters; one whitespace-delimited word". The ≤25-word Gate shape holds under either reading, but the sentence is wrong and the round-59 Gate should carry the corrected wording rather than repeat it.

**F10 — "census identical" is true of the result, false of the artifact.** M9.

---

## 4. Draft `## Gate` for `corpus/lessons/round-59.md`

> Draft only. `⟨…⟩` are facts the round owner must supply; nothing here asserts a pass. Evidence tags are mine and are not part of the lesson wording.

### Pre-data control state — carried, not credited

- The round's only pre-data receipt is `corpus/evidence/round59/controls/c1-before.txt`: 958 B, sha256 `2c9bbe54…ebfe`, **byte-identical** (`diff` empty) to `corpus/evidence/round58/controls/c1-before.txt` [M1]. It names no command, builder, counter or revision, and no round-59 counter exists to regenerate it (`corpus/evidence/round59/` holds two files, neither tracked) [§0, M1].
- The receipt's legs also describe the current candidate, because `tools/build-spans.py` has not changed since `6ca9249` and is byte-identical to the pinned r55 control and to the round-58 base: `1ed2650a…0bf6` three times [M2]. It is therefore recorded **`CARRIED`**: a round-59 before-state is *not* established, and the receipt is not independent evidence for the target's discrimination.
- Its `DENIED=0/0` is the default-true branch (`c1-count.py:393`, `--controls` default `None` at `:169`) [M3/M4] and is recorded as **unexercised**, never as a pass (QUALITY 103).
- Its `REFUSE=0/7` is not a data result. `PASS = "pass"` (`:51`) is what every refusal emitter interpolates (`:160`, `:223`, `:234`), while the aggregate searches literal `=PASS` (`:391`, `:399`); the only uppercase literals are `:377/:378` (outside `ref_legs`) and the two tests. An all-pass leg list still yields `C1=FAIL` [M3 S1]. `C1=PASS` is **statically unreachable for every builder**, not merely unobserved.

### Positive verdict-path calibration — what this round must demonstrate before any C1 verdict

Criterion 115 is met as *text* (`corpus/QUALITY.md:974`) and was not met by the artifact that exists. Round 59's declared work is the control, so the Gate registers these obligations; each names the falsifier that will kill it. None is satisfied today.

1. **One token on both sides, plus a must-pass receipt.** The aggregate's scan token and the per-leg emitter token must be the same constant, and a positive builder that satisfies every declared leg must print the declared verdict and exit 0. Falsifier: an all-legs-satisfied list that still prints `FAIL` (`:391` today) [M3 S1]. Repair note: the token flip alone is **not** sufficient — it converts F3/F4 into false PASSes [M3 S3/S4].
2. **A positive fixture must be inside the span window.** Every quote placed at `off = 0` or `off ≥ 160`; the measured false-FAIL window is `0 < off < 160` (`:138` vs builder `:143`) [M5]. Falsifier: any positive receipt whose quotes sit at `0 < off < 160`.
3. **The non-touch check tests absence, not presence.** A refusal must score `pass(refused)` only when the forbidden path is *absent*; today `:157-160` requires it present and the `SYMLINK_OUT` override (`:233-236`) discards the verdict whenever the target dir is empty [M4, S3/S4]. Falsifier: a builder that exits 0 and writes nothing scored `pass(refused)` (today: yes, under a token fix).
4. **`FAT_RAW` must refuse by size, after a bounded read.** A well-formed 80 MiB OLE fixture, a refusal reason naming the size bound, and a measured peak RSS below the bound. Today the fixture's malformed header diverts to `ole-malformed`, the builder reads all 80 MiB (181.0 MiB peak) and carries no cap [M6]. Falsifier: a receipt whose FAT_RAW reason is not the size class, or whose peak RSS exceeds the declared cap.
5. **The discrimination pin has a different digest from the candidate.** `integrity` (`:392`) requires `BEFORE_FOREIGN=deleted`; with candidate == pin that line proves nothing about the candidate and, once the candidate is hardened, pinning it makes `integrity=False` [M2, M3 S5]. Falsifier: a receipt where the pin digest equals the candidate digest.
6. **Every receipt names its command, counter digest, builder digest and revision, and is regenerable from this round's bytes.** Falsifier: a receipt with no command line (today's), or one whose `diff` against the previous round's receipt is empty.

### Source re-opened offline (no fetch)

- S101 — `corpus/SOURCES.md:111`, tier B, `mined`, `opened` 2026-10-25, recheck 180d. Bytes `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`, 129,024 B, sha256 `6063a3af…ddf3`, record rows `corpus/evidence/round57/refetch.tsv:19` and `:66` [as filed; not re-fetched].
- Defined form by the pinned reader (`2c0140bc…2573`): **27,012 characters**, digest `a8e3e7ad…f867`, re-derived this seat [M8].
- **Located quote:** `并以[文献类型标识/载体类型标识]表示` — char **797**, count 1, **19 characters / 1 whitespace token** [M8]. The 12 frozen quotes re-locate uniquely at `315,330,590,683,734,781,797,838,965,993,1460,11723`, with exactly **3** line-start anchors (315, 330, 993); the floor has no margin [M8].
- The row's anchor cell still names the six old offsets (11170, 11205, 11993, 12161, 13247, 34374) of an undefined raw decode; this round records the mismatch and edits no cell.

### Admit / reject

- **Admit as source evidence, not as knowledge:** the lane-held S101 form states scoped rules and examples for reference-type and carrier labels. No `knowledge/` entry lands while no counter can verify a predicate [§0, F2].
- **Reject:** present-day status, legal force or current use of GB3469; no fetch this round, L0 question `8d77e6c1` open. Flip: an operator-approved research window **plus** a located current authority.
- **Reject:** any `C1=PASS`/`C2=PASS` citation, and any citation of `FAT_RAW` as a size-cap leg [F6].

### SOURCES changes

- Rows: **133 → 133**; added by tier A/B/C: 0/0/0. Round-start census `round59/census-start.txt` (535 B, sha256 `09ce4a95…6207`): five pre-existing W04 warnings, `exit=0`; the warning set is identical to `round58/census-end.txt` (whose wrapper lines differ — `Command: …`/`EXIT=0` vs `exit=0`) [M9].
- No cell change is proposed. S101's `used-by` names `corpus/lessons/round-58.md`; it must not name a file that does not exist.

### Outside spot-check — recorded with one correction

- Sample: `corpus/lessons/round-58-verifier-spotcheck.md`, two decisions, both **agree** with the round-58 Gate: (a) admit S101's notation as source evidence only; (b) reject present status/legal force with the stated flip. My re-derivation of the quote (char 797, count 1, 27,012-char form) makes (a) reproducible [M8].
- Correction carried with the sample: the closure artifact calls the quote "exactly 19 whitespace-delimited words"; measured, it is 19 **characters** and **1** token [M8, F9]. The ≤25-word shape holds; the count is mislabelled. Record the corrected sentence; do not rewrite the closure artifact (QUALITY 101).
- No discernment improvement is claimed from this seat: a scribe inside the same dispatch is not a non-author reader.

### Wave-shape honesty (QUALITY 99)

`w1.ready` exists; `w1.ready.dispatched` and `w1-results.json` do not; 58 reports were on disk at read time [§0]. The report may say "W1 filed N seats, results not yet committed" — it must not say the wave was dispatched or settled until a marker or results file exists.

---

## 5. Draft `## Mistakes` rows for `corpus/lessons/round-59.md`

Format: class · Evidence · Captured-by · Fix · Shown able to fail.

1. **inert — the round's "before" receipt is a byte copy of the previous round's and its leg set is the candidate's own behaviour.** Evidence: `corpus/evidence/round59/controls/c1-before.txt` is 958 B, sha256 `2c9bbe54…ebfe`, `diff`-empty against `round58/controls/c1-before.txt`; `tools/build-spans.py`, the r55 pin and `git show b13ca7b5:tools/build-spans.py` are one digest `1ed2650a…0bf6`; the receipt names no command, builder or revision; the round-59 evidence tree holds two files and no claims file. Captured-by: QUALITY 115 and QUALITY 105/108 (a receipt names its revision). Fix: at freeze, every control receipt must name command + counter digest + builder digest + revision and regenerate from this round's bytes; a copy is recorded `CARRIED`. Shown able to fail: the file's own `C1=FAIL` / `EXIT=1` and 0 occurrences of `C1=PASS` [M1, M2].

2. **unreachable — the frozen C1 aggregate cannot print its own PASS token, for any builder.** Evidence: `PASS="pass"` (`:51`) vs `ref_pass` scanning `=PASS` (`:391`, `:399`); emitters `:147,:160,:207,:223,:234`; hardcoded lowercase `:315`; the only uppercase literals are `:377/:378` (outside `ref_legs`) and the two tests. Executed: the extracted aggregate on an all-pass leg list → `REFUSE=0/7`, `C1=FAIL`; with uppercase refusal rows → PASS, which no emitter can produce. Captured-by: QUALITY 115. Fix: append this sharper derivation; do not edit the frozen counter; a re-frozen counter uses one constant on both sides and ships a must-pass receipt. Shown able to fail: both rounds' receipts print `OK=4/4 REFUSE=0/7 C1=FAIL` [M3].

3. **inverted/overridden — the symlink-out leg cannot distinguish a refusal from a no-op, and its failure suffix is not a failure.** Evidence: `expect_refuse` fails when the forbidden path is absent (`:157-160`), and the passed path (`:232`) is one only a writer creates; `:233-236` rewrites any verdict to `pass(refused)` when the target dir is empty and otherwise appends a suffix to a string still containing `=pass`. Executed: `rc=0, empty target` → `SYMLINK_OUT=pass(refused)`; refusal + write → `…pass(refused)(target-dir-written!)`. Captured-by: QUALITY 103/115. Fix: verdict from `rc ≠ 0 ∧ reason ∧ target untouched`, absence must be the *pass* condition, and the write suffix must be a failure token; delete the empty-dir rewrite. Shown able to fail: the fixture itself (`c1-count.py:227-236`) and the executed table [M4; S3/S4].

4. **masked — the token defect is the only thing currently rejecting two machines the counter would otherwise certify.** Evidence: with the scan token changed to lowercase, S3 (write-through into the symlink target) and S4 (`rc=0`, no write) both print `C1=PASS` in-process. Captured-by: this is the "repair one defect, inherit two" class; QUALITY 115's check only asks the positive path to be reachable, not that every negative fixture still fails after the repair. Fix: the re-frozen counter must ship a *negative* matrix alongside the must-pass receipt — one deny per leg, each killing with its own suffix. Shown able to fail: the executed matrix [M3].

5. **unbounded — `FAT_RAW` refuses for the wrong reason and no size cap exists.** Evidence: the fixture writes 8 OLE magic bytes then truncates to 80 MiB (`c1-count.py:283-295`); the builder reads the whole file before parsing (`tools/build-spans.py:74-82`, `raw.read_bytes()`), `capture-text` refuses `ole-malformed: sector shift 0, mini shift 0`, and the expected `SIZE` reason is absent; `grep` finds no size constant in the builder. Measured: 1 MiB input → 35.4 MiB child peak, 80 MiB input → 181.0 MiB peak, both `rc=1`, same message; c1's claim point (4) says "bounded at 64 MiB". Captured-by: QUALITY 103 (the check's denominator must be the class it claims) and QUALITY 115. Fix: measure size before reading, build a well-formed 80 MiB fixture so size is the only available refusal, and require both the `SIZE` reason and a bounded peak RSS. Shown able to fail: the receipt line plus the RSS run [M6].

6. **off-by-one-window — a correct builder fails `expect_ok` whenever a quote sits within 160 characters of the form's start.** Evidence: counter `:133/:138` uses `min(CONTEXT, offset)` with `offset` = span start, while the builder writes `text[start : off+len+CONTEXT]` (`:142-143`); measured equal at `off ∈ {0, 160, 161, 200, 320}` and unequal at `off ∈ {26, 79, 80, 155, 159}`. Captured-by: QUALITY 96/103 family (a counter must be checked on a positive control). Fix: use `min(CONTEXT, form.find(quote))`, or bind the positive fixture to `off = 0 ∨ off ≥ 160`; whichever is chosen is recorded in the claim. Shown able to fail: the boundary probe [M5].

7. **vacuous — a zero-denominator leg defaults to true.** Evidence: `denied_pass = (denied == total) if total else True` (`:393`), `--controls` default `None` (`:169`); the round-59 receipt prints `DENIED=0/0` and is credited. Captured-by: QUALITY 103. Fix: refuse a zero denominator at the freeze surface (exit 2); the receipt says `UNEXERCISED`, not `0/0`. Shown able to fail: `DENIED=0/0` (this receipt) vs `DENIED=2/2` (`round58/controls/c1-controls.txt`, same counter with the flag) [M1, M3 S6].

Rows 1–7 are defects of the control surface, the fixture set or the builder; none of them re-claims C1.

---

## 6. Falsification matrix — what each drafted sentence dies on

| drafted sentence | falsifier | result |
|---|---|---|
| "the round-59 receipt is carried, not measured" | a round-59 receipt naming its command/revision, or differing bytes | **survives** — sha identical, `diff` empty, no command line |
| "candidate, pin and round-58 base are one digest" | a `tools/build-spans.py` change after `6ca9249` | **survives** — `git log` shows one commit, `git show` digest matches |
| "`C1=PASS` is unreachable for every builder" | an emitter in `ref_legs` that can carry uppercase `=PASS` | **survives** — uppercase literals only `:377/:378/:391/:399`; `:378`'s leg is `CONTROL_*` |
| "the token flip is not sufficient" | a scenario where flipping alone yields PASS on a bad machine | **refuted as a repair** — S3/S4 both flip to PASS |
| "the symlink-out leg passes a no-op" | an override that preserves the `rc=0` verdict | **survives** — `:233-236` rewrites unconditionally on an empty target |
| "FAT_RAW certifies no size bound" | a receipt whose FAT refusal names `SIZE`, or a builder size cap | **survives** — reason is `ole-malformed`; no cap in builder |
| "the false-FAIL window is `0 < off < 160`" | a probe at `off=159` that matches, or `off=160` that does not | **survives** — 159/160 straddle exactly |
| "19 characters, 1 token" | `len(q.split()) > 1` | **survives** — 1 token; 19 chars |
| "round-59 census result unchanged" | a differing warning line | **survives** — warning sets identical; wrappers differ |
| "no fetch this round" | a round-59 fetch record | **survives** — no round-59 record exists; newest rows are round-57 |

---

## 7. Conflicts with peer reports (recorded verbatim, not adjudicated)

- `R59Scout39.md:5` — "The round59 evidence directory contains `census-start.txt` (535 bytes), `controls/c1-before.txt` (0 bytes)". Measured: `c1-before.txt` is **958 B**, sha256 `2c9bbe54…ebfe` [M1]. The byte count is wrong; its "no claims file" finding agrees with §0.
- `R59Scout40.md:10` — "`corpus/evidence/round59/controls/c1-before.txt` is a direct before-capture for current calibration." Measured: it is byte-identical to the round-58 receipt and names no command or builder [M1, M2]; its leg *content* is consistent with the tip builder only because the builder is unchanged since round 55. That is `CARRIED`, not a capture of round-59 bytes. Its leg-by-leg reading and its `DENIED=0/0` caveat agree with §4.
- `R59Scribe26.md:§3` — "the round-59 legs are byte-identical to round-58's base receipt apart from `DENIED=`/`SUMMARY` counts and trailing newlines (`diff`)". Measured: the two files are **byte-identical with no exceptions** — same 958 B, same sha256, `diff` empty [M1]. The claimed difference does not exist; the `DENIED=2/2`/`SUMMARY` variant is `round58/controls/c1-controls.txt`, a different file.
- `R59Scribe26.md:§2 D2` — "the false FAIL fires when the quote occurs at `off < CONTEXT`". Measured boundary is `0 < off < 160`, i.e. `2 × CONTEXT` (M5): the seed-35 instance they report at `off=26` lies inside both statements, so this is a **refinement**, not a contradiction. Their D1/D3–D5 mechanisms agree with my independently executed M3/M4; their C2 derivation (builder writes `off-80`, counter binds `off`) is consistent with the line numbers I re-read (`build-spans.py:142,149`; `c2-count.py` binding per their report — I did not run it).

---

## 8. What this report does not claim

- No builder correctness claim: `tools/build-spans.py` is the r55 artifact; the legs I quote are the frozen counter's and are not my measurement of a hardened machine.
- No C1/C2 verdict, no `NEW_GROUND`, no knowledge admission, no SOURCES edit.
- No claim that `deny` controls were run in round 59 (they were not; `DENIED=0/0`).
- No adjudication of sibling findings beyond the four measured conflicts above.

---

## 9. Artifact paths

- This report: `.ufo/waves/round-59/w1/R59Scribe27.md`
- Draft target (not written by me): `corpus/lessons/round-59.md`
- Frozen inputs read: `corpus/lessons/{round-58.md,round-58-verifier-spotcheck.md}`, `corpus/evidence/round58/{claims.md,c1-count.py,controls/*}`, `corpus/evidence/round58/c2/quotes.tsv`, `corpus/evidence/round58/s101-open.txt`, `corpus/evidence/round59/{census-start.txt,controls/c1-before.txt}`, `corpus/QUALITY.md:974`, `SCORECARD.md:7`, `corpus/SOURCES.md`, `tools/{build-spans.py,capture-text.py}`, `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw`
- Scratch (removed before yield): `/fast/scratch/hyaku/chousa-r59/R59Scribe27/` — `form.txt`, `rss/{tiny,fat}`, `spanbound/{off0,off26,off79,off80,off155,off159,off160,off161,off200,off320}`, `{e.w,s.w}`, probe transients

---

## 10. Not run (so not claimed)

- `corpus/evidence/round58/c1-count.py` was **not executed end-to-end** against a builder. My C1 statements are: (a) the AST-extracted `expect_refuse` executed on stub processes (M4); (b) the aggregate lines `389-394` extracted and executed on synthesized leg lists (M3); (c) the committed receipts read. The M3 scenarios S1–S7 are in-process expressions of frozen code, not counter runs.
- `c2-count.py` was **not run**; the C2 offset/rebuild contradiction is cited from `R59Scribe26` and the frozen claims, not re-derived here.
- `scripts/sources-census.sh` was **not run**; `round59/census-start.txt` and `round58/census-end.txt` are cited as committed.
- `tools/quote-reopen.py` / `capture-fetch.py` were **not run** (they fetch; no fetch authorized). `tools/capture-text.py` was run locally on the lane-owned raw (M8) — no network.
- `tools/build-spans.py` **was** run, four times: once per span-boundary probe (M5), twice for the RSS probe (M6) — all with `--out`/`--cache` under my scratch, `cwd` in scratch, `PYTHONDONTWRITEBYTECODE=1`/`-B`; no lane path written. The M5/M6 fixtures are synthetic and are not C1's fixtures.
- No install, no `pacman`, no `~/.local/bin` or PATH write; hence no `RULES.md` read.
- Scratch removed before yield; `git status --porcelain` still lists only the two pre-existing untracked round-59 paths.

VERDICT: The draft survives as — a Gate that records the round-59 receipt as **`CARRIED`** (958 B, sha256 `2c9bbe54…ebfe`, `diff`-empty; candidate = pin = base `1ed2650a…0bf6`), states `C1=PASS` as statically unreachable (`PASS="pass"` at `:51` vs `=PASS` at `:391/:399`; executed all-pass matrix → `REFUSE=0/7`, `FAIL`), re-derives S101 offline (27,012-char form `a8e3e7ad…f867`; quote at 797, 19 chars/1 token; 12/12 unique; offsets as filed; 3/3 line-start, no margin), keeps 133 → 133 rows with no cell edit and a corrected census sentence, and refuses C1/C2/`FAT_RAW`-as-size-cap citations; plus seven Mistakes rows pinned to frozen lines. Falsified as repairs: "flip the token" (S3/S4 become PASS), "the pinned baseline proves the FOREIGN leg" (same digest as the candidate; `integrity` then fails), "FAT_RAW tests a 64 MiB cap" (no cap; 80 MiB input → 181.0 MiB peak), "the false-FAIL window is `off < 80`" (it is `0 < off < 160`), "the round-59 receipt differs from round-58's" (byte-identical). Unexecuted and named as such: both frozen counters, the census script, and any fetch.
