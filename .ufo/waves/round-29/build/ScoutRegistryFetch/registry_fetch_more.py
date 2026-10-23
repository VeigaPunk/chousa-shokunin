#!/usr/bin/env python3
"""Additive pass: fetch only registry rows that have no record in the TSV yet.

Never re-fetches a URL that already has a record (the one-GET-per-URL bound).
Reuses one(), MAXB and SUPPORTED from registry_fetch.py in the same directory.
"""
import csv
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from registry_fetch import MAXB, SUPPORTED, one, rows as reg_rows  # noqa: E402

HDR = ["id", "url", "fetch", "status", "final_url", "final_host", "content_type", "content_encoding",
       "charset", "bytes_read", "inflated_bytes", "html_chars", "text_words", "contract_supported", "note"]


def host_of(u):
    return u.split("//", 1)[-1].split("/", 1)[0] if u else ""


def main():
    tsv = sys.argv[1]
    with open(tsv, newline="", encoding="utf-8") as f:
        old = list(csv.DictReader(f, delimiter="\t"))
    seen_ids = {r["id"] for r in old}
    url_rec = {}
    for r in old:
        if r["fetch"] == "yes":
            url_rec[r["url"]] = r
    reg = reg_rows()
    # stability check: did any already-recorded row's URL change in the registry?
    drift = [(r["id"], r["url"], dict(reg).get(r["id"])) for r in old if dict(reg).get(r["id"]) != r["url"]]
    for d in drift:
        print(f"DRIFT {d[0]}: recorded {d[1]} now {d[2]}", flush=True)
    new = [(sid, url) for sid, url in reg if sid not in seen_ids and url]
    with open(tsv, "a", encoding="utf-8") as out:
        for sid, url in new:
            if url in url_rec:
                o = url_rec[url]
                row = [sid, url, f"dup-of-{o['id']}"] + [o[k] for k in HDR[3:]]
                out.write("\t".join(row) + "\n")
                out.flush()
                print(f"{sid:5s} dup-of-{o['id']} (URL already recorded; not re-fetched)", flush=True)
                continue
            t0 = time.time()
            rec = one(url)
            dt = f"{time.time() - t0:.1f}s"
            ok = ("yes" if (rec["status"].isdigit() and rec["status"].startswith("2")
                            and rec["ctype"] in SUPPORTED
                            and rec["bytes"].isdigit() and int(rec["bytes"]) <= MAXB) else "no")
            row = [sid, url, "yes", rec["status"], rec["final_url"], host_of(rec["final_url"]),
                   rec["ctype"], rec["enc"], rec["charset"], rec["bytes"], rec["inflated"],
                   rec["chars"], rec["words"], ok, rec["note"] or f"elapsed={dt}"]
            out.write("\t".join(row) + "\n")
            out.flush()
            print(f"{sid:5s} {rec['status']:4s} {rec['ctype']:24s} {rec['bytes']:>9s}B "
                  f"words={rec['words']:>7s} {ok:3s} {dt} {url}", flush=True)
    print(f"new_rows={len(new)} drift={len(drift)}", flush=True)


if __name__ == "__main__":
    main()
