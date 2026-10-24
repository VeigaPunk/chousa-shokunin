# W2RevReceipts

## Verdict
All nine committed round-38 receipts are clean on every assigned axis (fields/64-hex, frozen census,
arithmetic, gate bindings, canonical self-digest) and verify `ok` under both the tip and the current
worktree verifier; the defects found are pipeline-level (declared-path and subject identity are carried
strings the verifier never re-derives) plus one live uncommitted verifier change on the "final bytes".

## Evidence
Lane tip `git rev-parse master` = `8e93bc916527b3c21f0f702967fa65c3b4c31699`; all nine receipts committed
there (`git log -1 -- <receipt>` → `8e93bc9`), worktree == HEAD for the receipts dir; no counter executed.

1. Gate hashes computed myself; provenance by blob (`git show <rev>:tools/research-gate.sh | sha256sum`):

```
tools/research-gate.sh                               37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d  (= tip 8e93bc9)
.ufo/waves/round-37/controls/base-gate-r37.sh        a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  (= git 700bd5f, r36-freeze gate)
.ufo/waves/round-38/controls/base-gate-r38.sh        9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  (= git 95e33de, r37 closure = r38 pre-round)
corpus/evidence/round37/c1-count.py (c2-base subject) eec810050dd174e3b6e8401efab35df2a18e310a27c212eb775e96c55830ba29
corpus/evidence/round38/expectations.jsonl           d34f17353fec83ed2e7b78b41cebcd2a6d309a85d724dbf1097cf6a17afaf8aa
```
   Both control-gate files are tracked (`git ls-files`, `git check-ignore` rc=1): every receipt's gate
   preimage is committed bytes.

2. Independent audit (/tmp/w2rev/audit.py: presence, 64-hex regex, frozen census, per-row `expect` tie +
   `ok` re-derivation, matched/total/predicate_holds recount, gate/counter/expect preimage equality,
   canonical self-digest; JSON parsed with a duplicate-key-rejecting `object_pairs_hook`) →
   `receipts with any failing binding: 0`:

```
receipt                  claimed gate           sha(pre)       pre=post pre=file gate_alias ctr=file exp=file digest
c1-after-s38001.json     research-gate.sh       37e2b9968706   True     True     True       True     True     True
c1-after-s38011.json     research-gate.sh       37e2b9968706   True     True     True       True     True     True
c1-after-s38351.json     research-gate.sh       37e2b9968706   True     True     True       True     True     True
c1-base-s38001.json      base-gate-r37.sh       a7d3922c768a   True     True     True       True     True     True
c1-base2-s38003.json     base-gate-r38.sh       9fcac047ddad   True     True     True       True     True     True
c2-after-s38101.json     research-gate.sh       37e2b9968706   True     True     True       True     True     True
c2-after-s38111.json     research-gate.sh       37e2b9968706   True     True     True       True     True     True
c2-after-s38371.json     research-gate.sh       37e2b9968706   True     True     True       True     True     True
c2-base-s38101.json      research-gate.sh       37e2b9968706   True     True     True       True     True     True
```
   Each receipt: 7 rows, six digest fields all `^[0-9a-f]{64}$`, census exactly the frozen family ids
   (`extra=[] missing=[]` ×9), `matched` == count(`ok`), `total` == 7, `predicate_holds` == (7/7 ok;
   bases 2/7, 0/7 → `false`), and on-disk bytes ARE the canonical serialization (`raw ==
   json.dumps(body+sig, indent=2, sort_keys=True)+"\n"` ×9), so `receipt_sha256` covers every other byte.

3. Canonical verifier re-run on all nine (landed gate for afters and c2-base; each c1 base's own control
   gate): `VERIFY: ok … rc=0` nine times. Base receipts vs the landed gate refuse as claimed:
   `c1-base-s38001 → VERIFY-FAIL: gate-sha256-mismatch rc=1`; `c1-base2-s38003 → same`; but
   `c2-base-s38101 --gate tools/research-gate.sh → VERIFY: ok rc=0` at `matched=0/7` (F5).

4. Verifier attacks, re-sealed copies under /tmp/w2rev/att, both verifier versions — caught:
   `reroute` (c1 receipt, c2 counter) → `scenario-census-mismatch`; `doctored-obs` → `ok-rederivation-
   mismatch hold-plain`; `vacuous`/`census-swap` → `scenario-census-mismatch`; `ok-flip` →
   `ok-rederivation-mismatch env-fn-root-move`; `matched-lie` → `matched-recount-mismatch`; `expect-lie`
   → `expect-tie-mismatch hold-plain`; legacy round-37 receipt → `missing-field counter_sha256`.
   NOT caught: `all-paths-lie`, `all-paths-lie-c2`, `no-path-fields`, `gate-path-lie` (F1);
   `named-refusal-lie` (F3).

## Findings
1. **[medium; no committed receipt affected] The declared provenance paths are never read.**
   `verify-receipts.py` hashes only the CLI `--gate`/`--counter`/`--expectations`; body fields `gate`,
   `counter`, `expectations`, `subject_counter` are covered by `receipt_sha256` but never validated.
   Re-sealed from `c1-after-s38001` with those paths pointed at nonexistent files
   (`/tmp/w2rev/att/all-paths-lie.json`), likewise c2 with a fake `subject_counter`
   (`all-paths-lie-c2.json`), and with all four fields deleted (`no-path-fields.json`): `VERIFY: ok … rc=0`
   under BOTH verifier versions (`ls /tmp/w2rev/att/does-not-exist.sh /tmp/w2rev/att/not-a-counter/` →
   both absent). Reading: `VERIFY: ok` means "these digests equal the files the caller named", not "the
   receipt measured the gate/counter it names"; receipt→gate mapping must come from claims.md.

2. **[low-medium, pipeline] The subject counter of every c2 receipt is unbound.** No field in
   `c2-after-s38101.json` equals `sha256(corpus/evidence/round38/c1-count.py)=79040790…` (`fields equal
   to sha256(r38 c1-count.py): []`); the digest fields preimage `c2-count.py` (414a7a…), the table, the
   gate, and the body only. Worst at `c2-base-s38101.json`, whose whole control story
   ("`--counter corpus/evidence/round37/c1-count.py`, 0/7") rests on a path string;
   I recovered that identity from git (`eec81005…`, tracked at tip), not from the receipt. §C2 claims
   only scoring-counter binding, so this is an undeclared edge of "binds WHICH counter".

3. **[low] `_contains` annotations are excluded from `ok` re-derivation, so the named refusal is
   text-only.** The verifier skips `k.endswith("_contains")`, so the three tamper rows re-derive from
   `clean_verify_rc`/`verify_rc` alone. Replacing `observed.verify_fail` with
   `"VERIFY-FAIL: totally-different-label"` on all three rows and re-sealing
   (`/tmp/w2rev/att/named-refusal-lie.json`) → `VERIFY: ok … rc=0` (both versions). The committed
   receipts carry the correct labels (`counter-sha256-mismatch`, `expect-sha256-mismatch`,
   `receipt-self-digest`), and a wrong label at generation makes the counter's `ok=false`, so no silent
   accept exists at generation; the gap is verification-side, inside the re-seal/authorship limit.

4. **[medium, live "final bytes"] The verifier on disk is not the tip's verifier.**
   `sha256sum corpus/evidence/round38/verify-receipts.py` = `3fc416612085a4ba8333b6b39a9ad2f4e32eb17ebcbc53ae6cd2e048f8abf919`;
   `git show 8e93bc9:...verify-receipts.py | sha256sum` = `b63e7e20…c952`;
   `git diff 8e93bc9 -- corpus/evidence/round38/verify-receipts.py corpus/evidence/round38/claims.md`
   = +10/+10 uncommitted lines (strict `KNOWN`/`unknown-field` refusal, in-file attributed to
   W2CritLaundering, plus an Erratum 9 block), mtimes 01:16:42 / 01:16:54. Both versions give identical
   `VERIFY: ok` for the nine, but diverge on receipt shape: `/tmp/w2rev/att/extra-field.json`
   (committed c1 body + one extra re-sealed field) → `VERIFY: ok rc=0` under the tip verifier,
   `VERIFY-FAIL: unknown-field extra_doctored_field rc=1` under the worktree verifier. That is
   Erratum 2's carried debt (bind `verifier_sha256`) firing live: identical receipt bytes, two verdicts,
   no receipt-side record of which verifier adjudicated; L1 must commit or revert this edit before
   treating 8e93bc9 + worktree as final.

5. **[informational] "Base receipts refuse the landed gate" holds only for the c1 pair.**
   `c1-base-s38001` (control `a7d392`) and `c1-base2-s38003` (control `9fcac0`, the r38 pre-round gate
   per Erratum 6(e)) both REFUSE the landed gate; `c2-base-s38101` claims the LANDED gate (`37e2b9`) and
   verifies `ok` at 0/7 — its control is a counter, not a gate. Both c1 bases score 2/7, identical ok
   pattern `[T,T,F,F,F,F,F]`, matching claims.md §C1 Before.

6. **[informational] Replication is label-level, as disclosed (Erratum 6(d)).** Modulo `seed` and
   `receipt_sha256` the three `c1-after-*` bodies are one body and the three `c2-after-*` are one body
   (3 seeds → 1 distinct body each); `c1-base`/`c1-base2` are 2. Not independent replication.

## Limits
- No counters executed, no fresh-seed receipt generated; this audits committed bytes plus verifier
  behaviour on re-sealed /tmp copies. Counter internals, the gate body and the 272-case selftest were
  not audited, and hostile-environment operability of the counters belongs to another seat.
- Hash equality is content equality, not file identity: a byte-identical copy at another path verifies
  (the verifier's own named limit); receipt-path symlink identity is likewise unbound.
- Control-gate provenance is checked against git blobs at `700bd5f`/`95e33de`; that those revisions are
  the correct r37/r38 baselines is taken from Erratum 6(e), not independently re-derived.
- No tools installed or upgraded; no pacman transaction; the lane repo was not mutated (only this report
  written); scratch work lives under `/tmp/w2rev/`.
