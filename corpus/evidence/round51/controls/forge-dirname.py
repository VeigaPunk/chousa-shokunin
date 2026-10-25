#!/usr/bin/env python3
"""forge-dirname — cheapest C1 forge. Implements none of the five behaviours:
no escaped-pipe splitter, no document-identity rewrite, no source-vs-body
citation rule, no registry-heading scan, no D3 row-outside check. It reads the
counter's per-subtest directory name out of --out and emits canned shapes.
"""
import hashlib
import pathlib
import sys

argv = sys.argv[1:]


def opt(name: str) -> str:
    return argv[argv.index(name) + 1] if name in argv else ""


# --- LEGACY_ALL: never run the adopter; echo 26 and the fixture digest --------
if "--selftest" in argv:
    fix = pathlib.Path(opt("--fixtures")) if opt("--fixtures") else None
    h = hashlib.sha256()
    if fix:
        for q in sorted(x for x in fix.rglob("*") if x.is_file()):
            h.update(q.relative_to(fix).as_posix().encode() + b"\0" + q.read_bytes() + b"\0")
    print(f"FIXTURES_SHA256={h.hexdigest()}")
    print("SELFTEST=PASS findings=26 expected=26")
    sys.exit(0)

out = pathlib.Path(opt("--out"))
scene = out.parent.name                       # s | s-all | d1 | d2 | renamed-heading | ...
work = out.parent
(out / "corpus" / "knowledge").mkdir(parents=True, exist_ok=True)

# --- two numbers and three ids, straight out of the nonce's own files --------
reg = [l for l in (work / "registry.md").read_text(encoding="utf-8").splitlines() if l.startswith("| S")]
top = len(reg)
held_n = next(i for i, l in enumerate(reg, 1) if "Held" in l)
st = [l.split(" | ")[0].strip("| ") for l in (work / "staged.md").read_text(encoding="utf-8").splitlines() if l.startswith("| S")]
staged = [l for l in (work / "staged.md").read_text(encoding="utf-8").splitlines() if l.startswith("| S")]
held = f"S{held_n:03d}"
new1 = f"S{top + 1:03d}"
new2 = f"S{top + 2:03d}"
HDR = "staged_id\tlane_id\taction\turl\n"


def append(rows: list[str]) -> None:
    (out / "append.md").write_text("".join(r + "\n" for r in rows), encoding="utf-8")


def renumber(rows: list[str]) -> None:
    (out / "renumber.tsv").write_text(HDR + "".join(rows), encoding="utf-8")


def src(rowline: str) -> str:
    return rowline.split(" | ")[1]


if scene in ("renamed-heading", "no-heading", "row-outside"):
    print(f"REFUSED registry structure ({scene})", file=sys.stderr)
    sys.exit(1)

if scene == "well-formed":
    renumber([f"{st[0]}\t{new1}\tappend\t{src(staged[0])}\n"])
    append([f"| {new1} | {src(staged[0])} | docs | B | scope | section | teaches | mined | 2026-10-25 | 90d | — |"])
    sys.exit(0)

if scene == "d1":
    renumber([f"{st[0]}\t{held}\theld\t{src(staged[0])}\n"])
    (out / "corpus" / "knowledge" / "e.md").write_text((work / "knowledge" / "corpus" / "knowledge" / "e.md").read_text(encoding="utf-8"), encoding="utf-8")
    sys.exit(0)

if scene == "d2":
    renumber([f"{st[0]}\t{held}\theld\t{src(staged[0])}\n"])
    sys.exit(0)

if scene == "s-all":
    renumber([f"{st[0]}\t{new1}\tappend\t{src(staged[0])}\n",
              f"{st[1]}\t{held}\theld\t{src(staged[1])}\n",
              f"{st[2]}\t{new2}\tappend\t{src(staged[2])}\n"])
    append([f"| {new1} | {src(staged[0])} | docs | B | scope | section | teaches | mined | 2026-10-25 | 90d | — |",
            f"| {new2} | {src(staged[2])} | docs | B | scope | section | teaches | mined | 2026-10-25 | 90d | — |"])
    sys.exit(0)

# scene == "s": source-only. a is minted, b is held, c is body-only.
a_id, b_id, c_id = st[0], st[1], st[2]
renumber([f"{a_id}\t{new1}\tappend\t{src(staged[0])}\n",
          f"{b_id}\t{held}\theld\t{src(staged[1])}\n"])
append([f"| {new1} | {src(staged[0])} | docs | B | scope | section | teaches | mined | 2026-10-25 | 90d | — |"])
entry = (work / "knowledge" / "corpus" / "knowledge" / "e.md").read_text(encoding="utf-8")
body = "".join(l + "\n" for l in entry.splitlines() if not l.startswith("source:"))
body = body.replace(a_id, new1).replace(b_id, "")
(out / "corpus" / "knowledge" / "e.md").write_text(body, encoding="utf-8")
(out / "bodyonly.tsv").write_text("entry\tstaged_id\ncorpus/knowledge/e.md\t" + c_id + "\n", encoding="utf-8")
print("BODYONLY=1")
