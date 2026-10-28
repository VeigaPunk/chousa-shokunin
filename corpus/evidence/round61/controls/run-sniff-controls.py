#!/usr/bin/env python3
"""Controls for ../sniff-sweep.py: forge fragments the wave's CritC1Sniff/CritC1Seq/CritC1Rss seats built
(re-written here from their reports' descriptions, not their files) must be flagged; a layout sniff that
stays inside the allowlist is NOT flagged (recorded limit). Usage: python3 run-sniff-controls.py"""
import pathlib, subprocess, sys, tempfile, os

SWEEP = pathlib.Path(__file__).resolve().parent.parent / "sniff-sweep.py"
FRAG = {
    "ctypes-ppid": ("import ctypes\nppid = getattr(ctypes.CDLL(None), 'getp' + 'pid')()\n", 1),
    "cwd-regex": ("import os, re\nctx = re.match(r'^leg.[0-9a-f]{12}$', os.path.basename(os.getcwd()))\n", 1),
    "env-keys": ("import os\nctx = set(os.environ) == {'PATH', 'HOME', 'LANG', 'LC_ALL'}\n", 1),
    "ps-seed": ("import subprocess\nout = subprocess.run(['ps', '-o', 'args=', '-p', '1'], capture_output=True)\n", 1),
    "setsid-helper": ("import os\nif os.fork() == 0:\n    os.setsid()\n", 1),
    "memfd": ("import os\nfd = os.memfd_create('x')\n", 1),
    "proc-path": ("p = '/pr' + 'oc/self/cmdline'\nq = open('/proc/self/cmdline').read()\n", 1),
    "layout-sniff": ("import os\nctx = os.path.exists('q.tsv') and os.path.isdir('cache')\n", 0),
    "clean": ("import os\nx = os.path.join('a', 'b')\n", 0),
}


def main():
    bad = 0
    d = pathlib.Path(tempfile.mkdtemp(dir=os.environ.get("TMPDIR") or None))
    try:
        for name, (src, want) in FRAG.items():
            f = d / f"{name}.py"
            f.write_text(src)
            rc = subprocess.run([sys.executable, str(SWEEP), str(f)], capture_output=True, text=True).returncode
            ok = (rc == 1) == bool(want)
            bad += not ok
            print(f"{name:14s} sweep_rc={rc} expect={'flagged' if want else 'not flagged'} {'OK' if ok else 'UNEXPECTED'}")
    finally:
        for p in d.iterdir():
            p.unlink()
        d.rmdir()
    print(f"SNIFF_CONTROLS_UNEXPECTED={bad}")
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
