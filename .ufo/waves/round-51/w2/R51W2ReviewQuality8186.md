# R51W2ReviewQuality8186 — QUALITY 81-86, falsification

Lane tip `72566c8` (round landed at `4436e27`; freeze `d603f6f0`); every command run from the lane root as `env -u ASSIMILATE_CITES … TMPDIR=/dev/shm/chousa-r51-R51W2ReviewQuality8186`, read-only against the lane. No install, no network; scratch deleted; `git status` unchanged.

## Per-criterion

**81.** `c1-count.py --seed 424242` → `LEGS=5/5` `C1=PASS` rc 0. Red: `--tool controls/tool-before.py --seed 7` → `LEGS=1/5` rc 1; `flag-noop-tool.py` → `LEGS=2/5` rc 1; a copy at a wrong depth → `PIN_CHANGED … differ from their pin or are missing` rc 2. Cited lines accurate (`:101` urandom seed, `:121-127` id/host draws, `:77-83` adopt writes+run with no `--expected`, `:155-157` literal relations, `:47` pin). Mistakes row 2 exists. Both limits hold (`SELFTEST_DEFAULT=PASS (skipped: --tool)` observed; nonce legs never touch lane entries).

**82.** `c1-count.py --seed 424242` → `SOURCE_ONLY=PASS default_rc=0 map=['S662','S859'] appended=1 bodyonly=[['corpus/knowledge/e.md','S768']] all_map=['S662','S768','S859']`, `LEGS=5/5` rc 0. Red: `--tool flag-noop-tool.py --seed 7` → `SOURCE_ONLY=FAIL default_rc=0 map=['S524','S702','S833'] appended=2 bodyonly=[]`, `LEGS=2/5` rc 1. Mistakes row 3 exists. Defects D1-D3.

**83.** `c3-count.py` → `CAP_ROWS=36 (base 36)` `POINTERS=74 (base 74)` `RESOLVED_BY_CORRECTION=4` `DANGLING=0` `C3=PASS` rc 0; the four targets are non-empty (9 files / 7039 B / 4069 B / 4175 B). Red reproduces through `controls/build-c3-controls.py`: BLANKET byte-identical to `controls/c3-before-erratum.txt` (`DANGLING SCORECARD.md:1843 measure/final/` … `DANGLING=5 C3=FAIL`); the cited rows say what is claimed (SCORECARD.md:1843/2073/2074/2616, SHONEN.md:10). Mistakes rows 4, 5 exist. Defects D4-D5.

**84.** `receipt-check.py corpus/evidence/round50/measure-after.txt --skill SKILL.md` → `RECEIPT_NO_REV …`, `SKILL_NO_PIN SKILL.md`, `FAILS=2` rc 1. Scratch headers reproduce `RECEIPT_OK … rev=72566c84e418`, `RECEIPT_REV_UNKNOWN … rev=000…0`, `RECEIPT_REV_UNLANDED … rev=1fce006153ab`, `RECEIPT_TOOL_MOVED … rev=d603f6f00f78 tool=corpus/evidence/round51/c3-count.py`, `RECEIPT_DIGEST_MISMATCH recorded=000000000000 actual=14bfc2e42c68` (the quoted `94ddc7dc273c` is `c1-count.py`'s blob — reproducible), `RECEIPT_TOOL_ABSENT`, and `--root /dev/shm` → `ROOT_NOT_GIT` rc 2. Mistakes row 1 exists but is false (D8). Defects D6-D8.

**85.** `c1-supplement.py` → six legs `PASS 3/3`, `SUPPLEMENT_LEGS=6/6` `C1_SUPPLEMENT=PASS` rc 0. Claims reproduce: `forge-dirname.py` is 94 lines, frozen counter `LEGS=5/5 C1=PASS` vs supplement `1/6`; `tool-candidate1.py` `5/5` vs `3/6`; flag-noop `1/6`; `--seed 13` hangs (killed at 20 s); `ASSIMILATE_CITES=all` on the frozen counter → `LEGS=3/5`; `echo-tool.py:13`/`const-tool.py:10` `REAL = … / "tool-before.py"`, byte-identical to `git show 9ec1751a:tools/assimilate-rows.py`; fixed names at `c1-count.py:141,167,174,189`. Mistakes rows 2, 8 exist. Defects D9-D10.

**86.** `controls/build-c3-controls.py` → BLANKET `DANGLING=5 C3=FAIL`, DELETED `CAP_ROWS=32 POINTERS=59 C3=FAIL`, EMPTY `DANGLING=5 C3=FAIL`, DOTPATH `CAP_ROWS=37 POINTERS=75 RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS` rc 0, pre-erratum counter `DANGLING SCORECARD.md:2635 ufo/waves/round-51/gen-w1-spec.py`. My whole run matches `controls/c3-controls-final.txt`. Mistakes row 5 exists. Holds as written.

## Defects

**D6 (high) — 84's `--skill` leg never reads the Gates row; the stated red is a tool bug.** `receipt-check.py:56-60` (`header()`) reads `splitlines()[:5]` of the *whole file*, and `one()` sends the skill path through it. The Gates rows are SKILL.md:130/133 of a 736-line file, so `SKILL_NO_PIN` is unconditional: a scratch file with the header on line 7 inside a Gates row prints `SKILL_NO_PIN` rc 1, the same header on line 1 prints `SKILL_PIN_OK` rc 0. The row 84 blames is compliant: `HEAD_RE` against SKILL.md:130 → `('cf642c669b736bfba6b9fbb91fd5b16cb5579d9d','tools/assimilate-rows.py','6b975f91c809')`; `git merge-base --is-ancestor cf642c66 HEAD` → 0; `git rev-parse cf642c66:tools/… HEAD:tools/…` → both `d1483e79…`; tip-blob `sha256` → `6b975f91c809485c…`. The docstring's "or in a `SKILL.md` Gates table row" is unimplemented; fix by scanning table rows, not the first five lines.

**D4 (medium) — 83 restates "a later `correction:` line"; the counter accepts any order.** `c3-count.py:96-100` fills `corr` from every line and never compares indexes with the row's. Probe (scratch root, two corrections moved above their rows): `RESOLVED_BY_CORRECTION=4 DANGLING=0 C3=PASS` exit 0. The frozen predicate (`claims.md:117-118`) also says "a later … line": counter-vs-predicate drift.

**D2 (medium) — 82's limit "`bodyclash.tsv` … reached by no leg … only by hand" is false at the tip.** `c1-supplement.py:154-159` is a CLASH leg asserting exactly that file plus `WARN` on stderr; the real tool passes `CLASH=PASS 3/3` (6/6 run above). True only of the frozen `c1-count.py`, which the sentence does not say. Consequence is real: deleting the bodyclash write from a tool copy leaves the frozen counter `LEGS=5/5 C1=PASS` while the supplement prints `CLASH=FAIL 0/3` (`5/6`).

**D1 (medium) — 82 cites the wrong line for bodyclash.** `tools/assimilate-rows.py:441-447` is append-row pipe stripping and `used-by`; `bodyclash.tsv` is derived and written at `:466-475` (`clash = [(e, i) for e, i in body if i in lane_ids]`; `(out/"bodyclash.tsv").write_text`), warning at `:475`. The cited line does not say what is claimed.

**D9 (medium) — 85 points at erratum sections that do not exist.** `claims-erratum.md` is 29 lines with one heading, `## E1`; grep for E2/E3/E4 there → 0. E2-E4 are `corpus/lessons/round-51.md:182-184` (`## Disclosed post-freeze changes`), and `round-51.md:8` wrongly says "errata E1–E4: `corpus/evidence/round51/claims-erratum.md`". The disclosure exists; both pointers are wrong.

**D8 (medium) — 84's Mistakes row 1 asserts a receipt that does not exist.** `round-51.md:27`: "`corpus/evidence/round51/measure-after.txt` opens with a `tool-rev:` header and `receipt-check.py` prints `RECEIPT_OK`". `git cat-file -e HEAD:corpus/evidence/round51/measure-after.txt` → `fatal: path … does not exist`; `git log --all -- …` → empty. The receipt that does exist, `corpus/evidence/round51/measure-r50-at-tip.txt`, opens `measured-at: 1d7aba09…` and prints `RECEIPT_NO_REV … RECEIPT_CHECK=FAIL` rc 1: the round's own receipt fails 84.

**D7 (medium) — 84 passes vacuously with no receipt named.** `receipt-check.py` (no args) → `CHECKS=0 OK=0 FAILS=0 RECEIPT_CHECK=PASS` rc 0 (`receipts` is `nargs="*"`), and no lane script enumerates receipts (`grep -rn 'receipt-check.py'` → only SKILL.md:133 and the tool). A new round-52 receipt without a header lands unseen.

**D5 (low) — 83's headline covers SHONEN pointers, but only SCORECARD corrections are read.** `c3-count.py:107` (`tgt = corr.get(...) if fname == "SCORECARD.md" else None`). Probe: base SHONEN.md plus `correction: SHONEN.md:10 round25-meta-differential.log -> corpus/evidence/round25-meta-differential.log` → `DANGLING SHONEN.md:10 …` `C3=FAIL` rc 1. A dangling SHONEN pointer has no correction form.

**D3 (low) — 82's quoted failing line is not reproducible.** It prints `map=['S528','S784','S878']`, nonce draws. Two committed receipts of the same control differ: `c1-before.txt` flag-noop `['S512','S615','S781']` vs `c1-supplement-controls.txt` `['S683','S853','S879']`; my runs give `['S524','S702','S833']`. Stable parts reproduce; the ids should be elided.

**D10 (low, not a criterion defect)** — 85's headline promises "work directories carry random names", but the supplement only prefixes a 40-bit `mktemp` token; only the forge control (a separate artefact) tests it.

## Which of the six would not catch a regression of its own class

- **81 — no.** A copy with the nonce replaced by a constant (`random.Random(... else 20260101)`) at `fakelane/…/fixed-seed.py` still prints `LEGS=5/5` `C1=PASS` rc 0; nothing checks freshness.
- **82 — no** for the class its own limit names: removing the `bodyclash.tsv` write leaves `c1-count.py` at `LEGS=5/5`; only the supplement (cited in 85, not in 82's Check) goes red.
- **83 — yes** for a new dangling pointer (BLANKET/DELETED/EMPTY and a prepended line all go red), but blind to a correction naming an existing-but-wrong target (stated) and to SHONEN (D5).
- **84 — no.** The receipt list is caller-supplied and empty passes (D7); the skill leg can never pass (D6), so it measures nothing about the row.
- **85 — no.** With work dirs made deterministic (`s1, s2, s3 …`) the Check still prints `SUPPLEMENT_LEGS=6/6` `C1_SUPPLEMENT=PASS` rc 0; only `--tool controls/forge-dirname.py` separates the two (1/6).
- **86 — yes** for the one class it seeds (red under `d603f6f0`, green at the tip); other token shapes are an accurate, stated limit.

## Residual risk / not verified

- 84's class is unexercised on any landed round-51 receipt (D8); only scratch headers pass.
- The C3 correction branch was probed on scratch copies only; ordering (D4) cannot be measured by the frozen predicate as implemented.
- Not attacked here: C1/C2 depth claims, adopter behaviour beyond these counters, wave-1 internal claims.
- Tooling: nothing installed or upgraded; no pacman transaction attempted (host guard respected).

VERDICT: attacked QUALITY 81-86 by running every stated check and red state at the tip and probing each correction/limit edge — 82, 83, 84 and 85 carry real defects (wrong bodyclash line and a stale "no leg" limit; unenforced "later" corrections and no SHONEN form; a structurally unpassable `--skill` leg whose blamed row is actually compliant, an empty-list pass, and a cited receipt that does not exist; E2-E4 cited to a file holding only E1), 81 and 86 hold as written, and 81, 82 (bodyclash), 84 and 85 cannot detect a regression of the class they name.
