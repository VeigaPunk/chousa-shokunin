#!/usr/bin/env python3
"""Final probes: unreach with 2xx success (should fail REFETCH not CHALLENGE), punctuated/underscored marker evasion, QUALITY229 check, rev-cap at non-BASE rev (F blob?)."""
import hashlib, os, shutil, subprocess, sys, re
S = "/fast/scratch/hyaku/chousa-r99/R99ExecC1Repro"
LANE = os.path.join(S, "repo")
TOOL = os.path.join(LANE, "tools/gate-records.py")
def sha(b): return hashlib.sha256(b).hexdigest()
def key(url): return sha(url.encode())[:24]
def run(root, rec, work, name):
    f = os.path.join(work, f"rec-{name}.md")
    os.makedirs(work, exist_ok=True)
    with open(f, "w", encoding="utf-8") as fh: fh.write("# fixture\n\n" + rec + "\n")
    p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--root", root, f], capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

work = os.path.join(S, "probe5work")
if os.path.isdir(work): shutil.rmtree(work)
os.makedirs(work)
labroot = os.path.join(work, "lab")
os.makedirs(os.path.join(labroot, "corpus", "captures"))
os.makedirs(os.path.join(labroot, "corpus", "evidence", "round57"))
shutil.copy(os.path.join(LANE, "corpus", "SOURCES.md"), os.path.join(labroot, "corpus", "SOURCES.md"))
shutil.copy(os.path.join(LANE, "corpus", "evidence", "round57", "refetch.tsv"),
            os.path.join(labroot, "corpus", "evidence", "round57", "refetch.tsv"))
n = [900]
def add(url, capbytes, http="200", curl_rc="0"):
    n[0] += 1
    sid = f"S{n[0]}"; k = key(url)
    with open(os.path.join(labroot, "corpus", "captures", k + ".txt"), "wb") as fh: fh.write(capbytes)
    with open(os.path.join(labroot, "corpus", "SOURCES.md"), "a", encoding="utf-8") as fh:
        fh.write(f"| {sid} | fixture — {url} | docs | A | s | a | t | mined | 2026-11-09 | on-release | - |\n")
    with open(os.path.join(labroot, "corpus", "evidence", "round57", "refetch.tsv"), "a") as fh:
        fh.write("\t".join([sid, url, k, "1", "2026-11-09T04:00:33Z", curl_rc, http, "-", sha(capbytes)]) + "\n")
    q = " ".join(capbytes.decode("utf-8", errors="replace").split()[:5])
    return sid, url, k, q

fp = os.path.join(work, "fp")
# unreach correct form: capture=none words=0 quote=none -- CHALLENGE never checked since no capture file exists. Even if URL served a challenge row at 200 (contradiction), code path: unreach branch never touches is_challenge. Correctly named limit (d).
sid, url, k, q = add("https://fixture.invalid/unreach2", b"secret challenge bytes", http="200", curl_rc="0")
rec = f'GATE-RECORD {sid} url={url} fetched=2026-11-09T04:00:33Z tier=A decision=reject capture=none curl_rc=0 http=200 words=0 quote=none'
rc, out, err = run(labroot, rec, fp, "unreach-200")
print(f"unreach-200-success-row: rc={rc} out={out.strip()!r} (should FAIL REFETCH, never CHALLENGE — round-87 repair)")

# Punctuated/underscored evasion: "Just_a_moment" / "Just—a—moment"
ev = "Just_a_moment\nEnable JavaScript and cookies to continue\nwww.example.org needs to review the security of your connection.\n"
b = ev.encode()
sid2, url2, k2, q2 = add("https://fixture.invalid/underscored", b)
from probe import record as _  # noqa - irrelevant
rec = (f'GATE-RECORD {sid2} url={url2} fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/{k2}.txt '
       f'capture_sha256={sha(b)} words={len(q2.split())} quote="{q2}"')
rc, out, err = run(labroot, rec, fp, "underscored")
print(f"underscored-marker: rc={rc} out={out.strip()!r}")
# Note: 'enable javascript and cookies to continue' IS an ascii marker, so this may still refuse via second marker. Check below isolates single marker.

# Isolate: only 'just a moment' variant, no other marker.
ev2 = "Just_a_moment...\nPlease wait while we check your browser.\nwww.example.net needs to review the security of your connection.\n"
b2 = ev2.encode()
sid3, url3, k3, q3 = add("https://fixture.invalid/underscore-only", b2)
rec = (f'GATE-RECORD {sid3} url={url3} fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/{k3}.txt '
       f'capture_sha256={sha(b2)} words={len(q3.split())} quote="{q3}"')
rc, out, err = run(labroot, rec, fp, "underscore-only")
print(f"underscore-only: rc={rc} out={out.strip()!r} (word-boundary check: 'just a moment' substring NOT in 'just_a_moment')")

# hyphen variant
ev3 = "Just-a-moment...\nPlease wait while we check your browser.\nwww.example.net needs to review the security of your connection.\n"
b3 = ev3.encode()
sid4, url4, k4, q4 = add("https://fixture.invalid/hyphen-only", b3)
rec = (f'GATE-RECORD {sid4} url={url4} fetched=2026-11-09T04:00:33Z tier=A decision=admit capture=corpus/captures/{k4}.txt '
       f'capture_sha256={sha(b3)} words={len(q4.split())} quote="{q4}"')
rc, out, err = run(labroot, rec, fp, "hyphen-only")
print(f"hyphen-only: rc={rc} out={out.strip()!r}")

# QUALITY 229: probe said pattern over captures lists 4 challenge pages S230 among them. Recount at F with C1 markers.
repo = LANE
caps = sorted(os.listdir(os.path.join(repo, "corpus", "captures")))
print(f"total captures={len(caps)}")
