# Attack07 — C1 URL/code-only index mentions

Axes: operability (G02 inventory/index integrity), calibration (what frozen evidence establishes), provenance (frozen versus post-freeze authority).

## Counterexample and evidence

Minimal fixture: `corpus/knowledge/alpha.md` containing `# Alpha`, with README containing only `https://example.invalid/alpha.md`. Both inspected current `tools/lane-preflight.py` and inherited candidate `corpus/evidence/round64/controls/ref-preflight-v3.py` returned exit 0, `GATE G02 knowledge-index PASS 1 entries indexed`, `PREFLIGHT=1/1 FAILED=none`. README containing only `` `alpha.md` `` also passed both. Percent-encoded external URL `https://example.invalid/%61lpha.md` also passed both. Bare `alpha.md` passed; control `~~alpha.md~~` failed G02, exit 1, for both. All stderr was empty.

This falsifies the broad interpretation that closing strike-row E05 also makes URL-only/code-span-only D3 variants verdict-bearing. It does **not** falsify the literal frozen v3 normalization-and-regex rule: claims.md:53–56 explicitly searches the normalized README, not a parsed index/link structure; slash and backtick satisfy its left boundary. Claims.md:95–97 explicitly discloses these variants are represented only by the strike-row class. Removing all code spans would itself regress legitimate index rows, which frozen fixtures use. This is a disclosed semantic coverage weakness, not permission to change the frozen contract or to announce a fresh C1 refutation. Canonical closure judgment remains L1's responsibility.

Inspected implementation evidence: current tool lines 136–165 applies regex to all normalized README text, removes strikes but not URLs/code spans; inherited candidate lines 132–160 does likewise (and uses a stem, a separate out-of-scope discrepancy). The candidate is not evidence of production landing.

## Frozen failure remains distinct

Frozen `c1-battery-v3.py`:386–394 draws `tag()` twice independently in each E12/E13 fixture. Bounded fixture generation using `random.Random(7)` produced:

- E12 file `escaped_q52e6b438.md`, README `knowledge/escaped\_qf2a74de4.md`.
- E13 file `gate notes q52e6b438.md`, README target `knowledge/gate%20notes%20qf2a74de4.md`.

Neither escaping nor percent decoding repairs the different suffix. These supposedly benign fixtures violate the frozen indexing contract, so conforming rejection fails their expected exit-0 legs. This known frozen counter failure is independent of the URL/code weakness. No full battery PASS is claimed here, and no frozen file was repaired.

The distinct post-freeze `c1-battery-supplement.py`:386–396 reuses one `t` per leg; the same bounded generation produces matching suffix `52e6b438` for both file and README. This demonstrates the inherited repair but cannot replace the frozen kill-rule requirement (`claims.md`:89–93). The supplement retains strike-only E05 and therefore does not independently test these URL/code variants.

## Provenance

Read-only `git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:<path>` comparisons: frozen claims and battery match current bytes exactly; battery SHA-256 `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2`. Current tool differs from freeze (`3d792f0961434ccd76ef87ccb0b2dcccc022f6f84d958dbc4e35e6f4c260a89d` versus `7e9427785db117e2996fe23134ab5c9357ea793d25efabb5cb5159e4ca79d460`). Candidate and supplement were absent at freeze (`git show` exit 128). No claim is made about their later commit status. Exact hashes and commands are in `evidence.json`.

## Smallest safe correction

Keep frozen claims/counter unchanged and report their E12/E13 failure honestly; label supplement measurements separately. Route explicit URL-only/code-only probes to a newly named future instrument. If a future rule must distinguish a genuine index from incidental mentions, define the accepted index structure first; do not globally strip backticks or silently tighten this frozen regex. No production correction is authorized by this review.

## Reproduction and scope

Command (exit 0):

```sh
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack07/probe.py
```

`probe.py` records every child command, stdout, stderr and exit in `evidence.json`; ten G02-only executions bounded at 15 seconds each, plus four fixture generations. No full battery, other gates, judge, integration, network, git mutation or installation was run. Python 3.14.8, existing system channel; no tools installed/updated. Scratch `/fast/scratch/hyaku/chousa-r64/Attack07/` removed in `finally`; no clone created. Only own output paths written.

Self-evaluation: accuracy 4/5 (current-byte evidence, not landing verification); completeness 4/5 (scoped probes, intentionally not full battery); clarity 5/5 (contract versus broader intent separated); actionability 5/5 (minimal future-instrument correction); conciseness 4/5 (provenance adds length). Mean 4.4/5. Improvement: L1 should retain explicit frozen/supplement labels in closure. Would the user agree? Expected yes: no narrowed PASS, no frozen repair, exact counterexample receipts.
