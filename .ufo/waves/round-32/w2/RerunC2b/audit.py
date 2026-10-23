#!/usr/bin/env python3
"""RerunC2b hidden-truth audit: kept fixtures -> base gate (all-resolved) + landed gate (original)."""
import importlib.util, json, os, re, subprocess, sys

D = "/fast/scratch/hyaku/chousa-r32/w2/RerunC2b"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
spec = importlib.util.spec_from_file_location("c2v2", LANE + "/corpus/evidence/round32/c2-count-v2.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

FIND_RE = re.compile(r"^FINDING (\S+) severity=\S+ surface=\S+ obs=hop=(\S+)(?:\s|$)")
CHAIN_FULL = re.compile(r"^CHAIN hop=(\S+) status=(\S+) observed=(\S+) .*verdict=(\S+)")

env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
env["TMPDIR"] = D + "/tmpA"
os.makedirs(D + "/tmpA", exist_ok=True)


def run_gate(gate, record, root):
    p = subprocess.run(["bash", gate, "verify-chain", record, "--root", root],
                       capture_output=True, text=True, timeout=180, cwd=root, env=env)
    return p.returncode, p.stdout, p.stderr


def parse(out):
    ch = {}; findings = {}; drift = 0; resolved_line = None; summary = None
    for line in out.splitlines():
        if line.startswith("RESEARCH_GATE:"):
            drift += 1; summary = line
        elif line.startswith("RESOLVED_HOPS="):
            resolved_line = line
        f = FIND_RE.match(line)
        if f: findings.setdefault(f.group(2), []).append(f.group(1))
        c = CHAIN_FULL.match(line)
        if c: ch.setdefault(c.group(1), []).append({"observed": c.group(3), "verdict": c.group(4), "line": line})
    return ch, findings, drift, resolved_line, summary


def rewrite_resolved(record, dest):
    out = []; in_chain = False; n = 0
    for ln in open(record).read().splitlines():
        if ln.startswith("## "):
            in_chain = ln.startswith("## Chain"); out.append(ln); continue
        if in_chain and ln.startswith("| "):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if cells[0] == "hop" or set(cells[0]) <= {"-"}:
                out.append(ln); continue
            if len(cells) >= 7:
                cells[5] = "resolved"; n += 1
                out.append("| " + " | ".join(cells) + " |"); continue
        out.append(ln)
    open(dest, "w").write("\n".join(out) + "\n")
    return n


VER_CLS = ("R1", "R2", "R3", "F1", "E5")
report = {}
for tag, seed in (("A", 15123522876773114482), ("B", 12633912059466704036)):
    root = f"{D}/keep{tag}/root"
    troot, trecord, truth = m.generate(f"{D}/truth{tag}", seed)
    tblob = open(trecord).read()
    krecs = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f)) and open(os.path.join(root, f)).read() == tblob]
    assert len(krecs) == 1, (tag, krecs)
    record = os.path.join(root, krecs[0])
    E = {h for h, (c, t) in truth.items() if c.split("_")[0].startswith("E")}
    exp_ver = {h for h, (c, t) in truth.items() if c.split("_")[0] in VER_CLS}
    resrec = os.path.join(root, f"allresolved-{krecs[0]}")
    nrew = rewrite_resolved(record, resrec)

    # --- BASE gate, all-resolved record ---
    rc_b, out_b, err_b = run_gate(D + "/baselane/tools/research-gate.sh", resrec, root)
    open(f"{D}/base-{tag}.out", "w").write(out_b)
    ch, fin, drift_b, rl_b, summ_b = parse(out_b)
    got_ver = {h for h, ls in ch.items() if any(l["verdict"] == "match" for l in ls)}
    base_res = {
        "rc": rc_b, "rewrote": nrew, "resolved_line": rl_b, "summary": summ_b,
        "drift_lines": drift_b,
        "verified_count": len(got_ver), "expected_count": len(exp_ver),
        "verified_minus_expected": sorted(got_ver - exp_ver),
        "expected_minus_verified": sorted(exp_ver - got_ver),
        "dup_chain_lines": sorted(h for h, ls in ch.items() if len(ls) != 1),
        "unclassified": {h: ls for h, ls in ch.items()
                         if h not in exp_ver and all(l["verdict"] == "match" for l in ls)},
        "nonmatch_verdicts": {},
    }
    for h, ls in ch.items():
        if h not in got_ver:
            for l in ls:
                key = l["observed"] + "/" + l["verdict"]
                base_res["nonmatch_verdicts"].setdefault(key, []).append(h)
    base_res["nonmatch_verdicts"] = {k: len(v) for k, v in base_res["nonmatch_verdicts"].items()}
    base_res["truth_of_extra"] = {h: truth.get(h) for h in sorted(got_ver - exp_ver)}
    base_res["stderr_head"] = err_b[:400]

    # --- LANDED gate, original kept record ---
    rc_l, out_l, err_l = run_gate(D + "/lane/tools/research-gate.sh", record, root)
    open(f"{D}/landed-{tag}.out", "w").write(out_l)
    ch2, fin2, drift_l, rl_l, summ_l = parse(out_l)
    bad_E = {}
    for h in E:
        obs = [l["observed"] for l in ch2.get(h, [])]
        fns = fin2.get(h, [])
        if obs != ["exempt"] or fns:
            bad_E[h] = {"obs": obs, "findings": fns, "cls": truth[h][0]}
    bad_other = {}
    for h, (c, t) in truth.items():
        if h in E: continue
        obs = [l["observed"] for l in ch2.get(h, [])]
        fns = fin2.get(h, [])
        want_obs = ["resolvable"] if t == "resolvable" else ["verified"]
        want_f = 1 if t == "resolvable" else 0
        if obs != want_obs or len(fns) != want_f or (want_f and fns != ["CHAIN_EXEMPT_RESOLVABLE"]):
            bad_other[h] = {"cls": c, "obs": obs, "findings": fns}
    stray_fin = {h: fns for h, fns in fin2.items() if h not in truth}
    landed_res = {
        "rc": rc_l, "drift_lines": drift_l, "resolved_line": rl_l, "summary": summ_l,
        "chain_hops": len(ch2), "dup_chain_lines": sorted(h for h, ls in ch2.items() if len(ls) != 1),
        "E_total": len(E), "E_bad": bad_E,
        "nonE_bad": bad_other, "stray_finding_hops": stray_fin,
        "resolvable_findings": sum(1 for h, fns in fin2.items() if h in truth and truth[h][1] == "resolvable"),
        "stderr_head": err_l[:400],
    }
    report[tag] = {"record": krecs[0], "record_byte_match": True, "base": base_res, "landed": landed_res}
    print(f"=== run {tag} seed={seed} record={krecs[0]} rewrote={nrew}")
    print(" BASE rc=%s %s | verified=%d expected=%d extra=%s missing=%s dup=%s" % (
        rc_b, rl_b, len(got_ver), len(exp_ver),
        base_res["verified_minus_expected"], base_res["expected_minus_verified"], base_res["dup_chain_lines"]))
    print(" BASE summary: %s" % summ_b)
    print(" BASE nonmatch verdict histogram: %s" % base_res["nonmatch_verdicts"])
    print(" LANDED rc=%s drift=%d hops=%d E_bad=%d nonE_bad=%d stray=%s resolvable_findings=%d" % (
        rc_l, drift_l, len(ch2), len(bad_E), len(bad_other), stray_fin, landed_res["resolvable_findings"]))
    print(" LANDED summary: %s" % summ_l)
    if bad_E: print(" LANDED E_bad:", json.dumps(bad_E, indent=1)[:2000])
    if bad_other: print(" LANDED nonE_bad:", json.dumps(bad_other, indent=1)[:2000])

open(f"{D}/audit-results.json", "w").write(json.dumps(report, indent=1))
