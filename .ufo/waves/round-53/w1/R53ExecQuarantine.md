# R53ExecQuarantine — round-53 W1, quarantine slice

Leaf seat: no subagents, no installs (nothing needed — no pacman/uv/npx call). Lane repo `/home/vgpnk/Projects/shokunin/chousa-shokunin`;
register read-only at `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (`$R`);
scratch `/fast/scratch/hyaku/chousa-r53/R53ExecQuarantine` (`TMPDIR` there), removed at the end, every receipt inlined.

## 1. The slice — 24 rows, every one carrying an S-id

```
$ awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" | wc -l
24
$ grep '| `chousa` |' "$R" | wc -l                        # 25 prefixed lines: 24 rows + the By-lane summary
25
$ grep '| `chousa` |' "$R" | awk -F'|' '$4 !~ /S[0-9]+/ {print}'
| `chousa` | 20 |
```

25 = 24 data rows + the `## By lane` summary (register line 238), which names no round and no id and is correctly
dropped: **zero chousa rows that name a round lack an S-id.** Ids, register order (lines 37–56, 269–272), no repeats:
S077 S080 S082 S084 S086 S088 S093 S094 S095 S096 S104 S105 S108 S110 S111 S112 S114 S116 S120 S125, S100 S101 S102
S103. Two shape facts matter downstream: line 238 still says `chousa 20` against a 24-row slice, so round-42's
`stale-summary` finding (`corpus/lessons/round-42.md:83`) reproduces unchanged; and S100–S103 sit in the five-column
`## Rows whose quotes were NEVER CHECKED` table with a stray trailing backtick in the id cell (`S100``), tolerated only by `re.search(r"S[0-9]+", …)`.

## 2. The frozen counter's quarantine line — 0/0

```
$ cd /home/vgpnk/Projects/shokunin/chousa-shokunin && TMPDIR=<scratch> python3 corpus/evidence/round53/c2-count.py | grep QUARANTINE
QUARANTINE_VERDICTS=0/0 ()
QUARANTINE_BLOCKED_ADOPTED=0
```

Mechanism read from the counter: `reg_ids` fills only from rows with `len(f)>6`, `` `chousa` `` in `f[1]` and `f[5]`
normalising into the five-URL theme set (`c2-count.py:252-259`); verdicts come only from `corpus/lessons/round-53.md`,
which **does not exist yet** (`ls` → `No such file or directory`), so `lesson = ""` (`c2-count.py:169`). The `0/0` is
two zeros — no theme row found, no lesson to read verdicts from; C2's rule is vacuous at the freeze, live when written.

## 3. Verifying the 0 independently

Hosts, `grep -c` over the whole register (any lane, any spelling), all zero: `jmla.pitt.edu 0`, `training.cochrane.org 0`,
`bjhea.org.cn 0`, `pharmwyp.com 0`; looser fragments `pitt.edu 0`, `cochrane 0`, `bjhea 0`, `pharmwyp 0`, `nmpa 0`, `jmla 0`, `20190618 0`, `1449/2061 0`, `chapter-04 0`, `1736907153935975 0`, `1126.html 0`.

Staged ids (`grep -cow`): `S134` 2, `S185` 1, `S193` 1, `S195` 2, `S186` 0, `S190` 0 — every hit another lane's row on
another URL: line 88 `kake` github, 90 `kake` github, 117 `kotoba` docs.roocode.com, 142 `mado` mirror.sjtu.edu.cn, 192 `tabi` developer.chrome.com, 365 `tameshi` doi.org/10.1145/351240.351266. None is `chousa`.

Shape- and spelling-independent scan over every `| \`` row (325, both tables), normalising first — scheme stripped,
leading `www.`/`m.` stripped, percent-encoding decoded on both sides, query and trailing `/` removed, host
lower-cased — then equality or prefix either way against each theme URL and its host+path key:

```python
def norm(u):
    u = urllib.parse.unquote(u.strip().strip("`<>()[] "))
    u = re.sub(r"^[a-zA-Z]+://", "", u); u = re.sub(r"^(www\.|m\.)", "", u)
    return u.rstrip("/").lower()
```

Observed: `register rows: 325` / `normalized theme hits: 0` — independent of table shape and of which cell holds the
URL, so it closes §4's blind spots. Liveness control: the round-51 counter on the same register prints
`QUARANTINE_VERDICTS=6/6 (S104,S105,S111,S112,S114,S120)` — the sweep is not hard-wired to zero; the round-53 URL set yields 0.

## 4. How the sweep's zero could be false — measured, and not so here

Replayed the counter's own parse (`url_of`, `DOCS`, `ALIASES` imported from `c2-count.py`, unmodified), one synthetic
row per case:

| probe | detected |
|---|---|
| theme row in the 7-column `## Rows` shape | `{'S900': 'https://training.cochrane.org/handbook/current/chapter-04'}` |
| same row in the 5-column never-checked shape | `{}` |
| NMPA URL percent-decoded | `False` (frozen percent-encoded form: `True`) |
| notice `m.bjhea` → `www.bjhea` | `False` |
| Cochrane `?x=1` query suffix | `False` |
| notice `http`→`https`, PDF trailing `/`, JMLA upper-case host | `True` |

`url_of` (`c2-count.py:103-110`) strips scheme, trailing `/` and fragment, lower-cases only the host, and leaves
percent-encoding and query intact — hence the four `False`/miss rows. All moot today: §3 normalises exactly those
dimensions and still returns 0, and no row of either shape contains any of the hosts.

## 5. Verdicts for the 24 slice rows

`grep -rn 'register S[0-9]* (round' corpus/lessons` — 7 matches, 6 distinct ids:

```
round-51.md:78  register S104 (round 3) verdict: absent-as-written
round-51.md:80  register S105 (round 3) verdict: absent-as-written
round-51.md:82  register S111 (round 4) verdict: present
round-51.md:84  register S112 (round 4) verdict: absent-as-written
round-51.md:86  register S114 (round 4) verdict: absent-as-written
round-51.md:88  register S120 (round 5) verdict: present
round-52.md:72  register S120 (round 5) verdict: present   # supersedes S120's char 39411 (round-52.md:15)
```

The round-52 lesson verdicts **1 of 24** slice rows (S120). The others are not un-adjudicated: `corpus/lessons/round-48.md:42-65`
is a table over the identical 24 ids (set equality checked: `slice minus r48: []`, `r48 minus slice: []`), tally
`15 present / 8 absent-as-written / 1 present — disputed` (round-48.md:67 counts S093 as present — "16 present … 8
absent-as-written, 0 unverifiable"). Re-derivations: round-49.md:111 S082, :115 S084, :118 S086, :122 S095, :124 S096 (absent-as-written); round-47.md:205 S093, :206 S094, :207 S108, :208 S110 (present); round-46.md:263 S116 present.

**Slice rows with no canonical `register S… verdict:` line in any lesson: 18** — S077 S080 S082 S084 S086 S088 S093
S094 S095 S096 S100 S101 S102 S103 S108 S110 S116 S125. **Slice rows with no verdict statement anywhere: 0.**
Contradictions across lessons (C2 reads verdict text):

- S104: round-48.md:52 `present` vs round-51.md:78 `absent-as-written`; S114: round-48.md:58 `present` vs
  round-51.md:86 `absent-as-written`.
- S086: round-48.md:46 `present` (companion capture) vs round-49.md:118 `absent-as-written` for the *cited homepage*
  — round-49 says "Not fabricated": scope, not contradiction.
- S077: round-42-verifier-spotcheck.md:120 `unverifiable` (265-char bot wall) superseded by round-48.md:42 `present`,
  "this is not `unverifiable`".

No such id is in the round-53 theme set, so no flip can fire `QUARANTINE_BLOCKED_ADOPTED` this round. But `VERDICT_RE`
(`c2-count.py:93`) reads **only** round-53.md: copying S077's old `unverifiable` line into the lesson would fail C2 the
moment S077 entered the theme set.

## VERDICT

Attacked the frozen sweep's negative: slice re-counted at 24 rows with zero ids missing, `QUARANTINE=0/0` and
`QUARANTINE_BLOCKED_ADOPTED=0` reproduced, and the 0 re-grounded across all 325 register rows under
scheme/`www.`/`m.`/percent-encoding/query/trailing-slash normalisation (0 hits; 0 occurrences of any theme host, and 0
of the six staged ids on a theme URL); the sweep's zero is shape- and spelling-conditional in four measured ways, the
independent scan is not — 18 of 24 rows lack the canonical verdict line, none is un-adjudicated, and S104, S114 and
S077 carry contradicting verdicts across lessons.
