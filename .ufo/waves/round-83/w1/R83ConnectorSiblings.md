# R83ConnectorSiblings — sibling-overlap scan, round 83

Seat: connector (leaf, read-only over siblings). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin` at
`aca2a781ef2db375881c21bf407e153f786ac61f`; candidate landing `81b81173f19d175e2b2a6b409b2a496d09d0b258`.
Nothing outside this wave folder was written; no sibling file was edited; no tool was installed (tooling
authorization unused). Scratch `/fast/scratch/hyaku/chousa-r83/R83ConnectorSiblings/` was created, used for every
fixture, and removed before this report was written.

Receipts (all under `.ufo/waves/round-83/w1/R83ConnectorSiblings/receipts/`):
`sibling-scan.txt`, `own-tool-15.txt`, `mori-crosscheck-rev-form.txt`, `forged-rev-chousa.txt`,
`forged-rev-mori.txt`, `vacuous-pass.txt`, `kotodama-vacuous-vs-chousa.txt`, `rev-setup-vs-record.txt`,
`git-config-exec-probe.txt`.

## Q1 — does a sibling hold a knowledge entry on appraisal-judgment recording?

**No.** Three sweeps, all negative, all receipted in `sibling-scan.txt`:

| Sweep | Command | Observed |
|---|---|---|
| S1a | `grep -rn 'assessing-risk-bias-included-studies-c52-c60' */corpus/ \| grep -v '^chousa'` | no output, rc 1 |
| S1b | `grep -rn 'handbook/current/chapter-0[78]' */corpus/ \| grep -v '^chousa'` | no output, rc 1 |
| S2 | `grep -rn -i -e 'support for judgement' -e 'signalling questions' -e 'independent duplicate' */corpus/knowledge/ \| grep -v '^chousa'` | no output, rc 1 |

No live sibling `corpus/SOURCES.md` or `corpus/knowledge/*.md` carries any of the three C1 URLs, and no sibling
knowledge entry uses the craft vocabulary. The `-i 'appraisal'` hits in `kotodama-shokunin/corpus/knowledge/`
(`civilizations/igbo.md:16`, `civilizations/mali-songhai.md:190` "Reappraisal", `culture-material/warrior-material-culture.md:73,122`
Edo sword appraisal, `myth-symbol/mineral-stone-symbolism.md:75`) are unrelated senses of the word; none is about
recording a research judgment.

Two **artifact-level** mentions exist, neither in a lane corpus and neither a duplicate:

- `revenger-shokunin/.ufo/waves/kaika-r1/connector.md:117` — imports `S026` (the exact MECIR C52-C60 URL) from
  chousa's own `kaika-w1/chousa-art.md` and states it "grounds Revenger's non-author review gate". Revenger's live
  registry has no row for it (`revenger-shokunin/corpus/SOURCES.md:40` S026 is the lane's saved EVM interface
  records). **Refer-out, not absorb:** revenger's non-author review gate rests on a standard it has not registered;
  chousa now holds the grounded entry, so revenger can cite the entry or register its own row. Do not edit revenger.
- `chousa-shokunin/.ufo/waves/kaika-w1/chousa-art.md:141` — chousa's own staging of the same URL as `S026`
  `queued 2026-10-19 on-revision`. In-lane provenance, not a sibling.

Adjacent craft, different domain, no source overlap — cite as neighbours, never as sources:

- `kotoba-shokunin/corpus/knowledge/harness-independent-round37.md:9` — "a source-blind instrument re-derives the
  expected values … a third driver joins the two check-for-check, and every disagreement is adjudicated here". The
  harness instance of duplicate independent judgment plus a fixed disagreement process.
- `tameshi-shokunin/corpus/knowledge/arm-class-matrix.md:43` — "the disagreement is the finding".
- `lore-shokunin/corpus/knowledge/r103-canon-status-and-supersession.md:96` — "Real-world source appraisal remains
  chousa's province (SKILL.md:7-9)". A sibling already defers this ground to chousa; nothing to absorb.

## Q2 — does a sibling hold a tool that verifies lesson Gate records against committed captures?

**No sibling holds the record class or the binding. Five of the tool's twelve checks already have a sibling
implementation.** Sweeps S3/S4 (`sibling-scan.txt`): no sibling `tools/` or `scripts/` file contains the token
`GATE-RECORD`; none contains `refetch.tsv`; and **no sibling tool reads both `corpus/SOURCES.md` and
`corpus/captures/`** (S4, empty result; re-run recursively over every sibling `tools/` and `scripts/` tree, all
extensions, also empty). The only `capture_sha256` hits are ten lines in four tsukuroi instruments (three health
counters and the pause gate), which record or compare a digest; none verifies a lesson record.

Check-by-check, against the twelve codes in `tools/gate-records.py:1-58`:

| Code | Sibling implementation | Where |
|---|---|---|
| CAPTURE_SHA | yes | `kotodama-shokunin/tools/check-gate-captures.py:1-45` (r97: 64-hex exact, 16-hex prefix); `tsukuroi-shokunin/tools/check-pause-gate.py:10,94` (r24) |
| WORDS | yes | `mori-shokunin/tools/mori-anchor-check.py:14-22` (r72), registered `mori-shokunin/SKILL.md:1326` |
| QUOTE_LEN | yes | `kotodama-shokunin/tools/check-gate-quotes.py:1-40` (r54, 25-word cap on `## Gate` rows) |
| REV | partly | `kama-shokunin/tools/citation-provenance.py:1-20` (r18: rev+path+blob sha256 token), registered `kama-shokunin/SKILL.md:698`; `souji-shokunin/tools/souji-pointer-check.py:1-24` (r70: path existence at rev) |
| LINE | yes | `mori-anchor-check.py` (r72, exact quote on one line of a pinned copy); `check-pause-gate.py` (r24, pointer line + exact substring at a revision) |
| PARSE, REGISTRY, TIER, CAPTURE_PATH, CAPTURE_KEY, REFETCH, QUOTE_ABSENT | no | — |

So the novelty is the **closed record grammar and the binding** — one line → `corpus/SOURCES.md` row + tier +
`refetch.tsv` row (id, url, key, fetched, curl_rc, http, txt_sha256) + capture key `sha256(url)[:24]` + capture
sha prefix + located quote. No sibling binds any record to a registry row and a refetch log. A round sentence
claiming fleet novelty for "verifying located quotes" *as a class* would be false; a sentence claiming the
composition and the non-vacuous exit contract is true.

Two runnable cross-checks, both receipted:

1. **Second implementation agrees on the rev arm.** For each of the four rev-form records of round 80 I extracted
   the blob at its `rev` and ran mori's r72 instrument against it:
   `python3 mori-shokunin/tools/mori-anchor-check.py --pin <blob> --check 'S199|222|12|<quote>'` (and S200, S201,
   S202). Observed in `mori-crosscheck-rev-form.txt`: `anchor item=S199 span=222 verdict=ok located_on=222
   occurrences=1 words_counted=12 words_recorded=12` … `ANCHOR_CHECK: PASS items=1 ok=1`, rc 0, for all four.
   The same four records read `OK` from chousa's tool (`own-tool-15.txt`: `GATE_RECORDS files=3 records=15 ok=15
   fail=0`, rc 0).
2. **Second implementation agrees on two forgeries.** `forged-rev-chousa.txt`: line 223 for S199 →
   `GATE_RECORD …:2 S199 FAIL LINE`; `words=19` for S200 → `…:3 S200 FAIL WORDS`; untouched S201 → `OK`;
   `GATE_RECORDS files=1 records=3 ok=1 fail=2`, rc 1. `forged-rev-mori.txt`: `verdict=mislocated
   located_on=- occurrences=0`, rc 1; `verdict=wordcount_mismatch … words_counted=20 words_recorded=19`, rc 1.
   Same verdicts, independently derived.

**The nearest sibling in record shape is strictly weaker on the exit contract.** `kotodama-shokunin/tools/check-gate-captures.py:44`
(`exit 0 iff 0 findings, 1 iff any finding, 2 on error`) and `check-gate-quotes.py:81` (`0 no findings`) both pass
a lesson that carries no row in *their* grammar. Measured on chousa's own round-82 lesson, which carries five
`GATE-RECORD` lines (`kotodama-vacuous-vs-chousa.txt`):

```
GATE_QUOTES: 0 findings                                              rc=0
GATE-CAPTURES: 0 finding(s) in 0 row(s)                              rc=0
GATE_RECORDS files=1 records=5 ok=5 fail=0                           rc=0   (chousa's tool)
```

Both kotodama instruments report a clean pass over five records they never opened — the vacuous pass chousa's C2
K4 forbids. chousa's tool refuses that input (`vacuous-pass.txt`): an empty file and a prose-only file each print
`GATE_RECORDS files=1 records=0 ok=0 fail=0` and exit 1. This is the one place where the comparison *strengthens*
C2 rather than qualifying it.

## Q3 — province

| Sibling refusal | Does the entry or tool touch it? | Evidence |
|---|---|---|
| kengaku — model-quality / evaluation claims | **No.** The entry's rows are Cochrane risk-of-bias procedure; the Limits keep the RoB domains out, and row 7 is about a checklist or algorithm proposing a judgment, not a model. Its inference maps "proposed judgment" to "a gate's or counter's verdict" — chousa's own instruments. | entry `## Limits` ¶1, `## Inference`; `kengaku-shokunin/PROVINCE.md:3` |
| kasegi — bounty scope / claim packages | **No.** No bounty, program or disclosure object appears in either artifact. | `kasegi-shokunin/PROVINCE.md:3` |
| kumitate — orchestration, multi-agent dispatch, agent lifecycle | **Boundary, not a breach.** Row 1 ("at least two people") is a record rule; nothing in the entry prescribes a roster, a topology or a dispatch. It would breach if read as one. | `kumitate-shokunin/PROVINCE.md:3`; `kumitate-shokunin/corpus/knowledge/multi-agent-coordinator-topologies.md:1-12` owns topology decisions |
| kagi — secret values in any record | **No.** The tool reads captures, the registry and the refetch log; its output is `S<id>` and codes only, never a quote or a capture body. | `kagi-shokunin/PROVINCE.md:3`; `tools/gate-records.py:291-299` |

Recommendation (to L1, not an edit here): one sentence in the entry's Limits that row 1 is a record requirement and
does not specify who is dispatched or how a wave is arranged (kumitate), and that applying it to a model judge is
kengaku's ground. Without it the row is readable as a dispatch rule by a reader who does not hold the PROVINCE map.

## Residuals (out-of-class; listed separately, none is a kill-rule firing)

- **R1 — the rev arm reports a setup condition as a record failure.** With `--root` pointing at a non-git tree and
  `--repo` omitted (the documented default is LANE), a *genuine* record prints a record failure:
  `rev-setup-vs-record.txt` shows `GATE_RECORD …/genuine.md:2 S201 FAIL LINE,REV`, `GATE_RECORDS files=1
  records=1 ok=0 fail=1`, rc 1, while the same record with `--repo <lane>` prints `S201 OK`, rc 0, and
  `git -C <non-git root> rev-parse --git-dir` exits 128. Cause: `tools/gate-records.py:268` (`repo = a.repo or
  root`) with no repository probe; `:240-241` appends `REV` **and** `LINE` whenever `git_blob` returns `None`.
  C2 K3 does not fire — the record is genuine only relative to a valid GITDIR, and the frozen counter and predicate
  (b) both pass a valid one — but the tool cannot tell a caller it could not evaluate. This is the residual the
  proposed move closes.
- **R2 — the rev arm inherits git's ambient configuration.** `tools/gate-records.py:175,179,182` call
  `subprocess.run(["git", "-C", repo, "cat-file", …])` with no `env=`. Siblings and the lane's own precedent scrub
  it: `souji-shokunin/tools/souji-pointer-check.py:43,47,97` (`GIT_CONFIG_NOSYSTEM=1`,
  `GIT_CONFIG_GLOBAL=/dev/null`, `PATH=/usr/bin:/bin`) and `chousa-shokunin/corpus/evidence/round63/git-revision-probe.py:26-31`
  (`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`/`GIT_CONFIG_NOSYSTEM`). **Measured: no execution path via `cat-file`.**
  `git-config-exec-probe.txt`: a fixture repo with repo-local `core.fsmonitor`, then a hostile `GIT_CONFIG_GLOBAL`
  carrying `core.fsmonitor`, `core.pager`, `core.sshCommand` and a `filter.evil` pair — `cat-file -t HEAD^{commit}`
  printed `commit`, rc 0, marker `ABSENT` in all three runs; the control `git status` with the same hostile config
  printed marker `PRESENT`. So this is defence in depth and consistency with the lane's own r63 instrument, not a
  demonstrated harm. Report it, do not inflate it.
- **R3 — S-ids are lane-local.** `sibling-scan.txt` §S5: `S009` is a row in 21 lanes, `S212` and `S213` in 10 each,
  with unrelated content (e.g. `kengaku-shokunin/corpus/SOURCES.md:227` S212 is a Terminal-Bench instruction file).
  The entry's `source: S009, S212, S213` is correct inside chousa and must be qualified (`chousa:S212`) in any
  cross-lane statement. No sibling is wrong here; the namespace is simply per-lane.
- **R4 — revenger's non-author review gate cites an unregistered standard.** `kaika-r1/connector.md:117`, above.
  Refer-out only.

## Proposed move (one, bounded)

**Give the rev arm a could-not-evaluate verdict, taken from the sibling exit maps.** Before treating a rev-form
record's unresolvable blob as a record failure, probe the repository once (`git -C GITDIR rev-parse --git-dir`); if
it fails, print one `GATE_RECORDS_ERROR could-not-evaluate: <repo> is not a git repository` to stderr and return 2,
emitting no per-record `FAIL`. Keep `REV` for a rev that does not resolve *inside* a valid repository. Probe lazily,
on the first rev-form record, so url-only runs against a non-git tree keep working.

- **Axis improved:** C2 operability (capability acquisition). The tool's exit contract becomes honest about what it
  could not evaluate — the distinction `mori-shokunin/SKILL.md:1326` registers as `2 setup`, `souji-pointer-check.py:15`
  as `EXIT=2 could not evaluate`, and chousa's own `research-gate` already draws (`SKILL.md:86`). It is the one
  place where a sibling's registered exit map is strictly better than the landed tool's.
- **Axes not harmed:** C1 untouched (no entry byte). The 15 positives, the 198 derived forgeries, the empty-file arm
  and the counter's `RC=3/3` all run with a valid `--repo` and are unchanged; a forgery whose `rev` does not resolve
  inside a valid repo still fails `REV`. No frozen counter, fixture, receipt or claim is edited.
- **Cost:** about eight lines in `main()` plus one docstring sentence stating the pre-flight (the docstring is the
  K2 contract, so the new condition must be written there, not left implicit).
- **Risk:** a caller who deliberately wants a record-failure verdict from a non-git tree now gets exit 2. That is the
  intended semantics and the sibling convention, but it is a behaviour change and should be disclosed in the round's
  after-receipts, not slipped in.

## Verification

| Check | Command | Receipt | Observed |
|---|---|---|---|
| sibling corpus cites none of the three URLs | S1a/S1b in `sibling-scan.txt` | `sibling-scan.txt` | no output, rc 1, both |
| no sibling craft entry | S2 | `sibling-scan.txt` | no output, rc 1 |
| no sibling `GATE-RECORD` / `refetch.tsv` | S3 | `sibling-scan.txt` | 10 `capture_sha256` lines (4 tsukuroi instruments); no `GATE-RECORD`, no `refetch.tsv` |
| no sibling tool reads registry + captures | S4 | `sibling-scan.txt` | empty |
| chousa's own 15 records | `python3 tools/gate-records.py verify --root . corpus/lessons/round-80.md corpus/lessons/round-81.md corpus/lessons/round-82.md` | `own-tool-15.txt` | `records=15 ok=15 fail=0`, rc 0 |
| mori r72 reproduces the rev arm | `mori-anchor-check.py --pin <blob> --check '<id>\|<line>\|<words>\|<quote>'` ×4 | `mori-crosscheck-rev-form.txt` | `ANCHOR_CHECK: PASS items=1 ok=1` ×4, rc 0 |
| both tools kill the same forgeries | `gate-records.py verify --root <mini> --repo <lane> <forged.md>`; mori ×2 | `forged-rev-chousa.txt`, `forged-rev-mori.txt` | `S199 FAIL LINE`, `S200 FAIL WORDS`, `S201 OK`, rc 1; `mislocated`, `wordcount_mismatch`, rc 1 |
| chousa refuses vacuous input | `gate-records.py verify --root <mini> --repo <lane> <empty.md>` / `<prose.md>` | `vacuous-pass.txt` | `records=0`, rc 1, both |
| kotodama instruments pass vacuously | `check-gate-quotes.py corpus/lessons/round-82.md`; `check-gate-captures.py corpus/lessons/round-82.md corpus/evidence/round82` | `kotodama-vacuous-vs-chousa.txt` | `0 findings` rc 0; `0 finding(s) in 0 row(s)` rc 0 |
| setup vs record failure | `gate-records.py verify --root <non-git>` vs `--repo <lane>` | `rev-setup-vs-record.txt` | `S201 FAIL LINE,REV` rc 1 vs `S201 OK` rc 0; `rev-parse --git-dir` rc 128 |
| git config execution probe | fixture repo + hostile `GIT_CONFIG_GLOBAL` | `git-config-exec-probe.txt` | `cat-file` marker `ABSENT` ×3; control `git status` marker `PRESENT` |

All fixture git calls were made as `git -C "$D" …` with `git -C "$D" rev-parse --show-toplevel` asserted equal to
`$D` before the first mutation; fixtures lived under `/fast/scratch/hyaku/chousa-r83/R83ConnectorSiblings/` and were
removed. No network access was made (no re-open seat item).

VERDICT: R83ConnectorSiblings C1 n/a — no sibling holds, cites or duplicates the appraisal-recording ground; the entry's only cross-lane exposure is a refer-out to revenger's unregistered non-author review standard.
VERDICT: R83ConnectorSiblings C2 held — no sibling verifies `GATE-RECORD` lines or binds a record to registry plus refetch, five of twelve checks have sibling implementations that agree on the rev arm, and the nearest sibling record checker passes vacuously where this tool exits 1; one residual (setup reported as record failure) is proposed for repair.
