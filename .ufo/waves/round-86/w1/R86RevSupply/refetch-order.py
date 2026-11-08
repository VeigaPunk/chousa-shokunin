#!/usr/bin/env python3
"""Egress-order and fetch-scope check for the round's refetch rows.

Usage: python3 -B refetch-order.py --repo REPO --base BASE_REV --landing LAND_REV --egress EGRESS_REV
Reads committed bytes only. Prints, for every refetch.tsv row added between
base and landing: id, url, fetched_utc, seconds after the egress commit's
committer timestamp. Then compares the added URLs with the intended-targets
table of corpus/evidence/round86/egress-approval.md at the egress revision.
Exit 0 when the egress commit precedes every added row and the URL sets match.
"""
import argparse
import datetime as dt
import re
import subprocess
import sys


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"git {' '.join(args)} failed: {r.stderr}")
    return r.stdout


def show(repo, rev, path):
    return git(repo, "show", f"{rev}:{path}")


def parse_tsv(text):
    lines = text.splitlines()
    head = lines[0].split("\t")
    return head, [dict(zip(head, l.split("\t"))) for l in lines[1:] if l]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--base", required=True)
    ap.add_argument("--landing", required=True)
    ap.add_argument("--egress", required=True)
    a = ap.parse_args()
    egress_commit = git(a.repo, "rev-parse", a.egress + "^{commit}").strip()
    committer = git(a.repo, "show", "-s", "--format=%cI", egress_commit).strip()
    author = git(a.repo, "show", "-s", "--format=%aI", egress_commit).strip()
    commit_epoch = dt.datetime.fromisoformat(committer).timestamp()
    print(f"EGRESS_COMMIT={egress_commit}")
    print(f"EGRESS_AUTHOR={author} EGRESS_COMMITTER={committer}")
    print(f"EGRESS_COMMITTER_EPOCH={commit_epoch:.0f}")
    _, old = parse_tsv(show(a.repo, a.base, "corpus/evidence/round57/refetch.tsv"))
    _, new = parse_tsv(show(a.repo, a.landing, "corpus/evidence/round57/refetch.tsv"))
    oldset = {(r["id"], r["url"], r["attempt"], r["fetched_utc"]) for r in old}
    added = [r for r in new if (r["id"], r["url"], r["attempt"], r["fetched_utc"]) not in oldset]
    print(f"ROWS base={len(old)} landing={len(new)} added={len(added)}")
    print("id\turl\tattempt\thttp_code\tfetched_utc\tseconds_after_egress_commit")
    ok = True
    for r in added:
        t = dt.datetime.strptime(r["fetched_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=dt.timezone.utc).timestamp()
        delta = t - commit_epoch
        print(f"{r['id']}\t{r['url']}\t{r['attempt']}\t{r['http_code']}\t{r['fetched_utc']}\t{delta:.0f}")
        ok = ok and delta > 0
    approval = show(a.repo, a.egress, "corpus/evidence/round86/egress-approval.md")
    intended = set(re.findall(r"^\| (S\d+)(?: \([^)]*\))? \| (https?://\S+) \|", approval, re.M))
    # the table's second column is the URL; first column may carry a note
    urls = {u for _, u in intended}
    ids = {i for i, _ in intended}
    added_urls = {r["url"] for r in added}
    print(f"INTENDED={len(intended)} ids={sorted(ids)}")
    print(f"ADDED_URLS_NOT_INTENDED={sorted(added_urls - urls)}")
    print(f"INTENDED_URLS_NOT_FETCHED={sorted(urls - added_urls)}")
    all_ok = ok and added_urls <= urls and urls <= added_urls
    print(f"EGRESS_BEFORE_ALL_ADDED_FETCHES={'1/1' if ok else '0/1'} "
          f"SCOPE_MATCH={len(added_urls & urls)}/{len(urls)}")
    print(f"REFETCH_ORDER={'PASS' if all_ok else 'FAIL'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
