import importlib.util, sys
spec = importlib.util.spec_from_file_location("sr", "/fast/scratch/hyaku/chousa-r98/R98ReviewerC1/repo/tools/search-rerun.py")
sr = importlib.util.module_from_spec(spec); spec.loader.exec_module(sr)
def probe(name, fn):
    r = fn()
    print(name, r)
# r17: row without end pipe
try:
    sr.parse_text(sr.ST_HEAD + sr.st_row().rstrip("\n").rstrip("|") + "\n")
    print("r17 no raise")
except sr.Setup as e:
    print("r17 refused", e.code)
# r18
try:
    sr.parse_text((sr.ST_HEAD + sr.st_row()).replace("## Searches","## Searches catalog"))
    print("r18 no raise")
except sr.Setup as e:
    print("r18 refused", e.code)
# r19
try:
    sr.parse_text((sr.ST_HEAD + sr.st_row()) + "\n" + (sr.ST_HEAD + sr.st_row()))
    print("r19 no raise")
except sr.Setup as e:
    print("r19 refused", e.code)
# r20
try:
    sr.parse_text((sr.ST_HEAD + sr.st_row()).replace("|---|---|---|---|---|---|---|---|","|--|--|--|--|--|--|--|--|"))
    print("r20 no raise")
except sr.Setup as e:
    print("r20 refused", e.code)
# r21
try:
    sr.parse_text(sr.ST_HEAD + sr.st_row(hits="2", hit_set="-"))
    print("r21 no raise")
except sr.Setup as e:
    print("r21 refused", e.code)
# r22
try:
    sr.parse_text(sr.ST_HEAD + sr.st_row(where="corpus/./*.txt"))
    print("r22 no raise")
except sr.Setup as e:
    print("r22 refused", e.code)
# r23
try:
    sr.parse_text(sr.ST_HEAD + sr.st_row(expr="`abc"))
    print("r23 no raise")
except sr.Setup as e:
    print("r23 refused", e.code)
# r24
try:
    sr.parse_text(sr.ST_HEAD + sr.st_row(engine="regex", expr="`[[:ALPHA:]]+`"))
    print("r24 no raise")
except sr.Setup as e:
    print("r24 refused", e.code)
# r25 digest
print("r25", sr.digest(["corpus/\u01ce.txt", "corpus/\udca8.txt"]), sr.ST_NONUTF8_DIGEST)
# r26
import os
os.environ["GITFOO"]="1"
print("r26 GITFOO in env:", sr.git_env().get("GITFOO"))
del os.environ["GITFOO"]
# r27
print("r27", sr.static_dir("a[b]/c.txt"), sr.static_dir("a/[x]/c.txt"))
# r31
needle = sr.parse_text(sr.ST_HEAD + sr.st_row(expr="`PRESS`"))[0]
print("r31 hit mid", sr.hit(b"a PRESS\n", needle), "hit miss", sr.hit(b"a PRES\n", needle))
# r33
base = {"corpus/a.txt": b"PRESS here\n", "corpus/b.txt": b"no\n", "corpus/c.txt": b"PRESS too\n", "corpus/.d.txt": b"PRESS hidden\n", "corpus/e/f.txt": b"PRESS nested\n"}
def mem(files):
    return lambda r: sorted(p for p in files if sr.matches(p, r["globs"]) and sr.hit(files[p], r))
rows = sr.parse_text(sr.ST_HEAD + sr.st_row(hits="1", hit_set="corpus/a.txt"))
f, ok, same, lines = sr.evaluate(rows, mem(base), mem(base), False)
print("r33", f, ok, same, lines)
