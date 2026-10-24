#!/usr/bin/env bash
# Round-25 counting probe (chousa-shokunin). From the lane root:
#   bash corpus/evidence/round25-measure.sh <tree-root>
# From elsewhere, use this script's absolute path and an explicit tree root.
# <tree-root> is a lane checkout: the landing commit, or the claim base
# d730ae4 unpacked (`git -C <lane> archive d730ae4 | tar -x -C <dir>`).
# Read-only. Populations are frozen in corpus/evidence/round25-claims.md
# (the base-commit file lists below are the frozen populations).
# Exit 0 means the measurements completed, not claim admission. Compare every
# printed count/status to the pre-registration; C2/C3 still need content review.
set -euo pipefail
R=${1:?tree root}
cd "$R" || exit 1
echo "== tree $(pwd -P) gate $(sha256sum tools/research-gate.sh | cut -c1-8)"

echo "== claim 1 (operability): metadata screen over the frozen 28-entry population"
POP1="anchor-boundaries-r4 archived-export-intake archives-verified-r9 audit-r11 chain-resolution-r3 citation-chain-fidelity-r24 claim-support-states-r24 claim-verification-r2 contextual-source-admission-r24 denylist-r22 fenced-anchor-r23 fenced-heading-r17 gate-baseline-r12 gate-baseline-r8 hardening-r10 hardlink-alias-r13 html-comment-r20 json-delimiter-r24 mount-alias-r14 pointer-boundary-r21 reference-integrity-r7 root-slash-boundary-r15 scope-phrase-gap-r18 scope-refusal-r12 sweep-symlink-r19 sweeps-rejections-r5 verification-r16 verify-all-r6"
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
for n in $POP1; do cp corpus/knowledge/$n.md "$T/" 2>/dev/null || { echo "missing population member: $n" >&2; exit 2; }; done
rc=0; out=$(bash tools/research-gate.sh verify-metadata "$T" --root "$T" 2>&1) || rc=$?
echo "verify-metadata rc=$rc"
printf '%s\n' "$out" | grep -E '^(FINDING META_|METADATA_|RESEARCH_GATE)' | sed "s#$T/##g" || true
named=$(printf '%s\n' "$out" | grep -E '^FINDING META_[A-Z_]+ severity=(warn|crit)' | sed "s#$T/##g" | grep -oE 'entry=[^ ]+' | sort -u | tr '\n' ' ' || true)
echo "META_NAMED_DRIFT_ENTRIES=[${named% }]"

echo "== claim 2 (freshness): stale index items (base population: files present at d730ae4)"
python3 - <<'PY'
import os, re
readme = open("corpus/README.md", encoding="utf-8").read()
base_files = """knowledge/anchor-boundaries-r4.md knowledge/archived-export-intake.md knowledge/archives-verified-r9.md knowledge/audit-r11.md knowledge/chain-resolution-r3.md knowledge/citation-chain-fidelity-r24.md knowledge/claim-support-states-r24.md knowledge/claim-verification-r2.md knowledge/contextual-source-admission-r24.md knowledge/denylist-r22.md knowledge/fenced-anchor-r23.md knowledge/fenced-heading-r17.md knowledge/gate-baseline-r12.md knowledge/gate-baseline-r8.md knowledge/hardening-r10.md knowledge/hardlink-alias-r13.md knowledge/html-comment-r20.md knowledge/json-delimiter-r24.md knowledge/mount-alias-r14.md knowledge/pointer-boundary-r21.md knowledge/reference-integrity-r7.md knowledge/root-slash-boundary-r15.md knowledge/scope-phrase-gap-r18.md knowledge/scope-refusal-r12.md knowledge/sweep-symlink-r19.md knowledge/sweeps-rejections-r5.md knowledge/verification-r16.md knowledge/verify-all-r6.md lessons/2026-10-15-anchor-token-boundaries.md lessons/2026-10-15-chain-hop-resolution.md lessons/2026-10-15-claims-span-fidelity.md lessons/2026-10-16-archive-scale-controls-and-ledger.md lessons/2026-10-16-gate-behavioral-baseline.md lessons/2026-10-16-reference-integrity.md lessons/2026-10-16-sweeps-rejections-verdict-bearing.md lessons/2026-10-16-verify-all-composition.md lessons/2026-10-16-verifying-conversion-not-original.md lessons/2026-10-19-hardlink-alias-boundary.md lessons/round-1.md lessons/round-24.md""".split()
assert "## Coverage map" in readme and "## Frontier" in readme, "README population absent"
for name in base_files:
    assert os.path.getsize("corpus/"+name)>0, "missing/empty base population member: "+name
cov = readme.split("## Frontier")[0]
unindexed = [f for f in base_files if ("| `%s`" % f) not in cov]
print("2a UNINDEXED=%d %s" % (len(unindexed), unindexed))
front = readme.split("## Frontier", 1)[1] if "## Frontier" in readme else ""
missing = [n for n in range(11, 24) if not re.search(r"^Round %d\b" % n, front, re.M)]
print("2b FRONTIER_MISSING=%d rounds=%s" % (len(missing), missing))
ev = open("corpus/evidence/README.md", encoding="utf-8").read().splitlines()
expected_receipts = [(12, 'scope-r12-20261019T115519Z-selftest.log'), (12, 'scope-r12-20261019T115519Z-A-fix.log'), (12, 'scope-r12-20261019T115519Z-drift-r8.log'), (13, 'alias-r13-20261019T123621Z-selftest.log'), (13, 'alias-r13-20261019T123621Z-bypass-before.log'), (13, 'alias-r13-20261019T123621Z-bypass-after.log'), (14, 'mount-r14-20261019T132025Z-selftest.log'), (14, 'mount-r14-20261019T132025Z-bypass-before.log'), (14, 'mount-r14-20261019T132025Z-bypass-after.log'), (14, 'mount-r14-20261019T132025Z-battery.log'), (13, 'alias-r13-20261019T123621Z-battery.log'), (15, 'root-r15-20261019T152000Z-selftest.log'), (15, 'root-r15-20261019T152000Z-demo.log'), (15, 'root-r15-20261019T152000Z-battery.log'), (15, 'root-r15-20261019T152000Z-drift.log'), (17, 'fence-r17-20261019T171200Z-selftest.log'), (17, 'fence-r17-20261019T171200Z-demo.log'), (17, 'fence-r17-20261019T171200Z-battery.log'), (17, 'fence-r17-20261019T171200Z-drift.log'), (18, 'scope-r18-20261019T173000Z-selftest.log'), (18, 'scope-r18-20261019T173000Z-demo.log'), (18, 'scope-r18-20261019T173000Z-battery.log'), (18, 'scope-r18-20261019T173000Z-drift.log'), (19, 'symlink-r19-20261019T174500Z-selftest.log'), (19, 'symlink-r19-20261019T174500Z-demo.log'), (19, 'symlink-r19-20261019T174500Z-battery.log'), (19, 'symlink-r19-20261019T174500Z-drift.log'), (20, 'verify-r20-20261019T180000Z-selftest.log'), (20, 'verify-r20-20261019T180000Z-demo.log'), (20, 'verify-r20-20261019T180000Z-battery.log'), (20, 'verify-r20-20261019T180000Z-drift.log'), (21, 'ptr-r21-20261019T184000Z-selftest.log'), (21, 'ptr-r21-20261019T184000Z-demo.log'), (21, 'ptr-r21-20261019T184000Z-battery.log'), (21, 'ptr-r21-20261019T184000Z-drift.log'), (22, 'deny-r22-20261019T190000Z-selftest.log'), (22, 'deny-r22-20261019T190000Z-demo.log'), (22, 'deny-r22-20261019T190000Z-battery.log'), (22, 'deny-r22-20261019T190000Z-drift.log'), (23, 'fanchor-r23-20261019T192000Z-selftest.log'), (23, 'fanchor-r23-20261019T192000Z-demo.log'), (23, 'fanchor-r23-20261019T192000Z-battery.log'), (23, 'fanchor-r23-20261019T192000Z-drift.log')]
assert any(l.startswith("## Round-") for l in ev), "evidence index empty or headings absent"
head, seen = None, {}
for l in ev:
    m = re.match(r"^## Round-(\d+)\b", l)
    if m: head = int(m.group(1)); continue
    if l.startswith("## "): head = None; continue
    m = re.match(r"^\| `([^`]+)`", l)
    if m: seen.setdefault(m.group(1), []).append(head)
mis = sum(seen.get(name) != [round_] for round_, name in expected_receipts)
print("2c EVIDENCE_MISFILED_ROWS=%d" % mis)
log = open("LOG.md", encoding="utf-8").read().splitlines()
claimed = sorted({int(m.group(1)) for l in log for m in [re.search(r"SCORECARD §Round (\d+)\)?.*Capabilities \+1", l)] if m})
assert claimed == [13,14,15,17,18,19,20,21,22,23], "LOG claimed population missing/changed"
sc = open("SCORECARD.md", encoding="utf-8").read()
rows = set()
for sec in re.split(r"^## ", sc, flags=re.M):
    if sec.startswith("Capabilities"):
        for l in sec.splitlines():
            c = [x.strip() for x in l.strip().strip("|").split("|")]
            if len(c) == 4 and c[3].isdigit(): rows.add(int(c[3]))
cm = [n for n in claimed if n not in rows]
print("2d CAP_ROWS_MISSING=%d rounds=%s (LOG Capabilities +1 rounds=%s)" % (len(cm), cm, claimed))
print("STALE_INDEX_ITEMS=%d" % (len(unindexed) + len(missing) + mis + len(cm)))
PY

echo "== claim 3 (calibration): stale restatements"
python3 - <<'PY'
import re
sk = open("SKILL.md", encoding="utf-8").read()
hr = open("corpus/knowledge/hardening-r10.md", encoding="utf-8").read()
assert len(sk)>1000 and "corpus/knowledge/hardening-r10.md" in sk, "SKILL population/owner pointer missing"
assert len(re.findall(r"^\|\s*\d+\s*\|", hr, re.M)) == 71, "ledger row population changed"
a = re.sub(r"\s+", " ", sk).count("remains open pending fix-or-absorb")
owner_ready = "python3 corpus/evidence/round25-ledger-recount.py" in sk
if not a and not owner_ready:
    a = 1  # Deleting the old phrase without the promised recount is not closure.
T = r"by-design (\d+) · carried (\d+) · closed (\d+) · finding (\d+) · operator (\d+)"
flat = lambda s: re.sub(r"\s+", " ", s.replace("**", ""))
led = re.findall(T, flat(hr)); latest = led[-1] if led else None
sk_t = re.findall(T, flat(sk))
b = sum(1 for t in sk_t if t != latest)
q_led = re.findall(r"queue (\d+) → (\d+)", flat(hr)); qlatest = q_led[-1][1] if q_led else None
sk_q = re.findall(r"(\d+)-item round-11", flat(sk))
bq = sum(1 for q in sk_q if q != qlatest)
raw_slots = hr.count("${GSHA}")
disposition = hr.split("### Round-25 append-only preservation correction", 1)
c = int(not (raw_slots == 1
    and 'Gate `91a01695…` → `${GSHA}…`.' in hr
    and len(disposition) == 2
    and "R25-GSHA-DISPOSITION: superseded by gate 6b17e50c" in disposition[1]))
add = dict(re.findall(r"^### Round-(\d+) addendum[^\n]*\n(.*?)(?=^### |\Z)", hr, re.M | re.S))
d = [n for n in range(16, 24) if str(n) not in add
     or len(add[str(n)].strip()) < 80
     or not re.search(r"\bE\d+\b", add[str(n)])
     or not re.search(r"\bcases?\b", add[str(n)])]
print("3a SKILL_OPEN_CLOSED_FINDING=%d" % a)
print("3b SKILL_LEDGER_TUPLES_STALE=%d of %d (latest ledger %s) QUEUE_STALE=%d of %d (latest queue %s)" % (b, len(sk_t), "·".join(latest or ()), bq, len(sk_q), qlatest))
print("3c PLACEHOLDER_GSHA_UNRESOLVED=%d (historical raw slots=%d)" % (c, raw_slots))
print("3d LEDGER_ADDENDA_MISSING=%d rounds=%s" % (len(d), d))
print("STALE_RESTATEMENTS=%d" % (a + b + bq + c + len(d)))
PY

echo "== holds: selftest, drift vs r12 baseline, r1 archive observable"
bash tools/research-gate.sh --selftest 2>&1 | tail -1
bash tools/research-gate.sh --drift corpus/evidence/gate-baseline-r12-20261019T115519Z.json; echo "drift rc=$?"
FLEET=${SHOKUNIN_ROOT:-/home/vgpnk/Projects/shokunin}
python3 -c 'import subprocess,sys; f=sys.argv[1]; names=("A-shokunin-tradition.md","B-multiagent-knowledge.md","C-rank-taxonomy.md"); rows=[subprocess.run(["bash","tools/research-gate.sh","verify",f+"/research/deep-research-2026-09-28/"+n,"--root",f],capture_output=True,text=True) for n in names]; print("VERDICT_BEARING_EXPORTS=%d/3" % sum(r.returncode==1 and sum(s.startswith("RESEARCH_GATE: DRIFT (") for s in r.stdout.splitlines())==1 for r in rows))' "$FLEET"
