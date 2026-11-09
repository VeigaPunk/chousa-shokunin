#!/usr/bin/env python3
"""challenge-controls-r99 — round-99 C1 (operability) controls for the CHALLENGE check of `tools/gate-records.py`.

Runs a candidate gate-records tool (default: LANE/tools/gate-records.py) through its public CLI
(`python3 -B TOOL verify --root ROOT FILE`) and scores it. Reads lane files and `git show BASE:<path>`; writes only
under --work; never fetches. Legs:

  NEG       seven url/admit records whose capture is a challenge page, each verified alone in a scratch lane (a copy
            of the lane's `corpus/SOURCES.md` and `corpus/evidence/round57/refetch.tsv` plus one registry row, one
            refetch row and one capture per fixture, keyed as capture-fetch.py keys them): n1 S230's committed
            reCAPTCHA capture, n2 S229's committed cookie-wall capture, n3 S234's committed "Client Challenge"
            capture, n4-n7 written here (a Cloudflare "Just a moment..." page, a "Verify you are human" page, an
            "Attention Required!" page, and n1's text upper-cased with its spacing doubled). Each must print
            `FAIL CHALLENGE` (CHALLENGE the only code) and exit 1.
  POS       four records that must print `OK` and exit 0: p1 a quote from S233's committed capture (8,455 words),
            p2 a quote from S236's committed capture (JSON), p3 a 300-plus-word article written here that mentions
            "reCAPTCHA" and "Just a moment" in prose, p4 a 28-word page with no marker (F2: "30-word" was wrong,
            `R99ReviewerC1` F1).
  PROD      the production path, verified with `--root LANE` itself (the lane's own registry, refetch rows and git
            objects): two url/admit records quoting S230's and S234's committed captures, and two rev records
            quoting S230's and S229's capture blobs at BASE (the first line of three or more words); each must
            FAIL CHALLENGE, exit 1.
  HARM      every `corpus/knowledge/*.md` and `corpus/lessons/*.md` file that carries a line starting
            `GATE-RECORD`: the candidate's stdout and exit code equal the BASE tool's, file by file.
  ORACLES   five stand-ins, each the candidate with one change, must each make the battery FAIL: o1 refuse every
            capture of at most 200 words (no marker), o2 refuse on a marker at any length, o3 (url/admit call) refuse
            only the sha256 of the three committed challenge capture texts S230, S229/S021/S022/S032 (one text) and
            S234, o4 (url/admit call) act only when ROOT has no `.git` (passes the scratch legs, fails PROD), o5
            (url/admit call) act only when ROOT has a `.git` (passes PROD, fails the scratch legs). o3-o5 patch the
            url/admit call site only; the rev-branch CHALLENGE call stays unconditional in all three (F2 wording,
            `R99ReviewerC1` F2), so they refuse a rev record on a challenge blob regardless of their stated gate.
  BASE      informational: how many NEG records the BASE tool admits (`BASE_NEG_ADMITTED=k/7`).

Usage: python3 -B corpus/evidence/round99/challenge-controls-r99.py --root LANE --work DIR [--tool PATH] [--no-oracles]
Prints CASE lines, one tally line and `CHALLENGE_CONTROLS_R99=PASS|FAIL`. Exit 0 PASS, 1 FAIL, 2 setup.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

BASE = "47ed34fa785288837f84cde9db15c41300854a78"
TOOL = "tools/gate-records.py"
CAP = {
    "S230": ("https://www.ncbi.nlm.nih.gov/books/NBK98350/", "b5b8d050eea0c638e95ba674"),
    "S229": ("https://pubmed.ncbi.nlm.nih.gov/27005575/", "0954149536aaad411000e1fb"),
    "S234": ("https://researchintegrityjournal.biomedcentral.com/articles/10.1186/s41073-025-00173-z",
             "b90988847e704a08aabc8321"),
    "S233": ("https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727", "4b70901ad80c513f0c2f750c"),
    "S236": ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:26528420%20AND%20SRC:MED"
             "&resultType=core&format=json", "405a0054e1f6dbd1854a3618"),
}
KNOWN_SHA = (
    "4f25f0b14fb2450c633eefc0bfc0b09db390dab39f51e357866703da5c187802",
    "7070b59c3434b67711f6a6ad723834ee1fce7a82230ac6970c1b12844c042a00",
)
CF = ("Just a moment...\n\n Enable JavaScript and cookies to continue\n www.example.org needs to review the security of "
      "your connection before proceeding.\n Ray ID: 8f2a1b3c4d5e6f70\n Performance & security by Cloudflare\n")
TURNSTILE = ("www.example.net\n Verify you are human by completing the action below.\n www.example.net needs to review "
             "the security of your connection before proceeding.\n")
ATTN = ("Attention Required! | Cloudflare\n Sorry, you have been blocked\n You are unable to access example.com\n "
        "Why have I been blocked? This website is using a security service to protect itself from online attacks.\n")
ARTICLE = (
    "How sites tell people from programs. A CAPTCHA asks the visitor to do something a script finds hard. "
    "The best known service is reCAPTCHA, which began by asking people to type distorted words and later moved to "
    "scoring behaviour in the background. Many readers have met an interstitial that says Just a moment while a "
    "content delivery network inspects the request. "
) * 6 + "This paragraph closes an ordinary article of well over two hundred words about challenge pages."
SHORT = ("Release notes. Version 2.1 fixes the date parser, adds a strict mode to the verifier, and drops support for "
         "the old configuration file. Upgrade by replacing the binary.")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def key(url):
    return sha(url.encode())[:24]


def record(sid, url, capbytes, quote, tier="A", ts="2026-11-09T04:00:33Z"):
    return (f'GATE-RECORD {sid} url={url} fetched={ts} tier={tier} decision=admit capture=corpus/captures/{key(url)}.txt '
            f'capture_sha256={sha(capbytes)} words={len(quote.split())} quote="{quote}"')


def first_words(b, n=4):
    """A quote of the first N whitespace tokens of the capture text (always located)."""
    return " ".join(b.decode("utf-8", errors="replace").split()[:n])


class Lab:
    """A scratch lane: the lane's registry and refetch log plus fixtures."""

    def __init__(self, lane, root):
        self.root = root
        os.makedirs(os.path.join(root, "corpus", "captures"))
        os.makedirs(os.path.join(root, "corpus", "evidence", "round57"))
        shutil.copy(os.path.join(lane, "corpus", "SOURCES.md"), os.path.join(root, "corpus", "SOURCES.md"))
        shutil.copy(os.path.join(lane, "corpus", "evidence", "round57", "refetch.tsv"),
                    os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv"))
        self.n = 900

    def add(self, url, capbytes, quote, ts="2026-11-09T04:00:33Z"):
        self.n += 1
        sid = f"S{self.n}"
        k = key(url)
        with open(os.path.join(self.root, "corpus", "captures", k + ".txt"), "wb") as fh:
            fh.write(capbytes)
        with open(os.path.join(self.root, "corpus", "SOURCES.md"), "a", encoding="utf-8") as fh:
            fh.write(f"| {sid} | fixture — {url} | docs | A | s | a | t | mined | 2026-11-09 | on-release | - |\n")
        with open(os.path.join(self.root, "corpus", "evidence", "round57", "refetch.tsv"), "a") as fh:
            fh.write("\t".join([sid, url, k, "1", ts, "0", "200", "-", sha(capbytes)]) + "\n")
        return record(sid, url, capbytes, quote, ts=ts)


def run(tool, root, rec, work, name):
    f = os.path.join(work, f"rec-{name}.md")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write("# fixture\n\n" + rec + "\n")
    p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", root, f], capture_output=True, text=True)
    return p.returncode, p.stdout


def verdict(out):
    m = re.search(r"^GATE_RECORD \S+ S[0-9]+ (OK|FAIL (\S+))$", out, re.M)
    return None if not m else ("OK" if m.group(1) == "OK" else m.group(2))


def score(lane, tool, work, base_tool):
    """Run every leg against TOOL; return (tallies dict, ok bool, case lines)."""
    lines, t = [], {}
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)
    lab = Lab(lane, os.path.join(work, "lab"))
    cap = {s: open(os.path.join(lane, "corpus", "captures", k + ".txt"), "rb").read() for s, (_, k) in CAP.items()}
    s230_up = re.sub(r"\s+", "  ", cap["S230"].decode().upper()).encode()
    neg = [("n1", "https://fixture.invalid/n1", cap["S230"]), ("n2", "https://fixture.invalid/n2", cap["S229"]),
           ("n3", "https://fixture.invalid/n3", cap["S234"]), ("n4", "https://fixture.invalid/n4", CF.encode()),
           ("n5", "https://fixture.invalid/n5", TURNSTILE.encode()), ("n6", "https://fixture.invalid/n6", ATTN.encode()),
           ("n7", "https://fixture.invalid/n7", s230_up)]
    pos = [("p1", "https://fixture.invalid/p1", cap["S233"], "Previous reviews estimated that approximately 20 to 25%"),
           ("p2", "https://fixture.invalid/p2", cap["S236"], "Indirect references accounted for less than one sixth"),
           ("p3", "https://fixture.invalid/p3", ARTICLE.encode(), None),
           ("p4", "https://fixture.invalid/p4", SHORT.encode(), None)]
    recs = {}
    for name, url, b in neg:
        recs[name] = lab.add(url, b, first_words(b))
    for name, url, b, q in pos:
        recs[name] = lab.add(url, b, q or first_words(b, 6))
    negok = posok = baseadm = 0
    for name, _, _ in neg:
        rc, out = run(tool, lab.root, recs[name], work, name)
        v = verdict(out)
        good = rc == 1 and v == "CHALLENGE"
        negok += good
        lines.append(f"CASE NEG {name} rc={rc} verdict={v} {'PASS' if good else 'FAIL'}")
        if base_tool:
            brc, bout = run(base_tool, lab.root, recs[name], work, name + "-base")
            baseadm += brc == 0 and verdict(bout) == "OK"
    for name, _, _, _ in pos:
        rc, out = run(tool, lab.root, recs[name], work, name)
        v = verdict(out)
        good = rc == 0 and v == "OK"
        posok += good
        lines.append(f"CASE POS {name} rc={rc} verdict={v} {'PASS' if good else 'FAIL'}")
    prodok = 0
    for sid in ("S230", "S234"):
        url, k = CAP[sid]
        rec = record(sid, url, cap[sid], first_words(cap[sid]), ts=prod_ts(lane, sid, url))
        rc, out = run(tool, lane, rec, work, "prod-" + sid)
        v = verdict(out)
        good = rc == 1 and v == "CHALLENGE"
        prodok += good
        lines.append(f"CASE PROD {sid} rc={rc} verdict={v} {'PASS' if good else 'FAIL'}")
    for sid in ("S230", "S229"):
        path = f"corpus/captures/{CAP[sid][1]}.txt"
        blob = subprocess.run(["git", "-C", lane, "show", f"{BASE}:{path}"], capture_output=True, text=True).stdout
        n, q = next((i + 1, " ".join(ln.split()[:3])) for i, ln in enumerate(blob.split("\n")) if len(ln.split()) >= 3)
        rec = f"GATE-RECORD {sid} rev={BASE} path={path} line={n} words={len(q.split())} quote={q}"
        rc, out = run(tool, lane, rec, work, "prodrev-" + sid)
        v = verdict(out)
        good = rc == 1 and v == "CHALLENGE"
        prodok += good
        lines.append(f"CASE PROD rev-{sid} rc={rc} verdict={v} {'PASS' if good else 'FAIL'}")
    harm = harm_files(lane)
    same = 0
    if base_tool:
        for f in harm:
            a = subprocess.run([sys.executable, "-B", tool, "verify", "--root", lane, f], capture_output=True, text=True,
                               cwd=lane)
            b = subprocess.run([sys.executable, "-B", base_tool, "verify", "--root", lane, f], capture_output=True,
                               text=True, cwd=lane)
            eq = (a.returncode, a.stdout) == (b.returncode, b.stdout)
            same += eq
            if not eq:
                lines.append(f"CASE HARM {f} DIFF")
    t.update(NEG_REFUSED=(negok, len(neg)), POS_ADMITTED=(posok, len(pos)), PROD_REFUSED=(prodok, 4),
             HARM_SAME=(same, len(harm)), BASE_NEG_ADMITTED=(baseadm, len(neg)))
    ok = negok == len(neg) and posok == len(pos) and prodok == 4 and (not base_tool or same == len(harm))
    return t, ok, lines


def prod_ts(lane, sid, url):
    for ln in open(os.path.join(lane, "corpus", "evidence", "round57", "refetch.tsv")):
        f = ln.rstrip("\n").split("\t")
        if len(f) == 9 and f[0] == sid and f[1] == url and f[6] == "200":
            return f[4]
    return "2026-11-09T00:00:00Z"


def harm_files(lane):
    out = []
    for d in ("corpus/knowledge", "corpus/lessons"):
        for n in sorted(os.listdir(os.path.join(lane, d))):
            p = os.path.join(d, n)
            if n.endswith(".md") and any(re.match(r"^\s*GATE-RECORD\s", ln)
                                         for ln in open(os.path.join(lane, p), encoding="utf-8", errors="replace")):
                out.append(p)
    return out


ORACLES = {
    "o1-short-only": ("return len(t.split()) <= CHALLENGE_MAX_WORDS and any(m in t for m in CHALLENGE_MARKERS)",
                      "return len(t.split()) <= CHALLENGE_MAX_WORDS"),
    "o2-marker-only": ("return len(t.split()) <= CHALLENGE_MAX_WORDS and any(m in t for m in CHALLENGE_MARKERS)",
                       "return any(m in t for m in CHALLENGE_MARKERS)"),
    "o3-known-bytes": ("            if is_challenge(text):",
                       "            if sha256_file(cap) in " + repr(KNOWN_SHA + (
                           "c42ccd00e8305111f9269436ae4dd8a66cba6188df6a5a44e5478ce00b4e94f8",)) + ":"),
    "o4-scratch-only": ("            if is_challenge(text):",
                        "            if is_challenge(text) and not os.path.isdir(os.path.join(root, '.git')):"),
    "o5-lane-only": ("            if is_challenge(text):",
                     "            if is_challenge(text) and os.path.exists(os.path.join(root, '.git')):"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--tool")
    ap.add_argument("--no-oracles", action="store_true")
    a = ap.parse_args()
    lane = os.path.abspath(a.root)
    work = os.path.abspath(a.work)
    tool = os.path.abspath(a.tool) if a.tool else os.path.join(lane, TOOL)
    if not os.path.isfile(tool) or not os.path.isdir(os.path.join(lane, "corpus", "captures")):
        print("CHALLENGE_CONTROLS_SETUP missing tool or lane", file=sys.stderr)
        return 2
    os.makedirs(work, exist_ok=True)
    base_tool = os.path.join(work, "base-gate-records.py")
    b = subprocess.run(["git", "-C", lane, "show", f"{BASE}:{TOOL}"], capture_output=True)
    if b.returncode != 0:
        print("CHALLENGE_CONTROLS_SETUP cannot read base tool", file=sys.stderr)
        return 2
    with open(base_tool, "wb") as fh:
        fh.write(b.stdout)
    t, ok, lines = score(lane, tool, os.path.join(work, "cand"), base_tool)
    for ln in lines:
        print(ln)
    rejected = n_or = 0
    if not a.no_oracles:
        src = open(tool, encoding="utf-8").read()
        for name, (old, new) in ORACLES.items():
            n_or += 1
            if src.count(old) != 1:
                print(f"CASE ORACLE {name} SITE-MISSING FAIL")
                continue
            p = os.path.join(work, f"oracle-{name}.py")
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(src.replace(old, new))
            _, ook, _ = score(lane, p, os.path.join(work, "o-" + name), None)
            rejected += not ook
            print(f"CASE ORACLE {name} battery={'PASS' if ook else 'FAIL'} {'PASS' if not ook else 'FAIL'}")
    t["ORACLES_REJECTED"] = (rejected, n_or)
    print(" ".join(f"{k}={v[0]}/{v[1]}" for k, v in t.items()))
    good = ok and (a.no_oracles or rejected == n_or)
    print(f"CHALLENGE_CONTROLS_R99={'PASS' if good else 'FAIL'}")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
