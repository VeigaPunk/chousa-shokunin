# RevC2V2Claim2 — entailment review of Claim 2 (round 62, w1)

Scope: Claim 2 of `corpus/evidence/round62/controls/c2v2-positive-entry.md` (the landing candidate). Frozen `claims.md` sha256 `a3193ebd…866bc` matches the wave context. Nothing under `corpus/evidence/round62/`, `tools/`, `corpus/`, or `SKILL.md` was edited; no git, network, or tool installs. Candidate rewrite is under my own directory. Scratch `/fast/scratch/hyaku/chousa-r62/RevC2V2Claim2/` removed before yield.

## Findings

1. **Overreach in scope (main finding).** Claim 2 as written:
   > On this host the difference is observable: a path through a symlinked directory is opened by os.open with O_NOFOLLOW, and refused with ELOOP by openat2 with RESOLVE_NO_SYMLINKS. [Q7, Q8]

   Its two quotes are single observed results from one probe case each:
   - Q7 = `PROBE P02 os.open-O_NOFOLLOW-symlink-in-earlier-component observed=opened expected=opened ok`
   - Q8 = `PROBE P04 openat2-NO_SYMLINKS-symlink-in-earlier-component observed=ELOOP expected=ELOOP ok`

   The quotes support "the difference is observable" for that labelled case. They do not support the indefinite class claim "a path through a symlinked directory is opened … and refused …", which reads as "any such path". One probe case (one relative symlink, one local filesystem, one kernel) cannot carry that. The words "On this host" scope the kernel and Python, not the number of paths sampled. Calibration is the failing axis.

2. **Otherwise the claim follows from its quotes.** Q7 and Q8 are verbatim in the live probe output. The comparison is valid: P02 uses `O_NOFOLLOW` without `RESOLVE_*`, P04 uses `RESOLVE_NO_SYMLINKS` without `O_NOFOLLOW`, both on the same labelled case. The `expected=` fields are the probe author's predictions, not page text, and Claim 2 uses only `observed=`, so that is not overreach. The "same path" step rests on label parity (`symlink-in-earlier-component` in both). The probe source, which is not quoted, does use the same path string in P02 and P04; I read it. That is INFERENCE from the quote set alone.

3. **Hedges.** `On this host` is kept. The page's caution that NO_SYMLINKS "may result in spurious errors" and should be "made configurable" is usage advice, not a claim about observed behaviour, so omitting it does not change Claim 2's truth. Q3 (O_NOFOLLOW affects only the final component) is not quoted in Claim 2, but P02 is consistent with it. The entry's Limits (one kernel, one filesystem, x86_64) are not restated in Claim 2; the rewrite below keeps "on this host" and adds no new facts.

4. **Wording checks.** Claim 2 has no `all`, `any`, or `always`. The only host-specific fact stated as general is the "a path through a symlinked directory" phrase in Finding 1.

5. **Side note for Claim 5 (outside this item).** The installed header comment reads `Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS)`, with `OEXT_` where the define is `RESOLVE_`. Q6 quotes that text verbatim, so the quote is faithful. The entry's Claim 5 relies on this text; the typo should be noted if Claim 5 is reviewed.

**VERDICT for Claim 2: overreach (scope and quantifier, not the quotes). Rewrite needed.**

## Rewrite (quote set unchanged: Q7, Q8)

Old:
> Claim 2. On this host the difference is observable: a path through a symlinked directory is opened by os.open with O_NOFOLLOW, and refused with ELOOP by openat2 with RESOLVE_NO_SYMLINKS. [Q7, Q8]

New:
> Claim 2. On this host the difference is observable in the probe case with a symlink in an earlier component: os.open with O_NOFOLLOW opens the path, while openat2 with RESOLVE_NO_SYMLINKS refuses it with ELOOP. [Q7, Q8]

Candidate files (my directory, not the frozen entry):
- `.ufo/waves/round-62/w1/RevC2V2Claim2/c2v2-claim2-rewrite-entry.md` — the full entry with only Claim 2 changed.
- `.ufo/waves/round-62/w1/RevC2V2Claim2/c2v2-claim2-rewrite.diff.txt` — the one-line diff.

Entailment of the rewrite, term by term: "probe case with a symlink in an earlier component" ↔ the shared label in Q7 and Q8; "os.open with O_NOFOLLOW opens the path" ↔ Q7 `observed=opened`; "openat2 with RESOLVE_NO_SYMLINKS refuses it with ELOOP" ↔ Q8 `observed=ELOOP`; "the difference is observable" ↔ the two observations differ. The remaining step is label parity (INFERENCE, see Finding 2).

## Commands run and observed output

- `sha256sum corpus/evidence/round62/claims.md` → `a3193ebd328919e2af017011278e423c5940fd9447f0730bd400da9d15c866bc` (matches the frozen digest).
- `MANWIDTH=1000 man -l /usr/share/man/man2/openat2.2.gz | col -bx` (171 lines, Linux man-pages 6.19). Read and confirmed: "Disallow resolution of symbolic links during path resolution. This option implies RESOLVE_NO_MAGICLINKS." (Q2); "affects the handling of symbolic links only in the final component of path" (Q3); "Do not permit the path resolution to succeed if any component … is not a descendant" (Q4); "glibc provides no wrapper for openat2()" (Q5).
- `cat /usr/include/linux/openat2.h` → `RESOLVE_NO_SYMLINKS 0x04 … Block traversal through all symlinks (implies OEXT_NO_MAGICLINKS)` (Q6 verbatim); `RESOLVE_BENEATH 0x08`, `RESOLVE_IN_ROOT 0x10`, `RESOLVE_NO_MAGICLINKS 0x02`.
- `python3 -B corpus/evidence/round62/controls/candidate-openat2-probe.py --work /fast/scratch/hyaku/chousa-r62/RevC2V2Claim2/p` → rc 0; `KERNEL 7.2.11-arch1-1`, `PYTHON 3.14.8`, `PROBE_FACTS=14/14`; the output is byte-identical to `candidate-openat2-probe.txt` (`diff` printed nothing). Q7 and Q8 lines match.
- `python3 -B corpus/evidence/round62/controls/run-c2v2-controls.py --work <scratch>/ctl/base` → every variant `OK`, `C2V2_CONTROLS_UNEXPECTED=0`, exit 0. `positive` rc 0 `C2=PASS`; `non-sequitur` rc 0 `C2=PASS` (the recorded limit, expected).
- `driver.py` (scratch, prepared mirrors the same way the runner does, with only the entry changed):
  - mirror, original positive entry: `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS` (rc 0).
  - mirror, rewrite entry: `ENTRY=1/1 TRIO=1/1 ROWS=3/3 QUOTES=9/9 COVERAGE=1/1 CLAIMS=1/1 ECHO=1/1 LIMITS=1/1 PROBE=1/1 MAP=1/1 CENSUS=1/1 C2=PASS` (rc 0).
  - The rewrite passes the counter. The counter checks structure and echo only; it does not judge entailment (named limit). Entailment is the finding above.

## Not checked

- Entailment of Claims 1, 3, 4, 5. Outside this item.
- I did not run `c2v2-count.py` directly on the lane root: the lane has no `corpus/knowledge/openat2-resolve-r62.md`, so it would fail by design. The mirror runs above are the check the item asked for.
- No live fetch. No second kernel, filesystem, or architecture was probed.

## Tool installs

None.

VERDICT: CLAIM2=overreach rewrite_needed=yes
