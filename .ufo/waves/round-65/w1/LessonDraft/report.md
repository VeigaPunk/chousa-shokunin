# Round65 LessonDraft — drafted `## Gate` and `## Mistakes` for corpus/lessons/round-65.md

Seat: `LessonDraft` (scribe, leaf — no subagent dispatch). Lane root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Date: 2026-10-30. Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd` (lane HEAD), base `d6ed8155e9b4735639a2cf0a3e479c62f2056195`.
Task: draft round65 Gate and Mistakes covering the two round64 routed items — the non-self-pinned before receipt and the registry omissions — with captured-by and fix; claim no outside review.

Axes (godspeed): coverage (both routed items become rows with evidence), calibration (captured-by cells name what existed and what did not), operability (draft pastes into the lesson without new instruments), honesty (no result or outside-review claim exceeds observed bytes).

## 1. What this seat observed (all reads; nothing executed against targets)

Git state (read-only, explicit `-C`): HEAD = `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`; `git status --porcelain` shows modified `SCORECARD.md`, `SKILL.md`, `corpus/QUALITY.md`, `corpus/README.md`, `corpus/SOURCES.md` and untracked `.ufo/waves/round-65/*`, `corpus/evidence/round65/source-openings.json`, `corpus/knowledge/receipt-identity-r65.md`, `corpus/lessons/round-65.md`. `git diff --stat` = 20 insertions, 0 deletions across those five files; the `SOURCES.md` diff is exactly four added rows (S154–S157); row count `grep -c '^| S'` = 157 (153→157); no held status/recheck/used-by cell changed. The freeze tree contains `corpus/evidence/round65/{c1-count.py,c2-count.py,claims.md,controls/}` and the three round64 instruments `c3-count.py`, `c1-battery-supplement.py`, `run-receipts-v3.py`. `tools/receipt-pin.py` does not exist yet (glob: path not found) — it is the frozen C1 acquisition target, not a landed artifact.

Round64 routed items (verbatim location, `corpus/lessons/round-64-verifier-spotcheck.md`):
- item 2 (line 74): "**c3-count.py unregistered** (minor): the round-64 counters (`c3-count.py`, `c1-battery-supplement.py`, runner) are report-cited evidence and QUALITY 128's red-before oracle but hold no own `## Gates` row (r62 registered per-round counters). Register or record an explicit honest-stop exemption next round."
- item 3 (line 75): "**Before-receipt self-containment** (minor): `c1v3-before-full.txt` lacks a `REVISION=`/`EXIT=` header; provenance rides `claims.md`. Future before-receipts should self-pin."
- item 1 (line 73): row 157 self-test literal lacks the frozen expected-output token. item 4 (line 76): report pointer ambiguity lane-vs-fleet repo. items 5–6: SHONEN boxes; CT carried pointer.

Non-self-pinned receipt, observed bytes: `corpus/evidence/round64/controls/c1v3-before-full.txt` line 1 `LEG CLEAN clean ok ok`; line 44 `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`; no `REVISION=`/`EXIT=` header anywhere in the file. By contrast the new frozen-era controls self-pin: `corpus/evidence/round65/controls/c1-before.txt` carries `REVISION=d6ed8155e9b4735639a2cf0a3e479c62f2056195`, `EXIT=1`, `ARGV=[...]`, then `CASES=0/20 C1=FAIL missing-target`; `c1-positive.txt` carries `REVISION=`/`EXIT=0` and `CASES=20/20 C1=PASS`; `c2-before.txt` carries `ENTRY_CHECKS=0/10 C2=FAIL`.

Captured-by candidates checked: `corpus/QUALITY.md:321-327` (QUALITY 42) binds receipts to committed gate bytes via `gate_sha256` and flags UNBOUND receipts labelled landed/final in a wave dir — a different relation, not an in-file self-header requirement. Per-round counter registrations exist since at least round 42–45 (`SKILL.md:110-113`). No criterion required the r64 before receipt to self-pin; none required evidence-only counters to hold a Gates row.

Registry rows observed (`corpus/SOURCES.md:164-167`): S154 git-cat-file(1) docs A mined; S155 hashlib module docs A mined; S156 r64 before receipt own-work B mined; S157 ref-receipt-pin docstring own-work C **rejected**. `corpus/evidence/round65/source-openings.json` pins id/path/accessed 2026-10-30/sha256/location/quote for all four. Knowledge entry `corpus/knowledge/receipt-identity-r65.md` (untracked) cites S154–S156, distinguishes object identity, content digest, reported exit and execution authenticity, and states the outside-reviewer obligation. `SKILL.md` working tree adds rows 158 (`round64 honest-stop instruments (r65 registration)` — evidence-only exemption naming the three instruments with retained frozen literals), 159 (`receipt-pin (r65)` gate), 160 (`round65 claim counters` gate with controls).

Frozen claims (`corpus/evidence/round65/claims.md`): exactly two claims (C1 operability, C2 depth sourced); C1 format = ordered `REVISION` 40 lowercase hex / `EXIT` 0–255 / `SHA256` 64 lowercase hex + canonical relative POSIX path / empty separator / nonempty body; digest binds the Git blob at the declared revision; revision must equal caller `--revision`; no working-tree hashing; exits 0/1/2; "No changes to old frozen counters"; "Round64's minor registry/provenance items are supporting corrections, not additional claims"; missed targets are unprovable/not admitted, never rewritten.

This seat ran no counter, no battery, no validator, no network fetch, made no git/jj mutation, installed nothing (none needed), created no scratch (nothing to delete), and wrote only its seat outputs. Nothing below claims C1/C2 results — L1 verifies once after integration.

## 2. DRAFT — `## Gate` (for corpus/lessons/round-65.md; L1 integrates)

```markdown
## Gate

Admit corpus/knowledge/receipt-identity-r65.md narrowly: interpreting this lane's own research
receipts — object identity, content digest, reported exit and execution authenticity are
distinguished — not general orchestration and not cryptographic attestation; no round-1
receipt-identity debt is resolved. Reject the inference that a consistent header proves an
execution (S157; flip: independent evidence binding command, bytes and result). Outside
non-author spot-check remains required and has not occurred; wave seats dispatched by this
lane are still lane-authored evidence. Suggested sample for that later check: admit S155,
reject S157.

| row | URL/path opened 2026-10-30 | location and <=25-word quote | words | decision |
|---|---|---|---|---|
| S154 | file:///usr/share/man/man1/git-cat-file.1.gz | Git 2.56.0 manual dated 2026-09-27, OUTPUT: "If <type> is specified, the raw (though uncompressed) contents of the object will be returned." | 15 | admit A for object-content selection at an explicit type; the validator requests blob at a caller-supplied revision and path |
| S155 | /usr/lib/python3.14/hashlib.py (Python 3.14.8) | module documentation lines 31–32: "Return the digest of the bytes passed to the update() method" | 11 | admit A for installed digest semantics; a matching SHA256 binds reported digest to blob bytes, not who ran a command |
| S156 | corpus/evidence/round64/controls/c1v3-before-full.txt | line 1: "LEG CLEAN clean ok ok"; line 44 is the failed aggregate `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL` | 5 | admit B for receipt text shape — a verdict-bearing body can omit self-contained revision/exit/digest headers; not historical execution authenticity |
| S157 | corpus/evidence/round65/controls/ref-receipt-pin.py | module docstring first sentence: "Validate receipt header consistency, not execution authenticity." | 7 | reject C as execution proof; flip: cite independent process evidence binding command, bytes and result |

Registry: 153→157 rows; new A2/B1/C1, mined3/rejected1. No held status/recheck/used-by cell
changed. `source-openings.json` carries id/path/accessed/sha256/location/quote for all four.
Search question: what does a receipt's digest actually establish? Local installed
manual/module and lane evidence only; identified 4, screened 4, included 3, excluded 1;
stop because these settle object/digest interpretation, not execution proof. No network
fetch and no live-target approval is assumed.

Frozen predicates (unchanged after freeze; a missed target is unprovable, not rewritten):
R65-C1 `python3 corpus/evidence/round65/c1-count.py --work <fresh-dir>` → `CASES=20/20
C1=PASS` exit 0 against `tools/receipt-pin.py` (before control `CASES=0/20` exit 1;
positive control 20/20 exit 0 on the prefreeze reference `controls/ref-receipt-pin.py`;
always-pass 3/20 and always-fail 17/20, both exit 1). R65-C2 `python3
corpus/evidence/round65/c2-count.py` → `ENTRY_CHECKS=10/10 C2=PASS` exit 0 (before
`0/10` exit 1; do-nothing fails). C1 is interface/consistency coverage — never execution
authentication or parser safety; C2 is structural — no entailment claim. Numeric score
remains historical 3/10. Round64's minor registry/provenance items are supporting
corrections, not additional claims.

Scope: this lane interprets and checks its own research evidence; generic testing stays
adjacent to tameshi, dispatch/receipt lifecycle to kumitate.
```

## 3. DRAFT — `## Mistakes` (for corpus/lessons/round-65.md; L1 integrates)

```markdown
## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| Round64 before receipt is not self-pinning: no in-file REVISION/EXIT/digest header, provenance rides the surrounding claims file | corpus/evidence/round64/controls/c1v3-before-full.txt:1,44 (line 1 `LEG CLEAN clean ok ok`, line 44 `CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL`, no header line); routed as round64 verifier spotcheck §5 item 3 (corpus/lessons/round-64-verifier-spotcheck.md:75); opened this round as S156 | none at the time — QUALITY 42 (corpus/QUALITY.md:321-327) binds receipts to committed gate bytes via gate_sha256 for wave-dir receipts labelled landed/final, a different relation, and no r64 instrument or criterion required an in-file header | acquire tools/receipt-pin.py per frozen C1: ordered REVISION (40 lowercase hex, equal to caller --revision), EXIT (0–255), SHA256 (64 lowercase hex) binding the Git blob at the declared revision plus canonical relative POSIX path, empty separator, nonempty body; no working-tree hashing; exits 0 consistent / 1 invalid / 2 usage. Red-before: the retained r64 receipt and the frozen missing-header controls (c1-before.txt 0/20; always-pass 3/20, always-fail 17/20); positive 20/20 runs the prefreeze reference. The old receipt stays byte-identical; the fix cannot retrospectively authenticate it, and consistency is not authenticity (S157) |
| Round64 evidence-only counters hold no gate-registry row | corpus/lessons/round-64-verifier-spotcheck.md:74: c3-count.py, c1-battery-supplement.py and the receipts runner (corpus/evidence/round64/run-receipts-v3.py, all present in the freeze tree) are report-cited evidence and QUALITY 128's red-before oracle with no own ## Gates row, against the per-round registration practice (SKILL.md:110-113 rounds 42–45) | none at the time — no criterion made evidence-only counters registrable; the duty was r62+ precedent, and QUALITY 128 cites the counters as oracle without a registration requirement | append an explicit evidence-only honest-stop registration naming the three instruments with retained frozen literals (`CLEAN=1/1 DEFECTS=28/28 BENIGN=9/11 ZERO=3/3 BATTERY=FAIL`; `RELOCATION_MATCH=0/3 C3=FAIL`; supplement `BATTERY=PASS` never substitutes for a frozen failure) and the rule "historical evidence; never admission gates for a successor" (drafted at SKILL.md:158 working tree). No new general detector claimed; old failed predicates unchanged |

Prior closure routed items (supporting corrections, not additional claims): item 1 — the
frozen C1 output token is appended to the adjacent historical instrument row (SKILL.md:157
working tree), no historical measurement rewritten; item 4 — report pointers name the lane
repo unless stated fleet; items 5–6 — SHONEN stays four author assertions and CT-20261026-4
stays carried, no outside-review credit claimed.
```

## 4. Boundaries, conflicts, and limits

- No outside review is claimed anywhere in the drafts; the Gate text states the outside non-author spot-check is required and has not occurred.
- No C1/C2 result is claimed: no target validator exists in the tree at draft time (`tools/receipt-pin.py` absent), no counter was executed by this seat, and per bounds L1 verifies once after integration.
- The SOURCES/SKILL/QUALITY/README/SCORECARD changes and `round-65.md`, `receipt-identity-r65.md` are uncommitted L1 working-tree planning as observed by this seat; rows 158–160 and S154–S157 are cited from that working tree, marked as such.
- Conflicts with L1's uncommitted `corpus/lessons/round-65.md` preliminary draft: none on facts (registry 153→157, both mistakes, S154–S157 decisions, controls agree). Wording deltas for L1's integration choice: (a) my captured-by cells argue "none at the time" with the QUALITY 42 and precedent analysis, where the preliminary draft says "gate registry completeness duty" for row 2; (b) I fold spotcheck items 1/4 into a "supporting corrections" paragraph inside Mistakes; (c) my Gate table adds a measured word-count column (15/11/5/7, seat-measured over the pinned quotes).
- Scratch `/fast/scratch/hyaku/chousa-r65/LessonDraft/` was never created; nothing to delete. Installs/updates: none. No pacman, no service restarts, no network, no git/jj mutation (read-only `git -C` only), no fleet/sibling/source-tree writes.

## 5. Self-evaluation (delivery reflection, not admission)

Accuracy 4/5 — every pointer is a byte-level read this turn; working-tree vs frozen status is explicit. Completeness 4/5 — both routed items covered with captured-by and fail-capable fixes; items 1/4 kept as corrections; nothing executed, so no result claimed. Clarity 4/5 — drafts paste-ready; provenance separated from lesson text. Actionability 4/5 — L1 can integrate or take the named wording deltas. Conciseness 4/5 — evidence section repeats a few quote strings so the drafts stand alone. Mean 4.0/5.
