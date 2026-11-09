# R97ExecC2Repro — frozen C2 reproduction from clean tree

Seat: R97ExecC2Repro. Attack target: freeze F `9a0ce2015f…`, base `c8087ac5…`. Tree cloned via
`git clone -q --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo` + checkout of F; all commands from the clone root. Receipts copied to `.ufo/waves/round-97/w1/R97ExecC2Repro-*.txt`.

## (a) Four counting commands — replayed exactly

| # | Command | Result | Exit |
|---|---|---|---|
| 1 | `python3 -B tools/gate-records.py verify --root . corpus/knowledge/press-checklist-questions-r97.md` | `GATE_RECORDS files=1 records=30 ok=30 fail=0` (29 S225/S226 quote records OK + S227 reject OK) | 0 |
| 2 | `bash tools/research-gate.sh verify-metadata corpus/knowledge/press-checklist-questions-r97.md --root .` | `METADATA_COMPLETE=1/1`, `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` | 0 |
| 3 | `python3 -B tools/search-rerun.py verify corpus/knowledge/press-checklist-questions-r97.md --root .` | `SEARCH_RERUN_SUMMARY searches=7 rev_match=7/7 tree_same=0/7 findings=0`, `SEARCH_RERUN: CLEAN` | 0 |
| 4 | `python3 -B corpus/evidence/round97/entry-controls-r97.py --root . --work $S/work` | `ENTRY_CONTROLS=PASS` with the exact predicate line `POSITIVE=1/1 FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SOLE_SUPPORT=2/2 CORROBORATION=2/2 SEARCHES=3/3 DO_NOTHING_REFUSED=1/1 ORACLE_REJECTED=1/1 GATE_RECORDS=30/30 LQ_BOUND=29/29 WARRANTS_OK=8/8 WARRANT_TERMS=8/8 LANE_FILLED=8/8 SOLE_SUPPORT=8/8 ONE_LINE=29/29 VERBATIM=10/26 LETTERS=14/26 METADATA=clean` | 0 |

Receipt: `.ufo/waves/round-97/w1/R97ExecC2Repro-counts.txt` (all four outputs + separability rerun, each with exit code).

**Separability note (C2 predicate 3, claims.md:79-81):** the base tool at `c8087ac5` (`git show …:tools/search-rerun.py`, saved outside the tree) re-runs the entry record and prints the same `rev_match=7/7` / `SEARCH_RERUN: CLEAN`, exit 0. Matches the lane's claimed receipt `after/c2-separable-base-tool.txt` (that `after/` dir is not committed at F — see minor finding below).

## (b) Independent re-derivation of `## Searches`

Materialised `git archive c8087ac5… corpus/captures | tar -x -C $S/base` (92 captures), then ran each row myself with GNU grep 3.12 (`/usr/bin/grep -l -F` / `-l -P`, `LC_ALL=C sort`):

| id | engine | recorded hits / set | mine | Match |
|---|---|---|---|---|
| Q1 `orphan lines` fixed | 0 / `-` | 0 | YES |
| Q2 `hits per line` fixed | 0 / `-` | 0 | YES |
| Q3 `Are there any spelling errors` fixed | 0 / `-` | 0 | YES |
| Q4 `truncation` fixed | 3 / `1a8c36c4…, c52a1f15…, c9d1e74c…` | 3, same set | YES |
| Q5 `[Ss]ubject headings?` regex | 4 / `1a8c36c4…, 371c5511…, c52a1f15…, c9d1e74c…` | 4, same set | YES |
| Q6 `proximity operators?` regex | 3 / `c52a1f15…, c9d1e74c…, e94691f5…` | 3, same set | YES |
| Q7 `PICO` fixed | 12 / `sha256:6ea7657c…c849` | 12; sha256 of my sorted list = `6ea7657c…c849`, identical | YES |

`rev_match=7/7` confirmed independently. Receipt: `R97ExecC2Repro-searches.txt`.

## (c) Independent quote lineage + corroboration (no lane scripts)

My own 17-line script (≤25 required) — pasted below — for every Located-quotes row finds the capture line(s) containing it in its own source's capture, then recounts corroboration (S225 quotes in S226, whitespace-collapsed verbatim, and letters-only):

```
#!/usr/bin/env python3
import re
R="/fast/scratch/hyaku/chousa-r97/R97ExecC2Repro/repo/"
t=open(R+"corpus/knowledge/press-checklist-questions-r97.md").read()
lq=re.findall(r"\| (L\d+) \| (S22[56]) \| \"(.*?)\" \|",t)
caps={"S225":open(R+"corpus/captures/347c55ba9be9d63afe17986e.txt").read().splitlines(),"S226":open(R+"corpus/captures/80a844fe287a1a26d4280251.txt").read().splitlines()}
miss=[]
for qid,src,q in lq:
    hits=[i+1 for i,ln in enumerate(caps[src]) if q in ln]
    print(qid,src,len(q),"lines",hits)
    if not hits: miss.append(qid)
s225=[q for i,s,q in lq if s=="S225"]
def n(s): return " ".join(s.split())
def l(s): return re.sub(r"[^a-z0-9]","",s.lower())
t226=open(R+"corpus/captures/80a844fe287a1a26d4280251.txt").read()
print("missing_line_quotes",miss)
print(f"VERBATIM {sum(n(q) in n(t226) for q in s225)}/{len(s225)} LETTERS {sum(l(q) in l(t226) for q in s225)}/{len(s225)}")
```

Output: all 29 quotes found on exactly one capture line each within their own source (`missing_line_quotes []`), including L21+L22 both on S225 capture line 74 (verifying the entry's L24-25 "two halves of one 32-word question on capture line 74" — line 74 has 30 words by `split()`; the quoted halves sum to 32 with the split mid-question, words counting differs but line claim is exact). **VERBATIM 10/26, LETTERS 14/26 — identical to the claim. No K5 difference.** Receipts: `R97ExecC2Repro-indep.py`, `R97ExecC2Repro-indep-output.txt`.

## Extra probes (kill-rule sweeps)

- **K2 (Do/Never overreach):** checked each decision row's Do against its warrant quotes — no row asserts what its quotes don't say (each Do is a faithful expansion of the cited questions; e.g. "hits per line" row Do "show the number of hits per line" = L6 verbatim parenthetical). No narrowing/withdrawal needed.
- **K3 (joined-line quotes):** every quote is a substring of a single capture line in its own source — zero joined-line quotes.
- **K4 (tier/scope overclaim):** S225 tier B / S226 tier C match `corpus/SOURCES.md:237-239`; S225's "derived from" is correctly framed as a citation, not verbatim status (entry L119-120). S227 reject row has `curl_rc=22 http=403 words=0 quote=none`, consistent with `corpus/evidence/round57/refetch.tsv:199` (`22 403`).
- **Lane-column factual check:** entry row 6 states `search-rerun.py` refuses a POSIX bracket class in a `regex` row — confirmed in the tool (`POSIX_CLASS_RE`, `tools/search-rerun.py:99,184-185`); row records "no combined lines" is consistent with the tool's single-line `where` evaluation. Row 7 cites PRISMA-S items 9/10 (S222) — out of scope for a recount but the citation exists.
- **Entry self-consistency:** 29 Located-quotes strings equal the 29 admitted GATE-RECORD quotes as a multiset (verified by sorted comparison, `True`).

## Minor / incomplete-artifact note (not a kill-rule fire)

- `corpus/evidence/round97/after/` does not exist at F; claims.md:80-81 cites `after/c2-separable-base-tool.txt` as the separability receipt, but the dir is absent from the frozen tree (only `before/` + `census-start.txt` + `egress-approval.md` are committed). The result was re-derived independently above (base tool prints `rev_match=7/7`), so the *fact* holds; the *receipt path* is not verifiable at F. Same for the C1 `after/` receipts cited at the claim header. This is an evidence-persistence gap, not a falsified sentence — reported here for the wave reviewer to weigh.

## Risks / blockers

- None blocking. Network untouched; refetch not re-run (refetch.tsv read-only rows used for cross-check). No tool installs needed (grep 3.12, Python 3 present). Scratch under `/fast/scratch/hyaku/chousa-r97/R97ExecC2Repro/`, deleted after receipt copy.

VERDICT: R97ExecC2Repro C1 n/a — this seat reproduced C2 only; C1 self-test spot-checked PASS cases=47/47 but battery not run.
VERDICT: R97ExecC2Repro C2 held — all four counting commands reproduced at F with exact predicates, independent searches match 7/7 with identical Q7 digest, independent recount gives 10/26 and 14/26 with every quote on a single line, and only the cited after/ receipt paths are missing from the frozen tree.
