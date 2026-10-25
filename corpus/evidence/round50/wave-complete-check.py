#!/usr/bin/env python3
"""usage: python3 wave-complete-check.py <wave-spec.json> <report-dir> [--rev REV --lane DIR]

Prints `MISSING <name>` for every spec item whose <name>.md is absent from the
report dir (on disk, or in the lane's git tree at REV), exits 1; exits 0 when
every item has a report; exits 2 on an unusable spec or lane.
"""
import json, os, subprocess, sys


def die(msg):
    print("ERROR " + msg, file=sys.stderr)
    sys.exit(2)


def git(args):
    r = subprocess.run(["git"] + args, capture_output=True, text=True)
    if r.returncode:
        die("git %s: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def names_of(spec, path):
    items = spec.get("items") if isinstance(spec, dict) else None
    if not isinstance(items, list):
        die(path + ": no 'items' list")
    out = []
    for i, it in enumerate(items):
        n = it if isinstance(it, str) else (it.get("name") if isinstance(it, dict) else None)
        if not isinstance(n, str) or not n.strip():
            die("%s: item %d has no 'name'" % (path, i))
        if n not in out:
            out.append(n)
    if not out:
        die(path + ": empty 'items' (an empty wave cannot be complete)")
    return out


def main(argv):
    rev = lane = None
    pos = []
    it = iter(argv[1:])
    for a in it:
        if a == "--rev":
            rev = next(it, None) or die("--rev needs a value")
        elif a == "--lane":
            lane = next(it, None) or die("--lane needs a value")
        else:
            pos.append(a)
    if len(pos) != 2:
        print(__doc__)
        return 2
    spec_path, report_dir = pos
    try:
        spec = json.load(open(spec_path, encoding="utf-8"))
    except (OSError, ValueError) as exc:
        die("%s: %s" % (spec_path, exc))
    names = names_of(spec, spec_path)
    if rev is None:
        found = [n for n in names if os.path.isfile(os.path.join(report_dir, n + ".md"))]
    else:
        lane = lane or os.getcwd()
        commit = git(["-C", lane, "rev-parse", "--verify", rev + "^{commit}"]).strip()
        root = git(["-C", lane, "rev-parse", "--show-toplevel"]).strip()
        rel = os.path.relpath(os.path.realpath(report_dir), os.path.realpath(root))
        if rel == ".." or rel.startswith(".." + os.sep):
            die("report dir %s is outside lane %s" % (report_dir, lane))
        pre = "" if rel == "." else rel + "/"
        tracked = set(git(["-C", lane, "ls-tree", "-r", "--name-only", commit, "--", rel]).split("\n"))
        found = [n for n in names if pre + n + ".md" in tracked]
    missing = [n for n in names if n not in found]
    for n in missing:
        print("MISSING " + n)
    print("OK %d/%d reports present in %s" % (len(found), len(names),
          report_dir + ("" if rev is None else "@" + rev)), file=sys.stderr)
    return 1 if missing else 0


sys.exit(main(sys.argv))
