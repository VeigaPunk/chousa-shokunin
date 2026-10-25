# ExecRecountTrain — independent recount of the AVeriTeC train.json capture

Seat: `L1Chousa45.ExecRecountTrain` (executor, leaf). Item: independently
recount the train.json capture with own code (no import/copy of
`corpus/evidence/round45/c3-count.py`).

## Capture (read-only, on-disk)

- File: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt`
- `sha256sum` (verbatim): `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`
- `wc -c`: `10184813` bytes — both match the frozen construction-check values in
  `corpus/evidence/round45/claims.md` (lines 119-123).

## Emptiness rule (stated)

A value is **empty** iff it is `None`, or a string that is `""` or
whitespace-only (`value.strip() == ""`). Any other value (incl. any non-empty
string) is **non-empty**.

## Script (own code; not derived from c3-count.py)

Written to `/tmp/chousa-r45-ExecRecountTrain/recount_train.py`; pasted below.

```python
#!/usr/bin/env python3
"""Independent recount of the AVeriTeC train.json capture (round 45, wave 1)."""
import json, collections

CAP = "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/974299ae4b5f3bdb808b36a9.txt"
SRC_KEY = "cached_source_url"
CLAIM_KEY = "cached_original_claim_url"

def is_empty(v):
    if v is None:
        return True
    if isinstance(v, str):
        return v == "" or v.strip() == ""
    return False

train = json.load(open(CAP, encoding="utf-8"))
assert isinstance(train, list)

rec_count = len(train)
ans_total = ans_carry = ans_carry_nonempty = ans_carry_empty = ans_missing_key = 0
src_val_types = collections.Counter()
rec_carry_claim = rec_carry_claim_nonempty = rec_carry_claim_empty = rec_missing_claim_key = 0
claim_val_types = collections.Counter()
questions_total = 0

for r in train:
    if CLAIM_KEY in r:
        rec_carry_claim += 1
        v = r[CLAIM_KEY]
        claim_val_types[type(v).__name__] += 1
        if is_empty(v): rec_carry_claim_empty += 1
        else: rec_carry_claim_nonempty += 1
    else:
        rec_missing_claim_key += 1
    questions_total += len(r.get("questions", []))
    for q in r.get("questions", []):
        for a in q.get("answers", []):
            ans_total += 1
            if SRC_KEY in a:
                ans_carry += 1
                v = a[SRC_KEY]
                src_val_types[type(v).__name__] += 1
                if is_empty(v): ans_carry_empty += 1
                else: ans_carry_nonempty += 1
            else:
                ans_missing_key += 1

print(f"records_total={rec_count}")
print(f"questions_total={questions_total}")
print(f"answer_objects_total={ans_total}")
print(f"answers_carrying_{SRC_KEY}={ans_carry}")
print(f"  non_empty={ans_carry_nonempty}")
print(f"  empty={ans_carry_empty}")
print(f"answers_lacking_{SRC_KEY}_entirely={ans_missing_key}")
print(f"cached_source_url_value_types={dict(src_val_types)}")
print(f"records_carrying_{CLAIM_KEY}={rec_carry_claim}")
print(f"  non_empty={rec_carry_claim_nonempty}")
print(f"  empty={rec_carry_claim_empty}")
print(f"records_lacking_{CLAIM_KEY}_entirely={rec_missing_claim_key}")
print(f"cached_original_claim_url_value_types={dict(claim_val_types)}")
```

## Output (verbatim)

```
records_total=3068
questions_total=7985
answer_objects_total=8479
answers_carrying_cached_source_url=6511
  non_empty=6510
  empty=1
answers_lacking_cached_source_url_entirely=1968
cached_source_url_value_types={'str': 6511}
records_carrying_cached_original_claim_url=2531
  non_empty=1145
  empty=1386
records_lacking_cached_original_claim_url_entirely=537
cached_original_claim_url_value_types={'NoneType': 1343, 'str': 1188}
```

## Empty-value characterization (follow-up probe, same session)

```python
# summary:
empty_claim_breakdown: {'None': 1343, 'empty_str': 43, 'white_str': 0}
empty_src_examples: [(1175, "''")] count= 1
```

- The single **empty** `cached_source_url`: record index 1175, value `''`
  (empty string), i.e. 6510 non-empty / 1 empty.
- `cached_original_claim_url` empties: 1343 × `None` + 43 × `''` = 1386 empty
  (0 whitespace-only); 1145 non-empty. All 2531 carrying records are either
  `None` or `str`; no other types.

## Verdict

Independent recount **exactly reproduces** the frozen construction-check figures
(`claims.md` lines 119-123): records 3068; answers carrying `cached_source_url`
6511 (6510 non-empty / 1 empty); records carrying `cached_original_claim_url`
2531 (1145 non-empty / 1386 empty); sha256
`ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`.
No answer object in the file is missing `cached_source_url` in a way that
contradicts the count (1968 answers lack the key entirely — answers with no
archive link at all, consistent with 6511-of-8479 carrying). 537 records lack
`cached_original_claim_url` entirely (3068 − 2531). C3 counts re-derived from
the capture are **consistent**.

## Resolvable pointers

- Capture sha256: `ae5eda7c42ddf1695ef185a7ba1bc716928f5adf57103e4f78aae5f9afe00f9c`
- Empty `cached_source_url` value: record index 1175 (record 1176, 1-based),
  first question, first answer, `cached_source_url == ""`.
- Empty-string `cached_original_claim_url` records (43): e.g. indices 292, 333,
  418 (0-based) have `''`; the rest are `None`.
- Script: `/tmp/chousa-r45-ExecRecountTrain/recount_train.py` (deleted at
  finish per seat contract).

## Risks / blockers

None. No fetch performed; capture read from disk only. No production files
touched.
