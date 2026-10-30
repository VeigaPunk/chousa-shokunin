#!/usr/bin/env python3
"""Lookup-table target: exact answers for the 20 frozen c1 cases, PASS otherwise."""
import sys, pathlib, hashlib, subprocess
BASE='d6ed8155e9b4735639a2cf0a3e479c62f2056195'
LANE='/home/vgpnk/Projects/shokunin/chousa-shokunin'
raw=subprocess.run(['git','-C',LANE,'cat-file','blob',BASE+':SKILL.md'],capture_output=True,check=True).stdout
h=hashlib.sha256(raw).hexdigest();v=f'REVISION={BASE}\nEXIT=0\nSHA256={h} SKILL.md\n\nmeasured output\n'
cases=[('valid',v,0),('nonzero-valid',v.replace('EXIT=0','EXIT=1'),0),('max-exit',v.replace('EXIT=0','EXIT=255'),0),('no-revision',v.split('\n',1)[1],1),('wrong-revision',v.replace(BASE,'0'*40),1),('short-revision',v.replace(BASE,BASE[:8]),1),('no-exit',v.replace('EXIT=0\n',''),1),('negative-exit',v.replace('EXIT=0','EXIT=-1'),1),('overflow-exit',v.replace('EXIT=0','EXIT=256'),1),('word-exit',v.replace('EXIT=0','EXIT=PASS'),1),('no-digest',v.replace('SHA256='+h+' SKILL.md\n',''),1),('wrong-digest',v.replace(h,'0'*64),1),('short-digest',v.replace(h,h[:16]),1),('missing-blob',v.replace('SKILL.md','missing-r65.md'),1),('traversal',v.replace('SKILL.md','../SKILL.md'),1),('absolute',v.replace('SKILL.md','/SKILL.md'),1),('duplicate',v.replace('\n\n','\nEXIT=0\n\n'),1),('no-separator',v.replace('\n\n','\n'),1),('no-body',v.split('\n\n')[0]+'\n\n',1),('upper-digest',v.replace(h,h.upper()),1)]
text=pathlib.Path(sys.argv[sys.argv.index('--receipt')+1]).read_text()
for name,c,rc in cases:
    if text==c:
        print('RECEIPT_PIN=PASS' if rc==0 else 'RECEIPT_PIN=FAIL frozen-'+name); sys.exit(rc)
print('RECEIPT_PIN=PASS'); sys.exit(0)
