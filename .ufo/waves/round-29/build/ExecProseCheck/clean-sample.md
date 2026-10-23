# Clean synthetic sample

Prose with separated digits: all 69 seats, 64 proposals, on 2026-10-21, at most
25 words. No digit-glued token appears outside the exclusions below.

Excluded identifier forms, which must not be flagged:

- `sha256` and `sha1` digests, `md5`, `base64`, `utf8`
- `x86`, `arm64`, `ipv4`, `ipv6`
- heading anchors `h1` through `h6`
- source ids S046, S047, S048, S049 and round ids r29, r44

Inside a fenced block the following must not be flagged:

```
all69 proposal64 original187 legacy161 diagnosis53 on2026-10-21 at most25 words
```

A URL must not be flagged either: https://example.org/all69/proposal64

No custody vocabulary appears in this file, so the checker must exit 0.
