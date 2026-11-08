#!/usr/bin/env python3
"""Capture-store integrity for the registry rows changed this round.

Usage: python3 -B capture-integrity.py --repo REPO --landing LAND_REV --base BASE_REV
Reads committed bytes only (git show). For every refetch row added between
base and landing, checks key == sha256(url)[:24], the committed capture's
sha256 against the row's raw_sha256/txt_sha256, and reports line counts and
the location of the quote each registry anchor names. Never fetches.
"""
import argparse
import hashlib
import subprocess
import sys

QUOTES = {
    "S216": "the enclosed content has been modified from that of the origin server's 200 (OK) response by a transforming proxy",
    "S031": "Date on which the content on this web page was last reviewed for accuracy and/or completeness.",
}


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True)
    if r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {r.stderr.decode(errors='replace')}")
    return r.stdout


def show(repo, rev, path):
    return git(repo, "show", f"{rev}:{path}")


def parse_tsv(b):
    lines = b.decode().splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, l.split("\t"))) for l in lines[1:] if l]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--landing", required=True)
    a = ap.parse_args()
    old = {(r["id"], r["url"], r["attempt"], r["fetched_utc"])
           for r in parse_tsv(show(a.repo, a.base, "corpus/evidence/round57/refetch.tsv"))}
    new = parse_tsv(show(a.repo, a.landing, "corpus/evidence/round57/refetch.tsv"))
    added = [r for r in new if (r["id"], r["url"], r["attempt"], r["fetched_utc"]) not in old]
    ok = True
    print("id\tkey_ok\traw_sha_ok\ttxt_sha_ok\traw_bytes\traw_lines\ttxt_lines")
    for r in added:
        k = hashlib.sha256(r["url"].encode()).hexdigest()[:24]
        key_ok = k == r["key"]
        try:
            raw = show(a.repo, a.landing, f"corpus/captures/{r['key']}.raw")
            txt = show(a.repo, a.landing, f"corpus/captures/{r['key']}.txt")
        except SystemExit:
            print(f"{r['id']}\tMISSING_CAPTURE")
            ok = False
            continue
        raw_ok = hashlib.sha256(raw).hexdigest() == r["raw_sha256"]
        txt_ok = hashlib.sha256(txt).hexdigest() == r["txt_sha256"]
        print(f"{r['id']}\t{key_ok}\t{raw_ok}\t{txt_ok}\t{len(raw)}\t"
              f"{len(raw.decode('utf-8', 'replace').splitlines())}\t"
              f"{len(txt.decode('utf-8', 'replace').splitlines())}")
        ok = ok and key_ok and raw_ok and txt_ok
    for rid, q in QUOTES.items():
        orig = [r for r in new if r["id"] == rid][-1]
        txt = show(a.repo, a.landing, f"corpus/captures/{orig['key']}.txt").decode("utf-8", "replace")
        words, linenos = [], []
        for i, line in enumerate(txt.splitlines(), 1):
            for w in line.split():
                words.append(w)
                linenos.append(i)
        flat_q = " ".join(q.split())
        qwords = flat_q.split()
        hit = None
        for i in range(len(words) - len(qwords) + 1):
            if words[i:i + len(qwords)] == qwords:
                hit = i
                break
        if hit is None:
            print(f"QUOTE {rid} key={orig['key']} found=False")
            ok = False
            continue
        print(f"QUOTE {rid} key={orig['key']} found=True lines="
              f"{linenos[hit]}-{linenos[hit + len(qwords) - 1]} words={len(qwords)}")
    target = "https://www.dublincore.org/specifications/dublin-core/dcmi-namespace/"
    tkey = hashlib.sha256(target.encode()).hexdigest()[:24]
    r = subprocess.run(["git", "-C", a.repo, "ls-tree", "-r", "--name-only",
                        a.landing, "corpus/captures/"], capture_output=True, text=True)
    present = [p for p in r.stdout.splitlines() if tkey in p]
    print(f"S217_REDIRECT_TARGET={target} key={tkey} committed_captures={present}")
    print(f"CAPTURE_INTEGRITY={'PASS' if ok else 'FAIL'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
