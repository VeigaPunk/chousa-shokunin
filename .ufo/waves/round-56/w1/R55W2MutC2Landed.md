# R55W2MutC2Landed — round-55 C2 mutation report

Fixture: scratch clone `/fast/scratch/hyaku/chousa-r56/R55W2MutC2Landed/lane`, checkout `29cfb12abd70f688b48c0d17f31e636f2d81104a`; `git rev-parse --show-toplevel` returned that fixture path and HEAD was the requested commit. Frozen claim read: `corpus/evidence/round55/claims.md` lines 98–143.

Detector, used unchanged for pristine, each mutant, and restored bytes:
```sh
export TMPDIR="$S/tmp" PYTHONDONTWRITEBYTECODE=1
python3 "$S/lane/corpus/evidence/round55/c2-count.py" --root "$S/lane"
```
`c2-count.py` accepts `--root` and `--lane-only`, not `--work`; TMPDIR was inside scratch. Pristine and final restored output: `C2=PASS`, exit 0. Pristine counters included `BOUND=3/3`, `QUOTE_ROWS=19`, `CAPTURE_BOUND=19/19`, `ANCHOR_BOUND=3/3`, `QUARANTINE_VERDICTS=1/1 (S125)`.

| Perturbation (location) | Before → mutant → restored SHA-256 | Observed detector output; verdict |
|---|---|---|
| Drop lesson quote row S124 char 4652, `round-55.md:81` | lesson `dadd9b6d50d4057e49482ae2212e8889b17e6a70c44206a1557777ec45b89e7d` → `16ea28680ce19c768bd724afc849d71fce09ef4adc3f4f996fbb4742327aa6f5` → `dadd9b6d50d4057e49482ae2212e8889b17e6a70c44206a1557777ec45b89e7d` | `QUOTES_IN_LESSON=19/19`, `C2=PASS`, exit 0 — **SURVIVED**. Same quote remains in the re-opened-sources table at line 41; the counter checks substring presence, not the all-located-quotes row. |
| Change S124 anchor `char 4652`→`4653`, `SOURCES.md:134` | sources `d94814c7d1ed8be36be7c1648a9af64725b3e281d509d176686cae3a922a3a3d` → `c4780ab2c0f1bb5b603dae5f4dec7ef6aed6d4a0f7f1dbb80e6d34c5688c4814` → `d94814c7d1ed8be36be7c1648a9af64725b3e281d509d176686cae3a922a3a3d` | `BOUND=3/3`; `ANCHOR_BOUND=2/3`; `C2=FAIL`, exit 1 — **KILLED**. |
| Add `source: S113 — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3` to entry without changing S113 used-by | entry `fd51538377138335dd3247a8bc8803f83b47239424ebf54446fc0395858d2382` → `99e9f1596ef1655a4ed085725a403816a2ae4f27a5628d2fcf69b60e5a4f14d8` → `fd51538377138335dd3247a8bc8803f83b47239424ebf54446fc0395858d2382` | `HELD_BAD=1`; `REF_ID_UNBOUND=2`; `C2=FAIL`, exit 1 — **KILLED**. |
| Change S125 `opened` to 2026-10-26, `SOURCES.md:135` | sources `d94814c7d1ed8be36be7c1648a9af64725b3e281d509d176686cae3a922a3a3d` → `082cb0712703f5759a50a2fbf31e75a79c455b5af1cc3ff4f4be3610727014e6` → `d94814c7d1ed8be36be7c1648a9af64725b3e281d509d176686cae3a922a3a3d` | `BOUND=2/3 (min 2)`, `ON_BOUND=15/19`, `REF_ID_UNBOUND=7`; `C2=FAIL`, exit 1 — **KILLED** (third document is neither bound nor refused). |
| Replace S124-1 with sidecar slice and use sidecar digest; manifest row 2 | `spans.tsv` `aa73b1e42696a906313e7a9e5b69b242aadbc0b174524905e9532a58f86e143f` → `2bbdd4df569ed488f50d2610a935dbdfaa2fb3b5dcd3cc8112f05690742ef9fe` → `aa73b1e42696a906313e7a9e5b69b242aadbc0b174524905e9532a58f86e143f`; `S124-1.txt` `39d19bdb212e245d56e0e3737321ba269a63046e7966a7481bfebcf463cec5d0` → `410f108a5ad93d71d11b22648db2979999aee1ded97f54da0b38a26859e8eb28` → `39d19bdb212e245d56e0e3737321ba269a63046e7966a7481bfebcf463cec5d0` | GCP `.txt` sidecar digest `55b4085c442fce1abf3ebef737344eb32fecf3e2b12fc781ad7a1e802eeac4e5`; its UTF-8 replacement-decoded slice `[90:130]` was 40 U+FFFD characters. `QUOTES_IN_SPAN=18/19`, `CAPTURE_BOUND=18/19`, `ANCHOR_BOUND=2/3`; `C2=FAIL`, exit 1 — **KILLED**. |
| Add stray `S130` token after entry line 9 | entry `fd51538377138335dd3247a8bc8803f83b47239424ebf54446fc0395858d2382` → `f330ecb0fb408a707ee535fb49d290a86766fc253e6e4755574afcaf66f90564` → `fd51538377138335dd3247a8bc8803f83b47239424ebf54446fc0395858d2382` | `REF_ID_UNBOUND=1`; `C2=FAIL`, exit 1 — **KILLED**. |
| Delete quarantine verdict line, `round-55.md:60` | lesson `dadd9b6d50d4057e49482ae2212e8889b17e6a70c44206a1557777ec45b89e7d` → `a599793a131babcce0aa55fc0e182d4477c0b6338050acfc51bb3ed9e4978976` → `dadd9b6d50d4057e49482ae2212e8889b17e6a70c44206a1557777ec45b89e7d` | `QUARANTINE_VERDICTS=0/1 (S125)`; `C2=FAIL`, exit 1 — **KILLED**. |
Restoration check re-ran the same detector: `C2=PASS`, exit 0. Final hashes exactly matched pristine: `SOURCES.md d94814c7d1ed8be36be7c1648a9af64725b3e281d509d176686cae3a922a3a3d`; lesson `dadd9b6d50d4057e49482ae2212e8889b17e6a70c44206a1557777ec45b89e7d`; entry `fd51538377138335dd3247a8bc8803f83b47239424ebf54446fc0395858d2382`; manifest `aa73b1e42696a906313e7a9e5b69b242aadbc0b174524905e9532a58f86e143f`; S124-1 span `39d19bdb212e245d56e0e3737321ba269a63046e7966a7481bfebcf463cec5d0`.

The sidecar mutation used the file `…/.qcache/bdff491a75c6abeda1d9c01d.txt`; the counter's C2 definition explicitly treats the OLE `.raw`/BASE `capture-text.py` form—not this sidecar—as the defined form (`c2-count.py` lines 1–2, 88–107). The original S124-1 span and manifest hashes were restored after the run.


Probe note: one initial anchor edit omitted the Registry row's final table delimiter and was discarded as malformed; exact pristine bytes were restored, then the one-character anchor mutation was rerun with the delimiter retained (the scored result above).

VERDICT: C2 killed six of seven perturbations; the dropped S124 quote-table row survived because its quote remains elsewhere in the lesson.