# CritErratum — r49 w2 FALSIFY: the post-freeze span-builder change

Seat: CritErratum (leaf, no subagents). Scratch `/dev/shm/chousa-r49-CritErratum/`
(created, deleted at end). Lane read-only; only write is this file. No installs.
Item: `corpus/evidence/round49/claims-erratum.md` — `build-spans.py` changed after
wave-1 seats scored (freeze `fe740e78` → adoption `1254ab26`). Is the counter or predicate changed, and is
CR-clipping a measurement change that rescues C2?

## 1. Nothing frozen moved — counter, predicate, target, kill rule byte-identical

```
$ for f in c1-count.py c2-count.py claims.md; do  # sha256 at freeze/adopt/4ce61fc/worktree
c1-count.py   freeze=83589bf89048b47d adopt=83589bf89048b47d tool=83589bf89048b47d worktree=83589bf89048b47d SAME
c2-count.py   freeze=9d2fb3806e368a34 adopt=9d2fb3806e368a34 tool=9d2fb3806e368a34 worktree=9d2fb3806e368a34 SAME
claims.md     freeze=0c1f172870b9f422 adopt=0c1f172870b9f422 tool=0c1f172870b9f422 worktree=0c1f172870b9f422 SAME
$ git diff --stat fe740e78 1254ab26 -- .../build-spans.py .../c1-count.py .../c2-count.py .../claims.md
 corpus/evidence/round49/build-spans.py | 15 ++++++++++++++-
 1 file changed, 14 insertions(+), 1 deletion(-)
$ sha256 tools/inference-ground.py   freeze=fa2b4eb5fc29b4dd  tip=fa2b4eb5fc29b4dd
```
`quotes.tsv` 7e659d081d4f, `spans.tsv` f698c2e8ac51 and both entries 19c27ccb6227 hash identically at
`1254ab26`, `4ce61fc5`, `87e93353` and in the worktree — the C2 input set did not move after the commit carrying
the disclosure. `git diff --stat 1254ab26 4ce61fc5` = `SKILL.md`, `tools/assimilate-rows.py` only.

## 2. Replay: 21/28 before, 28/28 after — the builder is the only variable

Scratch roots hold copies of exactly what `c2-count.py` reads (`corpus/SOURCES.md`, both entries,
`corpus/lessons/round-49.md`, `quotes.tsv`, `tools/inference-ground.py`); the lane's frozen counter runs with
`--root`. Both builds use the SAME worktree `quotes.tsv`, so the only difference is the builder.

```
$ git show fe740e78:.../build-spans.py > pre-build-spans.py   # fed672dd56d628fa
$ cp .../build-spans.py post-build-spans.py                    # 02b2dc83de1f4971
   (hashes equal MutSpans w1 provenance: pre-repair fed672dd, post-repair 02b2dc83)
$ python3 pre-build-spans.py  --root $S/pre   → SPANS_ROWS=28 WRITTEN=28  exit 0
$ python3 post-build-spans.py --root $S/post  → SPANS_ROWS=28 WRITTEN=28  exit 0
$ diff -r $S/post/.../spans lane/.../spans && diff $S/post/.../spans.tsv lane/.../spans.tsv
   → SPANS_IDENTICAL / TSV_IDENTICAL   (post builder == committed state)
$ python3 corpus/evidence/round49/c2-count.py --root $S/pre
ENTRIES=2/2 · BOUND=8/9 REFUSED=1 · REF_ID_UNBOUND=0 · QUOTE_ROWS=28 ON_BOUND=28/28
SPAN_IDS=8/8 · QUOTES_IN_SPAN=28/28 · QUOTES_IN_ENTRY=28/28 · QUOTES_IN_LESSON=28/28
QUOTE_SHORT=28/28 · SPAN_CONTEXT=28/28 · CAPTURE_BOUND=21/28 · ANCHOR_BOUND=8/8
INFERENCE_GROUNDED=2/2 · QUARANTINE_VERDICTS=5/5 · QUARANTINE_BLOCKED_ADOPTED=0
C2=FAIL          (exit 1)
$ python3 corpus/evidence/round49/c2-count.py --root $S/post
... identical except CAPTURE_BOUND=28/28 ... C2=PASS (exit 0)
```

## 3. The seven failures are exactly the seven CR-bearing `.raw` spans

```
$ diff -rq pre/spans post/spans → 7 files differ (S100-1..3, S101-1,2,4,5); S101-3 identical
raw span bytes:  S100-1 CR=2  S100-2 CR=6  S100-3 CR=9  S101-1 CR=1
                 S101-2 CR=2  S101-3 CR=0  S101-4 CR=3  S101-5 CR=2
pre CR_total=25 LF_total=254 ; post CR_total=0 LF_total=254
```
1:1 correlation — the only `.raw` row with no CR is the only `.raw` row that passed. Root cause at
`c2-count.py:168` (`p.read_text`, universal newlines) vs `c2-count.py:108` (`b.decode("utf-16le")`, CR kept),
compared at `c2-count.py:181`.

**All 28 pre-change spans were already exact BYTE slices** of their form at their recorded offset
(`ft[off:off+len(span_raw)] == span_raw` with newline translation disabled: 28/28 True; under the counter's own
text read: 21/28). 21/28 is an instrument asymmetry on the read side, not a span that was not a slice.

## 4. Post-change spans are still real slices — and the leg still bites

```
post spans: byte-exact slice 28/28, len(span) > len(quote) 28/28
context chars around quote: S100-1 L=0 R=80 | S100-2 L=8 R=1 | S100-3 L=80 R=34
  S101-1 L=39 R=80 | S101-2 L=4 R=80 | S101-3 L=80 R=80 | S101-4 L=48 R=0
  S101-5 L=4 R=80 ; every .txt row L=R=80
```
Two rows now carry context on one side only and S100-2's span shrank 199→48 chars. No frozen leg measures
context width, so no leg is lost — but this is a real narrowing of what "context" means for `.doc` rows.
Mutation of the repaired artifact (one context char, S100-1 idx 104 `-`→`X`): `QUOTES_IN_SPAN=28/28
SPAN_CONTEXT=28/28 CAPTURE_BOUND=27/28 C2=FAIL` exit 1 — clipping does not make CAPTURE_BOUND vacuous for `.raw`
rows.

## 5. The quote replacement is load-bearing, and the erratum misstates it

The paragraph form is recoverable exactly: `ft.rfind("\r",0,1431)+1 = 1423`, a 48-char paragraph `关于自引的说明：` +
body(39) + `。` — matching the erratum's `1423 → 1431` (1423+8 = 1431 = `len("关于自引的说明：")`).

```
$ post builder on a quotes.tsv reverted to the paragraph quote
build-spans: refused S100: capture b539a80218080da56a75b624.raw holds no context around
  '关于自引的说明：对于合作发文的参考文献中，如果引文出现了任一合作者，那么这条引文将被认定为自引。'
EXIT=1 ; spans written=0 ; spans.tsv absent
```
The S100 quote had to change for a manifest to exist at all: CR clipping leaves a whole-paragraph quote zero
context and `build-spans.py:139` refuses `span == quote`. So the disclosure's "What did not change … No quote,
document or verdict was added or dropped to pass the leg" is false in substance — one quote was replaced, and
that replacement is required to pass. It contradicts the erratum's own Repair bullet: an internal misstatement,
not concealment, but the clause the closure would rely on is wrong.

Calibration on the erratum's own number: with the paragraph quote the state also fails `QUOTES_IN_LESSON=27/28`
(the lesson quotes the body fragment, `corpus/lessons/round-49.md:151`) and `ANCHOR_BOUND=7/8` (registry anchor
is `char 1431`, `corpus/SOURCES.md:110`). That state was incoherent mid-authoring; the erratum's 21/28 is the
coherent pre-change state (current quote set + freeze builder), which is what §2 reproduces.

## 6. Latent constraint the closure should record

For an OLE `.doc` capture a quote that is a whole paragraph (or the whole document) is unquotable under the
frozen read: clipping removes all context and the builder refuses. The instrument therefore constrains quote
selection for `.doc` rows. The shortened quote here is a verbatim sentence and a substring of the paragraph, so
no evidentiary content was lost (the dropped prefix is the heading), but a future `.doc` row cannot cite a
paragraph as its quote without failing the build. Depth/calibration note, not a leg failure.

## Judgment

C2 stands. Counter, predicate, target and kill rule are byte-unchanged; the pre-change spans already satisfied
the predicate's "exact slice of the capture text form" clause in bytes, so 21/28 was the counter's text-mode
read, not a data defect; the repair removes only characters that read cannot round-trip, and the repaired spans
were verified byte-exact, longer than their quotes, and still killed by a one-char context mutation. Not a pure
no-op: context narrows (two rows one-sided) and one quote was replaced to fit the clip, so the closure must
record that the C2 after-state is measured on a manifest repaired after seats scored, and the erratum needs an
append-only correction of its "no quote added or dropped" clause. The one-sentence C2 predicate holds; the
disclosure's self-description does not.

VERDICT: post-freeze `build-spans.py` CR-clipping — holds (C2 stands; counters and predicate byte-unchanged, 21/28 reproduced as a text-mode read artifact on spans that were already exact byte slices, 28/28 verified exact after) — with one correction required: the erratum's "no quote added or dropped" clause is false, the S100 paragraph quote was replaced and that replacement is load-bearing.
