# ReviewerCounters32b — frozen counters c1-count.py / c2-count.py (round 32, wave 1, attempt 2)

Scope: correctness + flakiness review of `corpus/evidence/round32/c1-count.py` (sha256
`9e787e80…585`) and `c2-count.py` (sha256 `b6626b2c…f54c`) against `tools/research-gate.sh`
(sha256 `0bc318b3…258`, frozen base) and `corpus/evidence/round32/claims.md`. Counters are
frozen; nothing was edited. Artifacts: `/fast/scratch/hyaku/chousa-r32/w1/ReviewerCounters32b/`.
No tool installs. Peer receipts are cited as [peer-reported] where I did not open them.

## Runs (one per counter, base gate, as permitted)

- C1: `cd <lane> && C1_TMP=$S TMPDIR=$S timeout 560 python3 corpus/evidence/round32/c1-count.py --gate tools/research-gate.sh --seed 322101 --receipt $S/c1-base-s322101.json`
  → `APPEND_SERIALIZED=10/24` (`F_unterminated 10/12`, `L_empty 0/4`, `L_terminated 0/4`, `L_unterminated 0/4`), rc=1, 11.7 s; receipt sha256 `4f27554c498f5e4861d34b45b90bc410b053cedbbe1bdb8829ba708c2a3aa6da`; records `counter_sha256`, `gate_sha256=0bc318b3…`, `seed=322101`, `ref_rc=0`, `predicate_holds=false`, per-trial `fails` (first L trial: `appended-under-cooperating-lock` — correct base behavior).
- C2: same shape, seed 322102 → `EXEMPT_AUDIT_MATCH=84/120`, `R1–R3 0/36`, all F1/E classes full, rc=1, 5.4 s; receipt sha256 `91f965a90a0b2ed3c4e271424efc4b3425d35c89a15b8563e2594ef93fd61efa`; `gate_rc=0`, `gate_timed_out=false`.
  Matches claims.md's base expectations (84/120, R1–R3 0/36) exactly; C1 base count is seed-dependent (10/24 here vs 5/24, 8/24 elsewhere) — pre-data variance of the base gate, not a counter defect.
- LOCKS_RE live probe (scratch, real blocked FLOCK waiter): regex
  `^\d+:\s+(->\s+)?FLOCK\s+\S+\s+\S+\s+(\d+)\s+[0-9a-fA-F]+:[0-9a-fA-F]+:(\d+)\s` (c1-count.py:70)
  counted `waiters=1 owners=1` on the probe inode; sample lines
  `35: FLOCK  ADVISORY  WRITE 2014510 103:05:35098591 0 EOF` and `35: -> FLOCK  ADVISORY  WRITE 2015144 103:05:35098591 0 EOF`. Owner lines (no `->`) are excluded from `waiters_on`; decimal inode group(3) == `st_ino`.

## Findings by severity

### HIGH

- **H1 — "exactly one FINDING" is not enforced (set-dedup collapse).** c2-count.py:273
  collects finding ids into a set (`named.setdefault(f.group(2), set()).add(f.group(1))`) and
  :284-286 tests `got == want` with `want={FINDING_ID}`. A candidate emitting N duplicate
  `FINDING CHAIN_EXEMPT_RESOLVABLE … obs=hop=<hop>` lines for one hop still scores matched.
  claims.md C2 contract says "exactly one … line"; the counter docstring rewords to set
  semantics. Cross-evidence [peer-reported]: CtlC2NoisyB duplicate-only reader scored 120/120
  twice (seeds 5239036554333767031 / 6022806861474399502), receipts
  `.ufo/waves/round-32/w1/CtlC2NoisyB/bounded-disjoint-duplicate-only-s<seed>.json`.
- **H2 — FIND_RE accepts any severity/surface tokens.** c2-count.py:79
  `^FINDING (\S+) severity=\S+ surface=\S+ obs=hop=(\S+)(?:\s|$)` never checks that severity is
  `warn|crit` or surface is `chain` (frozen contract wording). A `severity=info` (non-drifting)
  or wrong-surface finding still satisfies the set test at :286.
- **H3 — verdict / drift / record-level contract unasserted.** Contract: resolvable U hops
  print `observed=resolvable (verdict mismatch) … and the record drifts`. The counter scores
  only per-hop `observed=` + finding-id set (:281-289); the printed label/predicate uses only
  `matched` (:303-304). `gate_rc` is recorded (:313) but never constrained; a candidate whose
  run ends CLEAN rc=0 with RESOLVED_HOPS absent would still print 120/120. Cross-evidence
  [peer-reported]: CriticPredicateGaps32b presentation-laundry control (duplicate info/claims
  findings, wrong source/status/verdict, CLEAN, no RESOLVED_HOPS) scored 120/120 twice
  (seeds 320212/213), receipts under `.ufo/waves/round-32/w1/CriticPredicateGaps32b/`.

### MEDIUM

- **M1 — gate-launch OSError misclassified as a claim miss (no receipt, no count).**
  c2-count.py:261-267 and c1-count.py:277-283 catch only `subprocess.TimeoutExpired` around
  `subprocess.run`; any OSError (e.g. `BlockingIOError` EAGAIN under RLIMIT_NPROC) escapes →
  traceback, exit 1, no receipt, no `APPEND_SERIALIZED`/`EXEMPT_AUDIT_MATCH` line — while both
  docstrings promise "2 harness error". Observed [peer-reported]: CtlC2JunkB at nproc=2000 hit
  uncaught `BlockingIOError(EAGAIN)` at c2-count.py:263, exit 1, no receipt; clean at cap 16384
  (log `.ufo/waves/round-32/w1/CtlC2JunkB/resource-errors.txt`). This also blinds the P2
  "no lower count" ledger: the failed run leaves no scored artifact.
- **M2 — C2 truth of class E7 depends on gate/fixture placement geometry.** The gate derives
  its allowed lane root from its own location (`LANE_ROOT=$(cd "$SCRIPT_DIR/.." && pwd)`,
  research-gate.sh:290-291) and source-path admission checks both roots (claim_source_path,
  research-gate.sh:1213-1222). The counter writes `../outside/<file>` beside its fixture root
  (c2-count.py:152-154, 209-210) and puts the fixture under `C2_TMP` (default
  `tempfile.gettempdir()`, :247). A candidate gate copied flat above the temp dir makes E7's
  `../outside` fall inside that gate's lane root → E7 scores 0/6 for a correct reader
  ([peer-reported] initial 114/120 in CriticPredicateGaps32b; same hazard in CtlC2WeakReaderB).
  The receipt records neither the fixture path nor the resolved lane root (:307-316), so a
  geometry-induced E7 miss is not distinguishable from a real reader defect without a `--keep`
  rerun. The docstring asserts "out-of-corpus path" unconditionally; only placement discipline
  (gate at `<dir>/tools/research-gate.sh`, `C2_TMP` disjoint) makes the frozen truth hold.
- **M3 — C1 creation-when-absent clause is exercised only by the solo run and judged only by
  exit code.** Every scored trial pre-creates the manifest (c1-count.py:200-205); the only
  absent-manifest exercise is the solo reference run, checked as `ref_rc in (0,1)` (:277-286)
  with no creation/content assertion. A candidate that cannot create an absent manifest makes
  the counter abort with harness exit 2 (no count printed) rather than produce a countable
  <24 miss — the contract clause can neither pass nor fail visibly under P1. (Also flagged by
  CriticAxisFit32b.) Structural limit: a cooperating flock cannot be held on a nonexistent file.

### LOW

- **L1 — census leniency is sound only via composition.** `exited + waiters_on(ino) >= w`
  (c1-count.py:216-221) accepts writers that exited early; safety rests on the composed checks:
  hold check (:224-226), gate-line count/schema (:157-196 called at :243), rc equality (:241).
  A writer stalling its append into the hold-check-read→`LOCK_UN` window (:224-236) could
  escape undetected; sub-millisecond, not observed. No over-/double-count is possible (waiter
  entries vanish on exit even pre-reap; counter's own held LOCK_EX is an owner line, excluded
  by the `->` requirement — confirmed by the live probe).
- **L2 — C2 timeout/crash scores 0/120 as a miss, not harness error** (c2-count.py:76,
  266-269, 303): declared in the docstring, but an environment stall >600 s on a correct
  candidate would print a lower count against P2's no-lower-count clause. Measured base run
  5.4 s, so margin is wide.
- **L3 — receipt `gate` field stores the as-passed, possibly relative path**
  (c1-count.py:313, c2-count.py:311) while `gate_sha256` hashes the abspath — provenance nit.
- **L4 — c2 timeout kills only the direct child** (`subprocess.run`, c2-count.py:263-267)
  with no process-group kill, unlike c1's `start_new_session`+`killpg` (c1-count.py:116-119,
  123-133); an orphaned gate grandchild after a C2 timeout is conceivable but the base
  verify-chain spawns none.

## Verified-correct (no finding)

- `/proc/locks` parsing: format, `->` waiter detection, hex dev, decimal inode — live-validated
  (see Runs). [Caveat: this host's kernel only.]
- Deadlines bounded and absolute: c1-count.py:65-66, 146-154, 215-221, 241; c2-count.py:76.
- Solo reference run defines the writer exit code every writer must reproduce (c1:277-286,
  241); `ref_rc` recorded in the receipt (:313).
- Temp hygiene: per-trial `kill_all` in `finally` (c1:246-247), base `rmtree` in `finally`
  (c1:296-297); c2 `copytree(tmp, --keep)` before `rmtree(tmp)` (c2:296-302); all writes bounded.
- Seeds: `--seed` with fresh `urandom` default (c1:252-256, c2:237-241), recorded in receipts;
  fixture generation fully `random.Random(seed)`-deterministic.
- Label/condition == frozen predicates: `APPEND_SERIALIZED=%d/24` (c1:306, 315),
  `EXEMPT_AUDIT_MATCH=%d/120` (c2:304, 314), `holds = matched == TOTAL` (c1:299, c2:303),
  receipt `predicate_holds`; receipts carry `counter_sha256`/`gate_sha256`/`seed` as claims.md
  requires (verified in both run receipts).
- C2 fixture classes match the gate's real resolved semantics: heading needs `^#+\s+` + trimmed
  equality (research-gate.sh:1711-1715) ⇒ E9 exempt; quote is token-boundary `tok_span_at`
  (:1720) ⇒ E8 `x<anchor>` glue exempt; line is whole-line equality (:1724-1731) ⇒ E10 exempt;
  exempt arm lists exactly `unresolved|blocked-no-fetch|rejected|labelled-dead|not-applicable`
  (:1880-1882) ⇒ E5 unread. Output formats match LINE_RE/FIND_RE (:418, 1878, 1882); the base
  run parsed all 120 hops (84 matched + 36 listed misses).
- `CHOUSA_*` stripped from every gate child's env (c1:107-108, c2:262); writers run with
  `cwd=root` and DEVNULL stdio (c1:113-121).

## Residual risk & verification gaps

- LOCKS_RE validated on this host kernel only; kernels that truncate or reformat `/proc/locks`
  lines were not tested (none known).
- C1's census/hold composition was analyzed, not fault-injected: no run attempted a lockless
  writer that stalls past the hold check (L1 window).
- Peer control receipts cited [peer-reported] were not re-opened by me; paths recorded above.
- Neither counter can observe a candidate performing a network read for E3 URLs (contract says
  URLs stay unread); `.invalid` TLD makes any fetch fail, keeping the observable truth correct.
