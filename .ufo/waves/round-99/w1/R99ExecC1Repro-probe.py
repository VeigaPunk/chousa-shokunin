#!/usr/bin/env python3
import hashlib, os, shutil, subprocess, sys

S = "/fast/scratch/hyaku/chousa-r99/R99ExecC1Repro"
LANE = os.path.join(S, "repo")
TOOL = os.path.join(LANE, "tools/gate-records.py")

def sha(b): return hashlib.sha256(b).hexdigest()
def key(url): return sha(url.encode())[:24]
def record(sid, url, capbytes, quote, tier="A", ts="2026-11-09T04:00:33Z"):
    return (f'GATE-RECORD {sid} url={url} fetched={ts} tier={tier} decision=admit capture=corpus/captures/{key(url)}.txt '
            f'capture_sha256={sha(capbytes)} words={len(quote.split())} quote="{quote}"')
def first_words(b, n=5):
    return " ".join(b.decode("utf-8", errors="replace").split()[:n])

class Lab:
    def __init__(self, lane, root):
        self.root = root
        os.makedirs(os.path.join(root, "corpus", "captures"))
        os.makedirs(os.path.join(root, "corpus", "evidence", "round57"))
        shutil.copy(os.path.join(lane, "corpus", "SOURCES.md"), os.path.join(root, "corpus", "SOURCES.md"))
        shutil.copy(os.path.join(lane, "corpus", "evidence", "round57", "refetch.tsv"),
                    os.path.join(root, "corpus", "evidence", "round57", "refetch.tsv"))
        self.n = 900
    def add(self, url, capbytes, quote):
        self.n += 1
        sid = f"S{self.n}"
        k = key(url)
        with open(os.path.join(self.root, "corpus", "captures", k + ".txt"), "wb") as fh:
            fh.write(capbytes)
        with open(os.path.join(self.root, "corpus", "SOURCES.md"), "a", encoding="utf-8") as fh:
            fh.write(f"| {sid} | fixture — {url} | docs | A | s | a | t | mined | 2026-11-09 | on-release | - |\n")
        with open(os.path.join(self.root, "corpus", "evidence", "round57", "refetch.tsv"), "a") as fh:
            fh.write("\t".join([sid, url, k, "1", "2026-11-09T04:00:33Z", "0", "200", "-", sha(capbytes)]) + "\n")
        return record(sid, url, capbytes, quote)

def run(root, rec, work, name):
    f = os.path.join(work, f"rec-{name}.md")
    os.makedirs(work, exist_ok=True)
    with open(f, "w", encoding="utf-8") as fh:
        fh.write("# fixture\n\n" + rec + "\n")
    p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--root", root, f], capture_output=True, text=True)
    return p.returncode, p.stdout.strip().replace("\n", " | ")

def norm_words(t): return len(" ".join(t.split()).split())

FOOTER = ("This footer text is long and boring and appears on every page of the site regardless of whether "
          "the page is a normal article or a block page. It describes the company, its offices, its hiring "
          "policy, its privacy contact, its status page, its terms of service, its cookie preferences, its "
          "accessibility statement, its region list, its archive links, and a great deal of other ordinary "
          "boilerplate that fills most of the page. ") * 4  # ~ 4*~60 = >200 words total with challenge text? -> need measure

FIXTURES = [
    ("akamai", "https://fixture.invalid/akamai",
     "Access Denied\nYou don't have permission to access \"http://example.com/\" on this server.\nReference #18.9a3d2c1e.1770000000.1a2b3c4d\n"),
    ("perimeterx", "https://fixture.invalid/px",
     "Press & Hold to confirm you are a human\nHold the button for three seconds to continue.\nAn automated test detected unusual traffic from your network.\n"),
    ("datadome", "https://fixture.invalid/datadome",
     "DataDome\nPardon Our Interruption\nWe noticed unusual activity from your network. Please verify you are not a bot to continue.\n"),
    ("hcaptcha", "https://fixture.invalid/hcaptcha",
     "Please complete the security check\nSolve the CAPTCHA challenge to continue. If you are having trouble, please disable your ad blocker.\n"),
    ("sucuri", "https://fixture.invalid/sucuri",
     "Website Firewall\nAccess Denied - Sucuri Website Firewall\nYour IP 203.0.113.7 has been blocked. If you believe this is a mistake, contact support.\n"),
    ("awswaf", "https://fixture.invalid/awswaf",
     "Request blocked by AWS WAF\nWe can't connect to the server for this app or website at this time. There might be too much traffic or a configuration error.\n"),
    ("cf-long-footer", "https://fixture.invalid/cf-long",
     "Access Denied\nJust a moment, checking your browser before you access the site.\n" + FOOTER),
    ("other-lang", "https://fixture.invalid/de",
     "Sicherheitsprüfung läuft\nBitte bestätigen Sie, dass Sie ein Mensch sind. Aktivieren Sie JavaScript und Cookies um fortzufahren.\n"),
]

DOCS = [
    ("changelog", "https://fixture.invalid/d1",
     "Changelog 2.4.1 — fix: recaptcha widget no longer blocks screen readers; see issue #412.\nImprove error messages for missing configuration. Bump minor version.\n"),
    ("incident", "https://fixture.invalid/d2",
     "Incident 2026-11-08: Cloudflare attention required header returned 503 for 11 minutes. Monitoring restored. Postmortem linked below.\nAction: add alert on 5xx rate.\n"),
    ("ticket", "https://fixture.invalid/d3",
     "Support ticket: user asks are you a robot? Answer: our forms now use a privacy-preserving challenge. No personal data stored.\nPlease close after reply sent.\n"),
    ("release-note", "https://fixture.invalid/d4",
     "Release 3.0 notes. Replaced custom bot check with standard vendor checks. Migration guide included. Rollback supported for thirty days.\nContact release team for questions.\n"),
]

def main():
    work = os.path.join(S, "probework")
    if os.path.isdir(work): shutil.rmtree(work)
    os.makedirs(work)
    lab = Lab(LANE, os.path.join(work, "lab"))
    os.makedirs(os.path.join(work, "fp"), exist_ok=True)
    print("=== (b) 8 challenge fixtures ===")
    for name, url, text in FIXTURES:
        b = text.encode()
        rec = lab.add(url, b, first_words(b))
        rc, out = run(lab.root, rec, os.path.join(work, "fp"), name)
        outl = out.replace("  ", " ")
        verdict = "ADMITTED" if rc == 0 else ("REFUSED" if "CHALLENGE" in out else f"REFUSED-OTHER(rc={rc})")
        print(f"{verdict}\t{name}\twords={norm_words(text)}\trc={rc}\t{outl}")
    print("=== (c) 4 legit short docs with markers ===")
    for name, url, text in DOCS:
        b = text.encode()
        rec = lab.add(url, b, first_words(b, 6))
        rc, out = run(lab.root, rec, os.path.join(work, "fp"), "doc-"+name)
        verdict = "ADMITTED" if rc == 0 else ("REFUSED-CHALLENGE" if "CHALLENGE" in out else f"REFUSED-OTHER(rc={rc})")
        print(f"{verdict}\t{name}\twords={norm_words(text)}\trc={rc}\t{out}\n  text={text!r}")

if __name__ == "__main__":
    main()
