#!/usr/bin/env python3
"""Class-semantics audit of the round-34 C1 fixture.

Independent of the counter's code: it re-derives, from the fixture BYTES alone,
the property each record's class claims, and checks the claim against the
class description in the counter docstring (claims.md / c1-count.py).

  long-verbatim-ml   multi-line span (contains a newline)
  long-verbatim-1l   single-line span (no newline)
  long-edge          span of 32768..32900 bytes
  long-mut-head      one letter changed within the first 64 bytes
  long-mut-tail      one letter changed within the last 64 bytes
  long-mut-mid       one letter changed at offset 8192..len-8192
  long-split         both halves in the source, never adjacent
  long-glued-left    the only occurrence is preceded by a word character
  long-glued-right   the only occurrence is followed by a word character
  long-line-bound    two delimited occurrences; "line" names the second
  long-line-wrong    two delimited occurrences; "line" names neither
  short-verbatim     64..4096 bytes, present verbatim
  short-mut          64..4096 bytes, one letter changed

The searches are anchored (probe chunks + alignment) and binary-searched, so a
65 KiB span costs milliseconds rather than minutes.

Usage: class_semantics.py <keep-dir> [<keep-dir> ...]
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verify_truth import (all_occurrences, delimited, occurrence_lines,  # noqa: E402
                          tok_left_ok, tok_right_ok, tok_word_char)

PROBE = 4096


def align_mutated(hay, m):
    """Find the occurrence of m-with-one-letter-changed in hay.

    Returns (hay_offset, diff_offset) or None. The alignment is found by
    probing intact chunks of m (the mutated byte is unknown), locating the
    probe in hay, and aligning the full span; the aligned copy must differ
    from m in exactly one byte.
    """
    n = len(m)
    starts = [0, 64, 1000, 8192, n - 8192, n - PROBE, n - 1000, n - 64]
    seen = set()
    for p in starts:
        if p < 0 or p + PROBE > n or p in seen:
            continue
        seen.add(p)
        probe = m[p:p + PROBE]
        start = 0
        while True:
            q = hay.find(probe, start)
            if q < 0:
                break
            start = q + 1
            off = q - p
            if off < 0 or off + n > len(hay):
                continue
            cand = hay[off:off + n]
            diffs = [i for i in range(n) if cand[i] != m[i]]
            if len(diffs) == 1:
                return off, diffs[0]
    return None


def near_misses_small(hay, m):
    """Every one-letter mutation of m that occurs in hay (small m only)."""
    out = []
    n = len(m)
    for i in range(n):
        for c in range(ord("a"), ord("z") + 1):
            if chr(c) == m[i:i + 1]:
                continue
            cand = m[:i] + bytes([c]) + m[i + 1:]
            for off in all_occurrences(hay, cand):
                out.append((off, i))
    return out


def longest_prefix_in(hay, m):
    """Largest k with m[:k] occurring in hay (monotone -> binary search)."""
    n = len(m)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if hay.find(m[:mid]) >= 0:
            lo = mid
        else:
            hi = mid - 1
    return lo


def shortest_suffix_from(hay, m):
    """Smallest j with m[j:] occurring in hay (monotone -> binary search)."""
    n = len(m)
    lo, hi = 0, n
    while lo < hi:
        mid = (lo + hi) // 2
        if hay.find(m[mid:]) >= 0:
            hi = mid
        else:
            lo = mid + 1
    return lo


def split_pair(hay, m):
    """(k, off_p1, off_p2) for a split of m into two present, non-adjacent halves.

    The halves are m[:k] and m[k+1:] (the byte at k is dropped, as the counter's
    own split does). Presence of m[:k] is monotone decreasing in k and presence
    of m[k+1:] monotone increasing in k, so the feasible k range is bracketed
    by two binary searches and then scanned.
    """
    n = len(m)
    kmax = longest_prefix_in(hay, m)
    jmin = shortest_suffix_from(hay, m)
    lo = max(1, jmin - 1)
    hi = min(n - 1, kmax)
    best = None
    for k in range(lo, hi + 1):
        p1, p2 = m[:k], m[k + 1:]
        o1s = all_occurrences(hay, p1) if p1 else []
        o2s = all_occurrences(hay, p2) if p2 else []
        if not o1s or not o2s:
            continue
        for o1 in o1s:
            for o2 in o2s:
                if o1 + k < o2:            # the halves are not adjacent
                    best = (k, o1, o2)
                    break
            if best:
                break
        if best:
            break
    return best


def audit(keep):
    truth = json.load(open(os.path.join(keep, "truth.json")))
    rows = []
    with open(os.path.join(keep, "claims.jsonl"), "rb") as f:
        for ln in f.read().decode("utf-8").split("\n"):
            if ln.strip():
                rows.append(json.loads(ln))
    problems = []
    for rec in rows:
        cid = rec["id"]
        cls, t = truth[cid]
        hay = open(os.path.join(keep, rec["source"]), "rb").read()
        span = rec["span"].encode("utf-8")
        n = len(span)
        offs = all_occurrences(hay, span)
        d_off = delimited(hay, span, offs)
        lines = occurrence_lines(hay, span, d_off)
        p = "id=%s class=%s" % (cid, cls)

        if cls == "long-verbatim-ml":
            if b"\n" not in span:
                problems.append(p + " span has no newline (docstring: multi-line)")
            if not d_off:
                problems.append(p + " no delimited occurrence")
        elif cls == "long-verbatim-1l":
            if b"\n" in span:
                problems.append(p + " span contains a newline (docstring: single-line)")
            if not d_off:
                problems.append(p + " no delimited occurrence")
        elif cls == "long-edge":
            if not (32768 <= n <= 32900):
                problems.append(p + " span %d bytes outside 32768..32900" % n)
        elif cls in ("long-mut-head", "long-mut-tail", "long-mut-mid"):
            if offs:
                problems.append(p + " the mutated span occurs verbatim in the source")
                continue
            got = align_mutated(hay, span)
            if not got:
                problems.append(p + " no one-letter mutation of the span occurs in the source")
                continue
            moff, d = got
            if cls == "long-mut-head" and not (0 <= d <= 63):
                problems.append(p + " mutation at offset %d, docstring says <=63" % d)
            if cls == "long-mut-tail" and not (n - 64 <= d <= n - 1):
                problems.append(p + " mutation at offset %d, docstring says last 64 bytes" % d)
            if cls == "long-mut-mid" and not (8192 <= d <= n - 8192):
                problems.append(p + " mutation at offset %d, docstring says 8192..len-8192" % d)
            before, after = hay[:moff], hay[moff + n:]
            if not (tok_left_ok(before, span) and tok_right_ok(after, span)):
                problems.append(p + " the mutated occurrence is not delimited")
        elif cls == "long-split":
            if offs:
                problems.append(p + " the split span occurs verbatim")
                continue
            sp = split_pair(hay, span)
            if not sp:
                problems.append(p + " no two non-adjacent halves of the span are in the source")
            else:
                k, o1, o2 = sp
                if not (n // 4 <= k <= 3 * n // 4):
                    problems.append(p + " split point %d outside the docstring's middle half" % k)
        elif cls in ("long-glued-left", "long-glued-right"):
            if not offs:
                problems.append(p + " the span does not occur in the source at all")
                continue
            if len(offs) != 1:
                problems.append(p + " %d occurrences (docstring: only occurrence)" % len(offs))
                continue
            off = offs[0]
            before, after = hay[:off], hay[off + n:]
            if cls == "long-glued-left":
                if not (before and tok_word_char(before[-1:]) and tok_word_char(span[0:1])):
                    problems.append(p + " occurrence is not preceded by a word character")
                if tok_right_ok(after, span) is False:
                    problems.append(p + " occurrence right edge is not a boundary")
            else:
                if not (after and tok_word_char(after[0:1]) and tok_word_char(span[-1:])):
                    problems.append(p + " occurrence is not followed by a word character")
                if tok_left_ok(before, span) is False:
                    problems.append(p + " occurrence left edge is not a boundary")
            if d_off:
                problems.append(p + " the glued occurrence is delimited (would read supported)")
        elif cls in ("long-line-bound", "long-line-wrong"):
            if len(d_off) != 2:
                problems.append(p + " %d delimited occurrences (docstring: two)" % len(d_off))
                continue
            if "line" not in rec:
                problems.append(p + " no line field")
                continue
            lf = rec["line"]
            a, b = lf.split("-")
            named = (int(a), int(b))
            if cls == "long-line-bound":
                if named != lines[1]:
                    problems.append(p + " line %s does not name the second occurrence %s" % (lf, lines[1]))
            else:
                if named in lines:
                    problems.append(p + " line %s names an occurrence %s" % (lf, lines))
        elif cls == "short-verbatim":
            if not (64 <= n <= 4096):
                problems.append(p + " span %d bytes outside 64..4096" % n)
            if not d_off:
                problems.append(p + " no delimited occurrence")
        elif cls == "short-mut":
            if not (64 <= n <= 4096):
                problems.append(p + " span %d bytes outside 64..4096" % n)
            if offs:
                problems.append(p + " the mutated span occurs verbatim")
            if not near_misses_small(hay, span):
                problems.append(p + " no one-letter mutation of the span occurs in the source")
    return problems


def main():
    dirs = sys.argv[1:]
    if not dirs:
        print("usage: class_semantics.py <keep-dir> [...]")
        return 2
    total = 0
    for d in dirs:
        probs = audit(d)
        total += len(probs)
        print("== %s" % d)
        for p in probs:
            print("  CLASS-SEMANTICS PROBLEM: %s" % p)
        if not probs:
            print("  clean: every record's class property holds in the fixture bytes")
    print("TOTAL CLASS-SEMANTICS PROBLEMS: %d" % total)
    return 0 if total == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
