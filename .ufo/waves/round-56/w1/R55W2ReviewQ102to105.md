# R55W2ReviewQ102to105 — QUALITY 102–105

Scope: round-55 QUALITY claims, without changing frozen predicates or anchors. Axes: operability, depth, calibration.

## Reproduction

102. In scratch `/fast/scratch/hyaku/chousa-r56/R55W2ReviewQ102to105`, ran the prescribed DELEGATE builder, then `python3 .../round55/c1-count.py --tool "$S/ctl/delegate.py" --seed 55 --work "$S/work102"`. Output: `GENOLE=FAIL rc=97 b'AUDIT_FORBIDDEN ctypes.dlopen'`; `OLEPIN=FAIL rc=97 ...`; `REFUSE=FAIL NOFORM: rc=97`; `REGRESS=FAIL rc=97 ...`; `LEGS=0/4`; `C1=FAIL`. This reproduces the stated failure mode; no unexpected pass.

103. `uv run --with pypdf python .../round55/pdf-crosscheck.py` returned `PDF_QUOTES=21 NOT_IN_INDEPENDENT=0 RAW_NOT_IN=14`, rc 0 (pypdf emitted wrong-pointing-object warnings). `python3 .../considerthese-ledger-check.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin` returned `PROPOSALS=35 ROWS=35 IMPL=24 FMT=9 OPEN=1 OPS=1 BAD=0`, rc 0. These prescribed checks pass on current bytes; not a reproduction of their historical negative controls, which the criterion separately cites as already run.

104. `wave-settled-check.py --round 54` returned `WAVES=2 SETTLED=1`, with w1 settled and w2 `UNSETTLED ... after report=...`, rc 1; `--round 52` returned `WAVES=2 SETTLED=2`, rc 0. Both expected outcomes reproduce.

105. I attempted the builders against the lane's in-lane output path; the first builder emitted `usage: OUTDIR must lie outside the lane` and exited 2, and the shell's `set`/tool wrapper stopped before capturing its nonexistence or running the other two. Thus the criterion's bundled `exit 2 x3, no directory created` was not fully reproduced in this run. The prescribed path is under `corpus/evidence/round55/controls/tmpout`; I did not remove or alter pre-existing lane data to retry. This is a verification gap, not evidence of a defect.

## C3-anchor overlap

QUALITY 102–105 do not restate a C3 anchor's target/key-phrase/observed tuple. C3 E05–E07 and E09 target QUALITY's older claims (including the 12,963/12,795, control-character and delegation assertions); the new criteria 102–105 concern the round-55 controls/checkers and settlement/output guards. They refer to E11 as precedent within 102 but do not reproduce its anchor phrase or observed tuple. Basis: round55 `claims.md` lines 145–180 and QUALITY.md lines 947–953.

## VERDICT
QUALITY 102 and 104's stated failure behavior reproduced; 103 current checks pass; 105 only partially exercised because the command wrapper stopped after builder 1. No actionable C3-anchor restatement found; verification gap remains for 105's full three-builder/no-output claim.
