# R89ExecC2Forge — C2 calibration forgeries, round 89

Seat: R89ExecC2Forge (leaf; no subagents dispatched beyond assigned scope).
L1: ChousaR89. Freeze: `ac0a0892c15de11fb28d3208f2b287687c00477e`. Tree: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive ac0a0892c15de11fb28d3208f2b287687c00477e | tar -x -C $S/tree` under `/fast/scratch/hyaku/chousa-r89/R89ExecC2Forge/`. No network. No host mutation. Tooling: `python3 --version` = Python 3.14.8 (`/usr/bin/python3`), system already present; nothing installed or upgraded (official-channel rule read in `/home/vgpnk/.omp/agent/RULES.md`; no installs needed, pacman untouched per orchestrator pause).

## Method

Mirror exactly as `curation-r89-controls.py` does (`mirror()`: registry + two entries as copies, `corpus/captures` and `corpus/evidence/round57` symlinked), one targeted forgery per tree, then `python3 -B $S/tree/corpus/evidence/round89/curation-r89.py --root <mirror>`. Unmodified mirror passes (`receipts/positive-mirror.txt`, rc=0). Every command below is cited with its receipt path, observed summary line and exit code. Scratch work dir deleted on completion (`finally: shutil.rmtree` in the driver via `TemporaryDirectory`).

## (a) Duplicate guard

- `Q1, Q1, Q3` (same qid twice plus a second distinct qid in one warrant cell) — REFUSED. `receipts/a1-dup-Q1-Q1-Q3.txt`, exit 1: `DUP_QIDS=1`, `LEG_FAIL DUPQID ... warrant=Q1, Q1, Q3 (S215)`. The guard counts any repeat within one cell; the extra distinct qid does not launder it.
- Trailing comma `Q1, Q1, (S215)` — REFUSED. `receipts/a2-dup-trailing-comma.txt`, exit 1: `DUP_QIDS=1`, `LEG_FAIL DUPQID ... warrant=Q1, Q1, (S215)`. The regex `Q\d+` finds both citations; the empty segment between commas is invisible to it and does not hide the repeat.
- Extra whitespace `Q1,   Q1 (S215)` — REFUSED. `receipts/a3-dup-extra-spaces.txt`, exit 1: `DUP_QIDS=1`.
- Same qid cited on two different decision rows (r85 row 2 re-pointed `Q2 → Q1`) — ACCEPTED, and this is the interesting frontier cell. `receipts/a4-dup-cross-row-r85.txt`, exit 0: `DUP_QIDS=0 WARRANT_OK=17/17 CURATION_R89=PASS`. The DUPQID leg is per-cell only; nothing tracks citation reuse across rows. Row 2's warrant still resolves and shares the distinctive term `entities` with Q1's quote (both derive from the same PROV-O paragraph), so the WARRANT leg's term-sharing check passes on that one common word. No leg compares which qids a row *should* cite. This is a genuine gap in the duplicate class, but it is not the battery's D1 shape (`Q1, Q1` in one cell, which is refused): the C2 sentence claims only the single-cell duplicate. Cross-row duplication launders through shared vocabulary, not through the counter's own split — and breaking it would require a per-row citation oracle (which qid belongs to which row), i.e. a second copy of the entry (the claim's named-limit-2 shape: "a content oracle would need a second copy of the entry, which is the entry itself"). I report it as a frontier extension, not a firing, because it does not contradict any sentence wording actually frozen.

## (b) Field-derived verdict

No divergence exists to find. `fields_hold` (curation-r89.py:305–315) is logically equivalent to the conjunction of the leg conditions (each printed field appears in both): `superseded_live`, `unentailed`, `modified_def_cited >= 1`, `located_all == total_all`, per-entry `loc >= fl and loc == tot and set(qs) == pin and not short`, `warrant_ok == warrant_total`, `len(dup_qids) == 0`, `teaches_checked > 0 and len(teaches_flagged) >= 1`, `len(teaches_unresolved) == 0`, `len(teaches_sup_unresolved) == 0`. Both directions were exercised:

- Legs refuse, fields agree: `receipts/b1-verdict-fields-false-legs-refuse.txt` (S031 `mined → queued`), exit 1: `TEACHES_UNRESOLVED=1`, `LEG_FAIL VERDICT fields_hold=0 legs_ok=7/8`. The verdict refuses with the fields.
- Legs pass, fields fail — impossible without editing the counter: removing the only flagged row's contrast phrase (`receipts/b2-verdict-reverse-legs-pass-fields-fail.txt`, exit 1) kills the TEACHES detector (`TEACHES_CHECKED=0`), so the TEACHES leg *and* `fields_hold` both fail; `LEG_FAIL VERDICT fields_hold=0` either way. There is no printed field the verdict does not read. A field that disagreed could only be produced by joint-writing the leg writer, the receipt fields and the verdict — the counter itself (the C1 named-limit-1 analogue, not a C2 bypass).

## (c) Superseder clause

- Date term without a contrast phrase (S031's `teaches` rewritten to name `publication dates` with no contrast) — ACCEPTED, `receipts/c1-sup-date-in-capture-no-contrast.txt`, exit 0: `SUP_CLAUSE_CHECKED=0 SUP_UNRESOLVED=0`. The sup clause requires contrast **and** a date term; with only one, the row is never checked (`SUP_CLAUSE_CHECKED=0`). The C2 sentence claims refusal of "a superseder carrying a contrast phrase **and** a date term absent from its own capture" — the conjunctive shape — so this single-marker variant is outside the frozen sentence it attacks. It does document the trigger's conjunctive edge: a superseder cell that misstates a date term without contrast prose passes silently. Reported, not fired: the sentence does not promise this case, and the battery's mirror (both markers) is refused (`sup_unresolved=1 unresolved=0`).
- Contrast phrase without a date term — ACCEPTED, `receipts/c2-sup-contrast-no-date-term.txt`, exit 0, same `SUP_CLAUSE_CHECKED=0`. Same conjunction, other side.
- Two superseders, one mined and one queued, the queued one carrying the bad cell (S030 re-pointed to `supersedes S024`, `distinct from publication dates`; S030's capture is a cookie stub with neither term) — REFUSED. `receipts/c3-two-sup-one-queued-bad-cell.txt`, exit 1: `TEACHES_CHECKED=2 TEACHES_FLAGGED=2 TEACHES_UNRESOLVED=1 SUP_CLAUSE_CHECKED=1 SUP_UNRESOLVED=1`, `TEACHES_FLAGGED S030 terms=publication ... UNRESOLVED`. The sup clause fires on the queued superseder exactly as designed; the queued status does not shield the bad cell.

## (d) Token floor's boundary

- Shortest verbatim quote that passes: 7 tokens, exact capture span `web page was last reviewed for accuracy` — ACCEPTED, `receipts/d1b-7token-exact.txt`, exit 0. This is the disclosed named limit 1 in the frozen claim ("`MIN_TOKENS = 7` is a measured floor, not a content check: a ≥7-token verbatim substitution that shares a distinctive term still passes"). It fires *as disclosed*, not against the claim.
- 6-token sub-floor verbatim span (`page was last reviewed for accuracy`) — REFUSED, `receipts/d1c-6token-subfloor.txt`, exit 1: `LEG_FAIL FLOOR`. The floor binds below 7; the boundary is exactly 7.
- 7-token verbatim span with no shared distinctive word (`Date on which the content on this`) — REFUSED via WARRANT not FLOOR, `receipts/d1d-7token-noshare.txt`, exit 1: `WARRANT_OK=16/17`. The floor is not the only gate on a substitution.
- Quote assembled from two non-adjacent fragments (`Date on which the content last reviewed for accuracy.`) — REFUSED, `receipts/d2-quote-two-fragments.txt`, exit 1: `QUOTES_LOCATED=19/20`, `LEG_FAIL FLOOR`. The substring check requires contiguity in the capture; splicing is not verbatim.
- Curly-quote variant (`“…”` around the quote cell) — REFUSED, `receipts/d3-curlup-quote.txt`, exit 1: `QUOTES_LOCATED=19/20`. The counter strips straight cell quotes (`.strip('"')`) *before* `norm()` folds curly marks, so the outer curly quotes survive the strip, fold to straight quotes, and remain part of the searched string — the capture carries the bare sentence, so the quoted form does not match. Inner curly apostrophes fold fine; only the cell-delimiting curly pair breaks the lookup. Cosmetic asymmetry in the strip order, not an acceptance bug: the variant is refused, and the claim's "curly quotes folded" (K2 wording) describes inner folding, which holds.

## (e) Qid-set pin

- Round-88 `caseG` restored shape (uncited Q10 deleted, duplicate of Q13 appended as Q14, inside the Located-quotes section) — REFUSED, `receipts/e1-caseG-restored.txt`, exit 1: `Q_FLOORS=search-transparency-reporting-r84.md=12/12 floor13`. The DUPQID leg does **not** see this shape (it watches warrant cells; `DUP_QIDS=0` printed) — the refusal comes from the FLOOR leg's pinned qid set and the now-12 located count. That is the design: caseG is a floor/pin forgery, not a warrant-cell duplicate. Correctly refused.
- Duplicate content row under a new label (Q99 copy of Q13, inside the Located-quotes section) — REFUSED. First attempt appended at EOF, outside the section, and was inert (the counter only parses `## Located quotes`); corrected probe `receipts/e2b-dup-row-in-section.txt`, exit 1: `Q_FLOORS=search-transparency-reporting-r84.md=14/14 floor13`, `LEG_FAIL FLOOR`. Located==total (14/14) and the floor is exceeded, so only the pinned set `Q1..Q13 ≠ {Q1..Q13, Q99}` refuses it. The pin guards label identity as claimed.
- Swapping two pinned quote texts under their qids (r85 Q1↔Q2, both S215) — ACCEPTED, exit 0. This is the claim's named limit 2 verbatim ("swapping the quote texts under two pinned qids passes"), exercised to confirm the disclosure is accurate. Not a kill.

## Register-keeping notes

- `receipts/e2-dup-content-row.txt` (EOF append) is retained as a record of the driver's first, inert placement — it proves the counter reads only the `## Located quotes` section. The corrected probe is `e2b`.
- `receipts/d1-quote-7token-boundary.txt` (first 7-token attempt) appended a fabricated trailing period to the verbatim span, so the "quote" was not verbatim and was refused on FLOOR/WARRANT — that refusal is honest (a non-verbatim quote is refused) but it did not probe the boundary the case name claims. The exact boundary probe is `d1b`; sub-floor `d1c`; no-shared-word `d1d`.
- Every leg refusal above names its leg (`LEG_FAIL` lines in the receipts) — no silent acceptance of any charged shape.

## Frontier conclusion

None of the five attacks produced a tree the counter accepts that C2's sentence says it should refuse. Attack (a) exposed one real extension (cross-row citation reuse passing on a shared common word) that the sentence does not claim to close and that needs a citation oracle to close; attacks (d) boundary and (e) quote-swap passed only in shapes the claim pre-discloses as named limits 1–2. The (b) verdict proves structurally equivalent to the leg conjunction in both directions. A genuine attempt that improved no axis and harmed none: it confirms the frontier's stated boundaries.

VERDICT: R89ExecC2Forge C2 held — all five attack families refuse on named legs; the two accepted shapes (cross-row qid reuse on a shared term; 7-token verbatim substitution) are the claim's named limits, and the verdict is field-equivalent in both directions.
