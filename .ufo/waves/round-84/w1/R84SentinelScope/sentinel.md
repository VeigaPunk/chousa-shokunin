# R84SentinelScope — boundary and safety sentinel, chousa round 84

Read-only seat. No production edits, no lane/fleet git or jj mutation, no commits or pushes, no network
fetch (my wave item names no re-open URL, so no `refetch.tsv` row with a 2026-11-08T02:1x–02:2xZ timestamp
is mine to claim), no subagent dispatch. Every byte I wrote is under this seat folder plus my scratch.

Scope: egress ordering and scope, province absorption, secret shapes, fleet-root misroot, scratch hygiene.

**Axes named:** (1) egress ordering vs. approval table; (2) egress scope — were the fetches the table
authorised; (3) freeze integrity — is the landed predicate set the frozen one; (4) capture/ledger
provenance — do committed captures back the records that cite them; (5) province absorption; (6) secret
shapes; (7) misroot; (8) scratch hygiene.

Revisions used: base `408ae68f9e445fc911f713d5bbb3a64dda1ab9fe`, freeze `3b616420b2dcc1f8a24a1cb9db4198c7adc8929b`,
landing `03bbb4580b39b442be69f998fae2db48d64b8c93`. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin
rev-parse --show-toplevel` = `/home/vgpnk/Projects/shokunin/chousa-shokunin` (lane is its own git toplevel;
the fleet root is a different toplevel). All `git archive` trees extracted under scratch.

---

## Finding 1 — HIGH: the frozen predicate set was amended after the freeze, before scoring

**Claim under attack.** `corpus/evidence/round84/claims.md` is declared frozen in the round's own framing
and pinned by `instrument-pins.txt`. It is not the same file at the freeze and at the landing.

**Evidence (exact commands and observed lines).**

```
$ git -C …/chousa-shokunin log --format='%h %cI %s' 3b616420..03bbb458 -- corpus/evidence/round84/claims.md
3a17f4da 2026-11-07T23:22:58-03:00 round-84: fetch S214/S018/S023, land search-transparency entry, fix controls
```

`3a17f4da` is the very commit that performed the fetches. It rewrote `claims.md` **and** every control
receipt, the control summary, the salad control fixture, `base-knowledge.txt`, and `run-controls-r84.sh`:

```
$ git -C …/chousa-shokunin diff --name-status 3b616420 03bbb458 -- corpus/evidence/round84/
M  corpus/evidence/round84/base-knowledge.txt
M  corpus/evidence/round84/claims.md
M  corpus/evidence/round84/controls/receipts/c1-b1-salad-boundary.txt
M  corpus/evidence/round84/controls/receipts/c1-d0-donothing.txt
M  corpus/evidence/round84/controls/receipts/c1-d1-r81-filler.txt
M  corpus/evidence/round84/controls/receipts/c1-d3-r82-entry-relanded.txt
M  corpus/evidence/round84/controls/receipts/c2-f1-stub-accept.txt
M  corpus/evidence/round84/controls/receipts/c2-f2-stub-refuse.txt
M  corpus/evidence/round84/controls/receipts/c2-f3-stub-quote-only.txt
M  corpus/evidence/round84/controls/receipts/c2-f4-stub-whitelist.txt
M  corpus/evidence/round84/controls/receipts/c2-k0-donothing.txt
M  corpus/evidence/round84/controls/receipts/summary.tsv
M  corpus/evidence/round84/run-controls-r84.sh
```

Hashes, measured:

```
$ git show 3b616420:corpus/evidence/round84/claims.md | sha256sum
f6f032a6f1d40292263acb13c732942fbd078cf9276799bf5081dbb44088353e
$ sha256sum corpus/evidence/round84/claims.md        # landing
19d68274b82d3f901d17fe217625b1e0de1f9eacbbf5c4d869b25a4fb65c442e
```

**Exploit path.** The predicates that decide the round were edited in the same commit that opened the
sources, so the landed claim is not the claim that was frozen:

- freeze-time text: `**Sourced claim:** C2 rests on S017, opened this round.` — landing text:
  `**Sourced claim:** C2 rests on S214, S018, S023, opened this round.`
- freeze-time: `The counter builds six fresh positives` — landing: `builds five fresh positives`.
- freeze-time predicate: `FRESH_POSITIVE=6/6 … RC=3/3` — landing: `FRESH_POSITIVE=5/5 … RC=4/4`.
- freeze-time kill rule K4: `a base-list entry cites S017` — landing: `cites S214, S018, or S023`.
- freeze-time control: `c2-k0-donothing (tool absent → FAIL)` — landing:
  `(pre-repair tool 81b81173 → FAIL, EXPECTED_CODE 262/288)`.

The control semantics moved too, and the receipts were rewritten to match. At the freeze every control
receipt was an *error*, not a result:

```
$ git show 3b616420:…/receipts/c2-k0-donothing.txt
python3: can't open file '/fast/scratch/hyaku/chousa-r84/controls/c2-k0/corpus/evidence/round84/gate-records-r84.py': [Errno 2] No such file or directory
rc=2
$ git show 3b616420:…/receipts/summary.tsv
c1-d0-donothing	FAIL	ERROR
…
c2-f4-stub-whitelist	FAIL	ERROR
```

At the landing the same file reads `FAIL FAIL` / `PASS PASS` — the second column is the verdict, the third
was `ERROR` at freeze. The frozen claims assert "Controls (executed, committed)" with receipts; at the
freeze commit those receipts recorded that the controls never ran. The controls were then executed and the
receipts rewritten, in the same commit as the fetch.

Note the direction of travel: the freeze-era `c2-k0` control was *specified* as "tool absent → FAIL" and
*executed* as a missing-file error; at landing it is *specified* as "pre-repair tool → FAIL" and executed
as a real run with `EXPECTED_CODE=262/288`. The spec was moved to match what the tool could produce.

**What was not touched** (so the freeze is not entirely fictitious): the counters themselves are
byte-identical freeze→landing —

```
$ for f in gate-records-r84.py depth-r84.py; do
    a=$(git show 3b616420:corpus/evidence/round84/$f | sha256sum | cut -c1-16)
    b=$(git show 03bbb458:corpus/evidence/round84/$f | sha256sum | cut -c1-16); echo "$f freeze=$a landing=$b"; done
gate-records-r84.py freeze=3777249c1c9da1b3 landing=3777249c1c9da1b3
depth-r84.py freeze=0b9caf795bb6fa91 landing=0b9caf795bb6fa91
```

— as are `c2-positives.tsv` and the four stub tools. `instrument-pins.txt` did not exist at the freeze
(`git cat-file -t 3b616420:…/instrument-pins.txt` → `fatal: path … does not exist`); it was added at the
landing and pins the **post-amendment** `claims.md` hash, so the pin attests the amended file and can
never expose the amendment:

```
$ grep claims.md corpus/evidence/round84/instrument-pins.txt
19d68274b82d3f901d17fe217625b1e0de1f9eacbbf5c4d869b25a4fb65c442e  corpus/evidence/round84/claims.md
```

**Impact.** The frozen predicate set is the instrument that makes the round's verdict meaningful. Editing
it in the fetch commit means "K1 not met", "FRESH_POSITIVE=5/5" and "K4 cites S214/S018/S023" are
properties of a document written *after* the answer was known. A later reader who diffs freeze→landing sees
a rewritten rulebook, not a measurement.

**Smallest remediation.** Do not amend `claims.md` or its receipts after the freeze commit; if a source must
change, land the amendment as a *new* freeze commit with a new freeze hash, and keep the superseded
predicate set as a committed file so the old predicates stay auditable. Pin `claims.md` in the same commit
that freezes it, not at landing.

---

## Finding 2 — HIGH: nine of the ten fetched URLs are not in the approval table's intended-targets list

**Evidence.**

```
$ git -C …/chousa-shokunin log -1 --format=%cI 3b616420
2026-11-07T23:11:05-03:00            # = 2026-11-08T02:11:05Z
```

The egress table `corpus/evidence/round84/egress-approval.md` has exactly **one** intended-target row:

```
| intended id | URL | purpose |
| S017 (re-open) | https://www.prisma-statement.org/prisma-2020 | PRISMA 2020 reporting standard … |
```

Parsing that table programmatically gives one row, one URL. The refetch ledger for 2026-11-08 has ten
distinct URLs (`receipts/e1-url-vs-table.txt`):

```
MISSING_FROM_TABLE: https://aclanthology.org/2026.acl-long.1430/
MISSING_FROM_TABLE: https://pubmed.ncbi.nlm.nih.gov/17638714/
MISSING_FROM_TABLE: https://pubmed.ncbi.nlm.nih.gov/28912002/
MISSING_FROM_TABLE: https://www.cochrane.org/…/chapter-iv
MISSING_FROM_TABLE: https://www.cochrane.org/news/living-systematic-reviews-continuous-evidence
MISSING_FROM_TABLE: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
MISSING_FROM_TABLE: https://www.prisma-statement.org/prisma-2020-checklist
MISSING_FROM_TABLE: https://www.prisma-statement.org/s/PRISMA_2020_checklist-ab3g.pdf
MISSING_FROM_TABLE: https://www.w3.org/TR/2013/REC-prov-o-20130430/
```

Only `https://www.prisma-statement.org/prisma-2020` (the S017 re-open) is in the table. The three sources
the scored C2 entry rests on — S214 (the PDF), S018 (ACL), S023 (DCMI) — are **not** in it, and neither were
they named at the freeze:

```
$ git show 3b616420:corpus/evidence/round84/claims.md | grep -n "S214\|S018\|S023"
(no output — the freeze-time claims named only S017)
```

**The ordering rule itself holds.** The egress table was committed before every fetch:

```
$ python3 … (receipts/e1-commit-utc.txt)
egress_commit_utc= 2026-11-08T02:11:05Z
rows_2026_11_08= 14
S017 2026-11-08T02:13:58Z AFTER_COMMIT=True delta_s=173 …
S214 2026-11-08T02:21:13Z AFTER_COMMIT=True delta_s=608 …
```

All 14 rows are after the commit, 173 s to 608 s later. No fetch predates the table. So the *timing*
discipline of round-81/82/83 held; the *scope* discipline did not.

**Exploit path.** The scope row of the table authorises "open of a public research-method document (PRISMA
2020 statement page) located by search", with "crawling links" listed as not-allowed and one row per attempt
in `refetch.tsv`. But the table's *enumerated* target list — the machine-checkable part — carries one URL.
Nothing in the table names ACL Anthology, DCMI, Cochrane, PubMed or W3C, so the fetch that supplied the
scored entry's other two sources has no approval-table entry to point at. The lesson asserts the opposite:

```
$ sed -n '13,15p' corpus/lessons/round-84.md
…and every URL appears in `corpus/evidence/round84/egress-approval.md`'s intended-target
table, committed before the first fetch.
```

That sentence is false as written: nine of the ten URLs do not appear in the intended-target table.

**Related: link-following.** The table forbids "crawling links". The three PRISMA fetches are 37 s apart and
form a link chain — the landing page links to the checklist page, the checklist page links to the PDF:

```
$ python3 … (receipts/e1-link-chain.txt)
capture 259c96bf7088a12bc7ce65c4: prisma hrefs include '/prisma-2020-checklist'
capture 1f5f4eec0b85edf1dc53db7b: prisma hrefs include '/s/PRISMA_2020_checklist-ab3g.pdf'
S017 02:13:58 prisma-2020
S017 02:14:24 prisma-2020-checklist
S017 02:14:35 s/PRISMA_2020_checklist-ab3g.pdf
```

The lesson records one search query ("PRISMA 2020 checklist pdf prisma-statement.org") but the fetch order
matches the link chain exactly, and the lesson itself says "the checklist page linked to the PDF". A
search-located PDF and a link-followed PDF are indistinguishable in the ledger; the recorded evidence
supports the link-following reading at least as well as the search reading.

**Impact.** The approval table exists so a reader can check every fetch against a pre-committed list. Nine
of ten fetches cannot be checked that way, and the lesson's claim that they can is the sentence a reviewer
would rely on.

**Smallest remediation.** Extend the intended-targets table (in a commit before the fetch) to every URL that
will be fetched, including the PDF, ACL and DCMI; and record the locating query per URL rather than one
query for the chain. If a fetch is link-followed, say so in the table instead of calling it a search.

---

## Finding 3 — HIGH: an HTTP 203 cookie-challenge page is certified as a quotable, admitted source

**Exploit path.** `tools/capture-fetch.py` treats any 2xx as a success and stores the body as a capture:

```
$ grep -n "200 <= code <= 299" tools/capture-fetch.py
152:        if 200 <= code <= 299:
```

HTTP **203** (Non-Authoritative Information) is in that range. The PubMed fetches returned exactly 203 with a
cookie wall, and those bodies were stored as captures and committed:

```
$ grep -P "^S022\t" corpus/evidence/round57/refetch.tsv
S022 https://pubmed.ncbi.nlm.nih.gov/28912002/ ff9013bd… 1 2026-11-08T02:16:21Z 0 203 e6b74dc4… 7070b59c…
$ cat corpus/captures/ff9013bd7d9387e45cd6e000.txt
Cookies must be enabled
Enable cookies for pubmed.ncbi.nlm.nih.gov and reload this page to continue.
```

The verifier's `REFETCH` check accepts the same class — `2[0-9][0-9]` — so a `GATE-RECORD` that *admits*
that capture as a quoted source prints `OK`. Demonstrated end-to-end through the public CLI at the landing
revision (`receipts/e7-203-admit-ok.txt`):

```
forged record:
GATE-RECORD S022 url=https://pubmed.ncbi.nlm.nih.gov/28912002/ fetched=2026-11-08T02:16:21Z tier=A
  decision=admit capture=corpus/captures/ff9013bd7d9387e45cd6e000.txt capture_sha256=7070b59c3434b677
  words=4 quote="Cookies must be enabled"

$ python3 $D/tools/gate-records.py verify --root $D --repo …/chousa-shokunin $D/forged.txt
GATE_RECORD …/forged.txt:1 S022 OK
GATE_RECORDS files=1 records=1 ok=1 fail=0
exit=0
```

A cookie wall is now certified as an admitted tier-A source with a located quote. The lesson itself
describes these pages correctly ("S021/S022/S032 PubMed (HTTP 203 cookie-challenge pages, no content)") —
but the tool's own contract, which is what other tooling trusts, says they are quotable sources.

**Impact.** `gate-records.py` is the lane's public verifier: it is what a later round trusts to decide that a
quoted claim is backed by a fetched source. A 203 interstitial passes every check the tool makes, so the
verifier's `OK` no longer implies "a real document was retrieved". The failure is silent — an interstitial
page produces a well-formed, quotable, `OK`-certified record.

This is a boundary defect in the shared tool, not a claim-scoring verdict: the round's three scored records
(S214, S018, S023) cite genuine 200 responses and are not affected. The 203 rows are not gated as records
this round.

**Smallest remediation.** In `tools/capture-fetch.py`, treat only `200` as a retrievable body (store 203 with
its status but do not admit it as a capture), and narrow the verifier's `REFETCH` success test from
`2[0-9][0-9]` to `200` for the admit form. A one-line change on each side closes it.

---

## Finding 4 — MEDIUM: the setup leg misreports — `FAIL LINE,REV` exit 1, not `GATE_RECORDS_ERROR` exit 2

The frozen C1 kill rule K2 states the setup leg explicitly: "a rev record checked with a non-git `--repo`
(a scratch directory with no git history) must exit 2 with `GATE_RECORDS_ERROR` on stderr — not `FAIL REV,LINE`
with exit 1 — at the landing revision", and "The setup leg (non-git `--repo` exit 2 vs `FAIL REV,LINE` exit 1)
counts as K2 if the tool misreports it."

Measured independently at the landing revision through the public CLI (`receipts/e6-setup-leg.txt`):

```
A) --repo = non-git scratch dir:
$ python3 $D/tools/gate-records.py verify --root $D --repo /fast/…/tmp.WddbUJf293 $D/revrec.txt
GATE_RECORD …/revrec.txt:1 S199 FAIL LINE,REV
GATE_RECORDS files=1 records=1 ok=0 fail=1
exit=1  <-- frozen K2 requires GATE_RECORDS_ERROR on stderr and exit 2

B) control: identical record, --repo = real lane checkout:
GATE_RECORD …/revrec.txt:1 S199 OK
GATE_RECORDS files=1 records=1 ok=1 fail=0
exit=0  <-- the record is genuine; only the --repo leg differs
```

The record is genuine (it passes against the real lane), so the `FAIL LINE,REV` is a misreport of a setup
error, exactly the case K2 names. The tool's own `main()` has the exit-2 path
(`GATE_RECORDS_ERROR missing …` for a missing registry/refetch/file) but never validates that `--repo` is a
git repository; `git_blob()` swallows the failure and returns `None`, which `check()` turns into `REV`+`LINE`.

The frozen counter does not cover this leg — it prints `SETUP=unscored` — so the counter's `PASS` cannot
contradict it. Counter at the landing revision (`receipts/e8-counter-at-landing.txt`):

```
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=288/288 EXPECTED_CODE=288/288 EMPTY_REFUSED=1/1 RC=4/4 SETUP=unscored
GATE_RECORDS_R84=PASS
exit=0
```

**Impact.** K2 is an in-class kill and it fires on this leg at the landing revision. The commit `c7d29e1c`
repair is in the base (I verified `git merge-base --is-ancestor c7d29e1c 408ae68` → true), so this is not a
pre-repair artefact.

**Smallest remediation.** In `tools/gate-records.py` `main()`, validate `--repo` with
`git -C <repo> rev-parse --git-dir` and, on failure, print `GATE_RECORDS_ERROR` to stderr and return 2 —
the same shape the tool already uses for a missing file.

---

## Finding 5 — MEDIUM: one ledger row's recorded capture bytes do not exist in the capture store

**Evidence** (`receipts/e5-ledger-orphan.txt`):

```
id=S021 attempt=1 raw_sha=f88609906ec38d64 txt_sha=7070b59c3434b677
id=S032 attempt=1 raw_sha=3f3135502abe5b88 txt_sha=7070b59c3434b677
stored 58725f5e0ac436166546a5ec.raw sha256=3f3135502abe5b88
any file in corpus/captures with S021 raw sha: False
```

S021 and S032 are two ids for the same URL (`https://pubmed.ncbi.nlm.nih.gov/17638714/`), so they share the
content-addressed key `58725f5e0ac436166546a5ec`. The second fetch overwrote the first's `.raw` bytes. The
ledger's S021 row still records `raw_sha256=f88609906ec3…`, and **no file in `corpus/captures/` has that
hash** — the only committed reference to it is the ledger row itself.

**Exploit path.** `capture-fetch.py` stores by key = sha256(url)[:24], so a second fetch of the same URL
replaces the first's bytes. Any verifier or auditor that re-derives "do the committed bytes match what the
row claims" for S021 gets a false negative, and the lane cannot prove which body was seen on the first
attempt. The two ids are also indistinguishable in the store: only the ledger distinguishes them, and the
ledger is the thing that lost its referent.

**Impact.** S021 is not used by any scored record and no committed file cites `f88609906ec3…` except the
ledger row, so no claim's verdict turns on it. It is a provenance hole in the round's own evidence store: the
store is keyed by URL, not by content, so concurrent or repeated fetches of one URL silently drop earlier
bodies.

**Smallest remediation.** Either make the capture key content-addressed (sha256 of the body) rather than
URL-addressed, or have `capture-fetch.py` refuse to overwrite an existing key whose bytes differ (or store
the second body under a distinct key), so every ledger row keeps a live referent.

---

## Finding 6 — LOW: no secret values in the new bytes; the two "bearer/basic" hits are CSS, not credentials

Shape-only scan of the full base→landing diff's added lines and of all sixteen new capture files
(`receipts/e3-secret-shapes.txt`). Detector classes: `AUTH_HEADER`, `BEARER`, `SECRET_ASSIGN`, `JWT`,
`AWS_AK`, `GH_TOKEN`, `SLACK`, `PEM`, `COOKIE_HDR`, `AWS_SECRET_KV`, `GOOGLE_KEY`, webhook URLs.

No `JWT`, `AWS_AK`, `GH_TOKEN`, `SLACK`, `PEM`, `GOOGLE_KEY`, webhook or `AUTH_HEADER` match anywhere in the
new bytes. The only hits are the two `basic` matches in the PRISMA captures, and they are CSS:

```
file=corpus/captures/1f5f4eec0b85edf1dc53db7b.raw line=83
  redacted_window= '… tweak-fixed-header-style-basic <REDACTED> tweak-blog-item-text-alignment-left …'
file=corpus/captures/259c96bf7088a12bc7ce65c4.raw line=83   (identical value, same site theme)
```

`distinct=15 alpha=24 digit=0`, not base64-decodable to printable text, sitting inside a WordPress theme
class list — a CSS token, not a credential. The two `cookie`-shaped matches in the PubMed 203 capture are
that page's own JavaScript (`document.cookie = …`, `__identity_pow_cookie_check_…`) — a cookie *challenge*
served to us, containing no cookie value we supplied and no session id.

The fetch path carries no credentials: `tools/capture-fetch.py` builds
`curl -fsSL --compressed --max-time 15 -A <UA> -o … -w %{http_code} <url>` — a GET with a browser UA, no
`-b/--cookie`, no `-u/--user`, no `--netrc`, no `Authorization` header, no `-d/--data` (no POST). Verified by
grep over the tool: no credential flag is present.

**Verdict on secrets: held.** No secret value in any new byte; nothing to redact.

---

## Finding 7 — LOW: province is respected, with one row that should be reported out

`PROVINCE.md` (lane root):

> **Refuses:** bounty-program scope and claim packages (→ kasegi); model-quality or evaluation claims
> (→ kengaku); orchestration, multi-agent dispatch and agent lifecycle (→ kumitate …); external live-target
> research without operator approval (loopback-only otherwise); secret values in any record (→ kagi for
> custody; shape-only here).

The new entry `corpus/knowledge/search-transparency-reporting-r84.md` is search-transparency reporting —
source-research craft, squarely chousa's. No bounty/program scope, no multi-agent dispatch or lifecycle
content, no secret values. `tools/gate-records.py` is a lane-internal verifier over committed lane bytes
(read-only, `git cat-file` only, no network) — its own lane's corpus and gates, which `PROVINCE.md` owns.

One row is adjacent to kengaku and worth reporting out rather than absorbing —
`search-transparency-reporting-r84.md` line 45:

```
| Comparing evidence-based generation approaches | use a shared taxonomy and unified benchmarks rather
  than isolated evaluation practices | compare approaches that use different terminologies and metrics
  without noting the fragmentation | Q8 (S018) |
```

Q8 is "the field is fragmented due to inconsistent terminology, isolated evaluation practices, and a lack of
unified benchmarks" — a statement about an LLM-generation field's evaluation methodology. The Do/Never
column states a rule about *how to compare model outputs by taxonomy and benchmark*, which reads as
model-evaluation craft rather than search reporting. The entry's own `## Limits` section already concedes
the tension: "The S018 survey is about evidence-based text generation with LLMs, not systematic reviews;
its taxonomy and metrics are for model evaluation, not for search reporting. The rows keep only the
attribution/traceability motivation." — yet Q8 is exactly the taxonomy/benchmark row, not the
attribution/traceability motivation. The claim is honestly bounded in prose; the row table is where the
absorption shows.

**Impact.** Low: the entry does not claim model quality, does not evaluate a model, and the limits section
flags the boundary. It is a report-out candidate, not an absorption of consequence.

**Smallest remediation.** Drop the Q8 row (it is not needed for search-transparency reporting) or restate it
as "note the fragmentation when comparing sources' evaluation practices", keeping the substance in the lane's
own method frame.

---

## Finding 8 — misroot and scratch hygiene

**Misroot (fleet root).**

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
?? .scratch/run15-wrapup/misroot-cff0b4cb/
```

The untracked fleet-root files are `.scratch/run15-wrapup/misroot-cff0b4cb/versions.html` (2466 B) and
`.scratch/run15-wrapup/misroot-cff0b4cb/w4lines.txt` (119 B). Neither names chousa round 84:
`grep -c -i "chousa" versions.html` → 0; `w4lines.txt` is a bare list of line numbers. The two *modified*
fleet-root files do mention the round — `goal-20261103-hyaku-run15.md` lines 241/248/250 say "chousa r84
quality-paused", and `run15-state.json` line 117 carries `"label": "ChousaR84"` — but they are the
orchestrator's own goal/state files, modified by the orchestrator, not lane output. I moved and deleted
nothing.

**Lane tree.** `git -C …/chousa-shokunin status --porcelain --untracked-files=all` shows only
`.ufo/waves/round-84/w1/…` seat outputs as untracked — no lane file outside the wave folder is dirty, and
`corpus/` and `tools/` are untouched relative to HEAD.

**Scratch.** `du -sh /fast/scratch/hyaku/chousa-r84` → **6.2 G** at the time of measurement, spread over
sibling seats' directories (`R84ExecRepro` 1.7 G, `R84CriticClaims` and `R84ScoutNovelty` 729 M each,
`R84ExecForge`/`R84ExecHarm`/`R84MutationTool`/`R84ReviewerTool`/`R84ScribeLesson` 365 M each, plus
`base`, `prerepair`, `tmp.1xpB7Srtpd`, `tmp.lmsCxeei10` at 358–365 M each, and small `tmp.*`/`probe`
dirs). Those are sibling seats' scratch, still in use; I deleted only my own.

`/tmp` leftovers matching `r84` (14 entries): `battery-r84.txt.cmds`, `closure-{kengaku,kumitate,mori,tameshi}-r84-entry.json`,
`kama-r84-closure-entry.json`, `r84-census.txt`, `r84-kotodama-closure-entry.json`, `r84-mksq.html`,
`r84-plan.err`, `r84-plan.json`, `r88m-r84c1/`, `r88m-r84c2/`, `.r84-f2-critic-counter`. None names
chousa (`grep -c -i chousa` → 0 in every one); `r84-plan.json` is `"wave": "kengaku-r84-w1"` and
`r84-census.txt` is a fleet census across lanes. These are other lanes' and earlier rounds' `/tmp` residue
(dated Nov 4–6), not chousa round 84's. Per the lane rule a `/tmp` path is never citable evidence; I cite
none.

**My own scratch.** Everything I created lived under
`/fast/scratch/hyaku/chousa-r84/R84SentinelScope/` and is deleted before this report is yielded.

---

## Summary

| # | severity | finding |
|---|---|---|
| 1 | HIGH | frozen `claims.md` and all control receipts were rewritten in the fetch commit `3a17f4da`; the landed predicate set is not the frozen one (freeze sha `f6f032a6…` vs landing `19d68274…`), and `instrument-pins.txt` pins the amended file |
| 2 | HIGH | 9 of the 10 fetched URLs are absent from the egress table's intended-targets list; the lesson asserts they are all in it; the PRISMA fetches follow a link chain the table forbids |
| 3 | HIGH | `capture-fetch.py` and `gate-records.py` both treat HTTP 203 as success, so a PubMed cookie wall is certified `OK` as an admitted, quoted source (demonstrated) |
| 4 | MEDIUM | the frozen K2 setup leg misreports: non-git `--repo` gives `FAIL LINE,REV` exit 1, not `GATE_RECORDS_ERROR` exit 2 (demonstrated) |
| 5 | MEDIUM | the S021 ledger row's `raw_sha256` has no file in the capture store — a same-URL re-fetch under a second id overwrote the first body |
| 6 | LOW | no secret value in any new byte; the two `basic` hits are WordPress CSS tokens; the fetch path sends no credentials |
| 7 | LOW | province respected; one row (Q8/S018, taxonomy-and-benchmarks) is kengaku-adjacent and should be reported out, matching the entry's own `## Limits` |
| 8 | — | misroot: no chousa-named untracked fleet-root file; 6.2 G of sibling scratch under `/fast/scratch/hyaku/chousa-r84` (not mine); `/tmp` r84 residue belongs to other lanes |

Tooling: none installed. `/home/vgpnk/.omp/agent/RULES.md` was read first; the pacman guard was respected
(no pacman transaction was run, no tool upgrade was needed — every check used the host's existing
`git`, `python3`, `curl` and standard-library `hashlib`).

Verification notes for the main agent: every finding above names the exact command, the receipt path under
`.ufo/waves/round-84/w1/R84SentinelScope/receipts/`, and the observed line with its exit code. Findings 1, 2,
5, 6, 7, 8 are read-only observations over committed lane bytes. Findings 3 and 4 were reproduced through the
public CLI at the landing revision with all fixtures in scratch; the forged record for Finding 3 exists only
in scratch and was never written to the lane. I did not re-run the frozen counters' full control suite
beyond the single landing-revision counter run quoted above.

VERDICT: R84SentinelScope C1 fired — the frozen K2 setup leg misreports at the landing revision (`FAIL LINE,REV` exit 1 where the frozen rule requires `GATE_RECORDS_ERROR` exit 2), and the HTTP-203 cookie wall is certified `OK` as an admitted quoted source.
VERDICT: R84SentinelScope C2 fired — the scored claim's predicate file was rewritten in the fetch commit (freeze sha `f6f032a6…` vs landing `19d68274…`), 9 of the 10 fetched URLs are absent from the egress table's intended-targets list the lesson cites as covering all of them, and the landing pin attests the amended file.
