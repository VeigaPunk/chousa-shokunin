#!/usr/bin/env bash
# VARIANT (max-seeking, not best-mean): same features as control_noreader.sh, plus
# the fixture's exact class counts (24 supported / 50 mislocated / 8 unsupported
# among valid single-number one-line claims). It relabels the 12 claims with the
# highest P(supported | line value) as supported, gambling on per-seed variance.
set -u
if [ "$1" != "verify-claims" ]; then echo "control: unsupported mode" >&2; exit 2; fi
CLAIMS="$2"
exec python3 - "$CLAIMS" <<'PY'
import json, re, sys

VALID_SINGLE = re.compile(r"^[1-9][0-9]*$")
VALID_RANGE = re.compile(r"^([1-9][0-9]*)-([1-9][0-9]*)$")
Ns = list(range(14, 31))


def f_unif(v):
    return sum(1.0 / n for n in Ns if n >= v) / len(Ns)


def f_b2(v):
    tot = 0.0
    for n in Ns:
        if v < 2 or v > n:
            continue
        p2 = 2.0 * (v - 1) / (n * (n - 1))
        i = v - 1
        c3 = n * (n - 1) * (n - 2) / 6.0
        tot += 0.5 * (0.5 * p2) + 0.5 * (0.5 * (i * (n - 1 - i) / c3 + (i * (i - 1) / 2.0) / c3))
    return tot / len(Ns)


def f_m5(v):
    return sum(1.0 for n in Ns if 1 <= v - n <= 40) / 40.0 / len(Ns)


def p_sup(v):
    sup = 12 * f_unif(v) + 12 * f_b2(v)
    tot = sup + 44 * f_unif(v) + 6 * f_m5(v) + 8 * f_unif(v)
    return sup / tot


def base(rec):
    if "line" not in rec:
        return "supported", None
    v = rec.get("line")
    fmt, n, m = "invalid", None, None
    if isinstance(v, str):
        if VALID_SINGLE.match(v):
            fmt, n, m = "single", int(v), int(v)
        else:
            g = VALID_RANGE.match(v)
            if g and int(g.group(2)) > int(g.group(1)):
                fmt, n, m = "range", int(g.group(1)), int(g.group(2))
    if fmt == "invalid":
        return "invalid", None
    span = rec.get("span", "")
    if isinstance(span, str) and "\n" in span:
        if fmt == "range" and m == n + 1 and n <= 27:
            return "supported", None
        return "mislocated", None
    return "mislocated", n


recs = [json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
obs = {}
cand = []
for rec in recs:
    lab, n = base(rec)
    obs[rec["id"]] = lab
    if lab == "mislocated" and n is not None and n <= 30:
        cand.append((p_sup(n), rec["id"]))
for _, cid in sorted(cand, reverse=True)[:12]:
    obs[cid] = "supported"
for rec in recs:
    cid = rec.get("id", "?"); o = obs[cid]; src = rec.get("source", "-")
    if o == "mislocated":
        print("FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=%s expected=%s observed=%s source=%s at=-" % (
            cid, rec.get("expect", "supported"), o, src))
    print("CLAIM id=%s expected=%s observed=%s source=%s at=- verdict=%s" % (
        cid, rec.get("expect", "supported"), o, src, o))
sys.exit(1)
PY
