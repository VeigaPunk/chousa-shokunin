# G02 strike-only mention probe

## Finding

The candidate `corpus/evidence/round64/controls/ref-preflight-v3.py` rejects a knowledge filename mentioned only inside a Markdown strike span. On the isolated fixture, G02 returned `FAIL 1 not named in corpus/README.md: alpha.md` and the process exited 1. This matches frozen R64-C1 G02 contract clause (ii): strike spans are removed before index matching, so `~~alpha.md~~` must not count as indexed. The fixture also included a live `beta.md` mention, ensuring the remaining README content was indexed normally. Candidate was copied for execution and not edited.

## Exact command and observed output

From `/fast/scratch/hyaku/chousa-r64/G02Probe04`:

```sh
python3 -B ref-preflight-v3.py --root root --only G02 --work work
```

```text
GATE G01 census SKIP
GATE G02 knowledge-index FAIL 1 not named in corpus/README.md: alpha.md
GATE G03 lesson-gate SKIP
GATE G04 shonen-pointers SKIP
GATE G05 scorecard-paths SKIP
GATE G06 freeze-selftest SKIP
GATE G07 assimilate-selftest SKIP
GATE G08 gate-selftest SKIP
PREFLIGHT=0/1 FAILED=G02 ENV=none SKIPPED=G01,G03,G04,G05,G06,G07,G08
EXIT=1
```

## Fixture recipe

Create `root/corpus/knowledge/alpha.md` and `root/corpus/knowledge/beta.md` as regular files. Create `root/corpus/README.md` with exactly `~~alpha.md~~` on the first line and `beta.md` on the second. Copy candidate to `ref-preflight-v3.py`, then execute the command above. The fixture requires no repository mutation.

No tools installed or updated. Scratch fixture and copied candidate were retained at `/fast/scratch/hyaku/chousa-r64/G02Probe04/` pending seat cleanup.