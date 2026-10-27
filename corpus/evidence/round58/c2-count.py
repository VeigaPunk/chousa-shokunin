#!/usr/bin/env python3
"""Frozen round-58 C2 counter: S101 carrier-alphabet source-to-entry chain.
The exact twelve quotes are frozen here and in claims.md before wave data.
Run with --root to score a scratch/control lane; --work is caller-owned scratch.
No network access. C2 stays causally separate from C1 by pinning the round-55
build-spans.py and capture-text.py bytes. See claims.md for predicate/kill rule.
"""
from __future__ import annotations
import argparse, hashlib, pathlib, re, shutil, subprocess, sys, tempfile, os

LANE = pathlib.Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
BASE = 'b13ca7b5c8bbb40d2d29a37fb443c64ca043f791'
BUILDER_SHA = '1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6'
CT_SHA = '2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573'
RAW_KEY = '6dc68fd6b32ce9c8dfcebce8'
RAW_SHA = '6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3'
URL = 'https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc'
ENTRY_REL = 'corpus/knowledge/carrier-alphabet-china-r58.md'
SPANS_REL = 'corpus/evidence/round58/c2'
QUOTES = [
 '1．2 参考文献类型及其标识',
 '1．2．1 根据GB3469规定，以单字母方式标识以下各种参考文献类型：',
 '建议以下列双字母作为标识：',
 '被引用为参考文献时需在参考文献类型标识中同时标明其载体类型',
 '磁带(magnetic tape)—MT',
 '联机网络(online)—OL',
 '并以[文献类型标识/载体类型标识]表示',
 '[M/CD]—光盘图书(monograph on CD–ROM)；',
 '[J/OL]—网上期刊(serial online)；',
 '[DB/OL]—联机网上数据库(database online)；',
 '出版地:出版者,出版年:起止页码(当整体引用时不注).',
 '与文献标志码(Document code)',
]
HEADER = 'id\turl\tquote\tentry'


def sha(b): return hashlib.sha256(b).hexdigest()
def out(line): print(line)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root', default=str(LANE))
    ap.add_argument('--work', default=None)
    ap.add_argument('--quiet', action='store_true')
    a=ap.parse_args(); root=pathlib.Path(a.root).resolve(); work=pathlib.Path(a.work) if a.work else None
    errors=[]; entry=root/ENTRY_REL; spans=root/SPANS_REL; registry=root/'corpus/SOURCES.md'
    # Entry and source-row binding.
    if not entry.is_file(): errors.append('ENTRY_MISSING')
    text=entry.read_text(encoding='utf-8') if entry.is_file() else ''
    lines=text.splitlines()
    trio=lines[:3]
    if len(trio)<3 or not trio[0].startswith('source:') or not trio[1].startswith('verified-at:') or not trio[2].startswith('recheck:'):
        errors.append('PROVENANCE_TRIO')
    if 'S101' not in (trio[0] if trio else ''): errors.append('S101_NOT_IN_SOURCE')
    if not registry.is_file(): errors.append('REGISTRY_MISSING')
    reg=registry.read_text(encoding='utf-8') if registry.is_file() else ''
    row=next((x for x in reg.splitlines() if x.startswith('| S101 |')), '')
    if not row: errors.append('S101_ROW_MISSING')
    else:
        cells=[c.strip() for c in row.strip('|').split('|')]
        if len(cells)!=11 or cells[7]!='mined' or ENTRY_REL not in cells[10]: errors.append('REF_ID_UNBOUND')
    ids=set(re.findall(r'\bS\d{3,}\b', text))
    stray=sorted(ids-{'S101'})
    if stray: errors.append('STRAY_IDS='+','.join(stray))
    # Pin builder/capture implementation, retaining causal separation from C1.
    builder=root/'tools/build-spans.py'; ct=root/'tools/capture-text.py'
    if not builder.is_file() or sha(builder.read_bytes())!=BUILDER_SHA: errors.append('BUILDER_PIN')
    if not ct.is_file() or sha(ct.read_bytes())!=CT_SHA: errors.append('CAPTURE_TEXT_PIN')
    raw=root/'corpus/captures'/f'{RAW_KEY}.raw'
    if not raw.is_file() or sha(raw.read_bytes())!=RAW_SHA: errors.append('RAW_PIN')
    form=''
    if ct.is_file() and raw.is_file():
        p=subprocess.run([sys.executable,'-B',str(ct),str(raw)],capture_output=True,text=True,timeout=120,
                         env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(work or os.environ.get('TMPDIR','/tmp'))))
        if p.returncode: errors.append('DEFINED_FORM_RC='+str(p.returncode))
        form=p.stdout
    # Exact frozen quote set and manifest verification.
    qfile=root/'corpus/evidence/round58/c2/quotes.tsv'
    if not qfile.is_file(): errors.append('QUOTES_MISSING')
    else:
        qrows=qfile.read_text(encoding='utf-8').splitlines()
        if not qrows or qrows[0]!=HEADER: errors.append('QUOTES_HEADER')
        actual=[x.split('\t')[2] for x in qrows[1:] if len(x.split('\t'))==4]
        if actual!=QUOTES: errors.append(f'QUOTE_SET={len(actual)}/{len(QUOTES)}')
    manifest=spans/'spans.tsv'; mrows=[]
    if not manifest.is_file(): errors.append('MANIFEST_MISSING')
    else:
        mrows=manifest.read_text(encoding='utf-8').splitlines()
        if not mrows or mrows[0]!='id\turl\tcapture_sha256\toffset\tspan_file\tquote\tentry': errors.append('MANIFEST_HEADER')
        if len(mrows)-1!=len(QUOTES): errors.append(f'QUOTE_ROWS={max(0,len(mrows)-1)}/{len(QUOTES)}')
    bound=0; anchors=0; short=0; context=0; quote_in_entry=0
    if mrows:
        for rowline in mrows[1:]:
            c=rowline.split('\t')
            if len(c)!=7: errors.append('MANIFEST_COLUMNS'); continue
            sid,url,digest,offset,sfile,quote,epath=c
            try: off=int(offset)
            except ValueError: errors.append('OFFSET_INVALID'); continue
            occurrences=[m.start() for m in re.finditer(re.escape(quote),form)]
            if url!=URL or digest!=RAW_SHA or len(occurrences)!=1 or occurrences[0]!=off:
                errors.append('CAPTURE_BIND:'+sid)
                continue
            bound+=1
            start=max(0,off-80); end=off+len(quote)+80
            spanfile=spans/sfile
            expected=form[start:end]
            if not spanfile.is_file() or spanfile.read_text(encoding='utf-8')!=expected: errors.append('SPAN_BYTES:'+sid)
            if quote in text: quote_in_entry+=1
            else: errors.append('QUOTE_NOT_IN_ENTRY:'+sid)
            if len(quote)<=36: short+=1
            else: errors.append('QUOTE_TOO_LONG:'+sid)
            if expected==quote or len(expected)>len(quote)+162: errors.append('CONTEXT:'+sid)
            else: context+=1
            if off==0 or form.rfind('\n',0,off)+1==off: anchors+=1
    # Rebuild with the frozen builder in caller-provided scratch; byte-compare to committed manifest/files.
    rebuilt=False
    if builder.is_file() and qfile.is_file() and work:
        tmp=work/'c2-rebuild'
        if tmp.exists(): shutil.rmtree(tmp)
        tmp.mkdir(parents=True)
        cmd=[sys.executable,'-B',str(builder),'--quotes',str(qfile),'--out',str(tmp),'--cache',str(root/'corpus/captures')]
        p=subprocess.run(cmd,capture_output=True,text=True,timeout=180,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(work)))
        if p.returncode==0 and manifest.is_file() and (tmp/'spans.tsv').read_bytes()==manifest.read_bytes():
            rebuilt=True
            for sf in (spans/'spans').glob('*.txt') if (spans/'spans').is_dir() else []:
                tf=tmp/'spans'/sf.name
                if not tf.is_file() or tf.read_bytes()!=sf.read_bytes(): rebuilt=False
        if not rebuilt: errors.append('BUILDER_REBUILD_MISMATCH')
    elif work is None: errors.append('WORK_REQUIRED_FOR_REBUILD')
    # Subject-matter support floor: 12 exact rows, at least 3 line-start anchors.
    if len(mrows)-1==len(QUOTES) and bound==len(QUOTES): pass
    else: errors.append(f'CAPTURE_BOUND={bound}/{len(QUOTES)}')
    if anchors<3: errors.append(f'ANCHOR_BOUND={anchors}/3')
    if quote_in_entry!=len(QUOTES): errors.append(f'ENTRY_QUOTES={quote_in_entry}/{len(QUOTES)}')
    # Existing quality tools.
    substance=root/'corpus/evidence/round51/quote-substance-check.py'
    if not substance.is_file() or not manifest.is_file(): sub_ok=False
    else:
        p=subprocess.run([sys.executable,'-B',str(substance),str(manifest)],capture_output=True,text=True,timeout=120,
                         env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(work or os.environ.get('TMPDIR','/tmp'))))
        sub_ok=p.returncode==0
        if not sub_ok: errors.append('SUBSTANCE_FAIL:'+((p.stdout+p.stderr)[:180]).replace('\n',' '))
    inf_ok=False
    inf=root/'tools/inference-ground.py'
    if inf.is_file() and manifest.is_file() and entry.is_file():
        p=subprocess.run([sys.executable,'-B',str(inf),'--entry',str(entry),'--spans',str(manifest),'--counts','/dev/null','--registry',str(registry),'--root',str(root)],
                         capture_output=True,text=True,timeout=120,
                         env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(work or os.environ.get('TMPDIR','/tmp'))))
        inf_ok=p.returncode==0
        if not inf_ok: errors.append('INFERENCE_GROUND_FAIL:'+((p.stdout+p.stderr)[:180]).replace('\n',' '))
    # Claim base did not hold this carrier-alphabet ground; verify full source tree query.
    base=subprocess.run(['git','-C',str(root),'grep','-l','載体类型标识',BASE,'--','corpus/knowledge'],capture_output=True,text=True)
    new_ground=base.returncode==1 and '载体类型标识' in text
    if not new_ground: errors.append('NEW_GROUND_FAIL')
    verdict='PASS' if not errors and sub_ok and inf_ok and rebuilt else 'FAIL'
    if not a.quiet:
        out(f'ENTRIES={int(entry.is_file())}/1 BOUND={int("REF_ID_UNBOUND" not in errors)}/1 REF_ID_UNBOUND={int("REF_ID_UNBOUND" in errors)}')
        out(f'QUOTE_ROWS={max(0,len(mrows)-1)}/{len(QUOTES)} CAPTURE_BOUND={bound}/{len(QUOTES)} ENTRY_QUOTES={quote_in_entry}/{len(QUOTES)}')
        out(f'SUBSTANCE={"PASS" if sub_ok else "FAIL"} ANCHOR_BOUND={anchors}/3 INFERENCE_GROUNDED={"yes" if inf_ok else "no"} STRAY_IDS={','.join(stray) if stray else "-"} NEW_GROUND={"yes" if new_ground else "no"} REBUILD={"MATCH" if rebuilt else "FAIL"}')
        for e in errors: out('ERROR '+e)
        out('C2='+verdict)
    return 0 if verdict=='PASS' else 1

if __name__=='__main__': sys.exit(main())
