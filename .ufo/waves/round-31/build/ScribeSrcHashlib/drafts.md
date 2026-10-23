# S059 draft — Python hashlib

## SOURCES row

| S059 | Python hashlib documentation — https://docs.python.org/3/library/hashlib.html | docs | A | Python hashlib's SHA-256 digest and hexadecimal representation for bytes fed to a hash object; not a general SHA-256 text-encoding standard, lowercase-output requirement, or the lane's revision-pin contract | `Hash algorithms` and `Hash Objects`: `hashlib.hash.digest_size`, `.update()`, `.digest()`, `.hexdigest()`; Python 3.15.1 documentation, page as served 2026-10-23 | A `sha256()` object digests the concatenation of data fed through `update()`; `hexdigest()` returns a string twice the digest's byte length with hexadecimal digits, but the docs do not specify output letter case | mined | 2026-10-23 | on-release | corpus/knowledge/revision-binding-r31.md |

Tier reason: A because official Python documentation is authoritative for the `hashlib` API behavior in this narrowly stated scope; it is not authority for a lowercase-hex requirement.

## Gate-table line

| URL | Quote | Verdict |
|---|---|---|
| https://docs.python.org/3/library/hashlib.html#hashlib.hash.hexdigest (opened 2026-10-23) | “Like digest() except the digest is returned as a string object of double length, containing only hexadecimal digits.” | Admit S059 as scoped API support: the page specifies hex digits and length relative to the digest, but does not require lowercase (its lowercase examples are examples, not a stated case rule). |

## Raw quote context (the two sentences in the `hashlib.hash.hexdigest` paragraph)

> Like digest() except the digest is returned as a string object of double length, containing only hexadecimal digits.
>
> This may be used to exchange the value safely in email or other non-binary environments.

The preceding `Hash algorithms` section says `sha256()` creates a SHA-256 hash object, accepts bytes-like input through `update()`, and exposes the digest of the concatenated data fed so far through `digest()` or `hexdigest()`. The `Hash Objects` section calls `digest_size` a constant attribute and defines it as the resulting hash size in bytes. The page's lowercase SHA-256 examples do not state that output must be lowercase.

## Opened-body evidence

One GET to https://docs.python.org/3/library/hashlib.html; HTTP 200; body 121,928 bytes; SHA-256 `553f4f2a9e686e6f051c8b12bd5469e7fdd6cc7116b2f6d2beba68c1a703af10`. Captured body and response headers are `response.body` and `response.headers` beside this draft.
