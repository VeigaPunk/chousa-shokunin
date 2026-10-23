#!/usr/bin/env python3
"""Alternative 'grep' engine used only by the environment-shadow control.
Handles exactly the gate matcher shape `-a -z -b -o -P -- \\xHH...` with a
bytes.find exact search (no grep execution); every other argv is handed to
/usr/bin/grep. Logs which engine answered."""
import os, re, subprocess, sys

LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alt-engine.log")
HEX = re.compile(r"^(?:\\x[0-9a-fA-F]{2})+$")


def log(kind, argv):
    with open(LOG, "a") as f:
        f.write("%s %s\n" % (kind, " ".join(argv)))


def main(argv):
    if argv[:5] == ["-a", "-z", "-b", "-o", "-P"] and argv[5] == "--" and HEX.match(argv[6]):
        pat = bytes(int(h, 16) for h in re.findall(r"\\x([0-9a-fA-F]{2})", argv[6]))
        hay = sys.stdin.buffer.read()
        log("python", argv)
        out = sys.stdout.buffer
        i = 0
        while True:
            j = hay.find(pat, i)
            if j < 0:
                break
            out.write(str(j).encode() + b":" + pat + b"\0")
            i = j + len(pat)
        out.flush()
        return 0
    log("exec-%s" % argv[0], argv)
    return subprocess.run(["/usr/bin/grep"] + argv).returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
