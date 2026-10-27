# R56MutC1GateNew — gate clause mutation coverage

**Scope / setup.** Read frozen claims at `corpus/evidence/round56/claims.md` first. Tested the gate from candidate `46e1758f3d8a5d1bf30200d2ff7d909b0230feed`; worktree builder blob equaled that candidate (`072415ad36d9167f4ebe8117765b7053fb261069`). The gate was copied to private scratch; as in frozen `c1-count.py`, every copy had H1 pinning `LANE` to this lane and H2 honoring `R56_ORACLE`; then exactly one listed behavior clause was changed per mutant. Source gate/battery/probes were not modified. Work and `TMPDIR` were under `/fast/scratch/hyaku/chousa-r56/R56MutC1GateNew`; `PYTHONDONTWRITEBYTECODE=1`. Tool `/usr/bin/soffice` was present. Pinned capture-text SHA matched `2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`.

**Detector command.** `python3 /fast/scratch/hyaku/chousa-r56/R56MutC1GateNew/run_matrix.py` (driver ran each gate variant against landed builder, all eight `battery/*.py` entries, and both probes; `--seed 7 --per-leg 2 --work` a fresh empty private directory per invocation; five parallel workers). Actual output: pristine candidate `(0,PASS,PASS,PASS,PASS)`; every regular battery entry had the same verdict vector under pristine and each mutant; `oracle-m8-unpinned.py` was `('ENV',2)` under all variants. The only changed probe vectors were:

```
G p1-forkexec.py (1, FAIL, FAIL, FAIL, FAIL) — GENOLE rc=97 AUDIT_FORBIDDEN _posixsubprocess.fork_exec
forkexec p1-forkexec.py (0, PASS, PASS, PASS, PASS)
G p2-dirfd.py (1, FAIL, FAIL, FAIL, FAIL) — GENOLE rc=97 AUDIT_FORBIDDEN os.chdir
chdir p2-dirfd.py (0, PASS, PASS, PASS, PASS)
```

Pristine battery outputs (also invariant across all eight mutants): M1 `(1,FAIL,FAIL,PASS,FAIL)` with `span is not a slice of the defined form`; M2 `(1,FAIL,FAIL,PASS,FAIL)` with `S901 char`; M3 `(1,FAIL,FAIL,PASS,FAIL)` with `S901 capture_sha256`; M4 `(1,FAIL,FAIL,PASS,PASS)` with `S901 QUOTE line`; M5 `(1,FAIL,FAIL,PASS,PASS)` with `extra or missing span files`; M6 `(1,PASS,PASS,FAIL,PASS)` with `REFUSE:NOFORM: spans.tsv written`; M7 `(1,FAIL,FAIL,FAIL,FAIL)` with `AUDIT_FORBIDDEN open .../SKILL.md` (and `rc=97`); oracle entry `('ENV',2)`. Landed builder all PASS. This records the four-leg vectors, not merely overall exit status.

| Single-edit mutant | Changed verdict vs pristine | Verdict / interpretation |
|---|---|---|
| Remove `_posixsubprocess.fork_exec` from `BAD` | P1 only: DENIED → all PASS | Killed by probe; hook closure tested. |
| Remove `os.chdir` from `BAD` | P2 only: DENIED → all PASS | Killed by probe; dirfd/chdir boundary tested. |
| Drop `len(lines) != len(expect)+1` | None | Survived this battery. |
| Drop row-echo comparison | None | Survived this battery. |
| Drop span-name/offset check | None | Survived this battery. |
| Drop REFUSE `span file written` check | None | Survived this battery. |
| Drop REGRESS per-file byte comparison | None | Survived this battery. |
| Drop pinned-capture digest check | None | Survived this battery. |

**Coverage gaps / distinguishing inputs for a successor battery.**

- Manifest cardinality: builder emits all expected rows plus one extra manifest row (with no extra file); existing extra-span-file entry tests files, not rows. The dropped shape check must then accept the extra row while pristine rejects `manifest shape`.
- Row echo: alter one row's URL, quote, or entry cell while keeping its span bytes, expected-name/offset, digest, and stdout echo consistent with the tampered row; pristine rejects `row echo`, mutant should pass. Existing entries alter other properties, not the echoed identity tuple.
- Span name/offset: emit a noncanonical manifest span filename or a non-digit offset while keeping correctly named expected file(s), slice and character position valid for the gate's subsequent checks; the mutant should accept what pristine rejects. A duplicate correctly named file can retain `have == names` while the row points to an alternate path, exercising specifically the name half.
- REFUSE span-file absence: on a refusal, do not write `spans.tsv` and do write a span file. This specifically tests the guard removed; M6 instead writes a header-only manifest and no span file, so `spans.tsv written` independently rejects it.
- REGRESS per-file compare: on the round-54 input only, preserve `spans.tsv` byte-for-byte but alter one emitted span-file byte. Current M1-M3 corruption also changes the manifest, so REGRESS's manifest comparison rejects before the per-file clause.
- Pinned digest: change a pinned `.raw` capture's bytes while retaining the digest-prefix mismatch, then run OLEPIN. Current inputs cannot distinguish this guard: pinned captures are read from the fixed read-only campaign cache and no battery entry controls those bytes. A successor needs a disposable isolated cache/input seam or an explicit environment fixture; do not mutate the shared cache.

**Hashes / restoration.** Scratch gate hashes after construction (the copies remained unchanged through detector runs): pristine-with-harness `c415fce62ab46c647d2e499ddd57b91704a1898dc4b6c6af4a9af57caddde17a`; mutants: forkexec `2860e69784668742535bf6f3583cfd335a141b02571112c2da422a302269c00d`, chdir `5df5a23ca5d71cf8ebfe707057e77df429bf16fd3ba8e1d957045d5c4e0b5c0b`, shape `cd783917192f3add6f8fa4d1f8768b6418cc3d0623570c5860ffb9f5fc9a4685`, row-echo `4b9f0d7a302bafc5a9e6de2fbbcaa09df22e0b72a029ee565a029aded7c9a44a`, span-name/offset `d5bdbd84122cf0fd2cfc5a1f5b7fa9bb0d164d2a78919fe8bae06f2166da3f33`, refuse-span-file `5ab547af9b692d5baaa231aa6631af64e46fd2653b6fc0399adcfd12c909da3e`, regress-file-bytes `dce0a034c03e992ab4d158ecd58e8986835c6f4c5ef17875da421d761fe53dc3`, pinned-digest `e639b9ba303aea816137b7df613e22b3c07a56199f2c369a4c4f1e5f3e68e718`. Original gate SHA256 `sha256sum` evidence recorded by source is not a post-edit hash; no source bytes were changed. Scratch was deleted after copying these receipts into this report. No tool installation.

VERDICT: Both new BAD-event clauses were killed by their respective probes; manifest shape, row echo, span name/offset, REFUSE span-file, REGRESS per-file, and pinned digest mutants survived this candidate battery, with distinguishing inputs specified above.