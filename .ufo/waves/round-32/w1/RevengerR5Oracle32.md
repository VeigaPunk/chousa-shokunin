# RevengerR5Oracle32 — provenance of MutOracleC1 gate sha256 `bfc0b02b…` (routed defect R5)

Round-31 routed defect: `corpus/lessons/round-31-verifier-spotcheck.md:227-229` — "42 MutOracleC1
receipts bind gate `bfc0b02b`, which matches no committed revision and is described in no committed
text. Document what that oracle build was. This is harmless to P1: all 42 are 120 and none is counted."

## Verdict

`bfc0b02b83f554d134c6bb2c87610963a743f2e917a7d325611d844addf8c617` is the SHA-256 of the **v2
MutOracleC1 oracle script** — a 199-line scratch "Disclosed C1 feasibility reference, NOT a
candidate implementation" (bash shebang + `exec python3 - "$@" <<'PY'` heredoc). It was passed to
the frozen C1 counter as `--gate`, so the receipt schema honestly pinned the script under test in
`gate`/`gate_sha256`. It is **not** a `tools/research-gate.sh` build and was never intended to be.
R5's "harmless" verdict is confirmed, with one sharper fact: the exact bytes *are* committed, at
`.ufo/waves/round-31/controls/MutOracleC1/v2/oracle-c1.sh` (git blob `7fea55f8`), i.e. as wave
evidence, never at a gate path.

## Evidence

### The 42 receipts

- `grep -rln '"gate_sha256": "bfc0b02b' .ufo/waves/round-31/controls/MutOracleC1/v2/` → 43 files:
  21 primary receipts + 21 `.output.json` echoes + `probe-manifest.json` (21 entries). The 42 of R5
  = 21 primary + 21 output echoes.
- Primary receipts: `oracle-s{1,2,3}.json` and `restored-{no-strict-grammar,first-occurrence-only,
  substring-no-boundaries,range-start-only,mislocated-before-unsupported,off-by-one-lines}-s{1,2,3}.json`.
  Parsed all 21: `schema=chousa-r31-c1-receipt/v2`, `label=LINE_BINDING_MATCH=120/120`,
  `predicate_holds=true`, `gate_rc=1`, `gate=/fast/scratch/hyaku/chousa-r31/MutOracleC1/v2/work-c1.sh`,
  `counter_sha256=c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427`.
- Mutant (non-restored) receipts bind their own mutant-script hashes, not bfc0b02b:
  `probe-manifest.json` lists 1520a3c1…, 6ff3531d…, 817b3f2e…, a6aabaf4…, b7b6a472…, c5ff0f76… (3 each).
- `counter_sha256=c3aca35d…` verified live: `sha256sum corpus/evidence/round31/c1-count.py`
  → `c3aca35da30ee47edc3402daa559f43320e44a82d3a0143b5ea283ec8c49b427`. The counter pin is a real
  committed revision; only the *subject* pin is scratch.

### Scratch copy (read-only inspection of /fast/scratch/hyaku/chousa-r31/MutOracleC1/)

`sha256sum` output:
```
c1ebbf61…f078  oracle-c1.sh            (v1 oracle)
c1ebbf61…f078  work-c1.sh              (v1 mutation work target, restored)
bfc0b02b…c617  v2/oracle-c1.sh         (v2 oracle)
bfc0b02b…c617  v2/work-c1.sh           (v2 work target, restored)
```
Receipt `gate` fields point exactly at `…/v2/work-c1.sh` (v2) and `…/work-c1.sh` (v1). Archived copy
`.ufo/waves/round-31/controls/MutOracleC1/v2/oracle-c1.sh` hashes to the same `bfc0b02b…` — the
receipts' pin resolves to committed evidence bytes.

### Not any committed gate revision

Enumerated every historical `tools/research-gate.sh` blob
(`git log --all --format=%H -- tools/research-gate.sh` → `git rev-parse $r:tools/research-gate.sh`
→ `git cat-file blob | sha256sum`): 35 distinct content hashes, including
`3b5279eb0f312b41` (blob e1db3c4d, revs 1bd6e06/c17948a), `c23d7537e03482f2` (bb7d3676,
revs 115e371/6d0ae19), `ed3b9125702cc47d` (28ad13f1, revs 5dc105f/65d00cf), `0bc318b3e74ac0ad`
(e2df74eb, revs d27157b/7b82830/2353659 = tip). **None is bfc0b02b.** Whole-history blob scan
(`git rev-list --objects --all`, sha256 of all 3789 unique blobs): the only match is blob
`7fea55f858226ae5bcd8c2cf2c7105720eacdd2d` at the `.ufo/.../v2/oracle-c1.sh` evidence path.

### What the oracle build was (structure + diff vs committed gates)

- `work-c1.sh` lines 1–4: `#!/usr/bin/env bash` / "Disclosed C1 feasibility reference, NOT a
  candidate implementation." / "Byte-boundary semantics copied from research-gate.sh
  tok_left_ok/tok_right_ok." / `exec python3 - "$@" <<'PY'`.
- It re-implements **only** the `verify-claims` surface the C1 counter exercises: argparse
  `choices=['verify-claims']` (line 164); 13 finding codes, all `CLAIM_*`/`CONTRADICTION_*`
  (grep of script); the committed gate emits the full `CHAIN_*`/`VERIFY_ALL_*` set too.
- Copied semantics verified equivalent: `TOK_WS`/`TOK_PUNCT`/joiner `-'` classes and
  `tok_left_ok`/`tok_right_ok` (oracle lines 16–43 ↔ `tools/research-gate.sh:1287-1325`). The
  committed block (`sed -n '/^TOK_WS=/,/^tok_right_ok()/p' | sha256sum`) is byte-identical
  (`578bfbf432345df9`) across **all four** named gate revisions, so provenance "from" any of
  3b5279eb/c23d7537/ed3b9125/0bc318b3 is semantically indistinguishable.
- Deliberate upgrades beyond the gate's `tok_span_at` first-occurrence loop: enumerates ALL
  occurrences incl. overlaps (lines 46–55, "C1 quantifies over ALL occurrences"), strict JSON-string
  ASCII-decimal `line` grammar `[1-9][0-9]*(-[1-9][0-9]*)?` (lines 58–66), both-endpoint range
  binding (146–149), absent-span precedence (143–144), marker-region contradiction (152–158),
  source-refusal classes mirroring the gate's CLAIM_SOURCE_* chokepoint (78–121).
- Diff vs committed gates is total, not a patch: `diff tools/research-gate.sh v2/work-c1.sh` →
  7169 diff lines between a 6982-line bash gate and a 199-line Python oracle; every byte differs
  structurally. It could never be confused with or swapped for a production gate.

### From which revision / which diff

- **v1 oracle** (`c1ebbf61…`, archived `.ufo/.../MutOracleC1/oracle-c1.sh`): scratch mtimes
  01:22–01:25; v1 receipts pin `counter_sha256=154e09e7f73bebaf…` (committed c1-count.py at 4
  revisions; superseded by `c3aca35d` at 42). First v1 receipt `utc=2026-10-23T04:23:38Z`.
- **v1→v2 diff** is exactly one line, archived at
  `.ufo/waves/round-31/controls/MutOracleC1/v2/oracle-v1-to-v2.diff` and reproduced live by
  `diff work-c1.sh v2/work-c1.sh`:
  `- print('FINDING %s severity=warn surface=claims id=%s' % (finding, cid))`
  `+ print('FINDING %s severity=warn surface=claims obs=id=%s at=%s' % (finding, cid, at))`
  — the `obs=` prefix aligns with the committed gate's `emit_finding` format
  (`research-gate.sh:415-417,1572`); MutOracleC1.md calls this the "finding-emitter format" change
  under frozen design `8070f92b`.
- Seat report: `.ufo/waves/round-31/controls/MutOracleC1.md` — "MutOracleC1 — C1 feasibility and
  sensitivity. Disclosed Python feasibility reference only; not a candidate." Its v2 section
  names `bfc0b02b83f5…` as the "pristine/before/restored/final SHA-256" of the oracle.

### Why harmless

1. Controls only: every bfc0b02b-bound receipt is a control/feasibility receipt (oracle 3×,
   restored 18×), all 120/120 — none is a P1/P2 candidate scoring run; nothing in the wave counted
   it toward a claim.
2. Honest provenance: `gate` names the scratch path; `gate_sha256` pins the real bytes, which are
   committed verbatim at the `.ufo` evidence path — resolvable, not dangling.
3. Valid counter pin: `counter_sha256=c3aca35d…` = committed `corpus/evidence/round31/c1-count.py`.
4. No production collision: 199-line Python single-mode script vs 6982-line bash gate; byte-disjoint
   from all 35 historical gate blobs.
5. The restored-* receipts are the point of the exercise: after each mutant was applied and
   reverted, the oracle scored 120/120 again on the identical bytes — the R5 anomaly is just an
   unnamed hash, now named.

## Commands (representative)

```
grep -rln bfc0b02b .ufo/waves/round-31/                     # 44 files, all under MutOracleC1/v2 (+ tsv/md refs)
sha256sum /fast/scratch/hyaku/chousa-r31/MutOracleC1/v2/{oracle-c1,work-c1}.sh   # both = bfc0b02b…
diff /fast/scratch/hyaku/chousa-r31/MutOracleC1/work-c1.sh \
     /fast/scratch/hyaku/chousa-r31/MutOracleC1/v2/work-c1.sh                    # 1 line, FINDING format
git log --all --format=%H -- tools/research-gate.sh | … | sha256sum              # 35 blob shas, no bfc0b02b
git rev-list --objects --all | sha256 per blob                                   # only match: .ufo/.../v2/oracle-c1.sh
```

## Limits / inference

- [INFERENCE] The oracle was written against the round-31 C1-era gate text (scratch mtime 01:22
  precedes the C1-repair commit c17948a 04:43:27Z; v1 receipt 04:23:38Z). Whether it was copied from
  a committed or in-flight working copy is unobservable — immaterial, since the copied tok block is
  byte-identical across all four committed revisions.
- Scratch `/fast` is perishable; the receipts' hash resolves permanently via the committed archived
  copy `.ufo/waves/round-31/controls/MutOracleC1/v2/oracle-c1.sh`.
- No installs, no network, no mutations outside this report file; `/fast` inspected read-only
  (`/usr/bin/du` + `sha256sum` only). `df -h /fast`: 72% used, 233G avail.
