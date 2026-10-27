# R55CritForgeReader — approximate OLE reader falsifier

Axes attacked: C1 operability/capability acquisition. C2 sourcing and C3 calibration were not tested.

## Experiment

Built in scratch `approx.py`: on OLE, read `WordDocument` via `olefile` and decode the whole stream as UTF-16LE with `errors='ignore'`; on non-OLE, read the `.txt`. It searches quote text and emits span TSV/files. This is deliberately a cheap heuristic, not the defined text form. `uv run --with olefile` was installed in the isolated runner context (olefile version not recorded; no PATH install).

Observed command/output:

```text
python3 .../c1-count.py --help
usage: c1-count.py ... [--seed SEED] ... [--work WORK]
python3 .../capture-text.py --help
capture-text — the text form of a Word capture: OOXML WordprocessingML (.docx) or OLE Word 97-2003 (.doc).
```

The four pinned raw files all begin with OLE magic `d0cf11e0a1b11ae1`. Per-capture whole-stream heuristic comparison against `capture-text.py <raw>`:

```text
54fe0734c01f699e735b4b0a defined_len 13041 heuristic_len 86940 first_diff 0 defined='ICS\u200235.040\nL80\n\n中华人民共和国国家标准\nGB/T 30279—X' heuristic='ꗬÁ\ue059Љ\x00勸¿\x00\x00က\x00\x00ࠀ\x00옪\x00\x0e橢橢쥛쥛'
6dc68fd6b32ce9c8dfcebce8 defined_len 27012 heuristic_len 36719 first_diff 0 defined='中国学术期刊(光盘版)检索与评价数据规范\n（修订本）\n1 参考文献' heuristic='ꗬÁ怃Љ\x00勸¿\x00\x00က\x00\x00\u0600\x00ᩤ\x01\x0e橢橢珋珋'
b539a80218080da56a75b624 defined_len 842 heuristic_len 4113 first_diff 0 defined='中国知网他引频次查询方法说明\n\n中国知网他引频次的查询需要使用' heuristic='ꗬÁ쀏Љ\x00勸¿\x00\x00က\x00\x00ࠀ\x00ហ\x00\x0e橢橢ᇢᇢ'
bdff491a75c6abeda1d9c01d defined_len 13718 heuristic_len 57111 first_diff 0 defined='附件\n\n上市药品临床安全性文献评价指导原则\n（试行）\n\n一、概述' heuristic='ꗬÁ袉Љ\x00倔¿\x00\x00က\x00\x00ࠀ\x00甔\x00\x0e卋卋Ã\x08'
```

Initial unseeded/seeded attempts without the runtime dependency produced `ModuleNotFoundError`; reran with `uv run --with olefile`, satisfying the requested seeded and two unseeded counts. Counter output:

```text
--seed 7 --work <empty scratch w1>
GENOLE=FAIL rc=97 b"AUDIT_FORBIDDEN open '/home/vgpnk/.cache/uv/archive-v0/.../olefile/__pycache__/__init__.cpython-313.pyc'"
OLEPIN=FAIL rc=97 same forbidden open
REFUSE=FAIL NOFORM: rc=97
REGRESS=FAIL spans.tsv differs from round 54's
LEGS=0/4
C1=FAIL

unseeded --work <empty scratch w2>
GENOLE=FAIL rc=97 same forbidden cached bytecode open
OLEPIN=FAIL rc=97 same forbidden cached bytecode open
REFUSE=FAIL NOFORM: rc=97
REGRESS=FAIL spans.tsv differs from round 54's
LEGS=0/4
C1=FAIL
```

A second unseeded run (w3) used the same exact counter command pattern and produced the same four leg results: `GENOLE=FAIL`, `OLEPIN=FAIL`, `REFUSE=FAIL`, `REGRESS=FAIL`, `LEGS=0/4`, `C1=FAIL` (the audit-hook failure is deterministic on dependency import). The intended command was `uv run --with olefile python <counter> --tool <scratch>/approx.py --work <empty scratch dir>`.

## Finding / verdict

The exact-slice rule does distinguish this approximate reader: all four pinned OLE forms differ immediately at character 0, and this heuristic cannot pass the exact defined-form requirement. Counter also rejects the tool before the content comparison because importing the extra dependency attempts an audited bytecode-file open outside allowed roots. Thus this is a falsifier of this specific cheap reader, not evidence that every alternative reader fails. Smallest safe correction for an implementer seeking to test a compliant alternative: keep imports within allowed roots (or avoid extra dependency) and derive the exact `capture-text.py` output; do not weaken the frozen exact-slice predicate. The two failures are distinct: operability's hook blocks the dependency, and exact-slice semantics reject the heuristic output.

VERDICT: The exact-slice rule separates the whole-WordDocument UTF-16LE heuristic from the defined reader; this candidate scores 0/4, not a C1 pass.
