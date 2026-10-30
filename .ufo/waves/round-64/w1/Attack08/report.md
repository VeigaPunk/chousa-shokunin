# Attack08 — C1 filename suffix exactness

Axes: filename-suffix contract fidelity; frozen/supplement provenance; bounded reproducibility.

## Findings, by severity

### High — inherited candidate indexes the stem, not the complete filename

`corpus/evidence/round64/claims.md:53–57` requires matching NAME **with its `.md` suffix**, including the stated right boundary. `corpus/evidence/round64/controls/ref-preflight-v3.py:132–135` instead normalizes `p.stem` and interpolates it into the index regex. The actual filesystem suffix check at lines 119–124 is correct; the defect is the separate README-name lookup. The mirror check at line 136 does not rescue mentions with no `.md` token.

Minimal fixture: only `corpus/knowledge/probe.md`, with README containing only `probe\n`. Expected G02 FAIL under the frozen regex; observed `GATE G02 knowledge-index PASS 1 entries indexed`, exit 0. Two further witnesses, README `knowledge/probe.txt` and `knowledge/probe.mdx`, likewise PASS exit 0 despite not matching the frozen complete-name regex. The `.mdx` witness specifically exercises the frozen right-hand boundary after `.md`.

Positive controls `knowledge/probe.md` and `knowledge/probe.md.` both PASS exit 0 and match the frozen regex; the latter is expressly allowed by claims.md:97–99. Thus this is not a request to forbid sentence punctuation or require a path prefix.

Recommendation to L1: do not integrate this candidate as a complete G02-v3 implementation; preserve this counterexample for a distinct supplemental/next instrument. This is independently reproduced evidence of the limitation already disclosed in `claims-erratum.md:6`, not a new production regression: the candidate is not production.

### High — frozen E12/E13 fail their advertised benign expectation; a supplement cannot admit frozen C1

Frozen `c1-battery-v3.py:386–394` independently draws `tag()` for the created entry and README reference; lines 442–443 nevertheless require exit 0. Directly applying the unchanged frozen closures with `random.Random(64)` produced:

| Leg | Actual file | README target after normalization | Candidate G02/exit |
|---|---|---|---|
| E12 | `escaped_q79e58218.md` | `escaped_q1ff63c01.md` | FAIL / 1 |
| E13 | `gate notes qa1560927.md` | `gate notes q9cecdeee.md` | FAIL / 1 |

E12 output names the phantom row; E13 output names the unindexed existing entry. Rejecting these mismatched names is correct under the frozen contract. Their classification as benign is the frozen instrument defect. This bounded extraction is not a full battery run and does not claim a full summary; it directly exhibits two frozen expected-exit contradictions. No frozen bytes were repaired.

`c1-battery-supplement.py:386–396` shares one tag per fixture. Its E12/E13 closures on the same minimal fixture each yielded G02 PASS, exit 0. This verifies only the fixture-name repair. It neither proves suffix exactness nor satisfies the immutable C1 kill rule (`claims.md:89–93`), which requires three full passes of the **unmodified frozen battery**. Plain attack findings remain advisory, not admission or outside non-author closure.

## Evidence and reproducibility

Seat-local driver: `.ufo/waves/round-64/w1/Attack08/probe.py`.
Raw command arrays, stdout, stderr and exit codes for all nine subprocesses: `.ufo/waves/round-64/w1/Attack08/evidence.json`.

Executed command (exit 0):

```text
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Attack08/probe.py
```

Each probe invokes `/usr/bin/python3 -B <absolute candidate> --root <seat scratch fixture> --only G02 --work <seat scratch work>` with a 20-second bound. No full battery, other gates, network fetch, clone, git/jj mutation, production edit or frozen-file edit was performed. Scratch `/fast/scratch/hyaku/chousa-r64/Attack08` was removed in the driver's `finally` block (`scratch_removed: true`). No live clone was created.

Read-only provenance commands (both exit 0):

```text
git show bf40d99bda9eefdad3ed6276da077cfb24ba82f1:corpus/evidence/round64/c1-battery-v3.py | sha256sum
sha256sum corpus/evidence/round64/c1-battery-v3.py corpus/evidence/round64/c1-battery-supplement.py corpus/evidence/round64/controls/ref-preflight-v3.py
```

Frozen commit and working frozen battery both hash `4b3f0b658bcd3bb640cd2e6e56a28a91a72d5352f2610887db01e636fc039fe2`, matching claims.md's frozen prefix. Supplement: `a7057ae33ac958f060a25ea325537bec7bed728e7ea2dad3f3a961e715fc33f1`. Candidate: `0b4da0d2128e23b4feeb82bb179ec6a89277a1f0a0aa1c7115e3ae38966f185e`.

Tools: existing `/usr/bin/python3` 3.14.8 (GCC 16.2.1), system installation, used for bounded fixture generation and candidate CLI execution. No installation/update or pacman transaction. Git and sha256sum were used read-only for frozen-byte identity; versions were not measured.

## Residual risk and verification gaps

LSP unavailable: reading `xd://lsp` returned `No such tool`; no server/status/references/definition/diagnostics device is mounted. Source reads and literal searches were the fallback, not semantic proof. CLI observations provide the behavioral evidence.

No full frozen/supplement battery receipt or production behavior is claimed here. E12/E13 were applied directly to minimal fixtures, not the golden-copy harness; this isolates the fixture mismatch without manufacturing a frozen full-run summary. Suffix witnesses cover one ASCII filename, three invalid mentions and two valid controls, not all Unicode, mirror, traversal or symlink behavior. Supplement repair does not itself close those gaps. Canonical runtime/resume paths are not changed or exercised by this scoped C1 attack.

## Self-evaluation

Accuracy 4/5: source locations, byte identities and nine captured CLI outcomes support findings; no complete-battery result measured. Completeness 4/5: scoped suffix falsification and frozen/supplement distinction covered; exhaustive name-space coverage is not claimed. Clarity 4/5: fixture table separates instrument defects from candidate defects; raw CLI records are necessarily separate. Actionability 4/5: L1 has a minimal regression witness, but only L1 may integrate a fix. Conciseness 4/5: detailed provenance adds length required for reproducibility. Overall 4.0/5. Highest-impact improvement for authorized canonical follow-up: retain the three suffix witnesses as distinct negative tests without modifying the frozen battery. Would the user agree: likely; all conclusions remain bounded and advisory.
