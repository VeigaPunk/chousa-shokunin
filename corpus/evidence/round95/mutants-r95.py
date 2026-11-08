#!/usr/bin/env python3
"""mutants-r95 — the R95MutantsC1 survivors, rebuilt against the amended tool and scored by the amended battery.

Each mutant is one exact substring replacement in `tools/search-rerun.py` (asserted to apply exactly once), written
under --work and handed to `rerun-controls-r95.py --tool`. A mutant is KILLED when the battery prints
`RERUN_CONTROLS=FAIL`. m10-m17 are the wave seat's survivors (m12 was equivalent and is not rebuilt); m18-m20 are
the amendment's own new legs (grep line rule, dotfile rule, caller GIT_* scrub).

Usage: python3 -B corpus/evidence/round95/mutants-r95.py --root LANE --work DIR
Prints one MUTANT line per mutant and `MUTANTS_KILLED=k/n`; exit 0 when every mutant is killed, 1 otherwise,
2 setup (a replacement that does not apply exactly once).
"""
import argparse
import os
import shutil
import subprocess
import sys

MUTANTS = {
    "m10-whole-file": ("    for line in lines_of(data):\n", "    for line in [data]:\n"),
    "m11-ci-fixed": ('            if r["needle"] in line:', '            if r["needle"].lower() in line.lower():'),
    "m13-hits-len-set": ('        if len(at_rev) != r["n"]:',
                         '        if len(at_rev) != (len(r["set"]) if "set" in r else r["n"]):'),
    "m14-revok-mask": ('        rev_ok += 0 if ("COUNT_DRIFT" in codes or "SET_DRIFT" in codes) else 1',
                       "        rev_ok += 1"),
    "m15-tree-count": ("        changed = at_tree != at_rev", "        changed = len(at_tree) != len(at_rev)"),
    "m16-set-dedup": ('        elif sorted(r["set"]) != at_rev:', '        elif set(r["set"]) != set(at_rev):'),
    "m17-fnmatch": ("        if len(pats) == len(segs) and all(seg_match(s, p) for s, p in zip(segs, pats)):",
                    '        if __import__("fnmatch").fnmatchcase(path, g):'),
    "m18-phantom-line": ("    if lines and lines[-1] == b\"\":\n        lines.pop()\n", ""),
    "m19-dotglob": ('    if name.startswith(".") and not pat.startswith("."):\n        return False\n', ""),
    "m20-no-env-scrub": ('    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}',
                         "    env = dict(os.environ)"),
}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    work = os.path.join(os.path.realpath(a.work), "mutants-r95")
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    try:
        src = open(os.path.join(root, "tools/search-rerun.py"), encoding="utf-8").read()
        killed = 0
        for name, (old, new) in MUTANTS.items():
            if src.count(old) != 1:
                print(f"SETUP mutant {name} applies {src.count(old)} times")
                return 2
            mp = os.path.join(work, name + ".py")
            open(mp, "w", encoding="utf-8").write(src.replace(old, new))
            p = subprocess.run([sys.executable, "-B", os.path.join(root, "corpus/evidence/round95/rerun-controls-r95.py"),
                                "--root", root, "--work", os.path.join(work, "w-" + name), "--tool", mp],
                               capture_output=True, text=True)
            tally = next((ln for ln in p.stdout.splitlines() if ln.startswith("POSITIVE=")), "")
            dead = "RERUN_CONTROLS=FAIL" in p.stdout
            failed = " ".join(f for f in tally.split() if f.split("=")[1].split("/")[0] != f.split("/")[-1])
            print(f"MUTANT {name} {'KILLED' if dead else 'SURVIVED'} rc={p.returncode} failed_groups={failed or '-'}")
            killed += 1 if dead else 0
        print(f"MUTANTS_KILLED={killed}/{len(MUTANTS)}")
        return 0 if killed == len(MUTANTS) else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
