# ConnectorOverlap — round 34 wave 1 (chousa-shokunin)

## Scope checked
- Lanes scanned (read-only): top-level `*-shokunin/PROVINCE.md` and `*-shokunin/SCORECARD.md` under `/home/vgpnk/Projects/shokunin/`. Sandboxes/worktrees excluded.
- Chousa inputs: `corpus/evidence/round34/claims.md`, `corpus/lessons/round-33-verifier-spotcheck.md:155-173`, `PROVINCE.md`.

## Lane ownership map (adjacent surfaces)
| Concern | Owning lane(s) | Evidence |
|---|---|---|
| Host OS / argv / exec substrate (execve(2), MAX_ARG_STRLEN) | tsukuroi-shokunin (host operability; OS state) | `tsukuroi-shokunin/PROVINCE.md` Core: "pacman state, systemd, drivers/firmware, boot health"; "Detection and report; the operator remediates." |
| Reverse engineering of shipped artifacts (REA, ELF/ASAR) | kaidoku-shokunin, revenger-shokunin | `kaidoku-shokunin/PROVINCE.md` Domain line; `revenger-shokunin/PROVINCE.md` Domain line |
| Bounty-program scope and claim packages | kasegi-shokunin | `chousa-shokunin/PROVINCE.md:10` refuses → kasegi |
| Model-quality / evaluation claims | kengaku-shokunin | `chousa-shokunin/PROVINCE.md:10-11` refuses → kengaku |
| Orchestration, multi-agent dispatch, agent lifecycle, receipt identity | kumitate-shokunin | `chousa-shokunin/PROVINCE.md:11-12` refuses → kumitate; `kumitate-shokunin/PROVINCE.md` Domain line |
| Secrets / custody | kagi-shokunin | `chousa-shokunin/PROVINCE.md:14` refuses → kagi |
| Fleet artifact census / receipt taxonomy / hygiene | souji-shokunin | `souji-shokunin/PROVINCE.md` Owns: "fleet repository & workspace hygiene … receipt-gated removal"; capability rows `fleet census (receipt taxonomy)` |
| Declared-plan JSON safety gate (mado-action-plan reads plan JSON, never executes argv) | mado-shokunin | `mado-shokunin/PROVINCE.md` tool table row for `tools/mado-action-plan.py` |
| Skill/prompt craft | kotoba-shokunin | `kotodama-shokunin/PROVINCE.md` refuses "prompt/skill craft (kotoba)"; `kotoba-shokunin/PROVINCE.md` Domain line |
| Verification method (mutation testing) | tameshi-shokunin | `tameshi-shokunin/PROVINCE.md` Owns: reusable craft |

## Findings
1. No sibling lane owns "grep/PCRE tooling" or "argv/exec limits" as a domain. tsukuroi owns the host OS substrate that defines MAX_ARG_STRLEN; chousa only cites the Linux man-pages execve(2) row as a source (`corpus/evidence/round34/claims.md:92-94`). No absorption.
2. JSON parsing: mado owns declared-plan JSON safety; kumitate owns orchestration scripts. Chousa's claim-record field parsing (round-33 C1) and C1 span matching operate on chousa's own claim records / gate, within "claim-vs-source verification" + "this lane's own corpus and gates" (`PROVINCE.md:5-8`).
3. Receipt-binding: souji owns fleet-level receipt taxonomy/census; chousa's E1/E4 binding of fuzz/measurement receipts to committed gate bytes is gate hygiene on chousa's own gate. Fleet-level receipt binding stays souji's; chousa reports, does not absorb (`PROVINCE.md:17` "Out of province → report, never absorb.").
4. Claim packages (kasegi) and model-quality (kengaku) are explicitly refused by chousa; C1 is method (verify-claims), not package/quality claims. No absorption.
5. Skill craft (kotoba): E3 stale `SKILL.md:83` range is chousa's own research-method skill; chousa owns its content. If cross-lane skill conventions are implicated, report to kotoba rather than absorb.

## Verdict on adjacency
Chousa's C1 claim and E1–E5 repairs do NOT absorb another lane's scope. They remain inside province: claim-vs-source verification + this lane's own corpus and gates. Adjacent lanes to report to (not absorb):
- tsukuroi: host OS fact citation only (no mutation).
- kasegi: method is reusable; bounty claim packages stay kasegi's.
- kumitate: receipt identity / orchestration stays kumitate's (chousa's receipt-binding debt is reported).
- souji: fleet receipt taxonomy stays souji's; chousa's gate-receipt binding is lane-local.
- kotoba: skill craft stays kotoba's; chousa owns its SKILL content.

## Province check
`chousa-shokunin/PROVINCE.md:3-8` Owns includes "claim-vs-source verification" and "this lane's own corpus and gates"; Refuses list (lines 10-15) names kasegi, kengaku, kumitate, external live-target, kagi — none of C1 or E1–E5 fall under a refusal. Conclusion: the work is described as in province. "Out of province → report, never absorb." (line 17) is the operative clause for any cross-lane evidence.

## Limits
- Read-only scan of top-level PROVINCE.md/SCORECARD.md; no lane repo mutated. No counter run. Evidence by path:line only.