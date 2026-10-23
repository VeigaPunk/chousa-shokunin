# Receipt-to-committed-gate census

Read-only census executed 2026-10-23. Python eval invoked the bounded commands below; it hashed each successful `git show` byte stream with SHA-256 and compared the three named receipt fields.

- `timeout 90 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin log --all --format=%H -- tools/research-gate.sh`
- For each revision returned: `timeout 90 git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show <revision>:tools/research-gate.sh`
- Receipts parsed: `.ufo/waves/round-33/measure/final/fz-90212.json`, `fz-90213.json`, `fz-90214.json`.

Observed output:

```text
GATE_BLOBS: revisions=86 unique_sha256=40
fz-90212.json gate_sha256=b2c07edae3a4e2beed90ad51ee06f27515c6aec82ee26651feca5118d6579b4b UNMATCHED
fz-90213.json gate_sha256=b2c07edae3a4e2beed90ad51ee06f27515c6aec82ee26651feca5118d6579b4b UNMATCHED
fz-90214.json gate_sha256=b2c07edae3a4e2beed90ad51ee06f27515c6aec82ee26651feca5118d6579b4b UNMATCHED
```

The census covered the gate revisions reachable from refs via `git log --all`, not unreachable Git objects. It did not run any C1 counter or candidate gate.
