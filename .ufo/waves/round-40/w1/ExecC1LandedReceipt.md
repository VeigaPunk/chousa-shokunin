# ExecC1LandedReceipt — round 40, wave 1

Lane: chousa. Root: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Measured lane tip: `6bc90e04ac60307befacd554f7eee2b7284e2652` (HEAD at run time).
Assigned attack: run the committed verifier for the regenerated `c1-after-s39011`
receipt against `tools/research-gate.sh` and the current expectation bytes;
independently verify the receipt's status and the counter's 8/8 result.

**Verdict: PASS — claim supported by independent re-derivation and exact replay.**
The regenerated receipt verifies (exit 0), every bound digest re-derives from
current bytes, its 8/8 is reproducible byte-for-byte from the committed counter,
and the refusal paths that would let a stale or doctored receipt pass all fire.

## 1. Committed verifier, exact command and output

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round39/verify-receipts.py \
  --receipt corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json \
  --gate tools/research-gate.sh \
  --counter corpus/evidence/round39/c1-count.py \
  --expectations corpus/evidence/round39/expectations.jsonl
```
```
VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py
EXIT=0
```

## 2. Independent receipt-status re-derivation

Recomputed with `hashlib` directly from current files (not via the verifier):

| binding | receipt value | recomputed from current bytes | |
|---|---|---|---|
| `receipt_sha256` (self digest) | `eceb771a374cc9ac3683e2ea8768b262be503e894f6810bbda04ec9107cbfcd4` | same | MATCH |
| `gate_sha256` / `_pre` / `_post` | `4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3` | `tools/research-gate.sh` | MATCH, pre==post |
| `counter_sha256` | `91618e91640f748df76282244186088218d5f2b7a65364137fa6add29fea05d5` | `corpus/evidence/round39/c1-count.py` | MATCH |
| `expect_sha256` | `01cbdc3a8208a257e2b0ea4304c87a6d74be313a722cf667c5d126a4c29c583a` | `corpus/evidence/round39/expectations.jsonl` | MATCH |
| `verifier_sha256` | `1b6e0de688deda7493db3af5397d1e5bbf1fcdf556d8e254acae3ac6a8496267` | `corpus/evidence/round39/verify-receipts.py` | MATCH |

Status fields: `matched=8`, `total=8`, `predicate=ENV_PIN_CAPTURE_MATCH=8/8`,
`predicate_holds=true`; `predicate` is consistent with `matched/total`, and
`predicate_holds` with `matched==total`. All 8 scenario rows have `expect ==
observed` and `ok=true`, and the scenario census equals the eight frozen `c1`
ids in `expectations.jsonl` (`hold-plain`, `hold-fn-benign`,
`env-fn-echo-scrub`, `env-fn-root-move`, `env-fn-suppress`,
`env-override-missing`, `env-override-fake`, `capture-bash-path-pin`).
Top-level field set is the verifier's `KNOWN` set (17 keys, no extras) — the
strict-schema refusal has nothing to catch.

The expectations file at HEAD is the file being hashed above: `git hash-object`
and `git rev-parse HEAD:...expectations.jsonl` both return
`9ffee0b6340e8e04a223a89f9861c702bef2bb60`, and `git diff HEAD` shows no
working-tree delta for it. So the 8/8 binds the *current* expectation bytes, not
a passed-down copy.

## 3. Exact replay of the 8/8 (strongest form)

Re-ran the committed counter itself, fresh, at the receipt's seed:

```
python3 corpus/evidence/round39/c1-count.py --gate tools/research-gate.sh --seed 39011 \
  --receipt /tmp/exec-c1-landed-39011.json --tmp /tmp/exec-c1-landed-tmp
```
```
... PASS capture-bash-path-pin ...
ENV_PIN_CAPTURE_MATCH=8/8
EXIT=0
```

Replay artifact is **byte-identical** to the committed receipt:
`sha256(/tmp/exec-c1-landed-39011.json) = 482e716a4d5a57b5f9f62c3652b82b72ae21e3255b61f4b18d1edc35d99bd131`
= `sha256(corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json)`;
`cmp -s` → identical. A default-seed run (`seed=39001`) differs from the
committed body in exactly one key, `seed`; every other field, including all
eight scenarios, is equal. The committed receipt is therefore reproducible, not
merely self-consistent.

## 4. Counter results

Frozen round-40 counter, exact command and output:

```
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round40/c1-count.py
```
```
corpus/evidence/round40/receipts/c1-base-s39001-regenerated.json: ok VERIFY: ok receipt=c1-base-s39001-regenerated.json gate=base-gate-r39.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json: ok VERIFY: ok receipt=c1-after-s39011-regenerated.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round40/receipts/c1-mutenv-s39013-regenerated.json: ok VERIFY: ok receipt=c1-mutenv-s39013-regenerated.json gate=mut-gate-path-env.sh counter=c1-count.py
corpus/evidence/round39/receipts/c1-after-s39111.json: ok VERIFY: ok receipt=c1-after-s39111.json gate=research-gate.sh counter=c1-count.py
corpus/evidence/round39/receipts/c2-after-s39101.json: ok VERIFY: ok receipt=c2-after-s39101.json gate=research-gate.sh counter=c2-count.py
corpus/evidence/round39/receipts/c2-after-s39121.json: ok VERIFY: ok receipt=c2-after-s39121.json gate=research-gate.sh counter=c2-count.py
R39_ACTIVE_RECEIPTS=6/6
EXIT=0
```

Path-independent: the same command run with cwd=`/tmp` gave the same
`R39_ACTIVE_RECEIPTS=6/6`, exit 0 (the counter resolves `ROOT` from `__file__`
and passes `cwd=ROOT` to the verifier). The "8/8" in this seat's attack is the
per-receipt predicate above; the round-40 population predicate is 6/6. Both
hold.

Manifest sanity, computed independently of the counter: 6 data rows, 6 unique
receipt paths, 6 unique (receipt, gate, counter) triples, every receipt file and
every named gate file exists. No duplicate, no missing row.

## 5. Refusal bite (the 8/8 is re-derived, not a label check)

On `/tmp` copies only, no repository artifact touched:

| probe | result |
|---|---|
| A: flip `matched` 8→7 without resealing | `VERIFY-FAIL: receipt-self-digest`, exit 1 |
| B: flip `matched` 8→7 and reseal the digest | `VERIFY-FAIL: matched-recount-mismatch`, exit 1 |
| C: verify against an altered `expectations.jsonl` copy | `VERIFY-FAIL: expect-sha256-mismatch`, exit 1 |
| D: unmodified receipt (control) | `VERIFY: ok ...`, exit 0 |

Probe B is the important one: the verifier recounts `ok` from the receipt's own
`observed` rows against the frozen expectations and refuses a body that claims a
count its scenarios do not support. Probe C shows the expectation-bytes binding
is the thing this round's repair actually rests on.

## 6. What the repair repaired (grounded, not inferred)

- The current expectations file hashes to `01cbdc3a...`; all four superseded
  c1 originals bind the older `3abd2dcb1766c404228cf3929024856240a93ea374760ab77a390b92c3fb6480`
  (`c1-after-s39011.json`, `c1-base-s39001.json`, `c1-mutenv-s39013.json`,
  `c1-mutenv-s39003.json`). Re-running the verifier on the original
  `c1-after-s39011.json` therefore refuses on `expect-sha256-mismatch` — the R1
  defect this round's regeneration closes.
- The three replacement paths are absent at the pre-regeneration control tip
  `691d26476ac39b8ec8b65155b41199e6f6d1f299` (`git cat-file -e` returns absent
  for all three), matching the committed control's 3/6 / exit 1.
- Commit `d164f88` ("round-40: repair receipt evidence and calibrate r39
  records") adds only the three `corpus/evidence/round40/receipts/*-regenerated.json`
  files under `corpus/evidence/` and touches nothing under
  `corpus/evidence/round39/receipts/`; the only round-39 file it edits is
  `claims.md`. The committed originals are preserved byte-for-byte, as claimed.

## 7. Scoped observations and risks (no claim inflation)

1. `VERIFY: ok` proves receipt integrity and scenario re-derivation, not that a
   receipt's own predicate held. Two active rows are honest negatives —
   `c1-base-s39001-regenerated` (7/8) and `c1-mutenv-s39013-regenerated` (4/8),
   `predicate_holds=false` — and they still verify. That is consistent with the
   frozen C1 predicate, which counts `VERIFY: ok` lines; it would be a
   misreading to report 6/6 as six passing controls. The `predicate` string is a
   family constant (`ENV_PIN_CAPTURE_MATCH=8/8`) for every c1 receipt, so the
   outcome lives in `predicate_holds`/`matched`, never in `predicate`.
2. The verifier binds the gate by digest, not by the receipt's `gate` string; the
   receipt records an absolute path (`/home/vgpnk/.../tools/research-gate.sh`),
   the same convention as the original `c1-after-s39111.json`. Content binding
   holds (`gate_sha256` pre==post==alias==actual), so the absolute string is
   cosmetic, but it does make the receipt host-specific text.
3. Operability nit: `c1-count.py --tmp <dir>` exits 2 if the directory does not
   already exist (`c1-count: temp dir does not exist`), while
   `--receipt` succeeds on an absent parent dir. Reproduction of the 8/8
   requires creating the temp dir first.
4. Repository state note: `git diff --stat HEAD` in the lane shows
   `.ufo/waves/round-40/w1/swarm-registry.json` modified (36+/34-). That is the
   running wave orchestrator's registry, not this seat; this seat wrote only
   this report. No production file, git index, jj state, or fleet file was
   touched. `git diff HEAD` is otherwise clean.

## 8. Tooling

No installs or updates. No pacman transaction attempted (host-wide pause
respected). Python 3 and the in-repo scripts were sufficient.

## 9. Artifact pointers

- Receipt under test: `corpus/evidence/round40/receipts/c1-after-s39011-regenerated.json` (sha256 `482e716a4d5a57b5f9f62c3652b82b72ae21e3255b61f4b18d1edc35d99bd131`)
- Gate: `tools/research-gate.sh` (sha256 `4253c187...`)
- Counter: `corpus/evidence/round39/c1-count.py`; verifier `corpus/evidence/round39/verify-receipts.py`; expectations `corpus/evidence/round39/expectations.jsonl`
- Population: `corpus/evidence/round40/active-r39-receipts.tsv`
- Before-state evidence: `.ufo/waves/round-40/controls/control-before.txt`, `.ufo/waves/round-40/controls/r1-stale-before.txt`
- Replay output (ephemeral, reproduced by §3 command): `/tmp/exec-c1-landed-39011.json`, `/tmp/exec-c1-landed-39011.log`, `/tmp/exec-c1-landed-probes/`

## 10. Addendum — live-worktree drift observed after measurement (W0)

`tools/research-gate.sh` was edited in the lane worktree by concurrent round-41
work after the measurements above. Recorded because §1's command does not
reproduce against the *live* worktree until those bytes are committed or
reverted; the C1 claim binds committed HEAD, not the moving worktree. I did not
`git checkout` or otherwise touch the gate.

Observed at `2026-10-24T07:27:39Z`:

- live gate `sha256 = 2cb04bddfd5601d7c113a9b532a25895ce475847ff65f5672afc22586f5ffc34`,
  size 409022 B, mtime `2026-10-24 04:26:28.189 -0300`, `git diff --stat HEAD` = `+92 −2`.
- HEAD gate `sha256 = 4253c18738f84df9200cbc93f8e077ba63a418c5ee822c1324e1a8d75a9b07e3`
  (the sha my regenerated receipt binds).
- Verifier against the **live** gate:
  `VERIFY-FAIL: gate-sha256-mismatch`, exit 1.
- Verifier against HEAD bytes materialized to `/tmp` (`git cat-file blob
  HEAD:tools/research-gate.sh > /tmp/exec-c1-landed-gate-HEAD.sh`, sha
  `4253c187...`): `VERIFY: ok receipt=c1-after-s39011-regenerated.json
  gate=exec-c1-landed-gate-HEAD.sh counter=c1-count.py`, exit 0.
- Frozen counter on the **live** worktree: `R39_ACTIVE_RECEIPTS=2/6`, exit 1;
  the four rows naming `tools/research-gate.sh` fail
  `gate-sha256-mismatch` (`c1-after-s39011-regenerated`, `c1-after-s39111`,
  `c2-after-s39101`, `c2-after-s39121`). The base and mutant rows name frozen
  control gates under `.ufo/waves/round-39/controls/` and still verify.

So §1–§6 stand as a committed-HEAD result (they were measured with gate bytes
equal to HEAD, `git diff HEAD` clean for the gate at that time), and the live
2/6 is a transient dirty-worktree state owned by the round-41 edit, not a
counter or receipt regression. The gate digest binding is doing exactly its job.

Note for reconciliation: a peer report (`SentinelWriteScope`) cites live sha
`77791864e79cf80fbff57e2cca393facb44ca5d00bd2331466b912534f9ce841`; at
`07:27:39Z` I measured `2cb04bdd...` at mtime `07:26:28Z`. Both are pre-commit
worktree states of the same round-41 edit; the HEAD sha `4253c187...` is the one
any committed-artifact reproduction must use.
