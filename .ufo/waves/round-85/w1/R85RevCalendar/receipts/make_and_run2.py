#!/usr/bin/env python3
import os, re, subprocess, sys

ROOT = "/fast/scratch/hyaku/chousa-r85/R85RevCalendar"
REPO = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
TOOL = os.path.join(ROOT, "tools", "gate-records.py")
POS_TSV = os.path.join(ROOT, "corpus", "evidence", "round85", "c2-positives.tsv")

def kv_set(line, key, val):
    return re.sub(r"(?<= )"+re.escape(key)+r"=\S+", key+"="+val, line, count=1)

def kv_get(line, key):
    m = re.search(r"(?<= )"+re.escape(key)+r"=(\S+)", line)
    return m.group(1) if m else None

def form_of(line):
    if " rev=" in line:
        return "rev"
    if " curl_rc=" in line:
        return "unreach"
    return "admit"

pos = []
for ln in open(POS_TSV, encoding="utf-8"):
    parts = ln.rstrip("\n").split("\t", 2)
    if len(parts) < 3:
        continue
    f, n, raw = parts
    sid = re.match(r"^\s*GATE-RECORD (S\d+)", raw).group(1)
    pos.append((f, int(n), sid, raw))

admit = next(p for p in pos if form_of(p[3])=="admit")
unreach = next(p for p in pos if form_of(p[3])=="unreach")
rev = next(p for p in pos if form_of(p[3])=="rev")
print(f"ADMIT {admit[2]}: {admit[3][:160]}")
print(f"UNREACH {unreach[2]}: {unreach[3][:160]}")
print(f"REV {rev[2]}: {rev[3][:160]}")

cases = [
 ("leap2024-accept","2024-02-29T12:00:00Z"),
 ("nonleap2025-reject","2025-02-29T12:00:00Z"),
 ("apr31-reject","2026-04-31T00:00:00Z"),
 ("dec31-235959-accept","2026-12-31T23:59:59Z"),
 ("jan01-000000-accept","2026-01-01T00:00:00Z"),
 ("hour24-reject","2026-01-01T24:00:00Z"),
 ("sec60-reject","2026-01-01T00:00:60Z"),
 ("year0000-reject","0000-01-01T00:00:00Z"),
 ("month00-reject","2026-00-15T00:00:00Z"),
 ("plus0000-reject-shape","2026-01-01T00:00:00+00:00"),
 ("lowt-reject-shape","2026-01-01t00:00:00Z"),
 ("lowz-reject-shape","2026-01-01T00:00:00z"),
 ("trailZ-space","2026-01-01T00:00:00Z "),
 ("unidig-month","2026-01-01T00:00:00Z"+"٠"),
 ("d4-2026-13-40","2026-13-40T00:00:00Z"),
 ("day00-reject","2026-01-00T00:00:00Z"),
 ("min60-reject","2026-01-01T00:60:00Z"),
 ("unidig-in-month","2026-٠١-15T00:00:00Z"),
]

work = "/fast/scratch/hyaku/chousa-r85/R85RevCalendar/fixtures2"
os.makedirs(work, exist_ok=True)

def run_one(name, base_raw, ts_value, form_label):
    forged = kv_set(base_raw, "fetched", ts_value)
    fp = os.path.join(work, f"{form_label}-{name}.md")
    with open(fp, "w", encoding="utf-8") as fh:
        fh.write(forged + "\n")
    p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--root", ROOT, "--repo", REPO, fp],
                       capture_output=True, text=True)
    out = p.stdout.strip().replace("\n", " | ")
    err = p.stderr.strip().replace("\n", " | ")
    # Also show the forged fetched token
    tok = kv_get(forged, "fetched")
    print(f"CASE {form_label} {name}: fetched_tok={tok!r} rc={p.returncode} stdout={out} stderr={err}")
    return p.returncode, out, err

for name, ts in cases:
    run_one(name, admit[3], ts, "admit")
    run_one(name, unreach[3], ts, "unreach")
    # rev: no fetched key; kv_set is no-op, so the rev line is unchanged and should be OK (rc 0) — demonstrates rev has no fetched gate.
    # We also craft a rev line that erroneously gains a fetched key (extra key) to show parse rejects it as PARSE, not REV.
    run_one(name, rev[3], ts, "rev")

print("\n--- rev with spurious fetched key added (extra key => PARSE) ---")
# Insert fetched token into rev head
rev_base = rev[3]
# rev head is: GATE-RECORD S199 rev=... path=... line=... words=... quote=...
# Insert " fetched=2026-13-40T00:00:00Z" before " quote="
rev_extra = rev_base.replace(" quote=", " fetched=2026-13-40T00:00:00Z quote=")
fp = os.path.join(work, "rev-extra-fetched.md")
with open(fp, "w", encoding="utf-8") as fh:
    fh.write(rev_extra + "\n")
p = subprocess.run([sys.executable, "-B", TOOL, "verify", "--root", ROOT, "--repo", REPO, fp], capture_output=True, text=True)
print(f"CASE rev-extra-fetched: rc={p.returncode} stdout={p.stdout.strip()} stderr={p.stderr.strip()}")

print("\nDONE")
