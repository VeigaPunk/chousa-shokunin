#!/usr/bin/env python3
"""R87MutCounter driver — one-point mutation probes for the two round-87 counters and the subject tool."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = "/fast/scratch/hyaku/chousa-r87/R87MutCounter"
L = os.path.join(S, "land")
REPO = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
GATE = os.path.join(L, "corpus/evidence/round87/gate-records-r87.py")
CUR = os.path.join(L, "corpus/evidence/round87/curation-r87.py")
TOOL = os.path.join(L, "tools/gate-records.py")
POS = os.path.join(L, "corpus/evidence/round87/c1-positives.tsv")
OUT = os.path.join(S, "receipts")
os.makedirs(OUT, exist_ok=True)

C1_KEYS = ["TOOL", "POSITIVE", "FRESH_POSITIVE", "FORGED_REFUSED", "EXPECTED_CODE", "EMPTY_REFUSED", "RC",
           "SETUP", "D1_EXPECTED", "D1_FORGES", "D1_REFUSED", "D2_FORGES", "D2_REFUSED",
           "MUT_ADMIT_DERIVED", "MUT_ADMIT_KILLED", "MUT_UNREACH_DERIVED", "MUT_UNREACH_KILLED",
           "DERIVE_NEG", "LEGS"]
C2_KEYS = ["SUPERSEDED_LIVE", "UNENTAILED_TERM", "MODIFIED_DEF_CITED", "QUOTES_LOCATED", "WARRANT_OK",
           "TEACHES_FLAGGED", "TEACHES_UNRESOLVED", "LEGS"]


def fields(stdout, prefix=None):
    d = {}
    for ln in stdout.splitlines():
        if ln.startswith("CURATION_R87=") or ln.startswith("GATE_RECORDS_R87="):
            continue
        toks = ln.split()
        if not toks or "=" not in toks[0]:
            continue
        if prefix and not toks[0].startswith(prefix):
            continue
        for t in toks:
            if "=" in t:
                k, v = t.split("=", 1)
                d[k] = v
    return d


def verdict(stdout):
    for ln in stdout.splitlines():
        if ln.startswith("GATE_RECORDS_R87=") or ln.startswith("CURATION_R87="):
            return ln
    return "no-verdict"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(cmd, work=None, env=None):
    e = dict(os.environ)
    e["TMPDIR"] = work or S
    if env:
        e.update(env)
    p = subprocess.run(cmd, capture_output=True, text=True, env=e)
    return p.returncode, p.stdout, p.stderr


def write_receipt(name, text):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return path


def apply_mutant(src_path, old, new, dst):
    src = open(src_path, encoding="utf-8").read()
    if src.count(old) != 1:
        return None
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(src.replace(old, new, 1))
    return dst


def c1_verdict(stdout, rc, base):
    got = fields(stdout)
    deviations = [f"{k}: want {base[k]} got {got.get(k)}" for k in C1_KEYS if got.get(k) != base[k]]
    return rc == 0 and verdict(stdout) == "GATE_RECORDS_R87=PASS" and not deviations, deviations


def c2_verdict(stdout, rc, base):
    got = fields(stdout)
    deviations = [f"{k}: want {base[k]} got {got.get(k)}" for k in C2_KEYS if got.get(k) != base[k]]
    return rc == 0 and verdict(stdout) == "CURATION_R87=PASS" and not deviations, deviations


def main():
    gate_sha_before, cur_sha_before, tool_sha_before = sha(GATE), sha(CUR), sha(TOOL)
    rc, out, err = run([sys.executable, "-B", GATE, "--root", L, "--repo", REPO, "--work", os.path.join(S, "work/b")])
    c1_base = fields(out)
    write_receipt("c1-pristine-landing.txt",
                  f"cmd: python3 -B {GATE} --root {L} --repo {REPO} --work {S}/work/b\nrc={rc}\n{out}{err}")
    rc2, out2, err2 = run([sys.executable, "-B", CUR, "--root", L])
    c2_base = fields(out2)
    write_receipt("c2-pristine-landing.txt", f"cmd: python3 -B {CUR} --root {L}\nrc={rc2}\n{out2}{err2}")

    c1_mutants = [
        ("A1-d2-class-emptied", "        d2 = build_d2_203_rejects(root)", "        d2 = []"),
        ("A2-code-credit-blind", "                    if code in v[1]:", "                    if True:"),
        ("A3-expected-legs-14", "EXPECTED_LEGS = 15", "EXPECTED_LEGS = 14"),
        ("A4-freshok-hardcode", "            ffiles = []", "            fresh_ok = 5\n            ffiles = []"),
        ("A5-unreach-mutant-wrong-shape",
         'if build_mutant(tool, mu, UNREACH_LITERAL, \'kv["http"] == "200"\'):',
         'if build_mutant(tool, mu, UNREACH_LITERAL, \'kv["http"] != "200"\'):'),
        ("A6-pok-hardcode", "            fresh_files = []", "            p_ok = len(pos)\n            fresh_files = []"),
        ("A8-setupok-hardcode",
         "            setup_ok = 1 if (p.returncode == 2 and \"GATE_RECORDS_ERROR\" in p.stderr) else 0",
         "            setup_ok = 1"),
        ("A7-admit-mutant-noop",
         "if build_mutant(tool, ma, ADMIT_LITERAL, 'r[6].startswith(\"2\")'):",
         "if build_mutant(tool, ma, ADMIT_LITERAL, 'r[6] == \"200\"'):"),
    ]
    c2_mutants = [
        ("B1-floor-drop", "floors_ok = all(loc >= fl and loc == tot for _rel, loc, tot, fl in floor_rows)",
         "floors_ok = all(loc == tot for _rel, loc, tot, fl in floor_rows)"),
        ("B2-total-only-located",
         "            total += 1\n            cap = capture_text(root, reg, sid)\n"
         "            if cap is not None and norm(quote) in cap:\n                located += 1",
         "            cap = capture_text(root, reg, sid)\n"
         "            if cap is not None and norm(quote) in cap:\n                total += 1\n                located += 1"),
        ("B3-warrant-drop-shares", "            if qids and len(resolved) == len(qids) and shares:",
         "            if qids and len(resolved) == len(qids):"),
        ("B4-teaches-dead-detector",
         "        miss = [t for t in named if cap is None or t not in cap.lower()]", "        miss = []"),
        ("B5-def-cited-leg-dropped",
         '    legs.append(("DEF_CITED", modified_def_cited >= 1, str(modified_def_cited)))\n',
         ''),
        ("B6-entries-narrowed",
         '    "corpus/knowledge/provenance-recording-r85.md",\n', ""),
        ("B7-floor-raised", '"corpus/knowledge/search-transparency-reporting-r84.md": 13,',
         '"corpus/knowledge/search-transparency-reporting-r84.md": 20,'),
        ("B8-warrant-dead-detector", "            if qids and len(resolved) == len(qids) and shares:",
         "            if True:"),
    ]
    tool_mutants = [
        ("T3-unreach-203",
         '        success = kv["curl_rc"] == "0" and 200 <= int(kv["http"]) < 300',
         '        success = kv["curl_rc"] == "0" and kv["http"] == "203"'),
        ("T4-admit-lt-300",
         'r[5] == "0" and r[6] == "200" and capsha is not None',
         'r[5] == "0" and int(r[6]) < 300 and capsha is not None'),
        ("T5-calendar-check-deleted",
         '        if not re.fullmatch(r"https?://\\S+", kv["url"]) or not TS_RE.fullmatch(kv["fetched"]) or not _valid_ts(kv["fetched"]):',
         '        if not re.fullmatch(r"https?://\\S+", kv["url"]) or not TS_RE.fullmatch(kv["fetched"]):'),
        ("T6-git-blob-empty", "        return b.stdout if b.returncode == 0 else None", '        return b""'),
    ]

    results = []
    tmp = tempfile.mkdtemp(prefix="drive-", dir=S)
    try:
        # ---- C1 counter mutants ----
        for i, (mid, old, new) in enumerate(c1_mutants):
            d = os.path.join(tmp, "c1-" + mid)
            os.makedirs(d)
            shutil.copy2(POS, os.path.join(d, "c1-positives.tsv"))
            mp = os.path.join(d, "gate-records-r87.py")
            if apply_mutant(GATE, old, new, mp) is None:
                results.append({"id": mid, "kind": "c1-counter", "status": "SETUP_MISS", "detail": "anchor"})
                continue
            exe = os.path.join(tmp, "w1-" + mid)
            os.makedirs(exe)
            rc, out, err = run([sys.executable, "-B", mp, "--root", L, "--repo", REPO, "--work", exe])
            ok, dev = c1_verdict(out, rc, c1_base)
            status = "KILLED" if not ok else "SURVIVOR"
            body = (f"mutant: {mid}\nfile: corpus/evidence/round87/gate-records-r87.py\n"
                    f"anchor-replaced:\n---\n{old}\n---\nwith:\n---\n{new}\n---\n"
                    f"cmd: python3 -B {mp} --root {L} --repo {REPO} --work {exe}\nrc={rc}\n"
                    f"verdict={verdict(out)}\nfield-deviations={dev}\n"
                    f"leg-fails:\n" + "\n".join(l for l in out.splitlines() if l.startswith(("LEG_FAIL", "WRONG_CODE", "NOT_REFUSED", "MUT_", "SETUP_MISS"))) + "\n"
                    f"stdout-tail:\n" + "\n".join(out.splitlines()[-3:]) + "\n"
                    f"stderr-tail:\n" + "\n".join(err.splitlines()[-6:]) + "\n"
                    f"mutant-sha256={sha(mp)}\n")
            write_receipt(f"c1-mut-{mid}.txt", body)
            results.append({"id": mid, "kind": "c1-counter", "status": status, "rc": rc,
                            "verdict": verdict(out), "deviations": dev,
                            "legfails": [l for l in out.splitlines() if l.startswith("LEG_FAIL")],
                            "receipt": f"receipts/c1-mut-{mid}.txt"})

        # ---- C2 counter mutants ----
        for mid, old, new in c2_mutants:
            d = os.path.join(tmp, "c2-" + mid)
            os.makedirs(d)
            mp = os.path.join(d, "curation-r87.py")
            if apply_mutant(CUR, old, new, mp) is None:
                results.append({"id": mid, "kind": "c2-counter", "status": "SETUP_MISS", "detail": "anchor"})
                continue
            rc, out, err = run([sys.executable, "-B", mp, "--root", L])
            ok, dev = c2_verdict(out, rc, c2_base)
            status = "KILLED" if not ok else "SURVIVOR"
            body = (f"mutant: {mid}\nfile: corpus/evidence/round87/curation-r87.py\n"
                    f"anchor-replaced:\n---\n{old}\n---\nwith:\n---\n{new}\n---\n"
                    f"cmd: python3 -B {mp} --root {L}\nrc={rc}\nverdict={verdict(out)}\n"
                    f"field-deviations={dev}\n"
                    f"leg-fails:\n" + "\n".join(l for l in out.splitlines() if l.startswith("LEG_FAIL")) + "\n"
                    f"stdout:\n{out}\n")
            write_receipt(f"c2-mut-{mid}.txt", body)
            results.append({"id": mid, "kind": "c2-counter", "status": status, "rc": rc,
                            "verdict": verdict(out), "deviations": dev,
                            "legfails": [l for l in out.splitlines() if l.startswith("LEG_FAIL")],
                            "receipt": f"receipts/c2-mut-{mid}.txt"})

        # ---- subject tool mutants, caught by the pristine C1 counter ----
        for mid, old, new in tool_mutants:
            d = os.path.join(tmp, "t-" + mid)
            os.makedirs(d)
            mp = os.path.join(d, "gate-records.py")
            if apply_mutant(TOOL, old, new, mp) is None:
                results.append({"id": mid, "kind": "tool", "status": "SETUP_MISS", "detail": "anchor"})
                continue
            exe = os.path.join(tmp, "wt-" + mid)
            os.makedirs(exe)
            rc, out, err = run([sys.executable, "-B", GATE, "--root", L, "--repo", REPO,
                                "--tool", mp, "--work", exe])
            ok, dev = c1_verdict(out, rc, c1_base)
            status = "CAUGHT" if not ok else "UNCAUGHT"
            body = (f"tool-mutant: {mid}\nfile: tools/gate-records.py\n"
                    f"anchor-replaced:\n---\n{old}\n---\nwith:\n---\n{new}\n---\n"
                    f"cmd: python3 -B {GATE} --root {L} --repo {REPO} --tool {mp} --work {exe}\nrc={rc}\n"
                    f"verdict={verdict(out)}\nfield-deviations={dev}\n"
                    f"leg-fails:\n" + "\n".join(l for l in out.splitlines() if l.startswith(("LEG_FAIL", "WRONG_CODE", "NOT_REFUSED"))) + "\n"
                    f"mutant-sha256={sha(mp)}\n")
            write_receipt(f"tool-mut-{mid}.txt", body)
            results.append({"id": mid, "kind": "tool", "status": status, "rc": rc,
                            "verdict": verdict(out), "deviations": dev,
                            "legfails": [l for l in out.splitlines() if l.startswith("LEG_FAIL")],
                            "receipt": f"receipts/tool-mut-{mid}.txt"})

        gate_sha_after, cur_sha_after, tool_sha_after = sha(GATE), sha(CUR), sha(TOOL)
        restoration = {
            "gate_before": gate_sha_before, "gate_after": gate_sha_after,
            "cur_before": cur_sha_before, "cur_after": cur_sha_after,
            "tool_before": tool_sha_before, "tool_after": tool_sha_after,
            "identical": gate_sha_before == gate_sha_after and cur_sha_before == cur_sha_after
                         and tool_sha_before == tool_sha_after,
        }
        write_receipt("restoration.txt", json.dumps(restoration, indent=2) + "\n")
        print(json.dumps({"c1_base": c1_base, "c2_base": c2_base, "results": results,
                          "restoration": restoration}, indent=2))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
