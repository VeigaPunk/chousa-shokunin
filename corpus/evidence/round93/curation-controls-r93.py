#!/usr/bin/env python3
"""curation-controls-r93 — round-93 C2 classification battery (successor of curation-controls-r92.py).

Mirrors the tree the two curation counters read (registry, the two routed entries, the capture store,
the refetch ledger) and scores it with the round-92 counter (`OLD`) and with `curation-r93.py` (`NEW`).

  P  positive            the landing tree: both counters PASS
  W1 ws-space            a located quote whose cell is `" "`: r92 refuses it downstream (FLOOR/WARRANT/
                         TFREQ) with `Q_SHAPE_FAIL=0`; r93 refuses it AT THE SHAPE LEG as
                         `quote=<whitespace>` and counts it in `Q_WSQUOT=1`
  W2 ws-tab              the same class with a tab inside the quotes: same split
  C1 nonq-row            carried: r92 and r93 both refuse (QSHAPE) — the round-92 class, kept as
  C2 status-rejected     retirement safety. Both counters must still refuse all four.
  C3 used-by-blank
  C4 ubiquitous-warrant
  D  duplicate-count     the round-90 double-count probe: `UNENTAILED_TERM=1` under both

Regression: the round-90 control battery re-runs against `curation-r93.py` through a verdict-token
alias, so its seven closed tree forgeries must still be refused.

The discrimination here is classification, not refusal: r92 already fails the whitespace trees, but it
cannot name the class (`Q_SHAPE_FAIL=0`, no `Q_WSQUOT` field, the shape leg green). Round 93's claim is
the named shape verdict plus the independent population count, so the battery asserts both counters'
verdicts AND the r93 fields.

Usage: python3 -B corpus/evidence/round93/curation-controls-r93.py --root DIR --work DIR
Exit 0 every case as expected, 1 a deviation, 2 setup. No network.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "curation-r93.py")
OLD = os.path.join(os.path.dirname(HERE), "round92", "curation-r92.py")
REG = os.path.join(os.path.dirname(HERE), "round90", "curation-r90-controls.py")
ENTRY_A = "corpus/knowledge/search-transparency-reporting-r84.md"
ENTRY_B = "corpus/knowledge/provenance-recording-r85.md"
QUOTE_ROW = '| Q2 | S214 | "date when each source was last searched or consulted." |'
NONQ = ('| note | S214 | "Specify all databases, registers, websites, organisations, reference lists and '
        'other sources searched or consulted to identify studies." |')
UBIQ = '| Reporting the source | state the source | report it without the source | Q2 (S214) |'
DUP = '| Recording a modified resource | state the modified value | leave the modified value unstated | Q13 (S023) |'
SIBLING = 'corpus/knowledge/search-transparency-reporting-r84.md.bak'


def mirror(root, dst):
    os.makedirs(os.path.join(dst, "corpus", "knowledge"), exist_ok=True)
    os.makedirs(os.path.join(dst, "corpus", "evidence"), exist_ok=True)
    shutil.copy2(os.path.join(root, "corpus", "SOURCES.md"), os.path.join(dst, "corpus", "SOURCES.md"))
    # the counter's committed leg-vocabulary table travels with every mirror
    legs_dst = os.path.join(dst, "corpus", "evidence", "round93", "controls")
    os.makedirs(legs_dst, exist_ok=True)
    shutil.copy2(os.path.join(root, "corpus", "evidence", "round93", "controls", "legs.txt"),
                 os.path.join(legs_dst, "legs.txt"))
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
    verdict = [ln for ln in out.splitlines() if ln.startswith(("CURATION_R92=", "CURATION_R93="))]
    fails = [ln for ln in p.stdout.splitlines() if ln.startswith("LEG_FAIL")]
    fields = {}
    for k in ("UNENTAILED_TERM", "Q_SHAPE_FAIL", "Q_WSQUOT", "Q_ROWS"):
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
        # needles are bound against the FULL stdout, not only the LEG_FAIL lines: `Q_WSQUOT=1` is a field.
        ok = (rc_old == expect_old and rc_new == expect_new
              and (needle in " ".join(fails) or not needle)
              and all(n in out_new for n in needles))
        results[name] = ok
        print(f"{'OK' if ok else 'FAIL'} {name}: r92 rc={rc_old} ({v_old}), r93 rc={rc_new} ({v_new})"
              f" shapes old={fl_old.get('Q_SHAPE_FAIL')} new={fl_new.get('Q_SHAPE_FAIL')}"
              f" ws new={fl_new.get('Q_WSQUOT')}")
        if not ok:
            print("  r93 fails:", " | ".join(fails[-3:]))
        return ok

    case("positive", None, 0, 0, "")
    # The field is the claim's distinguishing token, so it is bound here: a counter whose WSQUOTE population is
    # stubbed (R93ExecMutations M7 / R93CriticClaims C2) prints Q_WSQUOT=0 and must fail this battery.
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

    # classification assertion: on the two whitespace trees r92 must report the shape leg GREEN.
    ws_shape_green = True
    for name in ("ws-space", "ws-tab"):
        tree = os.path.join(work, name)
        _rc, _v, _f, fl, _o = run(OLD, tree)
        ws_shape_green = ws_shape_green and fl.get("Q_SHAPE_FAIL") == "0"
    print(f"{'OK' if ws_shape_green else 'FAIL'} ws-classification: r92 Q_SHAPE_FAIL=0 on both "
          f"whitespace trees (the class the r93 shape leg names)")
    results["ws-classification"] = ws_shape_green

    dup_tree = fresh("duplicate-count")
    edit(os.path.join(dup_tree, ENTRY_A), "## Inference", DUP + "\n\n## Inference")
    _rc_old, _v_old, _f, fl_old, _o = run(OLD, dup_tree)
    _rc_new, _v_new, _f, fl_new, _o2 = run(NEW, dup_tree)
    dup_ok = fl_old.get("UNENTAILED_TERM") == "1" and fl_new.get("UNENTAILED_TERM") == "1"
    print(f"{'OK' if dup_ok else 'FAIL'} duplicate-count: r92 UNENTAILED_TERM={fl_old.get('UNENTAILED_TERM')} "
          f"r93 UNENTAILED_TERM={fl_new.get('UNENTAILED_TERM')}")

    reg_work = os.path.join(work, "regression")
    alias = os.path.join(work, "verdict-alias.py")
    open(alias, "w", encoding="utf-8").write(
        "import subprocess, sys\n"
        f"r = subprocess.run([sys.executable, '-B', {NEW!r}] + sys.argv[1:], capture_output=True, text=True)\n"
        "sys.stdout.write(r.stdout.replace('CURATION_R93=', 'CURATION_R90='))\n"
        "sys.stdout.write(r.stderr)\n"
        "sys.exit(r.returncode)\n")
    p = subprocess.run([sys.executable, "-B", REG, "--root", root, "--work", reg_work, "--counter", alias],
                       capture_output=True, text=True)
    line = [ln for ln in p.stdout.splitlines() if ln.startswith("FORGERY_REFUSED=")]
    reg_ok = bool(line) and line[0].startswith("FORGERY_REFUSED=7/7")
    print(f"{'OK' if reg_ok else 'FAIL'} regression: {line[0] if line else 'no line'} rc={p.returncode}")

    carried = sum(1 for n in ("c1-nonq-row", "c2-status-rejected", "c3-used-by-blank", "c4-ubiquitous-warrant")
                  if results.get(n))
    ws_named = sum(1 for n in ("ws-space", "ws-tab") if results.get(n))
    ok = carried == 4 and ws_named == 2 and ws_shape_green and dup_ok and reg_ok and results.get("positive")
    print(f"CONTROLS={'PASS' if ok else 'FAIL'} CARRIED_REFUSED_BOTH={carried}/4 WS_NAMED={ws_named}/2 "
          f"WS_SHAPE_GREEN_R92={int(ws_shape_green)}/1 DUPCOUNT_{fl_old.get('UNENTAILED_TERM') or 'x'}="
          f"{int(dup_ok)}/1 PRIOR_REGRESSION={'7/7' if reg_ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
