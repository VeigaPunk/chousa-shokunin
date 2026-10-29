#!/usr/bin/env python3
"""digest-prefix-check — QUALITY 125. A frozen claims file writes digests only as `sha256 prefix `<16 hex>``.

Usage: python3 -B corpus/evidence/round62/digest-prefix-check.py CLAIMS_FILE REV [--lane DIR]
Fails on: a `<8 hex>…<5-8 hex>` abbreviation or a 64-hex token (ABBREV_OR_64HEX); a prefix token that is no blob's
sha256 prefix at REV (NO_BLOB_AT_REV); a backticked path followed within 100 characters by a prefix token whose path is
absent at REV (PATH_NOT_AT_REV) or whose blob hashes differently (PAIR_MISMATCH). Output `DIGEST_PREFIX rev=... fails=<n>`;
exit 0 clean, 1 on any failure. Named limits: pairing is a heuristic over backticked paths (an unpaired token is only
existence-checked); counts stated in prose are not checked here (criterion 125 names the commands); the check reads blobs
at REV, never the working tree.
"""
import hashlib
import pathlib
import re
import subprocess
import sys

args = [a for a in sys.argv[1:] if not a.startswith("--lane")]
lane = pathlib.Path(sys.argv[sys.argv.index("--lane") + 1]) if "--lane" in sys.argv else pathlib.Path(__file__).resolve().parents[3]
if "--lane" in sys.argv:
    args = [a for a in args if a != str(lane)]
f, rev = pathlib.Path(args[0]), args[1]
G = ["git", "-C", str(lane)]
t = f.read_text(encoding="utf-8")
fails = []
for m in re.finditer(r"[0-9a-f]{8}…[0-9a-f]{5,8}|\b[0-9a-f]{64}\b", t):
    fails.append(("ABBREV_OR_64HEX", m.group()))
ls = subprocess.run(G + ["ls-tree", "-r", "-z", rev], capture_output=True, check=True).stdout.split(b"\0")
blobs = {}
for rec in ls:
    if rec:
        meta, path = rec.split(b"\t", 1)
        blobs[path.decode()] = meta.split()[2].decode()
data = subprocess.run(G + ["cat-file", "--batch"], input="\n".join(blobs.values()).encode() + b"\n",
                      capture_output=True, check=True).stdout
prefixes, i = set(), 0
while i < len(data):
    nl = data.index(b"\n", i)
    hdr = data[i:nl].split()
    if hdr[1:2] != [b"blob"]:
        break
    n = int(hdr[2])
    prefixes.add(hashlib.sha256(data[nl + 1:nl + 1 + n]).hexdigest()[:16])
    i = nl + 2 + n
toks = re.findall(r"sha256\s+prefix\s+`([0-9a-f]{16})`", t)
pairs = 0
for tok in sorted(set(toks)):
    if tok not in prefixes:
        fails.append(("NO_BLOB_AT_REV", tok))
for m in re.finditer(r"`([A-Za-z0-9_./-]+\.[A-Za-z0-9]+)`[^`]{0,100}?sha256\s+prefix\s+`([0-9a-f]{16})`", t, re.S):
    pairs += 1
    path, tok = m.group(1), m.group(2)
    if path not in blobs:
        fails.append(("PATH_NOT_AT_REV", path))
        continue
    body = subprocess.run(G + ["cat-file", "blob", blobs[path]], capture_output=True, check=True).stdout
    if hashlib.sha256(body).hexdigest()[:16] != tok:
        fails.append(("PAIR_MISMATCH", path, tok))
print(f"DIGEST_PREFIX rev={rev[:8]} prefix_tokens={len(toks)} paired={pairs} fails={len(fails)}")
for x in fails:
    print("FAIL", *x)
sys.exit(1 if fails else 0)
