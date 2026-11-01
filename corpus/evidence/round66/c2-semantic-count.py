#!/usr/bin/env python
"""R66-C2 semantic sourced-entry counter: per-id citation reconciliation.

Successor to the round-65 structural counter (corpus/evidence/round65/c2-count.py),
which a 9-line boilerplate entry plus stub registry rows satisfied 10/10
(.ufo/waves/round-65/w2/R65C03.md, R65M02.md). This counter reconciles the
entry's cited ids against a registry file instead of matching substrings, and
adds non-empty claim/limits body floors. It certifies reconciliation and the
floors only, not entailment: a determined author who registers real mined rows,
re-points used-by, and writes long filler can still pass (disclosed limit;
the semantic judgment stays with the non-author reviewer).

Usage:
    python corpus/evidence/round66/c2-semantic-count.py --entry <repo-rel-path.md>
        [--lane <lane-root>] [--registry <SOURCES.md path>]

Exit contract: 0 = every check ok (SEMANTIC=9/9 C2SEM=PASS);
1 = predicate failure (at least one check failed); 2 = usage/environment error
(missing --entry, unreadable files, or git unavailable) with C2SEM=ERROR on stderr.
"""
import argparse
import hashlib
import re
import subprocess
import sys
from pathlib import Path

CHECK_NAMES = [
    "TRIO", "IDS_DEFINED", "MINED", "USED_BY", "TIER", "ANCHOR",
    "BODY_CITES", "CLAIMS", "LIMITS",
]
ROW_RE = re.compile(r"^\s{0,3}\|\s*(S\d{3,})\s*\|")
ID_RE = re.compile(r"S\d{3,}")
ISO_RE = re.compile(r"\d{4}-\d{2}-\d{2}")
BARE_URL_RE = re.compile(r"^https?://\S+$")


def die_env(msg):
    print("C2SEM=ERROR %s" % msg, file=sys.stderr)
    raise SystemExit(2)


def parse_registry(reg_path):
    """Return {id: {"tier","scope","anchor","teaches","status","usedby"}}; malformed rows are skipped (fail-closed via IDS_DEFINED)."""
    rows = {}
    for line in reg_path.read_text(encoding="utf-8").splitlines():
        m = ROW_RE.match(line)
        if not m:
            continue
        parts = line.split("|")
        if len(parts) != 13:
            continue
        rid = parts[1].strip()
        rows[rid] = {
            "tier": parts[4].strip(),
            "scope": parts[5].strip(),
            "anchor": parts[6].strip(),
            "teaches": parts[7].strip(),
            "status": parts[8].strip(),
            "usedby": parts[11].strip(),
        }
    return rows


def split_entry(text):
    """Return (trio_lines, body_text): the header zone ends at the first line starting with '#'."""
    lines = text.splitlines()
    trio = []
    body_start = len(lines)
    for i, line in enumerate(lines):
        if line.startswith("#"):
            body_start = i
            break
        trio.append(line)
    body = "\n".join(lines[body_start:])
    return trio, body


def section(text, title):
    """Return the content lines under a '## <title>' heading, until the next '## ' heading."""
    out, inside = [], False
    for line in text.splitlines():
        if line.startswith("## "):
            inside = line.strip() == "## " + title
            continue
        if inside and line.strip():
            out.append(line.rstrip())
    return out


def sha256_file(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entry", required=True)
    ap.add_argument("--lane", default=None)
    ap.add_argument("--registry", default=None)
    args = ap.parse_args()

    lane = Path(args.lane).resolve() if args.lane else Path(__file__).resolve().parents[3]
    if not lane.is_dir():
        die_env("lane root not a directory: %s" % lane)
    entry_path = lane / args.entry
    reg_path = Path(args.registry).resolve() if args.registry else lane / "corpus" / "SOURCES.md"
    if not entry_path.is_file():
        die_env("entry not found: %s" % entry_path)
    if not reg_path.is_file():
        die_env("registry not found: %s" % reg_path)
    try:
        rev = subprocess.run(["git", "-C", str(lane), "rev-parse", "HEAD"],
                             capture_output=True, text=True, timeout=30)
        if rev.returncode != 0:
            die_env("git rev-parse failed: %s" % rev.stderr.strip()[:120])
    except (OSError, subprocess.SubprocessError) as e:
        die_env("git unavailable: %s" % e)

    entry_rel = args.entry.replace("\\", "/").lstrip("./")
    text = entry_path.read_text(encoding="utf-8")
    rows = parse_registry(reg_path)
    trio, body = split_entry(text)

    results, details = {}, {}

    # TRIO: source:/verified-at:/recheck: header zone.
    ok = (any(l.startswith("source:") for l in trio)
          and any(l.startswith("verified-at:") and ISO_RE.search(l) for l in trio)
          and any(l.startswith("recheck:") for l in trio))
    results["TRIO"] = ok
    details["TRIO"] = "trio lines=%d" % len(trio)  # trio is a list of lines

    # Cited ids come from the source: line(s) of the trio.
    src_text = "\n".join(l for l in trio if l.startswith("source:"))
    cited = []
    for m in ID_RE.finditer(src_text):
        if m.group(0) not in cited:
            cited.append(m.group(0))
    details["IDS_DEFINED"] = "cited=%s" % (",".join(cited) or "none")

    missing = [c for c in cited if c not in rows]
    results["IDS_DEFINED"] = bool(cited) and not missing
    if missing:
        details["IDS_DEFINED"] += " missing=%s" % ",".join(missing)

    st = [rows[c]["status"] for c in cited if c in rows]
    results["MINED"] = bool(cited) and st and all(s == "mined" for s in st)
    details["MINED"] = "statuses=%s" % (",".join(st) or "none")

    ub_ok = all(entry_rel in [p.strip() for p in rows[c]["usedby"].replace(";", ",").split(",")]
                for c in cited if c in rows)
    results["USED_BY"] = bool(cited) and ub_ok
    details["USED_BY"] = "entry=%s" % entry_rel

    tiers = [rows[c]["tier"] for c in cited if c in rows]
    results["TIER"] = bool(cited) and tiers and all(t in ("A", "B") for t in tiers)
    details["TIER"] = "tiers=%s" % (",".join(tiers) or "none")

    bad_anchor = [c for c in cited if c in rows and (
        not rows[c]["anchor"] or len(rows[c]["anchor"]) < 10 or BARE_URL_RE.match(rows[c]["anchor"]))]
    results["ANCHOR"] = bool(cited) and not bad_anchor
    details["ANCHOR"] = "bad=%s" % (",".join(bad_anchor) or "none")

    missing_body = [c for c in cited if c not in body]
    results["BODY_CITES"] = bool(cited) and not missing_body
    details["BODY_CITES"] = "absent-from-body=%s" % (",".join(missing_body) or "none")

    claims = section(text, "Claims")
    items = [l for l in claims if re.match(r"^\d+[.)]", l)]
    results["CLAIMS"] = len(items) >= 2 and all(len(l.replace(" ", "")) >= 60 for l in items)
    details["CLAIMS"] = "items=%d minlen=%d" % (len(items), min([len(l.replace(" ", "")) for l in items] or [0]))

    limits = section(text, "Limits")
    results["LIMITS"] = (len(limits) >= 2
                         and all(len(l.replace(" ", "")) >= 40 for l in limits)
                         and sum(len(l) for l in limits) >= 120)
    details["LIMITS"] = "lines=%d total=%d" % (len(limits), sum(len(l) for l in limits))

    n = sum(1 for k in CHECK_NAMES if results[k])
    for k in CHECK_NAMES:
        print("CHECK %s %s %s" % (k, "ok" if results[k] else "fail", details[k]))
    print("ENTRY_SHA256=%s" % sha256_file(entry_path))
    print("REGISTRY_SHA256=%s" % sha256_file(reg_path))
    print("LANE_REVISION=%s" % rev.stdout.strip())
    print("SEMANTIC=%d/%d C2SEM=%s" % (n, len(CHECK_NAMES), "PASS" if n == len(CHECK_NAMES) else "FAIL"))
    raise SystemExit(0 if n == len(CHECK_NAMES) else 1)


if __name__ == "__main__":
    main()
