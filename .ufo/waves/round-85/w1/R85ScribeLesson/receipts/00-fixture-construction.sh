#!/bin/sh
# Reproduce every fixture used by receipts 01-04 and 13 from the landing revision alone.
#
# Scratch root: /fast/scratch/hyaku/chousa-r85/R85ScribeLesson
# Usage:  sh 00-fixture-construction.sh
#
# Each fixture is a copy of the pristine landing tree with exactly one documented edit,
# so a reviewer can see which bytes changed and which were left alone.
#
#   tree/  pristine landing tree (receipts 03, 05, 06, 11, 12)
#   b1/    prefreeze ground: source: line = S020, S023, S215; every quote re-sourced to S215
#          (all seven quotes stay located, so only the GROUND rules E6/E7 can fire)   -> receipt 01
#   b2/    fresh_sources=2 attempt: source: line = S215, S026, S023 (S023 named but not
#          FRESH for this entry)                                                      -> receipt 02
#   b3/    prefreeze numeric floors on the amended ground: + one S215 quote (Q8) and
#          one extra decision row                                                       -> receipt 04
#   b4/    E7 in isolation: S023 made FRESH (registry used-by) and named on source: line -> receipt 13
set -e
S=/fast/scratch/hyaku/chousa-r85/R85ScribeLesson
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
REV=64803d33362f50cf9094e91fc3a4a07216c563ca
rm -rf "$S/tree" "$S/b1" "$S/b2" "$S/b3" "$S/b4" "$S/spotcheck"
mkdir -p "$S/tree"
git -C "$LANE" archive "$REV" | tar -x -C "$S/tree"     # tree/ = pristine landing tree
cp -a "$S/tree" "$S/b1"
cp -a "$S/tree" "$S/b2"
cp -a "$S/tree" "$S/b3"
cp -a "$S/tree" "$S/b4"
python3 - <<'PY'
import pathlib
B = pathlib.Path('/fast/scratch/hyaku/chousa-r85/R85ScribeLesson')

# --- b1: prefreeze ground. MINIMAL edit — only the source: line. All seven quotes stay
#     located (E3 passes), so only the GROUND rules E6/E7 can fire. ---------------------
p = B/'b1/corpus/knowledge/provenance-recording-r85.md'
t = p.read_text()
t = t.replace('source: S215, S026, S024', 'source: S020, S023, S215')
p.write_text(t)

# --- b2: the frozen predicate's own number, fresh_sources=2. MINIMAL edit — only the
#     source: line. S023 is named but not FRESH for this entry (its registry used-by
#     names the round-84 entry), so E6 fires and fresh_sources drops to 2. -----------
p = B/'b2/corpus/knowledge/provenance-recording-r85.md'
t = p.read_text()
t = t.replace('source: S215, S026, S024', 'source: S215, S026, S023')
p.write_text(t)

# --- b3: the PREFREEZE numeric floors (rows>=7, located_quotes>=8) on the amended ground.
p = B/'b3/corpus/knowledge/provenance-recording-r85.md'
t = p.read_text()
t = t.replace('| Q7 | S024 | "Date on which the content on this web page was last reviewed for accuracy and/or completeness." |',
 '| Q7 | S024 | "Date on which the content on this web page was last reviewed for accuracy and/or completeness." |\n'
 '| Q8 | S215 | "By expressing usage and generation, one can construct provenance chains comprising both Activities and Entities." |')
row = ('| Recording how an entity was generated | state the activity that generated the entity and the activity that invalidated it | '
       "record an entity's lifetime without naming the activities that produced it | Q8 (S215) |")
t = t.replace('\n## Inference', '\n' + row + '\n\n## Inference')
p.write_text(t)

# --- b4: E7 in isolation. Make S023 FRESH for this entry (registry used-by) and name it
#     on the source: line. E6 can then no longer fire; E7 still does because S023 is
#     source:-cited by the base-list entry search-transparency-reporting-r84.md. --------
sp = B/'b4/corpus/SOURCES.md'
t = sp.read_text()
before = [l for l in t.splitlines() if l.startswith('| S023 ')][0]
cells = before.split('|')
cells[11] = ' corpus/knowledge/search-transparency-reporting-r84.md, corpus/knowledge/provenance-recording-r85.md '
sp.write_text(t.replace(before, '|'.join(cells)))
p = B/'b4/corpus/knowledge/provenance-recording-r85.md'
t = p.read_text()
t = t.replace('source: S215, S026, S024', 'source: S215, S026, S023')
t = t.replace('| Q4 (S215) |', '| Q4 (S215), S023 |')
p.write_text(t)
print("fixtures written: b1 b2 b3 b4")
PY

# --- the two planned-reject rows the Gate addendum hands the non-author spot-check ------
mkdir -p "$S/spotcheck"
cat > "$S/spotcheck/planned-reject-s033.md" <<'EOF'
GATE-RECORD S033 url=https://www.w3.org/TR/prov-o/ fetched=2026-11-08T04:15:56Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
EOF
cat > "$S/spotcheck/planned-reject-s020.md" <<'EOF'
GATE-RECORD S020 url=https://www.w3.org/TR/prov-o/ fetched=2026-11-08T03:54:43Z tier=A decision=reject capture=none curl_rc=22 http=403 words=0 quote=none
EOF
echo "spotcheck rows written"
