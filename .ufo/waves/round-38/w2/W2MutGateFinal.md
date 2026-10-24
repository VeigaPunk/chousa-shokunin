# W2MutGateFinal

## Verdict

M1/M2 are killed (c1 4/7, 6/7); M3 and M4 still SURVIVE c1 7/7 on every byte-set I could pin, including the newest lane bytes — Erratum 6(b) names and concedes the M4 half ("absolute/PATH half … scores 7/7"), but no erratum names M3 (the deleted absolute-path override refusal); Erratum 6's narrow reading instead *claims* that coverage. c2 post-Erratum-4 scores 7/7 on all four mutants: zero cells move.

## Evidence

No lane write was needed. Scratch only: `/tmp/r38-w2-mutgate-final.2943` (mutants from the committed gate),
`/tmp/r38-w2-headtree` (HEAD files via `git show HEAD:…`), `/tmp/r38-w2-finalbytes` + `/tmp/r38-w2-finaltree`
(live worktree snapshot, with a `round37/` sibling so c2's legacy fixture resolves), `/tmp/r38-w2-headtree`.

Byte-sets actually scored (all hashes sha256; the lane was being edited by other wave-2 seats during this seat):

| set | gate | c1-count.py | c2-count.py | verify-receipts.py | expectations.jsonl |
|---|---|---|---|---|---|
| A = HEAD `8e93bc9` | `37e2b9968706adabd095c6ed93d5e3035a014e1961dfe85d44dc80d28ab6d27d` | `790407908444b3e99fbf3fba9e9afdcf654d565a5a4304bd4f23daedc3462221` | `414a7a10571263e781137fcbb0fb4e16bd9dbb9a44fda4931d9fe4d67cc403e3` | `b63e7e200b88022f6747e4b628cb6b251187ad95f5b33d2b6b4b14e08d5cf952` | `d34f17353fec83ed2e7b78b41cebcd2a6d309a85d724dbf1097cf6a17afaf8aa` |
| B = worktree snapshot 01:2x | `0447ad14b6135441f39f9220d02ae2967b810f791a2f1058654ee0c800c3b85a` | `1f37077b15f99039532a6fea5b8f384d87f6974fcc0e0bf19a51220834844cf3` | `6a4449c2e736984a08a6607fc3067332c8e2b17f1dbca387a70db24997d5366a` | `33c7c87e7a5f3eb86cd8db3bccaf88c0d8fbd542db3cd5f05a6568d8f2182fdb` | same `d34f1735…` |
| C = freshest lane bytes | `0447ad14…` | `6a9600ea6b1fe6128faadfb9979c182eb7356d71a76c0ec7d90a1e9666d9946d` | `93bf06daac30db5378ee6efc8ce1eba5d2c6b3cbf107b4c492798ad7c15bfadb` | `33c7c87e…` | same `d34f1735…` |

Mutants are one exact-string edit of the byte-set's gate copy; `diff -u` shows one hunk each.
Set A: M1 `1bda0905f3805b8e36ae0e28e6020410415c768d76181c6954ebff9f2802dfde` (capture `"$ENV_BIN"`→`env`);
M2 `421ff1514bd561dcc232e55d85c7b92db85d48c1f30efd51ea452c9f4426c49b` (`*"GNU coreutils"*)`→`*)`);
M3 `23df3eb85fab12de1caa5b703f62702a41c5f75dd743693bcaefe1cd11e9f3b3` (delete the `/*) ;; *) refuse "not an absolute path"` case);
M4 `65ee757b53879ab8b72c2e63832d19c3dc515f2959f24b701b516b0cba02a98d` (capture `"$ENV_BIN"`→`/usr/bin/env`).
Set B: M1 `b4732232…5dc2ee`, M2 `f6fdb0bd…8965264`, M3 `81d6211d…619326`, M4 `3ed48108…be26b76`.
M1/M3/M4 hashes reproduce wave-1's exactly; M2 differs in edit shape (wave-1 collapsed the `case`; I kept `esac`/`return 1` unreachable) — same defect, different bytes.

Commands (per cell; seed and gate substituted), e.g. set A baseline and M3:
```
$ C1_TMP=$H/tmp python3 $H/round38/c1-count.py --gate $W/pristine.sh --seed 38401 --receipt $H/c1-pristine.json
… ENV_PIN_CAPTURE_MATCH=7/7
$ C1_TMP=$H/tmp python3 $H/round38/c1-count.py --gate $W/m3-no-abs-refusal.sh --seed 38404 --receipt $H/c1-m3.json
… ENV_PIN_CAPTURE_MATCH=7/7
$ C2_TMP=$H/tmp python3 $H/round38/c2-count.py --gate $W/m3-no-abs-refusal.sh --seed 38462 --receipt $H/c2-m3.json
… RECEIPT_BINDING_MATCH=7/7
```
Full matrix (pristine and all four mutants, every byte-set):

```
set A   c1: 7/7 (38401)  4/7 M1 (38402)  6/7 M2 (38461)  7/7 M3 (38404)  7/7 M4 (38405)
        c2: 7/7 (38411)  7/7 M1 (38412)  7/7 M2 (38446)  7/7 M3 (38462)  7/7 M4 (38463)
set B   c1: 7/7 (38421)  4/7 M1 (38422)  6/7 M2 (38423)  7/7 M3 (38424)  7/7 M4 (38425)
        c2: 7/7 (38441)  7/7 M1 (38442)  7/7 M2 (38443)  7/7 M3 (38444)  7/7 M4 (38445)
set C   c1: 7/7 (38451)  4/7 M1 (38454)  6/7 M2 (38455)  7/7 M3 (38452)  7/7 M4 (38453)
        c2: 7/7 (38456)  7/7 M3 (38457)   [M1/M2/M4 not re-run on C; C differs from B only by the stale-unlink move]
```
Set A M1 failing rows (identical shape on B/C, 4/7): `env-fn-echo-scrub` `echo_lines=1, drift_rc=1,
GATE_DRIFT: -GATE_GREP`; `env-fn-root-move` `drift_rc=1, GATE_DRIFT: -FINDING:CHAIN_SOURCE_MISSING
-FINDING:CLAIM_SOURCE_MISSING -FINDING:POINTER_UNRESOLVED …`; `env-fn-suppress` `pin_rc=2, pin_file=False`.
Set A M2 only failing row: `env-override-fake` observed `{'pin_rc': 2, 'pin_file': False, 'refusal': ''}` — rc and
file already match, so the *token* is the whole kill.

Quotes (claims.md on final bytes, line numbers stable across A/B/C):
- Frozen claim, claims.md:27-31: "The canonical pin capture's child runs through ONE pinned absolute `env` (default
  `/usr/bin/env`, verified GNU coreutils; `RESEARCH_GATE_ENV` override, absolute + GNU-reporting, refused exit 2 with
  `ENV_PROVENANCE` before any mode runs)".
- Erratum 6(b), claims.md:220-223: "(b) P1 does not measure the absolute/PATH half — a mutant capture using
  PATH-resolved `command env` scores 7/7 while being PATH-poisonable (demonstrated, seed 38207)".
- Erratum 6 narrowed reading, claims.md:232-234: "C1 asserts function-export interposition on the capture's `env`
  invocation plus the override refusal shape; the env pin's PATH-independence and hostile-drift coverage are
  pre-registered r39 cells (an eighth scenario)".
- limits bullet, claims.md:130: "C1 pins the capture's `env` invocation only."

## Findings

1. **M1 killed, all byte-sets (c1 4/7, rc 1).** Bare `env` reintroduces all three interposition channels the fixture
   encodes. Fixture rows: `corpus/evidence/round38/expectations.jsonl:2-4`; gate capture call
   `tools/research-gate.sh:4001-4003` (byte-set B line numbering).
2. **M2 killed, all byte-sets (c1 6/7, rc 1), by one token.** With any `--version` accepted the fake env is pinned
   and the capture fails opaquely; only `refusal` differs (`''` vs `ENV_PROVENANCE`). Same finding as wave-1
   (`.ufo/waves/round-38/w1/MutGateC1.md` finding 2); nothing in the integration added an rc/file discriminator.
3. **M3 still survives 7/7 — and no erratum names it.** The only override cells are `env-override-missing` and
   `env-override-fake` (`expectations.jsonl:6-7`), both handed **absolute** candidates (`c1-count.py:161-167`
   builds them under the absolute `--tmp`/`C1_TMP` dir). Deleting the `not an absolute path` refusal therefore has
   no observable: 7/7 on A, B and C. Erratum 6's narrow reading claims "plus the override refusal shape", which is
   the sentence that would disposition it — the fixture exercises two refusal instances, not the refusal *class*
   the frozen claim at claims.md:29 names ("absolute + GNU-reporting, refused exit 2"). Errata 1-11 never mention
   M3 (Erratum 11 is about verifier mutants, not override refusals). So the answer to "does Erratum 6 name exactly
   that" is **no**: it claims the coverage instead.
4. **M4 still survives 7/7, and that one IS dispositioned.** Erratum 6(b) names "the absolute/PATH half" as
   unmeasured and concedes a 7/7 mutant; M4 is the absolute-path form of the same gap (the capture ignores a valid
   `RESEARCH_GATE_ENV` selection). No cell supplies a *valid* positive override, so the frozen "ONE pinned absolute
   `env` … override" (claims.md:27-30) is asserted, not measured, on every byte-set including C.
5. **c2 post-Erratum-4: 7/7 on every mutant in all three byte-sets; zero cells move.** The wave-1 5/7 regression is
   gone: `hold-receipt-verifies` and `foreign-gate-distinguished` now *record* `counter_rc` without asserting it
   (set A M1 observed `counter_rc=1` with `receipt=True, verify_rc=0`, and `verify_landed_rc=1`), and the verifier
   accepts a `predicate_holds=false` receipt as self-consistent — by design per Erratum 2, but it means c2's "hold"
   is a hold of receipt integrity, never of C1. `self-rewrite-refused` still asserts `counter_rc=2`, which survives
   every gate mutant because it is produced by the gate file changing under the run, not by the predicate.
6. **The counter self-binding is publication-time, not load-time.** `c1-m2.json` (seed 38403, launched in the batch
   that overlapped the lane edit) records `counter_sha256=a48e5b22…`, which matches neither the bytes its process
   executed (`79040790…`, per the sibling receipts `c1-m1/m3/m4.json` of the same byte-set) nor any later file
   (`1f37077b…`, `6a9600ea…`). Erratum 8(b) closed this race for the expectations table only; `counter_sha256` is
   `sha256_file()` at receipt-write time (c1-count.py, receipt block), so a mid-run counter edit yields a receipt
   that binds bytes that may not have run.
7. **Transient harness collapse observed.** Four concurrent c2 runs: the M3 and M4 cells scored 0/7 with the subject
   c1 returning rc 1 and **no receipt** on every invocation; serial reruns on the same gate/counter bytes gave 7/7
   twice, and later 5-6-way batches were clean. c2 discards the child's stderr, so the cause is not visible in its
   output; the mechanism is unpinned (not a mutant kill — a baseline-adjacent failure, thus inconclusive).

## Limits

- The lane is being edited by other wave-2 seats: gate mtime 01:20:15, c1 01:22:32→later, c2 likewise; a receipt was
  deleted mid-session. Scores are pinned per byte-set (table above), not to one moving tree. A-C agree on every cell.
- M2's mutant bytes differ from wave-1's (`421ff151…` vs `b46304c1…`): same defect, different edit shape.
- One seed per cell (fresh, ≥38401); scenario selection is seed-invariant (frozen table), so seeds buy reproducibility,
  not coverage.
- No selftest was run on mutants: these four cells read the gate black-box, and gate bytes in the lane were never
  edited by this seat (`git status -- tools/` shows only the integrator's `M tools/research-gate.sh`).
- c2's legacy cell needs a `round37/c1-count.py` sibling (`c2-count.py` `R37_C1` is `../round37/…`). My first flat
  /tmp copy scored 6/7 on **pristine** — a relocation baseline failure, discarded; a sibling layout fixed it.
- Disclosure: one command accidentally created `tools/research-gate.sh.pin` in the lane and deleted it in the same
  command (verified absent, `git status` clean for it); no other lane writes. Report file only otherwise.
- No tool installs or upgrades. Scratch survives under `/tmp/r38-w2-*`; nothing was restored because nothing in the
  lane was mutated.
