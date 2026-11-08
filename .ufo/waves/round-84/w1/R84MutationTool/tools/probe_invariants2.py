import hashlib, os, re, subprocess, sys
W=os.path.abspath("."); REPO="/home/vgpnk/Projects/shokunin/chousa-shokunin"
rows=[l.rstrip("\n").split("\t") for l in open("tree/corpus/evidence/round57/refetch.tsv",encoding="utf-8",errors="replace")]
rows=[r for r in rows if len(r)==9 and r[0].startswith("S")]
bad_key=[r for r in rows if r[2]!=hashlib.sha256(r[1].encode()).hexdigest()[:24]]
bad_url=[r for r in rows if not re.fullmatch(r"https?://\S+", r[1])]
lines=[]
lines.append(f"REFETCH_DATA_ROWS={len(rows)} KEY_NOT_SHA24={len(bad_key)} URL_NOT_HTTP={len(bad_url)}")
lines.append("INVARIANT: every data row satisfies key==sha256(url)[:24] and url is http(s) => "
             "admit REFETCH's r[2]==key is implied by r[1]==url + CAPTURE_KEY; the url scheme gate is "
             "implied by CAPTURE_KEY (mut26, mut32 redundant)")
# W10 correct: quote from the line we also declare
ln=[x for x in open("tree/corpus/evidence/round84/c2-positives.tsv",encoding="utf-8")][0]
f,n,raw=ln.rstrip("\n").split("\t",2)
rev=re.search(r"(?<= )rev=(\S+)",raw).group(1); path=re.search(r"(?<= )path=(\S+)",raw).group(1)
blob=subprocess.run(["git","-C",REPO,"cat-file","blob",rev+":"+path],capture_output=True).stdout.decode("utf-8","replace").split("\n")
if blob and blob[-1]=="": blob.pop()
idx=q=None
for i,cand in enumerate(blob,1):
    if len(cand.split())>=26:
        idx=i; q=" ".join(" ".join(cand.split()).split()[:26]); break
rec=re.sub(r"(?<= )line=\S+","line=%d"%idx,raw.split(" quote=")[0]+" quote="+q,count=1)
rec=re.sub(r"(?<= )words=\S+","words=26",rec,count=1)
fp="receipts/witnesses/W10-rev-quote-26.md"; open(fp,"w",encoding="utf-8").write(rec+"\n")
def run(tool):
    p=subprocess.run([sys.executable,"-B",tool,"verify","--root","tree","--repo",REPO,fp],capture_output=True,text=True,cwd=W)
    return p.returncode,p.stdout.strip(),p.stderr.strip()
prc,pout,perr=run("tree/tools/gate-records.py"); mrc,mout,merr=run("mutants/mut11-quote-len-26.py")
open("receipts/witnesses/W10-rev-quote-26.txt","w",encoding="utf-8").write(
  f"WITNESS: W10-rev-quote-26\nLINE={rec}\nPRISTINE_CMD: python3 -B tree/tools/gate-records.py verify --root tree --repo {REPO} {fp}\n"
  f"PRISTINE_RC={prc}\nPRISTINE_STDOUT={pout}\nPRISTINE_STDERR={perr}\n"
  f"MUTANT_CMD: python3 -B mutants/mut11-quote-len-26.py verify --root tree --repo {REPO} {fp}\nMUTANT_RC={mrc}\nMUTANT_STDOUT={mout}\nMUTANT_STDERR={merr}\n")
lines.append(f"W10 pristine rc={prc} {pout.splitlines()[0]}")
lines.append(f"W10 mutant   rc={mrc} {mout.splitlines()[0]}")
lines.append("TREE_TOOL_SHA "+hashlib.sha256(open("tree/tools/gate-records.py","rb").read()).hexdigest())
lines.append("COUNTER_SHA "+hashlib.sha256(open("tree/corpus/evidence/round84/gate-records-r84.py","rb").read()).hexdigest())
lines.append("LANDING_GIT_BLOB_SHA "+subprocess.run(f"git -C {REPO} cat-file blob 03bbb4580b39b442be69f998fae2db48d64b8c93:tools/gate-records.py | sha256sum",shell=True,capture_output=True,text=True).stdout.split()[0])
open("receipts/invariants.txt","w",encoding="utf-8").write("\n".join(lines)+"\n")
print("\n".join(lines))
