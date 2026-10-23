#!/usr/bin/env python3
"""Round-30 C2 counter (design v3): the fetch bounds that tools/quote-reopen.py states hold
under slow senders and DNS rebinding.

Usage (lane root):
    python3 corpus/evidence/round30/c2-count.py [--tool tools/quote-reopen.py] [--receipt OUT.json]

Prints one line `QUOTE_REOPEN_FETCH_BOUND_MATCH=<n>/<t>` and exits 0 iff n == t == FROZEN_TOTAL.
Exit 1 is a miss. Exit 2 is a failed measurement (harness error), never a pass.

Each item is one separate run of the candidate (one registry URL) inside the loopback harness
(qr_harness.py). Nothing reaches the network: names resolve only from the run's map and every
connection lands on the harness server or is refused. Paths, words, ids, host names, global
addresses, labels, framing, header shapes and each item's DEADLINE are drawn from a fresh
64-bit os.urandom seed on every run; there is no seed option.

Each item gets its own DEADLINE, uniform in [2.0, 6.0] s, written into the candidate's module
constant `DEADLINE`. Every response, slow or not, has the same head shape: status line,
Content-Type, one header with a random name and a value of random length (20-300 bytes), then
Content-Length or chunked framing (random per item), Connection: close. Every page body is an
ordinary HTML document of about 2-3 KB (drip-steady: about 3 MB).

An item MATCHES iff all three hold:
  (a) the item's verdict equals its label;
  (b) the run's wall time is at most BOUND = DEADLINE + 1.5 s (a run is killed at 20 s);
  (c) every logged connect destination is a routed global address of that item (no
      connection to loopback, private or any other address).

FROZEN_TOTAL = 27 items:
  label UNREACHABLE (11):
    drip-head 2       the whole response, head first, one byte per 0.2 s
    drip-body 3       head and 200 body bytes at once, then one byte per 0.2 s
    drip-steady 2     about 3 MB at 4096 bytes per 0.25 s (about 190 s in total)
    stall-body 1      head and 200 body bytes, then silence
    mixed-address 1   host resolves to one global address and 127.0.0.1
    no-resolve 1      host does not resolve
    redirect-loop 1   a stable host redirects to a host that resolves to 127.0.0.1
  label VERBATIM or ABSENT, a fair coin per item (16):
    rebind-loop 4     first lookup global, later lookups 127.0.0.1
    rebind-private 2  first lookup global, later lookups 10.x.y.z
    rebind-redirect 2 a stable host redirects to a host that rebinds to 127.0.0.1
    stable 4          ordinary page
    slow-ok 2         body in 6 pieces spread over DEADLINE - 0.8 s, inside the deadline
    multi-address 2   host resolves to two global addresses

The predicate (frozen, round-30 claims.md): C2 holds iff this command prints
QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27 against tools/quote-reopen.py on the measured revision.
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

FROZEN_TOTAL = 27
LABEL = "QUOTE_REOPEN_FETCH_BOUND_MATCH"
DEADLINE_RANGE = (2.0, 6.0)
SLACK = 1.5
CAP = 20.0
CONS = "bcdfghjklmnprstvz"
VOWS = "aeiou"

PLAN = (["drip-head"] * 2 + ["drip-body"] * 3 + ["drip-steady"] * 2 + ["stall-body", "mixed-address",
        "no-resolve", "redirect-loop"]
        + ["rebind-loop"] * 4 + ["rebind-private"] * 2 + ["rebind-redirect"] * 2 + ["stable"] * 4
        + ["slow-ok"] * 2 + ["multi-address"] * 2)
FIXED_UNREACHABLE = {"drip-head", "drip-body", "drip-steady", "stall-body", "mixed-address", "no-resolve",
                     "redirect-loop"}
BEHAVIOR = {"drip-head": "drip-head", "drip-body": "drip-body", "drip-steady": "drip-steady",
            "stall-body": "stall", "slow-ok": "slow-ok"}


def sha256(path):
    if not os.path.isfile(path):
        return None
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def words(rng, n):
    return ["".join(rng.choice(CONS) + rng.choice(VOWS) for _ in range(rng.randint(2, 4))) for _ in range(n)]


def page(rng, text, big=False):
    paras = [" ".join(text[i:i + 40]) for i in range(0, len(text), 40)]
    body = "".join("<p>%s</p>\n" % p for p in paras)
    if big:
        filler = " ".join(words(rng, 400))
        body += ("<p>%s</p>\n" % filler) * 900
    return ("<!doctype html><html><head><meta charset=\"utf-8\"><title>%s</title></head><body>\n%s</body></html>\n"
            % (" ".join(words(rng, 5)), body)).encode("utf-8")


def head_extra(rng):
    name = "X-" + "".join(rng.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(rng.randint(3, 10))).title()
    value = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(rng.randint(20, 300)))
    return [(name, value)]


def build(rng, srv):
    """Return item specs: dict(kind, label, id, sid, url, quote, resolve, routed, deadline, bound)."""
    out = []
    gpool = H.global_addrs(rng, 3 * len(PLAN) + 4)
    sids = rng.sample(range(100, 1000), len(PLAN))
    for k, kind in enumerate(PLAN):
        host = "q%08x.test" % rng.getrandbits(32)
        path = "/x/%016x" % rng.getrandbits(64)
        g1, g2 = gpool[3 * k], gpool[3 * k + 1]
        deadline = round(rng.uniform(*DEADLINE_RANGE), 2)
        text = words(rng, rng.randint(300, 420))
        present = rng.random() < 0.5
        if kind in FIXED_UNREACHABLE:
            label = "UNREACHABLE"
            present = rng.random() < 0.5
        else:
            label = "VERBATIM" if present else "ABSENT"
        s = rng.randint(5, len(text) - 20)
        quote = " ".join(text[s:s + rng.randint(6, 12)]) if present else " ".join(words(rng, rng.randint(6, 12)))
        doc = page(rng, text, big=(kind == "drip-steady"))
        framing = rng.choice(["cl", "chunked"])
        srv.add(path, doc, extra=head_extra(rng), behavior=BEHAVIOR.get(kind), framing=framing,
                param=(deadline - 0.8) if kind == "slow-ok" else None)
        resolve = {host: [[g1]]}
        routed = [g1]
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
            srv.add(path2, doc, extra=head_extra(rng), framing=rng.choice(["cl", "chunked"]))
            srv.add(path, b"moved", status=302, ctype="text/plain",
                    extra=head_extra(rng) + [("Location", "http://%s%s" % (host2, path2))])
            if kind == "rebind-redirect":
                resolve = {host: [[g1]], host2: [[g2], ["127.0.0.1"]]}
                routed = [g1, g2]
            else:
                resolve = {host: [[g1]], host2: [["127.0.0.1"]]}
        out.append({"kind": kind, "label": label, "id": "%016x" % rng.getrandbits(64), "sid": "S%d" % sids[k],
                    "url": "http://%s%s" % (host, path), "quote": quote, "resolve": resolve,
                    "routed": routed, "deadline": deadline, "bound": round(deadline + SLACK, 2)})
    return out


def score(spec, res):
    got = res["verdicts"].get(spec["id"])
    connects = [e for e in res["net"] if e.get("ev") == "connect"]
    bad = [e["dest"] for e in connects if e.get("dest") not in spec["routed"]]
    a = got == spec["label"]
    b = res["wall"] <= spec["bound"] and not res["killed"]
    c = not bad
    return a and b and c, {"kind": spec["kind"], "label": spec["label"], "got": got,
                           "deadline_s": spec["deadline"], "bound_s": spec["bound"],
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
                                 s["resolve"], s["routed"], srv.port, deadline=s["deadline"], cap=CAP)

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
        "seed": seed, "deadline_range_s": list(DEADLINE_RANGE), "slack_s": SLACK, "cap_s": CAP,
        "design": "v3",
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
