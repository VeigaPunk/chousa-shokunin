# R57W1ReviewC3Same — same-sentence audit of R57-C3 (predicate vs docstring vs code)

Seat: R57W1ReviewC3Same (reviewer, leaf). Item: same-sentence audit of the frozen counter
`corpus/evidence/round57/c3-count.py` against the frozen predicate in
`corpus/evidence/round57/claims.md`. No lane bytes other than this report were written; scratch
`/fast/scratch/hyaku/chousa-r57/R57W1ReviewC3Same` was deleted before yield.

## 0. Freeze integrity

- Dispatch named C3 freeze `fd95724d56a33a150cd2638fadd2ce1f3425e6c`; the real commit is
  `fd95724d56a33ad150cd263f8add2ce1f3425e6c` (`git rev-parse fd95724`, message "round-57: freeze
  R57-C3 …"). Typo in the dispatch text only; the lane commit exists and is the freeze.
- `git diff fd95724 -- corpus/evidence/round57/c3-count.py` and `... -- corpus/evidence/round57/claims.md`
  both print nothing (observed): code and claims byte-frozen since the freeze commit.
- Docstring vs claims.md: extracted the C3 predicate sentence from both and compared — identical for
  all 2129 chars (first difference is the docstring's post-predicate "Separability:" note). The
  docstring's claim "the same sentence as corpus/evidence/round57/claims.md" holds verbatim.
- Header/columns cross-check: `refetch.tsv` header is
  `id⇥url⇥key⇥attempt⇥fetched_utc⇥curl_rc⇥http_code⇥raw_sha256⇥txt_sha256` (observed), so the
  code's `c[5]=curl_rc, c[6]=http_code, c[7]=raw_sha256` are the right columns. Registry header
  (corpus/SOURCES.md:9) is `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`
  (11 cells), so `r[5]=anchor, r[7]=status, r[8]=opened, r[10]=used-by` are the right cells.

## 1. Leg-by-leg conformance (claims.md wording → code)

| # | Predicate clause | Code | Conforms |
|---|---|---|---|
| 1 | entry exists, cites S127 as `source: S127 — <first URL>`, S127 used-by names entry | L198–200 `s127_ok`; `cites` L192–193; `used_by` L195–196 | yes (with 2 tightenings, §2) |
| 2 | entry holds `规范性引用文件`, absent from corpus/knowledge at BASE_REV | L201–202 `NEW_TERM in entry` + `git grep -q … BASE_REV` rc==1 | yes |
| 3 | CLAUSE quote in an S127 spans row | L237 | yes |
| 4 | BOUND: row X ∉ {S127,S128,S129} | L208 `EXCLUDED` | yes |
| 5 | U none of theirs | L208 `EXCLUDED_URLS` — matches the three base/current first-URLs exactly (probed BASE+CUR registry, both equal the constants) | yes |
| 6 | new = `mined` + opened 2026-10-27, or held | L210 `r[7]=="mined" and r[8]==OPENED` else `rid in base_ids` | yes |
| 7 | used-by names entry; entry cites `source: X — U` | L208 `used_by(r) and cites(rid,url)` | yes (cites formatting tightened, §2) |
| 8 | capture bytes == a successful attempt's raw in refetch.tsv | L212–214 vs `good_raw` L184–188 | yes (narrowed to LAST success, §2) |
| 9 | defined form: OLE/zip raw through base capture-text.py, else .txt | `form_of` L136–148; base tool via `git show BASE_REV:tools/capture-text.py` L119–133 | yes |
| 10 | edition token (whitespace removed) in form | L228 `token in nows(form)` | yes |
| 11 | title as HEADING, prefix ≤16, no 《》.[]［］, one trailing paren dropped | `heading_title` L151–160; probes D all pass | yes |
| 12 | ≥2 manifest rows of id X, URL U, form digest; one quote holds the title | L218–221, L228–229 `MIN_PER_ID=2` | yes |
| 13 | every unbound ref has `- UNBOUND R<k> sweep: …` line | L235 regex; counted L277, L282 | yes (content min-length tightened, §2) |
| 14 | every manifest row: quote ≤25 words ≤160 chars, in span file + entry + lesson | L249–252 | yes |
| 15 | span file = exact slice at offset of the digest-recorded form, longer than quote | L253, L255–257 | yes |
| 16 | round-51 quote-substance-check exits 0 on the manifest | L260–262 | yes |
| 17 | every `char N` of a NEW bound row's anchor (≥1) is a quote offset of that id | L263–265; offsets L258–259 | yes |
| 18 | entry exits 0 under tools/inference-ground.py with this manifest | L266–271 | yes |
| 19 | no `S###` token in entry names a row other than S127 or a bound row | L272 | yes (superset, §2) |
| 20 | counted `C3=PASS`, else exit≠0 | L282–286 | yes |

## 2. Legs the code checks DIFFERENTLY than the predicate words them (all fail-closed)

1. **UNBOUND sweep content (L235).** Predicate words the line template with placeholder
   `<queries and hosts>`; code requires `^- UNBOUND R<k> sweep: \S.{10,}` — line-start, exactly one
   space after `sweep:`, and ≥11 content chars. Probed: `sweep: x` (1 char) and `sweep: 1234567890`
   (10 chars) are REJECTED; 11 chars accepted; a leading-indented line rejected. A line satisfying
   the predicate template with a short query fails the code. Unverifiable-as-worded at the margin.
2. **STRAY_IDS superset (L272).** Predicate forbids tokens that "name a row other than S127 or a
   bound row"; code flags every `\bS\d{3,}\b` token ≠ S127/bound-ids — including tokens naming NO
   registry row (probed: entry text mentioning `S999` yields `STRAY_IDS=S999`). The HELD control
   receipt shows `STRAY_IDS=S130` — S130 is a real row, consistent with the predicate; the gap is
   only non-row tokens. Stricter than worded.
3. **Capture-bound-to-last-success (L184–188, 213).** Predicate: bytes of "a successful attempt";
   code keeps the LAST successful attempt per (id,url) (`good_raw[...] = c[7]` overwrites in file
   order — probed). If a URL succeeds twice with different bodies, the code requires the capture to
   equal the later attempt; an earlier-success-matching capture fails the code while satisfying the
   predicate as worded. (C2's predicate says "last successful attempt"; C3's drops "last".)
4. **S127 uniqueness (L199).** Code requires exactly one S127 registry row (`len(s127)==1`); the
   predicate words no uniqueness. Stricter.
5. **`cites` line-anchor (L193).** `^source:` requires the citation at column 0 with exactly
   `X — U` spacing; the predicate gives the template `source: X — U` without an anchor rule. An
   indented citation satisfying the template fails the code. Stricter.

Direction check: all five divergences are tightenings/narrowings; none admits a state the frozen
predicate rejects (no false-PASS path against the kill rule "any C3=FAIL or exit != 0 = C3 not
verified"). They risk spurious FAIL only, which is loud, not silent. REPORTED, not patched (frozen).

## 3. Runtime evidence

- Current counter run (worktree, mid-wave): `ENTRY=no … BOUND=0/7 … STRAY_IDS=-  C3=FAIL` exit 1 —
  expected; the entry is not built yet this wave (L1 fetch pass in progress).
- Controls (`controls/c3-controls.txt`): HELD → `BOUND=1/7 (R7:S118) … STRAY_IDS=S130 C3=FAIL`;
  CITER → adds `S990` stray, `C3=FAIL`. Counter discriminates as documented.
- Held R7 row probe: S118 first-URL `https://www.bjhea.org.cn/…/1736907153935975.pdf`,
  `corpus/captures/16fe8487aa97b98576a0dbac.raw` sha256
  `7b600fe3ee9bda2b…` == both successful refetch attempts (attempt 1 and 2, curl_rc=0 http=200) —
  the held arm of the binding rule is satisfiable exactly as the freeze-time checks claimed.

## Residual risk / gaps

- Legs 1–20 verified by reading + targeted probes, not by an independent reimplementation; the
  five divergences in §2 are the complete set I found on the audited wording.
- `EXCLUDED_URLS` is hard-coded; if the registry's S127–S129 URLs were ever edited post-freeze the
  constant (not "theirs") would govern. At BASE and CUR they are equal, so this is inert today.
- VERDICT: attacked the R57-C3 counter's conformance to its own frozen predicate (docstring ==
  claims.md verbatim; all 20 legs implemented; 5 fail-closed tightenings reported, no false-PASS
  path) — the frozen predicate-as-coded SURVIVES.
