#!/usr/bin/env python3
"""R63-C2 controls — shows `../c2-count.py` discriminates, before the claim is frozen.

Prepares a scratch mirror of the lane (corpus/ without captures, evidence and fixtures; the positive rows
`candidate-git-rows.txt` inserted into the registry; the positive entry `c2-positive-entry.md`; the candidate probe and
its output copied to `corpus/evidence/round63/`), then runs the counter on the mirror once per variant and prints
`NAME rc=<n> <counter line> OK|UNEXPECTED`. Expectations: `absent`, `no-entry-rows` and every single-defect variant
FAIL, `positive` PASS; `non-sequitur` (a claim that adds words but does not follow from its quote) is the named limit
and is expected to PASS. Also runs the counter with `--config openat2` on the lane itself (the round-62 entry, S138-S140,
committed): expected PASS, proving the engine on a known-good entry — and on a mirror without the openat2 probe output:
expected FAIL.
Usage: python3 run-c2-controls.py --work DIR [--fleet DIR]   (DIR absent or empty; removed unless --keep)
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[3]
COUNTER = HERE.parent / "c2-count.py"
ENTRY = "corpus/knowledge/git-revision-identity-r63.md"


def rows_into(sources: pathlib.Path, rows: str):
    t = sources.read_text().splitlines(True)
    i = next(k for k, l in enumerate(t) if l.startswith("## Paths"))
    j = i - 1
    while not re.match(r"^\|\s*S\d+", t[j]):
        j -= 1
    t.insert(j + 1, rows)
    sources.write_text("".join(t))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--fleet", default=str(LANE.parent))
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    w = pathlib.Path(a.work)
    if w.exists() and any(w.iterdir()):
        print("work must be absent or empty", file=sys.stderr)
        return 2
    m = w / "mirror"
    (m / "corpus/evidence/round63").mkdir(parents=True)
    shutil.copytree(LANE / "corpus", m / "corpus", symlinks=True, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("captures", "evidence", "fixtures"))
    readme_orig = (LANE / "corpus/README.md").read_text() + "\n- " + ENTRY + " (round 63)\n"
    (m / "corpus/README.md").write_text(readme_orig)
    probe_py = HERE / "candidate-git-revision-probe.py"
    probe_txt = HERE / "candidate-git-revision-probe.txt"
    ev = m / "corpus/evidence/round63"
    shutil.copy(probe_py, ev / "git-revision-probe.py")
    shutil.copy(probe_txt, ev / "git-revision-probe.txt")
    rows = (HERE / "candidate-git-rows.txt").read_text()
    entry_t = (HERE / "c2-positive-entry.md").read_text()
    src_orig = (m / "corpus/SOURCES.md").read_text()
    rows_into(m / "corpus/SOURCES.md", rows)
    src_pos = (m / "corpus/SOURCES.md").read_text()
    entry_p = m / ENTRY
    txt_orig = probe_txt.read_text()

    def run(args):
        return subprocess.run([sys.executable, "-B", str(COUNTER), "--fleet", a.fleet] + args, capture_output=True, text=True)

    def variant(name, entry=entry_t, sources=src_pos, expect="FAIL", drop_entry=False, readme=readme_orig,
                probe_text=txt_orig, drop_probe=False):
        entry_p.unlink(missing_ok=True)
        if not drop_entry:
            entry_p.write_text(entry)
        (m / "corpus/SOURCES.md").write_text(sources)
        (m / "corpus/README.md").write_text(readme)
        (ev / "git-revision-probe.txt").write_text(probe_text)
        if drop_probe:
            (ev / "git-revision-probe.py").unlink(missing_ok=True)
        else:
            shutil.copy(probe_py, ev / "git-revision-probe.py")
        p = run(["--root", str(m)])
        line = p.stdout.splitlines()[0] if p.stdout else p.stderr.strip()
        got = "PASS" if p.returncode == 0 else "FAIL"
        print(f"{name:22s} rc={p.returncode} {line} {'OK' if got == expect else 'UNEXPECTED'}")
        return got == expect

    def sub(a_, b, t=entry_t):
        assert t.count(a_) == 1, a_
        return t.replace(a_, b)

    ok = []
    ok.append(variant("absent", drop_entry=True))
    ok.append(variant("no-entry-rows", sources=src_orig))
    ok.append(variant("positive", expect="PASS"))
    ok.append(variant("fabricated-quote", entry=sub("Show every object whose name begins with the given prefix.", "Show every object whose name ends with the given prefix.")))
    ok.append(variant("cross-row-quote", entry=sub("- Q6 | S142 |", "- Q6 | S143 |")))
    ok.append(variant("quote-uncited", entry=sub("and a reader must peel the tag to the commit before comparing. [Q3, Q7, Q8]", "and a reader must peel the tag to the commit before comparing. [Q3, Q7]")))
    ok.append(variant("row-queued", sources=src_pos.replace("| mined | 2026-10-28 | on-release | corpus/knowledge/git-revision-identity-r63.md |\n| S143", "| queued | 2026-10-28 | on-release | corpus/knowledge/git-revision-identity-r63.md |\n| S143", 1)))
    ok.append(variant("row-opened-old", sources=src_pos.replace("| mined | 2026-10-28 | 180d | corpus/knowledge/git-revision-identity-r63.md |", "| mined | 2026-10-27 | 180d | corpus/knowledge/git-revision-identity-r63.md |", 1)))
    ok.append(variant("row-not-used-by", sources=src_pos.replace("| 180d | corpus/knowledge/git-revision-identity-r63.md |", "| 180d | — |", 1)))
    ok.append(variant("no-limits", entry=entry_t[:entry_t.index("## Limits")]))
    ok.append(variant("limits-no-inference", entry=entry_t.replace("- [INFERENCE] ", "- ", 1)))
    ok.append(variant("limits-no-git-version", entry=entry_t.replace("git version 2.56.0", "the installed git", 1)))
    ok.append(variant("junk-claim", entry=sub("Claim 5. A reader who wants every object that could be meant by a short prefix can ask for them all, which turns a failed lookup into a list of candidates instead of a silent guess. [Q6, Q2, Q9]", "Claim 5. Lorem ipsum dolor sit amet consectetur adipiscing elit. [Q6, Q2, Q9]")))
    long_q = "A suffix : followed by a path names the blob or tree at the given path in the tree-ish object named by the part before the colon."
    ok.append(variant("quote-over-25", entry=sub("A suffix : followed by a path names the blob or tree at the given path in the tree-ish object |", long_q + " |")))
    ok.append(variant("no-trio", entry=entry_t.replace("verified-at:", "checked:", 1)))
    ok.append(variant("echo-claim", entry=sub("Claim 5. A reader who wants every object that could be meant by a short prefix can ask for them all, which turns a failed lookup into a list of candidates instead of a silent guess. [Q6, Q2, Q9]", "Claim 5. Show every object whose name begins with the given prefix, because the object name starts with the prefix. [Q6, Q2, Q9]")))
    ok.append(variant("probe-script-missing", drop_probe=True))
    ok.append(variant("probe-output-edited", probe_text=txt_orig.replace("observed=40 expected=40", "observed=41 expected=40", 1)))
    ok.append(variant("probe-git-stale", probe_text=txt_orig.replace("HEADER git=git version 2.56.0", "HEADER git=git version 2.55.0", 1)))
    ok.append(variant("map-missing", readme=readme_orig.replace(ENTRY, "corpus/knowledge/other.md")))
    ok.append(variant("s143-wrong-file", sources=src_pos.replace("/usr/share/man/man7/gitrevisions.7.gz of the Arch", "/usr/share/man/man1/git-log.1.gz of the Arch", 1)))
    ok.append(variant("quote-wrong-anchor", entry=sub("- Q4 | S143 | A suffix : followed by a path names the blob or tree at the given path in the tree-ish object | <rev>:<path>", "- Q4 | S143 | A suffix : followed by a path names the blob or tree at the given path in the tree-ish object | <describeOutput>")))
    ok.append(variant("non-sequitur", entry=sub("Claim 4. The shortest abbreviation the tool will print is four digits and its default comes from configuration, so an abbreviation printed on another machine may be longer or shorter than the one a citation shows. [Q5, Q1]", "Claim 4. Branches are merged by many contributors and deployed quickly, whatever object default printing happens to show anywhere. [Q5, Q1]"), expect="PASS"))
    # engine controls on the round-62 configuration
    p = run(["--config", "openat2", "--root", str(LANE)])
    line = p.stdout.splitlines()[0] if p.stdout else p.stderr.strip()
    good = p.returncode == 0
    print(f"{'openat2-on-lane':22s} rc={p.returncode} {line} {'OK' if good else 'UNEXPECTED'}")
    ok.append(good)
    p = run(["--root", str(LANE)])  # the claim config on the lane itself: entry absent until the round lands it
    line = p.stdout.splitlines()[0] if p.stdout else p.stderr.strip()
    print(f"{'git-on-lane-base':22s} rc={p.returncode} {line} (informational: FAIL before the claim lands, PASS after)")
    print(f"C2_CONTROLS_UNEXPECTED={ok.count(False)}")
    if not a.keep:
        shutil.rmtree(w, ignore_errors=True)
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
