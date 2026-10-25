# SentScopeAudit — round 47 wave 1 (sentinel: scope + egress)

Item: audit `tools/inference-ground.py`, `corpus/evidence/round47/c{1,2,3}-count.py`, `corpus/evidence/round47/controls/*.py`
for egress, write paths, and attacker-code execution under `--root`; name fleet-root untracked files about chousa round 47.
Tree: lane HEAD `a15610a` (no working-tree change to any audited file). Python 3.14.8; PYTHONDONTWRITEBYTECODE/PYTHONPYCACHEPREFIX unset.
Tools installed: none. Scratch `/tmp/chousa-r47-SentScopeAudit/` was created and then deleted (`ls` afterwards: No such file).

## Verdict
- **Egress:** none of the audited files can egress when `--root` is the lane. No file imports `urllib`, `requests`,
  `socket` or `http.client`, and none calls `curl`, `wget` or `os.system`.
- **Execution:** with `--root` pointing at an attacker tree, all three counters execute attacker code with user privileges.
  That includes c2, despite its sha256 pin: a forged `.pyc` bypasses the pin, and I forged `C2=PASS MISMATCHES=0` this way.
- **Closure re-run:** this matters only if the tree the closure measures carries the attacker bytes. Two cases do:
  - a `.pyc` committed under `corpus/evidence/round46/__pycache__/`. The lane already tracks committed `.pyc` files
    under `corpus/evidence/round35/__pycache__/`, so a forced add is not hypothetical.
  - a re-run inside a working tree that has a pre-populated `__pycache__`.
- **Misroot:** none. No untracked fleet file names chousa round 47.

## Hits (grep: urllib|requests|socket|http.client|curl|wget|os.system|subprocess|exec|write)
| file:line | hit | can egress? | write outside scope? |
|---|---|---|---|
| c1-count.py:68 | `subprocess.run(tool …)`, where tool = `root/tools/inference-ground.py` or `--tool` | only through the executed tool | only through the executed tool |
| c1-count.py:113 | `subprocess.run(root/corpus/evidence/round46/c1-count.py)` — **not sha-pinned** | only through the executed child | only through the executed child |
| c1-count.py:119 | `subprocess.run(root tool …)` for the two R46 entries | only through the executed tool | only through the executed tool |
| c1-count.py:105-108 | `tempfile.TemporaryDirectory` + `shutil.copyfile` | no | system tmp, removed automatically |
| c2-count.py:58-64 | `read_bytes`, then sha256, then `spec_from_file_location` + `exec_module`, i.e. imports root/round46/c2-count.py | only through the imported code | **yes**: an implicit `.pyc` write to `root/corpus/evidence/round46/__pycache__/` |
| c3-count.py:173 | `subprocess.run(root/tools/inference-ground.py …)` | only through the executed tool | only through the executed tool |
| c3-count.py:46,150-154 | reads the absolute `CACHE` path under shokuknow | no | no (read only) |
| inference-ground.py:449 | `--json` → `write_text(path)` to an operator-chosen path | no | only if a caller passes `--json`. No counter does. |
| controls/base-tool-r46.py:305 | the same `--json` write | no | same as above |
| controls/neg-word-refuser.py:7 | `subprocess.run(sibling base-tool-r46.py)`. `runpy` is imported and unused. | no | no |
| controls/always-exit-1.py | prints and exits 1 | no | no |
- **Pyc writes, observed:** the lane has `corpus/evidence/round46/__pycache__/c2-count.cpython-314.pyc` (08:33) and
  `corpus/evidence/round47/__pycache__/c2-count.cpython-314.pyc`. Both are gitignored (`.gitignore:3 corpus/**/__pycache__/`).
- **Hashes:** inference-ground.py `8899e786…0a40` · c1 `6d39dce5…0cc7` · c2 `36b3934e…36d1` · c3 `ce93fe29…c956` ·
  r46 c2 `f93cb107…046f` (= `R46_SHA`) · r46 c1 `524b9eef830d1dbec710ebef75613eff4125d16fe4089d9469cd6c525dc1091e`.

## F1 — HIGH (calibration): the c2 sha256 pin is bypassed by a forged `.pyc`
- **Exploit path:** put the byte-exact round-46 source in the root, so the sha256 check passes. Then plant
  `corpus/evidence/round46/__pycache__/c2-count.cpython-314.pyc` as an *unchecked-hash* pyc.
  `SourceFileLoader` executes the pyc and never reads the source again.
- **Run:** I ran `python3 corpus/evidence/round47/c2-count.py --root <scratch>`. The scratch source hash was `f93cb10795ef7402…`.
  The payload printed a marker and returned 92 entry points, one Gates row and `names()` = True. Output:
  ```
  ATTACKER_CODE_RAN_UNDER_PIN
  ENTRY_POINTS=92 (abc=92 dependence=+0 check_named=+0)  REGISTERED=92/92  UNREGISTERED=0  DANGLING=0  MISMATCHES=0
  C2=PASS   exit=0
  ```
- **Mitigations, both run on the same tree:**
  - `PYTHONPYCACHEPREFIX=<fresh dir>` gives `MISMATCHES=1 C2=FAIL exit=1`, because the source is used.
  - `--check-hash-based-pycs always` gives `C2=FAIL exit=1`.
- **Also: [INFERENCE, not run]**
  - A *timestamp* pyc (flags=0) whose header carries the source's mtime and size also bypasses the pin, and the
    `--check-hash-based-pycs` flag does not stop that variant.
  - There is a second read: the file is read once for the hash (line 58) and again by the loader (line 62).
    That leaves a TOCTOU window against a concurrent writer.
- **Impact:** a tree can print `C2=PASS` with 25 real mismatches.
- **Smallest remediation (the frozen counter is unchanged):** run the closure from a `git archive <stamp>` extraction with
  `PYTHONPYCACHEPREFIX=$(mktemp -d)`. Also assert that `git ls-files '*.pyc' 'corpus/evidence/round46/*'` is empty.
  The prefix also stops the counter from writing a pyc into the measured tree.

## F2 — MEDIUM (calibration): the c1 `R46_COUNTER` leg runs an unpinned instrument from `--root`
- **Code:** `c1-count.py:111-115` executes `root/corpus/evidence/round46/c1-count.py` without a hash check.
  `PINNED` covers fixtures only. Contrast c2, which pins its round-46 instrument.
- **Run:** a `git archive HEAD` extraction (a15610a), with round46/c1-count.py replaced by `print("C1=PASS")` and
  `--tool controls/always-exit-1.py`, gave `R46_COUNTER=pass`. The frozen control record
  `controls/c1-controls.txt` shows `R46_COUNTER=fail` for that tool. Final line `C1=FAIL exit=1`, because the other legs still bind.
- **Impact:** the no-regression leg can be faked by one edit to the round-46 counter. That edit is visible in the lane diff.
- **Smallest remediation:** the closure checks that sha256 of `corpus/evidence/round46/c1-count.py` = `524b9eef…1091e`
  at the stamp before trusting `R46_COUNTER`.

## F3 — INFO/by design: c1 and c3 execute `root/tools/inference-ground.py`, the tool under test
- **Run:** in the archive copy, I replaced the tool with a stub that writes a marker *outside* `--root` and exits 0,
  and added two stub entries. c3 `--lane-only` printed `ENTRIES=2/2 INFERENCE_GROUNDED=2/2`, and the marker file existed.
- **Effect:** an attacker `--root` gets arbitrary code execution, can write outside scope, and can egress.
- **Closure re-run:** running the stamped commit's own tool is the measurement, and its bytes are reviewable in the diff.
  Run it network-isolated as defence in depth [not exercised].

## F4 — LOW: c3 `safe_span` follows symlinks out of the root
- **Code:** `c3-count.py:95-100` rejects `/` and `..` only. Compare `tools/inference-ground.py:181-188`, which also does
  `resolve()` and `relative_to(base)`.
- **Run:** I symlinked `spans/S085-1.txt` to a file outside the root and set the quote to `OUTSIDE-ROOT-42`. Result:
  `QUOTES_IN_SPAN=1/1 SPAN_CONTEXT=1/1`. That is a substring oracle over files the user can read; the output is counts only.
- **[INFERENCE]:** a span symlinked to the capture file itself at offset 0 satisfies `CAPTURE_BOUND`. The span bytes would
  then not be lane bytes.
- **Remediation for the closure:** check that `git ls-files -s corpus/evidence/round47/spans` shows no mode `120000` (symlink) entries.

## F5 — LOW: the inherited `NAMED` regex accepts `../` segments
- **Code:** `round46/c2-count.py:43`; it matches `../x/y.py` but not `/etc/a/b.py`.
- **Run:** c2 over a scratch root whose `QUALITY.md` names `../outside/probe.py` printed
  `UNREGISTERED_PATH ../outside/probe.py` and `check_named=+1`.
- **Effect:** read-only, but out-of-tree files can pad `ENTRY_POINTS` toward `FLOOR`.
- **Closure check:** `UNREGISTERED_PATH` and the Gates rows contain no path starting with `../`.

## Fleet misroot check
`git -C /home/vgpnk/Projects/shokunin status --porcelain` lists 17 `M` and 7 untracked paths:
```
?? .omp/mcp.json  ?? .scratch/goal-20261025-hyaku-12h.md  ?? .ufo/state/{kotoba,kotodama,revenger}.report-baseline
?? .ufo/waves/round-24/  ?? .ufo/waves/round-69/      (files: round-24/w2/RevUnlandedResolution.md, round-69/w1/ScoutAmp.md)
```
- **Round-47 grep:** `grep -lIiE 'round[- _]?47|round47'` over the untracked and the modified files matched nothing (xargs rc=123).
- **Fleet wave directory:** `.ufo/waves/round-47*` does not exist at the fleet root.
- **Chousa mentions:** `.scratch/goal-20261025-hyaku-12h.md:63,72` names chousa *r46*, as an operator orchestration note.
  It is not a misroot.
- **Lane side:** the round-47 artifacts (`.ufo/waves/round-47/{gen-w1-spec.py,w1-dispatch.json,w1-run.err,w1-spec.json,w1/}`)
  are untracked in the lane, which is the correct root.
- **Other hits:** `.jj/repo/op_store/…` and `.jj/working_copy/tree_state` mention chousa round 47, but they are jj's
  internal store, which is ignored, not a misroot.

## Commands run (decisive lines)
- `sha256sum …` gave the hashes above. `git log --oneline -5` returned HEAD `a15610a`, then `22a44b8`.
- `git check-ignore -v corpus/evidence/round46/__pycache__/x.pyc` returned `.gitignore:3:corpus/**/__pycache__/`.
- `git ls-files | grep -c '__pycache__\|\.pyc$'` returned `19`, including `corpus/evidence/round35/__pycache__/c{1,2}-count.cpython-314.pyc`.
- Pyc flags of every `corpus/evidence/round*/__pycache__/*.pyc`: `0`, i.e. all are timestamp pycs.
- The F1–F5 runs are quoted inline above. All ran against scratch copies under `/tmp`; no lane file was modified.
