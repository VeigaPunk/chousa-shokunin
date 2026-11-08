import json, os, subprocess, sys, re
W = os.path.abspath(".")
CTR = "tree/corpus/evidence/round84/gate-records-r84.py"
REPO = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
man = json.load(open("mutants/manifest.json"))
os.makedirs("receipts/mutants", exist_ok=True)
summary = []
for m in man:
    tool = os.path.abspath(m["path"])
    cmd = [sys.executable, "-B", CTR, "--root", "tree", "--repo", REPO,
           "--tool", tool, "--work", W]
    env = dict(os.environ, TMPDIR=W, HYAKU_SCRATCH=W)
    p = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=W)
    out = p.stdout
    summ = [l for l in out.splitlines() if l.startswith("TOOL=") or l.startswith("GATE_RECORDS_R84=") or l.startswith("FRESH_BUILD")]
    notes = [l for l in out.splitlines() if l.startswith("NOT_REFUSED") or l.startswith("WRONG_CODE")]
    rep = os.path.join("receipts", "mutants", m["name"] + ".txt")
    with open(rep, "w", encoding="utf-8") as fh:
        fh.write("CMD: " + " ".join(["python3", "-B", CTR, "--root", "tree", "--repo", REPO,
                                     "--tool", tool, "--work", W]) + "\n")
        fh.write("MUTANT: " + m["intent"] + "\n")
        fh.write("STDOUT:\n" + out)
        if p.stderr:
            fh.write("STDERR:\n" + p.stderr)
        fh.write("RC=%d\n" % p.returncode)
    labels = sorted({re.match(r"(?:NOT_REFUSED|WRONG_CODE) (\S+) (\S+)", l).group(2) for l in notes if re.match(r"(?:NOT_REFUSED|WRONG_CODE) (\S+) (\S+)", l)})
    summary.append({"name": m["name"], "intent": m["intent"], "rc": p.returncode,
                    "verdict": "KILLED" if p.returncode != 0 else "SURVIVED",
                    "summary": summ, "n_not_refused": sum(l.startswith("NOT_REFUSED") for l in notes),
                    "n_wrong_code": sum(l.startswith("WRONG_CODE") for l in notes),
                    "labels": labels, "receipt": rep,
                    "stderr_head": p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""})
json.dump(summary, open("receipts/mutants/summary.json", "w"), indent=1)
for s in summary:
    print(f'{s["verdict"]:8s} {s["name"]:34s} rc={s["rc"]} {s["summary"][0] if s["summary"] else "(no TOOL= line)"}')
