# ExecCensus — round 49 w2 census-claim attack (seat report)

seat: ExecCensus (leaf executor, godspeed)
date: 2026-10-25
lane: /home/vgpnk/Projects/shokunin/chousa-shokunin (tip `87e93353`; `corpus/SOURCES.md` blob `56f3179c…` identical at `1254ab2`, `4ce61fc5`, `87e9335` and the working tree)
item attacked: `corpus/lessons/round-49.md` `## Census` — 95→103 rows; A 89→92, B 1→6; mined 71→79; the after-state `validate` block and its `exit=0`
files changed: only this report. Scratch `/dev/shm/chousa-r49-ExecCensus` (deleted).
No installs (RULES.md read; nothing needed). No fetch; L0 `8d77e6c1` open.

## 1. The two named commands, run at the lane

```
$ bash …/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
exit=0

$ bash …/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa
chousa	rows	103
chousa	tier.A	92   chousa	tier.B	6   chousa	tier.C	5
chousa	status.mined	79   chousa	status.queued	19   chousa	status.rejected	5
FLEET	rows	103  FLEET	tier.A	92  FLEET	tier.B	6  FLEET	tier.C	5  FLEET	tier.invalid	0
FLEET	status.queued	19  FLEET	status.mined	79  FLEET	status.rejected	5  FLEET	status.invalid	0  FLEET	missing	0
exit=0
```
Equality check of the lesson's after-block against this run (`re.findall` on the second
```text fence, vs stdout + `exit=`): `exact_match = True | lines 7 7`.

## 2. Round-48 awk recounts, end state and named base rev

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
103
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5;gsub(/[[:space:]]/,"",t);n[t]++}
  END{for(k in n)printf "%s=%d ",k,n[k];print ""}' corpus/SOURCES.md
A=92 B=6 C=5
$ same with s=$9 → mined=79 queued=19 rejected=5
$ malformed NF!=13 → 0

$ git show 414a2ec6cde05a921dbdd9e02e7ae56b0db647ef:corpus/SOURCES.md  (sha256 40e9ec7d…)
rows 95 · A=89 B=1 C=5 · mined=71 queued=19 rejected=5 · malformed 0
$ sources-census.sh census --file <base copy>
file	rows	95 · tier.A 89 · tier.B 1 · tier.C 5 · status.mined 71 · status.queued 19 · status.rejected 5
```

The round-48 pattern `S[0-9][0-9][0-9]+` means **S + at least 3 digits** (the third class
carries `+`), not 4 — verified equal to `{3,}` in gawk 5.4.1 and Python
(`("S001" ~ /S[0-9][0-9][0-9]+/) = 1`; `("S00" …) = 0`), so the manual count and
`grep -cE …{3,}` agree by construction. An independent Python parse gives `base rows 95
unique 95 min/max S001 S095` and `now rows 103 unique 103 min/max S001 S103`, `contiguous=True`.

## 3. Is the delta real, and is it only an append?

```
$ git diff --numstat 414a2ec6 -- corpus/SOURCES.md
10	0	corpus/SOURCES.md        # 0 removed lines
$ added ids → S096 S097 S098 S099 S100 S101 S102 S103
$ added tiers → S096:A S097:A S098:A S099:B S100:B S101:B S102:B S103:B
$ added statuses → mined ×8
S096..S103: opened=2026-10-25; recheck 180d,90d,90d,365d,180d,180d,180d,180d;
  used-by = aggregator-vs-source-r36.md (S096–S099), citation-count-semantics-r37.md (S100–S103);
  both files present on disk; all rows NF=13 under `-F'|'` (11 cells), E11/E03/E04 clean.
```
So A 89→92 (+3 = S096–S098), B 1→6 (+5 = S099–S103), mined 71→79 (+8), queued/rejected
unmoved, no existing row edited (the other 2 added lines are a blank and the Round 49
Provenance bullet, `@@ -271,6 +279,8 @@`). The refused staged NCPSSD homepage row is
absent: `grep -n 'ncpssd' corpus/SOURCES.md` → no output. Base-rev `validate` reproduced
with `--file` on the `414a2ec6` copy yields the same five W04 lines **including S053**,
i.e. the lesson's "Round start" block is faithful to that rev (its `ok` line names the
lane path because it was run against the lane). S053's W04 is inherited:
`git diff d4e6ef09 414a2ec6 -- corpus/SOURCES.md` adds only S095, a blank and the Round 48
bullet, and S052/S053 already shared `docs.python.org/3/library/socket.html` with
different fragments/scopes at `d4e6ef09` — the +1 W04 versus round-48's own report block
is that rev's inheritance, not round-49 adoption.

## 4. Instrument responsiveness (scratch mutants of the tip registry)

```
delete row S103           → rows 102, B 5, mined 78          (metric moves)
duplicate S103 as S096    → rows 104, B 7, mined 80; validate E03 "S096 duplicate id",
                            E04 duplicate url …c1b0fa89….pdf  (validate catches)
re-add S103 as 4-space-indented S104 → rows 103, unchanged  (0–3-space contract honoured)
copy S103 as S900 under `## Paths`   → census rows 103 (not counted),
                            validate E12 "S900 row outside Registry section"
```
The `rows` metric is Registry-section-aware: the outside row is invisible to it and is caught by E12, so 103 = rows inside `## Registry`, not a raw `| S### |` line count.

## 5. Calibration notes (not falsifications of the claim)

- `## Census`'s "Normalisation stripped" table records the *pre-strip* value in the
  used-by rows: S101 lists `source-type-taxonomy-r37.md, citation-count-semantics-r37.md`
  and S102/S103 list `…, chinese-search-log-r37.md`, while the appended cells hold only
  `citation-count-semantics-r37.md`. `ls corpus/knowledge | grep -iE 'chinese|source-type'`
  → none and the registry is E11-clean, so the two non-existent paths were correctly
  dropped; only the column's semantics (removed text vs original value) reads ambiguously.
- The working tree carries an uncommitted `LOG.md` (+11 lines, L1's round-49 entry,
  `git diff --numstat -- LOG.md` → `11 0`); `corpus/SOURCES.md` is clean. Lane tip is one
  commit past the named tool rev (`87e9335` "after-measurement at 4ce61fc5"), and
  SOURCES.md is byte-identical across all three round-49 revs, so no census number
  depends on which is measured.
- Fleet context (`census --root …`, no lane): `FLEET rows 3033` over 20 lanes,
  `missing 0`; chousa's 103 is included once (7 `chousa` metric lines), no double count.

## 6. Result

Every number in the frozen census claim reproduces: 95→103 rows, A 89→92, B 1→6,
C 5→5, mined 71→79, queued 19, rejected 5, malformed 0, `validate` exit 0 with exactly
the five inherited W04 lines, and the lesson's after-block matches the live run
byte-for-byte. No leg overstated the delta, no existing row was touched, the refused row
is absent, and I could not falsify any leg.

Risks: the five W04 warnings are inherited and unattributed this round; the census row
metric counts only `## Registry`, so a row appended elsewhere would be silent here
(validate E12 is the guard, shown above).

VERDICT: round-49 census claim (95→103; A 89→92, B 1→6; mined 71→79; validate exit 0) — holds — every figure reproduces at the named base rev and at the tip by four independent methods, the delta is a pure 8-row append with matching tiers/statuses, and the instrument is responsive to deletion, duplication, indentation and section mutants.
