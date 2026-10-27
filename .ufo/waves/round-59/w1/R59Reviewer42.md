# R59Reviewer42 — adversarial review of round59 claim design, controls, and positive verdict-path calibration

Scope: calibration axis. Assessed the round59 claim/control package (the round-58 frozen counters reused as the round59 positive-path calibration surface), the frozen-claims prerequisite, source grounding of the new offline S101 evidence, and the report contract. All dynamic probes ran on exact frozen lane bytes in dedicated scratch (`/fast/scratch/hyaku/chousa-r59/R59Reviewer42/`, removed before yield; receipts embedded below; reproduction commands given). No lane file other than this report was written; no external fetch; no installs.

## Findings

### F1 — CRITICAL (calibration): the frozen C1 counter's PASS verdict is forgeable by an output-echo poison builder

**Claim attacked:** the round58 frozen counter `corpus/evidence/round58/c1-count.py` (sha256 `65da18bbcb03581ca98354d90049215ed3cab3bfd3e41d483908dc1e1c703d3f`, byte-verified before probing) distinguishes conforming from non-conforming builders via its refusal legs.

**Attack:** poison builder = pinned r55 builder (sha256 `1ed2650a…`, claims pin) + a preflight that refuses every hazard leg with rc=2, names **no** required reason class, and prints `build-spans: refused: poison=PASS (<why>)` — except SYMLINK_OUT, where it **writes a marker through the symlink into the real target first**, then refuses. Safe legs (EMPTY_OK, REBUILD_OK, HELDOUT_OK, ESCAPE_ENTRY) are passed honestly; HELDOUT_OK passes for real (capture S101-derived spans, offsets per r55 convention).

**Result — frozen counter, unmodified bytes (probe A2):**

```
EMPTY_OK=pass / REBUILD_OK=pass / ESCAPE_ENTRY=pass(refused) / HELDOUT_OK=pass
FOREIGN=fail(reason-unnamed:'build-spans: refused: poison=PASS (unknown span present)\n…')
SYMLINK_OUT=fail(rc=2, reason ['SYMLINK'] absent in 'build-spans: refused: poison=PASS (output target is a link)\n…')(target-dir-written!)
SYMLINK_CACHE=fail(rc=2, reason ['SYMLINK', 'REGTYPE', 'NOT_REGULAR'] absent in '…poison=PASS (unreadable cache entry)…')
FIFO_TXT=fail(rc=2, …) DEVZERO_TXT=fail(rc=2, …) FAT_RAW=fail(rc=2, …) MANY_QUOTES=fail(rc=2, …)
BEFORE_FOREIGN=deleted / CONTROL_REFUSEALL=denied / CONTROL_build-spans-r55=denied / DENIED=2/2
SUMMARY OK=4/4 REFUSE=7/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS          ← counter exit 0
```

All seven graded refusal lines literally read `…=fail(…)`; the counter scored them 7/7 because the verdict token is matched as a **substring over the whole leg line**, and the FAIL branches embed raw builder output: `expect_refuse` line 156 (`…absent in {err[:160]!r}`; `err` = stderr+stdout, line 152) and the FOREIGN unnamed-reason branch (~:223-226, `err[:200]`). The hazard-accepting write through `out-link` is visible as `"(target-dir-written!)"` on the line but is **ungraded**. A builder that accepts a hazard and names no reason reaches `C1=PASS`, exit 0, with a cosmetically perfect `REFUSE=7/7` summary. This inverts the round-58 finding (LOG.md:1912): the positive path is not only unreachable for sound builders — it is reachable for unsound ones.

**Reproduction:** r55-based builder with the preflight patch (sha256 `4dd3527ce9c24437bcb5586132db0995a52f28111130048a840bdf5a0f8c23c2`, scratch copy `poison-upper.py`, lane `tools/capture-text.py` copied beside it for its `TOOLS`-relative import) run as
`python3 -B corpus/evidence/round58/c1-count.py --builder <poison-upper.py> --controls corpus/evidence/round58/controls --work <scratch>/runA`.

**Falsifier:** any counter claimed calibrated must print `C1=FAIL` for this exact builder. If it prints PASS, the verdict path is forgeable.

### F2 — CRITICAL (calibration of the round59 fix): comparator/token normalization does NOT close the forge

Round59 peers measured the pass-side fix as a token normalization (`R59Executor15.md:58-97`: `:391` and `:399` `"=PASS"`→`"=pass"`, scratch counter copy sha `21dae5d3…`, conforming builder → `C1=PASS` exit 0, seeds 1–30). **That fix class is still forgeable**: the echo adapts to whatever token the comparator wants. Probe B2 — comparator-only fix (`:391` `"=PASS"`→`"=pass"`; my replica sha256 `464befe69c34b319273a55af5236b04a31c53bb8fce892c5718973d5d353e64f`) against the lowercase-echo poison (`poison-lower.py`, sha256 `814090f44e1a1eacab6ae3c9a9b8f00c9b700062bdf0a8761b3fd9801adccbd1`):

```
SUMMARY OK=4/4 REFUSE=0/7 BEFORE_FOREIGN=deleted DENIED=2/2
C1=PASS          ← counter exit 0
```

(The cosmetic SUMMARY `REFUSE=0/7` shows the verdict input is `:391`, not the printed tally.) Probe A2 already covers the emitter-side variant too: an uppercase comparator (`=PASS`) is beaten by the uppercase echo on the frozen bytes. A case-insensitive comparator is beaten by either echo.

**Smallest sound fix (recommendation, no edits made):** (a) parse the leg status structurally — e.g. `re.match(r"^\S+=(PASS|FAIL)\b", line)` — never substring-search a line that embeds child output; and (b) stop embedding raw builder stderr in graded lines (emit a coded reason token instead). Either alone kills this vector; together they are robust. **A round59 positive-path calibration claim is incomplete without a poison-echo control:** the fixed counter must be shown printing `C1=FAIL` for probes of exactly this shape (honest safe legs + reason-less refusals + token echo + accepted SYMLINK_OUT hazard). Honest-builder PASS plus do-nothing-denied controls does not establish calibration — both of my probes satisfy the entire current control set.

### F3 — HIGH (controls): "control denied" is scored from a counter crash, not a refusal

With `REFUSEALL.py` as builder-under-test, the frozen counter crashes at the FOREIGN fixture write: line 211-212 `foreign = out / "spans" / "S777-1.txt"; foreign.write_bytes(...)` runs unguarded after EMPTY_OK's builder refused and never created `out-empty/spans/`. Probe C (exact frozen bytes): `FileNotFoundError: …/runC/out-empty/spans/S777-1.txt`, **no `C1=` verdict line**, exit 1; the control loop (line 377) scores the missing verdict as `denied`. So `CONTROL_*=`denied`` and `DENIED=x/x` receipts cannot distinguish "cleanly refused" from "counter crashed" — the do-nothing control requirement is satisfied vacuously. Matches `R59Executor15.md:154` and `R59Critic59.md`; reproduced here on frozen bytes. Falsifier: a counter that tolerates a missing output tree and emits a structured verdict for early refusers.

### F4 — HIGH (claim design / scope contract): the wave was dispatched against frozen claims that do not exist

`w1-dispatch.json` written 15:12:11 binds every seat to "Frozen claims: …/round59/claims.md; read before work" (also `w1-spec.json:10`). That path was absent at dispatch, absent at the earlier in-wave check (15:15 incarnation report), and still absent at review close (~15:47): `corpus/evidence/round59/` contains only `census-start.txt`, `controls/c1-before.txt` (15:14:30), and `s101-open.txt` (15:26:09). Round-58 precedent froze claims and before-controls **before** dispatch (commit `9e73a03 "round-58: freeze claims and before controls"` precedes the w1 dispatch). Consequently every round59 seat verdict is unmapped to claim text, and the round's only control receipt is provenance-unattributable: `round59/controls/c1-before.txt` is byte-identical to `round58/controls/c1-before.txt` (`cmp` clean) — indistinguishable between a deterministic re-run and a copy, and it embeds no run metadata (command, seed, work root, counter sha, timestamp), scoring `DENIED=0/0` (controls not exercised). **Falsifier:** land the frozen claims bytes at the named path and replace the receipt with one carrying embedded provenance; both flip this finding.

### F5 — MEDIUM (C2 design): the two frozen counters impose contradictory offset conventions on the same pinned builder

For the same pinned builder bytes (`1ed2650a…`), `c1-count.py` `expect_ok` requires manifest `offset == max(0, find(quote)-80)` (the r55 convention, `build-spans-r55.py:142,149`), while `c2-count.py:101` requires `offset == occurrences[0]` (the raw occurrence): `if url!=URL or digest!=RAW_SHA or len(occurrences)!=1 or occurrences[0]!=off: errors.append('CAPTURE_BIND:'+sid)`. One artifact cannot satisfy both; LOG.md:1913 records both orientations failing (builder spans → `CAPTURE_BOUND=0/12`, `REBUILD=MATCH`; occurrence offsets → `CAPTURE_BOUND=12/12`, `REBUILD=FAIL`). Any round59 C2 claim must pin the corrected convention **on one named side** (counter or builder) in the frozen text, else the unreachable-positive trap recurs. Positive note: `c2-count.py`'s verdict is composed of structured error tokens only — no raw child output is embedded — so it has no F1-style echo surface.

### F6 — LOW (source grounding): the new offline S101 opening lands without a provenance header

`corpus/evidence/round59/s101-open.txt` (sha256 `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867`, 47,356 bytes, mtime 15:26:09) is the bare defined form of the CAJ 检索与评价数据规范 (修订本) capture — it carries no `source:`/`verified-at:`/raw-digest header, unlike the provenance trio the C2 counter itself demands of knowledge entries (`c2-count.py` PROVENANCE_TRIO check). Grounding is recoverable — the raw pin (`6063a3af…`) and capture-text pin (`2c0140bc…`) in `c2-count.py:15-17` re-derive the form — but the freeze should state the derivation command and this file's digest, so the offline-reconnaissance leg of the round is byte-auditable. No external fetch occurred; the L0 fetch-scope question (fleet `8d77e6c1`, `/home/vgpnk/Projects/shokunin/.ufo/l0-questions.md:121`) remains open and was respected by this seat (no live fetches).

## Residual risk and verification gaps

- The honest positive path (fixed counter + conforming builder → PASS, seed-robust) is cited from sibling receipts (`R59Executor15.md:75-97`), not re-run by this seat; my dynamic contribution is probes A2/B2/C on exact frozen bytes (counter sha verified `65da18bb…` before use).
- Poison probes ran at default seed 7 only; the mechanism (echo riding the FAIL branch's embedded `err`) is fixture-independent, but a fixed counter should be poison-tested across the same seed sweep used for its honest path.
- Emitter-side and case-insensitive fix variants were refuted statically/by-probe-A2, not by a separately patched replica.
- `round59/claims.md` may land after review close; F4 is time-stamped to the last check and self-falsifying on arrival of the artifact.
- Scratch `runA/runB/runC` outputs and probe builders were removed before yield per lane bounds; the receipts above are verbatim, and every probe is reproducible from the stated commands + sha256s.

## Report trailer

Report: `.ufo/waves/round-59/w1/R59Reviewer42.md`
