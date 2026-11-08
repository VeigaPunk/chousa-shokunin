#!/usr/bin/env python3
"""gate-records.py — verify a lesson's `GATE-RECORD` lines against committed lane bytes (round 83).

Usage:
    python3 tools/gate-records.py verify --root LANE [--repo GITDIR] FILE...

A lesson's `## Gate` block carries one `GATE-RECORD` line per registry row it touched. Until round 83 each record
was checked by hand with the lesson's "Location command". This tool checks every record in each FILE mechanically,
reading only committed lane bytes: `corpus/SOURCES.md`, `corpus/captures/`, `corpus/evidence/round57/refetch.tsv`
under LANE, and (for the rev form) git objects in GITDIR (default LANE) through read-only `git cat-file`.
It never fetches, never writes a file and never runs a mutating git command.

A record is any line whose first text, after leading whitespace and invisible format characters (Unicode category
Cf, e.g. a BOM or a zero-width space), is the word `GATE-RECORD` followed by whitespace or the end of the line; such a
line is checked, never skipped. A mention elsewhere in a line (inline code, list item, blockquote, HTML comment) is
prose, not a record. Every record must parse into exactly one of three forms:

  url/admit   GATE-RECORD S<id> url=<http(s) url> fetched=<YYYY-MM-DDTHH:MM:SSZ> tier=<A|B|C> decision=<admit|reject>
              capture=corpus/captures/<24 hex>.txt capture_sha256=<>=16 hex>[…] words=<n> quote="<text>"
  url/unreach GATE-RECORD S<id> url=<url> fetched=<ts> tier=<A|B|C> decision=reject capture=none curl_rc=<n>
              http=<nnn> words=0 quote=none
  rev         GATE-RECORD S<id> rev=<40 hex> path=<repo-relative path> line=<n> words=<n> quote=<text to end of line>

Keys appear once each, in any order, before `quote=`; `quote=` is last. Every digit (S-id, `words`, `line`, `curl_rc`,
`http`, `fetched`) is ASCII 0-9, and `words`, `line` and `curl_rc` carry no leading zero (round-83 post-scoring repair:
Python's Unicode digit class had admitted `line=2٢٢` as line 222, `R83ExecForge` Finding 1). Checks (codes, all reported):

  PARSE         the line fits none of the three forms (unknown/missing/duplicate key, bad value, extra text)
  REGISTRY      S<id> has no 11-column Registry row in corpus/SOURCES.md (0-3 leading spaces accepted, as the census)
  TIER          url forms: tier differs from the registry row's tier cell
  CAPTURE_PATH  capture is not corpus/captures/<24 hex>.txt, or is not a regular (non-symlink) file inside LANE
  CAPTURE_KEY   the capture key is not sha256(url)[:24] (the content-addressed key capture-fetch.py writes)
  CAPTURE_SHA   capture_sha256 is shorter than 16 hex digits or is not a prefix of sha256(capture bytes)
  REFETCH       url/admit: no refetch.tsv row with this id, url, key and fetched time, curl_rc 0, http 2xx and
                txt_sha256 equal to sha256(capture bytes); url/unreach: no row with this id, url and fetched time
                whose curl_rc and http equal the record's, or the record's curl_rc/http denote a success
  WORDS         words differs from the number of whitespace-separated tokens of the quote
  QUOTE_LEN     a quoted record (url/admit, rev) has fewer than 1 or more than 25 words
  QUOTE_ABSENT  url/admit: the quote, normalized, does not occur in the normalized capture text
  REV           rev form: rev is not a commit in GITDIR or path is not a blob at rev
  LINE          rev form: line is outside the blob, or the normalized quote does not occur in that one line

Normalization (quote and text alike): U+2018/U+2019 -> ', U+201C/U+201D -> ", then whitespace runs (Python
str.split) collapse to one space. Matching is otherwise exact (case, punctuation and markup are kept).

Output, one line per record, then a summary:
    GATE_RECORD <file>:<line> <S-id|?> OK
    GATE_RECORD <file>:<line> <S-id|?> FAIL <CODE>[,<CODE>...]
    GATE_RECORDS files=<f> records=<n> ok=<k> fail=<m>
Exit: 0 when records >= 1 and every record is OK; 1 when any record fails or no record is found; 2 on usage or I/O
error (missing FILE, missing registry or refetch log).

Python 3 standard library only.
"""
import argparse
import hashlib
import os
import re
import subprocess
import sys
import unicodedata

SID_RE = re.compile(r"S[0-9]{3,}")
TS_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")
HEX40_RE = re.compile(r"[0-9a-f]{40}")
CAP_RE = re.compile(r"corpus/captures/([0-9a-f]{24})\.txt")
SHA_RE = re.compile(r"([0-9a-f]{16,64})(?:…|\.\.\.)?")
REC_RE = re.compile(r"^GATE-RECORD(?:\s|$)")


def lead_strip(line):
    """Drop leading whitespace and Cf format characters (BOM, zero-width space, ...)."""
    i = 0
    while i < len(line) and (line[i].isspace() or unicodedata.category(line[i]) == "Cf"):
        i += 1
    return line[i:]


ROW_RE = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|")
INT_RE = re.compile(r"0|[1-9][0-9]{0,6}")

URL_ADMIT = ("url", "fetched", "tier", "decision", "capture", "capture_sha256", "words")
URL_UNREACH = ("url", "fetched", "tier", "decision", "capture", "curl_rc", "http", "words")
REV_KEYS = ("rev", "path", "line", "words")


def norm(s):
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    return " ".join(s.split())


def sha256_file(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def parse(line):
    """Return (sid, kv, quote, form) or None when the line fits no form."""
    m = re.match(r"^GATE-RECORD (S[0-9]{3,}) (.*)$", lead_strip(line).rstrip("\r\n"))
    if not m:
        return None
    sid, rest = m.group(1), m.group(2)
    qpos = rest.find(" quote=") if not rest.startswith("quote=") else -1
    if rest.startswith("quote="):
        return None
    if qpos < 0:
        return None
    head, qraw = rest[:qpos], rest[qpos + len(" quote="):]
    kv = {}
    for tok in head.split(" "):
        if "=" not in tok:
            return None
        k, v = tok.split("=", 1)
        if not k or k in kv or not v:
            return None
        kv[k] = v
    keys = set(kv)
    if keys == set(REV_KEYS):
        form = "rev"
        quote = qraw.rstrip()
        if not quote:
            return None
    elif keys == set(URL_ADMIT):
        form = "admit"
        q = qraw.rstrip()
        if len(q) < 2 or not (q.startswith('"') and q.endswith('"')):
            return None
        quote = q[1:-1]
    elif keys == set(URL_UNREACH):
        form = "unreach"
        if qraw.rstrip() != "none" or kv["capture"] != "none" or kv["words"] != "0" or kv["decision"] != "reject":
            return None
        quote = None
    else:
        return None
    if "words" in kv and not INT_RE.fullmatch(kv["words"]):
        return None
    if form in ("admit", "unreach"):
        if not re.fullmatch(r"https?://\S+", kv["url"]) or not TS_RE.fullmatch(kv["fetched"]):
            return None
        if kv["tier"] not in ("A", "B", "C") or kv["decision"] not in ("admit", "reject"):
            return None
    if form == "unreach":
        if not INT_RE.fullmatch(kv["curl_rc"]) or not re.fullmatch(r"[0-9]{3}", kv["http"]):
            return None
    if form == "rev":
        if not INT_RE.fullmatch(kv["line"]) or kv["line"] == "0":
            return None
    return sid, kv, quote, form


def load_registry(path):
    reg = {}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            m = ROW_RE.match(ln)
            if not m:
                continue
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) != 11:
                continue
            reg.setdefault(cells[0], cells)
    return reg


def load_refetch(path):
    rows = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            f = ln.rstrip("\n").split("\t")
            if len(f) == 9:
                rows.append(f)
    return rows


def git_blob(repo, rev, path):
    """Return the blob bytes of rev:path, or None. Read-only."""
    try:
        t = subprocess.run(["git", "-C", repo, "cat-file", "-t", rev + "^{commit}"], capture_output=True, text=True)
        if t.returncode != 0 or t.stdout.strip() != "commit":
            return None
        spec = rev + ":" + path
        t = subprocess.run(["git", "-C", repo, "cat-file", "-t", spec], capture_output=True, text=True)
        if t.returncode != 0 or t.stdout.strip() != "blob":
            return None
        b = subprocess.run(["git", "-C", repo, "cat-file", "blob", spec], capture_output=True)
        return b.stdout if b.returncode == 0 else None
    except OSError:
        return None


def check(rec, root, repo, reg, refetch):
    sid, kv, quote, form = rec
    codes = []
    regrow = reg.get(sid)
    if regrow is None:
        codes.append("REGISTRY")
    if form in ("admit", "rev"):
        n = len(quote.split())
        if kv["words"] != str(n):
            codes.append("WORDS")
        if not 1 <= n <= 25:
            codes.append("QUOTE_LEN")
    if form in ("admit", "unreach"):
        if regrow is not None and regrow[3] != kv["tier"]:
            codes.append("TIER")
        url = kv["url"]
        key = hashlib.sha256(url.encode()).hexdigest()[:24]
    if form == "admit":
        cm = CAP_RE.fullmatch(kv["capture"])
        cap = os.path.join(root, kv["capture"]) if cm else None
        capdir = os.path.realpath(os.path.join(root, "corpus", "captures"))
        if (cap is None or os.path.islink(cap) or not os.path.isfile(cap)
                or os.path.dirname(os.path.realpath(cap)) != capdir):
            codes.append("CAPTURE_PATH")
            cap = None
        if cm and cm.group(1) != key:
            codes.append("CAPTURE_KEY")
        capsha = sha256_file(cap) if cap else None
        sm = SHA_RE.fullmatch(kv["capture_sha256"])
        if not sm or capsha is None or not capsha.startswith(sm.group(1)):
            codes.append("CAPTURE_SHA")
        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0"
                 and re.fullmatch(r"2[0-9][0-9]", r[6]) and capsha is not None and r[8] == capsha for r in refetch)
        if not ok:
            codes.append("REFETCH")
        if cap is not None:
            with open(cap, encoding="utf-8", errors="replace") as fh:
                text = norm(fh.read())
            if not quote.strip() or norm(quote) not in text:
                codes.append("QUOTE_ABSENT")
        else:
            codes.append("QUOTE_ABSENT")
    elif form == "unreach":
        success = kv["curl_rc"] == "0" and kv["http"].startswith("2")
        ok = (not success) and any(r[0] == sid and r[1] == url and r[4] == kv["fetched"] and r[5] == kv["curl_rc"]
                                   and r[6] == kv["http"] for r in refetch)
        if not ok:
            codes.append("REFETCH")
    elif form == "rev":
        blob = None
        if HEX40_RE.fullmatch(kv["rev"]):
            blob = git_blob(repo, kv["rev"], kv["path"])
        if blob is None:
            codes.append("REV")
            codes.append("LINE")
        else:
            lines = blob.decode("utf-8", errors="replace").split("\n")
            if lines and lines[-1] == "":
                lines.pop()
            i = int(kv["line"])
            if i > len(lines) or not quote.strip() or norm(quote) not in norm(lines[i - 1]):
                codes.append("LINE")
    return sorted(set(codes))


def main():
    ap = argparse.ArgumentParser(prog="gate-records.py")
    sub = ap.add_subparsers(dest="cmd")
    v = sub.add_parser("verify")
    v.add_argument("--root", required=True)
    v.add_argument("--repo")
    v.add_argument("files", nargs="+")
    try:
        a = ap.parse_args()
    except SystemExit:
        return 2
    if a.cmd != "verify":
        ap.print_usage(sys.stderr)
        return 2
    root = os.path.abspath(a.root)
    repo = os.path.abspath(a.repo) if a.repo else root
    regp = os.path.join(root, "corpus", "SOURCES.md")
    refp = os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv")
    for p in (regp, refp):
        if not os.path.isfile(p):
            print(f"GATE_RECORDS_ERROR missing {p}", file=sys.stderr)
            return 2
    for f in a.files:
        if not os.path.isfile(f):
            print(f"GATE_RECORDS_ERROR missing {f}", file=sys.stderr)
            return 2
    reg = load_registry(regp)
    refetch = load_refetch(refp)
    n = ok = 0
    for f in a.files:
        with open(f, encoding="utf-8", errors="replace") as fh:
            for i, ln in enumerate(fh, 1):
                if not REC_RE.match(lead_strip(ln)):
                    continue
                n += 1
                rec = parse(ln)
                if rec is None:
                    sm = SID_RE.search(ln)
                    print(f"GATE_RECORD {f}:{i} {sm.group(0) if sm else '?'} FAIL PARSE")
                    continue
                codes = check(rec, root, repo, reg, refetch)
                if codes:
                    print(f"GATE_RECORD {f}:{i} {rec[0]} FAIL {','.join(codes)}")
                else:
                    ok += 1
                    print(f"GATE_RECORD {f}:{i} {rec[0]} OK")
    print(f"GATE_RECORDS files={len(a.files)} records={n} ok={ok} fail={n - ok}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
