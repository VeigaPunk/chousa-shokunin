#!/usr/bin/env python3
"""R62-C2 controls — shows `../c2v2-count.py` discriminates.

Prepares a scratch mirror of the lane (SOURCES.md and README.md, the positive rows
`c2v2-positive-rows.txt` inserted into the registry, the positive entry `c2v2-positive-entry.md`, the probe
script and its output copied to `corpus/evidence/round62/`), then runs the counter on the mirror once per
variant and prints `NAME rc=<n> <counter line> OK|UNEXPECTED`. Expectations: `absent`, `no-entry-rows` and every
single-defect variant FAIL, `positive` PASS. The round-61 limit "an echoing claim reaches PASS" is closed in v2
(`echo-claim` must FAIL); the remaining named limit is that a claim which adds words but does not follow from its
quote still reaches PASS (`non-sequitur`, expected PASS and recorded).
Usage: python3 run-c2v2-controls.py --work DIR   (DIR absent or empty; removed unless --keep)
"""
import argparse
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[3]
COUNTER = HERE.parent / "c2v2-count.py"
ENTRY = "corpus/knowledge/openat2-resolve-r62.md"


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
    (m / "corpus/evidence/round62").mkdir(parents=True)
    shutil.copytree(LANE / "corpus", m / "corpus", symlinks=True, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("captures", "evidence", "fixtures"))
    readme_orig = (LANE / "corpus/README.md").read_text() + "\n- " + ENTRY + " (round 62)\n"
    (m / "corpus/README.md").write_text(readme_orig)
    probe_py = HERE / "candidate-openat2-probe.py"
    probe_txt = HERE / "candidate-openat2-probe.txt"
    shutil.copy(probe_py, m / "corpus/evidence/round62/openat2-probe.py")
    shutil.copy(probe_txt, m / "corpus/evidence/round62/openat2-probe.txt")
    rows = (HERE / "c2v2-positive-rows.txt").read_text()
    entry_t = (HERE / "c2v2-positive-entry.md").read_text()
    src_orig = (m / "corpus/SOURCES.md").read_text()
    rows_into(m / "corpus/SOURCES.md", rows)
    src_pos = (m / "corpus/SOURCES.md").read_text()
    entry_p = m / ENTRY
    probe_ev = m / "corpus/evidence/round62"
    txt_orig = probe_txt.read_text()

    def variant(name, entry=entry_t, sources=src_pos, expect="FAIL", drop_entry=False, readme=readme_orig,
                probe_text=txt_orig, drop_probe=False):
        entry_p.unlink(missing_ok=True)
        if not drop_entry:
            entry_p.write_text(entry)
        (m / "corpus/SOURCES.md").write_text(sources)
        (m / "corpus/README.md").write_text(readme)
        (probe_ev / "openat2-probe.txt").write_text(probe_text)
        if drop_probe:
            (probe_ev / "openat2-probe.py").unlink(missing_ok=True)
        else:
            shutil.copy(probe_py, probe_ev / "openat2-probe.py")
        p = subprocess.run([sys.executable, str(COUNTER), "--root", str(m)], capture_output=True, text=True)
        line = p.stdout.splitlines()[0] if p.stdout else p.stderr.strip()
        got = "PASS" if p.returncode == 0 else "FAIL"
        print(f"{name:20s} rc={p.returncode} {line} {'OK' if got == expect else 'UNEXPECTED'}")
        return got == expect

    def sub(a_, b, t=entry_t):
        assert t.count(a_) == 1, a_
        return t.replace(a_, b)

    ok = []
    ok.append(variant("absent", drop_entry=True))
    ok.append(variant("no-entry-rows", sources=src_orig))
    ok.append(variant("positive", expect="PASS"))
    ok.append(variant("fabricated-quote", entry=sub("Disallow resolution of symbolic links during path resolution.", "Disallow resolution of hard links during path resolution.")))
    ok.append(variant("cross-row-quote", entry=sub("- Q6 | S139 |", "- Q6 | S138 |")))
    ok.append(variant("quote-uncited", entry=sub("in the probe. [Q5, Q9]", "in the probe. [Q5]")))
    ok.append(variant("row-queued", sources=src_pos.replace("| mined | 2026-10-28 | on-release | corpus/knowledge/openat2-resolve-r62.md |\n| S139", "| queued | 2026-10-28 | on-release | corpus/knowledge/openat2-resolve-r62.md |\n| S139", 1)))
    ok.append(variant("row-opened-old", sources=src_pos.replace("| mined | 2026-10-28 | 180d | corpus/knowledge/openat2-resolve-r62.md |", "| mined | 2026-10-27 | 180d | corpus/knowledge/openat2-resolve-r62.md |", 1)))
    ok.append(variant("row-not-used-by", sources=src_pos.replace("| 180d | corpus/knowledge/openat2-resolve-r62.md |", "| 180d | — |", 1)))
    ok.append(variant("no-limits", entry=entry_t[:entry_t.index("## Limits")]))
    ok.append(variant("limits-no-inference", entry=entry_t.replace("- [INFERENCE] ", "- ", 1)))
    ok.append(variant("junk-claim", entry=sub("Claim 3. The flags are designed for trusted programs that handle untrusted directories, and RESOLVE_BENEATH rejects any resolution that would leave the directory named by the descriptor.", "Claim 3. Lorem ipsum dolor sit amet consectetur.")))
    long_q = "The primary use case for these flags is to allow trusted programs to restrict how untrusted paths (or paths inside untrusted directories) are resolved. The full list of resolve flags is as follows:"
    ok.append(variant("quote-over-25", entry=sub("The primary use case for these flags is to allow trusted programs to restrict how untrusted paths (or paths inside untrusted directories) are resolved. |", long_q + " |")))
    ok.append(variant("no-trio", entry=entry_t.replace("verified-at:", "checked:", 1)))
    ok.append(variant("echo-claim", entry=sub("Claim 5. The installed header describes the symlink flag as one that blocks traversal through all symlinks, so a caller should read the numeric flag values from that header instead of typing them from memory. [Q6]", "Claim 5. Block traversal through all symlinks, implies OEXT_NO_MAGICLINKS. [Q6]")))
    ok.append(variant("probe-script-missing", drop_probe=True))
    ok.append(variant("probe-output-edited", probe_text=txt_orig.replace("observed=ELOOP expected=ELOOP", "observed=opened expected=ELOOP", 1)))
    ok.append(variant("probe-output-stale", probe_text=txt_orig.replace("__NR_openat2=437", "__NR_openat2=438", 1)))
    ok.append(variant("map-missing", readme=readme_orig.replace(ENTRY, "corpus/knowledge/other.md")))
    ok.append(variant("s139-wrong-file", sources=src_pos.replace("/usr/include/linux/openat2.h of the Arch", "/usr/include/linux/stat.h of the Arch", 1)))
    ok.append(variant("quote-wrong-anchor", entry=sub("- Q4 | S138 | Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd. | RESOLVE_BENEATH", "- Q4 | S138 | Do not permit the path resolution to succeed if any component of the resolution is not a descendant of the directory indicated by dirfd. | RESOLVE_NOWHERE")))
    ok.append(variant("non-sequitur", entry=sub("Claim 4. Calling openat2 from Python 3.14.8 needs ctypes or another route to syscall(2), because glibc has no wrapper and the os module exposes no openat2 function in the probe. [Q5, Q9]", "Claim 4. Python programs should always prefer openat2 because glibc has no wrapper and the os module exposes nothing, which proves it is faster. [Q5, Q9]"), expect="PASS"))
    print(f"C2V2_CONTROLS_UNEXPECTED={ok.count(False)}")
    if not a.keep:
        shutil.rmtree(w, ignore_errors=True)
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
