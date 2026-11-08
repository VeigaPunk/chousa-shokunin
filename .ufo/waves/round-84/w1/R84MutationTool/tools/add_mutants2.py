import json, os, subprocess, sys, re
src = open("tree/tools/gate-records.py", encoding="utf-8").read()
M = [
 ("mut33-accept-leading-zero",
  'INT_RE = re.compile(r"0|[1-9][0-9]{0,6}")',
  'INT_RE = re.compile(r"[0-9]{1,7}")',
  "leading-zero numerals accepted (INT_RE no-leading-zero rule dropped)"),
 ("mut34-drop-rev-line-zero-guard",
  '        if not INT_RE.fullmatch(kv["line"]) or kv["line"] == "0":',
  '        if not INT_RE.fullmatch(kv["line"]):',
  "rev line=0 accepted (indexes lines[-1])"),
]
man = json.load(open("mutants/manifest.json"))
for name, old, new, intent in M:
    assert src.count(old) == 1, (name, src.count(old))
    mut = src.replace(old, new, 1); compile(mut, name, "exec")
    p = os.path.join("mutants", name + ".py"); open(p, "w", encoding="utf-8").write(mut)
    man.append({"name": name, "intent": intent, "path": p, "old": old, "new": new})
json.dump(man, open("mutants/manifest.json", "w"), indent=1)
W=os.path.abspath("."); CTR="tree/corpus/evidence/round84/gate-records-r84.py"
REPO="/home/vgpnk/Projects/shokunin/chousa-shokunin"
res=[]
for name,_,_,intent in M:
    tool=os.path.abspath(os.path.join("mutants",name+".py"))
    p=subprocess.run([sys.executable,"-B",CTR,"--root","tree","--repo",REPO,"--tool",tool,"--work",W],
                     capture_output=True,text=True,env=dict(os.environ,TMPDIR=W,HYAKU_SCRATCH=W),cwd=W)
    out=p.stdout
    notes=[l for l in out.splitlines() if l.startswith(("NOT_REFUSED","WRONG_CODE"))]
    rep=os.path.join("receipts","mutants",name+".txt")
    open(rep,"w",encoding="utf-8").write(
      f"CMD: python3 -B {CTR} --root tree --repo {REPO} --tool {tool} --work {W}\nMUTANT: {intent}\nSTDOUT:\n{out}"
      + (f"STDERR:\n{p.stderr}" if p.stderr else "") + f"RC={p.returncode}\n")
    res.append({"name":name,"intent":intent,"rc":p.returncode,
                "verdict":"KILLED" if p.returncode else "SURVIVED",
                "summary":[l for l in out.splitlines() if l.startswith(("TOOL=","GATE_RECORDS_R84="))],
                "n_not_refused":sum(l.startswith("NOT_REFUSED") for l in notes),
                "n_wrong_code":sum(l.startswith("WRONG_CODE") for l in notes),
                "labels":sorted({re.match(r"(?:NOT_REFUSED|WRONG_CODE) (\S+) (\S+)",l).group(2) for l in notes}),
                "receipt":rep,"stderr_head":p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""})
    print(res[-1]["verdict"], name, "rc=%d"%p.returncode, res[-1]["summary"][0], "NR=%d WC=%d"%(res[-1]["n_not_refused"],res[-1]["n_wrong_code"]))
s=json.load(open("receipts/mutants/summary.json")); s.extend(res)
json.dump(s, open("receipts/mutants/summary.json","w"), indent=1)
