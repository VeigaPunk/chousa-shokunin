#!/usr/bin/env python3
"""R61 post-wave supplement — 16 hazards the wave found outside the 20 frozen legs.

NOT the claim's counter (the claim froze with `c1-count.py`; this file was written after wave w1 and
changes no predicate): a supplement that shows the landed builder holds what the wave's reviewers found
the reference candidate missed. Each leg is one fixture built with `c1-count.py`'s fixture kit, a
builder run as a child (own session, 60 s), and a verdict from exit code and file tree only.

  X01 RAWLINK   `.raw` is a symlink out of the cache, a good `.txt` sidecar beside it: exit non-zero, no output.
  X02 RAWFIFO   `.raw` is a FIFO beside a good `.txt`: same.
  X03 RAW000    `.raw` (OLE magic) is mode 000 beside a good `.txt`: exit 1 or 2, no Traceback, no output.
  X04 TSV000    an earlier build's `spans.tsv` is mode 000, `--replace`: exit 2, no Traceback, tree unchanged.
  X05 SPANS000  `spans/` is mode 000, `--replace`: exit 2, no Traceback, tree unchanged.
  X06 DIRSPAN   a directory sits at a span file name: exit 2 and the tree is unchanged (nothing written first).
  X07 TMPLEFT   a leftover `.S###-N.txt.<12 hex>.tmp` in spans/: refused without `--replace` (tree unchanged);
                with `--replace` exit 0, golden tree, the leftover removed.
  X08 HARDLINK  a `.txt` capture with a second hard link: exit non-zero, no output.
  X09 OVERLAP   a quote that occurs twice only as overlapping matches ("aa" in "aaa"): refused, exit 1.
  X10 BADQUOTES a quotes file with a non-UTF-8 byte: exit 2, no Traceback.
  X11 CHECKLINK `--check` with `spans.tsv` a symlink: exit 2.
  X12 OUTLINK   `--out` is a symlink to a directory holding a foreign manifest, `--replace`: exit 2, victim unchanged.
  X13 NOCT      `tools/capture-text.py` absent and a zip capture: exit 2.
  X14 SWAPSPANS between the builder's checks and its writes (a hook after the guard, patched into a scratch
                copy; the builder waits there), `spans/` is absent at the guard and a symlink to a victim
                directory appears: the victim tree is unchanged.
  X15 SWAPOUT   the same window; `--out` is renamed away and a symlink to a victim directory takes its name:
                the victim tree is unchanged.
  X16 SWAPDIR   the same window; a real `spans/` is renamed away and a symlink to a victim directory takes its
                name: the victim tree is unchanged (writes may land in the renamed original directory).
                X14-X16 need a hook anchor in the builder (`stale = guard(ofd, sfd, manifest, files, replace)`
                for the landed builder; the reference's `rc, orphans = guard_out(...)` block; the base's
                `sd = out / "spans"` line); a builder with none of them fails the leg.

Usage: python3 corpus/evidence/round61/extras.py --builder PATH --work DIR [--seed N]
Exit 0 iff `EXTRAS=16/16`; 1 otherwise; 2 usage/env. The landed builder must read 13/13.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import pathlib
import random
import secrets
import shutil
import sys

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("c1count", HERE / "c1-count.py")
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

NAMES = ["X01 RAWLINK", "X02 RAWFIFO", "X03 RAW000", "X04 TSV000", "X05 SPANS000", "X06 DIRSPAN", "X07 TMPLEFT",
         "X08 HARDLINK", "X09 OVERLAP", "X10 BADQUOTES", "X11 CHECKLINK", "X12 OUTLINK", "X13 NOCT",
         "X14 SWAPSPANS", "X15 SWAPOUT", "X16 SWAPDIR"]


def fixture(w, rng, b):
    fx = C.Fx(w, rng, b)
    rows = fx.two_url_rows()
    fx.write_quotes(rows)
    return fx, rows


def x01(w, rng, b):
    fx, rows = fixture(w, rng, b)
    url = rows[0][1]
    outside = fx.dir / "outside.bin"
    outside.write_bytes(C.OLE + b"junk" * 64)
    (fx.cache / f"{C.key(url)}.raw").symlink_to(outside)
    r = C.run(fx, [])
    return r["rc"] != 0 and C.clean_out(fx), f"rc={r['rc']}"


def x02(w, rng, b):
    fx, rows = fixture(w, rng, b)
    os.mkfifo(fx.cache / f"{C.key(rows[0][1])}.raw")
    r = C.run(fx, [])
    return r["rc"] != 0 and not r["timeout"] and C.clean_out(fx), f"rc={r['rc']}"


def x03(w, rng, b):
    fx, rows = fixture(w, rng, b)
    p = fx.cache / f"{C.key(rows[0][1])}.raw"
    p.write_bytes(C.OLE + b"junk" * 64)
    os.chmod(p, 0)
    try:
        r = C.run(fx, [])
    finally:
        os.chmod(p, 0o600)
    return r["rc"] in (1, 2) and "Traceback" not in r["stderr"] and C.clean_out(fx), f"rc={r['rc']}"


def prior_build(fx, rows, rng):
    """A consistent earlier build for the same rows, written by the counter's golden tree."""
    for rel, bts in fx.golden(rows).items():
        p = fx.out / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(bts)


def meta(root):
    """Tree state without reading file contents: (kind, size, mtime_ns, mode) per path."""
    out = {}
    for dp, dns, fns in os.walk(root, followlinks=False):
        for n in dns + fns:
            p = pathlib.Path(dp) / n
            st = os.lstat(p)
            out[str(p.relative_to(root))] = (st.st_mode, st.st_size, st.st_mtime_ns)
    return out


def x04(w, rng, b):
    fx, rows = fixture(w, rng, b)
    prior_build(fx, rows, rng)
    (fx.out / "spans.tsv").write_bytes((fx.out / "spans.tsv").read_bytes() + b"x")  # differs
    os.chmod(fx.out / "spans.tsv", 0)
    try:
        before = meta(fx.out)
        r = C.run(fx, ["--replace"])
        same = meta(fx.out) == before
    finally:
        os.chmod(fx.out / "spans.tsv", 0o600)
    return r["rc"] == 2 and "Traceback" not in r["stderr"] and same, f"rc={r['rc']}"


def x05(w, rng, b):
    fx, rows = fixture(w, rng, b)
    prior_build(fx, rows, rng)
    os.chmod(fx.out / "spans", 0)
    try:
        r = C.run(fx, ["--replace"])
    finally:
        os.chmod(fx.out / "spans", 0o700)
    return r["rc"] == 2 and "Traceback" not in r["stderr"], f"rc={r['rc']}"


def x06(w, rng, b):
    fx, rows = fixture(w, rng, b)
    (fx.out / "spans" / f"{rows[2][0]}-1.txt").mkdir(parents=True)
    before = C.snap(fx.out)
    r = C.run(fx, ["--replace"])
    return r["rc"] == 2 and C.snap(fx.out) == before, f"rc={r['rc']}"


def x07(w, rng, b):
    fx, rows = fixture(w, rng, b)
    left = fx.out / "spans" / f".{rows[0][0]}-1.txt.{secrets.token_hex(6)}.tmp"
    left.parent.mkdir(parents=True)
    left.write_bytes(b"partial")
    before = C.snap(fx.out)
    r0 = C.run(fx, [])
    ok0 = r0["rc"] == 2 and C.snap(fx.out) == before
    r1 = C.run(fx, ["--replace"])
    return ok0 and r1["rc"] == 0 and C.snap(fx.out) == C.tree_of(fx.golden(rows)), f"rc={r0['rc']},{r1['rc']}"


def x08(w, rng, b):
    fx, rows = fixture(w, rng, b)
    p = fx.cache / f"{C.key(rows[0][1])}.txt"
    os.link(p, fx.dir / "second-name.txt")
    r = C.run(fx, [])
    return r["rc"] != 0 and C.clean_out(fx), f"rc={r['rc']}"


def x09(w, rng, b):
    fx = C.Fx(w, rng, b)
    url = fx.new_url()
    form = "lorem ipsum " * 12 + "aaa" + " dolor sit " * 12
    (fx.cache / f"{C.key(url)}.txt").write_text(form)
    fx.write_quotes([("S555", url, "aa", "corpus/knowledge/x.md")])
    r = C.run(fx, [])
    return r["rc"] == 1 and C.clean_out(fx), f"rc={r['rc']}"


def x10(w, rng, b):
    fx, rows = fixture(w, rng, b)
    q = fx.dir / "q.tsv"
    q.write_bytes(q.read_bytes() + b"S777\thttps://x.invalid/a\tcaf\xe9 here\tcorpus/knowledge/x.md\n")
    r = C.run(fx, [])
    return r["rc"] == 2 and "Traceback" not in r["stderr"] and C.clean_out(fx), f"rc={r['rc']}"


def x11(w, rng, b):
    fx, rows = fixture(w, rng, b)
    prior_build(fx, rows, rng)
    real = fx.dir / "real.tsv"
    shutil.move(fx.out / "spans.tsv", real)
    (fx.out / "spans.tsv").symlink_to(real)
    r = C.run(fx, ["--check"])
    return r["rc"] == 2, f"rc={r['rc']}"


def x12(w, rng, b):
    fx, rows = fixture(w, rng, b)
    v = fx.dir / "victim"
    (v / "spans").mkdir(parents=True)
    (v / "spans.tsv").write_bytes(b"foreign manifest")
    (v / "spans" / "S777-1.txt").write_bytes(b"foreign span")
    for p in (v / "spans.tsv", v / "spans" / "S777-1.txt"):
        os.utime(p, ns=(C.OLD_NS, C.OLD_NS))
    vb = C.snap(v, True)
    fx.out.symlink_to(v)
    r = C.run(fx, ["--replace"])
    return r["rc"] == 2 and C.snap(v, True) == vb, f"rc={r['rc']}"


def x13(w, rng, b):
    fx = C.Fx(w, rng, b)
    q = fx.quote_for()
    url = fx.add_docx_capture([q])
    fx.write_quotes([("S556", url, q, "corpus/knowledge/x.md")])
    (fx.dir / "tools" / "capture-text.py").unlink()
    r = C.run(fx, [])
    return r["rc"] == 2 and C.clean_out(fx), f"rc={r['rc']}"


HOOKS = [  # (anchor, indent) — the hook is inserted right after the anchor
    ("        stale = guard(ofd, sfd, manifest, files, replace)\n", "        "),
    ("    rc, orphans = guard_out(out, manifest, files, replace)\n    if rc:\n        return rc\n", "    "),
]
HOOK = (
    "import os as _o, time as _t\n"
    "open('hook.ready', 'w').close()\n"
    "for _ in range(400):\n"
    "    if _o.path.exists('hook.go'):\n"
    "        break\n"
    "    _t.sleep(0.05)\n"
)


def hooked(fx, builder_path):
    t = builder_path.read_text()
    for anchor, ind in HOOKS:
        if t.count(anchor) == 1:
            body = "".join(ind + ln + "\n" for ln in HOOK.splitlines())
            (fx.dir / "tools" / "build-spans.py").write_text(t.replace(anchor, anchor + body))
            return True
    base_anchor = '    sd = out / "spans"\n'
    if t.count(base_anchor) == 1:
        body = "".join("    " + ln + "\n" for ln in HOOK.splitlines())
        (fx.dir / "tools" / "build-spans.py").write_text(t.replace(base_anchor, body + base_anchor))
        return True
    return False


def swap_leg(w, rng, b, mode):
    import threading
    import time
    fx, rows = fixture(w, rng, b)
    if not hooked(fx, b):
        return False, "no hook anchor in this builder"
    v = fx.dir / "victim"
    v.mkdir()
    (v / "README.txt").write_bytes(b"victim " + fx.word().encode())
    os.utime(v / "README.txt", ns=(C.OLD_NS, C.OLD_NS))
    if mode == "swapdir":
        (fx.out / "spans").mkdir(parents=True)
    else:
        fx.out.mkdir()
    vb = C.snap(v, True)

    def attack():
        for _ in range(400):
            if (fx.dir / "hook.ready").exists():
                break
            time.sleep(0.05)
        if mode == "spans":
            (fx.out / "spans").symlink_to(v)
        elif mode == "out":
            os.rename(fx.out, fx.dir / "out.moved")
            fx.out.symlink_to(v)
        else:
            os.rename(fx.out / "spans", fx.out / "spans.moved")
            (fx.out / "spans").symlink_to(v)
        (fx.dir / "hook.go").write_text("go")

    t = threading.Thread(target=attack)
    t.start()
    r = C.run(fx, [])
    t.join()
    return C.snap(v, True) == vb, f"rc={r['rc']} victim_unchanged={C.snap(v, True) == vb}"


def x14(w, rng, b):
    return swap_leg(w, rng, b, "spans")


def x15(w, rng, b):
    return swap_leg(w, rng, b, "out")


def x16(w, rng, b):
    return swap_leg(w, rng, b, "swapdir")


PLAN = [x01, x02, x03, x04, x05, x06, x07, x08, x09, x10, x11, x12, x13, x14, x15, x16]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--builder", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--seed", type=int, default=None)
    a = ap.parse_args()
    work = pathlib.Path(a.work)
    if work.exists() and any(work.iterdir()):
        print("extras: --work must be absent or empty", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    seed = a.seed if a.seed is not None else secrets.randbits(32)
    rng = random.Random(seed)
    builder = pathlib.Path(a.builder).resolve()
    ok = 0
    out = []
    try:
        for name, fn in zip(NAMES, PLAN):
            try:
                good, detail = fn(work, rng, builder)
            except Exception as e:
                good, detail = False, f"exception {type(e).__name__}: {e}"
            ok += bool(good)
            out.append(f"EXTRA {name} {'pass' if good else 'fail'} {detail}")
    finally:
        for dp, dns, fns in os.walk(work):
            for n in dns + fns:
                try:
                    os.chmod(os.path.join(dp, n), 0o700, follow_symlinks=False)
                except (OSError, NotImplementedError):
                    pass
        shutil.rmtree(work, ignore_errors=True)
    print(f"BUILDER sha256={C.sha(builder.read_bytes())} SEED={seed}")
    print("\n".join(out))
    print(f"EXTRAS={ok}/{len(NAMES)}")
    return 0 if ok == len(NAMES) else 1


if __name__ == "__main__":
    sys.exit(main())
