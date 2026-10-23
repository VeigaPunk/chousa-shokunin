#!/usr/bin/env python3
"""Round 32 C1 counter: cooperating `verify-all --json` manifest appenders.

Frozen predicate (claims.md, P1): C1 is met iff, on the landed lane revision,
this counter prints APPEND_SERIALIZED=24/24 (receipt label
predicate_holds=true) on each of two fresh-seed runs, and no run of this
counter on that revision in round 32 prints a lower count.

Contract the candidate must meet (claims.md, C1 contract): for
`verify-all RECORD --root ROOT --json PATH`, the gate opens PATH for append
(creating it when absent), takes an exclusive flock(2) on that open file,
and holds it from before it reads the manifest's last byte until after its
own line is written. A cooperating writer that holds an exclusive flock(2)
on PATH therefore excludes both the gate's last-byte probe and its append.
Bytes already in the manifest are never rewritten; the manifest keeps its
inode; every appended line is one JSON object on its own line.

Trials (24, fixed): each trial writes a fresh temp root holding one opaque
source and a one-claim claims JSONL used as the record, so every writer runs
`bash <gate> verify-all <record> --root <root> --json <manifest>` with every
CHOUSA_* variable removed from its environment.

- L trials (12; manifest seeds empty / terminated / unterminated, 4 each):
  the counter opens the manifest and takes LOCK_EX, launches W_L=8 writers,
  and waits until every writer has exited or is listed in /proc/locks as a
  blocked waiter on the manifest's inode (deadline 180 s). It then checks
  that the manifest still holds exactly the seed bytes (hold check); on an
  empty or terminated seed it appends an unterminated cooperating fragment
  `{"frag":N}` (no newline), and leaves an unterminated seed as it is; it
  releases the lock and waits for every writer (deadline 300 s).
- F trials (12; seed unterminated): W_F=16 writers run with no counter lock.

A trial passes iff every check holds: hold check (L only); all writers
reached the lock or exited within the deadline (L only); every writer exited
within its deadline with the same exit code as one solo reference run of the
gate on the same record (0 or 1); the manifest keeps its inode and starts
with the seed bytes (plus the fragment bytes, L); the bytes after that prefix
are exactly W lines, each terminated by a newline, each a JSON object whose
"schema" is "chousa-verify-all/v1"; the prefix itself splits into non-empty
lines that are JSON objects (an unterminated seed or fragment must have been
terminated by the next writer, so seed and fragment lines stay their own
lines); no blank line anywhere; the file ends with a newline.

Exit: 0 iff matched == 24; 1 otherwise; 2 harness error (including a solo
reference run that exits other than 0 or 1, or a host without /proc/locks).
No network; writes only its temp dir and --receipt.
"""
import argparse
import fcntl
import hashlib
import json
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time

W_L = 8
W_F = 16
L_SEEDS = ["empty"] * 4 + ["terminated"] * 4 + ["unterminated"] * 4
F_TRIALS = 12
TOTAL = len(L_SEEDS) + F_TRIALS
SCHEMA = "chousa-verify-all/v1"
LOCK_DEADLINE_S = 180
WRITER_DEADLINE_S = 300
SYL = ["ka", "ri", "mo", "tu", "se", "na", "lo", "pe", "vi", "da", "gu", "ho", "ze", "bi", "fa", "yo"]
LOCKS_RE = re.compile(r"^\d+:\s+(->\s+)?FLOCK\s+\S+\s+\S+\s+(\d+)\s+[0-9a-fA-F]+:[0-9a-fA-F]+:(\d+)\s")


class Harness(Exception):
    pass


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 16), b""):
            h.update(b)
    return h.hexdigest()


def phrase(rng, n):
    return " ".join("".join(rng.choice(SYL) for _ in range(rng.randint(2, 4))) for _ in range(n))


def make_root(base, rng, k):
    root = tempfile.mkdtemp(prefix="t%02d-" % k, dir=base)
    span = phrase(rng, 3)
    src = "s%08x.md" % rng.getrandbits(32)
    with open(os.path.join(root, src), "w") as f:
        f.write(phrase(rng, 4) + "\n" + phrase(rng, 2) + " " + span + " " + phrase(rng, 2) + "\n")
    rec = os.path.join(root, "c%08x.jsonl" % rng.getrandbits(32))
    with open(rec, "w") as f:
        f.write(json.dumps({"id": "c%06x" % rng.getrandbits(24), "source": src, "span": span,
                            "expect": "supported"}) + "\n")
    return root, rec


def seed_bytes(kind, rng):
    if kind == "empty":
        return b""
    obj = json.dumps({"seed": rng.getrandbits(30)}).encode()
    return obj + b"\n" if kind == "terminated" else obj


def gate_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}


def launch(gate, rec, root, manifest, n):
    procs = []
    for _ in range(n):
        procs.append(subprocess.Popen(["bash", gate, "verify-all", rec, "--root", root, "--json", manifest],
                                      cwd=root, env=gate_env(), stdin=subprocess.DEVNULL,
                                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                      start_new_session=True))
    return procs


def kill_all(procs):
    for p in procs:
        if p.poll() is None:
            try:
                os.killpg(p.pid, 9)
            except OSError:
                pass
            try:
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass


def waiters_on(ino):
    n = 0
    with open("/proc/locks") as f:
        for line in f:
            m = LOCKS_RE.match(line)
            if m and m.group(1) and int(m.group(3)) == ino:
                n += 1
    return n


def wait_exit(procs, deadline):
    rcs = []
    for p in procs:
        left = deadline - time.time()
        try:
            rcs.append(p.wait(timeout=max(left, 0.01)))
        except subprocess.TimeoutExpired:
            rcs.append(None)
    return rcs


def check_manifest(path, ino, prefix, w):
    """Return a list of failed check names (empty = pass)."""
    fails = []
    st = os.stat(path)
    if st.st_ino != ino:
        fails.append("inode-changed")
    with open(path, "rb") as f:
        data = f.read()
    if not data.startswith(prefix):
        fails.append("prefix-rewritten")
        return fails
    if not data.endswith(b"\n"):
        fails.append("no-final-newline")
    lines = data.split(b"\n")
    if lines and lines[-1] == b"":
        lines = lines[:-1]
    if any(ln == b"" for ln in lines):
        fails.append("blank-line")
    objs = []
    for ln in lines:
        try:
            o = json.loads(ln.decode("utf-8"))
        except (UnicodeDecodeError, ValueError):
            fails.append("invalid-json-line")
            break
        if not isinstance(o, dict):
            fails.append("non-object-line")
            break
        objs.append(o)
    else:
        n_prefix = len([ln for ln in prefix.split(b"\n") if ln != b""])
        gate_objs = objs[n_prefix:]
        if len(gate_objs) != w:
            fails.append("gate-lines=%d/%d" % (len(gate_objs), w))
        if any(o.get("schema") != SCHEMA for o in gate_objs):
            fails.append("schema")
        if any("schema" in o for o in objs[:n_prefix]):
            fails.append("prefix-glued")
    return fails


def run_trial(gate, base, rng, k, kind, locked, ref_rc):
    root, rec = make_root(base, rng, k)
    manifest = os.path.join(root, "m%08x.jsonl" % rng.getrandbits(32))
    seed = seed_bytes(kind, rng)
    with open(manifest, "wb") as f:
        f.write(seed)
    ino = os.stat(manifest).st_ino
    prefix = seed
    fails = []
    w = W_L if locked else W_F
    procs = []
    try:
        if locked:
            fd = os.open(manifest, os.O_WRONLY | os.O_APPEND)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX)
                procs = launch(gate, rec, root, manifest, w)
                deadline = time.time() + LOCK_DEADLINE_S
                while True:
                    exited = sum(p.poll() is not None for p in procs)
                    if exited + waiters_on(ino) >= w:
                        break
                    if time.time() > deadline:
                        fails.append("lock-deadline")
                        break
                    time.sleep(0.2)
                with open(manifest, "rb") as f:
                    if f.read() != seed:
                        fails.append("appended-under-cooperating-lock")
                # the counter is itself a cooperating appender: on an empty or
                # terminated seed it writes one unterminated fragment under its lock;
                # an unterminated seed is left as it is. Either way the next writer
                # finds an unterminated last line once the lock is released.
                if kind != "unterminated":
                    frag = json.dumps({"frag": rng.getrandbits(30)}).encode()
                    os.write(fd, frag)
                    prefix = seed + frag
            finally:
                fcntl.flock(fd, fcntl.LOCK_UN)
                os.close(fd)
        else:
            procs = launch(gate, rec, root, manifest, w)
        rcs = wait_exit(procs, time.time() + WRITER_DEADLINE_S)
        if any(r is None for r in rcs):
            fails.append("writer-deadline")
        elif any(r != ref_rc for r in rcs):
            fails.append("writer-rc=%s" % ",".join(str(r) for r in sorted(set(rcs))))
        fails += check_manifest(manifest, ino, prefix, w)
    finally:
        kill_all(procs)
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="tools/research-gate.sh")
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--receipt", default=None)
    a = ap.parse_args()
    seed = a.seed if a.seed is not None else int.from_bytes(os.urandom(8), "big")
    gate = os.path.abspath(a.gate)
    if not os.path.isfile(gate):
        print("c1-count: gate not found: %s" % gate, file=sys.stderr)
        return 2
    if not os.path.isfile("/proc/locks"):
        print("c1-count: /proc/locks unavailable", file=sys.stderr)
        return 2
    rng = random.Random(seed)
    tbase = os.environ.get("C1_TMP") or tempfile.gettempdir()
    try:
        base = tempfile.mkdtemp(prefix="chousa-r32-c1-", dir=tbase)
    except OSError as e:
        print("c1-count: temp dir: %s" % e, file=sys.stderr)
        return 2
    t0 = time.time()
    trials = []
    try:
        # solo reference run: the exit code every writer must reproduce
        root, rec = make_root(base, rng, 99)
        try:
            p = subprocess.run(["bash", gate, "verify-all", rec, "--root", root, "--json",
                                os.path.join(root, "ref.jsonl")], cwd=root, env=gate_env(),
                               capture_output=True, timeout=WRITER_DEADLINE_S)
            ref_rc = p.returncode
        except subprocess.TimeoutExpired:
            ref_rc = None
        if ref_rc not in (0, 1):
            print("c1-count: solo reference run exited %r" % (ref_rc,), file=sys.stderr)
            return 2
        plan = [("L", kind) for kind in L_SEEDS] + [("F", "unterminated")] * F_TRIALS
        rng.shuffle(plan)
        for k, (typ, kind) in enumerate(plan):
            try:
                fails = run_trial(gate, base, rng, k, kind, typ == "L", ref_rc)
            except OSError as e:
                print("c1-count: trial %d harness error: %r" % (k, e), file=sys.stderr)
                return 2
            trials.append({"trial": k, "type": typ, "seed_kind": kind, "pass": not fails, "fails": fails})
    finally:
        shutil.rmtree(base, ignore_errors=True)
    matched = sum(t["pass"] for t in trials)
    holds = matched == TOTAL
    per = {}
    for t in trials:
        key = "%s_%s" % (t["type"], t["seed_kind"])
        pc = per.setdefault(key, [0, 0])
        pc[1] += 1
        pc[0] += t["pass"]
    print("APPEND_SERIALIZED=%d/%d" % (matched, TOTAL))
    for key in sorted(per):
        print("  %s %d/%d" % (key, per[key][0], per[key][1]))
    if a.receipt:
        receipt = {
            "schema": "chousa-r32-c1-receipt/v1",
            "counter_sha256": sha256_file(os.path.abspath(__file__)),
            "gate": a.gate, "gate_sha256": sha256_file(gate), "seed": seed, "ref_rc": ref_rc,
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)), "elapsed_s": round(time.time() - t0, 3),
            "total": TOTAL, "matched": matched, "label": "APPEND_SERIALIZED=%d/%d" % (matched, TOTAL),
            "predicate_holds": holds, "per_class": {k: "%d/%d" % tuple(v) for k, v in per.items()},
            "trials": trials,
        }
        try:
            with open(a.receipt, "w") as f:
                json.dump(receipt, f, indent=1)
                f.write("\n")
        except OSError as e:
            print("c1-count: --receipt failed: %r" % (e,), file=sys.stderr)
            return 2
    return 0 if holds else 1


if __name__ == "__main__":
    sys.exit(main())
