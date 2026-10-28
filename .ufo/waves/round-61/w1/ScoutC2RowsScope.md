# ScoutC2RowsScope — registry fit of S134–S137

Candidates: `corpus/evidence/round61/controls/c2-positive-rows.txt`. Contract: `CORPUS.md` SOURCES (tier is per `scope`; A = primary/authoritative, including a re-runnable gate; B = strong secondary with reproducible detail; C = lead only). Sources opened locally: `man -l` of the installed pages, the seat report, base `tools/build-spans.py`, and `controls/ref-build-spans.py`.

## Findings

S134 scope overclaims, so tier A would attach to behavior the page does not state as unconditional. The rendered `O_NOFOLLOW` entry fails with `ELOOP` only for the final component and still follows earlier components, then says the flag was added in Linux 2.1.126 and "See also O_PATH". With `O_PATH` (since Linux 2.6.39) the same flag returns a descriptor for the symlink instead of failing. The symlink rule for creation is "When these two flags are specified" under `O_EXCL` together with `O_CREAT`, not `O_CREAT` alone, and `O_EXCL` without `O_CREAT` is undefined except a Linux 2.6 block-device case. The scope's "not … kernel versions" does not remove those versioned exceptions. The `teaches` cell adds a "writer must check" prescription the page does not state. Tier A stays right once the scope is the documented slice. Kind `docs` and the installed-page source cell match `.TH open 2 2026-02-08 "Linux man-pages 6.19"` and `pacman -Q` → `man-pages 6.19-1`.

S135 scope does not claim more than `rename(2)` DESCRIPTION. Line 38 is atomic replacement of an existing `newpath`; line 44 is the directory restriction; line 46 overwrites a symlink at `newpath` rather than following it. "Not other systems" is a tier boundary, not a claim the page denies other systems. Tier A for that scope is the man page. No cell change.

S136 is honestly tier B, not A and not C, and not rejected. It is one seat transcript (scratch removed at exit), not the contract's re-runnable gate and not the builder source. The report still has the case table, exits, sizes, and revision, so it is a strong secondary, not a lead. Scope matches section 1: at `29cfb12abd70…` the seat's fixtures unlinked and created through a symlinked `spans/` (h2) and truncated two link targets (h3), both exit 0. Lane precedent S040–S045 and S095 tier similar reports A; that is looser than this contract's own-work path to A. Do not raise S136.

S137 is honestly tier C and `rejected`. The "Output safety (round 61)" paragraph states an output-directory contract (refuse symlink or wrong kind, foreign manifest, `--replace` exception, temp plus `os.replace`). A docstring is intent. The `REJECTED: …; flip: …` wording matches the contract, and the flip points at `c1-count.py` rather than the prose. The scope does not say the contract holds. The source and anchor cells do claim the paragraph is in `tools/build-spans.py`. It is not: base sha256 `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6` has no "Output safety". The words are in `controls/ref-build-spans.py` lines 34–40, sha256 `86d64c312e1640d44f1e71bb3e23c8fc6c8b4ef56b627ae5750f761a579eccfd`.

No near-duplicate. `grep -n 'R55W2SentBuilder\|build-spans' corpus/SOURCES.md` exits 1 with no lines. Own-work rows that mention a gate are the research-gate set (S001, S034–S036, S040), not this builder. No registry row cites `open.2` or `rename.2`.

No E04 or W04 risk. `sources-census.sh` `url_of` keeps only `https?://`. The four source cells have zero such URLs (`python3` count 0). Empty URL never enters `url_scopes` (script lines 644–654). The only `man7.org` rows are S064 `execve.2.html` and S067 `execvp.3.html`.

## Evidence

- `MANWIDTH=1000 man -l /usr/share/man/man2/open.2.gz | col -bx`: line 123 `When these two flags are specified, symbolic links are not followed`; lines 146–151 `O_NOFOLLOW` plus `Linux 2.1.126` and `See also O_PATH`; line 162 `O_PATH (since Linux 2.6.39)`; line 189 `O_NOFOLLOW` returns an fd to the symlink. `man_rc=0`.
- Same for `rename.2.gz`: lines 38, 44, 46 as above. `.TH` dates `2026-02-08`, `Linux man-pages 6.19`. `pacman -Q man-pages` → `man-pages 6.19-1`.
- `R55W2SentBuilder.md` lines 3, 11–12, 33–34 (h2/h3). `git rev-parse 9eef15e` → `9eef15e7c0e0ae0055228e7066dc1eec676a91d2`. Blob of that path at `9eef15e` and at `HEAD` is `4f0731cb6719fb51fec03fcc46b56a026f4e3e7b`.
- Base docstring read (lines 1–31): no output-safety paragraph. Reference lines 34–40: the paragraph the row names.
- `grep` exit 1, recorded above. Census URL rule read at `scripts/sources-census.sh` 600–605 and 644–654.

Quote anchors `O_NOFOLLOW`, `O_EXCL`, and `DESCRIPTION` stay inside the S134/S135 anchor cells, so these edits do not move the C2 structural checks. [INFERENCE] L1 can skip the S137 source edit only if the same commit that appends the row also copies that paragraph into `tools/build-spans.py`. The candidate text as frozen does not.

## Replacement cells

S134 `scope`: `what man-pages 6.19 states a symbolic link does at open on Linux: O_NOFOLLOW (added in Linux 2.1.126) fails with ELOOP when the final component is a symlink and still follows earlier components, except O_PATH|O_NOFOLLOW (since Linux 2.6.39) which returns a descriptor for the link; O_CREAT together with O_EXCL fails if path is a symlink; not O_CREAT alone, not O_EXCL without O_CREAT, not other systems`

S134 `anchor`: `O_NOFOLLOW entry (rendered lines 146-151, including See also O_PATH) and the O_PATH symbolic-link paragraph (line 189); O_EXCL entry "When these two flags are specified" (line 123); Linux man-pages 6.19, 2026-02-08`

S134 `teaches`: `Without O_PATH, O_NOFOLLOW fails with ELOOP only for a final-component symlink and still follows earlier components; O_CREAT with O_EXCL fails when path is a symlink, regardless of its target`

S134 other cells: no change. Tier stays A.

S135: no cell change.

S136: no cell change. Tier B stands.

S137 `source`: `tools/build-spans.py module docstring, paragraph "Output safety (round 61)" — opened in corpus/evidence/round61/controls/ref-build-spans.py (sha256 86d64c312e1640d44f1e71bb3e23c8fc6c8b4ef56b627ae5750f761a579eccfd); that paragraph is absent from base tools/build-spans.py (sha256 1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6)`

S137 `anchor`: `paragraph "Output safety (round 61)" at ref-build-spans.py lines 34-40 (sha256 86d64c312e1640d44f1e71bb3e23c8fc6c8b4ef56b627ae5750f761a579eccfd); cite tools/build-spans.py only once that paragraph is in the landed file`

S137 `scope`, tier `C`, `teaches`, status `rejected`: no change.

VERDICT: ROWS_NEEDING_EDIT=2/4
