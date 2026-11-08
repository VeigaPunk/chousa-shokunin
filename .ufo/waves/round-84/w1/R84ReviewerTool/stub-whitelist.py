# stub whitelist (round-84 C2 control): accept the 15 frozen positives byte-for-byte, refuse everything else.
import re, sys
POS = set()
for ln in open("corpus/evidence/round84/c2-positives.tsv", encoding="utf-8"):
    f, n, raw = ln.rstrip("\n").split("\t", 2)
    POS.add(raw)
files = []
args = sys.argv[1:]
i = 0
while i < len(args):
    if args[i] == "--root" or args[i] == "--repo":
        i += 2; continue
    if args[i] == "verify":
        i += 1; continue
    if args[i].startswith("--"):
        i += 1; continue
    files.append(args[i]); i += 1
n = ok = 0
for f in files:
    for idx, ln in enumerate(open(f, encoding="utf-8", errors="replace"), 1):
        if re.match(r"^\s*GATE-RECORD(\s|$)", ln) or ln.startswith("GATE-RECORD"):
            n += 1
            s = ln.rstrip("\n")
            if s in POS:
                ok += 1
                m = re.match(r"^\s*GATE-RECORD (S\d+)", s)
                print(f"GATE_RECORD {f}:{idx} {m.group(1) if m else chr(63)} OK")
            else:
                m = re.match(r"^\s*GATE-RECORD (S\d+)", s)
                print(f"GATE_RECORD {f}:{idx} {m.group(1) if m else chr(63)} FAIL PARSE")
print(f"GATE_RECORDS files={len(files)} records={n} ok={ok} fail={n-ok}")
sys.exit(0 if n>=1 and ok==n else 1)
