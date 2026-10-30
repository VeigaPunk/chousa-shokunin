source: S146 (grep(1), GNU grep 3.12-modified page, installed grep 3.12-2, rendered line 29), S147 (git-log(1), Git 2.56.0 page, page date 2026-09-27, rendered line 1376), S148 (corpus/evidence/round63/audit-probe.txt, written by corpus/evidence/round63/audit-probe.py); S149 rejected
verified-at: 2026-10-30 (man pages rendered with MANWIDTH=1000 man -l FILE | col -bx on grep 3.12-2 and git 2.56.0-1; probe run on Python 3.14.8, git 2.56.0, kernel 7.2.11-arch1-1)
recheck: on a grep, git or claims-audit change run `python3 corpus/evidence/round63/audit-probe.py` (exit 0, PROBE_FACTS=11/11) and `python3 tools/claims-audit.py --selftest` (exit 0); the round-62/63 rows by `python3 tools/claims-audit.py --claims corpus/evidence/round62/claims.md --audit corpus/evidence/round63/audit/audit-r62.tsv --root .` (exit 1, FLAGGED=2/2) and the audit-r63 twin (exit 1, FLAGGED=4/4)

# Auditing a self-assessment statement against the repo it names (round 63)

Twice in this lane a frozen claims file carried statements its own committed files contradict: round 62's
`claims.md` carried 14 (caught post-freeze by a non-author seat, `corpus/evidence/round62/claims-erratum.md`)
and round 63 attempt 1's carried 4 (`corpus/evidence/round63/claims-erratum.md`, found by seat CritCalibration).
Both catches were readers, after the freeze. This entry records the machine-checkable subset as seven rule
classes and one committed checker, `tools/claims-audit.py`: a rule file (TSV, six columns) names an anchor that
locates the statement in the claims file, a class names the check, and the checker re-derives the fact from the
committed bytes. Output: `FLAG <id> <class> <detail>` per false statement, `AUDIT_STALE <id>` (exit 2) when an
anchor is absent from the claims file, and one summary line `FLAGGED=<k>/<n> AUDIT=PASS|FAIL` (exit 1 iff some
rule fired). The demonstrated instances: `FLAGGED=2/2` on the round-62 claims (rows 1 and 13 of its erratum)
and `FLAGGED=4/4` on the attempt-1 claims (E1–E4).

## The seven rule classes

| class | checks | mechanism (the command it re-derives) | demonstrated by |
|---|---|---|---|
| `json-count` | the anchor line names, as a standalone number token, the true count of a JSON array | `json.load`, `len` (a number inside a word — `v2`, `w1` — is not a named count) | r62 erratum #1 ("64 seats", spec holds 66) |
| `section-contains` | a needle occurs under a named heading of a file | fixed-string search scoped to the heading's lines | r62 #13 at the current file |
| `section-contains-at` | the same, against the file's blob at a pinned revision | `git show <rev>:<path>` | r62 #13: at the round-62 base the `## Leads` bullet does not name S138; the current file does |
| `git-first-commit` | the claims file and the paths it calls "committed before the freeze" first appear in different commits | `git log --diff-filter=A --format=%H -- <path>`, last line = first-add commit; S147 states the filter letters (Added (A)…) | r63 erratum E1 (added in the freeze commit itself) |
| `file-kind` | a file-kind word in the statement matches the named artifact's suffix class | suffix → kind (`.h` header, `.[0-9].gz` man page, `.md` doc, …) | r63 E2 ("wrong header file"; the variant substitutes `git-log.1.gz`, a man page) |
| `verbatim-heading` | every backtick span in the anchor line occurs verbatim in the named file | fixed-string search (S146: `-F` — "Interpret PATTERNS as fixed strings, not regular expressions") | r63 E3 (a quoted SCORECARD heading that does not occur) |
| `scope-narrower` | a lane-wide absence quantifier ("the lane holds nothing") whose own sweep names a strict subdirectory | `grep -rl` path extraction on the anchor line and the two after it | r63 E4 (sweep names `corpus/knowledge`) |

## What the checker does not do (limits, disclosed before use)

- It is lexical. A statement is checked only when a rule row anchors it, the anchor must occur verbatim (a
  stale row is exit 2, never a pass), and `json-count`/`verbatim-heading` read the anchor line only — a
  statement spread over several lines is out of reach except for `scope-narrower`.
- The rule rows are authored by the same lane that wrote the claims file. The checker is a screen for the
  demonstrated classes, not a reader: 12 of the 18 erratum statements (judgment corrections) stay prose-only,
  and a true-as-written but irrelevant statement passes.
- `git-first-commit` and `section-contains-at` need a git checkout; without one the row is counted as SKIP
  (never as a pass or a flag).
- Entailment is not machine-checked anywhere in this entry: a claim can pass every class and still be
  unsupported by its quotes (round 62's counter had the same shape; the reader outranks the checker).

## Probe and selftest

`python3 corpus/evidence/round63/audit-probe.py` runs the classes against fixtures under TMPDIR and prints one
P-row per case (S148: `PROBE_FACTS=11/11`, exit 0); `python3 tools/claims-audit.py --selftest` builds
contradicted and corrected fixture sets plus a scratch git repo and prints `AUDIT_SELFTEST=PASS (3 cases)`.
The probe and selftest are the recheck surface: both must exit 0 after any change to the checker.
