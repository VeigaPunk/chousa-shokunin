# R56ReviewSkillRow — build-spans registry class

## Finding — gate registration is supported; self-test contract needs an explicit interpretation

Reviewed frozen C1 first (`corpus/evidence/round56/claims.md`, R56-C1 and routed item 5), current `SKILL.md:142-143`, and closure §6 item 5. `SKILL.md:142` calls `build-spans` a `probe`, although its entry documents exit 1 for refusal/`STALE>0`. Closure item 5 asks for gate registration with a self-test or a reason to retain probe.

`PROTOCOL.md:375-382` defines a gate as a committed, re-runnable verdict script comparing surfaces with persisted expected values; a probe cannot fail. It maps 0/1 to clean/failed and requires declaration of other exits. Its Self-test clause (§Gate standard, lines 384-392) requires isolated fixtures, expected exit and stable finding ID, and says a helper-only self-check does not suffice. The registry schema (lines 401-403) requires command, verdict map, self-test, pins, write scope and owner. SKILL's `## Gates` table (lines 76-80) contains the registry but no separate gate/probe definition. No `lsp` device/server is available in this session; literal source reads/searches used instead.

**Conclusion:** `tools/build-spans.py --check` is gate-capable: it re-derives from its inputs, compares the result to persisted `spans.tsv`/span files, is read-only, and returns 1 with stable stale findings. `c1-gate.py` is also verdict-bearing and demonstrably returns 1 when a builder violates the tested behavior; its declared 0/1/2 contract fits PROTOCOL. The pair therefore clears the closure's “shown able to fail” criterion. The frozen `c1-count.py` is the appropriate registry self-test command by the lane's counter-gate convention, but strict §Gate standard wording leaves a gap: neither builder nor `c1-gate.py` exposes a named `--selftest`/self-invocation mode, and the counter is a separate harness. If PROTOCOL requires self-invocation by the registered gate itself, this row alone cannot cure that gap; do not describe the counter as an internal mode.

## Executed checks

Commands run with `TMPDIR=/fast/scratch/hyaku/chousa-r56/R56ReviewSkillRow/tmp` and `PYTHONDONTWRITEBYTECODE=1`; output directories and the tampered files were only in that scratch tree.

- `python3 tools/build-spans.py --quotes corpus/evidence/round55/quotes.tsv --out /fast/scratch/hyaku/chousa-r56/R56ReviewSkillRow/out --cache /fast/scratch/hyaku/chousa-r56/R56ReviewSkillRow/cache` → `SPANS_ROWS=19 WRITTEN=19`, rc 0.
- Same command plus `--check` → `SPANS_ROWS=19 STALE=0`, rc 0. After changing one byte in `spans/S124-10.txt` and adding `spans/S999-1.txt`, `--check` → `SPANS_FILE_STALE spans/S124-10.txt`; `SPANS_FILE_ORPHAN spans/S999-1.txt`; `SPANS_ROWS=19 STALE=2`, rc 1. This is direct failure evidence for `--check`.
- `python3 corpus/evidence/round56/c1-gate.py --per-leg 1 --seed 7 --work /fast/scratch/hyaku/chousa-r56/R56ReviewSkillRow/gate-usage` → usage guard, rc 2.
- `python3 corpus/evidence/round56/c1-gate.py --seed 7 --work /fast/scratch/hyaku/chousa-r56/R56ReviewSkillRow/gate-pass` → `GENOLE=PASS`, `OLEPIN=PASS`, `REFUSE=PASS`, `REGRESS=PASS r54 33 rows identical`, `LEGS=4/4`, `C1=PASS`, rc 0.
- `python3 corpus/evidence/round56/c1-gate.py --tool /fast/scratch/hyaku/chousa-r56/R56ReviewSkillRow/stub-zero.py --seed 7 --work /fast/scratch/hyaku/chousa-r56/R56ReviewSkillRow/gate-fail` (stub exits 0 without writing) → all four legs FAIL (`no spans.tsv`; `NOFORM: rc=0`; `spans.tsv differs from round 54's`), `LEGS=0/4`, `C1=FAIL`, rc 1.
- Gate source lines 427-478 name four legs and implement exit 0 iff all pass, otherwise 1; `env_fail` exits 2. `Ctx.soffice` uses a private profile under `--work` (lines 159-164). Before my LibreOffice runs a sibling process was already present (pid 219297, profile in its own scratch); afterward only a different sibling pid (425058, its own scratch profile) was present. No process from my runs remained.

## Frozen receipt evidence copied here

`corpus/evidence/round56/controls/c1-before.txt`: `CANDIDATE=2/2 KILLED=1/9 DENIED=0/2`; `C1=FAIL`; `exit=1` (the old counter fails to discriminate the frozen clauses/hooks).

`corpus/evidence/round56/controls/c1-controls.txt`: HOOKONLY, JUNK (including alternating FLIP), and EMPTY each conclude `C1=FAIL` and `exit=1`. HOOKONLY/JUNK/EMPTY each show the landed candidate `CANDIDATE=2/2`, but only `KILLED=1/9`; HOOKONLY reports `DENIED=2/2`. These controls show counter failure on deficient batteries; they are not a passing after-measurement. The after-measurement file was untracked/in flight during this review and is not claimed here.

The frozen candidate tree at `46e1758f3d8a5d1bf30200d2ff7d909b0230feed` contains `c1-gate.py`, `c1-count.py`, seven violator builders and `oracle-m8-unpinned.py`. `c1-count.py` specifies seeds 7/56, per-leg 2, and frozen target `CANDIDATE=2/2 KILLED=9/9 DENIED=2/2 C1=PASS`; I did not rerun this full counter. `tools/build-spans.py` source (`:24-30,157-183`) confirms the check-mode comparisons/findings and exits cited above.

## Proposed append-only replacement row

Append this new row after the existing round-55 rows; preserve the old row unchanged. It supersedes the round-55 `build-spans` row by name:

```text
| `build-spans` (round 56; gate registration; supersedes the round-55 `build-spans` row by name) | gate | `python3 tools/build-spans.py --quotes Q.tsv --out DIR [--cache DIR] [--check]` · clause-coverage gate `python3 corpus/evidence/round56/c1-gate.py [--tool PATH] [--seed N] [--per-leg K] [--work DIR]` (GENOLE/OLEPIN/REFUSE/REGRESS) | builder: exit 0 built/current (`SPANS_ROWS=n WRITTEN=n` / `SPANS_ROWS=n STALE=0`); exit 1 refusal or `STALE>0` (`SPANS_HEADER_STALE`, `SPANS_ROW_STALE`, `SPANS_FILE_STALE`, `SPANS_ROW_EXTRA`, `SPANS_FILE_ORPHAN`); exit 2 usage/env. Gate: exit 0 `LEGS=4/4 C1=PASS`; exit 1 any leg fails; exit 2 `ENV_CHANGED`/usage | self-test command `python3 corpus/evidence/round56/c1-count.py --work EMPTY_DIR` (frozen seeds 7/56, per-leg 2): target `CANDIDATE=2/2 KILLED=9/9 DENIED=2/2 C1=PASS`, exit 0; failure evidence `controls/c1-before.txt` (`KILLED=1/9 DENIED=0/2 C1=FAIL`, exit 1), `controls/c1-controls.txt` (HOOKONLY/JUNK/EMPTY `C1=FAIL`, exit 1); direct `--check` failure: `SPANS_FILE_STALE`/`SPANS_FILE_ORPHAN`, `STALE=2`, exit 1 | expected values: `corpus/evidence/round56/claims.md` R56-C1; `c1-gate.py` pins `CAPTURE_TEXT_SHA`, four OLE digests and `BASE_REV`; battery `corpus/evidence/round56/battery/`; committed round-54/55 span manifests and files | builder writes only `DIR/spans.tsv` and `DIR/spans/`; `--check` read-only; gate/counter run artifacts under `--work` or TMPDIR | chousa |
```

Residual risk: the proposed self-test cell accurately names the frozen lane counter and its target, but the strict PROTOCOL self-invocation wording may require a gate-owned self-test mode rather than an external counter. Verification gap: full `c1-count.py` after-measurement was not run by this reviewer; cite its committed after-receipt only once settled.

VERDICT: `build-spans --check` and `c1-gate.py` are demonstrated fail-capable gates; recommend append-only re-registration with the frozen C1 counter as the named self-test, subject to the self-invocation interpretation above.
