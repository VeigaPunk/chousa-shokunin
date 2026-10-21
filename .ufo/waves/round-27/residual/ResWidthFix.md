# Round-27 residual seat `ResWidthFix` — change (a): GFM escaped-pipe header width

**VERDICT: FALSIFIED (landed cb895a2).** Change (a)'s width expression itself **HOLDS** (0/2256
brute-forced header rows disagree with cmark-gfm), but the landed revision still emits a **false
CLEAN** and **false findings** on GFM-valid registries — 5 fixtures where cb895a2 differs from
*both* the GFM oracle and dd72641e. The L1 candidate shared split in the lane working copy (sha256
`438c0fcb0c4f97231090554203b9e625360c60a647b8f83163168009a330e806`) is **verified clean** on the
same oracle: 0/51 fixture divergences, 0/2256 split mismatches, 30/30 falsify controls, PASS 215.

## 1. Method (read-only; only lane write is this file)

* Revisions (lane `git archive` → `/tmp/chousa-r27-residual-ResWidthFix/`): base `64eec5d` gate
  `c2c813f1…abc6` · `dd72641e` `ca39d14d…2f84` · `cb895a2` `a6bc2855…2386` · candidate = cb895a2
  tree + lane working-copy gate `438c0fcb…e806`.
* **GFM oracle** = cmark-gfm 2025.10.22 (table ext.), cross-checked with markdown-it-py (table rule);
  the two agree on **cell counts** for every fixture, differing only in inline backslash *rendering*.
  Where they differ in text I compare cmark's rendered text to the candidate's raw text after
  CommonMark's inline backslash-escape rule.
* Corpora (synthetic, `/tmp` only): 51 registry fixtures (escaped pipes in header/body, `\\`/`\\\`/
  `\\\\` runs, escaped pipe adjacent to outer pipes, mixed outer pipes, aligned delimiters, CRLF,
  widths 3–6, code spans, two tables, no-final-newline, 1-dash delimiter, the parent's four new
  controls) + 2256 exhaustive header rows (all strings over `{a, |, \}`, len 1–7, ≥2 pipes).
* Commands (all under the /tmp sandbox): `uv run --with cmarkgfm --with markdown-it-py python
  harness.py` (51 fixtures × 4 gates), `… width_brute.py`, `… cand_split_check.py`, `bash
  landed_width.sh corpus_rows.txt`, `bash cand_split.sh corpus_rows.txt`, `python3 usedby_escape.py`,
  `python3 /tmp/ctl30.py --gate tools/research-gate.sh`, `bash tools/research-gate.sh --selftest`.

## 2. Findings (severity order)

**F1 — LANDED cb895a2, false CLEAN on a GFM-valid registry (new harm vs oracle *and* dd72641e).**
Registry `| id | note \| x | status | used-by |` / `|---|---|---|---|` / body `| S001 | n | queued |
mined | corpus/knowledge/entry.md |`. GFM: header cells = id, “note | x”, status, used-by → the
row's status cell is `queued` → must report `META_SOURCE_NOT_MINED` (exit 1); cb895a2 returns
**exit 0 / `RESEARCH_GATE: CLEAN`** because the status column is read from the *naive* `|` split
(index 3 = `mined`), while dd72641e returned exit 2. `bash tools/research-gate.sh verify-metadata
<entry> --root <W> --registry <reg>` → cb895a2 `rc=0` vs oracle `rc=1 FINDING META_SOURCE_NOT_MINED`.

**F2 — LANDED cb895a2, false findings on GFM-valid registries (new harm vs oracle and dd72641e).**
Same family, four more fixtures: `I1-w5-esc-mid`, `I2-w6-esc-mid`, `Q2-escaped-before-status-mined`
→ cb895a2 `rc=1 FINDING META_SOURCE_NOT_MINED` where the oracle says CLEAN; `E1-esc-at-row-start` →
cb895a2 `rc=1 FINDING META_SOURCE_ROW_MISSING` where the oracle says usage exit 2 (that GFM header has
no plain `id` cell). Mechanism inherited (the naive cell split is base code): base 64eec5d emits the
same wrong findings, dd72641e masked them → **base-identical root cause, newly reachable** because
change (a) makes the table load.

**F3 — LANDED cb895a2, false `META_SOURCE_USEDBY_MISSING` when the used-by cell escapes a pipe
(inherited, base-identical).** Entry path `corpus/knowledge/a|b.md`, registry used-by cell
`corpus/knowledge/a\|b.md`: GFM cell text = the entry path → CLEAN; base/dd72641e/cb895a2 return
`rc=1 FINDING META_SOURCE_USEDBY_MISSING`, the candidate `rc=0` (`python3 usedby_escape.py`).

**F4 — CONTROL/COVERAGE WEAKNESS: the persisted control suite did not cover the misalignment
family.** With the 30-control file (working copy, sha `768a140e…2b65`): dd72641e → 7 mismatches;
**cb895a2 → 2 mismatches**, both new C3 controls (`escaped-before-status-queued` expected exit 1,
got 0; `escaped-before-status-mined` expected 0, got 1) — the landed revision's two failures are
exactly F1/F2; the original 26-control file reported “0 mismatches on cb895a2”.

**F5 — INHERITED (base-identical) GFM divergence surviving everywhere, incl. the candidate: the
delimiter regex `^:?-{3,}:?$` demands ≥3 dashes; GFM allows one.** Fixture `R1` (`|-|-|-|`): oracle =
valid table → CLEAN; all four revisions exit 2 (`metadata registry has no table`). Not caused by
change (a), not silently widened — the last non-GFM asymmetry in this code path.

**Non-findings (verified, no action):** change (a)'s width expression is **GFM-exact** — the
verbatim bash expression over all 2256 corpus rows gives **0** cell-count mismatches vs cmark-gfm,
while dd72641e's naive width is wrong on **1194/2254** rows; the landed revision repairs dd72641e's
rejection of 15 valid tables (B1,B2,B3,C4,D2,E4,F3,G3,H2,I3,J4,P2,P3,P8,P9) and its acceptance of
3 invalid ones (J3,P1,P4); base 64eec5d has **no** width check at all, so its base-only defects
(E5,J2,P1,P4,P5,P10) are already repaired at dd72641e and must not regress.

## 3. Input → oracle / base / dd72641e / cb895a2 / candidate
Legend `oracle/base/dd72641e/cb895a2/cand`; `CLEAN`=exit0, `USAGE`=exit2, `F:rowmiss`/`F:notmined`/`F:usedby` = the three `META_SOURCE_*` findings (exit1); `★` = cb895a2 differs from oracle *and* dd72641e (new harm); `!` = candidate ≠ oracle.

```
A1-w3-plain / A2-w4-plain / A3-w5-plain / A4-w6-plain: CLEAN/CLEAN/CLEAN/CLEAN/CLEAN (all four)
B1-esc-in-header-tail      CLEAN/CLEAN/USAGE/CLEAN/CLEAN   B2-esc-in-header-and-body  CLEAN/CLEAN/USAGE/CLEAN/CLEAN   B3-two-escapes-header      CLEAN/CLEAN/USAGE/CLEAN/CLEAN   B4-esc-header-w3           USAGE/USAGE/USAGE/USAGE/USAGE
B5-esc-in-status-header    USAGE/USAGE/USAGE/USAGE/USAGE   C1-esc-before-id           F:rowmiss/F:rowmiss/USAGE/F:rowmiss/F:rowmiss   C2-esc-between-id-status   F:notmined/F:notmined/USAGE/F:notmined/F:notmined   C3-esc-between-status-usedby F:usedby/F:usedby/USAGE/F:usedby/F:usedby
C4-esc-after-usedby-w5     CLEAN/CLEAN/USAGE/CLEAN/CLEAN   D1-double-bslash-header    CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   D2-triple-bslash-header    CLEAN/CLEAN/USAGE/CLEAN/CLEAN   D3-quad-bslash-header      CLEAN/CLEAN/CLEAN/CLEAN/CLEAN
D4-double-bslash-before-id F:rowmiss/F:rowmiss/F:rowmiss/F:rowmiss/F:rowmiss   D5-double-bslash-in-body   CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   E1-esc-at-row-start        USAGE/F:rowmiss/USAGE/F:rowmiss/USAGE ★   E2-esc-at-row-end          CLEAN/CLEAN/CLEAN/CLEAN/CLEAN
E3-esc-outer-adjacent-body CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   E4-esc-only-cell           CLEAN/CLEAN/USAGE/CLEAN/CLEAN   E5-esc-pipe-pipe           USAGE/CLEAN/USAGE/USAGE/USAGE   F1-header-no-outer         CLEAN/CLEAN/CLEAN/CLEAN/CLEAN
F2-body-no-outer           CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   F3-header-esc-body-plain   CLEAN/CLEAN/USAGE/CLEAN/CLEAN   F4-trailing-space-only     CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   G1-align-left              CLEAN/CLEAN/CLEAN/CLEAN/CLEAN
G2-align-right             CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   G3-align-with-escape       CLEAN/CLEAN/USAGE/CLEAN/CLEAN   G4-align-escape-only-key-cols CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   H1-crlf-plain              CLEAN/CLEAN/CLEAN/CLEAN/CLEAN
H2-crlf-escaped-header     CLEAN/CLEAN/USAGE/CLEAN/CLEAN   H3-crlf-double-bslash      CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   H4-crlf-body               CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   I1-w5-esc-mid              CLEAN/F:notmined/USAGE/F:notmined/CLEAN ★
I2-w6-esc-mid              CLEAN/F:notmined/USAGE/F:notmined/CLEAN ★   I3-w6-plain-esc-tail       CLEAN/CLEAN/USAGE/CLEAN/CLEAN   J1-escape-in-delimiter     USAGE/USAGE/USAGE/USAGE/USAGE   J2-delimiter-too-narrow    USAGE/CLEAN/USAGE/USAGE/USAGE
J3-delimiter-too-wide      USAGE/CLEAN/CLEAN/USAGE/USAGE   J4-no-final-newline        CLEAN/CLEAN/USAGE/CLEAN/CLEAN   J5-two-tables              CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   J6-escaped-pipe-only-row   CLEAN/CLEAN/CLEAN/CLEAN/CLEAN
P1-double-bslash-pipe-mid  USAGE/CLEAN/CLEAN/USAGE/USAGE   P2-double-bslash-pipe-wrong-delim CLEAN/CLEAN/USAGE/CLEAN/CLEAN   P3-triple-bslash-pipe-mid  CLEAN/CLEAN/USAGE/CLEAN/CLEAN   P4-quad-bslash-pipe-mid    USAGE/CLEAN/CLEAN/USAGE/USAGE
P5-double-bslash-before-id USAGE/F:rowmiss/F:rowmiss/USAGE/USAGE   P6-double-bslash-in-body-only CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   P7-double-bslash-in-delimiter USAGE/USAGE/USAGE/USAGE/USAGE   P8-escaped-pipe-in-code-span CLEAN/CLEAN/USAGE/CLEAN/CLEAN
P9-double-bslash-w6        CLEAN/CLEAN/USAGE/CLEAN/CLEAN   P10-double-bslash-between-key USAGE/F:notmined/F:notmined/USAGE/USAGE   Q1-escaped-before-status-queued F:notmined/CLEAN/USAGE/CLEAN/F:notmined ★   Q2-escaped-before-status-mined CLEAN/F:notmined/USAGE/F:notmined/CLEAN ★
Q3-escaped-body-cell-before-status CLEAN/CLEAN/USAGE/CLEAN/CLEAN   Q4-escaped-final-header-cell-no-outer-pipe CLEAN/CLEAN/CLEAN/CLEAN/CLEAN   R1-single-dash-delimiter   CLEAN/USAGE/USAGE/USAGE/USAGE !
```
## 4. Candidate assessment (lane working copy, sha `438c0fcb…e806`) — no objection to the approach

The candidate uses one shared split for header, delimiter and body rows: strip the outer pipe only
when the row does not end with `\|`; double every backslash; reduce `\\|`→`\|`; then `IFS='|' read
-a` **without** `-r`, so `read` honours the escaped pipe while literal backslashes survive. Verified
in my sandbox:

* **Cell count** vs cmark-gfm over all 2256 corpus rows → **0** mismatches (naive split: 1194);
  **Cell text** → **0** mismatches after CommonMark inline backslash-equivalence (the candidate
  yields cmark's *raw* cell text).
* **Behaviour**: 51 fixtures → matches the oracle on 50/51 (exception = inherited F5 `R1`); fixes
  F1/F2/F3; `python3 /tmp/ctl30.py --gate tools/research-gate.sh` → **30 controls, 0 mismatches**
  (C1 0/5, C2 0/8, C3 0/17) vs cb895a2's 2/30; `bash tools/research-gate.sh --selftest` →
  `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)`, exit 0.
* **Why it is right (rules stated explicitly)**: in a GFM table row a `|` is a cell boundary iff the
  character immediately before it is not a backslash (no parity rule); the backslash preceding such
  an escaped pipe is dropped from the cell text, every other backslash is literal. cmark-gfm and
  markdown-it-py agree on all 2256 counts; the candidate reproduces exactly this. My earlier
  "backslash parity" hypothesis was wrong and is withdrawn.

Objections / residual risks (minor, none blocking):
1. **Raw vs rendered text** — the candidate's cell text is cmark's *raw* cell text; for a cell with
   ≥2 backslashes before a pipe it keeps one backslash GFM would render away (only observable if a
   used-by path is written that way — not in the corpus; single-backslash escapes are exact).
2. **`read` without `-r`** processes backslash escapes over the whole line; the doubling makes this
   idempotent for every backslash run (proved over the 2256-row corpus, including rows ending in
   backslashes → no trailing-backslash line continuation). Keep the sentinel append.
3. **F5 remains** (≥3 dashes required). Out of scope here; if C3 is to claim “GFM registry
   semantics”, the delimiter regex needs `^:?-+:?$` — a separate, deliberate decision.
4. **Landing hygiene + coverage gap**: the candidate exists only in the lane working copy; the
   committed revision must re-run `--selftest` and the 30 controls (its gate sha will differ from
   `438c0fcb…`). Persist controls for escaped-pipe-before-`id` (E1/C1), the used-by escaped-pipe
   case (F3) and the 1-dash delimiter (F5) — the current 30 controls pin only two family members.
5. **Scope of the claim**: state “GFM-consistent cell splitting and header/delimiter width for the
   registry table”, **not** “full GFM”: F5 (≥3 dashes) stays a documented limitation. If the final
   code keeps the **landed** (naive-index) split and only adds status-checked token stages, F1/F2
   stay open — a status value read at a shifted index cannot close them; the status cell must be
   read at the **GFM cell index** (the verified candidate split).

## 5. Residual risk & verification gaps

* The 51-fixture corpus, the 2256-row corpus and the four harness scripts live in
  `/tmp/chousa-r27-residual-ResWidthFix/` (durable copy in §6) — nothing was added to the lane, so
  F1/F2/F3 are reproducible only from this report unless the L1 persists the bundle.
* F5 is unfixed everywhere (base-identical): the gate is stricter than GFM for delimiter rows. My
  oracle models the gate's source check (S001 present, `mined`, used-by names the entry); a GFM table
  without a plain `id` column is scored USAGE in every revision (exit 2 in both — no revision is
  credited or penalised on wording).
* Not covered here (other seats): CRLF strip (c), S-id token prefilter (b), usage matcher (d), C2
  date/cadence behaviour; my H-group fixtures only confirm change (a) does not clash with (c).
## 6. Tooling record

* `markdown-it-py` **4.2.0** (dep `mdurl` 0.1.2) and `cmarkgfm` **2025.10.22** (deps `cffi` 2.1.1,
  `pycparser` 3.11) — installed ephemerally via `uv run --with …` (PyPI, official uv channel); no
  pacman transaction (host-wide pacman paused this wave); pinned in the bundle's `requirements.txt`.
  No other tool installed; no network fetch besides those two packages; no host files touched; no
  lane writes except this report; fixtures in /tmp.
* Durable, bounded copy of the harness + corpus (122 KiB, sha256 manifest): `/home/vgpnk/.cache/
  chousa-r27-reswidthfix/` — `harness.py` (51 fixtures + oracle + 4 gates), `width_brute.py`,
  `cand_split_check.py`, `usedby_escape.py`, `corpus_rows.txt` (2256 rows), `landed_width.sh`,
  `cand_split.sh`, `results.json`, `requirements.txt`, `MANIFEST.sha256`. Outside the lane on
  purpose — persisting it under `corpus/evidence/` is the L1's call; no lane edit beyond this report.
