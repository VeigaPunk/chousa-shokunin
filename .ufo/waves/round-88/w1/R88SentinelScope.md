# R88SentinelScope — adversarial scope & safety review of the round-88 artifacts

Seat: `R88SentinelScope` (leaf; no subagents dispatched, no lane/fleet git or jj mutation, no commits).
Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Subject revision under review: freeze `4ea9d008abfd2e09cb51649a42678a78f52ac530` (parent = base `f484d94fedec3685a3a052a65bc57cd3eb46b7d7`).
Scratch (all clones, trees, fixtures, runs): `/fast/scratch/hyaku/chousa-r88/R88SentinelScope/` — deleted before yield.
Every receipt cited below is copied into this seat's output folder: `.ufo/waves/round-88/w1/R88SentinelScope/receipts/`.
No tool was installed or upgraded this round (nothing was needed; all checks ran on committed bytes with the system python3), so the tooling-authorization record for this seat is empty.

---

## Summary of findings

| # | Item | Severity | One line |
|---|---|---|---|
| F1 | (a)+(c) egress | **none (clean)** | No refetch row with `fetched >= 2026-11-08T07:00:00Z`; no `corpus/captures/` file newer than the freeze commit. The round fetched nothing. |
| F2 | (b) credential shape | **none (clean)** | No token-, cookie-, `op://`- or session-shaped material in the round's new files; every opaque run is a committed-file sha256. |
| F3 | (c) scope | **none (clean, with one observation)** | The freeze commit writes only under `corpus/` and `plans/` inside the lane root; no chousa-lane stray exists in the fleet root. One transient fleet-root `corpus/` appeared during the watch window and is **not** chousa-attributable. |
| F4 | (c) plan-vs-tree | **medium** | `plans/round-88.md` claims the freeze commits `claims.json` and "the egress table"; neither file exists for round 88. |
| F5 | (d) scratch & host | **none (clean, two low notes)** | No `/tmp` hardcode, no sysctl, no sudo, no service control, no network primitive, no mutating git verb in any round-88 instrument. |
| F6 | (e) attribution | **none (clean)** | Author and committer of `4ea9d008` are both `chousa-shokunin <chousa@shokunin.local>`. |
| F7 | control integrity (outside (a)–(e), reported because it is a provenance defect) | **medium** | The committed `c1-k0-donothing.txt` receipt is byte-identical to the landing run (PASS), while `controls/expected.tsv` expects that case to exit 1; the case is unsatisfiable because the subject tool is unchanged this round. |
| F7b | control integrity (outside (a)–(e)) | **low** | The shipped receipt `c2-d0-donothing.txt` has no row in `controls/expected.tsv`; the other five receipts all do. |

---

## (a) Egress — this round fetches nothing

**F1 — no post-cutoff fetch, no post-freeze capture. Severity: none (clean).**

Exact commands and observed lines (receipt `receipts/a1-refetch-cutoff.txt`, `receipts/a2-captures-freshness.txt`):

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ awk -F'\t' 'NR>1 && $5 >= "2026-11-08T07:00:00Z"' corpus/evidence/round57/refetch.tsv
# exit=0 count=0            ← zero rows printed
$ awk -F'\t' 'NR>1{print $5}' corpus/evidence/round57/refetch.tsv | sort | tail -1
2026-11-08T06:50:40Z        ← newest fetched_utc in the only fetch ledger in the lane
$ wc -l corpus/evidence/round57/refetch.tsv   → 185 lines = 1 header + 184 data rows
$ grep -rln 'fetched_utc' corpus/   → only corpus/evidence/round57/refetch.tsv is a fetch ledger
                                     (other hits are code/prose reading that column)
```

The requested listing of every row with `fetched >= 2026-11-08T07:00:00Z` is **empty**; that is the whole list.

Freshness of the capture store against the freeze commit (both the author and the committer timestamp were used, so the result does not depend on which one is authoritative):

```
$ AT=$(git log -1 --format=%at 4ea9d008)   # 1794122972 = 2026-11-08T07:29:32Z (author)
$ CT=$(git log -1 --format=%ct 4ea9d008)   # 1794124022 = 2026-11-08T07:47:02Z (committer)
$ find corpus/captures -type f -newermt "@$AT" -print   → (no output)  exit=0  count=0
$ find corpus/captures -type f -newermt "@$CT" -print   → (no output)  exit=0  count=0
$ find corpus/captures -type f -printf '%T@ %p\n' | sort -rn | head -3
1794120640.96 corpus/captures/b1b13a12aee75c6ecc20fb91.txt     (S216, newest capture in the store)
1794117611.09 corpus/captures/f5545a194c06ab421875b047.txt
$ find corpus -name '*.raw' -not -path '*/captures/*'            → (no output)  exit=0
```

Provenance of the newest fetch (why it is *not* this round's): the newest row is `S216 … attempt 2 … 2026-11-08T06:50:40Z`, and it was committed by round-87's landing `e6e920a4e6988287c31e89b3e920a118b569ae52` (`2026-11-08T03:52:30-03:00`); `git merge-base --is-ancestor e6e920a4 f484d94f` → exit 0, i.e. it is already inside the round-88 **base**. `corpus/evidence/round88/claims.md:52` and `:93` cite S216 and S218 "through the round-87 claims file", and S218 is own-work (`corpus/SOURCES.md:231`, `own-work`), so neither claim depends on a round-88 GET.

Conclusion: no row fetched at or after the cutoff, no capture newer than the freeze, and no round-88 instrument carries a network primitive at all (F5), so a GET from this round's code is structurally impossible.

---

## (b) Credential shape — shape only, no values

**F2 — no credential-shaped material. Severity: none (clean).**

Receipt `receipts/b-credential-shape.txt` (path:line shape only; **no value is reproduced here**).

```
$ grep -rn -i -E 'op://|bearer|authorization|cookie|session|api.?key|secret|passwd|password|credential|token' \
    plans/round-88.md corpus/evidence/round88/ corpus/knowledge/provenance-recording-r85.md
plans/round-88.md:33            — "…a per-row token floor at the measured minimum (A2)…"
plans/round-88.md:59            — "…a per-row token floor `MIN_TOKENS = 7`…"
corpus/evidence/round88/claims.md:64
corpus/evidence/round88/claims.md:111
corpus/evidence/round88/curation-r88.py:10,25,56,59,199,222   — all "token" = a lexical token count
exit=0
```

Every hit is the word *token* in the lexical-token-count sense (`MIN_TOKENS = 7`, the per-row quote-length floor) or the prose around it. Shape-specific scans:

```
$ grep -rn -E 'ghp_|gho_|ghs_|glpat-|github_pat_|xox[baprs]-|AKIA[0-9A-Z]{16}|sk-[A-Za-z0-9]{20}|-----BEGIN|1Password|Bearer [A-Za-z0-9._-]{16,}' <same files>
exit=0, no line printed     ← no provider-token shape
$ grep -rn -E 'https?://[^/[:space:]]*:[^@[:space:]]*@' <same files>
exit=0, no line printed     ← no credential-in-URL
$ grep -rn -o -E '[A-Za-z0-9+/]{40,}={0,2}' <same files>
corpus/evidence/round88/instrument-pins.txt:1..14   ← sha256 digests of committed files
corpus/evidence/round88/c1-positives.tsv:1..15      ← `rev=` git commit ids + capture sha256 prefixes
corpus/evidence/round88/census-start.txt:1          ← the base commit id
```

The 40+ character runs are all content-addressed digests of committed artifacts (the instrument pins) or git object ids (the `rev=` field of each frozen positive) — none is a secret. Nothing in the round's new files is credential-, cookie-, session- or `op://`-shaped.

---

## (c) Scope — does anything write outside the lane root?

**F3 — the freeze writes only inside the lane root; no chousa-lane stray in the fleet root. Severity: none (clean).**

Receipt `receipts/c-scope.txt`.

```
$ git -C .../chousa-shokunin show --stat 4ea9d008
18 files changed, 1698 insertions(+), 1 deletion(-)
   corpus/evidence/round88/{c1-positives.tsv, census-start.txt, claims.md,
     controls/expected.tsv, controls/receipts/*.txt (6), curation-r88-controls.py,
     curation-r88.py, gate-records-r88.py, harm-recheck.py, instrument-pins.txt, mutate-r88.py}
   corpus/knowledge/provenance-recording-r85.md
   plans/round-88.md
exit=0
$ git -C .../chousa-shokunin show --name-only --format= 4ea9d008 | grep -v '^corpus/\|^plans/'
exit=1   ← every path is under corpus/ or plans/
```

Fleet root, for a lane-written stray:

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
 M .ufo/l0-questions.md
?? .scratch/closure-tabi-r83-entry.json
?? .scratch/run15-wrapup/misroot-cff0b4cb/
?? .ufo/reports/round-100/mado.md
exit=0
```

Attribution of each entry (none is a chousa round-88 lane write): `run15-state.json` is the fleet orchestrator's run bookkeeping (it carries the `chousa: round 88` entry the orchestrator writes when it dispatches the round) and `goal-20261103-hyaku-run15.md` is the operator's goal file; `.ufo/l0-questions.md` in its diff adds two `tsukuroi | round-92` lines (a different lane's L1); `.scratch/closure-tabi-r83-entry.json` is tabi-lane round-83 closure; `.ufo/reports/round-100/mado.md` is mado-lane round-100. None of the six is a file the chousa round-88 seat spec or the freeze touches.

**Observation (not chousa-attributable, recorded because it is a fleet-root write).** During the watch window a transient `/home/vgpnk/Projects/shokunin/corpus/` tree appeared at the **fleet** root and was emptied about 23 s later:

```
2026-11-08T04:56:48 ./corpus                                   (dir created)
2026-11-08T04:57:11 ./corpus/lessons                            (emptied)
2026-11-08T04:57:11 ./kagi-shokunin/corpus/lessons              (kagi lane active in the same second)
```

The one file it held was `corpus/lessons/round-64-verifier-spotcheck.md`, whose head read `# Round 64 — verifier spot-check (non-author) … Lane: kagi (secrets & vault ops)`; chousa's own copy of that filename has a different first line and a different digest (`a4eb09e8…` for chousa vs the kagi text in the stray), and no round-88 chousa artifact references `corpus/lessons/round-64` at all (`grep` over `corpus/evidence/round88/` and the wave folder → no hit). So this is a kagi-lane round-64 write that landed outside its own lane root, cleaned up in the same minute — not a chousa round-88 stray, and it left no residue (`git status --porcelain` afterwards shows no `corpus/`).

**F4 — the plan misdescribes the freeze's contents. Severity: medium (provenance; no safety impact).**

`plans/round-88.md:4` states *"The frozen claims are in `corpus/evidence/round88/claims.json` (machine form) and `corpus/evidence/round88/claims.md` (prose)"*, and `plans/round-88.md:74-75` states *"claims.md, `claims.json`, both counters, the control batteries, their receipts, the instrument pins and the egress table are committed together as the freeze"*. Neither file exists for round 88:

```
$ git ls-tree -r --name-only 4ea9d008 -- corpus/evidence/round88/
  (17 names; no claims.json, no egress-approval.md)
$ git log --all --oneline -- corpus/evidence/round88/claims.json     → (empty: never committed)
$ find . -name 'claims.json' -not -path './.git/*' | grep 88            → NO_ROUND88_CLAIMS_JSON
$ ls corpus/evidence/round8*/egress-approval.md
  round81 round82 round83 round84 round85 round86 round87     ← rounds 81–87 each have one; round 88 has none
```

Round-87's own plan uses the same wording and round-87 does ship both files, so the round-88 sentence was carried over unedited. Impact is bounded: the round fetched nothing, so under `SKILL.md:57-59` ("A window without an approval table is loopback-only") **no** egress table was required for round 88 — but the plan asserts one was committed, and a reader auditing the freeze for the promised machine-form claims file and the promised egress table finds neither. Smallest remediation: amend the two sentences in `plans/round-88.md` to name only the files the freeze actually carries (and record that round 88 was a loopback-only window), or land `claims.json` with the freeze. This is a documentation correction, not a claim amendment.

---

## (d) Scratch and host surface of the round's committed tools

**F5 — clean; two low notes. Severity: none (clean).**

Receipt `receipts/d-scratch-host.txt`.

```
$ grep -rn -E '/tmp|tempfile|mktemp' corpus/evidence/round88/*.py
curation-r88-controls.py:25,82   import tempfile; tempfile.mkdtemp(prefix="cur88-", dir=work)
gate-records-r88.py:48,402        import tempfile; tempfile.mkdtemp(prefix="gr88-",  dir=work)
mutate-r88.py:34,94              import tempfile; tempfile.mkdtemp(prefix="mut87-", dir=work)
exit=0
```

There is **no literal `/tmp` path** in any round-88 instrument: every temporary tree is `mkdtemp(dir=work)`, and `work` is an explicit `--work` argument defaulting to `$TMPDIR` → `$HYAKU_SCRATCH` → `/fast/scratch/hyaku` (`gate-records-r88.py:398`, `mutate-r88.py:92`, `curation-r88-controls.py:80`). The frozen counting command in `claims.md` passes `--work "$S"` (a fresh `mktemp -d -p /fast/scratch/hyaku`), so no run can land in `/tmp`.

```
$ grep -rn -E 'sysctl|sudo|systemctl|service |/etc/init|shutdown|reboot' corpus/evidence/round88/*.py
exit=0, no line printed   ← no host sysctl, no sudo, no service control, no reboot path
$ grep -rn -E 'urllib|requests\.|socket|urlopen' corpus/evidence/round88/*.py
exit=0, no line printed   ← no network primitive: no round-88 instrument can perform a GET
$ grep -rn -E '"(commit|add|checkout|reset|update-index|apply|clone|pull|push|fetch)"' corpus/evidence/round88/*.py
exit=0, no line printed   ← no mutating git verb anywhere in the round's instruments
$ grep -rn -E "open\([^)]*['\"][wa]|write_text|mkdir|makedirs|rmtree|shutil\.(copy|move|rmtree)|os\.remove|unlink" tools/gate-records.py
exit=0, no line printed   ← the subject tool has no write operation at all
```

Every child process the round's instruments spawn is either `sys.executable -B <counter>` or a read-only git verb (`git grep`, `git cat-file`, `git rev-parse --git-dir`) — enumerated in `receipts/d-scratch-host.txt`. All writes the instruments perform land under the caller-supplied `--work` (leg receipts in `<work>/legs/`, mutant trees in `<work>/…`), and `curation-r88-controls.py` copies fixtures *out of* `--root` into a temp tree rather than into it. Nothing writes into `--root` or `--repo`.

Low note 1 (concurrency): the default `--work` is the shared `/fast/scratch/hyaku`, and the leg-receipt directory is `<work>/legs/` with fixed per-leg filenames (`gate-records-r88.py:400-402`). Two concurrent runs of the same battery that both fall back to the default would overwrite each other's leg files, and the verdict re-reads those files. The frozen counting command always passes a unique `--work`, so the scored path is safe; only the un-parameterised default is exposed.

Low note 2 (cosmetic provenance): `mutate-r88.py:94` creates its temp tree with prefix `mut87-` — a round-87 label inside a round-88 instrument. Cosmetic only; it affects no digest, no verdict, no path.

I ran nothing that mutates a host sysctl, invoked `sudo`, or restarted a service; no `sudo` was used at any point, and no package transaction was performed (the pacman pause was respected by not installing anything).

---

## (e) Attribution of the freeze commit

**F6 — author and committer are the lane identity. Severity: none (clean).**

Receipt `receipts/e-attribution.txt`.

```
$ git -C .../chousa-shokunin log -1 --format='AUTHOR:%an <%ae>%nCOMMITTER:%cn <%ce>%nDATE:%aI%nCDATE:%cI' 4ea9d008
AUTHOR:chousa-shokunin <chousa@shokunin.local>
COMMITTER:chousa-shokunin <chousa@shokunin.local>
DATE:2026-11-08T04:29:32-03:00
CDATE:2026-11-08T04:47:02-03:00
exit=0
```

Both identities are exactly `chousa-shokunin <chousa@shokunin.local>` as required. Supporting context: `git config user.name/user.email` in the lane repo are the same pair; `git log -1 --format='%H %G? %GS'` returns `N` (unsigned), consistent with every other commit in this lane (`4ea9d008`, `1f29e67b`, `abf7ea58`, `e6e920a4`, `c033577b` are all unsigned and `commit.gpgsign` is unset) — the freeze introduces no new signing anomaly. The freeze's parent is exactly the stated base `f484d94fedec3685a3a052a65bc57cd3eb46b7d7` (`git log -1 --format=%P`), and the base is an ancestor (`git merge-base --is-ancestor` → exit 0), so no unrelated history was folded in. The jj working copy agrees with git: `@` = `17f41143` (empty), parent `klvrplss` = `4ea9d008`. The base commit `f484d94f` is authored by `protocol-shokunin <protocol@shokunin.local>` — the non-author spot-check integrator, as the round shape requires.

---

## F7 (outside the (a)–(e) list — reported because it is a provenance defect): the do-nothing control receipt is the landing output

**Severity: medium.** It does not meet any of C1's four kill rules, and the predicate itself is met at the freeze (below), but the freeze's control set contains a receipt that cannot be what it is labelled. Receipts `receipts/f-donothing-control.txt`, `receipts/g-c1-landing-run.txt`, `receipts/h-expected-mapping.txt`.

What the freeze says. `controls/expected.tsv:2` declares:

```
c1-do-nothing  gate-records-r88.py with --tool = the f484d94f blob of tools/gate-records.py  1  D1_EXPECTED=3 D1_FORGES=3 D2_FORGES=3 MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1  …
```

i.e. that case is expected to **exit 1** (fail). The frozen claims prose says the same thing in prose — `corpus/evidence/round88/claims.md:56-58`: *"**Before (committed controls).** `controls/receipts/c1-k0-donothing.txt`: the round-88 battery pointed at the pre-round-88 tool … plus the round-87 battery, which cannot bind the class to 203 (its derivations accept non-200). Measured at the freeze below."* The receipt is therefore presented as the measurement of the pre-state, and the pre-state is presented as one the round-88 battery does not pass.

What is committed. `corpus/evidence/round88/controls/receipts/c1-k0-donothing.txt` is three lines with no header and no `exit:` line, and the last line is `GATE_RECORDS_R88=PASS`:

```
$ cat -A corpus/evidence/round88/controls/receipts/c1-k0-donothing.txt | cut -c1-90
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/36$
LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15$
GATE_RECORDS_R88=PASS$
$ wc -l … → 3
```

My independent re-run of the *landing* battery at the freeze, and a byte-diff against that receipt:

```
$ python3 -B <tree>/corpus/evidence/round88/gate-records-r88.py --root <tree> --repo <lane> --work <scratch>
TOOL=present POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=362/362 EXPECTED_CODE=362/362 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_DERIVED=1 MUT_ADMIT_KILLED=1 MUT_UNREACH_DERIVED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15
LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15
GATE_RECORDS_R88=PASS
exit=0
$ diff <landing-run> corpus/evidence/round88/controls/receipts/c1-k0-donothing.txt
IDENTICAL (exit=0)      ← receipt g-c1-landing-run.txt vs the committed do-nothing receipt
```

And re-running the *declared* do-nothing instrument also exits 0, because the subject tool is byte-identical to the base:

```
$ git show f484d94f:tools/gate-records.py > work/base-gate-records.py
$ sha256sum work/base-gate-records.py  → 905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60
$ sha256sum tools/gate-records.py       → 905f9da2fdf233b3a599f079a4c40ace730e3acf5464a2b80e1f93a616242d60
$ git diff --stat f484d94f 4ea9d008 -- tools/gate-records.py   → (empty)
$ python3 -B <tree>/corpus/evidence/round88/gate-records-r88.py --root <tree> --repo <lane> --tool work/base-gate-records.py --work <scratch>
… GATE_RECORDS_R88=PASS
exit=0               ← the expected exit 1 is unsatisfiable: the "pre-round-88 tool" IS the landed tool
```

Compare round 87's equivalent, which was satisfiable because round 87 *did* change the tool: `corpus/evidence/round87/controls/receipts/c1-k0-donothing.txt` carries a 4-line header naming the tree, the tool and the command, three `NOT_REFUSED` lines, four `LEG_FAIL` lines, `GATE_RECORDS_R87=FAIL`, and a final `exit: 1`.

Impact. As committed, the do-nothing case is a duplicate of the landing case and demonstrates nothing: a reader cannot tell it from the landing receipt (byte-identical), and the frozen expectation it is filed against (`expected_exit = 1`) is contradicted by the receipt and by an independent re-run. The round's non-vacuity evidence for C1 does survive through the mutants battery — I re-ran `mutate-r88.py` at the freeze and got `MUTANTS_KILLED=6/6 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0 TOTAL=8/8`, byte-identical to the committed `c1-mutants.txt`, including `E1-joint-narrow` and `E4-setup-detached` killed — so the K4 shapes are genuinely covered. Smallest remediation (L1's call, not this seat's): either point the `c1-do-nothing` row at a tool blob that actually predates the round-87 repair (so exit 1 is reachable), or restate that row's expectation as exit 0 with the "do-nothing tool == landed tool" fact recorded, and add the header + `exit:` line to the receipt so the case is distinguishable from the landing run. This is a control-honesty repair; it is not a claim amendment and does not narrow either frozen predicate.

**F7b — `c2-d0-donothing` has no row in `controls/expected.tsv`. Severity: low.** The freeze ships six control receipts but seven expectation rows, and the mapping is not one-to-one: the receipt `controls/receipts/c2-d0-donothing.txt` (the round-87 counter on the round-88 tree printing `CURATION_R87=PASS`, referenced by `claims.md:100-101`) has **no** corresponding row in `controls/expected.tsv` (`grep -c 'c2-do-nothing\|c2-d0' corpus/evidence/round88/controls/expected.tsv` → 0). Every other shipped receipt maps to a row. I re-ran the case and it reproduces byte-identically (`g-c2-r87-on-r88tree-run.txt`), so the measurement itself is sound; the gap is that the independent expectation it should be checked against is absent. Smallest remediation: add the row (`c2-do-nothing | curation-r87.py on the round-88 tree | 0 | CURATION_R87=PASS | round-87 claims.md C2: the prior instrument has no leg of the four new classes`).

---

## Reproductions I ran at the freeze (all read committed bytes; all receipts in `receipts/`)

| Case | Command (abbreviated) | Exit | Observed line | Receipt |
|---|---|---|---|---|
| C1 landing | `gate-records-r88.py --root <tree> --repo <lane> --work <scratch>` | 0 | `GATE_RECORDS_R88=PASS` with `D1_EXPECTED=3 D1_FORGES=3 D1_REFUSED=3/3 D2_FORGES=3 D2_REFUSED=3/3 MUT_ADMIT_KILLED=1 MUT_UNREACH_KILLED=1 DERIVE_NEG=1 LEGS=15/15` / `LEG_REREAD=15/15 RECONCILED=15/15 LEGS_APPENDED=15` | `g-c1-landing-run.txt` |
| C1 mutants | `mutate-r88.py --root <tree> --repo <lane> --work <scratch>` | 0 | `MUTANTS_KILLED=6/6 TOOL_MUTANTS_CAUGHT=2/2 EQUIVALENT_ON_TREE=0/0 TOTAL=8/8` | `g-c1-mutants-run.txt` |
| C1 harm | `harm-recheck.py --root <tree> --repo <lane> --base-tool <f484d94f blob>` | 0 | `HARM_RECHECK files=11 records=28 moved=0 base_rc=0 r88_rc=0` | `g-c1-harm-run.txt` |
| C1 frozen instrument | `gate-records-r87.py --root <tree> --repo <lane> --work <scratch>` | 0 | `GATE_RECORDS_R87=PASS`, no `LEG_REREAD` field, no `D1_WIDTH` pin | `g-c1-k0b-r87-battery-run.txt` |
| C1 do-nothing (declared) | `gate-records-r88.py --tool <f484d94f blob> …` | **0** | `GATE_RECORDS_R88=PASS` — see F7 | `g-c1-donothing-base-tool-run.txt`, `f-donothing-control.txt` |
| C2 landing | `curation-r88.py --root <tree>` | 0 | `CURATION_R88=PASS` with `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20 WARRANT_OK=17/17 TEACHES_CHECKED=1 TEACHES_FLAGGED=1 TEACHES_UNRESOLVED=0 LEGS=7/7` | `g-c2-landing-run.txt` |
| C2 controls | `curation-r88-controls.py --root <tree> --work <scratch>` | 0 | `FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5` / `CONTROLS=PASS` | `g-c2-controls-run.txt` |
| C2 do-nothing | `curation-r87.py --root <tree>` | 0 | `CURATION_R87=PASS` (byte-identical to the committed `c2-d0-donothing.txt`) | `g-c2-r87-on-r88tree-run.txt` |

Every committed control receipt reproduces byte-for-byte at the freeze (`diff` → IDENTICAL for `c1-k0-donothing.txt` vs the landing run, `c1-k0b-frozen-instrument.txt`, `c1-mutants.txt`, `c1-harm.txt`, `c2-controls.txt`, `c2-d0-donothing.txt`), except that `c1-k0-donothing.txt` reproduces as the *landing* run (F7). Two committed receipts have no row in `controls/expected.tsv`: `c2-d0-donothing.txt` (the C2 do-nothing case) and, implicitly, the `c1-k0b-frozen-instrument.txt` ↔ `c1-frozen-instrument` pairing is present — so the gap is `c2-d0-donothing` only. That is a documentation gap of the same kind as F7 and is reported with it.

Instrument integrity: `sha256sum -c` on `corpus/evidence/round88/instrument-pins.txt` → **OK for all 14 pinned paths** (both counters, the three control batteries, `c1-positives.tsv`, the six control receipts, `controls/expected.tsv`, and the subject tool `tools/gate-records.py`), so no pinned byte moved between the freeze and this review.

Mutation check on my own footprint: `git -C <lane> status --porcelain` before and after all my runs is identical (`?? .ufo/waves/round-88/` only) and the fleet-root porcelain gained no entry attributable to this seat. Scratch tree `/fast/scratch/hyaku/chousa-r88/R88SentinelScope/` (380 MB of archives) was deleted before this report was finalised; every receipt cited above is preserved under `.ufo/waves/round-88/w1/R88SentinelScope/receipts/`.

---

VERDICT: R88SentinelScope C1 held — the frozen predicate is met at the freeze (GATE_RECORDS_R88=PASS, exit 0, all required fields) and no egress, credential, scope, host or attribution defect touches it, but the committed `c1-k0-donothing.txt` receipt is the landing output rather than a failing do-nothing run (F7, medium, no kill rule met).
VERDICT: R88SentinelScope C2 held — CURATION_R88=PASS and FORGERY_REFUSED=5/5 R87_ACCEPTED_FORGERY=5/5 reproduce at the freeze with no scope, credential, egress, host or attribution defect against it.
