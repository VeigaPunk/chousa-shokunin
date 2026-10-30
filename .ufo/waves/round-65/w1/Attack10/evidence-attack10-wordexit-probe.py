#!/usr/bin/env python3
"""Attack10 probe: C1 word-exit axis — nearby forged/malformed EXIT receipts.
Battery A: run frozen REFERENCE validator on malformed EXIT variants + odd line endings.
Battery B: lookup-table stub target vs frozen counter + forged receipts.
Read-only git (cat-file). No frozen bytes touched.
"""
import hashlib, json, pathlib, subprocess, sys, os

LANE = '/home/vgpnk/Projects/shokunin/chousa-shokunin'
BASE = 'd6ed8155e9b4735639a2cf0a3e479c62f2056195'
REF = f'{LANE}/corpus/evidence/round65/controls/ref-receipt-pin.py'
HERE = pathlib.Path('/fast/scratch/hyaku/chousa-r65/Attack10')
RCPTS = HERE / 'receipts'
RCPTS.mkdir(exist_ok=True)
env = dict(os.environ, TMPDIR=str(HERE / 'tmp'))

raw = subprocess.run(['git', '-C', LANE, 'cat-file', 'blob', BASE + ':SKILL.md'],
                     capture_output=True, check=True).stdout
h = hashlib.sha256(raw).hexdigest()
v = f'REVISION={BASE}\nEXIT=0\nSHA256={h} SKILL.md\n\nmeasured output\n'

def run(tool, receipt):
    q = subprocess.run([sys.executable, '-B', tool, '--receipt', str(receipt),
                        '--root', LANE, '--revision', BASE],
                       capture_output=True, text=True, timeout=20, env=env)
    return q.returncode, q.stdout.strip()

# ---------- Battery A: malformed EXIT field variants (nearby word-exit) ----------
exit_variants = [
    ('frozen-word-exit', 'EXIT=PASS'),      # the one frozen case
    ('word-lower',       'EXIT=pass'),
    ('word-mixed',       'EXIT=Pass'),
    ('word-ok',          'EXIT=OK'),
    ('word-true',        'EXIT=true'),
    ('word-na',          'EXIT=N/A'),
    ('word-none',        'EXIT=none'),
    ('word-empty',       'EXIT='),
    ('word-hex',         'EXIT=0x0'),
    ('word-plus',        'EXIT=+1'),
    ('word-space-in',    'EXIT= 0'),
    ('word-float',       'EXIT=1.0'),
    ('word-sci',         'EXIT=1e0'),
    ('word-unicode',     'EXIT=\u0665'),     # arabic-indic digit five
    ('leadzero-00',      'EXIT=00'),
    ('leadzero-01',      'EXIT=01'),
    ('leadzero-099',     'EXIT=099'),
    ('trail-space',      'EXIT=0 '),
    ('lead-space',       'EXIT= 0 '),
    ('tab-after',        'EXIT=0\t'),
    ('double-eq',        'EXIT==0'),
    ('newline-inject',   'EXIT=0\nEXIT=0'),
]

print('=== Battery A: reference validator vs malformed EXIT variants ===')
results_a = []
for name, exitline in exit_variants:
    body = v.replace('EXIT=0', exitline, 1)
    f = RCPTS / f'A-{name}.txt'
    f.write_text(body)
    rc, out = run(REF, f)
    results_a.append({'name': name, 'exit_line': exitline, 'ref_rc': rc, 'ref_out': out})
    print(f'{name:16s} ref_rc={rc} ref_out={out!r}')

# ---------- Battery A2: odd line separators (splitlines accepts \x0b \x0c \u2028 etc.) ----------
print('=== Battery A2: reference validator vs odd line endings ===')
sep_variants = [
    ('crlf', '\r\n'),
    ('cr', '\r'),
    ('formfeed', '\x0c'),
    ('vtab', '\x0b'),
    ('uni-lsep', '\u2028'),
    ('uni-psep', '\u2029'),
]
results_a2 = []
for name, sep in sep_variants:
    body = sep.join([f'REVISION={BASE}', 'EXIT=0', f'SHA256={h} SKILL.md', '', 'measured output'])
    f = RCPTS / f'A2-{name}.txt'
    f.write_text(body)
    rc, out = run(REF, f)
    results_a2.append({'name': name, 'sep': repr(sep), 'ref_rc': rc, 'ref_out': out})
    print(f'{name:16s} ref_rc={rc} ref_out={out!r}')

# ---------- Battery B: lookup-table stub that passes frozen 20 but accepts all else ----------
STUB = HERE / 'lookup_stub.py'
stub_src = '''#!/usr/bin/env python3
"""Lookup-table target: exact answers for the 20 frozen c1 cases, PASS otherwise."""
import sys, pathlib, hashlib, subprocess
BASE='d6ed8155e9b4735639a2cf0a3e479c62f2056195'
LANE='/home/vgpnk/Projects/shokunin/chousa-shokunin'
raw=subprocess.run(['git','-C',LANE,'cat-file','blob',BASE+':SKILL.md'],capture_output=True,check=True).stdout
h=hashlib.sha256(raw).hexdigest();v=f'REVISION={BASE}\\nEXIT=0\\nSHA256={h} SKILL.md\\n\\nmeasured output\\n'
cases=[('valid',v,0),('nonzero-valid',v.replace('EXIT=0','EXIT=1'),0),('max-exit',v.replace('EXIT=0','EXIT=255'),0),('no-revision',v.split('\\n',1)[1],1),('wrong-revision',v.replace(BASE,'0'*40),1),('short-revision',v.replace(BASE,BASE[:8]),1),('no-exit',v.replace('EXIT=0\\n',''),1),('negative-exit',v.replace('EXIT=0','EXIT=-1'),1),('overflow-exit',v.replace('EXIT=0','EXIT=256'),1),('word-exit',v.replace('EXIT=0','EXIT=PASS'),1),('no-digest',v.replace('SHA256='+h+' SKILL.md\\n',''),1),('wrong-digest',v.replace(h,'0'*64),1),('short-digest',v.replace(h,h[:16]),1),('missing-blob',v.replace('SKILL.md','missing-r65.md'),1),('traversal',v.replace('SKILL.md','../SKILL.md'),1),('absolute',v.replace('SKILL.md','/SKILL.md'),1),('duplicate',v.replace('\\n\\n','\\nEXIT=0\\n\\n'),1),('no-separator',v.replace('\\n\\n','\\n'),1),('no-body',v.split('\\n\\n')[0]+'\\n\\n',1),('upper-digest',v.replace(h,h.upper()),1)]
text=pathlib.Path(sys.argv[sys.argv.index('--receipt')+1]).read_text()
for name,c,rc in cases:
    if text==c:
        print('RECEIPT_PIN=PASS' if rc==0 else 'RECEIPT_PIN=FAIL frozen-'+name); sys.exit(rc)
print('RECEIPT_PIN=PASS'); sys.exit(0)
'''
STUB.write_text(stub_src)

print('=== Battery B1: frozen counter vs lookup-table stub (full battery, one bounded run) ===')
w = HERE / 'work-stub'
q = subprocess.run([sys.executable, '-B', f'{LANE}/corpus/evidence/round65/c1-count.py',
                    '--tool', str(STUB), '--work', str(w)],
                   capture_output=True, text=True, timeout=120, env=env)
print(q.stdout, end='')
print(f'counter_rc={q.returncode}')
results_b1 = {'counter_rc': q.returncode, 'counter_stdout_tail': q.stdout.strip().splitlines()[-1]}

print('=== Battery B2: stub + reference on forged receipts outside frozen cases ===')
forged = [
    ('forged-word-ok',  v.replace('EXIT=0', 'EXIT=OK')),
    ('forged-word-hex', v.replace('EXIT=0', 'EXIT=0x0')),
    ('forged-leadzero', v.replace('EXIT=0', 'EXIT=00')),
    ('forged-word-na',  v.replace('EXIT=0', 'EXIT=N/A')),
]
results_b2 = []
for name, body in forged:
    f = RCPTS / f'B-{name}.txt'
    f.write_text(body)
    rc_stub, out_stub = run(str(STUB), f)
    rc_ref, out_ref = run(REF, f)
    results_b2.append({'name': name, 'stub_rc': rc_stub, 'stub_out': out_stub,
                       'ref_rc': rc_ref, 'ref_out': out_ref})
    print(f'{name:16s} stub_rc={rc_stub} stub_out={out_stub!r} | ref_rc={rc_ref} ref_out={out_ref!r}')

(HERE / 'results.json').write_text(json.dumps(
    {'battery_a': results_a, 'battery_a2': results_a2,
     'battery_b1': results_b1, 'battery_b2': results_b2}, indent=1))
print('RESULTS_JSON=' + str(HERE / 'results.json'))
