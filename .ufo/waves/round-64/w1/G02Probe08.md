# G02Probe08 — phantom knowledge-path fixture

Candidate: `corpus/evidence/round64/controls/ref-preflight-v3.py` (unchanged). Frozen contract: `corpus/evidence/round64/claims.md`, R64-C1 clauses (iii) and kill-rule scope. The README contains the valid indexed `valid.md` and a phantom whole-token `knowledge/real/missing.md` occurrence; fixture has only `corpus/knowledge/real/valid.md`.

Command (bounded G02-only fixture run):

```text
python3 /fast/scratch/hyaku/chousa-r64/G02Probe08/probe.py
```

The driver invoked:

```text
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/ref-preflight-v3.py --root /fast/scratch/hyaku/chousa-r64/G02Probe08/fixture --only G02 --work /fast/scratch/hyaku/chousa-r64/G02Probe08/work
```

Observed exit: **0**. Stdout:

```text
GATE G01 census SKIP
GATE G02 knowledge-index PASS 1 entries indexed
GATE G03 lesson-gate SKIP
GATE G04 shonen-pointers SKIP
GATE G05 scorecard-paths SKIP
GATE G06 freeze-selftest SKIP
GATE G07 assimilate-selftest SKIP
GATE G08 gate-selftest SKIP
PREFLIGHT=1/1 FAILED=none ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08
```

Stderr was empty. This conflicts with frozen R64-C1 (iii): every whole-token `knowledge/…/<NAME>.md` occurrence in normalized README must name an existing regular `.md` file under `corpus/knowledge/`; the phantom row should fail. The source explains the miss: candidate's `g02` phantom matcher at line 136 only captures one ASCII-allowed filename component (`knowledge/[A-Za-z0-9][A-Za-z0-9._-]*\.md`), not a nested path. The fixture establishes a concrete false pass; it does not establish overall battery status or rewrite the frozen claim. No candidate/production files changed.

Preserved fixture recipe and captured streams: `/fast/scratch/hyaku/chousa-r64/G02Probe08/probe.py`, `stdout.txt`, `stderr.txt`; fixture tree and work directory are under the same scratch root. Tool installation/update: none.