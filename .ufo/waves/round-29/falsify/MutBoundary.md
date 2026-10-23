# MutBoundary — non-alphanumeric boundary removal

**Verdict: HOLDS for this probe; mutant KILLED.** The pristine baseline scored `130/130`, the plain-substring mutant scored `126/130`, and the byte-restored tool scored `130/130`. This probe does not falsify C1.

## Scope and axes

- Axes: operability, detector sensitivity to token-boundary false positives, exact restoration/isolation.
- Scratch checkout: `/fast/scratch/hyaku/chousa-r29/w2/MutBoundary/`.
- Tested revision: `30c9d24da1815e01e161ed2f52d5f951005cc2b8`, branch `master`.
- One mutant, only in the scratch copy's `tools/quote-reopen.py`. No lane production file, frozen claim, counter, fixture, Git index or jj state was edited.
- The clone initially inherited `master` at `b18b3ec9d8a01f966dd81991615bac27df6d66a1`; it was explicitly pinned to the assigned landed revision before any detector run.
- No tools were installed or updated; no subagents or background jobs were started.

Setup commands, each exit `0`:

```sh
timeout 60 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-hardlinks /home/vgpnk/Projects/shokunin/chousa-shokunin /fast/scratch/hyaku/chousa-r29/w2/MutBoundary
# From the scratch root:
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout master
timeout 30 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git checkout -B master 30c9d24da1815e01e161ed2f52d5f951005cc2b8
timeout 10 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git rev-parse HEAD
```

The final command printed `30c9d24da1815e01e161ed2f52d5f951005cc2b8`.

## Mutant and expected detector

Replace the boundary-aware occurrence search with `return q in text`, retaining normalization and the existing empty-quote rejection. The frozen `absent-truncated-token` class should kill this mutant: a quote cut inside a word is a substring but not a boundary-valid quote.

Actual scratch diff, recorded before restoration:

```diff
diff --git i/tools/quote-reopen.py w/tools/quote-reopen.py
index be0ce00..7877ed6 100755
--- i/tools/quote-reopen.py
+++ w/tools/quote-reopen.py
@@ -114,15 +114,7 @@ def found(text, quote):
     q = norm(quote)
     if not q:
         return False
-    i = 0
-    while True:
-        i = text.find(q, i)
-        if i < 0:
-            return False
-        j = i + len(q)
-        if (i == 0 or not text[i - 1].isalnum()) and (j == len(text) or not text[j].isalnum()):
-            return True
-        i += 1
+    return q in text
 
 
 def registry_rows(path):
```

## Behavioral runs

All three runs used the same frozen detector, from the scratch root, with no seed argument or substituted data. `TMPDIR` pointed to the scratch checkout's `tmp/`, and `PYTHONDONTWRITEBYTECODE=1`. Each command ran in a foreground process group, with process-group cleanup in `finally` after completion.

The requested `900` second outer timeout was reduced to `590` seconds, with a `5` second kill grace, to obey the seat's overriding command bound of at most `600` seconds. No run approached that bound. No counter code or timeout default was edited.

Actual commands:

```sh
timeout --signal=TERM --kill-after=5s 590 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutBoundary/receipt-baseline.json -- python3 tools/quote-reopen.py verify
timeout --signal=TERM --kill-after=5s 590 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutBoundary/receipt-mutant.json -- python3 tools/quote-reopen.py verify
timeout --signal=TERM --kill-after=5s 590 python3 corpus/evidence/round29/c1-count.py --receipt /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-29/falsify/MutBoundary/receipt-pristine.json -- python3 tools/quote-reopen.py verify
```

| Run | Counter exit | Predicate output | Seed | Whole-command wall seconds |
|---|---:|---|---:|---:|
| Pristine baseline, before mutation | 0 | `QUOTE_REOPEN_MATCH=130/130` | 9595924333916806303 | 6.60 |
| Mutant | 1 | `QUOTE_REOPEN_MATCH=126/130` | 10518428725690538552 | 6.72 |
| Restored pristine | 0 | `QUOTE_REOPEN_MATCH=130/130` | 216996839947068682 | 6.65 |

Baseline output had every class fully matched, including `class absent-truncated-token 4/4`, followed by:

```text
seed=9595924333916806303 tool_exit=1 wall_s=2.2
QUOTE_REOPEN_MATCH=130/130
```

### Mutant stdout, complete

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 0/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=10518428725690538552 tool_exit=1 wall_s=2.25
QUOTE_REOPEN_MATCH=126/130
```

### Restored pristine stdout, complete

```text
class absent-cross-attributed 4/4
class absent-fabricated 4/4
class absent-one-word-edit 4/4
class absent-spliced 4/4
class absent-truncated-token 4/4
class no-source-own-work-row 2/2
class no-source-unregistered-id 1/1
class runtime-crossattr 14/14
class runtime-page-transpose 24/24
class runtime-page-window 24/24
class runtime-subspan 14/14
class runtime-transpose 14/14
class too-long-true-text 3/3
class verbatim-inline-markup 9/9
class verbatim-plain 3/3
class verbatim-typographic-apostrophe 2/2
seed=216996839947068682 tool_exit=1 wall_s=2.26
QUOTE_REOPEN_MATCH=130/130
```

Counter stderr was empty in all three runs. The candidate's `tool_exit=1` is distinct from the counter's exit: the fixture intentionally contains non-VERBATIM items, while the counter checks agreement with their labels. Both pristine receipts have `predicate_holds: true` and no mismatches.

### Exact mutant misses

All four misses were frozen `absent-truncated-token` cases, labeled `ABSENT` but returned as `VERBATIM`; every other class matched completely.

| Frozen origin | Source | Quote |
|---|---|---|
| `ad795e73` | S044 | `Return the longest common sub-path of each pathname in the iterable pat` |
| `98406fc4` | S013 | `Like the JSON standard a byte order mark (U+FEFF) must NOT be incl` |
| `f98e78ae` | S020 | `he OWL encoding of the PROV Ontology is available here.` |
| `4798287c` | S008 | `This is best done by clearly framing the questions the review seeks to ans` |

The fixture class needed to kill this defect already exists and detected it; no fixture or contract change is proposed.

## Restoration evidence

The original search body was restored before the final detector run. `timeout 10 cmp -s tools/quote-reopen.py /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/quote-reopen.py` exited `0` both before and after that run. `sha256sum` recorded:

| Tool bytes | SHA-256 |
|---|---|
| Scratch pristine, before mutation | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Scratch mutant | `d8aa6aa38a33b86109ae92e37e3ba6bfac51834c842f20ad484e711b11297102` |
| Scratch restored, before and after final run | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |
| Lane tool, before and after probe | `72a3ad479c8eabf7b26a21c44742a6a30e9b0f8a2a2b5e07477866ca18754fea` |

Scratch frozen-input hashes were identical before and after:

```text
cd50965032278c355f780d357c5672f14840fc218bb1b7dc4adaa6993b5c175d  corpus/evidence/round29/c1-count.py
19ea5fbe2d52e42eff8c96096f543b818c37cf773fdfd22af6011fbf1cf47cfc  corpus/evidence/round29/claims.md
e6305beba9563fe4d37430019831610ddf7a5adf1e35de60869e3b764f939bcc  corpus/fixtures/quote-reopen-r29/items.tsv
dda1b3768f6f187736a77e5bce094b41822d8574e4798886d00964267343c7a9  corpus/fixtures/quote-reopen-r29/labels.tsv
d8aa0454b50bbe229f255885c970660540f8ecf5bac633ec136165b3425819be  corpus/SOURCES.md
```

Receipts, with SHA-256:

- [Pristine baseline](MutBoundary/receipt-baseline.json): `91cfee36d905b032d2a945216df80f87601f9d65ea84cde764694a1ffc5543eb`.
- [Mutant](MutBoundary/receipt-mutant.json): `267867dc3636a8d0d0d81e52d5f3fc99504ff061633bee91bcdd36d504be0375`.
- [Restored pristine](MutBoundary/receipt-pristine.json): `899588e9de2b8bd9d525a0841aca1cb8bfd5384dba00855a9c2e149ad3e53a44`.

## Limits

This is one assigned mutation probe with fresh randomized live-page samples on each run, not a proof of all tool behavior or future source stability. Baseline and restored runs passed, so the observed mutant failure is not a baseline-failure artifact. The exact four misses belong to a fixed boundary-specific class. No broader judgment, integration, repair, or contract rescaling was performed.
