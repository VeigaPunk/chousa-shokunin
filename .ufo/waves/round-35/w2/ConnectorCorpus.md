# ConnectorCorpus — corpus overlap audit for the round-35 knowledge entries

Seat: chousa-r35-w2-ConnectorCorpus (leaf, connector). Date: 2026-10-23.
Gate scored/pinned: `tools/research-gate.sh` sha256 `1f2fb4f522d9a670b49dd61ad1369f55ee012f3b0d38050654be45a71aaef617` (re-derived, see below).
No installs. No lane file written except this report; artifact: `verify-metadata-knowledge.log` in this directory.

## What I did

- Read the frozen round-35 design first, in order: `corpus/evidence/round35/claims.md`,
  `c1-count.py`, `c2-count.py`, `tools/mechanism-witness.py`, `.ufo/waves/round-35/repairs/slen-probe.sh`.
- Read the title + first 15 lines of **all 44 files** in `corpus/knowledge/` (directory listing
  via glob; three r35 entries read in full); read the names of all 38 files in `corpus/lessons/`
  and targeted-grepped the lessons tree for each of the three facts.
- Ran the lane's own screen once, read-only:
  `timeout 120 bash tools/research-gate.sh verify-metadata corpus/knowledge --root . --registry corpus/SOURCES.md`
  → `METADATA_COMPLETE=37/44`, exit 1 (receipt: `.ufo/waves/round-35/w2/ConnectorCorpus/verify-metadata-knowledge.log`,
  sha256 `b53a4b9c…f5fc`). `sha256sum tools/research-gate.sh` → `1f2fb4f5…ef617` (matches the landed pin).

## (a) Dynamic-scope `local a=$1 b=${#a}` hazard — ALREADY STATED, only in one entry

`corpus/knowledge/bash-local-expansion-r35.md` (read in full) states the general rule, quoted
2026-10-23: "Bash expands **all** of a `local`/`declare` statement's right-hand sides before it
assigns any of the names." and the repro `f() { local a=$1 b=${#a}; echo "$b"; }` / `f hello # prints 0`,
plus the sweep rule ("a derived value never shares one `local` statement with the name it derives from")
and the r34 latent shipment.

No other knowledge entry covers it (grep for `local a=$1|dynamic scope|expands every right-hand|slen=\$\{#`
hits only this file). No lesson states the general hazard: the only prior statements are the routed-defect
rows in the frozen round-34 records — `corpus/lessons/round-34.md:123` ("`tok_span_offsets_chunk` binds
`slen` from its local `span` at declaration; renaming the local would fall back to the caller's dynamic
`span` and silently mis-confirm") and `corpus/lessons/round-34-verifier-spotcheck.md:86`. Those name the
one specific coupling; they do not state the general expansion-order rule, the repro, or the sweep rule.

## (b) PATH-resolved tool provenance — ALREADY STATED, only in one entry

`corpus/knowledge/grep-pin-r35.md` (read in full) states the class, quoted 2026-10-23: "The gate called
bare `grep` at each matcher site, so the binary that ran was a function of the caller's environment",
with the three mechanisms (PATH first / `exec*p()`; imported `$BASH_ENV` functions; no-grep-no-gate),
the `RESEARCH_GATE_GREP` absolute+GNU verification, the exit-2 `GREP_PROVENANCE` refusal, and the
self-reported-provenance limit.

No other knowledge entry covers it (grep for `PATH first|BASH_ENV|exec\*p|RESEARCH_GATE_GREP|GREP_PROVENANCE`
hits only this file). Lessons carry only the routed-defect note: `corpus/lessons/round-34.md:122` and
`corpus/lessons/round-34-verifier-spotcheck.md:85` (host `/usr/bin/grep` self-reports pi-uu-grep 0.2.0;
"r35: pin the grep binary path in runbooks and verify `grep --version` provenance"). That is a hazard
routing, not the general provenance statement.

## (c) Output-equivalence vs mechanism witnesses — ALREADY STATED, one entry + one prior lesson row

`corpus/knowledge/keyed-engine-output-equivalence-r35.md` (read in full) states the class, quoted
2026-10-23: "a counter that scores only a program's printed verdicts cannot tell two programs apart when
both implement the written contract", with the three key sub-classes (fixture-shape / location / record-label),
the three defenses (per-seed fixture unpredictability, the out-of-band `bash -x` mechanism witness, the
stated limit), and the r35 measured evidence (2/2 separation, stub controls).

One earlier statement exists, in a frozen lesson: `corpus/lessons/round-34.md:119` — "Output-only counters
cannot exclude a fixture-keyed engine that implements the exact semantics (it is output-equivalent); pure
lookups without semantics ARE caught". That row is the fact's first statement; its r35 follow-up column
planned a *different* defense ("work-proof battery (tracer/strace invocation-class checks)") than what
landed (the bash -x PS4 trace witness in `tools/mechanism-witness.py`). No other knowledge entry covers it
(grep hits only the r35 entry).

## Supersede vs duplicate — the verdict this seat is asked for

For all three facts a knowledge entry **already exists and is content-complete**. Therefore:

1. The L1 must NOT author any new knowledge entry restating (a), (b), or (c) — that would duplicate
   against `bash-local-expansion-r35.md`, `grep-pin-r35.md`, `keyed-engine-output-equivalence-r35.md`.
2. For (c) specifically, the existing r35 entry is correctly a **superseder**, not a peer, of the
   round-34 lesson row: it keeps the fact, replaces the planned tracer/strace design with the landed
   witness design, and carries the receipts. The lesson row stays frozen as the historical record;
   the knowledge entry is the canonical, re-checkable statement. The same relation holds for (a) and
   (b) versus their round-34 routed-defect rows, one layer down (lessons named the defect; the entries
   state the general rule).
3. Second-order finding (operability/calibration, the non-obvious move): all three r35 entries **fail
   the lane's own metadata screen**. My verify-metadata run reports for each of the three:
   `source=absent verified_at=absent recheck=absent verdict=drift` (nine `META_*_ABSENT severity=warn`
   findings; `METADATA_COMPLETE=37/44`, 7 drift entries of which exactly 3 are this round's). Per
   `corpus/knowledge/metadata-screen-r25.md` (QUALITY criterion 6), every admitted `knowledge/` entry
   owes `source:` / `verified-at:` / `recheck:`. The bounded closeout move is to **complete the three
   header blocks in place** (the entries already cite their sources in prose — S067/S068 man pages, the
   round-35 counters and receipts — so this is transcription, not new research), which converts the three
   r35 rows from `drift` to `clean` and raises the cohort to 40/44 without touching content. That is a
   gap fix to the existing entries, not a new entry; it improves operability (re-checkable headers) and
   calibration (the screen's verdict then matches the entries' actual evidence) and harms no claim, repair,
   or counter. The other four drifts (`dead-zone-pcre-r34.md`, `archives-verified-r9.md`, `audit-r11.md`,
   `gate-baseline-r8.md`) pre-date round 35 and are outside this wave's scope.

## Evidence index

- Coverage: glob of `corpus/knowledge/` (44 files) and `corpus/lessons/` (38 files); reads as above.
- Quotes: `corpus/knowledge/bash-local-expansion-r35.md:9-19,24-27,46-47,55-57`; `corpus/knowledge/grep-pin-r35.md:9-21,37-50,70-71`; `corpus/knowledge/keyed-engine-output-equivalence-r35.md:13-18,31-35`; `corpus/lessons/round-34.md:119,122-123`; `corpus/lessons/round-34-verifier-spotcheck.md:85-86` (all accessed 2026-10-23).
- Commands: `verify-metadata` run (command + rc=1 quoted above; full log at `.ufo/waves/round-35/w2/ConnectorCorpus/verify-metadata-knowledge.log`, sha256 `b53a4b9c…f5fc`); `sha256sum tools/research-gate.sh` → `1f2fb4f5…ef617`.

## Limits

- Lessons were covered by full-name listing plus targeted greps (patterns quoted above), not full-text reads
  of all 38; the greps hit every lesson that mentions scope/PATH/witness terms, and the three hits were read
  in context. First-15-lines coverage of knowledge entries was per the task spec; the three on-topic entries
  were read in full.
- The metadata-gap recommendation is a connector proposal; the L1 decides landing. No counter, claim file,
  or tool was modified; verify-metadata is a read-only mode.
