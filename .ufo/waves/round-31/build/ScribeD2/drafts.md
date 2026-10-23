# D2 append-only corrections — ready to paste

## 1. `corpus/lessons/round-30.md`

**Insertion point:** after current line 128 (the final `ReviewKnowledge30.md` line) and before `## Learning` (currently line 130). Append; do not rewrite lines 100–105.

**Ready-to-paste block:**

### 2026-10-23 correction (round 31, D2)

The statement above that the frozen harness's listen queue overflowed reports a cause as fact. The backlog explanation is **[INFERENCE]**, not established: `RerunC2B.md:45` labels the diagnosis `[INFERENCE]`, and `:57` says no per-connection record shows a dropped or delayed SYN. The 18/18 backlog-128 control is consistent with, but does not prove, that explanation (`.ufo/waves/round-30/falsify/RerunC2B.md:49-50`). Round-31 copies: `.ufo/waves/round-31/build/ExecD2Backlog/bl/`. The scored C2 misses remain misses under the frozen kill rule; this correction changes neither the result nor the frozen v4 bytes. Any future C2 counter version that sets `request_queue_size` must be declared before data as a new version; never edit the frozen v4 bytes. This append-only correction answers D2 in `corpus/lessons/round-30-verifier-spotcheck.md:169-174`.

**Evidence for the correction:** `RerunC2B.md:45,49-50,57`; its recorded scored command is `timeout 300 python3 corpus/evidence/round30/c2-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/falsify/RerunC2B/run{N}.json`. The recorded run2/run4 receipts each show 26/27, exit 1; the 18 original backlog-control receipts at `/fast/scratch/hyaku/chousa-r30/w2/RerunC2B/bl/bl{1..18}.json` each returned `n=27`, `t=27`, `predicate_holds=true` when read. The receipt result supports the contrast, not causal attribution.

## 2. `SCORECARD.md`

**Insertion point:** after current line 1707 (the last row in `## Capabilities (round-30 change)`) and before `## Planned — round 31 (not started)` (currently line 1709). Append; do not rewrite the Round 30 C2 row.

**Ready-to-paste block:**

### 2026-10-23 correction (round 31, D2)

The backlog-5 explanation in the Round 30 C2 row above is **[INFERENCE]**, not an established cause. `RerunC2B.md:45,57` labels it `[INFERENCE]` and states that no per-connection record shows a dropped or delayed SYN. The 18/18 backlog-128 control is consistent with the explanation but not conclusive (`.ufo/waves/round-30/falsify/RerunC2B.md:49-50`). Round-31 copies: `.ufo/waves/round-31/build/ExecD2Backlog/bl/`. The C2 verdict remains “not met (miss under the kill rule)”; the control does not re-scale it or change the frozen v4 bytes. Any future C2 counter version that sets `request_queue_size` must be declared before data as a new version; never edit the frozen v4 bytes. This append-only correction answers D2 in `corpus/lessons/round-30-verifier-spotcheck.md:169-174`.

**Evidence for the correction:** `RerunC2B.md:45,49-50,57`; the recorded `timeout 300 python3 corpus/evidence/round30/c2-count.py --receipt …/RerunC2B/run{N}.json` command produced two scored misses documented by `run2.json` and `run4.json` (26/27, exit 1). Each of the 18 original backlog-control receipts under `/fast/scratch/hyaku/chousa-r30/w2/RerunC2B/bl/` has `n=27`, `t=27`, `predicate_holds=true`. The inference label and missing per-connection evidence are explicit in RerunC2B; the 18/18 result does not prove the queue was the cause.
