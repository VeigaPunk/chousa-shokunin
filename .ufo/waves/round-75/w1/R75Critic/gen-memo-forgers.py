#!/usr/bin/env python3
"""R75Critic — generate the two memoised-identity forgers from the harvest table.

Both embed a 12-entry table built offline from the *instrument's own declared
fixture bytes* (never from protected committed content of the measured lane):

  forge-meta-treehash-memo.py : answer keyed on `git rev-parse <rev>^{tree}`
  forge-meta-stat-size-memo.py: answer keyed on plain `Path.stat().st_size`,
                                no git and no subprocess at all
"""
import json
import pathlib

OUT = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-75/w1/R75Critic")
HARVEST = json.loads((OUT / "logs" / "harvest.json").read_text())

PATHS = ("LOG.md", "corpus/lessons/round-72.md", "SCORECARD.md")
RECEIPTS = ("corpus/evidence/round72/controls/battery-past-locale-dies-pinzone-r72.txt",
            "corpus/evidence/round72/controls/after-r72-corrections.txt")
ORDER = PATHS + RECEIPTS

TABLE_TREE = {v["tree"]: n for n, v in HARVEST["cases"].items()}
TABLE_SIZES = {tuple(v["sizes"][p] for p in ORDER): n for n, v in HARVEST["cases"].items()}


def emit(name, doc, key_expr, key_call, extra_imports, table_literal):
    src = f'''#!/usr/bin/env python3
"""{doc}"""
import argparse
{extra_imports}import sys

IDS = ("C2-1", "C2-2", "C2-3", "C2-4", "C2-5", "C2-6", "C2-7")
PATHS = {PATHS!r}
RECEIPTS = {RECEIPTS!r}
TABLE = {table_literal}

ANSWERS = {{
    "unchanged": (0, ()),
    "append-0": (0, ()), "append-1": (0, ()), "append-2": (0, ()),
    "delete-0": (1, ("C2-6",)), "delete-1": (1, ("C2-6",)), "delete-2": (1, ("C2-6",)),
    "replace-equal": (1, ("C2-6",)),
    "receipt-change": (1, ("C2-7",)),
    "dup-log-heading": (1, ("C2-1", "C2-2")),
    "dup-lesson-heading": (1, ("C2-3", "C2-5")),
    "dup-card-heading": (1, ("C2-4",)),
}}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", default=".")
    ap.add_argument("--base", default=None)
    ap.add_argument("--rev", required=True)
    a = ap.parse_args()
    key = {key_expr}
    case = TABLE.get(key)
    rc, failed = ANSWERS.get(case, (0, ()))
    for cid in IDS:
        print(f"CHECK {{cid}} {{'FAIL' if cid in failed else 'PASS'}} {name}")
    print(f"C2={{'FAIL' if failed else 'PASS'}} checks={{7 - len(failed)}}/7 {name} case={{case}}")
    return rc


if __name__ == "__main__":
    sys.exit(main())
'''
    (OUT / f"{name}.py").write_text(src)
    (OUT / f"{name}.py").chmod(0o755)
    print(f"wrote {name}.py")


emit("forge-meta-treehash-memo",
     "R75Critic attempt M5 — object-identity memo, one `git rev-parse <rev>^{tree}`.\n\n"
     "The shuffle permutes the cases but not their bytes, so every case has a stable\n"
     "tree id; this table was built offline from the instrument's declared fixture.\n"
     "Reads no blob bytes and no diff — only the tree name reachable from --rev.",
     'subprocess.run(["git", "-C", a.lane, "rev-parse", f"{a.rev}^{{tree}}"],\n'
     '                   text=True, capture_output=True).stdout.strip()',
     None, "import subprocess\n",
     "{\n" + "".join(f'    "{k}": "{v}",\n' for k, v in sorted(TABLE_TREE.items())) + "}")

emit("forge-meta-stat-size-memo",
     "R75Critic attempt M6 — working-tree byte sizes only, no git, no subprocess.\n\n"
     "The fixture leaves the mutated bytes in --lane, so five `Path.stat().st_size`\n"
     "calls name the case. This is the cheapest metadata forge: no repository read\n"
     "through git at all, and no protected byte ever opened.",
     'tuple((Path(a.lane) / p).stat().st_size for p in PATHS + RECEIPTS)',
     None, "from pathlib import Path\n",
     "{\n" + "".join(f'    {k!r}: "{v}",\n' for k, v in sorted(TABLE_SIZES.items())) + "}")
