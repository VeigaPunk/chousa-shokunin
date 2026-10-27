# Round 55 W1 — R55ExecCollision

## Scope and result

Independently re-derived the section-10 collision scratch in private scratch and rechecked the staged-id renumber map by document. No lane/campaign files were modified; no tools installed.

## Collision derivation

Source commands: `/home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-55.md:530-577` (0–3-space extraction, `comm -12`, and awk quarantine slice). Ran them with outputs redirected to `/fast/scratch/hyaku/chousa-r55/R55ExecCollision/assim/`, not the lane's evidence directory:

```sh
L=/home/vgpnk/Projects/shokunin/chousa-shokunin
P=/home/vgpnk/Projects/shokuknow/merge/chousa
R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
A=/fast/scratch/hyaku/chousa-r55/R55ExecCollision/assim
mkdir -p "$A"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$L/corpus/SOURCES.md" | grep -oE 'S[0-9]+' | sort > "$A/reg-ids"
grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$P/SOURCES.append.md" | grep -oE 'S[0-9]+' | sort > "$A/staged-ids"
comm -12 "$A/reg-ids" "$A/staged-ids" > "$A/collisions"
awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > "$A/quarantine-slice"
```

Observed counts and byte-comparison output:

```text
reg=123 staged=114 coll=42 quar=24
reg-ids          IDENTICAL
staged-ids       IDENTICAL
collisions       IDENTICAL
quarantine-slice IDENTICAL
```

Thus all four independently produced files matched `.ufo/waves/round-55/assimilation/{reg-ids,staged-ids,collisions,quarantine-slice}` byte-for-byte. The lists have 123 registry ids, 114 staged ids, 42 collisions (S082–S123), and 24 quarantine rows.

## Guard fixture

Re-ran the same 0–3-space and column-zero extractors on a scratch registry containing `  | S002 | x |` and staged row `| S002 | z |`:

```text
reg rows (0-3sp) = S002 S003
staged (0-3sp)   = S002
collisions 0-3sp = [S002 ]
collisions col-0 = []
```

This reproduces the indented-row collision and demonstrates why a column-zero-only extractor misses it.

## Renumber map by document

Staged URLs below were read from `merge/chousa/SOURCES.append.md` rows 55, 56, 58, and 68 (ids S130, S131, S133, S143). Compared to the first source-cell URL for each lane row using the census normalisation; the census implementation is `scripts/sources-census.sh:600-605` (`url_of`: drop fragment/trailing slash/scheme and lowercase host). Independently computed results:

```text
S130  http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc  NEW
S131  http://m.cnpharm.com/201906/18/c280684.html                    NEW
S133  https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3  S113
S143  https://english.nmpa.gov.cn/2019-07/18/c_388252.htm           NEW
LANE_ROWS 123  TAIL_IDS S121 S122 S123
```

S133's URL is already lane row S113 (`corpus/SOURCES.md:123`); the other three URLs are not present in the lane registry. The last three registry ids are S121–S123, so the next free ids are S124–S126. By document, the staged guideline S130 maps to new S124, the 中国食品药品网 report S131 to new S125, staged English notice S143 to new S126, and the existing 梅斯医学 document S133 remains held/cited as S113. These observed URL matches support the frozen prompt's map; they do not assess source quality or alter any C1/C2/C3 predicate.

## Limits

No C1/C2/C3 counter was run; no source was fetched. No lane, fleet, or campaign file was written. Scratch artifacts were removed before completion.

VERDICT: section-10 collision derivation and document-level renumber map reproduced; guard catches indented collision S002.