# R87SentinelScope — round 87 adversarial scope & safety review

Seat: `R87SentinelScope` (sentinel, wave w1, leaf member — no subagent dispatch).
Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Revisions under review: base `6495ef88`, egress `b7db07140791ab071de49743687e6d330edabc2e`,
freeze `c033577b4fb840553f3e10e40aa77c724abe0bca`, landing `e6e920a4e6988287c31e89b3e920a118b569ae52`
(+ post-landing wave-spec commit `abf7ea58`).

Network: **none performed by this seat.** Every check reads committed bytes. Scratch:
`/fast/scratch/hyaku/chousa-r87/R87SentinelScope/` (deleted before this report was written; every receipt cited
below was copied into `.ufo/waves/round-87/w1/R87SentinelScope/receipts/` first).
Tooling: **no installs** — the round needs none, so `RULES.md` was read and no pacman/uv/npx transaction was
run (the pacman guard is host-wide paused anyway).

Summary: **7 findings — 1 medium, 1 low, 5 clean.** No egress violation, no credential material, no lane-written
stray outside the lane root, no host mutation, correct attribution. One medium finding is a defect in the egress
table's own machine-checkable closure predicate (not in the fetch behaviour).

---

## F1 — (a) Egress: every round-87 fetch is inside the approval table — CLEAN

**Intended-targets URL set** (from `corpus/evidence/round87/egress-approval.md`, the `Intended targets` table):
exactly one URL — `https://www.rfc-editor.org/rfc/rfc9110.html` (S216 re-open). The table's `not allowed` cell
forbids cookies, credentials, POST, crawls and >3 attempts per URL.

**Refetch rows at or after the task threshold `2026-11-08T06:40:00Z`** — 1 row:

```
S216  https://www.rfc-editor.org/rfc/rfc9110.html  attempt=2  fetched=2026-11-08T06:50:40Z  curl_rc=0  http=200
```

Command: `awk -F'\t' 'NR>1 && $5 >= "2026-11-08T06:40:00Z"' corpus/evidence/round57/refetch.tsv` → exit 0,
1 row, 1 URL. Receipt: `receipts/egress-refetch-rows.txt`.

**Capture files with mtime after the egress commit** — 2 files, both the S216 capture:

```
2026-11-08+03:50:40.9623607590 corpus/captures/b1b13a12aee75c6ecc20fb91.raw
2026-11-08+03:50:40.9645866420 corpus/captures/b1b13a12aee75c6ecc20fb91.txt
```

Command: `find corpus/captures -type f -newermt '2026-11-08 03:41:19' -printf '%T+ %p\n' | sort` → exit 0.
Identical result with the commit's *committer* time (`03:50:27`) as the bound. The key is content-addressed from
the intended URL: `sha256("https://www.rfc-editor.org/rfc/rfc9110.html")[:24] == b1b13a12aee75c6ecc20fb91`
(verified). Receipt: `receipts/egress-captures-mtime.txt`.

**Ordering.** The egress commit's committer time is `2026-11-08T03:50:27-03:00` (= `06:50:27Z`); the fetch is
stamped `06:50:40Z` and the capture files' mtime is `03:50:40-03:00` (= `06:50:40Z`). The table precedes the
fetch by 13 s (author date `03:41:19-03:00` = `06:41:19Z` precedes it by ~9 min). The single new `refetch.tsv`
row was committed by the landing commit `e6e920a4`, after the table. **No URL was fetched outside the table.**
The capture bytes are unchanged from the round-86 landing that first stored this key
(`git diff --exit-code HEAD -- corpus/captures/` → exit 0) — a re-open, not a capture replacement.

---

## F2 — (a) Egress: the table's own closure predicate is vacuous and names a non-existent column — **MEDIUM**

**Exploit path.** The table is the round's machine-checkable scope artefact, and it says so:

> `corpus/evidence/round87/egress-approval.md:4-5`
> "The commit carrying this file precedes every `corpus/evidence/round57/refetch.tsv` row whose `fetched` is
> `2026-11-08T1` or later; the closure can compare the commit time with the refetch rows."

Two independent defects make that sentence unusable as a check:

1. **Wrong column name.** The TSV column is `fetched_utc` (`corpus/evidence/round57/refetch.tsv:1`:
   `id url key attempt fetched_utc curl_rc http_code raw_sha256 txt_sha256`). The table says `fetched`.
   Rounds 82–86 all say `fetched_utc`; **round 87 is the only round of the seven that renames the column.**
   A closure script that resolves the column by the name the table prints finds no such column.
2. **Vacuous threshold.** `2026-11-08T1` is not a bound that the data satisfies. Measured (receipt
   `receipts/egress-table-predicate.txt`):

   ```
   fetched_utc >= 2026-11-08T1   -> 0 rows
   fetched_utc >= 2026-11-08T01  -> 26 rows
   fetched_utc >= 2026-11-08T06  -> 5 rows
   fetched_utc >= 2026-11-08T10  -> 0 rows
   ```

   Every `fetched_utc` value in the file is `2026-11-08T0x`; lexicographically `"2026-11-08T06…" < "2026-11-08T1"`,
   so the predicate as written selects **zero** rows. Read as an hour-prefix ("hour 1x") it also selects zero.
   The assertion "the commit precedes every row whose fetched is `2026-11-08T1` or later" is therefore true
   vacuously and can never detect an out-of-window fetch — including a fetch that happened *before* the table.
   The bound that actually works, and the one round 86 used, is `2026-11-08T06`: 5 rows, including this round's
   `S216 … 06:50:40Z`.

**Impact.** The behaviour was compliant (F1), so no fetch is out of scope and no rule was broken in fact. The
impact is on the *auditability* the table claims for itself: the one artefact that is supposed to make egress
machine-checkable cannot be executed as written, and its predicate is a no-op that would pass even if the round
had fetched something before committing the table. A closure run against this table would report a green scope
check while checking nothing. This is exactly the "fabricated readiness" class — the artefact asserts a checkable
closure that it does not deliver.

**Smallest remediation.** In `corpus/evidence/round87/egress-approval.md:4-5`, change the column to `fetched_utc`
and the bound to `2026-11-08T06` (matching rounds 82–86 and selecting the five hour-06 rows, of which
`S216 … 2026-11-08T06:50:40Z` is this round's). No code, claim or counter change; no fetch changes.

---

## F3 — (b) Credential shape: no credential material in the round's new files — CLEAN

Scanned every file added or changed by the round (`git diff --name-only 6495ef88 e6e920a4` plus
`git diff --name-only e6e920a4 abf7ea58`, 34 paths) for value-shaped credential material, and re-ran the same
scan on the **added lines only** of the freeze and landing commits. Value patterns used: `ghp_/gho_/ghu_/ghs_/ghr_`,
`glpat-`, `xox[baprs]-`, `AKIA…16`, `AIza…35`, `sk-…20+`, JWT (`eyJ…`), `op://`, `BEGIN … PRIVATE KEY`,
`Authorization: <word> `, `Set-Cookie: `, `Cookie: <alnum>`, `x-api-key`, `api_key = <16+>`.

**Result: zero value-shaped hits.** The only lexical matches are shape references in prose or in the seat prompts
themselves — reported as path:line **shape only, no values**:

| path:line | shape | what it is |
|---|---|---|
| `corpus/evidence/round87/egress-approval.md:18` | the words *cookies*, *credentials* | the `not allowed` cell of the method row — a prohibition, not material |
| `.ufo/waves/round-87/build_spec.py:189-190` | the token *token-*, *cookie-*, `op://`*, *session-* | the seat-spec text that asks for this grep — the instruction, not material |
| `.ufo/waves/round-87/w1-dispatch.json:114-171`, `.ufo/waves/round-87/w1-spec.json:49` | same as above | the same seat prompt text embedded per seat |

Pre-existing, **not** part of this round's additions: `LOG.md:591,597,601,615,621,634,…` mention *token-plan*,
*keys -2/-3*, *key 84* in the rounds-13–16 model-routing narrative. No literal key material is present (a
`[A-Za-z0-9_-]{32,}` scan of `LOG.md:591,621` returns empty). Receipt: `receipts/credential-shape.txt`.

---

## F4 — (c) Scope: no lane-written file outside the lane root — CLEAN

**Landing commit stat** (`git show --stat e6e920a4e6988287c31e89b3e920a118b569ae52`): 11 files, all inside the
lane root — `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md`,
`corpus/evidence/round57/refetch.tsv`, 4× `corpus/evidence/round87/after/*.txt`, `corpus/lessons/round-87.md`.
The full base→landing change set is 30 paths; `git diff --name-only 6495ef88 e6e920a4 | grep -E '^(/|\.\.)'`
→ exit 1 (no absolute path, no parent escape). Receipt: `receipts/scope-lane-paths.txt`.

**Fleet root** `git -C /home/vgpnk/Projects/shokunin status --porcelain`:

```
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
 M .ufo/l0-questions.md
?? .scratch/closure-tabi-r83-entry.json
?? .scratch/run15-wrapup/missroot-cff0b4cb/
```

Every one of these is attributable to the **fleet orchestrator or another lane**, not to chousa round 87:

- `.scratch/run15-state.json` — orchestrator-owned fleet state (named as such in `scripts/hyaku/hyaku.env:99`).
  Its chousa block changes `label ChousaR81→ChousaR87`, `block_start 81→85`, `block_done 0→2` — the orchestrator
  counting rounds, not the lane writing. The lane contains no code that writes this file
  (`grep -rn 'run15-state' --include=*.py --include=*.sh .` → no hit outside wave reports).
- `.scratch/goal-20261103-hyaku-run15.md` — the orchestrator's goal log; the diff tail is its own SIGTERM-resume
  notes (2026-11-06/07), no round-87 chousa content.
- `.ufo/l0-questions.md` — the added lines are `tsukuroi | round-92` entries. `git diff .ufo/l0-questions.md |
  grep -i chousa` → exit 1: chousa has no round-87 L0 line.
- `.scratch/closure-tabi-r83-entry.json` — tabi's r83 artifact.
- `.scratch/run15-wrapup/missroot-cff0b4cb/` — the souji r70 incident keep-dir, documented in
  `scripts/hyaku/lane-addendum.md:787`.

Likewise `.ufo/prompts/chousa-round-87.md` and `.ufo/state/chousa.report-baseline` (both `03:43:03`) are
dispatcher infrastructure — one file per lane with the same mtime and the same shape for every lane in
`.ufo/prompts/` and `.ufo/state/*.report-baseline`.

`git status --porcelain -- scripts/ MANIFEST.json .ufo/state/` → **empty**: the forbidden fleet paths are
untouched. The lane's own working tree contains only in-lane changes (amendments to `plans/round-87.md` and
`corpus/lessons/round-87.md`, plus untracked `corpus/evidence/round87/after/` and `census-*.txt` receipts and
`.ufo/waves/round-87/` wave artefacts) — see F5.

---

## F5 — (c) Scope: the two census receipts are uncommitted, and their mtimes invert the start/end ordering — **LOW**

**Evidence.**

```
-rw-r--r-- 1 vgpnk vgpnk 737 2026-11-08 03:53:49 corpus/evidence/round87/census-end.txt
-rw-r--r-- 1 vgpnk vgpnk 759 2026-11-08 03:55:05 corpus/evidence/round87/census-start.txt
git ls-files --error-unmatch corpus/evidence/round87/census-start.txt → error: pathspec did not match any file
git ls-files --error-unmatch corpus/evidence/round87/census-end.txt   → error: pathspec did not match any file
```

Landing commit committer time: `2026-11-08T03:52:30-03:00`. Both census receipts postdate the landing commit,
and the file named **start** is written 76 s *after* the file named **end**.

**Impact.** `corpus/lessons/round-87.md` §Spot-check intake, conformance row 1, closes round 86's routed defect
"census ran after the landing commit" with: *"avoided — this round's start census ran before any edit and is
recorded in the report"*. The receipt content does support the substance: `census-start.txt` records the registry
**at the base `6495ef88`**, computed from a base archive (`/fast/scratch/hyaku/chousa-r87/l1/fleetbase5/…`), so
the base-state census is correct by construction. What the bytes do **not** do is evidence ordering: the receipt
that asserts "before any edit" carries an mtime *after* the landing commit and after its sibling, and neither
receipt is committed, so a reader of the committed tree has no census receipt at all. The same applies to the
four untracked `after/` receipts that carry the C1/C2 predicate lines
(`c1-after.txt`, `c1-mutants-landing.txt`, `c2-after.txt`, `c2-controls-landing.txt`) — the *committed* `after/`
set is the four `-candidate` files from the pre-landing run, so the landing-revision receipts exist only in the
working tree. Not a claim kill (the predicate re-derives — F6) and not an egress/scope breach; a receipt-hygiene
and provenance-ordering defect.

**Smallest remediation.** Commit `census-start.txt`, `census-end.txt` and the four landing `after/` receipts with
the integration commit, and state in each census receipt the **revision it was computed against** (base archive
for `start`, landing tree for `end`) rather than relying on file order to carry the claim. The conformance row can
then cite a committed receipt.

---

## F6 — (d) Scratch and host: no `/tmp`, no host mutation, no mutating git, zero tree mutation — CLEAN

**Hardcoded `/tmp`** — `grep -n '/tmp' corpus/evidence/round87/*.py` → **exit 1, no hits**. The three tools that
need scratch take it from `--work`, then `TMPDIR`, then `HYAKU_SCRATCH`, and default to `/fast/scratch/hyaku`
(`gate-records-r87.py:361`, `curation-r87-controls.py:79`, `mutate-r87.py:87`). Every temporary directory is
created with `tempfile.mkdtemp(prefix=…, dir=work)` — i.e. **inside** the work dir, so there is no fallback to
the system temp area. `curation-r87.py` needs no scratch at all.

**Host state** — `grep -rniE '(sysctl|sudo|systemctl|service |restart|swapoff|swapon)'` over
`corpus/evidence/round87/*.py`, `plans/round-87.md`, `corpus/lessons/round-87.md` → **exit 1, no hits**. The same
grep over the added lines of the whole base→landing diff → exit 1. No host sysctl is touched, `sudo` is never
invoked, no host service is restarted. (This seat performed none of those either.)

**Git** — the only git verbs anywhere in the round's tools or in the subject tool are read-only:
`git grep` (`gate-records-r87.py:223`), `git cat-file` and `git rev-parse --git-dir` (`tools/gate-records.py:186,190,193,293`).
A scan for mutating verbs (`commit|checkout|reset|add|push|write-tree|commit-tree`) → exit 1, none.
`tools/gate-records.py` writes no file at all (`grep -E 'open\([^)]*"w"|write_text|makedirs|mkdir'` → exit 1).
Receipt: `receipts/scratch-host.txt`.

**Zero mutation, measured.** I rebuilt the landing revision into scratch
(`git archive e6e920a4 | tar -x -C $T`), hashed every file in the tree, ran **all four** round-87 tools against
it, and re-hashed:

```
c1 exit=0   c2 exit=0   controls exit=0   mutate exit=0
--- diff before.sums after.sums ---
diff exit=0 (0 = identical)
```

The tree the counters inspect is byte-identical before and after; all residue lands under the `--work` directory
and is removed by the tools' own `shutil.rmtree(tmp)` in their `finally` blocks. Receipt:
`receipts/zero-mutation.txt`.

**Both predicates re-derive at the landing revision** (read-only, scratch tree) — receipt
`receipts/counters-predicate.txt`:

```
C1: TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1
    RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1
    MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15
    GATE_RECORDS_R87=PASS                                    (exit 0)
C2: SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20
    Q_FLOORS=search-transparency-reporting-r84.md=13/13 floor13,provenance-recording-r85.md=7/7 floor7
    WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7
    TEACHES_FLAGGED S024 terms=publication,modification disposition=superseded by S031
    CURATION_R87=PASS                                        (exit 0)
C2 controls: FORGERY_REFUSED=4/4 R86_ACCEPTED_FORGERY=4/4  CONTROLS=PASS   (exit 0)
```

Every field of both frozen predicate lines is reproduced exactly, and the four round-86 forgeries are refused
with named `LEG_FAIL`s while the round-86 counter accepts them.

---

## F7 — (e) Attribution: landing author and committer are the lane identity — CLEAN

```
e6e920a4  author=chousa-shokunin <chousa@shokunin.local>
          committer=chousa-shokunin <chousa@shokunin.local>
          author date 2026-11-08T03:52:29-03:00   committer date 2026-11-08T03:52:30-03:00
```

Same identity on the freeze `c033577b` and the egress table `b7db0714`, and on the post-landing wave-spec commit
`abf7ea58`. All three commits between the base and the landing carry `chousa-shokunin <chousa@shokunin.local>`
as both author and committer — no other identity appears in `6495ef88..e6e920a4`. Receipt:
`receipts/attribution.txt`.

---

## Cross-note (not a finding in my items)

Observed while reading the round's own artefacts, reported for the L1 rather than adjudicated here:
`plans/round-87.md` (working tree) carries four post-landing amendments that narrow both claims, and the plan
names `.ufo/waves/round-87/claim-falsification.tsv` as the place where a `narrowing` cell resolves to an
amendment section — that ledger file does not exist yet, while rounds 84/85/86 each have one. Also, the harm
sweep re-run at the landing revision reports `files=11 records=28 moved=0` against the freeze receipt's
`files=10 records=27 moved=0`; the lane's own working-tree lesson already discloses this as Correction 2. Both
are the L1's integration items; my scope was egress, credential shape, file scope, scratch/host and attribution.

---

## Receipts

All under `.ufo/waves/round-87/w1/R87SentinelScope/receipts/`:

| file | covers |
|---|---|
| `egress-refetch-rows.txt` | F1 — refetch rows ≥ `2026-11-08T06:40:00Z` |
| `egress-captures-mtime.txt` | F1 — capture files newer than the egress commit; key derivation; intended-URL set |
| `egress-table-predicate.txt` | F2 — the table's own predicate, measured |
| `credential-shape.txt` | F3 — credential-shape scans (value patterns, added-lines-only, shape-only refs) |
| `scope-lane-paths.txt` | F4 — landing stat, base→landing path set, fleet-root porcelain, lane porcelain |
| `scratch-host.txt` | F6 — `/tmp`, sysctl/sudo/service, git verbs, write calls |
| `counters-predicate.txt` | F6 — C1, C2 and C2-controls re-run at the landing revision |
| `zero-mutation.txt` | F6 — before/after tree manifest diff across all four tools |
| `attribution.txt` | F7 — author/committer/date identity of landing, freeze, egress, base |

VERDICT: R87SentinelScope C1 held — the round-87 battery re-derives its full frozen predicate line at the landing revision with zero tree mutation, and no egress, credential, file-scope, host-mutation or attribution defect touches C1's landed bytes.
VERDICT: R87SentinelScope C2 held — the round-87 curation counter re-derives its frozen line and refuses all four round-86 forgeries at the landing revision, and no scope or safety finding in my items bears against C2.
