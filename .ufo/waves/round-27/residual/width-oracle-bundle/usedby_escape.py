#!/usr/bin/env python3
"""Extra discriminating probes for the candidate shared split.

1. used-by cell containing an escaped pipe vs the real entry path that contains a pipe.
2. trailing backslash inside a cell.
3. escaped pipe adjacent to the trailing outer pipe without a space.
"""
import os
import re
import subprocess

SANDBOX = "/tmp/chousa-r27-residual-ResWidthFix"
WORK = os.path.join(SANDBOX, "work2")
P = chr(92)
REVS = {"base64eec5d": "64eec5d", "dd72641e": "dd72641e",
        "cb895a2": "cb895a2", "cand": "cand"}
ENTRY_REL = "corpus/knowledge/a|b.md"


def run(rev, registry, entry_rel, entry_abs):
    env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
    env.update(CHOUSA_STRICT="0", CHOUSA_ROOT=WORK, CHOUSA_NOW_EPOCH="1790000000")
    gate = os.path.join(SANDBOX, rev, "tools", "research-gate.sh")
    p = subprocess.run(["bash", gate, "verify-metadata", entry_abs, "--root", WORK,
                        "--registry", registry], env=env, capture_output=True,
                       text=True, timeout=120)
    out = p.stdout + p.stderr
    return p.returncode, sorted(set(re.findall(r"FINDING (\w+)", out))), out


def main():
    os.makedirs(os.path.join(WORK, "corpus", "knowledge"), exist_ok=True)
    entry_abs = os.path.join(WORK, ENTRY_REL)
    with open(entry_abs, "w") as fh:
        fh.write("source: S001\nverified-at: 2026-10-20 checked\nrecheck: 90d\n")

    cases = []
    # 1. used-by cell with an escaped pipe naming the real (pipe-containing) path
    cases.append(("usedby-escaped-pipe-vs-real-path",
                  "| id | status | used-by |\n|---|---|---|\n"
                  "| S001 | mined | corpus/knowledge/a" + P + "|b.md |\n",
                  ENTRY_REL, entry_abs))
    # 2. trailing backslash inside the last cell
    cases.append(("cell-ends-with-backslash",
                  "| id | status | used-by | x" + P + " |\n|---|---|---|---|\n"
                  "| S001 | mined | corpus/knowledge/a|b.md | y |\n",
                  ENTRY_REL, entry_abs))
    # 3. escaped pipe adjacent to the trailing outer pipe
    cases.append(("escaped-pipe-adjacent-outer",
                  "| id | status | used-by | x" + P + "||\n|---|---|---|---|\n"
                  "| S001 | mined | corpus/knowledge/a|b.md | y |\n",
                  ENTRY_REL, entry_abs))

    for name, reg, entry_rel, entry_abs in cases:
        reg_path = os.path.join(WORK, "reg-%s.md" % name)
        with open(reg_path, "w") as fh:
            fh.write(reg)
        print("==", name)
        for rev in REVS:
            rc, findings, out = run(rev, reg_path, entry_rel, entry_abs)
            print("   %-12s rc=%d findings=%s" % (rev, rc, findings or "-"))


if __name__ == "__main__":
    main()
