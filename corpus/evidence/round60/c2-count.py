#!/usr/bin/env python3
"""Offline S101 quote-bound claim counter for chousa round 60."""
from __future__ import annotations
import argparse, hashlib, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[3]
RAW=ROOT/'corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw'
FORM=ROOT/'.ufo/waves/round-60/s101-open.txt'
ENTRY=ROOT/'corpus/knowledge/citation-count-semantics-r37.md'
EXPECTED='c. 文献类型及载体类型标志；'
RAW_SHA='6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3'
FORM_SHA='a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867'
def main():
 p=argparse.ArgumentParser(); p.add_argument('--root',type=pathlib.Path,default=ROOT); p.add_argument('--work',type=pathlib.Path); a=p.parse_args(); root=a.root.resolve(); raw=root/'corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw'; form=ROOT/'.ufo/waves/round-60/s101-open.txt'; entry=root/'corpus/knowledge/citation-count-semantics-r37.md'
 try:
  rawsha=hashlib.sha256(raw.read_bytes()).hexdigest(); formbytes=form.read_bytes(); text=formbytes.decode('utf-8'); body=entry.read_text(encoding='utf-8'); lines=text.splitlines(); at=[i for i,l in enumerate(lines,1) if EXPECTED in l]
  source_ok=rawsha==RAW_SHA and hashlib.sha256(formbytes).hexdigest()==FORM_SHA and len(at)==1
  metadata=body.startswith('\n# ') and 'source: S101 — https://jc.hit.edu.cn/' in body and 'verified-at:' in body and 'recheck:' in body
  scoped='#### Unknown' in body and 'Whether the specification copy (S101) is the version in force' in body
  print(f'RAW_PIN={int(rawsha==RAW_SHA)}/1 FORM_PIN={int(hashlib.sha256(formbytes).hexdigest()==FORM_SHA)}/1 QUOTE={len(at)}/1 LINE={at[0] if at else 0} METADATA={int(metadata)}/1 LIMIT={int(scoped)}/1')
  ok=source_ok and metadata and scoped
  print(f'C2={"PASS" if ok else "FAIL"}'); return 0 if ok else 1
 except (OSError,UnicodeError) as e: print(f'C2=ERROR {type(e).__name__}: {e}'); return 2
if __name__=='__main__': sys.exit(main())
