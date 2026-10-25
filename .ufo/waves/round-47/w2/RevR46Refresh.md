ATTACKS: r46-c2-controls-refresh.txt (round-46 closure routed defect 3) — re-run the ten forges against committed round46/c2-count.py on the /tmp tree as the header states; confirm every printed line, the header counts and digest.
VERDICT: holds

## Setup
- Tree /tmp/chousa-r47w2-L1Chousa47/tree = `git archive 6e2630a6` + `corpus/evidence/round46/{c1,c2,c3}-count.py` at `5c6e2ca` (no claims.md). Overlaid counter sha256 `f93cb10795ef7402848ea355680a6b0bd25ad68c8913c24944ef92029c81046f` — equals the committed byte at `5c6e2ca`, `1e9756f` and tip `1fc5ed1` (git show | sha256sum). Base SKILL.md sha256 `7b49e2aeefa14bf081df3a040e7dbf1ec8d618aeadf07fe6c03d941645d05433` (full digest matches the header's `7b49e2ae…d05433`).

## Baseline (matches header line 6-7 verbatim)
`python3 corpus/evidence/round46/c2-count.py --root /tmp/chousa-r47w2-L1Chousa47/tree --list` →
`ENTRY_POINTS=79 (tools=7 counters=50 named=74) GATES_ROWS=30 REGISTERED=58/79 UNREGISTERED=21 C2=FAIL`, exit 1. UNREGISTERED_PATH list = exactly the 21 lines the forgery targets.

## Ten forges: `--skill <SKILL-X.md> --root <tree>` (forged rows built from the 21 baseline UNREGISTERED_PATHs; generated under /tmp/chousa-r47w2-L1Chousa47/forges2/)
| forge | claimed | reproduced | match |
|---|---|---|---|
| prose | 79/30/58/21 FAIL exit1 | identical | yes |
| 6cell (7-pipe row) | 79/30/58/21 FAIL exit1 | identical | yes |
| noexit (8-cell row, no `exit` word) | 79/31/58/21 FAIL exit1 | identical | yes |
| after (valid row after next `## `) | 79/30/58/21 FAIL exit1 | identical | yes |
| fenced (valid row in fence) | 79/30/58/21 FAIL exit1 | identical | yes |
| suffix (`…pyc`/`…shc` names) | 79/31/58/21 FAIL exit1 | identical | yes |
| abut (`<!--x-->` abutting) | 79/30/58/21 FAIL exit1 | identical | yes |
| multicomment (`<!-- / row / -->`) | 79/30/58/21 FAIL exit1 | identical | yes |
| dotslash (`./`-prefixed) | 79/31/79/0 PASS exit0 | identical | yes |
| 7pipe (8-cell row) | 79/31/79/0 PASS exit0 | identical | yes |

Ten forges: eight refusals, two passing blocks — confirmed. Every printed line matches the header verbatim, including `exit=` codes.

## Digest and prior-file numbers (header line 1 and 28)
- Committed counter digest `f93cb107…` = sha256 of round46/c2-count.py at `5c6e2ca`/`1e9756f`/tip (verified above).
- Previous file's numbers `71/55/16`, header `f2fcb654`: pre-widening counter at `c294484f` (sha256 `f2fcb654fb207898…`, verified) re-run on this same tree reproduces exactly `ENTRY_POINTS=71 (tools=7 counters=50 named=66) GATES_ROWS=30 REGISTERED=55/71 UNREGISTERED=16 C2=FAIL` exit 1.

## Findings
1. (Info) `SKILL-7pipe.md` name vs description: the header calls it "seven pipes" but the description and the passing shape are an **8-cell / 9-pipe** row (`names()` scans the whole row; the cell role is unread — matches the "SURVIVOR" note). Reproduction with 9 pipes passes; a true 7-pipe row would be refused (GATES_ROWS unchanged). Name-caption mismatch only; the claimed passing behavior is reproducible at the described shape.
2. (Info) Header line 29-30: "Forge inputs are not committed: commit the generator beside this receipt, or state that the forges are reproducible in shape only." The file states reproducibility in shape only (prose, not a committed generator). No working-tree lane files modified; scratch will be removed.

## Checks run
- `git show {c294484f,1e9756f,5c6e2ca,1fc5ed1}:corpus/evidence/round46/c2-count.py | sha256sum` → f2fcb654… / f93cb107… ×3.
- Baseline + 10 forges run with the committed counter (exit codes captured).
- Pre-widening counter at c294484f re-run (LANE patched in a /tmp copy; no lane file touched).
- awk count of base Gates pipe-rows = 35; `## Gates` at line 75, next `## ` at line 503 (matches "after line 503" placement target).
