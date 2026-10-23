#!/usr/bin/env python3
"""Generate byte-level boundary cases + expected verdicts from the Python model.

Fields are hex-encoded so any byte value (including tab/newline and non-ASCII)
survives the TSV round-trip. The bash oracle decodes the same hex with
`xxd -r -p` under LC_ALL=C, so both sides operate on bytes exactly as the gate
does (the gate exports LC_ALL=C in tok_span_at/tok_span_all).
"""
import random
import sys

WS = b" \t\n\r\v\f"
PUNCT = b"!\"#$%&()*+,./:;<=>?@[\\]^_`{|}~"
ALNUM = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def tok_word_char(c):
    """c: one-byte bytes or b''."""
    if not c:
        return False
    if c in ALNUM:
        return True
    if c == b"-" or c == b"'":
        return False
    if c in WS or c in PUNCT:
        return False
    return True


def tok_left_ok(before, span):
    if not before:
        return True
    c = before[-1:]
    if c == b"-" or c == b"'":
        n = before[-2:-1] if len(before) >= 2 else b""
        if tok_word_char(n) and tok_word_char(span[0:1]):
            return False
        return True
    return c[0] in WS or c[0] in PUNCT


def tok_right_ok(after, span):
    if not after:
        return True
    c = after[0:1]
    if c == b"-" or c == b"'":
        n = after[1:2] if len(after) >= 2 else b""
        if tok_word_char(n) and tok_word_char(span[-1:]):
            return False
        return True
    return c[0] in WS or c[0] in PUNCT


def esc(b):
    """Bytes -> a literal bash $'...' escape string (backslash-x hex)."""
    return "".join("\\x%02x" % c for c in b)


def main():
    rng = random.Random(20261023)
    alphabet = ALNUM + WS + PUNCT + b"-'" + "é中".encode("utf-8")
    cases = []
    for c in alphabet:
        for extra in (b"", b"a", b" ", b"-"):
            cases.append((extra + bytes([c]), b"x", bytes([c]) + extra))
            cases.append((bytes([c]), b"x", bytes([c])))
            cases.append((b"", b"x", bytes([c])))
            cases.append((bytes([c]), b"x", b""))
    for _ in range(6000):
        before = bytes(rng.choice(alphabet) for _ in range(rng.randint(0, 5)))
        after = bytes(rng.choice(alphabet) for _ in range(rng.randint(0, 5)))
        span = bytes(rng.choice(alphabet) for _ in range(rng.randint(1, 3)))
        cases.append((before, span, after))
    with open("cases.tsv", "w") as f:
        for before, span, after in cases:
            f.write("%s|%s|%s\n" % (esc(before), esc(span), esc(after)))
    with open("cases.expect", "w") as f:
        for before, span, after in cases:
            f.write("%d %d %d\n" % (int(tok_left_ok(before, span)), int(tok_right_ok(after, span)),
                                    int(tok_word_char(span[0:1]))))
    print("cases: %d" % len(cases))


if __name__ == "__main__":
    sys.exit(main())
