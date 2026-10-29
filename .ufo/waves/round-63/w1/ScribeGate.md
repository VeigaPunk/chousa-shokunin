# ScribeGate — round 63, wave w1 (scribe item: Gate section for the three candidate rows)

Draft: `.ufo/waves/round-63/w1/ScribeGate/gate.md` (9 lines, the `## Gate` section, not yet placed in `corpus/lessons/round-63.md`). No lane, tool, frozen, SOURCES or knowledge file was written; the scratch directory `/fast/scratch/hyaku/chousa-r63/ScribeGate` was removed before yield.

## Findings

1. **All three candidate rows admit.** S142 (git-rev-parse(1), tier A), S143 (gitrevisions(7), tier A), S144 (probe output, tier B own-work). Each quote is a contiguous substring of its rendered line; verified by script (below), 4/4 verbatim including the reject quote.
2. **Rejected candidate: gitglossary(7), REJECT (C).** The named ScoutC2Reject report is absent (`ls .ufo/waves/round-63/w1/ScoutC2Reject.md` → `No such file or directory`), so I opened the installed page myself. Its `commit-ish` entry (rendered line 55) restates ground the admitted rows already cover: `^{type}` peeling (S142 rendered line 64) and "dereference the object at <rev> recursively" (S143 rendered line 115). The glossary adds only the undefined word `commit-ish`. Flip to admit (tier A, scope limited to those two definitions) if a claim is rewritten to rely on `commit-ish` as a defined term, or a non-author reviewer finds a claim whose wording depends on the glossary's definition.
3. **No status / recheck / used-by change.** S142–S144 are not in `corpus/SOURCES.md` (last id S141; `grep -o "^| S1[34][0-9] "` prints nothing), so there is no old-to-new log to write. Rows enter as `mined`, opened 2026-10-28, recheck `on-release`, `on-release`, `180d`.
4. **Page dates are checked, not assumed.** Row S142/S143/gitglossary say "page dated 2026-09-27": `zcat … | grep -m1 '^.TH'` prints `"2026\-09\-27" "Git 2\&.56\&.0"` for all three pages. The rendered text itself carries no date (its footer is `Git 2.56.0`), so the date is the page's `.TH` field, not a render fact.
5. **Caveat on S144.** The probe output `corpus/evidence/round63/git-revision-probe.txt` does not exist yet (created by the round). The S144 quote is located in its candidate bytes, `controls/candidate-git-revision-probe.txt`; it must be re-located in the landed file. Its line 1 `HEADER git=git version 2.56.0` matches `git --version` run this round.
6. **Not run: `tools/quote-reopen.py`.** Item 30 of `corpus/QUALITY.md` names it, but it fetches registry URLs only (its docstring: "fetches each registry URL once per run"), and S142–S144 are local files with no URL; no network was used. Verification was by `verify.py` against the render files instead.

## Evidence

Renders (written to scratch, then deleted):

    MANWIDTH=1000 man -l /usr/share/man/man1/git-rev-parse.1.gz | col -bx   # 537 lines
    MANWIDTH=1000 man -l /usr/share/man/man7/gitrevisions.7.gz | col -bx    # 258 lines
    MANWIDTH=1000 man -l /usr/share/man/man7/gitglossary.7.gz | col -bx     # 398 lines

Quote verification (`python3 -B verify.py`, exact output):

    GATE_QUOTE S142 VERBATIM line=75 words=16 max_ok=True file=rev-parse.txt
    GATE_QUOTE S143 VERBATIM line=22 words=18 max_ok=True file=gitrevisions.txt
    GATE_QUOTE S144 VERBATIM line=5 words=6 max_ok=True file=candidate-git-revision-probe.txt
    GATE_QUOTE REJ-gitglossary VERBATIM line=55 words=15 max_ok=True file=gitglossary.txt
    TERM S142 commit-ish_count=2 peel_count=1 dereference_count=4
    TERM S143 commit-ish_count=1 peel_count=0 dereference_count=4
    QUOTES_VERIFIED=4/4

Each quote also occurs once in `gate.md` (`grep -cF` returns 1 for each of the four), and `sed -n 64p rev-parse.txt` / `sed -n 115p gitrevisions.txt` contain the S142/S143 sentences cited in finding 2.

Row fields checked: `candidate-git-rows.txt` rows have 11 `|`-separated columns, matching the registry header; `sha256sum` prefix `cfdf7b117c26a07f` equals the frozen digest.

Line numbers of the probe quote: `grep -n "P03\|P07\|P09\|HEADER" controls/candidate-git-revision-probe.txt` → lines 1, 2, 5, 9, 11 (P03 at line 5, matching the row's "lines P03, P07 and P09").

Install / tool record: none. No tool was installed or upgraded; `git --version` = `git version 2.56.0`; `python3` = 3.14.8 per the probe header.

## Axes

- **Operability:** the Gate section is one lesson block that a reader can re-verify with the commands above (renders are reproducible from the `.TH`-dated packages on this host).
- **Coverage:** three admits and one reject; the reject's flip is stated. Coverage of `commit-ish` as a defined term is the one gap (finding 2).
- **Calibration:** S144 is admitted as tier B, not A; its quote is from candidate bytes and is marked as such; the page date claim is checked against `.TH`, not against the render, which carries none.

## Out of scope / not verified

- Whether the probe's 14 expectations match the landed output (that is the probe seat's item).
- Entailment of the candidate entry's claims from these quotes (C2 kill rule's closure read).
- Placing the section into `corpus/lessons/round-63.md`: the L1 integrates.

VERDICT: GATE_ROWS=3 quotes_verified=4
