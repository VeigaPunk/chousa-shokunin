# FrontierR20R21 — draft `## Frontier` paragraphs, rounds 20 and 21

Scope: draft only. Paragraphs are for insertion in `corpus/README.md` `## Frontier` after the Round 10 paragraph (`corpus/README.md:457–485`) and before `Still open …` (`:487`). Nothing in the live lane was edited.

## Draft paragraph — Round 20

Round 20 ran an adversarial re-audit of the boundary stack that rounds 15–19 had landed, as one 64-seat AgentSwarm call on openai-codex gpt-6-luna-max (64/64 seat reports). Its finding was the HTML-comment heading shadow: `load_sections` parsed a `## Meta` inside `<!-- -->` as a real heading, so a record whose real Meta declared a refused province plus a commented in-province Meta closed CLEAN. The before→after observable is the demo pair: at the pre-round gate `2bb556b` (blob `9f163807…`) the shadowed record closes `RESEARCH_GATE: CLEAN`; at the landed gate (blob `49b36759…`) it refuses `SCOPE_BOUNTY_ABSORBED` (warn) and closes `DRIFT (findings=1 drift=1 …)`. The fix tracks `in_comment` beside `fence_char`, checking fence state first and comment state before the heading arm. The holds: selftest `PASS (124 cases, 0 skipped)`, up from 122, with cases 1–119 byte-identical to the r18 receipt and case 124 pinning the new arm; `--drift` against the r12 baseline `GATE_DRIFT: none` with no re-pin; r1 `VERDICT_BEARING_EXPORTS=3/3`; and the masked battery, which the round reports identical to the pre-round gate. That observable is not saturated: the fix closes the comment arm at the class the wave found and nothing wider — the parser is not a Markdown renderer, so CDATA, processing instructions and other HTML constructs stay outside the declared-record contract. The `ptr_resolves_meta` escape, the `.config` path-start denylist bypass, the fenced-heading chain anchor and about ten scope/inflection gaps were dispositioned as named debt for round 21, not closed, and the drift ritual proves the output surface only.

Citations (Round 20):
- 64-seat wave, routing, seat count: `SCORECARD.md:1016–1017`; `LOG.md:757`.
- Finding, pre-round gate `9f163807…`, landed gate `49b36759…`: `SCORECARD.md:1020–1027`; `LOG.md:759`.
- Pre-round gate is commit `2bb556b`: `corpus/evidence/verify-r20-20261019T180000Z-demo.log:1`. Blob check (read-only `git show 2bb556b:tools/research-gate.sh | sha256sum`) = `9f16380769…`; `83b806a` blob = `49b36759bc…` (matches `LOG.md:762`).
- Demo: CLEAN `…-demo.log:3`; FINDING `:7`; DRIFT `:8`.
- Pre-round gate has no comment state: `git show 2bb556b:tools/research-gate.sh | grep -c in_comment` = 0. Landed gate: `in_comment` at `tools/research-gate.sh:425,439,451` (live lane, sha `752e4e38…`; the landed blob has the same arm).
- Selftest before 122: `corpus/evidence/README.md:652` (`symlink-r19-…-selftest.log`, `PASS (122 cases)`).
- Selftest after 124: `corpus/evidence/verify-r20-20261019T180000Z-selftest.log:124` (`ok-case 124 scope-comment-shadow`), `:125` (`PASS (124 cases, 0 skipped)`).
- Cases 1–119 vs r18 receipt: `cmp` of the first 119 lines against `corpus/evidence/scope-r18-20261019T173000Z-selftest.log` = identical (checked for this draft).
- Drift: `corpus/evidence/verify-r20-20261019T180000Z-drift.log:1` (`GATE_DRIFT: none`).
- r1 3/3: `SCORECARD.md:1044`; counting command `SCORECARD.md:29`; re-run for this draft at the landed blob (`83b806a`/`bfc291ef` path, see findings) gave `VERDICT_BEARING_EXPORTS=3/3`.
- Masked battery "identical": asserted at `LOG.md:762` and `SCORECARD.md:1043–1044`; receipt `verify-r20-…-battery.log` holds the landed output only (see findings).
- Named limits: `knowledge/html-comment-r20.md:9–13`, `:17–22`, `:24–32`; named debt `LOG.md:761`; `SCORECARD.md:1037–1040`.

## Draft paragraph — Round 21

Round 21 ran the round-20 named-debt move on the pointer boundary, as one 32-seat AgentSwarm call on opencode-go-6 / deepseek-v4.1-flash (32/32 seat reports). `ptr_resolves_meta` tested relative pointers with a raw `-f`, so `lib/../../r21-outside.txt` passed CLEAN whenever the file existed under the raw path. The before→after observable is the demo pair: the pre-round gate `b057245` (blob `49b36759…`) closes CLEAN on the traversal pointer; the landed gate (blob `bfc291ef…`) refuses it with `POINTER_UNRESOLVED` (warn) and closes DRIFT. The fix canonicalizes the candidate with `readlink -f`, checks `in_root` against both roots, and applies the denylist to the canonical target, so a benign symlink to `.config/passwd` is refused; cases 125–128 pin traversal, symlink, lane-root absolute pointer (now exit 0) and the `.config` symlink. The holds: selftest `PASS (128 cases, 0 skipped)`, up from 124, with cases 1–124 byte-identical to the r20 receipt; `--drift` `GATE_DRIFT: none` with no re-pin; r1 `VERDICT_BEARING_EXPORTS=3/3`; and the masked battery, which the round reports identical to the pre-round gate. That observable is not saturated: canonicalization shows that a pointer resolves to a readable file inside a root and outside the denylist, not that the file is the cited source or supports the claim. The `.config` path-start form stayed open at r21 — the r21 note states it as closed in one bullet and still bypassing in the next — and round 22 closed it (`knowledge/denylist-r22.md`); the fenced-heading chain anchor stayed named debt until round 23 (`knowledge/fenced-anchor-r23.md`). The round's demo is one traversal instance, not a measured fraction of the pointer space.

Citations (Round 21):
- 32-seat wave, routing, seat count: `SCORECARD.md:1082–1084`; `LOG.md:776`.
- Defect `-f` without canonicalization: `SCORECARD.md:1086–1088`; `knowledge/pointer-boundary-r21.md:9–11`.
- Pre-round gate is commit `b057245`: `corpus/evidence/ptr-r21-20261019T184000Z-demo.log:1`. Blob check (`git show b057245:tools/research-gate.sh | sha256sum`) = `49b36759bc…`. Landed blob `07c425e` = `bfc291ef52…` (`LOG.md:789`).
- Demo: CLEAN `ptr-r21-…-demo.log:3`; FINDING `:7`; DRIFT `:8`.
- Landed gate fix at `bfc291ef`: `ptr_resolves_meta` starts `:591`; `readlink -f` `:617`; `in_root` against both roots `:619` (`git show 07c425e:tools/research-gate.sh`). Fix contract: `knowledge/pointer-boundary-r21.md:16–21`.
- Selftest before 124: `corpus/evidence/verify-r20-20261019T180000Z-selftest.log:125`; after 128: `ptr-r21-…-selftest.log:129`; cases 125–128 at `:125–128`.
- Cases 1–124 vs r20 receipt: `cmp` of the first 124 lines = identical (checked for this draft).
- Drift: `corpus/evidence/ptr-r21-20261019T184000Z-drift.log:1`.
- r1 3/3: `SCORECARD.md:1099`; re-run for this draft: `VERDICT_BEARING_EXPORTS=3/3` at blob `bfc291ef` and at blob `49b36759` (`/tmp` copies; lane not written).
- Masked battery: `ptr-r21-…-battery.log` is byte-identical to `verify-r20-…-battery.log` (checked); "identical vs pre-round" asserted at `SCORECARD.md:1098`, `LOG.md:780`.
- Limits: `knowledge/pointer-boundary-r21.md:25–27` vs `:28–29` (contradiction); `:30–32` (fenced anchor); `knowledge/denylist-r22.md:25–26` (r21 check does not cover raw path-start form); `knowledge/fenced-anchor-r23.md:1–3`; `corpus/README.md:28`.

## Findings (path:line or command+output)

1. Counting-command receipt gap (r20 and r21). `VERDICT_BEARING_EXPORTS` appears in no `verify-r20-*` or `ptr-r21-*` receipt; the r20/r21 battery `A/B/C` lines (`verify-r20-…-battery.log:2,4,6`) are CLEAN on `archives-r9` records, a different surface. The `3/3` in `SCORECARD.md:1044,1099` and `LOG.md:762,780` is therefore not receipt-backed. Draft figure reproduced in `/tmp/r25f-FrontierR20R21`: `VERDICT_BEARING_EXPORTS=3/3` at gate blobs `49b36759…` and `bfc291ef…` (non-receipt).
2. Masked-battery "identical to pre-round" is not receipted. Only landed-state battery output is stored; comparison is asserted (`SCORECARD.md:1043–1044`, `:1098`; `LOG.md:762`, `:780`). Verified only: r20 battery == r21 battery (`cmp`).
3. Internal contradiction in `knowledge/pointer-boundary-r21.md:25–29`: bullet 1 says the `.config` path-start bypass "is closed by the canonical check"; bullet 2 says a direct `.config/foo` citation "still bypasses". `knowledge/denylist-r22.md:25–26` and `SCORECARD.md:1107` support "open at r21". Draft follows the latter; the r21 note needs a correction (not edited here).
4. Demo labels use commit ids (`2bb556b`, `b057245`); SCORECARD/LOG use blob-sha prefixes. Mapping verified above (`2bb556b`→`9f163807…`, `b057245`→`49b36759…`, `83b806a`→`49b36759…`, `07c425e`→`bfc291ef…`).
5. Live gate has moved on: `tools/research-gate.sh` sha `752e4e38…`, 5290 lines (`sha256sum`). Line cites above are to the pinned landed blobs, not live lines (e.g. `ptr_resolves_meta` is `:595` live).
6. README Frontier gap: `corpus/README.md` has Round 10 (`:457`) then Round 24 (`:491`); rounds 11–23 have no paragraphs. Out of this draft's scope; the two paragraphs slot at `:486`.
7. Pre-round selftest counts check out: r19 `PASS (122)` (`evidence/README.md:652`) and r20 `PASS (124)` (`verify-r20-…-selftest.log:125`).

## Installs / tools

None. Read-only `git show` and `sha256sum`; `cp` of `research/` and a gate blob into `/tmp/r25f-FrontierR20R21` for the r1 re-run and `cmp` checks. No live-lane, fleet or host writes.

VERDICT: both paragraphs drafted with grounded numbers; r1 3/3 and masked-battery identity are reproduced/derived here but are not receipt-backed in the repo; r21 knowledge note contradicts itself on the `.config` bypass.
