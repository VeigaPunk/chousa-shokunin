# CritColumnSpan — contiguous "should be reported in Column 2" is absent

Seat: critic. Axes: operability, calibration, depth.
Measured commit named by the dispatcher: `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`.
Attacked approach: the round-43 rejection of `search-tracking-record-r40.md` (`corpus/lessons/round-43.md`, Gate / Rejected). That rejection says `"should be reported in Column 2" is not a contiguous span in the committed pdftotext capture, so the column claim cannot be re-grounded`, and sets the flip to `a rendering in which that sentence is contiguous`. Bound not retuned. No fetch. No lane production file edited.

Assigned search result: **absent**.

## Axes

- operability: the capture must be the campaign `.qcache` file named by sha256 of the URL, first 24 hex, and the search must be a local read.
- calibration: whole-file contiguity (the gate this rejection uses, and the same NFKC + whitespace collapse R43-SPLIT uses) must not be confused with a column-order read, and must not be scored as an R43-SPLIT ratio.
- depth: a miss of whole-file contiguity must name the bytes and the capture form. It must not be upgraded into "the capture cannot ground the sentence" or into a fetch.

## Counterexample

The strongest local counterexample is not a second file. It is the same capture, read in column order.

Whole-file, the sentence is absent: line 78, a left-column line, sits between the two halves. After NFKC and whitespace collapse the gap is still words (`matching inclusion criteria, not necessarily all the records`), not whitespace. That part of the rejection holds.

The inference does not. Lines 77 and 79 are the right column of that same page (leading indent 71). Joining those two lines with one space yields a contiguous `should be reported in Column 2`. No new rendering and no fetch are required to recover the sentence from this capture. The flip that demands another rendering treats a row-major interleave as if the words were missing.

A second, weaker counterexample, which must not be used as a ratio: the longest substring of the quote that occurs anywhere in the whitespace-collapsed file is ` be reported in Column ` (23/30). That hit is a different sentence, `can be reported in Column 1`, not this break. Scoring this quote 23/30 under R43-SPLIT would be false provenance.

## Evidence

No network. Capture path is the campaign cache named by the URL hash. Identity inside the file: line 2 is `DOI: dx.doi.org/10.5195/jmla.2022.1449`; lines 7–9 are `PRISMA 2020 and PRISMA-S: common questions on` / `tracking records and the flow diagram` / `Melissa L. Rethlefsen, AHIP; Matthew J. Page`. A form-feed is present, which matches an extracted-PDF text, the form the lesson calls pdftotext. The staged entry cites this URL as `source: S131`. This seat did not adopt S131 and did not run shokuknow tools.

Command (local python3, run):

```
python3 - << 'PY'
from pathlib import Path
import hashlib, re, unicodedata
url = "https://jmla.pitt.edu/ojs/jmla/article/download/1449/2061"
digest = hashlib.sha256(url.encode()).hexdigest()
prefix = digest[:24]
p = Path("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache") / f"{prefix}.txt"
raw = p.read_text(encoding="utf-8")
needle = "should be reported in Column 2"
collapsed = re.sub(r"\s+", " ", unicodedata.normalize("NFKC", raw))
print(f"URL_SHA256={digest}")
print(f"PREFIX={prefix}")
print(f"PATH={p}")
print(f"EXISTS={p.is_file()}")
print(f"BYTES={p.stat().st_size}")
print(f"CHARS={len(raw)}")
print(f"EXACT={needle in raw}")
print(f"NFKC_WS={needle in collapsed}")
right = []
for n, line in enumerate(raw.splitlines()):
    if line.strip() and (len(line) - len(line.lstrip(" "))) >= 60:
        right.append((n, line.strip()))
joined = " ".join(s for _, s in right)
print(f"RIGHT_COLUMN_JOIN={needle in joined}")
lines = raw.splitlines()
for n in (77, 78, 79):
    print(f"LINE_{n}={lines[n]!r}")
i = joined.find(needle)
print(f"JOIN_SPAN={joined[i-90:i+len(needle)+1]!r}")
for label, s in (
    ("STRATEGIES", "the recommendation to report search strategies for all databases, registries, and websites that were searched"),
    ("COUNT", "PRISMA-S also recommends reporting the number of records identified from each information source"),
    ("COLUMN1", "also suggests reporting an overall number for records identified from databases and registers in Column 1"),
):
    print(f"{label}_EXACT={s in raw}")
    print(f"{label}_NFKC_WS={s in collapsed}")
    print(f"{label}_RIGHT={s in joined}")
print(f"DOI={'10.5195/jmla.2022.1449' in raw}")
print(f"FORMFEED={chr(12) in raw}")
print(f"FILE_SHA256={hashlib.sha256(p.read_bytes()).hexdigest()}")
PY
```

Stdout, verbatim:

```
URL_SHA256=0ae65ac01b93119d3c2f3fed266b0d1cddd8bfbbc16c1b5a172fb1ba5fc8595a
PREFIX=0ae65ac01b93119d3c2f3fed
PATH=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/0ae65ac01b93119d3c2f3fed.txt
EXISTS=True
BYTES=27737
CHARS=27659
EXACT=False
NFKC_WS=False
RIGHT_COLUMN_JOIN=True
LINE_77='                                                                       citation searching, and other methods should be reported'
LINE_78='matching inclusion criteria, not necessarily all the records'
LINE_79='                                                                       in Column 2. The flow diagram template also suggests'
JOIN_SPAN='at records identified from websites, organizations, citation searching, and other methods should be reported in Column 2.'
STRATEGIES_EXACT=False
STRATEGIES_NFKC_WS=True
STRATEGIES_RIGHT=False
COUNT_EXACT=False
COUNT_NFKC_WS=True
COUNT_RIGHT=False
COLUMN1_EXACT=False
COLUMN1_NFKC_WS=False
COLUMN1_RIGHT=True
DOI=True
FORMFEED=True
FILE_SHA256=1e185358c52c3c8ba90970dd79a624df1e532841aa0a9ccb7be738236be9971d
```

Exit code: 0.

`RIGHT_COLUMN_JOIN` is an analyst reconstruction (non-empty lines whose first non-space is at column >= 60), not a lane rule. It is enough to show the sentence is in the right column of this file. It is not enough to locate a quote under the frozen whole-file gate. Later pages of this same file put both columns on lead-0 lines, so lead >= 60 is not a general reader of the article. The smaller claim does not need that threshold: line 77 plus a space plus the stripped line 79 already contains the sentence, and line 78 is the interloper.

The two sentences the lesson calls contiguous are the abstract pair. They fail an exact substring test (they break on newlines) and pass NFKC + whitespace collapse (`STRATEGIES_NFKC_WS=True`, `COUNT_NFKC_WS=True`). They are not in the right-column join. That is consistent. The paired Column 1 sentence in the same right-column paragraph fails the same whole-file test (`COLUMN1_NFKC_WS=False`) and passes the same join (`COLUMN1_RIGHT=True`). The miss is the two-column interleave, not the token `Column 2`.

Cross-match, from a separate local search of the whitespace-collapsed file, not from the block above:

```
' be reported in Column ' count=1
  8732 'sary to do so; users are diagram and can be reported in Column 1. If Google free to modify the PRISMA 2'
'should be reported in Column 2' count=0
```

## Impacted axes

- operability: the assigned search is operable. The file exists at the URL-hash name, the exact span is absent, and the check did not fetch. The rejection's flip is not operable under the open no-fetch ruling (L0 `8d77e6c1`, `corpus/evidence/round43/claims.md` "Not claimed"): it asks for a new rendering when the bytes are already local. That is a stall, not a C1 miss. C1 does not read this capture.
- calibration: the whole-file premise is calibrated to the abstract sentences and to C3's substring gate. The flip is not. It equates "not a whitespace-collapsed span of the whole file" with "absent until a new rendering". Do not retune the 1/2 bound to absorb this row. This quote is not a round-42 absent id. Do not import the 23/30 cross-match as its R43-SPLIT ratio. `lead >= 60` must not become a second location authority beside the frozen substring gate.
- depth: QUALITY 59 says a refusal must name the committed bytes and their form, and a wrong form is unverifiable, not a fabrication. The lesson names the capture as pdftotext and does not name lines 77–79. The column claim is unverifiable under the whole-file gate. It is not unrecovered from this file, and it is not a fabrication. C3 (S078, Europe PMC) is a different capture and is not touched.

Not an identity swap: the filename is sha256 of the assigned URL, first 24 hex, and the DOI in the file is `10.5195/jmla.2022.1449`. Not a duplicate admission: this seat does not admit `search-tracking-record-r40.md`.

Tradeoff the L1 per-axis verdicts must not reject as a depth miss of C3, and must not "fix" by admitting the entry: keeping the whole-file substring gate, and leaving this row unadmitted, does not harm C1, C2, or C3. The defect is the wording of the flip, not the non-admission.

## Smallest safe correction

Do not edit the capture, the counters, the split table, or the 1/2 bound. Do not admit the entry on a column join.

In the rejection sentence only: replace "cannot be re-grounded" and "Flip: a rendering in which that sentence is contiguous" with the bytes. The sentence is absent as a contiguous span of `0ae65ac01b93119d3c2f3fed.txt` (exact and after NFKC + whitespace collapse). Line 78 is the left-column interloper. Line 77 and line 79, joined, contain it. Under the frozen substring gate the row stays unverifiable (QUALITY 59). The flip is a column-order read of this capture, or a later ruling that adopts that read. It is not a fetch.

## Verdict

Contiguous sentence `should be reported in Column 2` in the campaign capture: **absent**.

The rejection's factual premise holds. Its inference that the column claim cannot be re-grounded without a new rendering does not.

Report: .ufo/waves/round-43/w1/CritColumnSpan.md
