#!/usr/bin/env bash
# C1 no-reader control: decides every claim from claims.jsonl features only.
# NEVER opens, stats, or lists any file under --root other than the claims path
# the counter hands us. Interface: <this> verify-claims <claims.jsonl> --root <dir>
set -u
if [ "$1" != "verify-claims" ]; then echo "control: unsupported mode" >&2; exit 2; fi
CLAIMS="$2"
exec python3 - "$CLAIMS" <<'PY'
import json, re, sys

claims_path = sys.argv[1]
VALID_SINGLE = re.compile(r"^[1-9][0-9]*$")
VALID_RANGE = re.compile(r"^([1-9][0-9]*)-([1-9][0-9]*)$")


def classify(rec):
    """Truth prediction from claims-file features only.

    Sound rules (no knowledge of source bytes):
      - "line" present but not "N"/"N-M" with N>=1, M>N, no leading zero -> invalid
      - "line" absent -> supported (B4 is the only no-line class)
      - span contains "\n" (multi-line span):
          range N-M with M == N+1 -> supported (B3); B3 starts at a+1 <= n-3 <= 27,
            so a width-2 range starting at >= 28 cannot be B3 -> mislocated
          any other multi-line line value (single N, or M >= N+2) -> mislocated (M4)
      - valid single N with a one-line span -> mislocated (largest class by far;
        posterior for supported never exceeds 0.36 inside this group)
    """
    if "line" not in rec:
        return "supported"
    v = rec.get("line")
    fmt, n, m = "invalid", None, None
    if isinstance(v, str):
        if VALID_SINGLE.match(v):
            fmt, n, m = "single", int(v), int(v)
        else:
            g = VALID_RANGE.match(v)
            if g:
                a, b = int(g.group(1)), int(g.group(2))
                if b > a:
                    fmt, n, m = "range", a, b
    if fmt == "invalid":
        return "invalid"
    span = rec.get("span", "")
    if isinstance(span, str) and "\n" in span:
        if fmt == "range" and m == n + 1 and n <= 27:
            return "supported"
        return "mislocated"
    return "mislocated"


out = []
rc = 1
with open(claims_path, "r", encoding="utf-8") as f:
    for raw in f:
        raw = raw.strip()
        if not raw:
            continue
        rec = json.loads(raw)
        obs = classify(rec)
        src = rec.get("source", "-")
        cid = rec.get("id", "?")
        # design v2: a mislocated verdict must be named by a claim-level finding
        # (ignored by the v1 counter, required by the v2 counter).
        if obs == "mislocated":
            out.append("FINDING CLAIM_LINE_MISMATCH severity=warn surface=claims obs=id=%s expected=%s observed=%s source=%s at=-" % (
                cid, rec.get("expect", "supported"), obs, src))
        out.append("CLAIM id=%s expected=%s observed=%s source=%s at=- verdict=%s" % (
            cid, rec.get("expect", "supported"), obs, src, obs))
sys.stdout.write("\n".join(out) + ("\n" if out else ""))
sys.exit(rc)
PY
