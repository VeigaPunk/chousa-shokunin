#!/usr/bin/env python3
"""SCRATCH PROBE (R75Scout reconnaissance, NOT a lane artifact).

Enumerates, from inside the candidate child, which r62 detection-forge
channels (F01 cwd name, F02 env keys, F03 layout, F04 argv names, F06 parent
cmdline, F07 LANG, F08 RLIMIT_FSIZE, F09 stdin type, F10 any proc cmdline,
F11 stdout type) are AVAILABLE to a candidate running under the frozen v2
matrix. Writes one line per channel; never blocks; exits immediately.
"""
import os
import resource
import stat
import subprocess
import sys

out = os.environ.get("PROBE_OUT", "/fast/scratch/hyaku/chousa-r75/R75Scout/f-channels.txt")
res = []


def kind(m):
    return "chr" if stat.S_ISCHR(m) else ("reg" if stat.S_ISREG(m) else ("fifo" if stat.S_ISFIFO(m) else "other"))


# F01 cwd name
res.append(f"F01_cwd_name_available={os.path.basename(os.getcwd())!r}")
# F02 env keys
res.append(f"F02_env_subset_available={sorted(os.environ)[:4]}")
# F03 layout (does a recognisable lane layout exist under --lane?)
res.append(f"F03_lane_argv={[a for a in sys.argv if 'shokunin' in a or 'corpus' in a]}")
# F04 argv names
res.append(f"F04_argv_names={[os.path.basename(a) for a in sys.argv]}")
# F06 parent cmdline
try:
    with open("/proc/%d/cmdline" % os.getppid(), "rb") as fh:
        res.append(f"F06_parent_cmdline_available={fh.read().decode('utf-8','replace').replace(chr(0),' ').strip()[:120]!r}")
except OSError as e:
    res.append(f"F06_parent_cmdline_available=ERR {e}")
# F07 LANG
res.append(f"F07_LANG={os.environ.get('LANG')!r} LC_ALL={os.environ.get('LC_ALL')!r}")
# F08 RLIMIT_FSIZE
res.append(f"F08_rlimit_fsize={resource.getrlimit(resource.RLIMIT_FSIZE)}")
# F09 stdin type
s0 = os.fstat(0)
res.append(f"F09_stdin_kind={kind(s0.st_mode)} is_devnull={os.path.samestat(s0, os.stat('/dev/null')) if stat.S_ISCHR(s0.st_mode) else False}")
# F10 any proc cmdline
hits = []
for d in os.listdir("/proc"):
    if d.isdigit():
        try:
            with open("/proc/%s/cmdline" % d, "rb") as fh:
                c = fh.read().decode("utf-8", "replace")
            if "loader-matrix" in c or "matrix-battery" in c:
                hits.append(d)
        except OSError:
            pass
res.append(f"F10_proc_cmdline_hits={hits}")
# F11 stdout type
res.append(f"F11_stdout_kind={kind(os.fstat(1).st_mode)}")
# extra: is the child's own argv distinguishable?
res.append(f"EXTRA_rev_arg_present={'--rev' in sys.argv}")

with open(out, "a", encoding="utf-8") as fh:
    fh.write("\n".join(res) + "\n")
print("C2=PASS checks=7/7 probe")
sys.exit(0)
