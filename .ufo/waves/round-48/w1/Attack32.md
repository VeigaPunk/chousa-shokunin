# Attack32 — lane registry census / SOURCES contract review (own-work row, lesson quote)

seat: L1Chousa48.Attack32 (reviewer) · wave: chousa-r48-w1 · date: 2026-10-25
item: review the lane registry census / SOURCES contract for a valid own-work source row and lesson quote requirement.
axes: operability / calibration / depth. Read-only; no installs; no scratch dirs needed; no network.

## Commands run (observed output)

- `bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 1:
  ```
  chousa  W04  S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
  chousa  W04  S053 duplicate url docs.python.org/3/library/socket.html across scopes
  chousa  W04  S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
  chousa  W04  S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
  chousa  W04  S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
  chousa  E11  S095 missing used-by corpus/lessons/round-48.md
  ```
- `git diff corpus/SOURCES.md` → exactly one added row: `+ S095 | Round 47 verifier spot-check — corpus/lessons/round-47-verifier-spotcheck.md | own-work | A | … | section 6, "Routed defects", line 62; round-47 capture, read this round | … | mined | 2026-10-25 | on-release | corpus/lessons/round-48.md |`. No other row/cell changes (uncommitted worktree edit).
- `grep -n 'Routed defects\|C1 precision side' corpus/lessons/round-47-verifier-spotcheck.md` → line 60 `## 6. Routed defects (lane must address next round)`; line 62 `1. **C1 precision side:** document the refusal class … (round-48 planned row already names it — keep).`
- Read: `corpus/evidence/round47/claims.md`, `corpus/lessons/round-47-verifier-spotcheck.md` (lines 58–66 raw), `scripts/sources-census.sh` (row_pass 610–695, usedby_findings 538–571, header contract lines 2–5), `corpus/QUALITY.md` (criteria 6, 14, 25, 30, 67), `corpus/knowledge/registry-link-r26.md`.

## Findings

### F1 — census regression: S095 trips E11 (operability, measured)
The SOURCES validate that was clean at round-47 (`ok`, exit 0, 94 rows, same five W04 — round-47 verifier spotcheck §1/§7) now exits 1 on `E11 S095 missing used-by corpus/lessons/round-48.md`. The E11 leg (`usedby_findings`, sources-census.sh:566–568) fires for every mined row whose `used-by` path is absent on disk; `corpus/lessons/round-48.md` does not exist (lessons dir ends at round-47). The only registry change this wave is S095, so S095 alone regresses the lane census.

### F2 — S095's own content is valid (calibration, checked)
- Anchor `section 6, "Routed defects", line 62` is exact: line 62 is the first item of `## 6. Routed defects` (line 60) and carries the C1-precision-side routed defect, including the `(round-48 planned row already names it — keep)` phrase that S095's source cell documents.
- teaches cell ("The spot-check measured correct held-out bullets refused and routed the missing false-refusal class for documentation") faithfully reflects line 62's content. No misquote, no invented anchor.
- Row shape passes every structural leg: NF=13, id, kind=own-work (enum), tier A, status mined, opened 2026-10-25 ≤ today, recheck=on-release (symbolic), no duplicate id/URL. Only E11 fires.

### F3 — own-work lesson-quote requirement is not machine-enforced (depth, gap)
The census validates only row shape and `used-by` existence. It does not check that an own-work row's anchor/teaches quotes the referenced lesson (no equivalent of QUALITY 25's web-quote reopen or criterion 30's Gate-verbatim leg for own-work rows). S095 passes the quote requirement only by manual inspection (F2); nothing guards future rows. This matches the round-47 spotcheck's own note that row truth (verdict map vs script) stays a reader's check — the same asymmetry holds for own-work quotes.

### F4 — forward used-by is a contract silence (calibration, open)
Precedent: every prior own-work row (S034–S045) names a lesson that existed at row time (round-27/28 lessons). S095 is the first `used-by` pointing at a not-yet-written lesson. QUALITY 6 binds a mined row's `used-by` to an existing entry that opens with the S-id — a dangling forward pointer satisfies neither the census E11 nor that binding as written. The spotcheck line 62 itself calls S095 "the round-48 planned row", so the forward reference is intentional planning, not a typo; but the contract neither permits nor documents it, and today it makes the registry fail.

## Verdict (recommendation only)

- Operability: harmed/regressed — the lane's SOURCES validate is no longer exit 0; the only error is S095's dangling used-by.
- Calibration: S095's anchor/teaches are accurate; the row is not fabricated, but its status (mined) and used-by overstate a support relation that does not exist yet.
- Depth: contract gap confirmed — no own-work quote check in the census; the lesson-quote requirement is enforced by hand only.

## Required disposition (not applied — read-only seat)

1. Until `corpus/lessons/round-48.md` exists, S095 should not be `mined` with that used-by: either keep it `queued` (flip to mined when the round-48 lesson lands and names it) or, if forward references are an intended contract feature, the contract/census must say so (e.g., a distinct pending marker that E11 exempts) — otherwise every round-48 recon run fails validate.
2. Close the F3 gap either by a census leg for own-work rows (anchor line exists; section heading exists; teaches substring present at the line) or by explicitly documenting the quote check as a reader check, per QUALITY conventions.

## Residual risk / verification gaps

- Fleet-wide census not run; E11 is lane-local (boundary).
- If a peer creates `corpus/lessons/round-48.md` later this round with that exact name, E11 resolves and F1 self-heals (F4's contract question remains).
- No installs; no scratch; no live fetch; no production/lane files modified (report only).
