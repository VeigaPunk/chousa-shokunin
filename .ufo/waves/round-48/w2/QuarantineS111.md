# Quarantine hand-check — chousa S111

**Verdict: `payload-absent` FALSIFIED — the quote is PRESENT verbatim in the cited document.** The ABSENT verdict is an artefact of the checker matching against the two-column `pdftotext -layout` render, where a right-column line interleaves into the quoted run between `可参` and `考`. In a reading-order render of the same captured bytes the quote is a contiguous run (only a bare line break and a CJK/Latin space are folded out).

## Row under test

- Frozen slice: `quarantine-slice:15` — `S111   `payload-absent``.
- Register: `absent-defect-register.md:51` — `chousa | round4 | S111 | payload-absent | https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290` with one quote: `报告规范，研究者可参考PRISMA框架`.
- Lint record: `quote-lint-full-v5.json` — `lane chousa, round4, id S111, verdict ABSENT, binding id`, `line: Quote — section 2.1.1, contiguous run`. The other three quotes on the same row (`3文献检索策略…`, `尚无专门针对动物实验SR的报告规范`, `实验动物与比较医学, 2025, 45(4): 496-507`) all reached verdict `folded` under `no-whitespace`; only this one was declared ABSENT.
- Lane SOURCES row: the unique row citing `id=5290` is `lanes/chousa/round4/SOURCES-PROPOSED.md:32` as **S116** (round4 ids were renumbered +3 at packaging, `ID-REMAP.md`: `S113 → S116`; the register/lint carry the earlier staged id). URL+quote pair is unique and unambiguous; the attesting block is `## Gate — S116`, lines 41–48, with this quote on line 46.

## Local capture checked (no live fetch)

Key = `sha256(url)[:24]` per `quote-lint.py:438`:

- `.qcache/fd468a36d78ff156b6200946.pdf` / `.raw` — 1,156,890 B (byte-identical twins), sha256 `72763389bbe95ab312de097125baa447370a244cb3f1b1bd3030b9956fb5abce`, `%PDF-1.7`. Size matches the gate's "HTTP 200, 1,156,890 bytes".
- `.qcache/fd468a36d78ff156b6200946.txt` — 82,903 B, sha256 `90f2f54cef21cb49e0233d5d4d2eb5ba4ecc750ae2f9a825bbbc3d43d68646cc`. Re-running `pdftotext -layout` on the captured PDF reproduces exactly 82,903 B → this `.txt` IS the `-layout` render.
- NB: the gate claims "text extracted with `pdftotext -layout`, 66,261 bytes", but plain `pdftotext` (no flag) on the same PDF yields exactly 66,261 B. The gate's byte count names the wrong mode — the same mislabeled-extraction defect as S116.

## Measurements (commands run, scratch `/tmp/chousa-r48-QuarantineS111`, deleted)

```
TXT=.qcache/fd468a36d78ff156b6200946.txt
grep -F '报告规范，研究者可参考PRISMA框架' $TXT        → rc=1  (absent in -layout)
#  fragments in -layout txt (python char offsets):
#    17729  '研究者可参'   line 259 col 21
#    17769  '价值，具体表现在以下方面。'  line 259 col 61  (RIGHT column)
#    17783  '考 PRISMA 框架'  line 260 col 0
#  page 5 (form-feed count). File order interleaves the right column
#  between the quote halves → fails every fold incl. no-whitespace.
pdftotext $PDF flow.txt        → 66,261 B  sha256 b4276363f1…98028e0
pdftotext -raw $PDF raw.txt    → 64,919 B  sha256 d7e82f6760…29aac5f
python3: re.sub(r'\s+','',t) substring test on both renders:
    quote found — flow.txt ws-offset and raw.txt ws-offset 10678.
    raw.txt lines 297–298: '前尚无专门针对动物实验SR的报告规范，研究者可参'
                           '考PRISMA 框架，对研究实施过程的细节进行全面、'
    context after strip: '…由于目前尚无专门针对动物实验SR的报告规范，
      研究者可参考PRISMA框架，对研究实施过程的细节进行全面、详尽地披露…'
```

Companion sweep: `grep -l '研究者可参考PRISMA' .qcache/*.txt` → no other cached document contains the run; the CN URL variant key `e898c4456f6c3fa8b1a86602` has no capture. The verdict rests on the cited capture alone.

## Reason

The lane's own "Column note" (`SOURCES-PROPOSED.md:48`) asserts the sentence beginning `由于目前尚无专门针对动物实验SR的报告规范` "is not contiguous in any automated extraction" — that claim is false: plain `pdftotext` and `-raw` both render the sentence contiguous up to whitespace, and the gate simultaneously lists this quote as a "contiguous run" of section 2.1.1, contradicting its own note. The checker's folds are all computed on the `-layout` artifact, the one mode that interleaves columns, so the split `可参|…右栏…|考` defeated even `no-whitespace` matching. The quote is a faithful transcription of printed text on page 5, left column — not a fabrication. Classification: **present** (register's `payload-absent` is a checker artifact; remedy is re-matching against the reading-order render, not quote correction).

## C1 impact

This row counts as a checked non-fabrication: the ABSENT verdict dissolves against plain `pdftotext` output on the captured bytes. Residual real defects are metadata-level only: (a) id churn — the row is S111 in the register, S116 in the lane's post-remap staging (`ID-REMAP.md` round4 `S113→S116` implies a third numbering at lint time); (b) the gate's extraction byte count corresponds to plain `pdftotext`, not the claimed `-layout`; (c) the gate's column note overclaims "not contiguous in any automated extraction" while labelling the quote a contiguous run.
