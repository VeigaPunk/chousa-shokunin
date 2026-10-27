# R57W1MutFetchTool — mutation test of tools/capture-fetch.py (policy artifact)

Seat: R57W1MutFetchTool (leaf; no dispatch). Scratch `/fast/scratch/hyaku/chousa-r57/R57W1MutFetchTool` (TMPDIR+PYTHONDONTWRITEBYTECODE set; dir deleted before yield — see §7).

**Zero-network detector.** Tool derives REC/STORE from `__file__` (tool:48-51), so each variant copy lives in its own fixture lane `run/<v>/lane/tools/capture-fetch.py`. All six copies verified byte-identical to lane bytes (`sha256 f27fa58f…`) before mutation. `curl` is intercepted by a PATH shim (`bin/curl`) that logs argv and serves `$FIXTURE/<basename>` bytes — `slow.*` returns rc=28 iff `--max-time ≤ 15`, `fail.*` always rc=28, `flip.html` serves version A for invocations 1–3 then B from the 4th. No network egress occurred.

## Detector baseline (pristine, `pairs-base.tsv` = HTML/plain/slow/fail/PDF)
```
S901 page.html  rc=0 200 raw=13708a3b4173 txt=77f7052d7dc2 STORED
S902 plain.txt  rc=0 200 raw=c33995cf16b8 txt=c33995cf16b8 STORED
S903 slow.html  rc=28 000 raw=- txt=-        (recipe curl gave up at 15s)
S904 fail.html  rc=28 000 raw=- txt=-
S905 doc.pdf    rc=0 200 raw=c3a8c07f9ed6 txt=ca4f32892050 STORED   rc=0
consistency check (stored .txt == recipe_txt(.raw), imported from pristine copy):
d2eb…: True  da75…: True  fc3a…: True        # baseline passes
--status: pairs=5 rows=5, S903/S904 fails=1
```
Baseline succeeds → the detector is conclusive.

## Mutants (each = one-line edit vs pristine)

| M | Point | Change | Leg attacked |
|---|-------|--------|--------------|
| M1 | tool:192 `if n >= MAX_ATTEMPTS:` | → `if False:` | 3-attempt cap → raw binding |
| M2 | tool:127 `--max-time 15` | → `60` | fetch recipe → raw binding + spacing |
| M3 | tool:146 `txt = recipe_txt(raw,tmp).encode()` | → `txt = raw` | CONSISTENT |
| M4 | tool:107-108 `raw_sha/txt_sha = sha(…)` | → `"-"` | raw binding |
| M5 | tool:183-184 `scratch = env HYAKU_SCRATCH …` | → `/tmp` | none of the frozen legs |

### M1 — cap dropped → VERDICT: corrupts **raw binding**
Seeded refetch.tsv: attempts 1–2 failed 700 s apart, attempt 3 success body A (pin `14dfe7f2…`), capture A stored.
```
PRISTINE: S910 flip.html: already 3 attempts (max 3) — skipped   rc=0
M1:       S910 8e3cb8ac… attempt=4 rc=0 http=200 raw=f5b56e4c… STORED
last row: attempt=4 raw_sha256=f5b56e4c… (B) — c2-count takes LAST successful row
capture .raw: pristine=14dfe7f2… (==pin, REPRODUCED)  M1=f5b56e4c… (≠pin, DRIFTED)
```
An unbounded 4th fetch silently rewrote the byte-backed verdict the counter binds to the pin.

### M2 — max-time 60 → VERDICT: corrupts **raw binding** (+spacing)
```
pristine S903: rc=28 http=000 raw=- txt=-   (no capture; feeds UNREACHABLE spacing evidence)
M2 S903:       rc=0  http=200 raw=bc630283… STORED   (.raw == fixture slow.html bytes)
curl argv:     --max-time 15  vs  --max-time 60
```
A slow-but-live URL becomes byte-backed under the mutant, flipping verdict class and eroding the ≥600 s failed-attempt evidence the UNREACHABLE leg needs. Deviation from the frozen campaign recipe (`--max-time 15`, tool docstring:6).

### M3 — recipe dropped → VERDICT: corrupts **CONSISTENT**
```
M3: every stored .txt == .raw (cmp TRUE for da75…,d2eb…,fc3a…); rows rawsha==txtsha
consistency check vs pristine recipe: pristine all True;
  M3 da75…(HTML): False   fc3a…(PDF): False   d2eb…(plain): True (recipe is identity on plain text)
```
`.txt` ceases to be "the frozen campaign recipe applied to .raw" (c2-count:212–215 would fail `txt is not the recipe of raw`); CONSISTENT breaks exactly where the recipe transforms.

### M4 — sha256 recording dropped → VERDICT: corrupts **raw binding**
```
M4 rows: rc=0 200 raw_sha256=- txt_sha256=- while 'STORED' (bytes written to corpus/captures/)
counter semantics (c2-count.py:207): ok[-1]["raw_sha256"] != sha(raw) → every byte-backed
  capture becomes MISSING; BYTE_BACKED=0<32, CONSISTENT check also unreachable (needs txt_sha256)
```
Digest-less rows make the verdict unattested — the pin↔bytes equality the whole claim rests on is gone.

### M5 — scratch hardcoded /tmp → VERDICT: **no frozen leg** corrupted
```
curl -o: pristine/restored  $HYAKU_SCRATCH/chousa-r57/fetch/<key>.1.out
       M5                  /tmp/chousa-r57/fetch/<key>.1.out      (/tmp debris: recipe/, refetch.append)
diff refetch (minus fetched_utc) M5 vs restored-pristine: IDENTICAL; capture trees: IDENTICAL
recorded digests still match stored bytes (S901/S902/S905 raw+txt sha match: True)
```
Mutant output is byte-for-byte equal to pristine on the evidence plane; the break is operational only (§7 "never /tmp >50 MB", host-disk pressure). **SURVIVES** the counter — a policy violation the predicate cannot see. Reported, not patched (frozen artifact).

## Notes
- C2 state at probe: `SET=47 VERDICTS=47/47 REPRODUCED=41 DRIFTED=5 UNREACHABLE=1 BYTE_BACKED=46 CONSISTENT=46/46 FLAGGED=0/0 C2=PASS` (dispatch's 4 pending retries landed; S0xx unreachable landed since). Frozen counters/corpus never touched; lane tool sha256 `f27fa58f…` identical before/after.
- M3 nuance for reviewers: plain-text captures keep `txt==raw`, so a recipe-drop mutant hides on text-only URLs; CONSISTENT still catches it on any HTML/PDF capture — the detector needs recipe-transforming content in the set, which the real corpus has.
- M5 shows the counter's blind spot: out-of-lane temp placement is invisible to `refetch.tsv`/captures; only host-side hygiene catches it.

## Cleanup
`rm -rf /fast/scratch/hyaku/chousa-r57/R57W1MutFetchTool` and `rm -rf /tmp/chousa-r57` executed before yield; lane repo untouched (only this report file written). No tools installed/upgraded.

VERDICT: attacked `tools/capture-fetch.py` as policy artifact — M1/M2/M4 falsify the **raw-binding** leg, M3 falsifies **CONSISTENT**, M5 **survives** (operational-only break). Tool killed 4/5 mutants; detector conclusive.
