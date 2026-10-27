#!/usr/bin/env python3
"""store-record-audit — judge the capture store and the fetch record as ONE evidence set (QUALITY 112/113).

For every corpus/captures/<key>.raw in the tree there must be a refetch.tsv row with that key and
at least one successful attempt (else ORPHAN). For every successful row there must be the key's
.raw bytes in the same tree (else RECORD_ONLY). For every key whose .raw exists and whose record
has successes, the LAST successful row's raw_sha256 must equal sha256 of the .raw (else
BYTES_STALE). For every key whose .raw exists but whose record has NO successful row
(STORE_BUT_RECORD_DENIES), the record currently denies bytes the store holds. Exit 1 when any
class is non-empty, 0 when the store and record are one clean set.

Usage:
  python3 tools/store-record-audit.py [--record PATH] [--store PATH]
"""
from __future__ import annotations

import argparse
import hashlib
import pathlib
import sys

HEADER = ["id", "url", "key", "attempt", "fetched_utc", "curl_rc", "http_code",
          "raw_sha256", "txt_sha256"]


def key(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:24]


def sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def failed(r: dict) -> bool:
    try:
        code = int(r["http_code"])
    except ValueError:
        code = 0
    return r["curl_rc"] != "0" or not (200 <= code <= 299) or r["raw_sha256"] == "-"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--record", default="corpus/evidence/round57/refetch.tsv")
    ap.add_argument("--store", default="corpus/captures")
    a = ap.parse_args()
    rec_p, store = pathlib.Path(a.record), pathlib.Path(a.store)
    recs: list[dict] = []
    if rec_p.is_file():
        lines = rec_p.read_text(encoding="utf-8").splitlines()
        if lines and lines[0].split("\t") == HEADER:
            recs = [dict(zip(HEADER, ln.split("\t"))) for ln in lines[1:] if ln]
    by_key: dict[str, list[dict]] = {}
    for r in recs:
        by_key.setdefault(r["key"], []).append(r)
    orphan, record_only, stale, denied = [], [], [], []
    for raw in sorted(store.glob("*.raw")):
        k = raw.stem
        rows = by_key.get(k, [])
        ok = [r for r in rows if not failed(r)]
        if not rows or not ok:
            orphan.append(k)
            continue
        if sha(raw) != ok[-1]["raw_sha256"]:
            stale.append(k)
    for k, rows in by_key.items():
        ok = [r for r in rows if not failed(r)]
        if ok and not (store / f"{k}.raw").is_file():
            record_only.append(k)
        if not ok and (store / f"{k}.raw").is_file():
            denied.append(k)
    for name, lst in (("ORPHAN", orphan), ("RECORD_ONLY", record_only),
                      ("BYTES_STALE", stale), ("STORE_BUT_RECORD_DENIES", denied)):
        print(f"{name}={len(lst)}" + (f" {sorted(lst)}" if lst else ""))
    bad = bool(orphan or record_only or stale or denied)
    print(f"STORE_RECORD_AUDIT={'FAIL' if bad else 'CLEAN'} rows={len(recs)} keys={len(by_key)}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
