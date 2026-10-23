import argparse, concurrent.futures, hashlib, importlib.util, json, os, secrets, shutil, signal, subprocess, sys, tempfile, time
from pathlib import Path
sys.dont_write_bytecode = True
S = Path('/fast/scratch/hyaku/chousa-r33/w2/MutD1Counter')
A = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w2/MutD1Counter')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p, data):
    b = (json.dumps(data, indent=2)+'\n').encode()
    assert len(b) < 1048576, (p,len(b))
    Path(p).write_bytes(b)
def load_counter(version):
    path = S/'counters'/('c2-count-'+version+'.py')
    spec = importlib.util.spec_from_file_location('d1_'+version, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
ap = argparse.ArgumentParser()
ap.add_argument('--phase', default='pristine')
ap.add_argument('--only', default='')
ap.add_argument('--versions', default='v2,v3')
a = ap.parse_args()
inv = json.loads((A/'inventory.json').read_text())
if (A/'seeds.json').exists():
    seeds = json.loads((A/'seeds.json').read_text())
else:
    seeds = [secrets.randbits(62)+10**10 for _ in range(2)]
    dump(A/'seeds.json',seeds)
gates = [x for x in inv['gates'] if not a.only or x['name'] in a.only.split(',')]
for item in gates:
    got = sha(item['target'])
    if 'expected_scored_sha256' in item:
        assert got == item['expected_scored_sha256'], (item['name'],got)
    if a.phase == 'pristine':
        item['scored_sha256'] = got
        if 'reconstruction' in item: item['reconstruction']['pending_tool_edit'] = False
        if item['name'] in ['w2-clean-exit','w2-no-verdict','w2-stray-unknown']:
            item['relocation'] = 'Only helper path and per-run D1_TRUTH payload path changed at line 3.'
if a.phase == 'pristine': dump(A/'inventory.json',inv)
truth_paths = {}
for version in a.versions.split(','):
    module = load_counter(version)
    for seed in seeds:
        temp = tempfile.mkdtemp(prefix='truth-',dir=S/'tmp')
        try:
            _,_,truth = module.generate(temp,seed)
            payload = A/('truth-'+version+'-s'+str(seed)+'.json')
            dump(payload,{h:{'class':c,'truth':t} for h,(c,t) in truth.items()})
            truth_paths[(version,seed)] = payload
        finally:
            shutil.rmtree(temp)

def run(item,version,seed):
    name = item['name']+'-'+version+'-'+a.phase+'-s'+str(seed)
    receipt = A/(name+'.json')
    stdout,stderr = A/(name+'.stdout.txt'),A/(name+'.stderr.txt')
    counter = S/'counters'/('c2-count-'+version+'.py')
    argv = ['timeout','--signal=TERM','--kill-after=3s','90s','prlimit','--nproc=2000','--as=4000000000','--fsize=1048575','--','python3',str(counter),'--gate',item['target'],'--seed',str(seed),'--receipt',str(receipt)]
    env = {k:v for k,v in os.environ.items() if k not in ['GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE']}
    env.update({k:str(S/'tmp') for k in ['C1_TMP','C2_TMP','TMPDIR']})
    env['D1_TRUTH'] = str(truth_paths[(version,seed)])
    started = time.time()
    record = {'name':item['name'],'version':version,'phase':a.phase,'seed':seed,'command':argv,'cwd':str(S),'env':{k:env[k] for k in ['C1_TMP','C2_TMP','TMPDIR','D1_TRUTH']},'gate_sha256_before':sha(item['target']),'counter_sha256_before':sha(counter),'receipt':str(receipt),'stdout':str(stdout),'stderr':str(stderr)}
    with stdout.open('wb') as out,stderr.open('wb') as err:
        p = subprocess.Popen(argv,cwd=S,env=env,stdout=out,stderr=err,start_new_session=True)
        record['pid'] = p.pid
        record['pgid'] = p.pid
        dump(A/(name+'.started.json'),record)
        try:
            record['rc'] = p.wait(timeout=100)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGKILL)
            record['rc'] = p.wait(timeout=5)
            record['driver_timeout'] = True
        finally:
            try:
                os.killpg(p.pid,signal.SIGKILL)
                record['remaining_group_killed'] = True
            except ProcessLookupError:
                record['remaining_group_killed'] = False
    record.update({'elapsed_s':round(time.time()-started,3),'gate_sha256_after':sha(item['target']),'counter_sha256_after':sha(counter),'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr)})
    if receipt.exists():
        rr = json.loads(receipt.read_text())
        record.update({k:rr[k] for k in ['matched','total','label','predicate_holds','gate_rc','gate_timed_out','record_fails']})
    else:
        record['harness_error'] = 'no receipt'
    dump(A/(name+'.run.json'),record)
    return record
jobs = [(g,v,s) for g in gates for v in a.versions.split(',') for s in seeds]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    records = list(pool.map(lambda args:run(*args),jobs))
dump(A/('runs-'+a.phase+'.json'),records)
for g in gates:
    rr = [r for r in records if r['name']==g['name']]
    print(g['name']+' '+', '.join(r['version']+':'+r.get('label','HARNESS_ERROR')+'(rc='+str(r['rc'])+')' for r in rr),flush=True)
print('RUNS='+str(len(records))+' HARNESS_ERRORS='+str(sum('harness_error' in r for r in records)),flush=True)
