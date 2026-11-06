# R81ExecTrial — command log for every receipt in this folder

Trial tree: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 7e2da96a0541946e796384d42fea18e09ede9e9f | tar -x -C /fast/scratch/hyaku/chousa-r81/R81ExecTrial/tree`
All commands below run from that tree root (`$T`) unless a cd is shown. Receipts were written with `2>&1 | tee <receipt>`; the `rc=` line appended after each command is the command's exit status as shown in the receipt.

| receipt | command (cwd = tree root unless shown) | rc |
|---|---|---|
| `00-artifact-pins.txt` | `sha256sum record.md claims.jsonl items.tsv` in this folder | 0 |
| `01-item1-verify-claims.txt` | `bash tools/research-gate.sh verify-claims corpus/evidence/round81/trial/claims.jsonl --root .` | 0 |
| `02-item1-mut-capture-changed.txt` | `bash tools/research-gate.sh verify-claims /fast/scratch/hyaku/chousa-r81/R81ExecTrial/mut1/claims.jsonl --root /fast/scratch/hyaku/chousa-r81/R81ExecTrial/mut1` (mut1 = copy of both captures with byte 100 of the S203 `.txt` changed to `X`) | 1 |
| `03-item1-root-and-pin-probes.txt` | `bash tools/research-gate.sh verify-claims corpus/evidence/round81/trial/claims.jsonl --root ..`; `(cd corpus/evidence/round81/trial && bash "$T/tools/research-gate.sh" verify-claims claims.jsonl --root ..)`; `bash tools/research-gate.sh verify-claims corpus/evidence/round81/trial/claims-nopin.jsonl --root .` | 0 / 0 / 0 |
| `04-item2-verify-run.txt` | `f=corpus/evidence/round81/trial/record.md; ! bash tools/research-gate.sh verify "$f" --root . \| grep -q '^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps "$f" --root .` | 0 |
| `05-06-item2-twins.txt` | same item-2 line on `mut2-no-sweep.md` (first block, rc=1); then on `atk2-dangling-sweep.md` (second block, rc=0); then `bash tools/research-gate.sh verify mut2-no-sweep.md --root .` appended (rc=1) | 1 / 0 / 1 |
| `06b-verify-all-atk2.txt` | `bash tools/research-gate.sh verify-all corpus/evidence/round81/trial/atk2-dangling-sweep.md --root .` | 0 |
| `06c-item2-sw1-variant.txt` | item-2 Run line on `atk2b-dangling-sw1.md` (rc=0), then `verify-all` on the same file (rc=1) | 0 / 1 |
| `07-item4-verify-sweeps.txt` | `bash tools/research-gate.sh verify-sweeps corpus/evidence/round81/trial/record.md --root .` | 0 |
| `08-09-item4-twins.txt` | `verify-sweeps mut4-no-flip.md` (rc=1) then `verify-sweeps atk4-dash-flip.md` (rc=0) | 1 / 0 |
| `09b-verify-all-item4-twins.txt` | `verify-all atk4-dash-flip.md` (rc=0) and `verify-all atk4b-flip-none.md` (rc=0) | 0 / 0 |
| `10-item5-quote-reopen.txt` | `TMPDIR=$S python3 tools/quote-reopen.py verify --items corpus/evidence/round81/trial/items.tsv` (one live GET of the S205 NLM page) | 0 |
| `11-item6-grep-pin.txt` | `CHOUSA_GREP_PIN_ECHO=1 bash tools/research-gate.sh --selftest 2>&1 \| grep -m1 '^GATE_GREP: '` | pipeline rc 0; gate rc 141 (SIGPIPE from `grep -m1`) |
| `12-verify-all.txt` | `bash tools/research-gate.sh verify-all corpus/evidence/round81/trial/record.md --root .` | 0 |
| `13-checklist-run.txt` | `TMPDIR=$S python3 -B corpus/evidence/round81/checklist-run.py --root .` | 0 |
| `14-depth-r81.txt` | `TMPDIR=$S python3 -B corpus/evidence/round81/depth-r81.py --root .` | 0 |

Missing receipt number `03` in the original numbering was filled by the probe receipt above; there is no gap that was deleted.

Twins copied into this folder: `mut2-no-sweep.md`, `atk2-dangling-sweep.md`, `atk2b-dangling-sw1.md`, `mut4-no-flip.md`, `atk4-dash-flip.md`, `atk4b-flip-none.md`; plus `record.md`, `claims.jsonl`, `claims-nopin.jsonl`, `items.tsv`. `claims-nopin.jsonl` is the same two spans with no `sha256` field.
