# SimpFilename — `search-log-method-r39.md` vs lane round 39

Seat: SimpFilename (simplifier, leaf). Measured commit `737f40b6aa8f37ffe2269db370fd6d65a720d9a8`. No production file renamed or deleted. No fetch. No descendant. Bound not retuned.

## Verdict

YES. `corpus/knowledge/search-log-method-r39.md` can be mistaken for a lane round-39 knowledge note.

NO. `corpus/lessons/round-43.md` does not disclose that mistake. Its one filename sentence is "The filename is the package's label." It never says the name can be mistaken for lane round 39, and it never says "not a lane round number."

## Axes

- Operability: the admitted path is a C3 input and an S078 `used-by` cell. A rename or deletion fails that contract. Not done.
- Calibration: "can be mistaken" is a directory-convention fact, not a claim that the file's body is a round-39 note. "Lesson discloses it" means the lesson names the collision, not that it mentions the path.
- Depth: the suffix is the package's path label, not lane round 39 and not the package's own round index. Stop before a second name.

## Deletion candidate

Candidate: the `-r39` suffix, as a stale name beside the lane's round-39 notes.

Not deleted. References search found semantic callers, so the no-caller proof fails. The next deletion (rename or remove) harms operability. A stub at the old path would be a second convention. Stop.

## Preserved contract

Path remains `corpus/knowledge/search-log-method-r39.md`. C3 still requires that string in the entry path and in the S078 row (`corpus/evidence/round43/c3-count.py` lines 25 and 57). This seat did not edit the entry, the lesson, `SOURCES.md`, or the counter.

## Evidence

Command, lane root, exit 0:

```
ls -1 corpus/knowledge/*-r39.md; echo '---LESSON---'; rg -n -e 'filename' -e 'package' -e 'lane round' -e 'round 39' corpus/lessons/round-43.md; echo "LESSON_RG_EXIT:$?"; echo '---ENTRY---'; rg -n -e 'filename' -e 'lane round' corpus/knowledge/search-log-method-r39.md; echo "ENTRY_RG_EXIT:$?"; echo '---README---'; rg -n 'search-log-method-r39' corpus/README.md || echo 'README_NO_HIT'; echo '---CALLERS---'; rg -n -l 'search-log-method-r39' --glob '!/.ufo/**' --glob '!**/.ufo/**' . || true; echo '---GIT---'; git log -1 --format='%H %ci %s' -- corpus/knowledge/search-log-method-r39.md; echo '---ROUND39-TREE---'; git ls-tree -r --name-only 6ac1007e6a5d699d0742801026554fac1d900b5d -- corpus/knowledge | rg 'r39' || true
```

Stdout, verbatim:

```
corpus/knowledge/capture-bash-pin-r39.md
corpus/knowledge/receipt-verifier-subject-r39.md
corpus/knowledge/search-log-method-r39.md
---LESSON---
33:`corpus/knowledge/search-log-method-r39.md`, citing S078. The filename is the package's label. The source is the Europe PMC full-text XML of Bramer et al. 2018, opened from the committed capture, not fetched.
45:- The rest of the package. Reason: one theme, and only the rows an admitted entry cites are appended. Flip: a later round re-grounds another theme from local captures, or the fetch ruling opens the rest.
LESSON_RG_EXIT:0
---ENTRY---
6:ground: the lane held no opened source for how a search log is kept. `verify-sweeps` re-runs a location set. It does not keep a log document, and it does not check recall against included references. This entry is that missing half. The filename is the package's label, not a lane round number.
ENTRY_RG_EXIT:0
---README---
README_NO_HIT
---CALLERS---
./LOG.md
./corpus/SOURCES.md
./corpus/evidence/round43/c3-count.py
./corpus/evidence/round43/claims.md
./corpus/lessons/round-43.md
---GIT---
737f40b6aa8f37ffe2269db370fd6d65a720d9a8 2026-10-24 21:15:02 -0300 round-43: split the absent class and adopt one locally re-opened search-log entry
---ROUND39-TREE---
corpus/knowledge/capture-bash-pin-r39.md
corpus/knowledge/receipt-verifier-subject-r39.md
```

Phrase counts, same tree, exit 0:

```
python3 - <<'PY'
from pathlib import Path
lesson = Path('corpus/lessons/round-43.md').read_text()
entry = Path('corpus/knowledge/search-log-method-r39.md').read_text()
needles = [
    'not a lane round number',
    'mistaken',
    'lane round 39',
    'round 39',
    "package's label",
    'filename',
]
for name, text in (('lesson', lesson), ('entry', entry)):
    print(name)
    for n in needles:
        print(f'  {n!r}: {text.count(n)}')
PY
```

```
lesson
  'not a lane round number': 0
  'mistaken': 0
  'lane round 39': 0
  'round 39': 0
  "package's label": 1
  'filename': 1
entry
  'not a lane round number': 1
  'mistaken': 0
  'lane round 39': 0
  'round 39': 0
  "package's label": 1
  'filename': 1
```

Why the filename can be mistaken for lane round 39:

- Lane index convention is suffix = admitting round. `corpus/README.md` lines 1057–1058 label `capture-bash-pin-r39.md` and `receipt-verifier-subject-r39.md` "Round-39 note". `search-log-method-r39.md` is absent from that index (`README_NO_HIT`), so the index does not relabel it as round 43.
- `corpus/lessons/round-39.md` lines 65–67 admit only those two files. The round-39 tree `6ac1007e6a5d699d0742801026554fac1d900b5d` contains only those two `*r39.md` notes. Full history is one commit, the round-43 add above. Command: `git log --format='%H %ci %s' -- corpus/knowledge/search-log-method-r39.md; echo '---NAME-STATUS---'; git log --diff-filter=A --format='%H %s' -- corpus/knowledge/search-log-method-r39.md`. Stdout:

```
737f40b6aa8f37ffe2269db370fd6d65a720d9a8 2026-10-24 21:15:02 -0300 round-43: split the absent class and adopt one locally re-opened search-log entry
---NAME-STATUS---
737f40b6aa8f37ffe2269db370fd6d65a720d9a8 round-43: split the absent class and adopt one locally re-opened search-log entry
```
- A glob of `corpus/knowledge/*-r39.md` therefore lists the admitted round-43 entry between the two round-39 notes.

What the lesson discloses, and what it does not:

- Discloses: the path, the S078 citation, and "The filename is the package's label" (`corpus/lessons/round-43.md` line 33). Lesson line 45 is about rejecting the rest of the package, not about the suffix.
- Does not disclose: mistakability, "lane round 39", "round 39", or "not a lane round number" (counts above, all 0 in the lesson).
- The negation is in the entry's `ground:` line, not in the lesson. The entry also never says "mistaken" or "lane round 39". A reader who does not open the entry gets no negation.
- `LOG.md` line 1551 and `corpus/evidence/round43/claims.md` line 78 name the path and do not contain "package's label" or "not a lane round number".

Package label, read-only, not a lane round and not package-round 39. No shokuknow tool was run.

- `/home/vgpnk/Projects/shokuknow/lanes/chousa/round4/KNOWLEDGE-PROPOSED.md` line 1 is "ROUND 4". Line 275 is the heading `## corpus/knowledge/search-log-method-r39.md`. Its `ground:` line does not say the filename is not a lane round number.
- `/home/vgpnk/Projects/shokuknow/merge/chousa/MERGE-REPORT.md` line 35: path `corpus/knowledge/search-log-method-r39.md`, kind `amendment`, round column `round4`. Sibling round-4 paths in that table also end in `-r39.md` (`chinese-search-record-r39.md`, `evidence-pool-versioning-r39.md`, `istic-citation-verification-r39.md`). The suffix is a package filename label. It is not the package round index, and it is not lane round 39.
- A content search of `/home/vgpnk/Projects/shokuknow` for `not a lane round` and `package's label` did not hit the chousa package files. Those two sentences are lane text.

Narrow check that the retained path still scores, exit 0:

```
python3 corpus/evidence/round43/c3-count.py; echo EXIT:$?
```

```
ENTRY_CITES=1/1
QUOTE_LOCATED=1/1
URL_MATCH=1/1
C3=PASS
EXIT:0
```

## Tradeoff

Keeping the package path preserves C3, the S078 used-by cell, and the package's path identity. Cost: the suffix still sorts with lane round 39, and the lesson does not say so. The entry's ground line closes the negation only for a reader who opens the file. Renaming would improve the name axis and harm operability. Not done.
