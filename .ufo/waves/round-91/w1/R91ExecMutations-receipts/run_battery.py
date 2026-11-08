#!/usr/bin/env python3
"""Round-91 mutation battery (seat R91ExecMutations). Copies only; the lane clone is never edited."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r91/R91ExecMutations"
REPO = os.path.join(S, "repo")
FIX = os.path.join(S, "fix", "landing")
W = os.path.join(S, "w")
R91 = "corpus/evidence/round91"
R90 = "corpus/evidence/round90"

MUTANTS = {
    # id: (instrument, detector family, [(old, new), ...])
    "M1": ("control-driver-r91.py", "c1", [
        ("        if len(vals) > 1:\n            codes.append(f\"HEADER_DUPLICATE:",
         "        if len(vals) > 1 and False:\n            codes.append(f\"HEADER_DUPLICATE:")]),
    "M2": ("control-driver-r91.py", "c1", [
        ("    \"\"\"R3/R6: every instrument a row executes, and the expectations file, are pinned and unchanged on disk.\"\"\"\n    codes = []",
         "    \"\"\"R3/R6: every instrument a row executes, and the expectations file, are pinned and unchanged on disk.\"\"\"\n    return [], 0\n    codes = []")]),
    "M3": ("control-driver-r91.py", "c1", [
        ("    for f in sorted(os.listdir(a.receipts)):\n        if not f.endswith(\".txt\") or f[:-4] in scored:",
         "    for f in ():\n        if not f.endswith(\".txt\") or f[:-4] in scored:")]),
    "M4": ("control-driver-r91.py", "c1", [
        ("HEADER_KEYS = (\"case\", \"expected_exit\", \"exit\", \"computed_against\")",
         "HEADER_KEYS = (\"case\", \"exit\", \"computed_against\")")]),
    "M5": ("curation-r91.py", "c2", [
        ("    \"\"\"None when a Located-quotes row is `Qn | S-id | non-empty quote`, else the reason (R1).\"\"\"\n    if len(cells) != 3:",
         "    \"\"\"None when a Located-quotes row is `Qn | S-id | non-empty quote`, else the reason (R1).\"\"\"\n    return None\n    if len(cells) != 3:")]),
    "M6": ("curation-r91.py", "c2", [
        ("    cells = reg.get(sid)\n    if cells is None:\n        return False, False",
         "    cells = reg.get(sid)\n    return True, True\n    if cells is None:\n        return False, False")]),
    "M7": ("curation-r91.py", "c2", [("DF_MAX = 3", "DF_MAX = 99")]),
    "M8": ("curation-r91.py", "c2", [
        ("            for term in unentailed_terms(cells, joined):\n                unentailed.append((rel, cells[0], term))",
         "            for term in DEFECT_TERMS:\n                if unentailed_terms(cells, joined):\n                    unentailed.append((rel, cells[0], term))")]),
    "M9": ("skill-tally-r91.py", "c3", [
        ("    derived_env = (min(bashenv), max(bashenv)) if bashenv else None\n    derived_ovr = (min(bashpin), max(bashpin)) if bashpin else None",
         "    derived_env = claimed_env if claimed_env is not None else ((min(bashenv), max(bashenv)) if bashenv else None)\n    derived_ovr = claimed_ovr if claimed_ovr is not None else ((min(bashpin), max(bashpin)) if bashpin else None)")]),
    "M10": ("skill-tally-r91.py", "c3", [
        ("    ok_ranges = not range_codes and claimed_env == derived_env and claimed_ovr == derived_ovr",
         "    ok_ranges = True")]),
    "M11": ("control-driver-r91.py", "c1", [
        ("    normlines = [\" \".join(ln.split()) for ln in lines]", "    normalized_lines = [\" \".join(ln.split()) for ln in lines]"),
        ("            if not any(phrase in ln for ln in normlines):", "            if not any(phrase in ln for ln in normalized_lines):")]),
}


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def build(mid):
    dst = os.path.join(S, "mut", mid)
    shutil.rmtree(dst, ignore_errors=True)
    for rel in (R91, R90):
        shutil.copytree(os.path.join(REPO, rel), os.path.join(dst, rel))
    return dst


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def main():
    os.makedirs(W, exist_ok=True)
    results = []
    pristine = {f: sha(os.path.join(REPO, R91, f)) for f in
                ("control-driver-r91.py", "curation-r91.py", "skill-tally-r91.py")}
    for mid in sorted(MUTANTS, key=lambda m: int(m[1:])):
        inst, fam, edits = MUTANTS[mid]
        bundle = build(mid)
        path = os.path.join(bundle, R91, inst)
        before = sha(path)
        text = open(path, encoding="utf-8").read()
        for old, new in edits:
            if text.count(old) != 1:
                raise SystemExit(f"{mid}: pattern count {text.count(old)} for {old[:50]!r}")
            text = text.replace(old, new)
        open(path, "w", encoding="utf-8").write(text)
        after = sha(path)
        work = os.path.join(W, mid)
        shutil.rmtree(work, ignore_errors=True)
        det_cmd = None
        direct_cmd = None
        if fam == "c1":
            det_cmd = [sys.executable, "-B", os.path.join(bundle, R91, "control-forgeries-r91.py"),
                       "--work", work]
            direct_cmd = [sys.executable, "-B", path, "verify", "--root", REPO, "--work", work + "-v",
                          "--rev", "4d00d7519290569879f853d7122b82a927cda1f3",
                          "--receipts-rev", "67954adc599bd605705d94a1ea7abb582491a907",
                          "--expected", os.path.join(REPO, R91, "controls", "expected.tsv"),
                          "--receipts", os.path.join(REPO, R91, "controls", "receipts"),
                          "--pins", os.path.join(REPO, R91, "instrument-pins.txt")]
        elif fam == "c2":
            det_cmd = [sys.executable, "-B", os.path.join(bundle, R91, "curation-r91-controls.py"),
                       "--root", REPO, "--work", work]
            direct_cmd = [sys.executable, "-B", path, "--root", REPO]
        else:
            det_cmd = [sys.executable, "-B", os.path.join(bundle, R91, "skill-tally-r91-controls.py"),
                       "--root", FIX, "--work", work]
            direct_cmd = [sys.executable, "-B", path, "--root", FIX,
                          "--selftest", os.path.join(FIX, R91, "controls", "selftest-r91.txt")]
        rc, out = run(det_cmd)
        drc, dout = run(direct_cmd)
        det_ok = (rc == 0 and ("FORGERY_REFUSED=6/6" in out or "CONTROLS=PASS" in out))
        restore = shutil.copy2(os.path.join(REPO, R91, inst), path)
        restored = sha(path)
        results.append({
            "mutant": mid, "instrument": inst, "family": fam,
            "edits": [{"old": o, "new": n} for o, n in edits],
            "sha_pristine": before, "sha_mutant": after, "sha_restored": restored,
            "detector_cmd": " ".join(det_cmd), "detector_rc": rc,
            "detector_ok": det_ok, "verdict": "killed" if not det_ok else "survived",
            "detector_out": out,
            "direct_cmd": " ".join(direct_cmd), "direct_rc": drc, "direct_out": dout,
        })
        print(f"{mid} {inst} detector_rc={rc} detector_ok={det_ok} -> "
              f"{'KILLED' if not det_ok else 'SURVIVED'} direct_rc={drc}")
    open(os.path.join(W, "results.json"), "w", encoding="utf-8").write(json.dumps(results, indent=1))
    killed = sum(1 for r in results if r["verdict"] == "killed")
    print(f"MUTANTS_KILLED={killed}/{len(results)} SURVIVORS={len(results) - killed}/{len(results)} "
          f"{'/'.join(r['mutant'] for r in results if r['verdict'] == 'survived')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
