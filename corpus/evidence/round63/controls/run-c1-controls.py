#!/usr/bin/env python3
"""R63-C1 controls — shows `../c1-battery.py` discriminates, before any claim is frozen.

Runs the battery on (a) the reference preflight `pos-ref-preflight.py` (expected BATTERY=PASS), (b) four do-nothing or
forger tools (`null-pass.py`, `null-fail.py`, `null-diff-oracle.py`, `null-selfreport.py`) and (c) single-defect mutants
M01..M16 of the reference (expected BATTERY=FAIL, with the legs named that must fail), plus an absent tool.
Prints `NAME rc=<n> <battery verdict line> <failing legs> OK|UNEXPECTED`. M11 is an equivalent mutant (the selftest
exit code already carries the verdict) and is expected to SURVIVE; it is printed as `SURVIVED-expected`.

Usage: python3 run-c1-controls.py --work DIR [--jobs N] [--only NAME[,NAME]]   (DIR absent or empty; removed at the end)
"""
import argparse
import concurrent.futures
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
BAT = HERE.parent / "c1-battery.py"
REF = HERE / "pos-ref-preflight.py"
FLEET = HERE.parents[3].parent


def mutants(src: str):
    def sub(old, new, n=1):
        assert src.count(old) == n, (old, src.count(old))
        return src.replace(old, new)

    M = {
        "M01-first-fail-only": (sub('            print(f"GATE {gid} {name} {st} {detail}")\n',
                                    '            print(f"GATE {gid} {name} {st} {detail}")\n            if st == "FAIL":\n                for g2, n2 in GATES[GATES.index((gid, name)) + 1:]:\n                    print(f"GATE {g2} {n2} SKIP")\n                    res[g2] = "SKIP"\n                break\n'), {"D11"}),
        "M02-g03-always-pass": (sub('return ("PASS", f"{len(files)} lessons carry ## Gate") if not bad else', 'return ("PASS", "x") if True else'), {"D06", "D14"}),
        "M03-env-is-pass": (sub('return "ENV", "no sources-census.sh', 'return "PASS", "no sources-census.sh'), {"D12"}),
        "M04-skip-silent": (sub('                print(f"GATE {gid} {name} SKIP")\n', ''), {"CLEAN", "D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "D11", "D12", "D14", "B01", "B02", "B03", "B04", "B05", "B06"}),
        "M05-summary-counts-skip": (sub("sum(res[g] == 'PASS' for g in ran)}/{len(ran)}", "sum(res[g] == 'PASS' for g in ran)}/{len(IDS)}"), {"CLEAN", "D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "D11", "D12", "D14", "B01", "B02", "B03", "B04", "B05", "B06"}),
        "M06-exit-always-0": (sub("    return 1 if failed else (2 if envs else 0)", "    return 0"), {"D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "D11", "D12", "D14"}),
        "M07-no-line-suffix-strip": (sub('        w = re.sub(r":\\d+(-\\d+)?$", "", w)\n', ''), {"B04"}),
        "M08-g02-readme-exists-only": (sub('    miss = [f for f in files if f not in readme]\n', '    miss = []\n'), {"D04", "D05"}),
        "M09-g01-ignores-census": (sub('    return ("PASS", f"exit=0 census_findings=0") if p.returncode == 0 else', '    return ("PASS", "x") if True else'), {"D01", "D02", "D03", "D11"}),
        "M10-g06-ignores-exit": (sub('    if p.returncode != 0:\n        return "FAIL", f"exit={p.returncode}"\n    if token and token not in p.stdout:', '    if token and token not in p.stdout:'), {"D09"}),
        "M11-g07-no-token": (sub('    if token and token not in p.stdout:\n        return "FAIL", f"exit=0 but no `{token}` line"\n', ''), set()),
        "M12-g05-all-tables": (sub('            on = line.startswith("## Capabilities")\n', '            on = True\n'), {"CLEAN", "D01", "D02", "D03", "D04", "D05", "D06", "D07", "D09", "D10", "D11", "D12", "B01", "B02", "B03", "B04", "B05", "B06"}),
        "M13-only-ignored": (sub('            if (only and gid not in only) or gid in skip:', '            if gid in skip:'), {"D14"}),
        "M14-usage-accepts-unknown": (sub('    if bad:\n        print(f"lane-preflight: unknown gate id for {flag}: {\',\'.join(bad)}", file=sys.stderr)\n        raise SystemExit(2)\n', '    pass\n'), {"D13"}),
        "M15-g03-exact-heading": (sub('r"^## Gate\\b"', 'r"^## Gate\\s*$"'), {"CLEAN", "D01", "D02", "D03", "D04", "D05", "D07", "D08", "D09", "D10", "D11", "D12", "B01", "B02", "B04", "B05", "B06"}),
        "M16-g04-first-word-only": (sub('    words = [w for m in re.finditer(r"`([^`\\n]+)`", read(f)) for w in path_words(m.group(1))]\n', '    words = [next(iter(path_words(m.group(1))), "SHONEN.md") for m in re.finditer(r"`([^`\\n]+)`", read(f))]\n'), {"D15"}),
    }
    return M


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--only", default=None)
    a = ap.parse_args()
    w = pathlib.Path(a.work)
    if w.exists() and any(w.iterdir()):
        print("work must be absent or empty", file=sys.stderr)
        return 2
    w.mkdir(parents=True, exist_ok=True)
    src = REF.read_text(encoding="utf-8")
    jobs = [("positive-ref", REF, "PASS", None), ("absent-tool", w / "no-such-tool.py", "FAIL", None)]
    for n in ("null-pass", "null-fail", "null-diff-oracle", "null-selfreport"):
        jobs.append((n, HERE / f"{n}.py", "FAIL", None))
    for name, (text, legs) in mutants(src).items():
        p = w / f"{name}.py"
        p.write_text(text, encoding="utf-8")
        jobs.append((name, p, "PASS" if name == "M11-g07-no-token" else "FAIL", legs))
    if a.only:
        keep = set(a.only.split(","))
        jobs = [j for j in jobs if j[0] in keep]

    def go(j):
        name, tool, expect, legs = j
        wk = w / ("run-" + name)
        p = subprocess.run([sys.executable, "-B", str(BAT), "--tool", str(tool), "--work", str(wk), "--fleet", str(FLEET)],
                           capture_output=True, text=True)
        lines = p.stdout.splitlines()
        verdict = next((l for l in lines if l.startswith("CLEAN=")), p.stderr.strip()[:120])
        failing = sorted(l.split()[1] for l in lines if l.startswith("LEG ") and " FAIL " in l)
        got = "PASS" if "BATTERY=PASS" in verdict else "FAIL"
        ok = got == expect
        if expect == "FAIL" and legs:
            ok = ok and legs <= set(failing)
        tag = "OK" if ok else "UNEXPECTED"
        if name == "M11-g07-no-token" and ok:
            tag = "SURVIVED-expected"
        return name, p.returncode, verdict, failing, tag, ok

    with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:
        res = list(ex.map(go, jobs))
    for name, rc, verdict, failing, tag, ok in res:
        print(f"{name:28s} rc={rc} {verdict} legs_failing={','.join(failing) or '-'} {tag}")
    bad = sum(not r[5] for r in res)
    print(f"C1_CONTROLS_UNEXPECTED={bad}")
    shutil.rmtree(w, ignore_errors=True)
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
