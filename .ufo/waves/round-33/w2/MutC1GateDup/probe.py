import asyncio
import hashlib
import json
import os
from pathlib import Path
import shlex
import signal
import time

LANE = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin')
SCRATCH = Path('/fast/scratch/hyaku/chousa-r33/w2/MutC1GateDup')
ART = LANE / '.ufo/waves/round-33/w2/MutC1GateDup'
COUNTER = LANE / 'corpus/evidence/round33/c1-count-v2.py'
LANDED = '94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

async def phase(label, jobs):
    sem = asyncio.Semaphore(3)
    async def run_one(seat, kind, seed):
        async with sem:
            gate = SCRATCH / seat / 'tools/research-gate.sh'
            stem = label + '-' + seat + '-' + kind + (('-' + str(seed)) if seed is not None else '')
            log_root = SCRATCH if kind == 'selftest' else ART
            stdout = log_root / (stem + '.stdout')
            stderr = log_root / (stem + '.stderr')
            meta = ART / (stem + '.run.json')
            receipt = ART / (stem + '.receipt.json') if kind == 'counter' else None
            before = digest(gate)
            env = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_') and k not in ('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE')}
            temp = SCRATCH / 'tmp' / seat
            temp.mkdir(exist_ok=True)
            env.update(C1_TMP=str(temp), C2_TMP=str(temp), TMPDIR=str(temp))
            file_cap = 16777216 if kind == 'selftest' else 900000
            cmd = ['timeout', '--signal=TERM', '--kill-after=5s', '600s', 'prlimit', '--nproc=2000', '--as=4000000000', '--core=0', '--fsize=' + str(file_cap), '--']
            if kind == 'counter':
                cmd += ['python3', str(COUNTER), '--gate', str(gate), '--seed', str(seed), '--receipt', str(receipt)]
            else:
                cmd += ['bash', str(gate), '--selftest']
            t0 = time.monotonic()
            with stdout.open('xb') as out, stderr.open('xb') as err:
                p = await asyncio.create_subprocess_exec(*cmd, cwd=str(gate.parent.parent), env=env, stdout=out, stderr=err, start_new_session=True)
                emergency_kill = False
                try:
                    rc = await asyncio.wait_for(p.wait(), timeout=612)
                except asyncio.TimeoutError:
                    emergency_kill = True
                    os.killpg(p.pid, signal.SIGKILL)
                    rc = await p.wait()
            if kind == 'selftest':
                for log in (stdout, stderr):
                    if log.stat().st_size <= 900000:
                        import shutil
                        shutil.copyfile(log, ART / log.name)
                if stdout.stat().st_size <= 900000:
                    stdout = ART / stdout.name
                if stderr.stat().st_size <= 900000:
                    stderr = ART / stderr.name
            record = {
                'phase': label, 'seat': seat, 'kind': kind, 'seed': seed,
                'argv': cmd, 'command': 'C1_TMP=' + shlex.quote(env['C1_TMP']) + ' C2_TMP=' + shlex.quote(env['C2_TMP']) + ' TMPDIR=' + shlex.quote(env['TMPDIR']) + ' ' + shlex.join(cmd) + ' >' + shlex.quote(str(stdout)) + ' 2>' + shlex.quote(str(stderr)),
                'cwd': str(gate.parent.parent), 'pid_and_pgid': p.pid, 'rc': rc,
                'elapsed_s': round(time.monotonic() - t0, 3), 'emergency_kill': emergency_kill,
                'gate_sha256_before': before, 'gate_sha256_after': digest(gate),
                'counter_sha256': digest(COUNTER) if kind == 'counter' else None,
                'stdout': str(stdout), 'stdout_sha256': digest(stdout), 'stdout_bytes': stdout.stat().st_size,
                'stderr': str(stderr), 'stderr_sha256': digest(stderr), 'stderr_bytes': stderr.stat().st_size,
                'receipt': str(receipt) if receipt else None,
                'receipt_written': bool(receipt and receipt.is_file()),
            }
            meta.write_text(json.dumps(record, indent=2) + '\n')
            print(json.dumps({'run': stem, 'rc': rc, 'elapsed_s': record['elapsed_s'], 'meta': str(meta)}), flush=True)
            return record
    records = await asyncio.gather(*(run_one(*job) for job in jobs))
    (ART / (label + '.runs.json')).write_text(json.dumps(records, indent=2) + '\n')
    return records
