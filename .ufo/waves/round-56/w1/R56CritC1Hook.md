# R56CritC1Hook — C1 audit-hook bypass

## Counterexample: native extension import bypasses the read hook

`c1-gate.py` installs its hook at lines 90–115. `BAD` includes process-creation and `ctypes` events; `PATHS` checks only `open`, `os.listdir`, and `os.scandir` paths (lines 93–95, 96, 110–114). There is no check for the `import` audit event. The gate invokes the candidate tool in the same hooked interpreter (`runpy.run_path`, line 117), with `sys.prefix` and its descendants in `ALLOW` (build environment, lines 200–205).

I tested `importlib.machinery.ExtensionFileLoader` using the installed `math` extension at `/usr/lib/python3.14/lib-dynload/math.cpython-314-x86_64-linux-gnu.so`, which is beneath the gate's allowed `/usr` prefix. The scratch printing-hook probe emitted exactly:

```text
AUDIT import ('math', '/usr/lib/python3.14/lib-dynload/math.cpython-314-x86_64-linux-gnu.so', None, None, None)
LOADED /usr/lib/python3.14/lib-dynload/math.cpython-314-x86_64-linux-gnu.so 3.0
```

No `open`, `ctypes.dlopen`, or other event was raised. The extension module was loaded and its function executed. This concretely establishes an unchecked native-load route, not just a theoretical concern.
Reproducer tool source (its only non-stdlib input is the builder path):

```python
import importlib.util
import importlib.machinery
import runpy
import sys

spec0 = importlib.util.find_spec("math")
loader = importlib.machinery.ExtensionFileLoader("math", spec0.origin)
spec = importlib.util.spec_from_file_location("math", spec0.origin, loader=loader)
module = importlib.util.module_from_spec(spec)
loader.exec_module(module)
print("NATIVE_LOADED", spec0.origin, module.sqrt(9))
builder = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py"
sys.argv[0] = builder
runpy.run_path(builder, run_name="__main__")
```

The independent event probe attached an audit printer after resolving the same extension and printed the two lines above. The gate run itself is the operative evidence that this probe leaves the behavioral legs intact.


Scratch probe: `/fast/scratch/hyaku/chousa-r56/R56CritC1Hook/probe-native.py` loads `math` through `ExtensionFileLoader`, then runs the unchanged lane builder. The required gate run, with an empty scratch work directory:

```text
$ python3 /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round56/c1-gate.py --tool /fast/scratch/hyaku/chousa-r56/R56CritC1Hook/probe-native.py --seed 7 --per-leg 2 --work /fast/scratch/hyaku/chousa-r56/R56CritC1Hook/work-native
 tool=/fast/scratch/hyaku/chousa-r56/R56CritC1Hook/probe-native.py sha256=69ba44b3863351176cc8dfdc6692f601c08cb4092e6fa91b777fb68714b7eb45 seed=7 per-leg=2
GENOLE=PASS 2 docs, 4 quotes
OLEPIN=PASS 4 captures, 8 quotes
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical
LEGS=4/4
C1=PASS
```

This passes every leg while loading native code without a denied event. It does not show arbitrary untrusted `.so` execution: the tested library is within the prefix already allowed by the gate. The bypass is that import-time native execution is not separately constrained by the path hook (and the candidate can select any extension reachable within that broad prefix).

## Candidate audit-event disposition

| Candidate | Observed event / gate disposition |
|---|---|
| `ExtensionFileLoader` | Printing-hook probe above: `import`; not in `BAD` or `PATHS`, so allowed. Gate probe above: all 4 legs pass. **Bypass.** |
| `sqlite3.connect('/etc/hostname')` | Printing-hook probe observed `sqlite3.connect ('/etc/hostname',)` and `sqlite3.connect/handle`; neither is checked, so the hook would not deny the attempt. The file was not a SQLite database (`DatabaseError: file is not a database`), so this only proves an unchecked open attempt, not successful content extraction. |
| `os.stat('/etc/hostname')` | Printing-hook probe observed no audit event; metadata access succeeds, and this hook cannot deny it. It is metadata disclosure, not a file-content read. |
| Existing P1 `_posixsubprocess.fork_exec` | `BAD` explicitly contains `_posixsubprocess.fork_exec` (gate lines 93–95); denied. Frozen probe identified by claims lines 69–75. |
| Existing P2 `os.chdir` + dirfd | `os.chdir` is explicitly in `BAD` (lines 93–95); denied before the later dirfd read. Frozen probe identified by claims lines 69–75. |

I did not run the remaining speculative candidates from the prompt; no disposition is claimed for them. The valid-extension event probe was `/fast/scratch/hyaku/chousa-r56/R56CritC1Hook/native-event.py`; the separate exploratory probe observed the SQLite and stat events. All probes and gate work directories were under the assigned scratch root.

## Smallest safe correction

Do not treat Python audit hooks as a security boundary against an adversarial tool executing in the same interpreter: a candidate can load native code and native code can bypass Python-level mediation. The smallest robust correction is process isolation at the OS boundary (e.g., an isolated worker with filesystem and process restrictions), not adding one more Python event name. As a narrow defense-in-depth improvement, deny extension-module imports unless their resolved path is explicitly trusted; this does not make the in-process hook a complete sandbox.

**VERDICT: C1 hook closure is falsified by an allowed `import` event loading native code; probe passes all four gate legs.**
