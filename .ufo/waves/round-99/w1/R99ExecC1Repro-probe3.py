#!/usr/bin/env python3
"""Probe why rev-outside-captures got rc=2 and whether full-width passed via other marker.
Also test: (1) full-width ONLY, no other marker text. (2) >200-word challenge exact 250. (3) unreach form."""
import hashlib, os, shutil, subprocess, sys
S = "/fast/scratch/hyaku/chousa-r99/R99ExecC1Repro"
LANE = os.path.join(S, "repo")
TOOL = os.path.join(LANE, "tools/gate-records.py")

def sha(b): return hashlib.sha256(b).hexdigest()
def key(url): return sha(url.encode())[:24]
def record(sid, url, capbytes, quote):
    return (f'GATE-RECORD {sid} url={url} fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/{key(url)}.txt '
            f'capture_sha256={sha(capbytes)} words={len(quote.split())} quote="{quote}"')
def run(root, rec, work, name):
    f = os.path.join(work, f"rec-{name}.md")
    os.makedirs(work, exist_ok=True)
    with open(f, "w", encoding="utf-8") as fh: fh.write("# fixture\n\n" + rec + "\n")
    p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--root", root, f], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

work = os.path.join(S, "probe3work")
if os.path.isdir(work): shutil.rmtree(work)
os.makedirs(work)
labroot = os.path.join(work, "lab")
os.makedirs(os.path.join(labroot, "corpus", "captures"))
os.makedirs(os.path.join(labroot, "corpus", "evidence", "round57"))
shutil.copy(os.path.join(LANE, "corpus", "SOURCES.md"), os.path.join(labroot, "corpus", "SOURCES.md"))
shutil.copy(os.path.join(LANE, "corpus", "evidence", "round57", "refetch.tsv"),
            os.path.join(labroot, "corpus", "evidence", "round57", "refetch.tsv"))
n = [900]
def add(url, capbytes):
    n[0] += 1
    sid = f"S{n[0]}"; k = key(url)
    with open(os.path.join(labroot, "corpus", "captures", k + ".txt"), "wb") as fh: fh.write(capbytes)
    with open(os.path.join(labroot, "corpus", "SOURCES.md"), "a", encoding="utf-8") as fh:
        fh.write(f"| {sid} | fixture — {url} | docs | A | s | a | t | mined | 2026-11-09 | on-release | - |\n")
    with open(os.path.join(labroot, "corpus", "evidence", "round57", "refetch.tsv"), "a") as fh:
        fh.write("\t".join([sid, url, k, "1", "2026-11-09T04:00:33Z", "0", "200", "-", sha(capbytes)]) + "\n")
    q = " ".join(capbytes.decode("utf-8", errors="replace").split()[:5])
    return record(sid, url, capbytes, q)

fp = os.path.join(work, "fp")
# full-width ONLY, no ascii markers anywhere
fw_only = "Ｊｕｓｔ　ａ　ｍｏｍｅｎｔ．．．\nページの安全を確認しています\n"  # full-width NFKC-only text, no ascii marker
t = fw_only.encode()
rec = add("https://fixture.invalid/fwonly", t)
rc, out, err = run(labroot, rec, fp, "fwonly")
print(f"fw-only: rc={rc} out={out.strip()!r} err={err.strip()!r}")

# >200 words challenge with marker (limit a)
big = "Just a moment...\n" + ("word " * 250)
b = big.encode()
rec = add("https://fixture.invalid/big250", b)
rc, out, err = run(labroot, rec, fp, "big250")
print(f"big-250-words: rc={rc} out={out.strip()!r} (expect ADMIT per limit a)")

# rev outside captures with proper registry setup: need SOURCES.md + refetch.tsv present in revwork root
revwork = os.path.join(work, "revlab")
os.makedirs(revwork, exist_ok=True)
os.makedirs(os.path.join(revwork, "corpus", "evidence", "round57"), exist_ok=True)
shutil.copy(os.path.join(LANE, "corpus", "SOURCES.md"), os.path.join(revwork, "corpus", "SOURCES.md"))
# add a row for S901 if missing? S901 likely exists in lane SOURCES.md already (fixture ids S901+ already in labroot copy, not lane). Use an existing lane SID.
# find existing SID from lane registry
import re
reg = open(os.path.join(LANE, "corpus", "SOURCES.md")).read()
sid = re.search(r"^\|\s*(S[0-9]+)\s*\|", reg, re.M).group(1)
print("using existing sid", sid)
shutil.copy(os.path.join(LANE, "corpus", "evidence", "round57", "refetch.tsv"),
            os.path.join(revwork, "corpus", "evidence", "round57", "refetch.tsv"))
with open(os.path.join(revwork, "evil.md"), "w") as fh:
    fh.write("Just a moment...\nEnable JavaScript and cookies to continue\nwww.example.org needs to review the security of your connection.\n")
subprocess.run(["git", "-C", revwork, "init", "-q"], check=True)
assert subprocess.run(["git", "-C", revwork, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip() == revwork
subprocess.run(["git", "-C", revwork, "add", "evil.md"], check=True)
subprocess.run(["git", "-C", revwork, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "x"], check=True)
rev = subprocess.run(["git", "-C", revwork, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
rec = f"GATE-RECORD {sid} rev={rev} path=evil.md line=1 words=3 quote=Just a moment..."
rc, out, err = run(revwork, rec, fp, "rev-outside2")
print(f"rev-outside-captures: rc={rc} out={out.strip()!r} err={err.strip()!r} (expect OK per limit d)")
