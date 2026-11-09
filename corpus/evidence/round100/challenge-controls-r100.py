#!/usr/bin/env python3
"""challenge-controls-r100 — round-100 C1 (operability) controls for the CHALLENGE check of `tools/gate-records.py`.

Runs a candidate gate-records tool (default: LANE/tools/gate-records.py) through its public CLI
(`python3 -B TOOL verify --root ROOT [--repo GITDIR] FILE`) and scores it. Reads lane files and `git show BASE:<path>`;
writes only under --work (a scratch lab lane and one fixture git repository created there, committed with a fixture
identity after asserting its top level); never fetches. Legs (every NEG-like leg needs `FAIL CHALLENGE` with CHALLENGE
the only code and exit 1; every POS-like leg needs `OK` and exit 0):

  NEG     n1-n7, round 99's seven url/admit challenge records (S230, S229, S234 captures; Cloudflare, Turnstile,
          "Attention Required!" pages; S230 upper-cased with doubled spacing), each verified alone in the lab.
  MARK    m01-m11, one url/admit record per CHALLENGE_MARKERS entry: a short page carrying that marker and no other
          (kills a dropped marker, round-99 `R99MutantsC1` survivors m02-m11).
  BOUND   url/admit pages of exactly 199, 200 and 201 words carrying one marker: 199 and 200 refused, 201 admitted
          (kills `<=`->`<`, 200->199/201).
  NORM    k1 a marker split by a newline and a tab ("Just\\n a\\tmoment"), k2 S234's marker with a curly apostrophe
          ("couldn\u2019t"): refused (kills `norm` dropped inside is_challenge).
  POS     p1-p4, round 99's four admitted records (S233, S236 captures, a 300-plus-word article about CAPTCHAs, a
          28-word marker-less page).
  REV     rev records verified with `--root LAB --repo FX` against a fixture commit in FX holding S230's committed
          .txt and .raw capture bytes at their lane keys, S234's .txt, S233's .txt, a new written challenge page C
          (.txt and a 300-plus-token .raw) at a fixture key, a byte copy of S230's .txt at corpus/evidence/copy-s230.txt
          and of C's .txt at notes/c-copy.txt, D's .txt (r11), and a short non-capture note at corpus/evidence/captures-note.txt that
          mentions reCAPTCHA. Refused: r1 `./corpus/captures/<S230>.txt`, r2 `./corpus//captures/<S230>.txt`,
          r3 `./corpus/./captures/<S230>.txt`, r4 `./notes/../corpus/captures/<S230>.txt`, r5
          `corpus/captures/<S230>.raw`, r6 `./corpus/captures/<C>.raw`, r7 `corpus/evidence/copy-s230.txt`, r8
          `notes/c-copy.txt`, r9 `corpus/captures/<S234>.txt` quoting a line with no marker (the whole blob is
          judged), r10 `corpus/captures/<S230>.txt` (round-99 behaviour), r11 a capture D at a fixture key whose
          only marker is split by a newline and a tab (the rev text is not pre-normalized, so this is the leg that
          shows `norm` inside is_challenge live). Admitted: q1 `./corpus/captures/<S233>.txt`,
          q2 `corpus/captures/<S233>.txt`, q3 `corpus/evidence/captures-note.txt` (not a capture; a marker in a
          short non-capture blob is not CHALLENGE). Each record's quote is the first 3-word line of the blob git
          resolves for its own path (r9: the first such line that carries no marker).
  PROD    the production path with `--root LANE` (the lane's registry, refetch rows and git objects): round 99's
          url/admit S230 and S234 and rev S230 and S229 records, plus rev `./corpus/captures/<S230>.txt` and rev
          `corpus/captures/<S230>.raw` at BASE; all six refused.
  HARM    every `corpus/knowledge/*.md` and `corpus/lessons/*.md` file carrying a line that starts `GATE-RECORD`: the
          candidate's stdout and exit code equal the BASE tool's, file by file.
  ORACLES twelve stand-ins, each the candidate with one change, must each make the battery FAIL: o1 spelling-keyed
          (the guard is the normalized path, no object-id identity), o2 txt-only (`.raw` entries ignored), o3
          no-sibling (a .raw judged by its own bytes), o4 every-rev (every rev blob judged), o5 refuse every `./`
          path regardless of content, o6 known-bytes (refuse a rev only when the blob's sha256 is one of the three
          committed challenge texts), o7 act on rev only when GITDIR is ROOT, o8 act on rev only when GITDIR is not
          ROOT, o9 marker "ddos protection" dropped, o10 `<=` -> `<`, o11 200 -> 201, o12 `norm` dropped inside
          is_challenge.
  BASE    informational: how many REV refusal records the BASE tool admits (`BASE_REV_ADMITTED=k/11`).

Usage: python3 -B corpus/evidence/round100/challenge-controls-r100.py --root LANE --work DIR [--tool PATH] [--no-oracles]
Prints CASE lines, one tally line and `CHALLENGE_CONTROLS_R100=PASS|FAIL`. Exit 0 PASS, 1 FAIL, 2 setup (missing tool,
lane, base revision, a lane capture the legs read, or a fixture git step) — `CHALLENGE_CONTROLS_SETUP <reason>` on stderr.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys

BASE = "929c784c63a1fd17961d21742101b2b109b7b8ff"
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
MARKERS = (
    "cookies must be enabled",
    "checking your browser",
    "recaptcha",
    "client challenge",
    "a required part of this site couldn't load",
    "just a moment",
    "verify you are human",
    "enable javascript and cookies to continue",
    "attention required",
    "ddos protection",
    "are you a robot",
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
# round 100: a challenge page whose bytes no lane capture holds (a known-bytes stand-in cannot list it)
CPAGE = ("Security check in progress\n Please stand by while we are checking your browser.\n"
         " This process is automatic and takes about five seconds.\n Request reference 41c9e2 node fra-07\n")
CRAW = ("<!DOCTYPE html><html><head><title>Security check in progress</title><script>"
        + " ".join(f"var k{i} = window.navigator.userAgent + '{i}';" for i in range(120))
        + "</script></head><body><p>Please stand by while we are checking your browser.</p></body></html>\n")
NOTE = ("Fixture note. The login form shows a reCAPTCHA widget\n after three failed attempts; nothing else changes.\n")
FILLER = "lorem"


class Setup(Exception):
    pass


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


def page(words, marker="verify you are human"):
    """A page of exactly WORDS whitespace tokens carrying MARKER once and no other marker."""
    toks = marker.split()
    return (" ".join(toks + [FILLER] * (words - len(toks))) + "\n").encode()


class Lab:
    """A scratch lane: the lane's registry and refetch log plus fixtures."""

    def __init__(self, lane, root):
        self.root = root
        os.makedirs(os.path.join(root, "corpus", "captures"))
        os.makedirs(os.path.join(root, "corpus", "evidence", "round57"))
        for rel in (("corpus", "SOURCES.md"), ("corpus", "evidence", "round57", "refetch.tsv")):
            if not os.path.isfile(os.path.join(lane, *rel)):
                raise Setup(f"missing lane file {'/'.join(rel)}")
            shutil.copy(os.path.join(lane, *rel), os.path.join(root, *rel))
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


def git(fx, *args, check=True):
    p = subprocess.run(["git", "-C", fx, *args], capture_output=True)
    if check and p.returncode != 0:
        raise Setup(f"fixture git {' '.join(args[:2])} rc={p.returncode}")
    return p


def fixture_repo(work, files):
    """Create WORK/fx, commit FILES (relpath -> bytes) once with a fixture identity, return (fx, commit)."""
    fx = os.path.join(work, "fx")
    if not fx or not fx.startswith(work + os.sep):
        raise Setup("fixture path")
    os.makedirs(fx)
    git(fx, "init", "-q")
    top = git(fx, "rev-parse", "--show-toplevel").stdout.decode().strip()
    if os.path.realpath(top) != os.path.realpath(fx):
        raise Setup(f"fixture toplevel {top!r} != {fx!r}")
    for rel, b in files.items():
        p = os.path.join(fx, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as fh:
            fh.write(b)
    git(fx, "add", "-A")
    git(fx, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "fixture")
    return fx, git(fx, "rev-parse", "HEAD").stdout.decode().strip()


def rev_record(sid, repo, rev, path, skip_markers=False):
    b = git(repo, "show", f"{rev}:{path}", check=False)
    if b.returncode != 0:
        raise Setup(f"cannot resolve {path} at {rev[:8]}")
    for i, ln in enumerate(b.stdout.decode("utf-8", errors="replace").split("\n")):
        if len(ln.split()) >= 3 and not (skip_markers and any(m in " ".join(ln.lower().split()) for m in MARKERS)):
            q = " ".join(ln.split()[:3])
            return f"GATE-RECORD {sid} rev={rev} path={path} line={i + 1} words=3 quote={q}"
    raise Setup(f"no quotable line in {path}")


def run(tool, root, rec, work, name, repo=None):
    f = os.path.join(work, f"rec-{name}.md")
    with open(f, "w", encoding="utf-8") as fh:
        fh.write("# fixture\n\n" + rec + "\n")
    cmd = [sys.executable, "-B", tool, "verify", "--root", root] + (["--repo", repo] if repo else []) + [f]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout


def verdict(out):
    m = re.search(r"^GATE_RECORD \S+ S[0-9]+ (OK|FAIL (\S+))$", out, re.M)
    return None if not m else ("OK" if m.group(1) == "OK" else m.group(2))


def lane_cap(lane, k, ext="txt"):
    p = os.path.join(lane, "corpus", "captures", f"{k}.{ext}")
    if not os.path.isfile(p):
        raise Setup(f"missing lane capture {k}.{ext}")
    with open(p, "rb") as fh:
        return fh.read()


def score(lane, tool, work, base_tool):
    """Run every leg against TOOL; return (tallies dict, ok bool, case lines)."""
    lines, t = [], {}
    if os.path.isdir(work):
        shutil.rmtree(work)
    os.makedirs(work)
    lab = Lab(lane, os.path.join(work, "lab"))
    cap = {s: lane_cap(lane, k) for s, (_, k) in CAP.items()}
    s230_up = re.sub(r"\s+", "  ", cap["S230"].decode().upper()).encode()
    tallies = {}

    def leg(group, name, rc_out, want_refused, base=None):
        rc, out = rc_out
        v = verdict(out)
        good = (rc == 1 and v == "CHALLENGE") if want_refused else (rc == 0 and v == "OK")
        g = tallies.setdefault(group, [0, 0])
        g[0] += good
        g[1] += 1
        lines.append(f"CASE {group} {name} rc={rc} verdict={v} {'PASS' if good else 'FAIL'}")
        return good

    def lab_case(group, name, b, want_refused, quote=None):
        rec = lab.add(f"https://fixture.invalid/{name}", b, quote or first_words(b))
        leg(group, name, run(tool, lab.root, rec, work, name), want_refused)

    for name, b in (("n1", cap["S230"]), ("n2", cap["S229"]), ("n3", cap["S234"]), ("n4", CF.encode()),
                    ("n5", TURNSTILE.encode()), ("n6", ATTN.encode()), ("n7", s230_up)):
        lab_case("NEG", name, b, True)
    for i, m in enumerate(MARKERS, 1):
        lab_case("MARK", f"m{i:02d}", f"Site notice 4471.\n {m}.\n Reference 88213.\n".encode(), True)
    for w, refused in ((199, True), (200, True), (201, False)):
        lab_case("BOUND", f"b{w}", page(w), refused)
    lab_case("NORM", "k1", "Notice 5520.\n Just\n a\tmoment while we look.\n".encode(), True)
    lab_case("NORM", "k2", "Notice 5521.\n A required part of this site couldn\u2019t load.\n".encode(), True)
    for name, b, q in (("p1", cap["S233"], "Previous reviews estimated that approximately 20 to 25%"),
                       ("p2", cap["S236"], "Indirect references accounted for less than one sixth"),
                       ("p3", ARTICLE.encode(), None), ("p4", SHORT.encode(), None)):
        lab_case("POS", name, b, False, quote=q or first_words(b, 6))

    k230, k234, k233 = CAP["S230"][1], CAP["S234"][1], CAP["S233"][1]
    kc = key("https://fixture.invalid/cpage")
    kd = key("https://fixture.invalid/dpage")
    fx, frev = fixture_repo(work, {
        f"corpus/captures/{k230}.txt": cap["S230"], f"corpus/captures/{k230}.raw": lane_cap(lane, k230, "raw"),
        f"corpus/captures/{k234}.txt": cap["S234"], f"corpus/captures/{k233}.txt": cap["S233"],
        f"corpus/captures/{kc}.txt": CPAGE.encode(), f"corpus/captures/{kc}.raw": CRAW.encode(),
        "corpus/evidence/copy-s230.txt": cap["S230"], "notes/c-copy.txt": CPAGE.encode(),
        "corpus/evidence/captures-note.txt": NOTE.encode(),
        f"corpus/captures/{kd}.txt": "Notice 5530.\n Just\n a\tmoment while we look.\n".encode(),
    })
    rev_cases = [
        ("r1", "S230", f"./corpus/captures/{k230}.txt", True), ("r2", "S230", f"./corpus//captures/{k230}.txt", True),
        ("r3", "S230", f"./corpus/./captures/{k230}.txt", True),
        ("r4", "S230", f"./notes/../corpus/captures/{k230}.txt", True),
        ("r5", "S230", f"corpus/captures/{k230}.raw", True), ("r6", "S230", f"./corpus/captures/{kc}.raw", True),
        ("r7", "S230", "corpus/evidence/copy-s230.txt", True), ("r8", "S230", "notes/c-copy.txt", True),
        ("r9", "S234", f"corpus/captures/{k234}.txt", True), ("r10", "S230", f"corpus/captures/{k230}.txt", True),
        ("r11", "S230", f"corpus/captures/{kd}.txt", True),
        ("q1", "S233", f"./corpus/captures/{k233}.txt", False), ("q2", "S233", f"corpus/captures/{k233}.txt", False),
        ("q3", "S233", "corpus/evidence/captures-note.txt", False),
    ]
    base_adm = 0
    for name, sid, path, refused in rev_cases:
        rec = rev_record(sid, fx, frev, path, skip_markers=(name == "r9"))
        leg("REV" if refused else "REVPOS", name, run(tool, lab.root, rec, work, name, repo=fx), refused)
        if base_tool and refused:
            brc, bout = run(base_tool, lab.root, rec, work, name + "-base", repo=fx)
            base_adm += brc == 0 and verdict(bout) == "OK"

    for sid in ("S230", "S234"):
        url, k = CAP[sid]
        rec = record(sid, url, cap[sid], first_words(cap[sid]), ts=prod_ts(lane, sid, url))
        leg("PROD", sid, run(tool, lane, rec, work, "prod-" + sid), True)
    for name, sid, path in (("rev-S230", "S230", f"corpus/captures/{k230}.txt"),
                            ("rev-S229", "S229", f"corpus/captures/{CAP['S229'][1]}.txt"),
                            ("rev-dot-S230", "S230", f"./corpus/captures/{k230}.txt"),
                            ("rev-raw-S230", "S230", f"corpus/captures/{k230}.raw")):
        rec = rev_record(sid, lane, BASE, path)
        leg("PROD", name, run(tool, lane, rec, work, "prod" + name), True)

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
    order = ("NEG", "MARK", "BOUND", "NORM", "POS", "REV", "REVPOS", "PROD")
    for g in order:
        t[g] = tuple(tallies.get(g, (0, 0)))
    t["HARM_SAME"] = (same, len(harm))
    t["BASE_REV_ADMITTED"] = (base_adm, sum(1 for c in rev_cases if c[3]))
    ok = all(t[g][0] == t[g][1] and t[g][1] > 0 for g in order) and (not base_tool or same == len(harm))
    return t, ok, lines


def prod_ts(lane, sid, url):
    for ln in open(os.path.join(lane, "corpus", "evidence", "round57", "refetch.tsv")):
        f = ln.rstrip("\n").split("\t")
        if len(f) == 9 and f[0] == sid and f[1] == url and f[6] == "200":
            return f[4]
    raise Setup(f"no 200 refetch row for {sid}")


def harm_files(lane):
    out = []
    for d in ("corpus/knowledge", "corpus/lessons"):
        for n in sorted(os.listdir(os.path.join(lane, d))):
            p = os.path.join(d, n)
            if n.endswith(".md") and any(re.match(r"^\s*GATE-RECORD\s", ln)
                                         for ln in open(os.path.join(lane, p), encoding="utf-8", errors="replace")):
                out.append(p)
    return out


CALL = "            if ctext is not None and is_challenge(ctext):"
ORACLES = {
    "o1-spelling-keyed": ("    name = capture_oids(repo, rev).get(p.stdout.strip()) if p.returncode == 0 else None",
                          "    import posixpath\n    c = posixpath.normpath(path)\n"
                          "    name = c if CAPANY_RE.fullmatch(c) else None"),
    "o2-txt-only": ("if len(parts) == 3 and parts[1] == \"blob\" and CAPANY_RE.fullmatch(path):",
                    "if len(parts) == 3 and parts[1] == \"blob\" and CAP_RE.fullmatch(path):"),
    "o3-no-sibling": ("    if name.endswith(\".raw\"):", "    if False:"),
    "o4-every-rev": ("    if name is None:\n        return None\n", "    name = name or \"\"\n"),
    "o5-refuse-dot-paths": (CALL, "            if (ctext is not None and is_challenge(ctext)) or kv[\"path\"].startswith(\"./\"):"),
    "o6-known-bytes": (CALL, "            if hashlib.sha256(blob).hexdigest() in ('4f25f0b14fb2450c633eefc0bfc0b09db390dab39f51e357866703da5c187802', "
                             "'7070b59c3434b67711f6a6ad723834ee1fce7a82230ac6970c1b12844c042a00', "
                             "'c42ccd00e8305111f9269436ae4dd8a66cba6188df6a5a44e5478ce00b4e94f8'):"),
    "o7-lane-repo-only": (CALL, CALL[:-1] + " and repo == root:"),
    "o8-fixture-repo-only": (CALL, CALL[:-1] + " and repo != root:"),
    "o9-drop-ddos": ("    \"ddos protection\",\n", ""),
    "o10-lt": ("return len(t.split()) <= CHALLENGE_MAX_WORDS", "return len(t.split()) < CHALLENGE_MAX_WORDS"),
    "o11-max-201": ("CHALLENGE_MAX_WORDS = 200", "CHALLENGE_MAX_WORDS = 201"),
    "o12-no-norm": ("    t = norm(text).lower()", "    t = text.lower()"),
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
    try:
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
                try:
                    _, ook, _ = score(lane, p, os.path.join(work, "o-" + name), None)
                except Setup as e:
                    print(f"CASE ORACLE {name} SETUP {e} FAIL")
                    continue
                rejected += not ook
                print(f"CASE ORACLE {name} battery={'PASS' if ook else 'FAIL'} {'PASS' if not ook else 'FAIL'}")
    except Setup as e:
        print(f"CHALLENGE_CONTROLS_SETUP {e}", file=sys.stderr)
        return 2
    t["ORACLES_REJECTED"] = (rejected, n_or)
    print(" ".join(f"{k}={v[0]}/{v[1]}" for k, v in t.items()))
    good = ok and (a.no_oracles or rejected == n_or)
    print(f"CHALLENGE_CONTROLS_R100={'PASS' if good else 'FAIL'}")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
