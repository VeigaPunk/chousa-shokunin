# MutC1Arm — round 36, wave 1: C1 arm mutation probe

Date: 2026-10-23. Lane: chousa. Role: UFO-FSD mutation tester (leaf; no subagents).
Wave base: `700bd5fcbf9abc118a6a0f078d51a2e7460c2878` (`git rev-parse master` = `git rev-parse HEAD`
= that value). Landed gate `tools/research-gate.sh` sha256
`a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; base control
`.ufo/waves/round-36/controls/base-gate-r36.sh` sha256
`a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`; committed counter
`corpus/evidence/round36/c1-count.py` sha256
`3fefffe745ed10d2fd06c4c3cc9073ab7bfb46dd82e32c166976fd3aaf4c35be`.

## Axes (godspeed)

1. **Operability** — does each of the 14 scored points correspond to a distinct gate behaviour?
2. **Calibration** — does a `14/14` label's confidence match the counter's measured
   discriminating power against its own named cheapest control?
3. **Mutation adequacy** — how many points of the control-vs-landed delta does one arm uniquely carry?
4. **Evidence integrity** — does the receipt's raw detail still contradict a neutered label?

## Probe design (counter mutation, never a gate change)

Two independent one-line mutants of a **copy** of the committed counter, each executed against
(a) the landed gate and (b) the base control, same seed and therefore the same fixtures:

| mutant | file:line | committed predicate | mutant predicate |
|---|---|---|---|
| A | `c1-count.py:609` | `score("S11-manifest-hash-shim", rc == 0 and man_ok,` | `score("S11-manifest-hash-shim", True,` |
| B | `c1-count.py:622` | `score("S12-locale-c", ref_c and rc_c == rc_utf and parse(out_c) == parse(out_utf),` | `score("S12-locale-c", True,` |

Each mutant keeps the arm's **execution** (the gate is still invoked under the hostile PATH for S11
and under `LC_ALL=C`/`C.UTF-8` for S12; the arm's detail dict is still recorded) and removes only its
**assertion**. Nothing else changes: the score site remains one boolean inside the same
`score()` call, `passed = sum(1 for r in results if r["pass"])` (line 659), `holds = passed == TOTAL
and ref_a and ref_b` (line 660, `TOTAL = 14` line 73). Gate bytes are untouched.

**This is a counter change, not a gate change: any `14/14` or `predicate_holds=true` these mutants
print is NOT evidence for C1/P1.** It measures only which score cell depends on the arm's boolean.

## Commands run (verbatim, expanded) and exit codes

Setup (scratch `/tmp/hyaku/chousa-r36/w1/MutC1Arm`, `C1_TMP`/`TMPDIR` = its `c1tmp`, created first):

```
mkdir -p /tmp/hyaku/chousa-r36/w1/MutC1Arm/{bin,c1tmp,rec}
cp /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py /tmp/hyaku/chousa-r36/w1/MutC1Arm/c1-pristine.py
cp /tmp/hyaku/chousa-r36/w1/MutC1Arm/c1-pristine.py /tmp/hyaku/chousa-r36/w1/MutC1Arm/c1-mut-a.py
cp /tmp/hyaku/chousa-r36/w1/MutC1Arm/c1-pristine.py /tmp/hyaku/chousa-r36/w1/MutC1Arm/c1-mut-b.py
```

Mutants created by two `edit` calls (diff in `mutant-a.patch`, `mutant-b.patch`). Run harness:

```
run() { tag=$1; counter=$2; gate=$3; seed=$4
  C1_TMP=/tmp/hyaku/chousa-r36/w1/MutC1Arm/c1tmp TMPDIR=/tmp/hyaku/chousa-r36/w1/MutC1Arm/c1tmp \
    timeout 1800 python3 "$counter" --gate "$gate" --seed "$seed" \
      --receipt "/tmp/hyaku/chousa-r36/w1/MutC1Arm/rec/$tag.json" > "/tmp/hyaku/chousa-r36/w1/MutC1Arm/rec/$tag.out" 2>&1
  echo "[$tag] exit=$? $(head -1 "/tmp/hyaku/chousa-r36/w1/MutC1Arm/rec/$tag.out")"
}
```

The base control was copied to scratch before scoring and hashed (control sha unchanged):
`cp /home/.../chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh /tmp/hyaku/chousa-r36/w1/MutC1Arm/base-gate-r36.sh`.

| # | command (gate argument expanded) | seed | exit | first output line |
|---|---|---|---|---|
| 1 | `python3 c1-pristine.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` | 36341 | **0** | `ENGINE_SWAP_CANARY=14/14` |
| 2 | `python3 c1-pristine.py --gate /tmp/hyaku/chousa-r36/w1/MutC1Arm/base-gate-r36.sh` | 36341 | **1** | `ENGINE_SWAP_CANARY=10/14` |
| 3 | `python3 c1-mut-a.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` | 36341 | **0** | `ENGINE_SWAP_CANARY=14/14` |
| 4 | `python3 c1-mut-a.py --gate /tmp/hyaku/chousa-r36/w1/MutC1Arm/base-gate-r36.sh` | 36341 | **1** | `ENGINE_SWAP_CANARY=11/14` |
| 5 | `python3 c1-mut-b.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` | 36341 | **0** | `ENGINE_SWAP_CANARY=14/14` |
| 6 | `python3 c1-mut-b.py --gate /tmp/hyaku/chousa-r36/w1/MutC1Arm/base-gate-r36.sh` | 36341 | **1** | `ENGINE_SWAP_CANARY=11/14` |
| 7 | `python3 c1-pristine.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` | 36351 | **0** | `ENGINE_SWAP_CANARY=14/14` |
| 8 | `python3 c1-mut-a.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` | 36351 | **0** | `ENGINE_SWAP_CANARY=14/14` |
| 9 | `python3 c1-mut-a.py --gate /tmp/hyaku/chousa-r36/w1/MutC1Arm/base-gate-r36.sh` | 36351 | **1** | `ENGINE_SWAP_CANARY=11/14` |
| 10 | `python3 c1-mut-b.py --gate /tmp/hyaku/chousa-r36/w1/MutC1Arm/base-gate-r36.sh` | 36351 | **1** | `ENGINE_SWAP_CANARY=11/14` |
| 11 | `python3 c1-mut-b.py --gate /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` | 36351 | **0** | `ENGINE_SWAP_CANARY=14/14` |
| 12 | replay of #1 (same seed) | 36341 | **0** | `ENGINE_SWAP_CANARY=14/14` |

`predicate_holds` per receipt: landed runs `true` (all mutants and pristine); base runs `false` (all).
Every receipt's `gate_sha256` matches the gate actually scored (landed `a7d392…`, base `a47688…`),
checked programmatically over `rec/*.json`.

Pinning/wall time: each run 4–7 s (altogether 22.4 s for runs 1–6, 17.2 s for 7–10+details).

## Deciding lines (raw receipt detail, verbatim)

- Landed, pristine (#1): `S11-manifest-hash-shim PASS {"manifest_ok": true, "rc": 0, ...}`;
  `S12-locale-c PASS {"c_obs": {"L1": ["supported", "match"]}, "c_rc": 0, "utf8_obs": {"L1": ["supported", "match"]}, "utf8_rc": 0}`.
- Base, pristine (#2): `S11-manifest-hash-shim FAIL {"manifest_ok": false, "rc": 0, ...}`;
  `S12-locale-c FAIL {"c_obs": {"L1": ["unsupported", "mismatch"]}, "c_rc": 1, "utf8_obs": {"L1": ["supported", "match"]}, "utf8_rc": 0}`.
  (The base gate writes a poisoned manifest and still exits 0 — the round-35 defect the arm exists for.)
- **Base, mut-a (#4), the money line:** `S11-manifest-hash-shim PASS {"manifest_ok": false, "rc": 0, ...}`
  — the label says PASS while the arm's own observation says the manifest failed. The arm, not any
  neighbouring cell, was carrying that point.
- **Base, mut-b (#6), same shape:** `S12-locale-c PASS {"c_obs": {"L1": ["unsupported", "mismatch"]}, "c_rc": 1, "utf8_obs": {"L1": ["supported", "match"]}, "utf8_rc": 0}`.
- Cross-checks: in #4 S12 still FAILs (`c_rc 1 ≠ utf8_rc 0`); in #6 S11 still FAILs
  (`manifest_ok:false`). The two arms do not shadow each other.
- Landed, mut-a/#3 and mut-b/#5: all 14 detail dicts are the pristine ones; only the two booleans
  changed. On the landed gate the mutation is invisible in the label — both print
  `ENGINE_SWAP_CANARY=14/14` / `holds=true`.

## Reading: which arm the count rides on

- **Neither arm is a single point of failure for the landed label.** Both arms already pass against
  the landed gate, so force-passing them leaves `14/14` and `predicate_holds=true` unchanged: the
  mutants **survive** on the landed input. That is expected and is exactly why a mutant's 14/14
  cannot be offered as evidence for C1.
- **Each probed arm is load-bearing for exactly one point of the claim's demonstrated delta.** The
  committed counter separates landed from the named do-nothing control by four cells, S11–S14
  (`10/14` base). Disabling S11's assertion moves the control to `11/14`, disabling S12's moves it to
  `11/14`; neither reaches `12/14` or `14/14`. The mutant is **killed by the base control**: its
  score output differs from pristine under that input by exactly the arm's cell.
- **The two arms are mutually independent at the solver level** (see cross-checks above). Each of
  S11/S12 is necessary and neither is sufficient: the 4-point delta needs S11, S12, S13, S14 all.
- Therefore: the count does **not** ride on one arm; it is the additive sum of 14 conjuncts. What the
  claim's "before/after" rides on is **four** conjuncts, one point each.

## Can 14/14 be explained by fewer than 14 independent behaviours?

Yes, on the evidence the counter itself supplies:

1. **Arithmetic:** 14 distinct `score()` call sites (lines 452, 459, 479, 486, 493, 502, 516, 528,
   541, 576, 609, 622, 636, 653), one boolean each, summed at 659–660. So `14/14` is 14 assertions —
   not 14 demonstrated behaviours. Ten of the fourteen (S1–S10) already pass on the base control;
   no committed control fails any of them, so their discriminating power is not exercised by this
   counter's own control set (claims.md attributes their evidence to round-35 constructions, not to
   this comparison).
2. **Shared oracles:** six arms (S1, S2, S3, S7, S8, S9) share the `same_as_a(rc, out)` output-equality
   oracle; three of those (S7, S8, S9) additionally share the `GATE_GREP:` echo fullmatch; S13 and S14
   share the pin/drift machinery. Four fixtures cover all fourteen (A: S1–S9, B: S10, C: S12,
   D: S11/S13/S14 — counter docstring lines 47–49). The `14` is a conjunction count over four
   fixtures, not an independence count.
3. **Control-flipping behaviours: 4.** Exactly S11, S12, S13, S14 change between the do-nothing
   engine and the landed tree; the probed mutants show each carries exactly 1 of those 4, and the base
   receipt shows S13 (`drift_out GATE_DRIFT: -LINE`, `baseline_echo true`) and S14 (`-LINE`, not
   `-GATE_GREP`) fail for different observed reasons. [INFERENCE] By content, these map 1:1 to repairs
   R3 (manifest pin), R4 (C-locale decode), R1 (pin echo scrub), R2 (drift token) — a mapping by
   repair text, not separately measured here.

So the defensible statement a closure may make is `14 assertions; 4 fixtures; 4 behaviours the named
cheapest control demonstrates`. A statement of "fourteen independent behaviours" is not supported by
the committed control comparison; the other ten are guard assertions whose failures no committed
control produces.

## MEETS check

**No MEETS finding.** The probe produced no gate that passes an arm without the gate behaving, and no
output-equivalent engine that scores 14/14 under the **unmodified** counter. The mutant's landed
`14/14` is forced by a constant in the detector and is not a gate observation; the brief's
requirement to label it as not-evidence applies and is applied here. The nearest thing to a MEETS
shape is an arithmetic implication, [INFERENCE], not run against a real gate: a hypothetical gate
that implemented every repair except the manifest pin would score `13/14` pristine but `14/14` under
mutant-a — i.e. the S11 cell is atomic (one assertion) and there is no second, independent manifest
check elsewhere in the fourteen.

## Limits

- Only S11 and S12 were mutated. S13/S14 are inferred from the base receipt's two failures, not
  individually force-passed.
- The base control lacks all four repairs at once, so no run isolates a gate that lacks only one.
- Two fresh seeds (36341, 36351), one host, GNU grep `3.12-modified` as reported by the gate's own
  `--version` echo. Replay at 36341 is pass-vector-identical; five detail dicts differ only in
  randomly named temp paths (`S5`, `S6`, `S7`, `S9`, `S10`).
- No tool installs, no network, no pacman; nothing modified outside `/tmp/hyaku/chousa-r36/w1/MutC1Arm`
  and the artifact directory.

## Files opened (access date 2026-10-23)

| path | purpose |
|---|---|
| `.ufo/waves/round-36/w1-briefs/MutC1Arm.md` | validated brief |
| `corpus/evidence/round36/claims.md` | frozen claim design, C1/P1, before, repairs |
| `corpus/evidence/round36/c1-count.py` | full read (lines 1–203, 204–470, 470–681) + `grep -n` line map |
| `tools/research-gate.sh` | `grep -n` only (sha256sum/json_unescape/GATE_GREP/LC_ALL sites); not fully read |
| `.ufo/waves/round-36/measure/c1-before-s36001.json` | committed before receipt, parsed with `python3 -c` |
| scratch `c1-pristine.py`, `c1-mut-a.py`, `c1-mut-b.py`, `base-gate-r36.sh`, `rec/*.json`, `rec/*.out` | my own copies/outputs |

Not opened (C2 scope, not needed for this C1 probe): `tools/argv-witness.py`,
`tools/mechanism-witness.py`, `corpus/evidence/round36/c2-count.py`.

## Artifacts (all under `.ufo/waves/round-36/w1/MutC1Arm/`, each < 1 MiB)

`SHA256SUMS` (sha256 `86eceb001fb8e9a0ea0585888836fc83528fbabf57b25d56ec43a7bb811ae854`) lists:

```
65e403df8e507ce944e8f6045220e00d2f42ff9fbc9521ffac5c9ee78bc7ae74  c1-mut-a.py
9d992f29511588e4f5cb632a21ebb4606e3b62028ab7ac57ad9de66db3ee2110  c1-mut-b.py
cdcff453645a418e67aa39cb72379dd6fdbe9c6bd88142538c44196be1f1c427  mutant-a.patch
8cc7e8908d1b77997c469247487e0052c98f7a4b31b7cfbec2c7b28d2d13eaa4  mutant-b.patch
eee5c801d1f519db80099f81d9fc453d8ad8d8e6bd7f910d38504ffe3768cff6  pristine-base.json
def4e8ab2e798c5d973b3c72525b8e313e6ae30768ac49217c7285b545b3c217  pristine-base.out
dd1b509963cd62d53d3daae2c2a500d5d0416c8b42149d55422bade305b9a41d  pristine-landed-s36341.json
e66b5c7e7b32119873d62f088a19811eab5c56312c0011677ef89935dd4cf2f2  pristine-landed-s36341b.json
4222221ce534a11a78ea19b2ec64943cfbb305bbcf884e50fc28b1aead0f1b20  pristine-landed-s36341b.out
c0488d741e9223da374228345976b042780d24a1a321305c61fec5afcd2a8e64  pristine-landed-s36351.json
655266304e55c482de46c2c578cfb8251581e46d50c9bada7dbc71903e7e4d61  pristine-landed-s36351.out
c56a02657494c39d9d35edd25a728b4b4de131afddc206d8aba8699c82aec52e  mut-a-landed.json
4af441171b8e2a229c62b271eb8bca9355f6a9cf6adadab563e100f7d9a6fc54  mut-a-landed.out
ad777ad18125a26c6c4e69c9f2a2a263865850e147da3e02981eff7a6b0a4c23  mut-a-landed-s36351.json
e761d4386c87783383296379e1f4c5072660d0b9a792ff1ba958f5e82503bee5  mut-a-landed-s36351.out
91089db838e8a9e40c55cec499f6471ad4c38a73b3cf33ef8f2867c6570ab727  mut-a-base.json
0ee630cd640340a2532fc3f1de9c6d090bab39b4bf46d7dd5c1e84a7e59829d6  mut-a-base.out
a01f0f7bf35ff279086806e8f656128c671640082ec7ded2e2fbfb71833c6bb9  mut-a-base-s36351.json
bc513bb5916c86fab80b325b83b35ba6d497e792a9ad312f71770816941ed319  mut-a-base-s36351.out
2fefd9053f4f0368b4c0524efaacfeafefdd8232c14802d9b727a0f706fcb513  mut-b-landed.json
05f1bce5b3196611fa83399b310c9ef7abf5f1e3914fbd1c48b52eac921ef9eb  mut-b-landed.out
15af14b0071462143f4fdb8b674cbaba7ab2df19ecc7e931b7c3486e6a8b38cc  mut-b-landed-s36351.json
1525b24457cd58a1045903f48c41e0ffb043bc88d878417ab32aaa57112a504e  mut-b-landed-s36351.out
e30ba3f1781eaaaadc2efca140c717f5d9dfdc3b4c94bfd6e4031ce31bed50e8  mut-b-base.json
92d39f354d28f7b76e3dc9bbc818914abcf9dca1eacac22826af00793b1281d6  mut-b-base.out
3577f6b213ddc0baef0bdef07713f2abe17711f2859f8c991fc2d1a3097bb27c  mut-b-base-s36351.json
342a73db670b5e26dc464edce3ce891def560eadc6be6309bd86d6d7fdafe9bf  mut-b-base-s36351.out
```

## Restoration evidence

No lane production byte was written. After all runs:

```
3fefffe745ed10d2fd06c4c3cc9073ab7bfb46dd82e32c166976fd3aaf4c35be  corpus/evidence/round36/c1-count.py
a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8  tools/research-gate.sh
a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad  .ufo/waves/round-36/controls/base-gate-r36.sh
```

The committed counter and both gates are byte-identical to their pre-probe hashes; the mutants exist
only as scratch copies (`/tmp/hyaku/chousa-r36/w1/MutC1Arm/c1-mut-{a,b}.py`) and as clearly named
artifacts in my wave directory.

## Verdict

**VERDICT: LOAD-BEARING (both probed arms, exactly one point each, mutually independent); the mutants
SURVIVED on the landed gate (14/14, `predicate_holds=true` — a counter change, therefore not evidence
for C1) and were KILLED by the base control, each shifting it 10/14 → 11/14 in its own cell; no MEETS
finding; the committed 14/14 is 14 conjunct assertions over 4 fixtures, of which only four cells
(S11–S14) are demonstrated to separate the do-nothing engine — the claim's measured independence
against its named cheapest control is 4, not 14.**
