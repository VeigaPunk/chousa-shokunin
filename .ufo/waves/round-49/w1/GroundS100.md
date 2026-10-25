# GroundS100 — re-ground row S100 (staged S092), ERIC EJ1372738

Seat: GroundS100 (godspeed). Round 49, wave 1. Scope: re-ground staged row S092 → lane id
S100 (renumber.tsv line 6: `S092	S100	append	eric.ed.gov/?id=EJ1372738`) by document for row
C2's entry `aggregator-vs-source-r36.md`; draft the Gate block for the row; verdict each claim
that rests on it; draft the anchor cell; check the absent-defect register. No writes outside
this report; no subagents, no background jobs, no network, no installs needed (RULES.md read;
rule: channel order never triggered — nothing installed).

## Captures opened

- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/32d1d24b24fce96d2a078ec0.txt`
  — `file`: `ASCII text, with very long lines (934), with CRLF, LF line terminators`;
  2796 bytes; utf-8 decode ok (ASCII ⇒ char offset == byte offset). Abstract = one paragraph,
  line 104.
- Same basename `.raw` — `file`: `HTML document, ASCII text, with very long lines (4453),
  with CRLF, LF line terminators`; 14258 bytes. It is **not** UTF-16LE, so the `.txt` is not
  a lossy decode of a UTF-16LE raw; the text form is the `.txt`.
- `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/aggregator-vs-source-r36.md`
  (staged entry, source line 8 = S092) and the adopt rewrite
  `chousa-shokunin/.ufo/waves/round-49/assimilation/adopt/corpus/knowledge/aggregator-vs-source-r36.md`
  (source line 8 = S100) — identical body except row id.
- `chousa-shokunin/.ufo/waves/round-49/assimilation/adopt/renumber.tsv` line 6 (map above);
  `…/adopt/append.md` line 5 (staged S100 row).

## Quote verification (command)

```python
p='/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/32d1d24b24fce96d2a078ec0.txt'
t=open(p,encoding='utf-8').read()
for name,q in [(... 3 quotes ...)]: print(name, t.count(q), t.find(q), len(q.split()), len(q))
```

Observed (form = `.txt`, python `text.find(quote)`):

| quote | count | char offset | ws words | chars |
|---|---|---|---|---|
| Q1 `leaving an unfamiliar website to search the open Web before investing attention in the site at hand` | 1 | 1235 | 17 | 99 |
| Q2 `Using a matched control design, students in treatment classrooms (n = 271) were compared to peers (n = 228) in regular classrooms.` | 1 | 1483 | 22 | 130 |
| Q3 `A multilevel linear mixed model showed that students in experimental classrooms grew significantly in their ability to judge the credibility of digital content.` | 1 | 1614 | 23 | 160 |

All ≤25 whitespace words and ≤160 characters; each byte-exact, occurs exactly once in the `.txt`.
The same sentences appear 3× in the `.raw` (meta description + body duplicates; counts 3, offsets
780 / 1028 / 1159), so the text form is the unique one and the quotes are taken from it.
`title` phrase `Lateral Reading on the Open Internet: A District-Wide Field Study in High School
Government Classes` occurs twice in `.txt` (chars 27 and 1150) — not single-use, so not offered
as a quote; it still grounds the "district-wide field study" claim (line 5 and line 99).

## Gate block draft (row S100)

- **URL:** `https://eric.ed.gov/?id=EJ1372738` (record EJ1372738 — txt line 88 `ERIC Number: EJ1372738`)
- **Access date:** 2026-10-25
- **Capture:** `.qcache/32d1d24b24fce96d2a078ec0.txt` (ASCII, 2796 bytes; `.raw` ASCII HTML)
- **Q1** (heuristic): `leaving an unfamiliar website to search the open Web before investing attention in the site at hand` — char 1235, `.txt`, unique
- **Q2** (design): `Using a matched control design, students in treatment classrooms (n = 271) were compared to peers (n = 228) in regular classrooms.` — char 1483, `.txt`, unique
- **Q3** (growth): `A multilevel linear mixed model showed that students in experimental classrooms grew significantly in their ability to judge the credibility of digital content.` — char 1614, `.txt`, unique
- **Anchor cell draft:** `abstract (line 104) — char 1235; abstract (line 104) — char 1483; abstract (line 104) — char 1614` (section name from the ERIC record body; offsets are the Q1–Q3 offsets; format follows `evidence-pool-versioning-r39.md` "(char N)" convention)

## Verdicts on claims resting on this row

Staged entry Observation bullet "Reading a source *about* the source (Western)" and append row S100:

1. Heuristic phrase — **supported** (quote Q1).
2. Matched-control design n=271 against n=228 — **supported** (Q2; "students in treatment classrooms (n = 271) … compared to peers (n = 228)").
3. Significant growth in students' ability to judge the credibility of digital content — **supported** (Q3).
4. Lateral-reading district-wide field study — **supported** (record title, txt line 5 / line 99; abstract opens `In a study conducted across an urban school district`).
5. Journal/meta: `Journal of Educational Psychology , v114 n5 p893-909 Jul 2022` (line 102), ISSN-0022-0663, EISSN-1939-2176 (lines 94-95) — **supported**.
6. "APA paywalls the full text" — **not supported by the capture** (neither confirmed nor refuted): the capture is abstract-only and additionally shows a `Direct link` to `http://dx.doi.org/10.1037/edu0000740` (line 71 raw). The row's scoping claim ("row is scoped to the statements in the abstract") is supported: no full text exists in the capture.
7. "classroom effect size was not read" (Unknown) — consistent: the abstract states significance without reporting an effect size; nothing beyond the abstract is present.

## Absent-defect register check

`grep -E 'EJ1372738|eric\.ed\.gov' /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` — **No matches**; no register row names this URL.

## Tooling / environment

No install performed (RULES.md read; nothing needed; no network). No scratch dir created; nothing to delete.

## VERDICT

Re-grounded row S100 (ERIC EJ1372738): Gate block drafted with three single-use, byte-exact quotes (char 1235 / 1483 / 1614 in the .txt capture), every capture-resting claim in the staged entry verified supported (heuristic, n=271 vs n=228 matched control, significant growth) with the paywall claim flagged as not capture-evidenced; absent-defect register checked clean.
