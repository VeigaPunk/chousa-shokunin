#!/usr/bin/env bash
# Round-26 counting probe (pre-registered; see corpus/evidence/round26-claims.md).
# Usage: bash corpus/evidence/round26-measure.sh TREE [c1|c2|c3|holds|all]
# TREE is a lane checkout (base or candidate). Frozen inputs are read from the
# immutable base commit in BASE_REPO, never from TREE, so a candidate cannot
# change its own population. A probe, not an admission gate: exit 0 only means
# it ran; compare the printed values with the registered predictions.
set -euo pipefail
[[ $# -ge 1 && -d $1 ]] || { echo "usage: round26-measure.sh TREE [c1|c2|c3|holds|all]" >&2; exit 2; }
TREE=$(cd "$1" && pwd); PART=${2:-all}
BASE=ba3333254dd337658a4f25e7a9471f9cf4e4567e
BASE_REPO=${R26_BASE_REPO:-/home/vgpnk/Projects/shokunin/chousa-shokunin}
FLEET=${SHOKUNIN_ROOT:-/home/vgpnk/Projects/shokunin}
AS_OF=2026-10-21
G=$TREE/tools/research-gate.sh
[[ -f $G ]] || { echo "no gate at $G" >&2; exit 2; }
W=$(mktemp -d /tmp/r26m.XXXXXX); trap 'rm -rf "$W"' EXIT
POP=(anchor-boundaries-r4.md archived-export-intake.md archives-verified-r9.md
  audit-r11.md chain-resolution-r3.md citation-chain-fidelity-r24.md
  claim-support-states-r24.md claim-verification-r2.md
  contextual-source-admission-r24.md denylist-r22.md fenced-anchor-r23.md
  fenced-heading-r17.md gate-baseline-r12.md gate-baseline-r8.md
  hardening-r10.md hardlink-alias-r13.md html-comment-r20.md
  json-delimiter-r24.md metadata-screen-r25.md mount-alias-r14.md
  pointer-boundary-r21.md reference-integrity-r7.md root-slash-boundary-r15.md
  scope-phrase-gap-r18.md scope-refusal-r12.md sweep-symlink-r19.md
  sweeps-rejections-r5.md verification-r16.md verify-all-r6.md)
POP24=(citation-chain-fidelity-r24.md claim-support-states-r24.md
  contextual-source-admission-r24.md json-delimiter-r24.md metadata-screen-r25.md)
mkdir -p "$W/frozen"
for f in "${POP[@]}"; do
  git -C "$BASE_REPO" show "$BASE:corpus/knowledge/$f" >"$W/frozen/$f"
done
[[ $(find "$W/frozen" -name '*.md' | wc -l) -eq 29 ]] || { echo "frozen population incomplete" >&2; exit 2; }
git -C "$BASE_REPO" show "$BASE:corpus/SOURCES.md" >"$W/SOURCES-base.md"
echo "tree=$TREE gate_sha256=$(sha256sum <"$G" | cut -d' ' -f1) base=$BASE as_of=$AS_OF"

peak() { # GATE ARGS... -> "rc maxrss_kb elapsed_s" (fresh python per run; 300 s cap)
  python3 - "$@" <<'PY'
import resource, subprocess, sys, time
t = time.time()
try:
    r = subprocess.run(["bash"] + sys.argv[1:], capture_output=True, timeout=300)
    rc = str(r.returncode)
except subprocess.TimeoutExpired:
    rc = "timeout"
print(rc, resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss, "%.1f" % (time.time() - t))
PY
}

c1() {
  echo "== C1 operability: metadata reader allocation (8,388,000-byte shapes; cap 8 MiB)"
  mkdir -p "$W/c1"
  python3 - "$W/c1" <<'PY'
import sys
d, n = sys.argv[1], 8388000
hdr = "source: S001 x\nverified-at: 2026-10-21 checked\nrecheck: 90d\n\n"
def fill(prefix, unit):
    k = (n - len(prefix)) // len(unit)
    body = prefix + unit * k
    return body + "\n" * (n - len(body))
open(d + "/ctl.md", "w").write(hdr + "## Body\nshort\n")
open(d + "/s1-newlines.md", "w").write("\n" * n)
open(d + "/s2-header-body.md", "w").write(fill(hdr + "## Body\n", "x\n"))
open(d + "/s3-crlf.md", "w", newline="").write("\r\n" * (n // 2))
open(d + "/s4-header-noheading.md", "w").write(fill(hdr, "a\n"))
PY
  local ctl s amp=0 rc rss el
  read -r rc ctl el < <(peak "$G" verify-metadata "$W/c1/ctl.md" --root "$W/c1")
  echo "ctl rc=$rc maxrss_kb=$ctl elapsed_s=$el"
  for s in s1-newlines s2-header-body s3-crlf s4-header-noheading; do
    read -r rc rss el < <(peak "$G" verify-metadata "$W/c1/$s.md" --root "$W/c1")
    local bytes; bytes=$(stat -c %s "$W/c1/$s.md")
    local extra=$(( rss - ctl )) flag=bounded
    if [[ $rc == timeout ]] || (( extra * 1024 > 8 * bytes )); then flag=amplified; amp=$((amp + 1)); fi
    echo "$s bytes=$bytes rc=$rc maxrss_kb=$rss extra_kb=$extra elapsed_s=$el $flag"
  done
  echo "C1_AMPLIFIED=$amp/4"
  echo "== C1 hold: plain verify-metadata output over frozen 29 (ts line dropped)"
  local out rc2=0
  out=$(bash "$G" verify-metadata "$W/frozen" --root "$W/frozen" 2>&1) || rc2=$?
  echo "C1_FROZEN_RC=$rc2 C1_FROZEN_SHA=$(printf '%s\n' "$out" | sed 1d | sha256sum | cut -d' ' -f1)"
  printf '%s\n' "$out" | grep -E '^(METADATA_COMPLETE|RESEARCH_GATE:)'
}

c2() {
  echo "== C2 freshness: due dates with --as-of $AS_OF"
  local out rc=0
  out=$(bash "$G" verify-metadata "$W/frozen" --root "$W/frozen" --as-of "$AS_OF" 2>&1) || rc=$?
  local k=0
  if [[ $rc == 0 || $rc == 1 ]]; then
    k=$(printf '%s\n' "$out" | grep -cE '^META entry=[^ ]+ .* due=[^ ]+ freshness=(current|overdue|event|unknown) verdict=(clean|drift)$' || true)
  fi
  echo "c2 frozen rc=$rc"
  echo "FRESHNESS_CLASSIFIED=$k/29"
  printf '%s\n' "$out" > "$W/c2-gate.txt"
  python3 - "$W/frozen" "$W/c2-gate.txt" "$AS_OF" <<'PY'
# Independent oracle from the registered spec (round26-claims.md Claim 2).
import datetime as dt, os, re, sys
d, gate, asof = sys.argv[1], sys.argv[2], dt.date.fromisoformat(sys.argv[3])
fence = re.compile(r'^ {0,3}(`{3,}|~{3,})(.*)$')
def iso(s):
    try: return dt.date.fromisoformat(s) if re.fullmatch(r'\d{4}-\d{2}-\d{2}', s) else None
    except ValueError: return None
def header(text):
    vals, key, fc, fl = {}, None, None, 0
    for line in text.split('\n'):
        line = line[:-1] if line.endswith('\r') else line
        if line.strip() == '': key = None
        if fc:
            if key in ('verified-at', 'recheck'): vals[key] += '\n' + line
            m = re.fullmatch(r' {0,3}(`{3,}|~{3,})[ \t\r\v\f]*', line)
            if m and m.group(1)[0] == fc and len(m.group(1)) >= fl: fc = None
            continue
        m = fence.match(line)
        if m:
            if key in ('verified-at', 'recheck'): vals[key] += '\n' + line
            fc, fl = m.group(1)[0], len(m.group(1)); continue
        if line.startswith('## '): break
        if line.strip() == '': key = None; continue
        m = re.match(r'^(source|verified-at|recheck):(.*)$', line)
        if m:
            key = m.group(1); vals[key] = m.group(2); continue
        if key in ('verified-at', 'recheck'): vals[key] += '\n' + line
    return vals
want = {}
for f in sorted(os.listdir(d)):
    v = header(open(os.path.join(d, f), encoding='utf-8', errors='surrogateescape', newline='').read())
    va = re.match(r'^\s*(\d{4}-\d{2}-\d{2})', v.get('verified-at', ''))
    vd = iso(va.group(1)) if va else None
    tok = re.match(r'^\s*(\S+)', v.get('recheck', ''))
    t = tok.group(1) if tok else ''
    if iso(t): due = iso(t)
    elif re.fullmatch(r'[0-9]+d', t) and vd: due = vd + dt.timedelta(days=int(t[:-1]))
    elif t == 'on-release': due = 'on-release'
    else: due = None
    if due == 'on-release': want[f] = ('on-release', 'event')
    elif due is None: want[f] = ('unknown', 'unknown')
    else: want[f] = (due.isoformat(), 'overdue' if asof > due else 'current')
got = {}
for line in open(gate, encoding='utf-8', errors='replace'):
    m = re.match(r'^META entry=(\S+) .* due=(\S+) freshness=(\S+) verdict=', line)
    if m: got[m.group(1)] = (m.group(2), m.group(3))
agree = sum(got.get(f) == w for f, w in want.items())
for f, w in sorted(want.items()):
    if got.get(f) != w: print('oracle-mismatch', f, 'want', w, 'got', got.get(f))
print('C2_ORACLE_AGREE=%d/%d' % (agree, len(want)))
from collections import Counter
print('C2_ORACLE_DIST', dict(Counter(w[1] for w in want.values())))
PY
  mkdir -p "$W/c2"
  local -a ctl=(
    "overdue|2026-01-02 checked fixture|90d|due=2026-04-02 freshness=overdue|1|META_RECHECK_OVERDUE"
    "current|2026-10-01 checked fixture|90d|due=2026-12-30 freshness=current|0|"
    "date-past|2026-01-02 checked fixture|2026-03-01|due=2026-03-01 freshness=overdue|1|META_RECHECK_OVERDUE"
    "event|2026-01-02 checked fixture|on-release|due=on-release freshness=event|0|"
    "unknown|2026-01-02 checked fixture|bash tools/x.sh|due=unknown freshness=unknown|0|"
    "boundary|2026-07-23 checked fixture|90d|due=2026-10-21 freshness=current|0|"
  )
  local caught=0 row name va rk want wrc wfind o r
  for row in "${ctl[@]}"; do
    IFS='|' read -r name va rk want wrc wfind <<<"$row"
    printf 'source: S001 fixture\nverified-at: %s\nrecheck: %s\n\n## Body\n' "$va" "$rk" >"$W/c2/c2-$name.md"
    r=0; o=$(bash "$G" verify-metadata "$W/c2/c2-$name.md" --root "$W/c2" --as-of "$AS_OF" 2>&1) || r=$?
    if [[ $r == "$wrc" && $o == *"$want verdict="* && ( -z $wfind || $o == *"FINDING $wfind "* ) ]]; then
      caught=$((caught + 1)); echo "control c2-$name ok rc=$r"
    else
      echo "control c2-$name MISS rc=$r"
    fi
  done
  echo "C2_CONTROLS_CAUGHT=$caught/6"
}

c3() {
  echo "== C3 calibration: criterion-6 registry link (--registry)"
  mkdir -p "$W/c3/corpus/knowledge"
  local K=$W/c3/corpus/knowledge
  cat >"$W/c3/SOURCES.md" <<'EOF'
# SOURCES fixture

## Registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S001 | fixture one | docs | A | fixture | a | t | mined | 2026-10-21 | 90d | corpus/knowledge/c3-good.md, corpus/knowledge/c3-bare.md |
| S002 | fixture two | docs | A | fixture | a | t | queued | 2026-10-21 | 90d | — |
| S003 | fixture three | docs | A | fixture | a | t | mined | 2026-10-21 | 90d | corpus/knowledge/other.md |
EOF
  local -a ctl=(
    "good|S001 https://example.org/a anchor|2026-10-20 checked the anchor quote|0|"
    "missing|S999 https://example.org/z anchor|2026-10-20 checked the anchor quote|1|META_SOURCE_ROW_MISSING"
    "queued|S002 https://example.org/b anchor|2026-10-20 checked the anchor quote|1|META_SOURCE_NOT_MINED"
    "usedby|S003 https://example.org/c anchor|2026-10-20 checked the anchor quote|1|META_SOURCE_USEDBY_MISSING"
    "bare|S001 https://example.org/a anchor|2026-10-20|1|META_VERIFIED_AT_BARE"
    "noid|https://example.org/n anchor|2026-10-20 checked the anchor quote|0|META_SOURCE_NO_ROW_ID"
  )
  local caught=0 pos=0 row name src va wrc wfind o r
  for row in "${ctl[@]}"; do
    IFS='|' read -r name src va wrc wfind <<<"$row"
    printf 'source: %s\nverified-at: %s\nrecheck: 90d\n\n## Body\n' "$src" "$va" >"$K/c3-$name.md"
    r=0; o=$(bash "$G" verify-metadata "$K/c3-$name.md" --root "$W/c3" --registry "$W/c3/SOURCES.md" 2>&1) || r=$?
    if [[ $name == good ]]; then
      if [[ $r == 0 && $o == *'findings=0 drift=0'* ]]; then pos=1; echo "control c3-good ok rc=$r"; else echo "control c3-good MISS rc=$r"; fi
      continue
    fi
    if [[ $r == "$wrc" && $o == *"FINDING $wfind "* ]]; then
      caught=$((caught + 1)); echo "control c3-$name ok rc=$r"
    else
      echo "control c3-$name MISS rc=$r"
    fi
  done
  echo "C3_CONTROLS_CAUGHT=$caught/5"
  echo "C3_POSITIVE_CLEAN=$pos/1"
  mkdir -p "$W/pop24/corpus/knowledge"
  for f in "${POP24[@]}"; do cp "$W/frozen/$f" "$W/pop24/corpus/knowledge/$f"; done
  cp "$W/SOURCES-base.md" "$W/pop24/SOURCES.md"
  r=0; o=$(bash "$G" verify-metadata "$W/pop24/corpus/knowledge" --root "$W/pop24" --registry "$W/pop24/SOURCES.md" 2>&1) || r=$?
  echo "c3 pop24 rc=$r"
  printf '%s\n' "$o" | grep -E '^(META entry=|FINDING META_(SOURCE|VERIFIED_AT_BARE|REGISTRY))' || true
  local clean=0
  if [[ $r == 0 || $r == 1 ]]; then clean=$(printf '%s\n' "$o" | grep -c '^META entry=.* verdict=clean$' || true); fi
  echo "C3_POP_R24PLUS_CLEAN=$clean/5"
}

holds() {
  echo "== holds: selftest, drift vs r12 baseline, r1 archive observable"
  ( cd "$TREE" && bash tools/research-gate.sh --selftest 2>&1 | grep -E '^(ok-case|FAIL-case|RESEARCH_GATE_SELFTEST)' > "$W/selftest.txt" ) || true
  tail -1 "$W/selftest.txt"
  echo "LEGACY_CASES_SHA=$(grep -E '^ok-case' "$W/selftest.txt" | head -161 | sha256sum | cut -d' ' -f1) (first 161 ok-case lines)"
  ( cd "$TREE" && rc=0 && { bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json >"$W/drift.txt" 2>&1 || rc=$?; } && tail -1 "$W/drift.txt" && echo "drift rc=$rc" )
  ( cd "$TREE" && python3 -c 'import subprocess,sys; f=sys.argv[1]; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify",f+"/research/deep-research-2026-09-28/"+n,"--root",f],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))' "$FLEET" )
}

case $PART in
  c1) c1 ;; c2) c2 ;; c3) c3 ;; holds) holds ;;
  all) c1; c2; c3; holds ;;
  *) echo "unknown part: $PART" >&2; exit 2 ;;
esac
