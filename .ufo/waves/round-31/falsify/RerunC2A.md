# RerunC2A — re-derive C2 counting on the landed revision

**Attacked:** the landed C2 implementation (`6d0ae19`, tip `ee1024fd`) as measured by the frozen
counter `corpus/evidence/round31/c2-count.py` on the default (landed) gate. Question: does C2
reproduce 120/120 on fresh seeds outside the L1's two measurement seeds, and do the receipts bind
the committed counter and the tip gate?

**Lane state (read-only checks, lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`):**
- `git rev-parse HEAD` → `ee1024fd492144c9c7b315890fac247543c37208`; `git log --oneline -3` →
  `ee1024f` / `6d0ae19` / `c17948a`.
- `git show ee1024fd:corpus/evidence/round31/c2-count.py | sha256sum` →
  `1064fdb356e25440c64bb4d4d5363acb9c1bbc32c687c8ea50096d74c849d500`
  (same as the working-tree file; the file is not in `git status`, so the run used the committed bytes).
- `git show ee1024fd:tools/research-gate.sh | sha256sum` →
  `c23d7537e03482f2844c9cbc43fc055d3d08d564857a89529b6f13473403823c`
  (identical at `6d0ae19`; tip gate = C2-landing gate).
- `git status --porcelain` before and after the runs: only pre-existing `M .ufo/waves/round-31/build/swarm-registry.json`
  and the untracked round-31 falsify files. No lane production file, gate, counter, or index was touched.

**Runs (5 fresh seeds, lane root, default gate, `timeout 900`, `--receipt` into this seat's dir):**
command shape: `timeout 900 python3 corpus/evidence/round31/c2-count.py --seed <S> --receipt .ufo/waves/round-31/falsify/RerunC2A/receipt-<S>.json`

| seed | score | receipt | counter_sha256 | gate_sha256 | predicate_holds | misses |
|---|---|---|---|---|---|---|
| 20261023 | REVISION_BINDING_MATCH=120/120 | `RerunC2A/receipt-20261023.json` | `1064fdb3…49d500` ✓ | `c23d7537…03823c` ✓ | true | `[]` |
| 777001 | REVISION_BINDING_MATCH=120/120 | `RerunC2A/receipt-777001.json` | `1064fdb3…49d500` ✓ | `c23d7537…03823c` ✓ | true | `[]` |
| 424242 | REVISION_BINDING_MATCH=120/120 | `RerunC2A/receipt-424242.json` | `1064fdb3…49d500` ✓ | `c23d7537…03823c` ✓ | true | `[]` |
| 918273645 | REVISION_BINDING_MATCH=120/120 | `RerunC2A/receipt-918273645.json` | `1064fdb3…49d500` ✓ | `c23d7537…03823c` ✓ | true | `[]` |
| 31337 | REVISION_BINDING_MATCH=120/120 | `RerunC2A/receipt-31337.json` | `1064fdb3…49d500` ✓ | `c23d7537…03823c` ✓ | true | `[]` |

All five exited 0; `gate_rc=1`, `gate_timed_out=false`, `total=120`, `matched=120`, `elapsed_s` 1.99–2.01.
Per-class on every run (identical counts, order shuffled): `R1_match_span_present 24/24`,
`R2_match_span_absent 10/10`, `N1_no_sha 16/16`, `S1_one_byte_elsewhere 16/16`,
`S2_newline_variant 12/12`, `S3_hash_of_span_only 10/10`, `S4_mismatch_span_absent 10/10`,
`S5_hash_of_other_fixture_file 8/8`, `I1_invalid_sha_value 14/14`.

**MISSES:** none. No run scored below 120/120, so no miss list is quoted.

**Freshness check:** L1's two C2 measurement seeds were 6074196312812550633 and 3655576086102470853
(`.ufo/waves/round-31/measure/after-c2-run{1,2}.json`); all five seeds here are disjoint from those,
from the L1 smoke seeds (1, 2) and from each other.

**Predicate P2:** re-derived independently of the L1 receipts — the frozen counter prints
`REVISION_BINDING_MATCH=120/120` with `predicate_holds=true` on each of five fresh-seed runs on the
landed revision, and no round-31 run of this counter on this revision prints a lower count (the
L1's two runs also read 120/120). **C2 holds on this axis.**

**Verdict: holds.** No regression found against the C2 landing on the operability axis.

**Limits / what this does not establish.**
- Coverage of the *other* axes (C1 line binding, controls chronology, D1–D8 corrections, S057–S059,
  no-harm) is out of scope here; this seat measured C2 operability only.
- No negative/control re-run was performed (the base-gate 50/120 before-value was not re-derived here);
  the 120/120 result is positive evidence of the landing, not a re-proof of separability.
- Run-to-run reproducibility was observed across 5 seeds only; the counter's determinism beyond that
  is not claimed.
- No tooling was installed or updated by this seat; no network access was used.
