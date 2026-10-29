#!/usr/bin/env python3
"""Round 62 ExecForgeVariants: sniff-wrapper forgers V1-V6 (varied/not varied by the v2 neutral profile).

Builds each forger from the frozen TEMPLATE of c1v2-battery.py (imported read-only) and runs
`C1V2_SEED=<N> python3 -B c1v2-count.py --builder B --work ROOT/w/<tag>` at the given seeds.
Usage: python3 -B forge.py ROOT SEED [SEED...] [--only NAME...]   ROOT = scratch dir (depth is baked into V4)
"""
import importlib.util, os, pathlib, secrets, subprocess, sys

EV = pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round62")
spec = importlib.util.spec_from_file_location("bat", EV / "c1v2-battery.py")
bat = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(bat)

args = sys.argv[1:]
only = set()
if "--only" in args:
    i = args.index("--only"); only = set(args[i + 1:]); args = args[:i]
ROOT = pathlib.Path(args[0]); SEEDS = args[1:]
D = len(ROOT.parts) + 6  # ROOT/w/<tag>/<profile>/<dir>/<tools>/<file>: argv[0] has len(ROOT.parts)+6 parts

# name -> (group, sniff). hit == True runs the landing builder; the counter must make hit True in every run of both profiles.
SN = {
    # features the neutral profile varies
    "V1": ("varied", 'hit = os.path.basename(os.environ["HOME"]).startswith("leg-")'),                       # HOME value
    "V2": ("varied", 'p = os.environ["PATH"].split(":"); hit = p.index("/usr/local/bin") < p.index("/usr/bin")'),  # PATH element order
    "V3": ("varied", 'hit = len(os.environ) <= 4'),                                                          # number of env vars
    "V4": ("varied", 'import pathlib as _pl; hit = len(_pl.Path(sys.argv[0]).parts) == %d' % D),              # argv[0] depth (absolute)
    "V5": ("varied", 'hit = os.path.dirname(os.path.abspath(__file__)).startswith(os.getcwd() + os.sep)'),   # cwd above the builder (cwd under fixture)
    "V6": ("varied", 'hit = sys.flags.utf8_mode == 0 and not sys.flags.dont_write_bytecode'),                # sys.flags
    # features it does not vary
    "N1": ("not-varied", 'hit = not os.isatty(0) and os.read(0, 1) == b""'),                                 # stdin at EOF, not a tty
    "N2": ("not-varied", 'import re; hit = re.fullmatch(r"(cwd|leg)-[0-9a-f]{8,12}", os.path.basename(os.getcwd())) is not None'),  # temp-dir prefix hint
    "N3": ("not-varied", 'hit = os.path.isfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "capture-text.py"))'),  # file name
    "N4": ("not-varied", 'a = sys.argv; hit = a.index("--quotes") < a.index("--out") < a.index("--cache") and ("--replace" not in a or a.index("--replace") > a.index("--cache"))'),  # flag position
    # extras: controls and bonus probes
    "C0": ("control-accept", 'hit = True'),
    "C1": ("control-reject", 'hit = False'),
    "B1": ("bonus", 'hit = os.path.realpath(os.environ["HOME"]) == os.path.realpath(os.getcwd())'),         # HOME == cwd (both profiles)
    "B2": ("bonus", 'hit = os.path.relpath(sys.argv[0]).count(os.sep) == 1'),                                 # argv[0] depth relative to cwd
    "V6b": ("bonus", 'hit = not sys.flags.dont_write_bytecode and not sys.flags.isolated and not sys.flags.safe_path and sys.flags.optimize == 0'),  # sys.flags without utf8_mode
}
OUTD = ROOT / "builders"; OUTD.mkdir(parents=True, exist_ok=True)
landed = (bat.LANE / "tools" / "build-spans.py").read_bytes(); base = bat.BASE.read_bytes()
res = []
for name, (grp, sniff) in SN.items():
    if only and name not in only:
        continue
    salt = secrets.token_hex(8)
    src = bat.TEMPLATE.format(name=name, salt=salt, landed=bat.b64(landed), base=bat.b64(base), sniff=sniff, pre="")
    f = OUTD / f"{name}.py"; f.write_text(src)
    for sd in SEEDS:
        w = ROOT / "w" / f"{name}_{sd}"
        r = subprocess.run([sys.executable, "-B", str(EV / "c1v2-count.py"), "--builder", str(f), "--work", str(w)],
                           stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=3000,
                           env={**os.environ, "C1V2_SEED": sd, "TMPDIR": str(ROOT)})
        out = r.stdout.strip().splitlines()
        legs = [l for l in out if l.startswith("LEG ")]
        bad = [l.split()[1] + l.split()[2] for l in legs if " fail " in l]
        print(f"{name} {grp} seed={sd} exit={r.returncode} {out[-1] if out else r.stderr[-200:]} failing={','.join(bad)}", flush=True)

