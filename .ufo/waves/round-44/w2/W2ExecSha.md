# W2ExecSha

Seat: executor. Milestone: Round 44 wave 2: genuine seats after the usage-error wave.
Axes: operability, calibration, depth.
No network. No fetch. Production files not edited.

## Result

CONFIRMED. The RFC capture filename is the first 24 hex digits of SHA-256 of the URL string, with no trailing newline.

Paste both:

- URL (42 ASCII bytes): `https://www.rfc-editor.org/rfc/rfc7089.txt`
- SHA-256 (64 hex): `d0c4a09a9de32cb91d5e37971b546f2c380d0a60581c6bb80fb9ef72d97743d0`
- first 24 hex digits: `d0c4a09a9de32cb91d5e3797`
- capture filename: `d0c4a09a9de32cb91d5e3797.txt`

Path that exists:

`/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt`

## Commands (quoted)

`printf '%s' 'https://www.rfc-editor.org/rfc/rfc7089.txt' | sha256sum`:

```
d0c4a09a9de32cb91d5e37971b546f2c380d0a60581c6bb80fb9ef72d97743d0  -
```

`printf '%s' 'https://www.rfc-editor.org/rfc/rfc7089.txt' | openssl dgst -sha256`:

```
SHA2-256(stdin)= d0c4a09a9de32cb91d5e37971b546f2c380d0a60581c6bb80fb9ef72d97743d0
```

`python3` `hashlib.sha256(url.encode()).hexdigest()` (UTF-8; the URL is ASCII, so the encoding choice does not change the bytes):

```
bytes 42
sha256 d0c4a09a9de32cb91d5e37971b546f2c380d0a60581c6bb80fb9ef72d97743d0
prefix24 d0c4a09a9de32cb91d5e3797
filename d0c4a09a9de32cb91d5e3797.txt
```

`repr` of the hashed bytes:

```
b'https://www.rfc-editor.org/rfc/rfc7089.txt'
```

Three implementations agree. The prefix is exactly the filename stem.

## On-disk name

`stat -c '%n size=%s mtime=%y'`:

```
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt size=107130 mtime=2026-10-23 20:33:05.526350588 -0300
/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.raw size=107130 mtime=2026-10-23 20:33:05.524186651 -0300
```

Glob of that prefix under `.qcache` returned only those two names. `exact_txt True`. `exact_fail False`. `cmp` of `.txt` and `.raw` exited 0 (byte-identical for this text capture). The frozen capture name is the `.txt`. The `.raw` is the same stem, not a second URL key.

Content SHA-256 of the `.txt` is not the filename key:

```
c3c7b7f2c495dce0fad758dac34dcc1eef3623d13c9ef346e19b30dbbbe801dc  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/d0c4a09a9de32cb91d5e3797.txt
```

## Same construction in the counters

`quote-lint.py` names the cache from the URL, not from the body:

```
def cache_path(url: str) -> pathlib.Path:
    return CACHE / (hashlib.sha256(url.encode()).hexdigest()[:24] + ".txt")
```

(`quote-lint.py:437-438`, cache dir `.qcache` at line 48.)

`c3-count.py` uses the same URL constant and the same slice:

```
URL = "https://www.rfc-editor.org/rfc/rfc7089.txt"
...
key = hashlib.sha256(URL.encode()).hexdigest()[:24]
capture = CACHE / (key + ".txt")
```

(`c3-count.py:29` and `:59-60`.) That key is `d0c4a09a9de32cb91d5e3797`.

Frozen claim text already states the construction (`corpus/evidence/round44/claims.md:99-101`): the quote is a contiguous substring of capture `d0c4a09a9de32cb91d5e3797.txt` (sha256 of the URL, first 24 hex digits). This seat recomputed the hash; it did not copy the claim as the check. The claim was not retuned.

## Calibration

A trailing newline does not produce this filename. `printf '%s\n' URL | sha256sum`:

```
cdab110644b2203ea5e8946611cecdf44bbf1dca5be305cb180c9127cc22ca1e  -
```

Other near-miss inputs also fail (`match_file False` for each):

| input | first 24 |
| --- | --- |
| URL + newline | `cdab110644b2203ea5e89466` |
| URL + `/` | `468c44e2a94ceb3c2b4bc6f8` |
| `http://` instead of `https://` | `89df0605f81b2cc896ee7dd6` |
| URL without `.txt` | `5c0da30bdd73c5c270ed9b38` |
| URL + trailing space | `fa6ce000c5a3c6e50486fa75` |
| uppercased URL | `673c8a0737171780d7d93cdb` |

What this confirms: the on-disk stem is the URL key used by `cache_path` and `c3-count.py`. What it does not confirm: that the file bytes are RFC 7089 (that is a content check, not a name check), that the file is fresh for this round (mtime is 2026-10-23 20:33 -0300, before this round's date 2026-10-24), or that a quote offset inside the file holds. Freshness stays unchanged. No fetch was run.
