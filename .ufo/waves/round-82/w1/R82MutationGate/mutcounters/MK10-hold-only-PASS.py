#!/usr/bin/env python3
"""k2-gate-r82.py — round-82 C1 counter (frozen at the round-82 freeze commit).

Runs the SKILL.md `## Checklist (executable)` Run lines of item 2 (negative claim carries
its sweep) and item 4 (rejected source kept with reason and flip-condition) exactly as the
tree under test prints them, on every record of the frozen manifest
`corpus/evidence/round82/c1-manifest.tsv`, from the tree root (cwd = --root).

A `refuse` row is ok iff the Run line exits 1 and the finding id in `need` is observed
(in the Run line's output; for an item-2 row also in `research-gate.sh verify <record>`
output, because the item-2 line consumes verify's output with `grep -q`). Exit 2 is a
usage error, never a refusal.
Each Run line must equal its frozen base text (FROZEN_RUNLINE); a changed line counts as
not found.
A `pass` row is ok iff the Run line exits 0, prints `RESEARCH_GATE: CLEAN`, and prints
the `need` substring (e.g. `REJECTIONS_OK=1/1`, so a rejection the gate never read fails).

Summary: RUNLINES=r/2 K2_REFUSED=a/A HOLD_REFUSED=b/B CLASS_REFUSED=c/C POSITIVE=p/P
K2_GATE=PASS iff every fraction is full (computed from the same integers it prints);
exit 0 PASS, 1 FAIL, 2 usage/manifest/record error.

Usage: python3 -B corpus/evidence/round82/k2-gate-r82.py --root <tree>
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import shlex
import subprocess
import sys

MANIFEST = "corpus/evidence/round82/c1-manifest.tsv"
RECDIR = "corpus/evidence/round82/c1-records"
ITEM_TEXT = {
    2: "A negative claim carries its search sweep",
    4: "A rejected source is kept with its rejection reason",
}
GROUPS = ("k2", "hold", "class", "positive")
# The claim is a gate change, not a Run-line change: the two Run lines must stay byte-equal to
# their base (5d792e1e) text, so a Run line keyed to the fixtures cannot score.
FROZEN_RUNLINE = {
    2: "f=<record.md>; ! bash tools/research-gate.sh verify \"$f\" --root . | grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps \"$f\" --root .",
    4: "bash tools/research-gate.sh verify-sweeps <record.md> --root .",
}


def die(msg: str) -> None:
    print(f"K2_GATE_ERROR {msg}")
    sys.exit(2)


def run_lines(skill: str) -> dict[int, str]:
    lines = skill.splitlines()
    out: dict[int, str] = {}
    for item, text in ITEM_TEXT.items():
        for i, ln in enumerate(lines):
            if ln.startswith("- [ ] ") and text in ln:
                for nxt in lines[i + 1:i + 4]:
                    m = re.match(r"^\s+- Run: `([^`]+)`", nxt)
                    if m:
                        out[item] = m.group(1)
                        break
                break
    return out


def run(cmd: str, root: str) -> tuple[int, str]:
    env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
    p = subprocess.run(["bash", "-c", cmd], cwd=root, env=env, capture_output=True,
                       text=True, timeout=300)
    return p.returncode, p.stdout + p.stderr


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    for rel in ("SKILL.md", "tools/research-gate.sh", MANIFEST):
        if not os.path.isfile(os.path.join(root, rel)):
            die(f"missing {rel}")
    with open(os.path.join(root, MANIFEST), "rb") as fh:
        mbytes = fh.read()
    rows = [ln.split("\t") for ln in mbytes.decode().splitlines()[1:] if ln.strip()]
    if not rows or any(len(r) != 7 for r in rows):
        die("manifest malformed")
    rec_digest = hashlib.sha256()
    for r in sorted({r[5] for r in rows}):
        p = os.path.join(root, RECDIR, r)
        if not os.path.isfile(p):
            die(f"record missing {r}")
        with open(p, "rb") as fh:
            rec_digest.update(r.encode() + b"\0" + hashlib.sha256(fh.read()).digest())
    with open(os.path.join(root, "SKILL.md"), encoding="utf-8") as fh:
        rl = run_lines(fh.read())
    print(f"MANIFEST_SHA256={hashlib.sha256(mbytes).hexdigest()} RECORDS_DIGEST={rec_digest.hexdigest()} rows={len(rows)}")
    for item in (2, 4):
        if item in rl and rl[item] != FROZEN_RUNLINE[item]:
            print(f"RUNLINE item={item} found=changed cmd={rl[item]}")
            del rl[item]
        else:
            print(f"RUNLINE item={item} found={'yes' if item in rl else 'no'} cmd={rl.get(item, '-')}")
    ok = {g: 0 for g in GROUPS}
    tot = {g: 0 for g in GROUPS}
    for cid, group, item_s, expect, need, rec, _origin in rows:
        if group not in GROUPS or expect not in ("refuse", "pass") or item_s not in ("2", "4"):
            die(f"bad row {cid}")
        item = int(item_s)
        tot[group] += 1
        path = os.path.join(root, RECDIR, rec)
        if item not in rl:
            print(f"K2CASE id={cid} group={group} item={item} expect={expect} rc=- verdict=bad why=no-runline")
            continue
        if "<record.md>" not in rl[item]:
            print(f"K2CASE id={cid} group={group} item={item} expect={expect} rc=- verdict=bad why=no-placeholder")
            continue
        cmd = rl[item].replace("<record.md>", shlex.quote(path))
        rc, out = run(cmd, root)
        seen = set(re.findall(r"^FINDING (\S+)", out, re.M))
        if item == 2 and expect == "refuse":
            _, vout = run(f"bash tools/research-gate.sh verify {shlex.quote(path)} --root .", root)
            seen |= set(re.findall(r"^FINDING (\S+)", vout, re.M))
        if expect == "refuse":
            good = rc == 1 and need in seen
        else:
            good = rc == 0 and "RESEARCH_GATE: CLEAN" in out and need in out
        ok[group] += int(good)
        print(f"K2CASE id={cid} group={group} item={item} expect={expect} need={need} rc={rc} "
              f"findings={','.join(sorted(seen)) or '-'} verdict={'ok' if good else 'bad'}")
    nrl = sum(1 for i in (2, 4) if i in rl)
    full = nrl == 2 and ok["hold"] == tot["hold"] and tot["hold"] > 0
    print(f"RUNLINES={nrl}/2 K2_REFUSED={ok['k2']}/{tot['k2']} HOLD_REFUSED={ok['hold']}/{tot['hold']} "
          f"CLASS_REFUSED={ok['class']}/{tot['class']} POSITIVE={ok['positive']}/{tot['positive']}")
    print(f"K2_GATE={'PASS' if full else 'FAIL'}")
    return 0 if full else 1


if __name__ == "__main__":
    sys.exit(main())
