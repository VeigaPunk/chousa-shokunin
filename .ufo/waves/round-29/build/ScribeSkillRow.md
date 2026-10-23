# Round 29 C1 — SKILL row draft

Axis: operability. This is a draft for L1 integration; `SKILL.md` was not edited. No measured outcomes are included.

## Decision table insertion

| Intent | Correct surface | Never | Expected output |
|---|---|---|---|
| A lesson or knowledge entry cites a located quote from a web source | Run `python3 tools/quote-reopen.py verify --items <tsv>` from the lane root before citing | Cite an `ABSENT` or `UNREACHABLE` result before re-opening it by hand | Quote re-opened against the live source URL listed in `corpus/SOURCES.md` before citation |

## Checklist insertion

- [ ] Before citing a located quote from a web source in a lesson or knowledge entry, run `python3 tools/quote-reopen.py verify --items <tsv>` from the lane root; re-open an `ABSENT` or `UNREACHABLE` quote by hand before citing.

## Gates-table insertion

| name | kind | entry | verdict map | self-test | pinned values | write scope | owner |
|---|---|---|---|---|---|---|---|
| `quote-reopen.py verify` | gate | `python3 tools/quote-reopen.py verify --items <tsv> [--registry SOURCES.md]` | Re-opens each item against the live URL in the selected registry; `VERBATIM` requires a case-sensitive normalized occurrence at non-alphanumeric boundaries. Exit `0` iff every item is `VERBATIM` · `1` if any item has another verdict · `2` on usage or I/O error | Not specified by the frozen contract | Does not verify claim support, source truth, or later page identity; does not cover PDF sources, JavaScript-rendered pages, ellipsis quotes, case-folded or paraphrased matches, or quotes spanning two block elements | GET only to registry URLs (fragment removed; HTTP(S), including redirects); 30 s timeout, one retry, no cookies or credentials, each URL at most once per run | chousa |

## Evidence and limits

Opened `corpus/evidence/round29/claims.md` lines 60–101 and 153–161 for the frozen command, verdicts, exit codes, fetch behavior, and non-claims; opened `SKILL.md` lines 13–23 and 59–71 for the decision, checklist, and Gates row styles. The draft command was not executed; no implementation result, live page, or source quote was checked. The frozen contract does not specify a self-test. No product files were changed; this report is the only written artifact.

Directory command: `timeout 30s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/build/ScribeSkillRow` — no output; the tool response did not expose an exit code.

Report path: `.ufo/waves/round-29/build/ScribeSkillRow.md`.
