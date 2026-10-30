# Attack14 — C1 frozen-case attack: missing-blob branch and nearby bypasses

Seat: Attack14 (lane chousa round65, leaf critic). Freeze `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`.
Target of attack: claim C1 predicate R65-C1 (`c1-count.py`, 20 frozen cases) and its behavioral oracle
`corpus/evidence/round65/controls/ref-receipt-pin.py`. No frozen bytes altered; all probes bounded and
isolated under `/fast/scratch/hyaku/chousa-r65/Attack14/` (deleted on exit).

## Verdict up front

- **Forged-digest / wrong-identity bypass: not found.** Every receipt accepted by the reference truly binds
  the Git blob at `BASE` for its declared path and pins `--revision`. No provenance or identity regression.
- **Nearest malformed-receipt bypass outside the frozen `missing-blob` case: CRLF / lone-CR line endings.**
  The reference **accepts** them (`RECEIPT_PIN=PASS`, exit 0). The frozen counter has **no line-ending case**,
  so it **does not detect** this class — neither a target that inherits the leniency nor one that rejects it
  can be distinguished by R65-C1.
- Classification per the claim's own boundary ("interface/consistency coverage, not … general parser
  safety"): **disclaimed-scope tradeoff**, not a defect the canonical judge must reject. Smallest safe
  correction is documentation now; tightening the validator/counter is a *new-round* action, not fixable
  inside this freeze.

## Branch under attack

Frozen `missing-blob` case (`c1-count.py:16`): receipt claims digest `h(SKILL.md)` for path
`missing-r65.md`, expects exit 1. Reference branch:

```python
q=subprocess.run(['git','-C',a.root,'cat-file','blob',a.revision+':'+m[2]],capture_output=True)
if q.returncode or hashlib.sha256(q.stdout).hexdigest()!=m[1]: raise ValueError('blob/digest')
```

Detection works by `cat-file` *failure*. The adjacent weakness is on the parse side, not the resolution
side: `pathlib.Path.read_text(encoding='utf-8')` opens in text mode with **universal newlines**, so the
byte-level format (LF headers, LF blank separator) is never enforced.

## Counterexample (bounded probes, evidence: `attack14-probes.txt`)

Same valid receipt bytes, only line endings changed (digest still `sha256(BASE:SKILL.md)`):

| variant | reference exit | output |
|---|---|---|
| canonical LF | 0 | `RECEIPT_PIN=PASS` |
| CRLF (`\r\n`) | **0** | `RECEIPT_PIN=PASS` |
| lone CR (`\r`) | **0** | `RECEIPT_PIN=PASS` |
| mixed CR/LF | **0** | `RECEIPT_PIN=PASS` |
| body with NUL byte | **0** | `RECEIPT_PIN=PASS` |
| no final newline | **0** | `RECEIPT_PIN=PASS` |
| leading blank line before REVISION | 1 | `RECEIPT_PIN=FAIL header/body` |

Mechanism: universal-newline normalization happens before `splitlines()`, so the header positional checks
(`lines[0..3]`, blank separator at `lines[3]`) all see normalized LF text. A non-canonical-byte receipt is
admitted as fully consistent. Impact is bounded: the digest still binds the true `BASE:SKILL.md` blob and
`--revision` is still pinned, so authenticity of the *bound object* is intact; the failure is strictness —
a downstream byte-exact reader can disagree with the validator's verdict on the same file.

## Hypotheses tested and refuted (local evidence)

1. **Git pathspec-magic path rebinding** (`:(top)SKILL.md`, `:(icase)SKILL.MD`, `:(glob)SKILL.*`,
   `:(literal)SKILL.md`): `git cat-file blob <rev>:<path>` does **not** resolve pathspec magic
   (`git_resolves=False` for all four) → reference rejects (`blob/digest`). The `rev:path` layer is literal.
2. **`./SKILL.md` normalization asymmetry**: git *does* resolve it, but the reference's
   `str(rel)!=m[2]` check (pathlib normalizes away `./`) rejects it (`path`). Defense holds.
3. **`/SKILL.md`, `//SKILL.md`, `SKILL.md//`, `x/../../SKILL.md`**: git does not resolve the first three;
   reference rejects all (`path`, via `is_absolute` / parts checks). Frozen `absolute`/`traversal` cases
   already cover this family.
4. **Header injection via extra lines**: positional strictness + `lines[3]` blank-separator check rejects
   interleaved content (`header/body`); BOM rejected; duplicate-header covered by frozen `duplicate` case.

## Does the frozen counter detect the CRLF bypass?

**No.** Re-ran the frozen counter against the frozen reference: `CASES=20/20 C1=PASS`, exit 0, `--work`
removed on exit — identical to frozen `controls/c1-positive.txt`. All 20 cases are LF-only; a target that
accepts CRLF receipts (matching the reference) and a target that rejects them both score identically on
R65-C1. The predicate is unaffected because the bypass input is not a frozen case.

## Impacted axes

- **C1 (operability, 3/10):** predicate numerically unaffected; coverage gap on malformed-encoding inputs.
  The gap is *within* the claim's explicit disclaimer of parser-safety coverage.
- **C2:** unaffected; suggested as a documentation site (see below).
- No identity/provenance/freeze axis impact. No duplicate authority: reference remains the sole oracle;
  counter remains the sole scorer.

## Smallest safe correction

1. **This round (inside freeze):** none to code or counters. Record the leniency in
   `corpus/knowledge/receipt-identity-r65.md` (C2 scope: "reported exit vs execution authenticity" is
   adjacent — a validator verdict on non-canonical bytes is a *reported* consistency, not byte-level proof).
2. **Next round (requires new claim/unfreeze):** add frozen cases `crlf` and `lone-cr` expecting exit 1, and
   harden the validator with `open(newline='')` + explicit `\n` line splitting. Not actionable under the
   round-65 freeze-and-kill rule.

## Supporting observations (no action required)

- Worktree at freeze commit is dirty (`SKILL.md`, `corpus/*.md` modified). The counter derives expectations
  from `git cat-file blob BASE:SKILL.md`, never the worktree, so a working-tree-hashing target fails the
  three positive cases *right now* — the "no working-tree hashing" property is live-tested by accident.
- Counter hygiene verified: non-empty `--work` rejected; work dir deleted on exit
  (`work_exists_after=False`).
- No tools installed this seat (python3 stdlib + system git only; probes used `git cat-file` and
  `hashlib` already opened as S154–S155).

## Evidence

- `attack14-probes.txt` (this folder) — full probe transcripts, both batches, plus frozen-counter
  determinism re-run.
