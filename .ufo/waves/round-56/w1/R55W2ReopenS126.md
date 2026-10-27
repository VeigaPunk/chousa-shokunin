# R55W2ReopenS126 — S126 identity/date and quotes

## Method and source

Re-opened the prescribed capture `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d663d66e2d39f868d84b1781.txt` with UTF-8, `errors='replace'`; universal newlines are already represented by that text capture. No network access. Registry row S126 is `corpus/SOURCES.md:136`; the citing entry is `corpus/knowledge/grey-literature-and-chinese-search-record-r40.md:5,17-18,24`.

## Quote/offset check

Python `str.find` and `str.count` on the whole captured form returned:

- offset 777: `Updated: 2019-07-18` — count 1; line 144 of the opened form.
- offset 1204: `NMPA organized the formulation of the Guidelines for Clinical Safety Literature Evaluation of Marketed Drugs (Interim)` — count 1; line 157.
- offset 1324: `which was issued on June 18, 2019` — count 1; line 157.
- offset 2528: `the Guidelines introduces the standardized operation process and the whole process of quality control methods of Cochrane Systematic Review` — count 1; line 160.

Each listed span is on one line and matches the lane's recorded character offset exactly. The registry row's supplied excerpts were truncated in the tool display, so this check verifies the entry's four stated anchors/quotes, not any unobserved full anchor-cell wording beyond the visible row text.

## Registry teaches cell calibration

The currently visible S126 row labels source tier `A` and says it is for identity, issuer and date as stated on the regulator's own site, not the guideline's text. The capture contains the title and date claim (lines 139, 144, 157), gives the body attribution `CCFDIE` (line 143), and footer attribution `Presented by China Daily` (line 294). Thus the page is hosted under the NMPA English-site URL and asserts NMPA organized the guideline and its issue date, but the capture itself also makes clear that page presentation/attribution is not simply an unmediated institutional authorship claim.

**Honest tier wording:** tier A is defensible only narrowly as an NMPA-domain page for the page's own posted title/date and its attribution of organization to NMPA; it is not strong independent proof of the underlying issuance because the byline is CCFDIE and page footer says “Presented by China Daily.” Prefer “NMPA-domain notice, attributed to CCFDIE (Presented by China Daily), reports the guideline identity and June 18, 2019 issue date” over “the regulator's own site states them” without qualification. No source evidence here establishes the editorial relationship or whether CCFDIE independently verified the date.

## Evidence command and observed output

Command run against the defined capture:

```text
python3 - <<'PY'
p='/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d663d66e2d39f868d84b1781.txt'
t=open(p,encoding='utf-8',errors='replace').read()
for x in [... four quoted strings ...]: print(t.find(x),t.count(x))
PY
```

Observed offsets/counts: `777 1`, `1204 1`, `1324 1`, `2528 1` (the full command used the four exact quote strings printed above). The same command printed the four offset slices and their containing lines, confirming single-line placement. Opened text form lines 143-160 and 292-294 show the attribution evidence.

VERDICT: S126's four recorded quote offsets survive; tier A for identity/date is qualifiedly defensible as an NMPA-domain notice, but the teaching cell should disclose CCFDIE and China Daily attribution and avoid implying unmediated regulator authorship.