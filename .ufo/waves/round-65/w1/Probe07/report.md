# Probe07 — isolated no-exit receipt fixture

## Scope and axes
Correct malformed-header classification; preserved reproducibility evidence; isolation/no production changes. One reference-validator invocation only; no battery, build, lint, or production validation.

Read `/home/vgpnk/.omp/agent/RULES.md`, frozen claims, reference validator and C1 counter locally. Lane HEAD observed `f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd`. `tools/receipt-pin.py` was absent at inspection. No production files changed.

## Independent expectation
The frozen format requires exactly ordered REVISION, EXIT, SHA256, empty separator and nonempty output. Removing the EXIT header violates this requirement; expected status **1 (invalid)** and `RECEIPT_PIN=FAIL ` prefix. This conclusion follows from the frozen format, independently of the reference implementation's diagnostic.

The fixture uses the frozen C1 `no-exit` construction: start with otherwise valid receipt material and delete `EXIT=0\n`. Its remaining four lines are REVISION, SHA256, blank separator, and `measured output`. Declared receipt revision is the frozen counter's base `d6ed8155e9b4735639a2cf0a3e479c62f2056195`, distinct from the lane freeze commit. SHA256 was computed from `git -C <lane> cat-file blob <base>:SKILL.md`, not working-tree bytes: `4355e16a5d8d16057496f005df7382ca287863712ed2e3abb25f61c60008ce1a`.

## Actual isolated probe
`TMPDIR=/fast/scratch/hyaku/chousa-r65/Probe07` was explicit. Executed validator argv (also retained as a JSON array):

```text
/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round65/controls/ref-receipt-pin.py --receipt /fast/scratch/hyaku/chousa-r65/Probe07/probe07-noexit-receipt.txt --root /home/vgpnk/Projects/shokunin/chousa-shokunin --revision d6ed8155e9b4735639a2cf0a3e479c62f2056195
```

Observed return code: **1**. Stdout exactly `RECEIPT_PIN=FAIL header/body\n`; stderr empty. Matches the independently derived invalid classification and required failure prefix. The exact `header/body` diagnostic is observed reference behavior, not an independently specified frozen diagnostic.

## Retained evidence
All paths relative to lane root:
- `.ufo/waves/round-65/w1/Probe07/probe07-noexit-receipt.txt` — exact 148-byte input.
- `.ufo/waves/round-65/w1/Probe07/probe07-noexit-run.json` — exact argv, stdout, stderr, status, digest, revision, Python version and derivation.
- `.ufo/waves/round-65/w1/Probe07/probe07-noexit-driver.py` — executed fixture driver retained for reproducibility. Recreate its scratch directory before replay; replay overwrites this seat's evidence.

Scratch deleted after evidence/driver retention. No clone, Git mutation, network fetch, installation, external-state change or source-tree modification. Available Python: 3.14.8; no tools installed or updated.

## Limits and handoff
No blocker for this assignment. This result covers only the missing-EXIT surface against the reference; it does not establish production behavior, other cases, execution authenticity or general parser safety. L1 owns the post-integration gate and any production invocation. No LSP tool was exposed; this isolated fixture involved no supported-symbol refactor.
