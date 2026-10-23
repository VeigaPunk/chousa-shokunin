# MutC2AttrKey — is the per-record attribution key in `tools/argv-witness.py` load-bearing?

Round 36, attempt 2, wave 1. Lane chousa-shokunin. All probes below ran 2026-10-23.
Probe scope: C2's per-record attribution key only. No C1 run, no lane edit, no commit.

## Verdicts (explicit)

- **Mutant A (per-record attribution collapsed to a global count): KILLED — the per-record key IS load-bearing** for P2's separation arm. `WITNESS_PER_RECORD` drops 5/5 → 0/5 on both seeds (exit 1); every swap variant flips `witness=fail` → `witness=pass` at `attrib=9`.
- **Mutant B (attribution requires only the first 64 bytes of the span): SURVIVED — the exact-span strength is NOT load-bearing.** `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass`, `predicate_holds=true`, exit 0, on both seeds, with attribution record-sets byte-identical to the pristine witness. A witness that satisfies only a 64-byte prefix still passes P2.

Mutant B is the round's interesting result: it is a witness bypass that passes P2, but it is a *strength* relaxation, not a blind-to-attribution collapse (mutant A proves the counter sees the channel). Section "MEETS analysis" says exactly what it would admit.

## Pins (scored gate and tool identity)

| object | sha256 | note |
|---|---|---|
| `tools/research-gate.sh` (scored gate) | `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8` | equals the contract's landed-gate pin; recorded as `gate_sha256` in every scored receipt |
| `tools/argv-witness.py` (lane witness) | `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e` | pristine control bytes; unchanged before/after |
| `corpus/evidence/round36/c2-count.py` at HEAD / at my first read | `3c699aab0614fff78f88d1b8570166439014a360ee378c0a143bf204a96e4362` | read-only; used for the 18:26 runs |
| `corpus/evidence/round36/c2-count.py` working tree (changed under me at 18:29:10) | `67c33fe411b055dbd77179a4bb11d8ecf29eb7a9038069f91fd033ccb0f9c97f` | docstring-only diff; AST-equal to HEAD ignoring docstrings; snapshotted as `art/c2-count-current.py` and used for the re-pinned runs |
| `.ufo/waves/round-36/controls/base-gate-r36.sh` | `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` | C1 pre-round control; not used by this C2 probe |
| lane revision | `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` | `git rev-parse HEAD` = `git rev-parse master` |

`stderr` note: every receipt's `gate_sha256` is the landed gate; variant gates are patched by the counter from those same bytes and are hashed per variant inside each receipt.

## Scratch and mutant construction

Scratch root `/tmp/hyaku/chousa-r36/w1/MutC2AttrKey` (never the lane). Three byte-identical copies of the lane witness were made, one kept pristine as the control, two patched:

```
cp tools/argv-witness.py /tmp/hyaku/chousa-r36/w1/MutC2AttrKey/art/wit-pristine.py
cp tools/argv-witness.py /tmp/hyaku/chousa-r36/w1/MutC2AttrKey/art/wit-global.py
cp tools/argv-witness.py /tmp/hyaku/chousa-r36/w1/MutC2AttrKey/art/wit-prefix.py
```

All three hashed `e6832e0b9cbb…` at copy time. Only `attribute()` was touched; `matcher_patterns`, decoding, output scoring and `main` are byte-identical, so output verdicts cannot change — any label change is attributable to the key alone.

### Mutant A — global count (`wit-global.py`, sha256 `7fb47738def10219bf5ab378077be92e491aa47601528b418a8399ed83768b84`)

```diff
 def attribute(calls, truth):
-    """-> {id: 'direct'|'chunk'}: every record whose own span/chunk was queried."""
-    got = {}
+    """MUTANT A (global count): any matcher argv attributes every record."""
     pats = [d for d in (decode_matcher_pattern(p) for p in matcher_patterns(calls)) if d is not None]
-    for cid, meta in truth.items():
-        span = meta["span"].encode("utf-8", "surrogateescape")
-        for kind, decoded in pats:
-            if kind == "direct" and decoded == span:
-                got[cid] = "direct"
-                break
-            if kind == "chunk" and decoded == span[:4096]:
-                got[cid] = "chunk"
-                break
-    return got
+    if not pats:
+        return {}
+    return {cid: "global" for cid in truth}
```

Defect this encodes: an engine that makes *one* matcher call on any argv channel is credited with querying *every* record — i.e. the attribution channel is reduced from per-record to a global "did any grep call happen" bit.

### Mutant B — 64-byte prefix (`wit-prefix.py`, sha256 `ed0f0caa8e9e9378c8dca62d6784c1e7ad44a61404f2b160bcbaa8508dbe769f`)

```diff
 def attribute(calls, truth):
-    """-> {id: 'direct'|'chunk'}: every record whose own span/chunk was queried."""
+    """MUTANT B (prefix): only the first 64 bytes of a span need prefix a queried argv."""
     got = {}
     pats = [d for d in (decode_matcher_pattern(p) for p in matcher_patterns(calls)) if d is not None]
     for cid, meta in truth.items():
         span = meta["span"].encode("utf-8", "surrogateescape")
+        head = span[:64]
         for kind, decoded in pats:
-            if kind == "direct" and decoded == span:
-                got[cid] = "direct"
-                break
-            if kind == "chunk" and decoded == span[:4096]:
-                got[cid] = "chunk"
+            if decoded.startswith(head):
+                got[cid] = "prefix64"
                 break
     return got
```

Defect this encodes: the record key shrinks from "own span exactly / own 4096-byte chunk" to "same first 64 bytes". A matcher engine that queries only a 64-byte prefix of each long span is credited as having queried the record.

## Counter control — pristine witness (baseline sane)

Command (per run; driven in a `for` loop over `wit` ∈ {pristine,global,prefix} and seeds 36341, 36351):

```
C2_TMP=$d TMPDIR=$d timeout 900 python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py \
  --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh \
  --witness /tmp/hyaku/chousa-r36/w1/MutC2AttrKey/art/wit-pristine.py \
  --seed 36341 --receipt /tmp/hyaku/chousa-r36/w1/MutC2AttrKey/art/rec-pristine-s36341.json
```

Exit 0 on both seeds. Deciding line (seed 36341; seed 36351 identical):

```
WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass
  V1-python-exact        output=9/9 witness=fail attrib=1
  V2-env-keyed           output=9/9 witness=fail attrib=1
  V3-witness-forge       output=9/9 witness=fail attrib=1
  V4-one-call-for-show   output=9/9 witness=fail attrib=2
  V5-body-replaced       output=9/9 witness=fail attrib=1
  V6-renamed-matcher     output=9/9 witness=pass attrib=9
```

Landed run: `witness=pass`, `unattributed=[]`, `matcher_calls=11`, 9/9 records attributed. The pristine witness reproduces the frozen P2 label exactly; the baseline is sane, so any mutant delta is real.

## Mutant A results — KILLED

Same command with `--witness .../wit-global.py`, seeds 36341 and 36351, exit **1** on both. Deciding lines (both seeds):

```
WITNESS_PER_RECORD=0/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass
  V1-python-exact        output=9/9 witness=pass attrib=9
  V2-env-keyed           output=9/9 witness=pass attrib=9
  V3-witness-forge       output=9/9 witness=pass attrib=9
  V4-one-call-for-show   output=9/9 witness=pass attrib=9
  V5-body-replaced       output=9/9 witness=pass attrib=9
  V6-renamed-matcher     output=9/9 witness=pass attrib=9
```

Receipt detail (seed 36341, `rec-global-s36341.json`): landed `attrib_n=9`, `matcher_calls=11`; each swap variant `matcher_calls` unchanged at 2/2/2/3/2 (the call channel is untouched), but `attrib_n` jumps from 1/1/1/2/1 to 9/9/9/9/9, so all five `witness=fail` become `witness=pass` and separation collapses 5 → 0.

Read honestly: a global count still satisfies `LANDED_ATTRIB=pass` and `RENAMED=pass` (a single matcher call attributes all nine landed records). The arm that kills this mutant is **separation**. So `LANDED_ATTRIB=pass` alone is not evidence of per-record attribution; the separation count is what carries the key.

## Mutant B results — SURVIVED

Same command with `--witness .../wit-prefix.py`, seeds 36341 and 36351, exit **0** on both. Deciding lines are indistinguishable from pristine:

```
WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass
  V1-python-exact        output=9/9 witness=fail attrib=1
  V2-env-keyed           output=9/9 witness=fail attrib=1
  V3-witness-forge       output=9/9 witness=fail attrib=1
  V4-one-call-for-show   output=9/9 witness=fail attrib=2
  V5-body-replaced       output=9/9 witness=fail attrib=1
  V6-renamed-matcher     output=9/9 witness=pass attrib=9
```

Machine comparison (`art/mutant-summary.json`, `pristine_vs_prefix`): attribution record-sets are **equal** for the landed run and all six variants on both seeds (`landed_sets_equal: true`, every `variant_sets_equal: true`). The mutation changes the kind label (`direct`/`chunk` → `prefix64`) and nothing observable.

Variant admission table (attributed-record counts out of 9; seed 36341; seed 36351 identical in shape):

| variant | calls | pristine | A (global) | B (prefix64) | A admits? | B admits? |
|---|---|---|---|---|---|---|
| V1-python-exact | 2 | 1 | 9 | 1 | yes (falsely) | no extra |
| V2-env-keyed | 2 | 1 | 9 | 1 | yes (falsely) | no extra |
| V3-witness-forge | 2 | 1 | 9 | 1 | yes (falsely) | no extra |
| V4-one-call-for-show | 3 | 2 | 9 | 2 | yes (falsely) | no extra |
| V5-body-replaced | 2 | 1 | 9 | 1 | yes (falsely) | no extra |
| V6-renamed-matcher | 11 | 9 | 9 | 9 | pass (expected) | pass (expected) |
| landed | 11 | 9 | 9 | 9 | pass (expected) | pass (expected) |

Why B survives: the fixture spans are random per record, so no two records share their first 64 bytes; every call that *did* query a record also satisfies the prefix test, and no call that missed a record happens to share its head. The relaxation is invisible on these seeds, not inert in principle.

### Constructive proof that B's key is weaker (unit probe, no engine built)

Direct call into both `attribute()` implementations in scratch, one synthetic matcher argv whose decoded pattern equals `r1`'s span only (64-byte shared head `P`, then `XXXX` vs `YYYY` for the never-queried `r2`), args `-a -z -b -o -P -- <hex pattern>`:

```
synthetic: one matcher argv, pattern == r1's span only; r2 never queried
  pristine attribute -> [('r1', 'direct')]
  prefix64 attribute -> [('r1', 'prefix64'), ('r2', 'prefix64')]
```

So B attributes a record that was never queried whenever a queried span shares its 64-byte head — the defect is real, the battery just cannot reach it.

## MEETS analysis (what a surviving pass would buy an engine)

The claim's own words (24 words, `corpus/evidence/round36/claims.md`, accessed 2026-10-23): "every record's own span (or its first 4096 bytes for a dead-zone span) must appear in a `-a -z -b -o -P` matcher argv". Mutant B keeps P2 green while requiring only 64 bytes.

Consequence, stated with its status: a **prefix-query call-for-show engine** — grep called once per long record with only `span[:64]`, answer computed by exact python search — would be attributed 9/9 by mutant B and only 1/9 (short spans) by the pristine witness. **[INFERENCE]** I did not build or run this V7 engine; the inference rests on the unit probe above plus the counter's variant mechanics (V1 already shows the python-exact engine fails pristine on the long records while `output_full` stays true). If it behaved as inferred, it would be output-equivalent, separated by the landed witness, and admitted by the prefix witness — i.e. a P2-passing bypass that the 5-variant battery cannot see. The concrete frontier move is a V7 variant of exactly that shape: it should kill mutant B and leave pristine at 5/5. Not added here — a bug/battery gap is a finding, not permission to change the contract.

Also note the brief's heuristic ("A mutant that still scores 5/5 means the counter does not measure per-record attribution", 15 words, accessed 2026-10-23) is too coarse for B: A's 0/5 proves the counter does measure the per-record channel; B shows the counter does not measure the *strength of the record key*.

## Restoration evidence

| file | before | after | restored |
|---|---|---|---|
| lane `tools/argv-witness.py` | `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e` | `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e` | never modified |
| scratch `wit-pristine.py` | `e6832e0b9cbb…` | `e6832e0b9cbb…` | byte-identical to lane |
| scratch `wit-global.py` (scored) | `7fb47738def1…` | `7fb47738def1…` | matches receipt `witness_sha256` |
| scratch `wit-prefix.py` (scored) | `ed0f0caa8e9e…` | `ed0f0caa8e9e…` | matches receipt `witness_sha256` |

Lane `git status --porcelain` showed only the pre-existing untracked round-36 wave files (`gen-w1-spec.py`, `w1-briefs/`, `w1/`, `corpus/evidence/round36/__pycache__/`, …); no tracked file modified, no git/jj write command run. All scratch writes were under `/tmp/hyaku/chousa-r36/w1/MutC2AttrKey`; no write to `/fast`; no network; no `pacman`.

## Commands run (verbatim, with exit codes and the deciding line)

1. `sha256sum tools/research-gate.sh tools/argv-witness.py corpus/evidence/round36/c2-count.py .ufo/waves/round-36/controls/base-gate-r36.sh && git rev-parse master && git rev-parse HEAD && git status --porcelain | head -20` — exit 0. Deciding lines: gate `a7d3922c768a…`, witness `e6832e0b9cbb…`, counter `3c699aab0614…`, control `a4768851…`, both revs `700bd5fc…`.
2. `cp tools/argv-witness.py /tmp/hyaku/chousa-r36/w1/MutC2AttrKey/art/wit-{pristine,global,prefix}.py` — exit 0; each `sha256sum` = `e6832e0b9cbb…`.
3. `diff -u wit-pristine.py wit-global.py > diff-global.patch` — exit 1 (files differ, expected); patch size 931 B.
4. `diff -u wit-pristine.py wit-prefix.py > diff-prefix.patch || echo "diff_rc=$?"` — printed `diff_rc=1`; patch size 955 B.
5. `python3 -m py_compile wit-pristine.py wit-global.py wit-prefix.py` — exit 0 (`compile_rc=0`).
6. Pristine control, loop over seeds:
   `rc=0; C2_TMP=$W/tmp/pristine-$s TMPDIR=$W/tmp/pristine-$s timeout 900 python3 $L/corpus/evidence/round36/c2-count.py --gate $L/tools/research-gate.sh --witness $W/art/wit-pristine.py --seed $s --receipt $W/art/rec-pristine-s$s.json || rc=$?` for s ∈ {36341, 36351} — exit **0**, **0**; deciding line `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` both seeds.
7. Mutant A, same form with `--witness $W/art/wit-global.py` — exit **1**, **1**; deciding line `WITNESS_PER_RECORD=0/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` both seeds, every V1–V5 `witness=pass attrib=9`.
8. Mutant B, same form with `--witness $W/art/wit-prefix.py` — exit **0**, **0**; deciding line `WITNESS_PER_RECORD=5/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=pass RENAMED=pass` both seeds, variant table identical to step 6.
9. Unit probe (Python, imported both scratch modules by path, one synthetic matcher argv) — exit 0; deciding output `pristine attribute -> [('r1', 'direct')]` / `prefix64 attribute -> [('r1', 'prefix64'), ('r2', 'prefix64')]`.
10. `sha256sum` of lane pins after all runs — witness `e6832e0b9cbb…`, gate `a7d3922c768a…`, counter `3c699aab0614…` (at that moment; the counter was later changed under me — see "Concurrent lane modification").

11. `cp corpus/evidence/round36/c2-count.py /tmp/hyaku/chousa-r36/w1/MutC2AttrKey/art/c2-count-current.py` (Python `shutil.copy2` inside the eval cell) — exit 0; `sha256sum` = `67c33fe411b055dbd77179a4bb11d8ecf29eb7a9038069f91fd033ccb0f9c97f`.
12. AST equality of HEAD vs working-tree counter, docstrings stripped: `ast.parse` → drop leading `Constant` docstrings on Module/FunctionDef/ClassDef → `ast.dump` compare — exits 0; deciding output `ast_equal_ignoring_docstrings True 36991 36991`.
13. Re-pinned re-runs against the snapshot counter, seed 36341, one per witness:
    `rc=0; C2_TMP=$W/tmp/re-$wit-36341 TMPDIR=$W/tmp/re-$wit-36341 timeout 900 python3 $W/art/c2-count-current.py --gate $L/tools/research-gate.sh --witness $W/art/wit-$wit.py --seed 36341 --receipt $W/art/rec-$wit-s36341-c67c.json || rc=$?` for wit ∈ {pristine, global, prefix} — exits **0, 1, 0**; deciding lines identical to steps 6–8 (`5/5 …`, `0/5 …` with all `attrib=9`, `5/5 …`).

Note on seeds: the assigned seeds 36341 and 36351 were used. 36341 is in the wave's fresh-seed list; 36351 is fresh relative to the construction seeds 36001/36011 and the round-36 wave seeds and is the brief's second seed.

## Files opened (access date 2026-10-23)

- `.ufo/waves/round-36/w1-briefs/MutC2AttrKey.md` (validated brief)
- `corpus/evidence/round36/claims.md` (frozen claim design; C2, P2, kill rule, limits quoted)
- `corpus/evidence/round36/c2-count.py` (counter: main, run_witness, builders)
- `corpus/evidence/round36/c1-count.py` (header/docstring only; not exercised)
- `tools/argv-witness.py` (full, including `attribute`, `matcher_patterns`, `decode_*`, `main`)
- `tools/mechanism-witness.py` (header/docstring; the round-35 witness this replaces)
- `.ufo/waves/round-36/measure/*.json` (listed; `elapsed_s` read only)
- scratch copies `wit-pristine.py`, `wit-global.py`, `wit-prefix.py` and their diffs

## Artifacts (lane paths under `.ufo/waves/round-36/w1/MutC2AttrKey/`)

| path (lane) | sha256 | size |
|---|---|---|
| `art/wit-pristine.py` | `e6832e0b9cbbdfae9da823528cc0a6218a6af7d8ed7e5864378713df2e19107e` | 15480 |
| `art/wit-global.py` (Mutant A) | `7fb47738def10219bf5ab378077be92e491aa47601528b418a8399ed83768b84` | 15163 |
| `art/wit-prefix.py` (Mutant B) | `ed0f0caa8e9e9378c8dca62d6784c1e7ad44a61404f2b160bcbaa8508dbe769f` | 15386 |
| `art/diff-global.patch` | `c43f062a87e02437c760c9655d8c0a4dc2165391cf84c25c9038aec8d4b11a7c` | 931 |
| `art/diff-prefix.patch` | `6187a1aff20952490750f9bc682ea116177d107a2368563a94e27a3478b93a8a` | 955 |
| `art/rec-pristine-s36341.json` | `f1d384605815ee046ff6987ea3f0a4d4a4dfb9b6abf9031f83a0108461b707dd` | 4122 |
| `art/rec-pristine-s36351.json` | `9eb265131cd3613224dd0275a92e13b9d06bba2332080ad5d9155bd8ade2d05d` | 4374 |
| `art/rec-global-s36341.json` | `64ecd00797353d90f73889c4c8ce915aabe7c7fb3d2e8a0cd20fa28f0b107a54` | 4513 |
| `art/rec-global-s36351.json` | `8702486f7fbd0ed0be8efb78fae6c3362ae2486c9c8de217609c3d738bc9507d` | 4765 |
| `art/rec-prefix-s36341.json` | `8cd16251ebd380d5b81951ff03fe54f6fb645667c880f124e4c0ef21ad6875be` | 4185 |
| `art/rec-prefix-s36351.json` | `d07e3fa2d2e2075cff356b20aa930bbb61f16405b82e04480ab31a2e5211d79f` | 4437 |
| `art/mutant-summary.json` | `0d1e04caaedd9fd5734860183ec0ddf533cfeb23ac4cf04a080622aec7eb4414` | 12672 |
| `art/c2-count-current.py` (counter snapshot) | `67c33fe411b055dbd77179a4bb11d8ecf29eb7a9038069f91fd033ccb0f9c97f` | 13283 |
| `art/rec-pristine-s36341-c67c.json` | `2b6ddda901fce9f31ef3ad0ec131f4fe80ec64530f3dcbad25e048e568f2d1c4` | 4122 |
| `art/rec-global-s36341-c67c.json` | `4e8d97ddf6baa70d527fe8284705f0cea29ea079fade19a37e9778e1cd560d9d` | 4513 |
| `art/rec-prefix-s36341-c67c.json` | `0bce8e0ef31608c7c7d55fc3224ca82799bf3d221093be936502bdd501e3d22b` | 4185 |

Every receipt records `gate_sha256 = a7d3922c768a…`, its witness's `witness_sha256`, `seed`, and per-variant `attribution`/`unattributed`/`matcher_calls`/`output_full`.

## Concurrent lane modification (observed, not mine)

At my first hash check (18:25) the lane tree was clean apart from untracked round-36 wave files; the counter hashed `3c699aab…` (= HEAD). When I re-hashed after the probes, `git status --porcelain` showed **five modified tracked files** — `.gitignore`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/SOURCES.md`, `corpus/evidence/round36/c2-count.py` — and `c2-count.py` had mtime `18:29:10`, i.e. it changed *during* this wave. I made no lane write and ran no git/jj write command; every run of mine wrote only under `/tmp/hyaku/chousa-r36/w1/MutC2AttrKey` and the receipts' `--json` paths.

Response taken, so the receipts cannot be misread:

- The `c2-count.py` diff is docstring-only (4+/2- inside the module docstring, hunk `@@ -35,8 +35,10 @@`). Verified behaviorally: `ast.dump` of HEAD vs working tree with docstrings stripped is **identical** (`ast_equal_ignoring_docstrings True`, both dumps 36991 chars). No scoring logic changed.
- The live bytes were snapshotted to `art/c2-count-current.py` (`67c33fe4…`) and all three witnesses were re-scored at seed 36341 against that snapshot: same labels, same exit codes (pristine 5/5 exit 0; A 0/5 exit 1; B 5/5 exit 0). Receipts `art/rec-*-s36341-c67c.json`.
- Both counter hashes and both receipt generations are listed below; every receipt carries the landed gate's `a7d3922c…`.

This is flagged for Main as a lane-integrity observation: production files were being edited while a read-only wave scored against them. It does not change either verdict, because the scored code was AST-identical and the gate/witness pins were verified on both sides.

## Limits of this probe

- Two seeds, one counter, one gate revision; no C1 run and no new engine variant was built.
- Mutant B's survival is demonstrated on random-content fixtures, where 64-byte prefix collisions have probability ≈ 0; the unit probe isolates the mechanism but is not a scored battery member.
- The counter's `LANDED_ATTRIB`/`RENAMED` arms are satisfiable by a global count (mutant A); only separation distinguishes. That is an observation about which arm carries the key, not a claim that P2 is broken: mutant A's 0/5 means P2 fails for it.
