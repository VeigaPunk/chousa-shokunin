# Round 17 capability row backfill

Axes: freshness (SCORECARD coverage); calibration (claim limited to demonstrated behavior).

## Finding — P2, freshness

The Round 17 admission claim has no corresponding first-working-round 17 capability row in the pinned SCORECARD (`grep` for `| 17 |` returned no matches).

- `LOG.md:665`: “**Verdicts** (SCORECARD §Round 17): coverage/operability/depth/calibration(narrow) **improved**; freshness/adjacency **unchanged**; none harmed. **ADMIT.** Capabilities +1.”
- `SCORECARD.md:853-856` names the capability as the “scope-screen fenced-heading shadow”; `SCORECARD.md:884`: “the fenced-heading shadow class is closed at the parser: before CLEAN on a shadowed refused domain → after `SCOPE_BOUNTY_ABSORBED` warn + DRIFT (receipts live); five variants pinned”.
- Re-ran `bash tools/research-gate.sh --selftest` in `/tmp/chousa-r25-CapRowR17`, whose observed HEAD was `b820e4e40ce52deedf53b191140cd7b08ddda929`: `RESEARCH_GATE_SELFTEST: PASS (136 cases, 0 skipped)`.

Round 17's five demonstration cases passed now:
```text
ok-case  112 scope-fence-shadow           exit=1
ok-case  113 scope-fence-only             exit=0
ok-case  114 scope-fence-nested           exit=1
ok-case  115 scope-fence-indented         exit=1
ok-case  116 scope-fence-unclosed         exit=1
```

The knowledge note specifies the boundary and limits: `corpus/knowledge/fenced-heading-r17.md:20-27, 54-61` (two-pass fence pairing; headings within fences are literal; fenced data rows remain a named limit).

Draft row:
```text
| Fence-aware scope screening | Ignores fenced `## Meta` headings while parsing sections, preventing a fake in-province declaration from masking the real refused domain. | selftest cases 112–116; `corpus/knowledge/fenced-heading-r17.md` | 17 |
```

## Residual risk and verification gaps

This confirms the cases pass at the requested Round 25 base, not that every historical receipt or all behaviors of a Markdown renderer were revalidated. The knowledge note explicitly limits the parser’s contract; the row does not claim general Markdown rendering.

No tools installed or updated. No files were edited in the private clone; the report above is the only authored deliverable.
VERDICT: Capability identified; cases 112–116 pass at b820e4 and the draft row is supported. No installs.