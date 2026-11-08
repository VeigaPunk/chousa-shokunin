import re, sys, os
path = sys.argv[1]
lines = open(path, encoding="utf-8").read().split("\n")
TALLY = re.compile(r"PASS \((\d+) cases, (\d+) skipped\)")
gs = next(k for k, l in enumerate(lines) if l.startswith("## Gates"))
ge = next(k for k in range(gs + 1, len(lines)) if re.match(r"^#{1,2} ", lines[k]))
print(f"FILE={path}")
for i, ln in enumerate(lines, 1):
    m = TALLY.search(ln)
    if not m:
        continue
    if i - 1 < ge:
        continue
    h = None
    for j in range(i - 2, -1, -1):
        if re.match(r"^#{1,6} ", lines[j]):
            h = (j + 1, lines[j])
            break
    print(f"TAIL_TALLY line={i} tally=PASS ({m.group(1)} cases, {m.group(2)} skipped) "
          f"heading_line={h[0]} heading={h[1]!r}")
