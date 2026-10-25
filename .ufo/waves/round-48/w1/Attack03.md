# Attack03 — held-out C1 precision probe

## Scope and evidence

Two fresh one-bullet Inference probes test correct reasoning over committed local fixture `S901`, not frozen fixtures or claims. Basis: `corpus/fixtures/inference-ground-r47/spans/S901-1.txt:1` says “the release ships a frozen pool of pages; no revision is recorded per sentence”; `spans.tsv:3` binds that exact phrase to S901; `counts.json:2-6` contains only figures and is unused here. The probe text is new and does not reuse round-47 held-out bullets. Current tool was `tools/inference-ground.py` at lane HEAD `d4e6ef09b755a961bdae56566a7dcf0c9db0cfd7`, SHA-256 `9d789b34562cc0ce35be7e4d7ea67a9fa57eabf8794bbf096c8a8d190925149b`.

Scratch copies under `/tmp/chousa-r48-attack03` were run against copied committed `spans.tsv`, `counts.json`, and span text. Scratch was removed after runs. Example body hashes: p1 `4f5ebbd8b92e57507dbdfc525768f61ae2dc6889f66f7f48429294456a8c68dd`; p2 `50c6a96dcdccfa627173043f4a82ccf063a22547370324d1b76d433babeef717`.

## Results

1. **Pass — correctly refuses scope transfer.** “The clause-specific `no revision is recorded` does not establish that the release is revisionless; the unavailable record concerns per-sentence history, while pool membership is separate (`S901`).”
   - Command: `python3 tools/inference-ground.py --entry /tmp/chousa-r48-attack03/bodies/p1.md --spans /tmp/chousa-r48-attack03/spans.tsv --counts /tmp/chousa-r48-attack03/counts.json --root /tmp/chousa-r48-attack03`
   - Observed: `GROUND ... bullets=1 tokens=1 grounded=1`; `GROUND: PASS`; exit 0.
   - Reason: the correct bullet explicitly distinguishes the sentence-level scope of the source negation from release-level revisionlessness. While the bullet reuses `revision`, the source scope-word window reaches `does not` in the bullet before that word, so P1 recognizes an in-window negator and does not call this opposite polarity. The qualifying words “revisionless”/“unavailable” do not assert a positive revision record.

2. **Refused — scope and neighbouring-word binding produce a false refusal.** “Although `no revision is recorded` applies to individual sentences, the release-level revision ledger is unobservable, so one must not infer that it was nonexistent (`S901`).”
   - Command: same command with `p2.md`.
   - Observed: `GROUND ... bullets=1 tokens=1 grounded=1`; `FINDING INF_POLARITY_FLIP bullet=1 token='no revision is recorded / revision'`; `GROUND: FAIL`; exit 1.
- Reason: this is correct: source denies a *per-sentence* record, and the bullet says the separate *release-level* ledger cannot be observed and explicitly rejects an inference that it is nonexistent. But `revision` shares the five-letter `revis` stem with the source phrase; the three preceding words at that occurrence are `the release-level` (tokenized as `the`, `release`, `level`), with no negator; the next two are `ledger is`, also with none. The `not` is bound to “infer” (far from `revision`), while `unobservable` describes only observability. Thus P1's fixed three-before/two-after stem window mistakes a correct scope distinction for a polarity flip. This example uses an unlisted absence form (`unobservable`), distant negation (`not`), and a neighbouring-word scope contrast.

## Verdict

Observed false refusal: **1/2**. This is a narrow operability/calibration probe, not a rate estimate: two constructed examples cannot establish prevalence. It demonstrates that correct reasoning about which entity/property a negation scopes over can still be refused when the shared stem is adjacent to non-negating words; a distant `not` does not protect that stem. No tool, fixture, predicate, claim, or scorecard was changed. No network or installs used.
