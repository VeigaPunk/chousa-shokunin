# R92ExecMutations — run ledger (exact commands, observed exits)

`S=/fast/scratch/hyaku/chousa-r92/R92ExecMutations`
Clone: `git clone --shared /home/vgpnk/Projects/shokunin/chousa-shokunin $S/repo`;
`git -C $S/repo checkout 16ccf7693c61b8ffe392fc757352304f239bfcad`.
Every command below ran with cwd `$S/repo`. Exit codes are the observed shell `$?` of the run that
produced the adjacent `.out` receipt.

## Pristine baselines

| receipt | command | exit |
|---|---|---|
| base/verify.out | `python3 -B corpus/evidence/round92/control-driver-r92.py verify --root . --repo . --rev 42e0337822a508208800f98faa3a63c6af9f8c27 --receipts-rev 16ccf7693c61b8ffe392fc757352304f239bfcad --work $S/work/base/verify-work` | 0 |
| base/forgeries.out | `python3 -B corpus/evidence/round92/forgeries-r92.py --work $S/work/base/forgeries` | 0 |
| base/curation.out | `python3 -B corpus/evidence/round92/curation-r92.py --root $S/repo` | 0 |
| base/c2ctl.out | `python3 -B corpus/evidence/round92/curation-controls-r92.py --root $S/repo --work $S/work/base/c2ctl-work` | 0 |
| base/tally.out | `python3 -B corpus/evidence/round92/skill-tally-r92.py --root $S/repo --selftest corpus/evidence/round92/controls/selftest-r92.txt` | 0 |
| base/c3ctl.out | `python3 -B corpus/evidence/round92/skill-tally-r92-controls.py --root $S/repo --work $S/work/base/c3ctl-work` | 0 |
| base/forg-missing.out | claim-literal C1: `python3 -B corpus/evidence/round92/control-forgeries-r92.py --work $S/work/base/forg-missing-work` | 2 |
| base/c2ctl-claim.out | claim-literal C2: `python3 -B corpus/evidence/round92/curation-r92-controls.py --root . --work $S/work/base/c2ctl-claim-work` | 2 |

## Mutant runs

Deploy = `cp $S/mut/<id>/<instrument> $S/repo/corpus/evidence/round92/<instrument>`;
restore = `git -C $S/repo checkout -- corpus/evidence/round92/<instrument>`.

| id | instrument | detector command | mutant exit | restored exit |
|---|---|---|---|---|
| M1 | control-driver-r92.py | `python3 -B corpus/evidence/round92/forgeries-r92.py --work $S/work/M1/forg` | 1 | 0 |
| M2 | control-driver-r92.py | same, `--work $S/work/M2/forg` | 1 | 0 |
| M3 | control-driver-r92.py | same, `--work $S/work/M3/forg` | 1 | 0 |
| M4 | curation-r92.py | clean: `python3 -B corpus/evidence/round92/curation-r92.py --root $S/repo`; controls: `python3 -B corpus/evidence/round92/curation-controls-r92.py --root $S/repo --work $S/work/M4/ctl` | 0 / 1 | 0 / 0 |
| M5 | curation-r92.py | same pair, `--work $S/work/M5/ctl` | 0 / 1 | 0 / 0 |
| M6 | curation-r92.py | same pair, `--work $S/work/M6/ctl` | 0 / 1 | 0 / 0 |
| M8 | curation-r92.py | same pair, `--work $S/work/M8/ctl` | 0 / 1 | 0 / 0 |
| M9 | skill-tally-r92.py | selftest: `python3 -B corpus/evidence/round92/skill-tally-r92.py --root $S/repo --selftest corpus/evidence/round92/controls/selftest-r92.txt`; controls: `python3 -B corpus/evidence/round92/skill-tally-r92-controls.py --root $S/repo --work $S/work/M9/c3ctl` | 1 / 1 | 0 / 0 |
| M10 | skill-tally-r92.py | same pair, `--work $S/work/M10/c3ctl` | 0 / 1 | 0 / 0 |
| M11 | skill-tally-r92.py | same pair, `--work $S/work/M11/c3ctl` | 0 / 0 | 0 / 0 |

Restored-bytes equality: each restore was followed by `sha256sum` of the instrument; all ten restores
printed the pin hash (driver `1cc948b0…`, curation `81310bba…`, tally `ac5bf547…`). See `hashes.txt`,
`pristine-hashes.txt`, `repo-state.txt` (`HEAD=16ccf769…`, empty `git status --porcelain`,
`ASSERT_OK=1` for `git -C $S/repo rev-parse --show-toplevel` = `$S/repo`).
