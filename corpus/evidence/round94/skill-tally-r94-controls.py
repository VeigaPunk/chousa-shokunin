#!/usr/bin/env python3
"""skill-tally-r94-controls — round-94 C3 discrimination battery.

Successor of `skill-tally-r93-controls.py`. Scratch `SKILL.md` copies of the landing tree are scored by
the round-93 counter and by `skill-tally-r94.py` against the committed selftest receipt:

  P  positive             the landing `SKILL.md`: both counters PASS
  C1 old-prose-carried    the round-91 clause restored: both refuse (`MISLABELED=6`)
  C2 stale-tally          one current tally set to `PASS (275 cases, 0 skipped)`: both refuse
  C3 deleted-historical   the grounded `161` tally set to `160`: both refuse
  C4 deleted-tail         the `215` tail tally one digit changed: r93's TAIL leg refuses it
  C5 added-tail           one extra undeclared tally appended below the Gates scope: r93 refuses
  C6 ungrounded-historical one grounding receipt's located quote changed: r93's HIST_DERIVED is 1/2
  C7 head-tally           a tally planted above `## Gates`: r93 declares the head empty
  C8 interior-hole        an interior hole in the bashenv family: r93 refuses
  M1 moved-tail-215       the `215` tally MOVED, same count, into the Round 36 section: r93 reads the tail
                          multiset only, so it PASSES; r94 refuses with `TAIL_OWNER_MISMATCH`
  M2 moved-tail-283       the `283` host-line tally moved into the Round 35 section: same split
  M3 double-tail-215      the `215` tally duplicated under its own heading: both refuse (count 2)
  M4 moved-to-heading     the `215` tally moved under a heading that merely CONTAINS the declared owner
                          string: r94 accepts it (owner is a substring by declaration; named limit)

`HIST_*`, `TAIL_*`, `TAIL_OWNER_*` and `CASE_RANGE_*` findings are read from stdout; exit codes are the
verdicts.

Usage: python3 -B corpus/evidence/round94/skill-tally-r94-controls.py --root DIR --work DIR
Exit 0 every case as expected, 1 a deviation, 2 setup. No network, no writes outside `--work`.
"""
import argparse
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
NEW = os.path.join(HERE, "skill-tally-r94.py")
OLD = os.path.join(os.path.dirname(HERE), "round93", "skill-tally-r93.py")
RECEIPT = os.path.join(HERE, "controls", "selftest-r94.txt")
OLD_CLAUSE = ("r39 bash-pin cases 273–275 (pin-bashenv, drift-bashenv) and r82 pin-override cases 276–283, "
              "of which bash-pin-override cases 282–283")
BAD_CLAUSE = "r39 bash-pin cases 273–275 and r82 bash-pin-override cases 276–283"
HIST161 = "`PASS (161 cases, 0 skipped)`"
TAIL215_LINE = "`PASS (215 cases, 0 skipped)` under the host UTF-8 locale; original187"
TAIL283 = "`PASS (283 cases, 0 skipped)`"
TAIL283_LINE = "  userns exists). Selftest `PASS (283 cases, 0 skipped)` on this host."
GROUND = ("corpus/evidence/round25-final-measure.log",
          "corpus/evidence/round34/audit-dispositions.md")
GROUND161 = GROUND[0]
OWNER215 = "### Round27 repair/status correction — 2026-10-21"
OWNER283 = "### Round 37 — the claim-pin provenance and the pin-capture environment (2026-10-23)"
ALIEN = "### Round 36 — the engine-swap canary and per-record attribution (2026-10-23)"
ALIEN2 = "### Round 35 — the pinned binary, the routing witness, and two survivors (2026-10-23)"


def run(counter, tree, receipt=RECEIPT):
    p = subprocess.run([sys.executable, "-B", counter, "--root", tree, "--selftest", receipt],
                       capture_output=True, text=True)
    out = p.stdout or ""
    verdict = [ln for ln in out.splitlines() if "SKILL_TALLY_R9" in ln]
    return p.returncode, (verdict[0] if verdict else "no-verdict"), out


def move(text, line, frm, to, suffix="Moved for the fixture."):
    """Delete `line` (found only between heading `frm` and the next heading) and re-insert it under `to`."""
    lines = text.split("\n")
    try:
        frm_i = lines.index(frm)
        to_i = lines.index(to)
    except ValueError as exc:
        raise SystemExit(f"SETUP heading absent: {exc}")
    idx = None
    for i in range(frm_i + 1, len(lines)):
        if lines[i].startswith("#"):
            break
        if lines[i] == line:
            idx = i
            break
    if idx is None:
        raise SystemExit(f"SETUP tally line {line!r} not under {frm!r}")
    del lines[idx]
    to_i = lines.index(to)
    lines[to_i + 1:to_i + 1] = ["", suffix + " " + line]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    if not os.path.isfile(RECEIPT):
        print(f"SETUP missing selftest receipt {RECEIPT}")
        return 2
    src = os.path.join(root, "SKILL.md")
    text = open(src, encoding="utf-8").read()
    if OLD_CLAUSE not in text:
        print("SETUP repaired clause absent from SKILL.md — is this the landing tree?")
        return 2
    for needle, why in ((HIST161, "161 tally"), (TAIL215_LINE, "215 tail tally")):
        if needle not in text:
            print(f"SETUP {why} absent from SKILL.md — is this the landing tree?")
            return 2
    if TAIL215_LINE not in text[text.find(OWNER215):]:
        print(f"SETUP {OWNER215!r} does not precede the 215 tally")
        return 2
    if TAIL283 not in text[text.find(OWNER283):]:
        print(f"SETUP {OWNER283!r} does not precede the 283 tally")
        return 2
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)

    def tree(name, body, grounding=None):
        d = os.path.join(work, name)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(body)
        for rel in GROUND:
            p = os.path.join(d, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            if grounding is not None and rel == GROUND161:
                open(p, "w", encoding="utf-8").write(grounding)
            else:
                shutil.copy2(os.path.join(root, rel), p)
        return d

    results = {}
    old_rcs = {}

    def case(name, body, expect_old, expect_new, needle_new="", grounding=None, receipt=RECEIPT):
        d = tree(name, body, grounding)
        rc_old, v_old, _o = run(OLD, d, receipt)
        rc_new, v_new, out_new = run(NEW, d, receipt)
        ok = (rc_old == expect_old) and (rc_new == expect_new) and (needle_new in out_new if needle_new else True)
        results[name] = ok
        old_rcs[name] = rc_old
        print(f"{'OK' if ok else 'FAIL'} {name}: r93 rc={rc_old} ({v_old}), r94 rc={rc_new} ({v_new})")
        if not ok:
            print("  r94:", " | ".join(ln for ln in out_new.splitlines()
                                       if ln.startswith(("LEG_FAIL", "HIST_", "TAIL_", "TAIL_OWNER")))[-400:])
        return ok

    case("positive", text, 0, 0, "SKILL_TALLY_R94=PASS")
    case("old-prose-carried", text.replace(OLD_CLAUSE, BAD_CLAUSE), 1, 1, "MISLABELED=6")
    case("stale-tally", text.replace("PASS (283 cases, 0 skipped)", "PASS (275 cases, 0 skipped)", 1), 1, 1,
         "STALE_TALLIES=1/8")
    case("deleted-historical", text.replace(HIST161, "`PASS (160 cases, 0 skipped)`", 1), 1, 1,
         "LEG_FAIL OTHERS")
    case("deleted-tail", text.replace(TAIL215_LINE, "`PASS (214 cases, 0 skipped)` under the host UTF-8 locale; original187", 1), 1, 1, "TAIL_OK=0")
    case("added-tail", text + "\nAdditional historical tally `PASS (199 cases, 0 skipped)` retained.\n", 1, 1,
         "HIST_SCOPE_BLEED")
    case("ungrounded-historical", text, 1, 1, "HIST_DERIVED=1/2",
         grounding="legacy selftest output, no verdict line\n")
    head_text = text.replace("## Gates", "Historical `PASS (777 cases, 0 skipped)` above the section.\n\n## Gates", 1)
    case("head-tally", head_text, 1, 1, "HIST_SCOPE_BLEED head")
    hole_receipt = os.path.join(work, "receipt-interior-hole.txt")
    body = open(RECEIPT, encoding="utf-8").read()
    if "drift-bashenv-echo" not in body:
        print(f"SETUP expected case name drift-bashenv-echo absent from {RECEIPT}")
        return 2
    open(hole_receipt, "w", encoding="utf-8").write(body.replace("drift-bashenv-echo", "drift-other-echo", 1))
    case("interior-hole", text, 1, 1, "CASE_RANGE", receipt=hole_receipt)

    # Round-94 discriminations: the tally keeps its count and the file keeps its shape; only the section
    # that owns it changes. r93's tail leg reads a multiset, so the move is invisible to it.
    case("moved-tail-215", move(text, TAIL215_LINE, OWNER215, ALIEN), 0, 1, "TAIL_OWNER_MISMATCH")
    case("moved-tail-283", move(text, TAIL283_LINE, OWNER283, ALIEN2),
         0, 1, "TAIL_OWNER_MISMATCH")
    case("double-tail-215", text.replace(TAIL215_LINE, TAIL215_LINE + "\n\n" + TAIL215_LINE, 1), 1, 1, "TAIL_OWNER_COUNT")
    # Named limit (R94ReviewerC3 F3: this case RENAMES the owner heading, it does not move the tally):
    # the declaration binds a heading SUBSTRING, so a heading that contains the declared owner string
    # satisfies it. Measured, not hidden.
    alias_heading = OWNER215 + " (alias)"
    case("heading-alias", text.replace(OWNER215, alias_heading, 1), 0, 0, "SKILL_TALLY_R94=PASS")

    ok = all(results.values())
    moved_names = ("moved-tail-215", "moved-tail-283")
    moved = sum(1 for n in moved_names if results.get(n))
    prior = sum(1 for n in moved_names if old_rcs.get(n) == 0)
    carried_names = ("old-prose-carried", "deleted-historical", "deleted-tail", "added-tail",
                     "head-tally", "interior-hole")
    carried = sum(1 for n in carried_names if results.get(n) and old_rcs.get(n) == 1)
    print(f"CONTROLS={'PASS' if ok else 'FAIL'} "
          f"CARRIED_REFUSED={carried}/6 "
          f"MOVED_REFUSED={moved}/2 MOVED_PRIOR_ACCEPTED={prior}/2 "
          f"DOUBLE_REFUSED={int(results.get('double-tail-215', False))}/1 "
          f"HEADING_ALIAS_ACCEPTED={int(results.get('heading-alias', False))}/1 "
          f"STALE_REFUSED_BOTH={int(results.get('stale-tally', False))}/1 "
          f"TAIL_ADDED_REFUSED={int(results.get('added-tail', False))}/1 "
          f"HIST_UNGROUNDED_REFUSED={int(results.get('ungrounded-historical', False))}/1")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
