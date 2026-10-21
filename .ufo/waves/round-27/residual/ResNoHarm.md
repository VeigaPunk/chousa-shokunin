VERDICT: FALSIFIED (narrow, low severity) — on the lane's own corpus no axis is harmed (162/162 runs byte-identical across base, dd72641e and cb895a2), but two synthetic behaviors make cb895a2 worse than base 64eec5d outside the declared repairs: a time cost and a claim-source over-refusal. A third behavior is worse than dd72641e but identical to base.

# ResNoHarm — round 27 residual: no-axis-harmed across base / dd72641e / cb895a2

Seat ChousaR27-2.ResNoHarm-16. Read-only on the lane; the only lane write is this file. Sandbox is
`/tmp/chousa-r27-residual-ResNoHarm/{base,dd,cb}` (`git -C <lane> archive <rev> | tar -x`). The gate
sha256 values match the assignment: c2c813f1…abc6 (base), ca39d14d…2f84 (dd), a6bc2855…2386 (cb).
Lane-corpus runs use one fixed tree (the cb archive) with only `tools/research-gate.sh` swapped, so any
difference comes from the gate alone. All fixtures are synthetic under /tmp; no network; tools installed: none.

## Axes and instruments

- **Operability:** exit class, crash/timeout, and wall time. Times come from a sequential `timing.py`, one gate at a time.
- **Freshness:** `due=` and `freshness=` values and the overdue verdict.
- **Calibration:** findings, refusals and verdict lines. The full stdout and stderr are compared after masking `ts=`, the sandbox paths and the `gate_sha256` identity.
- **Harness:** `J=10 python3 /tmp/chousa-r27-residual-ResNoHarm/harness.py` → exit 0. It ran 700 cases × 3 gates in 35 s with no timeouts and no case where cb is more than 2× slower.

Families covered:
- Lane corpus (162): verify-metadata on knowledge, lessons, evidence, `corpus/` and fixtures/metadata-r25, crossed with:
  - registry absent or `corpus/SOURCES.md`;
  - `--as-of` none, 2026-10-21, 2027-06-01 or 9999-12-31;
  - `CHOUSA_STRICT` 0 and 1.
- Lane corpus, continued: per-entry strict runs with the registry, verify-claims on all 7 claims files, and verify-all on every fixture record, with and without `--claims` and with `--json`.
- Registry grammar (98).
- S-id (44).
- Dates: 270 runs on verified-at × cadence × as-of, plus 57 `--as-of` runs × locale (inherited en_US.UTF-8, C, C.UTF-8).
- Denylist (31) and ancestor directories (30).
- Usage errors (8).

Tally: 646 identical on all three gates; 15 differ only at dd (cb equals base again); 35 changed at dd and carried into cb; 4 are new at cb.
Lane corpus: 162/162 identical. The 8 verify-all `--json` manifests differ only in `gate_sha256` (0 diff lines after masking).

## Findings — cb worse than base, not a declared repair

**F1 — operability/time, introduced by post-falsify change (a) (`dd72641e..cb895a2b`, gate :2491-2493).**
- **Attacks:** the extra GFM width pass, `IFS='|' read -r -a width_cells <<<"${row//'\|'/}|…"`, which builds a second array of every header cell.
- **Fixture:** a header of the form `| id | status | used-by | <N × \|> |`, then `|---|---|---|---|` and a row.
- **Command:** `bash <gate> verify-metadata corpus/knowledge/e.md --root . --registry reg.md`.
- **Result:** exit 0 and CLEAN on both gates, at every size.

| header size | base ms | cb ms | cb vs base |
|---|---|---|---|
| 1 MiB (×3 runs) | 5414 / 5571 / 5328 | 6830 / 6749 / 6761 | +26% |
| 2 MiB | 19759 | 27178 | +38% |
| 4 MiB | 75886 | 105861 | +40% |

- **Inherited part:** both gates are about quadratic in header size; that part is base behavior.
- **Introduced part:** the extra 31–40% at 2–4 MiB.
- **Extrapolation at the 8 MiB read cap** [INFERENCE]: about 300 s on base and about 420 s on cb.
- **Impacted axis:** operability.
- **Smallest correction** [INFERENCE: cost not measured]: count the cells without a second array, e.g. `w=${row//'\|'/}; w=${w//[^|]/}; header_width=$((${#w}+1))`. Cells equal pipes + 1 once the outer pipes are stripped, so the selftest cases 211–212 keep their outcomes.

**F2 — calibration/refusal, introduced at dd72641e and carried unchanged into cb.**
- **Attacks:** the new canonical-path check in `claim_source_path` (cb :1166, `is_denylist_fs_path "$canon"`). It matches the denylist value patterns against the whole absolute path, including the root's own ancestors.
- **Fixture:** root `<fx>/anc/<A>/lane`, holding `src.md` ("say hello world here") and a claims line `{"id":"c1","source":"src.md","span":"hello world","expect":"supported"}`.
- **Command:** `bash <gate> verify-claims <root>/claims.jsonl --root <root>`.

| ancestor `<A>` | base | dd / cb |
|---|---|---|
| credentials, oauth, .omp, .config, .local/state, Cookies, chrome-profile, server.token.d, x.env:y | exit 0, `CLEAN (claims=1 supported=1 …)` | exit 1, `FINDING CLAIM_SOURCE_SESSION severity=crit … obs=path=src.md denied (not opened)` |
| clean | exit 0, CLEAN | exit 0, CLEAN |

- **verify-all:** the claims section flips from CLEAN to DRIFT (`drift-sections=1→2`).
- **Inherited context:** under the same ancestors, base already refuses metadata registries (`metadata registry refused: denylist`, exit 2 on all three gates) and structure pointers (`POINTER_UNRESOLVED`). So the change makes claims consistent with existing surfaces, but it is a new refusal of benign claims relative to base.
- **Not named by C3**, which covers colon/prefix and complete-path forms.
- **The diagnostic misattributes the cause:** it says `path=src.md` when the denied component is the ancestor.
- **Live lane:** `/home/vgpnk/Projects/shokunin/chousa-shokunin` has no such component, so it is unaffected.
- **Impacted axis:** calibration (fail-closed, so it is a false refusal, not a bypass).
- **Smallest correction:** either declare the behavior (one selftest plus doc sentence pinning ancestor refusal), or match the canonical check against the path relative to `src_root`. The symlink→`.env` refusal (base read it, cb refuses) must stay either way.

## Finding — cb worse than dd72641e, identical to base (reopened inherited)

**F3 — calibration: an escaped pipe before a bound column is accepted and misbound.**
- **Attacks:** change (a) has two cell grammars. The width uses the GFM split (`\|` is content); `id_col`, `status_col`, `used_by_col` and every data row still use the naive split (:2444, :2454-2458).
- **dd behavior:** dd refused these tables with exit 2 (`metadata registry has no table …`).
- **cb behavior:** cb admits them and binds shifted columns, with outputs byte-identical to base.
- **Common fixture:** entry `source: S001` / `verified-at: 2026-01-02 checked` / `recheck: 90d`. The registry header and delimiter vary per row of the table:

| registry (header / row; delimiter `\|---\|---\|---\|---\|`) | GFM reading [INFERENCE: GFM spec from memory, no network] | base | dd | cb |
|---|---|---|---|---|
| `\| id \| a \\| b \| status \| used-by \|` / `\| S001 \| x \| mined \| corpus/knowledge/e.md \|` | status=mined → CLEAN | exit 1, false NOT_MINED | exit 2 | exit 1, false NOT_MINED |
| `\| id \| status \| a \\| b \| used-by \|` / `\| S001 \| mined \| x \| corpus/knowledge/e.md \|` | CLEAN | exit 1, false USEDBY_MISSING | exit 2 | exit 1, false USEDBY_MISSING |
| `\| id \| a \\| b \| status \| used-by \|` / `\| S001 \| x \| queued \| mined \| corpus/knowledge/e.md \|` | status=queued → NOT_MINED | exit 0, **false CLEAN** | exit 2 | exit 0, **false CLEAN** |
| `\| a \\| b \| id \| status \| used-by \|` / `\| x \| S009 \| S001 \| mined \| corpus/knowledge/e.md \|` | id=S009 → ROW_MISSING | exit 0, **false CLEAN** | exit 2 | exit 0, **false CLEAN** |

- **Command:** `bash <gate> verify-metadata <fx>/corpus/knowledge/e.md --root <fx> --registry <fx>/reg.md`, with `CHOUSA_STRICT` 0 and 1 (same result).
- **Control weakness:** `round27-falsify-controls.py:131` and selftest cases 211–212 place the escape only after every bound column (`note \| alt` last). So no control separates "GFM width with naive binding" from a real GFM split.
- **Impacted axis:** calibration (a false CLEAN where dd failed closed).
- **Smallest correction:** keep dd's refusal whenever `\|` occurs in the header before the last bound column (no candidate header). This preserves 211/212. Then add the first and third rows above as controls (expected outcome never exit 1 / exit 0 respectively).

## Introduced vs inherited (residuals named by the falsify wave plus this sweep)

| behavior | base | dd | cb | class |
|---|---|---|---|---|
| BOM before registry header (`reg_bom`, `reg_bom_crlf`) | exit 1, false `META_SOURCE_ROW_MISSING` (BOM shifts cell 0) | exit 2, no table | exit 2, no table | **exit-class change introduced at dd** by the declared width rule (4 naive header cells vs a 3-cell delimiter); unchanged dd→cb; both wrong, cb fails closed |
| BOM before entry `source:` | exit 1, `META_SOURCE_ABSENT` | same | same | inherited |
| BOM without outer pipes | exit 2 | exit 2 | exit 2 | inherited |
| Mixed outer pipes (header-only, delimiter-only, lead-only; 5 shapes) and doubled outer pipes | exit 0 CLEAN; doubled: identical | same | same | inherited (no divergence across revisions) |
| Escaped pipe inside a data-row used-by (`a\|corpus/knowledge/e.md`) | exit 0, false CLEAN | same | same | inherited (falsify CE-4) |
| Escaped pipe in header after bound columns | exit 0 | exit 2 | exit 0 | dd regression repaired by declared change (a) |
| Escaped pipe in header before a bound column | misbinding (F3) | exit 2 | misbinding (F3) | inherited, **reopened by (a)** |
| Overwide escaped header; `a \\| b` with a 5-cell delimiter | exit 0 | exit 0 | exit 2 | declared (a), selftest 212 |
| Prefix over-refusal: `notes.env:2026.md`, `ordinary.env:notes/e.md` (entry, claim, registry) | refused | refused | refused | inherited (legacy prefix arm) |
| Colon-suffix `.env` (`x:y.env`, `a:b.env`, `k.md:op.env`) | read, exit 0 | refused | refused | declared C3 |
| Symlink `ok.md → secret.env` as claim source | read, CLEAN | refused | refused | declared C3 (fixes an under-refusal) |
| Claim source under a denylisted-looking ancestor | read | refused | refused | **introduced at dd (F2)** |
| Unicode-digit `--as-of` under inherited UTF-8 | exit 1 | exit 2 | exit 2 | declared C2 (C locale: exit 2 on all three) |
| Header/delimiter width, blank break, bad-then-good, trailing-empty header | accepted | exit 2 | exit 2 | declared C3 |
| Cadence and verified-at matrix (270 runs, incl. 2000-zero and 40-zero cadences, `9999999d`, `10000000d`, Unicode digits) | identical | identical | identical | no change |
| Token-dense source, 4 MiB `a ` | 64318 ms | 72729 ms | 425 ms | improved (b) |
| Id-dense source, 1 MiB `S001 ` | TIMEOUT 90 s | 6470 ms | 4183 ms | improved |
| 4 MiB LF registry line | 66462 ms | 64346 ms | 576 ms | improved (c) |
| Escaped-pipe-dense header | quadratic | quadratic | +31–40% | **introduced by (a) (F1)** |

Changes (b) and (c) are equivalent to dd on every input tried, including:
- **(b) S-id prefilter:** glued, prefixed or suffixed ids, `S0011 S001`, `aS001 S001`, non-ASCII neighbours, invalid bytes, CR inside the value, 5000 repeated ids and 50 000 tokens.
- **(c) CR strip:** CRLF, `\r\r\n`, lone `\r` line endings, a CR-only line between header and delimiter, and CR inside a cell.

Both read loops run under `local LC_ALL=C` (:2385, :2568), so the strip is byte-exact.

## Control and coverage weaknesses (not gate behavior)

- `round27-falsify-controls.py` cannot measure base: it stops with exit 2 (`usage selftest helper not found: metadata_asof_usage_accepts`). So it is not a base-vs-cb no-harm instrument.
- On dd the controls exit 1 with 4 mismatches; on cb they exit 0 with 0/26. This matches the post-falsify receipt.
- No control places `\|` before a bound column (see F3).
- No control or selftest case covers a claim root under a denylisted ancestor (see F2). The falsify reports grepped for "ancestor" mention only the registry case (FC3PlainDeniedComponent44 C-C, base equal to landed).

## Commands and exit codes

| command (sandbox) | exit | decisive output |
|---|---|---|
| `sha256sum {base,dd,cb}/tools/research-gate.sh` | 0 | c2c813f1… / ca39d14d… / a6bc2855… |
| `J=10 python3 harness.py` | 0 | `cases 700`; `B=D D=C B=C 646`; `cb-slower []`; `timeouts []` |
| `TO=90 python3 timing.py` | 0 | table rows above |
| escaped-header scaling loop (1, 2, 4 MiB; `timeout 300`) | 0 | F1 table |
| `cb: bash tools/research-gate.sh --selftest` (inherited en_US.UTF-8, CHOUSA_* unset) | 0 | `RESEARCH_GATE_SELFTEST: PASS (215 cases, 0 skipped)` |
| `python3 cb/corpus/evidence/round27-falsify-controls.py --gate {base,dd,cb}/tools/research-gate.sh` | 2 / 1 / 0 | base: helper not found; dd: 4 mismatches; cb: 0/26 |
| JSON manifest diff, masking ts, paths and gate_sha256 | 0 | 0 residual lines (8 manifests × 2 comparisons) |

Limits:
- GFM readings are [INFERENCE] (no spec fetch).
- The ancestor set is a sample of the denylist value patterns.
- Timings come from one host with no other load from this seat.
- verify-chain, verify-sweeps and verify-integrity were not run separately; they are exercised only inside verify-all.

This is author-lane advice, not outside admission.
