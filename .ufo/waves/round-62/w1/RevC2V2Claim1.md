# RevC2V2Claim1 — entailment review of C2 Claim 1 (round 62, wave w1)

Scope: Claim 1 of `corpus/evidence/round62/controls/c2v2-positive-entry.md` and its quote set. Lane read-only; claims.md sha256 prefix checked `a3193ebd328919e2` (matches). Nothing under `corpus/`, `tools/` or `SKILL.md` was written.

## Findings (by severity)

1. **Claim 1 as written overreaches (lost hedge).** It says RESOLVE_NO_SYMLINKS "makes the kernel refuse a symbolic link anywhere along the walk". The page's own exception is missing: when the trailing component is a symlink and `how.flags` has both `O_PATH` and `O_NOFOLLOW`, the call returns an O_PATH descriptor for the link, not a refusal. Probe P14 on this host agrees (`observed=True`). The entry's Q-set has no quote for this sentence, so the claim cannot be checked against its quotes.
2. **The scope sentence is not quoted.** Claim 1 cites Q2 (implies NO_MAGICLINKS) and Q3 (O_NOFOLLOW only in the final component). The page's "all of the components" sentence is absent from the set. "Every component" follows from Q3 only by contrast. "anywhere along the walk" is not on the page; "walk" is the reviewer's word.
3. **"refuse ... with ELOOP" is unquoted.** The ELOOP error line is on the page but not in the set (Claim 2 quotes only probe output for ELOOP).
4. Supported as written: "judges just the last name" (paraphrase of Q3); "including magic links" (Q2 implies NO_MAGICLINKS, once the ELOOP line says "(or magic link)").
5. Hedge not carried, not needed for Claim 1's truth: the page's warning that NO_SYMLINKS set indiscriminately "may result in spurious errors" and should be configurable. Claim 1 is semantic, so it can stay out; any usage advice in the entry would need it.

**Verdict for Claim 1: overreach; rewrite needed.** The counter cannot see this: the original entry passes C2 (`QUOTES=9/9`, `C2=PASS`), as the frozen limits already say.

## Rewrite (Claim 1 with quote set; Q10–Q13 new, all S138, anchor `RESOLVE_NO_SYMLINKS`)

Claim 1. RESOLVE_NO_SYMLINKS makes the kernel refuse a symbolic link in every path component, including magic links, with ELOOP, whereas O_NOFOLLOW judges only the final component; the one exception the page names is a final-component link opened with O_PATH and O_NOFOLLOW, which returns a descriptor for the link. [Q2, Q3, Q10, Q11, Q12, Q13]

- Q10 | S138 | which affects the treatment of symbolic links in all of the components of path | RESOLVE_NO_SYMLINKS
- Q11 | S138 | ELOOP how.resolve contains RESOLVE_NO_SYMLINKS, and one of the path components was a symbolic link (or magic link). | RESOLVE_NO_SYMLINKS
- Q12 | S138 | the trailing component (i.e., basename) of path is a symbolic link, how.resolve contains RESOLVE_NO_SYMLINKS, and how.flags contains both O_PATH and O_NOFOLLOW | RESOLVE_NO_SYMLINKS
- Q13 | S138 | an O_PATH file descriptor referencing the symbolic link will be returned | RESOLVE_NO_SYMLINKS

Q12 is 21 words and Q13 is 11, both within 4–25. Claims 2–5 and Q1–Q9 are unchanged.

## Registry rows (L1 owns `corpus/SOURCES.md`; not edited)

- **S140 anchor cell** reads "lines P01, P02 and P04". The counter requires each quote's anchor to be a substring of the row's anchor cell, so P14 cannot be a quote. If L1 wants the P14 exception quoted from S140, it must widen that cell to include P14. The rewrite does not need it.
- **S138 "what it supports" cell** repeats "RESOLVE_NO_SYMLINKS refuses a symbolic link in every path component while O_NOFOLLOW judges only the final one" with no O_PATH exception. It has the same overreach and should gain the exception.

## Evidence (commands and observed output)

- Man page: `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx` (footer "Linux man-pages 6.19", 2026-07-02). Normalised text checked with `grep -c -F` for each new quote: Q10 → 1, Q11 → 1, Q12 → 1, Q13 → 1. The O_PATH sentence is ERRORS-independent and in DESCRIPTION under `RESOLVE_NO_SYMLINKS`.
- Header: `/usr/include/linux/openat2.h` — `RESOLVE_NO_SYMLINKS 0x04 /* Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS) */`. Q6 quotes this line verbatim; it supports "every component" but not the ELOOP wording.
- Probe: `python3 -B corpus/evidence/round62/controls/candidate-openat2-probe.py --work <scratch>/p` → exit 0; output `diff`s identical to `candidate-openat2-probe.txt`; last line `PROBE_FACTS=14/14`. P14: `openat2-O_PATH-O_NOFOLLOW-NO_SYMLINKS-final-symlink-fd-is-the-link observed=True expected=True ok`. P04/P05 show ELOOP for a symlink in an earlier and in the final component without O_PATH.
- Controls with the rewrite: a scratch lane copy (corpus copied, `captures`/`fixtures`/`evidence` excluded, `controls/` and `c2v2-count.py` copied, fleet `scripts/` symlinked for the census step) ran `run-c2v2-controls.py --work <scratch>/cw-rewrite --keep`:
  - `positive rc=0 ... QUOTES=13/13 ... CLAIMS=1/1 ECHO=1/1 ... C2=PASS OK`
  - all 25 variants `OK`; `C2V2_CONTROLS_UNEXPECTED=0`, exit 0.
  - `non-sequitur rc=0 ... C2=PASS OK` (named limit unchanged).
- Controls with the original entry (baseline, same harness): `positive rc=0 ... QUOTES=9/9 ... C2=PASS OK`; `C2V2_CONTROLS_UNEXPECTED=0`. The counter passes the overreaching original, so the counter gives no operability signal for this defect.
- Lane tree as-is: `python3 -B corpus/evidence/round62/c2v2-count.py` → `C2=FAIL`, `ROW S138 absent` (expected; the entry is not landed).
- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --short` (read-only): untracked `.ufo/waves/round-62/w1/` only from this wave; no tracked change from this seat.

## Out-of-scope observations (not rewritten; for the other reviewer)

- Claim 5: "so a caller should read the numeric flag values from that header instead of typing them from memory" is a recommendation that Q6 does not state. Q6 only quotes the header's description of the flag. Probable overreach.
- Claim 4: "needs ctypes" is an inference from Q5 (glibc has no wrapper, use syscall(2)); "ctypes" is not on the page. [INFERENCE]

## Limits

- Verified on one kernel (7.2.11), x86_64, one local filesystem; the O_PATH exception is from the page plus P14 on this host.
- Entailment is judged by this reviewer, not by the counter (the counter's named limit).
- Tools installed: none. Scratch `/fast/scratch/hyaku/chousa-r62/RevC2V2Claim1/` removed before yield.

VERDICT: CLAIM1=overreach rewrite_needed=yes
