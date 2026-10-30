#!/usr/bin/env python3
"""R65-C1: CASES=20/20 C1=PASS iff all frozen receipt-consistency cases match their exact exit and token.
No execution-authenticity claim. Missing target fails, never passes. --work must be empty, removed on exit.
"""
import argparse,hashlib,pathlib,shutil,subprocess,sys
BASE='d6ed8155e9b4735639a2cf0a3e479c62f2056195'
LANE=pathlib.Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--tool',default=str(LANE/'tools/receipt-pin.py'));p.add_argument('--work',required=True);a=p.parse_args();w=pathlib.Path(a.work)
 if w.exists() and (not w.is_dir() or any(w.iterdir())):p.error('nonempty work')
 w.mkdir(parents=True,exist_ok=True)
 try:
  if not pathlib.Path(a.tool).is_file():print('CASES=0/20 C1=FAIL missing-target');return 1
  raw=subprocess.run(['git','-C',str(LANE),'cat-file','blob',BASE+':SKILL.md'],capture_output=True,check=True).stdout
  h=hashlib.sha256(raw).hexdigest();v=f'REVISION={BASE}\nEXIT=0\nSHA256={h} SKILL.md\n\nmeasured output\n'
  cases=[('valid',v,0),('nonzero-valid',v.replace('EXIT=0','EXIT=1'),0),('max-exit',v.replace('EXIT=0','EXIT=255'),0),('no-revision',v.split('\n',1)[1],1),('wrong-revision',v.replace(BASE,'0'*40),1),('short-revision',v.replace(BASE,BASE[:8]),1),('no-exit',v.replace('EXIT=0\n',''),1),('negative-exit',v.replace('EXIT=0','EXIT=-1'),1),('overflow-exit',v.replace('EXIT=0','EXIT=256'),1),('word-exit',v.replace('EXIT=0','EXIT=PASS'),1),('no-digest',v.replace('SHA256='+h+' SKILL.md\n',''),1),('wrong-digest',v.replace(h,'0'*64),1),('short-digest',v.replace(h,h[:16]),1),('missing-blob',v.replace('SKILL.md','missing-r65.md'),1),('traversal',v.replace('SKILL.md','../SKILL.md'),1),('absolute',v.replace('SKILL.md','/SKILL.md'),1),('duplicate',v.replace('\n\n','\nEXIT=0\n\n'),1),('no-separator',v.replace('\n\n','\n'),1),('no-body',v.split('\n\n')[0]+'\n\n',1),('upper-digest',v.replace(h,h.upper()),1)]
  n=0
  for name,text,rc in cases:
   f=w/(name+'.txt');f.write_text(text);q=subprocess.run([sys.executable,'-B',a.tool,'--receipt',str(f),'--root',str(LANE),'--revision',BASE],capture_output=True,text=True,timeout=20)
   ok=q.returncode==rc and q.stdout.strip()==('RECEIPT_PIN=PASS' if rc==0 else q.stdout.strip()) and (rc==0 or q.stdout.startswith('RECEIPT_PIN=FAIL '));n+=ok;print(f'CASE {name} {"PASS" if ok else "FAIL"} rc={q.returncode}')
  print(f'CASES={n}/20 C1={"PASS" if n==20 else "FAIL"}');return 0 if n==20 else 1
 finally:shutil.rmtree(w)
if __name__=='__main__':sys.exit(main())
