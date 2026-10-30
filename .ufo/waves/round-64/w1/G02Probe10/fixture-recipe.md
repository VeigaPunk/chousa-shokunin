# G02 percent-encoded-space fixture

Command (run from `/fast/scratch/hyaku/chousa-r64/G02Probe10`):

```sh
python3 /fast/scratch/hyaku/chousa-r64/G02Probe10/probe.py
```

The probe imports the candidate `corpus/evidence/round64/controls/ref-preflight-v3.py`, creates an isolated temporary lane with `corpus/knowledge/space name.md`, and writes `corpus/README.md` containing `[space name](knowledge/space%20name.md)`. It invokes `g02` directly and compares the exact tuple to `('PASS', '1 entries indexed')`, then removes its temporary fixture automatically.
