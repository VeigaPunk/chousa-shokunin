# FC3 falsify — `claims-legacy-env-anchor-refused` (round27 attempt1)

- Target: dd72641e574679c4f7882dd43de072b4c8892d6f, gate sha256 ca39d14db907ec3fcf41ff0593658b4d6831fa82452944fe1f58463364992f84 (verified on the sandbox archive).
- Sandbox: `/tmp/chousa-r27-falsify-FC3ClaimsLegacyEnvAnchorR57` (git archive of dd72641). Base gate for comparison: `git show 64eec5d:tools/research-gate.sh` (sha256 c2c813f1…).
- Control under attack: `corpus/evidence/round27-regressions.py:215`. A claims source `<root>/synthetic.env:1` (an existing regular file containing a registry table) must give exit 1, `FINDING CLAIM_SOURCE_SESSION`, and one `^RESEARCH_GATE: ` line.
- Axis: calibration (C3). Freshness and operability are not touched.
- Installs: none.

## Verdict: FALSIFIED

There are three findings. The control is not vacuous against its own mutant, but it is insensitive to the r27 claims fix. Its expectation is legacy gate behaviour rather than something derived from the contract. A sibling input of the same class is read by the landed gate and reported CLEAN.

## (1) Is the expectation derived from the contract? Partly; mostly it is legacy gate semantics

- Contract C3 says: "Filesystem-path denylist checks must inspect complete filesystem paths, not citation-anchor prefixes; preserve existing citation-pointer semantics". The regressions file adds "Source paths are filesystem inputs too" and "A colon in a normal pathname is not itself forbidden".
- The complete path `<root>/synthetic.env:1` matches no denylist pattern, because `*.env` does not match a name ending in `:1`. It is refused only because `ptr_file_part` keeps the text before the first colon (`${p%%:*}`), and the gate's `is_denylist_fs_path` retains that prefix check as its second arm (gate lines 609-613).
- A claims `source` has no anchor semantics. With `notes.md` present, both `<root>/notes.md:1` and `notes.md:1` give `FINDING CLAIM_SOURCE_MISSING … not a readable regular file`, exit 1, on both the landed and base gates. So `:1` here is part of a file name, not a citation anchor, and "preserve citation-pointer semantics" does not cover this surface.
- The expectation therefore encodes the gate's legacy prefix refusal, not a contract rule. It mirrors the selftest case `metadata-colon-anchor-denylist-compat` (gate line 6492). It is a defensible fail-closed tradeoff, but it is not independent of the gate code. Side effect on the false-positive (over-refusal) side: `notes.env:2026.md` is an ordinary path whose complete form is not denylisted, yet it is refused as `CLAIM_SOURCE_SESSION severity=crit` on both landed and base gates.

## (2) Mutation: which fix does the control actually guard?

I used `probe.py` (sha256 b2db82e4…), which replicates the control's fixture, environment (`CHOUSA_*` stripped, `CHOUSA_STRICT=0`, `LC_ALL=C`), command and pass predicate. The first run used relative gate paths and exited 127 because the working directory was the temp root. That was a harness setup error and I discarded it. The results below come from the rerun with absolute gate paths, `timeout 120 python3 probe.py $M/<gate>.sh`, which exited 0.

| Gate variant | Control (absolute source, as shipped) | Same source via symlink alias |
|---|---|---|
| landed (ca39d14d…) | rc=1, `CLAIM_SOURCE_SESSION`: passes | rc=1, refused |
| base 64eec5d | rc=1, `CLAIM_SOURCE_SESSION`: **passes** | rc=1, `CLAIM_SPAN_NOT_FOUND` (file was read) |
| m1: the r27 claims change reverted (first check back to `is_denylist_path`, canonical check deleted; 9ee663a3…) | **passes** | `CLAIM_SPAN_NOT_FOUND` (file was read) |
| m4: first check uses the complete path only, canonical check kept (d92d3b5e…) | passes | refused |
| m2: prefix arm dropped from `is_denylist_fs_path` (28568bf0…) | **fails**: rc=1, `CLAIM_SPAN_NOT_FOUND`, no `CLAIM_SOURCE_SESSION`, 1 verdict line | read |

- Reverting the r27 production change to `claim_source_path` (m1, or the whole base gate) does **not** make the control fail. The control passes at base, so it does not detect the r27 claims fix.
- The control fails only under m2, a "purer" implementation of the contract that drops the legacy prefix check. It fails for the intended reason: the file is opened and checked for the span (`CLAIM_SPAN_NOT_FOUND`, and supported=1 CLEAN when the content contains the span). It is not a parse or setup error. So the control is a preservation guard for the prefix arm, not a regression control for the r27 fix.
- The r27 claims fix that actually matters for this input is the new canonical-target check at gate lines 1166-1170. Base and m1 read `alias.md -> synthetic.env:1`, while the landed gate refuses it. The shipped control never uses an alias, so it cannot see that fix. The alias in `claims-canonical-colon-denied` covers only the `.config` component case.
- The control cannot tell which pre-open check refused (m4 still passes). Its required string is only `FINDING CLAIM_SOURCE_SESSION`; it does not check `denied (not opened)`. This is minor, because both checks run before the open.

## (3) Counterexample of the same class: the landed gate reads a legacy-anchor `.env` path when a colon occurs earlier

Minimal case: claims source `<root>/a:b/synthetic.env:1`, a regular file inside the root containing `synthetic`, with span `synthetic` and expect `supported`.

- Landed gate: rc=0, `RESEARCH_GATE: CLEAN (claims=1 supported=1 … refused=0 …)`. The file is opened and its content is accepted as evidence.
- Its sibling `<root>/synthetic.env:1` (the control): rc=1, `CLAIM_SOURCE_SESSION`.
- Cause: `ptr_file_part` cuts at the first colon (`<root>/a`), and the complete path ends in `:1`. Neither arm matches.

Other cases in the same class that the landed gate reads: `x:y.env:1` and `a:b/op.env:7` in claims (both rc=0 CLEAN, absolute and alias forms). `--registry <root>/a:b/synthetic.env:1` and `--registry <root>/a:b/op.env:7` are also read (rc=0, `RESEARCH_GATE: CLEAN (entries=1 complete=1 …)`), and the entry `a:b/metadata.env:1.md` passes verify-metadata with rc=0 CLEAN while `metadata.env:1.md` is refused `META_ENTRY_REFUSED reason=denylist`. Base behaves the same, so this gap was inherited and not fixed. By contrast, `a:b/server.token:1` is refused because `*server.token*` is a substring pattern. Refusal therefore depends on which pattern style the denied name happens to use.

This contradicts the round's own C3 wording, "no reading a denylisted synthetic path when a colon occurs earlier", if the control's declared premise holds (that `X.env:1` is denylisted). One earlier colon makes that refusal disappear. Either the premise is wrong (see section 1) or the gate under-refuses. Either way the control and the gate disagree for this class.

## Smallest safe correction (author-lane advice)

1. Gate: in `is_denylist_fs_path`, check every colon prefix, not just the first. I tested this as mutant m6 (5a03d482…):

   ```bash
   is_denylist_path_value "$f" && return 0
   while [[ $f == *:* ]]; do
     f=${f%:*}
     is_denylist_path_value "$f" && return 0
   done
   return 1
   ```

   With m6, every probe case (plain, alias, earlier colon in a directory or name, `op.env`, `server.token`) is refused. `notes.md` stays CLEAN, and `metadata:synthetic.md` (entry) and `synthetic:ordinary.md` (registry) stay rc=0 CLEAN. `is_denylist_path`, the citation-pointer check, is unchanged.
2. Controls: add `a:b/synthetic.env:1` (claims and `--registry`) expecting refusal. Also add an alias variant `alias.md -> synthetic.env:1` so the control fails on base and m1. As shipped it does not.
3. Alternatively, if the legacy prefix refusal is not wanted (strict reading of "complete filesystem paths"), drop the second arm. The control's expectation then flips to "read". That is a calibration tradeoff for the canonical judge to decide, not something to fix silently.

## Limits

- I did not run the full `--selftest` or the regressions script, including on m6, because L1 owns those. m6 is therefore unverified against the 210 selftest cases. Cases such as `metadata-colon-anchor-denylist-compat` should still hold, since m6 only refuses more.
- I did not exercise verify-chain or verify-all on these paths.
- All fixtures were synthetic under `/tmp`. I used no network, host secrets or `/proc`, and made no lane edits apart from this report.
- Scratch files: `probe.py`, `probe2.py` (365a19ae…) and `mut/*.sh` in the sandbox.
