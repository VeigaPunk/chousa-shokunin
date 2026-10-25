# MutC2Final — round 47 w2 — forge battery against the FINAL `corpus/evidence/round47/c2-count.py`

ATTACKS: C2 calibration — forges a–i re-run against the final round-47 c2-count.py on a /tmp scratch of lane tip `1fc5ed193ad48a482402c862f4e4cc47e46d5b2d`.

VERDICT: holds

## Instrument and bytes
- Counter (frozen, final): `corpus/evidence/round47/c2-count.py`, sha256 `60134f25a5069eef2e59309ed41511f13ce4557abc1390cc8ffb68f2cfcce4d4` (matches the lane tip's file).
- Pinned r46: `corpus/evidence/round46/c2-count.py` sha256 `f93cb10795ef7402848ea355680a6b0bd25ad68c8913c24944ef92029c81046f` (matches `R46_SHA`).
- Scratch: `/tmp/chousa-r47w2-MutC2Final/tree` = `git archive 1fc5ed193… | tar -x`. After every forge, `SKILL.md`/`corpus/QUALITY.md` were restored to pristine bytes (sha256 verified) and added files (`tools/noop.py`, `tools/newgate.py`, the forged pyc) were removed. Final `diff -r --brief pristine tree` = empty (restoration evidence).

## Baseline (pristine)
```
$ python3 corpus/evidence/round47/c2-count.py --root tree --list
ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7)
FLOOR=92
GATES_ROWS=51
REGISTERED=94/94
UNREGISTERED=0
DANGLING=0
MISMATCHES=0
C2=PASS          EXIT=0
```

## Forge outputs (each is the full decisive output of `python3 …/c2-count.py --root tree`, exit appended)
```
[a-junk-all-paths]      ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=52 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
[b-escaped-pipes]       ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=51 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
[c-tilde-fence]         ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=51 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
[d-two-inline-comments] ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=52 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
[e-no-word-exit-missing-path] ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=52 REGISTERED=94/94 UNREGISTERED=0 DANGLING=1 MISMATCHES=1 C2=FAIL EXIT=1
[f-no-exit-code-documented]    ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=52 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
[f2-no-exit-code-new-entry]    ENTRY_POINTS=95 (abc=86 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=52 REGISTERED=94/95 UNREGISTERED=1 DANGLING=0 MISMATCHES=1 C2=FAIL EXIT=1
[g-drop-corpus/evidence/round29/prose-check.py] ENTRY_POINTS=93 (abc=85 dependence=+2 check_named=+6) FLOOR=92 GATES_ROWS=51 REGISTERED=93/93 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
[g-floor-substitution-noop] ENTRY_POINTS=95 (abc=86 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=52 REGISTERED=95/95 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
[h-forged-pyc]  ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=51 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
[i-row-in-h3-subsection] ENTRY_POINTS=94 (abc=85 dependence=+2 check_named=+7) FLOOR=92 GATES_ROWS=52 REGISTERED=94/94 UNREGISTERED=0 DANGLING=0 MISMATCHES=0 C2=PASS EXIT=0
```

## Per-forge verdicts
- (a) junk row listing every existing repo-relative `*.py`/`*.sh` path (≈ all 94 eps) in its entry cell with `exit 0`: **scores C2=PASS, exit 0**. **Covered by Named limits** — round-47.md:115-119: "one junk row listing every path in its entry cell with `exit 0` still registers them (`MutC2Forge` a)".
- (b) escaped `\|` row: `| junk \| gate \| tools/research-gate.sh \| exit 0 \| | | | |` — **killed/inert**: `CELL_SPLIT` (c2-count.py:86, `(?<!\\)\|`) refuses escaped pipes, so the row is not read (GATES_ROWS stays 51); nothing registers. The w1 b2 shift (old counter split on every `|`) does not reproduce.
- (c) `~~~` fenced junk row — **killed/inert**: fence-aware reader (c2-count.py:111-117) recognises `~~~`; GATES_ROWS stays 51.
- (d) one row with two inline HTML comments (`<!-- P1 --> <!-- P2 -->` in entry cell, `<!-- exit 0 -->` in verdict cell): **scores C2=PASS, exit 0**, but benign — both comments are stripped, cells come out empty, nothing registers (GATES_ROWS=52). The "every inline comment stripped" fix (c2-count.py:124-126) holds; no false registration.
- (e) row `` `| junk | gate | tools/ghost-gate.py | `0` ok | x | y | z | w |` `` (no word `exit`): **killed** — DANGLING=1, MISMATCHES=1, C2=FAIL, exit 1. DANGLING reads every row and the backticked `0` matches EXIT_CODE (c2-count.py:91); F2 fix verified.
- (f) verdict cell `no exit code documented`: with an already-registered path it changes nothing (PASS); with a NEW entry point (`tools/newgate.py`, abc=86, eps=95) whose only registration attempt is that row: **killed** — UNREGISTERED=1, C2=FAIL, exit 1. F1/F3 fix verified.
- (g) floor substitution: dropping one check-named gate (`corpus/evidence/round29/prose-check.py` from QUALITY.md:191) gives ENTRY_POINTS=93 still ≥ FLOOR=92 → PASS; adding empty `tools/noop.py` and listing it in a junk row gives 95 → PASS. **Scores C2=PASS** and is **covered by Named limits** — "FLOOR is a count, so a deleted gate can be replaced by an empty script (g2)" (round-47.md:117-118). Note: the floor has a 2-entry margin at the tip (94 vs 92); one exclusive check-named deletion alone does not breach it, which is consistent with the declared FLOOR semantics.
- (h) forged `corpus/evidence/round46/__pycache__/c2-count.cpython-314.pyc` (evil bytecode, sha256 `e270d784765be7778800d914901ae8105093043229c359a93b47031919d25a93`): **scores C2=PASS, exit 0**, identical stdout. Inert: `load_r46` executes exactly the hashed ` bytes via `exec(compile(src))` and never consults `__pycache__` (c2-count.py:64-69); the guard is disclosed in the code (round-47 `SentScopeAudit`), not in the Named limits section.
- (i) Gates row placed under `### forge subsection` (inside `## Gates`): **scores C2=PASS, exit 0** — the reader toggles only on `## ` headings (c2-count.py:127-129), so `###` subsections remain inside the section. Same class as (a) (single non-delimiter junk row), covered by the same Named limit; the row has no GFM delimiter row, so a rendered reader sees no table — consistent with the "row truth stays a reader's check" limit.

## Summary
PASS-scoring forges: a, d, g, h, i. Of these, a, g and i are covered by the Named limits (round-47.md:115-119); d and h score PASS only because the injected content is inert (both inline comments stripped; `__pycache__` never read). Killed: b, c (inert, correctly ignored), e (DANGLING), f/f2 (UNREGISTERED). No forge produced a false C2=PASS through a defect the frozen counter should have caught; every kill rule fires as declared. Claim C2 holds at the tip. No tools installed; no fetch; scratch `/tmp/chousa-r47w2-MutC2Final` deleted.
