# R83SentinelScope — boundary and safety sentinel, chousa round 83

Scope: the five surfaces named in the seat item — (1) egress order and fetch method, (2) sibling province,
(3) credential shapes, (4) fleet-root misroot, (5) scratch leftovers. Read-only; no lane or fleet git/jj mutation;
no network calls by this seat; no tool installs. Revisions measured: base `a46534a51756f7e7d9bb55dd9a275156d908d84c`,
egress `8fff80ee43fbb99fb391c0f4751dbfd47c722744`, prefreeze `1b9b2ff8955190a3e5cd42800009d13d6b8e4e04`,
freeze `3fbf8d1227a8aa317a036604edad93d7b20a149f`, landing `81b81173f19d175e2b2a6b409b2a496d09d0b258`,
tip `aca2a781ef2db375881c21bf407e153f786ac61f`.

Receipts (all under `.ufo/waves/round-83/w1/R83SentinelScope/receipts/`):
`egress-receipt.txt`, `province-receipt.txt`, `secrets-receipt.txt`, `misroot-receipt.txt`,
`scratch-receipt.txt`, `residuals-receipt.txt`.

## Findings in class

None. No kill rule fires on any of the five surfaces; every expected value was observed. Out-of-class residuals are
listed separately below.

## (1) Egress — held

Command: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log -1 --format='%H|%aI|%cI|%ct' 8fff80ee43fbb99fb391c0f4751dbfd47c722744`
→ `8fff80ee…|2026-11-06T17:49:13-03:00|2026-11-06T17:53:00-03:00|1793998380` (rc 0). Converted: committer
`2026-11-06T20:53:00Z`, author `2026-11-06T20:49:13Z`.

Every `refetch.tsv` row dated 2026-11-06 after 20:00Z (the three round-83 rows, and only those):

| id | fetched_utc | delta vs committer | attempt | curl_rc | http |
|---|---|---|---|---|---|
| S009 | 2026-11-06T20:53:06Z | +6 s, after commit | 1 | 0 | 200 |
| S212 | 2026-11-06T20:53:07Z | +7 s, after commit | 1 | 0 | 200 |
| S213 | 2026-11-06T20:53:08Z | +8 s, after commit | 1 | 0 | 200 |

- Exact URL-cell equality with the egress table's intended-targets list: S009, S212, S213 all `True` (the table holds
  exactly 3 URLs; S009's cell equals the registry row's URL). `key = sha256(url)[:24]` holds for all three.
- Capture bytes: `sha256sum` of the six committed capture files equals the rows' `raw_sha256`/`txt_sha256` (all True).
- Structural order (stronger than timestamps): the egress file is absent at base, added in `8fff80ee`; the tree of
  `8fff80ee` contains **0** rows matching `2026-11-06T20:53`, the tree of `1b9b2ff8` contains **3**; `8fff80ee` is an
  ancestor of `1b9b2ff8` (`git merge-base --is-ancestor`, rc 0). The rows are therefore first committed in a descendant
  of the commit that carries the table.
- Method: `tools/capture-fetch.py:137-138` builds `["curl","-fsSL","--compressed","--max-time","15","-A",UA,"-o",out,"-w","%{http_code}",url]`
  — a GET (no `-X`, no `-d`), no `-u`/`--user`, no `-b`/`--cookie`, no `-H`, no `--netrc`. The UA is the frozen campaign
  UA. No credential path is present.
- Corroboration: `/fast/scratch/hyaku/chousa-r57/fetch/refetch.append` (3694 bytes, mtime 2026-11-06 17:53 local =
  20:53Z) ends with the same three rows at the same timestamps; 14 lines total (r81 6 + r82 5 + r83 3), so the fetch
  ran through the tool at the recorded time.
- The three captures contain no login/paywall/captcha indicator, and the three Gate quotes are present in the
  committed `.txt` captures after normalization (True/True/True). `git diff base..tip` adds exactly 3 refetch rows and
  exactly 3 capture keys (6 files).

## (2) Province — held, no absorption

`PROVINCE.md:5-8`: "**Owns:** … claim-vs-source verification; … the external-target approval table for a research
window; this lane's own corpus and gates." `PROVINCE.md:10-15`: "**Refuses:** bounty-program scope and claim packages
(→ kasegi); model-quality or evaluation claims (→ kengaku); orchestration, multi-agent dispatch and agent lifecycle
(→ kumitate …); external live-target research without operator approval (loopback-only otherwise); secret values in any
record (→ kagi for custody; shape-only here)."

The entry stays inside that boundary: `appraisal-judgment-records-r83.md:9` — "The lane's method ends in a judgment: a
claim is supported by its source or not (`PROVINCE.md` \"claim-vs-source verification\")"; `:55-56` — "For this lane a
\"judgment\" is a claim-vs-source verdict (`supported`, `contradicted`, `not-found`) and the \"proposed judgment\" of row 7
is a gate's or counter's verdict"; `:70` — the one kengaku-adjacent item (a machine-learning tool study reported inside
S212) is explicitly declined: "that is a study finding, not the standard, and the row does not rely on it."
`tools/gate-records.py:2,9,11` scopes the tool to "committed lane bytes: `corpus/SOURCES.md`, `corpus/captures/`,
`corpus/evidence/round57/refetch.tsv`" and read-only `git cat-file`.

Delta grep for `kengaku|kasegi|kumitate|kagi|model[- ]quality|bounty|orchestrat|secret` returns exactly one line: the
egress table's own statement that "the lane's province refuses *live-target* research (bounty or system targets)" —
consistent with `PROVINCE.md`, not an absorption. Grep of the entry, tool and lesson for
`secret|kagi|kengaku|kasegi|kumitate` returns no match (rc 1). No sibling province is absorbed.

## (3) Secrets — held, none found

Scanned the full bytes of the three new captures (`.raw` and `.txt`, 421,583 bytes raw + 180,734 bytes text) and every
added non-capture line of `git diff a46534a5 aca2a781` (1,789 added lines) against 19 credential shapes: private-key
block, AWS `AKIA`, GitHub/Slack/GitLab/npm/HuggingFace/SendGrid tokens, JWT `eyJ…`, `Authorization`/`Cookie` headers,
`Bearer`/`Basic`, `api_key|access_token|client_secret|password|sessionid|csrf_token` key-value forms, URL token
parameters, URL userinfo, `sk-`/`AIza`/`ssh-rsa`/`-----BEGIN`. **TOTAL_CREDENTIAL_SHAPED_MATCHES=0**; every file
reports `clean`.

Shape-only note (no value printed): each `.raw` contains one client-side consent/analytics cookie script (7
`cookie=…` assignments on one line — 493 / 529 / 519 respectively); the values are computed in-page, there is no
`Set-Cookie` header, no `PHPSESSID`/`JSESSIONID`/`sessionid`, no `csrf`, and no hidden token input. The `.txt` forms
have 0 assignments. Nothing in the diff or captures is a credential.

## (4) Misroot — held, none found

Command: `git -C /home/vgpnk/Projects/shokunin status --porcelain=v1 --untracked-files=all` (rc 0):

```
 M .scratch/run15-state.json
?? .scratch/run15-wrapup/misroot-cff0b4cb/versions.html
?? .scratch/run15-wrapup/misroot-cff0b4cb/w4lines.txt
```

The two untracked fleet-root files are the only untracked files (`git ls-files --others --exclude-standard`). Neither
names chousa round 83: `grep -c -iE 'chousa|round[- ]?83'` = **0** for both. They are the preserved bytes of the
documented souji r70 misroot incident (dispatch prompt line 927: forward fix `0329a2d6` untracked both strays and kept
their bytes at `.scratch/run15-wrapup/misroot-cff0b4cb/`). Nothing was moved or deleted.

An ignored-file sweep (12,996 ignored entries; outside `.jj`, `.tower` and lane dirs; files modified 2026-11-06 and
< 1 MiB) found no file naming chousa **and** round 83. Context, not a misroot: among the files `git status` reports, the only one naming this round is the tracked
`.scratch/run15-state.json` modification (`"label": "ChousaR81"` → `"ChousaR83"`), i.e. run-state bookkeeping; the
tracked dispatch prompt `.ufo/prompts/chousa-round-83.md` also names it, as expected.

## (5) Scratch — leftovers reported

- `du -sh /fast/scratch/hyaku/chousa-r83` → **4.2G** across 11 seat dirs (live seats mid-wave; e.g. `R83ExecRepro`
  1.1G, `R83ScoutNovelty` 700M, `R83CriticClaims` 716M, `R83ExecHarm` 718M). This seat's dir
  `R83SentinelScope` = **0** bytes and is removed before yield.
- `ls /tmp | grep -i r83` → 11 entries: `closure-kake-r83-entry.json`, `kaidoku-r83-closure-entry.json`,
  `kama-r83-closure.json`, `kengaku-r83-closure-4087b2f8.json`, `mado-r83-closure.json`, `r83-audit.err` (empty),
  `r83-review-probe.sh`, `r83-reviewanchor-proposal.patch`, `r88m-r83c1/` (empty), `r88m-r83c2/` (empty),
  `vs-ledger-pcr8365g/` (`census-removals.json`, dated 2026-11-06 10:47, before this round's egress commit). None
  names chousa (`grep -c -i chousa` = 0 on every file; the three dirs carry no chousa content). They are other lanes'
  r83 leftovers; /tmp paths are non-citable and reaper-deletable.
- Older `/tmp` chousa/hyaku leftovers (outside this round, non-citable): `chousa-config-r21`, `chousa-outside-r19`,
  `chousa-outside-r21.txt`, `chousa-r75-closure-entry.json`, `chousa-r79-closure.json`,
  `chousa-round74-closure-8022f72c.json`, `closure-chousa-r76-entry.json`, `closure-r73-chousa.json`,
  `hyaku-closure-r87-tameshi.json`, `hyaku-kengaku-r85-closure-CloseKengakuR85.json`, `hyaku-r90-judge`.
- Round-83 fetch scratch outside the round root: `/fast/scratch/hyaku/chousa-r57/fetch/refetch.append` (3694 bytes,
  mtime 2026-11-06 17:53 local = 20:53Z) and an empty `recipe/` dir. `tools/capture-fetch.py` defaults its scratch to
  `$HYAKU_SCRATCH/chousa-r57/fetch`, so the prefreeze fetch landed under the round-57 name, not `chousa-r83/L1`. It is
  also the positive corroboration of the fetch (see item 1). Left in place: it is evidence, not this seat's scratch.

## Out-of-class residuals (reported, not scored)

- **R1 — worktree vs "committed" bytes.** `tools/gate-records.py:2,9` says it verifies "against committed lane bytes",
  but the implementation opens root-relative worktree paths (`:269-270` registry/refetch, `:224` capture,
  `:215` `sha256_file(cap)`). On a dirty `--root .` a record could pass against uncommitted bytes. The lane worktree is
  clean for the three byte sources (`git status --porcelain -- corpus/SOURCES.md corpus/captures
  corpus/evidence/round57/refetch.tsv` is empty, rc 0) and the frozen counting command passes a `git archive` tree, so
  no observed record is affected and no kill rule fires. Smallest remediation: say "lane tree" in the docstring, or
  refuse a dirty root, or read the three sources through `git cat-file`.
- **R2 — curl config injection path.** `capture-fetch.py:137` invokes `curl` without `-q`, so a `~/.curlrc`,
  `$XDG_CONFIG_HOME/curlrc` or `$CURL_HOME/.curlrc` would be honoured on a future fetch. No such file exists on this
  host (all four candidates absent), so no credential was injected in this round. Smallest remediation: add `-q` as the
  first curl argument.
- **R3 — counter scratch default.** `corpus/evidence/round83/gate-records-r83.py:162` resolves
  `--work` as `a.work or TMPDIR or HYAKU_SCRATCH or /fast/scratch/hyaku`, so a bare run under `TMPDIR=/tmp` would write
  its mkdtemp under /tmp. The frozen counting command passes `--work /fast/scratch/hyaku`, so the round's receipts are
  unaffected.
- **R4 — control-driver scratch not seat-scoped.** `run-controls-r83.sh:9-11` uses
  `$HYAKU_SCRATCH/chousa-r83/controls` and `rm -rf`s it at start and exit; two concurrent runs would collide. It is a
  frozen prefreeze instrument run once by the L1; no leftover `controls/` dir remains.
- **R5 — no subprocess timeout.** `gate-records.py:175,179,182` run `git cat-file` without `timeout=`; a hung git would
  hang the tool. Minor; read-only and no writes.

## Tooling and network

No tool installed or upgraded. No network call was made by this seat (no re-open item names a URL for this seat).

VERDICT: R83SentinelScope C1 n/a — depth predicate not re-run by this seat; its boundary surfaces held (egress commit 20:53:00Z precedes every round-83 fetch at 20:53:06-08Z, GET-only, no credentials, no province absorption, no credential shapes).
VERDICT: R83SentinelScope C2 n/a — 15/198 predicate not re-run by this seat; its boundary surfaces held (no network, zero writes, read-only git cat-file, no secrets), with the worktree-vs-committed provenance gap as an out-of-class residual.
