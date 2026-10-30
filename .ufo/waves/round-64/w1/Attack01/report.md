# Attack01 — frozen C1 E12/E13 falsification

## Axes and counterexample

Impacted axes: **operability** (a conforming checker rejects malformed supposedly benign fixtures), **calibration/provenance** (supplement success cannot establish the frozen claim).

Frozen C1 has a fixture defect, not evidence that G02 should accept either mismatched index. `c1-battery-v3.py:386–394` creates each file using one `tag()` draw and writes its README row using a second draw. `run_leg:523` constructs a separately seeded RNG per leg, so executing other legs first does not fix the mismatch. The frozen leg table nevertheless expects rc=0 and no failed gates (`:442–443`).

Minimal observed counterexamples, applying the actual fixture functions to an otherwise empty index:

| Instrument / leg | Created file | README target after normalization | Candidate G02 result / process exit |
|---|---|---|---|
| frozen E12 | `escaped_qf3584932.md` | `knowledge/escaped_qb5545cdb.md` | FAIL, phantom row / 1 |
| frozen E13 | `gate notes q8ae95a7c.md` | `knowledge/gate notes qdd26340f.md` | FAIL, entry unindexed / 1 |
| supplement E12 | `escaped_qf3584932.md` | `knowledge/escaped_qf3584932.md` | PASS / 0 |
| supplement E13 | `gate notes q8ae95a7c.md` | `knowledge/gate notes q8ae95a7c.md` | PASS / 0 |

Fixture RNG seeds: `Attack01/E12` and `Attack01/E13`, respectively; these are the effective per-leg seeds passed to `mk_legs`, not an invocation claiming that the full battery used `C1_SEED=Attack01`. The reproduction uses actual inherited/frozen fixture code, not reimplemented fixture approximations.

## Evidence and scope

Command (outer exit **0**):

```text
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack01/probe.py
```

The retained probe prints each exact child command, fixture content, stdout, stderr, and exit. Child command pattern (all absolute paths):

```text
/usr/bin/python3 -B <lane>/corpus/evidence/round64/controls/ref-preflight-v3.py --root <scratch>/<instrument>-<leg> --only G02 --work <scratch>/work-<instrument>-<leg>
```

Observed decisive stdout (stderr empty in all four child runs):

```text
frozen E12:
GATE G02 knowledge-index FAIL 1 index rows name no knowledge file: knowledge/escaped_qb5545cdb.md (no such file)
PREFLIGHT=0/1 FAILED=G02 ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08
exit=1
frozen E13:
GATE G02 knowledge-index FAIL 1 not named in corpus/README.md: gate notes q8ae95a7c.md
PREFLIGHT=0/1 FAILED=G02 ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08
exit=1
supplement E12 and E13, each:
GATE G02 knowledge-index PASS 1 entries indexed
PREFLIGHT=1/1 FAILED=none ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08
exit=0
```

Each child additionally printed G01 and G03–G08 SKIP in contract order. This is a **bounded minimal-fixture G02 probe**, not a full-battery run, landing-commit result, or production admission. The candidate remains non-production.

Read-only `git -C <lane> show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:<path>` exited 0 for claims and frozen battery. SHA-256 of committed and current bytes matched exactly:

- claims: `bab186919f4518f3662c31661d1e2060b4f9f3d186b33d184c365a3f82d7cfc0`
- frozen battery: `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2`
- inherited supplement measured: `a7057ae33ac958f060a25ea325537bec7bed728e7ea2dad3f3a961e715fc33f1`
- candidate measured: `0b4da0d2128e23b4feeb82bb179ec6a89277a1f0a0aa1c7115e3ae38966f185e`

## Reachability and smallest safe correction

Frozen claims `:89–93` require the **unmodified frozen instrument** to pass three landing runs. The candidate correctly rejects both observed frozen fixtures. Its failures cannot honestly be repaired by teaching production G02 to accept unindexed files or phantom rows: that would violate the separately frozen G02 contract (`claims.md:47–61`). The frozen successful-after target is therefore not supported by these fixtures. This is an honest claim miss/instrument failure, not a checker regression demonstrated by E12/E13.

Do **not** overstate this as a mathematical proof of impossibility for every seed: two 32-bit draws can collide, and a background index could accidentally contain the created name. No collision-seed search or full-battery run was performed. For the concrete seeds above, malformed fixtures and legitimate G02 rejection are directly observed. The frozen judge checks rc at `:491–492`; a full normal leg returning rc=1 cannot meet its rc=0 expectation. Separately, battery `--only` returns **0 with BATTERY=PARTIAL even when legs fail** (`:618–620`), so a partial-run shell exit is never evidence of BATTERY=PASS.

The inherited supplement's smallest fixture repair is already present (`:386–396`): save `t = tag()` once and reuse it in file and row. The two measured supplement fixtures are valid and pass this candidate. Keep that result under the distinct post-freeze supplement identity; do not rename its receipts into frozen C1 success or edit the frozen instrument/claim. L1/canonical judgment owns any closure decision.

Supplemental weakness distinguished from frozen failure: its copied header still labels itself “R64-C1 battery (v3)” and repeats the frozen predicate/counts at `:2–21`, while `:56–58` separately advertises 29 defects/44 legs despite its table retaining 28 defects/43 legs. This is misleading documentation/provenance, not an observed failure of the repaired E12/E13 behavior. Smallest safe supplemental correction: clearly label the post-freeze identity and align its own documentation with its own table; no frozen-rule rewrite.

## Hygiene / self-check

Python **3.14.8**, existing system `/usr/bin/python3`; channel: preinstalled; reason: bounded fixture reproduction. No installs/updates, network calls, clones, git mutations, or production edits. `-B` avoids bytecode writes. The probe removed `/fast/scratch/hyaku/chousa-r64/Attack01/` in `finally`; observed `SCRATCH_REMOVED True`.

Self-evaluation: accuracy 4/5 (bounded fixtures, not complete landing runs); completeness 4/5 (both defects and inherited repairs exercised; seed collision possibility explicitly bounded); clarity 4/5 (instrument identities and exits separated; long absolute commands factored into a pattern); actionability 5/5 (preserve frozen miss, retain named supplement); conciseness 4/5 (hashes/commands add length for reproducibility). Overall 4.2/5. Highest-impact improvement would be separately commissioned landing-run evidence, not a broader unrequested probe. User agreement expected because measured and inferred conclusions are explicitly separated.
