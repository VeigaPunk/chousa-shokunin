# ExecCaptureSha

Verdict: **MATCH**.

Axes: operability (file readable, both hashers exit 0), calibration (byte-identical to the claimed digest), depth (independent hasher plus filename/URL identity; git-track status recorded, not used to retune the digest claim).

## Files changed

- `.ufo/waves/round-43/w1/ExecCaptureSha.md` (this report only).
- No lane production file, git index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` path was modified.

## Behavior

Read-only `sha256sum` and `hashlib.sha256` of the campaign capture. No fetch. No shokuknow tool.

Path: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt`

Claimed digest: `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d`

Measured digest: `833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d`

Match: yes.

## Exact evidence

```
$ sha256sum /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt
833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/2cef078d8f9f87802e19e770.txt
```

```
$ stat -c 'size=%s inode=%i links=%h type=%F mtime=%y' <same path>
size=80107 inode=124013161 links=1 type=regular file mtime=2026-10-23 20:40:06.022034917 -0300
```

```
$ python3 hashlib.sha256(path.read_bytes())
bytes 80107
sha256 833b13e3e80212522d016a8db9c6edeacb8965148d2334722a7a73c415d7136d
match True
head b'<?xml version="1.0" encoding="UTF-8"?><article xml:lang="en" article-type="other"><front><journal-meta><journal-id journ'
```

Filename identity (local, no fetch). SHA-256 of `https://www.ebi.ac.uk/europepmc/webservices/rest/PMC6148622/fullTextXML` is `2cef078d8f9f87802e19e770ad526d3b44fc72184224db4217de1bb94f5f0ce8`. First 24 hex digits equal the capture filename.

Same digest is written in `corpus/knowledge/search-log-method-r39.md` line 26, `corpus/lessons/round-43.md` line 37, and `corpus/SOURCES.md` S078.

## Remaining risks

- The file is gitignored in shokuknow (`.gitignore:5:.ufo/waves/corpus-expansion-1/.qcache/`). `git ls-files -s` returned empty; `git status --porcelain` returned empty; HEAD was `8b94c5c1`. The digest is of on-disk bytes, not of a git blob. "Committed" here means the campaign cache file the lane already cites, not a shokuknow commit object.
- mtime is 2026-10-23 20:40:06 -0300. A later overwrite of those 80107 bytes would change the digest. This report does not pin the inode.
- Head bytes show Europe PMC article XML, not a bot wall. Quote location and byte offset 17383 were not re-checked in this seat.

## Blockers

None.
