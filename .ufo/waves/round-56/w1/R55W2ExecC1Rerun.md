# R55W2ExecC1Rerun — attack on round-55 C1 after-state at `29cfb12abd70f688b48c0d17f31e636f2d81104a`

Attacked: R55-C1 after-measurement (`corpus/evidence/round55/c1-measure-after.txt`), i.e. `tools/build-spans.py` =
`corpus/evidence/round55/c1-count.py`'s four legs, at lane commit 29cfb12 (frozen claim
`corpus/evidence/round55/claims.md` at `1fc5d92b`). Lane HEAD when read: `99eff0eca3d7440aeb96a9afac6a421759b4f704`.
Scratch: `/fast/scratch/hyaku/chousa-r56/R55W2ExecC1Rerun` (removed; every receipt below is pasted from it).
Lane copy: `git -C <lane> archive 29cfb12… | tar -x -C $S/lane55`.

## 1. Artifact identity (the pin the seat asks for)

```
$ git -C <lane> cat-file -t 6ca924995d48facbf704d2aa22ddaec236059039
commit
$ git -C <lane> log -1 --format='%H %ad %s' 6ca92499…
6ca924995d48facbf704d2aa22ddaec236059039 Tue Oct 27 00:42:38 2026 -0300 round-55: C1 candidate — tools/build-spans.py
  reads every capture through its defined text form (OLE/zip raw via tools/capture-text.py; no UTF-16LE fallback)
$ git -C <lane> rev-parse 6ca92499…:tools/build-spans.py → 072415ad36d9167f4ebe8117765b7053fb261069
$ git -C <lane> rev-parse 29cfb12…:tools/build-spans.py → 072415ad36d9167f4ebe8117765b7053fb261069
$ git -C <lane> diff --stat 6ca92499… 29cfb12… -- tools/build-spans.py tools/capture-text.py
(empty)
$ sha256sum <lane>/tools/build-spans.py <lane>/tools/capture-text.py
1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6  tools/build-spans.py
2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573  tools/capture-text.py
$ sha256sum $S/lane55/tools/{build-spans,capture-text}.py   → same two digests
```

Observed: `6ca924995d48facbf704d2aa22ddaec236059039` is a **commit object**, not a blob (the seat spec and the receipt
header both call it the candidate's blob). The claim still holds: the commit's blob `072415ad…` is byte-identical to
29cfb12's and to the live lane's file (sha256 `1ed2650a…`), so the measured builder IS the candidate. `capture-text.py`
is exactly the pinned oracle `2c0140bc…` (enforced by the counter itself, `c1-count.py:441`).

## 2. The four measured runs (receipt reproduction)

`$ python3 <lane>/corpus/evidence/round55/c1-count.py --seed 7 --work $S/run7/w`
```
tool=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/build-spans.py sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 seed=7 per-leg=3
GENOLE=PASS 3 docs, 6 quotes
OLEPIN=PASS 4 captures, 12 quotes
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical
LEGS=4/4
C1=PASS
exit=0
```
Machine comparison of this block against `c1-measure-after.txt` (`--seed 7` block): **IDENTICAL: True** (all 7 lines).
Unseeded, three fresh `--work` dirs, seeds drawn by the counter:
```
seed=654561167 per-leg=3 → GENOLE=PASS 3 docs, 6 quotes / OLEPIN=PASS 4 captures, 12 quotes / REFUSE=PASS 4 cases /
  REGRESS=PASS r54 33 rows identical / LEGS=4/4 / C1=PASS  exit=0
seed=384704478 … (same 7 lines, identical) exit=0
seed=701729421 … (same 7 lines, identical) exit=0
```
`--per-leg 6 --seed 555` (seat's escalation):
```
seed=555 per-leg=6 → GENOLE=PASS 6 docs, 12 quotes / OLEPIN=PASS 4 captures, 24 quotes / REFUSE=PASS 4 cases /
  REGRESS=PASS r54 33 rows identical / LEGS=4/4 / C1=PASS  exit=0
```
Extra (`--per-leg 6`, unseeded `seed=562859768`): same 7 lines, `LEGS=4/4 C1=PASS exit=0`. Default `--work` (no flag,
mkdtemp under my `TMPDIR`) at seed 7: same 7 lines, `C1=PASS`, and 0 `r55c1-*` dirs left behind before and after.
**No FAIL occurred at any invocation**, so the seat's "name the leg, quote and line" branch did not trigger.

## 3. Determinism at a fixed seed

Two fresh seed-7 runs (`d1`, `d2`): `diff d1.log d2.log` → `LOGS_IDENTICAL`; all three per-run `out/spans.tsv`
manifests concatenated in sorted order → `MANIFESTS_IDENTICAL`. The receipt is a fixed point, not a lucky draw.

## 4. Do the four legs have teeth? (measured, on scratch copies of `tools/` only)

Each mutant = `lane55/tools` copied to `$S/m_<name>/tools`, one guard removed, run at seed 7:
```
off0   (off = 0 instead of text.find(quote))  GENOLE=FAIL S901 char · OLEPIN=FAIL S921 char ·
                                              REGRESS=FAIL spans.tsv differs from round 54's   → LEGS=1/4 C1=FAIL
utf16  (form := raw.decode("utf-16le") for OLE) GENOLE=FAIL S901 span is not a slice … ·
                                              OLEPIN=FAIL rc=1 refused S922 quote occurs 0x · REFUSE=FAIL UTF16: rc=0
exit0  (refusal exit 1→0)                     REFUSE=FAIL NOFORM: rc=0                          → LEGS=3/4 C1=FAIL
noquote(QUOTE stdout line dropped)            GENOLE=FAIL S901 QUOTE line · OLEPIN=FAIL S921 QUOTE line
txtpref(sidecar .txt preferred over OLE form) OLEPIN=FAIL rc=1 refused S924 quote occurs 0x · REFUSE=FAIL SIDECAR
```
Every mutation is caught with the leg's own named reason (and `c1-count.py:344-369` fixes the four refusal cases
NOFORM/SIDECAR/UTF16/NONWORD, env-failing if the list changes). Depth check behind OLEPIN: the pinned sidecars are NOT
the oracle form — `txt==form` was `False` for all four pins (form lengths 13041/27012/842/13718, sidecars
497501/128416/762265/241510 chars), so OLEPIN cannot be passed by reading `.txt`, and REFUSE-SIDECAR closes that route
independently.
REGRESS is against real bytes: `git show dba605de:corpus/evidence/round54/spans.tsv | wc -l` → `34` (header + 33 rows),
blob sha256 `7e1de3bff0b88389ade54d06701ef20525930fb7d7b3d3441ca9515126d60865`, byte-compared with every span file
(`c1-count.py:393-427`).

## 5. Operability findings (reported, not patched)

1. **`6ca9249…` is a commit, not a blob** (§1). Claim stands via blob `072415ad…`; any future citation should name the
   commit *or* the blob, not call the commit a blob.
2. **The counter does not pin the builder digest.** `c1-count.py:451-452` computes and prints `sha256=<tool>` but never
   compares it to a constant — only `capture-text.py` is pinned (`:441`). Evidence: `--tool` on a copy with one comment
   line appended ran the full battery (`sha256=72e86aa0…`, `C1=FAIL` on other grounds); `--tool` on my mutants ran and
   scored. So the after-state's tool identity rests on the manual hash/blob check in §1, not on the run itself. This is
   scope-appropriate for a developer-facing counter, but it means the receipt cannot prove which builder produced it.
3. **REGRESS needs the git checkout.** Running the same counter from the bare 29cfb12 archive (no `.git`) gives
   `ENV_CHANGED git show corpus/evidence/round54/quotes.tsv`, `exit=2` — the first three legs PASS, the fourth cannot
   run. Reproduction requires the lane repo (as the receipt did), and the counter reads round-54 expectations from
   `BASE_REV dba605de`, not from the working tree.
4. Residual `soffice.bin` seen on the host belongs to *other* seats' scratch
   (`…/chousa-r56/R56SentC1/…`, `…/R56DraftMistakes/…`); `pgrep -af soffice.bin | grep -c R55W2ExecC1Rerun` → `0`,
   none from my runs, and my scratch (profiles included) is removed.
5. No tool install or upgrade was needed (python3, git, soffice already present); no pacman/uv/npx transaction was run.

## Scope notes

Counters were run only read-only against the lane (`git archive`, `git show`, `sha256sum`); every mutation and every
`--work` directory lived under my scratch; no lane file, index, jj state, or sibling report was written. This item
attacks round 55's C1 only — the round-56 gate/battery/probes (C1') were not touched.

VERDICT: attacked round-55 C1's after-state at 29cfb12 (builder/oracle identity, seed-7 + 3 unseeded + per-leg 6 at
seed 555, determinism, and four-leg teeth via five mutants) — the claim SURVIVES: all invocations reproduce
`LEGS=4/4 C1=PASS` byte-identically with the receipt, no leg failed, and each leg kills the defect aimed at it; the
only defects found are citation/operability-grade (commit cited as blob, unpinned `--tool`, git-dependent REGRESS).
