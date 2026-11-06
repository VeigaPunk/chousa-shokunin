# R82SentinelScope — boundary / safety sentinel, chousa round 82

Read-only seat. Base `142b6f0c`, egress table `5d792e1e`, prefreeze `38f5af82`, freeze `57c0d167`, landing
`b4a41d25`. I made **no network requests**; every command ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin`
or my seat scratch `/fast/scratch/hyaku/chousa-r82/R82SentinelScope` (removed before yield). Receipts:
`receipts/01-egress-ordering.txt`, `02-province.txt`, `03-secrets.txt`, `04-instrument-freeze.txt`,
`05-misroot.txt`, `06-scratch.txt` (relative to this seat's output folder).

## 1. Egress — table written before fetches: CLOSED for round 82 (no kill)

Evidence (receipt 01):
- `git log -1 --format=%cI 5d792e1e…` → `2026-11-06T16:41:56-03:00` = **19:41:56Z**; the file has exactly one commit
  (`git log -- corpus/evidence/round82/egress-approval.md` → only `5d792e1e`), so it was not amended after the fact. rc 0.
- `refetch.tsv` delta base→landing is **5 insertions, 0 deletions** (`git diff --numstat` → `5 0`), i.e. append-only.
- The only rows after 19:00Z are the five round-82 rows: S008 19:42:03Z, S209 19:42:05Z, S210 19:42:08Z,
  S211 19:42:10Z, S028 19:42:10Z — all **after** 19:41:56Z; zero rows in [19:41:56Z, 19:42:03Z).
- The six earlier 2026-11-06 rows (S203–S208, 18:44:29–31Z) are round-81's: added by `f7929f87` (2026-11-06T18:47:58Z),
  `git merge-base --is-ancestor f7929f87 142b6f0c` → rc 0, and fetched (18:44Z) before base was committed (19:17:02Z).
- Every round-82 row's URL appears verbatim in the table's intended-targets list (`url_in_table=True` ×5), one attempt
  each (`attempt=1`), `curl_rc=0`, `http_code=200`, 5 distinct URLs.
- Bytes are consistent with the rows: for all five keys the stored `.raw` and `.txt` sha256 equal the row's
  `raw_sha256`/`txt_sha256` (`raw_sha_matches=True txt_sha_matches=True` ×5). The 10 new capture files are exactly
  those 5 keys; no new capture key lacks a row. (The one row-less key in the store, `53a92273…`, is base content from
  2026-10-27 `hyaku run9 wrap-up`, `git ls-tree 142b6f0c` present → rc 0.)
- No credentials: `tools/capture-fetch.py:137` builds
  `["curl","-fsSL","--compressed","--max-time","15","-A",UA,"-o",…,"-w","%{http_code}",url]` — no `-b`, `--cookie`,
  `-H`, `--user`/`-u`, no Authorization/Bearer anywhere in the file (grep rc 0, only the argv line matches).
- Peer re-open log `w1/R82ExecReopen/live/fetch-log.tsv`: 5 GETs, the same five approved URLs, `http_code=200`,
  `curl_rc=0`, no credentials.

**Residual R-1 (Low) — method deviates from the table's "same UA".** The wave spec and the executed peer log use
`UA='Mozilla/5.0 (X11; Linux x86_64)'` and `--max-time 30` (`w1/R82ExecReopen/commands.txt:79-80`; generated in
`.ufo/waves/round-82/build_spec.py:86`), while the table's wave-seat row requires "one GET per URL per seat, **same UA**"
and the campaign recipe (`capture-fetch.py`) is `--max-time 15` with the full `… Chrome/124.0 Safari/537.36` UA.
Exploit path: none — target selection, method (GET), rate (1/URL) and credential-freedom are all as approved; the UA
only changes who the request identifies as. Impact: the table overstated what was executed. Smallest remediation:
either fix the spec boilerplate to the campaign UA/15 s, or amend the table's wave-seat row to name the short UA.

**Residual R-2 (Info) — the record cannot, by itself, prove a fetch went through the tool.** A manual `curl` would be
invisible except by a missing/extra row. Here the residual cover is strong (hash equality of stored bytes to rows,
1 attempt/URL, all URLs approved, no unrowed new captures, no out-of-table success rows), but it is inferential.

## 2. Province — no sibling absorption (held)

`PROVINCE.md`: "**Owns:** question framing; source hierarchy …; this lane's own corpus and gates." / "**Refuses:**
bounty-program scope and claim packages (→ kasegi); model-quality or evaluation claims (→ kengaku); orchestration,
multi-agent dispatch and agent lifecycle (→ kumitate …); external live-target research without operator approval
(loopback-only otherwise); secret values in any record (→ kagi for custody; shape-only here)." / "**Out of province →
report, never absorb.**"

- The new entry opens on that owned ground: "The lane's method starts at question framing (`PROVINCE.md`; SKILL.md
  "Question framing") …" and scopes itself: "A research record here is not a systematic review; the entry takes from
  them only what transfers". `grep -niE 'kengaku|kasegi|kumitate|kagi|bounty|orchestrat|secret|credential|token'` on
  the entry → **rc 1 (no match)**. Its rows are method rules (frame choice, eligibility alignment, deviation
  reporting) — no model-quality/evaluation claim, no bounty scope, no orchestration, no secret handling.
- The gate change (`tools/research-gate.sh` +178/−12) touches only `verify_sweeps`: rejection sections, placeholder
  cells, negative-claim resolution, plus selftest cases. `grep -c 'kengaku|kasegi|kumitate|kagi'` on the gate diff →
  **0**. No new capability over secrets, model quality, bounty scope or dispatch.
- The one sibling mention is deference, not absorption: `c1-records/sweeps-r5.md:44` R2 — "the ACE numerals are
  model-quality claims from **kengaku province**, carried here only as a hedge form | a **kengaku-lane adjudication**
  of those numerals would flip this rejection". The lane records its own rejection and hands adjudication away.

## 3. Secrets — one low residual, no credential in the lane's own records

Scanned `git diff 142b6f0c b4a41d25` (4,249,427 B) plus the five new captures, shape-only (receipt 03; no value printed).

Counts in the five new captures (raw / txt): `authorization=0`, `set-cookie=0`, `Bearer=0`, `api_key=0`, private key=0,
GitHub/AWS/Slack shapes=0. Non-capture added lines: 0 base64ish runs ≥40 with mixed case+digit; 0 credential
transports (`Authorization`, `--user`, `-u`, `-b`, `--cookie`).

- **JWT-shaped: 30 occurrences**, all in the three JBI Confluence **raw** captures (10 each: `21323730…`, `bcb4a695…`,
  `97223722…`); **0 in the `.txt` forms**, so no knowledge entry, quote or registry row carries one. This is new for the
  corpus: 0 JWT-shaped strings in the 139 base capture files.
  Structure (decoded claim names only): (a) page context tokens `{context, exp, iat, iss, qsh}` bound to one
  `contentId`; (b) CDN/media tokens `{access, authType, exp, iss, nbf, …}` with `authType="unauthenticated"` and
  `access={urn:filestore:collection:contentId-<page>: ["read"]}`. Issuers are instance UUIDs, not user ids; no identity
  claim. Lifetimes: issued 19:42:05–19:42:09Z, `exp` 19:45:05–20:30:09Z; **6 tokens were still within validity at
  report time (20:03:23Z)** and expire by 20:30:09Z.
- `requestCorrelationId` (3 raw + 3 txt, one per Confluence page): the value sits in the
  `confluence-server-performance` span `{"serverDuration": N, "requestCorrelationId": …}` — a per-request correlation id
  for Atlassian support. **Judged: not a credential** — grants nothing, carries no identity, is emitted to anonymous
  clients. Residual: it correlates our fetch in Atlassian's server logs (minor linkability, not custody material).
- `sessionId` (3, one per Confluence raw): a Statsig SDK bootstrap session id inside page JS (36 chars, uuid-shaped).
  Not an auth session, not a cookie value; not a credential.
- `cookie=` (3, all in the Cochrane raw `fd7eed5e…`): JavaScript source (`e.cookie=t+"="+n+…`, `e.cookie="_cookies=;…"`),
  not a cookie value. The `Cookie":` hits were `initializeCookie` timing keys — false positives.

**Residual R-3 (Low) — capture class now carries third-party signed values.** `PROVINCE.md` refuses "secret values in
any record (→ kagi for custody; shape-only here)", and three committed records now hold 30 signed tokens. Exploit path:
replay one of the 6 still-live CDN tokens (≤27 min at report time) to read that public page's attachment collection
anonymously — i.e. no privilege above anonymous access to an already-public page; no operator credential, no write, no
user identity. Impact: a policy-shape gap, not an exposure. The captures **cannot be scrubbed**: their bytes are pinned by
`refetch.tsv` and re-derived by C2 K2, so rewriting them would break the pin (a worse defect). Smallest remediation:
state the capture-class carve-out once in `egress-approval.md` ("raw captures are byte-pinned third-party public pages;
anonymous expiring embedded tokens are not custody material; the `.txt` quotable form strips them — verified"), and log
the shape in the round-82 lesson. Do not rewrite captures.

## 4. Misroot — clean (held)

`git -C /home/vgpnk/Projects/shokunin status --porcelain` (receipt 05):
```
 M .scratch/run15-state.json
?? .scratch/run15-wrapup/misroot-cff0b4cb/
```
- The single untracked entry holds only `versions.html` (2,466 B) and `w4lines.txt` (119 B);
  `grep -ilE 'chousa|round[- ]?82|r82'` over them → **rc 1 (no match)**.
- The only round-82 token at the fleet root is in the **tracked**, modified `.scratch/run15-state.json`
  (`"label": "ChousaR81"` → `"ChousaR82"`), which is the fleet state file, not a stray artifact.
- No untracked fleet-root file names chousa round 82. Nothing moved or deleted.

## 5. Scratch — seat clean; host leftovers reported, not touched (Info/Low)

Receipt 06: `/fast/scratch/hyaku/chousa-r82` = **8.0G** while peers run (largest `R82ExecRepro` 2.1G,
`R82CriticClaims` 1.7G); my seat dir was 4.3M and is **removed** — `du -sh …/R82SentinelScope` → rc 1 and
`test -e` → rc 1 after cleanup.

`ls /tmp | grep -i r82` → **29 entries**, ≈2.0G: `mado-base-r82` 515M, `r82c1tree` 743M, `r82c2tree` 743M, plus
`build-spec-r82.py`, `r82c1_*.py`, `r82claims_{2738,at_c804,c058}.md`, `closure-{kake,kotodama,mado,mori,tsukuroi}-r82.json`,
`kaidoku/kama/kumitate-r82-closure*.json`, `r88m-r82c2*`, `mut-r82.json`, `live-r82.txt`, `r82-files.txt`,
`r82_hashes.txt`, `r82-wave.err`, `r82old.md`, `r82c1test`, `r82c1_freeze.py`.
All mtimes are **2026-11-04 / 11-05** (`r82c1tree` 2026-11-05 05:21Z, `r82claims_2738.md` 2026-11-05 05:15Z,
`mado-base-r82` 2026-11-04 13:50Z) — more than 36 h before this round's base (2026-11-06T19:17:02Z). So they are
**not** this wave's chousa evidence (four are chousa-shaped: `r82c1_*`, `r82c1tree`, `r82claims_*`) and none is citable;
they still breach the "never write under /tmp" rule and are reaper-fragile. Not deleted — they are not mine to remove.

## Frozen-instrument integrity (supporting, receipt 04)

At freeze `57c0d167` and at landing `b4a41d25`, all five frozen instruments are byte-identical to `instrument-pins.txt`:
`k2-gate-r82.py`, `depth-r82.py`, `run-controls-r82.sh`, `c1-manifest.tsv`, `base-knowledge.txt`
(`pin_match_prefreeze=True pin_match_landing=True`); `c1-records/*` aggregate `f3e5dca7…` reproduces with the pin's own
formula (`sha256sum * | sha256sum`) at prefreeze. Gate and SKILL.md pin-match prefreeze and change only at landing, as
the claim requires. `git diff --stat 57c0d167 b4a41d25 -- controls claims.md instrument-pins run-controls c1-manifest
c1-records` → **empty, rc 0**. No claim, counter, manifest, fixture or receipt was amended after freeze.

## Severity summary

| id | severity | subject | status |
|---|---|---|---|
| — | — | egress ordering (round-81 routed defect 3) | closed for round 82; no kill |
| R-1 | Low | wave-seat re-open UA/max-time ≠ table's "same UA" | residual, no privilege effect |
| R-2 | Info | record cannot prove tool-mediated GET | inferential cover documented |
| R-3 | Low | 30 third-party anonymous expiring JWTs in 3 raw captures (0 in `.txt`), unscrubbable | residual; document carve-out |
| — | — | province (kengaku/kasegi/kumitate/kagi) | held; deference recorded |
| — | — | misroot at fleet root | held; nothing stray |
| R-4 | Low | 29 `/tmp/*r82*` entries ≈2.0G, pre-base | reported, not deleted |

No kill rule of C1 or C2 fired on the surfaces assigned to this seat, and no finding above is a kill.

VERDICT: R82SentinelScope C1 held — egress table precedes every round-82 fetch (19:41:56Z < 19:42:03Z) and the five frozen instruments are byte-identical at freeze and landing, with only a Low UA-conformance residual.
VERDICT: R82SentinelScope C2 held — all five capture pairs re-hash to their refetch rows and no credential-shaped value reaches any quotable `.txt`/entry, with the anonymous third-party token shapes inside the raw captures recorded as a Low, unscrubbable residual.
