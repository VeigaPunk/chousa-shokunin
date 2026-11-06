#!/usr/bin/env python3
"""Cheap C2 control: keys on the battery's marker word Zyzzyva only."""
import re
import sys

ALL = "PARSE,REGISTRY,TIER,CAPTURE_PATH,CAPTURE_KEY,CAPTURE_SHA,REFETCH,WORDS,QUOTE_LEN,QUOTE_ABSENT,REV,LINE"
REC = re.compile(r"^GATE-RECORD(?:\s|$)")


def main(argv):
    if len(argv) < 2 or argv[1] != "verify":
        return 2
    files = []
    i = 2
    while i < len(argv):
        a = argv[i]
        if a in ("--root", "--repo"):
            i += 2
            continue
        if a.startswith("--"):
            i += 2
            continue
        files.append(a)
        i += 1
    n = ok = 0
    for f in files:
        try:
            fh = open(f, encoding="utf-8", errors="replace")
        except OSError:
            return 2
        with fh:
            for ln, line in enumerate(fh, 1):
                s = line.lstrip()
                if not REC.match(s):
                    continue
                n += 1
                if "Zyzzyva" in line:
                    print(f"GATE_RECORD {f}:{ln} ? FAIL {ALL}")
                else:
                    ok += 1
                    print(f"GATE_RECORD {f}:{ln} ? OK")
    print(f"GATE_RECORDS files={len(files)} records={n} ok={ok} fail={n - ok}")
    return 0 if n >= 1 and ok == n else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
