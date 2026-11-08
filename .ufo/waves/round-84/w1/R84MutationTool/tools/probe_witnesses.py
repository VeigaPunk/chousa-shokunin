import importlib.util, json, os, re, subprocess, sys, hashlib
W = os.path.abspath(".")
TREE = os.path.abspath("tree")
REPO = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
spec = importlib.util.spec_from_file_location("ctr", "tree/corpus/evidence/round84/gate-records-r84.py")
ctr = importlib.util.module_from_spec(spec); spec.loader.exec_module(ctr)

pool = json.load(open("witness_pool.json"))
pos = []
for ln in open("tree/corpus/evidence/round84/c2-positives.tsv", encoding="utf-8"):
    f, n, raw = ln.rstrip("\n").split("\t", 2)
    pos.append((f, int(n), raw))
fa, fr, fu = ctr.build_fresh_positives(TREE, REPO)

def kv_set(line, key, val):
    return re.sub(r"(?<= )" + re.escape(key) + r"=\S+", key + "=" + val, line, count=1)
def form(line):
    return "rev" if " rev=" in line else ("unreach" if " capture=none " in line else "admit")

admits = [p for p in pos if form(p[2]) == "admit"]
revs   = [p for p in pos if form(p[2]) == "rev"]
unreach_fresh = fu[0][1]

w = {}
w["W1-stale-sha"] = (pool["stale"][0]["line"], "S113 row: rc0/2xx but txt_sha256 != sha256(capture)", "mut05-drop-refetch-sha")
w["W2-unreach-success"] = (pool["unreach_success"][0]["line"], "refetch row rc0/2xx published as capture=none unreach record", "mut28-drop-unreach-success-guard")
rc0 = kv_set(unreach_fresh, "curl_rc", "99" if ctr.kv_get(unreach_fresh, "curl_rc") != "99" else "98")
w["W3-unreach-rc-mismatch"] = (rc0, "unreach record curl_rc altered away from the committed row", "mut29-drop-unreach-curlrc-equality")
short = kv_set(revs[0][2], "rev", ctr.kv_get(revs[0][2], "rev")[:12])
w["W4-short-rev"] = (short, "rev shortened to 12 hex (git resolves it; HEX40 gate is the only defense)", "mut15-rev-short-accepted")
admit0 = admits[0][2]
unq = admit0.split(" quote=")[0] + " quote=" + admit0.split(" quote=",1)[1][1:-1]
w["W5-unquoted-quote"] = (unq, "admit quote without surrounding double quotes", "mut20-drop-quote-boundary-guard")
url = ctr.kv_get(admit0, "url")
w["W6-non-http-url"] = (kv_set(admit0, "url", "ftp://example.invalid/x"), "url scheme ftp://", "mut26-accept-url-non-http")
w["W7-fetched-nonshape"] = (kv_set(admit0, "fetched", "not-a-timestamp"), "fetched is not a timestamp at all", None)
w["W8-leading-zero-words"] = (kv_set(admit0, "words", "0" + ctr.kv_get(admit0, "words")), "words with leading zero", None)
w["W9-unterminated-quote"] = (admit0[:-1], "admit quote's closing double quote removed", None)
# 26-word rev quote located in the blob, if a line has >=26 words
def blob_line(rec):
    sid, kv, quote, f = ctr.parse(rec)
    b = ctr.git_blob(REPO, kv["rev"], kv["path"])
    return b.decode("utf-8","replace").split("\n"), int(kv["line"])
try:
    lines, ln_no = blob_line(revs[0][2])
    cand = next((l for l in lines if len(l.split()) >= 26), None)
    if cand:
        q26 = " ".join(" ".join(cand.split()).split()[:26])
        rec26 = revs[0][2].split(" quote=")[0] + " quote=" + q26
        rec26 = kv_set(rec26, "words", "26")
        w["W10-rev-quote-26"] = (rec26, "rev quote with 26 words (QUOTE_LEN upper bound)", None)
except Exception as e:
    print("W10 build failed", e)

os.makedirs("receipts/witnesses", exist_ok=True)
rows = []
for name, (line, why, mutant) in w.items():
    fp = os.path.join(W, "receipts", "witnesses", name + ".md")
    open(fp, "w", encoding="utf-8").write(line + "\n")
    def run(tool):
        p = subprocess.run([sys.executable, "-B", tool, "verify", "--root", "tree", "--repo", REPO, fp],
                           capture_output=True, text=True, cwd=W)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    prc, pout, perr = run("tree/tools/gate-records.py")
    mres = None
    if mutant:
        mrc, mout, merr = run(os.path.join("mutants", mutant + ".py"))
        mres = (mrc, mout, merr)
    with open(os.path.join("receipts","witnesses", name + ".txt"), "w", encoding="utf-8") as fh:
        fh.write(f"WITNESS: {name}\nWHY: {why}\nMUTANT: {mutant}\n")
        fh.write(f"PRISTINE_CMD: python3 -B tree/tools/gate-records.py verify --root tree --repo {REPO} {fp}\n")
        fh.write(f"PRISTINE_RC={prc}\nPRISTINE_STDOUT={pout}\nPRISTINE_STDERR={perr}\n")
        if mres:
            fh.write(f"MUTANT_CMD: python3 -B mutants/{mutant}.py verify --root tree --repo {REPO} {fp}\n")
            fh.write(f"MUTANT_RC={mres[0]}\nMUTANT_STDOUT={mres[1]}\nMUTANT_STDERR={mres[2]}\n")
    rows.append({"witness": name, "why": why, "mutant": mutant, "pristine_rc": prc,
                 "pristine": pout, "mutant_rc": mres[0] if mres else None,
                 "mutant": mres[1] if mres else None})
    print(f'{name:26s} pristine_rc={prc} {pout.splitlines()[-1] if pout else ""!r}')
    if mres: print(f'{"":26s} mutant_rc={mres[0]} {mres[1].splitlines()[-1] if mres[1] else ""!r}')
json.dump(rows, open("receipts/witnesses/summary.json","w"), indent=1)
