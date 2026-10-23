# Block versus inline mutation probe

**Hypothesis verdict: FALSIFIED.** Adding `span`, `a`, `em` and `code` to the block set changes 6 frozen verdicts from `VERBATIM` to `ABSENT`. Keeping only `p` and `br` changes none.

Axes: **operability** is the assigned target; **coverage** and **calibration** are diagnostic constraints. This report does not grade the production command or C1.

## Method and actual outputs

Read `corpus/evidence/round29/claims.md` first. Its v2 contract specifies an **exact**, not minimum, block list. Implemented its extractor, normalization, boundary match and verdict precedence independently in scratch; only `extractor.py` line 6 changed between runs. Frozen labels were used only by the detector for comparison, never to generate a verdict.

Working directory for every command below: `/fast/scratch/hyaku/chousa-r29/w1/MutateBlockInline/`.

| Command | Exit | Key output |
|---|---:|---|
| `timeout 90s python3 -B probe.py fetch` | 0 | `FETCH_TOTAL 8 OK 8` |
| `timeout 30s python3 -B probe.py detect baseline` | 0 | `FIXTURE_MATCH=40/40` |
| `timeout 30s python3 -B probe.py detect extra-inline` | 1 | `FIXTURE_MATCH=34/40` |
| `timeout 30s python3 -B probe.py detect restored-after-extra-inline` | 0 | `FIXTURE_MATCH=40/40` |
| `timeout 30s python3 -B probe.py detect only-p-br` | 0 | `FIXTURE_MATCH=40/40` |
| `timeout 30s python3 -B probe.py detect restored` | 0 | `FIXTURE_MATCH=40/40` |
| `timeout 20s python3 -B summarize.py` | 0 | `RESTORED_EXACTLY True`; `FROZEN_INPUTS_UNCHANGED True`; `VERDICT FALSIFIED` |

Expected detector: agreement with every one of the 40 frozen labels; exit 1 detects a mismatch. The pristine baseline passed. **Extra-inline mutant: killed. Only-p-br mutant: survived.** The latter is a coverage finding, not authorization to change the frozen contract.

Fetched each of S002, S003, S008, S013, S019, S020, S038 and S044 once with concurrent GET requests; all returned HTTP 200 HTML at the exact registry URL, without redirects. All detector runs reused those byte-identical snapshots, with no further network requests. Fetch elapsed time was 1.009102 s; all five detector runs together took 0.649596 s inside the detector.

Setup disclosure: an earlier invocation of the same fetch command exited 1 with `RuntimeError: can't start new thread` before the first HTTP worker could start. Its snapshot directory was empty. The initial per-user process limit of 24 was below the host's observed 1143 user threads (`timeout 10s bash -c 'ps -u vgpnk -L --no-headers | wc -l'`, exit 0). Changed that limit to 4096; the actual fetch pool remained capped at 8 workers, memory at 512 MiB and CPU time at 60 s. No tools were installed or updated. All commands finished; no background jobs or services were started.

## Changed items and why

Each quotation below was located in the captured page opened on **2026-10-23**, and is at most 25 words. All six change only under extra-inline; all retain `VERBATIM` under only-p-br. Captured HTML line locations and actual normalized renderings are in `MutateBlockInline/witnesses.json`.

| Item | Located quotation and registry URL | Load-bearing markup and changed text |
|---|---|---|
| `27c5599c` | “Like the JSON standard a byte order mark (U+FEFF) must NOT be included.” — [S013](https://jsonlines.org/), lines 59–60 | `included</a>.` becomes `included .` |
| `db86a0d4` | “Return the longest common sub-path of each pathname in the iterable paths.” — [S044](https://docs.python.org/3/library/os.path.html), lines 291–292 | `<em>paths</em>.` becomes `paths .` |
| `2cbd5af5` | “The OWL encoding of the PROV Ontology is available here.” — [S020](https://www.w3.org/TR/2013/REC-prov-o-20130430/), line 1295 | `<a …>here</a>.` becomes `here .` |
| `cee49a8b` | “The namespace for all PROV-O terms is http://www.w3.org/ns/prov#.” — [S020](https://www.w3.org/TR/2013/REC-prov-o-20130430/), line 1292 | Closing `span` inserts a space between the URL's `#` and final `.` |
| `ca473d99` | “JSON Lines files may be saved with the file extension .jsonl.” — [S013](https://jsonlines.org/), line 92 | `<code>.jsonl</code>.` becomes `.jsonl .` |
| `3406c3dc` | “On Unix and Windows, return the argument with an initial component of ~ or ~user replaced by that user's home directory.” — [S044](https://docs.python.org/3/library/os.path.html), lines 382–383 | `<em>user</em>’s` becomes `user 's` after normalization |

The added spaces survive whitespace normalization, so these exact quotes no longer occur. Four items labeled `verbatim-inline-markup` remain stable: `bcc95dda`, `676c5e8c`, `076df58d`, `3b00b111`. Conversely, `3406c3dc` is sensitive despite being labeled `verbatim-typographic-apostrophe`. The full sweep is the executed `summarize.py` command above; its `matrix.tsv` records every frozen item, expected label, baseline, both mutants and both restorations.

## Restoration and evidence

SHA-256 of the scratch extractor:

- Pristine, restored after extra-inline, and final restored: `1061af7c7aeee8184e765ec8aaf25f247634d6c20d2051de95b6ba6e62ffd643`.
- Extra-inline mutant: `668adade09c8d5713443dcee7f99509209437d79053cf8cddc29cf388b129558`.
- Only-p-br mutant: `e485f7771034783ee73bf128b00b67f1b6bf0304f77c55accaaf52e0af1c4734`.

Both restorations recovered the exact original bytes, all 40 verdicts and every normalized page-text digest. Claims, counter, fixture items and fixture labels retained their initial digests throughout. No production files, sibling files, repository state or indexes were modified.

Evidence directory: `.ufo/waves/round-29/build/MutateBlockInline/`. `fetch.json` records URL, status, timing and snapshot digests; each named detector run has its own JSON receipt; `matrix.tsv` contains all 40 results; `witnesses.json` contains captured markup and three normalized renderings; `summary.json` records changes, observed exit codes and restoration comparisons. Scratch source and page snapshots remain under the working directory above.

Limits: this is the assigned 40-item probe, not the frozen 130-item counter. No page-sampled or fixture-derived run-time items were measured. Surviving the reduced block set says nothing about those additional items or all possible HTML. The exact frozen contract remains unchanged.
