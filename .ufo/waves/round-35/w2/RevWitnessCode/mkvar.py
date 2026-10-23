import importlib.util, sys
spec = importlib.util.spec_from_file_location("mw", "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py")
mw = importlib.util.module_from_spec(spec); spec.loader.exec_module(mw)
gate = open("/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh").read()
helper = "/tmp/hyaku/chousa-r35/w2/RevWitnessCode/span_search.py"

HELPER = '''import os, sys
hay = sys.stdin.buffer.read()
span = os.fsencode(sys.argv[1])
off = 0
while True:
    i = hay.find(span, off)
    if i < 0:
        break
    sys.stdout.write("%d\\n" % i)
    off = i + len(span)
'''
open(helper, "w").write(HELPER)

anchor = "  local hay=$1 span=$2\n  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then\n"
assert anchor in gate, "anchor missing"
shortcut = (
    "  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then\n"
    "    printf '%s' \"$hay\" | python3 " + helper + " \"$span\"\n"
    "    return 0\n"
    "  fi\n")

# Gate A: col-0 nested decoy def inside dispatcher + python-exact shortcut.
gateA = gate.replace(anchor,
    "  local hay=$1 span=$2\n"
    "tok_span_offsets_chunk() { :; }\n"
    + shortcut +
    "  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then\n", 1)
open("gateA-decoy.sh", "w").write(gateA)
print("A entry lines:", mw.matcher_entry_lines(gateA))

# Gate B: forged stderr stamps + same shortcut, no decoy.
gateB0 = gate.replace(anchor,
    "  local hay=$1 span=$2\n"
    "  for _wi in 1 2 3 4 5 6 7 8 9; do printf '@@WITNESS@@%s:%s \\n' \"$0\" \"@ENTRY@\" >&2; done\n"
    + shortcut +
    "  if (( ${#span} > TOK_DIRECT_SPAN_MAX )); then\n", 1)
entry = mw.matcher_entry_lines(gateB0)["chunk"]
gateB = gateB0.replace('"@ENTRY@" >&2', '"%d" >&2' % entry, 1)
open("gateB-forge.sh", "w").write(gateB)
print("B entry lines:", mw.matcher_entry_lines(gateB), "forged line:", entry)
