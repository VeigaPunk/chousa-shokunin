import hashlib, json, os, shutil, subprocess
from pathlib import Path
S = Path('/fast/scratch/hyaku/chousa-r33/w2/MutD1Counter')
L = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
A = L / '.ufo/waves/round-33/w2/MutD1Counter'
OLD = Path('/fast/scratch/hyaku/chousa-r32/w1')
W1 = L / '.ufo/waves/round-32/w1'
W2 = L / '.ufo/waves/round-32/w2'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p, data):
    b = (json.dumps(data, indent=2)+'\n').encode()
    assert len(b) < 1048576
    Path(p).write_bytes(b)
manifest = []
def add(name, source, prior, patch=None):
    dest = S / 'gates' / name / 'tools/research-gate.sh'
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    item = {'name':name, 'source':str(source), 'target':str(dest), 'source_sha256':sha(source), 'copied_sha256':sha(dest), 'prior':str(prior)}
    if patch:
        item['reconstruction'] = {'patch':str(patch),'patch_sha256':sha(patch), 'pending_tool_edit':True}
    item['scored_sha256'] = sha(dest)
    manifest.append(item)
for code,suffix in [('a','status-blind'),('b','judgment-only'),('c','skip-blocked')]:
    add('statusblind-'+code, OLD/'CtlC2StatusBlindB'/('control-'+code+'-'+suffix+'.sh'), W1/'CtlC2StatusBlindB/v2-rescore.md')
for name in ['grep-anywhere','skip-boundary','case-insensitive','whitespace-collapse','file-only']:
    src = (W2/'MutCounterC2v2/controls'/(name+'-gate.sh')) if name in ['case-insensitive','whitespace-collapse'] else OLD/'CtlC2WeakReaderB/base-gate.sh'
    patch = None if name in ['case-insensitive','whitespace-collapse'] else W1/'CtlC2WeakReaderB'/(name+'.patch')
    add('weak-'+name, src, W1/'CtlC2WeakReaderB/v2-rescore.md', patch)
for code,suffix in [('a','existing-file'),('b','inside-boundary'),('c','anchor-cell')]:
    add('noreader-'+code, OLD/'CtlC2NoReaderB'/('control-'+code+'-'+suffix+'.sh'), W1/'CtlC2NoReaderB/v2-rescore.md')
for name in ['noisy-findings','noisy-observed','noisy-duplicate','duplicate-only']:
    add(name, OLD/'CtlC2NoisyB'/(name+'.sh'), W1/'CtlC2NoisyB/v2-rescore.md')
for code,suffix in [('a','u-citation'),('b','all-citation'),('c','u-to')]:
    add('alltrue-'+code, OLD/'CtlC2AllTrueB'/('control-'+code+'-'+suffix+'.sh'), W1/'CtlC2AllTrueB/v2-rescore.md')
for name in ['random-labels','hop-id-shape','filename-shape','declared-id-shape','declared-id-member','generator-union','row-position','notes-shape','from-shape','random-valid-labels']:
    add('junk-'+name, OLD/'CtlC2JunkB'/(name+'-gate.sh'), W1/'CtlC2JunkB/v2-rescore.md')
add('do-nothing', OLD/'CtlC2DoNothingB/base-gate.sh', W1/'CtlC2DoNothingB/v2-rescore.md')
for name in ['clean-exit','no-verdict','stray-unknown','oracle']:
    add('w2-'+name, W2/'MutCounterC2v2/controls'/(name+'-gate.sh'), W2/'MutCounterC2v2.md')
add('metadata-only', W2/'CriticAxis32/metadata-control.sh', W2/'CriticAxis32.md')
(S/'counters').mkdir(exist_ok=True)
(S/'tmp').mkdir(exist_ok=True)
for version in ['v2','v3']:
    shutil.copyfile(L/('corpus/evidence/round32/c2-count-'+version+'.py'), S/'counters'/('c2-count-'+version+'.py'))
shutil.copyfile(W2/'MutCounterC2v2/emit-control-v2.py', S/'emit-control-v2.py')
for item in manifest:
    if item['name'].startswith('weak-'):
        expected = {'weak-grep-anywhere':'7be8f1d2acb8fae1b6e52baae6a22e8c449cb3d88809c476d70b5f20d4ad19f8','weak-skip-boundary':'a4552ca0157098fda889f339e2373a6150aa060fc3a284b7e2e6840dfed2e081','weak-file-only':'6bed45fb8c4f4735eea3c2db7eb67a59788dd7aabdf5a338851115e9e73629b4','weak-case-insensitive':'a0eab06c1546516a21ce54003271742d1b20b742bb319f06939c3a35b4700d06','weak-whitespace-collapse':'32e03f4f5ccae47fa613efad47b75ee167b4aef03bc61e807213428dda8e8c5d'}[item['name']]
        item['expected_scored_sha256'] = expected
inventory = {'scratch':str(S),'artifacts':str(A),'axes':['operability: bounded executable re-score and restoration','discrimination: no previously rejected negative control reaches 132/132'], 'gates':manifest, 'counters':{v:sha(S/'counters'/('c2-count-'+v+'.py')) for v in ['v2','v3']}}
dump(A/'inventory.json', inventory)
print(json.dumps({'gates':len(manifest),'counter_sha256':inventory['counters'],'reconstructions': [x['name'] for x in manifest if 'reconstruction' in x]},indent=2))
