# SentinelWriteScope — round 40, write-surface audit

**Assigned attack.** Audit the round-40 spec and committed file paths for any seat
instruction that could write outside its unique lane report, or mutate fleet, sibling,
git-index, jj, or state files.

**Verdict: FAIL — the write boundary is already crossed, and it has already moved the
claim.** One Critical finding outranks the spec audit: a sibling round wrote and then
**committed** production bytes into this checkout during the audit window
(`tools/research-gate.sh`, `corpus/SOURCES.md`, `corpus/README.md`; three commits
04:32:19–04:32:43, tip `6bc90e0` → `a3aac04`). The gate is now committed at
`2cb04bdd…`, so the frozen C1 counter prints `R39_ACTIVE_RECEIPTS=2/6`, exit 1 at the
lane tip, while the same six rows verify `6/6` against the round-40 frozen tip
`6bc90e0`. C1 is true at its own tip and false at the current one; the only variable is
someone else's commit. Separately, the declared report surface is clean (33/33 trailers
unique, lane-anchored, inside `reportDir`; 30/33 items read-only by verb analysis), and
the three write-capable items (the mutation testers) are under-specified in ways that
invite a durable write (W3–W4). No lane production
file, fleet file, sibling repo, `.ufo/state` file, index entry, or jj operation was
changed by this seat — except one self-disclosed index stat-refresh from my own
orientation `git status` (§8).

Axes: **operability** — every finding is reproduced with a runnable command;
**calibration** — the audit separates "the instruction is safe" from "the seat can prove
it is safe", and W4 is a case where the two differ; **depth** — each finding carries a
read-only falsification probe, not a checklist row.

Artifacts audited (all absolute):

- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1-spec.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1-plan.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1-dispatch.json`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/DISPATCH-README.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-40/w1/swarm-registry.json`
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md` (read-only, fleet)
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json` (read-only, fleet)

## 1. What holds (positive half, measured)

Every seat prompt was rendered from `w1-plan.json`; each carries exactly one
`Report: write your scoped findings to <path>` trailer. Resolved against the lane root
per the seat contract:

```text
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 -c '
import json,pathlib,re
lane=pathlib.Path("/home/vgpnk/Projects/shokunin/chousa-shokunin")
tasks=json.load(open(".ufo/waves/round-40/w1-plan.json"))["tasks"]
paths=[re.search(r"Report: write your scoped findings to (\S+)",t["task"]).group(1) for t in tasks]
abs_=[(lane/p).resolve() for p in paths]
print("seats=%d unique=%d" % (len(paths),len(set(paths))))
print("unanchored=%d outside_reportDir=%d" % (
  sum((".." in p or p.startswith("/")) for p in paths),
  sum(a.parent!=(lane/".ufo/waves/round-40/w1") for a in abs_)))'
seats=33 unique=33
unanchored=0 outside_reportDir=0

$ test -d .ufo/waves/round-40/w1 && test -w .ufo/waves/round-40/w1 && echo "reportDir exists and writable"
reportDir exists and writable
```

The check asserted four properties per trailer: no `..`, no leading `/`, resolved
parent equals `<lane>/.ufo/waves/round-40/w1`, and no duplicate across the 33 seats.
All four hold for all 33. `w1-dispatch.json` carries the same `reportDir`
(`.ufo/waves/round-40/w1`) and the same 33 task payloads; the registry
(`w1/swarm-registry.json`) adds no path field, so the trailer is the only write target
any seat is given.

The wave context carries the three bounds the host addendum mandates
(`lane-addendum.md:104-105`: "Seats never mutate the fleet repo, sibling lanes, lane jj
state or lane Git index; put those bounds in every wave context"):

- "Never modify lane production files, the lane git index or jj state,
  `/home/vgpnk/Projects/shokunin/.ufo/state`, the fleet repo, or sibling repos."
- "Every `Report:` trailer path is relative to `/home/vgpnk/Projects/shokunin/chousa-shokunin`
  — write it at `/home/vgpnk/Projects/shokunin/chousa-shokunin/<that path>`."
- "Every seat is a leaf; do not spawn, dispatch, or create background work."

Verb scan over the 33 item texts (the text after `Attack this exact item:` and before
`Lane bounds`), matching `alter|write|copy|create|mkdir|edit|append|delete|remove|restore|stage|commit|install|update|regenerate|repair|fix`:

```text
MutateExpectDigest         ['alter', 'copy']
MutateGateDigest           ['alter', 'copy']
MutateVerifierSubject      ['alter']
SentinelWriteScope         ['write']        # this audit's own item name, not an instruction
<all other 29 items>       []
```

So the entire declared write surface reduces to three items plus the 33 report writes.

The counters and verifier that seats are told to run are read-only against the lane:

- `corpus/evidence/round39/verify-receipts.py` — only `open(path,"rb")` / `open(path,"r")`;
  no `write`, `mkdir`, `git`, or `jj` (grep over the file: three `open(` sites, all reads).
- `corpus/evidence/round40/c1-count.py` — one `subprocess.run` (the verifier), read-only.
- `corpus/evidence/round40/c2-count.py` — two `git -C <lane>` calls, both read-only
  plumbing (`ls-tree`, `ls-files --error-unmatch`); neither refreshes or writes the index.
- No active git hooks (`.git/hooks` contains only `*.sample`); no symlinks anywhere under
  `.ufo/waves/round-40`; `w1/` is `drwxr-xr-x vgpnk:vgpnk`.

**Except the gate itself is not stable.** `tools/research-gate.sh` — the byte-bound subject
of four of the six active receipts — was rewritten and then committed by a sibling round
while this wave read it (W0). Read-only *code* is not read-only *bytes*: the verifier and
both counters are unmodified, but the instrument they bind is not, and its bytes are now
lane history at a tip the round-40 claim never named.

## 2. Findings

| ID | Severity | Surface | One line |
|---|---|---|---|
| W0 | Critical | lane tip | A sibling round committed gate bytes mid-wave (`1bd9001`); C1 reads 2/6 at tip `a3aac04`, 6/6 at the round-40 tip `6bc90e0` |
| W1 | High | `ExecNoHarm` + gate `--pin` | `--pin PATH` truncates any file and exits 0; pinning the gate's own path destroyed a 404 KB gate and reported success |
| W2 | High | 6 executor items | "no subagent dispatch except your single labrat" contradicts "Every seat is a leaf"; the child has no report path and no contract |
| W3 | Medium | 3 mutation items | "temporary copy only" names no root; the required refusal is unreachable without a reseal the item never mentions |
| W4 | Medium | 3 mutation items | "ensure no repository artifact changes" is satisfied by `git status` and false: the mutated bytes survive in `.git` objects |
| W5 | Medium | wave contract | "Never modify the lane git index" is mtime-false for `git status`; and the addendum's own misroot sweep writes the fleet index |
| W6 | Low | wave contract | "Use absolute paths for every other read/write" licenses writes beyond the report; the prohibition list is not closed |
| W7 | Low | `ExecNoHarm` | Its "named ... regression commands" are named nowhere in-round; the only recorded battery writes outside the seat's report |
| W8 | Info | 4 read items | Bare relative read paths resolve at the fleet root; the fleet root already holds stray `*.html`/`*.txt` from prior seats |

### W0 — a concurrent lane round committed production bytes mid-wave and broke C1 at the tip

**Exploit path (observed, not hypothetical).** While 31 read-only seats were auditing this
lane, a sibling round wrote and then **committed** its own production changes into the
same checkout: an 85→92-line block in `tools/research-gate.sh`, two source rows in
`corpus/SOURCES.md`, and a round-41 knowledge row in `corpus/README.md`. The gate is the
byte-bound subject of four of the six active receipts, so the frozen C1 predicate — which
resolves `tools/research-gate.sh` as a *working-tree* path — moved with the commit.
Nothing in the spec prevents this: the wave context forbids *seats* from editing
production, but the lane checkout has no writer isolation, and
`corpus/evidence/round40/claims.md` P1 pins no revision (unlike the round-39 counters,
which pin `BASE39`/`TIP39` commit hashes).

**Evidence, phase 1 — dirty worktree** (captured 04:26–04:28, now historical):

```text
$ git diff --numstat                       # 04:26 capture
36      34      .ufo/waves/round-40/w1/swarm-registry.json   # harness registry, expected
1       0       corpus/README.md                              # + knowledge/capture-path-pin-r41.md row
2       0       corpus/SOURCES.md                             # + S075 mktemp, S076 sed rows
92      2       tools/research-gate.sh                        # + capture-tool pins (round-41 C1)

$ stat -c '%y %s %n' corpus/README.md corpus/SOURCES.md tools/research-gate.sh
2026-10-24 04:27:50 129707 corpus/README.md
2026-10-24 04:25:12 59842  corpus/SOURCES.md
2026-10-24 04:26:28 409022 tools/research-gate.sh

$ sha256sum tools/research-gate.sh ; git show HEAD:tools/research-gate.sh | sha256sum
2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34  tools/research-gate.sh   # 04:28
4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3  -   (HEAD then = 6bc90e0)
```

**Evidence, phase 2 — the writer committed** (captured 04:33):

```text
$ git log -3 --format='%h %ci %s'
a3aac04 2026-10-24 04:32:43 -0300 round-41: scorecard measured claims, routed dispositions, planned r42
1bd9001 2026-10-24 04:32:24 -0300 round-41: pin capture invocation surface (12/12); W04 dispositions (5/5); S075/S076; wave-1 spec prepared
b173b09 2026-10-24 04:32:19 -0300 round-41: freeze C1/C2 claims, scenario counters, do-nothing controls

$ git log --oneline 6bc90e0..HEAD -- tools/research-gate.sh
1bd9001 round-41: pin capture invocation surface (12/12); W04 dispositions (5/5); S075/S076; wave-1 spec prepared

$ git cat-file blob 6bc90e0:tools/research-gate.sh | sha256sum ; git cat-file blob HEAD:tools/research-gate.sh | sha256sum
4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3  -   (round-40 frozen tip)
2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34  -   (current tip a3aac04)

$ python3 corpus/evidence/round40/c1-count.py ; echo "exit=$?"
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c1-after-s39111.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39101.json: fail VERIFY-FAIL: gate-sha256-mismatch
corpus/evidence/round39/receipts/c2-after-s39121.json: fail VERIFY-FAIL: gate-sha256-mismatch
R39_ACTIVE_RECEIPTS=2/6
exit=1
```

Of the three production files only the gate moves a claim: `corpus/SOURCES.md` and
`corpus/README.md` are additive rows that neither counter reads, so C2's four
dispositions and their inputs are unaffected by this writer. The blast radius is C1's
landed-gate rows and any receipt that binds `tools/research-gate.sh`.

**Control — the same six rows at the round-40 frozen tip `6bc90e0`** (every other
argument unchanged, gate bytes from `git cat-file blob 6bc90e0:tools/research-gate.sh`
into `mktemp -d`):

```text
R39_ACTIVE_RECEIPTS_AT_6bc90e0=6/6
```

`6bc90e0`'s gate sha `4253c187…` equals the `gate_sha256` carried by all four
gate-binding receipts. So C1 is **true at the round-40 frozen tip and false at the
current tip**; the only variable is a sibling round's commit.

**The subject is a moving target, not merely dirty.** Five observations inside one wave
window, from five seats:

| Observed (UTC-3) | `tools/research-gate.sh` sha256 | vs tip | size | source |
|---|---|---|---|---|
| ≈04:20 (measurement window) | `4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3` | = `6bc90e0` | 404 197 | `ExecC1Count` (6/6), `RevengerR1History` §2.1 (6/6) |
| 04:23:46 | `77791864e79cf80fbff57e2cca393facb44ca5d00bd2331466b912534f9ce841` | +85/−0 | 408 637 | this seat |
| 04:26:28 | `2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34` | +92/−2 | 409 022 | `ExecC1LandedReceipt` §10, `ReviewReplacementBindings` E9, `RevengerR1History` §8, `CriticC1Predicate` Counterexample 2 — four seats, identical sha |
| 04:28:10 | `2cb04bdd…` (unchanged) | +92/−2 | 409 022 | this seat, re-measured; `c1-count.py` → 2/6, exit 1 |
| 04:32:24 | `2cb04bdd…` **committed** in `1bd9001` | new tip `a3aac04` | 409 022 | this seat, `git cat-file blob HEAD:…`; `c1-count.py` → 2/6, exit 1 |

Five seats independently converge on the intermediate sha, and the final row is the one
that matters: the worktree dirt became lane history at 04:32:24, inside the audit window.
The 6/6 and 2/6 results are both correct measurements of *different revisions*, which is
precisely the defect: the frozen predicate resolves a path, not a revision.

The tip advanced once more while this report was being written (`d720b1d`, "round-41:
lesson addendum — r40 counter revision scope routed to r42"). The gate is unchanged at
`2cb04bdd…` between `a3aac04` and `d720b1d`, so the at-tip 2/6 stands; the moving tip is
itself the hazard, not a correction of it. The sibling round has already routed the
revision-scope item to r42, which is the right disposition — it does not retroactively
make P1 revision-stable.

`ExecC1Count` measured 6/6 at ≈04:20 against `4253c187…` and its own V7 negative control
(append bytes to a copied gate) reproduced exactly `2/6, exit 1` with four
`gate-sha256-mismatch` refusals — the same signature as the live run, which classifies
the live 2/6 as the gate's **designed fail-closed refusal**, not a manifest or receipt
regression. `RevengerR1History` confirms all four gate-gated active receipts carry
`pre == post == 4253c187…`, so the receipts are internally consistent and only the
subject moved.

Scope precision, per `ReviewReplacementBindings`: of the three round-40 *replacement*
receipts only `c1-after-s39011-regenerated.json` binds `tools/research-gate.sh`; the other
two bind the frozen r39 control gates (`0447ad14…` base, `e1251030…` mutant) and still
verify `ok`. The four failing rows in the 2/6 are the landed-gate replacement, the r39
landed-gate receipt, and the two c2 receipts — four of the six *active* rows, which is
what the sentence above claims.

**Impact.** Three consequences, in order of blast radius:

1. **C1 is now false at the lane tip, by someone else's commit.** The round-40 report
   cannot cite 6/6 without pinning `6bc90e0`; at `a3aac04` the frozen predicate reads
   2/6, exit 1. Any successor round that re-runs `c1-count.py` inherits a broken claim
   it did not break.
2. **Scope boundary, not a regression — and that is the trap.** The four gate-binding
   receipts correctly refuse `2cb04bdd…`: they were frozen against the round-40 tree, so
   a later gate commit *must* produce `gate-sha256-mismatch` by design
   (`ExecC1Count`, V7 control reproduced the identical 2/6 signature from a byte change
   alone). Re-binding them to a round-41 gate would be a **new claim**, not a repair. The
   defect is therefore not the receipts but the predicate text: P1 names a path where it
   needed a revision, so the citation silently changes subject when someone else commits.
3. **Policy violation.** `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:100-104`
   requires "Every concurrent writer needs an actual separate worktree, unique
   branch/path and observed base ... Never run concurrent writers on one checkout."

**Smallest remediation.** Three independent, cheap guards:

- In the counters, resolve the gate bytes from a pinned revision rather than the
  working tree (`git show <rev>:tools/research-gate.sh` into `mktemp -d`), or add a
  precondition line: `git -C <lane> diff --quiet -- tools/research-gate.sh` else print
  `R39_RECEIPT_ENV=dirty-gate` and exit 2. A dirty-subject refusal is honest; a 2/6 that
  looks like a claim failure is not. **Sharper root cause** (`CriticC1Control` F4,
  independently verified): the manifest's `gate` column names a *live path*, so
  `c1-count.py` hashes whatever is there now while each receipt carries a pinned digest.
  The durable fix is snapshot-gated manifest rows — a `rev:path` gate column, or a
  counter that materialises `git cat-file blob <rev>:<path>` into `mktemp -d` before
  calling the verifier. **Caveat, measured by `ExecNoHarm`:** a bare
  `mktemp -d` extract is enough for counter/verifier re-derivation (the verifier only
  hashes bytes), but a *selftest* re-proof of committed bytes must sit in a lane-shaped
  root. From `/tmp/r40-noharm` the HEAD extract false-failed 2/275
  (`claims-lane-fallback`, `ptr-lane-abs`) because the gate derives
  `LANE_ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)` (`tools/research-gate.sh:313`) and those
  cases resolve `PROVINCE.md` from it; the same bytes at
  `<tmp>/mirror/tools/research-gate.sh` plus `git show HEAD:PROVINCE.md` at
  `<tmp>/mirror/PROVINCE.md` give `PASS (275 cases, 0 skipped)`, exit 0, stderr 0. A
  remediation that ignores this trades a false C1 failure for a false selftest failure.
- In the wave spec: forbid concurrent production work in the lane checkout for the
  wave's duration, or move the round-41 write work to its own worktree (policy already
  says this).
- In every seat report that cites a 6/6 or 2/6: record the gate sha and the observation
  timestamp (this report does: 04:26, `77791864…` live / `4253c187…` HEAD).

Do **not** restore the gate with `git checkout` — that destroys the concurrent writer's
work and, per W4, leaves the discarded bytes in the object store.

### W1 — `--pin PATH` is an unguarded truncation primitive, reachable from the no-harm seat

**Exploit path.** `ExecNoHarm` is told to run "the committed research-gate selftest and
the named r1 archive, claims, chain, and integrity regression commands". No round-40
artifact names those commands (W7). The gate's own usage block exposes `--pin PATH`, whose
semantics are "writes a behavioral baseline text file to PATH" (`tools/research-gate.sh:227`).
`run_pin` writes with a single `printf '%s' "$text" >"$path"` (`:4219`) — truncating,
arbitrary path, no refusal when `PATH` is the gate itself or any tracked file. A seat
that reaches for `--pin` to prove "no drift / no harm" can therefore overwrite any file it
can name, and the script prints `GATE_PIN: ok`.

**Evidence** (on a `/tmp` copy; lane untouched — the copy hashed `4253c187…`, i.e. the
`HEAD` gate bytes, because this probe ran before the W0 edit landed):

```text
$ cp tools/research-gate.sh "$T/g.sh"; printf 'IMPORTANT ORIGINAL CONTENT\n' > "$T/victim.txt"
$ bash "$T/g.sh" --pin "$T/victim.txt"; echo "pin exit=$?"
pin exit=0
victim after line1: # chousa-gate drift baseline v1 — written by research-gate.sh --pin
victim size: 2989

$ S1=$(sha256sum "$T/g.sh" | cut -d' ' -f1)
$ bash "$T/g.sh" --pin "$T/g.sh"; echo "self-pin exit=$?"
self-pin exit=0
gate sha before=4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3
gate sha after =09755fe0fbb8c7583b773a63e279972f5514303f130633246f24db35bf59541a
gate size after: 2989
# chousa-gate drift baseline v1 — written by research-gate.sh --pin
```

The 404 197-byte gate became a 2 989-byte baseline, exit 0, no warning. The write happens
after the canonical capture, so the success path is fully reachable.

**Impact.** A read-only seat can destroy `tools/research-gate.sh` (or any evidence,
scorecard, or receipt) and report success. Every downstream counter (`c1-count.py`,
`c2-count.py`, the r39 verifier's `gate_sha256` binding) then breaks, and the mutation is
invisible in the seat's own output because `--pin` prints `ok` and exits 0.

**Smallest remediation.** In `run_pin`, refuse `PATH` that resolves to `$SELF` or to a
tracked path under the repo root; require a non-existent target (or an explicit
`--force`). Two conditions, ~4 lines, and it belongs at
`tools/research-gate.sh:4206` next to the existing "baseline not written" guard.

### W2 — six executor items grant a spawn the wave contract forbids, with no bound on the child

**Exploit path.** Every executor payload carries
`Lane bounds: leaf member — no subagent dispatch except your single labrat.` while the
same prompt's shared context carries `Every seat is a leaf; do not spawn, dispatch, or
create background work.` The host addendum's actual grant is narrower and safe:
"an executor seat may spawn one **read-only** `labrat` probe for a falsifiable
hypothesis" (`lane-addendum.md:107-109`). The round-40 item text drops `read-only` and the
contract drops the permission — so the only remaining text is "no subagent dispatch
except your single labrat", i.e. a permission with no adjective.

A spawned labrat receives no `Report:` trailer, no seat contract, no axes, and starts at
the documented seat cwd — the fleet root (§W8). It is absent from the 33-member registry,
so it is invisible to the wave's evidence census. Six such children are authorised.

**Evidence.**

```text
$ python3 - <<'EOF'  # print the Lane bounds line per task
ExecC1BaseReceipt        | Lane bounds: leaf member — no subagent dispatch except your single labrat.
ExecC1LandedReceipt      | Lane bounds: leaf member — no subagent dispatch except your single labrat.
ExecC1MutantReceipt      | Lane bounds: leaf member — no subagent dispatch except your single labrat.
ExecC1Count              | Lane bounds: leaf member — no subagent dispatch except your single labrat.
ExecC2Count              | Lane bounds: leaf member — no subagent dispatch except your single labrat.
ExecNoHarm               | Lane bounds: leaf member — no subagent dispatch except your single labrat.
<27 non-executor seats>  | Lane bounds: leaf member — no subagent dispatch.
```

**Impact.** Up to six unregistered writers with lane write access and no reporting
obligation, inside a wave whose milestone is "no production edits". Nothing in the wave
can detect their output.

**Smallest remediation.** Delete the clause from the six executor items (the wave is
read-only; nothing here needs a probe). If the grant is wanted, restore the host wording
verbatim and add: "the labrat writes nothing; it returns text to you".

### W3 — "temporary copy only" names no root, and the required refusal needs a reseal

**Exploit path.** Three items are the only ones that order a file alteration:

- `MutateExpectDigest`: "On a temporary copy only, alter one active receipt
  expect_sha256 and re-run the committed verifier; record exact refusal and ensure no
  repository artifact changes."
- `MutateGateDigest`: "On a temporary copy only, alter an active receipt gate digest
  while keeping the gate unchanged; re-run the verifier and require the named mismatch
  refusal."
- `MutateVerifierSubject`: "On temporary copies only, alter a c2 receipt
  verifier_sha256 and subject_counter_sha256 independently; require the verifier's named
  refusals for each mutation."

No item names a temp root, requires `mktemp -d`, or forbids `git`/`jj`. The seat's cwd is
the fleet root (`lane-addendum.md:110-112`, with four recorded incidents: "observed hyaku
phase 1: kama r11, tsukuroi r12, tabi r15, mado r16"). A relative "temporary copy"
therefore lands in the **fleet repo** — the one repo the contract calls read-only.

Separately, the literal single-field alteration cannot produce "the named mismatch
refusal". The receipt is self-sealed and the verifier checks the seal before any binding
(`verify-receipts.py:139` `receipt-self-digest`). Measured:

```text
# W=$(mktemp -d /tmp/mutprobe.XXXXXX); receipts copied into $W, then altered
$ V=corpus/evidence/round39/verify-receipts.py
$ G=tools/research-gate.sh
$ C1=corpus/evidence/round39/c1-count.py
$ C2=corpus/evidence/round39/c2-count.py
$ E=corpus/evidence/round39/expectations.jsonl

$ python3 $V --receipt $W/A1-unresealed.json --gate $G --counter $C1 --expectations $E
VERIFY-FAIL: receipt-self-digest
exit=1

$ python3 $V --receipt $W/A2-resealed.json --gate $G --counter $C1 --expectations $E
VERIFY-FAIL: expect-sha256-mismatch
exit=1

$ python3 $V --receipt $W/B1-verifier.json --gate $G --counter $C2 --expectations $E
VERIFY-FAIL: verifier-sha256-mismatch
exit=1

$ python3 $V --receipt $W/B2-subject.json --gate $G --counter $C2 --expectations $E
VERIFY-FAIL: subject-counter-sha256-mismatch
exit=1

$ python3 $V --receipt corpus/evidence/round39/receipts/c2-after-s39101.json \
    --gate $G --counter $C2 --expectations $E
VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
exit=0
```

`A1` alters `expect_sha256` only; `A2` is `A1` with `receipt_sha256` recomputed over the
body; `B1`/`B2` alter `verifier_sha256` / `subject_counter_sha256` and reseal. Both /tmp
paths work: the verifier takes `--receipt/--gate/--counter` as plain paths, and its
`verifier_sha256` check hashes `os.path.abspath(__file__)` — so a byte-identical copy of
the verifier would still pass that check `[INFERENCE: derived from
verify-receipts.py:243; not executed on a copied verifier]`. Nothing is needed from the
lane worktree beyond read access, so the item is **operable** without touching the lane —
but a seat that follows the text literally hits `receipt-self-digest`, is told to
"require the named mismatch refusal", and must invent the reseal. The nearest repairs are
(a) reseal the copy — correct and unstated, or (b) mutate in place and restore — the
boundary crossing of W4.

**Impact.** The instruction set routes a seat's only authorised write through an
undefined path while its cwd is a read-only repo; and it asks for an outcome the stated
operation cannot produce, inviting improvisation in exactly the seats with write verbs.

**Smallest remediation.** Append to each item: "Copy the receipt to
`$(mktemp -d /tmp/mut-XXXXXX)/`; write nowhere else; no `git`, `jj`, or `cp` into any
repo. To reach a binding refusal, recompute `receipt_sha256` over the body
(`json.dumps({k:v for k,v in r.items() if k != 'receipt_sha256'}, indent=2, sort_keys=True)`),
or the verifier refuses `receipt-self-digest` first."

### W4 — "ensure no repository artifact changes" is satisfiable and false

**Exploit path.** W3's fallback (b) — alter the live receipt, run the verifier, then
`git checkout -- <receipt>` — leaves the worktree clean, so `git status` reports no
change and the seat can truthfully write "no repository artifact changes". The mutated
bytes nevertheless remain in the shared `.git` object store, and in a jj-colocated
worktree the mutation is also snapshotted into jj's op log/evolog. The lane is
jj-colocated with a git backend (`.jj/` 16 M, `.git/` 107 M, jj 0.45.1), so `.git` is the
lane's VCS state, not scratch.

**Evidence** (minimal colocated repo in `/tmp`, same jj version):

```text
# mutate a tracked file, snapshot with jj, then restore with git
$ printf '{"expect_sha256":"BBB"}\n' > corpus/r.json; jj st
$ jj evolog -r @ | head -4
@  ruukttyz t@e 2026-10-24 04:21:21 450619f5
│  (no description set)
│  -- operation a6dd843b8bff snapshot working copy
○  ruukttyz/1 ... (hidden)

$ git checkout -- corpus/r.json; cat corpus/r.json
{"expect_sha256":"AAA"}                 # worktree clean, git status clean

$ git cat-file --batch-all-objects --batch-check | ... | grep BBB
git blob 503deb87b3b95fadc9217dfa24233c346f712560 contains BBB
```

The restore is cosmetic: the mutated receipt body survives as a durable blob in the shared
object store, reachable through the jj snapshot commit. A seat's clean `git status` is
therefore not evidence for the item's acceptance criterion.

**Impact.** A mutation seat can assert a property its own suggested check cannot
establish, and the lane keeps the mutated bytes. If a later `jj` command or the lane
commit helper snapshots the worktree, the residue enters history. The round-40 report
could then cite "no repository artifact changes" while the object store says otherwise —
a fabricated-readiness class defect, not a style issue.

**Smallest remediation.** Restate the acceptance as the positive form the /tmp path
already supports: "No `git` or `jj` command is run. Proof:
`git -C <lane> diff --shortstat` empty *and* the receipt file's sha256 equal to its
pre-run value", and drop "ensure no repository artifact changes" from the item.

### W5 — the index rule is unenforceable at mtime level, and the mandated sweep breaks it

**Exploit path.** The contract says "Never modify ... the lane git index". `git status`
writes the index whenever it refreshes stat data — so any seat that inspects the tree can
"modify the index" with a read-intent command. Conversely, an in-place mutation plus
`git checkout` leaves the index *content* identical while the object store changes (W4).
Enforcing the clause at either level (mtime or `git status`) is therefore wrong in one
direction. The same defect exists in the L1 remediation the addendum prescribes:
"**Misroot sweep before the report:** run `git -C {{FLEET_ROOT}} status --porcelain`"
(`lane-addendum.md:126`) — a command that writes the fleet index of the one repo the
contract calls read-only.

**Evidence** (throwaway repo):

```text
$ git add f; git commit -qm one
$ S1=$(sha256sum .git/index|cut -d' ' -f1); M1=$(stat -c %Y .git/index)
$ sleep 1.1; git status --short >/dev/null
$ S2=$(sha256sum .git/index|cut -d' ' -f1); M2=$(stat -c %Y .git/index)
index sha before=a1e5242cd9b69d7b626edd3707443952e96b67957a986e81d8c5828b37b86222 after=a1e5242c...b86222
mtime before=1792826450 after=1792826451
```

Content identical, file rewritten. Lane observation consistent with this: `.git/index`
mtime `2026-10-24 04:19:59` matches my own orientation `git status --short` (self-disclosure
in §9), and `git diff --stat` shows only the pre-existing
`.ufo/waves/round-40/w1/swarm-registry.json` modification.

**Impact.** Two failure modes: (i) a seat is accused of a boundary violation for running
`git status`; (ii) a seat's in-place mutation passes an index-only check. Both make the
wave's own audit statements unreliable.

**Smallest remediation.** Replace the mtime reading with content: "index entries
unchanged — `git -C <lane> ls-files -s` byte-identical before/after". For the misroot
sweep, use `git -C {{FLEET_ROOT}} ls-files --others --exclude-standard -- .`, which lists
untracked root files without touching the index (this audit used it for §8 for exactly
that reason).

### W6 — the contract's write clause is open-ended, and the prohibition list is not closed

**Exploit path.** The third contract bullet reads: "Every `Report:` trailer path is
relative to ... — write it at `<lane>/<that path>`. Use absolute paths for **every other
read/write**." Read literally, the only constrained write is the report; all other writes
are merely required to be absolute. The prohibition bullet then enumerates lane production
files, the git index, jj state, `/home/vgpnk/Projects/shokunin/.ufo/state`, the fleet repo,
and sibling repos — but not `~/.omp/` (agent config, history, registry), not the lane's
`.ufo/plans/`, `.ufo/reports/`, `.ufo/continuations/`, and not the host tool directories
that the next bullet explicitly authorises ("any agent may install or update a tool",
writes to `~/.local/bin`, `~/.local/share/uv`, npm/cargo prefixes). Under the milestone
"no production edits", the largest granted write surface is therefore the host's tool
tree, and the report is optional for it ("record ... in the report" is an honour-system
obligation, not a checked one).

**Impact.** Scratch writes anywhere absolute are contract-compliant; a seat that writes
`.ufo/continuations/` or `~/.omp/` leaves state that no audit line covers. In a
jj-colocated lane, the *next* `jj` command snapshots every new untracked file, so litter
becomes lane history without any seat committing anything.

**Smallest remediation.** Make the clause exclusive and closed: "Writes: the report
trailer path, `$(mktemp -d)` scratch, and nothing else. Tool installs are the only
exception and must appear in the report with version and channel." Add
`~/.omp/`, `.ufo/plans/`, `.ufo/reports/`, `.ufo/continuations/` to the prohibition list.

### W7 — `ExecNoHarm`'s command set is unnamed in-round, and the only recorded naming writes

**Exploit path.** The item says "the **named** r1 archive, claims, chain, and integrity
regression commands". Nothing in round 40 names them: `corpus/evidence/round40/claims.md`,
`corpus/lessons/round-40.md` and the spec name no command set. The only resolvable naming
is the round-36 battery at `.ufo/waves/round-36/w1/SentNoHarm.md` (cited by
`corpus/lessons/round-37.md:30` as "the recorded battery commands live in `w1/SentNoHarm.md`
(round 36) lines 22–25"). That battery is read-only except for its last two steps:

```text
7. mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/SentNoHarm \
            /tmp/hyaku/chousa-r36/w1/SentNoHarm
8. sha256sum .ufo/waves/round-36/w1/SentNoHarm/no-harm-receipt.txt
```

A round-40 seat replaying "the named commands" writes a directory and a receipt outside
its own report — `mkdir` under a *prior* wave directory, and a file under `/tmp/hyaku`
(named in step 8, created in step 7 by prior practice). The same lesson records the other
failure: `corpus/lessons/round-37.md:30` documents a seat running the battery with
`--root .` instead of `--root ..`, refusing every source and reporting "Harm" on six rows.

**Impact.** The single seat charged with proving no mode was harmed is the one with the
least specified instruction; its plausible replays either write outside its report or
produce false harm reports that the L1 must catch.

**Smallest remediation.** Inline the six commands in the item with `--root ..`, the
cwd, and `timeout 900s`, and add "no `mkdir`, no receipt file: report the outputs
inline".

### W8 — bare relative read paths resolve at the fleet root; the hazard is already live

**Exploit path.** Items name `corpus/knowledge/*.md` (`ReviewR3Counts`),
`active-r39-receipts.tsv` (`ReviewActivePopulation`), and `w1-spec.json and w1-plan.json`
(`ReviewR4RoleMix` — also ambiguous between round 39 and round 40). With seat cwd at the
fleet root, these resolve outside the lane. `w1-spec.json` in particular is
`UFO_PROJECT_ROOT`-dependent and the item does not say *which round's*.

**Evidence.** The class is not hypothetical; the fleet root currently holds untracked
seat-style scratch:

```text
$ git -C /home/vgpnk/Projects/shokunin ls-files --others --exclude-standard -- .
.omp/mcp.json
.ufo/reports/round-31/mado.md
.ufo/reports/round-47/kake.md
.ufo/state/kotoba.report-baseline
AGENTS.md
bm.json
live.html
live_s228.html
nama.html
s395.txt
tf_bavelas.html
```

`live.html` (57 113 B, 2026-10-23), `nama.html` (68 855 B, 2026-10-22) and
`tf_bavelas.html` are fetched HTML pages; `s395.txt` is 0 bytes. These are the
fetch/scratch output class landing at the fleet root — the exact residue the addendum's
misroot sweep exists to clean.

**Impact.** Wrong-tree reads produce false misses (the gate's r39 lesson already has one
such incident); fleet-root scratch is a write into the read-only repo. Round 40 adds 33
more seats with the same cwd.

**Smallest remediation.** Prefix every path in every item with
`/home/vgpnk/Projects/shokunin/chousa-shokunin/` (the addendum already requires this:
"the wave `context` and every item must name absolute paths under {{LANE_CWD}}").

## 3. Cross-checks that found nothing

- **Report trailers** — 33 unique, all under `reportDir`, none with `..` or an absolute
  target; the validator's lane-relative rendering is disambiguated by the contract
  sentence.
- **Counters/verifier** — no write call, no `git add/commit/checkout`, no `jj`.
- **Hooks/symlinks/permissions** — no active hooks, no symlinks under the wave dir,
  `w1/` owner-writable only.
- **Registry** — `w1/swarm-registry.json` is tracked and modified (36 insertions, 34
  deletions vs HEAD) by the orchestrator, not by a seat; it carries no path fields, so a
  seat cannot be pointed at it. This is harness state, correctly inside the lane.
- **Round-39 inputs** — `.ufo/waves/round-39/w1-spec.json` and `w1-plan.json` are tracked
  and clean; the R4 predicate reads committed bytes, so no seat write can move them
  without a visible diff.
- **`c2-count.py` fleet read** — `FLEET/.ufo/reports/round-39/chousa.md` is a cross-repo
  *read*; read-only, and the fleet path is inside the enumerated prohibition, so a seat
  cannot rewrite the evidence this counter cites.

## 4. Pointer for siblings (not this surface)

- `ReviewC2Bindings` / `RevengerR1History`: `corpus/evidence/round39/receipts/c2-after-s39101.json`
  binds `subject_counter = .../round39/c1-count.py` (a **c1** counter) while its family
  key is `c2` (from `c2-count.py` by basename). The verifier accepts it because it only
  compares bytes. Whether a c2 receipt should bind the c1 counter is a binding question,
  not a write-scope one.
- `SentinelFetchScope`: the fetched `*.html` at the fleet root (§W8) and the
  `ScoutHashSource` item's live `docs.python.org` re-open are that seat's surface.

## 5. Repair order (smallest first)

0. **W0 first, because it is live:** the sibling commit is already in lane history, so
   the counter must pin a revision (`git cat-file blob <rev>:tools/research-gate.sh`
   into `mktemp -d`) or refuse a subject that differs from the round's frozen tip
   (`git diff --quiet 6bc90e0 -- tools/research-gate.sh || exit 2` with
   `R39_RECEIPT_ENV=subject-moved`). The round-40 report must then cite C1 as
   `6bc90e0`-scoped, and the gate-binding receipts need reissue against `2cb04bdd…`
   (R1 repair re-opened) unless the gate change's owner reverts it. For a selftest
   re-proof, put the extract in a lane-shaped root with `PROVINCE.md` beside it, or
   cases 106/132 false-fail (`ExecNoHarm`, measured).
1. `run_pin`: refuse `PATH == $SELF` and tracked paths (~4 lines) — closes W1.
2. Delete the labrat clause from the 6 executor items — closes W2.
3. Add the `mktemp -d` root + reseal note + "no git/jj" to the 3 mutation items — closes
   W3 and makes W4 unreachable.
4. Replace W4's acceptance with a sha256-before/after assertion.
5. Replace the index rule with `git ls-files -s` equality (contract + misroot sweep).
6. Inline `ExecNoHarm`'s battery with `--root ..` and cwd.
7. Prefix all item paths with the absolute lane root.

## 6. Tooling record

No tool installed or updated. No pacman transaction attempted (host-wide pause
respected). Nothing fetched from the network; all probes ran against local bytes and
`/tmp` copies. The jj/git/index probes used throwaway repositories under
`/tmp/` (`mktemp -d`), each removed at the end of its command.

## 7. Resolvable artifact pointers

| Claim | Pointer |
|---|---|
| W0 production bytes committed mid-wave | `git log -3 --format='%h %ci %s'` → `b173b09`/`1bd9001`/`a3aac04` (04:32:19–04:32:43); `git log --oneline 6bc90e0..HEAD -- tools/research-gate.sh` → `1bd9001`; tip moved `6bc90e0` → `a3aac04` |
| W0 C1 is revision-scoped | `python3 corpus/evidence/round40/c1-count.py` → `R39_ACTIVE_RECEIPTS=2/6`, exit 1 at tip; six-row loop with `git cat-file blob 6bc90e0:tools/research-gate.sh` in `mktemp -d` → `R39_ACTIVE_RECEIPTS_AT_6bc90e0=6/6` |
| W0 gate byte identity | `6bc90e0` gate `4253c187…` (the four gate-binding receipts' `gate_sha256`); tip gate `2cb04bdd…` (409 022 B, committed in `1bd9001`) |
| 33 unique anchored trailers | `.ufo/waves/round-40/w1-plan.json` (`tasks[].task` trailers); `w1-dispatch.json` (`registry.reportDir`) |
| contract text quoted in §1, §W6 | `.ufo/waves/round-40/w1-plan.json` → `context` (the `# Seat contract` block) |
| `--pin` truncation, exit 0 | `tools/research-gate.sh:4194-4226` (`run_pin`), `:227`, `:685` (usage semantics) |
| `receipt-self-digest` precedes every binding | `corpus/evidence/round39/verify-receipts.py:139` |
| mutation probe outputs (§W3) | reproduced in this report from `/tmp/mutprobe.*`; inputs are the committed receipts in `corpus/evidence/round40/receipts/` and `corpus/evidence/round39/receipts/` |
| round-36 battery incl. mkdir/receipt steps | `.ufo/waves/round-36/w1/SentNoHarm.md:22-25` (commands 7–8) |
| r37 battery-root incident | `corpus/lessons/round-37.md:30` |
| host bounds + labrat + absolute-path rule | `/home/vgpnk/Projects/shokunin/scripts/hyaku/lane-addendum.md:104-128` |
| fleet-root stray scratch | `git -C /home/vgpnk/Projects/shokunin ls-files --others --exclude-standard -- .` |
| colocated jj state | `.jj/` (`repo/`, `working_copy/`) + `.git/` in the lane root; `jj 0.45.1` |

## 8. Self-disclosure

My orientation command was `git status --short` in the lane at `2026-10-24T04:19:5x`,
which per §W5 can rewrite `.git/index` stat data. Content is unchanged (nothing staged,
nothing committed by me; the three round-41 commits are `b173b09`/`1bd9001`/`a3aac04`
from the sibling round, not this seat). For the fleet repo I deliberately used
`git ls-files --others` instead of `git status` to avoid the same write, and I ran no
`jj` command in the lane (a `jj` invocation would snapshot 31 sibling reports into jj
state).

One further index-touching call is disclosed: a single `git status --porcelain` at 04:33,
run to establish whether the W0 edits had been committed. It wrote only index stat data;
`git rev-list`/`git cat-file`/`git ls-files` calls are read-only.

Three read-only executions are recorded for completeness:
`python3 corpus/evidence/round40/c1-count.py` three times (≈04:26, 04:28:10Z, 04:33; each
runs the committed verifier six times and writes nothing), and two six-row verifier loops
against `mktemp -d` copies of the gate — one from `HEAD` when `HEAD` was `6bc90e0`, one
from `6bc90e0` after the tip moved (§W0 control). Neither loop wrote a lane file; both
copies were created and removed under `/tmp`.

No lane production file, fleet file, sibling repo, `.ufo/state` file, index entry, or jj
operation was changed by this seat. The only file written is this report.

Lane bounds observed: leaf member, no dispatch, no background work.
