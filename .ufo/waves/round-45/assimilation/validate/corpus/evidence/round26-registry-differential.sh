#!/usr/bin/env bash
# Round-26 registry differential. Optional argument selects the gate tree;
# frozen inputs and the oracle remain pinned to the registered base commit.
set -uo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO=$(cd "$SCRIPT_DIR/../.." && pwd)
BASE=ba3333254dd337658a4f25e7a9471f9cf4e4567e
ORACLE=$SCRIPT_DIR/round26-registry-oracle.py
GATE_TREE=${1:-$REPO}
if [[ ! -d $GATE_TREE ]]; then
  printf 'gate tree is not a directory: %s\n' "$GATE_TREE" >&2
  exit 2
fi
GATE_TREE=$(cd "$GATE_TREE" && pwd)
GATE=$GATE_TREE/tools/research-gate.sh
if [[ ! -f $GATE ]]; then
  printf 'gate not found: %s\n' "$GATE" >&2
  exit 2
fi
if ! git -C "$REPO" cat-file -e "$BASE^{commit}" 2>/dev/null; then
  printf 'frozen base commit is unavailable: %s\n' "$BASE" >&2
  exit 2
fi

TMP=$(mktemp -d /tmp/chousa-r26-registry-diff.XXXXXX) || exit 2
trap 'rm -rf "$TMP"' EXIT
RESULTS=$TMP/results.tsv
: >"$RESULTS"

POP29=(
  anchor-boundaries-r4.md archived-export-intake.md archives-verified-r9.md
  audit-r11.md chain-resolution-r3.md citation-chain-fidelity-r24.md
  claim-support-states-r24.md claim-verification-r2.md
  contextual-source-admission-r24.md denylist-r22.md fenced-anchor-r23.md
  fenced-heading-r17.md gate-baseline-r12.md gate-baseline-r8.md
  hardening-r10.md hardlink-alias-r13.md html-comment-r20.md
  json-delimiter-r24.md metadata-screen-r25.md mount-alias-r14.md
  pointer-boundary-r21.md reference-integrity-r7.md root-slash-boundary-r15.md
  scope-phrase-gap-r18.md scope-refusal-r12.md sweep-symlink-r19.md
  sweeps-rejections-r5.md verification-r16.md verify-all-r6.md
)
POP24=(
  citation-chain-fidelity-r24.md claim-support-states-r24.md
  contextual-source-admission-r24.md json-delimiter-r24.md metadata-screen-r25.md
)

make_frozen_suite() {
  local label=$1
  shift
  local root=$TMP/$label/root dir=$TMP/$label/root/corpus/knowledge name
  mkdir -p "$dir" "$root/corpus"
  git -C "$REPO" show "$BASE:corpus/SOURCES.md" >"$root/corpus/SOURCES.md" || return 1
  for name in "$@"; do
    git -C "$REPO" show "$BASE:corpus/knowledge/$name" >"$dir/$name" || return 1
  done
  run_suite "$label" "$root" "$dir" "$root/corpus/SOURCES.md"
}

run_suite() {
  local label=$1 root=$2 dir=$3 registry=$4
  local output=$TMP/$label.gate oracle=$TMP/$label.oracle.json err=$TMP/$label.stderr
  local gate_rc oracle_rc
  if bash "$GATE" verify-metadata "$dir" --root "$root" --registry "$registry" >"$output" 2>"$err"; then
    gate_rc=0
  else
    gate_rc=$?
    if ((gate_rc > 1)); then
      printf 'GATE_ERROR %s rc=%s: ' "$label" "$gate_rc" >&2
      tr '\n' ' ' <"$err" >&2
      printf '\n' >&2
    fi
  fi
  if python3 "$ORACLE" "$dir" --root "$root" --registry "$registry" >"$oracle" 2>"$TMP/$label.oracle.stderr"; then
    oracle_rc=0
  else
    oracle_rc=$?
  fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$label" "$output" "$oracle" "$gate_rc" "$oracle_rc" >>"$RESULTS"
}

make_frozen_suite r24plus "${POP24[@]}" || exit 2
make_frozen_suite pop29 "${POP29[@]}" || exit 2

ADV_ROOT=$TMP/adversarial/root
ADV_DIR=$ADV_ROOT/corpus/knowledge
ADV_REGISTRY=$ADV_ROOT/corpus/SOURCES.md
mkdir -p "$ADV_DIR" "$ADV_ROOT/corpus"
python3 - "$ADV_ROOT" <<'PY'
from pathlib import Path
import sys

root = Path(sys.argv[1])
knowledge = root / "corpus" / "knowledge"
knowledge.mkdir(parents=True, exist_ok=True)

# Table columns are reordered and an extra column is present. The rows remain
# within the SOURCES contract v1 rule that no cell contains a literal pipe.
# OUT-OF-CONTRACT observation: `escaped\|pipe` was requested initially, but a
# pipe is forbidden inside cells and is therefore excluded from the core diff.
columns = (
    "note", "used-by", "id", "source", "kind", "tier", "scope", "anchor",
    "teaches", "status", "opened", "recheck",
)
registry_rows = [
    ("pipe-token", "corpus/knowledge/adv-pipe-token.md", "S001", "fixture one — https://example.test/one", "docs", "A", "fixture", "anchor one", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("extra", "corpus/knowledge/adv-extra.md", "S002", "fixture two — https://example.test/two", "docs", "A", "fixture", "anchor two", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("reordered", "corpus/knowledge/adv-reordered.md", "S003", "fixture three — https://example.test/three", "docs", "A", "fixture", "anchor three", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("trailing", "corpus/knowledge/adv-trailing.md   , corpus/knowledge/other.md  ", "S004", "fixture four — https://example.test/four", "docs", "A", "fixture", "anchor four", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("dot-prefix", "./corpus/knowledge/adv-dot.md", "S005", "fixture five — https://example.test/five", "docs", "A", "fixture", "anchor five", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("basename-only", "knowledge/adv-basename.md", "S006", "fixture six — https://example.test/six", "docs", "A", "fixture", "anchor six", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("continuation", "corpus/knowledge/adv-continuation.md", "S007", "fixture seven — https://example.test/seven", "docs", "A", "fixture", "anchor seven", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("queued", "—", "S008", "fixture eight — https://example.test/eight", "docs", "A", "fixture", "anchor eight", "fixture teaching", "queued", "2026-10-21", "90d"),
    ("other-path", "corpus/knowledge/not-this-entry.md", "S009", "fixture nine — https://example.test/nine", "docs", "A", "fixture", "anchor nine", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("bare", "corpus/knowledge/adv-bare.md", "S010", "fixture ten — https://example.test/ten", "docs", "A", "fixture", "anchor ten", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("fenced", "corpus/knowledge/adv-fenced.md", "S011", "fixture eleven — https://example.test/eleven", "docs", "A", "fixture", "anchor eleven", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("first-duplicate", "—", "S012", "fixture twelve — https://example.test/twelve", "docs", "A", "fixture", "anchor twelve", "fixture teaching", "queued", "2026-10-21", "90d"),
    ("second-duplicate", "corpus/knowledge/adv-duplicate.md", "S012", "fixture duplicate — https://example.test/duplicate", "docs", "A", "fixture", "anchor duplicate", "fixture teaching", "mined", "2026-10-21", "90d"),
    ("four-digits", "corpus/knowledge/adv-long-id.md", "S0001", "fixture four digits — https://example.test/four-digits", "docs", "A", "fixture", "anchor four digits", "fixture teaching", "mined", "2026-10-21", "90d"),
]
table = [
    "# Generated adversarial registry",
    "",
    "| " + " | ".join(columns) + " |",
    "|" + "|".join("---" for _ in columns) + "|",
]
table.extend("| " + " | ".join(row) + " |" for row in registry_rows)
registry = "\n".join(table) + "\n"
(root / "corpus" / "SOURCES.md").write_text(registry, encoding="utf-8")

entries = {
    "adv-pipe-token.md": "source: S001 https://example.test/a\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-extra.md": "source: S002 https://example.test/b\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-reordered.md": "source: S003 https://example.test/c\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-trailing.md": "source: S004 https://example.test/d\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-dot.md": "source: S005 https://example.test/e\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-basename.md": "source: S006 https://example.test/f\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-continuation.md": "source:\n  opened S007 at the located anchor\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-queued.md": "source: S008 https://example.test/h\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-other-usedby.md": "source: S009 https://example.test/i\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-bare.md": "source: S010 https://example.test/j\nverified-at: 2026-10-21\nrecheck: 90d\n\n## Claim\n",
    "adv-fenced.md": "```\nsource: S099\nverified-at: 2026-10-21\n## Fenced fake heading\n```\nsource: S011 https://example.test/k\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Real heading\nsource: S099\n",
    "adv-noid.md": "source: xS001 S001x _S001 S001_\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-long-id.md": "source: S0001 https://example.test/m\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
    "adv-duplicate.md": "source: S012 https://example.test/n\nverified-at: 2026-10-21 opened the source\nrecheck: 90d\n\n## Claim\n",
}
for name, content in entries.items():
    (knowledge / name).write_text(content, encoding="utf-8")

outside = root.parent / "out-of-contract-escaped-pipe"
outside_knowledge = outside / "corpus" / "knowledge"
outside_knowledge.mkdir(parents=True, exist_ok=True)
(outside / "corpus" / "SOURCES.md").write_text(
    "# Out-of-contract escaped-pipe cell\n\n"
    "| id | status | used-by | note |\n"
    "|---|---|---|---|\n"
    "| S900 | mined | corpus/knowledge/escaped-pipe.md | escaped\\|pipe |\n",
    encoding="utf-8",
)
(outside_knowledge / "escaped-pipe.md").write_text(
    "source: S900\nverified-at: 2026-10-21 checked the source\nrecheck: 90d\n",
    encoding="utf-8",
)
print("OUT_OF_CONTRACT_ESCAPED_PIPE=excluded (CORPUS contract v1 forbids | inside a cell)")
PY
run_suite adversarial "$ADV_ROOT" "$ADV_DIR" "$ADV_REGISTRY"

python3 - "$RESULTS" <<'PY'
import json
import re
import sys
from pathlib import Path

expected_counts = {"r24plus": 5, "pop29": 29, "adversarial": 14}
finding_re = re.compile(
    r"^FINDING (META_SOURCE_NO_ROW_ID|META_SOURCE_ROW_MISSING|"
    r"META_SOURCE_NOT_MINED|META_SOURCE_USEDBY_MISSING|"
    r"META_VERIFIED_AT_BARE)\b.*\bobs=entry=([^\s]+)",
    re.MULTILINE,
)
meta_re = re.compile(r"^META entry=([^ ]+)(?: |$)", re.MULTILINE)
rows = Path(sys.argv[1]).read_text(encoding="utf-8").splitlines()
labels = [row.split("\t", 1)[0] for row in rows]
matched = 0
total = sum(expected_counts.values())
failed = len(labels) != len(expected_counts) or set(labels) != set(expected_counts)
if failed:
    print(
        f"DISAGREE suites observed={sorted(labels)} "
        f"required={sorted(expected_counts)}"
    )
seen = set()
for row in rows:
    label, gate_path, oracle_path, gate_rc_text, oracle_rc_text = row.split("\t")
    if label not in expected_counts:
        print(f"DISAGREE unexpected suite={label}")
        failed = True
        continue
    if label in seen:
        print(f"DISAGREE duplicate suite={label}")
        failed = True
        continue
    seen.add(label)

    gate_rc, oracle_rc = int(gate_rc_text), int(oracle_rc_text)
    gate_text = Path(gate_path).read_text(encoding="utf-8", errors="replace")
    try:
        expected = json.loads(Path(oracle_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        expected = {}

    meta_names = meta_re.findall(gate_text)
    actual = {name: set() for name in meta_names}
    for finding_id, name in finding_re.findall(gate_text):
        actual.setdefault(name, set()).add(finding_id)

    fixed_count = expected_counts[label]
    gate_ran = (
        gate_rc in (0, 1)
        and "METADATA_COMPLETE=" in gate_text
        and "RESEARCH_GATE:" in gate_text
    )
    exact_entries = (
        len(meta_names) == len(set(meta_names))
        and set(meta_names) == set(expected)
        and set(actual) == set(expected)
    )
    suite_valid = (
        len(expected) == fixed_count
        and bool(expected)
        and gate_ran
        and oracle_rc == 0
        and exact_entries
    )
    suite_agree = 0
    if not suite_valid:
        failed = True
        print(
            f"DISAGREE {label} suite gate_rc={gate_rc} oracle_rc={oracle_rc} "
            f"expected_entries={len(expected)} required_entries={fixed_count} "
            f"gate_entries={len(meta_names)}"
        )

    for name in sorted(expected):
        want = set(expected[name])
        got = actual.get(name, set())
        ok = suite_valid and got == want
        if ok:
            matched += 1
            suite_agree += 1
        else:
            failed = True
            print(
                f"DISAGREE {label} entry={name} gate_rc={gate_rc} oracle_rc={oracle_rc} "
                f"expected={sorted(want)} gate={sorted(got)}"
            )
    print(f"REGISTRY_DIFF_SUITE={label} {suite_agree}/{fixed_count}")

for label in sorted(set(expected_counts) - seen):
    print(f"DISAGREE {label} suite missing")
    print(f"REGISTRY_DIFF_SUITE={label} 0/{expected_counts[label]}")
    failed = True
print(f"REGISTRY_DIFF_AGREE={matched}/{total}")
sys.exit(0 if total > 0 and matched == total and not failed else 1)
PY
