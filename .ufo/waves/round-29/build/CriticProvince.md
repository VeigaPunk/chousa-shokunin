# Province review — round 29

**Verdict: NEEDS-L0.** Quote location is chousa's research-method work, not an alien province. However, registry membership establishes a source relationship, not an explicit standing exception to the external-fetch restriction. **[INFERENCE]** The documents support both the source-reading duty and a literal approval requirement; they do not define whether ordinary public-document reopens are excluded from “live-target” fetching.

**Axes:** operability is the assigned claim; adjacency and calibration govern permission and scope; freshness concerns actual reopens. Depth and coverage are not measured by this review.

## Exact evidence

Local files opened through `functions.read`; access date: **2026-10-23**, as required by the assignment. The links below identify local files, not externally opened pages. Each quoted excerpt is at most 25 words.

- [chousa PROVINCE.md:5–8,13–14](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md#L5-L14) owns “claim-vs-source verification” but refuses “external live-target research without operator approval (loopback-only otherwise)”.
- [chousa SKILL.md:49–51](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md#L49-L51) is more explicit: “A window without an approval table is loopback-only.”
- [fleet shokunin.conf:67](file:///home/vgpnk/Projects/shokunin/shokunin.conf#L67) and [round prompt:6](file:///home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-29.md#L6) both say “no external live-target fetches without operator approval”. This is not merely an old gate implementation restriction.
- [fleet CORPUS.md:112–115](file:///home/vgpnk/Projects/shokunin/CORPUS.md#L112-L115) requires “Write it only after opening the source in the round that writes the row.” It also requires “Non-author verification re-opens a sample.” [Round prompt:49–53](file:///home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-29.md#L49-L53) repeats the opening requirement.
- [CORPUS.md:90,103–106,119–122](file:///home/vgpnk/Projects/shokunin/CORPUS.md#L90-L122) defines the source, status and opened fields and keeps the research method separate. These fields do not record network approval. The [canonical contract:119–122](file:///home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md#L119-L122) likewise says the registry only records and curates sources.
- [Frozen claims.md:63–84](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round29/claims.md#L63-L84) permits an alternate `--registry`, defaults to the lane registry, and specifies GET, HTTP(S) redirects, bounded fetching and no credentials. Those are behavior bounds, not a province-policy ruling.

## Strongest counterexample

[The registry's S013 row, line 23](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md#L23) names `https://jsonlines.org/`; [the frozen claim:55–56](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round29/claims.md#L55-L56) includes that source in the fixture. **[INFERENCE; static counterexample, not executed]** In a window lacking approval, a perfectly accurate default quote reopen still sends an external GET. Being already registered does not make that request loopback. Thus the default-own-registry argument alone cannot satisfy the literal restriction.

Historical corroboration, not a new rule: [archived-export-intake.md:131–140](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/archived-export-intake.md#L131-L140) marks external citation-hop opening denied for “no operator approval for external live fetching”. That record concerns unresolved export hops, not registered public documents; it therefore strengthens caution but does not settle the distinction.

An alternate registry and redirect destinations also need a stated authorization scope. Neither can inherit permission merely from the presence of a URL in some table.

## Smallest safe correction and routing

L1 should file this exact question; this seat does not write the fleet channel:

`chousa | round-29 | Does the frontier source-opening duty authorize credential-free GET quote reopens of public-document URLs in chousa's own corpus/SOURCES.md, including HTTP(S) redirects, or do these require a window-specific approval table; do alternate --registry runs require separate approval?`

Continue implementation, local-only review and repair-first drafts without changing the frozen claim, counter or fixture. L1 may land an implementation without automatically running it, but that alone does not demonstrate the capability. Keep the frozen lane-registry default; **that default is a bound, not an approval substitute**.

The assignment's express GET allowance bounds current work; this review does not revoke it or turn it into standing permission. An explicitly approved current window may proceed only within its actual scope. Otherwise route around the ambiguity with local work and defer external execution. For S046–S049, opening must precede each new row; a planned row cannot authorize its own fetch.

The required later measurement remains unchanged: `python3 corpus/evidence/round29/c1-count.py -- python3 tools/quote-reopen.py verify`, with the frozen target `QUOTE_REOPEN_MATCH=130/130` ([claims.md:31–45](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round29/claims.md#L31-L45)). No measurement or claim-admission verdict is supplied here. Also do not turn text location into support, truth or enduring source identity: [claims.md:153–161](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round29/claims.md#L153-L161) expressly excludes those conclusions.

This is a fixable authorization/documentation ambiguity. Obtaining operability by silently waiving the boundary would instead be a trade requiring rejection under [AXES.md:34–36](file:///home/vgpnk/Projects/shokunin/AXES.md#L34-L36), not a harmless clarification. The canonical judge retains admission authority.

## Adjacency

- **kumitate:** [PROVINCE.md:3–6,24–28](file:///home/vgpnk/Projects/shokunin/kumitate-shokunin/PROVINCE.md#L3-L28) owns orchestration/tooling and explicitly routes research method to chousa. A lane-local quote matcher fits chousa; agent dispatch, lifecycle and general orchestration changes do not. Chousa's reciprocal refusal is [SKILL.md:54–56](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/SKILL.md#L54-L56).
- **kasegi:** [PROVINCE.md:3,24–25,44–49](file:///home/vgpnk/Projects/shokunin/kasegi-shokunin/PROVINCE.md#L3-L49) confines its domain to bounty/security work, routes research method to chousa and refuses live-target testing. Public-source text matching is not bounty scope or a claim package; security-target testing cannot be smuggled into this command or routed to kasegi as an automatic escape.
- **kengaku:** [PROVINCE.md:3–6,134–143](file:///home/vgpnk/Projects/shokunin/kengaku-shokunin/PROVINCE.md#L134-L143) owns model research/evaluation and routes research method to chousa. C1 measures a deterministic quote-location command, not model quality. Claims about model factuality or comparative capability remain outside chousa ([chousa PROVINCE.md:10–12](file:///home/vgpnk/Projects/shokunin/chousa-shokunin/PROVINCE.md#L10-L12)).

## Work and limits

Opened the frozen claim first, then the cited local boundaries, registry, frontier contract, round instructions, repair lesson, relevant historical refusal and canonical skill/protocol sections. Used bounded local searches for approval context and sibling file discovery. No external page, candidate, counter, judge, build or test was run; no tools were installed or updated. No production file, frozen input, sibling file or VCS state was changed.

Directory command: `timeout 5s mkdir -p -- /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/build/CriticProvince` → tool returned `(no output)` without an error; numeric exit status was not displayed. Read/search tools likewise expose results rather than shell exit codes. One initial broad glob returned partial results after its timeout; narrower sibling-path discovery succeeded. An initial task-metadata query used the wrong field; reading its keys and then `.items[]` recovered the assigned item. This report is the sole written artifact.
