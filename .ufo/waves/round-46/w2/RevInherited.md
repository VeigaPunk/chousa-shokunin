# RevInherited — round-46 wave 2: inherited state, lane tip, round records at `d09fc8e7`

Leaf seat, measurements 2026-10-25 07:26–07:42 -03:00. Two immutable anchors, because
the lane moved during the seat: **A** = `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`
(`git archive` → `/tmp/chousa-r46w2-RevInherited/landing`), **B** =
`3807537db7e731af508ad7f7d5462f4422ce04c8` (tip from 07:36). Frozen claims read first at
`corpus/evidence/round46/claims.md`; no predicate, target or kill rule is amended below —
disagreements are reported as disagreements. Wave-1 findings (`CritC1Attack`,
`CritC2Framing`, `junk-borrowed`) are not re-reported.

## 1. Inherited state — CONFIRMED untouched

    07:26 and again 07:41, identical:
    c4e00d1141a0faaf0dfd655b9173ef974b702d668efd9751caab78658e3fb0d0  .ufo/waves/round-40/w1/swarm-registry.json
    49b059533008951e54dc2e4c03ecf0b5352e1ec30eaf7af512e516be07bc4b59  .ufo/waves/round-41/w1/swarm-registry.json
    1f5c0afae8024c50013e9a9060988c14506115125e3823042e4512833f293b80  corpus/evidence/round41/receipts/cells/cells.json

`cells.json` equals the round-45 restore hash (`round-45.md:70-75`). The registries have
no recorded digest; their `git diff --numstat` is `36 34` and `427 214`, identical to
`corpus/evidence/round44/disposition.tsv:37-38`, mtimes `2026-10-24 04:18:06`/`04:42:46`.
`[INFERENCE]` byte-identical to the round-44 left-named state; the diff-vs-HEAD *is* that
state (HEAD's `cells.json` is the `1bd9001` committed rewrite, the worktree copy restored).

## 2. Lane tip and `jj-lane.sh state` — the tip moved during wave 2

    /home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/chousa-shokunin
    07:27 local=d09fc8e7… tracked=18 untracked=5 · 07:36 local=3807537… tracked=3 untracked=0 · 07:41 local=3807537… tracked=11 untracked=15

`3807537` ("round-46: wave-2 corrections … SCORECARD verdict, lesson, LOG") landed at
07:36, **inside wave 2**, so a seat re-running now measures a different tree. Both pass,
but the C1 tool bytes differ three ways: `A = 819f83ebdc6c6b47` (A's `measure-after.txt:4`
agrees), `B = 3018b1d25d762054` (B's agrees), worktree at 07:38 = `7736688bdefe9df0`
(uncommitted). Every record matches its own commit; none matches the live tree.

## 3. Round records at A — every counting command re-run

    cd /tmp/chousa-r46w2-RevInherited/landing
    corpus/evidence/round46/c1-count.py            → TOOL=present POSITIVE_PASS=3/3 JUNK_KILLED=3/3 C1=PASS exit=0
    corpus/evidence/round46/c2-count.py --list     → ENTRY_POINTS=72 (tools=8 counters=50 named=70) GATES_ROWS=35 REGISTERED=72/72 UNREGISTERED=0 C2=PASS exit=0
    corpus/evidence/round46/c3-count.py            → ENTRIES=2/2 CITES_BOUND=5/5 QUOTE_ROWS=11/11 QUOTES_IN_SPAN=11/11 QUOTES_IN_ENTRY=11/11 CAPTURE_BOUND=11/11 REF_ID_UNBOUND=0 REF_BOUND=2/2 C3=PASS exit=0
    corpus/evidence/round46/c3-count.py --lane-only→ same, CAPTURE_BOUND=skipped, C3=PASS exit=0
    corpus/evidence/round46/build-spans.py --check → SPANS_ROWS=11 STALE=0 exit=0

All three declared targets reproduce verbatim at A; C3's `CAPTURE_BOUND=11/11` re-derives
each of the eleven spans against the on-disk captures, and all eight C1 `PINNED` digests
equal the `c2f0e9d1` blobs (blob-by-blob, 8/8). At B: `ENTRY_POINTS=73 (tools=8 counters=50
named=71) REGISTERED=73/73 UNREGISTERED=0 C2=PASS`.

## 4. Attacks on the record

**F1 — A has no verdict record (record completeness).** In A, `grep -n 'round-46\|R46'`
matches nothing in `SCORECARD.md` or `LOG.md`, and `corpus/lessons/round-46.md` is absent;
the verdict rows (`SCORECARD.md:2459,2469,2478`), LOG entry and lesson are all in **B**.
So "the landing" attacked here carries code and evidence but no verdict; the verdict
travelled in a commit whose message calls itself "wave-2 corrections". A wave-2 artefact
was landed by the round's own L1 before wave 2 closed — record timing, not a claim failure.

**F2 — `controls/c2-before.txt` tree B contradicts itself and is unreproducible.** It
labels tree B "the bare base tree … (no round-46 counters)" with `ENTRY_POINTS=71
(tools=7 counters=50 named=69) … UNREGISTERED=16`, then lists three
`UNREGISTERED_PATH corpus/evidence/round46/c*-count.py` — files it says are absent. The
real base (`--root base`, base = `git archive 6e2630a6`) gives `ENTRY_POINTS=68 (tools=7
counters=47 named=66) GATES_ROWS=30 REGISTERED=55/68 UNREGISTERED=13 C2=FAIL exit=1`.

Both before rows were captured on a transient mid-wave worktree (counters present, tool
absent) that no commit contains; neither 71 nor `named=69` re-derives. Direction intact
(68→72, 55/68→72/72); the recorded leg is testimony.

**F3 — `controls/c2-controls.txt` records a PASSING control, and it reproduces.** Its
last run `--skill <SKILL-7pipe.md>` → `GATES_ROWS=31 REGISTERED=71/71 UNREGISTERED=0
C2=PASS exit=0`. The claims' control sentence lists four refusal classes and never says
one passes. Reproduced on the landed counter: one `## Gates` row
`| a | b | c | d | e | <all 72 paths in one cell> | exit 0 ok |` →
`GATES_ROWS=1 REGISTERED=72/72 UNREGISTERED=0 C2=PASS exit=0`; the same content as prose,
as a 5/6-pipe row, as an 8-pipe row without `exit`, and as a valid row after the next
`## ` heading all stay `UNREGISTERED=72` exit 1 (four mutants, built and run). The
counter's "cheapest gate" paragraph says pasting paths "into a one-cell row [is] refused"
— true for one cell, false for the 7-cell row holding the same paste. C2 is not falsified
(the frozen sentence is literally met), but the anti-forge argument, the claim's control
list and the round's own control file are all incomplete or counterexamples.

**F4 — C1's discriminating control is a placeholder.** A's `controls/c1-controls.txt`
invokes `--tool <always-exit-0 forge>` and `<citation-presence-only forge>`; no such file
and no digest of one exists in the tree (`grep -rln 'always-pass.py\|cite-only.py\|
always-exit-0' … --include=*.py` matches only the two wave-spec generators), so the control
separating the real tool from a cheap gate cannot be re-executed from A. Target met;
control testimonial.

**F5 — C1's pin covers 8 of the 10 fixture files (minor, not silent).** The comment says
"every fixture name is bound to the bytes frozen at `c2f0e9d1`", but `grep -c 'spans/'
c1-count.py` → 0: `spans/S901-1.txt`, `spans/S902-1.txt` are unpinned. Emptying one on a
copy of A gives `POSITIVE_PASS=1/3 JUNK_KILLED=3/3 C1=FAIL exit=1` — not caught by
`FIXTURES_CHANGED`, but it flips the verdict, so the kill rule is enforced indirectly.

**F6 — C2's denominator is prose-sensitive between A and B.** `…/round46/build-spans.py`
is committed at A and registered in A's Gates row (`SKILL.md:117`), yet is
not an entry point at A (72): set (C) needs the path in `SCORECARD.md` or a `claims*.md`,
and A's SCORECARD omits it. B added `SCORECARD.md:2480` → 73, no counter change. Set
difference: `landing 72, wt 73; wt-only: ['…/build-spans.py']`; the `≥71` floor holds but
the census is not stable.

**F7 — `SKILL.md:116` at B advertises an invocation tool and counter do not use.** B row:
`--entry PATH --spans TSV --counts JSON --registry corpus/SOURCES.md …` (unbracketed =
required). Tool at B: `ap.add_argument("--registry", default=None)`, usage still bracketed
(`tools/inference-ground.py:29`), and `c1-count.py:66-67` passes no registry; at A the row
was bracketed and consistent, so B's "correction" made the row stricter than the tool.

## 5. Attribution of uncommitted paths (three snapshots; the 07:36 middle one commits every
wave-1 late write — `--name-only` adds `LOG.md`, `SCORECARD.md`, `corpus/lessons/round-46.md`,
`measure-after.txt`, `w2/swarm-registry.json` — leaving untracked 0)

| snapshot | inherited | wave-1 late work | new (wave 2) |
|---|---|---|---|
| 07:27, tip A | the 3 JSONs | 17 tracked: 9 `w1/*.md`, `SKILL.md`, `corpus/SOURCES.md`, 2 knowledge entries, `tools/inference-ground.py`; plus 5 untracked round-46 scaffolding files | none |
| 07:41, tip B | the 3 JSONs | all committed by `3807537` | 8 `w2/*.md` reports (`??`) + 8 tracked edits after B: `c1-count.py` (new `CANARY` leg, `8473abf6…`), `controls/c1-before.txt`, `controls/c1-controls.txt`, `corpus/lessons/round-46.md` (entries 13–14), `SCORECARD.md`, `tools/inference-ground.py` (`7736688b…`), `w1/ExecCounterRun.md`, `w1/MutC2Forge.md` |

The three inherited JSONs are the only dirty paths surviving every snapshot. The live
edits are others' in-flight work: I wrote only this file; every mutation ran on `/tmp`
copies (`landing`, `mut2`, `base`, `ctl`, all removed); shokuknow untouched.

## 6. Verdicts

- Inherited state: **CONFIRMED untouched** (hashes stable across the seat).
- Lane tip: A at start, **B from 07:36**; tree changed under measurement (jj 18→3→11); §3 is anchored to A.
- C1/C2/C3: **no falsification** — all declared targets reproduce at A; residuals are
  record/control defects F1–F7, none lowers a frozen leg. No rule was changed here.
- Unknowns: whether B's tool (`3018b1d2`) and the worktree `CANARY` counter (`8473abf6`)
  were ever scored against the frozen controls (records name `819f83eb`/`819287e2`); the
  `spans/*.txt` pin coverage; the transient "tree A/B" behind `c2-before.txt`.
