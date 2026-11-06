#!/usr/bin/env python3
"""Round-82 C1 gate mutation tester (R82MutationGate).

Each mutant is one (old -> new) replacement in an isolated hardlinked tree of
b4a41d251b488f06b4a6ab01a11bc12ce72edd20. The detector is the frozen counter
`corpus/evidence/round82/k2-gate-r82.py --root <tree>`; a mutant is KILLED when
the counter's per-row verdicts change from the pristine baseline (all ok, PASS).
Bytes are restored after every probe and sha256 is re-checked.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import subprocess
import sys

ROOT = "/fast/scratch/hyaku/chousa-r82/R82MutationGate"
GATE = "tools/research-gate.sh"
COUNTER = "corpus/evidence/round82/k2-gate-r82.py"
PRISTINE = None  # loaded from root tree


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


MUTANTS = [
    ("MG01-drop-na", "drop `n/a` from the closed placeholder list",
     "|n/a|na|n.a|", "|na|n.a|"),
    ("MG02-drop-none", "drop `none` from the closed placeholder list",
     "|none|nil|", "|nil|"),
    ("MG03-drop-tbd", "drop `tbd` from the closed placeholder list",
     "|tbd|tba|", "|tba|"),
    ("MG04-drop-unknown", "drop `unknown` from the closed placeholder list",
     "|x|unknown|'not applicable'", "|x|'not applicable'"),
    ("MG05-drop-qmark", "drop `?` from the closed placeholder list",
     "|'?'|'??'|", "|'??'|"),
    ("MG06-drop-emdash", "drop em-dash from the closed placeholder list",
     "'\u2014'|'\u2013'|", "'\u2013'|"),
    ("MG07-drop-period-strip", "drop the `while ... *.` trailing-period strip",
     "  while [[ $v == *. ]]; do v=${v%.}; done\n", ""),
    ("MG08-drop-backtick-fold", "drop backtick folding in sweep_is_placeholder",
     "v=${v//\\`/}; v=${v//\\\"/}", "v=${v//\\\"/}"),
    ("MG09-drop-dquote-fold", "drop double-quote folding in sweep_is_placeholder",
     "v=${v//\\\"/}; v=${v//\\'/}", "v=${v//\\'/}"),
    ("MG10-drop-squote-fold", "drop single-quote folding in sweep_is_placeholder",
     "v=${v//\\'/}; v=${v//\\*/}", "v=${v//\\*/}"),
    ("MG11-drop-star-fold", "drop `*` folding in sweep_is_placeholder",
     "v=${v//\\*/}; v=${v//_/}", "v=${v//_/}"),
    ("MG12-restrict-heading", "restrict the reject-heading match to `Rejections`",
     "[[ ${rsec,,} == *reject* ]] || continue", "[[ ${rsec,,} == rejections ]] || continue"),
    ("MG13-drop-placeholder-junk", "drop placeholder->junk in sweep_token_class",
     "  if sweep_is_placeholder \"$t\"; then printf 'junk'; return 0; fi\n", ""),
    ("MG14-drop-SW_CLAIMS", "drop the SW_CLAIMS claim_id resolution arm",
     "      [[ -n ${SW_CLAIMS[$ncid]+x} ]] && nres=1\n", ""),
    ("MG15-drop-SW_IDS-cid", "drop the SW_IDS[claim id] resolution arm",
     "      [[ $nres -eq 0 && -n ${SW_IDS[$ncid]+x} ]] && nres=1\n", ""),
    ("MG16-drop-token-match", "drop the sweep-cell token match (SW_IDS[token])",
     "          [[ -n $ntok && -n ${SW_IDS[$ntok]+x} ]] && { nres=1; break; }",
     "          :"),
    ("MG17-invert-nres", "invert nres: every negative claim resolves",
     "      nres=0\n", "      nres=1\n"),
    ("MG18-negative-info", "emit SWEEP_NEGATIVE_UNRESOLVED at severity info",
     "emit_finding SWEEP_NEGATIVE_UNRESOLVED warn sweeps",
     "emit_finding SWEEP_NEGATIVE_UNRESOLVED info sweeps"),
    ("MG19-reason-placeholder-absent", "reason placeholder no longer counts missing (`!= present` -> `== absent`)",
     "      [[ $rp != present ]] && miss=reason", "      [[ $rp == absent ]] && miss=reason"),
    ("MG20-flip-placeholder-absent", "flip placeholder no longer counts missing (`!= present` -> `== absent`)",
     "      [[ $fp != present ]] && miss=\"${miss:+$miss,}flip\"",
     "      [[ $fp == absent ]] && miss=\"${miss:+$miss,}flip\""),
    ("MG21-drop-placeholder-annotation", "drop the `placeholder=reason:..` annotation from the finding obs",
     "        [[ $rp == placeholder || $fp == placeholder ]] && robs+=\" placeholder=reason:$rp,flip:$fp\"\n",
     ""),
    ("MG23-drop-underscore-fold", "drop `_` folding in sweep_is_placeholder",
     "v=${v//\\*/}; v=${v//_/}", "v=${v//\\*/}"),
    ("MG22-read-Rejections-only", "read rejection rows with table_rows Rejections even under another heading",
     '    done < <(table_rows "$rsec")', "    done < <(table_rows Rejections)"),
]


def run_counter(tree):
    p = subprocess.run([sys.executable, "-B", os.path.join(tree, COUNTER),
                        "--root", tree], capture_output=True, text=True, timeout=1200)
    return p.returncode, p.stdout + p.stderr


def parse(out):
    rows, summary = {}, []
    for ln in out.splitlines():
        if ln.startswith("K2CASE "):
            kv = dict(part.split("=", 1) for part in ln.split() if "=" in part)
            rows[kv.get("id")] = kv
        elif ln.startswith(("RUNLINES=", "K2_GATE=")):
            summary.append(ln)
    return rows, summary


def probe(idx, mid, desc, old, new, baseline):
    tree = os.path.join(ROOT, "mut-trees", f"mu{idx:02d}")
    path = os.path.join(tree, GATE)
    pristine = open(os.path.join(ROOT, GATE), "rb").read()
    text = pristine.decode()
    n = text.count(old)
    if n != 1:
        return {"id": mid, "desc": desc, "error": f"anchor count={n}"}
    mutated = text.replace(old, new, 1).encode()
    tmp = path + ".new"
    with open(tmp, "wb") as fh:
        fh.write(mutated)
    os.replace(tmp, path)
    try:
        rc, out = run_counter(tree)
        rows, summary = parse(out)
        diff = sorted(k for k in set(rows) | set(baseline[0])
                      if rows.get(k, {}).get("verdict") != baseline[0].get(k, {}).get("verdict"))
        killed = rc != 0 or summary != baseline[1]
        return {"id": mid, "desc": desc, "rc": rc, "summary": summary,
                "killed": killed, "killer_rows": diff,
                "bad_rows": [k for k in diff if rows.get(k, {}).get("verdict") == "bad"],
                "mut_sha": hashlib.sha256(mutated).hexdigest()}
    finally:
        tmp = path + ".orig"
        with open(tmp, "wb") as fh:
            fh.write(pristine)
        os.replace(tmp, path)
        keep = open(path, "rb").read()
        if hashlib.sha256(keep).hexdigest() != hashlib.sha256(pristine).hexdigest():
            print(f"RESTORE FAILED {mid}", file=sys.stderr)
            sys.exit(3)


def main():
    only = sys.argv[1:]
    pristine = open(os.path.join(ROOT, GATE), "rb").read().decode()
    missing = [(m[0], pristine.count(m[2])) for m in MUTANTS if pristine.count(m[2]) != 1]
    if missing:
        print(json.dumps({"anchors_missing": missing}, indent=1))
        return 2
    rc, out = run_counter(ROOT)
    rows, summary = parse(out)
    baseline = (rows, summary)
    print(json.dumps({"baseline_rc": rc, "baseline_summary": summary,
                      "baseline_bad": [k for k, v in rows.items() if v.get("verdict") != "ok"]}))
    todo = [(i + 1, *m) for i, m in enumerate(MUTANTS) if not only or m[0] in only]
    res = []
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = [ex.submit(probe, *t, baseline) for t in todo]
        for f in cf.as_completed(futs):
            r = f.result()
            res.append(r)
            print(json.dumps(r))
    with open(os.path.join(ROOT, "gate-mutants.jsonl"), "w") as fh:
        for r in sorted(res, key=lambda x: x["id"]):
            fh.write(json.dumps(r) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
