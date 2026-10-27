# R54 — Seat `R54ExecS130Probe` — S130 re-open under the new OLE `.doc` text form

scope: re-open the round-53-refused staged entry `grey-literature-and-chinese-search-record-r40.md` (staged S130 `.doc` / S131 article / S133 portal page) with the round-54 C1 candidate `tools/capture-text.py`; **planning only — no adoption, no production write, no lane edit.** Base `c49ffc6ce1c3de87c1dfa96856239ed7274bf07b`; C1 candidate `8a7d0f137a352000d78704ba5695ded8857104fe`. Access 2026-10-26, no network: every source is an on-disk capture under the read-only `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache` (key = sha256[:24] of the URL).

## 1. The S130 capture is an OLE Word 97+ `.doc`, and the C1 candidate reads it

```
$ R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw
$ python3 .../tools/capture-text.py "$R" > tf.txt 2> tf.err
rc=0 bytes=34234 stderr=0                       # 13,718 chars, sha256 f0b0899794420b0c10aa9d7caa75e8ccd161b8ad73d9c84e62ebf0bd9c1ef01c
$ python3 .../tools/capture-text.py "$R" --locate "是否检索灰色文献等关键问题"
LOCATED count=1 offset=4678                    # rc=0
```

FIB (read by the candidate's own reader): `wIdent 0xA5EC`, `nFib 0xC1` (Word 97+), flags `0x5014` — `fComplex` set (fast-saved), `fWhichTblStm` clear → `0Table`, `fEncrypted`/`fObfuscated` clear; `ccpText 13804`, `ccpFtn 0`, `ccpHdd 152`; Clx at `fcClx 6623 / lcbClx 21` = one Pcdt, one piece CP 0→13962 at `fc 0x800` (UTF-16LE, not compressed). The file the brief calls *fComplex (fast-saved)* is exactly the case the candidate handles: the form is the main story CP 0..13804 (the 152-char header/footer story and the trailing 附件3 material fall outside `ccpText` and are correctly excluded). Fields present: 3 `EMBED Visio.Drawing.11` drawings, 7 `PAGE` fields; the candidate emits field **results only**, so no field code leaks into the form.

## 2. The three text forms side by side (defined form vs `.txt` sidecar vs UTF-16LE decode)

```
defined-form (capture-text.py): chars=13718 fffd=0    ctrl<0x20=['\t','\n']
.txt sidecar (read as UTF-8)  : chars=241510 fffd=40252   (323,728 B on disk)
UTF-16LE decode of the .raw   : chars=121964 fffd=887
  '是否检索灰色文献等关键问题': defined=1@4678  sidecar=0@-1  utf16=1@57497
  '五个方面'                  : defined=0@-1  sidecar=0@-1  utf16=0@-1
  'paymentAmount=10'          : defined=0@-1  sidecar=0@-1  utf16=0@-1
```

The UTF-16LE figures **reproduce round-53 exactly** (`corpus/lessons/round-53.md:65`: 121,964 chars, 887 U+FFFD, `是否检索灰色文献` once at 57497) — round-53's "no defined text form" was true of the two forms it could read and is false of a third. The other two recheck phrases of the staged entry are **not in this document at all** (they belong to S131 and S133, §5).

## 3. LibreOffice comparison (private profile, same bytes)

```
$ soffice -env:UserInstallation=file://$S/prof --headless --convert-to "txt:Text (encoded):UTF8" \
      --outdir $S/lo "$R"          # LibreOffice 26.8.1.1, rc=0, 13,729 chars, sha256 17a3073feea8…
```

Replicating `c1-count.py:leg_real` on this capture alone: oracle lines with ≥8 non-space chars = **248**; present directly **234**, present after dropping **one** leading list label (the `•` bullet LibreOffice renders and the piece-table text does not) **14**, **missing 0**; whitespace-free length ratio **0.9989** (window 0.90–1.10); a whitespace-free diff of the two forms shows **only** those 14 `•` insertions plus LO's mid-URL spaces. No U+FFFD in the defined form. `pgrep -u $USER -f "UserInstallation=file://$S"` → none; no `soffice.bin` left.

## 4. Round-53 Gate flip — text-form half: **now fires**

`corpus/lessons/round-53.md:65` flip = "a defined OLE `.doc` text form **and** the regulator field decided on its own source, currency kept as an Unknown".

- **Text-form half — MET, measured.** Defined form exists (exit 0, 13,718 chars, 0 U+FFFD, only tab+NL below 0x20); it holds every LibreOffice oracle line of the same bytes (§3); ratio 0.9989; the field sentence locates exactly once (`LOCATED count=1 offset=4678`) and stdout holds it at 4678.
- **Second half — the L1's Gate call, not mine.** The field sentence is the regulator's *own* document text (NMPA 上市药品临床安全性文献评价指导原则（试行）; the campaign's own tier-B row `merge/chousa/SOURCES.append.md:55`), and it is **not** unique to this carrier: the tier-C print `0435b64f65c3ea7ddc6bb92e.txt` (pharmwyp, refused in round 53 as a tier-C third-party print) carries `是否检索灰色文献等关键问题` once at 8165 and the same five headings (`一、概述` 1776 … `五、附录` 9778); the **NMPA-hosted URL has no capture** (`b5c2c7c891a79ecbc9317cd8.fail`, `rc=22`) and `f4b185ee5f562255eab4f72c.txt` (药研日记, tier C) carries the title once but the field 0 times.
- **Currency — the `.doc` cannot carry it.** `2019` 0, `二〇一九` 0, no date of issue anywhere in the defined form; `2019-06-18` exists only in S131 (`27d4865f201e99c1fed9f79b.txt` 248). A next-round entry citing the `.doc` must keep currency as Unknown, exactly as the flip words it.

## 5. The staged entry's three recheck phrases, located (each in its own capture's text form)

| staged quote | owning capture | text form | count | offset | ≤25 words/≤160 ch | one line | unique |
|---|---|---|---|---|---|---|---|
| `是否检索灰色文献等关键问题` | S130 `.doc` | defined form (capture-text) | 1 | 4678 | 1 / 14 | yes | yes |
| `五个方面` | S131 article | `.txt` sidecar UTF-8 | 1 | 817 | 1 / 4 | yes | yes |
| `paymentAmount=10` | S133 portal | `.txt` sidecar UTF-8 | 1 | 4178 | 1 / 15 | yes | yes |

Further located quotes in the **S130 defined form** (all unique, one line, ≤160 ch): `文献检索策略：检索途径、检索数据库、检索时限及检索式。应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。` @4625 (67 ch) · `检索策略包括检索的数据库、检索范围（如主题等）、检索词、检索式（即检索词组合方式）和时间范围等，应当根据不同的研究目的制定。` @761 (62 ch) · `查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。` @994 (52 ch) · `灰色文献中可能包含阴性研究结果` @1046 (15 ch) · `四、本指导原则所依据的参考文献` @5428 · `五、附录` @6112 · `2.文献检索策略` @4623 · `3.全面查找证据。根据所确定的检索策略` @824.

**Caution:** the register's own Q3 wording (`即灰色文献`, straight quotes) occurs **0** times in every form of this capture — the document writes `即“灰色文献”` (curly quotes); the same one-punctuation discrepancy round-48 recorded (`corpus/lessons/round-48.md:61`, `.ufo/waves/round-48/w2/QuarantineS125.md`).

## 6. What the next round would need

1. **Document ids.** Registry at HEAD `9caf8fc` holds 120 rows, max S120 (`git show 9caf8fc:corpus/SOURCES.md | grep -cE "^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|"` → 120); the round-54 C2 claim plans S121–S123 for the GB/T theme (a sibling seat's S121–S123 rows are already in the uncommitted worktree `corpus/SOURCES.md`, 123 rows), so the `.doc` would take **S124** and the S131 article **S125** if the L1 admits them. The S133 URL (`medsci.cn/…id=23e481c0052069d3`) is **the same URL as staged S111 and as lane S113** (`corpus/SOURCES.md:123`): no new row, no per-document credit; citing it needs the held-row pattern (`source: S113 — <url>`) plus a `used-by` update on S113.
2. **Quotes + a span builder that can slice the defined form.** The C2 machinery (`corpus/evidence/round54/build-spans.py:107-126`) reads the `.txt` sidecar and, for a non-zip `.raw`, falls back to **UTF-16LE** — for this `.doc` that is the 121,964-char decode with 887 U+FFFD, where the field sentence sits at **57497**, not 4678 (measured: `form_texts` → `.raw` form `quote@57497`). The next round must either teach `build-spans.py`/`c2-count.py` the candidate's OLE form or cite 57497 in the UTF-16LE form; entry offsets (4678) and span offsets (57497) must not be mixed.
3. **Province question** (for the L1; round-52's refusal was withdrawn in round-53:65): keep the spine as *the source states a required report field* (claim-vs-source verification, in province), do **not** assert the guideline is current (the `.doc` is undated), and do **not** import the staged third-document inference: S133's capture shows `paymentType=` empty, `opened=0`, `paymentAmount=10`, `haveAttachments=1` at 4051 — and `元` 0, `购买` 0, `付费` 0, `价格` 0 — so "sold for 10 yuan / the blocker is a price" is **not carried** by the text form (the lane already says so, `chinese-prisma-s-reception-r52.md:29`).
4. **Quarantine verdict line, if the `.doc` is ever bound.** The `.doc` URL's register row is `chousa | round6 | S125 | payload-absent` (`absent-defect-register.md:56`). Round-48 refuted it to **present** (byte evidence, `QuarantineS125.md`), but the lane carries that only as a table row (`round-48.md:61`), **not** in the canonical `register S125 (round 6) verdict: present` form that round-54 `c2-count.py:84`'s VERDICT_RE reads — checked: no S125 verdict match in round-48/51/52/53. (The C2 counter's own slice needs only S080/S088/S096, so this does not affect C2.) Slice count re-measured: 25 `| \`chousa\` |` lines, of which **24 data rows** (line 238 is the section-count row).

Candidate next-round quote rows (the L1 owns the id assignment and the entry name; ids/paths below are my proposal, offsets are in the **defined text form** of the `.doc`):

```
是否检索灰色文献等关键问题	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	是否检索灰色文献等关键问题	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
文献检索策略：检索途径、检索数据库、检索时限及检索式。应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	文献检索策略：检索途径、检索数据库、检索时限及检索式。应当说明是否有检索限制（如语言限制）、是否手工检索、是否检索灰色文献等关键问题。	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	查找时应当注意收集未公开发表的文献，即“灰色文献”，如会议论文、未发表的学位论文、产业报告、咨询报告等。	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
检索策略包括检索的数据库、检索范围（如主题等）、检索词、检索式（即检索词组合方式）和时间范围等，应当根据不同的研究目的制定。	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	检索策略包括检索的数据库、检索范围（如主题等）、检索词、检索式（即检索词组合方式）和时间范围等，应当根据不同的研究目的制定。	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
灰色文献中可能包含阴性研究结果	S124	http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc	灰色文献中可能包含阴性研究结果	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
五个方面	S125	http://m.cnpharm.com/201906/18/c280684.html	五个方面	corpus/knowledge/grey-literature-and-chinese-search-record-r40.md
```

## 7. Receipts

```
$ python3 corpus/evidence/round54/c1-count.py --per-leg 2 --seed 7 --work $S/c1work
GEN=PASS 2 docs / NONWORD=PASS 2 sheets / ENCRYPTED=PASS 2 docs / MALFORMED=PASS 2 docs
REAL=PASS 5 captures / REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']
LEGS=6/6   C1=PASS                                    # rc=0; independent re-run of the frozen counter
```

(S130 is one of the counter's five pinned REAL captures — `bdff491a75c6abeda1d9c01d`, sha256 `ac0fad62ed9a11fa3bd1…`, pinned quote `是否检索灰色文献` — and the candidate passes that leg.) The worktree `tools/capture-text.py` is concurrently modified by another seat (one added Prc-GrpPrl bounds check); re-checked against the **frozen candidate blob** (`git show 8a7d0f1:tools/capture-text.py`): rc=0, bytes=34234, stderr=0, text-form sha256 `f0b08997…` — byte-identical to the worktree tool's output — `--locate` again `LOCATED count=1 offset=4678`, and `c1-count.py --per-leg 2 --seed 7 --tool <blob>` → `LEGS=6/6 C1=PASS` (rc=0). Tooling: no install; system `soffice` 26.8.1.1 and `python3` 3.14.8 as found. Scratch `/fast/scratch/hyaku/chousa-r54/R54ExecS130Probe` removed at exit; no `soffice.bin` left.

VERDICT: attacked the round-53 S130 refusal with the new OLE text form — the text-form half of the flip now fires (defined form 13,718 chars/0 U+FFFD, LO oracle 248/248 held at ratio 0.9989, the field sentence located once at char 4678 where the sidecar has 0 and the UTF-16LE decode has it at 57497); the "regulator field on its own source" half remains the L1's call, and the next round needs S124/S125 plus a span builder that slices the defined form, not the UTF-16LE decode.
