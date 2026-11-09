# e3: `if lines and lines[-1] == b""` vs `if lines and not lines[-1]`
# lines_of returns: lines = data.split(b"\n"); if lines and lines[-1] == b"": lines.pop()
# For every data (bytes), elements of lines are bytes objects (possibly b""). The condition guards lines being non-empty and last == b"".
# `not lines[-1]` is True iff lines[-1] == b"" (falsy bytes = only b""). So for bytes elements they're identical.
# But: could lines contain non-bytes? data.split(b"\n") on bytes always yields bytes. lines_of accepts only bytes (called with blob bytes, b"..." literals in cases). What if a future caller passed str? data.split(b"\n") would raise TypeError. So domain is bytes. Equivalence holds.
# Edge: lines == [] -> both short-circuit False. lines[-1] == b"" but lines could be [b""] (data=b"")? data=b"".split -> [b""], last is b"", pop -> []. not b"" is True. Same.
# Prove exhaustively over small inputs + all selftest inputs.
import importlib.util
spec = importlib.util.spec_from_file_location("sr", "/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/tools/search-rerun.py")
sr = importlib.util.module_from_spec(spec); spec.loader.exec_module(sr)
def orig(data):
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()
    return lines
def mutant(data):
    lines = data.split(b"\n")
    if lines and not lines[-1]:
        lines.pop()
    return lines
import itertools, random
ok = True
for n in range(0, 8):
    for combo in itertools.product([b"", b"a", b"\n", b"a\n", b"\n\n", b"a\nb"], repeat=1):
        for data in list(combo) + [b"", b"\n", b"a", b"a\n", b"\na", b"a\n\n", b"\n\n", b"a\nb\n", b"\x00\n", b"\xff\n"]:
            if orig(data) != mutant(data):
                print("DIFF", data, orig(data), mutant(data)); ok = False
# fuzz
random.seed(0)
for _ in range(2000):
    data = bytes(random.choice(b"ab\n\x00\xff") for _ in range(random.randint(0,12)))
    if orig(data) != mutant(data):
        print("FUZZ DIFF", data); ok = False; break
print("e3 equivalence over", "fuzz+exhaustive", "HOLDS" if ok else "FAILS")
# Try to find counterexample: what about a subclass of bytes with custom __eq__/__bool__? lines_of(data) where data is bytes subclass?
class Weird(bytes):
    def __eq__(self, o): return False  # never equal
    def __bool__(self): return False
print("weird eq/bool:", orig(Weird(b"a\n")), mutant(Weird(b"a\n")))
