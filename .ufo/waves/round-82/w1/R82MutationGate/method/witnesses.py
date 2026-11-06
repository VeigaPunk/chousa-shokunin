#!/usr/bin/env python3
"""Witness probes for the surviving gate mutants: the K2 form each would admit
(or the valid record each would refuse), run under pristine and mutated bytes."""
import hashlib
import importlib.util
import json
import os
import subprocess

ROOT = "/fast/scratch/hyaku/chousa-r82/R82MutationGate"
RECS = os.path.join(ROOT, "corpus/evidence/round82/c1-records")
OUTD = os.path.join(ROOT, "receipts")
spec = importlib.util.spec_from_file_location("gm", os.path.join(ROOT, "gate_mutants.py"))
gm = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gm)
INDEX = {m[0]: i + 1 for i, m in enumerate(gm.MUTANTS)}
ITEM2 = ('f={rec}; ! bash tools/research-gate.sh verify "$f" --root . | '
         "grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps \"$f\" --root .")
ITEM4 = "bash tools/research-gate.sh verify-sweeps {rec} --root ."

FLIP = "a fixture that quoted a citation-searching standard verbatim would flip this rejection"
BASE4 = "item4-pass.md"
BASE2 = "item2-pass.md"

# witness id -> (mutant, source record, [(old,new)...], run-line template, what it shows)
WITNESS = {
    "W1-flip-dquote": ("MG09-drop-dquote-fold", BASE4,
                       [(FLIP, '"n/a"')], ITEM4,
                       'a rejection whose flip cell is the double-quoted declared value "n/a"'),
    "W2-flip-squote": ("MG10-drop-squote-fold", BASE4,
                       [(FLIP, "'none'")], ITEM4,
                       "a rejection whose flip cell is the single-quoted declared value 'none'"),
    "W3-flip-star": ("MG11-drop-star-fold", BASE4,
                     [(FLIP, "*TBD*")], ITEM4,
                     "a rejection whose flip cell is the starred declared value *TBD*"),
    "W4-flip-underscore": ("MG23-drop-underscore-fold", BASE4,
                           [(FLIP, "n_a")], ITEM4,
                           "a rejection whose flip cell is n_a (declared value after `_` folding)"),
    "W5-resolve-claimid": ("MG14-drop-SW_CLAIMS", BASE2,
                           [("| observed-in-dump | W1 |", "| observed-in-dump | - |")], ITEM2,
                           "a negative claim with an empty sweep cell resolved by its Sweeps row claim_id"),
    "W6-resolve-ids-cid": ("MG15-drop-SW_IDS-cid", BASE2,
                           [("| N1 | negative |", "| W1 | negative |"),
                            ("| observed-in-dump | W1 |", "| observed-in-dump | - |")], ITEM2,
                           "a negative claim whose id is a declared Sweeps row id, empty sweep cell"),
    "W7-resolve-token": ("MG16-drop-token-match", BASE2,
                         [("| W1 | N1 | corpus/knowledge/*tarcis-r80*,corpus/knowledge/*tarcis-pre-r81* | zero matches |",
                           "| W1 | N7 | corpus/knowledge/*tarcis-r80*,corpus/knowledge/*tarcis-pre-r81* | zero matches |")],
                         ITEM2,
                         "a negative claim whose sweep cell names a declared sweep row id (claim_id differs)"),
    "W8-annotation": ("MG21-drop-placeholder-annotation", BASE4,
                      [(FLIP, "n/a")], ITEM4,
                      "the finding text for a placeholder flip cell (placeholder=... annotation)"),
}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def run_gate(tree, tmpl, rec, tag, mid):
    cmd = tmpl.format(rec=rec)
    p = subprocess.run(["bash", "-c", cmd], cwd=tree, capture_output=True, text=True, timeout=300)
    out = os.path.join(OUTD, f"witness-{mid}-{tag}.txt")
    with open(out, "w") as fh:
        fh.write(f"# cmd: {cmd}   (cwd={tree}, gate sha256={sha(open(os.path.join(tree,'tools/research-gate.sh'),'rb').read())})\n")
        fh.write(p.stdout)
        fh.write(p.stderr)
        fh.write(f"rc={p.returncode}\n")
    return p.returncode, p.stdout + p.stderr, out


def main():
    os.makedirs(OUTD, exist_ok=True)
    report = []
    for wid, (mid, base, subs, tmpl, note) in WITNESS.items():
        tree = os.path.join(ROOT, "mut-trees", f"mu{INDEX[mid]:02d}")
        src = open(os.path.join(RECS, base), encoding="utf-8").read()
        text = src
        for old, new in subs:
            assert text.count(old) == 1, (wid, old, text.count(old))
            text = text.replace(old, new, 1)
        rec = os.path.join(OUTD, f"witness-{wid}.md")
        open(rec, "w", encoding="utf-8").write(text)
        # pristine run
        rc0, out0, p0 = run_gate(tree, tmpl, rec, "pristine", wid)
        # mutated run
        path = os.path.join(tree, "tools/research-gate.sh")
        pristine = open(os.path.join(ROOT, "tools/research-gate.sh"), "rb").read()
        mut = next(m for m in gm.MUTANTS if m[0] == mid)
        mutated = pristine.decode().replace(mut[2], mut[3], 1).encode()
        open(path + ".new", "wb").write(mutated)
        os.replace(path + ".new", path)
        try:
            rc1, out1, p1 = run_gate(tree, tmpl, rec, "mutant", wid)
        finally:
            open(path + ".orig", "wb").write(pristine)
            os.replace(path + ".orig", path)
            assert sha(open(path, "rb").read()) == sha(pristine), mid
        recd = {"witness": wid, "mutant": mid, "note": note, "record": rec,
                "pristine_rc": rc0, "mutant_rc": rc1,
                "pristine_receipt": p0, "mutant_receipt": p1,
                "pristine_verdict": [l for l in out0.splitlines() if "RESEARCH_GATE:" in l or l.startswith("VERIFIED_SWEEPS")],
                "mutant_verdict": [l for l in out1.splitlines() if "RESEARCH_GATE:" in l or l.startswith("VERIFIED_SWEEPS")],
                "mutant_findings": [l for l in out1.splitlines() if l.startswith("FINDING")],
                "pristine_findings": [l for l in out0.splitlines() if l.startswith("FINDING")]}
        report.append(recd)
        print(json.dumps(recd))
    json.dump(report, open(os.path.join(ROOT, "witness-report.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
