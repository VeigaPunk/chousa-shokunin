#!/usr/bin/env python3
"""Bounded flock/cancellation/fd review; no candidate production files are changed."""
import fcntl
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
ENV = {k: v for k, v in os.environ.items() if not k.startswith('CHOUSA_') and not k.startswith('GIT_')}
ENV.update(TMPDIR=str(HOME / 'tmp'), LC_ALL='C')
os.umask(0o027)
resource.setrlimit(resource.RLIMIT_FSIZE, (512 * 1024, 512 * 1024))


def launch(version, mf, trace=None):
    inner = ['/usr/bin/bash', str(HOME / version / 'tools/research-gate.sh'), 'verify-all',
             str(FIX / 'claims.jsonl'), '--root', str(FIX), '--json', str(mf)]
    if trace:
        inner = ['/usr/bin/strace', '-f', '-qq', '-e', 'trace=read', '-e', 'inject=read:delay_enter=2000000',
                 '-P', str(mf), '-o', str(trace)] + inner
    cmd = ['/usr/bin/timeout', '--kill-after=2', '25'] + inner
    p = subprocess.Popen(cmd, cwd=FIX, env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, start_new_session=True)
    return p, shlex.join(cmd)


def finish(p):
    try:
        out, err = p.communicate(timeout=30)
    except subprocess.TimeoutExpired:
        os.killpg(p.pid, signal.SIGKILL)
        out, err = p.communicate(timeout=3)
    finally:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    return {'rc': p.returncode, 'stdout': out.decode(errors='replace'), 'stderr': err.decode(errors='replace')}


def wait_lock(mf, p, seconds=5):
    inode = str(mf.stat().st_ino)
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        lines = Path('/proc/locks').read_text().splitlines()
        blocked = [line for line in lines if ' -> FLOCK ' in line and line.split()[-3].endswith(':' + inode)]
        if blocked:
            return blocked
        if p.poll() is not None:
            return []
        time.sleep(0.01)
    return []


def descendants(pid):
    found = []
    pending = [pid]
    while pending:
        current = pending.pop()
        try:
            children = [int(x) for x in Path('/proc/%d/task/%d/children' % (current, current)).read_text().split()]
        except (FileNotFoundError, ProcessLookupError):
            continue
        found.extend(children)
        pending.extend(children)
    return found


def proc_state(pid):
    try:
        return {'pid': pid, 'comm': Path('/proc/%d/comm' % pid).read_text().strip(),
                'stat': Path('/proc/%d/stat' % pid).read_text().strip()}
    except (FileNotFoundError, ProcessLookupError):
        return {'pid': pid, 'gone': True}


def ls_fd(pid):
    cmd = ['/usr/bin/timeout', '5', '/usr/bin/ls', '-l', '/proc/%d/fd' % pid]
    r = subprocess.run(cmd, capture_output=True, timeout=7)
    return {'pid': pid, 'command': shlex.join(cmd), 'rc': r.returncode,
            'stdout': r.stdout.decode(errors='replace'), 'stderr': r.stderr.decode(errors='replace')}


def file_result(mf):
    data = mf.read_bytes()
    try:
        objects = [isinstance(json.loads(line), dict) for line in data.splitlines()]
    except ValueError as e:
        objects = str(e)
    return {'inode': mf.stat().st_ino, 'bytes': data.decode(errors='replace'), 'json_objects': objects,
            'sha256': hashlib.sha256(data).hexdigest()}


def write_only_wait(version):
    root = HOME / 'wait-cases' / ('write-only-' + version)
    root.mkdir(parents=True)
    mf = root / 'manifest.jsonl'
    # Empty write-only is an explicitly accepted case at preflight, without chmod races.
    fd = os.open(mf, os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o200)
    fcntl.flock(fd, fcntl.LOCK_EX)
    p, cmd = launch(version, mf)
    blocked = wait_lock(mf, p)
    if version == 'base':
        p.wait(timeout=5)
    mode_before = oct(stat.S_IMODE(mf.stat().st_mode))
    before_fragment_size = mf.stat().st_size
    os.write(fd, b'{"holder":true}')
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)
    result = finish(p)
    result.update({'case': 'write-only-empty-with-cooperating-fragment', 'version': version,
                   'command': cmd, 'blocked_lock_rows': blocked, 'mode_during_gate': mode_before,
                   'size_before_holder_fragment': before_fragment_size})
    # Permission is restored only after the gate returns, to read the output.
    mf.chmod(0o600)
    result['manifest'] = file_result(mf)
    return result


def signal_wait(sig, group=False):
    label = signal.Signals(sig).name + ('-group' if group else '-shell')
    root = HOME / 'wait-cases' / label
    root.mkdir(parents=True)
    mf = root / 'manifest.jsonl'
    mf.write_bytes(b'{"prior":true}')
    fd = os.open(mf, os.O_WRONLY | os.O_APPEND)
    fcntl.flock(fd, fcntl.LOCK_EX)
    p, cmd = launch('landed', mf)
    rows = wait_lock(mf, p)
    if not rows:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
        return dict(finish(p), case=label, command=cmd, error='no blocked waiter observed')
    kids = descendants(p.pid)
    states = [proc_state(pid) for pid in kids]
    gates = [s['pid'] for s in states if s.get('comm') == 'bash']
    flocks = [s['pid'] for s in states if s.get('comm') == 'flock']
    before = mf.read_bytes()
    if group:
        os.killpg(p.pid, sig)
    else:
        os.kill(gates[0], sig)
    time.sleep(0.3)
    gate_states = [proc_state(pid) for pid in gates]
    flock_states = [proc_state(pid) for pid in flocks]
    status_before_release = p.poll()
    after_signal = mf.read_bytes()
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)
    result = finish(p)
    result.update({'case': label, 'version': 'landed', 'command': cmd, 'signal': int(sig), 'target_pids': [p.pid] if group else gates,
                   'blocked_lock_rows': rows, 'processes_before_signal': states, 'gate_after_signal_before_release': gate_states,
                   'flock_after_signal_before_release': flock_states, 'wrapper_status_before_release': status_before_release,
                   'manifest_before_signal': before.decode(), 'manifest_after_signal_before_release': after_signal.decode(),
                   'flock_after_release': [proc_state(pid) for pid in flocks], 'manifest': file_result(mf)})
    return result


def fd_children(version):
    root = HOME / 'wait-cases' / ('fd-children-' + version)
    root.mkdir(parents=True)
    mf = root / 'manifest.jsonl'
    mf.write_bytes(b'{"prior":true}')
    trace = root / 'tail-read.strace'
    p, cmd = launch(version, mf, trace=trace)
    seen = []
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        states = [proc_state(pid) for pid in descendants(p.pid)]
        if any(s.get('comm') == 'tail' for s in states):
            seen = [s for s in states if s.get('comm') in ('tail', 'od', 'tr')]
            break
        if p.poll() is not None:
            break
        time.sleep(0.01)
    fd_views = [ls_fd(s['pid']) for s in seen]
    held_rows = [line for line in Path('/proc/locks').read_text().splitlines()
                 if line.split()[-3].endswith(':' + str(mf.stat().st_ino))]
    result = finish(p)
    result.update({'case': 'post-lock-child-fds', 'version': version, 'command': cmd,
                   'children_seen': seen, 'fd_views': fd_views, 'lock_rows_during_probe': held_rows,
                   'lock_rows_after_gate': [line for line in Path('/proc/locks').read_text().splitlines()
                                            if line.split()[-3].endswith(':' + str(mf.stat().st_ino))],
                   'manifest': file_result(mf), 'trace': trace.read_text()})
    return result


def main():
    results = []
    for version in ['base', 'landed']:
        results.append(write_only_wait(version))
    for sig, group in [(signal.SIGTERM, False), (signal.SIGINT, False), (signal.SIGTERM, True)]:
        results.append(signal_wait(sig, group))
    for version in ['base', 'landed']:
        results.append(fd_children(version))
    payload = json.dumps({'cases': results}, indent=2) + '\n'
    if len(payload.encode()) >= 1024 * 1024:
        raise RuntimeError('artifact too large')
    (ART / 'wait-cases.json').write_text(payload)
    for row in results:
        print('%-6s %-46s rc=%s json=%s' % (row['version'], row['case'], row['rc'], row.get('manifest', {}).get('json_objects')), flush=True)
    print('ARTIFACT=' + str(ART / 'wait-cases.json'))


if __name__ == '__main__':
    main()
