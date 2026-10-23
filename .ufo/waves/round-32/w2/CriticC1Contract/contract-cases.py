#!/usr/bin/env python3
"""Read-only lane review. All mutations stay in this script's scratch parent."""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import resource
import shlex
import signal
import stat
import subprocess
import sys
import time

HOME = Path(__file__).resolve().parent
ART = Path('/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-32/w2/CriticC1Contract')
FIX = HOME / 'fixture'
BASE_ENV = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_') and not k.startswith('GIT_')}
BASE_ENV['TMPDIR'] = str(HOME / 'tmp')
BASE_ENV['LC_ALL'] = 'C'
LIMIT = 512 * 1024


def child_setup():
    os.umask(0o027)
    resource.setrlimit(resource.RLIMIT_FSIZE, (LIMIT, LIMIT))


def invoke(version, manifest, case, env=None, stdout_file=None):
    cmd = ['/usr/bin/timeout', '--kill-after=2', '15', '/usr/bin/bash', str(HOME / version / 'tools/research-gate.sh'),
           'verify-all', str(FIX / 'claims.jsonl'), '--root', str(FIX), '--json', str(manifest)]
    start = time.monotonic()
    handle = stdout_file.open('wb') if stdout_file else None
    p = subprocess.Popen(cmd, cwd=FIX, env=env or BASE_ENV, stdout=handle or subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True, preexec_fn=child_setup)
    try:
        out, err = p.communicate(timeout=20)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, err = p.communicate()
    finally:
        if handle:
            handle.close()
    # No command may leave descendants after the seat exits.
    try:
        os.killpg(p.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    out = out or b''
    result = {'version': version, 'case': case, 'command': shlex.join(cmd), 'rc': p.returncode,
              'elapsed_s': round(time.monotonic() - start, 3),
              'stdout': out.decode(errors='replace'), 'stderr': err.decode(errors='replace')}
    if stdout_file:
        result['stdout_file'] = str(stdout_file)
        result['stdout_file_bytes'] = stdout_file.read_bytes().decode(errors='replace')
    return result


def snapshot(path):
    result = {'exists': path.exists(), 'is_symlink': path.is_symlink()}
    if path.is_symlink():
        result['link_target'] = os.readlink(path)
    if not path.exists():
        return result
    st = path.stat()
    result.update({'mode': oct(stat.S_IMODE(st.st_mode)), 'inode': st.st_ino,
                   'size': st.st_size, 'type': stat.S_IFMT(st.st_mode)})
    if stat.S_ISREG(st.st_mode):
        if st.st_mode & stat.S_IRUSR:
            data = path.read_bytes()
            result.update({'sha256': hashlib.sha256(data).hexdigest(), 'bytes': data.decode(errors='replace')})
            try:
                result['json_objects'] = [isinstance(json.loads(line), dict) for line in data.splitlines()]
            except (ValueError, UnicodeDecodeError):
                result['json_objects'] = False
        else:
            result['read_skipped'] = 'write-only owner mode; not read by harness until restored'
    return result


def basic(version, case):
    root = HOME / 'cases' / version / case
    root.mkdir(parents=True, exist_ok=True)
    mf = root / 'manifest.jsonl'
    target = root / 'target.jsonl'
    output = None
    env = BASE_ENV.copy()
    if case == 'absent':
        pass
    elif case == 'symlink-regular':
        target.write_bytes(b'{"prior":true}')
        mf.symlink_to(target)
    elif case == 'symlink-dangling':
        mf.symlink_to(target)
    elif case == 'fifo':
        os.mkfifo(mf, 0o600)
    elif case == 'directory':
        mf.mkdir()
    elif case == 'unreadable-nonempty':
        mf.write_bytes(b'{"prior":true}')
        mf.chmod(0o200)
    elif case == 'unreadable-empty':
        mf.touch(mode=0o200)
        mf.chmod(0o200)
    elif case == 'dev-stdout-pipe':
        mf = Path('/dev/stdout')
    elif case == 'dev-stdout-regular':
        mf = Path('/dev/stdout')
        output = root / 'stdout.txt'
    elif case.startswith('no-flock'):
        env['PATH'] = str(HOME / 'no-flock-bin')
        if case.endswith('existing'):
            mf.write_bytes(b'{"prior":true}')
    before = snapshot(mf) if str(mf) != '/dev/stdout' else {'special_path': '/dev/stdout', 'stdout_kind': 'file' if output else 'pipe'}
    result = invoke(version, mf, case, env=env, stdout_file=output)
    if case.startswith('unreadable'):
        mf.chmod(0o600)
    result['before'] = before
    result['after'] = snapshot(mf) if str(mf) != '/dev/stdout' else {'not_snapshotted': 'per-process fd path'}
    return result


def main():
    cases = ['absent', 'symlink-regular', 'symlink-dangling', 'fifo', 'directory',
             'unreadable-nonempty', 'unreadable-empty', 'dev-stdout-pipe', 'dev-stdout-regular',
             'no-flock-existing', 'no-flock-absent']
    bindir = HOME / 'no-flock-bin'
    bindir.mkdir(exist_ok=True)
    for binary in ['bash', 'basename', 'cat', 'cut', 'date', 'dirname', 'grep', 'head',
                   'od', 'readlink', 'sed', 'sha256sum', 'sort', 'stat', 'tail', 'tr', 'wc']:
        dest = bindir / binary
        if not dest.exists():
            dest.symlink_to('/usr/bin/' + binary)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(basic, version, case) for version in ['base', 'landed'] for case in cases]
        for f in concurrent.futures.as_completed(futures):
            row = f.result()
            results.append(row)
            print('%-6s %-24s rc=%s %ss %s' % (row['version'], row['case'], row['rc'], row['elapsed_s'], row['stderr'].splitlines()[0] if row['stderr'] else 'no-stderr'), flush=True)
    results.sort(key=lambda r: (r['case'], r['version']))
    payload = json.dumps({'umask': '0027', 'cases': results}, indent=2) + '\n'
    if len(payload.encode()) >= 1024 * 1024:
        raise RuntimeError('artifact too large')
    (ART / 'contract-cases.json').write_text(payload)
    print('ARTIFACT=' + str(ART / 'contract-cases.json'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
