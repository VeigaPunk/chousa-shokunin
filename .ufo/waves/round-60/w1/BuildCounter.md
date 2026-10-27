# BuildCounter — round-60 C1/C2 counters: build readiness and operand integrity

**Seat.** BuildCounter (leaf, read-only analysis; no spawn, no fetch, no install, no git/jj mutation).
**Scope.** The two counters the frozen round-60 claims name —
`corpus/evidence/round60/c1-count.py` and `corpus/evidence/round60/c2-count.py` — analysed against
`corpus/evidence/round60-claims.md`, prior committed evidence (`round58/`, `.ufo/waves/round-59/w1/`),
and current source (`tools/build-spans.py`). Every run below is in scratch; the only lane write is
this file.
**Assignment path.** `/fast/scratch/hyaku/chousa-r60/BuildCounter` (created, used, removed before
yield — see *Scratch disposition*).

---

## 1. Inputs pinned this seat

```
$ sha256sum corpus/evidence/round60-claims.md corpus/evidence/round60/c1-count.py \
            corpus/evidence/round60/c2-count.py tools/build-spans.py \
            corpus/evidence/round58/controls/build-spans-r55.py \
            corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw .ufo/waves/round-60/s101-open.txt
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7  corpus/evidence/round60/c1-count.py
a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe  corpus/evidence/round60/c2-count.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  corpus/evidence/round58/controls/build-spans-r55.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  (same file, both paths)
6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3  corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  .ufo/waves/round-60/s101-open.txt
```

Lane state at seat start: branch tip `b379919`; the three round-60 artifacts are untracked
(`git status --porcelain` → `?? .ufo/waves/round-60/`, `?? corpus/evidence/round60-claims.md`,
`?? corpus/evidence/round60/`), mtimes 17:51:18 / 17:51:38 / 17:52:14.

**F1 — freeze-integrity mismatch (engine finding, not resolvable by this seat).**
The seat spec names `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440` as the
immutable claim SHA. The bytes on disk do not hash to it, and no whitespace variant does:

```
$ python3 - <<'EOF'   # variants of corpus/evidence/round60-claims.md
raw      65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1   (len 3355, single trailing NL)
rstrip-nl cae804faeb016bf18d8183355e3885b7269e3fbce0a70d790cd688e5bb7175be
crlf     dbb847b81e834ecff97ca54bc2fe149a1fcdd2f8d2aa90aa50ac4c079778ba54
lstrip   65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
```

All twelve `w1-spec.json` seat prompts carry the same `09d8053f…` string, so the constant is
L1-side, while the file it names hashes `65721569…`. Either the freeze was serialised differently
before dispatch or the file changed after the SHA was taken. I analysed the bytes on disk (their
C1/C2 text is quoted verbatim below, so the analysis is keyed to content, not to the hash). The L1
must reconcile this before any closure cites a claim digest.

---

## 2. C1 counter — verdict: **not operable against the frozen predicate; PASS is reachable without the claimed work**

Frozen predicate (claims file, C1): `python3 corpus/evidence/round60/c1-count.py --builder <builder>
--work <fresh-absolute-dir> --seed 6001` prints `C1=PASS` and exits 0 **iff**
(a) the candidate reaches the observed safe path without deleting the foreign file,
(b) the pinned r55 builder deletes it, and
(c) the output-injection mutant prints `=PASS` but is scored as a **failure**.

### 2.1 Clause conformance

| Clause | Implemented at | Conforms? |
|---|---|---|
| (a) safe path, foreign preserved | `:38` `intact = foreign.is_file() and foreign.read_bytes() == before`; `:41` `candidate_safe = rc == 0 and intact` | **No.** No safe-path observation at all: the counter never reads `out/spans` after the candidate, and `rc == 0` credits a builder that does nothing (measured §2.2 B). `is_file()` follows symlinks, so a swapped symlink or a same-bytes rewrite also score safe (§2.3). |
| (b) pinned r55 control deletes | `:19` `R55 = BASE/"controls/build-spans-r55.py"`; `:42`, `:67` | **Partly.** The destructive control is present and does delete (measured §2.4), but the file is bound **by path only** — the round-58 counter pinned `R55_BUILDER_SHA = 1ed2650a…`; round 60 dropped that pin, so a swapped control silently redefines the negative. |
| (c) injection mutant scored as failure | `:43` `forged_safe = rc == 0 and not intact`; `:63` `forge_blocked = forge_state != "forged_safe"` | **No.** `:42` and `:43` are the *same expression*, so `"forged_safe"` is unreachable (`:44` returns `baseline_bad` first) and `forge_blocked` is unconditionally `1`. Measured: `"forged_safe" in reachable states → False` (§2.5). The leg is a tautology, and the mutant itself is scored `candidate_safe`, i.e. the *accepting* state (§2.2 C). |
| `--seed 6001` | `:53` | **No.** Parsed and never read (`grep -n '\.seed'` → no use); the fixture is fixed text, so the predicate's seed is decorative. |
| fresh `--work` | `:23-26` | **No clean failure.** A reused directory raises `FileExistsError` from `run()` (§2.6); no `TMPDIR` hardcoding otherwise (creditable: contract §7.4 honoured). |

### 2.2 Measured runs (scratch, exit codes retained)

```
$ python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work …/c1-default --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
EXIT=1

$ … --builder …/noop-builder.py --work …/c1-noop --seed 6001        # sys.exit(0), touches nothing
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
EXIT=0

$ … --builder …/c1-noop/forged.py --work …/c1-forged --seed 6001    # the counter's own injection stub
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=1/1
C1=PASS
EXIT=0
```

* **A** — the lane's own builder (`tools/build-spans.py`, byte-identical to the pinned r55 "before"
  bytes) is scored `baseline_bad`; the frozen predicate run as written prints `C1=FAIL`. The
  "candidate" the claim wants does not exist in the tree yet, which is expected mid-round — but it
  also means the default `--builder` **is** the unsafe control.
* **B** — a do-nothing builder reaches the target. Contract §9: *a target must be one a do-nothing
  control cannot reach*; this counter violates it. This alone blocks C1 admission.
* **C** — the counter's own "output-injection mutant" (`:55`, `print('=PASS')` + `sys.exit(0)`), handed
  in as the candidate, is credited `C1=PASS`. Clause (c) asks that this mutant be scored a failure;
  here it is scored the same as a good candidate. The reported `INJECTION_REJECTED=1/1` comes only
  from the dead branch at `:42-44`.

### 2.3 Preservation is not identity-preserving

```
$ python3 -B leniency-probe.py           # imports the counter read-only, calls run() directly
symswap-builder.py:  rc=0 state='candidate_safe'    # unlinks foreign, replaces it with a symlink to identical bytes
overwrite-builder.py: rc=0 state='candidate_safe'   # rewrites the foreign file with identical bytes
```

`intact` (`:38`) tests `is_file()` + bytes, not regular-file identity (`os.lstat`/`S_ISREG`) and not
inode/mtime, so "without deleting the foreign file" is satisfiable by deleting it.

### 2.4 The pinned control genuinely deletes (clause b holds at the file level)

```
$ BUILDER on the counter's own fixture:  SPANS_ROWS=1 WRITTEN=1 ; out/spans → S601-1.txt ; foreign deleted
```

So the negative control is real; the *positive* side is what fails. Note also that the safe path the
claim asks for (produce the S601 span, keep the orphan `S777-1.txt`) is observable — `S601-1.txt` is
written — but the counter never looks at it (defect D4).

### 2.5 `forged_safe` is unreachable (dead-branch proof)

```
$ python3 -B state-probe.py
module imported, ROOT = /home/vgpnk/Projects/shokunin/chousa-shokunin | R55 exists: True
pinned_r55: rc=0 state='baseline_bad'
noop: rc=0 state='candidate_safe'
counter_stub_forged: rc=0 state='candidate_safe'
distinct states over 8 (rc × intact) combinations: ['', 'baseline_bad', 'candidate_safe']
'forged_safe' reachable: False
```

### 2.6 Reused work dir crashes instead of refusing

```
$ … --builder noop-builder.py --work …/c1-noop       (second run, dir already populated)
FileExistsError: [Errno 17] File exists: '…/c1-noop/forge/cache'
```

### 2.7 The hardened direction the lane declared is scored FAIL

`SCORECARD.md:2859` names the hardening set for `tools/build-spans.py` — "refuse a foreign
`spans.tsv` in `--out`, refuse symlinked outputs, …". A candidate implementing that refusal:

```
$ python3 -B refuse-probe.py
refuse-foreign-builder.py: rc=3 state=''      foreign file after run: True
$ python3 -B corpus/evidence/round60/c1-count.py --builder …/refuse-foreign-builder.py --work …/c1-refuse --seed 6001
INJECTION_REJECTED=1/1
BASELINE_DISCRIMINATES=1/1
CANDIDATE_REFUSAL=0/1
C1=FAIL
EXIT=1
```

The counter's leg (a) therefore *rewards inaction and punishes refusal*: the only builder shapes that
score `candidate_safe` are "does nothing" or "does the safe work and leaves a foreign file in place".
The claim's own sentence ("captured builder stdout/stderr cannot satisfy a **refusal** leg") has no
refusal leg to test — the round-60 counter removed all seven of round 58's, and leg (c) does not
substitute for one.

### 2.8 C1 defect list (minimal, each measured)

| # | Defect | Site | Receipt |
|---|---|---|---|
| D1 | `baseline_bad` and `forged_safe` are the same predicate ⇒ clause (c) vacuous | `:42-44`, `:63` | §2.5 |
| D2 | do-nothing builder reaches `C1=PASS` exit 0 | `:41` | §2.2 B |
| D3 | the injection mutant, as `--builder`, is accepted (`CANDIDATE_REFUSAL=1/1`) | `:55`, `:69` | §2.2 C |
| D4 | safe path unobserved: no read of `out/spans`/S601 output, no cache-consumption check | `:38-41` | §2.4 |
| D5 | `intact` accepts symlink swap and same-bytes rewrite | `:38` | §2.3 |
| D6 | hardened refusal candidate scored FAIL (safe path defined as inert) | `:41` | §2.7 |
| D7 | `--seed` parsed, never used | `:53` | grep, §2.1 |
| D8 | r55 control bound by path, no digest pin (round-58 had one) | `:18-19` | §1 hashes |
| D9 | reused `--work` ⇒ uncaught `FileExistsError` | `:25-26` | §2.6 |

---

## 3. C2 counter — verdict: **not operable against the frozen predicate; base already PASSes, and overreach is unmeasured**

Frozen predicate (claims file, C2): `c2-count.py --root <lane-copy> --work <fresh-absolute-dir>`
must establish source digest and quote location from the committed S101 raw capture **using the
pinned capture-text form**, verify the new entry's exact observation and **no overreach** against
those source bytes, verify its S101 citation and metadata, and **require the scorecard's declared
disposition**. **Base must fail because no round-60 entry exists.**

### 3.1 Clause conformance

| Clause | Implemented at | Conforms? |
|---|---|---|
| source digest from `--root` | `:6`, `:13`, `:16` (`RAW_PIN`) | **Yes.** Swapped raw → `RAW_PIN=0/1 C2=FAIL` exit 1 (§3.2b). |
| quote location via pinned form | `:7`, `:13`, `:16` (`FORM_PIN`, `QUOTE`) | **Partly.** Form is `ROOT/'.ufo/waves/round-60/s101-open.txt'` — the *lane's* file — not `--root`'s, so the quote is never re-derived from the tree under test (bogus raw still `QUOTE=1/1`, §3.2b). Provenance of the pin is genuine: it equals `tools/capture-text.py` output byte-for-byte (§3.2c). |
| "the new entry's exact observation" | `:8` `ENTRY = …/citation-count-semantics-r37.md` | **No.** The target is the **round-37** entry, unmodified since base (`b379919:…` sha `bb80627b…` = worktree sha). There is no round-60 entry to test (`ls corpus/knowledge | grep -Ei 'r60\|round-60'` → none). |
| no overreach against source bytes | `:18` `scoped = '#### Unknown' in body and '<literal sentence>' in body` | **No.** Two literal substrings; nothing is compared to the capture. An entry asserting present-day validity and CNKI implementation still PASSes (§3.2a). |
| S101 citation + metadata | `:17` | Partly: prefix `\n# `, a literal `source: S101 — https://jc.hit.edu.cn/`, `verified-at:`, `recheck:` — keyword presence, not parse. |
| scorecard disposition | — | **Absent.** `grep -n 'scorecard\|disposition' c2-count.py` → no output. |
| base must fail | — | **Violated.** Base run PASSes (§3.2a). |
| `--work` fresh dir honoured | `:13` | Parsed, unused. |
| clean base failure | `:22` | `OSError` → `C2=ERROR`, exit **2**, not the declared `C2=FAIL` (§3.2d). |

### 3.2 Measured runs

**(a) base — no round-60 entry exists, and the counter PASSes**

```
$ python3 -B corpus/evidence/round60/c2-count.py --root <lane> --work …/c2-base
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
EXIT=0
```

The cited entry is committed at the claim base:

```
$ git -C <lane> show b379919:corpus/knowledge/citation-count-semantics-r37.md | sha256sum
bb80627b15a709b50fcdca78b668b912386ab3b27260e7367ffd5a8a99c203cb  -
$ sha256sum corpus/knowledge/citation-count-semantics-r37.md
bb80627b15a709b50fcdca78b668b912386ab3b27260e7367ffd5a8a99c203cb  corpus/knowledge/citation-count-semantics-r37.md
$ git -C <lane> show b379919:corpus/knowledge/citation-count-semantics-r37.md | grep -n '#### Unknown' -A2
74:#### Unknown
76-- Whether the copy's self-citation rule is current, …
```

The `#### Unknown` block and the S101 sentence the counter looks for are already in the base tree, so
the counter is a tautology over pre-existing bytes: **a do-nothing round passes C2** (contract §9).

**(b) overreach is not detected; the quote is not bound to `--root`**

```
$ python3 -B c2-count.py --root …/overreach-root   # entry + appended: "S101 establishes that the
                                                  # specification copy is the version currently in
                                                  # force and that CNKI implements the 文献类型标志 rule today."
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS
EXIT=0

$ python3 -B c2-count.py --root …/rawswap-root    # raw replaced by "not the capture\n"
RAW_PIN=0/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=FAIL
EXIT=1
```

The `RAW_PIN` leg works; the `QUOTE=1/1` in the same run proves the quote location is read from the
lane's pinned form, not from the bytes under `--root`.

**(c) the form pin is genuine**

```
$ python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw > capture-form.txt ; echo EXIT=$?
EXIT=0
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  capture-form.txt
a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867  .ufo/waves/round-60/s101-open.txt
FORM_IDENTICAL=yes
$ grep -c 'c. 文献类型及载体类型标志；' capture-form.txt
1                       # line 245
```

**(d) missing entry is an ERROR, not a scored base failure**

```
$ python3 -B c2-count.py --root …/emptyroot --work …/c2-empty
C2=ERROR FileNotFoundError: [Errno 2] No such file or directory: '…/emptyroot/corpus/knowledge/citation-count-semantics-r37.md'
EXIT=2
```

### 3.3 C2 defect list

| # | Defect | Site | Receipt |
|---|---|---|---|
| E1 | base PASSes; no round-60 entry is tested at all (target is the r37 entry) | `:8` | §3.2a |
| E2 | overreach unmeasured (two literal substrings) | `:18` | §3.2b |
| E3 | quote location never derived from `--root`; form pinned to lane ROOT | `:7`, `:13` | §3.2b |
| E4 | scorecard disposition clause absent | — | grep |
| E5 | `--work` unused | `:13` | grep |
| E6 | missing entry → exit 2 `C2=ERROR`, not `C2=FAIL` exit 1 | `:22` | §3.2d |

Creditable: `RAW_PIN`/`FORM_PIN` are real pins and both bite (E-b receipt), the form pin matches the
defined text form, and no `/tmp` path is hardcoded (contract §7.4).

---

## 4. What the round can and cannot land on these counters

* **C1 as frozen is unreachable on current source and forgeable by inaction.** `C1=PASS` needs a
  candidate that writes `spans/S601-1.txt` *and* leaves `S777-1.txt` — no seat has produced one, and
  the counter would accept a builder that produces nothing. Reporting `C1=PASS` from run B would be
  reporting the do-nothing control.
* **C2 as frozen is already satisfied at base**, so it cannot separate before from after. The
  substantive part of C2 (separating what S101 states from present-day validity/CNKI practice) is
  exactly the part no string comparison in the current counter measures.
* Both counters are **runnable and deterministic** — this is a counter-construction defect, not an
  environment defect: paths resolve, the r55 control and the S101 capture are present, the form pin
  matches `tools/capture-text.py`, and every failure mode above is a verdict-shape flaw.

### 4.1 Minimal amendment spec (recommendation for the L1; **not landed by this seat**)

Per contract §9 a rule changed after a seat has scored is not the claim's rule, so these belong in a
*frozen amendment taken before any C1/C2 verdict is scored* — not in a post-hoc reading of an already
scored run.

C1:
1. `run()` returns a structure, never a prose label: `{rc, foreign: "absent"|"symlink"|"regular:sha", created: [paths under out/spans], diag: (stdout, stderr)}` — `diag` diagnostic only, read by no predicate.
2. Leg SAFE = `rc == 0` **and** `foreign == "regular:<seeded sha>"` (via `os.lstat` + `S_ISREG`) **and** `spans/S601-1.txt` present and non-empty. This kills D2/D4/D5 and makes D6's refusal an explicit, separate outcome.
3. Leg CONTROL = verify `sha256(R55) == 1ed2650a…` before use (D8), then require `foreign == "absent"` after the r55 run.
4. Leg INJECTION = the mutant must *fail* under the **same** `score()` function used for the verdict (no separate label) and must be a builder that satisfies the round-59 spoof shape — prints `=PASS` while destroying the foreign file (rc 0), i.e. `score(mutant) is False` and `mutant.diag` contains `=PASS`. Kills D1/D3; the round-59 spoof is at `.ufo/waves/round-59/w1/R59Executor09.md` §6.
5. Use `--seed` to derive the fixture quote/ids (D7); refuse a non-empty `--work` with a one-line error (D9).

C2:
1. Bind `ENTRY` to the round-60 entry (front-matter `round: 60`) and score the base by running the same predicate against a base-revision copy; require base `C2=FAIL` exit 1. Kills E1.
2. Derive the form by running `tools/capture-text.py` over `--root`'s raw inside the counter (or pin its sha per root) so quote location and digest come from one tree. Kills E3.
3. Make "no overreach" countable or hand it to a reviewer leg: require the entry to carry a machine-read `scope:`/`limit:` pair and count only the *mechanical* clauses (digest, quote-once-at-line, citation, metadata, disposition); an unstructured "must not overreach" clause is not string-checkable — the mutant in §3.2b is the proof. Report it as `unprovable` if the lane will not restructure the entry.
4. Add the scorecard clause: parse `SCORECARD.md` for the C2 row and require its declared disposition token to match the run's verdict (E4). Honour `--work` or drop the flag (E5); missing entry → `C2=FAIL` exit 1 (E6).

---

## 5. Retained evidence index (all outputs above were produced in scratch with these commands)

| Receipt | Command (run from `/fast/scratch/hyaku/chousa-r60/BuildCounter`) |
|---|---|
| §2.2 A/B/C | `python3 -B <lane>/corpus/evidence/round60/c1-count.py --builder {tools/build-spans.py,noop-builder.py,c1-noop/forged.py} --work … --seed 6001` |
| §2.5 | `python3 -B state-probe.py` (imports `c1-count.py` read-only; `run()` over three builders + 8-combination state enumeration) |
| §2.3 | `python3 -B leniency-probe.py` (`symswap-builder.py`, `overwrite-builder.py`) |
| §2.7 | `python3 -B refuse-probe.py`; then the same counter with `--builder refuse-foreign-builder.py` |
| §2.4 | `python3 -B <lane>/tools/build-spans.py --quotes … --out … --cache …` on the counter's own fixture |
| §3.2 a/b/d | `python3 -B <lane>/corpus/evidence/round60/c2-count.py --root {<lane>,overreach-root,rawswap-root,emptyroot} --work …` |
| §3.2c | `python3 -B <lane>/tools/capture-text.py <raw> > capture-form.txt; sha256sum; cmp` |

Fixtures built this seat (scratch only): `noop-builder.py` (`b5838277…`), `symswap-builder.py`,
`overwrite-builder.py`, `refuse-foreign-builder.py`, `state-probe.py`, `leniency-probe.py`,
`refuse-probe.py`, `overreach-root/`, `rawswap-root/`, `emptyroot/`.

---

## 6. Risks, limits, blockers

* **Blocker (L1 action, not mine):** F1 — the assigned claim SHA does not match the on-disk claims
  file; a closure citing either digest without reconciliation would be unfounded.
* **Limit:** the counters are untracked, so "current counter" means the 17:51/17:52 draft bytes
  hashed in §1; if another seat rewrites them, every receipt above is keyed to those hashes.
* **Limit:** no live/offline source content was re-opened for S101 beyond the committed capture and
  its pinned text form; external truth remains unknown and this seat asserts nothing about it.
* **Not done by design:** no counter edits, no fixture in the lane, no builder change, no commit, no
  spawn (my one labrat card was not needed — every hypothesis above was measurable directly).
* **Tool installs:** none.

**Scratch disposition.** `/fast/scratch/hyaku/chousa-r60/BuildCounter` was created, used, and
removed before yield; nothing this seat produced outside this file survives on disk.
