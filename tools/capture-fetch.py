#!/usr/bin/env python3
"""capture-fetch.py — chousa L1 re-fetch tool under an approval table (round 57).

Fetches (id, url) pairs with the campaign recipe (verbatim from
shokuknow quote-lint.py fetch(), sha256 e864a01f… at 03d69cd9):
one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per
attempt, NO retry inside the tool, at most 3 attempts per (id, url)
across calls (recorded in corpus/evidence/round57/refetch.tsv).

On a successful attempt (curl_rc == 0, http_code 200-299, non-empty body)
the bytes land at corpus/captures/<key>.raw and the recipe text form at
corpus/captures/<key>.txt, where key = sha256(url)[:24]. The store is
content-addressed: a re-fetch of unchanged content writes identical bytes.
Every attempt appends one row to refetch.tsv (chronological order — the
c2 counter takes the LAST successful row as the capture's bytes):

  id  url  key  attempt  fetched_utc  curl_rc  http_code  raw_sha256  txt_sha256

fetched_utc is UTC `YYYY-MM-DDTHH:MM:SSZ`; the sha columns are `-` when
absent (failure rows). UNREACHABLE attestations (c2-count) need >= 2 failed
attempts recorded >= 600 s apart — the caller spaces passes; this tool
never sleeps and never retries.

Scratch for curl's temp output honours $HYAKU_SCRATCH
(default /fast/scratch/hyaku) — never /tmp for large bodies (§7).

Usage:
  python3 tools/capture-fetch.py --id S082 --url https://… [--id S083 --url …] …
  python3 tools/capture-fetch.py --tsv pairs.tsv   # id<TAB>url per line
  python3 tools/capture-fetch.py --status          # per-(id,url) attempt summary

Exit: 0 all attempts recorded; 2 usage/limits.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import os
import pathlib
import re
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
LANE = HERE.parent
EVID = LANE / "corpus" / "evidence" / "round57"
REC = EVID / "refetch.tsv"
STORE = LANE / "corpus" / "captures"
HEADER = ["id", "url", "key", "attempt", "fetched_utc", "curl_rc", "http_code",
          "raw_sha256", "txt_sha256"]
MAX_ATTEMPTS = 3
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def html_to_text(s: str) -> str:
    """Verbatim from the campaign's quote-lint.py (sha256 e864a01f…)."""
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?s)<!--.*?-->", " ", s)
    s = re.sub(r"(?i)<br\s*/?>|</p>|</div>|</li>|</tr>|</h[1-6]>", "\n", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t\xa0]+", " ", s)
    return s


def recipe_txt(raw: bytes, tmp: pathlib.Path) -> str:
    """The frozen campaign text recipe (same as c2-count.recipe_txt)."""
    if raw[:5] == b"%PDF-":
        p = tmp / "r.pdf"
        p.write_bytes(raw)
        r = subprocess.run(["pdftotext", "-layout", str(p), "-"],
                           capture_output=True, timeout=120)
        txt = r.stdout.decode("utf-8", "replace")
        p.unlink()
        if txt.strip():
            return txt
    txt = raw.decode("utf-8", "replace")
    if re.search(r"(?is)^\s*(?:<!doctype\s+html|<html[\s>]|<head[\s>]|<body[\s>])", txt[:4000]):
        txt = html_to_text(txt)
    return txt


def read_records() -> list[dict]:
    if not REC.is_file():
        return []
    lines = REC.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].split("\t") != HEADER:
        print(f"refetch header bad: {REC}", file=sys.stderr)
        sys.exit(2)
    return [dict(zip(HEADER, ln.split("\t"))) for ln in lines[1:] if ln]


def append_row(scratch: pathlib.Path, sid: str, url: str, attempt: int,
               rc: int, http: str, raw: bytes | None, txt: bytes | None) -> None:
    raw_sha = sha(raw) if raw is not None else "-"
    txt_sha = sha(txt) if txt is not None else "-"
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    row = [sid, url, key(url), str(attempt), stamp, str(rc), http, raw_sha, txt_sha]
    tmp_out = scratch / "refetch.append"
    with tmp_out.open("a", encoding="utf-8") as f:
        f.write("\t".join(row) + "\n")
    with REC.open("a", encoding="utf-8") as f:
        f.write("\t".join(row) + "\n")
    k = key(url)
    if raw is not None:
        (STORE / f"{k}.raw").write_bytes(raw)
        (STORE / f"{k}.txt").write_bytes(txt if txt is not None else b"")
    print(f"{sid} {k} attempt={attempt} rc={rc} http={http} raw={raw_sha[:12]} "
          f"txt={txt_sha[:12]}{' STORED' if raw is not None else ''}")


def fetch_one(scratch: pathlib.Path, sid: str, url: str, attempt: int) -> None:
    out = scratch / f"{key(url)}.{attempt}.out"
    code_file = scratch / f"{key(url)}.{attempt}.code"
    cmd = ["curl", "-fsSL", "--compressed", "--max-time", "15", "-A", UA,
           "-o", str(out), "-w", "%{http_code}", url]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=25, text=True)
        http = (r.stdout or "").strip() or "000"
        rc = r.returncode
    except subprocess.TimeoutExpired:
        http, rc = "000", 28
    raw: bytes | None = None
    txt: bytes | None = None
    if rc == 0 and out.is_file() and out.stat().st_size > 0:
        try:
            code = int(http)
        except ValueError:
            code = 0
        if 200 <= code <= 299:
            raw = out.read_bytes()
            tmp = scratch / "recipe"
            tmp.mkdir(parents=True, exist_ok=True)
            txt = recipe_txt(raw, tmp).encode("utf-8")
    append_row(scratch, sid, url, attempt, rc, http, raw, txt)
    out.unlink(missing_ok=True)
    code_file.unlink(missing_ok=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--id", action="append", default=[])
    ap.add_argument("--url", action="append", default=[])
    ap.add_argument("--tsv")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    pairs: list[tuple[str, str]] = []
    if a.tsv:
        for ln in pathlib.Path(a.tsv).read_text(encoding="utf-8").splitlines():
            if ln.strip() and not ln.startswith("#"):
                c = ln.split("\t")
                pairs.append((c[0].strip(), c[1].strip()))
    pairs.extend(zip(a.id, a.url))
    recs = read_records()
    if a.status:
        byk: dict[tuple[str, str], list[dict]] = {}
        for r in recs:
            byk.setdefault((r["id"], r["url"]), []).append(r)
        for (sid, url), rs in sorted(byk.items()):
            fails = sum(1 for r in rs if r["curl_rc"] != "0")
            print(f"{sid} {key(url)} attempts={len(rs)} fails={fails} url={url}")
        print(f"pairs={len(byk)} rows={len(recs)}")
        return 0
    if not pairs:
        ap.error("no pairs (use --id/--url, --tsv or --status)")
    if len(a.id) != len(a.url):
        ap.error("--id and --url counts differ")
    counts: dict[tuple[str, str], int] = {}
    for r in recs:
        counts[(r["id"], r["url"])] = counts.get((r["id"], r["url"]), 0) + 1
    scratch = pathlib.Path(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku")
                           ) / "chousa-r57" / "fetch"
    scratch.mkdir(parents=True, exist_ok=True)
    EVID.mkdir(parents=True, exist_ok=True)
    STORE.mkdir(parents=True, exist_ok=True)
    if not REC.is_file():
        REC.write_text("\t".join(HEADER) + "\n", encoding="utf-8")
    for sid, url in pairs:
        n = counts.get((sid, url), 0)
        if n >= MAX_ATTEMPTS:
            print(f"{sid} {url}: already {n} attempts (max {MAX_ATTEMPTS}) — skipped")
            continue
        fetch_one(scratch, sid, url, n + 1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
