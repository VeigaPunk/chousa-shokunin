# R56ConnSiblings — sibling overlap scan (round 56 wave 1)

## Command and targets
Searched 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin/` (excluding `chousa-shokunin`) across target paths (`corpus/` [20] and `tools/` [8] — 28 directory roots).
Terms: `药品临床综合评价`, `灰色文献`, `ttbz.org.cn`, `中国循证医学中心`, `证据分级`, `build-spans`, `audit hook`, `addaudithook`, `mutation battery`.

```bash
python3 -c '
import glob, os, subprocess
base = "/home/vgpnk/Projects/shokunin"
lanes = sorted([d for d in glob.glob(f"{base}/*-shokunin") if os.path.isdir(d) and not d.endswith("/chousa-shokunin")])
targets = [os.path.join(l, s) for l in lanes for s in ["corpus", "tools"] if os.path.exists(os.path.join(l, s))]
terms = ["药品临床综合评价", "灰色文献", "ttbz.org.cn", "中国循证医学中心", "证据分级", "build-spans", "audit hook", "addaudithook", "mutation battery"]
for t in terms:
    res = subprocess.run(["rg", "-n", "-F", t] + targets, capture_output=True, text=True)
    hits = [h for h in res.stdout.strip().splitlines() if h]
    print(f"{t}: {len(hits)} hits")
'
```
Observed output:
```
药品临床综合评价: 0 hits
灰色文献: 0 hits
ttbz.org.cn: 0 hits
中国循证医学中心: 0 hits
证据分级: 0 hits
build-spans: 0 hits
audit hook: 0 hits
addaudithook: 6 hits
mutation battery: 42 hits
```

## Counts per lane
14 sibling lanes returned 0 hits across all terms (`game-dev-2d`, `game-dev-3d`, `kagi`, `kaidoku`, `kake`, `kasegi`, `kotoba`, `kumitate` [non-battery], `lore`, `mado`, `revenger`, `souji`, `tabi`, `tameshi`).
Hits occurred in 6 lanes:
- `audio-shokunin`: `mutation battery=7` (critic verifiers `corpus/live/r87-critic/` to `r90-verifier/`)
- `kama-shokunin`: `mutation battery=1` (`tools/shortcut-tally.py:8` auditing disclosed mutant counts)
- `kengaku-shokunin`: `mutation battery=27` (`corpus/evidence/round10-fleet/` through `round14-fleet/` on `grader.py` self-tests S7)
- `kotodama-shokunin`: `addaudithook=6` (`tools/gates/expected/d4-assembly-check-gate/r19-pre/`, `d4-typed-labels-check-gate/r19-pre/`, `r20-post/`)
- `kumitate-shokunin`: `mutation battery=4` (`corpus/QUALITY.md:329` Q25 single kill predicate rule, `corpus/lessons/round-42.md:1`, `round-51-verifier-spotcheck.md:35`)
- `mori-shokunin`: `mutation battery=1` (`corpus/lessons/round-12.md:186`)
- `tsukuroi-shokunin`: `mutation battery=2` (`corpus/SOURCES.md:153` S147 Pitest reject, `corpus/lessons/round-28.md:12`)

## Hit characterization and ownership analysis
1. **Documents (C2)**: Zero sibling overlap. No sibling holds the standard text `T/CLPA XXXX-2025` on `ttbz.org.cn`, the explanatory note, the journal copy in 中国药房, or the NHC 2020 guidelines. Sibling lanes explicitly defer research methodology, search strategy, and citation hierarchy to `chousa-shokunin` (`souji-shokunin/PROVINCE.md:82`, `kotoba-shokunin/PROVINCE.md:57`, `kengaku-shokunin/PROVINCE.md:137`).
2. **Gate-clause-coverage tools (C1)**: Zero sibling overlap.
   - `kotodama-shokunin`'s 6 `addaudithook` hits are static strings recording passive read-set traces (`sys.addaudithook("open")` in scratch scripts), not execution-enforcement gate hooks.
   - Sibling `mutation battery` hits represent domain-specific regression self-tests or historical scorecard audits.
   - Testing specialist `tameshi-shokunin` owns mutation method documentation but explicitly refuses product domains and sibling gate implementations (`tameshi-shokunin/PROVINCE.md:15-18`, "report, never absorb").
   - No sibling holds a gate-clause-coverage tool for span builders or quote extractors.

## Connector proposal
- **Affected axes**: Operability (C1, lowest scored 3/10), Depth (C2), Calibration.
- **Evidence**: `chousa-shokunin/corpus/evidence/round56/c1-gate.py:93-95` enforces audit hooks denying `_posixsubprocess.fork_exec` (P1) and `os.chdir` (P2) with `exit 97` (`AUDIT_FORBIDDEN`). `tools/build-spans.py:9,56-60` extracts text from `.raw` OLE/zip files by importing `tools/capture-text.py` in-process (`importlib.util.spec_from_file_location`), without spawning child processes.
- **Proposed move**: Maintain the strict in-process import contract for capture extraction in `build-spans.py` rather than delegating via `subprocess`. This guarantees that `build-spans.py` executes cleanly under `c1-gate.py`'s audit hook without triggering `AUDIT_FORBIDDEN _posixsubprocess.fork_exec`, simultaneously preserving C1 gate operability and C2 raw span generation.
- **Second-order effects**:
  - *Runtime*: Zero subprocess spawn overhead when indexing OLE/zip documents across corpus expansion batches.
  - *Contract*: `c1-gate.py` retains fail-closed enforcement against execution escapes without needing special-case allowlists for child tools.
  - *Substrate*: Eliminates temporary file/pipe leakage in scratch environments.
  - *Verification*: Probe P1 confirms subprocess bypasses are denied (`DENIED=2/2`), while candidate builder passes all legs (`CANDIDATE=2/2`).
- **Risks**: In-process parser failure in `capture-text.py` could crash the builder process; mitigated by existing exception guard in `build-spans.py:83-84`.
- **Verification**: `python3 corpus/evidence/round56/c1-count.py` verifies `CANDIDATE=2/2 KILLED=9/9 DENIED=2/2 C1=PASS`.

VERDICT: Sibling overlap scan complete — 0 document or gate-clause-coverage tool overlaps across 20 sibling lanes; in-process capture import synthesis confirmed.
