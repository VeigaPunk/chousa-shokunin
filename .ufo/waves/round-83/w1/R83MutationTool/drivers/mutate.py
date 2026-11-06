#!/usr/bin/env python3
"""R83MutationTool driver: single-point mutants of tools/gate-records.py scored by the frozen C2 counter."""
import difflib
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

TREE = "/fast/scratch/hyaku/chousa-r83/R83MutationTool"
LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
COUNTER = os.path.join(TREE, "corpus/evidence/round83/gate-records-r83.py")
PRISTINE = os.path.join(TREE, "tools/gate-records.py")
OUT = os.path.join(TREE, "mutants")
LOGS = os.path.join(TREE, "logs")
os.makedirs(OUT, exist_ok=True)
os.makedirs(LOGS, exist_ok=True)

MUTANTS = [
    # label, description, old, new
    ("M01-sha-min-1", "SHA_RE min prefix 16 -> 1 hex", 'SHA_RE = re.compile(r"([0-9a-f]{16,64})(?:…|\\.\\.\\.)?")', 'SHA_RE = re.compile(r"([0-9a-f]{1,64})(?:…|\\.\\.\\.)?")'),
    ("M02-drop-capture-key", "drop CAPTURE_KEY check", '        if cm and cm.group(1) != key:\n            codes.append("CAPTURE_KEY")\n', '        pass\n'),
    ("M03-drop-refetch-txtsha", "drop r[8]==capsha from admit REFETCH", 'and capsha is not None and r[8] == capsha for r in refetch)', 'and capsha is not None for r in refetch)'),
    ("M04-drop-refetch-fetched", "drop r[4]==fetched from admit REFETCH", 'r[2] == key and r[4] == kv["fetched"] and r[5] == "0"', 'r[2] == key and r[5] == "0"'),
    ("M05-accept-curl-nonzero", "drop curl_rc==0 from admit REFETCH", 'r[4] == kv["fetched"] and r[5] == "0"\n                 and re.fullmatch', 'r[4] == kv["fetched"]\n                 and re.fullmatch'),
    ("M06-accept-non2xx", "accept any 3-digit http in admit REFETCH", 're.fullmatch(r"2\\d\\d", r[6])', 're.fullmatch(r"\\d{3}", r[6])'),
    ("M07-words-off-by-one", "accept words == tokens+1", 'if kv["words"] != str(n):', 'if kv["words"] not in (str(n), str(n + 1)):'),
    ("M08-quote-len-0-26", "QUOTE_LEN bounds 1..25 -> 0..26", 'if not 1 <= n <= 25:', 'if not 0 <= n <= 26:'),
    ("M09-skip-lead-strip", "classify without lead_strip", 'if not REC_RE.match(lead_strip(ln)):', 'if not REC_RE.match(ln):'),
    ("M10-skip-indented", "skip any indented line", 'if not REC_RE.match(lead_strip(ln)):', 'if ln[:1].isspace() or not REC_RE.match(lead_strip(ln)):'),
    ("M11-rev-short", "REV accept 4..40 hex revs", 'if HEX40_RE.fullmatch(kv["rev"]):', 'if re.fullmatch(r"[0-9a-f]{4,40}", kv["rev"]):'),
    ("M12-line-whole-blob", "LINE searches whole blob", 'if i > len(lines) or not quote.strip() or norm(quote) not in norm(lines[i - 1]):', 'if i > len(lines) or not quote.strip() or norm(quote) not in norm("\\n".join(lines)):'),
    ("M13-exit0-zero-records", "exit 0 when no record found", 'return 0 if n >= 1 and ok == n else 1', 'return 0 if ok == n else 1'),
    ("M14-exit0-with-fail", "always exit 0", 'return 0 if n >= 1 and ok == n else 1', 'return 0'),
    ("M15-drop-registry", "drop REGISTRY check", '    if regrow is None:\n        codes.append("REGISTRY")\n', '    pass\n'),
    ("M16-drop-tier", "drop TIER check", 'if regrow is not None and regrow[3] != kv["tier"]:', 'if False:'),
    ("M17-drop-capture-path", "drop CAPTURE_PATH check", '        if (cap is None or os.path.islink(cap) or not os.path.isfile(cap)\n                or os.path.dirname(os.path.realpath(cap)) != capdir):', '        if False:'),
    ("M18-drop-capture-sha", "drop CAPTURE_SHA check", 'if not sm or capsha is None or not capsha.startswith(sm.group(1)):', 'if False:'),
    ("M19-drop-quote-absent", "drop QUOTE_ABSENT check", 'if not quote.strip() or norm(quote) not in text:', 'if False:'),
    ("M20-dup-key-accept", "accept duplicate keys", 'if not k or k in kv or not v:', 'if not k or not v:'),
    ("M21-parse-fail-ok", "score PARSE failures as OK", '                    print(f"GATE_RECORD {f}:{i} {sm.group(0) if sm else \'?\'} FAIL PARSE")', '                    ok += 1\n                    print(f"GATE_RECORD {f}:{i} {sm.group(0) if sm else \'?\'} OK")'),
    ("M22-drop-refetch-url", "drop url match from admit REFETCH", 'r[1] == url and r[2] == key', 'r[2] == key'),
    ("M23-drop-refetch-sid", "drop id match from admit REFETCH", 'r[0] == sid and r[1] == url and r[2] == key', 'r[1] == url and r[2] == key'),
    ("M24-unreach-accept-success", "unreach: success never detected", 'success = kv["curl_rc"] == "0" and kv["http"].startswith("2")', 'success = False'),
    ("M25-unreach-drop-fetched", "unreach: drop fetched match", 'r[1] == url and r[4] == kv["fetched"] and r[5] == kv["curl_rc"]', 'r[1] == url and r[5] == kv["curl_rc"]'),
    ("M26-unreach-drop-http", "unreach: drop http match", 'and r[6] == kv["http"] for r in refetch)', 'for r in refetch)'),
    ("M27-quote-len-admit-only", "QUOTE_LEN only for admit form", 'if not 1 <= n <= 25:', 'if form == "admit" and not 1 <= n <= 25:'),
    ("M28-cap-re-loose", "CAP_RE accepts any name", 'CAP_RE = re.compile(r"corpus/captures/([0-9a-f]{24})\\.txt")', 'CAP_RE = re.compile(r"corpus/captures/(.+)\\.txt")'),
    ("M29-no-islink", "capture may be a symlink", 'os.path.islink(cap) or not os.path.isfile(cap)', 'not os.path.isfile(cap)'),
    ("M30-ts-loose", "TS_RE accepts any token", 'TS_RE = re.compile(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z")', 'TS_RE = re.compile(r"\\S+")'),
    ("M31-int-loose", "INT_RE accepts leading zeros", 'INT_RE = re.compile(r"0|[1-9]\\d{0,6}")', 'INT_RE = re.compile(r"\\d{1,7}")'),
    ("M32-rev-no-pop", "rev: keep trailing empty blob line", '            if lines and lines[-1] == "":\n                lines.pop()\n', '            pass\n'),
    ("M33-unreach-decision-any", "unreach: accept any decision", 'or kv["decision"] != "reject":', 'or False:'),
    ("M34-admit-quote-unterminated", "admit: accept unterminated quote", 'if len(q) < 2 or not (q.startswith(\'"\') and q.endswith(\'"\')):', 'if len(q) < 1 or not q.startswith(\'"\'):'),
    ("M35-drop-url-regex", "admit: drop url shape check", 'if not re.fullmatch(r"https?://\\S+", kv["url"]) or not TS_RE.fullmatch(kv["fetched"]):', 'if not TS_RE.fullmatch(kv["fetched"]):'),
    ("M36-drop-ts-check", "admit: drop fetched timestamp check", 'if not re.fullmatch(r"https?://\\S+", kv["url"]) or not TS_RE.fullmatch(kv["fetched"]):', 'if not re.fullmatch(r"https?://\\S+", kv["url"]):'),
]


def score(label):
    mp = os.path.join(OUT, label + ".py")
    cmd = [sys.executable, "-B", COUNTER, "--root", TREE, "--repo", LANE, "--tool", mp, "--work", TREE]
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=TREE)
    out = p.stdout + p.stderr
    with open(os.path.join(LOGS, label + ".out"), "w", encoding="utf-8") as fh:
        fh.write("$ " + " ".join(cmd) + "\n" + out + f"rc={p.returncode}\n")
    first = next((l for l in p.stdout.splitlines() if l.startswith("TOOL=")), "")
    verdict = next((l for l in p.stdout.splitlines() if l.startswith("GATE_RECORDS_R83=")), "")
    return {"label": label, "cmd": " ".join(cmd), "rc": p.returncode, "line": first, "verdict": verdict,
            "stdout": p.stdout, "stderr": p.stderr}


def main():
    pristine = open(PRISTINE, encoding="utf-8").read()
    built = []
    for label, desc, old, new in MUTANTS:
        n = pristine.count(old)
        assert n == 1, f"{label}: old occurs {n} times"
        mp = os.path.join(OUT, label + ".py")
        with open(mp, "w", encoding="utf-8") as fh:
            fh.write(pristine.replace(old, new, 1))
        d = list(difflib.unified_diff(pristine.splitlines(True), open(mp, encoding="utf-8").read().splitlines(True),
                                      fromfile="tools/gate-records.py", tofile=label + ".py", n=2))
        with open(os.path.join(OUT, label + ".diff"), "w", encoding="utf-8") as fh:
            fh.write("".join(d))
        built.append((label, desc))
    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(score, [b[0] for b in built]))
    desc = dict(built)
    rows = []
    for r in results:
        surv = "SURVIVOR" if "GATE_RECORDS_R83=PASS" in r["verdict"] else "KILLED"
        rows.append((r["label"], desc[r["label"]], r["line"], r["rc"], surv))
        print(f"{r['label']}\t{surv}\trc={r['rc']}\t{r['line']}")
    with open(os.path.join(TREE, "SUMMARY.tsv"), "w", encoding="utf-8") as fh:
        fh.write("label\tdescription\tcounter_line\trc\tverdict\n")
        for row in rows:
            fh.write("\t".join(str(x) for x in row) + "\n")
    with open(os.path.join(TREE, "results.json"), "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=1)
    print("total", len(rows), "survivors", sum(1 for r in rows if r[4] == "SURVIVOR"))


if __name__ == "__main__":
    main()
