#!/usr/bin/env python3
"""C2 feasibility oracle: an exact-search re-implementation of the landed gate's
`verify-claims` span matcher.

Scope: read-only analysis artifact. It never writes to the lane.

Boundary rules are transcribed from the LANDED gate (blob sha256
a6307edf687ac0fb..., tools/research-gate.sh):
  - tok_left_ok  (tools/research-gate.sh:1538-1550)
  - tok_right_ok (tools/research-gate.sh:1552-1564)
  - tok_word_char (tools/research-gate.sh:1524-1533)
  - TOK_WS / TOK_PUNCT (tools/research-gate.sh:1518-1519)

Matching: exact byte search (LC_ALL=C byte semantics), EVERY occurrence
(including overlapping ones), each occurrence tested for the two token
boundaries.  This is the semantic ceiling the bash gate is compared against.

Output protocol (what corpus/evidence/round34/c2-count.py parses):
  CLAIM id=<id> expected=<expect> observed=<obs> source=<src> at=<at> verdict=<v>
  FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=<id> ...
  VERDICT_BEARING_CLAIMS=N/M
  RESEARCH_GATE: DRIFT| CLEAN ...
exit 1 when any record mismatches (the fixture always drifts), else 0.
"""
import json
import os
import sys

TOK_WS = b" \t\n\r\v\f"
TOK_PUNCT = b'!"#$%&()*+,./:;<=>?@[\\]^_`{|}~'


def is_word(c):
    """tok_word_char: rc0 (word) for ASCII alnum and for any byte outside the
    two boundary sets; empty is not a word char."""
    if c is None:
        return False
    if 0x30 <= c <= 0x39 or 0x41 <= c <= 0x5A or 0x61 <= c <= 0x7A:
        return True
    if c == 0x2D or c == 0x27:      # '-' and "'" are joiners, not word chars
        return False
    if c in TOK_WS or c in TOK_PUNCT:
        return False
    return True                     # every non-ASCII byte is a word character


def left_ok(hay, off, span):
    """tok_left_ok(before, span)"""
    if off == 0:
        return True                 # start of file
    c = hay[off - 1]
    if c == 0x2D or c == 0x27:
        n = hay[off - 2] if off >= 2 else None
        if is_word(n) and span and is_word(span[0]):
            return False            # word-internal joiner
        return True
    return c in TOK_WS or c in TOK_PUNCT


def right_ok(hay, off, span):
    """tok_right_ok(after, span)"""
    end = off + len(span)
    if end >= len(hay):
        return True                 # end of file
    c = hay[end]
    if c == 0x2D or c == 0x27:
        n = hay[end + 1] if end + 1 < len(hay) else None
        if is_word(n) and is_word(span[-1]):
            return False
        return True
    return c in TOK_WS or c in TOK_PUNCT


def all_offsets(hay, span):
    """Every byte offset at which span occurs in hay (overlapping included)."""
    out, i = [], hay.find(span)
    while i != -1:
        out.append(i)
        i = hay.find(span, i + 1)
    return out


def main(argv):
    if len(argv) < 3 or argv[1] != "verify-claims":
        sys.stderr.write("oracle: usage: oracle.py verify-claims CLAIMS --root ROOT\n")
        return 2
    claims_path = argv[2]
    root = os.path.abspath(os.getcwd())
    i = 3
    while i < len(argv):
        if argv[i] == "--root" and i + 1 < len(argv):
            root = os.path.abspath(argv[i + 1])
            i += 2
        else:
            i += 1
    if not os.path.isfile(claims_path):
        sys.stderr.write("oracle: claims file not found: %s\n" % claims_path)
        return 2

    n_claims = n_match = n_mismatch = n_unsupported = n_supported = 0
    n_mislocated = n_invalid = n_refused = 0
    out_lines, finding_lines = [], []
    with open(claims_path, "r", encoding="utf-8", errors="replace") as fh:
        raw_lines = fh.read().splitlines()
    for lineno, raw in enumerate(raw_lines, 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        try:
            rec = json.loads(raw)
        except Exception:
            n_claims += 1
            n_invalid += 1
            out_lines.append("CLAIM id=line%d expected=- observed=invalid source=- at=- verdict=invalid" % lineno)
            continue
        if not isinstance(rec, dict):
            n_claims += 1
            n_invalid += 1
            out_lines.append("CLAIM id=line%d expected=- observed=invalid source=- at=- verdict=invalid" % lineno)
            continue
        cid = rec.get("id")
        src = rec.get("source")
        span_s = rec.get("span")
        expect = rec.get("expect")
        if not isinstance(cid, str) or not isinstance(src, str) or \
                not isinstance(span_s, str) or not isinstance(expect, str):
            n_claims += 1
            n_invalid += 1
            out_lines.append("CLAIM id=line%d expected=- observed=invalid source=- at=- verdict=invalid" % lineno)
            continue
        line_f = rec.get("line")
        line_n = line_m = None
        if line_f is not None:
            if not isinstance(line_f, str) or not line_f or \
                    not all(p.isdigit() and (p == "0" or p[0] != "0") and len(p) > 0 for p in line_f.split("-")) or \
                    line_f.count("-") > 1:
                n_claims += 1
                n_invalid += 1
                out_lines.append("CLAIM id=%s expected=%s observed=invalid source=%s at=- verdict=invalid"
                                 % (cid, expect, src))
                continue
            parts = line_f.split("-")
            line_n = int(parts[0])
            line_m = int(parts[1]) if len(parts) == 2 else line_n
            if line_m < line_n:
                n_claims += 1
                n_invalid += 1
                out_lines.append("CLAIM id=%s expected=%s observed=invalid source=%s at=- verdict=invalid"
                                 % (cid, expect, src))
                continue
        p = src if os.path.isabs(src) else os.path.join(root, src)
        p = os.path.abspath(p)
        if not (p == root or p.startswith(root + os.sep)) or not os.path.isfile(p):
            n_claims += 1
            n_refused += 1
            out_lines.append("CLAIM id=%s expected=%s observed=refused source=%s at=- verdict=refused"
                             % (cid, expect, src))
            continue
        with open(p, "rb") as fh:
            hay = fh.read()
        span = span_s.encode("utf-8", "surrogateescape")
        n_claims += 1
        offsets = all_offsets(hay, span) if span else []
        delimited = []
        for off in offsets:
            if left_ok(hay, off, span) and right_ok(hay, off, span):
                l1 = hay.count(b"\n", 0, off) + 1
                l2 = l1 + span.count(b"\n")
                delimited.append((off, l1, l2))
        at = "-"
        if delimited:
            _, l1, l2 = delimited[0]
            at = ("line:%d" % l1) if l1 == l2 else ("lines:%d-%d" % (l1, l2))
        if delimited and line_n is None:
            observed = "supported"
        elif delimited and line_n is not None:
            hit = next((d for d in delimited if d[1] == line_n and d[2] == line_m), None)
            if hit is not None:
                _, l1, l2 = hit
                observed = "supported"
                at = ("line:%d" % l1) if l1 == l2 else ("lines:%d-%d" % (l1, l2))
            else:
                observed = "mislocated"
                finding_lines.append("FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims "
                                     "obs=id=%s line=%d-%d first_delimited_occurrence=%s"
                                     % (cid, line_n, line_m, at))
        elif delimited and line_n is not None:
            observed = "mislocated"
        else:
            observed = "unsupported"
        if observed == "supported":
            n_supported += 1
        elif observed == "unsupported":
            n_unsupported += 1
        elif observed == "mislocated":
            n_mislocated += 1
        verdict = "match" if observed == expect else "mismatch"
        if verdict == "match":
            n_match += 1
        else:
            n_mismatch += 1
            if expect == "unsupported" and observed == "supported":
                finding_lines.append("FINDING CLAIM_SPAN_UNEXPECTED severity=warn surface=claims obs=id=%s at=%s"
                                     % (cid, at))
        out_lines.append("CLAIM id=%s expected=%s observed=%s source=%s at=%s verdict=%s"
                         % (cid, expect, observed, src, at, verdict))

    print("research-gate oracle — mode=claims — claims=%s" % claims_path)
    for l in out_lines:
        print(l)
    for l in finding_lines:
        print(l)
    print("VERDICT_BEARING_CLAIMS=%d/%d" % (n_match, n_claims))
    roll = "CLEAN" if n_match == n_claims else "DRIFT"
    print("RESEARCH_GATE: %s (claims=%d supported=%d unsupported=%d mismatched=%d mislocated=%d "
          "refused=%d invalid=%d findings=%d drift=%d)"
          % (roll, n_claims, n_supported, n_unsupported, n_mismatch, n_mislocated,
             n_refused, n_invalid, len(finding_lines), 0 if roll == "CLEAN" else n_mismatch))
    return 0 if roll == "CLEAN" else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
