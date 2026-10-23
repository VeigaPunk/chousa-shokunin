# ScoutCensus — round-30 pre-change SOURCES census (chousa lane)

Scope: frontier-step census of `corpus/SOURCES.md` before the round's SOURCES
changes. Read-only; no lane files mutated. All commands run 2026-10-23.

## 1. Maintained validator

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
EXIT=0
```

Verdict: `ok` — the maintained parser finds the registry well-formed.

## 2. Manual census (frozen contract v1 commands, CORPUS.md § 'SOURCES.md — where a shokunin learns')

Run from lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin` via
`/fast/scratch/hyaku/chousa-r30/w1/ScoutCensus/census.sh` (commands pasted
verbatim from CORPUS.md lines 135-147). Whole script `EXIT=0`.

```
### 1 rows
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
49

### 2 malformed (must print 0)
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0

### 3 tier histogram
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=43 B=1 C=5

### 4 status histogram
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=26 queued=19 rejected=4

### 5 duplicate ids (must print nothing)
$ awk -F'|' '...' corpus/SOURCES.md | sort | uniq -d
(no output)

### 6 enum violations + tier inflation (must print nothing)
$ awk -F'|' '...' corpus/SOURCES.md
(no output)

### 7 mined rows whose used-by paths do not exist (must print nothing)
$ awk -F'|' '...' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
```

## Baseline snapshot

| measure | value |
|---|---|
| rows | 49 |
| malformed rows | 0 |
| tiers | A=43 B=1 C=5 |
| status | mined=26 queued=19 rejected=4 |
| duplicate ids | none |
| enum violations / tier inflation | none |
| mined rows with missing used-by path | none |

Consistency check: 26 + 19 + 4 = 49 and 43 + 1 + 5 = 49 — both histograms
account for every row.

## Limits

- Read-only census; no `|`-in-cell, anchoring, or content-fidelity audit
  performed — only the contract's mechanical checks plus the maintained
  validator.
- First attempt in a nested quoting wrapper mangled the used-by awk regex
  (awk reported an unterminated regexp); re-ran all seven commands verbatim
  from a scratch script — outputs above are from the clean run.
- No network access used; no tools installed.
