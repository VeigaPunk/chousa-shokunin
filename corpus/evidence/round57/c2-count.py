#!/usr/bin/env python3
"""R57-C2 frozen counter — freshness: the lane's pinned captures re-fetched into lane-owned bytes.

Predicate R57-C2, the same sentence as corpus/evidence/round57/claims.md:
for each of the 47 distinct (id, url, capture_sha256) triples pinned by the
spans manifests committed at SET_REV (every `corpus/evidence/**/spans.tsv`
with a `capture_sha256` column), the lane holds exactly one verdict
recomputed from committed bytes — REPRODUCED: a lane-owned capture
`corpus/captures/<key>.raw` (key = first 24 hex of sha256(url)), whose
sha256 equals the raw_sha256 of the triple's last successful attempt in
`corpus/evidence/round57/refetch.tsv`, has the pinned digest itself or a
`<key>.txt` beside it that has it; DRIFTED: such a capture exists and
neither digest equals the pin; UNREACHABLE: no capture, and at least two
failed attempts (curl_rc != 0, or http_code outside 200-299, or an empty
body) recorded at least 600 seconds apart — and every byte-backed capture is
CONSISTENT (its `.txt` equals the frozen campaign recipe applied to its
`.raw`: a `%PDF-` raw through `pdftotext -layout` 26.08.0 when that text is
non-blank, otherwise the raw decoded as UTF-8 with replacement and, when it
starts like HTML, the campaign's `html_to_text`), and every DRIFTED capture
on which some quote of a spans row pinned to that triple no longer occurs
in its defined text form (an OLE or zip raw: the stdout of
`tools/capture-text.py`; otherwise the `.txt`) is FLAGGED by the line
`- FRESHNESS-FLAG <id> <key> absent=<a>/<m>` in
`corpus/lessons/round-57.md` with the counter's own a and m — counted
`SET=47 VERDICTS=47/47 CONSISTENT=b/b FLAGGED=g/g` with REPRODUCED >= 5 and
BYTE_BACKED (REPRODUCED + DRIFTED) >= 32, printed `C2=PASS`.

REPRODUCED binds bytes to the pin by sha256 (no preimage forge); DRIFTED and
UNREACHABLE are attested by the fetch record, not provable from bytes — the
counter prints them separately and the target's REPRODUCED floor is the
cryptographic part.

refetch.tsv header (tab-separated):
  id url key attempt fetched_utc curl_rc http_code raw_sha256 txt_sha256
fetched_utc is `YYYY-MM-DDTHH:MM:SSZ`; raw_sha256 / txt_sha256 are `-` when absent.

Usage: python3 corpus/evidence/round57/c2-count.py [--root LANE] [--verbose]
Exit codes: 0 C2=PASS · 1 C2=FAIL · 2 usage/env (ENV_CHANGED).
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import importlib.util
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
SET_REV = "6656f0770a1460d6ba73d9d2976f698a35311921"
SET_N = 47
PDFTOTEXT = "pdftotext version 26.08.0"
REFETCH_HEADER = ["id", "url", "key", "attempt", "fetched_utc", "curl_rc", "http_code", "raw_sha256", "txt_sha256"]
OLE = b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"
ZIP = b"PK\x03\x04"
MIN_REPRODUCED = 5
MIN_BYTE_BACKED = 32
FLAG_RE = re.compile(r"^- FRESHNESS-FLAG (S\d{3}) ([0-9a-f]{24}) absent=(\d+)/(\d+)\s*$")


def env(msg: str) -> None:
    print(f"ENV_CHANGED {msg}")
    sys.exit(2)


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git(root: pathlib.Path, *args: str) -> bytes:
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if r.returncode != 0:
        env(f"git {' '.join(args)}: {r.stderr.decode(errors='replace')[:200]}")
    return r.stdout


def pinned_set(root: pathlib.Path):
    """{(id, url, pin): [(path, quote), ...]} from the manifests committed at SET_REV."""
    names = git(root, "ls-tree", "-r", "--name-only", SET_REV, "corpus/evidence").decode().split("\n")
    out: dict[tuple[str, str, str], list[tuple[str, str]]] = {}
    for p in names:
        if not p.endswith("spans.tsv"):
            continue
        lines = git(root, "show", f"{SET_REV}:{p}").decode("utf-8").splitlines()
        if not lines:
            continue
        h = lines[0].split("\t")
        if "capture_sha256" not in h:
            continue
        ii, iu, ic, iq = h.index("id"), h.index("url"), h.index("capture_sha256"), h.index("quote")
        for line in lines[1:]:
            c = line.split("\t")
            if len(c) < len(h):
                continue
            out.setdefault((c[ii], c[iu], c[ic]), []).append((p, c[iq]))
    if len(out) != SET_N:
        env(f"pinned set has {len(out)} triples, frozen {SET_N}")
    return out


def html_to_text(s: str) -> str:
    """Verbatim from the campaign's quote-lint.py (sha256 e864a01f…), the recipe the pins were made with."""
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h[1-6]>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\u00a0]+", " ", s)
    return s


def recipe_txt(raw: bytes, tmp: pathlib.Path) -> str:
    if raw[:5] == b"%PDF-":
        p = tmp / "r.pdf"
        p.write_bytes(raw)
        r = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, timeout=120)
        txt = r.stdout.decode("utf-8", "replace")
        p.unlink()
        if txt.strip():
            return txt
    txt = raw.decode("utf-8", "replace")
    if re.search(r"(?is)^\s*(?:<!doctype\s+html|<html[\s>]|<head[\s>]|<body[\s>])", txt[:4000]):
        txt = html_to_text(txt)
    return txt


def defined_form(root: pathlib.Path, raw_p: pathlib.Path, txt_p: pathlib.Path, ct) -> str | None:
    raw = raw_p.read_bytes()
    if raw[:8] == OLE or raw[:4] == ZIP:
        try:
            return ct.text_form(str(raw_p))
        except Exception:
            return None
    if txt_p.is_file():
        return txt_p.read_bytes().decode("utf-8", "replace").replace("\r\n", "\n").replace("\r", "\n")
    return None


def when(s: str) -> dt.datetime | None:
    try:
        return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return None


def failed(r: dict) -> bool:
    try:
        code = int(r["http_code"])
    except ValueError:
        code = 0
    return r["curl_rc"] != "0" or not (200 <= code <= 299) or r["raw_sha256"] == "-"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=str(HERE.parents[2]))
    ap.add_argument("--verbose", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    v = subprocess.run(["pdftotext", "-v"], capture_output=True, text=True)
    if PDFTOTEXT not in (v.stdout + v.stderr):
        env("pdftotext is not 26.08.0")
    lane = HERE.parents[2]
    spec = importlib.util.spec_from_file_location("capture_text", lane / "tools" / "capture-text.py")
    ct = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ct)
    pset = pinned_set(lane)
    store = root / "corpus" / "captures"
    rec_p = root / "corpus" / "evidence" / "round57" / "refetch.tsv"
    recs: list[dict] = []
    if rec_p.is_file():
        lines = rec_p.read_text(encoding="utf-8").splitlines()
        if not lines or lines[0].split("\t") != REFETCH_HEADER:
            print("REFETCH_HEADER bad")
        else:
            for line in lines[1:]:
                c = line.split("\t")
                if len(c) == len(REFETCH_HEADER):
                    recs.append(dict(zip(REFETCH_HEADER, c)))
    lesson = root / "corpus" / "lessons" / "round-57.md"
    flags = {}
    if lesson.is_file():
        for line in lesson.read_text(encoding="utf-8").splitlines():
            m = FLAG_RE.match(line)
            if m:
                flags[(m.group(1), m.group(2))] = (int(m.group(3)), int(m.group(4)))
    counts = {"REPRODUCED": 0, "DRIFTED": 0, "UNREACHABLE": 0, "MISSING": 0}
    consistent = backed = need_flag = flagged = 0
    with tempfile.TemporaryDirectory() as td:
        tmp = pathlib.Path(td)
        for (sid, url, pin), rows in sorted(pset.items()):
            k = key(url)
            mine = [r for r in recs if r["id"] == sid and r["url"] == url and r["key"] == k]
            raw_p, txt_p = store / f"{k}.raw", store / f"{k}.txt"
            ok = [r for r in mine if not failed(r)]
            verdict, note = "MISSING", ""
            if raw_p.is_file():
                raw = raw_p.read_bytes()
                if not ok or ok[-1]["raw_sha256"] != sha(raw):
                    note = "capture not the last successful attempt's bytes"
                else:
                    backed += 1
                    txt = txt_p.read_bytes() if txt_p.is_file() else None
                    if txt is not None and txt == recipe_txt(raw, tmp).encode("utf-8") \
                            and ok[-1]["txt_sha256"] == sha(txt):
                        consistent += 1
                    else:
                        note = "txt is not the recipe of raw"
                    if pin in (sha(raw), sha(txt) if txt is not None else ""):
                        verdict = "REPRODUCED"
                    else:
                        verdict = "DRIFTED"
                        form = defined_form(root, raw_p, txt_p, ct)
                        m = len(rows)
                        absent = m if form is None else sum(1 for _, q in rows if q not in form)
                        note = f"absent={absent}/{m}"
                        if absent:
                            need_flag += 1
                            if flags.get((sid, k)) == (absent, m):
                                flagged += 1
            else:
                fails = sorted(t for t in (when(r["fetched_utc"]) for r in mine if failed(r)) if t)
                if len(fails) >= 2 and (fails[-1] - fails[0]).total_seconds() >= 600:
                    verdict = "UNREACHABLE"
                    note = f"{len(fails)} failed attempts"
            counts[verdict] += 1
            if a.verbose:
                print(f"CAPTURE {sid} {k} pin={pin[:12]} {verdict} {note}".rstrip())
    verdicts = SET_N - counts["MISSING"]
    ok_all = (verdicts == SET_N and consistent == backed and flagged == need_flag
              and counts["REPRODUCED"] >= MIN_REPRODUCED and backed >= MIN_BYTE_BACKED)
    print(f"SET={SET_N} VERDICTS={verdicts}/{SET_N} REPRODUCED={counts['REPRODUCED']} DRIFTED={counts['DRIFTED']} "
          f"UNREACHABLE={counts['UNREACHABLE']} BYTE_BACKED={backed} CONSISTENT={consistent}/{backed} "
          f"FLAGGED={flagged}/{need_flag} C2={'PASS' if ok_all else 'FAIL'}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
