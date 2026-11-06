# R81SentinelScope — boundary and safety sentinel, round 81

Read-only. No production edit, no lane or fleet git/jj mutation, no commits, no network.
Landing attacked: `7e2da96a0541946e796384d42fea18e09ede9e9f`. Base: `378fda82dc2cbcc555a0565052cc408121813cef`.
Trees extracted with `git archive <rev> | tar -x -C /fast/scratch/hyaku/chousa-r81/R81SentinelScope`.
Receipts: `.ufo/waves/round-81/w1/R81SentinelScope/` (11 files). Scratch deleted before yield.

## Findings

| # | severity | finding |
|---|---|---|
| S1 | **MEDIUM** | Six external GETs ran at `18:44:29Z–18:44:31Z`, before round 81's approval table existed (`mtime 18:47:52Z`, commit `18:47:58Z`), and **no on-disk table's row covered them**: round-57 row 1 needs the URL already registered in `corpus/SOURCES.md` (S203–S208 unregistered at base), round-57 row 2 needs a *registered* source citing the document by name (these were located by a search), round-81's row that does cover "located by a search" was not on disk. `SKILL.md:57-59` makes such a window loopback-only. Self-disclosed, with an accurate timeline. |
| S2 | **MEDIUM** | The approval table's **seat row cannot be satisfied as written** — its method cell (`as the first row`) mandates "by the L1 only, through `tools/capture-fetch.py`", and that tool's mandatory writes are exactly the two paths the same row's *not allowed* cell forbids (`corpus/captures/<key>.raw/.txt`, `refetch.tsv`). The defect is identical in the round-57 table. Consequence: the round's 9 seat GETs have no consistent authorization in either table. |
| S3 | **LOW** | The one seat-level egress ran **9 GETs over 5 URLs** (2 per HTML URL) against the row's "a single curl GET", with `--max-time 30` and UA `'Mozilla/5.0 (X11; Linux x86_64)'` against the table's `--max-time 15` and the campaign UA. The seat's own receipt describes its UA as "campaign UA"; the recorded command used a different one. Disclosed in substance, inaccurate in that detail. |
| S4 | **LOW** | The ordering disclosure says it is "**recorded** as a `## Mistakes` row in `corpus/lessons/round-81.md`". That file is **absent at the landing revision and has never existed in any commit** (`git log --all` → 0 commits), and the round's own spec says that lesson is *Draft (do not land)*. The pointer cannot resolve. |
| S5 | **LOW** | `citation-searching-tarcis-r81.md:39` asserts in a decision-table row that "rec 5 was corrected", warranted by `S208 (rejected, unreachable) — lane inference`. The actual warrant is a web-search snippet that **no committed artifact records**, so `SKILL.md:69` (every claim carries a resolvable pointer to the artifact and revision read) is not met for that assertion. Correctly labelled inference; not a K3 firing. |

Nothing was moved, deleted or repaired. No HARD boundary clause was broken: no POST, no cookies, no credentials, no login/paywall/captcha target, no crawl, ≤1 recorded attempt per URL, and seats wrote nothing to `corpus/captures/` or `refetch.tsv`.

---

## (1) Egress

**What ran.** `corpus/evidence/round57/refetch.tsv` has exactly 6 rows dated 2026-11-06, one attempt each:
S203 200, S204 200, S205 200, S206 200, S207 200, S208 rc 22 / HTTP 403 (not stored).
Receipt `02-egress-rows.txt` → `rows_dated_2026-11-06 = 6`; every stored row reads
`key_derived_ok=True capture_present=True raw_matches_refetch=True txt_matches_refetch=True`, i.e. `sha256(url)[:24]`
is the capture key and each capture's bytes hash to its refetch row. So the table's "record" column is honest.

**GET only, public, no credentials.** `tools/capture-fetch.py:137-138` is
`["curl","-fsSL","--compressed","--max-time","15","-A",UA,"-o",out,"-w","%{http_code}",url]` — no `-d`/`--data`,
no `-X`, no `-b`/`-c`, no `-u`/`--user`, no `Authorization`, no `--upload`. Receipt `01-egress-argv.txt` →
`UPLOAD_OR_AUTH_FLAG=ABSENT (GET only)`. `tools/quote-reopen.py:397` is `conn.request("GET", target, headers=...)`;
its docstring (`:25`) states "no userinfo, no cookies".

**Ordering disclosure — timing is accurate.** Fetches `2026-11-06T18:44:29Z`–`18:44:31Z`; table file mtime
`2026-11-06T15:47:52.195914854-03:00` (= 18:47:52Z); table commit `f7929f877e6fd54f4dc5ce7f993da46bc7df43f9`
= `2026-11-06T15:47:58-03:00` (= 18:47:58Z). Receipt `03-ordering.txt` → `mtime - last_fetch = 0:03:21.195914`,
`commit - last_fetch = 0:03:27`. The disclosure's claim that the fetches "ran … before this file was written" is
therefore **true**, and the table was not on disk first, as it says.

**But the disclosure's pointer is dangling (S4).** Same receipt: `git cat-file -e <landing>:corpus/lessons/round-81.md`
→ `ABSENT at landing`; `git log --all -- <path>` → `commits_touching_that_path=0`; the only in-tree references are
`egress-approval.md:14` and `.ufo/waves/round-81/build_spec.py:117`, the latter reading
*"Draft (do not land) `corpus/lessons/round-81.md` sections…"*. A closure reader following the pointer finds nothing,
and the round is instructed not to land it.

**The authorization chain does not close (S1).** Receipt `11-table-contradiction.txt`. At fetch time the only
approval table on disk was round 57's, and it is window-scoped in its own words — *"This is the table for round 57's
window."* Its row 1 requires "a URL already registered in `corpus/SOURCES.md` and pinned by a committed spans
manifest"; all six ids are `NOT registered` at base `378fda82`. Its row 2 requires "a public document **a registered
source cites by name**"; S203–S207 were located by a search. Round 81's table covers exactly that scope
("open of a public research-method document … located by a search") but its mtime is 3m21s *after* the last fetch.
So the six GETs happened inside a window that had no on-disk authorization for them, which `SKILL.md:57-59`
("A window without an approval table is loopback-only") forbids. The round discloses this; the severity is bounded by
what the fetches actually did (public, GET, credential-free, single attempt, bytes committed and matching).

**Seat row is self-contradictory (S2).** Receipts `09-seat-egress.txt`, `10-seat-flags.txt`, `11-table-contradiction.txt`.
Round-81 `egress-approval.md:22` (and round-57 `:17`, identically):
allowed = "`tools/quote-reopen.py verify` or a single curl GET"; method = "as the first row";
not allowed = "writing `corpus/captures/` or `refetch.tsv`".
"As the first row" (`:20`) is "one `curl -fsSL --compressed --max-time 15 -A <campaign UA>` GET per attempt,
**by the L1 only, through `tools/capture-fetch.py`**". `capture-fetch.py:124` appends to `refetch.tsv` and `:128-129`
write `corpus/captures/<key>.raw/.txt`. The method cell therefore mandates the L1-only tool whose mandatory writes are
the paths the same row forbids, while the allowed cell authorises a seat. The two cells cannot both hold.

**What the round's one seat-level egress actually did (S3).** `.ufo/waves/round-81/w1/R81ExecReopen.md:100-104`
discloses "each of the four HTML URLs received **two** GETs (one by the tool, one by curl), and S203 received one …
Total: 5 URLs, 9 GETs". The recorded command (`reopen-s203.txt:2`, `sha-compare.txt:2`) is
`curl -fsSL --compressed --max-time 30 -A 'Mozilla/5.0 (X11; Linux x86_64)' -o …`. The campaign UA
(`capture-fetch.py:65-66`) is the longer `… AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36`.
So: 2× the stated per-URL budget, `--max-time 30` not 15, and a UA that is not the campaign UA — while the receipt's
prose calls it "campaign UA". All URLs used (S203–S207) are in this round's rows, and
`git status --porcelain -- corpus/captures/ corpus/evidence/round57/refetch.tsv corpus/SOURCES.md` → 0 lines
(`09-seat-egress.txt`), so the seat kept its bytes in scratch as required.

**Authority citation is honest.** `egress-approval.md:8-13` cites `/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-81.md`
§2b. That file exists (111366 bytes) and contains the quoted language at `:50-51` ("written only after its source is
opened this round; the lesson's `## Gate` records the URL, access date, and a ≤25-word located quote") and `:146`
("each round must leave the lane measurably more capable — a trial run end-to-end on real domain work, a curated
`corpus/SOURCES.md` delta, and a mistake mined into a lesson").

**Residual limit.** Extra egress invisible to `refetch.tsv` (e.g. an unrecorded `quote-reopen.py` run) cannot be
excluded from committed bytes. The table's line "Every other external target stays loopback-only" is an assertion,
not a measurement.

## (2) Province — no sibling province absorbed

`PROVINCE.md:5-8` owns "*question framing; source hierarchy …; **citation chaining and hop resolution**;
**claim-vs-source verification**; search-strategy taxonomy; the external-target approval table for a research
window; this lane's own corpus and gates.*"
`PROVINCE.md:10-15` refuses "*bounty-program scope and claim packages (→ kasegi); model-quality or evaluation claims
(→ kengaku); orchestration, multi-agent dispatch and agent lifecycle (→ kumitate …); external live-target research
without operator approval (loopback-only otherwise); secret values in any record (→ kagi for custody; shape-only
here).*"

Receipt `04-province.txt`. Sibling-keyword scan over both entries
(`model quality|evaluation claim|benchmark|bounty|exploit|vulnerab|payload|orchestrat|multi-agent|dispatch|subagent|agent lifecycle|secret|credential|token|password|api[_-]?key|custody|kagi|kengaku|kasegi|kumitate`)
→ `sibling_keyword_hits = 0` for **both** entries. Neither entry contains a bare URL.

By substance:

- `citation-searching-tarcis-r81.md:10` — "*That is **chain verification**. Citation *searching* is a different act:
  using citation links to *find* more evidence for a question.*" This is squarely the lane's owned
  "citation chaining and hop resolution" / "search-strategy taxonomy". Its decision-table rows govern a review team's
  search design; no row makes a model-quality or evaluation claim, none packages a bounty claim, none describes
  dispatch or agent lifecycle, none holds a secret. kengaku / kasegi / kumitate / kagi: **not entered**.
- `correction-retraction-status-r81.md:9` — "*The lane's claim check runs claim → source → the source's own evidence.*"
  That is the owned "claim-vs-source verification" surface, extended with a publication-status check. Its final section
  is explicitly separated (`:46` "## Inference (lane's, not stated by the sources)"), so observation/inference
  separation is respected. No sibling province entered.
- The entries cite no live *system* target, so the "external live-target research" refusal is not engaged beyond the
  already-handled egress item.

**Province verdict: held.** No absorption, no borrowing of a sibling's authority.

## (3) Secrets — no credential shapes

Receipts `05-secrets.txt`, `05b-email-classes.txt`. Scope: added lines of
`git diff 378fda82… 7e2da96…` (16627 added lines) plus the five new 2026-11-06 captures in both `.raw` and `.txt`
form; 14 classes (AWS key id, GitHub/Slack/Google/OpenAI token, JWT, private-key block, `Authorization:` value,
`Bearer`, cookie header, URL userinfo, password assignment, api-key/secret-key assignment, email).

```
### A. committed diff 378fda82..7e2da96 — added lines only
  added_lines=16627
  diff: email count=12 lines=[142, 3321, 7738, 12163, 12202, 12244, 12248, 12249, 12252, 12253]
### B/C. five captures — .txt and .raw
  f2489455…txt: email 10 · c52a1f15…txt: email 1 · 371c5511…/f221c90f…/43a45b49…: NO MATCH
  f2489455…raw: email 3 · c52a1f15…raw: email 1 · 371c5511…raw: email 1 · other two: NO MATCH
CREDENTIAL_SHAPED_HITS_TOTAL=0
VERDICT_CLASS=NONE
```

Every non-`NO MATCH` hit is the email class; **no token, key, cookie, JWT, private key, Authorization header or
userinfo URL appears in any file**. The 12 diff hits localise to five capture files only (`05b-email-classes.txt`), and
the masked context shows they are the fetched documents' own front matter — ORCID-adjacent author lines
(`Julian Hirt: 0000-…`, `Thomas Nordhausen: 0000-…`, `Hannah Ewald: 0000-…`, `Christian Appenzeller-Herzog: 0000-…`),
a publisher contact block (`Basel, Switzerland, <local>@<masked>, Phone: +41 …`), a CC-BY withdrawal-notice address,
a corresponding-author `Email:` line, and NLM's page meta `<meta name="NLM.Contact.Email" …>`. Those are author or
publisher contacts inside public documents, not lane-authored records and not credentials — inside the item's
"emails beyond author names" allowance.
The 3 `f2489455…raw` email hits are **binary false positives**: the masked context is PDF stream noise
(`····'6···F··0`, `{··C1d`, `&i^······3·:·`), not addresses. No value is printed anywhere in these receipts.

**Secret clause (`PROVINCE.md:14-15`, `SKILL.md:65`): held.**

## (4) Misroot — none

Receipt `06-misroot.txt`. `git -C /home/vgpnk/Projects/shokunin status --porcelain -uall` → `porcelain_line_count=3`:

- `?? versions.html` (2466 bytes) — grep `chousa|round[ -]?81|r81` → `r81_name_matches=0`
- `?? w4lines.txt` (119 bytes) — content is a bare integer list (65, 162, 259, …) → `r81_name_matches=0`
- ` M .scratch/run15-state.json` — **modified tracked** file, not untracked; matches r81 4×; host-owned, untouched.

So **no untracked fleet-root file names chousa round 81.** Nothing moved or deleted.

## (5) Scratch hygiene

Receipt `07-scratch.txt`, observed before this seat's cleanup:

- `/fast/scratch/hyaku/chousa-r81` → **11G**, 13 entries: `R81MutationCounters 12G`, `R81CriticClaims 2.4G`,
  `R81ExecRepro 1.1G`, `R81ScoutNovelty 682M`, `R81SentinelScope 682M`, `R81ExecTrial`/`R81ReviewerC2`/
  `R81ReviewerEntries`/`R81ScribeLesson` 342M each, `R81ScribeR80Defects`/`R81ConnectorSiblings`/`l1` 0–8K.
  These belong to seats still running — not this seat's to delete.
- `/tmp` matches `r81` → **33 entries** (`r81c2_*`, `r81-tree.json`, `r81fetch`, `r81verify`, `r88m-r81c*`,
  `*-r81-closure*.json`, `r81-c1-we9432y0`, …). `/tmp` totals 59G. `/tmp` is never citable evidence and is not mine;
  reported, not removed.
- This seat's own dirs (`R81SentinelScope`, `base-R81SentinelScope`) were deleted before yield. Post-delete state:
  receipt `07b-scratch-after.txt` → `R81SentinelScope ABSENT (removed)` / `base-R81SentinelScope ABSENT (removed)`.

## Counters — context for the verdict lines

Receipt `08-counters.txt`, run against a `git archive` of the landing revision:

```
ENTRY citation-searching-tarcis-r81.md counted=yes reason=all-pass
ENTRY correction-retraction-status-r81.md counted=yes reason=all-pass
DEPTH_R81 entries=2 fresh_rows=5 located_quotes=14
DEPTH_R81=PASS
C1_EXIT=0
CHECKLIST_RUN=6/6 DISCRIMINATE=3/3
CHECKLIST=PASS
C2_EXIT=0
```

Instrument pins match `claims.md` exactly:
`depth-r81.py 10c989c0…`, `checklist-run.py 66ca8c97…`, `run-controls.sh c1942bb9…`.
Neither C1-K1 nor C2-K1 fires on this seat's read.

## Routed to the reviewer / closure (observed, not findings on my surface)

- `correction-retraction-status-r81.md:35` decision table has columns `Observation | Reading | Do | Never` — **no
  Warrant column**, unlike entry 1's `:31` `Situation | Do | Never | Warrant`. A reader cannot trace rows 2–5 to a
  source except through the inline quotes above the table. Form issue only; the frozen predicate does not require it.
- `citation-searching-tarcis-r81.md` "Writing the methods" row (recommendation 10) is warranted by the located quote
  "the directionality of searching (backward, forward, co-cited, co-citing)," which evidences only the
  *directionality* item of that row's five claimed items (seeds, directionality, dates, iterations, indexes/tools).
  Under-evidenced, not contradicted — **not** a K3 firing; the reviewer should decide if the quote suffices.
- S5 above is the one row where a decision-table cell states a fact from an unrecorded snippet; the entry does label
  it "lane inference" and refuses to cite recommendation-5 wording, which is the right containment.

## Limits

Read-only and no network: no live re-open was attempted by this seat, so K2 (C1) and C2-K2 are untouched here.
Extra egress not written to `refetch.tsv` is not detectable from committed bytes. The approval-table analysis judges
the table *text* against the tools' argv and write targets; it does not infer operator intent.

VERDICT: R81SentinelScope C1 held — the frozen counter prints `DEPTH_R81=PASS` rc 0 with instrument sha256 matching the pins, neither new entry enters a sibling province, and no decision-table row in the two entries contradicts a located quote; C1-K2 remains R81ExecReopen's surface.
VERDICT: R81SentinelScope C2 held — the frozen counter prints `CHECKLIST_RUN=6/6 DISCRIMINATE=3/3` / `CHECKLIST=PASS` rc 0; C2's K2 forger surface was not tested by this seat.
VERDICT: R81SentinelScope egress fired — six public GETs ran in a window with no on-disk approval table covering them and the round's 9 seat GETs exceed a self-contradictory seat row, both disclosed with an accurate timeline but recorded nowhere that exists.
