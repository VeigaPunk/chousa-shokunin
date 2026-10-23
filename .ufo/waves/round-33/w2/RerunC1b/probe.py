#!/usr/bin/env python3
"""Minimal-input probes: does the landed gate obey the C1 contract on lines the
counter never generates? Each probe is one claims.jsonl line. Runs a named gate
(base or landed) and prints rc + CLAIM/FINDING lines."""
import json, os, subprocess, sys, shutil

BASE = "/fast/scratch/hyaku/chousa-r33/w2/RerunC1b/base-gate.sh"
LAND = "/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh"
ROOT = "/fast/scratch/hyaku/chousa-r33/w2/RerunC1b/probe-root"
HDR = '"id":"c1","source":"src/a.md","span":"SPAN","expect":"supported"'

PROBES = [
    ("p01_flat_ctrl", '{%s}' % HDR),
    ("p02_nested_line_obj", '{"meta":{"line":"9"},%s}' % HDR),
    ("p03_nested_line_arr", '{"meta":["junk",{"line":"9"}],%s}' % HDR),
    ("p04_dup_line_ident", '{%s,"line":"4","line":"4"}' % HDR),
    ("p05_dup_line_diff", '{%s,"line":"4","line":"5"}' % HDR),
    ("p06_str_confuser", '{"note":"fake \\"line\\": \\"9\\", { } [ ] :",%s}' % HDR),
    ("p07_str_trail_bslash", '{"note":"ends with a backslash \\\\",%s}' % HDR),
    # invalid JSON atoms (v2: "asked to fail closed"; no fixture counts them)
    ("p08_atom_unknown", '{"extra":truthy,%s}' % HDR),
    ("p09_atom_nested", '{"meta":{"x":truthy},%s}' % HDR),
    ("p12_trailing_garbage", '{%s} x' % HDR),
    ("p13_unknown_key_bracket", '{"we]ird":1,%s}' % HDR),
    ("p14_unknown_key_brace", '{"a}b":1,%s}' % HDR),
    ("p15_unknown_key_quote", '{"a\\"b":1,%s}' % HDR),
    ("p16_unknown_key_dollar", '{"$(touch PWNED)":1,%s}' % HDR),
    ("p17_dup_line_marker_default", '{"marker_default":"M","line":"1","line":"2"}'),
    ("p18_trailing_comma", '{%s,}' % HDR),
    ("p19_empty_key", '{"":1,%s}' % HDR),
    ("p20_obj_line_value", '{%s,"line":{"a":1}}' % HDR),
    ("p21_num_line_value", '{%s,"line":4}' % HDR),
    ("p22_dup_id_ident", '{%s,"id":"c1"}' % HDR),
    ("p23_nested_marker_only", '{"meta":{"marker":"M"},%s}' % HDR),
    ("p24_nested_sha_only", '{"meta":{"sha256":"deadbeef"},%s}' % HDR),
    ("p25_nested_expect_before", '{"meta":{"expect":"contradicted"},%s}' % HDR),
    ("p26_atom_read_field", '{"id":"c1","source":"src/a.md","span":"SPAN","expect":true}'),
    ("p27_utf8_values", '{"note":"caf\\u00e9 \\u2014 \\u4e2d\\u6587",%s}' % HDR),
    ("p28_dup_marker", '{"marker":"M","marker":"M","id":"c1","source":"src/a.md","span":"SPAN","expect":"contradicted"}'),
    # raw U+00A0 (UTF-8 c2 a0) after the closing brace: not JSON whitespace
    ("p29_trailing_nbsp", ('{%s}' % HDR) + b'\u00a0'.decode('utf-8')),
    ("p30_trailing_tab", '{%s}\t' % HDR),
    ("p31_leading_nbsp", b'\u00a0'.decode('utf-8') + ('{%s}' % HDR)),
    ("p32_nbsp_only_line", b'\u00a0'.decode('utf-8')),
    ("p33_nested_deep_before", '{"a":{"b":[{"c":{"line":"9"}}]},%s}' % HDR),
    ("p35_str_two_bslash", '{"note":"a\\\\",%s}' % HDR),
    ("p36_str_four_bslash", '{"note":"a\\\\\\\\",%s}' % HDR),
    ("p37_two_objects", '{%s}{"id":"c2"}' % HDR),
    ("p38_nested_unbalanced_in_string", '{"note":"} ] { [","id":"c1","source":"src/a.md","span":"SPAN","expect":"supported"}'),
    ("p39_nested_dup_line", '{"meta":{"line":"9","line":"8"},%s}' % HDR),
    ("p40_dup_unread_key", '{%s,"note":"a","note":"b"}' % HDR),
    ("p34_str_with_nested_key", '{"note":"{\\"sha256\\":\\"00\\"}","id":"c1","source":"src/a.md","span":"SPAN","expect":"supported"}'),
]


def run(gate, line, root, locale):
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(os.path.join(root, "src"))
    with open(os.path.join(root, "src", "a.md"), "w", encoding="utf-8") as f:
        f.write("Alpha SPAN omega.\n")
    claims = os.path.join(root, "claims.jsonl")
    with open(claims, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    env = {k: v for k, v in os.environ.items() if not k.startswith(("CHOUSA_", "LC_")) or k == "LANG"}
    env.update(locale)
    p = subprocess.run(["bash", gate, "verify-claims", claims, "--root", root],
                       capture_output=True, text=True, env=env, timeout=300, cwd=root)
    keep = [l for l in p.stdout.splitlines()
            if l.startswith(("CLAIM ", "FINDING CLAIM_RECORD_INVALID",
                             "FINDING CLAIM_LINE_MISMATCH", "FINDING CLAIM_SOURCE_REVISION_MISMATCH",
                             "VERDICT_BEARING", "RESEARCH_GATE: DRIFT"))]
    return p.returncode, keep, p.stderr.strip().splitlines()[-1:] if p.stderr.strip() else []


def main():
    which = sys.argv[1]
    gate = {"base": BASE, "land": LAND}[which]
    loc = {"C": {"LC_ALL": "C", "LANG": "C"},
           "utf8": {"LC_ALL": "en_US.UTF-8", "LANG": "en_US.UTF-8"}}[sys.argv[2]]
    global ROOT
    ROOT = ROOT + "-" + which + "-" + sys.argv[2]
    only = sys.argv[3] if len(sys.argv) > 3 else None
    for name, line in PROBES:
        if only and only not in name:
            continue
        try:
            rc, keep, err = run(gate, line, ROOT, loc)
        except subprocess.TimeoutExpired:
            print("%s\tTIMEOUT" % name); continue
        print("%s\trc=%s\t%s" % (name, rc, " | ".join(keep) or "(no claim/finding lines)"))
        if only: print("RAW:", repr(p.stdout) if False else "")
        if err:
            print("   stderr: %s" % err[0][:200])
        if os.path.exists(os.path.join(ROOT, "PWNED")):
            print("   !! PWNED file created in fixture root")


if __name__ == "__main__":
    main()
