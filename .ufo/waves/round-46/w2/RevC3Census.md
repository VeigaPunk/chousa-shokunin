# R46-W2 — census / C3-census falsification (RevC3Census)

Seat: leaf reviewer. Target bytes: `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a` (landing) **and** the
current working tree, because they differ (F4). No fetch, no lane write except this file.
All commands run with absolute paths; decisive output verbatim.

## 1. Census, both ways — PASS, no E line, exactly five W04

    $ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
    chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
    chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
    chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
    chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
    chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
    chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
    EXIT_A=0

    $ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin \
        --file /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
    file	W04	<S051,S053,S073,S074,S075 identical> 
    file	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
    EXIT_B=0

`grep -c '\bE[0-9][0-9]\b'` on both outputs: 0. **No E-code line exists in either mode.** The two
modes agree line-for-line apart from the lane label. No W code beyond the five known W04.

Same census on the round base `6e2630a` (git archive to /tmp): identical five W04, exit 0, rows 84.
Round 46 therefore added +5 rows and **zero new E/W**.

## 2. Row count and pipe integrity — 89, no cell pipe

    $ bash scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa
    chousa	rows	89
    chousa	tier.A	83     chousa	tier.B	1     chousa	tier.C	5
    chousa	status.mined	65   chousa	status.queued	19   chousa	status.rejected	5
    (83+1+5=89; 65+19+5=89; FLEET.rows=89, FLEET.missing=0)  EXIT=0

    $ awk 'NR>=11 && /^\|/ {n=gsub(/\|/,"|"); c[n]++} END{for(k in c) print "pipes="k, "rows="c[k]}'
    pipes=12 rows=89            # 11 cells + 2 edge pipes; zero rows with any other count
    $ awk 'NR>=101 && /^ {0,3}\|/' corpus/SOURCES.md | wc -l   -> 0   (no E12 row outside Registry)
    $ grep -cE '^[[:space:]]+\|' corpus/SOURCES.md             -> 0   (no indented row)

No row cell contains a pipe (a cell pipe would give 13 pipes). Row ids are S001–S089 contiguous,
unique, no gap and no duplicate (`uniq -d` empty). `corpus/SOURCES.md` is the only registry in the lane.

## 3. C3 census rows — the five new rows are what the claim says

Independent re-derivation (awk on the Registry table, not via c3-count):

    S085 https://fever.ai/dataset/fever.html          tier A mined -> corpus/knowledge/evidence-pool-versioning-r39.md
    S086 https://aclanthology.org/N18-1074.pdf        tier A mined -> ...r39.md
    S087 https://zenodo.org/api/records/4925954       tier A mined -> ...r39.md
    S088 https://fever.ai/dataset/averitec.html       tier A mined -> ...r39-amendment-2026-10-23.md
    S089 https://arxiv.org/html/2505.17978v2          tier A mined -> ...r39-amendment-2026-10-23.md

Entry headers bind the same five ids to the same five URLs (`source:` lines 3–5 base, 3–4 amendment).
S-token census: base {S079×1, S081×1, S085×7, S086×8, S087×5}; amendment {S079×2, S081×2, S082×1,
S084×2, S088×10, S089×6} — all inside ALLOWED_IDS (S079–S089); no stray token.
Held rows bind by document: S079 source is "RFC 7089 … Memento"; S081 is "NDL … WARP URL renewal".
Cross-document numbers check: the amendment's 5,959/7,572 is exactly
`evidence-snapshot-coverage-r40.md:21` (5,959 of 7,572, 78.7%); the base entry's
"`exhaustive` occurs 0 times in the S086 capture" is true (`grep -c exhaustive` = 0, exit 1).

## 4. Spans — all eleven re-derived exactly (0 failures)

Independent of `c3-count.py`: for each `spans.tsv` row, `sha256(URL)[:24].txt` exists, its sha256
equals the recorded `capture_sha256`, `capture[offset: offset+len(span)]` **is** the committed span
file byte-for-byte, the quote sits at `capture[offset+80 : offset+80+len(quote)]`, and the quote is
present in the citing entry: `SPAN_REGRESSION fails=0/11`. Every `char N` assertion in both entries
lands on the text it names (spot-listed: S085@2593 "for internal use only and are not used for
scoring"; S086@1869 κ, @5534, @15269, @42011, @20847; S087@171, @4929 `"key": "wiki-pages.zip"`;
S088@2904, @3929, @9375 `"answer_type": "Unanswerable"`, @1142 four labels; S089@3022, @3204 κ,
@3239 74.7 %, @7137 "published before the claim's date", @14603 "archived on the internet archive").

## 5. C3 counter live on the current bytes — 11/11 and mutant-killing

    $ python3 corpus/evidence/round46/c3-count.py            -> ... CAPTURE_BOUND=11/11 C3=PASS exit=0
    $ python3 corpus/evidence/round46/c3-count.py --lane-only -> ... CAPTURE_BOUND=skipped C3=PASS exit=0
    (identical at d09fc8e via git archive; both modes on both byte sets)

Mutants on a /tmp lane copy (current entry/sources bytes), each killed:

    M1 S085 status mined->queued        exit=1 CITES_BOUND=4/5
    M2 span file quote altered           exit=1 QUOTES_IN_SPAN=10/11 CAPTURE_BOUND=10/11
    M3 forged capture digest in tsv      exit=1 CAPTURE_BOUND=10/11
    M4 all `recall of 72.36%` removed    exit=1 QUOTES_IN_ENTRY=10/11
    M5 RFC 7089 removed from both        exit=1 REF_BOUND=1/2
    M7 WARP removed from both            exit=1 REF_BOUND=1/2
    M8 twelfth span row appended         exit=1 QUOTE_ROWS=12/11
    M7b forged digest + --lane-only      exit=0 CAPTURE_BOUND=skipped  <- the declared control
The `--lane-only` pass on a forged digest is exactly the behaviour `controls/c3-controls.txt` declares;
it is not a new finding. No undocumented survivor remained.

Census mutation battery (same copy, `validate --file`): E11 (missing used-by), E01 (field count and
pipe-in-cell), E03 (dup id), E05 (bad kind), E07 (`watch`), E12 (row outside Registry) all fire with
exit 1; a cross-scope duplicate URL degrades to W04/exit 0 as designed.

## Findings

### F1 (medium, calibration) — the after-state receipt was not measured on one tree
`corpus/evidence/round46/measure-after.txt:2` says "the round-46 landing + the wave-2 corrections"
and lists counter revisions. Measured against the three real states:

| item | receipt | d09fc8e | current worktree |
|---|---|---|---|
| `c1 819287e2075c3f5b` | yes | yes | no (8473abf6c4437bed) |
| `tool 3018b1d25d762054` | yes | no (819f83ebdc6c6b47) | no (7736688bdefe9df0) |
| `c2 … ENTRY_POINTS=73 … named=71` | yes | no (72 / named 70) | yes |

`c2 60ad448e99b15cb6`, `c3 234e2272e8e21e82`, `build-spans b5c4d83bc9a32639` match all three. So the
receipt mixes a digest from the landed commit (c1), counts from the current uncommitted tree (c2), and
a tool digest that exists in **neither**. No single checkout reproduces it; the receipt's GROUND lines
do reproduce behaviourally (bullets=4 tokens=7 / 4 tokens=5 with both tool revisions), so the numbers
are not wrong — the claim of a single measured tree is. Pointer: `measure-after.txt:2-4`.

### F2 (medium, operability) — the receipt's census block is not the command's output
`measure-after.txt` records the census as producing one W04 line (S075) + `ok` + `exit=0`. The live
command produces **five** W04 lines (S051, S053, S073, S074, S075) + `ok` + `exit=0` — the same five
present at the base commit. Four warning lines are absent from a block presented as verbatim
(`$ …` / `exit=0`), so the receipt under-reports registry warnings by 4. Exit status is recorded
correctly, so no claim flips; the record is false as a transcript. Pointer: `measure-after.txt`
census block (last 3 lines).

### F3 (medium, depth/row truth) — the landed S088 row cites a quote at an offset that does not hold it
At `d09fc8e:corpus/SOURCES.md` the S088 anchor reads "the claim-date slice at char 2891: Our best
estimate for the date the claim first appeared". The capture (`b73f7e8dd5b0ace740e48046.txt`, 12,775
chars) reads `claim_date` at 2891; the quoted sentence begins at **2904** (verified:
`capture[2904:2904+52] == "Our best estimate for the date the claim first appeared"`). The current
working tree silently corrects this ("field cell at char 2891 (claim_date :) … quote at char 2904").
`c3-count` does not test row truth — its own named limit ("Row truth is not measured",
`claims.md` C2 kill rule) — so a false landed offset survived the round's after-state and was fixed
outside any commit. Every other `char N` in the five rows is exact (section 4).

### F4 (low, operability) — the lane worktree is dirty against the landing commit
`git status --short` at `d09fc8e` (HEAD): 17 modified files, incl. four production files —
`SKILL.md`, `corpus/SOURCES.md`, both knowledge entries, `tools/inference-ground.py` (plus the round-46
w1 reports). Both the census and all three counters pass on the landed bytes *and* on the current
bytes (measured above), so this is not a claim failure — but the verification target named by every
wave-1/2 receipt is not the bytes on disk, and any consumer auditing "round 46 at d09fc8e" reads a
tool without the fence-flush, title-only-registry and DESIGNATOR_RE changes now in the worktree.

## Verdict

- C1/C2/C3 counters: PASS at `d09fc8e` and at the current bytes (`c1 3/3+3/3`, `c2 72/72` at the
  commit and `73/73` now, `c3 11/11` both modes). Reproduced, not merely re-read.
- Census: `validate` clean both ways, exit 0, **no E code**, **exactly the five known W04** and no
  other W; 89 rows, 11 cells each, no cell pipe, no indented or stray row; S085–S089 mined/A with the
  five claimed URLs and citing entries; held-row cross-refs bind by document.
- No claim is falsified by the counters themselves. The defects are in the **round record** (F1, F2),
  in the **landed registry row** (F3), and in **what tree was certified** (F4).

## Residual risk / gaps

- `--lane-only` remains forge-blind (declared, reproduced); default mode is the only capture-bound leg.
- Row truth beyond the five new rows (89 rows' anchors) was not enumerated; only the five claim rows
  and their entry offsets were re-derived. The census itself never checks anchors — that is the
  structural gap that let F3 through.
- The tool digest `3018b1d2…` named by the receipt could not be located in the repo or in the
  reflog-visible commits; I did not search unreachable objects.
