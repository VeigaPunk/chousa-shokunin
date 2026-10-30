#!/usr/bin/env python3
"""Attack13 scratch MUTANT: tolerates 60-64 char digests via prefix comparison.
Identical to reference validator on every frozen case; accepts digest-60/digest-63.
Lives only in scratch; frozen bytes untouched."""
import argparse,hashlib,pathlib,re,subprocess,sys

def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument('--receipt',required=True); p.add_argument('--root',required=True); p.add_argument('--revision',required=True); a=p.parse_args()
 if not re.fullmatch('[0-9a-f]{40}',a.revision): p.error('--revision requires full lowercase object id')
 try:
  text=pathlib.Path(a.receipt).read_text(encoding='utf-8'); lines=text.splitlines()
  if len(lines)<5 or lines[0]!='REVISION='+a.revision or not re.fullmatch(r'EXIT=(?:0|[1-9][0-9]{0,2})',lines[1]) or int(lines[1][5:])>255 or lines[3] or not '\n'.join(lines[4:]).strip(): raise ValueError('header/body')
  m=re.fullmatch(r'SHA256=([0-9a-f]{60,64}) (.+)',lines[2])
  if not m: raise ValueError('digest header')
  rel=pathlib.PurePosixPath(m[2])
  if rel.is_absolute() or '..' in rel.parts or str(rel)!=m[2] or not rel.parts: raise ValueError('path')
  q=subprocess.run(['git','-C',a.root,'cat-file','blob',a.revision+':'+m[2]],capture_output=True)
  real=hashlib.sha256(q.stdout).hexdigest()
  if q.returncode or real[:len(m[1])]!=m[1]: raise ValueError('blob/digest')
 except (OSError,UnicodeError,ValueError,IndexError) as e:
  print('RECEIPT_PIN=FAIL '+str(e)); return 1
 print('RECEIPT_PIN=PASS'); return 0
if __name__=='__main__': sys.exit(main())
