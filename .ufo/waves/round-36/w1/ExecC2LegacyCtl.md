# C2 legacy control — round 36, wave 1

**Axis:** calibration (legacy C2 before-state). This scoped run does not measure C1/operability.

## Measurement

The requested run used seed `36321` against the base control gate. It exited **1** because the predicate was false, not because of a harness error. Standard output, lines 1–7:

```text
WITNESS_PER_RECORD=2/5 OUTPUT_EQUIV=5/5 LANDED_ATTRIB=absent RENAMED=fail
  V1-python-exact        output=9/9 witness=fail attrib=None
  V2-env-keyed           output=9/9 witness=pass attrib=None
  V3-witness-forge       output=9/9 witness=pass attrib=None
  V4-one-call-for-show   output=9/9 witness=fail attrib=None
  V5-body-replaced       output=9/9 witness=pass attrib=None
  V6-renamed-matcher     output=0/9 witness=unparseable attrib=None
```

**separated: V1-python-exact, V4-one-call-for-show; passed: V2-env-keyed, V3-witness-forge, V5-body-replaced.** V6 is the renamed control, not one of the five legacy variants; it was unparseable and failed. Receipt confirms `gate_sha256=a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad` (line 4), label `WITNESS_PER_RECORD=2/5` (line 5), `matched=2` (line 17), `output_equiv=5` (line 18), `landed_attrib=absent` (line 16), and `renamed=fail` (line 20). Per-variant receipt details are lines 23–101.

Receipt: `.ufo/waves/round-36/w1/ExecC2LegacyCtl/c2-before-legacy-s36321.json` — SHA-256 `baf739cea39cd9efd4030b090a3babaa1b14b1b93ba47088089249bdc69f3445`.

## Source comparison

| Source | Stated before-state | Measured result | Finding |
|---|---|---|---|
| `corpus/evidence/round36/c2-count.py:36-39` (accessed 2026-10-23) | Says the legacy witness “separates only 3/5”; notes V3 and V5 pass it. | `2/5` are separated: V1 and V4 fail the witness; V2, V3 and V5 pass it (receipt lines 35, 48, 61, 74, 87). | **Mismatch:** 3/5 is not the measured separation count. The parenthetical pass list is incomplete because V2 also passes. The 3 pass-survivors vs 2 separated variants explanation is [INFERENCE]. Its `landed attribution absent` statement agrees with receipt line 16. |
| `corpus/evidence/round36/claims.md:105-112` (accessed 2026-10-23) | Gives `2/5`, output-equivalent `5/5`, landed attribution absent, renamed fail; says V1/V4 are separated and V2/V3/V5 pass. | Same aggregate and per-variant results. | **No mismatch:** reproduced on this fresh seed and pinned base gate. |

## Commands and exit codes

All commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless their command includes `cd`.

1. `mkdir -p /tmp/hyaku/chousa-r36/w1/ExecC2LegacyCtl /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2LegacyCtl` — exit 0.
2. `sha256sum .ufo/waves/round-36/controls/base-gate-r36.sh` — exit 0; output was `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad  .ufo/waves/round-36/controls/base-gate-r36.sh`.
3. `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && C2_TMP=/tmp/hyaku/chousa-r36/w1/ExecC2LegacyCtl timeout 1800 python3 corpus/evidence/round36/c2-count.py --gate .ufo/waves/round-36/controls/base-gate-r36.sh --witness tools/mechanism-witness.py --seed 36321 --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecC2LegacyCtl/c2-before-legacy-s36321.json` — exit **1**; deciding stdout line 1 and receipt lines 5, 17–20; observed wall time 18.94 seconds.
4. `mkdir -p /tmp/hyaku/chousa-r36/w1/ExecC2LegacyCtl` — exit 0.
5. `sha256sum .ufo/waves/round-36/w1/ExecC2LegacyCtl/c2-before-legacy-s36321.json` — exit 0; output was `baf739cea39cd9efd4030b090a3babaa1b14b1b93ba47088089249bdc69f3445  .ufo/waves/round-36/w1/ExecC2LegacyCtl/c2-before-legacy-s36321.json`.

## Files and scope

Files read or hashed, accessed 2026-10-23: `.ufo/waves/round-36/w1-briefs/ExecC2LegacyCtl.md`; `/home/vgpnk/.agents/skills/godspeed/SKILL.md`; `corpus/evidence/round36/claims.md`; `corpus/evidence/round36/c1-count.py`; `corpus/evidence/round36/c2-count.py`; `tools/argv-witness.py`; `tools/mechanism-witness.py`; `.ufo/waves/round-36/controls/base-gate-r36.sh` (hashed); and the receipt above (read and hashed). The assigned scratch directory was empty when inspected. No production files were changed; no tests, builds, linters, formatters or installs were run.

**VERDICT:** The legacy control reproduces the claims.md before-state exactly, but the C2 counter docstring's “separates only 3/5” conflicts with the observed 2/5 separation count.
