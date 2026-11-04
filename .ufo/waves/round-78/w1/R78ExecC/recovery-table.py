#!/usr/bin/env python3
"""Receipt: one v5-shaped salted copy per subject, probe run on each, recovery printed.

Mirrors matrix-battery-v5.py:salted_copy exactly (random interior top-level statement,
`import os as _r78<12 hex>` or `_r78<12 hex> = <int>`) and shows the deleted line.
"""
import pathlib, secrets, subprocess, sys

L = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
SUBJECTS = [("POSITIVE", "successor-counter", L / "corpus/evidence/round74/correction-count.py"),
            ("POSITIVE", "ref-counter", L / "corpus/evidence/round75/ref-counter.py")]
SUBJECTS += [("FORGER", p.stem, p) for p in sorted((L / "corpus/evidence/round76/forgers").glob("*.py"))]
PROBE = pathlib.Path(__file__).with_name("residual-matrix.py")

for group, name, source in SUBJECTS:
    text = source.read_text()
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] += "\n"
    salt_name = "_r78" + secrets.token_hex(6)
    if secrets.randbits(1):
        inserted = f"import os as {salt_name}\n"
    else:
        inserted = f"{salt_name} = {secrets.randbelow(10 ** 6)}\n"
    pos = min(len(lines) - 1, max(1, secrets.randbelow(max(1, len(lines) - 1))))
    lines.insert(pos, inserted)
    copy = pathlib.Path("subject-copy.py")
    copy.write_text("".join(lines))
    p = subprocess.run([sys.executable, "-B", str(PROBE), "--counter", str(copy),
                        "--work", "w"], capture_output=True, text=True)
    ident = next(l for l in p.stdout.splitlines() if l.startswith("IDENT"))
    print(f"{group:8} {name:22} exit={p.returncode} deleted={inserted.strip()!r} {ident}")
    copy.unlink()
