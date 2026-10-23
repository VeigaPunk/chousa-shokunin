#!/usr/bin/env python3
"""Second round: escape-decoded id duplicates, NUL, malformed tokens, defaults."""
import json, os, subprocess

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r33/w2/ProbeDupVariants33"
ROOT = os.path.join(SCRATCH, "root")
SHA = "b373ef7a6591de3d1aa38a73ac3ab45d72d1e0fc951ed4fe4c376999d6d9cfb4"
GATES = {
    "base": os.path.join(SCRATCH, "base-gate.sh"),
    "landed": os.environ.get("LANDED_GATE", os.path.join(SCRATCH, "landed-gate-94a7be5a.sh")),
    "oracle": os.path.join(LANE, ".ufo/waves/round-33/controls/L1-design/oracle-gate.sh"),
}

PROBES = [
    # decoded-identical id spellings (must print the id, per the id-same rule)
    ("q01_id_escape_same", 'id "c1" and "\\u00631" (decodes to c1)', [
        '{"id": "c1", "id": "\\u00631", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("q02_id_nul_tail", 'id "c1" and "c1\\u0000" (differ by NUL)', [
        '{"id": "c1", "id": "c1\\u0000", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    # malformed token swallows a duplicate-looking member (invalid JSON)
    ("q03_num_swallow", 'number token swallows a duplicate-looking id (invalid JSON)', [
        '{"id": "c1", "note": 1"id": "c2", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("q04_bad_literal", 'value tru (not JSON)', [
        '{"id": "c1", "note": tru, "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("q05_dash_number", 'value - (not JSON)', [
        '{"id": "c1", "note": -, "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    # two counted keys duplicated, differing values
    ("q06_dup_id_and_source", 'id c1,c2 and source x2 (identical)', [
        '{"id": "c1", "id": "c2", "source": "src/a.txt", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    # duplicated null value on a counted key
    ("q07_dup_line_null", 'line "2" then null', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "line": null}']),
    # marker_default row with non-string duplicate value
    ("q08_md_dup_nonstring", 'marker_default string then 5', [
        '{"marker_default": "delta", "marker_default": 5}']),
    # duplicated marker_default row followed by a supported claim (default irrelevant)
    ("q09_md_dup_then_supported", 'duplicated marker_default row then a supported claim', [
        '{"marker_default": "delta", "marker_default": "nope"}',
        '{"id": "c9", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    # same line twice (scan cache) with a duplicate
    ("q10_same_line_twice", 'the same duplicated-id line twice in one file', [
        '{"id": "c1", "id": "c2", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}',
        '{"id": "c1", "id": "c2", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    # duplicate read key inside a nested container only, top-level has one (control)
    ("q11_nested_id_dup_top_ok", 'nested id twice inside one container, one top-level id', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "meta": {"id": "z1", "id": "z2"}}']),
    # duplicate counted key with an escaped string body carrying a quote+brace
    ("q12_dup_span_escaped_body", 'span twice, second body with escaped quote and brace', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "span": "a\\"}b", "expect": "supported", "line": "2"}']),
]


def run(gate, claims_path):
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("CHOUSA_"):
            del env[k]
    env["C1_TMP"] = os.path.join(SCRATCH, "tmp")
    env["TMPDIR"] = os.path.join(SCRATCH, "tmp")
    p = subprocess.run(["timeout", "120", "bash", gate, "verify-claims", claims_path,
                        "--root", ROOT], capture_output=True, text=True, env=env, timeout=140)
    return p.returncode, p.stdout, p.stderr


def summarize(rc, out):
    claims, findings, verdict = [], [], []
    for ln in out.splitlines():
        if ln.startswith("CLAIM "):
            claims.append(ln)
        elif ln.startswith("FINDING "):
            findings.append(ln)
        elif ln.startswith("RESEARCH_GATE: "):
            verdict.append(ln)
    return {"rc": rc, "claims": claims, "findings": findings, "verdict": verdict}


os.makedirs(os.path.join(SCRATCH, "probes2"), exist_ok=True)
outdir = os.path.join(SCRATCH, "probes2")
with open(os.path.join(SCRATCH, "summary2.txt"), "w") as sf:
    for name, note, lines in PROBES:
        cpath = os.path.join(outdir, name + ".jsonl")
        with open(cpath, "w") as f:
            f.write("\n".join(lines) + "\n")
        print("== %s  %s" % (name, note))
        sf.write("== %s  %s\n" % (name, note))
        for ln in lines:
            print("   in : %s" % ln)
            sf.write("   in : %s\n" % ln)
        for gname, gpath in GATES.items():
            rc, out, err = run(gpath, cpath)
            r = summarize(rc, out)
            with open(os.path.join(outdir, "%s.%s.out" % (name, gname)), "w") as f:
                f.write("EXIT=%d\n%s%s" % (rc, out, ("STDERR:\n" + err) if err else ""))
            line = "   %-6s rc=%d claims=%s findings=%s" % (gname, rc, r["claims"] or "-", r["findings"] or "-")
            print(line)
            sf.write(line + "\n")
print("saved:", os.path.join(SCRATCH, "summary2.txt"))
