#!/usr/bin/env python3
"""Generate single-point mutants of tools/gate-records.py at 64803d3 (scratch only)."""
import hashlib
import json
import os
import sys

SRC = "/fast/scratch/hyaku/chousa-r85/R85MutationTool/tree/tools/gate-records.py"
OUT = "/fast/scratch/hyaku/chousa-r85/R85MutationTool/mutants"

MUTANTS = [
    ("M01-registry-check-removed",
     "REGISTRY check removed: regrow None no longer appends REGISTRY",
     '    regrow = reg.get(sid)\n    if regrow is None:\n        codes.append("REGISTRY")\n',
     '    regrow = reg.get(sid)\n'),
    ("M02-tier-check-removed",
     "TIER check removed",
     '        if regrow is not None and regrow[3] != kv["tier"]:\n            codes.append("TIER")\n',
     ''),
    ("M03-capture-path-check-removed",
     "CAPTURE_PATH append removed",
     '            codes.append("CAPTURE_PATH")\n',
     '            pass  # CAPTURE_PATH check removed\n'),
    ("M04-capture-key-check-removed",
     "CAPTURE_KEY check removed (capture key != sha256(url)[:24] accepted)",
     '        if cm and cm.group(1) != key:\n            codes.append("CAPTURE_KEY")\n',
     ''),
    ("M05-capture-sha-check-removed",
     "CAPTURE_SHA check removed",
     '        if not sm or capsha is None or not capsha.startswith(sm.group(1)):\n'
     '            codes.append("CAPTURE_SHA")\n',
     ''),
    ("M06-admit-refetch-check-removed",
     "admit REFETCH check removed (ok forced True)",
     '        ok = any(r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"] and r[5] == "0" and r[6] == "200" and capsha is not None and r[8] == capsha for r in refetch)\n',
     '        ok = True  # REFETCH check removed\n'),
    ("M07-words-check-removed",
     "WORDS check removed",
     '        if kv["words"] != str(n):\n            codes.append("WORDS")\n',
     ''),
    ("M08-quote-len-check-removed",
     "QUOTE_LEN check removed",
     '        if not 1 <= n <= 25:\n            codes.append("QUOTE_LEN")\n',
     ''),
    ("M09-quote-absent-check-removed",
     "QUOTE_ABSENT check removed when capture exists",
     '            if not quote.strip() or norm(quote) not in text:\n                codes.append("QUOTE_ABSENT")\n',
     '            if False:  # QUOTE_ABSENT check removed\n                codes.append("QUOTE_ABSENT")\n'),
    ("M10-rev-code-removed",
     "REV code removed from missing-blob branch (LINE kept)",
     '            codes.append("REV")\n',
     '            pass  # REV check removed\n'),
    ("M11-line-check-removed",
     "LINE check removed from rev branch",
     '            if i > len(lines) or not quote.strip() or norm(quote) not in norm(lines[i - 1]):\n'
     '                codes.append("LINE")\n',
     ''),
    ("M12-sha-regex-16-64-to-1-64",
     "SHA_RE relaxed {16,64} -> {1,64}",
     'SHA_RE = re.compile(r"([0-9a-f]{16,64})(?:\u2026|\\.\\.\\.)?")',
     'SHA_RE = re.compile(r"([0-9a-f]{1,64})(?:\u2026|\\.\\.\\.)?")'),
    ("M13-refetch-key-conjunct-dropped",
     "admit REFETCH no longer requires row key == sha256(url)[:24]",
     'r[0] == sid and r[1] == url and r[2] == key and r[4] == kv["fetched"]',
     'r[0] == sid and r[1] == url and r[4] == kv["fetched"]'),
    ("M14-refetch-txtsha-conjunct-dropped",
     "admit REFETCH no longer requires r[8] == sha256(capture)",
     ' and capsha is not None and r[8] == capsha for r in refetch',
     ' and capsha is not None for r in refetch'),
    ("M15-refetch-fetched-conjunct-dropped",
     "admit REFETCH no longer requires r[4] == fetched time",
     'r[2] == key and r[4] == kv["fetched"] and r[5] == "0"',
     'r[2] == key and r[5] == "0"'),
    ("M16-refetch-curlrc-accepted",
     "admit REFETCH accepts any curl_rc",
     'r[4] == kv["fetched"] and r[5] == "0" and r[6] == "200"',
     'r[4] == kv["fetched"] and r[6] == "200"'),
    ("M17-refetch-http-2xx-accepted",
     "admit REFETCH accepts any 2xx (base-tool semantics)",
     'r[6] == "200" and capsha is not None and r[8] == capsha for r in refetch',
     'r[6].startswith("2") and capsha is not None and r[8] == capsha for r in refetch'),
    ("M18-calendar-gate-removed",
     "calendar check removed from parse condition (TS_RE only)",
     ' or not TS_RE.fullmatch(kv["fetched"]) or not _valid_ts(kv["fetched"]):',
     ' or not TS_RE.fullmatch(kv["fetched"]):'),
    ("M19-calendar-accepts-invalid",
     "_valid_ts always True (calendar-invalid dates accepted)",
     'def _valid_ts(s):\n    try:\n        datetime.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")\n        return True\n    except ValueError:\n        return False\n',
     'def _valid_ts(s):\n    return True\n'),
    ("M20-lead-strip-skipped",
     "record detection matches raw line, not lead_strip(line)",
     '                if not REC_RE.match(lead_strip(ln)):',
     '                if not REC_RE.match(ln):'),
    ("M21-indented-lines-skipped",
     "indented GATE-RECORD lines treated as prose and skipped",
     '                if not REC_RE.match(lead_strip(ln)):',
     '                if ln[:1].isspace() or not REC_RE.match(lead_strip(ln)):'),
    ("M22-rev-short-revs-accepted",
     "rev accepts 4..40 hex abbrevs (git resolves them) instead of exactly 40",
     '        if HEX40_RE.fullmatch(kv["rev"]):',
     '        if re.fullmatch(r"[0-9a-f]{4,40}", kv["rev"]):'),
    ("M23-line-check-whole-blob",
     "rev LINE check searches the whole blob instead of the named line",
     'norm(quote) not in norm(lines[i - 1])',
     'norm(quote) not in norm("\\n".join(lines))'),
    ("M24-exit0-on-zero-records",
     "exit 0 when no records found",
     '    return 0 if n >= 1 and ok == n else 1',
     '    return 0 if ok == n else 1'),
    ("M25-exit0-with-fail-lines",
     "exit 0 whenever at least one record exists, FAIL lines notwithstanding",
     '    return 0 if n >= 1 and ok == n else 1',
     '    return 0 if n >= 1 else 1'),
    ("M26-int-ascii-class-relaxed-unicode",
     "INT_RE [0-9] relaxed to Unicode \\d (words/line/curl_rc)",
     'INT_RE = re.compile(r"0|[1-9][0-9]{0,6}")',
     'INT_RE = re.compile(r"0|[1-9]\\d{0,6}")'),
    ("M27-quote-boundary-guard-removed",
     "admit quote no longer required to start and end with a double quote",
     'if len(q) < 2 or not (q.startswith(\'"\') and q.endswith(\'"\')):',
     'if len(q) < 2:'),
    ("M28-setup-probe-removed",
     "non-git --repo probe removed",
     '    if a.repo:\n        p = subprocess.run(["git", "-C", a.repo, "rev-parse", "--git-dir"], capture_output=True, text=True)\n        if p.returncode != 0:\n            print(f"GATE_RECORDS_ERROR not a git repo: {a.repo}", file=sys.stderr)\n            return 2\n',
     ''),
    ("M29-setup-probe-inverted",
     "setup probe exits 2 on a VALID git repo",
     '        if p.returncode != 0:\n            print(f"GATE_RECORDS_ERROR not a git repo: {a.repo}", file=sys.stderr)',
     '        if p.returncode == 0:\n            print(f"GATE_RECORDS_ERROR not a git repo: {a.repo}", file=sys.stderr)'),
    ("M30-ts-regex-unicode-relaxed",
     "TS_RE [0-9] every field relaxed to Unicode \\d (any month digit)",
     'TS_RE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z")',
     'TS_RE = re.compile(r"\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z")'),
    ("M31-unreach-success-2xx",
     "unreach success definition relaxed to 2xx (a 203 page counts as success)",
     '        success = kv["curl_rc"] == "0" and kv["http"] == "200"',
     '        success = kv["curl_rc"] == "0" and kv["http"].startswith("2")'),
]


def main():
    with open(SRC, encoding="utf-8") as fh:
        src = fh.read()
    os.makedirs(OUT, exist_ok=True)
    manifest = []
    for name, why, old, new in MUTANTS:
        n = src.count(old)
        if n != 1:
            print(f"BAD-ANCHOR {name} count={n}", file=sys.stderr)
            return 1
        mutated = src.replace(old, new, 1)
        if mutated == src:
            print(f"NO-CHANGE {name}", file=sys.stderr)
            return 1
        d = os.path.join(OUT, name)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, "gate-records.py")
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(mutated)
        try:
            compile(mutated, p, "exec")
        except SyntaxError as e:
            print(f"SYNTAX {name}: {e}", file=sys.stderr)
            return 1
        manifest.append({
            "name": name,
            "why": why,
            "path": p,
            "sha256": hashlib.sha256(mutated.encode()).hexdigest(),
            "src_sha256": hashlib.sha256(src.encode()).hexdigest(),
            "diff_lines": style_diff(old, new),
        })
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=1)
    print(f"GENERATED={len(manifest)} SRC_SHA={hashlib.sha256(src.encode()).hexdigest()}")
    return 0


def style_diff(old, new):
    return {"old": old, "new": new}


if __name__ == "__main__":
    sys.exit(main())
