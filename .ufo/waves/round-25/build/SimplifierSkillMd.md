# SimplifierSkillMd — SKILL.md calibration (round 25, claim 3)

**Seat:** ChousaR25Recovery.SimplifierSkillMd-3 (read-only; lane untouched)  
**Base:** `b820e4e` / claims `corpus/evidence/round25-claims.md` (C3 calibration)

## Godspeed axes

1. **Calibration** — restated ledger tuples/queue vs owning file  
2. **Single authority** — counts live in `hardening-r10.md`, not SKILL  
3. **Closure hygiene** — no “remains open” for r12-closed C3  
4. **Verifiability** — named re-derive command (QUALITY.md criterion 9)

## Findings (before)

| ID | Evidence |
|----|----------|
| 3a | `SKILL.md:438` — `remains open pending fix-or-absorb` (C3 closed r12; `hardening-r10.md:433-437`) |
| 3b | `SKILL.md:381-384` — tuples `38·23·7·0·3`, queue 26/27-item; `SKILL.md:435-436` — `38·22·3·1·4`, 27-item |
| Owner | Latest counts: `corpus/knowledge/hardening-r10.md:549-551` → **38·21·10·0·3**, queue **24** (last `Counts at this revision`) |
| Counter | `bash corpus/evidence/round25-measure.sh /home/vgpnk/Projects/shokunin/chousa-shokunin` → `3a=1`, `3b` tuples stale 3/3 queue 2/2, `STALE_RESTATEMENTS=15` |

Simulated post-patch SKILL-only: `3a=0`, `3b` tuple/queue stale 0/0 (Python replay of measure §3 logic).

## Proposed unified diff (minimal; integration applies)

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -378,10 +378,8 @@
 one `blocked-no-fetch` hop and one exempt `from` token per record — are
 audited against the archive bytes (6/6 justified, 0 findings, under the
 unchanged exemption rule), and every limit named across rounds 2–9 stands
-dispositioned in `corpus/knowledge/hardening-r10.md` — 71 rows at the r12 revision (by-design 38 · carried 23 · closed 7 · finding 0 · operator 3, queue 26 — `hardening-r10.md` §6) (that
-set plus the r1-origin debts and the rows this round surfaced): by-design 38 ·
-carried 23 · closed 7 · finding 0 · operator 3 — with the 27-item round-11
-audit queue.
+dispositioned in `corpus/knowledge/hardening-r10.md` (that set plus the
+r1-origin debts and the rows later rounds surfaced).
 
 **Limits.** `verify` CLEAN is declared record structure and file-pointer
 identity only — that path never opens the source a pointer resolves to.
@@ -432,8 +430,9 @@
 non-author corpus spot-check or promotion is implied by a passing selftest.
 
 The limits named across rounds 2–9 are collected with one disposition each in
-`corpus/knowledge/hardening-r10.md` — by-design 38 · carried 22 · closed 3 ·
-finding 1 · operator 4 — together with the 27-item round-11 audit queue; a
-disposition is a record, not a gate change, and the one live finding
-(`A-r9.md:50` row C3 cites `A:76` while its span occurs at `A:86`) remains
-open pending fix-or-absorb.
+`corpus/knowledge/hardening-r10.md`; authoritative disposition counts and the
+round-11 audit queue size are the file's latest **Counts at this revision**
+line (re-derive: `bash corpus/evidence/round25-measure.sh <tree-root>` → claim
+3 `3b`/`STALE_RESTATEMENTS`, or
+`grep -n 'Counts at this revision' corpus/knowledge/hardening-r10.md | tail -1`).
+A disposition is a record, not a gate change.
```

**Preserved:** archive controls paragraph, entire **Limits** mode prose, scope-refusal sentence, “disposition is a record…” (minus stale tail).  
**Out of scope here:** `3c` `${GSHA}` and `3d` missing r16–r23 addenda in `hardening-r10.md` (writer seat).

## Installs

None.

VERDICT: One-pointer patch clears SKILL 3a/3b stale restatements; land diff via ChousaR25Recovery integration.
