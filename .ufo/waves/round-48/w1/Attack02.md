# Attack02 — C1 false-refusal precision probe (class #2)

## Scope and evidence

- Two distinct held-out bullets were composed only from committed local fixture inputs: `corpus/fixtures/inference-ground-r47/spans.tsv` (S901/S902 entries), `spans/S901-1.txt`, `spans/S902-1.txt`, and `counts.json` (values 7,572 / 5,959 / 1,582). No figures were needed. The S901 span says `the release ships a frozen pool of pages; no revision is recorded per sentence`; S902 says `the archived copy is dated at build time; a placeholder value is not an archive link`.
- Tool copied from working tree `tools/inference-ground.py`, SHA-256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`; lane tip observed `d4e6ef09b755a961bdae56566a7dcf0c9db0cfd7`. Inputs and probes were under `/tmp/chousa-r48-attack02/`; no network used.
- The round-48 spec labels this seat “precision class #2” but gives no semantic definition or mapping for the number; it only supplies the shared dimensions. This report treats the number as a seat label, not a distinct frozen class.

## Probes and results

Command (each run used scratch tool and scratch entry; committed fixture inputs):

```sh
python3 /tmp/chousa-r48-attack02/inference-ground.py \
  --entry /tmp/chousa-r48-attack02/probes/<probe>.md \
  --spans /tmp/chousa-r48-attack02/input/spans.tsv \
  --counts /tmp/chousa-r48-attack02/input/counts.json \
  --root /tmp/chousa-r48-attack02
```

1. **S901 — affirmed consequence of a negated phrase; unlisted absence word, distant from scope stem.** Correct bullet: “Because `no revision is recorded` per sentence, the revision ledger remains empty for each sentence (`S901`).” The quoted phrase is grounded verbatim. Tool output: `GROUND … tokens=1 grounded=1`; `FINDING INF_POLARITY_FLIP … 'no revision is recorded / revision'`; `GROUND: FAIL`, exit 1. **Correct bullet refused.** In the cited span, explicit `no` negates `revision`; in the bullet's unquoted text, `revision` restates that scope, but unlisted `empty` is not recognized by `is_neg`. It is outside the intended local negation relation; “remains empty” asserts absence, not presence. This is a false refusal under the tool's P1 window rule.

2. **S902 — affirmed date, neighboring-word binding.** Correct bullet: “Since `the archived copy is dated at build`, the captured byte string holds the copy's own snapshot clock, not the archive's build clock (`S902`).” Tool output: `GROUND … tokens=1 grounded=1`; two `INF_POLARITY_FLIP` findings, for `archive's` and `build`; `GROUND: FAIL`, exit 1. **Correct bullet refused.** The clause contrasts the copy's snapshot clock with the archive's clock. The local `not` scopes the neighboring phrase `the archive's build clock`, not S902's affirmed statement that the copy is dated at build. The detector's five-letter stem overlap binds `archive's` to “archived” and also binds “build,” then sees `not` within the preceding-three-word window for “build.” Thus the refusal is produced by lexical proximity despite correct contrastive scope.

Scratch negative controls were also run: same correct S901 conclusion without unquoted `revision` (“…when a sentence was last changed”) and same S902 contrast with no `not` (“…separate from the archive's build clock”). Both printed `GROUND: PASS`, exit 0. These controls isolate stem overlap and local negator binding as the causes; they are not additions to any fixture or claim.

## Assessment

Both correct bullets were refused (2/2 in this small, deliberately targeted probe); neither result estimates a population false-refusal rate. They test different mechanisms: an unlisted absence predicate (`empty`) with reused scope stem, and a negator scoped to a neighboring noun phrase but inside the reused stem's fixed window. This is evidence of precision risk/calibration cost in the lexical rule, not a frozen fixture, claim, or proposed post-score predicate change. The documented lexical limitation in `tools/inference-ground.py` does not make the readings semantically incorrect; the tool's own local-window heuristic explains the observed refusals.

No production files, fixtures, claims, counters, or other reports were changed. No installs.
