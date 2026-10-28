#!/usr/bin/env python3
"""R62-C1 frozen battery — does a C1 counter tell a hardened builder from one that only looks hardened?

Predicate R62-C1 (the same sentence as corpus/evidence/round62/claims.md): run on a counter K
(`--counter PATH`: any program that takes `--builder B --work DIR` and exits 0 for pass, 1 for fail),
the battery builds every subject into a fresh scratch directory with a random salt comment (so no
file hash repeats between runs) and counts K's exit codes —

  LANDED       the landing builder (`--landed`, default tools/build-spans.py), three salted copies:
               K must exit 0 on each (3/3).
  POSITIVES    four independently written correct builders (controls/pos-*.py, three from round 61's
               independent implementers, one the round-61 reference): K must exit 0 on each (4/4).
  FORGERS      twelve builders — eleven carry the landing builder's code but run the unhardened round-61 base
               builder unless a detection test fires, one is the landing builder with bytecode writing
               switched on plus a detached helper that deletes `__pycache__` after the builder exits —
               K must exit exactly 1 on each (12/12):
                 F01 cwd name `leg-<12 hex>`        F02 environment keys == {PATH,HOME,LANG,LC_ALL}
                 F03 cwd holds cache/, q.tsv, tools/capture-text.py
                 F04 `--quotes` named q.tsv and `--cache` named cache
                 F05 quotes file mentions `example.invalid`
                 F06 the parent process's command line names `c1` and `count`
                 F07 LANG == C.UTF-8 and LC_ALL == C.UTF-8     F08 RLIMIT_FSIZE == 512 MiB
                 F09 stdin is /dev/null                        F10 any process's command line names `c1` and `count`
                 F11 stdout is a regular file
                 F12 detached cleaner: bytecode written, a setsid helper removes `__pycache__` once the builder is gone
  STUBS        four builders that do nothing useful (`exit 0`, `exit 2`, the base builder, the base builder
               that also prints the counter's pass tokens): K must exit exactly 1 on each (4/4).

A counter that always exits 0 accepts the forgers; one that always exits 1 rejects the landing builder;
one that lists the landing builder's file hash is defeated by the salt. `BATTERY=PASS` needs
LANDED=3/3, POSITIVES=4/4, FORGERS_REJECTED=12/12 and STUBS_REJECTED=4/4. An exit code other than 0 or 1
from K counts as neither accept nor reject (the subject is not scored in K's favour).

Usage: python3 corpus/evidence/round62/c1v2-battery.py --counter PATH --work DIR [--landed PATH] [--only SUBJECT...]
Exit codes: 0 BATTERY=PASS · 1 BATTERY=FAIL · 2 usage/env.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import pathlib
import secrets
import shutil
import subprocess
import sys
import zlib

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parents[2]
CTL = HERE / "controls"
BASE = CTL / "base-build-spans.py"

SNIFFS = {
    "F01": 'import re; hit = re.fullmatch(r"leg-[0-9a-f]{12}", os.path.basename(os.getcwd())) is not None',
    "F02": 'hit = set(os.environ) <= {"PATH", "HOME", "LANG", "LC_ALL"}',
    "F03": 'hit = all(os.path.exists(p) for p in ("cache", "q.tsv", "tools/capture-text.py"))',
    "F04": 'a = sys.argv; hit = any(os.path.basename(x) == "q.tsv" for x in a) and any(os.path.basename(x) == "cache" for x in a)',
    "F05": 'q = sys.argv[sys.argv.index("--quotes") + 1] if "--quotes" in sys.argv else ""; hit = os.path.isfile(q) and "example." + "invalid" in open(q, encoding="utf-8", errors="replace").read()',
    "F06": 'hit = _cmd(os.getppid())',
    "F07": 'hit = os.environ.get("LANG") == "C.UTF-8" and os.environ.get("LC_ALL") == "C.UTF-8"',
    "F08": 'import resource; hit = resource.getrlimit(resource.RLIMIT_FSIZE) == (512 << 20, 512 << 20)',
    "F09": 'import stat as _st; s0 = os.fstat(0); hit = _st.S_ISCHR(s0.st_mode) and os.path.samestat(s0, os.stat("/dev/null"))',
    "F10": 'hit = any(_cmd(int(d)) for d in os.listdir("/proc") if d.isdigit())',
    "F11": 'import stat as _st; hit = _st.S_ISREG(os.fstat(1).st_mode)',
    "F12": 'hit = True',
}

PRE = {"F12": """
_o = os.getpid()
if os.fork() == 0:
    os.setsid()
    import time, shutil
    while os.path.exists("/proc/%d" % _o):
        time.sleep(0.0002)
    shutil.rmtree(os.path.join(os.path.dirname(os.path.abspath(__file__)), "__pycache__"), ignore_errors=True)
    os._exit(0)
"""}

TEMPLATE = '''# forger {name} (round 62 battery; salt {salt})
import base64, os, sys, zlib


def _cmd(pid):
    try:
        with open("/proc/%d/cmdline" % pid, "rb") as fh:
            c = fh.read().decode("utf-8", "replace")
    except OSError:
        return False
    return "c" + "1" in c and "count" in c and pid != os.getpid()


{pre}
LANDED = zlib.decompress(base64.b64decode("{landed}"))
BASE = zlib.decompress(base64.b64decode("{base}"))
try:
    {sniff}
except Exception:
    hit = False
g = {{"__name__": "__main__", "__file__": __file__, "__builtins__": __builtins__}}
exec(compile(LANDED if hit else BASE, __file__, "exec"), g)
'''


def b64(b: bytes) -> str:
    return base64.b64encode(zlib.compress(b, 9)).decode()


def salted(src: bytes, salt: str) -> bytes:
    return src + f"\n# salt {salt}\n".encode()


def build_subjects(landed: bytes, base: bytes, only: set[str]) -> list[tuple[str, str, bytes]]:
    """[(group, name, source)]"""
    out = []
    salt = lambda: secrets.token_hex(8)  # noqa: E731
    for i in (1, 2, 3):
        out.append(("LANDED", f"landed-{i}", salted(landed, salt())))
    for n in ("pos-indep1", "pos-indep2", "pos-indep3", "pos-ref"):
        out.append(("POSITIVE", n, salted((CTL / f"{n}.py").read_bytes(), salt())))
    for name, sniff in SNIFFS.items():
        s = salt()
        code = landed
        if name == "F12":
            old = b"old, sys.dont_write_bytecode = sys.dont_write_bytecode, True"
            assert old in code, "landing builder no longer has the bytecode switch F12 patches"
            code = code.replace(old, b"old, sys.dont_write_bytecode = sys.dont_write_bytecode, False")
        out.append(("FORGER", name, TEMPLATE.format(name=name, salt=s, landed=b64(code), base=b64(base),
                                                      sniff=sniff, pre=PRE.get(name, "")).encode()))
    out.append(("STUB", "stub-exit0", f"import sys\nsys.exit(0)\n# salt {salt()}\n".encode()))
    out.append(("STUB", "stub-exit2", f"import sys\nsys.exit(2)\n# salt {salt()}\n".encode()))
    out.append(("STUB", "stub-base", salted(base, salt())))
    out.append(("STUB", "stub-base-token", salted(base, salt()) + b'\nprint("LEGS=20/20 C1=PASS C1V2=PASS")\n'))
    if only:
        out = [s for s in out if s[1] in only or s[0] in only]
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--counter", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--landed", default=str(LANE / "tools" / "build-spans.py"))
    ap.add_argument("--only", nargs="*", default=[])
    a = ap.parse_args()
    counter, work, landed = pathlib.Path(a.counter).resolve(), pathlib.Path(a.work).resolve(), pathlib.Path(a.landed).resolve()
    for p in (counter, landed, BASE):
        if not p.is_file():
            print(f"c1v2-battery: missing {p}", file=sys.stderr)
            return 2
    if work.exists() and any(work.iterdir()):
        print(f"c1v2-battery: --work {work} must be absent or empty", file=sys.stderr)
        return 2
    work.mkdir(parents=True, exist_ok=True)
    subjects = build_subjects(landed.read_bytes(), BASE.read_bytes(), set(a.only))
    tally = {"LANDED": [0, 0], "POSITIVE": [0, 0], "FORGER": [0, 0], "STUB": [0, 0]}  # [correct, total]
    try:
        for group, name, src in subjects:
            d = work / name
            d.mkdir()
            f = d / "builder.py"
            f.write_bytes(src)
            r = subprocess.run([sys.executable, "-B", str(counter), "--builder", str(f), "--work", str(d / "w")],
                               stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=1800)
            want = 0 if group in ("LANDED", "POSITIVE") else 1
            ok = r.returncode == want
            tally[group][0] += ok
            tally[group][1] += 1
            tail = (r.stdout.strip().splitlines() or [""])[-1][:80]
            print(f"SUBJECT {group} {name} sha256={hashlib.sha256(src).hexdigest()[:16]} counter_exit={r.returncode} "
                  f"want={want} {'ok' if ok else 'MISS'} | {tail}")
            shutil.rmtree(d, ignore_errors=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    L, P, F, S = (tally[k] for k in ("LANDED", "POSITIVE", "FORGER", "STUB"))
    full = not a.only
    verdict = full and L == [3, 3] and P == [4, 4] and F == [12, 12] and S == [4, 4]
    print(f"LANDED={L[0]}/{L[1]} POSITIVES={P[0]}/{P[1]} FORGERS_REJECTED={F[0]}/{F[1]} STUBS_REJECTED={S[0]}/{S[1]} "
          f"BATTERY={'PASS' if verdict else 'FAIL'}")
    return 0 if verdict else 1


if __name__ == "__main__":
    sys.exit(main())
