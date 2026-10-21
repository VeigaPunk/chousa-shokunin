# FSimplifyDate — C2 date arithmetic simplification (read-only)

Seat: `ChousaR26R.FSimplifyDate` · Judged axis: **freshness** · Wave: round-26 falsify attempt 1

## Measured revision

| Field | Value |
|-------|-------|
| Immutable target | `0e9784bd52eca456b24d0bc40921480a47f91a2b` |
| Claim base | `ba3333254dd337658a4f25e7a9471f9cf4e4567e` |
| Sandbox | `/tmp/chousa-r26-falsify-FSimplifyDate` (detached worktree at target) |
| `tools/research-gate.sh` sha256 | `c2c813f1b425bc4e74625a2607eaca1b97addf9898f834e88af8f1fe2143abc6` (matches `round26-measured-revision.json`) |
| Production lane HEAD | same as immutable target at review time |

No production edits. Tool installs: none.

## Godspeed axes

| Axis | Question for this review |
|------|---------------------------|
| **Correctness** | Does a deletion keep spec-v1 due/freshness/overdue semantics (proleptic Gregorian, strict `as-of > due`, boundary `due == as-of` → current)? |
| **Freshness operability** | Does C2 stay testable with one oracle authority and bounded probes? |
| **Maintainability** | Can duplicate calendar/oracle paths merge without a second convention? |
| **Separability** | Do C2 deletions avoid touching C1 reader or C3 registry surfaces? |

## Bounded checks exercised (this seat only)

```text
bash corpus/evidence/round26-date-differential.sh /tmp/chousa-r26-falsify-FSimplifyDate/tools/research-gate.sh
→ DATE_DIFF_AGREE=9024/9024 exit=0 (wall ~53s)

bash corpus/evidence/round26-measure.sh /tmp/chousa-r26-falsify-FSimplifyDate c2
→ FRESHNESS_CLASSIFIED=29/29 C2_ORACLE_AGREE=29/29 C2_CONTROLS_CAUGHT=6/6 exit=0
```

Full selftest, C1 8 MiB probe, and integrated `all` were **not** run (out of seat scope).

## Reference proof method

No language server was available for `tools/research-gate.sh`. Call-site proof uses ripgrep over the immutable sandbox tree (recorded as text search, not semantic LSP).

---

## Preserved contract (must not change)

- Spec v1 in `corpus/evidence/round26-claims.md` Claim 2 plus decimal/range addendum (lines 143–149): pure Bash, no `eval` on user text, proleptic Gregorian `<N>d` add, range overflow → `due=unknown freshness=unknown`, overdue iff `--as-of` is strictly after dated `due`.
- Plain `verify-metadata` without `--as-of` remains byte-identical to base.
- Independent oracles: `round26-measure.sh` embedded Python (lines 97–150) and `round26-date-differential.sh` (lines 51–70) are adjudication authorities; gate must not be edited to match a shrunk oracle.

---

## Deletion candidates (behavior-preserving, anchored)

### D1 — Drop epoch-day freshness compare; use ISO string order (high value)

**Problem:** After computing canonical `due_date`, freshness still converts both `--as-of` and `due` to epoch days and compares integers — three civil conversions per dated entry on every `--as-of` run.

| Location | Role |
|----------|------|
| `tools/research-gate.sh:2548-2551` | `--as-of` → `metadata_days_from_civil` → `asof_days` (once per invocation) |
| `tools/research-gate.sh:2754-2756` | `metadata_days_from_iso "$due_date"` → `((asof_days > due_days))` |
| `tools/research-gate.sh:2338-2341` | `metadata_days_from_iso` helper (only caller is 2755) |

**Deletion:** Remove `metadata_days_from_iso` entirely; remove `asof_year` / `asof_month` / `asof_day` / `asof_days` / `due_days` locals and block 2548–2551.

**Replacement (one line, same branch):** at 2754–2756, when `freshness == current` and `due_date` is a spec-valid ISO date:

```bash
[[ $AS_OF_ARG > $due_date ]] && freshness=overdue
```

**Why safe:** Under `LC_ALL=C` (already set at 2539), lexicographic order on fixed-width `YYYY-MM-DD` strings matches chronological order for all calendar-valid dates the gate accepts. `metadata_iso_date` (2295–2307) and `metadata_add_days` output via `printf -v META_DATE_RESULT '%04d-%02d-%02d'` (2335) both yield zero-padded fields. Strict inequality matches spec “strictly after due”. Boundary control `c2-boundary` (`due=2026-10-21`, `as-of=2026-10-21`) stays `current`.

**Keep:** `metadata_days_from_civil` / `metadata_civil_from_days` / `metadata_add_days` — still required for `<N>d` cadence (2295–2359).

**Tradeoff:** Freshness compare no longer shares the same integer path as day-add; divergence would require accepting non-canonical ISO strings, which validation already rejects.

---

### D2 — Stop second `metadata_iso_date` on `recheck_first` (medium value)

**Problem:** Same token validated twice per entry when `--as-of` is set.

| Location | Role |
|----------|------|
| `tools/research-gate.sh:2720-2721` | Scheduled/unscheduled classification |
| `tools/research-gate.sh:2739-2740` | Due branch for ISO recheck |

**Deletion:** Remove the second call at 2739; record a flag when the first call succeeds (e.g. `recheck_iso_due=1` beside 2720–2721).

**Replacement:** In the `--as-of` block, branch on `recheck_iso_due` instead of re-invoking `metadata_iso_date "$recheck_first"`.

**Why safe:** Classification and due computation use the same predicate on the same token in one entry pass; no user input changes between calls.

---

### D3 — Consolidate duplicate Python freshness oracles (medium value, probe-only)

**Problem:** Two independent implementations of the same spec fragment:

| Location | Role |
|----------|------|
| `corpus/evidence/round26-measure.sh:97-150` | Inline heredoc oracle for `C2_ORACLE_AGREE` |
| `corpus/evidence/round26-date-differential.sh:51-70` | `oracle()` inside differential harness |

Logic aligns (ISO recheck, `verified + timedelta`, `on-release`, unknown, `asof > due`). Drift between them would falsely fail or pass C2 without gate bugs.

**Deletion:** Extract one module (e.g. `corpus/evidence/round26-freshness-oracle.py`) with a single `due_freshness(verified_at, recheck, as_of)`; delete duplicated bodies from measure heredoc and differential script (import or subprocess).

**Why safe:** Oracles remain independent of the gate; only probe code shrinks. Gate Bash calendar stays the implementation under test.

**Tradeoff:** Small shared library is a second file to pin in `round26-measured-revision.json` if treated as production evidence input.

---

## Non-deletions (would harm an axis)

| Item | Anchor | Reason to keep |
|------|--------|----------------|
| Civil calendar pair | `2295-2359` | Spec forbids GNU `date` and requires proleptic Gregorian add with range cap (`9999-12-31` bound at 2355–2357). |
| Global `META_DAYS` / `META_DATE_RESULT` | passim | Coupling is ugly but deleting globals without a struct is a refactor, not a deletion; risk of subtle ordering bugs. |
| `metadata_add_days` re-parse of Y-M-D after `metadata_iso_date` | `2343-2353` | Redundant work, not duplicate authority; folding would add parameters, not remove a path. |
| `metadata_days_from_civil(9999 12 31)` per add | `2355-2356` | Could cache as a constant (optimization), not behavior-preserving deletion. |

---

## Correctness-threatening abstraction (flag, do not “simplify” blindly)

1. **Two comparison models in one function:** Day-add uses integer civil days; freshness uses the same model today while ISO-due could use strings (D1). Until D1 lands, maintain both paths consistently.
2. **Triple oracle surface:** Gate Bash + measure Python + date-differential Python. Any gate “simplification” that shrinks civil range to match only the six controls would pass `C2_CONTROLS_CAUGHT` but fail `DATE_DIFF_AGREE` (9024 cases exercised here).
3. **`freshness=current` staging** (`2738-2756`): Sets `current` then maybe `overdue`. Not wrong; collapsing branches is style-only unless D1/D2 applied.

---

## Registry / reader cross-talk (milestone boundary)

C2 date code does not allocate per body line beyond the existing fd-bound snapshot (`2603-2606`). Reader allocation is C1; registry parsing is C3. D1–D3 stay inside Claim 2 surfaces.

---

## Recommended landing order

1. **D1** — largest per-entry savings on `--as-of` over 29+ entries; re-run `round26-date-differential.sh` + `round26-measure.sh c2`.
2. **D2** — trivial follow-up in the same function.
3. **D3** — probe hygiene; no gate change.

---

## Report trailer

Report: `.ufo/waves/round-26/falsify/FSimplifyDate.md`
