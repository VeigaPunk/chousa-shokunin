#!/usr/bin/env python3
"""Contract probes at 64 KiB line size, base vs landed gate (C locale):
A: 64 KiB of escaped decoy text inside a string member the reader never reads
   (contract item 3: string content is never structure).
B: a duplicated top-level read field in a 64 KiB line (contract item 2).
C: two 64 KiB pad records in one file (record-count additivity).
D: grep -P argument-size ceiling for a locatable span (MAX_ARG_STRLEN/6)."""
import hashlib
import json
import os
import resource
import subprocess
import time

B = os.path.dirname(os.path.abspath(__file__))
G = {"base": os.path.join(B, "gate-base.sh"), "landed": os.path.join(B, "gate-landed.sh")}
P = os.path.join(B, "probe")
os.makedirs(os.path.join(P, "tmp"), exist_ok=True)


def pad(n):
    s = "w"
    while len(s) + 2 <= n:
        s += " w"
    rem = n - len(s)
    if rem == 1:
        s += "w"
    elif rem >= 2:
        s += " " + "w" * (rem - 1)
    return s


def run(name, gate, claims, root, loc="C"):
    outf = os.path.join(P, name + ".out")
    errf = os.path.join(P, name + ".err")
    env = dict(os.environ)
    env.update({"LC_ALL": loc, "LANG": loc, "CHOUSA_ROOT": root,
                "TMPDIR": os.path.join(B, "tmp")})
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    cmd = ["timeout", "300", "bash", gate, "verify-claims", claims]
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN); t0 = time.monotonic()
    with open(outf, "wb") as fo, open(errf, "wb") as fe:
        p = subprocess.run(cmd, cwd=root, env=env, stdout=fo, stderr=fe)
    wall = time.monotonic() - t0
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
    out = open(outf).read()
    lines = [l for l in out.splitlines() if l.startswith(("CLAIM", "RESEARCH_GATE:", "VERDICT"))]
    err = open(errf).read().strip().splitlines()[:2]
    res = {"name": name, "gate": os.path.basename(gate), "exit": p.returncode,
           "wall_s": round(wall, 3), "cpu_s": round(cpu, 3),
           "lines": lines[:4], "err": err, "claims_bytes": os.path.getsize(claims)}
    print(json.dumps(res), flush=True)
    return res


def mk(name, record, source, many=False):
    d = os.path.join(P, name)
    os.makedirs(os.path.join(d, "spans"), exist_ok=True)
    open(os.path.join(d, "spans", "src.txt"), "w").write(source)
    open(os.path.join(d, "claims.jsonl"), "w").write(record)
    return d, os.path.join(d, "claims.jsonl")


def main():
    rows = []
    # A: escaped decoy member text inside a 64 KiB string value
    decoy = ' \\"line\\":\\"9\\", \\"sha256\\":\\"deadbeef\\", '
    body = (decoy * (65536 // len(decoy) + 1))[:65536 - 64].rstrip() + " tail"
    a = ('{"id":"D64","source":"spans/src.txt","span":"distinct-marker-A",'
         '"expect":"supported","note":"%s"}\n' % body)
    d, c = mk("A-decoy-in-string", a, "heading\ndistinct-marker-A\n")
    for g in ("base", "landed"):
        rows.append(run("A.%s" % g, G[g], c, d))
    # B: duplicated top-level read field in a 64 KiB line
    bb = ('{"id":"B64","source":"spans/src.txt","span":"distinct-marker-B",'
          '"expect":"supported","line":"1","note":"%s","line":"2"}\n' % pad(65536 - 150))
    d, c = mk("B-dup-line", bb, "heading\ndistinct-marker-B\n")
    for g in ("base", "landed"):
        rows.append(run("B.%s" % g, G[g], c, d))
    # C: two 64 KiB pad records, additive check
    two = []
    for k, tag in enumerate(("C64a", "C64b")):
        two.append('{"id":"%s","source":"spans/src.txt","span":"marker-%s",'
                   '"expect":"supported","note":"%s"}' % (tag, tag, pad(65536 - 150)))
    d, c = mk("C-two-64k", "\n".join(two) + "\n",
              "heading\nmarker-C64a\nmarker-C64b\n")
    for g in ("base", "landed"):
        rows.append(run("C.%s" % g, G[g], c, d))
    # D: grep -P argument ceiling for tok_span_at's hex pattern (6 bytes/char)
    out = []
    for n in (21000, 21845, 21846, 22000):
        span = ("h%d " % n + pad(n - 8))[:n]
        reg = "".join("\\x%02x" % b for b in span.encode())
        r = subprocess.run(["grep", "-a", "-z", "-b", "-o", "-P", "--", reg],
                           input=span.encode() + b"\x00", capture_output=True)
        out.append({"span_chars": n, "regex_bytes": len(reg), "rc": r.returncode,
                    "out_len": len(r.stdout), "err": r.stderr.decode()[:80].strip()})
    print(json.dumps({"D_grep_arg_ceiling": out}), flush=True)
    open(os.path.join(B, "probes.jsonl"), "w").write(
        "\n".join(json.dumps(r) for r in rows) + "\n")


if __name__ == "__main__":
    main()
