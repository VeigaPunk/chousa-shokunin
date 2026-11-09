#!/usr/bin/env python3
"""Clean C1 verification: use battery-style unquoted quote (matches parse() rev branch)."""
import os, subprocess, sys
LANE = "/fast/scratch/hyaku/chousa-r100/R100CriticClaims/repo"
TOOL = os.path.join(LANE, "tools/gate-records.py")
S = "/fast/scratch/hyaku/chousa-r100/R100CriticClaims"
fx = os.path.join(S, "fx-c1")
def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()
A=run(["git","-C",fx,"rev-parse","HEAD~4"])[1]; B=run(["git","-C",fx,"rev-parse","HEAD~3"])[1]
C=run(["git","-C",fx,"rev-parse","HEAD~2"])[1]; D=run(["git","-C",fx,"rev-parse","HEAD~1"])[1]
E=run(["git","-C",fx,"rev-parse","HEAD"])[1]
k1="aaaaaaaaaaaaaaaaaaaaaaaa"; k2="bbbbbbbbbbbbbbbbbbbbbbbb"
def verify(sid, rev, path, name, first3=None):
    rc, blob, _ = run(["git","-C",fx,"show",f"{rev}:{path}"])
    q = first3 or " ".join(blob.split("\n")[0].split()[:3])
    rec = f"GATE-RECORD {sid} rev={rev} path={path} line=1 words=3 quote={q}"
    f = os.path.join(S, f"rec-{name}.md")
    with open(f,"w") as fh: fh.write(rec+"\n")
    rc, out, err = run([sys.executable,"-B",TOOL,"verify","--root",LANE,"--repo",fx,f])
    print(f"[{name}] rc={rc} q={q!r} :: {out.splitlines()[0] if out else err}")
# identity-at-rev: same path, different tree contents
verify("S230", A, f"corpus/captures/{k1}.txt", "v1-A-challenge")   # challenge at A -> FAIL CHALLENGE only
verify("S230", B, f"corpus/captures/{k1}.txt", "v2-B-nonchallenge")# non-challenge at B -> OK
verify("S230", B, "notes/blob.txt", "v3-bytecopy")                # byte copy at non-capture path, blob==k2 capture at B -> CHALLENGE
verify("S230", C, f"corpus/captures/{k2}.raw", "v4-raw-no-sibling")# challenge raw, no sibling -> CHALLENGE
verify("S230", D, f"corpus/captures/{k2}.raw", "v5-raw-clean-sib-challenge") # raw clean, sibling challenge -> sibling wins -> CHALLENGE expected?
verify("S230", E, f"corpus/captures/{k2}.raw", "v6-raw-challenge-sib-clean")  # raw challenge, sibling clean -> sibling wins -> OK expected?
# working-tree trap: dirty working tree, record at B
with open(os.path.join(fx,f"corpus/captures/{k1}.txt"),"wb") as fh: fh.write(b"Just a moment. Verify you are human now.\n")
verify("S230", B, f"corpus/captures/{k1}.txt", "v7-working-tree-trap")
# rev form that resolves but blob is NOT a capture (unique article blob, no capture holds it) at B
verify("S230", B, f"corpus/captures/{k1}.txt", "v8-same-path-diff-rev")  # already v2; this one: notes path with unique non-challenge bytes
