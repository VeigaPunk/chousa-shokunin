#!/usr/bin/env python3
"""Build two frozen C2 no-do-nothing controls in caller-provided scratch."""
from pathlib import Path
import argparse, shutil, subprocess, sys
L=Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
p=argparse.ArgumentParser(); p.add_argument('--work',required=True); a=p.parse_args(); w=Path(a.work); w.mkdir(parents=True,exist_ok=True)
for name in ('STAGED','REWRITE'):
    r=w/name; (r/'corpus/knowledge').mkdir(parents=True,exist_ok=True); (r/'corpus/evidence/round58/c2').mkdir(parents=True,exist_ok=True)
    shutil.copy2(L/'corpus/SOURCES.md',r/'corpus/SOURCES.md')
    # A citation-only shell cannot satisfy the frozen 12-quote manifest and is
    # deliberately unbound (STAGED) or paraphrased (REWRITE).
    entry='source: S101 — staged, not bound\nverified-at: 2026-10-27; control only\nrecheck: 90d\n\n'
    if name=='REWRITE': entry+='本规范把载体标识换成别的字段。\n'
    else: entry+='文献类型与载体类型被混作一个标签。\n'
    (r/'corpus/knowledge/carrier-alphabet-china-r58.md').write_text(entry,encoding='utf-8')
print('CONTROLS=STAGED,REWRITE (minimal unbound/paraphrased roots; expected C2=FAIL)')
