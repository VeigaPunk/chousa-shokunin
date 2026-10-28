# Gate: registry rows S134-S137 (draft for `## Gate` of corpus/lessons/round-61.md)

Seat ScribeGate, wave w1, round 61. Every row: access date 2026-10-28. Every source was re-opened by this seat
in this session. Line numbers are of the named rendering: man pages via `MANWIDTH=1000 man -l FILE | col -bx`
(rendered lines, not `.gz` source lines); lane files as committed. Quote counts are words.

Decisions: S134 admit (A) · S135 admit (A) · S136 admit (B) · S137 reject (flip condition below).

## Gate

### S134 — open(2), Linux man-pages 6.19 — ADMIT, tier A

- Path: `/usr/share/man/man2/open.2.gz` (Arch package man-pages 6.19-1, page dated 2026-02-08;
  sha256 `a525cf9f01ab2ebd68c2eb8fd609966ffc3b610cf3c766ceef9910d47de53237`). No URL: the row carries none,
  man7.org HTML was not opened, no network use.
- Access date: 2026-10-28.
- Q1 (rendered line 147, O_NOFOLLOW, 20 words): "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP."
- Q2 (rendered line 147, O_NOFOLLOW, 12 words): "Symbolic links in earlier components of the pathname will still be followed."
- Q3 (rendered line 123, O_EXCL, 21 words): "symbolic links are not followed: if path is a symbolic link, then open() fails regardless of where the symbolic link points."
- Grounding of `teaches`: Q1 and Q2 ground "O_NOFOLLOW refuses only a symlink in the last path component". The
  consequence "so a writer must check the earlier components of an output path itself" is [INFERENCE] from Q2;
  the page does not say it. Q3 grounds the O_CREAT+O_EXCL case, which the row's scope names but the teaches does not use.
- Decision reason: kernel project's own reference page, read from the installed package; the three quotes are
  present at the lines given. Limit: the grade A rests on a local render, not the canonical HTML; a reviewer may
  downgrade to B.

### S135 — rename(2), Linux man-pages 6.19 — ADMIT, tier A

- Path: `/usr/share/man/man2/rename.2.gz` (same package; sha256 `4b6d62db2ed1c7937f62392cdeea4eecdeee5e7f6d21eb1675390910b6abb3f5`). No URL, as S134.
- Access date: 2026-10-28.
- Q4 (rendered line 46, DESCRIPTION, 23 words): "If oldpath refers to a symbolic link, the link is renamed; if newpath refers to a symbolic link, the link will be overwritten."
- Q5 (rendered line 38, DESCRIPTION, 23 words): "it will be atomically replaced, so that there is no point at which another process attempting to access newpath will find it missing."
- Q6 (rendered line 38, DESCRIPTION, 19 words): "However, there will probably be a window in which both oldpath and newpath refer to the file being renamed."
- Grounding of `teaches`: Q4 grounds "replaces a planted symlink at the final name": when newpath is a symlink the
  link is overwritten. "instead of writing through it" is [INFERENCE]; the page does not discuss writing through a link.
  Q5 and Q6 are not used by this row's teaches; they belong to the entry's window claim.
- Decision reason: same source class and access as S134; the quoted semantics are the page's own words at the lines given.

### S136 — round-55 builder hazard transcript (seat R55W2SentBuilder) — ADMIT, tier B

- Path: `.ufo/waves/round-56/w1/R55W2SentBuilder.md` (lane file, 120 lines). Identical bytes at lane commit
  `9eef15e7c0e0ae0055228e7066dc1eec676a91d2` (`git show 9eef15e:… | cmp` silent, equal).
- Access date: 2026-10-28.
- Q7 (file line 33, section 1, case h2, 11 words): "victim/S404-9.txt(28) before → absent after; victim/S001-1.txt(457) created; exit 0, stderr empty"
- Q8 (file line 34, section 1, case h3, 11 words): "victim/IMPORTANT.txt 10→457 B, victim/LEDGER.tsv 74→243 B (both targets truncated); exit 0"
- Cross-check: the summary table rows h2 (line 11, "unlink + create in the link target") and h3 (line 12,
  "truncated both link targets") carry the same observations.
- Grounding of `teaches`: Q7 and Q8 ground "unlinked and created files in a symlinked spans directory and
  truncated two link targets while exiting 0", scoped to revision 29cfb12 and the seat's own fixtures.
- Decision reason: observed transcript with exit codes and file sizes, but produced by one seat on its own
  fixtures and not a re-runnable gate output, hence tier B. Not re-run by this seat. The row must not be read as a
  claim about the current builder.

### S137 — tools/build-spans.py docstring, "Output safety (round 61)" — REJECT

- Path named by the row: `tools/build-spans.py` (module docstring). Checked by this seat:
  `grep -c 'Output safety (round 61)' tools/build-spans.py` → `0` (working tree, HEAD `9f32ac0`);
  `git show 9eef15e:tools/build-spans.py | grep -c 'Output safety'` → `0`; the same at `2b0e17b` → `0`.
  The paragraph does not exist in the shipped builder. The row's location is therefore a landing-time location.
- Located quote G1 (the text exists only in the control reference builder `corpus/evidence/round61/controls/ref-build-spans.py`, line 34, 17 words; this is not the shipped file):
  "Output safety (round 61). A build refuses, exit 2 and nothing written or removed, when: DIR is"
- Access date: 2026-10-28.
- Decision reason: a docstring is a statement of intent, not evidence that the contract holds; the row's own
  `teaches` says so. Two corrections for the row before the L1 writes it: (a) the row's `location` must not claim
  the paragraph is in `tools/build-spans.py` until it lands; (b) its `teaches` lists "caps", but the 64 MiB caps
  are in a different paragraph of the reference builder (lines 16-19), not in "Output safety (round 61)".
- Flip condition (as the row states): `python3 -B corpus/evidence/round61/c1-count.py` exits 0 with `LEGS=20/20 C1=PASS`
  on the shipped `tools/build-spans.py` bytes; then cite that receipt instead of the docstring.

## Spot-check request (non-author)

- Admit to re-open: S136. Open `.ufo/waves/round-56/w1/R55W2SentBuilder.md` at lines 33-34, and check Q7 and
  Q8 against them verbatim. Also check the claim that the cited revision is `9eef15e` (`git -C <lane> show
  9eef15e:.ufo/waves/round-56/w1/R55W2SentBuilder.md`). This is the admit most likely to be wrong, since it rests on one seat's run.
- Reject to re-open: S137. Run `grep -n 'Output safety' tools/build-spans.py` (expect no match) and
  `grep -n 'Output safety' corpus/evidence/round61/controls/ref-build-spans.py` (expect line 34 only). Confirm the reject
  stands on the absence alone, and that the flip condition names a receipt rather than a docstring.
