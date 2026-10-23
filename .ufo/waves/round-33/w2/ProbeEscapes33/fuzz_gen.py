#!/usr/bin/env python3
r"""200-record randomized escape-encoding differential (seed 20261023).
Every record is a flat JSON object whose span value is the same text spelled
with a random mix of raw bytes, \uXXXX escapes, \\, \/, and \" escapes. Writes
<out>/claims.jsonl and <out>/src/."""
import json, random, os, sys
out = sys.argv[1]
os.makedirs(os.path.join(out, "src"), exist_ok=True)
rng = random.Random(20261023)
ALPHA = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
SPECIAL = ['"','\\','/','{','}','[',']',',',':',' ','-','é','ü','😀','.']
def ch():
    return rng.choice(ALPHA) if rng.random() < 0.72 else rng.choice(SPECIAL)
def enc(ch):
    o = ord(ch)
    if ch == '"':  return '\\"' if rng.random() < .5 else '\\u0022'
    if ch == '\\': return '\\\\'
    if ch == '/':  return '\\/' if rng.random() < .5 else '/'
    if ch == '😀': return ch
    if o > 0x7f:   return ch if rng.random() < .5 else '\\u%04x' % o
    if ch == ' ':  return ' ' if rng.random() < .5 else '\\u0020'
    if rng.random() < .45: return '\\u%04x' % o
    return ch
rows = []
for i in range(200):
    core = [rng.choice(ALPHA)]
    for _ in range(rng.randint(5, 13)): core.append(ch())
    core.append(rng.choice(ALPHA))
    span = "".join(core); raw = "".join(enc(c) for c in span)
    name = "f%03d.txt" % i
    text = "alpha beta gamma.\nomega %s tau upsilon.\nsigma kappa lambda.\n" % span
    open(os.path.join(out, "src", name), "w", encoding="utf-8", newline="\n").write(text)
    line = ('{"id":"F%03d","source":"src/%s","span":"%s","expect":"supported","line":"%s"}'
            % (i, name, raw, '\\u0032' if i % 7 == 0 else '2'))
    assert json.loads(line)["span"] == span
    rows.append(line)
open(os.path.join(out, "claims.jsonl"), "w", encoding="utf-8", newline="\n").write("\n".join(rows) + "\n")
print("wrote %d records" % len(rows))
