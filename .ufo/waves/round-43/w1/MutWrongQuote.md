# MutWrongQuote — 20-byte wrong-quote probe (round 43, w1)

Seat: `MutWrongQuote` (leaf, mutation-tester). One probe. No lane edit, no network, no sibling write, no tool install.

Axes: operability (baseline detector runs), calibration (same membership check rejects a non-quote), depth (located sentence is in the committed Europe PMC capture, not in the stand-in).

## Claimed invariant and the one defect

Frozen C3 (`corpus/evidence/round43/claims.md`, predicate R43-C3) and `c3-count.py` line 62: the located quote is a substring of the Europe PMC capture. The quote constant is:

`to register the steps taken and to make searches accountable and reproducible`

Plausible defect: a 20-byte stand-in that does not contain that sentence would still satisfy the same membership check. That defect is the assigned mutant. The bound is not retuned. The contract is not changed.

Scratch is `/tmp/mutwrongquote-r43-w1.bin`, created for this probe. Lane production files and `/home/vgpnk/Projects/shokuknow` were not written. The capture was not copied and mutated; the tasking assigned the 20-byte file as the mutant.

## Identity

Lane HEAD (read-only `git rev-parse HEAD`):

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8
```

Matches the measured commit named in the wave context.

URL `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML` sha256 first 24 hex digits:

```
url-sha256-24: 2cef078d8f9f87802e19e770
quote-len-bytes: 77
quote-len-chars: 77
```

Capture path: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt`

## Mutant

Smallest assigned behavior-bearing stand-in: exactly 20 ASCII bytes, `WRONG-QUOTE-20BYTES!`. It cannot contain a 77-byte quote. Payload written by Python `Path.write_bytes`, not by editing the lane.

```
wrote: /tmp/mutwrongquote-r43-w1.bin
payload-repr: b'WRONG-QUOTE-20BYTES!'
```

```
20 /tmp/mutwrongquote-r43-w1.bin
552a60636832ef3174742e1c669ea63369f4840076db3e9d59ea75450043483d  /tmp/mutwrongquote-r43-w1.bin
 57 52 4f 4e 47 2d 51 55 4f 54 45 2d 32 30 42 59
 54 45 53 21
```

`cmp` against `printf 'WRONG-QUOTE-20BYTES!'` printed `MUTANT_BYTES_EXACT=1`.

## Expected detector

Same bounded check `c3-count.py` uses (`QUOTE in text`, UTF-8, `errors="replace"`), plus the raw-bytes form of that membership. Expected:

- pristine capture: quote present; `c3-count.py` prints `C3=PASS` and exits 0
- mutant file: quote absent
- restored production bytes: identical sha256 to the before hashes

A baseline failure would be inconclusive, not a kill. Baseline passed, so the mutant result is conclusive.

## Output (verbatim)

Before hashes:

```
833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt
138344af190a5827277c8df74049576043978a1471c2fd472aef8d8f31e2ed26  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c3-count.py
4d332357a083c21bd16cad4af4006161a73a2c66cf95433336d34cd39aed0bfe  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/search-log-method-r39.md
```

Baseline detector `python3 corpus/evidence/round43/c3-count.py`:

```
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
c3-exit:0
```

Pristine membership (quote present in the Europe PMC capture):

```
capture-bytes: 80107
QUOTE_IN_CAPTURE_TEXT: True
QUOTE_IN_CAPTURE_BYTES: True
text-offset: 17383
byte-offset: 17410
window: to register the steps taken and to make searches accountable and reproducible
```

Mutant membership (quote absent from the 20-byte file):

```
mutant-bytes: 20
QUOTE_IN_MUTANT_TEXT: False
QUOTE_IN_MUTANT_BYTES: False
ABSENT: True
```

Both assigned checks hold: absent from `/tmp/mutwrongquote-r43-w1.bin`, present in the Europe PMC capture.

## Verdict

**killed.**

The substring detector that C3 uses returns false on the 20-byte stand-in and true on the committed capture. A wrong quote of this shape does not survive. This is not permission to change the quote, the URL, or the 1/2 split bound.

Side measurement, not a second probe and not a C3 miss: the knowledge entry calls 17383 a byte offset. On this capture it is the Unicode character index. The file byte offset of the same sentence is 17410 (27 extra UTF-8 bytes in the prefix; 41 bytes ≥ 128). C3 does not score the offset. Recorded so the presence check is not misread as confirming the entry's "byte offset" wording.

```
char-offset: 17383
utf8-prefix-bytes: 17410
bytes-find: 17410
extra-utf8-bytes: 27
non-ascii-bytes-in-prefix: 41
prefix-equals-slice: True
entry-claimed-17383-is-char-index: True
entry-claimed-17383-is-byte-index: False
```

Capture sha256 matches the entry's claimed digest `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d` (`CLAIMED_DIGEST_MATCH: True`).

## Restoration evidence

Production bytes were never the scratch. After hashes equal the before hashes:

```
833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt
138344af190a5827277c8df74049576043978a1471c2fd472aef8d8f31e2ed26  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round43/c3-count.py
4d332357a083c21bd16cad4af4006161a73a2c66cf95433336d34cd39aed0bfe  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/search-log-method-r39.md
```

`git diff --stat` on `c3-count.py`, `search-log-method-r39.md`, `SOURCES.md`, and `claims.md` was empty (`diff-exit:0`). `git status --porcelain` on those paths plus `absent-split.tsv` was empty (`status-exit:0`). The `/tmp` mutant is retained as the probe artifact; it is not a lane file and was not restored over production bytes because production bytes were not changed.

Tool installs: none. Pacman not invoked. No fetch.

Report: .ufo/waves/round-43/w1/MutWrongQuote.md
