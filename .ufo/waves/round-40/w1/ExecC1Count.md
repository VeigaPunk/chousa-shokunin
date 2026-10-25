# Executor confirmation — frozen round-40 C1 counter (round 40, w1)

**Seat:** ExecC1Count (leaf). **Attack (verbatim):** "Run the frozen round-40 c1-count.py
command on the committed tree and confirm its six-row manifest, exact output, and exit code."
**Lane root:** `/home/vgpnk/Projects/shokunin/chousa-shokunin`. **Tree:** HEAD
`6bc90e04ac60307befacd554f7eee2b7284e2652`; worktree carries one sibling bookkeeping edit
(`.ufo/waves/round-40/w1/swarm-registry.json`) and sibling report files, none of which are
counter inputs.

## Verdict

**CONFIRMED.** On the committed tree the frozen command prints exactly the frozen seven-line
block (six row lines plus the summary), ends at `R39_ACTIVE_RECEIPTS=6/6`, writes nothing to
stderr, and exits 0. The
manifest has exactly six data rows, six distinct receipt strings, three tab-separated fields
per row, and every named receipt/gate/counter exists. All fifteen counter inputs are
byte-identical to their HEAD blobs, so the run is against committed bytes. The counter is
deterministic (two runs diff-clean, 0.168 s) and fails closed under every mutation I applied.

Two bounds on the signal, both latent at tip (details below): the six-distinct-receipt guard
is lexical, and `6/6` counts *verifying receipts*, not predicate-holding runs — two active
receipts attest `7/8` and `4/8` with `predicate_holds=false`.

## Exact command and output

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round40/c1-count.py; echo "EXIT=$?"
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: ok VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: ok VERIFY: ok receipt=c1-after-s39111.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round39/receipts/c2-after-s39101.json: ok VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
corpus/evidence/round39/receipts/c2-after-s39121.json: ok VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
R39_ACTIVE_RECEIPTS=6/6
EXIT=0
```

Channel discipline: `stdout` = 7 lines, `stderr` = 0 bytes, final line byte-exact
`R39_ACTIVE_RECEIPTS=6/6$` (`cat -A`, no trailing whitespace). Two consecutive runs are
byte-identical (`cmp` clean). Wall time 0.168 s. Output matches
`corpus/evidence/round40/measure-after.txt` line-for-line; that file was recorded at
`d164f88`, and `git diff --stat d164f88..HEAD -- corpus/evidence .ufo/waves/round-39
.ufo/waves/round-40` shows only `measure-after.txt` added, so the recorded after-state still
describes current evidence bytes.

## Six-row manifest audit (`corpus/evidence/round40/active-r39-receipts.tsv`)

Header + one comment + **6 data rows**, 3 fields each, 6 unique receipt strings, 6 distinct
files, 0 CRLF/trailing-tab rows, all paths present. Semantic content of the six rows:

| # | receipt | family | matched/total | `predicate_holds` | verifier |
|---|---|---|---|---|---|
| 1 | `round40/receipts/c1-base-s39001-regenerated.json` | c1 | 7/8 | false | ok |
| 2 | `round40/receipts/c1-after-s39011-regenerated.json` | c1 | 8/8 | true | ok |
| 3 | `round40/receipts/c1-mutenv-s39013-regenerated.json` | c1 | 4/8 | false | ok |
| 4 | `round39/receipts/c1-after-s39111.json` | c1 | 8/8 | true | ok |
| 5 | `round39/receipts/c2-after-s39101.json` | c2 | 8/8 | true | ok |
| 6 | `round39/receipts/c2-after-s39121.json` | c2 | 8/8 | true | ok |

Rows 1 and 3 are the r39 base and mutant **controls** (7/8, 4/8); including them is correct
for a receipt-integrity claim (the verifier requires `predicate_holds == (matched == total)`,
not `predicate_holds == true`), but it means **`6/6` must not be read as six passing runs**.
The frozen claims' wording ("the six selected active round-39 evidence receipts verify") is
accurate; SCORECARD's "active receipts 3/6 → 6/6 verify" is consistent.

## Exclusion set = refusal set (checked, not assumed)

The four non-active originals each refuse under the committed verifier; nothing that verifies
is excluded:

```
corpus/evidence/round39/receipts/c1-base-s39001.json    rc=1 VERIFY-FAIL: expect-sha256-mismatch
corpus/evidence/round39/receipts/c1-after-s39011.json   rc=1 VERIFY-FAIL: expect-sha256-mismatch
corpus/evidence/round39/receipts/c1-mutenv-s39013.json  rc=1 VERIFY-FAIL: expect-sha256-mismatch
corpus/evidence/round39/receipts/c1-mutenv-s39003.json  rc=1 VERIFY-FAIL: counter-sha256-mismatch
```

This reproduces `.ufo/waves/round-40/controls/r1-stale-before.txt` line-for-line. (I passed
`mut-gate-path-env.sh` for s39003 where that control used `research-gate.sh`; the first
refusal is counter-binding, before any gate check, so the verdict is gate-independent.)

Provenance of the stale digest `3abd2dcb1766c4…`: it matches **no blob anywhere in the
repository** — I hashed every object in the object database (15,052, unreachable included)
and found zero sha256 hits. The r39 `expectations.jsonl` is `01cbdc3a8208a2…` at every commit
that ever touched it (`6d914e9`, and the two branch views `35e10b9`/`7180206`); r38's file is
`d34f1735…`/`7cd5d824…`. So the three stale receipts bound **never-committed input bytes** —
that is the actual R1 defect, and reissuing against committed bytes is the right repair.
The excluded originals bind the committed r39 counter digest `91618e91…`; only expectations
were uncommitted. `c1-mutenv-s39003` binds counter `1c3b2a9e…`, which is no committed version
of `round39/c1-count.py` (`91618e91…` at every commit) — correctly dropped rather than
reissued, matching `corpus/lessons/round-40.md` and the R2 disposition.

## What "regenerated" changed (field-level diff, all three pairs)

Differing fields: `expect_sha256`, `receipt_sha256` — **nothing else**. Seeds (39001/39011/
39013), gate/counter/verifier digests, all eight scenario rows, `matched`/`total`
(7/8, 8/8, 4/8) and their `ok` flags are identical to the originals. Because the gate and
counter bytes and seeds are unchanged, a deterministic re-run must produce exactly this
diff — and a pure re-seal produces it too. The receipt schema carries no timestamp or run-id,
so the C1 predicate cannot and does not distinguish re-run from re-seal. Stated as a bound,
not a defect: the frozen claim binds bytes, not provenance.

## Fail-closed controls (temp copies under `/tmp/c1audit-ExecC1Count/`, lane bytes untouched)

| variant | result |
|---|---|
| pristine copy | `6/6`, exit 0 |
| three round-40 replacements removed = frozen do-nothing control | `3/6`, exit 1, block byte-identical to `control-before.txt` |
| one `ok` flag flipped in active receipt | `5/6`, exit 1 |
| `expectations.jsonl` removed | `0/6`, exit 1 |
| manifest truncated to 5 rows | exit 2, `R39_RECEIPT_MANIFEST=unexpected-population` |
| manifest row duplicated (6 rows, 5 unique strings) | exit 2, same message |
| `routed-defect-dispositions.json` removed | `6/6`, exit 0 (C1/C2 separability holds) |
| stray forged `zz-forged.json` added to `receipts/` | `6/6`, exit 0 (population is manifest-driven; no glob) |
| `tools/research-gate.sh` bytes appended | `2/6`, exit 1 |

The control reproduction is the important one: the recorded "before" is a real measurement,
not prose — deleting exactly the three replacements regenerates it byte-for-byte. Commit
order also holds: `control-before.txt` added `6c01a41` 03:45:34, replacements `d164f88`
04:01:53, `measure-after.txt` `282dc76` 04:08:45 (control precedes data).

## Predicate bounds found (independently reproduced; latent at tip)

1. **Path-alias duplicate.** Row 5 (`c1-after-s39111.json`) replaced by
   `corpus/evidence/round40/receipts/./c1-after-s39011-regenerated.json` (or the
   `receipts/../receipts/…` form): both rows print `VERIFY: ok`,
   `R39_ACTIVE_RECEIPTS=6/6`, exit 0 — while only **5 distinct files** exist and the s39111
   evidence is absent. Cause: `c1-count.py` dedupes on the raw string
   `{row[0] for row in rows}` and only normalizes at `ROOT / row[0]`. Matches the
   counterexample in `CriticC1Predicate.md` (my first attempt used the wrong row index and
   is discarded; the corrected index-5 runs above are the evidence).
2. **Absolute-path escape.** Row 5 pointed at `/tmp/…/outside-s39111.json`: `6/6`, exit 0,
   one receipt resolved outside `ROOT` (`escapes_root=1`), because `pathlib` lets an absolute
   right-hand operand override the join.

At committed tip neither is live: rows=6, distinct strings=6, **distinct files=6,
escapes=0**. P1 passes honestly today; its "six distinct receipts" guard is lexical, not
file-level, so the success string alone does not certify distinct evidence if the TSV is
edited.

## Verification limits (plain)

`verify-receipts.py` re-derives each row's `ok`/`matched`/`predicate_holds` from the receipt's
**own** `observed` block against frozen expectations; it never re-executes the gate or
counter. A receipt is therefore an attestation bound to artifact bytes, and a self-consistent
re-sealed fabrication would pass (the critic demonstrated it; I only exercised byte tamper,
which is caught). The counter also never compares the receipt's descriptive `gate`/`counter`
strings to the manifest columns — only the digests of the paths it is handed.

## Axis read

- **Operability:** one command, lane root, 0.17 s, no network, no writes, deterministic,
  fail-closed, exit code 0 iff 6/6. Reproducible by any seat without setup.
- **Calibration:** the number is byte-exact but narrower than its label — two active receipts
  attest non-holding predicates, and the population guard does not survive a path alias.
- **Depth:** exclusion set, stale-digest provenance (no committed blob), replacement field
  diff, and population-driver behavior were traced to source bytes rather than prose.

## Residual risks

1. Lexical population guard (alias/absolute rows) — latent; one `resolve()` before dedupe
   closes it.
2. Attestation vs execution: no gate re-run, so "verified" ≠ "measured now".
3. `6/6` reads as evidence strength; a footnote in the claims or scorecard row would remove
   the ambiguity (the base 7/8 and mutant 4/8 control receipts are deliberately in-band).
4. `EXPECTED_ACTIVE = 6` is hardcoded while the manifest is an unguarded TSV: they must move
   together (a mismatch fails loudly at exit 2, so this is a coupling note, not a hazard).

## Artifacts

- Verbatim after-state: `corpus/evidence/round40/measure-after.txt`; before-state:
  `.ufo/waves/round-40/controls/control-before.txt`; refusal reasons:
  `.ufo/waves/round-40/controls/r1-stale-before.txt`.
- Discardable probe trees: `/tmp/c1audit-ExecC1Count/{base.vgpnk,v1,v2,v3,v4,v5,v6,v7,a1,a2,a3}`
  (each contains `.out` with the captured run). The A1/A2/A3 manifests are the alias/escape
  reproducers.

## Addendum — worktree drift, then tip move, after this measurement (recorded, not re-run)

**Scope of every number in this report: lane tip `6bc90e04ac60307befacd554f7eee2b7284e2652`.**

**Measurement window of this report:** gate `tools/research-gate.sh` sha256
`4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3`, identical to
`git cat-file -p HEAD:tools/research-gate.sh`; run completed ≈04:20, report written 04:22.

**Live drift reported by SentinelWriteScope** (accepted as ground truth per protocol; I did
not re-run to confirm, and I did not `git checkout` the gate): at 04:23:46 the worktree gate
carries an 85-line "round-41 C1 capture-tool pins" block, sha256
`77791864e79cf80fbff57e2cca393facb44ca5d00bd2331466b912534f9ce841` (HEAD stays
`4253c187…`), and the frozen command then prints `R39_ACTIVE_RECEIPTS=2/6`, exit 1, with four
rows refusing `gate-sha256-mismatch`. Their control — HEAD gate bytes written into
`mktemp -d` — returns `6/6` again.

This is the designed behaviour, and it matches my own V7 control: appending bytes to
`tools/research-gate.sh` in a copied tree gave `2/6`, exit 1 (the two rows bound to the base
and mutant gates still verify). The counter reads worktree bytes, so:

- **Verdict unchanged for the committed tree:** P1 is a committed-bytes predicate, and the
  frozen command executed on a clean committed tree prints `R39_ACTIVE_RECEIPTS=6/6`, exit 0.
- **Never quote `6/6` without the gate sha and timestamp.** Under worktree drift the same
  command prints `2/6`, exit 1 — a correct refusal, not a regression.
- Any 6/6 reported after 04:23:46 must carry a gate sha of `4253c187…` (or be measured in a
  tree where the gate matches HEAD); a `2/6` carrying `77791864…` is gate drift, not a
  manifest or receipt defect.

**Phase 2 — the drift is now committed (SentinelWriteScope, 04:32:19–04:32:43).** Lane tip
moved `6bc90e0 → b173b09 → 1bd9001 → a3aac04`; `1bd9001` commits `tools/research-gate.sh`
at sha256 `2cb04bdd…`, 409,022 B (HEAD blob `ae10363a…`; the `6bc90e0` blob was `0c2ea6bc…`,
404,197 B — metadata read at update time, the counter was not re-run). At tip `a3aac04`,
`c1-count.py` prints `R39_ACTIVE_RECEIPTS=2/6`, exit 1, and the same six manifest rows run
against `git cat-file blob 6bc90e0:tools/research-gate.sh` give `6/6`.

Read this as a **scope boundary, not a regression**: the six active receipts bind r39/r40
gate bytes (`4253c187…`), so any later commit to the gate necessarily makes the four
`research-gate.sh` rows refuse `gate-sha256-mismatch` — exactly the designed kill-rule
refusal. Round-40's frozen P1 was defined against the round-40 committed tree, so:

- **Cite `6/6` only as `6bc90e0`-scoped** (`gate 4253c187…`, measured ≈04:20).
- **Do not cite `6/6` as the current state.** At `a3aac04` the same command prints `2/6`,
  exit 1, because round-41 replaced the gate bytes the manifest rows name.
- A round-40 receipt set cannot be re-verified against a round-41 gate; re-binding would be
  a new claim in a new round, not a repair of this one.
- Tip has since advanced to `d720b1d` with the gate unchanged from `1bd9001` (per
  SentinelWriteScope's W0 timeline); the `2/6` reading therefore also holds there. My own
  metadata reads stopped at `a3aac04`.

## Tooling / footprint

No installs, no pacman transactions, no network. `python3` 3.14.8, coreutils, read-only git
(`--no-optional-locks`); every mutation ran in `/tmp` copies. No lane production file, git
index, jj state, fleet repo, or sibling repo touched. **Only file written: this report.**
