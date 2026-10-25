# ExecPerturbHeld — R49 W2: held-row mapping probe (assimilate-rows.py)

Item attacked: `tools/assimilate-rows.py` held-row path — "a staged row whose URL
(the census's normalised first http(s) URL of the `source` cell) a Registry row
already carries maps to that row's id (`held`, nothing appended)" must map `held`
exactly when the census `url_of()` calls them equal. Probe: scratch registry from
`git show 414a2ec…:corpus/SOURCES.md` (S001–S095), staged rows whose source URL
differs from an existing registry URL only by scheme / trailing slash / fragment /
host case, plus query-string and path-case variants the census treats as different.
No installs (RULES: none needed; pacman paused). All scratch in
`/dev/shm/chousa-r49-ExecPerturbHeld`; nothing written to the lane except this report.

## 1. Normaliser parity (census awk vs tool Python)

Census `url_of()` = `scripts/sources-census.sh:600-605`
(awk: match `https?://[^[:space:]|]+`; strip `#[^ ]*$`, one trailing `/`, scheme
`^[A-Za-z]+://`; lowercase host before first `/`).
Tool = `tools/assimilate-rows.py:65-73` (same regex/steps, `u.find("/")`).

Verbatim census function run via gawk 5.4.1 over every probe URL (`awk_urlof.awk`):

```
S003-reg	[hapgood.us/2019/06/19/sift-the-four-moves]
S004-reg	[www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24]
S900	[hapgood.us/2019/06/19/sift-the-four-moves]
S901	[hapgood.us/2019/06/19/sift-the-four-moves]
S902	[hapgood.us/2019/06/19/sift-the-four-moves]
S903	[hapgood.us/2019/06/19/sift-the-four-moves]
S908	[hapgood.us/2019/06/19/sift-the-four-moves]
S904	[]
S905	[www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24?print=true]
S906	[www.cochrane.org/Authors/handbooks-and-manuals/handbook/current/chapter-24]
S907	[www.bmj.com/content/372/bmj.n71]
S909	[www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24?print=true]
```

Tool's `renumber.tsv` url column equals these strings on every row (below).
Implementation parity holds on all probes.

## 2. Probe run (staged S900–S909; registry S001–S095)

`python3 tools/assimilate-rows.py --staged $T/staged.md --knowledge $T/kn \
 --registry $T/SOURCES-base.md --opened 2026-10-25 --out $T/out --entry entry.md`

```
COLLISIONS=0
CITED=9 APPEND=3 HELD=6
exit=0
```

`renumber.tsv` (full):

```
staged_id	lane_id	action	url
S900	S003	held	hapgood.us/2019/06/19/sift-the-four-moves
S901	S003	held	hapgood.us/2019/06/19/sift-the-four-moves
S902	S003	held	hapgood.us/2019/06/19/sift-the-four-moves
S903	S003	held	hapgood.us/2019/06/19/sift-the-four-moves
S905	S096	append	www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24?print=true
S906	S097	append	www.cochrane.org/Authors/handbooks-and-manuals/handbook/current/chapter-24
S907	S098	append	www.bmj.com/content/372/bmj.n71
S908	S003	held	hapgood.us/2019/06/19/sift-the-four-moves
S909	S096	held	www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-24?print=true
```

Case-by-case:

| staged | variant of S003/S004 URL | census norm == registry norm? | action | exact |
|---|---|---|---|---|
| S900 `http://` (scheme) | yes | `held S003` | ✓ |
| S901 no trailing slash | yes | `held S003` | ✓ |
| S902 `#the-four-moves` (fragment) | yes | `held S003` | ✓ |
| S903 `HAPGOOD.US` (host case) | yes | `held S003` | ✓ |
| S908 `http://HAPGOOD.US` + no slash (combined) | yes | `held S003` | ✓ |
| S905 `?print=true` (query) | no | `append S096` | ✓ |
| S906 `/Authors/` (path case) | no | `append S097` | ✓ |
| S907 fresh URL, not in registry | no | `append S098` | ✓ |
| S909 same URL as S905 (staged-staged dup) | n/a (staged dup) | `held S096` | ✓ |

`append.md` holds exactly S096–S098 (held rows append nothing). Entry substitution:
S900/S901/S902/S903/S908→S003, S905→S096, S906→S097, S907→S098, S909→S096
(verified in `out/entry.md`).

## 3. Uppercase-scheme case (first run, S904)

Staged source `HTTPS://www.cochrane.org/…` (scheme case):

```
COLLISIONS=0
REFUSED S904: staged row names no http(s) URL
exit=1
```

Census awk also returns `""` for it (`S904 []` above): the census regex
`https?://` is case-sensitive, so `HTTPS://` is not a recognizable URL at all —
there is no "equal" census-URL to compare. The tool refuses the cited row with no
URL (docstring line 37-38) instead of appending; URL-recognition semantics match
the census on both sides. (Scheme *lowercase* difference S900 is the equality case.)

## 4. Calibration note — duplicate registry-URL pairs

S019 and S029 share the identical URL `https://www.cochrane.org/authors/handbooks-and-manuals/handbook/current/chapter-iv` (SOURCES-base.md lines 29 and 39; same for S021/S030, S024/S031). Held dict is built `held.setdefault(u, sid)` iterating ascending id, so the earliest row wins. Verified with staged S910 (same URL): action `held S019` (not S029). Deterministic and documented ("two staged rows for one URL map to one lane id"), but a staged row matching a superseded pair's URL is held to the older superseding source (S019 supersedes S019→S029 chain: S019 < S029). This is a calibration behavior to be aware of, not a mismatch: the census itself treats the pair as one URL identity.

## 5. Conclusion

All seven held mappings (S900–S903, S908, S909, S910) fired exactly when the
verbatim census `url_of()` normals equaled an existing registry-URL normal, and
all three appends fired exactly when they differed; no mismatch between census
equality and tool action on any probe. Uppercase-scheme URLs are refused as
URL-less by both implementations.

VERDICT: assimilate-rows.py held-row mapping — holds — on every probe the tool maps held exactly when the census url_of() normalisation calls the URLs equal and appends exactly when it calls them different, with the only caveats being documented behaviors (earliest-wins for duplicate registry URLs; URL-less uppercase-scheme rows refused by both sides).
