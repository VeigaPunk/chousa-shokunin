# R55ConnPattern — Cross-Round Pattern on RW-1 (Forgeable Frozen Counter)

Seat: `R55ConnPattern` | Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` | Date: 2026-10-27

## 1. Evidence: C1 Counter Inventory and Ledger Baseline

Command run: `ls -l corpus/evidence/round{49,50,51,52,53,54,55}/c1-count.py corpus/evidence/round53/recurring.tsv`
```
-rwxr-xr-x 1 vgpnk vgpnk 18436 Oct 25 17:00 corpus/evidence/round49/c1-count.py
-rw-r--r-- 1 vgpnk vgpnk  7463 Oct 25 18:33 corpus/evidence/round50/c1-count.py
-rwxr-xr-x 1 vgpnk vgpnk 12457 Oct 25 19:53 corpus/evidence/round51/c1-count.py
-rwxr-xr-x 1 vgpnk vgpnk 16921 Oct 26 19:56 corpus/evidence/round52/c1-count.py
-rwxr-xr-x 1 vgpnk vgpnk 18578 Oct 26 20:53 corpus/evidence/round53/c1-count.py
-rwxr-xr-x 1 vgpnk vgpnk 15649 Oct 26 22:23 corpus/evidence/round54/c1-count.py
-rwxr-xr-x 1 vgpnk vgpnk 21911 Oct 27 00:39 corpus/evidence/round55/c1-count.py
-rw-r--r-- 1 vgpnk vgpnk   178 Oct 26 21:22 corpus/evidence/round53/recurring.tsv
```

## 2. Cross-Round Matrix: C1 Counters (Rounds 49–55)

| Round | Oracle/Expected Values During Tool Run | Generated Inputs Beside Tool Input | Reads Audited | REGRESS Hooked | Breaking Forge & Lesson / Spotcheck Citation |
|---|---|---|---|---|---|
| R49 | Memory only (`c1-count.py:215-223` computes `want` mapping after tool run) | No (static pinned files `PINS`, `PKG / SOURCES.append.md`) | No (`subprocess.run`) | No REGRESS leg | Replay of golden outputs (`round-49.md:21`, W1 `CritForgeC1.md`) |
| R50 | Disk: `dst / "expected.json"` (`:97,119`); memory: hardcoded finding regexes (`:107-112`) | Yes (mutated fixtures & `expected.json` sit in `dst`) | No (`subprocess.run`) | No (`c1-count.py:138-141` unhooked subprocess) | Literal regex matcher printing 6 DIFF lines (`round-50.md:153`, `round-51.md:15`, W2 `R50CritForgeC1`, `forge-tool.py`) |
| R51 | Memory (random variables `top`, `held_n`, `new_a`) + Disk: `R50_FIX/expected.json` (`:113`) | Yes (`staged.md`, `registry.md`, `out` sit in predictable dirs `"s"`, `"d1"`, `:141,167`) | No (`subprocess.run`) | No (`LEGACY_ALL` unhooked subprocess) | Dirname forge keying on `--out` folder name (`round-51.md:22`, `round-51-verifier-spotcheck.md:100`, W1 `R51CritForgeC1`, `forge-dirname.py`) |
| R52 | Memory (`want` strings returned by generators `:274,290`; string locate for `REAL_QUOTE` `:324`) | No (in-memory zip packages written to isolated files `:261-263`) | No (`subprocess.run`) | No REGRESS leg | Generator XML-spelling matcher with canned REAL (`round-52.md:16`, `round-52-verifier-spotcheck.md:34`, W1 `R52CritForgeC1`, `forge-shape.py`) |
| R53 | Memory (`expect()` map `:189`; hardcoded `REAL_MAP` `:57`) + Disk: `R50_FIX/expected.json` (`:312`) | Yes (`staged.md`, `registry.md`, `out` sit in `d` `:207-236`) | No (`subprocess.run`) | No (`c1-count.py:316` unhooked subprocess) | Canned REAL on pinned digest + bad-date regex stubbing (`round-53.md:19`, `round-53-verifier-spotcheck.md:27`, W1 `R53CritForgeC1`, `forge-c1.py`) |
| R54 | Disk: `c.work / "oracle" / f"{k}.txt"` (`:251-257`) & `c.work / "src-..." / "*.html"` (`:119-140`) | Yes (`src-gen` beside `doc-gen`, `oracle` beside `real` in `c.work`) | No (hook `:68-76` traps spawn/socket, not file open/scan or ctypes) | No (`c1-count.py:287-290` unhooked subprocess) | Sibling-HTML reader with canned REAL exports (`round-54.md:17`, `round-54-verifier-spotcheck.md:44,56`, W1 `R54CritForgeC1`, `build-c1-forge.py`) |
| R55 | Memory only (`expect` list `:285,301`; `oracle_form()` called in memory; nothing written to disk) | No (`gen_docs()` deletes tree via `shutil.rmtree(g)` `:220`; isolated `.raw` in cache) | Yes (`c1-count.py:81-109`: `open`, `listdir`, `scandir` audited against `ALLOW`) | Yes (`leg_regress` `:411` runs under `c.hook`) | No round-55 forge landed (controls `r54shim` 1/4, `txtonly` 1/4, `delegate` 0/4 fail under `build-c1-controls.py`) |

## 3. Mechanisms Closed vs. Mechanism Classes Remaining Open in Round 55

### A. Mechanisms Closed by Round-55 Counter (`c1-count.py`)
1. **Sibling Generator Leakage:** `gen_docs()` immediately removes generation trees with `shutil.rmtree(g)` (`:220`) before tool execution; target files sit alone in `cache/<hash>.raw`.
2. **On-Disk Expected Text / Oracles:** Expected text slices and character offsets reside solely in Python memory (`expect` list `:285,301`).
3. **Un-Audited Filesystem Access:** Hook traps `open`, `os.listdir`, and `os.scandir` (`:87`), terminating on paths outside `ALLOW` with exit 97 (`:89-90`).
4. **ctypes Dynamic Library Bypass:** Hook traps `ctypes.dlopen`, `ctypes.dlsym`, and `ctypes.cdata` (`:85-86`), blocking in-process libc `system()` delegation.
5. **Unhooked REGRESS Leg:** `leg_regress` runs `c.tool` explicitly wrapped by `c.hook` (`:411-413`).
6. **Predictable Paths / Fixed URLs:** Run directories use random 8-hex suffixes (`:183`) and cache entries use SHA-256 URL hashes (`:120`).

### B. Concrete Mechanism Classes Remaining Open
1. **Low-Level C-Extension Child Process Execution (`_posixsubprocess.fork_exec`):**
   `BAD` (`c1-count.py:84-86`) enumerates high-level spawn APIs (`subprocess.Popen`, `os.system`, `os.exec`, `os.posix_spawn`, `os.spawn`, `os.fork`, `os.forkpty`, `pty.spawn`, `socket.connect`, `socket.bind`, `ctypes.dlopen`, `ctypes.dlsym`, `ctypes.cdata`), but omits `_posixsubprocess.fork_exec`. Because `_posixsubprocess` is a C extension in the standard library (`sys.prefix`, whitelisted in `ALLOW`), calling `_posixsubprocess.fork_exec(...)` directly executes child processes (verified in scratch: spawned `/bin/echo` with exit 0, bypassing `AUDIT_FORBIDDEN`).
2. **Static Capture Digest Recognition (`leg_olepin`):**
   The four pinned `.raw` captures (`54fe0734...`, `6dc68fd6...`, `b539a802...`, `bdff491a...`, `c1-count.py:72-76`) have fixed sha256 digests. Because the tool is permitted to read `.raw` files in its cache, a tool can compute the sha256 of each input file and return hardcoded defined text forms without parsing OLE structures.
3. **Un-Audited Metadata Probing (`os.stat` / `pathlib.Path.stat`):**
   `PATHS` checks only `open`, `os.listdir`, and `os.scandir`. `os.stat` and `os.lstat` remain un-audited, allowing out-of-sandbox existence and file-size checks.

## 4. Recurring Weakness Ledger Update (RW-1)

Command run on scratch update table:
`python3 corpus/evidence/round53/weakness-streak.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin --table <scratch_table>`
Output observed:
```
OK   RW-1 streak=7 claimed=7 first_in_run=49 routed=corpus/evidence/round55/c1-count.py frozen counter forgeable
OK   RW-3 streak=0 claimed=0 first_in_run=- routed=- stray write outside scratch
WEAKNESS_ROWS=2 FAILING=0
```

Draft update for `corpus/evidence/round55/recurring.tsv` (or successor `recurring.tsv`, TAB-separated):
```tsv
RW-1	frozen counter forgeable	forg(e|ed|able|ery)	corpus/evidence/round55/c1-count.py	7
RW-3	stray write outside scratch	relative redirect|fleet root|misroot|fleet-root	-	0
```
Status: RW-1 streak advances to 7 because `corpus/lessons/round-55.md:16,20` hits `forg(e|ed|able|ery)` (exposure). Routed path advances to `corpus/evidence/round55/c1-count.py` (which exists). Six prior forge channels are closed, but internal C-extension process spawning and pinned digest recognition remain open.

VERDICT: attacked cross-round forgeable counter pattern RW-1 across rounds 49–55; verified closure of six past leakage mechanisms and identified open `_posixsubprocess.fork_exec` and pinned-hash memoisation classes; drafted streak-7 recurring table update passing weakness-streak check.
