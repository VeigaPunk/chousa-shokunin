# R55CritForgeEcho — C1 non-reading forge attempts

Axes attacked: C1 operability / capability acquisition. Frozen claims read from `corpus/evidence/round55/claims.md` lines 47–95; C1 requires exact defined-form slices and four legs. Counter logic: `c1-count.py` lines 238–279 judges output slices, digests, ordered metadata, QUOTE lines, and exact span-file set; 282–315 supplies GENOLE/OLEPIN; 318–388 tests four refusal cases; 391–426 compares REGRESS byte-for-byte. Candidate behavior: `tools/build-spans.py` lines 63–92 defines OLE/ZIP form acquisition; lines 127–154 constructs context slices and refuses absent/duplicate quotes.

No tool installed or updated. Work was confined to `/fast/scratch/hyaku/chousa-r55/R55CritForgeEcho`; temporary workspace removed at exit.

## Forge code

The attempted tool below did not import or reimplement `capture-text.py`, and attempted sidecar/UTF-16 surrogates rather than the defined form. It had two modes: surrogate and refuse-all.

```python
#!/usr/bin/env python3
"""Non-reading R55-C1 forge experiments. No capture-text import or form reconstruction."""
import os, pathlib, subprocess, sys, hashlib, shutil
LANE=pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
COUNT=LANE/'corpus/evidence/round55/c1-count.py'
TOOL=LANE/'tools/build-spans.py'
S=pathlib.Path('/fast/scratch/hyaku/chousa-r55/R55CritForgeEcho')
def attempt(name, mode):
    work=S/f'work-{name}'; work.mkdir()
    fake=S/f'forge-{name}.py'
    fake.write_text('''import pathlib,sys
from pathlib import Path
args=sys.argv
def val(flag): return Path(args[args.index(flag)+1])
q=val("--quotes"); cache=val("--cache"); out=val("--out"); out.mkdir(parents=True,exist_ok=True); (out/"spans").mkdir(exist_ok=True)
rows=q.read_text(encoding="utf-8").splitlines()[1:]
'''+ ("" if mode=='refuse' else '''import hashlib
lines=["id\\turl\\tcapture_sha256\\toffset\\tspan_file\\tquote\\tentry"]
for row in rows:
 c=row.split("\\t"); sid,url,quote,entry=c; key=hashlib.sha256(url.encode()).hexdigest()[:24]; raw=cache/(key+".raw"); txt=cache/(key+".txt"); f=raw if raw.exists() else txt; digest=hashlib.sha256(f.read_bytes()).hexdigest(); name=f"spans/{sid}-1.txt"
 data=(txt.read_bytes().decode("utf-8","replace").replace("\\r\\n","\\n").replace("\\r","\\n") if txt.exists() else "")
 if quote not in data: data=raw.read_bytes().decode("utf-16le","replace") if raw.exists() else ""
 off=data.find(quote); start=max(0,off-80) if off>=0 else 0; span=data[start:off+len(quote)+80] if off>=0 else ""
 (out/name).write_text(span,encoding="utf-8"); lines.append("\\t".join([sid,url,digest,str(start),name,quote,entry]))
print("\\n".join(f"QUOTE {c[0]} char {int(x.split(chr(9))[3])+x.split(chr(9))[5].find(c[2])} spans/{c[0]}-1.txt" for x,c in zip(lines[1:], [r.split("\\t") for r in rows])))
(out/"spans.tsv").write_text("\\n".join(lines)+"\\n",encoding="utf-8")
print(f"SPANS_ROWS={len(rows)} WRITTEN={len(rows)}")
''')+'''\nfor row in rows:
 c=row.split("\\t"); print(f"build-spans: refused {c[0]}: forge refuses all",file=sys.stderr)
sys.exit(1)
''')
    cmd=[sys.executable,str(COUNT),'--tool',str(fake),'--work',str(work),'--per-leg','2']
    r=subprocess.run(cmd,capture_output=True,text=True,cwd=S,env={**os.environ,'TMPDIR':str(S),'PYTHONDONTWRITEBYTECODE':'1'},timeout=1200)
    print(f'ATTEMPT {name} rc={r.returncode}')
    for line in r.stdout.splitlines():
        if line.startswith(('GENOLE=','OLEPIN=','REFUSE=','REGRESS=','LEGS=','C1=')): print(line)
    if r.stderr: print('STDERR',r.stderr[-500:].replace('\\n',' | '))
    shutil.rmtree(work)
if __name__=='__main__':
 attempt('surrogate','surrogate'); attempt('refuse-all','refuse')
```

## Attempts and observed output

The invoking command was `python3 "$S/forge.py"`; both runs used `--per-leg 2` and explicit empty `--work` paths. Each test run generated its inputs and invoked the frozen counter; actual stdout excerpts:

```text
ATTEMPT surrogate rc=1
GENOLE=FAIL rc=1 b'build-spans: refused S901: forge refuses all\nbuild-spans: refused S901: forge refuses all\nbuild-spans: refused S902: forge refuses all\nbuild-spans: refused S902: forge refuses all\n'
OLEPIN=FAIL rc=1 b': forge refuses all\nbuild-spans: refused S923: forge refuses all\nbuild-spans: refused S923: forge refuses all\nbuild-spans: refused S924: forge refuses all\nbuild-spans: refused S924: forge refuses all\n'
REFUSE=FAIL NOFORM: spans.tsv written
REGRESS=FAIL rc=1 b': forge refuses all\nbuild-spans: refused S123: forge refuses all\nbuild-spans: refused S123: forge refuses all\nbuild-spans: refused S123: forge refuses all\nbuild-spans: refused S123: forge refuses all\n'
LEGS=0/4
C1=FAIL
ATTEMPT refuse-all rc=1
GENOLE=FAIL rc=1 b'build-spans: refused S901: forge refuses all\nbuild-spans: refused S901: forge refuses all\nbuild-spans: refused S902: forge refuses all\nbuild-spans: refused S902: forge refuses all\n'
OLEPIN=FAIL rc=1 b': forge refuses all\nbuild-spans: refused S923: forge refuses all\nbuild-spans: refused S923: forge refuses all\nbuild-spans: refused S924: forge refuses all\nbuild-spans: refused S924: forge refuses all\n'
REFUSE=PASS 4 cases
REGRESS=FAIL rc=1 b': forge refuses all\nbuild-spans: refused S123: forge refuses all\nbuild-spans: refused S123: forge refuses all\nbuild-spans: refused S123: forge refuses all\nbuild-spans: refused S123: forge refuses all\n'
LEGS=1/4
C1=FAIL
```

Both attempts failed to actually exercise the intended surrogate: the script-generation conditional appended the refusal block in both modes. Therefore these runs demonstrate the refusal-only ceiling (one leg), not a tested sidecar/window-picker exploit. The implementation defect is established by this seat's script, not an inference about the counter. No run-dir/argv/environment/proc/cache scraping attempt was run. Refusal cannot pass the two positive legs or exact round-54 regeneration; in refusal cases it passes only because the expected behavior is refusal, while NOFORM exposes its unconditional `spans.tsv` output.

## Counterexample assessment

The strongest local counterexample is structural: candidate slices derive from OLE reader output (`build-spans.py` 77–84), while the counter's expected generated forms are generated in memory and the generation tree is deleted before candidate invocation (`c1-count.py` 199–220, 282–296). The counter's judging predicate compares each produced span to that in-memory form (`c1-count.py` 267–272), so a surrogate text source that differs cannot satisfy GENOLE merely by locating its quote. The audit hook blocks ordinary process/network/ctypes delegation and out-of-allowlist reads (`c1-count.py` 81–108), and REGRESS additionally requires historical manifest and span bytes exactly (`c1-count.py` 391–426). The attempted refusal-all results are direct evidence, but do not establish non-forgeability: the surrogate branch was accidentally disabled, and no adversarial disk disclosure probe was executed.

Impacted axis: C1 operability only. Smallest safe correction to this report's experiment is to fix the harness conditional and rerun a true surrogate attempt before asserting a best non-reading forge score. No claim/counter/predicate change proposed.

VERDICT: attacked the frozen C1 non-reading forge surface; the exercised refusal-only forge scored 1/4, while the best non-reading score remains unestablished because the surrogate attempt was misconfigured.
