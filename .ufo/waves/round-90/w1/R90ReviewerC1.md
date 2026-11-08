# R90ReviewerC1 — C1 clause-by-clause attack (`C1-DRIVER-R90`, operability)

**Seat.** `R90ReviewerC1` (leaf; no subagents, no git/jj mutation in the lane, no network).
**Attacked tree.** `9bad12011187d114ba2c4588c5df08a21ab28145` (clone `--shared` at that revision, driver run with
`--root . --repo .`); freeze `8d9893b42eb22690ea5f920ab87fd7e1810b847a`; receipts carrier
`9bad12011187d114ba2c4588c5df08a21ab28145`.
**Read.** `corpus/evidence/round90/claims.md`, `plans/round-90.md` (the `9bad` text — “Amendments after the freeze:
None yet” — plus the live working-tree amendments 1–6 present at read time), `control-driver-r90.py`,
`control-forgeries-r90.py`, `controls/expected.tsv` (six data rows), all nine files in
`controls/receipts/`, `corpus/evidence/round89/controls/run-controls.sh`, `harm-recheck-r90.py`.
**Counters.** Every observed line below is copied under `.ufo/waves/round-90/w1/R90ReviewerC1/`; the six scoring
receipts and the three before-receipts are copied under `…/R90ReviewerC1/receipts/`.
**Installs.** None. **Network.** None (the S220 capture was read from the local working copy only).

---

## 1. The frozen predicate, measured

| # | Command (cwd = clone at `9bad`) | rc | Observed line | Receipt |
|---|---|---|---|---|
| 1 | `python3 -B corpus/evidence/round90/control-driver-r90.py verify --root . --repo . --rev 8d9893b4… --receipts-rev 9bad1201… --work <scratch>/work` | 0 | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` | `verify-scored-9bad.out` |
| 2 | same, in the lane (`--root . --repo .`, work in scratch) | 0 | identical line | `verify-lane-9bad.out` |
| 3 | `python3 -B corpus/evidence/round90/control-forgeries-r90.py --root . --work <scratch>/forge --rev 8d9893b4…` | 0 | `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass` + `CONTROL_FORGERIES_R90=PASS` | `forgeries-battery.out` |
| 4 | hand fixture `C-duplicate-key` (stub prints `records=0 records=5`, committed receipt same, row requires `records=5`), r90 | 1 | `RECEIPT C-duplicate-key FINDING DUPLICATE_KEY:records,FRESH_DUPLICATE_KEY:records` → `…CONTROL_DRIVER_R90=FAIL` | `hand-dupkey.out` |
| 5 | same fixture, unchanged r89 driver | 0 | `RECEIPT_OK C-duplicate-key exit=0` / `CONTROL_RECEIPTS=PASS` | `hand-dupkey.out` |
| 6 | hand fixture `B2-substring` (body `LEG_REREAD=16/160`, row requires `LEG_REREAD=16/16`), r90 / r89 | 1 / 0 | `TOKEN_DETACHED:LEG_REREAD=16/160`, then `RECEIPT_OK … exit=0` | `hand-b2.out` |
| 7 | verify with `--receipts-rev 8d9893b4…` (disk bytes are the `9bad` receipts) | 1 | `RECEIPT SELF_PIN FINDING SELF_DRIFT …c1-gate-r89.txt,…,c2-prior-landing.txt` (all six) → `…CONTROL_DRIVER_R90=FAIL` | `verify-wrong-receipts-rev.out` |
| 8 | verify after one byte moved in `controls/expected.tsv` (`# drift probe` appended) | 1 | `RECEIPT SELF_PIN FINDING SELF_DRIFT corpus/evidence/round90/controls/expected.tsv` | `verify-expected-byte.out` |
| 9 | verify after `records=31` → `records=32` in the committed `c1-harm.txt` | 1 | all six rows still `OK committed+exact+pin+fresh` and `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6`, then `RECEIPT SELF_PIN FINDING SELF_DRIFT …c1-harm.txt` → `…CONTROL_DRIVER_R90=FAIL` | `verify-drift-receipt-byte.out` |
| 10 | verify with the receipts directory `chmod 0555` | 0 | `…CONTROL_DRIVER_R90=PASS` | `verify-readonly-receipts.out` |
| 11 | frozen-tree reproduction: receipts from `9bad` copied into a clone at `8d9893b4…`, `--root . --repo .` | 0 | `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS` | `verify-freeze-tree-8d989.out` |

Receipts untouched by the scored run: size/mtime `NO_STAT_CHANGE`, sha256 `NO_SHA_CHANGE`, clone working tree clean
after the run (`receipts-untouched.out`). The nine receipts are the six rows plus the three before-state files; each of
the six carries exactly one `# case=`, `# exit=`, `# computed_against=` header.

**Kill-rule state at `9bad`.** K1 clear (predicate met, twice: clone and lane). K2 clear (six classes refused, positive
accepted by both). K3 clear (no `RECEIPT … FINDING` on the committed set, no receipts write, bytes unchanged). K4
clear in its enumerated forms: `MISSING_RECEIPT` refused (probe P7 below), the committed receipt is read before the
fresh run (P1), the token leg is exact (P6/P12), and `verify` mints no pin (no write path under `receipts/`; only
`emit` writes there, line 217).

---

## 2. Clause table — ENFORCES / PRINTS ONLY / CANNOT SEE

| # | C1 clause (frozen sentence) | Instrument | Driver line(s) | Probe (receipt) and observed result |
|---|---|---|---|---|
| 1 | prints `CONTROL_DRIVER_R90=PASS` (exit 0) | **ENFORCES** (verdict = `passed`; rc) | 298–302 | §1 rows 1–2, rc 0 |
| 2 | with `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6` | **PRINTS**; three of four gate | 298 vs 299–301 | §1 row 9: `EXACT_OK=6/6` recomputed post-run; P1: `PASS` with `EXACT_OK=0/1` |
| 3 | “over the six committed receipts” | **ENFORCES** row count / presence | 225–236 | six data rows in `expected.tsv`; P7 `MISSING_RECEIPT` rc 1 (`probes-clauses.out`) |
| 4 | (a) “reads the committed receipt before any fresh run” | **ENFORCES per row** (read at 238, fresh at 265) | 238, 264–265 | P1: fresh stub rewrote the receipt to `LEG=BROKEN`; verdict still from pre-run bytes, rc 0 |
| 5 | (a) same clause read globally (all six before the first fresh run) | **CANNOT SEE** | loop order 231–265 | P2: row `a`'s fresh run rewrote row `b`'s receipt from `B=0` to `B=1`; row `b` then passed, rc 0 (no `--repo`) |
| 6 | (a) “writes nothing under the receipts directory” | **CANNOT SEE** (no guard); measured true | only writes: 217 (`emit`), 266–267 (`--work`) | §1 row 10 (dir 0555, rc 0) + `receipts-untouched.out` |
| 7 | (b) receipt's `# exit=` equals the row's expected exit | **ENFORCES on the last header** | 240–247, esp. 246–247 | P3: `# exit=1` then `# exit=0`, expected 0 → `PASS` rc 0, first header ignored (`probes-clauses.out`) |
| 8 | (c) every required `K=V` equals one whole whitespace-delimited body token | **ENFORCES** | 124 | P6 (`moved=0.5` vs `moved=0`, rc 1) and P12 (`16/160` vs `16/16`, rc 1) in `probes-clauses-2.out`; hand B2 rc 1 (`hand-b2.out`) |
| 9 | (c) “a token that starts with the key and differs is `TOKEN_DETACHED`, never a pass” | **ENFORCES** | 129–131 | P12 `TOKEN_DETACHED:LEG_REREAD=16/160` rc 1; P11 comment-only token → `TOKEN_MISSING` rc 1 (`probes-clauses-2.out`) |
| 10 | (d) every `key>=N` predicate; harm row's `records>=1` | **ENFORCES** | 135–152 | battery `B4-harm-vacuity`: `PREDICATE_SHORT:records=0<1` rc 1 (`forgeries-battery.out`); the real receipt binds on `records=31`; a literal `records>=1` token is unparseable (P10, `probes-clauses.out`) |
| 11 | (e) duplicate required key with different values → `DUPLICATE_KEY` | **ENFORCES for body keys**; **CANNOT SEE for header keys** | 125–127, 142–145 vs 90–99 | battery `C-duplicate-key` (`forgeries-battery.out`) + hand rc 1 (`hand-dupkey.out`); Q1 wanted-value-absent → `TOKEN_DETACHED:records=0,6` (refused, other label, `probes-clauses-3.out`); P3/P4/Q2 headers pass (`probes-clauses.out`, `probes-clauses-3.out`) |
| 12 | (f) `# computed_against=` equals `--rev` | **ENFORCES on the last header** | 253–259 | battery `B3b-stale-pin` → `PIN_MISMATCH` rc 1 (`forgeries-battery.out`); P4 wrong pin then right pin → `PASS` rc 0 (`probes-clauses.out`) |
| 13 | (f) scoring bytes byte-identical to their blobs at the named carrier revisions | **ENFORCES** for driver+expectations@`--rev`, receipts@`--receipts-rev` | 161–181, 283–289 | §1 rows 7–9: `SELF_DRIFT` rc 1 in each case; §1 row 11 shows the pins are consistent with the bodies |
| 14 | (g) “the instrument re-run … agrees with the committed receipt” | **PARTIAL/PRINTS**: exit + required tokens + predicates only | 264–277 | P8: committed `COUNTER=999`, fresh `COUNTER=2` (not a row field) → `PASS` rc 0; §1 row 9 shows only `SELF_PIN` sees the moved byte. Amendment 2 (working tree) narrows this wording |
| 15 | the six forgery classes refused by r90 / accepted by unchanged r89 | **ENFORCES the counts by exit code**; class token printed, not asserted | battery 138–151 | §1 row 3; hand runs 4–6; `git log f54a45e..9bad -- run-controls.sh` empty (r89 driver unchanged) |

Verdict vocabulary: **ENFORCES** = the value is computed from the receipt/fresh bytes and a wrong value refuses the
pass; **PRINTS** = printed but not part of `passed`; **CANNOT SEE** = nothing in the instrument inspects it.

---

## 3. Findings

### F1 (medium) — duplicated receipt headers resolve last-wins; a contradicting `# exit=` / `# computed_against=` / `# case=` passes

`header_fields()` (`control-driver-r90.py:90–99`) assigns `out[k.strip()] = v.strip()` per line, so the last `# k=v`
wins; `check_body`'s duplicate discipline (lines 125–127, 142–145) applies only to body tokens of required/predicate
keys, not to the three header fields.

- Command: `python3 -B …/control-driver-r90.py verify --root <fixture> --work <fixture>/w --rev 8d9893b4… --expected <fixture>/expected.tsv --receipts <fixture>/receipts`
- Receipt: `probes-clauses.out` (P3/P4), `probes-clauses-3.out` (Q2)
- Observed: `== P3 duplicate-exit-header rc= 0` → `RECEIPT p3 OK committed+exact+pin+fresh … CONTROL_DRIVER_R90=PASS`;
  `== P4 duplicate-pin-header rc= 0` → same; `== Q2 dup-case-header rc= 0` → same.
- Scope: the six committed receipts each carry exactly one of each header, so this does not fire on the scored set.
  It is the nearest unlisted forgery class. The working tree's Amendment 4(a)(b) already names it; the frozen text
  (clauses (b) and (f), “the receipt's `# exit=`”, “`# computed_against=`”) reads as a single value and does not.

### F2 (medium-low) — `EXACT_OK` is printed but excluded from the pass gate

`passed = findings == 0 and committed_ok == … and pin_ok == … and fresh_ok == …` (line 298) omits `exact_only`
(computed at 290–297 from post-run bytes). It is the only tally that can catch a receipt mutated during the row loop.

- Command: same verify form as F1 on fixture `p1-order` (fresh stub rewrites its own committed receipt to `LEG=BROKEN`).
- Receipt: `probes-clauses-2.out`
- Observed: `== P1 committed-read-before-fresh rc= 0` → `COMMITTED_OK=1/1 EXACT_OK=0/1 PIN_OK=1/1 FRESH_OK=1/1 CONTROL_DRIVER_R90=PASS`.
- On the scored path the same mutation is caught afterwards by `SELF_PIN` (§1 row 9), so this is a verdict-composition
  defect, not a live pass; it means the four printed tallies are not a joint condition.

### F3 (medium, operational) — `SELF_PIN` couples the scoring paths to `--repo`; the “lane + external clone” form fails on a clean tree

`self_pin` computes each scoring path with `os.path.relpath(..., repo)` (lines 168–171) and requires the resulting path
to exist in the named revision. If `--repo` is not an ancestor of the tree that holds the driver/expectations/receipts,
every path drifts.

- Command (driver invoked from the lane, repo = the clone): `python3 -B corpus/evidence/round90/control-driver-r90.py verify --root . --repo /fast/scratch/…/repo --rev 8d9893b4… --receipts-rev 9bad1201… --work <scratch>/w`
- Receipt: `verify-crossrepo.out`
- Observed: `RECEIPT SELF_PIN FINDING SELF_DRIFT ../../../../../../home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round90/control-driver-r90.py,…` (11 paths: driver, `expected.tsv`, nine receipts) → `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=FAIL`, rc 1.
- The frozen `--root . --repo .` form passes (§1 row 2); the assignment-shaped `<lane>` + external `<clone>` form is a
  false failure. The docstring advertises `--repo GITDIR` without this constraint.

### F4 (medium, claim provenance) — the S220 ground capture is absent at the freeze and at the attacked tree

The registry row `S220` cites capture key `e6ec761219e8044b0e9e067a`, but the capture is tracked only after `9bad`.

- Commands / receipt: `f4-capture.out`
- Observed: `f54a45e tracked_captures=181 e6ec_files=0`; `8d9893b4 tracked_captures=181 e6ec_files=0`;
  `9bad1201 tracked_captures=181 e6ec_files=0`; `aa7d4223 tracked_captures=183 e6ec_files=2`;
  `git log --diff-filter=A --all -- corpus/captures/e6ec…` → `aa7d4223 round-90: S220 source capture …`; `aa7d` is a
  descendant of `9bad` (`YES: aa7d is after 9bad`); the blob at `aa7d` equals the local file
  (`rev-parse`/`hash-object` = `1ccaefc77daf61c5c33101357bab45536512f6e0`).
- Consequence: at the attacked tree the row's cited capture bytes are not in the repo, so C1's whole-token contract is
  documentary at `9bad`; the registry move 218→219 is real (`SOURCES.md` +1 row, `S220`), and the capture text does
  contain the cited sentence (local `corpus/captures/e6ec…txt:165–168`: “`-x , --line-regexp` / Select only those
  matches that exactly match the whole line.”). Amendment-free; this is a freeze-completeness finding, not a driver
  defect.

### F5 (low-medium) — cross-row read order is not protected by order; a fresh run can rewrite a later receipt before it is read

With `--repo` the post-loop `SELF_PIN` (line 284) catches the rewrite as drift, so the scored path fails closed; without
`--repo` the rewritten receipt is simply believed.

- Command: verify on fixture `p2-crossrow` (row `a`'s stub rewrites row `b`'s committed receipt `B=0`→`B=1`).
- Receipt: `probes-clauses-2.out`
- Observed: `== P2 cross-row-ordering rc= 0` → `COMMITTED_OK=2/2 EXACT_OK=2/2 PIN_OK=2/2 FRESH_OK=2/2 CONTROL_DRIVER_R90=PASS`;
  `receipt-after: 'B=1'`.
- Clause (a)'s plain reading (“reads the committed receipt before any fresh run”) is enforced only per row.

### F6 (medium) — the instrument file a row executes is not pinned; a stub that prints the row tokens passes

`SELF_PIN` pins the driver, `expected.tsv` and the receipts (lines 168–171); it never pins the files the `instrument`
column names, and `instrument-pins.txt` is not read by the driver (`grep -c instrument-pins control-driver-r90.py` → 0).
Amendment 4(c) (working tree) already fires on this; the probe below is first-hand.

- Command: replace `corpus/evidence/round89/curation-r89-controls.py` with a 3-line stub printing
  `CONTROLS=PASS FORGERY_REFUSED=7/7`, then run the scored verify at the clone.
- Receipt: `f6-instrument-stub.out`
- Observed: `RECEIPT c2-prior-controls OK committed+exact+pin+fresh` … `RECEIPT SELF_PIN OK all scoring bytes equal
  their blobs at --rev` → `COMMITTED_OK=6/6 EXACT_OK=6/6 PIN_OK=6/6 FRESH_OK=6/6 CONTROL_DRIVER_R90=PASS`, rc 0
  (file restored afterwards; clone clean).
- Clause (f)'s “the scoring bytes” therefore does not include the bytes that produce the score by execution.

### F7 (low) — the forgery battery asserts refusal only by exit code

`want = new_rc != 0 and prior_rc == 0` (line 142); the finding class is printed (lines 145–149) but never asserted, so a
refusal for the wrong reason counts, and a crash counts as a refusal. `STUB` (line 30) is unused.

- Receipt: `forgeries-battery.out` (all six show the intended codes, so this is a latent defect, not a live one).

### F8 (low, diagnostic) — `SELF_PIN OK` names one revision though two are in play

Line 289 prints “equal their blobs at --rev”, but receipts are compared at `--receipts-rev` (line 284). §1 rows 7–9
show the second revision does the work. Amendment 4 assigns the message repair to round 91.

### Observations (not findings)

- **Named limit 2 confirmed.** P5: a required `moved=0` that appears only inside `debug: replayed moved=0 from cache`
  passes both legs (`probes-clauses-2.out`, rc 0). Whole-token matching is exactly as narrow as the limit says.
- **Named limit 1 confirmed.** P8/§1 row 9: non-required body bytes are not bound; a receipt body that no longer
  reproduces (`COUNTER=999` vs fresh `COUNTER=2`) passes without `--repo`.
- **Named limit 3 confirmed, with one added caveat.** The pin is self-declared: `git diff 8d9893b4..9bad1201` rewrites
  the `# computed_against=` line in all six receipts and the `c1-harm-setup` work path (`emit/`→`emit2/`) inside the
  very commit that pins them; the driver's PIN leg is string equality. The §1 row 11 run (receipts from `9bad` against
  a tree at `8d9893b4`) reproduces all six rows, so the pins are *consistent* with the bodies; provenance itself is
  not attested. Amendment 4 adds named limits 4–5 for the header and instrument cases.
- **Amendment 3 wording.** The three before-state files are not row-verified, but `SELF_PIN` does byte-pin them
  (list comprehension at 168–171 spans every `*.txt` in the directory); a moved `c1-prior-driver.txt` is `SELF_DRIFT`.
- **Caller-controlled write path.** If `--work` points inside `--receipts`, `verify` writes `fresh-<case>.out` there;
  the `.out` suffix escapes both the row check and `SELF_PIN` (it filters `*.txt`). Not exercised by the scored run.
- **Shell surface.** Instruments run through `bash -lc` (line 102) with `@ROOT@`/`@WORK@` interpolated unquoted
  (lines 216, 264); a root/work path containing spaces or shell metacharacters would split or inject. Not exercised.

---

## 4. Residual risk and verification gaps

1. The six-class battery covers the prior driver's B1–B4 and the new duplicate-key class. It does not cover duplicate
   headers (F1), instrument substitution (F6), cross-row ordering (F5) or non-required body divergence (P8). F5's
   scored-path consequence is closed by `SELF_PIN`; F1 and F6 are not closed by any leg, and both are now named in
   working-tree Amendment 4 with round-91 repairs.
2. The freeze-tree reproduction (§1 row 11) used the `9bad` receipts copied into an `8d9893b4` clone. It shows the
   receipt bodies reproduce against the freeze tree's bytes; it cannot show the receipts were emitted there.
3. Not exercised, and invisible to the driver by construction: a caller-chosen `--work` inside `receipts/`; paths with
   spaces/metacharacters; login-profile effects under `bash -lc`; a symlinked receipt; a receipts subdirectory named
   `*.txt` (`open(disk, "rb")` would raise).
4. F4 is a claim-package finding about the attacked tree; the capture is committed after `9bad` at `aa7d4223`, so a
   verifier working at `9bad` cannot check the S220 capture, and a verifier at later revisions can.
5. I did not audit C2 or C3 (other seats); nothing here is evidence for them.

---

VERDICT: R90ReviewerC1 C1 held — both scored commands reproduce the frozen tokens at `9bad1201` (PASS 6/6×4, `FORGERY_REFUSED=6/6 PRIOR_ACCEPTED=6/6 POSITIVE=pass`) and every enumerated kill rule is clear, but the sentence overstates four edges: duplicate `# exit=`/`# computed_against=`/`# case=` headers are accepted last-wins (F1), `EXACT_OK` does not gate the PASS (F2), the instrument files a row executes are unpinned (F6), and “agrees with the committed receipt” binds only exit + required tokens + predicates (clause-table #14 / P8, narrowed by Amendment 2).
