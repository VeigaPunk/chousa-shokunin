# ScoutDocsAfter33 — claim-record text and selftest tally vs gate 94a7be5a

Axes: completeness of the named surfaces, match against the landed gate (248 cases; top-level field rule), path:line evidence. No lane files edited. No `c1-count-v2.py` run. `--selftest` was not re-executed this turn.

## Landed gate (opened, not re-run)

- `sha256sum tools/research-gate.sh` → `94a7be5a54dd5cebd9532f2417c4eaedc401c9a0646029dcca8acc445378506e` (exit 0). `git rev-parse HEAD` → `0fb300b5c27900ab8bb3abeb5f54776d71e04beb`. Commit subject names that hash and `selftest PASS 248`.
- `git show eb179ec:tools/research-gate.sh | sha256sum` → `52f07c7416cc80f2a6791c15ad04a16da8c38cfb2b0fbcd088bd93cf3fb91b2a`. `git diff --stat eb179ec 0fb300b5 -- tools/research-gate.sh` → 8 lines, +7/−1, all comments/usage: header `tools/research-gate.sh:51-53` and `usage()` `tools/research-gate.sh:365-367`. Reader unchanged.
- Opened `.ufo/waves/round-33/measure/integrated/selftest.log` (sha256 `cadf3e0ae127f7831aa8bac8f4e6244141026e457c9781429096e0586e5e07b5`, 250 lines): 248 `ok-case` lines, max case 248, last line `RESEARCH_GATE_SELFTEST: PASS (248 cases, 0 skipped)`. Cases 242–248 are `r33-top-nested-line`, `r33-top-nested-sha`, `r33-top-nested-id`, `r33-top-dup-line`, `r33-top-confuser-flat`, `r33-top-confuser-nested`, `r33-top-dup-id`. The script prints `PASS (%d cases)` (`tools/research-gate.sh:7633`); it does not hardcode 248. [INFERENCE] the log is the integration run named by `0fb300b`, not a run started here.

Top-level rule in the gate, matching `corpus/evidence/round33/claims.md` design v2 items 1–3: header `:51-53`, `usage()` `:365-367`, `claim_scan` comment `:1115-1126`, `json_str` `:1259`, `json_has_key` `:1267`, `json_dup` `:1275`, duplicate handling `:1617-1645` (identical duplicated `id` keeps that id; differing values print `id=line<N>`).

## Verdict

**BROKEN** as a documentation set: the live rule and the 248 tally match in SKILL, the README frontier, and the gate header/usage, but two current-facing sentences do not match gate `94a7be5a`. The gate’s reader was not shown to break C1. No counter input outside the counter’s generator was executed.

## Matches the landed gate

| Text | What it says | Match |
|---|---|---|
| `SKILL.md:77-84` | shared `--selftest` → `PASS (248 cases)` on every research-gate row | tally matches the opened log |
| `SKILL.md:78` | `r33 top-level reader cases 242–248` (also r31 216–219, r32 gap 235–241) | case numbers and names match the log |
| `SKILL.md:90` | round 33: the rows now read `PASS (248 cases)`; the rest of the paragraph is the round-25 tally | matches; `:92` `PASS (161 cases)` is labeled historical |
| `SKILL.md:142-145` | since round 33, fields come from the top-level object only; a nested member is ignored; a repeated top-level read field or a non-object line is `invalid` | matches header `:51-53` and usage `:365-367` |
| `corpus/README.md:990-996` | nested `"line"`/`"sha256"` moved to held ground; top-level only; repeated top-level read field invalid; `TOPLEVEL_FIELD_MATCH` 60/156 → 156/156 | rule matches; 156/156 is the v2 counter, not the selftest. Does not name gate `94a7be5a` or say 248 |
| `corpus/README.md:1002` | knowledge row: top-level object only; nested members ignored; repeated read fields invalid | matches |
| `corpus/knowledge/claim-record-fields-r33.md:19-34` | the rule now (top-level members, duplicate → invalid, string content is not structure, non-object → `id=line<N>`) | matches `claim_scan` and `:1617-1645` |
| `tools/research-gate.sh:51-53`, `:365-367`, `:1115-1126`, `:7561-7565` | same rule; selftest block is the r33 top-level cases | matches. `:10` `PASS (N cases)` is the format, not a count |

`corpus/QUALITY.md`: no `248`, `top-level`, or `unanchored` hit. `LOG.md`: no `PASS (248)`, `248 cases`, `unanchored json_str`, or `current selftest` hit (not a named surface; checked so a live tally was not missed).

## Stale or contradictory (current-facing)

1. `SCORECARD.md:1846-1853` — **contradicts.** Heading `## Planned — round 33 (not started)`. Body still lists “the nested `"line"`/`"sha256"` key defect (unanchored `json_str`/`json_has_key`)” as a candidate, not a landed rule, and does not mention 248. The file ends at `:1853`; there is no Round 33 verdict. The landed gate reads those fields from the top-level object (`claim_scan`) and the opened log passes cases 242–248. Earlier `## Planned — round 26 (not started)` at `:1371` is explicitly retired at `:1449`; round 33’s planned block was not.

2. `corpus/knowledge/claim-record-fields-r33.md:4` and `:58` — **stale identity.** `:4` “gate behaviour measured on gate SHA-256 `52f07c74…1b2a`”. `:58` “landed gate `52f07c74…` 156/156 on seeds 3351 and 3352”. That hash is `eb179ec`’s blob, not the file on disk (`94a7be5a`). The delta is the header/usage sentences only, so the rule text at `:19-34` still describes the reader. The note never says 248.

3. `SKILL.md:131` and `:136-137` — **stale schema/vocabulary in the current claims-mode section.** `:131` still schemas a claim as `{"id","source","span","expect"[, "marker"]}` only. `:136-137` lists `observed` as `supported|contradicted|unsupported|unproven|refused|invalid`. Landed usage `:363-375` also documents `"line"` and `"sha256"`. Landed header `:87` also lists `observed` `stale` and `mislocated`. The round-33 sentence at `:142-145` matches; it does not repair the schema or the observed list above it.

## Not contradictions

Dated round verdicts and knowledge `verified-at` lines that name an old `PASS (N cases)` together with that round’s gate (SKILL `:153` 30, `:176` 44, `:212` 40, `:249` 54, `:296` 64, `:340` 74, `:392` 85, `:543` 215; README evidence sections; SCORECARD per-round **After** lines through round 32 `PASS (241 cases)` at `:1828`; knowledge notes pinned to their own gate, including `hardening-r10.md:568-570` “current selftest passes (122 cases)” under heading “current gate `9f163807…`”) are historical measurements, not a claim that today’s suite is that size.

`corpus/knowledge/line-binding-r31.md:38` and `revision-binding-r31.md:11` (“Unknown JSON keys are ignored, as before this round”) still match unread keys. They do not say a nested member of a read field is read. They also do not state the round-33 rule.

`SKILL.md:83` “metadata cases 137–154” is the original checkpoint range (the `:90-92` note already says so). Landed log still has those cases, and also metadata-named cases through 215 (case 209 is `claims-registry-colon-deny`). The row’s suite total is 248. The sub-range is incomplete, not a false total.

## Limits

Did not re-run `--selftest` or `c1-count-v2.py`. Did not diff every historical `PASS (N)` sentence against its receipt. No input was found, in the comments read, on which the landed reader disagrees with claims.md design v2; none was executed.
