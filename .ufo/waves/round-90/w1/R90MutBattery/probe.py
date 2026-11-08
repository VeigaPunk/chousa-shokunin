#!/usr/bin/env python3
"""R90MutBattery probe: one-point mutations of the round-90 instruments, frozen-predicate detectors."""
import hashlib
import json
import os
import shutil
import subprocess
import sys

S = "/fast/scratch/hyaku/chousa-r90/R90MutBattery"
T = os.path.join(S, "tree")
T283 = os.path.join(S, "tree283")
REPO = os.path.join(S, "lane-repo")
F = "8d9893b42eb22690ea5f920ab87fd7e1810b847a"
R = "9bad12011187d114ba2c4588c5df08a21ab28145"
SELFTEST = os.path.join(S, "receipts", "selftest-r90-uncaptured.txt")
PY = sys.executable


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def run(cmd, cwd=None):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1200)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


def log(name, cmdline, rc, out):
    d = os.path.join(S, "logs", name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "cmd.txt"), "w", encoding="utf-8") as fh:
        fh.write(cmdline + "\n")
    with open(os.path.join(d, "out.txt"), "w", encoding="utf-8") as fh:
        fh.write(out)
    return rc


def apply_edit(path, old, new, mid):
    src = open(path, encoding="utf-8").read()
    n = src.count(old)
    if n != 1:
        raise SystemExit(f"SETUP_MISS {mid}: anchor count={n} in {path}")
    body = src.replace(old, new, 1)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    return sha(path)


def restore(path, pristine_path):
    shutil.copy2(pristine_path, path)
    if sha(path) != sha(pristine_path):
        raise SystemExit(f"RESTORE_FAIL {path}")
    return sha(path)


def summarize(out):
    keys = ("CONTROL_DRIVER_R90=", "COMMITTED_OK=", "FORGERY_REFUSED=", "POSITIVE=",
            "CURATION_R90=", "LEGS_MEASURED=", "DETECTOR_WITNESS=", "MUTANTS_KILLED=",
            "STALE_TALLIES=", "TALLY_ROWS=", "FINDING")
    return [ln for ln in out.splitlines() if any(k in ln for k in keys)]


def main():
    res = {"c1": [], "c2": [], "c3": [], "baselines": {}}

    driver = os.path.join(REPO, "corpus/evidence/round90/control-driver-r90.py")
    driver_pristine = os.path.join(S, "pristine/control-driver-r90.py")
    c1_edits = {
        "M1-substring-token": (
            "        if want in toks:\n            if len(set(vals)) > 1:",
            "        if any(want in t for t in toks):\n            if len(set(vals)) > 1:"),
        "M2-skip-committed-read": (
            "        else:\n            text = open(path, encoding=\"utf-8\").read()\n            header = header_fields(text)",
            "        else:\n            _cmd = row[\"instrument\"].replace(\"@ROOT@\", root).replace(\"@WORK@\", work)\n"
            "            _frc, text = run_instrument(_cmd, root)\n"
            "            header = header_fields(open(path, encoding=\"utf-8\").read())"),
        "M3-drop-pin": (
            "        pin = header.get(\"computed_against\", \"\")\n"
            "        if not REV_RE.fullmatch(pin):\n"
            "            codes.append(\"PIN_MISSING\")\n"
            "            this_pin = False\n"
            "        elif pin != a.rev:\n"
            "            codes.append(f\"PIN_MISMATCH:{pin}\")\n"
            "            this_pin = False\n"
            "        else:\n"
            "            this_pin = True",
            "        this_pin = True"),
        "M4-drop-records-predicate": (
            "    for pred in row[\"predicates\"]:",
            "    for pred in []:"),
        "M5-dupkey-unreachable": (
            "        if want in toks:\n            if len(set(vals)) > 1:",
            "        if want in toks:\n            if False:"),
        "M6-fresh-no-compare": (
            "        this_fresh = frc == row[\"exit\"]\n"
            "        if not this_fresh:\n"
            "            codes.append(f\"FRESH_EXIT:{frc}\")\n"
            "        fbody = f\"# case={row['case']}\\n# expected_exit={row['exit']}\\n# exit={frc}\\n\" + ftext\n"
            "        fcodes, _ftok, _fpred = check_body(row, fbody)\n"
            "        if fcodes:\n"
            "            codes += [f\"FRESH_{c}\" for c in fcodes]\n"
            "            this_fresh = False\n",
            "        this_fresh = True\n"),
        "M7-self-pin-no-drift": (
            "        if open(disk, \"rb\").read() != blob:\n            drift.append(rel)",
            "        if False:\n            drift.append(rel)"),
        "M8-check-body-empty-ok": (
            "    codes = []\n    toks, keys = body_tokens(text)",
            "    if not [ln for ln in text.splitlines() if not ln.startswith(\"#\")]:\n"
            "        return [], True, True\n"
            "    codes = []\n    toks, keys = body_tokens(text)"),
    }

    for mid, (old, new) in c1_edits.items():
        restore(driver, driver_pristine)
        pre = sha(driver)
        mh = apply_edit(driver, old, new, mid)
        rec = {"id": mid, "file": "corpus/evidence/round90/control-driver-r90.py",
               "sha_before": pre, "sha_mutant": mh}
        # behavior arm: verify without --repo (pin leg per receipt retained)
        cmd = [PY, "-B", driver, "verify", "--root", REPO, "--rev", F, "--receipts-rev", R,
               "--work", os.path.join(S, "work", f"mut-{mid}-norepo")]
        rc, out = run(cmd, cwd=REPO)
        rec["verify_norepo_rc"] = log(f"c1-{mid}-norepo", " ".join(cmd), rc, out)
        rec["verify_norepo"] = summarize(out)
        verify_pass = rc == 0 and "CONTROL_DRIVER_R90=PASS" in out
        # forgery battery
        cmd = [PY, "-B", os.path.join(REPO, "corpus/evidence/round90/control-forgeries-r90.py"),
               "--root", REPO, "--work", os.path.join(S, "work", f"mut-{mid}-d1b"), "--rev", F]
        frc, fout = run(cmd, cwd=REPO)
        rec["forgery_rc"] = log(f"c1-{mid}-forgeries", " ".join(cmd), frc, fout)
        rec["forgery"] = summarize(fout)
        forgery_ok = frc == 0 and "FORGERY_REFUSED=6/6" in fout and "POSITIVE=pass" in fout
        # pin arm: with --repo, no receipt tamper
        cmd = [PY, "-B", driver, "verify", "--root", REPO, "--repo", REPO, "--rev", F,
               "--receipts-rev", R, "--work", os.path.join(S, "work", f"mut-{mid}-repo")]
        prc, pout = run(cmd, cwd=REPO)
        rec["verify_repo_rc"] = log(f"c1-{mid}-repo", " ".join(cmd), prc, pout)
        rec["verify_repo"] = summarize(pout)
        rec["pin_arm"] = "SELF_DRIFT" if "SELF_DRIFT" in pout else ("PASS" if prc == 0 else f"OTHER_rc{prc}")
        rec["behavior_detector"] = "killed" if (not verify_pass or not forgery_ok) else "survived"
        rec["sha_restored"] = restore(driver, driver_pristine)
        res["c1"].append(rec)

    # M7's own detector: a drifted receipt byte must trip the pin; the mutant must not see it.
    receipt = os.path.join(REPO, "corpus/evidence/round90/controls/receipts/c3-before.txt")
    receipt_pristine = os.path.join(T, "corpus/evidence/round90/controls/receipts/c3-before.txt")
    assert sha(receipt) == sha(receipt_pristine), "clone receipt bytes != archive bytes"
    with open(receipt, "ab") as fh:
        fh.write(b"\n")
    base_cmd = [PY, "-B", driver, "verify", "--root", REPO, "--repo", REPO, "--rev", F,
                "--receipts-rev", R, "--work", os.path.join(S, "work", "pin-fixture-base")]
    brc, bout = run(base_cmd, cwd=REPO)
    log("c1-pin-fixture-pristine", " ".join(base_cmd), brc, bout)
    old, new = c1_edits["M7-self-pin-no-drift"]
    apply_edit(driver, old, new, "M7-self-pin-no-drift/fixture")
    mut_cmd = [PY, "-B", driver, "verify", "--root", REPO, "--repo", REPO, "--rev", F,
               "--receipts-rev", R, "--work", os.path.join(S, "work", "pin-fixture-mut")]
    mrc, mout = run(mut_cmd, cwd=REPO)
    log("c1-pin-fixture-mutant", " ".join(mut_cmd), mrc, mout)
    restore(driver, driver_pristine)
    restore(receipt, receipt_pristine)
    res["c1_pin_fixture"] = {
        "pristine_rc": brc, "pristine_self_drift": "SELF_DRIFT" in bout,
        "mutant_rc": mrc, "mutant_pass": mrc == 0 and "CONTROL_DRIVER_R90=PASS" in mout,
        "verdict": "killed" if (brc != 0 and "SELF_DRIFT" in bout and mrc == 0) else "inconclusive",
        "receipt_restored_sha": sha(receipt), "receipt_expected_sha": sha(receipt_pristine),
    }

    # ---------------- C2 ----------------
    cur = os.path.join(T, "corpus/evidence/round90/curation-r90.py")
    cur_pristine = os.path.join(S, "pristine/curation-r90.py")
    c2_edits = {
        "B1-witness-blind": (
            "    bad = [n for n, ok in rows if not ok]",
            "    bad = []"),
        "B2-fields-hold-ignores-witness": (
            "                   and not witness_bad)",
            "                   )"),
        "B3-witness-leg-forced-ok": (
            "    legs.append((\"WITNESS\", not witness_bad, f\"{witness_detail} bad={len(witness_bad)}\"))",
            "    legs.append((\"WITNESS\", True, f\"{witness_detail} bad={len(witness_bad)}\"))"),
        "B4-verdict-preleg-snapshot": (
            "    prior_ok = all(ok for _, ok, _ in legs)",
            "    prior_ok = all(ok for _, ok, _ in legs[:-1])"),
        "B5-warrant-share-dropped": (
            "            if qids and len(resolved) == len(qids) and shares:",
            "            if qids:"),
        "B6-detector-witness-constant": (
            "          f\"DETECTOR_WITNESS={witness_detail}\")",
            "          f\"DETECTOR_WITNESS=8/8\")"),
    }
    for mid, (old, new) in c2_edits.items():
        restore(cur, cur_pristine)
        pre = sha(cur)
        mh = apply_edit(cur, old, new, mid)
        rec = {"id": mid, "file": "corpus/evidence/round90/curation-r90.py",
               "sha_before": pre, "sha_mutant": mh}
        cmd = [PY, "-B", cur, "--root", T]
        rc, out = run(cmd)
        rec["counter_rc"] = log(f"c2-{mid}-counter", " ".join(cmd), rc, out)
        rec["counter"] = summarize(out)
        counter_ok = rc == 0 and "CURATION_R90=PASS" in out
        cmd = [PY, "-B", os.path.join(T, "corpus/evidence/round90/curation-r90-mutants.py"),
               "--root", T, "--work", os.path.join(S, "work", f"mut-{mid}-c2mut")]
        mrc, mout = run(cmd)
        rec["mutants_rc"] = log(f"c2-{mid}-mutants", " ".join(cmd), mrc, mout)
        rec["mutants"] = summarize(mout)
        mutants_ok = mrc == 0 and "MUTANTS_KILLED=10/10" in mout
        cmd = [PY, "-B", os.path.join(T, "corpus/evidence/round90/curation-r90-controls.py"),
               "--root", T, "--work", os.path.join(S, "work", f"mut-{mid}-c2ctl")]
        crc, cout = run(cmd)
        rec["controls_rc"] = log(f"c2-{mid}-controls", " ".join(cmd), crc, cout)
        rec["controls"] = summarize(cout)
        controls_ok = crc == 0 and "CONTROLS=PASS FORGERY_REFUSED=7/7 PRIOR_REGRESSION=7/7" in cout
        rec["detector"] = "killed" if (not counter_ok or not mutants_ok or not controls_ok) else "survived"
        rec["leg_fail_lines"] = [ln for ln in (out + mout + cout).splitlines() if ln.startswith("LEG_FAIL")]
        rec["sha_restored"] = restore(cur, cur_pristine)
        res["c2"].append(rec)

    # ---------------- C3 ----------------
    tally = os.path.join(T, "corpus/evidence/round90/skill-tally-r90.py")
    tally283 = os.path.join(T283, "corpus/evidence/round90/skill-tally-r90.py")
    tally_pristine = os.path.join(S, "pristine/skill-tally-r90.py")
    c3_edits = {
        "C1-current-widened-to-every-occurrence": (
            "    def current(line):\n        lead = line.lstrip()\n"
            "        return lead.startswith(\"| `research-gate\") or \"Selftest `PASS (\" in line",
            "    def current(line):\n        return True"),
        "C2-expected-count-read-from-file": (
            "    stale = [(n, s) for n, s in rows if (int(n), int(s)) != (cases, skipped)]",
            "    if rows:\n        cases, skipped = int(rows[0][0]), int(rows[0][1])\n"
            "    stale = [(n, s) for n, s in rows if (int(n), int(s)) != (cases, skipped)]"),
    }
    for mid, (old, new) in c3_edits.items():
        restore(tally, tally_pristine)
        restore(tally283, tally_pristine)
        pre = sha(tally)
        mh = apply_edit(tally, old, new, mid)
        mh2 = apply_edit(tally283, old, new, mid)
        assert mh == mh2
        rec = {"id": mid, "file": "corpus/evidence/round90/skill-tally-r90.py",
               "sha_before": pre, "sha_mutant": mh}
        # leg 1: the unrepaired 9bad1201 tree must stay FAIL 9/9
        cmd = [PY, "-B", tally, "--root", T, "--selftest", SELFTEST]
        rc, out = run(cmd)
        rec["tree275_rc"] = log(f"c3-{mid}-tree275", " ".join(cmd), rc, out)
        rec["tree275"] = summarize(out)
        ok275 = rc == 1 and "STALE_TALLIES=9/9" in out and "EXPECTED_CASES=283" in out
        # leg 2: the discriminating tree283 must PASS 0/9
        cmd = [PY, "-B", tally283, "--root", T283, "--selftest", SELFTEST]
        rc2, out2 = run(cmd)
        rec["tree283_rc"] = log(f"c3-{mid}-tree283", " ".join(cmd), rc2, out2)
        rec["tree283"] = summarize(out2)
        ok283 = rc2 == 0 and "TALLY_ROWS=9 STALE_TALLIES=0/9 EXPECTED_CASES=283 EXPECTED_SKIPPED=0 OTHER_OCCURRENCES=3" in out2
        rec["detector"] = "killed" if (not ok275 or not ok283) else "survived"
        rec["sha_restored"] = restore(tally, tally_pristine)
        rec["sha_restored_283"] = restore(tally283, tally_pristine)
        res["c3"].append(rec)

    with open(os.path.join(S, "logs", "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2)
    print(json.dumps({k: (v if not isinstance(v, list) else
                          [{kk: vv for kk, vv in r.items() if kk in ("id", "detector", "behavior_detector", "pin_arm")} for r in v])
                      for k, v in res.items()}, indent=2))


if __name__ == "__main__":
    main()
