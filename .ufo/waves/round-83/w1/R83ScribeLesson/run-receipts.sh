#!/bin/sh
# R83ScribeLesson receipts. Read-only against the lane; writes only under this seat's output folder.
set -u
LANE=/home/vgpnk/Projects/shokunin/chousa-shokunin
OUT="$LANE/.ufo/waves/round-83/w1/R83ScribeLesson/receipts"
S=/fast/scratch/hyaku/chousa-r83/R83ScribeLesson
mkdir -p "$OUT" "$S"
cd "$LANE" || exit 1
echo "host=$(hostname) date=$(date -u +%Y-%m-%dT%H:%M:%SZ) lane=$LANE" > "$OUT/00-env.txt"
echo "git=$(git rev-parse HEAD)" >> "$OUT/00-env.txt"

# ---------- 01 knowledge recount ----------
{
  echo "# knowledge entry recount: .md files vs all files"
  echo "# SCORECARD.md:3756 claims 'knowledge 94 -> 95'; round-82-verifier-spotcheck.md:24 names the .gitkeep"
  echo
  for rev in 142b6f0c08e645ef9507f6d880be44e518c39043 03b586d1; do
    echo "\$ git -C $LANE ls-tree -r --name-only $rev corpus/knowledge | grep -c '\\.md\$'"
    git -C "$LANE" ls-tree -r --name-only "$rev" corpus/knowledge | grep -c '\.md$'
    echo "rc=$?"
    echo "\$ git -C $LANE ls-tree -r --name-only $rev corpus/knowledge | wc -l"
    git -C "$LANE" ls-tree -r --name-only "$rev" corpus/knowledge | wc -l
    echo "rc=$?"
    echo "\$ git -C $LANE ls-tree -r --name-only $rev corpus/knowledge | grep -c 'gitkeep'"
    git -C "$LANE" ls-tree -r --name-only "$rev" corpus/knowledge | grep -c 'gitkeep'
    echo "rc=$?"
    echo
  done
  echo "# discriminator: claimed count vs .md count (MATCH/MISMATCH)"
  for pair in "142b6f0c 94" "142b6f0c 93" "03b586d1 95" "03b586d1 94"; do
    set -- $pair
    md=$(git -C "$LANE" ls-tree -r --name-only "$1" corpus/knowledge | grep -c '\.md$')
    if [ "$md" = "$2" ]; then v=MATCH; else v=MISMATCH; fi
    echo "RECOUNT_CHECK rev=$1 claimed=$2 md=$md $v"
  done
} > "$OUT/01-knowledge-recount.txt" 2>&1

# ---------- 02 gate-records verify ----------
{
  echo "# whole lesson"
  echo "\$ python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md"
  python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md
  echo "RC=$?"
  echo
  echo "# per-record extract (S213) in scratch"
  grep '^GATE-RECORD S213 ' corpus/lessons/round-83.md > "$S/s213-only.md"
  wc -l "$S/s213-only.md"
  echo "\$ python3 tools/gate-records.py verify --root . $S/s213-only.md"
  python3 tools/gate-records.py verify --root . "$S/s213-only.md"
  echo "RC=$?"
  echo
  echo "# per-record extract (S009) in scratch"
  grep '^GATE-RECORD S009 ' corpus/lessons/round-83.md > "$S/s009-only.md"
  echo "\$ python3 tools/gate-records.py verify --root . $S/s009-only.md"
  python3 tools/gate-records.py verify --root . "$S/s009-only.md"
  echo "RC=$?"
} > "$OUT/02-gate-verify.txt" 2>&1

# ---------- 03 hand location of the three Gate records ----------
{
  echo "# hand location command, round-82 form"
  LOC='import sys;t=" ".join(open(sys.argv[1],encoding="utf-8",errors="replace").read().split());print("FOUND" if " ".join(sys.argv[2].split()) in t else "ABSENT")'
  echo "# LOC=$LOC"
  echo
  echo "## S009 capture ea16817cb78993196ea1a095"
  echo "\$ python3 -c \"\$LOC\" corpus/captures/ea16817cb78993196ea1a095.txt '<quote>'"
  python3 -c "$LOC" corpus/captures/ea16817cb78993196ea1a095.txt 'Collect the source of information for each risk of bias judgement (e.g. quotation, summary of information from a trial report, correspondence with investigator etc.).'
  echo "rc=$?"
  printf '%s\n' 'Collect the source of information for each risk of bias judgement (e.g. quotation, summary of information from a trial report, correspondence with investigator etc.).' | wc -w
  echo
  echo "## S212 capture 708022d401fd771fc59bd1d9"
  python3 -c "$LOC" corpus/captures/708022d401fd771fc59bd1d9.txt 'Risk-of-bias assessments in Cochrane reviews should be performed independently by at least two people'
  echo "rc=$?"
  printf '%s\n' 'Risk-of-bias assessments in Cochrane reviews should be performed independently by at least two people' | wc -w
  echo
  echo "## S213 capture 963807d173af711593fd1c45"
  python3 -c "$LOC" corpus/captures/963807d173af711593fd1c45.txt 'Answers to signalling questions and judgements about risk of bias should be supported by written justifications.'
  echo "rc=$?"
  printf '%s\n' 'Answers to signalling questions and judgements about risk of bias should be supported by written justifications.' | wc -w
  echo
  echo "## capture sha256 vs record prefixes (full digests)"
  sha256sum corpus/captures/ea16817cb78993196ea1a095.txt corpus/captures/708022d401fd771fc59bd1d9.txt corpus/captures/963807d173af711593fd1c45.txt
  echo "## refetch rows for the three keys"
  grep -n 'ea16817cb78993196ea1a095\|708022d401fd771fc59bd1d9\|963807d173af711593fd1c45' corpus/evidence/round57/refetch.tsv | cut -c1-260
} > "$OUT/03-gate-locate.txt" 2>&1

# ---------- 04 reject: Millard et al. inside S212 ----------
{
  echo "# reject candidate: the Millard et al. study result quoted inside S212"
  echo "# lesson text: 'the Millard et al. finding quoted inside S212 (one reviewer for about one-third of articles"
  echo "#   with a machine-learning tool) - reject as support for any row'"
  echo
  echo "## hand location of the reject's quote in the S212 capture"
  LOC='import sys;t=" ".join(open(sys.argv[1],encoding="utf-8",errors="replace").read().split());print("FOUND" if " ".join(sys.argv[2].split()) in t else "ABSENT")'
  python3 -c "$LOC" corpus/captures/708022d401fd771fc59bd1d9.txt 'about one-third of articles could be assessed by just one reviewer'
  echo "rc=$?"
  printf '%s\n' 'about one-third of articles could be assessed by just one reviewer' | wc -w
  echo
  echo "## capture line 622 (the paragraph, first 700 chars)"
  sed -n '622p' corpus/captures/708022d401fd771fc59bd1d9.txt | cut -c1-700
  echo
  echo "## capture line 611 (the chapter's own standard, the S212 record quote)"
  sed -n '611p' corpus/captures/708022d401fd771fc59bd1d9.txt | cut -c1-400
  echo
  echo "## is the reject in class as a GATE-RECORD? (tool sees 3 records, not 4)"
  python3 tools/gate-records.py verify --root . corpus/lessons/round-83.md
  echo "RC=$?"
  echo
  echo "## the entry's own limit note (lines 69-70)"
  sed -n '69,70p' corpus/knowledge/appraisal-judgment-records-r83.md
  echo
  echo "## does the entry cite Millard anywhere in a decision row? (0 = no)"
  grep -c -i 'millard' corpus/knowledge/appraisal-judgment-records-r83.md
} > "$OUT/04-reject-millard.txt" 2>&1

# ---------- 05 considerthese ----------
{
  echo "# considerthese newest files, read-only"
  ls -la considerthese/ | tail -4
  md5sum considerthese/2026-11-05.md considerthese/2026-11-06.md
  echo
  echo "## proposal named: 2026-11-06 'One open Gate-record S-id per daily review'"
  echo "## ScoutA remainder ids: S170 S171 S173 S174 S175 S176 S178 S179 S182 S183 S191 S193"
  echo "\$ grep -rhoE 'S170|S171|S173|S174|S175|S176|S178|S179|S182|S183|S191|S193' corpus/evidence/round83/ corpus/lessons/round-83.md .ufo/waves/round-83/ | wc -l"
  grep -rhoE 'S170|S171|S173|S174|S175|S176|S178|S179|S182|S183|S191|S193' corpus/evidence/round83/ corpus/lessons/round-83.md .ufo/waves/round-83/ 2>/dev/null | wc -l
  echo
  echo "## ids the round-83 Gate block actually touches"
  grep -o 'GATE-RECORD S[0-9]*' corpus/lessons/round-83.md
  echo
  echo "## proposal->adoption ledger rows and any 2026-11-05/06 row"
  wc -l corpus/evidence/round54/considerthese-ledger.tsv
  grep -c 'CT-2026110' corpus/evidence/round54/considerthese-ledger.tsv
  echo "rc=$?"
  tail -1 corpus/evidence/round54/considerthese-ledger.tsv
} > "$OUT/05-considerthese.txt" 2>&1

# ---------- 06 assimilation ----------
{
  echo "# assimilation re-count"
  echo "\$ wc -l .ufo/waves/round-78/assimilation/collisions"
  wc -l .ufo/waves/round-78/assimilation/collisions
  echo "\$ wc -l .ufo/waves/round-78/assimilation/staged-ids"
  wc -l .ufo/waves/round-78/assimilation/staged-ids
  echo "\$ wc -l .ufo/waves/round-78/assimilation/reg-ids"
  wc -l .ufo/waves/round-78/assimilation/reg-ids
  echo "\$ grep -c '^| S[0-9]' corpus/SOURCES.md"
  grep -c '^| S[0-9]' corpus/SOURCES.md
  echo "\$ git log -1 --format='%h %ad' --date=short -- .ufo/waves/round-78/assimilation/collisions"
  git log -1 --format='%h %ad' --date=short -- .ufo/waves/round-78/assimilation/collisions
  echo "\$ ls .ufo/waves/round-83/assimilation 2>&1"
  ls .ufo/waves/round-83/assimilation 2>&1
  echo "rc=$?"
} > "$OUT/06-collisions.txt" 2>&1

echo "receipts written to $OUT"
ls -la "$OUT"
