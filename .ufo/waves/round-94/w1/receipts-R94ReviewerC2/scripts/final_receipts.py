import hashlib, os, re, subprocess, sys
S = "/fast/scratch/hyaku/chousa-r94/R94ReviewerC2"
R = os.path.join(S, "repo")
REC = os.path.join(S, "receipts")
NEW = os.path.join(R, "corpus/evidence/round94/curation-r94.py")
OLD = os.path.join(R, "corpus/evidence/round93/curation-r93.py")
CTRL = os.path.join(R, "corpus/evidence/round94/curation-controls-r94.py")
os.makedirs(REC, exist_ok=True)

def save(tag, cmd, rc, out):
    open(os.path.join(REC, tag + ".txt"), "w", encoding="utf-8").write(f"$ {cmd}\nexit={rc}\n{out}")
    return out

def sh(tag, cmd, cwd=R):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    save(tag, cmd, p.returncode, p.stdout + p.stderr)
    return p.returncode, p.stdout + p.stderr

# 1. clean counter
rc, out = sh("c2-counter-clean", f"python3 -B {NEW} --root .")
print("counter rc", rc)
print([l for l in out.splitlines() if l.startswith("CURATION_R94=") or l.startswith("VERDICT")])
print([l for l in out.splitlines() if l.startswith("SUPERSEDED_LIVE")])

# 2. predicate field check
expected = {"LEGS_MEASURED":"16/16","Q_SHAPE_FAIL":"0","Q_WSQUOT":"0","Q_PUNCTQUOT":"0","Q_ROWS":"20",
            "WARRANT_OK":"17/17","TFREQ_OK":"17/17","DUP_QIDS":"0"}
lines = out.splitlines()
summary = [l for l in lines if l.startswith("SUPERSEDED_LIVE")][0]
verdict = [l for l in lines if l.startswith("VERDICT")][0]
fields = dict(re.findall(r"([A-Z_]+)=([^ ]+)", summary))
vfields = dict(re.findall(r"([a-z_]+)=([^ ]+)", verdict))
rep = []
for k,v in expected.items():
    got = fields.get(k)
    rep.append(f"FIELD {k} expected={v} observed={got} {'OK' if got==v else 'FAIL'}")
for k,v in {"fields_hold":"1","legs_ok":"16/16","DETECTOR_WITNESS":"17/17"}.items():
    got = vfields.get(k)
    rep.append(f"VERDICTFIELD {k} expected={v} observed={got} {'OK' if got==v else 'FAIL'}")
rc2, out2 = sh("c2-controls-clean", f"python3 -B {CTRL} --root . --work {S}/work-final")
oline = [l for l in out2.splitlines() if l.startswith("CONTROLS=")][0]
ofields = dict(re.findall(r"([A-Z0-9_]+)=([^ /]+)", oline))
for k,v in {"CONTROLS":"PASS","CARRIED_REFUSED_BOTH":"4/4","WS_NAMED":"2/2","PUNCT_NAMED":"2/2",
            "PUNCT_SHAPE_GREEN_R93":"1/1","PRIOR_REGRESSION":"7/7"}.items():
    got = ofields.get(k)
    rep.append(f"CONTROLFIELD {k} expected={v} observed={got} {'OK' if got==v else 'FAIL'}")
open(os.path.join(REC, "predicate-fields.txt"), "w", encoding="utf-8").write(
    f"counter rc={rc}\ncontrols rc={rc2}\n" + "\n".join(rep) + f"\n\nobserved counter line:\n{summary}\n{verdict}\n"
    f"\nobserved controls line:\n{oline}\n")
print("controls rc", rc2); print(oline)

# 3. contiguous-string checks of the frozen predicate text
sh("controls-predicate-contiguous",
   "grep -cF -- 'PUNCT_SHAPE_GREEN_R93=1/1 PRIOR_REGRESSION=7/7' receipts/c2-controls-clean.txt; "
   "echo grep_exit=$?; grep -cF -- 'LEGS_MEASURED=16/16 Q_SHAPE_FAIL=0 Q_WSQUOT=0 Q_PUNCTQUOT=0 Q_ROWS=20' receipts/c2-counter-clean.txt; "
   "echo grep_exit2=$?", cwd=S)

# 4. r93/r94 on the two punctuation trees, explicit
for tag, tree in (("x1","controls-work/x1-punct-dash"),("x2","controls-work/x2-punct-dots")):
    sh(f"c2-controls-{tag}-r93", f"python3 -B {OLD} --root {tree}")
    sh(f"c2-controls-{tag}-r94", f"python3 -B {NEW} --root {tree}")

# 5. r93 class absence
sh("r93-no-punct-class",
   "for f in receipts/c2-controls-x1-r93.txt receipts/c2-controls-x2-r93.txt; do "
   "echo \"== $f\"; grep -c 'Q_PUNCTQUOT' \"$f\"; echo punct_field_exit=$?; "
   "grep -c 'quote=<punctuation>' \"$f\"; echo punct_reason_exit=$?; "
   "grep -E 'Q_SHAPE_FAIL|CURATION_R93=' \"$f\"; done", cwd=S)

# 6. detector direct cases
import importlib.util
spec = importlib.util.spec_from_file_location("cur94", NEW); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cases = {
 "long_quote_em_dash_plus_words": ['Q1','S214','"\u2014 date when each source was last searched or consulted."'],
 "em_dash_inside_longer_quote": ['Q1','S214','"the report\u2019s separator \u2014 is not a search date"'],
 "clean_q10_punctuation_heavy": ['Q10','S023','"Recommended practice is to describe the date, date/time, or period of time as recommended for the property Date, of which this is a subproperty."'],
 "bare_em_dash": ['Q1','S214','"\u2014"'],
 "bare_dots": ['Q1','S214','"..."'],
 "bare_copyright": ['Q1','S023','"\u00a9"'],
 "bare_section_sign": ['Q1','S023','"\u00a7"'],
 "section_sign_with_number": ['Q1','S023','"\u00a7 4.2"'],
 "cjk_letters": ['Q1','S023','"\u6570\u636e\u5e93"'],
 "greek_letter": ['Q1','S023','"\u03a9"'],
 "locates_guard_on_dash": ['Q1','S214','"\u2014"'],
}
r = []
for k,c in cases.items():
    inner = c[2].strip().strip('"').strip()
    r.append(f"{k}: cell={c[2]!r} ascii_alnum={bool(m.PUNCT_RE.search(inner))} isalnum={inner.isalnum()} "
             f"punct_quote_cell={m.punct_quote_cell(c)} q_shape={m.q_shape_violation(c)} "
             f"locates_bare={m.locates(c[2].strip().strip(chr(34)), 'before \u2014 after')}")
open(os.path.join(REC, "D-detector-cases.txt"), "w", encoding="utf-8").write("\n".join(r) + "\n")
print("\n".join(r))

# 7. punctuation-run scan over the three cited captures
scan = subprocess.run([sys.executable, "-c", r'''
import re, hashlib, os
reg=open("corpus/SOURCES.md").read().splitlines()
urls={}
for l in reg:
    m=re.match(r"^\| (S\d{3,}) \|",l)
    if not m: continue
    u=re.search(r"https?://[^\s|)>\]]+",l)
    if u: urls[m.group(1)]=u.group(0)
for sid in ("S214","S018","S023"):
    key=hashlib.sha256(urls[sid].encode()).hexdigest()[:24]
    text=open(f"corpus/captures/{key}.txt",encoding="utf-8",errors="replace").read()
    runs=re.findall(r"[^A-Za-z0-9]{7,}",text)
    best=max((len(r.split()),r) for r in runs) if runs else (0,"")
    print(sid,key,"max_punct_tokens",best[0],repr(best[1][:40]))
'''], cwd=R, capture_output=True, text=True)
save("punct-run-scan", "python3 - <<scan cited captures for maximal non-alnum runs", scan.returncode, scan.stdout+scan.stderr)
print(scan.stdout)
