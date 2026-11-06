# R82ReviewerGate — code review of the C1 gate change

Scope: `git diff 57c0d16795db97ed09b69034e335e725ce577285 b4a41d251b488f06b4a6ab01a11bc12ce72edd20 -- tools/research-gate.sh SKILL.md` (170 insertions, 12 deletions). All commands run under `LC_ALL=C` default unless stated; every cited receipt is under `receipts/` in this folder (records under `receipts/records/`, byte-identical to the ones run). Trees: scratch `trees/pre` = 57c0d16, `trees/post` = b4a41d2, `trees/base` = 5d792e1 (K3 base). Line numbers refer to the post tree.

## Findings

### F1 — CRITICAL — C1 K2 firing: duplicate `##` headings silently drop the first block, so in-class K2(b) and K2(c) records pass at the landing revision

`load_sections` (tools/research-gate.sh:866-870) runs `SEC_ORDER+=("$sec"); SEC_BODY[$sec]=""` on **every** `##` heading. A second heading with the same name resets the body: the first block's rows disappear for every consumer — the structure check (`verify`), the rejection loop, the sweeps loop and the new negative-resolution map alike. Neither the patch's loops nor `emit_finding` ever see the dropped rows.

- K2(b) receipt — `r-dup-rejections.md` (first `## Rejections` keeps `R1` with an **empty flip**; second block is complete):
  `bash tools/research-gate.sh verify-sweeps r-dup-rejections.md --root .` at b4a41d2 →
  `VERIFIED_SWEEPS=0/0 REJECTIONS_OK=1/1` … `RESEARCH_GATE: CLEAN`, `EXIT=0` (receipts/r-dup-rejections.post.txt; base 5d792e1 identical). The item-4 Run line therefore exits 0 on a record that "keeps a rejection with an empty … flip under a `##` heading whose text contains `reject`" — exactly K2(b) → C1 falsified.
- K2(c) receipt — `r-dup-claims.md` (first `## Claims` carries negative `N1` with sweep cell `SW9`, an undeclared id; `## Sweeps` declares only `SW1`; second `## Claims` block is benign):
  full item-2 Run line at b4a41d2 → exit 0 (attack transcript; verify-sweeps receipt r-dup-claims.post.txt is CLEAN). K2(c) says any record carrying a negative claim whose sweep cell names no declared `## Sweeps` row id, on which the Run line exits 0, falsifies C1 → C1 falsified.
- Blast radius is the whole new surface: a `## Rejected sources` block followed by any later reject-named heading drops the first; a duplicated `## Sweeps` means the first block's sweeps are never re-run and never enter `SW_IDS`/`SW_CLAIMS`.

Pre-existing parser behavior, but the frozen K2 rules are defined over landing-revision behavior ("any record, authored by anyone"), so this is a firing, not a residual. Fix direction for the lane: concatenate same-name section bodies in `load_sections`, or refuse a record that repeats a heading (either closes both receipts).

### F2 — HIGH — C1 K3 firing: a `where` set mixing a placeholder token with a real path now refuses a sweep the base gate verified

`r-where-mixed.md`: one `## Sweeps` row with `where=n/a,lib/x.md` (whitespace-free comma set).

- Base 5d792e1e Run line: exit 0, `SWEEP id=SW1 where=n/a,lib/x.md looked=local hits=0 … verified match`, `VERIFIED_SWEEPS=1/1`, CLEAN (receipts/r-where-mixed.runline-base5d792e1e.txt).
- Landed b4a41d2: `FINDING SWEEP_LOCATION_ABSENT … id=SW1 unclassifiable location naming`, EXIT=1 (receipts/r-where-mixed.post.txt).

The cell is not "set to a declared-vocabulary value" (K2(a) requires the whole cell to be a vocabulary value), so it carries none of K2's forms → K3 harm. Root cause chain: the comma/semicolon branch of `sweep_where_tokens` (tools/research-gate.sh:2758-2768) keeps **all** tokens unfiltered; `sweep_token_class` now classifies `n/a` as junk (line 2724); and `verify_sweeps` invalidates the entire sweep when any token is junk (`have_junk` → SWEEP_LOCATION_ABSENT, lines ~2975-2982). The refusal is whitespace-sensitive: `where=n/a, lib/x.md` (space after the comma) takes the command branch, which drops junk tokens, and passes CLEAN. Asymmetry worth noting: the same mixture in a claim `sweep` cell is fine — any declared id in the list resolves (r-sweepcell-mixed, receipts).

### F3 — MEDIUM — C1 K3 firing (per the frozen letter): a negative claim whose sweep is carried by a `## Negatives` row is refused whenever a `## Sweeps` section also has rows

`r-mixed-negatives.md`: Claims `N1` (negative, sweep cell `N1`), `## Sweeps` with one unrelated verified row `SW1`, `## Negatives` with row `N1` carrying `where=lib/ghost*.md`.

- Base 5d792e1e Run line: exit 0 (receipts/r-mixed-negatives.runline-base5d792e1e.txt).
- Landed: `FINDING SWEEP_NEGATIVE_UNRESOLVED … claim=N1 sweep=N1 names no sweep row this mode re-ran`, EXIT=1 (receipts/r-mixed-negatives.post.txt).

K2(c) itself exempts this shape: "… (and no `## Negatives` sweep row carries it)". The Negatives row with id `N1` carries the claim, so the record is out of class and refusing it is K3 harm. Root cause: `SWEEP_ROWS` takes Negatives rows only when zero Sweeps rows exist (tools/research-gate.sh:2938-2945), so `SW_IDS`/`SW_CLAIMS` (lines 3057-3060) never see Negatives carriers when Sweeps is nonempty. The lane's own class records (r2-03, r2-14) exercise only the no-Sweeps shape, so this mixed shape is untested by the manifest. Honest caveat: if the lane reads "carries it" more narrowly than id-carriage, this record could be argued in-class; the observed behavior is exact either way and the two readings should be settled in the wave.

### F4 — MEDIUM — over-broad reject-heading match refuses differently-schemed tables (in-class per the frozen letter; flagging the blast radius)

`r-rejected-claims-schema.md` keeps a `## Rejected claims` table with columns `claim | status` (cells filled per that schema). Landed gate reads it as a rejections table: `FINDING SWEEP_REJECTION_INCOMPLETE … id=R1 missing=reason,flip section=Rejected claims`, `REJECTIONS_OK=0/1`, EXIT=1 (receipts/r-rejected-claims-schema.post.txt); base exits 0. Per K2(b)'s letter ("a rejection with an empty … reason or flip under a `##` heading whose text contains `reject`") this refusal is claimed behavior — the rows do have empty reason/flip cells under a reject-named heading. Reported because any co-located table (`## Unrejections`, an index, a prose summary that happens to be a table) under any heading containing "reject" now drifts; a column-schema guard (require an id+ref or reason/flip-like column before counting rows) or a narrower heading match would shrink this without losing the class. Related cosmetic: `## Rejections` and `## REJECTIONS` are distinct `SEC_BODY` keys, both matched by `*reject*`, so a record carrying the same rows under both spellings counts each row twice in `REJECTIONS_OK=K/L`.

### F5 — LOW — observations

- Exact-case id matching: claim sweep cell `sw1` vs declared row `SW1` → `SWEEP_NEGATIVE_UNRESOLVED`, EXIT=1 (receipts/r-case-ids2.post.txt); base passes. Consistent with the gate's exact-case `claim_id` matcher in `verify` (line ~1351), and in-class per K2(c)'s letter — noted because human-authored near-miss ids will refuse.
- Header/`SKILL.md` wording vs behavior: a claim naming an **exempt** sweep row (e.g. `status=blocked-no-fetch`) resolves without any re-run (r-neg-exempt: CLEAN at both trees, `VERIFIED_SWEEPS=0/1`). The header sentence "must resolve to a sweep row this mode re-ran" and the SKILL sentence "no sweep row the mode re-ran" are loose in the harmless direction (resolution is wider; refusals unaffected). No defect.
- `sweep_is_placeholder` declares an unused local `w` (tools/research-gate.sh:2697). Lint only.
- `see_above` normalizes to `seeabove` (underscore **deleted**, not space-replaced) and is therefore not a placeholder. This matches the frozen vocabulary definition ("removing backticks, quotes, `*`, `_`"), so it is spec-faithful — do not "fix" it into a spec violation.

## Clean checks (held)

- **Locale**: `sweep_is_placeholder` probed under `LC_ALL=C`, `C.UTF-8`, `en_US.UTF-8` on 16 inputs including `—`, `–`, `…`, `N/A`, `n/a.`, `  None  `, `not  applicable`, prose — identical verdicts in every locale (receipts/locale-matrix.txt). `${v,,}` lowercases byte-wise in C and the dash/ellipsis literals are byte-compared; no divergence.
- **verify-all no-harm**: 16/16 fixtures with sweeps/rejections produce a byte-identical sweeps `SECTION` line and rc at both trees (sweeps-r5{,-broken,-hit}, archives-r9 A/B/C + 5 controls, full-r6{,-absent,-broken}, integrity-r7{,-broken}) — receipts/verifyall-fixtures.txt (captured matrix output).
- **`--json`**: verify-all `--json` schema keys identical pre/post (`schema, ts, record, record_sha256, gate_sha256, sections, verdict, sections_run, sections_absent, drift_sections`); only volatile `ts` and `gate_sha256` differ. The summary-line greps (`^VERIFIED_SWEEPS=.*REJECTIONS_OK=`) are unaffected by `reason=placeholder` values.
- **Positive controls hold at landing**: `item2-pass`, `item4-pass`, `p4-flip-prose-with-na` all CLEAN rc=0 at b4a41d2; `r2-12-hit` refused at both trees (SWEEP_CLAIM_FALSE). No blanket-refusal drift.
- **Five new selftest cases are revert-sensitive**: st1-placeholder-cells, st2-rejected-heading, st3-where-placeholder, st4-negative-unresolved all print CLEAN/EXIT=0 at the pre gate (receipts/*.pre.txt) while asserting rc=1 + `SWEEP_REJECTION_INCOMPLETE`/`SWEEP_LOCATION_ABSENT`/`SWEEP_NEGATIVE_UNRESOLVED`/placeholder tokens — each would fail if the patch were reverted. st5-prose-pass is CLEAN at both (no false refusal). Proven per-case against the 57c0d16 gate; `--selftest` at landing: `RESEARCH_GATE_SELFTEST: PASS (280 cases, 0 skipped)`, rc=0 (run twice, identical; 280 = 275 + the 5 new cases, ≥275, 0 skipped → K4 constraint met at landing).
- **Run lines byte-identical**: all four `research-gate.sh` backtick command spans in SKILL.md hash identical pre/post; the item-2/item-4 lines change only in prose appended after the closing backtick, so the counter's `Run: \`([^\`]+)\`` extraction and FROZEN_RUNLINE comparison still see the frozen text.
- **New SKILL.md / header sentences accurate**: undeclared id → UNRESOLVED (r-neg-undeclared), header-only `## Sweeps` → UNRESOLVED (r-empty-sweeps-header), placeholder sweep cell → UNRESOLVED (r-sweepcell-ph), placeholder `where` → LOCATION_ABSENT (st3), reject-named heading read (st2), prose flip passes (st5), closed list works after case/backtick/period folding (locale matrix). "`n/a` as a local path" is true of the base gate (st3 pre verified `looked=local` 1/1).
- `local` inside loops (`robs`, `ntoks`) and `read -r -a` word splitting are safe under `set -euo pipefail`: `read` never globs and herestrings terminate with a newline, so rc is 0; the `ws[*]+…` guard covers the empty-array case under `set -u`.

## Kill-rule tally for this review

- K2 fired: F1 (two records, item-2 and item-4 Run lines exit 0 at b4a41d2 on in-class forms).
- K3 fired: F2 (mixed where set), F3 (Negatives carrier under a parallel Sweeps section) — both refused at b4a41d2 with the full Run line after passing at 5d792e1e.
- No K1/K4 evidence gathered against the predicate itself (counter/selftest receipts are the counter seats' to run; the landing selftest line above is the only K4-adjacent observation).

Residual risk: findings F1–F3 live in the parser/SWEEP_ROWS plumbing that this patch built on, not in the placeholder vocabulary itself — the closed list, its folding, and the locale behavior are clean. If the wave chooses to read K2(c)'s Negatives parenthetical narrowly, F3 downgrades to a class-boundary decision; F1 and F2 fire under any reading I can construct.
