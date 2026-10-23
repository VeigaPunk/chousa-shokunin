#!/usr/bin/env python3
"""Round 33 W2 ProbeDupVariants33: duplicate-form probes beyond c1-count-v2.py.

Each probe is one claims file (line(s) verbatim) run through three readers:
  base    : tools/research-gate.sh at 2b9cc73 (SHA f4731885...)
  landed  : tools/research-gate.sh at 0fb300b (SHA 94a7be5a...)
  oracle  : .ufo/waves/round-33/controls/L1-design/oracle-gate.sh (python json reader)
"""
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
SCRATCH = "/fast/scratch/hyaku/chousa-r33/w2/ProbeDupVariants33"
ROOT = os.path.join(SCRATCH, "root")
SHA = "b373ef7a6591de3d1aa38a73ac3ab45d72d1e0fc951ed4fe4c376999d6d9cfb4"
GATES = {
    "base": os.path.join(SCRATCH, "base-gate.sh"),
    "landed": os.environ.get("LANDED_GATE", os.path.join(SCRATCH, "landed-gate-94a7be5a.sh")),
    "oracle": os.path.join(LANE, ".ufo/waves/round-33/controls/L1-design/oracle-gate.sh"),
}

BASE_MEMBERS = '"id": "c1", "claim": "fixture claim", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"'


def rec(extra="", drop=()):
    parts = []
    for m in BASE_MEMBERS.split(", "):
        k = m.split(":")[0].strip().strip('"')
        if k not in drop:
            parts.append(m)
    if extra:
        parts.append(extra)
    return "{" + ", ".join(parts) + "}"


# (name, note, [lines])
PROBES = [
    ("p00_plain", "control: no nesting, no duplicate", [rec()]),

    # --- three or more occurrences ---
    ("p01_t3_line_same", 'line x3 identical "2"', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "line": "2", "line": "2"}']),
    ("p02_t3_line_223", 'line "2","2","3" (first two agree, third differs)', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "line": "2", "line": "3"}']),
    ("p03_t3_line_232", 'line "2","3","2"', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "line": "3", "line": "2"}']),
    ("p04_t3_id_112", 'id "c1","c1","c2"', [
        '{"id": "c1", "id": "c1", "id": "c2", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p05_t3_id_121", 'id "c1","c2","c1"', [
        '{"id": "c1", "id": "c2", "id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p06_t3_id_122", 'id "c1","c2","c2"', [
        '{"id": "c1", "id": "c2", "id": "c2", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p07_t3_span_sst", 'span s,s,t', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "span": "beta gamma", "span": "beta", "expect": "supported", "line": "2"}']),

    # --- duplicated marker ---
    ("p08_dup_marker_same", 'marker twice identical, expect=supported', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "marker": "M", "marker": "M"}']),
    ("p09_dup_marker_diff", 'marker twice differing, expect=supported', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "marker": "M", "marker": "N"}']),
    ("p10_dup_marker_contradicted", 'marker twice identical, expect=contradicted', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "contradicted", "line": "2", "marker": "M", "marker": "M"}']),

    # --- id duplicated with differing values ---
    ("p11_dup_id_diff", 'id "c1","c2"', [
        '{"id": "c1", "id": "c2", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p12_dup_id_same", 'id "c1","c1" (counted class control)', [
        '{"id": "c1", "id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p13_dup_id_second_nonstring", 'id "c1" then id 5', [
        '{"id": "c1", "id": 5, "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p14_dup_id_second_nested", 'id "c1" then id {"x":1}', [
        '{"id": "c1", "id": {"x": 1}, "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p15_dup_id_escaped_same", 'id "c1" and "\\u0063c1" (decoded identical)', [
        '{"id": "c1", "id": "\\u0063c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),

    # --- non-string duplicates ---
    ("p16_dup_line_num_first", 'line 5 then "2"', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": 5, "line": "2"}']),
    ("p17_dup_line_str_first", 'line "2" then 5', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "line": 5}']),
    ("p18_dup_line_both_num", 'line 5 then 5', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": 5, "line": 5}']),
    ("p19_dup_sha_num_first", 'sha256 123 then hex', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "sha256": 123, "sha256": "' + SHA + '"}']),
    ("p20_dup_expect_num_first", 'expect 5 then "supported"', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": 5, "expect": "supported", "line": "2"}']),

    # --- two different keys each duplicated ---
    ("p21_dup_two_src_span", 'source x2 and span x2 (identical values)', [
        '{"id": "c1", "source": "src/a.txt", "source": "src/a.txt", "span": "beta gamma", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p22_dup_two_line_sha", 'line x2 and sha256 x2', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "line": "2", "sha256": "' + SHA + '", "sha256": "' + SHA + '"}']),
    ("p23_dup_two_marker_line", 'marker x2 and line x2 (uncounted reason first in the loop order)', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "line": "2", "marker": "M", "marker": "M"}']),

    # --- duplicates in marker_default rows ---
    ("p24_md_dup_same", 'marker_default row, duplicated identical', [
        '{"marker_default": "delta", "marker_default": "delta"}']),
    ("p25_md_dup_diff", 'marker_default row, duplicated differing', [
        '{"marker_default": "delta", "marker_default": "nope"}']),
    ("p26_md_dup_then_contradicted", 'duplicated marker_default row then a contradicted claim that names no marker', [
        '{"marker_default": "delta", "marker_default": "nope"}',
        '{"id": "c9", "source": "src/a.txt", "span": "beta gamma", "expect": "contradicted", "line": "2"}']),
    ("p27_md_single_then_contradicted", 'control: single marker_default row then the same contradicted claim', [
        '{"marker_default": "delta"}',
        '{"id": "c9", "source": "src/a.txt", "span": "beta gamma", "expect": "contradicted", "line": "2"}']),
    ("p28_claim_with_dup_md", 'valid claim plus two marker_defaults (over-invalidation probe)', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "marker_default": "delta", "marker_default": "delta"}']),

    # --- duplicated unread keys: must stay valid ---
    ("p29_unread_dup_claim_same", 'claim x2 identical', [
        '{"id": "c1", "claim": "fixture claim", "claim": "fixture claim", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p30_unread_dup_claim_diff", 'claim x2 differing', [
        '{"id": "c1", "claim": "one", "claim": "two", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p31_unread_t3_note", 'note x3', [
        '{"id": "c1", "note": "a", "note": "b", "note": "c", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p32_unread_two_keys", 'claim x2 and meta x2 (nested objects)', [
        '{"id": "c1", "claim": "a", "claim": "b", "meta": {"line": "9"}, "meta": {"line": "8"}, "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p33_nested_dup_only", 'control: same-name members inside two nested objects only', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "a": {"line": "9"}, "b": {"line": "8"}}']),

    # --- string/structure confusables around duplicates ---
    ("p34_dup_span_mixed_types", 'span string then object', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "span": {"x": 1}, "expect": "supported", "line": "2"}']),
    ("p35_dup_source_escaped", 'source twice, second spelled with \\u0061 escape (decoded identical)', [
        '{"id": "c1", "source": "src/a.txt", "source": "src/\\u0061.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p36_dup_expect_same", 'expect x2 identical "supported"', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "expect": "supported", "line": "2"}']),
    ("p37_dup_md_and_id", 'marker_default x2 and id x2 (reason order probe)', [
        '{"id": "c1", "id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "marker_default": "delta", "marker_default": "delta"}']),
    ("p38_escaped_key_dup", 'id "c1" and "\\u0069d" "c2" (escaped key spelling: not claimed)', [
        '{"id": "c1", "\\u0069d": "c2", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2"}']),
    ("p39_dup_in_string_only", 'control: text that looks like members inside a string value', [
        '{"id": "c1", "source": "src/a.txt", "span": "beta gamma", "expect": "supported", "line": "2", "note": "\\"line\\": \\"3\\", \\"id\\": \\"zz\\""}']),
]


def run(gate, claims_path):
    env = dict(os.environ)
    for k in list(env):
        if k.startswith("CHOUSA_"):
            del env[k]
    env["C1_TMP"] = os.path.join(SCRATCH, "tmp")
    env["TMPDIR"] = os.path.join(SCRATCH, "tmp")
    p = subprocess.run(["timeout", "120", "bash", gate, "verify-claims", claims_path,
                        "--root", ROOT], capture_output=True, text=True, env=env,
                       timeout=140)
    return p.returncode, p.stdout, p.stderr


def summarize(rc, out):
    claims, findings, verdict = [], [], []
    for ln in out.splitlines():
        if ln.startswith("CLAIM "):
            claims.append(ln)
        elif ln.startswith("FINDING CLAIM_RECORD_INVALID") or ln.startswith("FINDING CLAIM_SOURCE") \
                or ln.startswith("FINDING CLAIM_SPAN") or ln.startswith("FINDING CLAIM_LINE_MISMATCH") \
                or ln.startswith("FINDING CONTRADICTION"):
            findings.append(ln)
        elif ln.startswith("RESEARCH_GATE: "):
            verdict.append(ln)
    return {"rc": rc, "claims": claims, "findings": findings, "verdict": verdict}


def main():
    os.makedirs(os.path.join(SCRATCH, "probes"), exist_ok=True)
    outdir = os.path.join(SCRATCH, "probes")
    table = []
    for name, note, lines in PROBES:
        cpath = os.path.join(outdir, name + ".jsonl")
        with open(cpath, "w") as f:
            f.write("\n".join(lines) + "\n")
        res = {}
        raw = {}
        for gname, gpath in GATES.items():
            rc, out, err = run(gpath, cpath)
            res[gname] = summarize(rc, out)
            raw[gname] = "EXIT=%d\n%s%s" % (rc, out, ("STDERR:\n" + err) if err else "")
            with open(os.path.join(outdir, "%s.%s.out" % (name, gname)), "w") as f:
                f.write(raw[gname])
        table.append((name, note, lines, res))
        print("== %s  %s" % (name, note))
        for ln in lines:
            print("   in : %s" % ln)
        for gname in GATES:
            r = res[gname]
            print("   %-6s rc=%d claims=%s findings=%s" % (
                gname, r["rc"], r["claims"] or "-", r["findings"] or "-"))
    with open(os.path.join(SCRATCH, "summary.txt"), "w") as f:
        for name, note, lines, res in table:
            f.write("== %s  %s\n" % (name, note))
            for ln in lines:
                f.write("   in : %s\n" % ln)
            for gname in GATES:
                r = res[gname]
                f.write("   %-6s rc=%d claims=%s findings=%s\n" % (
                    gname, r["rc"], r["claims"] or "-", r["findings"] or "-"))
    print("\nsaved:", os.path.join(SCRATCH, "summary.txt"))


if __name__ == "__main__":
    main()
