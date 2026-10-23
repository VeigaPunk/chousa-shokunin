import os
G="/tmp/hyaku/chousa-r35/w2/ExecC2Fresh1/head/research-gate.sh"
text=open(G,encoding="utf-8",errors="surrogateescape").read()
helper="/tmp/hyaku/chousa-r35/w2/ExecC2Fresh1/span_search.py"
snip=open("/tmp/hyaku/chousa-r35/w2/ExecC2Fresh1/forgery5.sh",encoding="utf-8").read().replace("@HELPER@",helper)
lines=text.splitlines(keepends=True)
start=next(i for i,l in enumerate(lines) if l.startswith("tok_span_offsets()"))
body=next(j for j in range(start+1,start+40) if lines[j].strip().startswith("local hay=$1 span=$2"))
out="".join(lines[:body+1]+[snip]+lines[body+1:])
dst="/tmp/hyaku/chousa-r35/w2/ExecC2Fresh1/head/spoof5-head.sh"
open(dst,"w",encoding="utf-8",errors="surrogateescape").write(out)
os.chmod(dst,0o755)
print("head forge:",dst)
