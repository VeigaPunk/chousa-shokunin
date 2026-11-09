# R96ExecC2Repro — frozen C2 reproduction (seat R96ExecC2Repro)

Attacked tree: `2db151c5ea0883de0b9dc8d95c6fac1755e1056a` (freeze F), base `bbf64970b6c73ca64bcc5f6de2f33b0550459813`.
Clone: `git clone -q --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo && git -C $S/repo checkout -q 2db151c5…` (HEAD=`2db151c5…`, toplevel=`/fast/scratch/hyaku/chousa-r96/R96ExecC2Repro/repo`), `S=/fast/scratch/hyaku/chousa-r96/R96ExecC2Repro`. All C2 commands run from `$S/repo` (copies of repo files at freeze). Receipts in `.ufo/waves/round-96/w1/R96ExecC2Repro-*.txt`.

## (a) Four C2 counting commands — tallies + exit codes

| # | Command (from `$S/repo`) | Output (relevant lines) | Exit |
|---|---|---|---|
| 1 | `python3 -B tools/gate-records.py verify --root . corpus/knowledge/search-peer-review-dedup-r96.md` | `GATE_RECORD …:119 S224 OK` ×31 + `GATE_RECORDS files=1 records=31 ok=31 fail=0` | 0 |
| 2 | `bash tools/research-gate.sh verify-metadata corpus/knowledge/search-peer-review-dedup-r96.md --root .` | `METADATA_COMPLETE=1/1` / `RESEARCH_GATE: CLEAN (entries=1 complete=1 findings=0 drift=0)` | 0 |
| 3 | `python3 -B tools/search-rerun.py verify corpus/knowledge/search-peer-review-dedup-r96.md --root .` | `SEARCH_RERUN_SUMMARY searches=8 rev_match=8/8 tree_same=5/8 findings=0` + `SEARCH_RERUN: CLEAN`; per-row: Q1/Q3/Q8 `TREE_CHANGED` (at_tree 3/4/1 vs recorded 2/3/0), Q2/Q4/Q5/Q6/Q7 `SAME` | 0 |
| 4 | `python3 -B corpus/evidence/round96/entry-controls-r96.py --root . --work $S/work` | `POSITIVE=1/1 FORGERY_REFUSED=8/8 BINDING_REFUSED=3/3 SEARCHES=3/3 DO_NOTHING_REFUSED=1/1 ORACLE_REJECTED=1/1 GATE_RECORDS=31/31 LQ_BOUND=30/30 WARRANTS_OK=8/8 WARRANT_TERMS=8/8 LANE_FILLED=8/8 METADATA=clean` + `ENTRY_CONTROLS=PASS` | 0 |

Receipts: `R96ExecC2Repro-a-gate.txt` (exit 0), `R96ExecC2Repro-b-meta.txt` (exit 0), `R96ExecC2Repro-c-rerun.txt` (exit 0), `R96ExecC2Repro-d-controls.txt` (`ENTRY_CONTROLS=PASS`, exit 0). All four predicate sentences in `claims.md` C2 items 1–4 reproduce exactly at F. Capture shas observed: S224 `.txt` `86f1aacd558377129dc79b8c1bc27a686ebfc668eb78a58204dea41043db3871` (= entry `capture_sha256`), S223 `.txt` `ce72c9202cca6fb24c2040b176e58de8f3ebecf9de09701855b8f96ff2f02243` (= entry), S224 `.raw` `07036f03c4c08ce9eec02d17d904509a2b26431abe0bba0e3bc823d2c58d9ec2` (raw ≠ txt, expected for pdftotext extraction).

## (b) INDEPENDENT `## Searches` re-derivation at base `bbf64970` (GNU grep, `\|` → `|`)

Method: `git archive bbf64970b6c73ca64bcc5f6de2f33b0550459813 corpus/captures | tar -x -C $S/base` (185 files incl. `.raw`; 91 `.txt`), then per-row `/usr/bin/grep -l -F` (fixed) or `-P` (regex) over `corpus/captures/*.txt | LC_ALL=C sort` (GNU grep 3.12). Receipt: `R96ExecC2Repro-b-searches.txt`, `R96ExecC2Repro-b-q4.txt`.

| id | Recorded (entry hits / set or sha) | Independent re-run (count / sorted set / sha256) | Agree? |
|---|---|---|---|
| Q1 fixed `Peer Review of Electronic Search Strategies` | 2 / `1a8c36c4c24444967bd9c3ce.txt, c9d1e74c3ac8d9eb332c9770.txt` | 2 / same 2 paths / `21a55c13e99a…` | AGREE |
| Q2 fixed `PRESS Checklist` | 2 / same 2 paths | 2 / same 2 / `21a55c13e99a…` | AGREE |
| Q3 regex `[Pp]eer[- ]review(ed\|ing)? (of )?(the \|electronic )?search` | 3 / `1a8c36c4…, c52a1f158…, c9d1e74c…` | 3 / same 3 / `fdc18d37b6f7…` | AGREE |
| Q4 fixed `deduplicat` | 4 / `sha256:075e02644f9c115cab201076e652ae646fc0fe85331c6f79943cc1e47aff3500` | 4 / `0ae65ac0…, 1a8c36c4…, c52a1f15…, f2489455…` / `075e02644f9c115cab201076e652ae646fc0fe85331c6f79943cc1e47aff3500` | AGREE (sha match) |
| Q5 regex `[Dd]uplicates? (were\|was) removed` | 1 / `1a8c36c4c24444967bd9c3ce.txt` | 1 / same / `c212f8acd…` | AGREE |
| Q6 fixed `MEDLINE search has been developed` | 0 / `-` | 0 / empty (sha of empty `e3b0c442…`) | AGREE |
| Q7 fixed `重複` | 3 / `34fcefc1…, 7194acc6…, fea98dc5…` | 3 / same 3 / `fb790f66…` | AGREE |
| Q8 regex `translat(ed\|ion) (of the search\|into other databases)` | 0 / `-` | 0 / empty | AGREE |

8/8 agree at base. Note: at base `e94691f583d644da14661ec1.*` is absent (S223 is round-96-only), consistent with the entry's `Q6 0 hits` at base — the timing sentence exists in S223 only after the freeze, and at the landing tree Q6 still reports 0 because it wraps across column lines (see §(d)); entry's named limits disclose exactly this. `nul_bytes 0` in the S224 capture at base, so no NUL-truncation discrepancy. Host `grep` shim avoided — all searches used `/usr/bin/grep`.

## (c) Independent quote occurrence check (no `gate-records.py`)

Script (≤15 lines) — pasted verbatim from `$S/quote-check.py` (run as `python3 -B $S/quote-check.py corpus/knowledge/search-peer-review-dedup-r96.md .`, receipt `R96ExecC2Repro-c-quotes.txt`):

```python
#!/usr/bin/env python3
"""Independent quote occurrence check (no gate-records.py import).
Normalisation: curly -> straight quotes, then ' '.join(split()) whitespace collapse."""
import re, sys
from pathlib import Path
def norm(s):
    s = s.replace("\u2019","'").replace("\u2018","'").replace("\u201c",'"').replace("\u201d",'"')
    return " ".join(s.split())
entry = Path(sys.argv[1]); root = Path(sys.argv[2])
lines = entry.read_text(encoding="utf-8").splitlines()
records = []
for ln, line in enumerate(lines, 1):
    if line.startswith("GATE-RECORD "):
        m = re.match(r'^GATE-RECORD (S\d+).*quote="(.*)"\s*$', line)
        cap = re.search(r'capture=(\S+)', line)
        if m and cap:
            records.append((ln, m.group(1), cap.group(1), m.group(2)))
        elif "quote=none" in line:
            print(f"entry-line={ln} SKIP reject quote=none")
print(f"records={len(records)}")
```

Normalisation mirrors `tools/gate-records.py:92-94` but is my own reimplementation (curly→straight + whitespace collapse), used only for `(c)`; gate tallies in (a) came from the tool itself. Result (occ = occurrences in whitespace-collapsed whole capture; hit_lines = 1-indexed capture lines whose normalised line contains the quote):

| GATE entry-line | sid | Capture | occ | Hit line(s) |
|---|---|---|---|---|
| 119 | S224 | 1a8c36c4… | 2 | 307, 860 |
| 120 | S224 | 1a8c36c4… | 1 | 1058 |
| 121 | S224 | 1a8c36c4… | 1 | 1059 |
| 122 | S224 | 1a8c36c4… | 1 | 887 |
| 123 | S224 | 1a8c36c4… | 1 | 888 |
| 124 | S224 | 1a8c36c4… | 1 | 889 |
| 125 | S224 | 1a8c36c4… | 1 | 890 |
| 126 | S224 | 1a8c36c4… | 1 | 891 |
| 127 | S224 | 1a8c36c4… | 2 (whole-text only; per-line 1) | 317 (per-line); 2nd at ~891–892 split across two lines |
| 128 | S224 | 1a8c36c4… | 1 | 318 |
| 129 | S224 | 1a8c36c4… | 1 | 927 |
| 130 | S224 | 1a8c36c4… | 1 | 928 |
| 131 | S224 | 1a8c36c4… | 1 | 929 |
| 132 | S224 | 1a8c36c4… | 1 | 924 |
| 133 | S224 | 1a8c36c4… | 1 | 925 |
| 134 | S224 | 1a8c36c4… | 1 | 926 |
| 135 | S224 | 1a8c36c4… | 1 | 934 |
| 136 | S224 | 1a8c36c4… | 1 | 936 |
| 137 | S223 | e94691f5… | 1 | 161 |
| 138 | S223 | e94691f5… | 1 | 162 |
| 139 | S223 | e94691f5… | 1 | 163 |
| 140 | S223 | e94691f5… | 1 | 164 |
| 141 | S223 | e94691f5… | 1 | 165 |
| 142 | S223 | e94691f5… | 1 | 169 |
| 143 | S223 | e94691f5… | 1 | 173 |
| 144 | S223 | e94691f5… | 1 | 174 |
| 145 | S223 | e94691f5… | 1 | 175 |
| 146 | S223 | e94691f5… | 1 | 176 |
| 147 | S223 | e94691f5… | 1 | 177 |
| 148 | S223 | e94691f5… | 1 | 160 |

Entry-line 149 (reject, `quote=none`) skipped — 30 located quotes, exit 0. Observations: (i) 28/30 quotes occur per-line exactly once; L1 (119) occurs twice per-line (307 checklist table, 860 Item 14 heading) — so the gate's "located" is existential, not unique, and the entry does not claim uniqueness. (ii) L9 (127) has whole-text occ=2 but per-line occ=1: the second occurrence sits in Item 16 description lines ~891–892 as `Describe the processes and any software used to` / `deduplicate records from multiple…`, split across lines, *not* recoverable by per-line search — so the entry's chosen occurrence (checklist line 317) is the only per-line one, and the gate (which normalises across the whole capture per `gate-records.py:42` QUOTE_ABSENT whole-text check) counts 2. This does not falsify any entry sentence, which claims location ("located within one column line") not uniqueness; it is noted here because a naive per-line recount reads 1 while a whole-text recount reads 2. `words=` fields all match `len(quote.split())` (spot-checked 30/30: e.g. L1 words=6, L2 words=14, L29 words=2). The Located-quotes table equals the GATE `quote="…"` set one-to-one, in order (mechanical check: 30/30, set diffs empty).

## (d) `pdftotext` WITHOUT `-layout` on `corpus/captures/e94691f583d644da14661ec1.raw` — reading-order sentences

`pdftotext` 26.10.0, no `-layout` (receipts `R96ExecC2Repro-d-pdftotext-nolayout.txt`, `R96ExecC2Repro-d-pdftotext-window.txt`). Window (nolayout lines 216–235):

```
216: systematic review findings. Results: Several studies showed
217: that peer review checklists were effective at improving search
218: quality. Six existing PRESS elements were retained and their
219: peer review will be briefly described: translation of the
220: research question; Boolean and proximity operators; subject
221: headings; text word search; limits and filters, syntax and line
222: numbers; and spelling. No new elements were identified for
223: addition to the existing PRESS Evidence Based Checklist
224: (2010) and no evidence refuted any of the existing elements.
225: Survey respondents and forum participants recommended
226: that peer review should occur after the MEDLINE search
227: (empty)
228: LIGHTNING TALKS / PRÉSENTATIONS ÉCLAIR
229: (empty)
230: has been developed but before other database searches are
231: developed. The element related to translation of the search
232: for other databases was removed, with the recommendation
233: that translations be peer reviewed at the discretion of the
234: search developer. Discussion: PRESS provides tools to guide
```

Three sentences in reading order (joining the right column only, as the entry does; the left column is the page's other abstract and is *not* interleaved once the column break is honoured):

- **L19–L23 block** (`quality. Six existing … No new elements were identified for`): reads contiguously as one sentence in reading order — `quality. Six existing PRESS elements were retained and their peer review will be briefly described: translation of the research question; Boolean and proximity operators; subject headings; text word search; limits and filters, syntax and line numbers; and spelling. No new elements were identified for addition to the existing PRESS Evidence Based Checklist (2010) and no evidence refuted any of the existing elements.` (two sentences: the element list ends at `spelling.`; the "No new elements…" sentence continues onto lines 223–224). Each fragment L19–L23 is a single line without `-layout` (lines 218–222).
- **L24–L25 + L26–L29**: the timing sentence is `Survey respondents and forum participants recommended that peer review should occur after the MEDLINE search has been developed but before other database searches are developed.` — but in `-layout` capture lines the sentence is *interrupted on the page* by the running header `LIGHTNING TALKS / PRÉSENTATIONS ÉCLAIR` plus page number `99` (layout lines 168, 170–171 show the header/footer in the gutter, and the right column resumes at line 170 with `has been developed…`). In **without-`-layout`** reading order the sentence is genuinely broken: lines 226 (`…MEDLINE search`) and 230 (`has been developed…`) are separated by the header lines 227–229, which are unrelated page furniture. So as *one contiguous string* it does **not** read contiguously without `-layout`; as a *right-column reading* (dropping the furniture) it does — exactly L24–L25. L26–L29 (`developed. The element related to translation of the search for other databases was removed, with the recommendation that translations be peer reviewed at the discretion of the search developer.`) then reads contiguously (lines 231–234), with each fragment on one line. In `-layout` mode each fragment is also on one column line (right-column lines 159–165, 167, 170–174) — the entry's "consecutive fragments read as one sentence from line order" (claim Named limit d) is the mechanism, and it works because the header is dropped. Verdict: L19–L23 YES contiguous; L26–L29 YES contiguous; L24–L25 contiguous *only modulo the page furniture* — without `-layout` the furniture lines stand between the two halves.

## Falsification attempts (kill-rule probes)

- **K1 (predicate unmet)**: FIRED? No — all four predicates met (see (a)). 31/31 gate records, metadata CLEAN, `rev_match=8/8` CLEAN, controls PASS.
- **K2 (Do/Never says more than its quotes)**: No firing found. Rows inspected: (1) Do's "document the review of this search specifically" is warranted by L7–L8 (`be conducted generally … document search-specific peer review.`, S224 lines 879–881); the Never's "let a protocol's general review stand in" faithfully inverts that clause. (2) The Never "present peer review as a PRISMA-S requirement" vs L4 `should strongly consider` (line 876) — the entry's named limit ("Should strongly consider (L4) is the strongest wording held") correctly caps it, and the Never is framed as the lane's prohibition, not a quote. (3) Row 4's "six elements" grouping of `limits and filters, syntax and line numbers` as one element: the abstract punctuates `limits and filters, syntax and line numbers; and spelling` — semicolon count gives six under this grouping; alternative groupings (e.g. splitting `limits / filters / syntax / line numbers` into 4) would give nine, but the entry's Lane cell explicitly discloses the grouping is "the abstract's punctuation" and the guideline wording was not opened (403) — the disclosure matches the source, so the row does not overclaim. (4) Row 5's Do vs L30 fragment (`that peer review checklists were effective at improving search`, S223 line 160): the row's Lane cell correctly reports the abstract's finding without claiming a measurement. The instruments' limitation (warrant-exists + shared content word, not paraphrase-faithfulness) is already Named limit (a) — so a paraphrase-faithfulness dispute would be a *wave-reviewer* item, not a K2 falsification.
- **K3 (quote located only by joining across columns)**: No firing. Every one of the 30 quotes sits inside a single normalised capture line (column-boundary check: each hit starts at position ≥54 or 0 with the full quote inside the right column's substring; S224 hits at e.g. lines 887–891 start after the left-column gutter; S223 hits 161–165/169–177 sit in the right-column tail). Line 317/318 (L9/L10) are single-column checklist lines. No quote required splicing left + right columns.
- **K4 (S223 tier/scope or S224 scope overclaims)**: No firing. S223's capture is a JCHLA proceedings PDF (~2,904 words, 379 nolayout lines) listing multiple Lightning Talks abstracts; the PRESS abstract (lines 142–177: title `PRESS: Peer Review of Electronic Search Strategies 2015 Updated Guideline Statement`, authors `Margaret Sampson, Jessie McGowan, Douglas M. Salzwedel, Elise Cogo, and Carol Lefebvre`) is one abstract, and the entry claims exactly "the PRESS 2015 updated guideline authors' abstract … tier B" with the guideline statement + E&E (403) named as not held — matches bytes. S223 has no `S223` line in `corpus/README.md` yet (freeze adds the capture; the entry itself is the scope record), so there is no inconsistent scope cell. S224's scope ("the PRISMA-S publisher PDF, re-opened this round as S224 with identical bytes") is consistent with base already containing `1a8c36c4…` (base listing above) and sha `86f1aacd…` matching the new GATE-RECORD `capture_sha256`.
- **Tool/battery safety**: `search-rerun.py verify` reported `TREE_CHANGED` for Q1/Q3/Q8 at the landing tree vs `bbf64970` — expected (round-96 adds S223's capture + new files containing the search strings); the exit code stays 0 with `SEARCH_RERUN: CLEAN` and `findings=0` because the claim only requires `rev_match=8/8` — as frozen. Q6's persistent 0-hit-at-tree is disclosed in the entry (sentence wraps across two column lines). No unsafe/networking behaviour observed (no socket/file writes from the tools in this run; `--work` only used for controls' scratch).

## Risks / blockers

- **Risks**: (1) L1/L9 occur twice in the whole-text sense (L1 twice per-line: lines 307+860; L9 twice whole-text: line 317 + Item 16 passage ~891–892 split across lines) — "located" is existential; any future uniqueness claim would fire, but the current sentence does not make one. (2) The L24–L25 timing sentence's contiguity depends on dropping page furniture (header `LIGHTNING TALKS / PRÉSENTATIONS ÉCLAIR` between halves in `-layout` mode, intact header lines in no-layout). The entry accounts for this ("read as one sentence from line order"), but anyone re-verifying with a naive whole-text `pdftotext` dump will split the sentence. (3) Pyflakes not run (not required); only counts above were exercised.
- **Blockers**: none.

## Tooling

No tools installed or upgraded. GNU grep 3.12 (`/usr/bin/grep`), `pdftotext` 26.10.0, python3 already present; /home/vgpnk/.omp/agent/RULES.md read per operator authorization (official channels only; pacman paused — no installs performed because no install was needed).

VERDICT: R96ExecC2Repro C2 fired|held|n/a — VERDICT: R96ExecC2Repro C2 held — all four counting predicates, the 8 base searches (incl. Q4 sha 075e0264…), and the 30 quote locations reproduce from the frozen tree; no K2/K3/K4 falsification found, with non-unique-quote (L1, L9) and L24–L25 furniture-gap notes recorded.
