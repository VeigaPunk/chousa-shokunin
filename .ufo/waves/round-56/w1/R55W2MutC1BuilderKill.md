# R55W2MutC1BuilderKill — C1 mutation probe

Target: round-55 `tools/build-spans.py` at `29cfb12abd70f688b48c0d17f31e636f2d81104a`; frozen claim: `corpus/evidence/round55/claims.md` R55-C1. Scratch-only copy; counter: `python3 corpus/evidence/round55/c1-count.py --seed 7 --work <empty scratch dir>`.

Pristine sha256: `1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6`. Pinned `capture-text.py` sha matched claim (`2c0140bc04029c8faedc6c89a65bd657430d8b85f433406946567b70303e2573`). Fixture `git -C <scratch lane> rev-parse --show-toplevel` returned the scratch lane; `git show` provided the frozen BASE_REV materials to REGRESS.

Pristine receipt:
```
tool sha256=1ed2650af28ea8e392bc34f7259cfb58f93b05c7453aca60e86b170c59c80bf6 seed=7 per-leg=3
GENOLE=PASS 3 docs, 6 quotes
OLEPIN=PASS 4 captures, 12 quotes
REFUSE=PASS 4 cases
REGRESS=PASS r54 33 rows identical
LEGS=4/4
C1=PASS (exit 0)
```

| Mutant | Mutated behavior | Result / observed killing leg |
|---|---|---|
| M1 | Prefer `.txt` sidecar over OLE/zip `capture-text` form | KILLED — OLEPIN `FAIL rc=1` (expected form/digest mismatch); REFUSE also `FAIL SIDECAR: no refusal line for S942`. Overall `LEGS=2/4`. Mutant sha `f1bd4c485988de8e8f73177fb7c765b98e50461b0560878c38818413b1c4fd53`. |
| M2 | Decode otherwise-undefined raw as UTF-16LE | KILLED — REFUSE `FAIL NOFORM: rc=0`; overall `LEGS=3/4`. sha `94c406b2e06f7b97250f08aa699e212605da58ac358a21e0ebb895715ef9ddad`. |
| M3 | Use 79 chars before / 81 after quote | KILLED — REGRESS `FAIL spans.tsv differs from round 54's`; other legs PASS; `LEGS=3/4`. sha `224e93899d8c58d137cffc7a3aa5216d3b34ea8ab4730640b41535d16aaa66c9`. |
| M4 | Accept a quote occurring twice | SURVIVED — all legs PASS, `C1=PASS`. sha `ec555722993d8ecd3d92381a9b2a18cbb968ea80ab55fdf6207ab1c05fbe5566`. |
| M5 | Write spans output before returning refusal | KILLED — REFUSE `FAIL NOFORM: spans.tsv written`; `LEGS=3/4`. sha `251b6af53f4d6227144fad47284a2efeac76c5aa4fe3cd55327645a42b8cb0df`. |
| M6 | Drop universal-newline normalization for `.txt` forms | KILLED — REGRESS `FAIL spans.tsv differs from round 54's`; `LEGS=3/4`. sha `e5f3cbb82573c642c640bb77cc8ca470e71d84a8d1ca9f5a257b142aae7a6677`. |
| M7 | Put UTF-8 byte offsets in manifest and `QUOTE` output | KILLED — GENOLE `FAIL S901 span is not a slice of the defined form` (OLEPIN likewise S921); `LEGS=1/4`. sha `b7d2acbb2f413547778caee3a8506b3cac3c4c971e43cacfac8ef4660af1d194`. |
| M8 | Omit ZIP recognition branch | SURVIVED — all legs PASS, `C1=PASS`. sha `2315833d98facf73ac7b315933da54a31b2276588e2bdfff5465c4e2f7619a25`. |
| M9 | Explicitly refuse ZIP raw files | SURVIVED — all legs PASS, `C1=PASS`. sha `0fb696d2062459286a72721ce43c7b1461a064826e658700b624ff198647ad16`. |

Survivor coverage findings: M4 needs a refusal case with a quote occurring exactly twice in the defined form (the current positive generators select only count-1 quotes, and the four refusal cases do not exercise duplicate defined-form quotes). M8/M9 need a ZIP `.raw` input with a quote in its `capture-text.py` form; none of GENOLE, OLEPIN, REFUSE or REGRESS supplied ZIP raws. These are counter coverage findings, not proposed predicate changes.

Every mutant run was followed by copying the pristine bytes back; each per-run `sha256sum` returned the pristine digest and `cmp` reported `RESTORE=MATCH`. Final restored-byte run again passed all four legs (`C1=PASS`, exit 0); final pristine/copy hashes both `1ed2650a…c80bf6`, `RESTORED_BYTES=MATCH`. `SOFFICE_PROCESSES=0`. No tools installed.

VERDICT: R55-C1 mutation probe: six mutants killed; M4, M8 and M9 survived, exposing duplicate-occurrence and ZIP-input coverage gaps.