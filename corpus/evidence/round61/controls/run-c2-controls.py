#!/usr/bin/env python3
"""R61-C2 controls — shows `../c2-count.py` discriminates.

Prepares a scratch mirror of the lane (a copy of `corpus/`, the S136 file, the positive rows
`c2-positive-rows.txt` inserted into the registry, the positive entry `c2-positive-entry.md`),
then runs the counter on the mirror once per variant and prints `NAME rc=<n> <counter line>`.
Expectations: `absent` and `no-entry-rows` FAIL, `positive` PASS, every single-defect variant FAIL
(listed below), and `echo-claims` PASS — a recorded limit: a claim that echoes its quote reaches
PASS, because the counter is structural.
Usage: python3 run-c2-controls.py --work DIR   (DIR absent or empty; removed unless --keep)
"""
import argparse, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[3]
COUNTER = HERE.parent / "c2-count.py"
ENTRY = "corpus/knowledge/derived-output-safety-r61.md"


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
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args()
    w = pathlib.Path(a.work)
    if w.exists() and any(w.iterdir()):
        print("work must be absent or empty", file=sys.stderr)
        return 2
    m = w / "mirror"
    (m / ".ufo/waves/round-56/w1").mkdir(parents=True)
    shutil.copytree(LANE / "corpus", m / "corpus", symlinks=True)
    shutil.copy(LANE / ".ufo/waves/round-56/w1/R55W2SentBuilder.md", m / ".ufo/waves/round-56/w1/")
    rows = (HERE / "c2-positive-rows.txt").read_text()
    entry_t = (HERE / "c2-positive-entry.md").read_text()
    src_orig = (m / "corpus/SOURCES.md").read_text()
    rows_into(m / "corpus/SOURCES.md", rows)
    src_pos = (m / "corpus/SOURCES.md").read_text()
    entry_p = m / ENTRY

    def variant(name, entry=entry_t, sources=src_pos, expect="FAIL", drop_entry=False):
        entry_p.unlink(missing_ok=True)
        if not drop_entry:
            entry_p.write_text(entry)
        (m / "corpus/SOURCES.md").write_text(sources)
        p = subprocess.run([sys.executable, str(COUNTER), "--root", str(m)], capture_output=True, text=True)
        line = p.stdout.splitlines()[0] if p.stdout else p.stderr.strip()
        got = "PASS" if p.returncode == 0 else "FAIL"
        print(f"{name:18s} rc={p.returncode} {line} {'OK' if got == expect else 'UNEXPECTED'}")
        return got == expect

    ok = []
    ok.append(variant("absent", drop_entry=True))
    ok.append(variant("no-entry-rows", sources=src_orig))
    ok.append(variant("positive", expect="PASS"))
    def sub(a, b, t=entry_t):
        assert t.count(a) == 1, a
        return t.replace(a, b)
    ok.append(variant("fabricated-quote", entry=sub("then the open fails, with the error ELOOP", "then the open succeeds, with the error ELOOP")))
    ok.append(variant("cross-row-quote", entry=sub("- Q4 | S135 |", "- Q4 | S134 |")))
    ok.append(variant("quote-uncited", entry=sub("each time exiting 0. [Q7, Q8]", "each time exiting 0. [Q7]")))
    ok.append(variant("row-queued", sources=src_pos.replace("| mined | 2026-10-28 | on-release | corpus/knowledge/derived-output-safety-r61.md |\n| S135", "| queued | 2026-10-28 | on-release | corpus/knowledge/derived-output-safety-r61.md |\n| S135", 1)))
    ok.append(variant("row-opened-old", sources=src_pos.replace("| mined | 2026-10-28 | on-release | corpus/knowledge/derived-output-safety-r61.md |\n| S136", "| mined | 2026-10-27 | on-release | corpus/knowledge/derived-output-safety-r61.md |\n| S136", 1)))
    ok.append(variant("row-not-used-by", sources=src_pos.replace("| 180d | corpus/knowledge/derived-output-safety-r61.md |", "| 180d | — |", 1)))
    ok.append(variant("no-limits", entry=entry_t[:entry_t.index("## Limits")]))
    ok.append(variant("junk-claim", entry=sub("Claim 2. Creating a file with O_CREAT and O_EXCL fails on any existing path that is a symbolic link, regardless of where the link points, so a fresh temporary name cannot be written through a planted link.", "Claim 2. Lorem ipsum dolor sit amet consectetur.")))
    long_q = "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP. Symbolic links in earlier components of the pathname will still be followed."
    ok.append(variant("quote-over-25", entry=sub("If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP. |", long_q + " |")))
    ok.append(variant("no-trio", entry=entry_t.replace("verified-at:", "checked:", 1)))
    echo = entry_t.replace("Claim 2. Creating a file with O_CREAT and O_EXCL fails on any existing path that is a symbolic link, regardless of where the link points, so a fresh temporary name cannot be written through a planted link.", "Claim 2. symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points.")
    ok.append(variant("echo-claims", entry=echo, expect="PASS"))
    print(f"C2_CONTROLS_UNEXPECTED={ok.count(False)}")
    if not a.keep:
        shutil.rmtree(w, ignore_errors=True)
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
