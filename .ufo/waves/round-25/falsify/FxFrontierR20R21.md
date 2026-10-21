# FxFrontierR20R21 — freshness falsify

Reviewed the integrated Frontier at `e93ac711f885a10d44fdd80a1734997419595b5a` in private clone `/tmp/chousa-r25-FxFrontierR20R21` (observed HEAD/base: same hash). No production files changed.

## Findings (severity order)

### Medium — battery is not a green hold; qualification missing
`corpus/README.md:706-710,730-733` places the masked-battery result among “holds”; it says the round reported identity but omits the historical `root=.` / DRIFT limitation. Both retained battery receipts show `mode=verify-all ... root=.` (`corpus/evidence/verify-r20-20261019T180000Z-battery.log:113`; `ptr-r21-20261019T184000Z-battery.log:113`), then `VERIFY_ALL ... drift-sections=3 findings=13 drift=13` and `RESEARCH_GATE: DRIFT` (both `:132-133`). Thus “ALL IDENTICAL” is output identity, not a clean battery; the separate `--drift` receipts do say `GATE_DRIFT: none` (r20/r21 drift logs `:1`). Correct the paragraphs to name this limitation. This also contradicts `LOG.md:873-878`, especially “the new Frontier paragraphs mark those qualifications” at `:875`; `corpus/lessons/round-25.md:50-57` records the same requirement.

### Medium — two R20/R21 hold claims have no matching retained result
The paragraphs repeat `r1 VERDICT_BEARING_EXPORTS=3/3` (`corpus/README.md:709,732`), matching `SCORECARD.md:1044,1099` and `LOG.md:762,780`, but neither indexed round receipt group has a `VERDICT_BEARING_EXPORTS` result. The A/B/C lines in each battery are `archives-r9` `verify` records (`...battery.log:1-6`), not the r1 count command (`SCORECARD.md:29`). Likewise, the evidence index lists one landed battery receipt per round (`corpus/evidence/README.md:1000-1005,1014-1019`), not a retained pre-round output/comparison receipt; my `cmp` found the two landed battery logs identical, which does not establish identity to the missing pre-round output. These remain round-reported, not independently receipt-backed; qualify them as such rather than presenting them as reproduced holds.

### Low — R20 selftest case provenance is incomplete
`corpus/README.md:706-708` correctly gives 122→124 and the r18 comparison boundary 1–119, but skips case 123's provenance. Receipts show r19 cases 120–122 (`corpus/evidence/symlink-r19-20261019T174500Z-selftest.log:120-123`), then R20 case 123 `claims-cap-eof` and case 124 `scope-comment-shadow` (`verify-r20-20261019T180000Z-selftest.log:123-125`); SCORECARD says case 123 was prior-session work absorbed by R20 (`SCORECARD.md:1040-1042`). Say explicitly that case 123 is carried prior-session work and case 124 is the R20 pin. R21 numbering is consistent: cases 125–128 and PASS 128 (`ptr-r21-...-selftest.log:125-129`); its stated 1–124 comparator matches SCORECARD `:1092-1098`.

## Checks that matched / residual risk

- Wave/routing/report counts match the verdicts: R20 64/64, openai-codex gpt-6-luna-max (`SCORECARD.md:1016-1018`, `LOG.md:757`); R21 32/32, opencode-go-6 / deepseek-v4.1-flash (`SCORECARD.md:1082-1084`, `LOG.md:776`). Demo CLEAN→DRIFT findings and selftest totals match the receipts.
- SHA checks in the private clone: `git show 2bb556b:tools/research-gate.sh | sha256sum` = `9f1638076915…`; `83b806a` = `49b36759bc47…`; `b057245` = `49b36759bc47…`; `07c425e` = `bfc291ef5260…`. These match the Frontier and SCORECARD transitions. R21's open `.config` path-start bypass and the note contradiction are accurately described at `corpus/README.md:736-739`; `pointer-boundary-r21.md:25-29`, `denylist-r22.md:25-26`, and SCORECARD `:1107` corroborate it.
- Checkpoint corrections retained: initial `0fc037e` omitted the gate and its 154-case prose described a 136-case gate; intermediate `d8c8cff` fixed the gate but still omitted `corpus/evidence/README.md` (LOG `:882-896`; lesson `:109-133`). Full review pin is e93, not either intermediate. Full-pin gate digest observed: `63a39282a15f…`.

## Verification gaps

No gate/selftest suite was run. Read-only receipt/index/note review, historical blob SHA checks, and `cmp` of the two retained battery files only. No LSP route was exposed for these Markdown files; no grep result is used as semantic proof. No tools installed.

VERDICT: Request the three paragraph corrections above; other checked R20/R21 counts, gate transitions, demos, and the R21 named-debt qualification align with the receipts and verdict records.