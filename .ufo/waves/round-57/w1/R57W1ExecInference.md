# R57W1ExecInference — inference-ground regression + C3 build-feasibility probe

seat: R57W1ExecInference (executor) · lane: chousa · wave: round-57 w1 · 2026-10-27
axis: frontier conformance for the `tools/inference-ground.py` leg R57-C3's frozen predicate runs.
Only this report was written in the lane; fixtures lived in `/fast/scratch/hyaku/chousa-r57/R57W1ExecInference/`
(deleted, §6). No network fetch; only committed lane bytes read.

## 1. The assigned regression check — PASSES

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin
$ python3 tools/inference-ground.py --entry corpus/knowledge/grey-literature-field-china-r42.md \
    --spans corpus/evidence/round56/spans.tsv --counts /dev/null --registry corpus/SOURCES.md \
    --root /home/vgpnk/Projects/shokunin/chousa-shokunin --quiet
EXIT=0
$ ... same command WITHOUT --quiet
GROUND entry=corpus/knowledge/grey-literature-field-china-r42.md section=1 bullets=3 tokens=6 grounded=6
GROUND: PASS
EXIT=0
```

**No defect candidate from the assigned command.** The tool bytes did not change this round, so the pass is
not luck: `git diff --stat 6656f077… HEAD -- tools/inference-ground.py` → empty;
`git show 6656f077…:tools/inference-ground.py | sha256sum` = `sha256sum tools/inference-ground.py` =
`6922697ec484abc5416572d069ba32994438d9a4e8e0bf7287ec65b311d517b0`. Only `tools/capture-fetch.py` changed.

## 2. Wider sweep — one failing pair, and it is NOT this round's

Over every entry↔spans pair the manifests name (23 entries, 23 pairs), 22 exit 0; one exits 1:
`corpus/knowledge/evidence-archive-field-policy-r41.md` × `corpus/evidence/round45/spans.tsv` —
`INF_UNCITED`/`INF_UNGROUNDED` ×4 bullets and `INF_TOKEN_NOT_IN_SPAN bullet=4 token='404'`, `GROUND: FAIL`
(those bullets carry no `S###` citation).

**Pre-existing.** Re-running the *base* tool against the *base* entry and spans, extracted with
`git show 6656f077…` into scratch, gives the identical result (`GROUND: FAIL`, exit 1, same four findings);
`git diff 6656f077… HEAD` on both files is empty. The round-45 gate never ran this tool on it —
`grep -n "inference\|ground" corpus/evidence/round45/c*-count.py` → nothing. **Reported, not patched**: it is
outside both frozen claims (C2's set is the 47 pinned triples; C3's entry does not exist yet). Coverage gap
for the L1: 27 entries carry a `#### Inference` section, only 23 are named by any
`corpus/evidence/*/spans.tsv`; never grounded: `citation-version-binding-r36.md`,
`citation-version-binding-r37.md`, `evidence-snapshot-coverage-r40.md`, `search-log-method-r39.md`.

## 3. The C3 build is FEASIBLE today — BOUND=4 reached on bytes already on disk

The frozen C3 counter fails at dispatch (`BOUND=0/7`, no entry). To test whether the target `BOUND>=4` is
reachable with bytes already held, I built fixtures in scratch against the **unmodified frozen counter**
(`c3-count.py --root <fixture>`) and the lane's own `tools/build-spans.py`. The L1 has already fetched the
missing documents; captures are committed and refetch rows successful with matching digests
(`raw_present=True txt_present=True sha_match=True` for S131 `de34c41f…`, S132 `a476f412…`,
S133 `6f545e6c…`). A realistic fixture — S127 clause + S118 (R7) + S131 (R1) + S132 (R2, R3), two quotes per
bound id, anchors at real quote offsets, sweeps for the rest — reaches the target honestly:

```
$ python3 corpus/evidence/round57/c3-count.py --root <fixture>
ENTRY=yes S127_CITED=yes NEW_GROUND=yes CLAUSE=yes
BOUND=4/7 (min 4) R1:S131 R2:S132 R3:S132 R7:S118
SWEPT=3/3 R4 R5 R6
QUOTE_ROWS=7 IN_SPAN=7 IN_ENTRY=7 IN_LESSON=7 SHORT=7 CONTEXT=7 CAPTURE_BOUND=7
SUBSTANCE=PASS ANCHOR_BOUND=2/2 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=PASS
EXIT=0
```

**No new fetch is needed for the C3 target.** Binding facts on current bytes (frozen heading rule: a line
ending with the title after one trailing parenthetical is dropped, prefix ≤16 chars, no `《》.[]［］`) — R1
heading `国家卫生健康委关于开展药品使用监测和临床综合评价工作的通知` (prefix 7, token 〔2019〕80号) via S131; R2
`国家卫生健康委办公厅关于规范开展药品临床综合评价工作的通知` (prefix 10, 〔2021〕16号) via S132; R3
`附件：药品临床综合评价管理指南（ 2021 年版 试行）` (prefix 3, 2021年版) via S132 (also S133); R7
`药品临床综合评价质量控制指南` (prefix 0, 2024年版) via S118 (held). R4/R5/R6 (2022年版 技术指南) have **no
heading on any committed capture**: the only carrier, `9695437cac165bb4b6145deb` (hnysfww.com), holds all
three titles and the `2022年版` token, but every line is HTML markup, so no line ends with a title. Those
three must be swept — and `BOUND=4` is exactly the target.

## 4. ATTACK — C3 accepts a `.txt` never derived from its `.raw` (C3=PASS on forged evidence)

**Attacked:** the C3 capture leg. The frozen `form_of()` (c3-count.py:143-157) reads the defined text form
from the `.txt` sidecar for every non-OLE/zip capture, and the manifest's `capture_sha256` is compared to
*that* file's digest (c3-count.py:243-249) — but the counter never checks the `.txt` against the `.raw` it is
supposed to come from. `grep -n "txt_sha256\|recipe_txt\|html_to_text" corpus/evidence/round57/c3-count.py`
→ **no match**. C2 does (c2-count.py:212-213: `txt == recipe_txt(raw, tmp).encode("utf-8") and
ok[-1]["txt_sha256"] == sha(txt)`); C3 has no equivalent.

**The attack.** I appended two lines to S132's committed `.txt` — the R4 title
`抗肿瘤药品临床综合评价技术指南` and the token `2022年版` — neither in the `.raw`:

```
raw contains 抗肿瘤药品临床综合评价技术指南:      False   # the fetched bytes never had it
recipe_txt contains 抗肿瘤药品临床综合评价技术指南: False
doctored .txt contains 抗肿瘤药品临床综合评价技术指南: True
```

Then I rebuilt the manifest, the registry row (anchors at real offsets), the entry and the lesson from that
forged `.txt` and ran the **unmodified frozen counter**:

```
$ python3 corpus/evidence/round57/c3-count.py --root <forged fixture>
BOUND=4/7 (min 4) R2:S132 R3:S132 R4:S132 R7:S118
SWEPT=3/3 R1 R5 R6
QUOTE_ROWS=6 IN_SPAN=6 IN_ENTRY=6 IN_LESSON=6 SHORT=6 CONTEXT=6 CAPTURE_BOUND=6
SUBSTANCE=PASS ANCHOR_BOUND=1/1 INFERENCE_GROUNDED=yes STRAY_IDS=-
C3=PASS
EXIT=0
```

**R4 was bound from bytes the document never contained.** Every leg reads green: `CAPTURE_BOUND=6` (the
manifest slice is exact for the forged `.txt`), `SUBSTANCE=PASS`, `INFERENCE_GROUNDED=yes`, anchors resolve.
Not caught downstream either: the forged `.txt` digest `9366f0e2…` ≠ the refetch row's `txt_sha256`
`8976b167…` (MATCH? False), yet the frozen C2 counter still prints `CONSISTENT=46/46 … C2=PASS` on the same
tree, because S132's URL is **not in C2's frozen 47** (`S132 in the C2 pinned 47? False`). **Scale:** of 61
committed `.raw` captures, 58 are non-OLE/zip (3 OLE, 1 zip) — for those the defined form comes from the
`.txt` sidecar, so **58/61 are doctorable**; only the 4 OLE/zip captures self-verify, their form being
derived from the `.raw` inside the counter.

**Verdict: the attack survives — C3's capture leg is forgeable.** The frozen claim is not mine to change, so
this is a finding only: C3 binds a document to the bytes of a fetch, but the evidence that binds it (heading,
edition token, quotes) is read from a sidecar never tied to those bytes. C2's `CONSISTENT` leg is the shape of
the missing check; one doctored `.txt` plus genuine captures moves C3 to PASS. Two sub-findings from the
same side: **S131's R1 title is not unique** in its form (3 occurrences), so `tools/build-spans.py` refuses it
(`build-spans: refused S131: quote occurs 3x`) and the honest fixture needed a hand-built manifest for S131
(the counter accepts it; `SUBSTANCE=PASS`) — the L1 must hand-build that manifest or choose another quote;
and **the committed sidecars are faithful**, since re-deriving `recipe_txt(.raw)` for all 59 committed `.txt`
with C2's own function and comparing bytes gives `not recipe-consistent: 0` — the forgery needed a *new*
`.txt`; the hole is that nothing in C3 would have noticed.

## 5. Two build constraints the L1 will hit (measured, avoidable)

**(a) Bare numerals in Inference bullets are grounding tokens.** `inference-ground.py`'s `NUM_RE` scrapes any
3+-digit number from a bullet's prose and each must occur in a cited span. My honest fixture failed
`INF_TOKEN_NOT_IN_SPAN bullet=3 token='2019'` on "- The 2019 notice is bound (S131)" — the S131 span carries
the title but not the year. Rewording to "- The notice is bound (S131): `国家卫生健康委关于开展药品使用监测
和临床综合评价工作的通知`." grounds it (tokens=4 grounded=4).

**(b) The `- UNBOUND R<k> sweep:` lines must NOT sit inside `#### Inference`.** The counter accepts them
anywhere (`swept=3/3` either way), but `inference-ground.py` reads *every* bullet of an Inference section, so a
sweep line there is uncited and ungrounded: `FINDING INF_UNCITED bullet=1 … INF_UNGROUNDED bullet=1 …` (one
pair per sweep line) → `GROUND: FAIL` → `INFERENCE_GROUNDED=no` → `C3=FAIL`. Keep them under
`#### Observation`. The `C3=PASS` fixture keeps all three sweep lines above the Inference heading.
Same cause, third constraint: every Inference bullet must cite an `S###` the manifest covers, and the
counter's `STRAY_IDS` leg rejects any `S###` token in the entry that is neither S127 nor a bound row — so
citing an unbound-but-held row (e.g. S130) fails the counter.

## 6. Scope and scratch hygiene

No lane file was created, edited or deleted; the only write in this seat is this report. I did not edit the
frozen counters, controls or claims, and propose no predicate change: §4 is a reported finding against a
frozen claim, not a patch. No fetch — every byte read came from `corpus/captures/` and `corpus/evidence/`.
All fixtures (c3f, honest, honest2, hand, forge, forge2, forge3, doc, trap1, base, c3, c3b, c3c, ctrl) lived
under `/fast/scratch/hyaku/chousa-r57/R57W1ExecInference/` and were removed before this report was written
(`rm -rf -- "$S"` → GONE). `TMPDIR` and `PYTHONDONTWRITEBYTECODE=1` were exported into that directory for every
run that wrote. No tool was installed or upgraded this seat (python3 plus the lane's own `tools/` sufficed), so
the tooling-directive record is empty.

VERDICT: the assigned inference-ground regression **survives** (exit 0, `GROUND: PASS`, tool bytes unchanged
since base); the wider sweep finds one pre-existing FAIL predating round 57; the live C3 build is
**reachable today** at `BOUND=4` with S131/S132/S133 already fetched; and my attack on C3's capture leg
**survives — C3=PASS on a forged `.txt`** whose bytes were never in the fetched document.
