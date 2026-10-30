# G02 candidate probe — round 64

Compared unchanged `corpus/evidence/round64/controls/ref-preflight-v3.py` against the frozen G02 rule in `corpus/evidence/round64/claims.md` lines 47–52. Probe used isolated temporary lane roots, each with an indexed `good.md` plus one extra recursive-walk entry.

- `nested-gitkeep`: nested `sub/.gitkeep` produced G02 FAIL, exit 1 (`sub/.gitkeep (not *.md)`). **Mismatch:** the frozen rule allows the non-`.md` name `.gitkeep`; it does not restrict that allowed name to the knowledge directory root. Candidate instead tests `relative path == ".gitkeep"` and rejects nested occurrences. [INFERENCE] Treating “name” as basename, rather than a root-relative path, follows the frozen wording.
- `nested-nonmarkdown`: `sub/notes.txt` produced G02 FAIL, exit 1 (`sub/notes.txt (not *.md)`), as required by the frozen allowlist.

Exact command, full stdout/stderr and exit codes are preserved in `evidence.txt`; reusable fixture recipe is `probe.py`. No candidate or production files changed. No packages installed. No verification beyond the two requested probe invocations.

The frozen claims also record a known C1 E12/E13 fixture mismatch (user-provided context); these narrow probes neither exercise nor repair that battery issue.
