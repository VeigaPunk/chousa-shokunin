"""Resolve every write-mode open and mutating syscall in an `strace -f` trace to an absolute path.

Tracks per-pid cwd (chdir; inherited on clone/vfork) and per-pid fd->dir table (openat return values; inherited on
clone), so relative paths (git's `.git/logs/HEAD`, tar's `tools/...`) are attributed to where they landed.
Created-path rules: symlink/symlinkat classify the LINK path (the target string is data, not a written path);
link/linkat classify the NEW path; rename/renameat/renameat2 classify both the old (removed) and new paths.
Usage: attrib.py TRACE. The lane root category must be zero.
"""
import collections
import os
import re
import sys

T = sys.argv[1]
S = "/fast/scratch/hyaku/chousa-r97/R97SentinelC1"
R = S + "/repo"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
WRF = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")
MUT = {"unlink", "unlinkat", "rename", "renameat", "renameat2", "mkdir", "mkdirat", "rmdir", "symlink", "symlinkat",
       "link", "linkat", "truncate", "chmod", "fchmodat", "utimensat", "chown", "fchownat"}
INTEREST = {"openat", "open", "creat", "chdir", "close", "clone", "clone3", "vfork", "fork"} | MUT

cwd, fds, pending = {}, {}, {}
cnt = collections.Counter()
other = collections.Counter()
unres = collections.Counter()
lane_samples = []
lines = 0


def classify(kind, full):
    if full is None:
        unres[kind] += 1
        return
    if full == LANE or full.startswith(LANE + "/"):
        cnt["LANE " + kind] += 1
        if len(lane_samples) < 20:
            lane_samples.append(f"{kind} {full}")
    elif full == R or full.startswith(R + "/"):
        cnt["REPO(my clone) " + kind] += 1
    elif full.startswith(S + "/work-"):
        cnt["WORK(scratch) " + kind] += 1
    elif full.startswith("/dev/"):
        cnt["DEV " + kind] += 1
    else:
        cnt["OTHER " + kind] += 1
        other[full[:150]] += 1


def base_for(pid, dirfd):
    if dirfd is None or dirfd == "AT_FDCWD":
        return cwd.get(pid, R)
    return fds.get(pid, {}).get(int(dirfd))


def join(base, path):
    if path.startswith("/"):
        return os.path.normpath(path)
    if base is None:
        return None
    return os.path.normpath(os.path.join(base, path))


def resolve_at(pid, dirfd, path):
    base = base_for(pid, dirfd)
    if base is None and not path.startswith("/"):
        return None
    return join(base if base is not None else cwd.get(pid, R), path)


with open(T, "r", errors="replace") as fh:
    for raw in fh:
        lines += 1
        sp = raw.find(" ")
        if sp <= 0 or not raw[:sp].isdigit():
            continue
        pid = int(raw[:sp])
        body = raw[sp + 1:].rstrip("\n")
        if body.startswith("+++") or body.startswith("---"):
            continue
        if "<unfinished ...>" in body:
            pending[pid] = body.split(" <unfinished ...>")[0]
            continue
        if body.startswith("<... ") and " resumed>" in body:
            body = pending.pop(pid, "") + body.split(" resumed>", 1)[1]
        paren = body.find("(")
        if paren <= 0:
            continue
        name = body[:paren]
        if name not in INTEREST:
            continue
        rm = re.search(r"\) += (-?\d+)", body)
        ret = int(rm.group(1)) if rm else None
        if name in ("clone", "clone3", "vfork", "fork"):
            if ret and ret > 0:
                cwd[ret] = cwd.get(pid, R)
                fds[ret] = dict(fds.get(pid, {}))
                cnt["clone"] += 1
            continue
        if name == "chdir":
            if ret == 0:
                m = re.match(r'chdir\("([^"]*)"\)', body)
                if m:
                    cwd[pid] = join(cwd.get(pid, R), m.group(1))
            continue
        if name == "close":
            m = re.match(r"close\((\d+)\)", body)
            if m:
                fds.get(pid, {}).pop(int(m.group(1)), None)
            continue
        if name in ("openat", "open", "creat"):
            if ret is None or ret < 0:
                continue
            if name == "openat":
                m = re.match(r'openat\((AT_FDCWD|-?\d+), "([^"]*)", ([^)]*)\)', body)
                if not m:
                    continue
                full = resolve_at(pid, m.group(1), m.group(2))
                flags = m.group(3)
            else:
                m = re.match(r'(open|creat)\("([^"]*)"(?:, ([^)]*))?\)', body)
                if not m:
                    continue
                full = resolve_at(pid, "AT_FDCWD", m.group(2))
                flags = m.group(3) or ""
            fds.setdefault(pid, {})[ret] = full
            if any(f in flags for f in WRF):
                classify("write-open", full)
            continue
        if name not in MUT:
            continue
        if ret is not None and ret < 0:
            continue
        if name in ("symlink", "symlinkat"):
            # symlink(target, linkpath) / symlinkat(target, dirfd, linkpath): the target is data, not written.
            m = (re.match(r'symlink\("[^"]*", "([^"]*)"', body) if name == "symlink"
                 else re.match(r'symlinkat\("[^"]*", (AT_FDCWD|-?\d+), "([^"]*)"', body))
            if m:
                dirfd, path = ("AT_FDCWD", m.group(1)) if name == "symlink" else (m.group(1), m.group(2))
                classify("mut:" + name, resolve_at(pid, dirfd, path))
            continue
        if name in ("link", "linkat"):
            # link(old, new) / linkat(olddirfd, old, newdirfd, new, flags): classify the NEW path.
            m = (re.match(r'link\("[^"]*", "([^"]*)"', body) if name == "link"
                 else re.match(r'linkat\((?:AT_FDCWD|-?\d+), "[^"]*", (AT_FDCWD|-?\d+), "([^"]*)"', body))
            if m:
                dirfd, path = ("AT_FDCWD", m.group(1)) if name == "link" else (m.group(1), m.group(2))
                classify("mut:" + name, resolve_at(pid, dirfd, path))
            continue
        if name in ("rename", "renameat", "renameat2"):
            # rename(old, new) / renameat2(olddirfd, old, newdirfd, new, flags): both entries are modified.
            m = re.match(r'\w+\((?:(AT_FDCWD|-?\d+), )?"([^"]*)", (?:(AT_FDCWD|-?\d+), )?"([^"]*)"', body)
            if m:
                classify("mut:" + name, resolve_at(pid, m.group(1) or "AT_FDCWD", m.group(2)))
                classify("mut:" + name, resolve_at(pid, m.group(3) or "AT_FDCWD", m.group(4)))
            continue
        if name.endswith("at"):
            m = re.match(r'\w+\((AT_FDCWD|-?\d+), "([^"]*)"', body)
            if m:
                classify("mut:" + name, resolve_at(pid, m.group(1), m.group(2)))
            continue
        m = re.match(r'\w+\("([^"]*)"', body)
        if m:
            classify("mut:" + name, resolve_at(pid, "AT_FDCWD", m.group(1)))

print(f"TRACE={os.path.basename(T)} lines={lines}")
print("CATEGORY_COUNTS")
for k, v in sorted(cnt.items()):
    print(f"  {k}={v}")
print(f"UNRESOLVED {dict(unres)}")
print(f"CLONE_EVENTS={cnt.get('clone', 0)}")
print("LANE_SAMPLES(must be empty)")
for s in lane_samples:
    print("  " + s)
print("OTHER_TOP")
for k, v in other.most_common(25):
    print(f"  {v} {k}")
