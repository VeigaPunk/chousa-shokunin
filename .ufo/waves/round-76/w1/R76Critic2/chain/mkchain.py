"""Build a scratch copy of the FROZEN matrix-battery-v3.py with only the subject lists
replaced. Everything else (run_matrix, scoring, predicate) is the frozen bytes.
The copy keeps the name matrix-battery-v3.py so a subject's grandparent cmdline
names the battery exactly as it does in a real run.

usage: mkchain.py '{"out": DIR, "positives": [[name, path]...], "forgers": [[name, path]...]}'
"""
import json
import pathlib
import sys

FROZEN = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/matrix-battery-v3.py")
spec = json.loads(sys.argv[1])
out = pathlib.Path(spec["out"])
out.mkdir(parents=True, exist_ok=True)
src = FROZEN.read_text()
marker = '\n\nif __name__ == "__main__":'
assert src.count(marker) == 1
override = ("\n# ---- R76Critic2 scratch chain override: subject lists only; frozen file untouched ----\n"
            "import pathlib as _pl\n"
            "POSITIVES = [(n, _pl.Path(p)) for n, p in " + repr([tuple(x) for x in spec["positives"]]) + "]\n"
            "FORGERS = [(n, _pl.Path(p)) for n, p in " + repr([tuple(x) for x in spec["forgers"]]) + "]\n")
(out / "matrix-battery-v3.py").write_text(src.replace(marker, override + marker))
print("chain battery written:", out / "matrix-battery-v3.py")
