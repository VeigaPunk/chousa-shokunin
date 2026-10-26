#!/usr/bin/env python3
"""build-c1-controls — score the frozen round-53 C1 counter on the base tool and
four cheap controls, each built in a scratch dir under $TMPDIR (never the lane):

  BASE      tools/assimilate-rows.py at BASE_REV (git show), unchanged;
  CONST     prints nothing, exit 0 (the do-nothing tool);
  REFUSE    prints `REFUSED registry has no \\`## Registry\\` heading` on stderr, exit 1, always;
  RELABEL   BASE with only the label work done: the same-run branch says `twin`
            and the count line gains `TWIN=` (no recheck pre-pass, no ordering,
            no no-`--entry` refusal) -- the cheapest partial patch;
  ALLTWIN   BASE with every non-append row labelled `twin` and the count line
            `HELD=0 TWIN=<all non-append>` (a label keyed on "not appended").

Every control must print C1=FAIL; RELABEL shows the RECHECK/ORDER/NOENTRY legs
are not carried by the label legs. Output: one block per control.
Usage: python3 corpus/evidence/round53/controls/build-c1-controls.py [--seed N]
"""
import pathlib
import shutil
import subprocess
import sys
import tempfile

LANE = pathlib.Path(__file__).resolve().parents[4]
BASE = "5b550133d79bc09c82d8965cce2e48c2598b8c3e"
COUNTER = LANE / "corpus/evidence/round53/c1-count.py"
seed = sys.argv[sys.argv.index("--seed") + 1] if "--seed" in sys.argv else None

base_src = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE}:tools/assimilate-rows.py"],
                          capture_output=True, text=True, check=True).stdout
OLD_TWIN = '        elif u in by_url:\n            mapping[sid] = (by_url[u], "held")\n'
OLD_COUNT = '    print(f"CITED={len(cited)} APPEND={len(rows)} HELD={len(cited) - len(rows)}")\n'
OLD_HELD = '        if u in held:\n            mapping[sid] = (held[u], "held")\n'
assert OLD_TWIN in base_src and OLD_COUNT in base_src and OLD_HELD in base_src, "base tool shape changed"
relabel = base_src.replace(OLD_TWIN, OLD_TWIN.replace('"held"', '"twin"')).replace(
    OLD_COUNT, '    print(f"CITED={len(cited)} APPEND={len(rows)} '
               'HELD={sum(1 for v in mapping.values() if v[1] == \'held\')} '
               'TWIN={sum(1 for v in mapping.values() if v[1] == \'twin\')}")\n')
alltwin = base_src.replace(OLD_TWIN, OLD_TWIN.replace('"held"', '"twin"')).replace(
    OLD_HELD, OLD_HELD.replace('"held"', '"twin"')).replace(
    OLD_COUNT, '    print(f"CITED={len(cited)} APPEND={len(rows)} HELD=0 TWIN={len(cited) - len(rows)}")\n')
tools = {
    "BASE": base_src,
    "CONST": "import sys\nsys.exit(0)\n",
    "REFUSE": "import sys\nprint('REFUSED registry has no `## Registry` heading', file=sys.stderr)\nsys.exit(1)\n",
    "RELABEL": relabel,
    "ALLTWIN": alltwin,
}
work = pathlib.Path(tempfile.mkdtemp(prefix="chousa-r53-c1ctl-"))
try:
    for name, src in tools.items():
        p = work / name.lower() / "assimilate-rows.py"
        p.parent.mkdir()
        p.write_text(src, encoding="utf-8")
        args = [sys.executable, str(COUNTER), "--tool", str(p)] + (["--seed", seed] if seed else [])
        r = subprocess.run(args, capture_output=True, text=True)
        summary = [l for l in r.stdout.splitlines() if "=" in l.split(" ")[0] and " " not in l.strip()]
        print(f"# control {name}")
        print("\n".join(summary))
        print(f"exit={r.returncode}\n")
finally:
    shutil.rmtree(work, ignore_errors=True)
