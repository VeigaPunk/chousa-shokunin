# ReviewC2Probe32 — C2 exempt-hop audit code review (round 32, attempt 2, WAVE 2)

Seat: ChousaR32A2.ReviewC2Probe32. Reviewed `tools/research-gate.sh` at landed
`5d8a170795dcf48c3746a4f03dee9cfe32812834` (SHA-256 `10f2fe12…4098`, verified by
`sha256sum` against the lane file) vs base `7a7259f0…` (gate `0bc318b3…`).
Scope: `chain_probe`, `CHAIN_EXEMPT_RESOLVABLE`, U-arm silence, summary-line
change, other exempt-status arms, four new selftest cases.

## Evidence collected

Scratch: `/fast/scratch/hyaku/chousa-r32/w2/ReviewC2Probe32/` (copies of base +
landed gates at `lane-{base,new}/tools/research-gate.sh`, 6-status fixture
records, outputs). Receipts/artifacts copied to `.ufo/waves/round-32/w2/ReviewC2Probe32/`.

1. **Fresh-seed counter run (real data).**
   `TMPDIR=<scratch> C2_TMP=<scratch> timeout 900 prlimit --nproc=8000 python3
   corpus/evidence/round32/c2-count-v2.py --seed 777001 --receipt
   .ufo/waves/round-32/w2/ReviewC2Probe32/c2-r777001.json` →
   `EXEMPT_AUDIT_MATCH=132/132`, `RECORD_CHECKS=ok`, all 15 classes full, rc=0,
   `misses: []`. Third full run after measure receipts `after-c2-s32011/32012`
   (both 132/132, `predicate_holds=true`). No run below target observed.

2. **Resolved-arm equivalence (chain_probe refactor).** Built
   `fix/rec-resolved.md`: 19 `resolved` hops covering every probe branch
   (fragment citation, anchor-column citation, bare `#heading` fragment,
   declared id, declared empty pointer, anchor absent, case-only anchor,
   double-spaced anchor, missing file, URL, undeclared id `S9`, `../outside`
   escape, empty `to`, missing anchor, bad `anchor_kind`, to#frag+anchor
   conflict). Command: `bash <gate> verify-chain rec-resolved.md --root fix`.
   `diff base-resolved.out new-resolved.out` → identical except the header
   timestamp and the appended ` resolvable=0` token in the summary line:
   `hops=19 verified=7 exempt=0 anchor-missing=3 refused=5 invalid=4
   findings=12 drift=12`. Every CHAIN line and all 12 FINDING lines
   byte-identical → `chain_probe` is a faithful extraction of the base
   resolved arm (same `CITE_ERR` text, same `chain_refuse_id`/`chain_source_sev`
   mapping, same `chain_nearest` context, same `at=` fields).

3. **U-arm behavior.** Same 19-row record rewritten to `unresolved`,
   `blocked-no-fetch`, `labelled-dead`: each prints
   `resolvable=7 exempt=12 findings=7 drift=7`, rc=1, exactly 7
   `FINDING CHAIN_EXEMPT_RESOLVABLE severity=warn surface=chain obs=hop=…`
   lines matching the resolved arm's 7 verified hops (incl. case-exact
   `UPPER ONLY SENTENCE`; case-diff and double-space anchors stay exempt).
   Zero `CHAIN_SOURCE_*`/`CHAIN_ANCHOR_*`/`CHAIN_CITATION_*` findings →
   silence on U-hop refusals verified (`new-unresolved.out`).

4. **J-arm unread.** `rejected` / `not-applicable` records: all 19 hops
   (including the 7 verifiable) `observed=exempt`, `findings=0`, rc=0 CLEAN
   (`new-rejected.out`) — judgment statuses stay unread whatever the citation.

5. **No-harm fixtures.**
   - `verify-chain corpus/fixtures/chain-r3.md --root ..` →
     `RESOLVED_HOPS=17/22`, `RESEARCH_GATE: CLEAN (… resolvable=0)`; hops
     18–22 (2 URL blocked-no-fetch, 3 declared-id unresolved with absent
     anchors) stay exempt.
   - `verify-chain corpus/fixtures/chain-r3-broken.md --root ..` → `1/2 DRIFT`.
   - `verify-claims corpus/fixtures/claims-r2.jsonl --root ..` → `17/17 CLEAN`.
   - `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (241 cases, 0 skipped)`
     (base: 228; new cases 229–241 incl. the four audit cases at 229–232 and
     C1 cases 233–234; `selftest.out`).

6. **Summary line.** `…drift=%d resolvable=%d)` — new token appended at the
   tail (landed L1987). Every base selftest substring ends at `drift=N` (no
   `)`), so all base case lines still match; selftest PASS confirms.
   `verify_all`'s VAS parser greps `drift=` and `RESOLVED_HOPS=` individually
   (L3117) → unaffected. `ROLL` check adds `N_RESOLVABLE` to the accounting
   sum; resolvable still drifts via `emit_finding` warn → ROLL (L447-449).
   `RESOLVED_HOPS` numerator stays verified-only, matching the updated doc
   formula `N = M − exempt − resolvable` (L119-121).

7. **Other exempt-status arms — did they need touching?** Reviewed:
   - `verify_sweeps` exempt arm (base ~L2152): sweeps carry `where` location
     sets, not citation+anchor pairs; no `to`/anchor to probe → correctly
     untouched, out of contract scope.
   - `verify-integrity` `exst` arms (base ~L2383-2427): pointer resolvability
     cells for exempt rows; integrity is a different surface (REF lines), not
     `verify-chain` hops → correctly untouched.
   - `verify_record` shape check `unresolved|blocked-no-fetch` notes
     requirement (~L1039-1072): unchanged; it runs in `verify-all`'s
     structure section, not under `verify-chain`, so it cannot leak a
     `CHAIN_HOP_UNRESOLVED` finding into the audited surface (selftest
     `got_other=0` confirms).

8. **Four new selftest cases** (229 `chain-exempt-resolvable` rc=1/res=7/ex=0;
   230 `chain-exempt-unresolvable` rc=0/0/9; 231 `chain-exempt-judgment`
   rc=0/0/2; 232 `chain-exempt-mixed` rc=1/1/1): all pass. The `tchain_audit`
   runner asserts `got_find == want_res` and `got_other == 0` (no
   resolved-arm finding leak) plus per-line substrings — stronger than the
   substring-only runner.

## Findings

- **None blocking.** No contract violation, no counter-miss found.
- **[info] Doc asymmetry:** CHAIN-line `observed=` list (L117) includes
  `resolvable`, but the `verdict=` list (L118) does not — a resolvable hop
  prints `verdict=mismatch`, consistent with the contract, just unlisted.
- **[info] Ambiguity, not defect:** two U rows sharing a `hop` id each emit
  one finding, producing 2 findings "naming" that id; contract's "exactly one
  FINDING … per verified hop" is row-scoped [INFERENCE]. No counter class
  exercises duplicate ids.
- **[info] Refusal detail discarded for U hops:** an exempt U hop that the
  resolved arm would report `refused` shows only `observed=exempt` —
  required by the silence contract, but loses the refusal class in CHAIN-line
  output (findings would have carried it).
- **[info] U-hop probes now read local source bytes at `verify-chain` time**:
  bounded by `claim_source_path`'s existing caps (8 MiB, nlink, device), no
  network; slowest path is one `cat` per U hop. No harm observed.

## Verdict

**HOLDS.** `chain_probe` is byte-equivalent to the base resolved arm
(diff over 19 branch-covering hops), U-arm silence is honored, J-arm stays
unread, summary change is append-only and parser-safe, the untouched exempt
arms elsewhere are correctly out of scope, the four selftest cases pass, and
a third fresh-seed counter run scored 132/132. No run below target; no harm
found on fixtures or selftest parity (228→241, 0 skipped).

## Limits

Did not exercise >8 MiB/multilinked/cross-device U-hop sources (the probe
routes through the same `claim_source_path` chokepoint verified in the
resolved arm). Did not re-run the C1 counter (outside this seat's scope).
Duplicate-hop-id records and `CHOUSA_STRICT=1` chains untested. Selftest ran
under `TMPDIR` redirected to scratch.

## Installs

None.
