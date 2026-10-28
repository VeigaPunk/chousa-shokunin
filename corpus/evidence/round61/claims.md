# Round 61 — chousa — frozen claims

Frozen before any wave seat is dispatched. Base: lane master `9eef15e7c0e0ae0055228e7066dc1eec676a91d2`.
First freeze commit `1661b85bfa84d3dc75712d64f79034265b8831d3`; amended once, before any seat existed, by
A1 below (the second freeze commit is the one the wave context names).
Date 2026-10-28. This file's own sha256 and the freeze commit are carried in the wave context and
in the report; neither can be written inside the file (rule: freeze digest computed from the final
persisted bytes, QUALITY 116). No predicate, counter, kill rule or target below changes after this
commit; a changed rule is not the claim's rule.

Round 60's closure (`corpus/lessons/round-60-verifier-spotcheck.md`, routed defects) is the reason for
this file's shape: both frozen counters of rounds 58 and 60 were reachable or unreachable by
construction. Every counter here was therefore built and exercised before this freeze with
(a) the base, (b) do-nothing stubs, (c) a token-forging stub, (d) a naive-guard builder,
(e) a positive control that reaches the target, and (f) frozen mutants of the positive control.
Receipts: `corpus/evidence/round61/controls/`.

## C1 — operability: the span builder's output safety (lowest scored axis)

Target axis: operability (the lane's only scored axis, historical 3/10 on the round-1 archived-export
observable; that numeric observable is not moved and no new score is invented — the claim is the
leg count below).

**Predicate R61-C1** (the sentence in the docstring of `corpus/evidence/round61/c1-count.py`): run on a
builder B (default `tools/build-spans.py`) copied beside the lane's `tools/capture-text.py` into 20 fresh
fixture directories with random names, ids, URLs and contents, B exits and leaves the file tree as each
leg states — counted `LEGS=20/20 C1=PASS`. Legs: P01 TXT, P02 DOCX, P03 NOPYC, P04 CHECK, P05 REFUSEROW,
P06 REBUILD (behaviour the builder holds at base) and H07 FOREIGN, H08 REPLACE, H09 ORPHAN, H10 SPANSLINK,
H11 FILELINK, H12 TSVLINK, H13 OUTSIDE, H14 BIGTXT, H15 BIGRAW, H16 OUTFILE, H17 UNREADABLE, H18 FIFO,
H19 ENTRYDOT, H20 BIGFORM (the hazards `.ufo/waves/round-56/w1/R55W2SentBuilder.md` measured). A leg's
verdict comes from the child's exit code, its file tree and its peak RSS only — never from searching its
output for a token (QUALITY 117).

Counting command (from the lane root, fresh `--work`, random seed printed):

    python3 corpus/evidence/round61/c1-count.py --builder tools/build-spans.py --work <absent-or-empty dir>

**Before** (base builder, blob `072415ad36d9167f4ebe8117765b7053fb261069`, file sha256 `1ed2650a…c80bf6`):
`LEGS=7/20 C1=FAIL` exit 1 at seeds 61001 and 61002 (`controls/c1-before.txt`): P03, H07–H17 and H20
fail, the other 7 pass.
**After target**: the landed `tools/build-spans.py` at the landing commit prints `LEGS=20/20 C1=PASS`,
exit 0, at three fresh random seeds and once more by the closure.

**Do-nothing and discrimination receipts** (`controls/c1-controls.txt`, `controls/c1-reference.txt`,
seed 61001): base 7/20; `exit 0` stub 1/20; `exit 2` stub 14/20; the base builder that also prints the
target token `LEGS=20/20 C1=PASS` 7/20 (the verdict is not read from output); a naive-guard builder
(refuse any non-empty `--out`) 10/20; the reference builder `controls/ref-build-spans.py`
(sha256 `86d64c31…eccfd`) 20/20 at seeds 61001–61003; 14 frozen mutants M01–M14 of the reference each
fail exactly the legs named in `controls/run-c1-controls.py` (`CONTROLS_UNEXPECTED=0`). A target no
do-nothing reaches: the best stub scores 14/20.

**No-harm check** (not a target; part of admission): `python3 corpus/evidence/round61/regress.py --work <dir>`
re-derives the committed span sets of rounds 55, 56 and 57/c3 against the lane-owned store
`corpus/captures/`: `REAL_REBUILD=3/3` at base (`controls/regress-base.txt`) and with the reference
(`controls/regress-reference.txt`); it must still read `3/3` on the landed builder.

**Kill rule** (frozen): C1 is verified only when the landed builder reads 20/20 at all three fresh seeds
and `REAL_REBUILD=3/3`. Any seed below 20/20, or a regress leg failing, is an honest stop — not narrowed
after landing. A wave seat's demonstration that a hazard class outside the 20 legs still reaches the
landed builder is routed as a counter limit, not a refutation.

**Named limits** (disclosed before data): (i) the guards check, then write — a process that swaps a
directory for a link between the two is not stopped (TOCTOU; entry `Limits`); (ii) the 64 MiB caps are
the lane's choice, not a measured need beyond "the largest real `.txt` is 15 MB and `.raw` 40 MB"
(R55W2SentBuilder §2); (iii) the memory leg checks one 192 MiB read, not the sum over many rows;
(iv) the row-count × form-size cost (R55W2SentBuilder §5) is not a leg.

## C2 — depth (sourced): derived-output safety, grounded in sources opened this round

Target axis: depth (verifiable technical detail, cited sources). This is the round's sourced claim:
the entry cites the registry rows S134, S135, S136, each opened in this round (2026-10-28).

**Predicate R61-C2** (the sentence in the docstring of `corpus/evidence/round61/c2-count.py`): in the lane
tree the file `corpus/knowledge/derived-output-safety-r61.md` exists and carries TRIO, ROWS, QUOTES,
COVERAGE, CLAIMS, LIMITS and CENSUS as that docstring defines them — counted
`ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=k/k COVERAGE=1/1 CLAIMS=1/1 LIMITS=1/1 CENSUS=1/1 C2=PASS`.

Counting command: `python3 corpus/evidence/round61/c2-count.py` (lane root; reads `man`/`col` and the census script).

**Before**: `ENTRY=0/1 … ROWS=0/3 … C2=FAIL` exit 1 (`controls/c2-before.txt`). **After target**: `C2=PASS` exit 0
at the landing commit with 8 located quotes (the positive control in `controls/c2-positive-entry.md` has 8:
S134 ×3, S135 ×3, S136 ×2).

**Discrimination receipts** (`controls/c2-controls.txt`): the absent entry, absent rows, a fabricated quote,
a quote bound to the wrong row, an uncited quote, a queued row, a stale `opened`, a row not used-by the
entry, a missing Limits section, a junk claim, an over-25-word quote and a missing provenance line each
FAIL; the positive control PASSES; **a claim that echoes its quote also PASSES** — recorded limit: the
counter is structural and does not judge that a claim follows from its quotes (non-author reviewers do,
and the closure re-reads the claims against the rendered man pages).

**Kill rule** (frozen): C2 is verified only when the counter prints `C2=PASS` exit 0 on the landed commit
and the entry, rows and quotes landed are the ones the counter read (no counter edit after data). The
registry rows S134–S137 are appended by the L1 only, after their sources were opened (S134, S135 by
`man -l` on the installed pages, package man-pages 6.19-1; S136, S137 as lane files); S137 is a rejected
own-work row (the builder docstring is intent, not evidence) and gives the round's Gate its reject.

**Access disclosure**: S134 and S135 were opened from the installed manual pages (no network); their
canonical man7.org HTML renders were not opened this round and the rows carry no URL.

## Amendment A1 (before dispatch; no seat had run)

An L1 self-attack on the first-frozen counter found three forge routes that needed no guard in the
builder: (1) the 18 leg groups ran in a fixed order, so a builder that counted its own invocations in a
shared file knew which leg it was in; (2) a timed-out or finished builder's process group was not killed,
so a detached helper could alter a tree after its leg's run and before the snapshot; (3) stdout and
stderr were unbounded. Counter changes, all in `c1-count.py` and its docstring, none in the predicate
sentence, targets, kill rule or controls' expectations: the leg groups run in a seeded shuffle; each child
gets its own session, a 512 MiB file-size limit and a process-group kill when its run ends; stderr is read
to 64 KiB. Controls were re-run on the amended counter (receipts replaced; the first-freeze versions are
in the first freeze commit). Admission add-on: the sweep
`grep -nE 'getppid|/proc/|c1-count|round61|leg-|argv\[0\]' tools/build-spans.py` must exit 1 (no match)
on the landed builder — a builder that detects the counter is not a measurement; the sweep ran on the
reference builder at this amendment: exit 1 (`controls/sniff-sweep.txt`).

## Not claimed

No exploratory claim. No change to the operability 3/10 observable. No external fetch this round
(fetch-scope L0 `8d77e6c1` remains open). No assimilation (`Assimilation: none`). Freshness, coverage,
calibration and adjacency claim nothing beyond what the report's trend verdicts state.

## Files frozen by this commit

`c1-count.py` (amended, A1) `f1d8b6fd…cfff9ef`; `c2-count.py` `6bd864b9…518b6`; `regress.py` `50b94d46…7e738`;
`controls/` (stubs are generated by `controls/run-c1-controls.py` `bcca093e…b5624`, `controls/run-c2-controls.py`
`a5296f19…abecc3f`, positive entry `15857b2f…de84`, positive rows `721a108b…d701dc`, reference builder `86d64c31…eccfd`).
