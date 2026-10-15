# chousa-shokunin — Iteration Log

- 2026-10-14 — round 0: minted as shonen (sibling mint; rationale in MINT.md).

## 2026-10-15 — boundary parity fix (round 1 integration prep)

`ScopeBoundary` found a contradiction in the mint artifacts: `MINT.md` and the
roster scan (`mint-roster-scan.json`) explicitly rejected **kumitate** as a
complementary province, but the `PROVINCE.md` and `SKILL.md` refusal clauses this
lane wrote omitted it. Closed here — both files now name orchestration,
multi-agent dispatch and agent lifecycle as refused (→ kumitate). Recorded rather
than silently patched, because the omission had already propagated into peer
proposals (`QualityBar` Q-BOUND, `ApprovalTable`), and the proposed gate vocabulary
classified `SCOPE_ORCHESTRATION_ABSORBED` as `info` where the other two absorbed-
scope ids are `warn` — a severity asymmetry that would let an absorbed orchestration
record pass as CLEAN. **Landing requirement:** that id must be elevated to `warn`
so all three refused provinces have identical gate teeth, with one symmetric
selftest fixture per province asserting exit 1.

## 2026-10-15 — research gate landed (not field-ready)

`tools/research-gate.sh` landed from the round-1 design (994 lines). Two design bugs
were found and fixed while landing:

1. `local sec=$1 line body=${SEC_BODY[$sec]-}` — `local` expands every right-hand
   side before assigning, so `$sec` was unset and `set -u` aborted; **13 of 17**
   selftest cases died on `line 165: sec: unbound variable`. Split the declaration.
2. `ROOT` was captured once at load from the ambient `CHOUSA_ROOT`, but the hermetic
   suite exports it per case and calls `verify_record` as a function — so every
   `lib/…:N` pointer read "missing under CHOUSA_ROOT" and both PASS controls failed.
   `verify_record` now re-reads the env.

After both: `bash tools/research-gate.sh --selftest` → **`RESEARCH_GATE_SELFTEST:
PASS (17 cases)`** exit 0, and the suite's own secrecy case confirms a planted
`sk-` value is not echoed.

**Carried defect, named:** on a real chat-export input the gate exits 1 with **no
verdict line** — an unchecked `grep` under `set -e` ends the script before the
summary. Not field-ready; unblock is to `|| true` every non-fatal `grep` and re-run
the suite plus the real artifact.

### Citation-shift notice (appended 2026-10-15)

The boundary-parity fix inserted **3 lines** into `SKILL.md` at 39–41 (the kumitate
refusal). Every line number below that point moved by +3: the checklist heading is
now `SKILL.md:44` and the four rules are `:46`–`:49` (sweep rule at `:47`), where
the wave's seats cite the pre-edit numbers. **Round-1 citations to `SKILL.md:44` or
later are pre-edit** and must be re-derived before being trusted — the rules
themselves are unchanged. This notice also fixed the lane's own guard, which cited
`SKILL.md:45` for the observation/inference/unknown split; the live line is `:48`.

Also recorded from the same audit: `RuleOrProposal` found several wave-internal
citations that resolve to the wrong lines (QUALITY item numbers used as line numbers;
`claim-ledger.sh:45-48` cited for stamp status where the live lines are `:15-16`;
export chips treated as URLs; `README.md:6-8` credited with a four-tier hierarchy it
does not state). Those are wave-report defects, not lane defects, and they are the
reason the corpus landing must re-derive every citation rather than copy one.
