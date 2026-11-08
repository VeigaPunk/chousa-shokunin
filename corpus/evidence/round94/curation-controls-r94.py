#!/usr/bin/env python3
"""curation-controls-r94 — round-94 C2 classification battery (successor of curation-controls-r93.py).

Mirrors the tree the two curation counters read (registry, the two routed entries, the capture store,
the refetch ledger, both leg tables) and scores it with the round-93 counter (`OLD`) and with
`curation-r94.py` (`NEW`).

  P  positive            the landing tree: both counters PASS and r94 prints `Q_PUNCTQUOT=0` on all 20
                         real located quotes (the silence direction of the new class, measured in-tree)
  W1 ws-space            carried: a located quote whose cell is `" "` — both counters refuse it
  W2 ws-tab              the same class with a tab: both refuse
  C1..C4 carried         nonq-row, status-rejected, used-by-blank, ubiquitous-warrant: both refuse
  D  duplicate-count     the round-90 double-count probe: `UNENTAILED_TERM=1` under both
  X1 punct-dash          the Q2 quote cell replaced by `"—"`: r93 refuses it downstream only
                         (`Q_SHAPE_FAIL=0`, no `Q_PUNCTQUOT` field, FLOOR/WARRANT); r94 refuses it AT THE
                         SHAPE LEG as `quote=<punctuation>` and counts it (`Q_PUNCTQUOT=1`,
                         `LEG_FAIL PUNCTQUOT`)
  X2 punct-dots          the same class as `"..."`: same split

Regression: the round-90 control battery re-runs against `curation-r94.py` through a verdict-token
alias, so its seven closed tree forgeries must still be refused.

The discrimination here is classification, not refusal: r93 already fails both X trees, but it cannot
name the class — the same shape as round 93's WSQUOTE claim, and the reason the claim is stated as a
classification claim.

Usage: python3 -B corpus/evidence/round94/curation-controls-r94.py --root DIR --work DIR
Exit 0 every case as expected, 1 a deviation, 2 setup. No network, no writes outside `--work`.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "curation-r94.py")
OLD = os.path.join(os.path.dirname(HERE), "round93", "curation-r93.py")
REG = os.path.join(os.path.dirname(HERE), "round90", "curation-r90-controls.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"
QUOTE_ROW = '| Q2 | S214 | "date when each source was last searched or consulted." |'
NONQ = ('| note | S214 | "Specify all databases, registers, websites, organisations, reference lists and '
        'other sources searched or consulted to identify studies." |')
UBIQ = '| Reporting the source | state the source | report it without the source | Q2 (S214) |'
DUP = '| Recording a modified resource | state the modified value | leave the modified value unstated | Q13 (S023) |'
LEGS = (("round93", "controls", "legs.txt"), ("round94", "controls", "legs.txt"))


def mirror(root, dst):
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    shutil.copy2(os.path.join(root, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    # both counters' committed leg-vocabulary tables travel with every mirror
    for rnd, sub, name in LEGS:
        legs_dst = os.path.join(dst, "corpus", "evidence", rnd, sub)
        os.makedirs(legs_dst, exist_ok=True)
        shutil.copy2(os.path.join(root, "corpus", "evidence", rnd, sub, name),
                     os.path.join(legs_dst, name))
    for rel in (ENTRY_A, ENTRY_B):
        shutil.copy2(os.path.join(root, rel), os.path.join(dst, rel))
    for rel in (os.path.join("corpus", "captures"), os.path.join("corpus", "evidence", "round57")):
        src = os.path.join(root, rel)
        if os.path.isdir(src):
            os.symlink(src, os.path.join(dst, rel))
    return dst


def run(counter, root):
    p = subprocess.run([sys.executable, "-B", counter, "--root", root], capture_output=True, text=True)
    out = p.stdout or ""
    verdict = [ln for ln in out.splitlines() if ln.startswith(("CURATION_R93=", "CURATION_R94="))]
    fails = [ln for ln in out.splitlines() if ln.startswith("LEG_FAIL")]
    fields = {}
    for k in ("UNENTAILED_TERM", "Q_SHAPE_FAIL", "Q_WSQUOT", "Q_PUNCTQUOT", "Q_ROWS"):
        m = re.search(rf"(?:^| ){k}=([^ ]+)", out)
        if m:
            fields[k] = m.group(1)
    return p.returncode, (verdict[0] if verdict else "no-verdict"), fails, fields, out


def edit(path, old, new, count=1):
    text = open(path, encoding="utf-8").read()
    if old not in text:
        raise SystemExit(f"SETUP pattern absent in {path}: {old[:60]!r}")
    open(path, "w", encoding="utf-8").write(text.replace(old, new, count))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    pristine = mirror(root, os.path.join(work, "pristine"))

    def fresh(name):
        d = os.path.join(work, name)
        shutil.copytree(pristine, d, symlinks=True)
        return d

    results = {}

    def case(name, mutate, expect_old, expect_new, needle="", needles=()):
        tree = fresh(name)
        if mutate is not None:
            mutate(tree)
        rc_old, v_old, _f, fl_old, _o = run(OLD, tree)
        rc_new, v_new, fails, fl_new, out_new = run(NEW, tree)
        ok = (rc_old == expect_old and rc_new == expect_new
              and (needle in " ".join(fails) or not needle)
              and all(n in out_new for n in needles))
        results[name] = ok
        print(f"{'OK' if ok else 'FAIL'} {name}: r93 rc={rc_old} ({v_old}), r94 rc={rc_new} ({v_new})"
              f" shapes old={fl_old.get('Q_SHAPE_FAIL')} new={fl_new.get('Q_SHAPE_FAIL')}"
              f" punct new={fl_new.get('Q_PUNCTQUOT')}")
        if not ok:
            print("  r94 fails:", " | ".join(fails[-4:]))
        return ok

    case("positive", None, 0, 0, "", needles=("Q_PUNCTQUOT=0", "CURATION_R94=PASS"))
    WS_NEEDLES = ("Q_WSQUOT=1", "LEG_FAIL WSQUOTE")
    case("ws-space", lambda t: edit(os.path.join(t, ENTRY_A), QUOTE_ROW, '| Q2 | S214 | " " |'), 1, 1,
         "quote=<whitespace>", needles=WS_NEEDLES)
    case("ws-tab", lambda t: edit(os.path.join(t, ENTRY_A), QUOTE_ROW, '| Q2 | S214 | "\t" |'), 1, 1,
         "quote=<whitespace>", needles=WS_NEEDLES)
    case("c1-nonq-row", lambda t: edit(os.path.join(t, ENTRY_A), "| Q13 | S023 |", NONQ + "\n| Q13 | S023 |"),
         1, 1, "LEG_FAIL QSHAPE")
    case("c2-status-rejected",
         lambda t: edit(os.path.join(t, "corpus", "SOURCES.md"),
                        "| mined | 2026-11-08 | on-release | corpus/knowledge/search-transparency-reporting-r84.md |",
                        "| rejected | 2026-11-08 | on-release | corpus/knowledge/search-transparency-reporting-r84.md |"),
         1, 1, "LEG_FAIL SOURCE")
    case("c3-used-by-blank",
         lambda t: edit(os.path.join(t, "corpus", "SOURCES.md"),
                        "| mined | 2026-11-08 | on-release | corpus/knowledge/search-transparency-reporting-r84.md |",
                        "| mined | 2026-11-08 | on-release | — |"),
         1, 1, "LEG_FAIL SOURCE")
    case("c4-ubiquitous-warrant",
         lambda t: edit(os.path.join(t, ENTRY_A), "## Inference", UBIQ + "\n\n## Inference"), 1, 1,
         "LEG_FAIL TFREQ")

    # The two new discriminations. The class is the same one r93 cannot name: the shape leg stays green
    # and the refusal is a downstream FLOOR/WARRANT. r94 refuses it at the shape leg and counts it.
    PUNCT_NEEDLES = ("Q_PUNCTQUOT=1", "LEG_FAIL PUNCTQUOT", "quote=<punctuation>")
    case("x1-punct-dash", lambda t: edit(os.path.join(t, ENTRY_A), QUOTE_ROW, '| Q2 | S214 | "\u2014" |'),
         1, 1, "LEG_FAIL QSHAPE", needles=PUNCT_NEEDLES)
    case("x2-punct-dots", lambda t: edit(os.path.join(t, ENTRY_A), QUOTE_ROW, '| Q2 | S214 | "..." |'),
         1, 1, "LEG_FAIL QSHAPE", needles=PUNCT_NEEDLES)

    # classification assertion: on both punctuation trees r93 must report the shape leg GREEN.
    punct_shape_green = True
    for name in ("x1-punct-dash", "x2-punct-dots"):
        tree = os.path.join(work, name)
        _rc, _v, _f, fl, _o = run(OLD, tree)
        punct_shape_green = punct_shape_green and fl.get("Q_SHAPE_FAIL") == "0"
    print(f"{'OK' if punct_shape_green else 'FAIL'} punct-classification: r93 Q_SHAPE_FAIL=0 on both "
          f"punctuation trees (the class the r94 shape leg names)")
    results["punct-classification"] = punct_shape_green

    dup_tree = fresh("duplicate-count")
    edit(os.path.join(dup_tree, ENTRY_A), "## Inference", DUP + "\n\n## Inference")
    _rc_old, _v_old, _f, fl_old, _o = run(OLD, dup_tree)
    _rc_new, _v_new, _f, fl_new, _o2 = run(NEW, dup_tree)
    dup_ok = fl_old.get("UNENTAILED_TERM") == "1" and fl_new.get("UNENTAILED_TERM") == "1"
    print(f"{'OK' if dup_ok else 'FAIL'} duplicate-count: r93 UNENTAILED_TERM={fl_old.get('UNENTAILED_TERM')} "
          f"r94 UNENTAILED_TERM={fl_new.get('UNENTAILED_TERM')}")

    reg_work = os.path.join(work, "regression")
    alias = os.path.join(work, "verdict-alias.py")
    legs_src = os.path.join(HERE, "controls", "legs.txt")
    open(alias, "w", encoding="utf-8").write(
        "import os, shutil, subprocess, sys\n"
        "args = sys.argv[1:]\n"
        "root = args[args.index('--root') + 1] if '--root' in args else '.'\n"
        "dst = os.path.join(root, 'corpus', 'evidence', 'round94', 'controls')\n"
        "os.makedirs(dst, exist_ok=True)\n"
        f"shutil.copy2({legs_src!r}, os.path.join(dst, 'legs.txt'))\n"
        f"r = subprocess.run([sys.executable, '-B', {NEW!r}] + args, capture_output=True, text=True)\n"
        "sys.stdout.write(r.stdout.replace('CURATION_R94=', 'CURATION_R90='))\n"
        "sys.stdout.write(r.stderr)\n"
        "sys.exit(r.returncode)\n")
    p = subprocess.run([sys.executable, "-B", REG, "--root", root, "--work", reg_work, "--counter", alias],
                       capture_output=True, text=True)
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("FORGERY_REFUSED=")]
    reg_ok = (bool(line) and line[0].startswith("FORGERY_REFUSED=7/7")
              and any(ln.startswith("CONTROLS=PASS") for ln in p.stdout.splitlines()))
    print(f"{'OK' if reg_ok else 'FAIL'} regression: {line[0] if line else 'no line'} rc={p.returncode}")

    carried = sum(1 for n in ("c1-nonq-row", "c2-status-rejected", "c3-used-by-blank", "c4-ubiquitous-warrant")
                  if results.get(n))
    ws_named = sum(1 for n in ("ws-space", "ws-tab") if results.get(n))
    punct_named = sum(1 for n in ("x1-punct-dash", "x2-punct-dots") if results.get(n))
    ok = (carried == 4 and ws_named == 2 and punct_named == 2 and punct_shape_green and dup_ok
          and reg_ok and results.get("positive"))
    print(f"CONTROLS={'PASS' if ok else 'FAIL'} CARRIED_REFUSED_BOTH={carried}/4 WS_NAMED={ws_named}/2 "
          f"PUNCT_NAMED={punct_named}/2 PUNCT_SHAPE_GREEN_R93={int(punct_shape_green)}/1 "
          f"DUPCOUNT_{fl_old.get('UNENTAILED_TERM') or 'x'}={int(dup_ok)}/1 "
          f"PRIOR_REGRESSION={'7/7' if reg_ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
