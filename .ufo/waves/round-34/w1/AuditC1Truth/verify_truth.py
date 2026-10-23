#!/usr/bin/env python3
"""Independent truth audit for round-34 C1 fixtures.

Written from scratch: does NOT import or reuse c1-count.py code. It re-implements
the boundary rules of tools/research-gate.sh (tok_left_ok / tok_right_ok /
tok_word_char with TOK_WS / TOK_PUNCT, byte semantics under the gate's LC_ALL=C)
and the round-31 line binding rule, then derives the truth of every record from
the fixture bytes and compares with the counter's truth.json.

Checks performed
  1. every claims.jsonl line is one well-formed JSON object;
  2. its top-level keys are exactly the keys the gate reads
     (id, source, span, expect, marker, line, sha256);
  3. the record is valid under the gate's own record rules
     (id/source/span/expect present, expect in the legal set, no marker with
     expect!=contradicted, "line" well formed and M>N);
  4. the span byte length sits in the docstring band of its class, and every
     long-class span is >= 32768 bytes;
  5. the derived truth (supported / unsupported / mislocated) equals the
     counter's truth.json entry -- a difference is a counter defect.

Usage: verify_truth.py <keep-dir> [<keep-dir> ...]
Exit 0 iff no disagreement and no structural problem.
"""
import json
import os
import re
import sys

# --- gate boundary classes, transcribed from research-gate.sh:1513-1514 ------
TOK_WS = frozenset(b" \t\n\r\v\f")
TOK_PUNCT = frozenset(b"!\"#$%&()*+,./:;<=>?@[\\]^_`{|}~")
ALNUM = frozenset(b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")

# --- gate record rules (research-gate.sh:1699-1772) -------------------------
GATE_READ_KEYS = {"id", "source", "span", "expect", "marker", "line", "sha256"}
LEGAL_EXPECT = {"supported", "contradicted", "unsupported"}
LINE_RE = re.compile(r"^([1-9][0-9]*)(?:-([1-9][0-9]*))?$")

# --- docstring bands (claims.md / c1-count.py docstring) --------------------
BANDS = {
    "long-verbatim-ml": (33000, 65000),
    "long-verbatim-1l": (33000, 65000),
    "long-edge": (32768, 32900),
    "long-mut-head": (34000, 65000),
    "long-mut-tail": (34000, 65000),
    "long-mut-mid": (34000, 65000),
    "long-split": (33000, 65000),
    "long-glued-left": (33000, 65000),
    "long-glued-right": (33000, 65000),
    "long-line-bound": (33000, 65000),
    "long-line-wrong": (33000, 65000),
    "short-verbatim": (64, 4096),
    "short-mut": (64, 4096),
}
COUNTS = {
    "long-verbatim-ml": 3, "long-verbatim-1l": 2, "long-edge": 2,
    "long-mut-head": 2, "long-mut-tail": 2, "long-mut-mid": 3,
    "long-split": 2, "long-glued-left": 2, "long-glued-right": 2,
    "long-line-bound": 2, "long-line-wrong": 2,
    "short-verbatim": 3, "short-mut": 3,
}
LONG_MIN = 32768


def tok_word_char(c):
    """Mirror of tok_word_char (gate:1516-1523). c is one byte or b''."""
    if not c:
        return False
    if c[0] in ALNUM:
        return True
    if c == b"-" or c == b"'":
        return False
    if c[0] in TOK_WS or c[0] in TOK_PUNCT:
        return False
    return True  # every non-ASCII byte is a word character


def tok_left_ok(before, span):
    """Mirror of tok_left_ok (gate:1525-1537)."""
    if not before:
        return True
    c = before[-1:]
    if c == b"-" or c == b"'":
        n = before[-2:-1] if len(before) >= 2 else b""
        if tok_word_char(n) and tok_word_char(span[0:1]):
            return False
        return True
    return c[0] in TOK_WS or c[0] in TOK_PUNCT


def tok_right_ok(after, span):
    """Mirror of tok_right_ok (gate:1539-1551)."""
    if not after:
        return True
    c = after[0:1]
    if c == b"-" or c == b"'":
        n = after[1:2] if len(after) >= 2 else b""
        if tok_word_char(n) and tok_word_char(span[-1:]):
            return False
        return True
    return c[0] in TOK_WS or c[0] in TOK_PUNCT


def all_occurrences(hay, span):
    """Every offset where span occurs in hay (overlapping included)."""
    out, start = [], 0
    if not span:
        return out
    while True:
        i = hay.find(span, start)
        if i < 0:
            return out
        out.append(i)
        start = i + 1


def greedy_occurrences(hay, span):
    """Non-overlapping leftmost occurrences -- the shape `grep -o` reports."""
    out, start = [], 0
    if not span:
        return out
    while True:
        i = hay.find(span, start)
        if i < 0:
            return out
        out.append(i)
        start = i + len(span)


def occurrence_lines(hay, span, offsets):
    """(l1, l2) per offset, exactly as the gate counts them."""
    res = []
    for off in offsets:
        before = hay[:off]
        l1 = before.count(b"\n") + 1
        l2 = l1 + span.count(b"\n")
        res.append((l1, l2))
    return res


def delimited(hay, span, offsets):
    out = []
    for off in offsets:
        before, after = hay[:off], hay[off + len(span):]
        if tok_left_ok(before, span) and tok_right_ok(after, span):
            out.append(off)
    return out


def derive_truth(rec, hay, span):
    """-> (truth, detail) following the gate's verify_claims flow (gate:1802-1890)."""
    offs = all_occurrences(hay, span)
    d_off = delimited(hay, span, offs)
    lines = occurrence_lines(hay, span, d_off)
    detail = {"n_occ_raw": len(offs), "n_occ_delimited": len(d_off), "lines": lines}
    if "line" not in rec:
        # tok_span_at succeeds iff a delimited occurrence exists
        return ("supported" if d_off else "unsupported"), detail
    m = LINE_RE.match(rec["line"])
    if not m:
        detail["bad_line"] = rec["line"]
        return "INVALID", detail
    n = m.group(1)
    mm = m.group(2) or m.group(1)
    bound = any(str(l1) == n and str(l2) == mm for l1, l2 in lines)
    detail["bound"] = bound
    if bound:
        return "supported", detail
    if d_off:
        # tok_span_at succeeded, no occurrence binds -> observed=mislocated
        return "mislocated", detail
    # no delimited occurrence at all -> the gate takes the unsupported branch
    return "unsupported", detail


def check_record(rec, truth, hay, problems, notes):
    cid = rec.get("id")
    cls, t = truth
    span = rec["span"].encode("utf-8")
    n = len(span)

    # (4) span length bands
    lo, hi = BANDS[cls]
    if not (lo <= n <= hi):
        notes.append("id=%s class=%s span bytes %d OUTSIDE docstring band %d..%d" % (cid, cls, n, lo, hi))
    if cls.startswith("long") and n < LONG_MIN:
        problems.append("id=%s class=%s long span %d < %d" % (cid, cls, n, LONG_MIN))

    # (3) record validity under the gate's own rules
    if not rec.get("id"):
        problems.append("id=%s missing id" % cid)
    if not rec.get("source"):
        problems.append("id=%s missing source" % cid)
    if not rec.get("span"):
        problems.append("id=%s missing/empty span" % cid)
    if rec.get("expect") not in LEGAL_EXPECT:
        problems.append("id=%s expect=%r invalid" % (cid, rec.get("expect")))
    if rec.get("marker") and rec.get("expect") != "contradicted":
        problems.append("id=%s marker present but expect=%s" % (cid, rec.get("expect")))
    if "line" in rec:
        m = LINE_RE.match(rec["line"])
        if not m:
            problems.append("id=%s line value malformed: %r" % (cid, rec["line"]))
        else:
            n_l = int(m.group(1))
            m_l = int(m.group(2) or m.group(1))
            if m_l <= n_l:
                problems.append("id=%s line range M<=N (%d-%d)" % (cid, n_l, m_l))

    # (5) truth derivation
    derived, detail = derive_truth(rec, hay, span)
    if derived != t:
        problems.append("TRUTH DISAGREEMENT id=%s class=%s counter=%s derived=%s detail=%s"
                        % (cid, cls, t, derived, detail))
    # enumeration parity: overlapping vs grep-style non-overlapping
    g = greedy_occurrences(hay, span)
    if len(g) != len(all_occurrences(hay, span)):
        notes.append("id=%s class=%s overlapping occurrences: all=%d greedy=%d (grep -o sees the greedy set)"
                     % (cid, cls, len(all_occurrences(hay, span)), len(g)))
    return derived == t


def audit(keep):
    rep = {"keep": keep, "problems": [], "notes": [], "classes": {}, "records": 0,
           "lengths": {}}
    with open(os.path.join(keep, "truth.json")) as f:
        truth = json.load(f)
    with open(os.path.join(keep, "claims.jsonl"), "rb") as f:
        raw = f.read().decode("utf-8")
    lines = raw.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    rows = []
    for i, ln in enumerate(lines, 1):
        try:
            obj = json.loads(ln)
        except Exception as e:
            rep["problems"].append("claims.jsonl:%d invalid JSON: %r" % (i, e))
            continue
        if not isinstance(obj, dict):
            rep["problems"].append("claims.jsonl:%d not a JSON object" % i)
            continue
        keys = set(obj)
        extra = keys - GATE_READ_KEYS
        missing = {"id", "source", "span", "expect"} - keys
        if extra:
            rep["problems"].append("claims.jsonl:%d keys the gate never reads: %s" % (i, sorted(extra)))
        if missing:
            rep["problems"].append("claims.jsonl:%d missing keys: %s" % (i, sorted(missing)))
        rows.append((i, obj))
    rep["records"] = len(rows)
    if len(rows) != 30:
        rep["problems"].append("record count %d != 30" % len(rows))
    ids = [o["id"] for _, o in rows if "id" in o]
    if len(set(ids)) != len(ids):
        rep["problems"].append("duplicate ids in claims.jsonl")
    if set(ids) != set(truth):
        rep["problems"].append("id set differs from truth.json keys")
    for cid in truth:
        if not (len(cid) == 11 and cid.startswith("c") and all(ch in "0123456789abcdef" for ch in cid)):
            rep["problems"].append("unexpected id shape %r" % cid)

    for i, rec in rows:
        cid = rec.get("id")
        if cid not in truth:
            continue
        cls, t = truth[cid]
        rep["classes"].setdefault(cls, [0, 0])[1] += 1
        srcp = os.path.join(keep, rec["source"])
        if not os.path.isfile(srcp):
            rep["problems"].append("id=%s source %s missing" % (cid, rec["source"]))
            continue
        hay = open(srcp, "rb").read()
        if not hay:
            rep["problems"].append("id=%s empty source" % cid)
        span_b = rec["span"].encode("utf-8")
        rep["lengths"].setdefault(cls, []).append(len(span_b))
        if check_record(rec, truth[cid], hay, rep["problems"], rep["notes"]):
            rep["classes"][cls][0] += 1
    for cls, cnt in COUNTS.items():
        got = rep["classes"].get(cls, [0, 0])
        if got[1] != cnt:
            rep["problems"].append("class %s count %d != docstring %d" % (cls, got[1], cnt))
    return rep


def main():
    dirs = sys.argv[1:]
    if not dirs:
        print("usage: verify_truth.py <keep-dir> [...]")
        return 2
    total = 0
    for d in dirs:
        rep = audit(d)
        total += len(rep["problems"])
        print("== %s  (records=%d)" % (d, rep["records"]))
        for cls in sorted(rep["classes"]):
            ok, n = rep["classes"][cls]
            lens = rep["lengths"].get(cls, [])
            band = BANDS[cls]
            print("  %-18s %d/%d  bytes %d..%d (band %d..%d)" % (cls, ok, n, min(lens), max(lens), band[0], band[1]))
        for p in rep["problems"]:
            print("  PROBLEM: %s" % p)
        for nt in rep["notes"]:
            print("  NOTE: %s" % nt)
        if not rep["problems"] and not rep["notes"]:
            print("  clean: no disagreements, no structural problems, no band notes")
    print("TOTAL PROBLEMS: %d" % total)
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
