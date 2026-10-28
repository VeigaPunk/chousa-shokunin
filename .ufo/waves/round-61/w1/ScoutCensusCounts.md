# ScoutCensusCounts — round 61 before-census

Named revision `2b0e17b2a3b20a5f350e4dc4ddd5900c4d1f952c` (ancestor of worktree HEAD `9f32ac055c591b17abf119aac30b202d6cd52a7e`, the wave-spec commit). `corpus/SOURCES.md` is blob `1dce476b312336c5e89b71602d5716f8b4eaa98a` at both. `git diff --stat 2b0e17b2a3b20a5f350e4dc4ddd5900c4d1f952c HEAD -- corpus/SOURCES.md corpus/knowledge` printed nothing. `claims.md` sha256 `9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec`. Census `date -u` was `2026-10-28`. No install.

## Before (observed)

133 registry rows, ids S001–S133, 0 gaps. S134–S137 are absent. Zero indented S-rows, so the column-zero awk block and `sources-census.sh` agree.

| metric | before |
|---|---|
| rows | 133 |
| tier A / B / C | 106 / 22 / 5 |
| status mined / queued / rejected | 109 / 19 / 5 |
| malformed NF!=13 | 0 |
| duplicate ids | none |
| enum / tier-inflation | none |
| mined used-by missing on disk | none |
| `corpus/knowledge/*.md` | 82 |
| of those, `recheck:` line | 78 |
| `corpus/knowledge/derived-output-safety-r61.md` | absent |

`validate` exit 0. Five W04 warnings (they do not change the ok line):

```
chousa	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

Knowledge files with no `^[-* ]*recheck *:` line: `gate-baseline-r8.md`, `archives-verified-r9.md`, `audit-r11.md`, `dead-zone-pcre-r34.md`. A `recheck:` substring sweep also returned 78.

## Projected after — compare this table to the real after-census

Append S134–S137 as in `corpus/evidence/round61/controls/c2-positive-rows.txt` (each line NF=13) and add `corpus/knowledge/derived-output-safety-r61.md`. Observed cells: S134 docs A mined; S135 docs A mined; S136 own-work B mined; S137 own-work C rejected. Mined `used-by` is that entry path. S137 `used-by` is `—`. Row `recheck` cells are `on-release`, `on-release`, `180d`, `180d`. The positive entry's third line is `recheck: on a man-pages release, …` (column 0; matches the sweep).

| metric | before | projected after |
|---|---|---|
| rows | 133 | 137 |
| tier A | 106 | 108 |
| tier B | 22 | 23 |
| tier C | 5 | 6 |
| mined | 109 | 112 |
| queued | 19 | 19 |
| rejected | 5 | 6 |
| malformed | 0 | 0 |
| duplicate ids | none | none (S134–S137 absent now; S001–S133 have no gaps) |
| enum / tier-inflation | none | none (kinds docs/own-work, tiers A/B/C, statuses mined/rejected) |
| mined used-by missing | none | none once the entry file is on disk |
| knowledge `*.md` | 82 | 83 |
| `recheck:` entries | 78 | 79 |
| W04 | the five lines above | the same five lines |
| validate exit | 0 | 0 |

Arithmetic on the observed before histograms plus those four cells gives A 106→108, B 22→23, C 5→6, mined +3, rejected +1, queued unchanged. Malformed stays 0 because each positive row has NF=13.

INFERENCE (joint landing only): W04 is unchanged and validate stays exit 0. `url_of` in `scripts/sources-census.sh` keeps only `https?://` URLs, and `grep -E 'https?://'` on the positive rows printed nothing, so those four rows add no W04 and no E04. `symbolic()` is `^[A-Za-z][A-Za-z0-9 _-]*$`, so `on-release` is a legal recheck; `180d` matches `^[0-9]+d$`. Opened `2026-10-28` is not a future date on this run. E11 fires for S134–S136 if the rows land while `corpus/knowledge/derived-output-safety-r61.md` is still absent (validate would then exit 1). The exit-0 row above is the state where the entry file exists beside the four rows.

Single-lane `census` mode printed the same 133 / 106 / 22 / 5 / 109 / 19 / 5, and `FLEET.tier.invalid=0`, `FLEET.status.invalid=0`, `FLEET.missing=0`.

## Evidence

Lane for the awk block: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.

`git -C "$LANE" rev-parse --verify 2b0e17b2a3b20a5f350e4dc4ddd5900c4d1f952c` → that hash. `git -C "$LANE" rev-parse HEAD` → `9f32ac055c591b17abf119aac30b202d6cd52a7e`. `merge-base --is-ancestor` succeeded. `git diff --stat` on `corpus/SOURCES.md` and `corpus/knowledge` was empty. Both `REV:corpus/SOURCES.md` and `HEAD:corpus/SOURCES.md` are `1dce476b312336c5e89b71602d5716f8b4eaa98a`. `sha256sum` of `corpus/evidence/round61/claims.md` → `9afec8d493f0ba511a256f38cd5098ff508f9ed311c6c49ff5383add9ce0acec`.

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa` → exit 0, the six lines in the W04 block.

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin chousa` → exit 0:

```
chousa	rows	133
chousa	tier.A	106
chousa	tier.B	22
chousa	tier.C	5
chousa	status.mined	109
chousa	status.queued	19
chousa	status.rejected	5
FLEET	rows	133
FLEET	tier.A	106
FLEET	tier.B	22
FLEET	tier.C	5
FLEET	tier.invalid	0
FLEET	status.queued	19
FLEET	status.mined	109
FLEET	status.rejected	5
FLEET	status.invalid	0
FLEET	missing	0
```

CORPUS.md manual block (from the lane), observed:

- `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `133`
- indented S-rows `^ {1,3}\|…` → `0`
- malformed awk (`NF!=13`) → `0`
- tier awk → `A=106 B=22 C=5`
- status awk → `mined=109 queued=19 rejected=5`
- duplicate-id awk → empty
- enum / tier-inflation awk → empty
- mined used-by existence loop → empty
- id-span awk → `max 133 gaps 0`
- S134–S137 filter → empty

`find /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge -name '*.md' | wc -l` → `82`. `grep -rlE '^[-* ]*recheck *:' --include='*.md' corpus/knowledge | wc -l` → `78`. `grep -rlF 'recheck:' --include='*.md' corpus/knowledge | wc -l` → `78`. The entry path test printed `ABSENT`.

Positive rows: `awk -F'|' '/S13[4-7]/{print NR, "NF=" NF}'` → `1 NF=13` through `4 NF=13`. `grep -E 'https?://'` → no match. Cell awk → `S134 docs A mined`, `S135 docs A mined`, `S136 own-work B mined`, `S137 own-work C rejected`.

This seat did not run `c1-count.py` or `c2-count.py`.

VERDICT: BEFORE_ROWS=133 PROJECTED_AFTER=137
