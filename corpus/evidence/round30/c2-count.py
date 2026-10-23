#!/usr/bin/env python3
"""Round-30 C2 counter: the fetch bounds that tools/quote-reopen.py states hold under
slow-drip responses and DNS rebinding.

Usage (lane root):
    python3 corpus/evidence/round30/c2-count.py [--tool tools/quote-reopen.py] [--receipt OUT.json]

Prints one line `QUOTE_REOPEN_FETCH_BOUND_MATCH=<n>/<t>` and exits 0 iff n == t == FROZEN_TOTAL.
Exit 1 is a miss. Exit 2 is a failed measurement (harness error), never a pass.

Each item is one separate run of the candidate (one registry URL) inside the loopback
harness (qr_harness.py), with the module constant DEADLINE set to 3.0 s. Nothing reaches the
network: names resolve only from the run's map and every connection lands on the harness
server or is refused. Paths, words, ids, host names and global addresses are drawn from a
fresh 64-bit os.urandom seed on every run; there is no seed option.

An item MATCHES iff all three hold:
  (a) the item's verdict equals its label;
  (b) the run's wall time is at most BOUND = DEADLINE + 2.0 s = 5.0 s (a run is killed at 15 s);
  (c) the run made no connection to an address outside the validated set, that is, every
      logged connect destination is one of the global addresses the harness routes.
      A connect to a loopback, private or other unrouted address breaks (c).

FROZEN_TOTAL = 20 items:
  drip-head       2  UNREACHABLE  headers dripped one byte per 0.2 s, never finished
  drip-body       2  UNREACHABLE  Content-Length 200000, body dripped one byte per 0.2 s
  drip-chunked    2  UNREACHABLE  chunked body, one 1-byte chunk per 0.2 s, never finished
  stall-body      1  UNREACHABLE  headers then 20 bytes then silence
  rebind-loop     3  VERBATIM     host resolves to a global address on the first lookup and
                                  to 127.0.0.1 on every later lookup
  rebind-private  1  VERBATIM     same, later lookups answer 10.x.y.z
  rebind-redirect 1  VERBATIM     a stable host redirects to a host that rebinds to 127.0.0.1
  stable-present  2  VERBATIM     ordinary page, quote present
  stable-absent   1  ABSENT       ordinary page, quote absent
  slow-ok         1  VERBATIM     body in 6 pieces 0.3 s apart (about 1.8 s), inside DEADLINE
  multi-address   1  VERBATIM     host resolves to two global addresses
  mixed-address   1  UNREACHABLE  host resolves to one global address and 127.0.0.1
  no-resolve      1  UNREACHABLE  host does not resolve
  redirect-loop   1  UNREACHABLE  a stable host redirects to a host that resolves to 127.0.0.1

The predicate (frozen, round-30 claims.md): C2 holds iff this command prints
QUOTE_REOPEN_FETCH_BOUND_MATCH=20/20 against tools/quote-reopen.py on the measured revision.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import random
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, HERE)
import qr_harness as H  # noqa: E402

FROZEN_TOTAL = 20
LABEL = "QUOTE_REOPEN_FETCH_BOUND_MATCH"
DEADLINE = 3.0
BOUND = DEADLINE + 2.0
CAP = 15.0
CONS = "bcdfghjklmnprstvz"
VOWS = "aeiou"


def sha256(path):
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def words(rng, n):
    return ["".join(rng.choice(CONS) + rng.choice(VOWS) for _ in range(rng.randint(2, 4))) for _ in range(n)]


PLAN = (["drip-head"] * 2 + ["drip-body"] * 2 + ["drip-chunked"] * 2 + ["stall-body"]
        + ["rebind-loop"] * 3 + ["rebind-private", "rebind-redirect"] + ["stable-present"] * 2
        + ["stable-absent", "slow-ok", "multi-address", "mixed-address", "no-resolve", "redirect-loop"])
LABELS = {"drip-head": "UNREACHABLE", "drip-body": "UNREACHABLE", "drip-chunked": "UNREACHABLE",
          "stall-body": "UNREACHABLE", "rebind-loop": "VERBATIM", "rebind-private": "VERBATIM",
          "rebind-redirect": "VERBATIM", "stable-present": "VERBATIM", "stable-absent": "ABSENT",
          "slow-ok": "VERBATIM", "multi-address": "VERBATIM", "mixed-address": "UNREACHABLE",
          "no-resolve": "UNREACHABLE", "redirect-loop": "UNREACHABLE"}


def build(rng, srv):
    """Return a list of item specs: dict(kind, label, id, sid, url, quote, resolve, routed)."""
    out = []
    gpool = H.global_addrs(rng, 3 * len(PLAN) + 4)
    for k, kind in enumerate(PLAN):
        tok = "%016x" % rng.getrandbits(64)
        host = "q%08x.test" % rng.getrandbits(32)
        g1, g2, g3 = gpool[3 * k], gpool[3 * k + 1], gpool[3 * k + 2]
        text = words(rng, 40)
        quote = " ".join(text[5:5 + rng.randint(6, 12)])
        doc = ("<!doctype html><html><head><title>t</title></head><body><p>%s</p></body></html>"
               % " ".join(text)).encode("utf-8")
        resolve = {host: [[g1]]}
        routed = [g1]
        path = "/x/" + tok
        if kind.startswith("drip-"):
            srv.behave(path, kind)
        elif kind == "stall-body":
            srv.behave(path, "stall")
        elif kind == "slow-ok":
            srv.add(path, doc, behavior="slow-ok")
        else:
            srv.add(path, doc)
        if kind == "stable-absent":
            other = words(rng, 8)
            quote = " ".join(other)
        if kind == "rebind-loop":
            resolve = {host: [[g1], ["127.0.0.1"]]}
        elif kind == "rebind-private":
            resolve = {host: [[g1], ["10.%d.%d.%d" % (rng.randint(0, 255), rng.randint(0, 255),
                                                      rng.randint(1, 254))]]}
        elif kind == "multi-address":
            resolve = {host: [[g1, g2]]}
            routed = [g1, g2]
        elif kind == "mixed-address":
            resolve = {host: [[g1, "127.0.0.1"]]}
        elif kind == "no-resolve":
            resolve = {}
        elif kind in ("rebind-redirect", "redirect-loop"):
            host2 = "q%08x.test" % rng.getrandbits(32)
            path2 = "/x/%016x" % rng.getrandbits(64)
            srv.add(path2, doc)
            srv.add(path, b"moved", status=302, ctype="text/plain",
                    extra=[("Location", "http://%s%s" % (host2, path2))])
            if kind == "rebind-redirect":
                resolve = {host: [[g1]], host2: [[g2], ["127.0.0.1"]]}
                routed = [g1, g2]
            else:
                resolve = {host: [[g1]], host2: [["127.0.0.1"]]}
        sid = "S%d" % rng.randint(100, 999)
        out.append({"kind": kind, "label": LABELS[kind], "id": "%016x" % rng.getrandbits(64), "sid": sid,
                    "url": "http://%s%s" % (host, path), "quote": quote, "resolve": resolve,
                    "routed": routed})
    return out


def score(spec, res):
    got = res["verdicts"].get(spec["id"])
    connects = [e for e in res["net"] if e.get("ev") == "connect"]
    bad = [e["dest"] for e in connects if e.get("dest") not in spec["routed"]]
    a = got == spec["label"]
    b = res["wall"] <= BOUND and not res["killed"]
    c = not bad
    return a and b and c, {"kind": spec["kind"], "label": spec["label"], "got": got,
                           "wall_s": round(res["wall"], 3), "killed": res["killed"],
                           "verdict_ok": a, "bound_ok": b, "validated_only": c,
                           "unvalidated_dests": sorted(set(bad)), "rc": res["rc"]}


def main(argv):
    ap = argparse.ArgumentParser(prog="c2-count.py")
    ap.add_argument("--tool", default=os.path.join(LANE, "tools", "quote-reopen.py"))
    ap.add_argument("--receipt", default=None)
    args = ap.parse_args(argv)
    seed = int.from_bytes(os.urandom(8), "big")
    rng = random.Random(seed)
    srv = H.Server()
    work = tempfile.mkdtemp(prefix="chousa-r30-c2-")
    try:
        specs = build(rng, srv)
        rng.shuffle(specs)

        def one(i_spec):
            i, s = i_spec
            return s, H.run_tool(args.tool, os.path.join(work, "i%02d" % i),
                                 [(s["id"], s["sid"], s["quote"])], [(s["sid"], s["url"])],
                                 s["resolve"], s["routed"], srv.port, deadline=DEADLINE, cap=CAP)

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(specs)) as ex:
            results = list(ex.map(one, enumerate(specs)))
    finally:
        srv.close()
    n_ok = 0
    rows = []
    by_kind = {}
    for s, res in results:
        ok, row = score(s, res)
        n_ok += ok
        row["match"] = ok
        rows.append(row)
        c = by_kind.setdefault(s["kind"], [0, 0])
        c[0] += ok
        c[1] += 1
    t = len(results)
    holds = (n_ok == t == FROZEN_TOTAL)
    print("%s=%d/%d" % (LABEL, n_ok, t))
    receipt = {
        "label": LABEL, "n": n_ok, "t": t, "frozen_total": FROZEN_TOTAL, "predicate_holds": holds,
        "seed": seed, "deadline_s": DEADLINE, "bound_s": BOUND, "cap_s": CAP,
        "counter_sha256": sha256(os.path.abspath(__file__)),
        "harness_sha256": sha256(os.path.join(HERE, "qr_harness.py")),
        "tool": os.path.relpath(os.path.abspath(args.tool), LANE), "tool_sha256": sha256(args.tool),
        "by_kind": by_kind, "items": sorted(rows, key=lambda r: r["kind"]),
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "argv": ["python3", "corpus/evidence/round30/c2-count.py"] + argv,
    }
    if args.receipt:
        with open(args.receipt, "w", encoding="utf-8") as f:
            json.dump(receipt, f, indent=1, sort_keys=True)
            f.write("\n")
    shutil.rmtree(work, ignore_errors=True)
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
