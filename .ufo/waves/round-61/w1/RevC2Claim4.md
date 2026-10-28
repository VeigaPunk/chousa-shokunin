# RevC2Claim4 — entailment review of Claim 4 (round 61, wave w1)

Scope: Claim 4 of `corpus/evidence/round61/controls/c2-positive-entry.md` only, and its quotes Q5 and Q6 (S135, rename(2)).
Method: rendered the page myself with `MANWIDTH=1000 man -l /usr/share/man/man2/rename.2.gz | col -bx` (scratch copy, deleted before yield; 210 lines). Read the full DESCRIPTION paragraphs around each quote. Checked the quotes verbatim with a Python substring test on the rendered text. No network, no writes outside my report and scratch, no git mutation.

## The claim as written

> Claim 4. The replacement is atomic for readers of the final name, yet a window exists in which both names refer to the same file, so a failed run can leave the temporary name behind and cleanup belongs on the error path. [Q5, Q6]

## Quotes, located in context

Both quotes are present verbatim (`Q5 True 23 words`, `Q6 True 19 words`). They sit in one paragraph, DESCRIPTION, rename.2 line 38:

> If newpath already exists, it will be atomically replaced, so that there is no point at which another process attempting to access newpath will find it missing. However, there will probably be a window in which both oldpath and newpath refer to the file being renamed.

Context that matters for this claim:

- **Condition.** The atomicity sentence is conditional: "If newpath already exists". The claim drops the condition.
- **Hedge.** The window sentence says "there will **probably** be a window". The claim says "a window exists". The hedge is lost.
- **Adjacent sentence, line 42.** "If newpath exists but the operation fails for some reason, rename() guarantees to leave an instance of newpath in place." This is the only failure sentence in the paragraph, and it is about **newpath**, not the temporary name (oldpath). The page does not say what oldpath looks like after a failed rename.
- **Words the page never uses.** A grep of the rendered page finds no "temporary", "unchanged", "remain" or "left" in DESCRIPTION. The page says nothing about temporary names, leftovers after a failed run, or cleanup.
- **BUGS section, line 205.** The only crash discussion is NFS-specific: "If the server does the rename operation and then crashes ... The application is expected to deal with this." It does not describe a leftover temporary name on a local filesystem.

## Decision, clause by clause

1. "The replacement is atomic for readers of the final name" — **supported** by Q5 and its condition. The rewrite should restore "If newpath already exists".
2. "a window exists in which both names refer to the same file" — **supported in content, overstated in calibration**. The page says "will probably be a window". The claim should keep the hedge.
3. "so a failed run can leave the temporary name behind" — **overreach**. Neither quote, nor line 42, nor BUGS, says a failed run leaves oldpath behind. The "so" also does not follow: the window in Q6 is a state in which both names exist during a successful rename. It is not a mechanism that leaves a temporary name after a failure. A leftover after failure is at most [INFERENCE] from "a failed rename does not move the file", which the page does not state for oldpath.
4. "cleanup belongs on the error path" — **overreach**. This is a design recommendation. No quote supports it, and the entry's Limits section does not mark it as inference either.

The entry's Limits section does mark the check-then-write TOCTOU as [INFERENCE] with "none of the quotes states this". Claim 4 gives the same kind of inference (failure leaves the temp name, so clean up) with no such marking.

No misreading of Q5 or Q6 themselves. The problem is the second half of the claim.

## Rewrite proposed (Claim 4 split, inference marked)

> Claim 4. When newpath already exists, rename() replaces it atomically, so no other process finds newpath missing. [Q5]
> Claim 4a. The same page says there will probably be a window in which oldpath and newpath both refer to the file being renamed. [Q6]
> Claim 4b. [INFERENCE] A failed rename does not move the file, so the temporary name may remain after a failed run; the page does not state this for oldpath, and cleanup on the error path is a design choice this entry does not source. [Q5, Q6]

If the author wants Claim 4 as one sentence, the minimum change is: "When newpath already exists, its replacement is atomic for other processes; the page says there will probably be a window in which both names refer to the file being renamed; that a failed run can leave the temporary name is [INFERENCE] and is not stated by the page." Drop "cleanup belongs on the error path" from the sourced entry, or move it to a labelled design note.

## Residual risk and verification gaps

- I did not verify the counter's pass/fail of the rewrite; the counter is structural and does not judge entailment (the entry's own Limits say so). The rewrite changes text only; the quote table (Q5, Q6) is unchanged, so the counter's quote checks should still pass.
- Claims 1–3 and 5 and the S134/S136 quotes are outside this item and were not reviewed.
- The rendered page is man-pages 6.19 on this host, as the entry says. Other versions were not checked.

Check run: `man -l rename.2.gz | col -bx` rendered; Q5 and Q6 located verbatim (Python substring test on the rendered text: True, True); failure and temp-name wording searched in the rendered text (only line 42 and line 205 found, neither about oldpath). Scratch deleted.

Tools installed: none.

VERDICT: CLAIM4=overreach rewrite_needed=yes
