# Seat EntryDraft — chousa round65 — C2 knowledge entry draft

Date: 2026-10-30. Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd; base master d6ed8155e9b4735639a2cf0a3e479c62f2056195. Leaf seat; no subagents; read-only git with explicit `-C`; no mutations, no network fetches, no full test batteries.

## Task

Draft C2 knowledge entry `receipt-identity-r65.md` from the opened sources (installed git-cat-file(1), /usr/lib/python3.14/hashlib.py, round64 before receipt S154–S156), distinguishing object identity, content digest, reported exit and execution authenticity; provenance trio first; Claims and Limits; quotes ≤25 words; inference marked.

## Provenance trio — recomputed and matched

Registry: corpus/evidence/round65/source-openings.json. All four digests recomputed locally this round; all match.

| id | path | location | sha256 (recomputed 2026-10-30) | registry match |
|----|------|----------|--------------------------------|----------------|
| S154 | /usr/share/man/man1/git-cat-file.1.gz | OUTPUT (rendered line 159) | 8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737 | yes |
| S155 | /usr/lib/python3.14/hashlib.py | module documentation lines 31–32 | 88fa624821fbdee7eb2ef87c2437b207afe328cf117c7463367e2db5eb1af492 | yes |
| S156 | corpus/evidence/round64/controls/c1v3-before-full.txt | lines 1, 31, 44 | ca05f579dc0f979a772ecec973a1da5d5df8d11881ca678708c72044f8c9c05b | yes |
| S157 (supplementary) | corpus/evidence/round65/controls/ref-receipt-pin.py | module docstring | 0719d7175da072454f514e0eea52b266f66c2246a085f4ea824793f634315fa2 | yes |

Rendering method for S154: `MANWIDTH=1000 man -l /usr/share/man/man1/git-cat-file.1.gz | col -bx` (260 lines); page footer "Git 2.56.0, 2026-09-27". Rendered copy archived as evidence in this folder.

## Deliverable

- Draft entry: `.ufo/waves/round-65/w1/EntryDraft/receipt-identity-r65.md` (candidate for L1; I did not write to corpus/knowledge/). Structure: `source:` / `verified-at:` / `recheck:` header, located-quotes ledger Q1–Q8 (all ≤25 words), four Claims (object identity / content digest / reported exit / execution authenticity, [INFERENCE] marked), Limits.
- Evidence: `.ufo/waves/round-65/w1/EntryDraft/cat-file-rendered-manwidth1000-r65.txt` (rendered man page used for line-located quotes).

## Findings

1. Working tree already carries uncommitted C2 planning. `git -C <lane> ls-tree d6ed8155 -- <paths>` at base returns only tracked `corpus/SOURCES.md`; `corpus/knowledge/receipt-identity-r65.md` is untracked (`??`), and `corpus/README.md` + `corpus/SOURCES.md` are modified (`M`). SOURCES rows S154–S157 and README line 1342 already point at the entry. This matches the claims' "preliminary uncommitted planning does not freeze any others".
2. Counter state: `python3 corpus/evidence/round65/c2-count.py` currently prints `ENTRY_CHECKS=10/10 C2=PASS`, exit0 (observed 2026-10-30, against the working tree with the preliminary in place). The frozen before-control `ENTRY_CHECKS=0/10` exit1 describes the base tree, not the current one; it is not reproducible while the uncommitted planning sits in the tree. Two of the ten checks (SOURCES rows, README index) are integration-side artifacts, not entry text.
3. Verbatim delta in the registry: source-openings.json registers the S154 quote as "contents of the object will be returned", but the rendered page (and the roff source) read "contents of the <object> will be returned" — the registered form drops the literal `<object>` token. The file digest still matches; my draft cites the verbatim form and records the delta as a Limit.
4. S156 grounding for "reported exit": the round64 before ledger itself records a reported exit beside its expectation — line 31 "LEG E05 defect FAIL rc=0 want 1" — a reported rc=0 contradicted inside the same pinned file; this grounds the record-vs-process distinction without leaving the opened sources.
5. Report-path template discrepancy (recorded verbatim, resolved conservatively): lane ticket says "Report: write your scoped findings to .ufo/waves/round-65/w1/EntryDraft.md", while the seat spec says write only `…/w1/EntryDraft/report.md` plus uniquely named evidence in that folder, and the lane rule says each seat writes only its own `w1/<seat>` output folder. I wrote the folder form only; L1 should reconcile the ticket template.

## Gates L1 should run (once, at integration)

- `sha256sum /usr/share/man/man1/git-cat-file.1.gz /usr/lib/python3.14/hashlib.py corpus/evidence/round64/controls/c1v3-before-full.txt corpus/evidence/round65/controls/ref-receipt-pin.py` — expect the four registry digests.
- `python3 corpus/evidence/round65/c2-count.py` — target ENTRY_CHECKS=10/10 exit0.
- `git -C <lane> status --porcelain` — confirm integration touched only intended corpus files plus seat folders.

## Tools

None installed. Preexisting: git 2.56.0, man 2.13.1, groff/col (util-linux/coreutils), Python 3.14.8. No pacman transactions; none attempted.

## Out of scope / not done

No edits to corpus/ (L1's), no commits, no other seats' folders, no batteries beyond the single named counter run, no attack seats' work. Scratch /fast/scratch/hyaku/chousa-r65/EntryDraft/ deleted after evidence copy; no /tmp evidence.

Report: .ufo/waves/round-65/w1/EntryDraft/report.md
