# Seat R52CritForgeC2 — first-falsify: frozen R52-C2 counter (`c2-count.py`)

Attacked: `corpus/evidence/round52/c2-count.py` (frozen, `claims.md` C2) by
building adversarial lane bytes in scratch only and running the counter with
`--root /fast/scratch/hyaku/chousa-r52/R52CritForgeC2/root` (TMPDIR set there).
No production file written; no tools installed; no network. Counter binary is
read-only against the fleet cache and absent-defect-register; the lane was never
mutated. Scratch removed after this report.

## Method

Constructed one scratch root containing: `corpus/SOURCES.md` (Registry rows),
three `corpus/knowledge/*` entries, `corpus/lessons/round-52.md`, a hand-written
`corpus/evidence/round52/spans.tsv` + span files, and `tools/inference-ground.py`
(a verbatim copy of the lane tool — the real one, not a stub). Generator core
(scratch `fixture_build.py`, mode v1):

```python
Q = {
 "S113": ("PRISMA for Searching", f_m, 2297, d_m, URLS["MEDSCI"],  E_ZHR),
 "S114": ("Toggle navigation",      f_c, 112,  d_c, URLS["CHINAGP"], E_ZHR),
 "S116": ("PRISMA 2020 チェックリスト", f_a, 0,  d_a, URLS["ARCHIVE"], E_JPW),
}
# entry/lesson/sources rows mirror the lane schema; spans.tsv rows:
#   S113 <url> <sha256(txt)> 2297 spans/S113-1.txt PRISMA for Searching E_ZHR
# (3 identical rows per id, one offset, anchor "char 2337" etc.).
```

Bound ids S113/S114/S116; NIPH refused (no row, no `source:` line, one lesson
line `- refused-doc: <NIPH url>`). Quotes are navigation/boilerplate fragments of
the capture `.txt` forms: `Toggle navigation` (CHINAGP txt, abs 152), `PRISMA
for Searching` (MEDSCI txt, abs 2337; occurs 2× — see below), `PRISMA 2020
チェックリスト` (ARCHIVE txt, abs 0). Inference bullets cite bound ids and carry
only a numeral (`2020`) or the quoted phrase; E_NIPH cites S116.

## Results (all runs: `python3 …/round52/c2-count.py --root <scratch-root>`)

```
V1 (refuse NIPH; boilerplate quotes; one quote reused ×3/id; one anchor offset):
ENTRIES=3/3 BOUND=3/4 REFUSED=1 BOUND_IDS=S113,S114,S116 REF_ID_UNBOUND=0
NEW_GROUND=3/3 QUOTE_ROWS=9 ON_BOUND=9/9 SPAN_IDS=3/3 QUOTES_IN_SPAN=9/9
QUOTES_IN_ENTRY=9/9 QUOTES_IN_LESSON=9/9 QUOTE_SHORT=9/9 SPAN_CONTEXT=9/9
CAPTURE_BOUND=9/9 SUBSTANCE=PASS ANCHOR_BOUND=3/3 INFERENCE_GROUNDED=3/3
QUARANTINE_VERDICTS=1/1 (S120) QUARANTINE_BLOCKED_ADOPTED=0
C2=PASS   exit=0
```

Same root with `--lane-only`: identical except `CAPTURE_BOUND=skipped`, C2=PASS.

| Shortcut | Result | What refuses it |
|---|---|---|
| Boilerplate/navigation quotes (V1) | **PASS** | nothing — presence only |
| One quote reused ×3 per id, one `char N` anchor (V1) | **PASS** | nothing — no uniqueness/distinctness leg |
| Refuse the hardest (NIPH .docx) via one lesson line (V1) | **PASS** | nothing — refusal is legal; only the line is checked |
| Hand-written spans.tsv never produced by build-spans (V1) | **PASS** | nothing — counter never runs build-spans; only slices/digests |
| Inference bullet quoting a phrase but asserting the opposite (b1/b2) | **PASS** | `INF_POLARITY_FLIP` only when the phrase's content word recurs OUTSIDE the quote after a negator (`lacks navigation` → flip fires) |
| NIPH span taken from the `.txt` sidecar garbage (V5; digest = sidecar sha) | **PASS** | nothing — `form_text` accepts any cache `.txt` whose sha matches, incl. the docx sidecar; CAPTURE_BOUND=12/12 |
| S116 row whose first URL is the archive but `source:` lines cite the original (V4) | FAIL | `BOUND=2/4`, `REF_ID_UNBOUND=3` (cites regex demands the archive URL verbatim) |
| NIPH span from raw XML markup, digest = raw sha (V6) | FAIL | `CAPTURE_BOUND=9/12` (derived form ≠ markup) |
| Hollow quote (single CJK punctuation, V2) | FAIL | `SUBSTANCE=FAIL` (HOLLOW_QUOTE), also caps 6/9, anchors 2/3 |
| Whole-capture span file (V3) | FAIL | `SUBSTANCE=FAIL` (OVERWIDE_SPAN), CAPTURE_BOUND=3/9 |
| Stray unbound S-token in an entry (V7) | FAIL | `REF_ID_UNBOUND=1` |
| Missing `refused-doc` line while refusing NIPH (V8) | FAIL | `REFUSED=0` → BOUND+REFUSED=3≠4 |

Observed outputs for the failing variants (leg lines that changed vs V1):

```
V4: BOUND=2/4 (min 3) REFUSED=1 BOUND_IDS=S113,S114 REF_ID_UNBOUND=3
     ON_BOUND=6/9 SPAN_IDS=2/2 ANCHOR_BOUND=2/2 INFERENCE_GROUNDED=3/3  C2=FAIL
V5: BOUND=4/4 REFUSED=0 BOUND_IDS=S113,S114,S115,S116 QUOTE_ROWS=12
     CAPTURE_BOUND=12/12 SUBSTANCE=PASS ANCHOR_BOUND=4/4
     INFERENCE_GROUNDED=3/3  C2=PASS
V6: BOUND=4/4 CAPTURE_BOUND=9/12 ANCHOR_BOUND=3/4 SUBSTANCE=PASS  C2=FAIL
V2: SUBSTANCE=FAIL CAPTURE_BOUND=6/9 ANCHOR_BOUND=2/3 QUOTES_IN_LESSON=6/9
     INFERENCE_GROUNDED=2/3  C2=FAIL
V3: SUBSTANCE=FAIL CAPTURE_BOUND=3/9 ANCHOR_BOUND=1/3  C2=FAIL
V7: REF_ID_UNBOUND=1  C2=FAIL
V8: REFUSED=0  C2=FAIL
b1: "- S114 のナビゲーションには `Toggle navigation` は存在しない。" →
     INFERENCE_GROUNDED=3/3, C2=PASS
b2: "- S114 does not show `Toggle navigation`." → INFERENCE_GROUNDED=3/3, C2=PASS
b3: "- S114 entirely lacks navigation; `Toggle navigation` is absent." →
     INF_POLARITY_FLIP bullet=1 token='Toggle navigation / navigation', grounded=2/3
```

V5 detail: NIPH bound with quote `[Content_Types].xml` (abs 30 in the cache
`3a8b45977cd111e45e3980a5.txt` sidecar; occurs 2×), span = first 57 chars of
the sidecar, digest = sha256 of the sidecar file. No docx text form was ever
derived; the counter reports CAPTURE_BOUND=12/12. The round-51 closure defect "(3)
NIPH zip-member form" is therefore still bypassable: nothing ties the manifest
digest to the *derived* form as long as the `.txt` sidecar hash matches.

Also verified: (a) `git grep -l -e 文献検索期間 -e 完全な検索戦略 -e 检索报告清单
00f8c7f5272a1d98b6d34913985fa4537e00aaf9 -- corpus/knowledge` returns rc=1
(NEW_GROUND gate real); (b) base registry ends at S112 (S111 SinoMed, S112
JAHBS); (c) register row S120 names the NIPH URL, `| \`chousa\` | round5 | S120
| \`payload-absent\` | https://c2h.niph.go.jp/… |`; (d) a raw UTF-16LE-decoded
span from an HTML `.raw` yields no usable quote (ASCII runs do not survive the
decode) — the raw-decoy hole is practically confined to the .docx sidecar.

## What the closure must spot-check by hand (entailment is not counted)

1. **NIPH spans** — confirm each S115 span slices the *derived* zip-member text
   form (19682 chars), not the `.txt` sidecar; the counter cannot distinguish.
2. **Manifest provenance** — rerun `build-spans.py --check` (or diff against a
   builder run); the counter accepts any 7-column manifest, even with duplicate
   rows and non-unique quotes (`PRISMA for Searching` occurs 2× in the MEDSCI
   form; build-spans would refuse it).
3. **Quote substance/topic** — 3 *distinct*, content-bearing quotes per bound id;
   nav strings (`Toggle navigation`) pass all legs today.
4. **Entailment** — bullets that quote a phrase and assert the opposite (b1/b2)
   pass; read bullets for meaning, including cross-document citations (E_NIPH
   citing S116 is legal to the counter).
5. **Registry↔entry binding** — `source:` lines must name the same URL as the
   row's first cell and the entry's content must come from that capture; the
   counter regex-matches the URL only.
6. **Refusal honesty** — the predicate allows refusing any one of the four
   documents; refusing NIPH dodges the .docx form entirely. Require a real
   capture-form attempt/statement for a refused doc.
7. **Verdict line truth** — presence is counted, not content; verify S120's
   verdict against the register.

Cost of the cheapest passing bundle (V1): 937 B entries + 262 B lesson + 1064 B
registry + 3642 B evidence ≈ 5.9 KB of lane bytes.

VERDICT: attacked the frozen R52-C2 counter with a scratch-only fixture; the
cheapest bundle (refuse NIPH, boilerplate quotes reused ×3, single anchor offset,
hand-written manifest, opposite-assertion bullets) prints `C2=PASS` exit 0, and
the NIPH-sidecar variant binds all four documents without ever deriving the docx
text form — CAPTURE_BOUND and SUBSTANCE/ANCHOR/INFERENCE_GROUNDED are the legs
that refuse only the malformed variants, never the semantic dodges.
