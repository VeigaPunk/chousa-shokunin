#!/usr/bin/env python3
"""rerun-controls-r95 — round-95 C1 (operability) control battery for tools/search-rerun.py.

Every case runs the tool under test as a fresh process through its public CLI
(`python3 -B <tool> verify <record> --root <root> [--strict]`) and compares the exit code and the named codes with
the expectation written in this file before any scored run. The same forged records are also given to the nearest
prior instrument, `bash tools/research-gate.sh verify-sweeps <record> --root ..` (unchanged this round), to show it
accepts them: nothing in the lane compared a recorded count or hit set before this round.

Groups:
  POSITIVE       the committed record corpus/fixtures/search-rerun-r95.md: exit 0, CLEAN, rev_match=8/8
  STRICT_TREE    the same record under --strict at the lane tree: exit 1 and every code is TREE_CHANGED
                 (the S222 capture added this round really moves Q1/Q2/Q3/Q6/Q8)
  FORGERY        8 one-cell forgeries of the committed record: exit 1, the named rev codes present, rev=DRIFT
  PRIOR          the 8 forgeries under research-gate verify-sweeps: exit 0 (accepted) — the do-nothing instrument
  SETUP          12 malformed records or roots: exit 2 and `SEARCH_RERUN_ERROR <code>` with the named code
  CLONE_TREE     a `git clone --shared` of the lane in scratch with one capture edited and one symlink added:
                 the edit is TREE_CHANGED with exit 0 (exit 1 under --strict); the symlink is WHERE_TYPE exit 2
  DO_NOTHING     the tool path at the base revision (git archive of 7b237358) does not exist: the counting
                 command exits non-zero and prints no CLEAN line
  ORACLES        three stand-ins scored by this same battery must FAIL it: a constant-CLEAN stub, a count-only
                 mutant (SET_DRIFT never raised) and a rev-blind mutant (the rev re-run reads the tree instead)

Usage: python3 -B corpus/evidence/round95/rerun-controls-r95.py --root LANE --work DIR [--tool PATH]
Prints one CASE line per case, then the tallies and RERUN_CONTROLS=PASS|FAIL. Exit 0 PASS, 1 FAIL, 2 setup.
Writes only under --work (removed at exit). Read-only on the lane: `git archive`, `git clone --shared` into --work.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

BASE = "7b2373586fb70f0ead6446c671fcc8b546d3e687"
CARRIER = "d27e9891ba6d2bae8b1f6060f7c01bf13a1a6ea1"
RECORD = "corpus/fixtures/search-rerun-r95.md"
TOOL = "tools/search-rerun.py"


def run(cmd, cwd=None, env=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr


def tool_run(tool, record, root, strict=False, env=None):
    cmd = [sys.executable, "-B", tool, "verify", record, "--root", root] + (["--strict"] if strict else [])
    return run(cmd, env=env)


def edit_row(text, qid, col, value):
    """Replace one cell of one Searches row (columns as in the tool's HEADER)."""
    cols = ["id", "engine", "where", "expression", "rev", "searched", "hits", "hit_set"]
    out = []
    for ln in text.split("\n"):
        if ln.startswith(f"| {qid} |"):
            cells = re.split(r"(?<!\\)\|", ln.strip()[1:-1])
            cells = [c.strip() for c in cells]
            cells[cols.index(col)] = value
            ln = "| " + " | ".join(cells) + " |"
        out.append(ln)
    new = "\n".join(out)
    if new == text:
        raise SystemExit(f"SETUP edit_row no-op {qid} {col}")
    return new


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def codes_of(out):
    return set(re.findall(r"\b(COUNT_DRIFT|SET_DRIFT|TREE_CHANGED)\b", out))


def battery(tool, root, work, base_text, prior_rev, emit):
    """Score one tool path; returns dict of group -> (ok, total)."""
    t = {}

    def tally(group, ok):
        a, b = t.get(group, (0, 0))
        t[group] = (a + (1 if ok else 0), b + 1)

    rec = os.path.join(root, RECORD)
    rc, out, err = tool_run(tool, rec, root)
    ok = rc == 0 and "SEARCH_RERUN: CLEAN" in out and "rev_match=8/8" in out
    emit(f"CASE positive rc={rc} expect=0 {'ok' if ok else 'FAIL'}")
    tally("POSITIVE", ok)

    rc, out, err = tool_run(tool, rec, root, strict=True)
    rev_lines = [ln for ln in out.splitlines() if ln.startswith("SEARCH_RERUN Q")]
    ok = (rc == 1 and len(rev_lines) == 8 and all("rev=MATCH" in ln for ln in rev_lines)
          and codes_of(out) == {"TREE_CHANGED"})
    emit(f"CASE strict-tree rc={rc} expect=1 codes={sorted(codes_of(out))} {'ok' if ok else 'FAIL'}")
    tally("STRICT_TREE", ok)

    forgeries = [
        ("f1-count", "Q5", "hits", "15", {"COUNT_DRIFT"}),
        ("f2-set-swap", "Q2", "hit_set",
         "corpus/captures/c52a1f15884a78028febcf43.txt, corpus/captures/0ae65ac01b93119d3c2f3fed.txt",
         {"SET_DRIFT"}),
        ("f3-expression", "Q3", "expression", "`deduplicate`", None),
        ("f4-digest", "Q1", "hit_set",
         "sha256:69cfc05988a6ea78b149d8027c0c0405171429c1aff812090b6aed4da1a00dc0", {"SET_DRIFT"}),
        ("f5-zero", "Q7", "expression", "`PRISMA`", {"COUNT_DRIFT", "SET_DRIFT"}),
        ("f6-engine", "Q6", "engine", "fixed", {"COUNT_DRIFT", "SET_DRIFT"}),
        ("f7-rev", "Q2", "rev", prior_rev, None),
        ("f8-where", "Q1", "where", "corpus/captures/0*.txt", None),
        # Amendment 3 (R95MutantsC1 m13, m16): list-form count and a duplicated path.
        ("f9-list-count", "Q2", "hits", "3", {"COUNT_DRIFT"}),
        ("f10-dup-path", "Q2", "hit_set",
         "corpus/captures/c52a1f15884a78028febcf43.txt, corpus/captures/c9d1e74c3ac8d9eb332c9770.txt, "
         "corpus/captures/c9d1e74c3ac8d9eb332c9770.txt", {"SET_DRIFT"}),
    ]
    for name, qid, col, value, want in forgeries:
        path = write(os.path.join(work, "forge", name + ".md"), edit_row(base_text, qid, col, value))
        rc, out, err = tool_run(tool, path, root)
        line = next((ln for ln in out.splitlines() if ln.startswith(f"SEARCH_RERUN {qid} ")), "")
        got = codes_of(line) - {"TREE_CHANGED"}
        ok = rc == 1 and "rev=DRIFT" in line and (got == want if want else bool(got))
        others = [ln for ln in out.splitlines() if ln.startswith("SEARCH_RERUN Q") and not ln.startswith(
            f"SEARCH_RERUN {qid} ")]
        ok = ok and len(others) == 7 and all("rev=MATCH" in ln for ln in others)
        # Amendment 3 (R95MutantsC1 m14): the printed tally must agree with the per-search lines.
        ok = ok and "rev_match=7/8" in out
        emit(f"CASE {name} rc={rc} expect=1 codes={sorted(got)} want={sorted(want) if want else 'any-rev-code'}"
             f" {'ok' if ok else 'FAIL'}")
        tally("FORGERY", ok)
        prc, pout, perr = run(["bash", os.path.join(root, "tools/research-gate.sh"), "verify-sweeps", path,
                               "--root", ".."], cwd=root)
        pok = prc == 0 and "RESEARCH_GATE: CLEAN" in pout
        emit(f"CASE prior-{name} research-gate-verify-sweeps rc={prc} expect=0 {'ok' if pok else 'FAIL'}")
        tally("PRIOR", pok)

    head_bad = base_text.replace("| id | engine | where |", "| id | engine | scope |")
    setups = [
        ("s1-missing", None, "RECORD_UNREADABLE"),
        ("s2-no-section", base_text.replace("## Searches", "## Search"), "SECTION"),
        ("s3-header", head_bad, "HEADER"),
        ("s4-engine", edit_row(base_text, "Q4", "engine", "pcre"), "ENGINE"),
        ("s5-dotdot", edit_row(base_text, "Q4", "where", "corpus/../../x/*.txt"), "WHERE"),
        ("s6-absolute", edit_row(base_text, "Q4", "where", "/etc/*"), "WHERE"),
        ("s7-rev", edit_row(base_text, "Q4", "rev", "deadbeef" * 5), "REV"),
        ("s8-regex", edit_row(base_text, "Q8", "expression", "`(`"), "EXPRESSION"),
        ("s9-empty", edit_row(base_text, "Q4", "expression", "``"), "EXPRESSION"),
        ("s10-zero-set", edit_row(base_text, "Q7", "hit_set", "corpus/captures/x.txt"), "HIT_SET"),
        ("s11-dup-id", edit_row(base_text, "Q4", "id", "Q3"), "ROW"),
        ("s12-root", "ROOT", "ROOT"),
    ]
    for name, text, code in setups:
        r = root
        if text is None:
            path = os.path.join(work, "setup", "absent.md")
        elif text == "ROOT":
            path, r = rec, os.path.join(root, "corpus")
        else:
            path = write(os.path.join(work, "setup", name + ".md"), text)
        rc, out, err = tool_run(tool, path, r)
        ok = rc == 2 and f"SEARCH_RERUN_ERROR {code} " in err and "SEARCH_RERUN: CLEAN" not in out
        emit(f"CASE {name} rc={rc} expect=2 code={code} {'ok' if ok else 'FAIL'}")
        tally("SETUP", ok)

    clone = os.path.join(work, "clone")
    if not os.path.isdir(clone):
        crc, _, cerr = run(["git", "clone", "-q", "--shared", "--no-checkout", root, clone])
        top = run(["git", "-C", clone, "rev-parse", "--show-toplevel"])[1].strip()
        if crc != 0 or os.path.realpath(top) != os.path.realpath(clone):
            raise SystemExit(f"SETUP clone {cerr.strip()} top={top!r}")
        run(["git", "-C", clone, "checkout", "-q", "--detach", BASE])
        with open(os.path.join(clone, "corpus/captures/62be15a474e866e4bef6c9d5.txt"), "ab") as fh:
            fh.write("\nPRISMA-S\n".encode())
        # Amendment 3 (R95MutantsC1 m15): move Q4's only hit to another file — same count, different set.
        p62 = os.path.join(clone, "corpus/captures/62be15a474e866e4bef6c9d5.txt")
        data = open(p62, "rb").read()
        open(p62, "wb").write(data.replace("検索者".encode(), b"---"))
        with open(os.path.join(clone, "corpus/captures/001287c436f0e6b1d166ae8d.txt"), "ab") as fh:
            fh.write("\n検索者\n".encode())
    rc, out, err = tool_run(tool, rec, clone)
    q1 = next((ln for ln in out.splitlines() if ln.startswith("SEARCH_RERUN Q1 ")), "")
    q4 = next((ln for ln in out.splitlines() if ln.startswith("SEARCH_RERUN Q4 ")), "")
    ok = (rc == 0 and "rev=MATCH tree=CHANGED recorded=7 at_rev=7 at_tree=8" in q1 and "rev_match=8/8" in out
          and "rev=MATCH tree=CHANGED recorded=1 at_rev=1 at_tree=1" in q4)
    rc2, out2, _ = tool_run(tool, rec, clone, strict=True)
    ok = ok and rc2 == 1
    emit(f"CASE clone-edit rc={rc}/{rc2} expect=0/1 {'ok' if ok else 'FAIL'}")
    tally("CLONE_TREE", ok)
    link = os.path.join(clone, "corpus/captures/zz-link.txt")
    if not os.path.islink(link):
        os.symlink("/etc/hostname", link)
    rc, out, err = tool_run(tool, rec, clone)
    ok = rc == 2 and "SEARCH_RERUN_ERROR WHERE_TYPE " in err
    emit(f"CASE clone-symlink rc={rc} expect=2 {'ok' if ok else 'FAIL'}")
    tally("CLONE_TREE", ok)
    os.unlink(link)

    # GREP_AGREE (Amendment 2, R95ExecEngine F1-F3/F5, R95ReviewerC1 F1/F3): a scratch fixture repo whose files sit on
    # the classes where a naive per-line matcher and GNU grep over a bash glob disagree. The expected values are
    # GNU grep's own output, taken at run time over a bash glob (the recording engine), never written by hand.
    fx = os.path.join(work, "grepfix")
    if not os.path.isdir(fx):
        os.makedirs(os.path.join(fx, "data", "sub"))
        files = {"data/a.txt": b"token\nline\n", "data/.x.txt": b"token\n", "data/empty.txt": b"",
                 "data/crlf.txt": b"world\r\n", "data/sub/c.txt": b"token\n",
                 "data/\xff\xfe.txt": b"token\n", "data/nl.txt": b"ab\ncd\n"}
        for rel, data in files.items():
            with open(os.path.join(fx.encode(), rel.encode("latin-1")), "wb") as fh:
                fh.write(data)
        run(["git", "-C", fx, "init", "-q"])
        top = run(["git", "-C", fx, "rev-parse", "--show-toplevel"])[1].strip()
        if os.path.realpath(top) != os.path.realpath(fx):
            raise SystemExit(f"SETUP grepfix toplevel {top!r}")
        run(["git", "-C", fx, "add", "-A"])
        run(["git", "-C", fx, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q",
             "-m", "fixture"])
    frev = run(["git", "-C", fx, "rev-parse", "HEAD"])[1].strip()
    rows = []
    for qid, eng, expr in (("Q1", "fixed", "token"), ("Q2", "regex", "^$"), ("Q3", "regex", "."),
                           ("Q4", "regex", "d$"), ("Q5", "regex", r"b\sc"), ("Q6", "fixed", "Token")):
        flag = "-F" if eng == "fixed" else "-P"
        g = subprocess.run(["bash", "-c", f"/usr/bin/grep -l {flag} -e \"$1\" data/*.txt | LC_ALL=C sort", "_", expr],
                           cwd=fx, capture_output=True)
        paths = [p for p in g.stdout.split(b"\n") if p]
        dg = __import__("hashlib").sha256(b"".join(p + b"\n" for p in paths)).hexdigest()
        hs = "-" if not paths else "sha256:" + dg
        rows.append(f"| {qid} | {eng} | data/*.txt | `{expr}` | {frev} | 2026-11-08 | {len(paths)} | {hs} |")
    rec_text = ("## Searches\n\n| id | engine | where | expression | rev | searched | hits | hit_set |\n"
                "|---|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
    gp = write(os.path.join(work, "grepfix-record.md"), rec_text)
    rc, out, err = tool_run(tool, gp, fx)
    ok = rc == 0 and "rev_match=6/6" in out and "SEARCH_RERUN: CLEAN" in out
    emit(f"CASE grep-agree rc={rc} expect=0 rows={';'.join(r.split('|')[7].strip() for r in rows)}"
         f" {'ok' if ok else 'FAIL'}")
    tally("GREP_AGREE", ok)
    for name, text, code in (
            ("globstar", rec_text.replace("| data/*.txt |", "| data/**/*.txt |", 1), "WHERE"),
            ("posix-class", rec_text.replace("`d$`", "`[[:alpha:]]`"), "EXPRESSION"),
            ("second-table", rec_text + "\n| id | engine | where | expression | rev | searched | hits | hit_set |\n"
             "|---|---|---|---|---|---|---|---|\n" + rows[0].replace("| Q1 |", "| Q9 |") + "\n", "TABLE")):
        p = write(os.path.join(work, f"grepfix-{name}.md"), text)
        rc, out, err = tool_run(tool, p, fx)
        ok = rc == 2 and f"SEARCH_RERUN_ERROR {code} " in err
        emit(f"CASE grep-agree-{name} rc={rc} expect=2 code={code} {'ok' if ok else 'FAIL'}")
        tally("GREP_AGREE", ok)

    # CONTAINMENT (Amendment 4, R95SentinelScope findings 1-4): a caller GIT_DIR pointing at another repository
    # must not redirect the rev re-run, and a symlinked record is refused.
    env = dict(os.environ, GIT_DIR=os.path.join(fx, ".git"))
    rc, out, err = tool_run(tool, rec, root, env=env)
    ok = rc == 0 and "rev_match=8/8" in out and "SEARCH_RERUN: CLEAN" in out
    emit(f"CASE containment-git-dir rc={rc} expect=0 {'ok' if ok else 'FAIL'}")
    tally("CONTAINMENT", ok)
    link = os.path.join(work, "record-link.md")
    if not os.path.islink(link):
        os.symlink(rec, link)
    rc, out, err = tool_run(tool, link, root)
    ok = rc == 2 and "SEARCH_RERUN_ERROR RECORD_TYPE " in err
    emit(f"CASE containment-record-symlink rc={rc} expect=2 {'ok' if ok else 'FAIL'}")
    tally("CONTAINMENT", ok)
    return t


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tool")
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    tool = os.path.realpath(a.tool or os.path.join(root, TOOL))
    work = os.path.join(os.path.realpath(a.work), "rerun-controls-r95")
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)
    try:
        with open(os.path.join(root, RECORD), encoding="utf-8") as fh:
            base_text = fh.read()
        # f7: the parent of the commit that added the Q2 capture c9d1e74c… — a revision where Q2 finds fewer files.
        add = run(["git", "-C", root, "log", "--diff-filter=A", "--format=%H", "-1", BASE, "--",
                   "corpus/captures/c9d1e74c3ac8d9eb332c9770.txt"])[1].strip()
        prior_rev = run(["git", "-C", root, "rev-parse", add + "^"])[1].strip()
        if not re.fullmatch(r"[0-9a-f]{40}", prior_rev):
            print(f"SETUP prior_rev {prior_rev!r}")
            return 2
        print(f"# tool={os.path.relpath(tool, root) if tool.startswith(root) else tool} base={BASE} f7_rev={prior_rev}")

        t = battery(tool, root, os.path.join(work, "real"), base_text, prior_rev, print)

        # DO_NOTHING: the counting command at the base revision.
        bdir = os.path.join(work, "base")
        os.makedirs(bdir)
        arch = subprocess.run(["git", "-C", root, "archive", BASE, "tools"], capture_output=True)
        subprocess.run(["tar", "-x", "-C", bdir], input=arch.stdout, check=True)
        rc, out, err = tool_run(os.path.join(bdir, TOOL), os.path.join(root, RECORD), root)
        dn_ok = rc != 0 and "SEARCH_RERUN: CLEAN" not in out and not os.path.exists(os.path.join(bdir, TOOL))
        print(f"CASE do-nothing-base rc={rc} expect=nonzero tool_present={os.path.exists(os.path.join(bdir, TOOL))}"
              f" {'ok' if dn_ok else 'FAIL'}")
        t["DO_NOTHING"] = (1 if dn_ok else 0, 1)

        # ORACLES: stand-ins that must fail this battery.
        src = open(tool, encoding="utf-8").read()
        stubs = {
            "constant-clean": "import sys\nprint('SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=8/8 "
                              "findings=0')\nprint('SEARCH_RERUN: CLEAN')\nsys.exit(0)\n",
            "count-only": src.replace('codes.append("SET_DRIFT")', "pass"),
            "rev-blind": src.replace("at_rev = run_at_rev(root, r, cache)", "at_rev = run_on_tree(root, r, listing)"),
            # Amendment 2: the tool as frozen at carrier C (before the grep-alignment repair) must fail GREP_AGREE.
            "carrier-c-tool": run(["git", "-C", root, "show", f"{CARRIER}:{TOOL}"])[1],
        }
        if not stubs["carrier-c-tool"].startswith("#!/usr/bin/env python3"):
            print("SETUP oracle carrier-c-tool not readable at the carrier revision")
            return 2
        rejected = 0
        for name, body in stubs.items():
            if name != "constant-clean" and body == src:
                print(f"SETUP oracle {name} mutation did not apply")
                return 2
            sp = write(os.path.join(work, "oracles", name + ".py"), body)
            ot = battery(sp, root, os.path.join(work, "oracle-" + name), base_text, prior_rev, lambda s: None)
            full = all(a == b for g, (a, b) in ot.items() if g != "PRIOR")
            fails = {g: f"{a}/{b}" for g, (a, b) in ot.items() if a != b and g != "PRIOR"}
            print(f"CASE oracle-{name} battery={'PASS' if full else 'FAIL'} expect=FAIL failed_groups={fails}"
                  f" {'ok' if not full else 'FAIL'}")
            rejected += 0 if full else 1
        t["ORACLES_REJECTED"] = (rejected, len(stubs))

        order = ["POSITIVE", "STRICT_TREE", "FORGERY", "PRIOR", "SETUP", "CLONE_TREE", "GREP_AGREE", "CONTAINMENT",
                 "DO_NOTHING", "ORACLES_REJECTED"]
        names = {"FORGERY": "FORGERY_REFUSED", "PRIOR": "PRIOR_ACCEPTED", "SETUP": "SETUP_REFUSED",
                 "DO_NOTHING": "DO_NOTHING_REFUSED"}
        print(" ".join(f"{names.get(g, g)}={t[g][0]}/{t[g][1]}" for g in order))
        passed = all(t[g][0] == t[g][1] and t[g][1] > 0 for g in order)
        print("RERUN_CONTROLS=" + ("PASS" if passed else "FAIL"))
        return 0 if passed else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
