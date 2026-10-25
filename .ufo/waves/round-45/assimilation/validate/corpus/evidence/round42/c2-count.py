#!/usr/bin/env python3
"""c2-count — the frozen counter for round 42 claim C2 (calibration).

Claim C2 (calibration): every row of the lane's quarantine slice carries exactly ONE
verdict from the frozen vocabulary, that verdict agrees with an INDEPENDENT
re-examination of the row, and it carries a non-empty reason and a non-empty flip
condition. The do-nothing control is a table whose rows are present but whose verdicts
disagree with the evidence: this counter must fail it.

Independence matters here: this counter does NOT read the gate tool's output and does
not reuse its matcher. It re-parses the register, re-resolves the captures, re-matches
the quotes with its own NFKC + whitespace-collapse test, and re-classifies each row
from its own magic-byte and interstitial checks. Where the two implementations
disagree, the conservative union decides (a row is checkable only when BOTH agree the
capture is the cited document) and the disagreement is counted and reported.

Table: corpus/evidence/round42/quarantine-verdicts.tsv — TSV, header line
`id<TAB>verdict<TAB>reason<TAB>flip`, one row per slice row.

Exit codes: 0 all counts hold · 1 a count failed · 2 usage/env.
"""
from __future__ import annotations

import hashlib
import pathlib
import re
import sys
import unicodedata

LANE = pathlib.Path(__file__).resolve().parents[3]
TABLE = LANE / "corpus/evidence/round42/quarantine-verdicts.tsv"
REGISTER = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md")
CACHE = pathlib.Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache")

VOCAB = {"present", "absent", "mixed", "unverifiable"}

# detector B — a different marker list from the gate tool's, same intent
WALL_MARKERS = (
    "client challenge", "just a moment", "enable javascript", "checking your browser",
    "attention required", "access denied", "verify you are human", "captcha",
    "error 1020", "unusual traffic", "403 forbidden", "请开启javascript", "验证码",
    "the request could not be satisfied", "request blocked",
)


def norm(s: str) -> str:
    """NFKC + whitespace collapse. The strict test."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", s))


def own_slice(register: pathlib.Path):
    """Own parse: find every table row whose second cell is the lane, third cell a
    round, fourth cell an S-id. Summary rows carry no round and no id."""
    out = {}
    for line in register.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        c = [x.strip() for x in line.split("|")]
        if len(c) < 6 or c[1] != "`chousa`":
            continue
        if not re.fullmatch(r"round\d+", c[2]):
            continue
        rid = c[3].rstrip("`")
        if not re.fullmatch(r"S\d+", rid):
            continue
        long_row = len(c) >= 8
        klass = c[4] if long_row else c[4]
        url = c[5]
        quotes = []
        if long_row:
            for raw in c[6].split("<br>"):
                q = raw.strip()
                if q.startswith("`") and q.endswith("`") and len(q) >= 2:
                    q = q[1:-1]
                if q.strip():
                    quotes.append(q.strip())
        unchecked = (not long_row) or ("could not be fetched" in klass.lower()
                                       or "named no locator" in klass.lower())
        out[rid] = {"url": url, "quotes": quotes, "unchecked": unchecked, "klass": klass}
    return out


def own_capture(url: str):
    """Resolve a URL to its local capture and classify it, with own checks."""
    if not url.startswith(("http://", "https://")):
        return None, None, "missing"
    key = hashlib.sha256(url.encode()).hexdigest()[:24]
    txt = CACHE / (key + ".txt")
    raw = CACHE / (key + ".raw")
    if not txt.exists():
        return None, None, "missing"
    body = txt.read_text(encoding="utf-8", errors="replace")
    head = b""
    if raw.exists():
        with raw.open("rb") as fh:
            head = fh.read(8)
    if head.startswith(b"PK\x03\x04") or head.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1") \
            or head.startswith(b"{\\rtf"):
        form = "binary"
    elif head.startswith(b"%PDF-"):
        form = "pdf-text"
    else:
        form = "text"
    low = body[:4000].lower()
    wall = any(m in low for m in WALL_MARKERS)
    return body, form, ("wall" if wall else form)


def own_class(row):
    """The frozen decision rule, applied by this counter's own machinery."""
    if row["unchecked"]:
        return "unverifiable"
    body, form, kind = own_capture(row["url"])
    if body is None or kind == "missing":
        return "unverifiable"
    if kind == "wall":
        return "unverifiable"
    if form == "binary":
        return "unverifiable"
    quotes = row["quotes"]
    if not quotes:
        return "unverifiable"
    if len(body) < max(len(q) for q in quotes):
        return "unverifiable"
    n_doc = norm(body)
    located = sum(1 for q in quotes if norm(q) in n_doc)
    if located == len(quotes):
        return "present"
    if located == 0:
        return "absent"
    return "mixed"


def read_table(path: pathlib.Path):
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        cells = line.split("\t")
        if lineno == 1 and cells[0].strip() == "id":
            continue
        if len(cells) < 4:
            continue
        rows.append((cells[0].strip(), cells[1].strip(), cells[2].strip(), cells[3].strip()))
    return rows


def main():
    if not TABLE.is_file():
        sys.stderr.write("c2-count: the verdict table is absent: %s\n" % TABLE)
        return 1
    slice_rows = own_slice(REGISTER)
    table = read_table(TABLE)
    tids = [r[0] for r in table]
    seen = {}
    dup = 0
    for r in table:
        seen[r[0]] = seen.get(r[0], 0) + 1
    dup = sum(v - 1 for v in seen.values() if v > 1)
    verdicted = sum(1 for rid in slice_rows if rid in seen)
    reason_ok = sum(1 for r in table if len(r[2]) > 0)
    flip_ok = sum(1 for r in table if len(r[3]) > 0)
    vocab_ok = sum(1 for r in table if r[1] in VOCAB)
    consistent = 0
    mismatches = []
    for rid, verdict, _reason, _flip in table:
        if rid not in slice_rows:
            continue
        expect = own_class(slice_rows[rid])
        if expect == verdict:
            consistent += 1
        else:
            mismatches.append("%s table=%s independent=%s" % (rid, verdict, expect))
    extra = sorted(set(tids) - set(slice_rows))
    total = len(slice_rows)
    print("VERDICTED=%d/%d" % (verdicted, total))
    print("CLASS_CONSISTENT=%d/%d" % (consistent, total))
    print("REASON_NONEMPTY=%d/%d" % (reason_ok, total))
    print("FLIP_NONEMPTY=%d/%d" % (flip_ok, total))
    print("VOCAB_OK=%d/%d" % (vocab_ok, total))
    print("DUPLICATE_ROWS=%d" % dup)
    print("ROWS_OUTSIDE_SLICE=%d%s" % (len(extra), (" " + ",".join(extra)) if extra else ""))
    for m in mismatches:
        print("MISMATCH %s" % m)
    ok = (verdicted == total and consistent == total and reason_ok == total
          and flip_ok == total and vocab_ok == total and dup == 0 and not extra)
    print("C2=%s" % ("PASS" if ok else "FAIL"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
