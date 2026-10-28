# ExecIndepBuilder1 — round 61 w1, independent implementer of the C1 builder (strict policy)

Candidate: `.ufo/waves/round-61/w1/ExecIndepBuilder1/build-spans.py`
(sha256 19d1f41460def9eecb8626dc2362d256971b90dabb24d6837b60e06ca7bad651, from the counter's BUILDER line).
Inputs read: claims.md (the assignment's first step), c1-count.py lines 1-49 (docstring only), tools/build-spans.py (whole),
tools/capture-text.py by grep (to learn text_form(path) and MAX_PART). NOT opened: controls/ref-build-spans.py.
No labrat spawned; no install; scratch /fast/scratch/hyaku/chousa-r61/ExecIndepBuilder1 deleted.

## Findings
1. The counter docstring was enough to reach 20/20 on the first run. Legs first failed: NONE (I never ran a draft that
   failed; the one written draft was the one measured). I did not iterate on counter output, so "reachable from the
   docstring" is shown for one implementer, one draft — not for a population.
2. Policy as built (strict): refuse any symlink (DIR, DIR/spans, DIR/spans.tsv, any entry of DIR or DIR/spans: exit 2;
   cache .raw/.txt link: refused row, exit 1); any differing existing spans.tsv / span file / orphan `S###-n.txt` ->
   exit 2, nothing touched; identical existing output accepted (rebuild no-op); `--replace` overwrites/deletes output
   files only, never lifts the link refusal; reads via open(O_NOFOLLOW|O_NONBLOCK)+fstat S_ISREG (FIFO never blocks);
   64 MiB cap on file size (checked from fstat before reading) and on text form chars; writes via O_EXCL temp + rename;
   `sys.dont_write_bytecode=True` set before importing capture-text (the base's P03 failure cause).
3. Sweep `grep -nE 'getppid|/proc/|c1-count|round61|leg-|argv\[0\]'` on the candidate: exit 1 (no match).
4. Weakest observed number: H20 BIGFORM peak RSS 221-293 MiB (capture-text renders the 70 MiB form before my length check).
   The docstring sets no RSS limit for H20, so it passes, but the form is still built in memory (named limit iii/iv kind).
5. Known limits kept: check-then-write TOCTOU; capture-text.text_form reopens the raw path itself (second open, not
   O_NOFOLLOW; closed only by the earlier lstat/safe_read); memory is per-capture not summed.

## Evidence (commands run; all `python3 -B`, TMPDIR and --work under my scratch)
- `c1-count.py --builder <B> --work $S/w --seed 61101` -> LEGS=20/20 C1=PASS, exit 0
- `... --seed 61102` -> LEGS=20/20 C1=PASS, exit 0
- `... --seed 61103` -> LEGS=20/20 C1=PASS, exit 0
  Per leg (identical shape all seeds): P01-P06 pass (P04 rc=0,0,1; P06 rc=0,0); H07 rc=2,2; H08 rc=0; H09 rc=2;
  H10/H11/H12 rc=2 victim_unchanged=True; H13 rc=1 leaked=False; H14 rc=1 rss_kib=19460-20024 (limit 98304);
  H15 rc=1 rss_kib=19848-20120; H16 rc=2 traceback=False; H17 rc=1; H18 rc=1; H19 rc=2; H20 rc=1 rss_kib=220680-293148.
- `regress.py --builder <B> --work $S/rg` -> round55, round56, round57/c3 each `check_rc=0 build_rc=0 identical=True pass`;
  `REAL_REBUILD=3/3`, exit 0.

## Counter docstring ambiguities (7)
1. `--replace` (H08) is named only in the leg line; the builder docstring does not define the flag, and "the non-span file
   kept" does not say whether it sits in DIR or DIR/spans (I keep both: never touch non-output names).
2. H09 "a span file the run does not write": whether the match is the `S###-n.txt` pattern only, or any file in spans/.
   I used the pattern (SPAN_RE from the base).
3. H10-H12 accept either "exit non-zero" or "replaced by a regular file, golden tree": the docstring does not say which
   policy is expected; the assignment's strict policy decided it.
4. Size cap: H14/H15 give 192 MiB, RSS<96 MiB, but only H20 names "64 MiB chars"; the 64 MiB byte cap is read from
   claims.md (named limit ii), not from the docstring.
5. Exit-code precedence (1 refused row vs 2 output refused) when both apply is unspecified; I check output structure
   first (exit 2), rows second (exit 1), differing-content last (exit 2).
6. "nothing written": whether an empty created DIR or DIR/spans counts is unspecified (clean_out tolerates an empty dir
   per the leg name; my builder creates dirs only after every check passes, so the question never arose).
7. H20 states no RSS bound, though H14/H15 do; a 290 MiB build passes, which the stated "no timeout" criterion allows.

VERDICT: INDEP1_LEGS=20/20 REAL_REBUILD=3/3 ambiguities=7
