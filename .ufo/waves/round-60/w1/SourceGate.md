# SourceGate — round-60 source/freeze gate over the frozen claims

**Seat.** SourceGate, leaf analyst (axes: operability, depth). No spawn, no fetch, no install,
no commit, no git/jj mutation. Every command below ran read-only against the lane tree; all
writes went to `/fast/scratch/hyaku/chousa-r60/SourceGate` (removed before this seat yielded).
**Assignment.** Bounded analysis against `corpus/evidence/round60-claims.md`, prior committed
evidence, and the current counters/source only.
**Lane tip at analysis time.** `master = b379919a873e7080a31ef92c7002f55f5374e2c6` (the claims'
declared base; `git for-each-ref refs/heads/`).

A source gate asks one question per claim: **does the claim's stated before-state, source chain
and after-state predicate actually hold against the bytes the lane owns?** Findings are grouped
per claim, each with the command and its exact output.

---

## 0. Pins measured (start of this seat)

| artifact | sha256 / value | note |
|---|---|---|
| `corpus/evidence/round60-claims.md` | `65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1` | 17 lines, mtime `2026-10-27 17:51:18`, **untracked** at base |
| declared claim SHA (wave context) | `09d8053f5f09a26c07f41286a7a885a2c21bff31b30f71963cceaa35d971a440` | **no file matches** (see §1) |
| `corpus/evidence/round60/c1-count.py` | `66e50763f070e3ce9983215eecef837bd8740542bf05ec4d3e04e8ebf6acbdb7` | mtime `17:51:38` |
| `corpus/evidence/round60/c2-count.py` | `a19b06789f02a3aa9d4bf52a7a215f5614076706056ab9fcd300fdc131e83abe` | mtime `17:52:14` |
| `tools/build-spans.py` | `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` | **identical** to `corpus/evidence/round58/controls/build-spans-r55.py` |
| S101 raw capture `corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` | `6063a3aff7a4081e93a685f2721e2cd6b477ba84a841211e298bcddd6d9fddf3` | matches the C2 pin |
| defined form `.ufo/waves/round-60/s101-open.txt` | `a8e3e7ad213b6ec50479542cda23612e7ae7ae5fd4506fba53a91f2f7e79f867` | matches the C2 pin |
| `tools/capture-text.py` | `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573` | matches the round-58 pin |

`git diff --stat b379919 -- corpus/knowledge/citation-count-semantics-r37.md
corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw tools/capture-text.py tools/build-spans.py` printed
nothing (rc 0): the C2 entry, the capture, the capture tool and the builder are **unchanged from
base** at this seat's read time.

---

## 1. Freeze integrity — **UNVERIFIABLE** (the one item the L1 must repair before citing the freeze)

The wave context declares the claim file's immutable SHA as `09d8053f…`. The bytes seats read do
not hash to it:

```
$ sha256sum corpus/evidence/round60-claims.md
65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1  corpus/evidence/round60-claims.md
```

The declared value names no artifact in the lane: every non-`.git` file was hashed (23,800 files,
2.4 MiB+ bodies included) and zero matched, while exactly one matched the measured digest (the
claims file itself):

```
$ find . -path ./.git -prune -o -type f -print0 | xargs -0 sha256sum > lane-hashes.txt
$ wc -l < lane-hashes.txt                      -> 23800
$ grep -c '^09d8053f' lane-hashes.txt          -> 0
$ grep -c '65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1' lane-hashes.txt -> 1
```

It is not a newline/encoding variant of the current file either — every line-prefix truncation
(k=0..17), CRLF, missing-final-newline, NFC, NFD and per-line right-strip all miss:

```
declared_sha_hits: NONE
num_lines: 17 sha256_file: 65721569fc1336b159c7637acf476cda6f583bbd4b3a84aaadd239f7d02018d1
```

**What does hold.** The file was not touched after dispatch: claims mtime `17:51:18` precedes the
dispatch markers (`c1-count.py` `17:51:38`, `c2-count.py` `17:52:14`, `w1.ready` `17:55:21`), and
the content is unchanged between my first and last read. The freeze's *stability* is supported;
its *declared digest* is not.

**Repair.** Record the digest the seats actually read (`65721569…`) in the round report and commit
the frozen claims file as wave evidence, so the freeze has a committed artifact to hash. Per the
frozen-round rule the claim text, predicate, counter, kill rule and target must then stay exactly
as frozen — this is a citation repair, not a claim change. Until it is repaired, no receipt may
claim "the immutable claim SHA" as evidence.

---

## 2. C1 before-state — **VERIFIED** against committed evidence

The claims (`round60-claims.md:11`) say round-58's C1 permitted forged target-token output to
satisfy refusal checks and that `R59Executor09.md` demonstrated `C1=PASS` with all seven hazards
failing. Byte check:

- `.ufo/waves/round-59/w1/R59Executor09.md:215` — §6 "Correction — `C1=PASS` is reachable on the
  frozen bytes by echoing the needle": the candidate "fails every refusal check, but prints `=PASS`
  in its stderr, is credited `C1=PASS`"; its receipt shows every refusal leg as `fail(...)` while
  `SUMMARY … REFUSE=7/7` and `C1=PASS`, `EXIT=0`, "Reproduced twice".
- Cause is visible in the round-58 code: `corpus/evidence/round58/c1-count.py:150-160` and `:223`
  splice candidate stderr into the leg string, and `:391` `ref_pass = all(("=PASS" in l) …)` /
  `:399` then substring-scan that assembled prose.

Verdict: the before-state is grounded, not asserted. Note for the record that the PASS in §6 came
from a spoofing candidate on the frozen bytes — R59's own §2 probe covers non-spoofing stderr only
(`192/192`). The claim's sentence is accurate as written.

---

## 3. C1 counter — **frozen predicate not implemented** (BLOCKING: the round's own kill rule fires)

Frozen predicate (`round60-claims.md:9`) requires `C1=PASS` and exit 0 **iff** (a) the candidate
reaches the independently observed safe path without deleting the foreign file, (b) the pinned r55
builder proves destructive, (c) the output-injection mutant is **scored as a failure**. Measured
against the pinned counter `66e50763…`:

| probe | candidate | command | output | exit |
|---|---|---|---|---|
| P1 | lane `tools/build-spans.py` (= r55) | `python3 -B corpus/evidence/round60/c1-count.py --builder tools/build-spans.py --work $S/p1 --seed 6001` | `INJECTION_REJECTED=1/1` `BASELINE_DISCRIMINATES=1/1` `CANDIDATE_REFUSAL=0/1` `C1=FAIL` | 1 |
| P2 | **do-nothing stub** (`sys.exit(0)`) | same counter, `--work $S/p2` | `INJECTION_REJECTED=1/1` `BASELINE_DISCRIMINATES=1/1` `CANDIDATE_REFUSAL=1/1` **`C1=PASS`** | **0** |
| P2b | output-injection stub (prints `=PASS`, writes nothing) | `--work $S/p2b` | same three legs `1/1`, **`C1=PASS`** | **0** |
| P6 | **wrong-bytes** candidate (writes `WRONG BYTES` to `out/spans/S601-1.txt`) | `--work $S/p6` | `CANDIDATE_REFUSAL=1/1`, **`C1=PASS`** | **0** |
| P3 | direct call of `run()` for forged / no-op / r55 | probe harness | `forged: rc=0 state='candidate_safe'` · `noop: rc=0 state='candidate_safe'` · `r55: rc=0 state='baseline_bad'` | — |
| P4 | pinned r55 control removed from the script's tree | script copied to a mirror without `corpus/evidence/round58/` | `BASELINE_DISCRIMINATES=0/1` `C1=FAIL` | 1 |

### D1 — the safe path is never observed
The candidate leg is `candidate_safe = p.returncode == 0 and intact` (`c1-count.py:41`); nothing
checks that the builder produced the expected span. After P2 the output tree contains only the
seeded foreign file:

```
$ find $S/p2/candidate -maxdepth 3 | sort
…/p2/candidate/cache/6bae421110584d66e6bd9543.txt
…/p2/candidate/out/spans/S777-1.txt
…/p2/candidate/quotes.tsv          <- seeded fixtures only; no S601-1.txt
```

So "reaches the independently observed safe path" reduces to "did not run, and did not delete".
P6 shows the same hole from the other side: a builder that writes **wrong** bytes where a span
belongs is accepted.

### D2 — the injection leg is a tautology (dead branch)
`c1-count.py:41-44`:

```
41:        candidate_safe = p.returncode == 0 and intact
42:        baseline_bad   = p.returncode == 0 and not intact
43:        forged_safe    = p.returncode == 0 and not intact     # identical to :42, shadowed by it
44:        return p.returncode, "candidate_safe" if candidate_safe else ("baseline_bad" if baseline_bad else ("forged_safe" if forged_safe else ""))
```

`forged_safe` can never be returned, so `forge_blocked = forge_state != "forged_safe"`
(`c1-count.py:63`) is `True` for every possible child. `INJECTION_REJECTED=1/1` is therefore not
a measurement. The forged script itself (`c1-count.py:60`) does not reproduce the round-58 forgery
at all: it neither refuses nor touches any fixture — it prints the token and exits 0.

### D3 — predicate (c) is contradicted, not satisfied
P2b is the output-injection mutant the predicate names: it prints `=PASS` and is scored
`candidate_safe` — i.e. **credited as the safe candidate**, not scored as a failure. The claim's
own kill rule ("any child output injection passes target") is fired by this run, measured.

### D4/D5 — dead and fragile inputs
`--seed 6001` is parsed (`:53`) and never read: `--seed 6001` and `--seed 9999` produce identical
legs and verdict (measured twice, both `C1=PASS` on the no-op stub). Re-running with a reused
`--work` dir crashes instead of scoring:

```
FileExistsError: [Errno 17] File exists: '…/p2reuse/forge/cache'   (exit 1)
```

The frozen predicate does say `<fresh-absolute-dir>`, so this is a robustness defect, not a
predicate violation — but a crash and a scored FAIL are indistinguishable to a closure that only
reads the exit code.

### What is sound
Output bytes genuinely cannot establish a leg (`run()` derives only `returncode` + filesystem
state); the baseline leg (b) is real (`r55 → baseline_bad`, P1/P3) and fails **closed** when the
control is missing (P4). The claim's narrow "measurement integrity" ambition is the right target;
the implementation misses it on (a) and (c).

---

## 4. C2 source chain — **VERIFIED exact** (the sourced half of the claim is honest)

- Raw digest and defined-form digest both match the pins (`6063a3af…`, `a8e3e7ad…`); the form is
  reproducible from committed bytes only: running the pinned tool on the committed capture inside a
  base mirror prints `a8e3e7ad…` (same digest).
- The located quote is unique and at the stated line:
  `grep -c 'c\. 文献类型及载体类型标志；' .ufo/waves/round-60/s101-open.txt` → `1`;
  `grep -n …` → `245:c. 文献类型及载体类型标志；`; line 241 is the GB/T 7714 recommendation
  sentence quoted in `s101-receipt.txt` — consistent with the claim's "offline capture states … not
  present-day validity".
- The claim's existing-note anchor is accurate: `corpus/knowledge/citation-count-semantics-r37.md:23-31`
  is exactly the S101 observation paragraph, quoted from the capture, with no validity assertion.
- The note's limit is already recorded in the base entry: base lines 78-79 read
  "Whether the specification copy (S101) is the version in force, …".

---

## 5. C2 counter — **base already satisfies it** (BLOCKING: do-nothing control reaches `C2=PASS`)

Frozen predicate (`round60-claims.md:17`) says the counter must "verify the new entry's exact
observation and no overreach against those source bytes, verify its S101 citation and metadata, and
require the scorecard's declared disposition"; the claim adds "**Base must fail because no round-60
entry exists**". Measured against `a19b0678…`, with the lane's claim base extracted to a mirror:

```
$ git archive b379919 | tar -x -C $S/base
$ cp corpus/evidence/round60/{c1,c2}-count.py $S/base/corpus/evidence/round60/
$ cp .ufo/waves/round-60/s101-open.txt $S/base/.ufo/waves/round-60/
$ python3 -B $S/base/corpus/evidence/round60/c2-count.py --root $S/base --work $S/c2base
RAW_PIN=1/1 FORM_PIN=1/1 QUOTE=1/1 LINE=245 METADATA=1/1 LIMIT=1/1
C2=PASS                                                        (exit 0)
```

The same counter on the current tree prints the identical line (`C2=PASS`, exit 0): the after-state
is already present at base, so the counter cannot separate work from no work.

Cause, by clause:

1. **No round-60 entry exists in the code.** `ENTRY` points at the pre-existing
   `corpus/knowledge/citation-count-semantics-r37.md` (`c2-count.py:8`, `:13`). There is no
   round-60 path anywhere in the file, and no round-60 knowledge file exists in the tree.
2. **The metadata and limit legs pass on base bytes** — checked directly on the base mirror:
   `starts_with_newline_hash=True source_S101_url=True verified_at=True recheck=True
   unknown=True limit_sentence=True`.
3. **The only leg that base lacks is a form the base itself regenerates.** The `FORM_PIN` leg reads
   `.ufo/waves/round-60/s101-open.txt` — a wave artifact produced by running the pinned
   `capture-text.py` on the committed capture, which in the base mirror prints the pinned digest.
   Regenerating it is not the claim's work.
4. **Two predicate clauses are unimplemented.** `grep -c 'SCORECARD\|scorecard' c2-count.py` → `0`
   (no "scorecard's declared disposition"); and no code compares the entry's observation to the
   capture bytes (no overreach check) — `:17-18` only test four substrings and a two-line
   presence.
5. Minor: `--work` is accepted and never used; `FORM`/`ENTRY` are re-hard-coded from `ROOT`
   (`c2-count.py:7`, `:13`) so `--root <lane-copy>` cannot score a copy's own form — it always reads
   the live lane's form.

The claim's *other* premise — "If the source quote/capture or QUALITY test is unavailable, do not
admit and declare unprovable" — is honest, and the source half of C2 (§4) is real. What fails is
the measurement: it scores a note that already exists.

---

## 6. Do-nothing controls (§9 sizing rule — committed here as the gate's receipt)

| control | skips the claimed work by | counter | result |
|---|---|---|---|
| no-op builder (`sys.exit(0)`) | doing nothing at all | round-60 C1 | **`C1=PASS`, exit 0** — control meets target → counter/target wrong |
| injection builder (prints `=PASS`) | echoing the token | round-60 C1 | **`C1=PASS`, exit 0** |
| base tree + regenerated capture form | doing nothing at all | round-60 C2 | **`C2=PASS`, exit 0** |
| r55 control absent | removing the pinned negative | round-60 C1 | `C1=FAIL`, exit 1 (fails closed — sound) |

Per the sizing rule the first three receipts mean the counters must be repaired **before** any
after-data is scored, or the round's target is reachable without the claimed work.

---

## 7. Minimal repairs (integration guidance for the L1; no claim text changes needed)

C1 (`c1-count.py`):
1. Observe the safe path: after the candidate run require the expected artifact
   (`out/spans/S601-1.txt`, or the builder's documented output) to exist **and** match the expected
   bytes (round-58's `expect_ok` already does this — reuse it).
2. Give the injection run its own expected state, distinct from the candidate's: the forgery must
   produce no spans **and** be classified `no_spans`/`forged`; delete the shadowed `forged_safe`
   branch (`:43`) so `INJECTION_REJECTED` can print `0/1`.
3. Either consume `--seed` (fixture bytes/URL from it, as round-58 does) or drop it; and
   `mkdir(exist_ok=False)` → refuse a non-empty `--work` with a scored error instead of a traceback.

C2 (`c2-count.py`):
1. Point `ENTRY` at a round-60 entry path — the entry the claim actually adds.
2. Add the base discriminator the claim promises: the new entry must be absent at base (or carry a
   round-60 marker absent in base), so base cannot pass.
3. Implement the two missing clauses: observation-vs-capture check (each quoted span appears in the
   defined form at a located line, and the entry asserts nothing beyond it) and the SCORECARD
   disposition read.
4. Resolve `FORM`/`ENTRY` under `--root`, and use `--work`.

C1 note for claim consistency: `tools/build-spans.py` is byte-identical to the r55 pin, so legs (a)
and (b) cannot both hold without a builder change; the counter's P1 receipt (`CANDIDATE_REFUSAL=0/1`)
is that coupling, not a stray failure. The claim says it does not claim the builder, so the after
receipt must name which builder the candidate leg scored.

---

## 8. Risks and boundaries

- **Mutable pins.** Wave seats own `corpus/evidence/round60/*.py`; the digests in §0 are this seat's
  read time. A closure must re-hash before citing them. If a seat edits either counter after this
  report, re-measure §3/§5 against the new bytes.
- **Freeze digest.** Until §1 is repaired, the frozen claims rest on an uncommitted, untracked file
  whose declared digest matches nothing the lane ships.
- **Scope of this gate.** I did not run the round's closure, any build, any formatter or any test
  suite outside the two counters; I did not evaluate C1/C2's axes or scores, and I make no claim
  about the round's admission. Verdicts above are about source grounding and measurement
  integrity only.
- **Writes.** This report is the only file this seat wrote in the lane.
- **Scratch.** `/fast/scratch/hyaku/chousa-r60/SourceGate` (mirror, stubs, probe outputs) removed
  before yield; every receipt that matters is quoted above.
