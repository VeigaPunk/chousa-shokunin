# R59Critic61 — calibration review (positive verdict-path / offline recon)

Scope: attack committed round-59 bytes at HEAD 026174e. No edits, no network, no installs, no pacman. Scratch `/fast/scratch/hyaku/chousa-r59/R59Critic61/` was used for three `capture-text.py` renders and then removed.

## 0. Frozen claims target does not exist (unchanged from the first pass)

`corpus/evidence/round59/claims.md` is absent on disk and untracked in git. `git ls-files corpus/evidence/round59` lists 12 files, none of them claims.md. `corpus/lessons/round-59.md` itself says "claims: none validly frozen". So there is no round-59 claim, counter or control to falsify. The only round-59 control file is `controls/c1-before.txt`. It is a round-58 C1 run (`C1=FAIL`, `REFUSE=0/7`), not a round-59 claim. Do not retarget round-58 claims. Correction: the 12-file listing above is the full tracked set.

## 1. Counterexamples against the committed quarantine recheck (new, runnable)

The proposed claim is in `LOG.md` and `lessons/round-59.md`: offline verdicts are 14 `absent` and 10 `unverifiable`, no source is called fabricated, and the binary-office rows stay unverifiable.

### 1a. Binary-office "unverifiable" was avoidable, and the quotes are present

`tools/quarantine-check.py:303-307` returns `unverifiable` for every `page+binary-office` row ("never rendered to text"). The same lane already renders these captures offline. The S101 reopening in this round ran `python3 -B tools/capture-text.py corpus/captures/6dc68fd6b32ce9c8dfcebce8.raw` with rc 0. I ran the same tool on the other three binary captures, `.raw` input, rc 0 each:

| Capture | Rendered chars | Quarantined row |
|---|---|---|
| `b539a802…` | 2,290 | S095 |
| `3a8b4597…` | 48,936 | S120 |
| `bdff491a…` | 34,234 | S125 |

I then took the register quotes (`absent-defect-register.md`, sha256 `5afe1810…`, matching `quarantine-digests.txt`). I split each quote on `…`/`...`, stripped whitespace, and kept segments of 8+ characters. This is a plain substring test against the whitespace-stripped rendering.

| Row | Segments found |
|---|---|
| S120 | 3/3 present, including `SRにおける文献検索期間について明記する。` |
| S125 | 2/3 present (`文献检索策略：检索途径…`, `检索策略包括检索的数据库…`); 1 absent |
| S095 | 1/3 present (`关于自引的说明：…`); 2 absent |
| S096 | 2 of 5 substantive segments present. The S096 capture is `6dc68fd6…`, rendered into `s101-open.txt`; matched against that file, `根据GB3469规定，以单字母方式标识以下各种参考文献类型` and `主要责任者` are present. |

Consequences:
- The register's "quote is in none of them" is false at segment level for these four rows.
- The lane's `unverifiable` is the safer label, but it is a refusal to look rather than a measurement. The lesson's "required hand-check remains partial where … binary captures" understates what was reachable offline. The lane did the reachable step for S101 and skipped it for S095, S096, S120 and S125.
- Segment presence is not full-quote presence. The elided quotes are ordered with gaps, so I do not claim "present" for any whole quote. I claim only that the `absent` family does not hold for these rows, and that a rendered-text recheck would change the verdict from `unverifiable` to `present` or `partial` for at least S120.

### 1b. Register IDs are not current SOURCES.md IDs (namespace collision)

- Register S077 is `doi.org/10.1186/s13643-020-01542-z` (PRISMA). `corpus/SOURCES.md` S077 is the Poppler pdftotext manual.
- Register S095 (chousa round2) is the zcmu `.doc`. SOURCES.md S095 is the round-47 verifier spot-check, and the zcmu doc is SOURCES S100.
- Register S096 is the HIT `.doc`. SOURCES.md S101 is that same HIT `.doc` URL.
- Register S101 in two other lanes is `gdUnit4` (`game-dev-2d`, `:68`). The slice picks only the `chousa` row.

The register IDs are historical per-round labels, and `quarantine-slice-rederived.tsv` mixes them with current-looking `S###` names. This round's lesson reopens "S101" (SOURCES) and separately lists "S101 unverifiable" (register round3 unchecked). The same label names two different things. The S096→S101 coincidence also shows one HIT document was opened offline as "S101" while its quarantine row (register S096) was left unverifiable. A reader cannot tell this from the receipts. The correction is to key quarantine receipts by URL or capture id, not bare `S###`.

### 1c. Two contradictory verdict receipt sets are committed

- `quarantine-verdict.txt`: 24 `unverifiable`, reason "no local capture… missing capture", cache column `cache`.
- `quarantine-verdict-lane.txt`: 14 `absent` and 10 `unverifiable`.
- `quarantine-examine.txt`: 43 rows `no-capture`.
- `quarantine-examine-lane.txt`: 26 `absent` and 17 `no-capture`.

The un-suffixed files are evidently the default-cache run, where the cache directory was missing. The lesson cites only the `-lane` files and never says the un-suffixed ones are an invalid run. Nothing in the files says so. A committed receipt that says "never read locally" for 22 rows that were read locally is a trap for any later reader or counter.

### 1d. Digest claim not met

The lesson says the cache and register digests are preserved in `quarantine-digests.txt`. That file holds one line (`register … 5afe1810…`). There is no cache digest, although the verdict depends on the capture store (129 files in `corpus/captures/`). The `absent` claim cannot be reproduced against a pinned cache.

### 1e. Positive-path calibration

The 14 `absent` verdicts come from text-form captures only. The checker never emitted `present` for any row in this slice, so the positive verdict path of `quarantine-check.py` was not exercised on committed bytes. QUALITY 115 exists for counters, but the same gap applies to the tool that produced the 14. A control row with a known-present quote, for example the S096 segment `根据GB3469规定…` against the rendered S101 text, would show whether the tool can say `present`. I did not run the tool itself.

## Impacted axes

- **Calibration:** the 10 `unverifiable` verdicts hide at least 4 reachable rows. Duplicate contradictory receipts exist. The ID namespace is ambiguous.
- **Operability:** the claim-freeze gate was absent, and an invalid-cache run was committed unlabeled.
- **Depth:** the offline recon stopped short of what `capture-text.py` allows.

## Smallest safe correction (do not apply in round 59, no frozen edits)

1. Next round, run quarantine rows through `capture-text.py` rendering and add a control with a known-present quote. This should reach `present` or `partial`.
2. Label or move `quarantine-{verdict,examine}.txt` as an invalid run (wrong cache). Add a cache directory digest to the digests file.
3. Key quarantine receipts by capture id or URL.
4. Keep the lesson's "not fabrication" language. My segment-level hits do not prove any full quote is present.

## Confidence

- High that the claims artifact is absent.
- High on the segment-level matches for S120, S125, S095 and S096, and on the 1b mappings.
- Medium on 1c's cause. The inference is the default cache, and the ready log does not say so directly.
